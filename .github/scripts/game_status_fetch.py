#!/usr/bin/env python3
"""GitHub Actions: fetch Polymarket game/series status -> intel/*.json.

云端每 5 分钟运行（服务器在首尔直连 Polymarket 被 451 限制，GitHub 美国节点
不受限）。输出：
  intel/game_status.json   每场 Game/Map Winner 市场状态（供流水线按小局出节点）
  intel/settlements.json   系列赢家结算（供服务器回填比赛结果）
  data/matches_today.json  今日比赛清单（Polymarket + 虎扑补漏）
  data/watchlist_events.json
提交到仓库 data 分支；服务器发布时拉取合并。

2026-10-25 云扫修复：① 白名单补 Worlds/全球总决赛（此前世界赛瑞士轮全部被
过滤，导致 10-14 起历史库停更）；② 新增虎扑赛程合并（CS2 全部 + 官方 Riot
未覆盖的 LoL），补 Polymarket 未挂牌场次。虎扑抓取失败仅降级为 Polymarket 结果，
不阻断工作流。
"""

from __future__ import annotations

import datetime
import json
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "Mozilla/5.0 danmu-intel"}


RETRY_CODES = {429, 500, 502, 503, 504}


def get(url: str, attempts: int = 5):
    """带退避重试的 GET（2026-10-11 固化）。

    教训：Polymarket gamma 偶发 500/超时，原实现直接抛出 -> 工作流失败 ->
    每 5 分钟一封 GitHub 失败邮件。上游瞬时故障必须自行重试吸收；
    仅对可重试错误（5xx / 429 / 网络超时）退避重试，其余 4xx 立即抛出。
    """
    last: Exception | None = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            last = e
            if e.code not in RETRY_CODES:
                raise
        except Exception as e:  # noqa: BLE001 超时/连接重置/响应截断
            last = e
        if i < attempts - 1:
            time.sleep(min(2 ** i, 8) + random.uniform(0, 0.4))
    raise last if last else RuntimeError(f"GET failed: {url}")


def norm_teams(title: str) -> list[str]:
    m = re.search(r":\s*(.+?)\s+vs\s+(.+?)\s*(?:\(|\-|$)", title or "", re.I)
    return [m.group(1).strip(), m.group(2).strip()] if m else []


def tracked(t: str) -> bool:
    """项目白名单联赛过滤（与 config/market_watchlist.json 口径一致）。"""
    if "LoL" in t or "League of Legends" in t:
        return any(
            k in t for k in (
                " LCK ", "LCK Challengers", " LPL ", " LCP ", " LEC ",
                "KeSPA Cup", "Kespa Cup", "K杯",
                # 世界赛（2026-10-25 补）：此前漏掉，导致世界赛瑞士轮全部被过滤
                "Worlds", "World Championship", "全球总决赛", "瑞士轮", "Swiss",
            )
        )
    if "Counter-Strike" in t:
        return any(k in t for k in ("IEM", "BLAST", "Esports World Cup", "EWC"))
    if "Dota" in t:
        return any(k in t for k in ("The International", "ESL One"))
    return False


def detect_format(title: str, markets: list[dict]) -> tuple[int, dict, bool]:
    """赛制识别 + Polymarket 内部多信号交叉校验（全部免费、无外部依赖）。

    三个信号（均为预测市场字段）：
      1. ou      Games Total O/U 市场最大值：0.5->BO1、2.5->BO3、4.5->BO5
                 （机器生成，最稳，作冲突时优先信号）
      2. title   标题 (BO\\d+) 标注（平台人工填写）
      3. games   小局 Winner 市场最大局数：仅取可区分值 G4->BO5、G2->BO3、G1->BO1
    结论：多数一致；不一致时以 O/U 为准并标记冲突，页面/流水线可据此显式标注。
    """
    ou_max = None
    max_g = 0
    for mk in markets:
        q = mk.get("question", "") or ""
        mm = re.search(r"Games Total: O/U ([\d.]+)", q)
        if mm:
            v = float(mm.group(1))
            ou_max = v if ou_max is None or v > ou_max else ou_max
        mm = re.search(r"(?:Game|Map)\s*(\d+)\s*Winner", q, re.I)
        if mm:
            max_g = max(max_g, int(mm.group(1)))
    fmt_ou = {0.5: 1, 1.5: 3, 2.5: 3, 3.5: 5, 4.5: 5}.get(ou_max)
    mm = re.search(r"BO\s*(\d+)", title or "", re.I)
    fmt_title = int(mm.group(1)) if mm else None
    fmt_games = {4: 5, 2: 3, 1: 1}.get(max_g)
    sources = {"ou": fmt_ou, "title": fmt_title, "games": fmt_games}
    cands = [v for v in (fmt_ou, fmt_title, fmt_games) if v and 1 <= v <= 5]
    if not cands:
        fmt, conflict = 5, True
    else:
        cnt: dict[int, int] = {}
        for v in cands:
            cnt[v] = cnt.get(v, 0) + 1
        fmt, n = max(cnt.items(), key=lambda kv: (kv[1], -abs(kv[0] - 5)))
        conflict = n < len(cands)
        if conflict and fmt_ou:
            fmt = fmt_ou
    return fmt, sources, conflict


def scan_candidates(backfill_from: str, horizon: str) -> dict[str, dict]:
    """用 Esports 标签（tag_id=64）精准拉电竞事件候选（避免被加密货币小时盘刷屏）。

    2026-08-25 固化：只保留近 3 天 + 今明两天开赛的候选（同市场扫描器口径）。
    2026-08-27：archived=false（进行中/未开始）+ archived=true（已结束归档）
    两批都要，否则已结束的今天场次会从今日页消失（教训：08-27 CS2 缺场次）。
    """
    candidates: dict[str, dict] = {}
    for arch in ("false", "true"):
        for off in range(0, 8):
            evs = get(
                "https://gamma-api.polymarket.com/events?tag_id=64"
                "&archived=%s&startDateMin=%s&startDateMax=%s&limit=100&offset=%d&order=startDate&ascending=false" % (arch, backfill_from, horizon, off * 100)
            )
            if not evs:
                break
            for e in evs:
                tt = e.get("title") or ""
                if not tracked(tt):
                    continue
                slug = e.get("slug") or ""
                mm = re.search(r"-(\d{4}-\d{2}-\d{2})$", slug or "")
                sd = mm.group(1) if mm else ""
                if sd and backfill_from <= sd <= horizon:
                    candidates[slug] = {"title": tt, "date": sd, "teams": norm_teams(tt)}
    return candidates


# ---- 虎扑赛程源（2026-10-25 补：CS2 全部 + 官方 Riot 未覆盖的 LoL）----

HUPU_API = (
    "https://match-api.hupu.com/1/8.2.10/matchallapi/bff/standard/"
    "getScheduleListByTagForH5"
)
HUPU_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 "
        "Safari/604.1"
    ),
    "Accept": "application/json, text/plain, */*",
}
HUPU_BUSINESSES = {"lol": "LoL", "cs2": "CS2"}
# 官方 Riot 已覆盖（由 Polymarket / 官方赛程源处理）的 LoL 联赛 + 世界赛
_HUPU_LOL_SKIP_KEYS = (
    "lck", "lpl", "lec", "lcp",
    "全球总决赛", "world championship", "worlds", "瑞士轮", "swiss",
)


def _hupu_iso(ms) -> str:
    if ms in (None, ""):
        return ""
    try:
        dt = datetime.datetime.fromtimestamp(int(ms) / 1000, tz=datetime.timezone.utc)
        return dt.isoformat(timespec="seconds").replace("+00:00", "Z")
    except (ValueError, TypeError, OSError):
        return ""


def _hupu_bj_date(ms) -> str:
    iso = _hupu_iso(ms)
    if not iso:
        return ""
    try:
        return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(
            datetime.timezone(datetime.timedelta(hours=8))
        ).date().isoformat()
    except ValueError:
        return ""


def _normalize_hupu(raw: dict, business: str) -> dict | None:
    if raw.get("matchType") != "against":
        return None
    against = raw.get("againstInfo") or {}
    members = against.get("memberInfos") or []
    if len(members) != 2:
        return None
    mid = str(raw.get("matchId") or "")
    if not mid:
        return None
    status = str(raw.get("matchStatus") or "").upper()
    teams = [str(m.get("memberName") or "").strip() for m in members]
    if not all(teams):
        return None
    key = raw.get("scoreItemKey") or {}
    return {
        "league": HUPU_BUSINESSES[business],
        "hupu_match_id": mid,
        "tournament": str(raw.get("matchIntroduction") or raw.get("matchName") or "").strip(),
        "teams": teams,
        "start_iso": _hupu_iso(raw.get("matchStartTimeStamp")),
        "date": _hupu_bj_date(raw.get("matchStartTimeStamp")),
        "status": (
            "completed" if status == "COMPLETED"
            else ("inProgress" if status == "INPROGRESS" else "notStarted")
        ),
        "score_item_key": {
            "out_biz_no": str(key.get("outBizNo") or ""),
            "out_biz_type": str(key.get("outBizType") or ""),
        },
        "member_ids": [
            {"name": str(m.get("memberName") or "").strip(),
             "member_id": str(m.get("memberId") or "")}
            for m in members
        ],
    }


def fetch_hupu() -> list[dict]:
    """抓虎扑 LOL + CS2 赛程并归一化（网络失败抛错，由调用方降级）。"""
    out: list[dict] = []
    for b in HUPU_BUSINESSES:
        qs = urllib.parse.urlencode({
            "businessType": "common",
            "datasource": "navigation",
            "businessId": b,
        })
        req = urllib.request.Request(f"{HUPU_API}?{qs}", headers=HUPU_HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
        if not payload.get("success"):
            raise RuntimeError(f"hupu {b} api not success: {payload.get('errorCode')}")
        for day in payload.get("result", {}).get("dayGameData", []) or []:
            for raw in day.get("matchData", []) or []:
                item = _normalize_hupu(raw, b)
                if item is not None:
                    out.append(item)
    return out


def _team_norm(name: str) -> str:
    """队伍名归一化去重键（小写 + 去非字母数字，容忍 Gen.G/GEN、BC.Game/BCGame 等写法）。"""
    return re.sub(r"[^a-z0-9]", "", str(name or "").lower())


def _hupu_skip_lol(tournament: str) -> bool:
    t = (tournament or "").lower()
    return any(k in t for k in _HUPU_LOL_SKIP_KEYS)


def merge_hupu(rows: list[dict], today_matches: list[dict], bj_today: str, bj_tomorrow: str) -> int:
    """合并虎扑场次（CS2 全部 + 官方/世界赛未覆盖的 LoL），返回新增条数。

    与 tools/export_today_matches.py merge_hupu 同口径（2026-10-25 上云）：
    世界赛 / LCK / LPL / LEC / LCP 由 Polymarket（白名单已修复）覆盖，虎扑跳过；
    虎扑只补 CS2 + 其他 LoL（德玛西亚杯等）。按归一化队伍名去重。
    """
    known = {tuple(sorted(_team_norm(t) for t in (m.get("teams") or []))) for m in today_matches}
    added = 0
    for e in rows:
        league = str(e.get("league") or "").upper()
        if league == "CS2":
            game = "cs2"
        elif league == "LOL":
            if _hupu_skip_lol(e.get("tournament") or ""):
                continue
            game = "lol"
        else:
            continue
        teams = e.get("teams") or []
        if len(teams) != 2:
            continue
        hid = str(e.get("hupu_match_id") or "").strip()
        if not hid:
            continue
        # 只取今明两天（北京时间），与本地 export 同口径；跨日凌晨场次由 start_iso 归并
        if e.get("date") not in (bj_today, bj_tomorrow):
            continue
        tkey = tuple(sorted(_team_norm(t) for t in teams))
        if tkey in known:
            continue
        mid = f"{game}-hupu-{hid}"
        today_matches.append({
            "id": mid,
            "slug": mid,
            "official_match_id": "",
            "league": "CS2" if game == "cs2" else "LoL",
            "teams": teams,
            "start_time": e.get("start_iso") or "",
            "end_time": "",
            "closed": bool(e.get("status") == "completed"),
            "_hupu": True,
            "_hupu_tournament": e.get("tournament") or "",
            "hupu_score_out_biz_no": str((e.get("score_item_key") or {}).get("out_biz_no") or ""),
            "hupu_score_out_biz_type": str((e.get("score_item_key") or {}).get("out_biz_type") or ""),
            "hupu_member_ids": e.get("member_ids") or [],
        })
        known.add(tkey)
        added += 1
    return added


def main() -> None:
    today = datetime.date.today().isoformat()
    horizon = (datetime.date.today() + datetime.timedelta(days=2)).isoformat()
    backfill_from = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
    try:
        candidates = scan_candidates(backfill_from, horizon)
    except Exception as e:  # noqa: BLE001
        # 上游整体不可用：保留上一份数据，不让工作流失败
        # （2026-10-11 固化：失败邮件由上游瞬时 500 触发，数据自愈只需 5 分钟）
        print(f"::warning::Polymarket 扫描失败，保留上一份数据：{type(e).__name__}: {e}", flush=True)
        return

    games: dict[str, dict] = {}
    settlements: dict[str, dict] = {}
    today_matches: list[dict] = []
    watch_events: list[dict] = []
    slug_failures: list[str] = []
    for slug, meta in candidates.items():
        try:
            evs = get(f"https://gamma-api.polymarket.com/events?slug={slug}")
            if not evs:
                continue
            game_start = None
            for mk in evs[0].get("markets", []):
                gst = mk.get("gameStartTime") or mk.get("startDate") or mk.get("start_date")
                if gst:
                    game_start = gst
                    break
            # 赛制识别 + 内部交叉校验（2026-08-25 固化）：
            # O/U 市场 / 标题 BO 标注 / 小局市场数量 三信号一致才定论；
            # 冲突时以 O/U 为准并标记 conflict，页面显式提示"赛制待确认"。
            fmt, fmt_sources, fmt_conflict = detect_format(meta["title"], evs[0].get("markets", []))
            gs: dict[int, dict] = {}
            winner = None
            for mk in evs[0].get("markets", []):
                q = mk.get("question", "") or ""
                raw = mk.get("outcomePrices")
                try:
                    if isinstance(raw, str):
                        raw = json.loads(raw)
                    prices = [float(x) for x in (raw or [])]
                except (ValueError, TypeError, json.JSONDecodeError):
                    prices = []
                mm = re.search(r"(?:Game|Map)\s*(\d+)\s*Winner", q, re.I)
                if mm:
                    gi = int(mm.group(1))
                    wi = (
                        0 if len(prices) >= 2 and prices[0] >= 0.99
                        else (1 if len(prices) >= 2 and prices[1] >= 0.99 else None)
                    )
                    gs[gi] = {"closed": bool(mk.get("closed")), "prices": prices, "winner": wi}
                    continue
                # 系列赢家市场：slug 与事件相同（如 lol-drxc-foxy-2026-08-25）
                if mk.get("slug") == slug and len(prices) >= 2:
                    outs = mk.get("outcomes") or [None, None]
                    if isinstance(outs, str):
                        try:
                            outs = json.loads(outs)
                        except json.JSONDecodeError:
                            outs = [None, None]
                    winner = (
                        outs[0] if len(outs) >= 2 and prices[0] >= 0.99
                        else (outs[1] if len(outs) >= 2 and prices[1] >= 0.99 else None)
                    )
            if gs:
                games[slug] = gs
            if winner:
                settlements[slug] = {
                    "winner": winner,
                    "teams": meta["teams"],
                    "date": meta["date"],
                    "title": meta["title"],
                }
            if meta["date"] in (today, (datetime.date.today() + datetime.timedelta(days=1)).isoformat()):
                try:
                    start_dt = datetime.datetime.fromisoformat(str(game_start).replace("Z", "+00:00"))
                    end_dt = start_dt + datetime.timedelta(hours=6)
                except (ValueError, TypeError):
                    start_dt, end_dt = None, None
                league = "LoL" if "LoL" in meta["title"] else ("CS2" if "Counter-Strike" in meta["title"] else "Dota2")
                today_matches.append({
                    "id": slug, "league": league, "teams": meta["teams"],
                    "start_time": start_dt.isoformat() if start_dt else game_start,
                    "end_time": end_dt.isoformat() if end_dt else "",
                    "closed": False,
                    "format": fmt,
                    "format_sources": fmt_sources,
                    "format_conflict": fmt_conflict,
                })
                watch_events.append({
                    "title": meta["title"], "slug": slug,
                    "start_time": start_dt.isoformat() if start_dt else game_start,
                    "end_time": end_dt.isoformat() if end_dt else "",
                    "time_status": "upcoming_within_window",
                })
        except Exception as e:  # noqa: BLE001 单场失败不拖垮整轮（下轮重试）
            slug_failures.append(f"{slug}({type(e).__name__})")
            continue
        time.sleep(0.3)

    # 虎扑补漏（2026-10-25）：CS2 全部 + 官方/世界赛未覆盖的 LoL；失败仅降级，不阻断
    bj_now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)
    bj_today = bj_now.date().isoformat()
    bj_tomorrow = (bj_now + datetime.timedelta(days=1)).date().isoformat()
    try:
        hupu_rows = fetch_hupu()
        hupu_added = merge_hupu(hupu_rows, today_matches, bj_today, bj_tomorrow)
    except Exception as e:  # noqa: BLE001
        hupu_added = -1
        print(f"::warning::虎扑赛程抓取失败，仅保留 Polymarket 场次：{type(e).__name__}: {e}", flush=True)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    (ROOT / "intel" / "game_status.json").write_text(
        json.dumps({"generated_at": now, "games": games}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ROOT / "intel" / "settlements.json").write_text(
        json.dumps({"generated_at": now, "settlements": settlements}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ROOT / "data").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "matches_today.json").write_text(
        json.dumps({"date": today, "matches": today_matches}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (ROOT / "data" / "watchlist_events.json").write_text(
        json.dumps({
            "generated_at": now,
            "events": watch_events,
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if slug_failures:
        print(
            f"::warning::{len(slug_failures)} 场比赛详情抓取失败（本轮跳过，下轮自动重试）："
            + ", ".join(slug_failures[:10]),
            flush=True,
        )
    print(
        f"games={len(games)} settlements={len(settlements)} today_matches={len(today_matches)} "
        f"hupu_added={hupu_added}",
        flush=True,
    )


if __name__ == "__main__":
    main()

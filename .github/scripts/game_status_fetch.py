#!/usr/bin/env python3
"""GitHub Actions: fetch Polymarket game/series status -> intel/*.json.

云端每 5 分钟运行（服务器在首尔直连 Polymarket 被 451 限制，GitHub 美国节点
不受限）。输出：
  intel/game_status.json   每场 Game/Map Winner 市场状态（供流水线按小局出节点）
  intel/settlements.json   系列赢家结算（供服务器回填比赛结果）
提交到仓库 data 分支；服务器发布时拉取合并。
"""

from __future__ import annotations

import datetime
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "Mozilla/5.0 danmu-intel"}


def get(url: str):
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=25).read())


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


def main() -> None:
    today = datetime.date.today().isoformat()
    horizon = (datetime.date.today() + datetime.timedelta(days=2)).isoformat()
    backfill_from = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
    candidates: dict[str, dict] = {}
    # 用 Esports 标签（tag_id=64）精准拉电竞事件（避免被加密货币小时盘刷屏），
    # 只保留今天/明天开赛的候选（2026-08-25 固化，同市场扫描器口径）
    for arch in ("false", "true"):
        # 2026-08-27：archived=false（进行中/未开始）+ archived=true（已结束归档）
        # 两批都要，否则已结束的今天场次会从今日页消失（教训：08-27 CS2 缺场次）
        for off in range(0, 8):
            evs = get(
                "https://gamma-api.polymarket.com/events?tag_id=64"
                "&archived=%s&limit=100&offset=%d&order=startDate&ascending=false" % (arch, off * 100)
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
            if not evs:
                break

    games: dict[str, dict] = {}
    settlements: dict[str, dict] = {}
    today_matches: list[dict] = []
    watch_events: list[dict] = []
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
        except Exception:  # noqa: BLE001
            continue
        time.sleep(0.3)

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
    print(f"games={len(games)} settlements={len(settlements)} today_matches={len(today_matches)}", flush=True)


if __name__ == "__main__":
    main()

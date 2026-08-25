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


def main() -> None:
    today = datetime.date.today().isoformat()
    horizon = (datetime.date.today() + datetime.timedelta(days=2)).isoformat()
    backfill_from = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
    candidates: dict[str, dict] = {}
    # 用 Esports 标签（tag_id=64）精准拉电竞事件（避免被加密货币小时盘刷屏），
    # 只保留今天/明天开赛的候选（2026-08-25 固化，同市场扫描器口径）
    for off in range(0, 8):
        evs = get(
            # 含已关闭事件（结算回填需要）；游戏状态由窗口+流水线自行过滤
            "https://gamma-api.polymarket.com/events?tag_id=64"
            "&archived=false&limit=100&offset=%d&order=startDate&ascending=false" % (off * 100)
        )
        if not evs:
            break
        for e in evs:
            t = e.get("title") or ""
            if not any(k in t for k in ("LoL", "League of Legends", "Counter-Strike", "Dota")):
                continue
            slug = e.get("slug") or ""
            # 用 slug 末尾的比赛日期，禁止用事件层 startDate（挂牌时间≠开赛时间，AGENTS 防错 2）
            mm = re.search(r"-(\d{4}-\d{2}-\d{2})$", slug or "")
            sd = mm.group(1) if mm else ""
            # 窗口：近 3 天（供结算回填）+ 今明两天（供流水线小局节点）
            if sd and backfill_from <= sd <= horizon:
                candidates[slug] = {"title": t, "date": sd, "teams": norm_teams(t)}
        if not evs:
            break

    games: dict[str, dict] = {}
    settlements: dict[str, dict] = {}
    for slug, meta in candidates.items():
        try:
            evs = get(f"https://gamma-api.polymarket.com/events?slug={slug}")
            if not evs:
                continue
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
    print(f"games={len(games)} settlements={len(settlements)}", flush=True)


if __name__ == "__main__":
    main()

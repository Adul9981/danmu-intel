# Aurora Gaming vs DENDELE CS · G3｜局中快照（核验：G3 未进行 · 系列已结束 AUR 2-0）· 2026-08-28

> 元信息：CS2 · BLAST Open Porto 2026（Fall）· Group A 败者组 R1 M1 · BO3
> slug=cs2-aur1-dendel-2026-08-28 · league=CS2
> 数据源：kick_gaules 1129 条 + kick_eslcs 3 条（表情）→ 本场有效样本 ≈ 0
> 数据窗口：20:17–20:54（北京时间 / 12:17–12:54 UTC）· 1132 条 / 359 活跃用户 · 平均 ≈30.7 条/分
> 状态：G3 未进行（多源一致）——Polymarket G1/G2 均结算 AUR 1.0/0.0，settlements winner=Aurora Gaming，matches.json result_inferred「Aurora Gaming 胜（Polymarket 结算）」，无 G3 小局市场；本节点为管线误切片，全节样本不足。

## 状态核验

本页为「G3｜局中（MID-GAME）」请求节点；核验结论 = G3 未进行，系列已结束，Aurora Gaming 2-0 胜。证据链：
1. Polymarket 小局市场（data/game_status.json，20:54 北京时间快照）仅 G1/G2，均 closed、AUR 1.0/0.0、winner=AUR；无 G3 市场；
2. runtime/settlements.json（20:53 北京时间生成）winner=Aurora Gaming；
3. docs/data/intel/matches.json result_inferred =「Aurora Gaming 胜（Polymarket 结算）」；
4. 弹幕口径 G2 16-12（OT）+「2-0 aurora」（19:36）；
5. 本节点窗口无任何 G3 进行中讨论（观众 20:39–20:48 赛后问比分：dendele ganhou? / dendele levou? / quanto acabou jogo do dendele?）。

## 0 核心情报速览

- 比分/进度：请求节点 G3｜局中；核验：G3 未进行，系列已结束 AUR 2-0（Polymarket G1/G2 结算确认）；本节点无本场弹幕样本。
- TOP 信号（风险 → 锚点 → 盘口 → 共识）：
  1. 风险：G3 未进行，系列已按 Polymarket 结算结束（AUR 2-0），本节点为管线误切片 → 无 G3 弹幕可交付，按缺源/样本不足呈现（→ §1/§11）。
  2. 风险：g3 切片窗口内容为其他场次混流（gaules 当时转播 G2×Spirit），跨场混流不可作本场信号（→ §7/§11）。
  3. 锚点：G1/G2 双小局均按 Polymarket 结算 AUR 1.0/0.0，弹幕口径 2-0（19:36）→ 系列已定，无 G3 方向博弈窗口（→ §1/§10）。
  4. 盘口：本节点无本场数字盘弹幕；G1 0.77 / G2 0.745 → 结算 1.0 → 市场与弹幕同向且已兑现（→ §4）。
  5. 共识：gaules 观众 20:39–20:48 连续追问 DENDELE 赛果，无 G3 进行中讨论 → 观众口径指向系列已结束（单源待验证）（→ §5）。
- 决策落点：无有效 G3 情报；系列已结束，转向赛后整场复盘与验证回填；建议固化「结算后禁止再切下一局窗口」规则。

## 1 比赛信息与结果总览 / 状态核验

- 对阵：Aurora Gaming（AUR）vs DENDELE CS；全称 Counter-Strike: Aurora Gaming vs DENDELE CS (BO3)；league=CS2；slug=cs2-aur1-dendel-2026-08-28；赛制 BO3；BLAST Open Porto 2026（Fall）Group A 败者组 R1 M1；开赛 17:00（北京时间 / 09:00 UTC）。
- 状态：请求节点 G3｜局中；核验 = G3 未进行（多源一致，见状态核验）。系列已结束。
- 结果/进度（弹幕口径 · 官方待回填）：G1（Cache，DENDELE 自选）AUR 1-0（Polymarket G1 结算确认）；G2（Mirage，AUR 自选）弹幕口径 AUR 16-12（OT）+ Polymarket G2 结算确认；G3（Nuke）按 2-0 不进行。官方回合比分/HLTV/战报待回填。
- 弹幕采集：截止 20:54（北京时间）· 窗口 20:17–20:54（12:17–12:54 UTC）· 1132 条 / 359 活跃用户 / 平均 ≈30.7 条/分；本场有效样本 ≈ 0。
- 数据源：kick_gaules 1129 + kick_eslcs 3（表情）；虎牙主源缺采。
- 跨源一致性提示：方向无背离（结算 + settlements + matches.json + 弹幕口径全部同向）；缺口 = 官方回合比分/HLTV/战报未回填；本节点切片与内容不匹配（跨场混流）→ 按缺源标注，不交付 G3 结论。

## 2 灰信号汇总（风险 · 观众质疑非结论）

- 本节点窗口：今日无灰信号（322/pix 类初筛命中均为其他场次/广告误报，与本场无关）。
- 纪律声明：G2 终局段灰信号（18:59–19:03，DENDELE 12-8 领先被翻后「322 Luquetá 启动 / Luquetá 收 pix」刷屏，中预警 · 单源 · 观众质疑非结论）已归入 G2 节点页；方向与结算同向（DENDELE 输），兑现统计待官方回填，不作因果结论。
- 词表改进点：葡语 322/pix/vendeu 未入规则词表（沿用前节点记录）。

## 3 BP 锚点与选人情报

- 图池（bot !mapas，前节点 18:16/18:35 两次一致）：G1 Cache（DENDELE 自选）AUR 1-0；G2 Mirage（AUR 自选）已结束；G3 Nuke 按 2-0 不进行。本节点无任何 G3 选图/BP 弹幕（样本不足）。
- 双方阵容（BLAST 官方名册口径 + 前节点弹幕交叉；当日首发待 HLTV 回填）：AUR = XANTARES · woxic（狙击）· Wicadia · Jimpphat · kyxsan（IGL）；DENDELE = gafolo · koala · maxxkor（狙击）· rdnzao · doc。本节点提及量均为 0。
- BP 后战绩情报（必抓项）：无战绩情报提及（本节点无「队伍×地图」胜率/强图弹幕；G2 CT/TR 侧胜率单源口径 18:30 已入前节点页）。
- BP 判负/判胜：无；G3 不存在，不做选图结论。

## 4 盘口与市场讨论

- 弹幕盘口讨论：无本场数字盘 → 样本不足。
- 市场快照（非弹幕）：G1/G2 均 closed、AUR 1.0/0.0（20:54 快照）；无 G3 市场；G1 0.77 → 1.0、G2 0.745 → 0.785 → 1.0（前节点记录）。
- 结构记录：settlements winner=Aurora Gaming；matches.json result_inferred 同向。
- 决策提示：无弹幕盘口共识，不做盘口方向判断；终局以 Polymarket 结算价为最终仲裁。

## 5 方向性情报板

- 正锚：今日无锚点（本节点）。
- 负锚：今日无锚点（本节点）。
- 群体共识：共识不足（本节点无进行中讨论）；赛后口径样本 5 条（单源待验证）：20:39:31「dendele ganhou?」/ 20:43:56「dendele levou?」/ 20:48:27「quanto acabou jogo do dendele?」+ 前节点 19:36「2-0 aurora」。
- 灰信号条件预测：今日无灰信号（本节点）；G2 灰信号按「观众质疑·非结论」记录，条件式口径 = 若兑现指向 DENDELE 一侧输（已随结算同向）。

## 6 情报含义与决策落点（LONG / SHORT）

- LONG（AUR）：方向已由 Polymarket 结算兑现（2-0），本节点无新增可交易窗口。
- SHORT（DENDELE）：无独立新增依据；灰信号只作风险标注。
- 观察点：① 官方回合比分/HLTV/战报回填 → 整场复盘闭环；② 切片器修复（结算后禁止切下一局窗口）；③ 虎牙主源补采与 VOD 回捞（本场全程缺主源）。

## 7 逐局复盘（证据层）

- 本节点窗口时间线：无本场事件弹幕 → 时间线为空；密度峰值 20:26（81 条/分；20:25=60、20:39=60、20:27=46）——内容为其他场次混流，非本场信号。
- 已发生片段（前局弹幕）：G2 终局段 18:58–19:07（弹幕口径 16-12 OT：DENDELE 11-5/12-8 领先 → AUR 连扳 8 回合含 OT；kyxsan 五杀 18:57、侧身 4 杀 18:58、Jimpphat B 点绕后 18:58）；G1 Cache AUR 1-0（结算确认，17:48 末局强起失败 GG 弹幕口径）。详见 g1/g2 节点页。
- 待观察：G3 未发生（按 2-0 不进行）；若官方反转（低概率）整场重审。

## 8 队伍 / 人员画像（带提及量）

- AUR：本节点 0 次；前节点 49 次 / G2 窗 23 次。历史画像（teams.json 累计 155，2026-08-26）：EWC R16 1:2 负 FURIA、「不会守 CT」、jimpphat 新援低迷；本场 G1/G2 双结算（待官方回合比分）。
- DENDELE：本节点 0 次；前节点 82 次 / G2 窗 42 次（全场最高）。历史画像（08-26 vs Spirit 0-2，TEAM_PROFILES dendelecs）：「领先送分/经济管理差」；本场自选 Cache 负 + G2 12-8 送掉（弹幕口径）；team_names.json 尚未登记（沉淀点）。
- 人员（前节点 G2 窗提及量）：kyxsan 11（尾段高光，单源待回填）、Luquetá 9（观众口径管理层，待官方核实）、doc 7（中段高光尾段隐身）、Wicadia 4、Jimpphat 3（与 players.json 负向画像对照）、koala 2、gafolo 1、XANTARES/woxic/maxxkor/rdnzao 0。本节点全部为 0。

## 9 联赛规律与版本

- 赛事结构：BLAST Open Porto 2026（Fall）· Group A 败者组 R1 M1 · BO3；CS2 默认采集集 = 虎牙 CSBOY 官方（123321）+ CSBOY-Mo（321123）+ BLAST 官方虎牙（blast）主源；Kick eslcs/gaules/esportsworldcup/cs2_maincast；Twitch 暂停。本场全程缺主源。
- 跨场候选规律（引用前节点）：① DENDELE「领先送分/经济管理差」样本 +2；② DENDELE 自选图连续不利（Cache 08-26 负 Spirit → 08-28 自选 Cache 负 AUR）；③ AUR「CT 侧强/打巴西队即巅峰」候选（单源）。
- 版本/地图池：本节点无版本讨论；G3 无图可论。
- 频道特征：gaules 多赛日并行 → 按「队伍×地图」过滤；本节点窗口混流严重。

## 10 预测验证回填明细

- 「AUR 2-0 候选」（G2 节点页 12:08 记录）→ 已兑现：settlements winner=Aurora Gaming（20:53 北京时间）+ game_status G1/G2 均 AUR 1.0/0.0（20:54 快照）+ 无 G3 市场。
- G2 方向预测（DENDELE 11-5/12-8 领先 → AUR 16-12 OT 弹幕口径）→ 方向兑现（Polymarket 结算确认）；回合比分待官方。
- 本节点新增预测：无（G3 无样本）。

## 11 数据与溯源

- 弹幕数据：data/intel_slices/cs2-aur1-dendel-2026-08-28_g3_mid.jsonl（1132 条 / 359 活跃用户 / 窗口 20:17–20:54 北京时间 = 12:17–12:54 UTC；密度峰值 20:26 81 条/分）。
- 规则层：runtime/vps_intel/cs2-aur1-dendel-2026-08-28_g3_mid_intel.json 未生成；g3_bp_intel.json（窗口 20:02–20:37）teams 段无 Aurora/DENDELE，内容为其他场次 → 误切片佐证。
- 完整性三栏：实际 = kick_gaules 1129 + kick_eslcs 3（表情）→ 本场有效样本 ≈ 0；预期 = 虎牙 CSBOY 官方/CSBOY-Mo/BLAST 官方虎牙 + Kick eslcs/gaules/esportsworldcup/cs2_maincast；缺口 = 虎牙主源全程离线未采、eslcs ≈ 未采、g3 窗口为误触发跨场混流（不构成有效数据）、VOD 未回捞。
- 采集截止：20:54（北京时间 / 12:54 UTC）；官方数据抓取时刻：game_status 12:54:36 UTC（= 20:54 北京时间）、settlements 12:53:30 UTC（= 20:53 北京时间）。
- 来源分层声明：本页无「本场 G3 弹幕」依据，全部按缺源/样本不足呈现；引用前节点结论带「前局弹幕/历史画像/盘口」标签并注明时间，不硬造。

## 本场长期沉淀点

1. 防错规则候选（固化建议）：小局结算/系列结束后，切片器必须先用 game_status closed + settlements winner 校验再切下一局窗口（G3 误切片教训：1158 + 1132 条跨场混流 + 规则层 JSON 误生成）。
2. 验证特征候选：观众「赛后结果询问型弹幕」（20:39–20:48）可作为「系列已结束」的弹幕侧验证特征（样本 +1）。
3. 画像沉淀：DENDELE「领先送分」候选 +2；team_names.json 尚未登记 DENDELE 缩写（待登记）；AUR「CT 侧强/打巴西队即巅峰」候选（单源）。

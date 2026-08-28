# Aurora Gaming vs DENDELE CS · 局中弹幕情报快照（G3｜局末/局间 · GAME-REVIEW）· 2026-08-28

> 元信息：CS2 · BLAST Open Porto 2026（Fall）· Group A（败者组 R1 M1）· BO3
> slug=cs2-aur1-dendel-2026-08-28 · league=CS2 · 开赛 17:00（北京时间 / 09:00 UTC）
> 数据源：kick_gaules 1287 条 + kick_eslcs 3 条（全表情）→ 本场有效样本 ≈ 0
> 数据窗口：20:17–21:03（北京时间 / 12:17–13:03 UTC）· 1290 条 / 395 活跃用户 / 平均 ≈28.0 条/分
> 状态：G3｜局末/局间（GAME-REVIEW）· 局中·非终局，结果待定（用户定稿标注）；数据核验 = 系列已按 Polymarket 结算 AUR 2-0 · G3 未进行 · 本节点切片为跨场混流误切片，无本场 G3 弹幕样本（样本不足）

## 0 核心情报速览

- 比分/进度：请求节点 G3｜局末/局间（GAME-REVIEW）；核验：系列已按 Polymarket 结算 AUR 2-0 · G3 未进行 · 本节点无本场 G3 弹幕样本（弹幕口径·官方待回填）
- TOP 信号（风险 → 锚点 → 盘口 → 共识）：
  1. 风险：G3 节点无本场有效弹幕（系列已按 Polymarket 结算 AUR 2-0，本切片为跨场混流误切片）→ 无 G3 样本可交付，不据本页做本场判断（→ 详 §1/§11）。决策落点：不据本页做任何本场方向/仓位判断。
  2. 风险：切片主体为其他场次（G2 vs Spirit）直播 + 频道广告/机器人推送 → 已按禁混源纪律整段排除，不并入本场信号（→ 详 §7/§11）。决策落点：跨场内容与本场情报无关，禁止混用。
  3. 锚点：系列方向三层一致（Polymarket G1/G2 双结算 AUR 1.0/0.0 + settlements winner=Aurora Gaming + matches.json 同向）→ 终局以 Polymarket 结算为最终仲裁，方向已兑现（→ 详 §1/§10）。决策落点：无新增操作窗口，等官方战报/HLTV 回填。
  4. 盘口：本窗口无本场数字盘讨论（词表命中均为其他场次/广告）→ 盘口侧无新增边际信息，样本不足（→ 详 §4）。决策落点：不据本页做盘口方向判断。
  5. 共识：弹幕仅赛后询问 DENDELE 赛果 + 单条「输 2-0」（20:48，单源）→ 与结算方向同向、样本量不足（→ 详 §5）。决策落点：方向参考沿用前节点（已与结算同向）。
- 决策落点：本节点边际信息 = ① 数据完整性异常：g3_end 切片错标（系列 2-0 结算后管线仍切 G3 窗口，捕获下一场 G2 vs Spirit 直播 + 广告/机器人推送），本场 G3 无实况样本；② 系列已按 Polymarket 结算 AUR 2-0（game_status G1/G2 双 closed + settlements + matches.json 三层一致），官方战报/HLTV 待核对；③ 建议固化「结算后停止切片 + 跨场混流回归测试」。

## 1 比赛信息与结果总览 / 状态核验

- 对阵/元数据：Aurora Gaming（AUR）vs DENDELE CS · 全称 Counter-Strike: Aurora Gaming vs DENDELE CS (BO3) · league=CS2 · slug=cs2-aur1-dendel-2026-08-28 · 赛制 BO3 · BLAST Open Porto 2026（Fall）· Group A（败者组 R1 M1）· 开赛 17:00（北京时间 / 09:00 UTC）
- 状态核验：请求节点 = G3｜局末/局间（GAME-REVIEW）· 局中·非终局，结果待定（用户定稿标注）；数据核验 = G3 未进行，系列已按 Polymarket 结算 AUR 2-0：① game_status.json（13:03:37 UTC = 21:03 北京时间快照）本场仅 G1/G2 两个小局市场、均 closed=true、AUR 1.0/DENDELE 0.0、winner=AUR，无 G3 市场；② runtime/settlements.json（同刻）winner=Aurora Gaming；③ docs/data/intel/matches.json result_inferred=「Aurora Gaming 胜（Polymarket 结算）」；④ 本切片无任何 G3 实况弹幕（nuke 提及 0）→ 用户口径「G3 进行中/刚结束」与结算文件冲突，以数据为准，标注样本不足
- 结果/进度（弹幕口径 · 官方待确认）：G1（Cache，DENDELE 自选）AUR 1-0（Polymarket G1 结算 1.0/0.0 确认）；G2（Mirage，AUR 自选）弹幕口径 AUR 16-12（OT）+ Polymarket G2 结算 1.0/0.0 确认；G3（Nuke，决胜图）按 2-0 不进行；官方回合比分/HLTV/战报待回填
- 弹幕采集：截止 21:03（北京时间）· 窗口 20:17–21:03（12:17–13:03 UTC）· 1290 条 / 395 活跃用户 / 平均 ≈28.0 条/分；本场有效样本 ≈ 0（详见 §11）
- 数据源：kick_gaules 1287 条 + kick_eslcs 3 条（全表情）· 虎牙主源缺采
- 跨源一致性提示：方向无背离（game_status + settlements + matches.json + 弹幕单条「输 2-0」20:48 同向）；缺口 = 官方回合比分/HLTV/战报未回填；本节点切片与内容不匹配（跨场混流）→ 按缺源标注，不交付 G3 结论

## 2 灰信号汇总（风险 · 观众质疑非结论）

- 本窗口（20:17–21:03 北京时间）词表初筛 → 人工复核：今日无有效灰信号 —— 322 / pix / vendeu / manipul 类命中 = 0 条；VAC 表情 = 0 条；「roteiro（剧本）」仅 1 条（20:34，其他场次闲聊玩梗语境）；其余命中全部为频道广告/机器人推送 → 无指向本场队伍/选手的质疑，无样本不硬造
- 原文摘录（中文意译，≤2 条/信号）：「剧本正在成型…kkk」（20:34，其他场次玩梗，已排除）｜Gaupoints / Flexform 广告类（20:18 起多次，机器人推送）
- 纪律声明：灰信号仅作风险标注与盘口对照素材，不作假赛/剧本结论；本节点无有效灰信号 → 无风险项、无条件预测。G2 灰信号沿用（前节点 g2_end）：18:59–19:03 DENDELE 12-8 领先后被翻引发 322/pix 梗集中（中预警 · 单源 · 观众质疑非结论），方向与结算同向（DENDELE 输），兑现统计待官方回填；本窗口未再现
- 词表改进点：葡语 322 / pix / vendeu 未入规则词表；Gaupoints/语音消息类机器人推送持续污染灰信号计数（前节点已记录）

## 3 BP 锚点与选人情报

- 图池（前节点 bot !mapas 多次一致口径）：G1 Cache（DENDELE 自选）→ AUR 1-0；G2 Mirage（AUR 自选）→ 已结束；G3 Nuke（决胜图）→ 系列按 2-0 结算，不进行。本窗口无任何 G3 选图/BP 弹幕（nuke 提及 0）；唯一图池弹幕为跨场 G2 vs Spirit（Dust2 / Cache / Ancient），已按禁混源纪律排除
- 双方阵容（BLAST 官方名册口径 · 当日首发待 HLTV/官方回填）：AUR = XANTARES · woxic（狙击）· Wicadia · Jimpphat · kyxsan（IGL）；DENDELE = gafolo · koala · maxxkor（狙击）· rdnzao · doc。本窗口提及量全部 0
- BP 后战绩情报（必抓项）：无战绩情报提及（本窗口无「队伍×地图」胜率/强图弹幕；G3 未进行 → 无 pick 锁定/图三转换窗口可扫）
- BP 判负/判胜：无

## 4 盘口与市场讨论

- 弹幕盘口讨论：无本场数字盘 → 样本不足（「可以押上老婆孩子吗」20:28 为 paiN vs NAVI 其他场次调侃，已排除）
- 市场快照（盘口佐证 · 非弹幕）：Polymarket game_status（13:03:37 UTC = 21:03 北京时间快照）：本场仅 G1/G2，均 closed=true、AUR 1.0 / DENDELE 0.0、winner=AUR；无 G3 市场；runtime/settlements.json（同刻）winner=Aurora Gaming；matches.json result_inferred 同向。前节点记录：G1 AUR 0.77 → 1.0、G2 AUR 0.745 → 0.785 → 1.0
- 决策提示：本页无新增盘口信息 → 不做盘口方向判断；终局以 Polymarket 结算价为最终仲裁，官方战报待核对

## 5 方向性情报板（正锚 × 负锚 × 共识 × 灰信号条件预测）

| 类型 | 对象 | 内容 | 证据来源 | 置信/状态 |
| --- | --- | --- | --- | --- |
| 正锚（看好） | AUR（系列） | G1/G2 Polymarket 双结算（AUR 1.0/0.0）+ settlements winner=Aurora Gaming → 系列方向已兑现；本窗口无新增本场锚点 | 结构源（Polymarket 结算）+ 前节点弹幕 | 多源确认 · 官方战报待核对 |
| 正锚（历史 · 带时间） | AUR | 08-26 AUR 以 16:12 惜败 G2 的高位队伍 → 实力层级推测偏 AUR（推测·待验证，非本窗口弹幕） | 历史画像（08-26 官方战报） | 待回填 |
| 负锚（看衰） | DENDELE | 08-26 → 08-28「领先送分 / 经济管理差」跨场叙事延续（G2 12-8 送掉，前节点弹幕口径）；本窗口仅「输 2-0」1 条（20:48，单源） | 前节点弹幕 + 本场弹幕（单源） | 方向已兑现（观众质疑·非结论） |
| 群体共识 | — | 共识不足：本窗口仅赛后询问 3 条 + 「输 2-0」1 条（样本量不足）；前节点「2-0 aurora」（19:36）已与结算同向 | 本场弹幕（样本不足） | 单源待验证 |
| 灰信号条件预测 | — | 今日无灰信号 → 无条件预测；G2 灰信号按「观众质疑·非结论」记录，条件式口径 = 若兑现指向 DENDELE 一侧输（已随结算同向） | 前节点弹幕（g2_end） | 兑现统计待官方回填 |

纪律：灰信号只作风险标注与兑现统计，不作假赛结论；本节点无本场样本，方向板仅引用前节点与结构源，未产生新的方向判断。

## 6 情报含义与决策落点（LONG / SHORT）

- LONG（看好 AUR）：方向已由 Polymarket 结算兑现（2-0），本节点无新增可交易窗口；若持有本场相关仓位，以结算价为最终仲裁，官方战报待核对
- SHORT（看衰 DENDELE）：无独立新增依据；灰信号只作风险标注（前节点 322/pix 梗已按中预警留痕，不作假赛结论）
- 本场观察点：① 官方战报 / HLTV 回填 G1/G2 具体回合比分（16-12 OT / 12-8 口径核对）；② 修复 g3 切片错标（结算后停切 + 切片健康检查）；③ 虎牙 CSBOY 主源补采与 VOD 回捞（本场全程缺主源）；④ 整场复盘页（类型 A）沉淀本场全部节点与验证回填

## 7 逐局复盘（证据层）

- G1 · Cache（DENDELE 选图）· 已结束（结算确认）：AUR 1-0 —— 末局 DENDELE 强起失败 GG（17:48 弹幕口径）；bot !mapas 17:49 / 18:01 输出「AURORA (1) VS (0) DENDELE」；官方回合比分待回填（详见 g1 节点页）
- G2 · Mirage（AUR 选图）· 已结束（结算确认）：弹幕口径 AUR 16-12（OT）——DENDELE 曾 11-5 / 12-8 领先、AUR 连扳 8 回合（多用户一致口述）+ Polymarket G2 结算 AUR 1.0/0.0；官方回合比分待核对（详见 g2_end 节点页）
- G3 · Nuke（决胜图）· 未进行：系列已按 AUR 2-0 结算（无 G3 小局市场、无实况切片内容）→ 本节点无 G3 局中事件，未发生段不适用
- 本节点窗口（20:17–21:03 北京时间）与本场相关条目（全部为赛后口径，无局中）：
  - 20:39:31「DENDELE 赢了吗？」（willcf1）→ 赛后询问
  - 20:43:56「DENDELE 输了吗？」（FelipeHeroi001）→ 赛后询问
  - 20:48:27「DENDELE 那场比分多少？」（pedroboiago22）→ 赛后询问
  - 20:48:54「输 2-0」（shuuy4）→ 紧随上一询问、语境指向 DENDELE 赛果；单源待官方
  - 20:26:27 / 20:43:03 / 21:03:27 bot !mapas：G2 vs Spirit 图池与比分（Dust2-Spirit 选 / Cache-G2 选 / Ancient 决胜；G2 0-1 Spirit）→ 跨场混流佐证，已排除
  - 原文摘录（葡语 → 中文意译）：「dendele ganhou?」20:39:31｜「dendele levou?」20:43:56｜「quanto acabou jogo do dendele?」20:48:27｜「perdeu 2x0」20:48:54｜「Mapas G2 (0) x (1) Spirit || Dust 2 - Pick: Spirit || Cache - Pick: G2 || Ancient - Decider!」20:43:03（跨场）
- 弹幕密度时间线（北京时间 · 峰值均为表情/机器人推送/跨场聊天，无本场事件锚点）：20:26（81 条/分，全窗口峰值）＞ 20:25（60）＞ 20:39（60）＞ 20:27（46）＞ 20:32（44）＞ 20:19（43）＞ 20:30（42）；窗口均值 ≈28.0 条/分
- 可验证情报痕迹 / 结果来源：本窗口无本场局中痕迹；系列结果来源 = Polymarket 结算（game_status G1/G2 双结算 + settlements winner）+ 前节点弹幕（G1/G2 口径）+ 本窗口「输 2-0」单条（20:48，单源待验证）

## 8 队伍 / 人员画像（带提及量）

### 队伍画像

| 队伍 | 本窗口提及量 | 本窗口画像 | 长期画像（带时间 · 非本窗口弹幕） |
| --- | --- | --- | --- |
| AUR（Aurora Gaming） | 有效提及 ≈ 0（BotRix 赛程推送除外） | 无局中评价 → 无有效样本 | teams.json（2026-08-26 更新，累计弹幕提及 155）：EWC R16 1:2 负 FURIA（官方确认）、「不会守 CT」、新援 jimpphat 低迷 → 本场 G1/G2 双结算（Polymarket），画像方向待官方比分回填验证 |
| DENDELE（DENDELE CS） | 有效提及 ≈ 4（赛后询问 3 + 「输 2-0」1） | 无局中评价 → 赛后口径与「输 2-0」同向（单源） | TEAM_PROFILES（2026-08-26，vs Spirit 0-2）：「领先送分 / 经济管理差」、观众灰信号约 14 条（无实锤）→ 08-28 G2 12-8 送掉再现（前节点弹幕口径），与「输 2-0」同向 |

### 人员画像

| 选手 | 提及量 | 本窗口评价 | 前节点引用（非本窗口 · g2_end 页） |
| --- | --- | --- | --- |
| XANTARES / woxic（狙）/ Wicadia / Jimpphat / kyxsan（IGL）（AUR） | 全部 0 | 无样本 | kyxsan 11 次（18:57 五杀/高光叙事）、Wicadia 4 次、Jimpphat 3 次（与 players.json 负向画像对照） |
| gafolo / koala / maxxkor（狙）/ rdnzao / doc（DENDELE） | 全部 0（「descente +koala」20:28 为饰品 bot 内容，非选手） | 无样本 | doc 7 次（中段高光尾段隐身）、koala 2 次、gafolo 1 次；Luquetá（DENDELE 组织人物，身份待官方核实）9 次（322/pix 梗相关） |

库登记状态：team_names.json 已登记 AUR（abbr=AUR / full=Aurora Gaming）；DENDELE 未登记 → 待整场复盘后登记（沉淀点）。

## 9 联赛规律与版本

- 赛事结构：BLAST Open Porto 2026（Fall）· Group A 败者组 R1 M1 · BO3；08-26 首日 AUR 0-2 G2、DENDELE 0-2 Spirit → 今日两队均为背靠背生死战；AUR 以 2-0 存活、DENDELE 出局（Polymarket 口径，官方待确认）
- 跨场候选规律（引用前节点）：① DENDELE「领先送分 / 经济管理差」样本 +2；② DENDELE 自选图连续不利（08-26 自选 Cache 负 Spirit → 08-28 自选 Cache 负 AUR）；③ AUR「CT 侧弱」历史画像 vs 本场双胜 → 需官方数据验证（推测·待验证）
- 版本 / 图池：本窗口无本场版本讨论（nuke 提及 0）；图池话题均为跨场 G2 vs Spirit（Dust2 / Cache / Ancient），按禁混源纪律不并入 → 样本不足
- 频道特征：gaules 多赛日并行 → 按「队伍×地图」过滤；本节点窗口混流严重（G2 vs Spirit 及相关选手弹幕 ≈79 条）

## 10 预测验证回填明细（沉淀层 · 闭环）

| 预测/悬念 | 来源 | 状态 |
| --- | --- | --- |
| 看衰 DENDELE 自选 Cache → AUR 拿下 G1 | 本场弹幕（g1 节点） | 已兑现（Polymarket G1 结算确认，AUR 1-0） |
| G2 方向（DENDELE 11-5/12-8 领先 → AUR 16-12 OT） | 本场弹幕（g2_end）+ 结构源 | 方向已兑现（Polymarket G2 结算确认）；回合比分待官方 |
| 「AUR 2-0 终结系列」（19:36 弹幕 + settlements 口径） | 本场弹幕（g2_end）+ 结构源 | 已兑现（settlements winner=Aurora Gaming + game_status G1/G2 双结算 + 无 G3 市场）；官方战报待核对 |
| 灰信号历史：DENDELE 08-26 约 14 条观众质疑是否再现 | 历史画像（08-26 战报） | 08-28 G2 再现 322/pix 梗集中（g2_end 节点，中预警）→ 已留痕，不作结论；本窗口未再现 |
| 本窗口新增预测 | — | 无（无本场样本，不硬造预测） |

回填机制：终局以 Polymarket 结算价为最终仲裁；官方比分 / HLTV / 战报回填后，由整场复盘页（类型 A）统一更新。

## 11 数据与溯源（沉淀层）

- 弹幕数据：data/intel_slices/cs2-aur1-dendel-2026-08-28_g3_end.jsonl（1290 条 / 395 活跃用户 / 窗口 20:17–21:03 北京时间 = 12:17–13:03 UTC；密度峰值 20:26 81 条/分；均值 ≈28.0 条/分；纯表情 326 条 25.3%、BotRix 119 条、Gaules 广告 9 条、命令 50 条（!dendele ×5）、跨场 G2 vs Spirit 相关 ≈79 条）
- 规则层：runtime/vps_intel/cs2-aur1-dendel-2026-08-28_g3_end_intel.json 未生成（用户指定路径不存在）；g3_mid 状态文件（13:03:35 UTC = 21:03 北京时间生成，source=codex）确认前节点由 Codex 产出；g3_bp_intel.json（窗口 20:02–20:37）teams 段无本场两队 → 误切片佐证
- 时间显示规范：页面全部时间为北京时间（UTC+8，弹幕 ts 换算 +8h；UTC 仅数据窗口括号备注）
- 采集截止：21:03（北京时间 / 13:03 UTC）；官方数据抓取时刻：game_status 13:03:37 UTC（= 21:03 北京时间）、settlements 13:03:37 UTC（= 21:03 北京时间）
- 来源分层声明：本页无「本场 G3 弹幕」依据，全部按缺源/样本不足呈现；引用前节点结论带「前局弹幕 / 历史画像 / 盘口」标签并注明时间；跨场内容（G2 vs Spirit）已按禁混源纪律排除；无数据支撑的推测未产生
- 待确认清单：官方战报 G1/G2 回合比分（16-12 OT / 12-8 / 12-6 口径出入）；系列 2-0 官方确认；当日首发一致性；g3 切片错标修复（结算后停切 + 跨场混流回归测试）

### 数据完整性三栏

| 实际数据源 | 预期数据源（DANMU_CAPTURE_RULES §17/§19 + leagues.json） | 缺口 |
| --- | --- | --- |
| kick_gaules 1287 条 + kick_eslcs 3 条（全表情）→ 本场有效样本 ≈ 0 | 虎牙 CSBOY 官方（123321）/ CSBOY-Mo（321123）【第一优先级主源】+ BLAST 官方虎牙（blast）+ KICK eslcs / gaules / esportsworldcup / cs2_maincast | 虎牙 CSBOY 系全程离线未采（主源缺失 · 重点告警）；BLAST 官方虎牙未采；KICK esportsworldcup / cs2_maincast 本窗口无本场数据；本节点切片错标（系列 2-0 结算后捕获的是下一场 G2 vs Spirit 直播内容）→ G3 无有效弹幕样本；VOD 未回捞 → 缺源 + 无样本，不交付完整结论 |

## 本场长期沉淀点

1. 切片错标防错（一次错误原则：记录 → 根因 → 固化 → 回归）：系列 2-0 结算后，管线仍按预设图数产出 g3_bp / g3_mid / g3_end 切片并捕获下一场（G2 vs Spirit）直播内容 → 固化规则：结算/终局检测通过后立即停止该场切片；切片健康检查（本场队伍提及量占比低于阈值即告警）；补跨场切片检测回归测试。
2. DENDELE「领先被翻」跨场叙事（08-26 vs Spirit 0-2 → 08-28 G1/G2，观众口径）→ 待官方数据回填后升级为队伍画像标签；灰信号纪律：观众质疑·非结论，需比赛数据验证。
3. 赛后询问型弹幕作为结束检测辅助信号：观众对已结束比赛的滞后询问（「dendele ganhou? / levou? / quanto foi?」20:39–20:48，本场样本 +1）＝结果不确定性窗口，可并入 verify_match_end 多信号校验。
4. 用户口径 vs 数据冲突处理：G3「进行中/刚结束」口径与结算文件冲突时，以 Polymarket 结算为最终仲裁（AGENTS.md 规则 18），页面如实标注「样本不足」，不硬造局中内容。

---

状态：局中·非终局，结果待定 · 数据核验：系列已按 Polymarket 结算 AUR 2-0 · 弹幕口径 · 官方待回填 · 灰信号仅为观众质疑非结论 · 采集截止 2026-08-28 21:03（北京时间）· 时间显示规范：UTC+8 · intel-report skill

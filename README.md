# Danmu Intel · 弹幕情报库（GitHub Pages 站点）

把虎牙 / SOOP 直播间弹幕加工成"有预测、有闭环"的电竞比赛情报。

## 目录

```text
index.html            产品首页（价值 / 数据底座 / 闭环钩子 / 入口）
intel/                弹幕情报页（索引 / 局中监控 / 整场复盘 / 灰信号统计）
preview/              产品框架预览 + 情报台内部预览
docs/                 弹幕情报库框架（分层架构 + 发布佐证闭环原则）
```

## 边界

```text
只展示聚合结论与统计，不裸展示弹幕流与用户身份；
灰信号为观众风险标注，非结论；页脚免责：不构成投资建议。
```

## 更新方式

```text
1. 新比赛情报页生成后复制到 intel/（保留文件名）。
2. 更新 intel_danmu_index.html 与灰信号统计页。
3. git add -A && git commit && git push（Pages 自动重新构建）。
```

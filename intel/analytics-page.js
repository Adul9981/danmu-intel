const $ = (id) => document.getElementById(id);
const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
}[char]));
const fmtNum = (value) => Number(value || 0).toLocaleString("zh-CN");
const fmtDuration = (seconds) => {
  const value = Number(seconds || 0);
  if (value < 60) return `${Math.round(value)}s`;
  const minutes = Math.floor(value / 60);
  const rest = Math.round(value % 60);
  return minutes < 60 ? `${minutes}m ${rest}s` : `${Math.floor(minutes / 60)}h ${minutes % 60}m`;
};
const pageName = (path) => {
  if (path === "/" || path === "/index.html") return "弹幕情报库首页";
  if (path.endsWith("/today.html")) return "今日情报";
  if (path.endsWith("/history.html")) return "历史情报库";
  if (path.endsWith("/pattern_decision_workspace.html")) return "形态决策台";
  if (path.endsWith("/pattern_atlas.html")) return "形态图谱";
  if (path.endsWith("/analytics.html")) return "访问用户统计";
  if (path.includes("/intel_danmu_") || path.includes("/intel_soop_")) return "比赛情报详情";
  if (path.includes("/match_")) return "比赛时间轴";
  if (path.includes("/intel_profile_")) return "队伍 / 选手画像";
  return path;
};
const outboundName = (id) => ({
  polymarket_market: "Polymarket 市场",
  telegram: "Telegram",
  youtube: "YouTube",
  github: "GitHub"
}[id] || id);

let rangeDays = 1;
let allPages = [];

function renderChart(rows) {
  if (!rows.length) {
    $("usageChart").innerHTML = '<div class="chart-empty">当前范围暂无匿名访问数据。</div>';
    return;
  }
  const max = Math.max(...rows.map((row) => Number(row.visitors) || 0), 1);
  $("usageChart").innerHTML = rows.map((row) => {
    const visitors = Number(row.visitors) || 0;
    const height = Math.max(3, visitors / max * 190);
    return `<div class="usage-day" title="${esc(row.day)} · ${fmtNum(visitors)} 访客 · ${fmtNum(row.sessions)} 会话">
      <b>${fmtNum(visitors)}</b>
      <div class="usage-bar" style="height:${height.toFixed(1)}px"></div>
      <span>${esc(String(row.day).slice(5))}</span>
    </div>`;
  }).join("");
}

function render(data) {
  const overview = data.overview || {};
  $("uVisitors").textContent = fmtNum(overview.uniqueVisitors);
  $("uSessions").textContent = fmtNum(overview.sessions);
  $("uPageviews").textContent = fmtNum(overview.pageViews);
  $("uActive").textContent = fmtNum(overview.activeVisitors5m ?? overview.activeNow5m);
  $("uActiveDetail").textContent = `${fmtNum(overview.activeSessions5m)} 个活跃标签页`;
  $("uReturning").textContent = fmtNum(overview.returningVisitors);
  $("uDuration").textContent = fmtDuration(overview.avgSessionSeconds);
  $("usageUpdated").textContent = `更新 ${new Date(data.generatedAt).toLocaleString("zh-CN", { hour12: false })}`;
  renderChart(data.daily || []);
  allPages = data.pages || [];
  renderPages();
  const outbound = data.outbound || [];
  $("usageOutbound").innerHTML = outbound.length ? outbound.map((row) => `<tr>
    <td>${esc(outboundName(row.link_id))}</td>
    <td class="num">${fmtNum(row.clicks)}</td>
    <td class="num">${fmtNum(row.visitors)}</td>
  </tr>`).join("") : '<tr><td colspan="3" class="subsym">当前范围暂无导流点击。</td></tr>';
}

function renderPages() {
  const query = ($("pageSearch")?.value || "").trim().toLowerCase();
  const rows = query ? allPages.filter((row) =>
    `${pageName(row.path)} ${row.path}`.toLowerCase().includes(query)
  ) : allPages;
  $("usagePages").innerHTML = rows.length ? rows.map((row) => `<tr>
    <td><b>${esc(pageName(row.path))}</b><span class="subsym">${esc(row.path)}</span></td>
    <td class="num">${fmtNum(row.views)}</td>
    <td class="num">${fmtNum(row.visitors)}</td>
  </tr>`).join("") : `<tr><td colspan="3" class="subsym">${query ? "没有匹配的页面。" : "当前范围暂无页面浏览。"}</td></tr>`;
}

async function load(days = rangeDays) {
  rangeDays = days;
  document.querySelectorAll("[data-days]").forEach((button) => {
    button.classList.toggle("active", Number(button.dataset.days) === days);
  });
  try {
    const apiOrigin = String(window.DANMU_ANALYTICS_API || "").replace(/\/$/, "");
    const response = await fetch(`${apiOrigin}/intel/api/stats?days=${days}`, { cache: "no-store" });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    render(await response.json());
  } catch (error) {
    $("usageUpdated").textContent = `统计接口不可用：${error.message}`;
  }
}

function boot() {
  document.querySelectorAll("[data-days]").forEach((button) => {
    button.addEventListener("click", () => load(Number(button.dataset.days)));
  });
  $("pageSearch").addEventListener("input", renderPages);
  load(1);
  setInterval(() => load(rangeDays), 60_000);
}

if (document.readyState === "complete") boot();
else window.addEventListener("load", boot, { once: true });

"""Render the standalone experiment page from the public, credential-free ledger."""
import json, html, math
from pathlib import Path
root = Path(__file__).resolve().parents[1]
d = json.loads((root/'data/cofi-android-harmony.json').read_text())
e = html.escape
rows = []
completed = sum(x["migration"] == "迁移自报完成" for x in d["experiments"])
pending = len(d["experiments"]) - completed
md = ['# 阶段1-所有model harness组合的A2H实验', '', '实验规划 · 2026-10-30 · 11 组。历史迁移自报完成 6 组，其余 5 组状态见下表。', '', '**自报完成不代表独立验收通过。** 已确认复用6组历史结果，补跑5组；当前执行状态以各行记录为准。', '', d.get('execution_note',''), '', '| 模型 / ID | Harness | 迁移状态 | 独立验收 | 结果镜像（本地 Tart） | 进度备注 |', '|---|---|---|---|---|---|']
for i, x in enumerate(d['experiments'], 1):
    done = x['migration'] == '迁移自报完成'
    image = '<code>'+e(x['result_image'])+'</code><small>本地克隆 · 远程地址待补</small>' if x['result_image'] else '<span class="muted">待产出</span>'
    if x['image_url']:
        assert x['image_url'].startswith('https://')
        image += '<a href="'+e(x['image_url'],quote=True)+'">下载镜像</a>'
    rows.append(f'''<tr data-state="{'done' if done else 'planned'}" data-harness="{e(x['harness'])}"><td class="number">{i:02}</td><td><strong>{e(x['model_family'])}</strong><small>{e(x['model_id'])}</small></td><td>{e(x['harness'])}<small>{e(x['harness_version'])}</small></td><td><span class="badge {'done' if done else ''}">{e(x['migration'])}</span><small>{e(x['evaluation'])}</small></td><td>{image}</td><td class="notes">{e(x['notes'])}<small>{e(x.get('schedule_window',''))}</small></td></tr>''')
    md.append('| '+' | '.join([x['model_family']+' / '+x['model_id'],x['harness']+' '+x['harness_version'],x['migration'],x['evaluation'],'`'+x['result_image']+'` · 远程地址待补' if done else '待产出', x['notes']+' '+x.get('schedule_window','')])+' |')
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>阶段1-所有model harness组合的A2H实验 · HMBot Benchmark</title>
<style>
:root{font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#182b32;background:#f4f6f3}*{box-sizing:border-box}body{margin:0}header{padding:22px 5vw;border-bottom:1px solid #dce4df;display:flex;justify-content:space-between;gap:20px;font-size:13px}a{color:#186c59}main{max-width:1540px;margin:auto;padding:52px 5vw}h1{font-size:clamp(30px,4vw,48px);letter-spacing:-1.5px;margin:12px 0 16px}h2{font-size:19px;margin:0 0 12px}.eyebrow{font-size:12px;font-weight:700;color:#27745f;letter-spacing:2px}.intro{max-width:780px;line-height:1.8;color:#587078}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:32px 0}.metric{padding:24px;background:white;border:1px solid #dce4df;border-radius:12px}.metric b{font-size:36px;display:block;margin-bottom:8px}.metric span{font-size:13px;color:#607477}.toolbar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:28px 0 14px}select,input{font:inherit;background:white;border:1px solid #c7d6cc;border-radius:7px;padding:10px;max-width:100%}label{font-size:13px}#count{margin-left:auto;color:#607477;font-size:13px}.table-wrap{overflow:auto;border:1px solid #dce4df;border-radius:12px;background:white}table{border-collapse:collapse;width:100%;min-width:1000px;text-align:left}th{font-size:11px;color:#667b7b;letter-spacing:1px;background:#eaf0eb;padding:16px}td{font-size:13px;padding:20px 16px;border-top:1px solid #edf1ee;vertical-align:top}small{display:block;font-size:11px;color:#607477;line-height:1.6;margin-top:7px}code{font-size:11px;overflow-wrap:anywhere}.badge{display:inline-block;background:#edf0f4;color:#596a7b;border-radius:6px;padding:5px 8px;font-size:11px;white-space:nowrap}.badge.done{background:#e3f2e8;color:#236a4b}.notes{max-width:220px;line-height:1.7;color:#607477}.number{color:#8a9998}.muted{color:#8a9998}.details{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:28px}.detail{padding:25px;background:#fff;border:1px solid #dce4df;border-radius:12px;font-size:13px;line-height:1.9}.detail ul{padding-left:20px}footer{margin:28px 0;color:#607477;font-size:12px;line-height:1.8}@media(max-width:700px){main{padding:30px 20px}.metrics{gap:8px}.metric{padding:16px}.metric b{font-size:28px}.details{grid-template-columns:1fr}header{padding:20px}.toolbar label{width:100%}#count{margin-left:0}}[hidden]{display:none!important}
</style><header><strong>HMBOT / BENCHMARK LAB</strong><span>EXPERIMENT PLAN · 2026.10.30</span></header><main><div class="eyebrow">COFI / CROSS-PLATFORM MIGRATION</div><h1>阶段1-所有model harness组合的A2H实验</h1><p class="intro">五种模型，两个 Harness，再加一组 Codex + GPT 对照。先锁定实验组合与历史产物，再统一推进迁移和独立测试。本阶段复用六组历史结果、补跑五组；最多两台 Tart 并行。DeepSeek / GLM 仅在北京时间 20:00–08:00 启动，运行中的实验不中断。</p>
<div class="metrics"><div class="metric"><b>11</b><span>实验组合</span></div><div class="metric"><b>COMPLETED_COUNT</b><span>迁移自报完成（含历史）</span></div><div class="metric"><b>PENDING_COUNT</b><span>尚未完成组合</span></div></div>
<div class="toolbar"><label>状态 <select id="state"><option value="all">全部状态</option><option value="done">迁移自报完成</option><option value="planned">尚未完成</option></select></label><label>Harness <select id="harness"><option value="all">全部 Harness</option><option>DevEco Code</option><option>Claude Code</option><option>Codex CLI</option></select></label><label>搜索 <input id="search" type="search" placeholder="模型 / 镜像名称"></label><span id="count" aria-live="polite">11 组</span></div>
<div class="table-wrap"><table><caption hidden>11 组 Cofi 安卓到鸿蒙实验</caption><thead><tr><th>#</th><th>模型 / 标识</th><th>HARNESS / 版本</th><th>迁移与验收</th><th>结果镜像</th><th>备注</th></tr></thead><tbody>ROWS</tbody></table></div>
<div class="details"><section class="detail"><h2>实验口径</h2><ul><li>固定 Cofi Android 源码提交 <code>e3212d7090b0dd3d81ec5a31cb0b0641f68c865a</code>。</li><li>新实验每组独立 Tart、8 CPU / 8 GiB、图形化与可见 Terminal；每轮先归档再释放设备。</li><li>启动前锁定模型准确 ID、reasoning effort、Harness 版本、prompt SHA 与基础镜像。GPT 使用 gpt-6-astra，ChatGPT 登录；实际默认 reasoning effort 为 medium，按用户要求显式设置 high。</li><li>历史 Claude Code 为 2.1.267；不能将不同版本、prompt 或设备接口的结果当成完全等条件实验。已确认复用六组历史结果；其差异仍保留在记录中。</li></ul></section><section class="detail"><h2>状态与镜像说明</h2><ul><li>“迁移自报完成”只表示 agent 已交付，不表示测试通过。</li><li>10/27 历史 Claude Code 测试存在定位和观测阻塞，不展示为有效综合分数；Pro 采用 10/28 重测，未套用旧版评分。</li><li>已核对表中已完成结果克隆本地存在。当前没有已确认的远程下载地址或 OCI digest；本地名称不是公开镜像 URL。</li><li>下载地址字段预留在 JSON 中。发布前须另行准备已去除凭据的结果镜像，本页不上传 VM 磁盘或原始日志。</li></ul></section></div><footer>范围外历史项：OpenCode + GLM、Codex + GLM、DSH + GLM、双账号 Flash 实验不计入这 11 组。<br><a href="../data/cofi-android-harmony.json">实验数据 JSON</a> · <a href="cofi-android-harmony.md">GitHub 文档版</a> · 更新时间：2026-10-30（Asia/Shanghai）</footer></main>
<script>const rows=[...document.querySelectorAll('tbody tr')];const state=document.querySelector('#state'),harness=document.querySelector('#harness'),search=document.querySelector('#search');function filter(){let n=0;for(const row of rows){row.hidden=!((state.value==='all'||row.dataset.state===state.value)&&(harness.value==='all'||row.dataset.harness===harness.value)&&row.textContent.toLowerCase().includes(search.value.trim().toLowerCase()));if(!row.hidden)n++}document.querySelector('#count').textContent=n+' / 11 组'}for(const el of [state,harness,search])el.addEventListener('input',filter);</script></html>'''.replace('ROWS',''.join(rows)).replace('COMPLETED_COUNT',str(completed)).replace('PENDING_COUNT',str(pending))
# Retests are independent records; keep the original 11-row matrix unchanged.
retest_rows = []
if d.get('retests'):
    md += ['', '## 镜像与 Prompt 补测（独立记录）', '', '原11组结果保留；本批用户授权立即启动，豁免夜间窗口。', '', '| 模型 | 状态 | 基础镜像 | 记录 |', '|---|---|---|---|']
    for x in d['retests']:
        harness_label = x['harness']+' '+x['harness_version'] + (' / CLI '+x['cli_version'] if x.get('cli_version') else '')
        prompt_label = ' · Prompt '+x.get('prompt_version','v1')
        retest_rows.append('<tr><td><strong>'+e(x['model_family'])+'</strong><small>'+e(x['model_id'])+'</small></td><td>'+e(x['migration'])+'<small>'+e(x['evaluation'])+'</small></td><td><code>'+e(x['base_image'])+'</code><small>'+e(harness_label+prompt_label)+'</small></td><td>'+e(x['notes'])+'<small>任务开始：'+e(x['started_at'])+' · '+e(x['schedule_window'])+'</small><code>'+e(x['run_id'])+'</code><small>'+('结果克隆：'+e(x['result_image']) if x.get('result_image') else '结果待归档')+'</small></td></tr>')
        md.append('| '+' | '.join([x['model_family']+' / '+x['model_id'],x['migration']+'；'+x['evaluation'],'`'+x['base_image']+'`',x['notes']])+' |')
    section='<section style="margin-top:32px"><h2>镜像与 Prompt 补测 · '+e(d['updated'])+'</h2><p class="intro">独立补测记录，原11组及既有补测均保留。Prompt v2 新增高保真迁移要求；各组镜像、模板与启动例外见记录。结果克隆归档状态见各行；暂无已核实的远程下载地址。</p><div class="table-wrap"><table><thead><tr><th>模型</th><th>状态</th><th>基础镜像 / 版本</th><th>记录</th></tr></thead><tbody>'+''.join(retest_rows)+'</tbody></table></div></section>'
    page=page.replace('<div class="details">',section+'<div class="details">')
    page=page.replace("document.querySelectorAll('tbody tr')", "document.querySelectorAll('tr[data-state]')")
    page=page.replace('更新时间：2026-10-30','更新时间：'+d['updated'])
# Evaluation metrics stay separate from migration self-reports. Missing is not zero.
def metric_value(metrics, key):
    value = metrics.get(key)
    if value is None:
        return '待发布'
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f'Invalid metric {key}: {value!r}')
    if key.endswith('_score'):
        if value > 100:
            raise ValueError(f'{key} must be between 0 and 100')
        return f'{value:g} / 100'
    if not isinstance(value, int):
        raise ValueError(f'{key} must be an integer')
    if key == 'total_tokens':
        return f'{value:,}'
    hours, remainder = divmod(value, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours}小时 {minutes}分 {seconds}秒' if hours else f'{minutes}分 {seconds}秒'

metric_keys = ('functional_score', 'ui_score', 'total_tokens', 'duration_seconds')
result_rows, result_md = [], []
for record in d['experiments'] + d.get('retests', []):
    values = [metric_value(record.get('metrics', {}), key) for key in metric_keys]
    model = record['model_family'] + ' / ' + record['model_id']
    harness = record['harness'] + ' ' + record['harness_version']
    run = record['run_id']
    metric_note = record.get('metrics_note') or '尚无可核实的指标记录。'
    result_rows.append('<tr><td><strong>'+e(model)+'</strong><small>'+e(harness)+'</small></td><td><code>'+e(run)+'</code></td>'+''.join('<td class="result-value'+(' muted' if value == '待发布' else '')+'">'+e(value)+'</td>' for value in values)+'<td class="notes">'+e(metric_note)+'</td></tr>')
    # Escape table delimiters even when model names contain Markdown characters.
    result_md.append('| '+' | '.join(str(value).replace('|', '&#124;').replace('\n', ' ') for value in [model, harness, run, *values, metric_note])+' |')
results_note = '功能分与 UI 分均为 0–100 分；Token 数为该次迁移运行消耗的总 Token（按对应 Harness 的统计口径），耗时为迁移任务从开始到结束的墙钟时间。未发布指标显示“待发布”，不记为 0；原始实验与补测按运行 ID 分别记录。Token 含缓存，不等于计费 Token；不同 Harness 的口径见各行。功能分含历史原始通过的行另行标注，不能直接排名。'
results_section = '<section id="migration-results" style="margin:32px 0"><h2>迁移测评结果</h2><p class="intro">'+e(results_note)+'</p><p><a href="../data/metrics-evidence.json">指标来源与安装包校验记录</a></p><div class="table-wrap"><table><caption hidden>迁移测评结果：功能分、UI 分、Token 数与迁移耗时</caption><thead><tr><th>模型 / HARNESS</th><th>运行 ID</th><th>功能分</th><th>UI 分</th><th>TOKEN 数</th><th>迁移耗时</th><th>评分与统计说明</th></tr></thead><tbody>'+''.join(result_rows)+'</tbody></table></div></section>'
page = page.replace('<div class="toolbar">', results_section+'<h2>迁移实验进度</h2><div class="toolbar">', 1)
page = page.replace("document.querySelectorAll('tbody tr')", "document.querySelectorAll('tr[data-state]')")
page = page.replace('.number{', '.result-value{white-space:nowrap;font-variant-numeric:tabular-nums}.number{')
progress_index = md.index('| 模型 / ID | Harness | 迁移状态 | 独立验收 | 结果镜像（本地 Tart） | 进度备注 |')
md[progress_index:progress_index] = ['## 迁移测评结果', '', results_note, '', '[指标来源与安装包校验记录](../data/metrics-evidence.json)', '', '| 模型 / ID | Harness | 运行 ID | 功能分 | UI 分 | Token 数 | 迁移耗时 | 评分与统计说明 |', '|---|---|---|---|---|---|---|---|', *result_md, '', '## 迁移实验进度', '']
(root/'experiments/cofi-android-harmony.html').write_text(page)
md += ['', '## 实验口径与待锁定项', '', '- 固定源码：`'+d['source_commit']+'`。每组独立 Tart，8 CPU / 8 GiB，图形化和可见 Terminal。', '- Codex 使用 gpt-6-astra + ChatGPT 登录；实际默认 reasoning effort 为 medium，按用户要求显式设置 high。DeepSeek / GLM 限北京时间 20:00–08:00 启动，最多两台 Tart 并行。', '- 六组历史完成记录已确认复用。历史 Claude Code 为 2.1.267，基础镜像与 prompt 存在差异，不能宣称完全等条件对照。', '- DeepSeek Pro 采用 10/28 重测；10/27 对旧版的测试不混入。其他历史测试存在定位/观测阻塞，不展示为有效综合分。', '- 镜像栏为已核实存在的本地 Tart 克隆名称；远程下载地址尚未提供。发布结果镜像前需去除凭据。本页未上传磁盘或原始日志。', '- OpenCode + GLM、Codex + GLM、DSH + GLM 和双账号实验不计入本矩阵。', '', '[结构化数据](../data/cofi-android-harmony.json) · [HTML 页面](cofi-android-harmony.html)', '']
(root/'experiments/cofi-android-harmony.md').write_text('\n'.join(md))

# App directory and interactive result views share the validated ledger and formatters.
from render_dashboard import render
render(d, metric_value)

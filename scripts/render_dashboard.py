"""Render the app directory and interactive, static result pages from the public ledger."""
import html
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
e = lambda value: html.escape(str(value), quote=True)


def batch_name(record, original=False):
    if record.get('batch') or record.get('batch_id'):
        return str(record.get('batch') or record['batch_id'])
    if original:
        return '阶段 1 · 原始 11 组'
    run = record['run_id']
    if 'skillopt-paired' in run:
        return '2026-11-06 · SkillOpt 配对复现'
    if 'skillopt' in run:
        return '2026-11-05 · SkillOpt 优化'
    if 'dw-' in run:
        return '2026-11-05 · DW 内置迁移'
    if 'deveco-v2-' in run:
        return '2026-11-03–04 · DevEco 镜像 v2 补测'
    date = re.search(r'20\d{6}', run)
    date = f'{date[0][:4]}-{date[0][4:6]}-{date[0][6:]}' if date else '日期未登记'
    return date + ' · ' + ('Prompt ' + str(record['prompt_version']) if record.get('prompt_version') else '独立补测')


def render(d, metric_value):
    apps = defaultdict(list)
    for original, records in [(True, d['experiments']), (False, d.get('retests', []))]:
        for record in records:
            row = dict(record)
            row['_batch'] = batch_name(row, original)
            app = row.get('app', 'Cofi')
            apps[app].append(row)
    slugs = {app: re.sub(r'[^a-z0-9]+', '-', app.lower()).strip('-') for app in apps}
    filenames = {app: ('cofi-android-harmony.html' if app == 'Cofi' else slugs[app]+'-android-harmony.html') for app in apps}
    def shell(title, body, prefix=''):
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} · HMBot Benchmark</title><link rel="stylesheet" href="{prefix}assets/dashboard.css"><script src="{prefix}assets/demo-access.js"></script><script defer src="{prefix}assets/dashboard.js"></script></head><body><header><strong>HMBOT / BENCHMARK</strong><a href="{prefix}index.html">全部 App ↗</a></header><main><div class="demo-notice">静态演示 · 登录仅控制界面跳转，不提供真实访问保护。访问记录仅保存在当前浏览器，不采集 IP。</div>{body}<footer>更新时间：{e(d['updated'])}（Asia/Shanghai）<br>结果来自独立运行记录；迁移自报完成不代表独立验收通过。<br><a href="https://github.com/mig-everything/hmbot-benchmark-dashboard">GitHub 仓库</a> · <a href="{prefix}access-logs.html">访问记录（本浏览器演示）</a><button type="button" data-demo-logout>退出演示账号</button></footer></main></body></html>'''
    login = '<div class="login-wrap"><div class="eyebrow">HMBOT / BENCHMARK</div><h1>登录迁移测评 Dashboard</h1><p class="intro">使用演示账号进入 App 目录。</p><form id="login-form"><label>Username<input name="username" autocomplete="username" required autofocus></label><label>Password<input name="password" type="password" autocomplete="current-password" required></label><p id="login-error" class="login-error" role="alert" aria-live="polite"></p><button class="primary" type="submit">登录</button></form><div class="demo-account">演示用户名：<strong>demo</strong><br>演示密码：<strong>demo123</strong><br>请勿输入真实账号密码。</div></div>'
    login_page = shell('演示登录', login)
    login_page = login_page.replace('<a href="index.html">全部 App ↗</a>', '<span>静态演示</span>')
    login_page = login_page.replace('<button type="button" data-demo-logout>退出演示账号</button>', '')
    (ROOT/'login.html').write_text(login_page)
    logs = '<div class="eyebrow">LOCAL VISIT HISTORY</div><h1>访问记录</h1><p class="intro">仅显示当前浏览器保存的演示访问记录。浏览器标识随机生成，不代表 IP 或真实身份；其他设备与访客的数据不可见。关闭标签页结束演示登录，清除浏览器数据会删除记录。</p><div class="log-actions"><span id="visit-status" role="status" aria-live="polite"></span><button type="button" id="clear-visits">清空本地记录</button></div><div class="table-wrap"><table><thead><tr><th>访问时间（北京时间）</th><th>演示用户</th><th>浏览器标识</th><th>IP</th><th>访问页面</th></tr></thead><tbody id="visit-rows"></tbody></table></div>'
    (ROOT/'access-logs.html').write_text(shell('访问记录 · 静态演示', logs))
    cards = []
    for app, records in apps.items():
        scored = sum(r.get('metrics', {}).get('functional_score') is not None for r in records)
        cards.append(f'''<a class="app-card" href="experiments/{filenames[app]}"><span class="app-icon">{e(app[0])}</span><h2>{e(app.replace('-', ' '))}</h2><p>Android → HarmonyOS<br>{len(records)} 次运行 · {len(set(r['harness'] for r in records))} 种 Harness</p><div><span class="badge {'good' if scored else 'warn'}">{str(scored)+' 次已有功能分' if scored else '待测评'}</span></div><span class="arrow">查看结果与运行记录 →</span></a>''')
    total = sum(len(rows) for rows in apps.values())
    (ROOT/'index.html').write_text(shell('迁移测评 · App 目录', f'''<div class="eyebrow">CROSS-PLATFORM MIGRATION</div><h1>每个 App，一份迁移成绩单。</h1><p class="intro">选择应用，比较不同模型、Harness 与实验批次的功能完备度、界面还原度和迁移成本。</p><div class="summary"><article><b>{len(apps)}</b><span>已登记 App</span></article><article><b>{total}</b><span>迁移运行记录</span></article><article><b>{sum(r.get('metrics',{}).get('functional_score') is not None for rows in apps.values() for r in rows)}</b><span>已有功能测评</span></article></div><div class="app-grid">{''.join(cards)}</div>'''))
    for app, records in apps.items():
        # The HTML itself is also ordered for readers without JavaScript.
        records.sort(key=lambda r: (r.get('metrics',{}).get('functional_score') is None, -(r.get('metrics',{}).get('functional_score') or 0), r['run_id']))
        def options(key):
            return ''.join(f'<option value="{e(value)}">{e(value)}</option>' for value in sorted(set(str(r[key]) for r in records)))
        rows = []
        for record in records:
            m = record.get('metrics', {})
            note = record.get('metrics_note') or '尚无可核实的测评指标。'
            historical = '历史原始通过' in note or '未按新' in note
            failed = any(word in record.get('migration','') for word in ['失败','耗尽','超限'])
            badges = ('<span class="badge warn">历史口径 · 谨慎比较</span>' if historical else '') + ('<span class="badge danger">迁移受阻 / 失败</span>' if failed else '')
            if m.get('functional_score') is None:
                badges += '<span class="badge warn">待测评</span>'
            if m.get('functional_score') == 0:
                badges += '<span class="badge danger">零确认通过 · 见说明</span>'
            attrs = {'model': record['model_id'], 'harness': record['harness'], 'batch': record['_batch'], 'run':record['run_id'], **{k: m.get(field) for k,field in [('functional','functional_score'),('ui','ui_score'),('tokens','total_tokens'),('duration','duration_seconds')]}}
            attributes = ' '.join(f'data-{key}="{e(value) if value is not None else ""}"' for key,value in attrs.items())
            cells = []
            for field in ['functional_score','ui_score','total_tokens','duration_seconds']:
                value = m.get(field)
                formatted = metric_value(m,field)
                if value is None:
                    cells.append('<td class="missing">待发布</td>')
                elif field.endswith('_score'):
                    color = 'high' if value >= 80 else 'mid' if value >= 50 else 'low'
                    cells.append(f'<td><div class="score {color}">{value:g}<small>/ 100 分</small></div><div class="bar"><span style="width:{value}%"></span></div></td>')
                else:
                    cells.append(f'<td class="numeric">{e(formatted)}</td>')
            details = f'''<details class="record-details"><summary>评分说明与运行记录</summary><p>{e(note)}</p><p><strong>迁移状态：</strong>{e(record.get('migration',''))}<br><strong>独立验收：</strong>{e(record.get('evaluation',''))}</p><p>{e(record.get('notes',''))}</p><p>运行 ID：<code>{e(record['run_id'])}</code><br>基础镜像：<code>{e(record.get('base_image','未登记'))}</code><br>结果镜像：<code>{e(record.get('result_image') or '未登记')}</code></p></details>'''
            rows.append(f'''<tr {attributes}><td><strong>{e(record['model_family'])}</strong><small>{e(record['model_id'])}</small>{badges}</td><td><span class="badge harness">{e(record['harness'])}</span><small>{e(record.get('harness_version',''))}</small></td><td>{e(record['_batch'])}<small>Prompt {e(record.get('prompt_version','v1'))}</small><small>{e(record['run_id'])}</small></td>{''.join(cells)}<td>{details}</td></tr>''')
        sort_headers = ''.join(f'<th aria-sort="{ "descending" if key=="functional" else "none"}"><button type="button" class="sort-head" data-sort="{key}" data-label="{label}">{label}{" ↓" if key=="functional" else " ↕"}</button></th>' for key,label in [('functional','功能完备度'),('ui','UI 分'),('tokens','Token 数'),('duration','迁移耗时')])
        scored = sum(r.get('metrics',{}).get('functional_score') is not None for r in records)
        content = f'''<div class="eyebrow">{e(app.upper())} / ANDROID → HARMONYOS</div><h1>{e(app.replace('-', ' '))} 迁移测评</h1><p class="intro">按模型、Harness 和实验批次查看结果。功能完备度为标准用例的确认通过比例，失败与受阻仍计入分母。原始实验与补测分别保留。</p><div class="summary"><article><b>{len(records)}</b><span>迁移运行</span></article><article><b>{scored}</b><span>已有功能测评</span></article><article><b>{len(set(r['_batch'] for r in records))}</b><span>实验批次</span></article></div>
<section id="migration-results"><h2>迁移测评结果</h2><div class="toolbar"><label>模型<select id="model"><option value="all">全部模型</option>{options('model_id')}</select></label><label>Harness<select id="harness"><option value="all">全部 Harness</option>{options('harness')}</select></label><label>实验批次<select id="batch"><option value="all">全部批次</option>{options('_batch')}</select></label><label>搜索<input id="search" type="search" placeholder="运行 ID、模型或备注"></label><label>排序指标<select id="sort"><option value="functional">功能完备度</option><option value="ui">UI 分</option><option value="tokens">Token 数</option><option value="duration">迁移耗时</option></select></label><label>排序方向<select id="direction"><option value="desc">从高到低</option><option value="asc">从低到高</option></select></label><button id="reset" type="button">重置</button></div><div class="result-meta"><span id="result-count" role="status" aria-live="polite">{len(records)} 次运行 · 功能完备度降序</span><a href="../data/metrics-evidence.json">指标来源与安装包校验记录 ↗</a></div><div class="table-wrap"><table><caption hidden>{e(app)} 迁移测评结果</caption><thead><tr><th>模型</th><th>Harness / 版本</th><th>实验批次 / 运行</th>{sort_headers}<th>说明与状态</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><p id="empty-results" class="empty" hidden>没有符合条件的运行记录。请调整筛选条件或点击重置。</p></section><p class="legend"><span class="badge good">80–100 分</span><span class="badge warn">50–79.9 分</span><span class="badge danger">低于 50 分</span> 色彩仅表示分数区间，不代表验收结论。缺失指标始终排在最后，0 分是有效值。</p><div class="method"><h2>如何阅读这些成绩</h2>默认按功能完备度降序展示，排序只调整查看顺序。历史原始通过、不同测试版本与覆盖范围仍需结合逐行说明比较；不能据此直接认定模型优劣。<br>Token 为原生日志记录的总量（可能含缓存、推理与子会话），不同 Harness 统计口径见说明。耗时为迁移运行时长，部分历史记录包含等待时间；未知值显示“待发布”。<br>批次优先读取记录的 batch / batch_id；未登记时按阶段或运行 ID 中的日期与 Prompt 分类。<br><a href="../data/cofi-android-harmony.json">结构化实验数据</a> · <a href="cofi-android-harmony.md">完整历史文档</a></div>'''
        (ROOT/'experiments'/filenames[app]).write_text(shell(app+' 迁移测评',content,'../'))

if __name__ == '__main__':
    raise SystemExit('Run python3 scripts/render.py to validate and generate all pages.')

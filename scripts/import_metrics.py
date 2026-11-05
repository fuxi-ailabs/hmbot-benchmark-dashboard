"""Import curated, version-matched local evidence; never copy raw sessions to the dashboard."""
import hashlib
import json
import re
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
LEDGER = ROOT / 'data/cofi-android-harmony.json'
ledger = json.loads(LEDGER.read_text())
records = {row['id']: row for row in ledger['experiments'] + ledger.get('retests', [])}
evidence = {}
for row in records.values():
    row['metrics_note'] = ''


def read(relative):
    return json.loads((WORKSPACE / relative).read_text())


def source_ref(relative):
    return {'path': str(relative), 'sha256': hashlib.sha256((WORKSPACE / relative).read_bytes()).hexdigest()}


# IDs in the later reports are stable comparison slots, NOT stable artifact versions.
# Explicitly map replaced GLM / Flash / Pro artifacts to their actual retest runs.
latest = 'benchmark-runs/cofi-eleven-rounds45-20261104/results.json'
previous = 'benchmark-runs/cofi-eleven-three-rounds-20261103/results.json'
latest_map = {
    'minimax-deveco': 'minimax-deveco', 'minimax': 'minimax-claude',
    'qwen-deveco': 'qwen-deveco', 'qwen': 'qwen-claude', 'glm': 'glm-claude',
    'deepseek-pro-claude': 'deepseek-pro-claude', 'deepseek': 'deepseek-flash-claude',
    'gpt-codex': 'gpt-codex',
    'glm-deveco': 'cofi-deveco-v2-glm-retest-20261103',
    'deepseek-flash-deveco': 'cofi-deveco-v2-flash-retest-20261103',
    'deepseek-pro-deveco': 'cofi-deveco-v2-deepseek-pro-retest-20261104',
}


def import_score(relative, result, target):
    row = records[target]
    artifact = result['artifact']
    # Named new runs must match the collected artifact path, even if the report ID does not.
    if row['run_id'].startswith(('s1-', 'cofi-deveco-v2-', 'cofi-deveco-pro-')):
        assert row['run_id'] in artifact['hap'], (target, artifact['hap'])
    hap = Path(artifact['hap'])
    actual_hash = hashlib.sha256(hap.read_bytes()).hexdigest()
    expected = artifact.get('hap_sha256') or artifact.get('sha256')
    assert expected is None or actual_hash == expected, target
    total = result.get('denominator', result.get('planned'))
    passed = result['passed']
    blocked = result.get('blocked', result.get('blocked_or_not_executed', 0))
    score = round(passed / total * 100, 1)
    assert score == result.get('functional_percent', result.get('verified_pass_percent_of_all_cases', score))
    ui = result['ui']
    row['metrics']['functional_score'] = score
    row['metrics']['ui_score'] = ui['score_percent']
    kind = result.get('baseline_kind', 'verified')
    note = f'通过 {passed}/{total}；受阻 {blocked}；UI {ui.get("pages", ui.get("pages_scored"))} 页。'
    if kind == 'historical_raw':
        note += '含历史原始通过，未按新标准全部复核，不参与直接排名。'
    elif passed == 0 and blocked == total:
        note += '全部因前置条件受阻；0% 表示确认通过占比，不表示全部功能失败。'
    else:
        note += '功能分为确认通过占全部用例的比例，受阻计入分母。'
    ui_note = result.get('ui_note', '')
    ui_source = str(ui.get('source', ui.get('origin', relative))).removeprefix(str(WORKSPACE) + '/')
    source_date = re.search(r'20\d{6}', ui_source)
    ui_date = datetime.strptime(source_date[0], '%Y%m%d').date().isoformat() if source_date else '日期见来源'
    note += f'UI 来源记录日期：{ui_date}。'
    if '既有' in ui_note:
        note += 'UI 沿用同一安装包既有评分。'
    row['metrics_note'] = note
    row['evaluation'] = '已有独立测试记录；仍有受阻或待复核项，未判定全部验收通过'
    evidence[target] = {
        'run_id': row['run_id'], 'score_source': source_ref(relative),
        'hap_sha256': actual_hash, 'benchmark_commit': result.get('benchmark_commit', '6963291214b1ae2b856d7737a39fd251cf7ee749'),
        'functional': {'passed': passed, 'total': total, 'blocked': blocked, 'basis': kind},
        'ui': {'source_record_date': ui_date, 'score': ui['score_percent'], 'pages': ui.get('pages', ui.get('pages_scored')), 'note': ui_note,
               'source_path': str(ui.get('source', ui.get('origin', relative))).removeprefix(str(WORKSPACE) + '/')},
    }
    usage = result.get('migration_usage')
    if usage:
        row['metrics']['total_tokens'] = usage['input_tokens'] + usage['output_tokens']
        timing = usage.get('timing', {})
        # log_span includes user wait; active time deliberately does not stand in for wall time.
        span = timing.get('log_span_ms')
        if span is None and timing.get('inactive_ms') == 0:
            span = timing.get('active_ms')
        if span is not None:
            row['metrics']['duration_seconds'] = round(span / 1000)
        evidence[target]['usage'] = {'source': source_ref(Path(usage['source']).relative_to(WORKSPACE)),
                                    'input_tokens': usage['input_tokens'], 'output_tokens': usage['output_tokens'],
                                    'wall_span_ms': span, 'definition': '输入（含缓存读取/写入）+输出；日志跨度含人工等待。'}
        row['metrics_note'] += 'Token 含缓存；耗时为日志跨度（含人工等待）。'


for result in read(latest)['artifacts']:
    import_score(latest, result, latest_map[result['artifact']['id']])
# The original Pro is not the Pro retest artifact used in rounds 4–5.
for result in read(previous)['artifacts']:
    if result['artifact']['id'] == 'deepseek-pro-deveco':
        import_score(previous, result, 'deepseek-pro-deveco')
for relative, target in [
    ('benchmark-runs/cofi-blockers-20261031/glm-deveco/results.json', 'glm-deveco'),
    ('benchmark-runs/cofi-stage1-completion-20261102/deepseek-flash-deveco/results.json', 'deepseek-flash-deveco'),
]:
    import_score(relative, read(relative), target)

# Sum per-response native usage once, including archived child sessions from this run only.
# Preflight sessions and sessions outside this migration working directory are excluded.
for target, row in records.items():
    run = row['run_id']
    folder = WORKSPACE / 'experiments' / run
    manifest_path = folder / 'manifest.json'
    if not manifest_path.exists():
        continue
    manifest = json.loads(manifest_path.read_text())
    snapshots = sorted(folder.glob('collected-*/native-sessions.json'))
    if not snapshots and (folder / 'collected/native-session.json').exists():
        snapshots = [folder / 'collected/native-session.json']
    if not snapshots:
        continue
    snapshot = snapshots[-1]
    snapshot_data = json.loads(snapshot.read_text())
    sessions = snapshot_data.get('sessions', {})
    if 'messages' in snapshot_data:
        sessions = {manifest.get('formal_session_id', manifest.get('session_id', run)): snapshot_data}
        assert not snapshot_data.get('descendants'), 'Import descendant usage explicitly'
    total_tokens, count, starts, ends, included = 0, 0, [], [], []
    for sid, session in sessions.items():
        messages = [json.loads(message[1]) for message in session.get('messages', [])]
        if not messages:
            continue
        assistants = [m for m in messages if m.get('role') == 'assistant']
        if not assistants or any(run not in m.get('path', {}).get('cwd', '') for m in assistants):
            continue
        included.append(sid)
        for message in messages:
            time = message.get('time', {})
            if time.get('created') is not None:
                starts.append(time['created'])
            if time.get('completed') is not None:
                ends.append(time['completed'])
            tokens = message.get('tokens', {})
            if message.get('role') == 'assistant' and tokens.get('total', 0) > 0:
                total_tokens += tokens['total']
                count += 1
    if count:
        row['metrics']['total_tokens'] = total_tokens
        if starts and ends:
            row['metrics']['duration_seconds'] = round((max(ends) - min(starts)) / 1000)
        entry = evidence.setdefault(target, {'run_id': run})
        entry['usage'] = {'source': source_ref(snapshot.relative_to(WORKSPACE)), 'session_ids': included,
                          'responses': count, 'total_tokens': total_tokens,
                          'definition': '原生逐响应 tokens.total 求和，包含同轮子会话；含缓存，推理按 Harness 原生口径；正式会话首条消息至最后响应完成，秒四舍五入。'}
        row['metrics_note'] = row.get('metrics_note', '') + 'Token 含缓存及同轮子会话；耗时取正式会话首条消息至最后响应完成。'
    # Codex publishes cumulative total usage; use the final value, never sum snapshots.
    rollouts = sorted(snapshot.parent.glob('native-rollouts/*.jsonl'))
    if row['harness'] == 'Codex CLI' and rollouts:
        last_usage = None
        for line in rollouts[0].open():
            event = json.loads(line)
            payload = event.get('payload', {})
            if event.get('type') == 'event_msg' and payload.get('type') == 'token_count':
                last_usage = (payload.get('info') or {}).get('total_token_usage') or last_usage
        if last_usage:
            row['metrics']['total_tokens'] = last_usage['total_tokens']
            start, end = manifest.get('task_started_at'), manifest.get('completion_observed_at')
            if start and end:
                row['metrics']['duration_seconds'] = round((datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds())
            evidence.setdefault(target, {'run_id': run})['usage'] = {
                'source': source_ref(rollouts[0].relative_to(WORKSPACE)),
                'total_token_usage': last_usage,
                'definition': '最后一条累计 total_tokens（包含缓存；推理已含于输出，不重复相加）；任务开始至完成被观察到的墙钟时长。',
                'start': start, 'end': end,
            }
            row['metrics_note'] = row.get('metrics_note', '') + 'Token 采用最终累计值（含缓存）；耗时截至观察到完成，可能含观察延迟。'

ledger['updated'] = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M CST')
LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'data/metrics-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
for row in records.values():
    print(row['id'], row['metrics'])

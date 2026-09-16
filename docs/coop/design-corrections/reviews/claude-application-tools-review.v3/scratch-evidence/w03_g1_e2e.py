"""W03: G1 end-to-end through the actual retainer - authored report retention for Claude,
same-name stdout exclusion, Grok unchanged. Invented sentinels only.
"""
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(INPUTS))
spec = importlib.util.spec_from_file_location(
    'retain_app', INPUTS / 'retain-application-review.successor.v1.py')
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

SENT = 'SYNTHETIC-INVENTED-PRIVATE-MARKER-DO-NOT-RETAIN'
DESIGN_S, BLIND_S, FRESH_S = ('aaaaaaaa-0000-4000-8000-000000000001',
                              'bbbbbbbb-0000-4000-8000-000000000002',
                              'ffffffff-0000-4000-8000-00000000000f')
CLAUDE_LOG = json.dumps({'uuid': 'u1', 'timestamp': 't1', 'message': {'content': [
    {'type': 'thinking', 'thinking': SENT + '-session-log'},
    {'type': 'tool_use', 'id': 'tu1', 'name': 'Read', 'input': {'file_path': '/x'}}]}})
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows = []


def run(ident, *, stdout_name='response.json', authored=None):
    with tempfile.TemporaryDirectory(prefix='opensip-g1-') as td:
        base = Path(td)
        root, stage, src = base / 'root', base / 'stage', base / 'src'
        (stage / 'files/docs').mkdir(parents=True)
        (stage / 'files/docs/x.md').write_text('synthetic staged doc\n')
        src.mkdir(parents=True)
        manifest = {'standing': 'SYNTHETIC', 'retainedManifestPath': 'm.json',
                    'files': [{'path': 'docs/x.md', 'sha256': sha(stage / 'files/docs/x.md'),
                               'bytes': (stage / 'files/docs/x.md').stat().st_size}],
                    'beforeImages': [], 'support': []}
        mp = stage / 'application-subject.v3.json'
        mp.write_text(json.dumps(manifest, indent=2) + '\n')
        digest = sha(mp)
        root.mkdir(parents=True, exist_ok=True)
        (root / 'm.json').write_bytes(mp.read_bytes())
        (src / 'review.json').write_text(json.dumps(
            {'verdict': 'ACCEPT', 'subjectManifestSha256': digest,
             'newMustIssues': [], 'newShouldIssues': []}))
        (src / Path(stdout_name).name).write_text(json.dumps(
            {'is_error': False, 'session_id': FRESH_S, 'result': 'public',
             'thinking': SENT + '-cli-envelope'}))
        (src / 'prompt.txt').write_text('p\n')
        for rel, body in (authored or {}).items():
            q = src / rel
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text(body)
        bound = {'vendor': 'claude', 'launch': {'stdoutName': stdout_name},
                 'independentDesignReview': {'sessionId': DESIGN_S},
                 'freshBlindConsumerReview': {'sessionId': BLIND_S}}
        dest = base / 'dest'
        R.run_retain(root=root, stage=stage, version='v3', bound=bound, dest=dest,
                     src=src, claude_log_text=CLAUDE_LOG)
        custody = json.loads((dest / 'custody.json').read_text())
        retained = sorted(str(q.relative_to(dest)) for q in dest.rglob('*') if q.is_file())
        leak = [str(q.relative_to(dest)) for q in dest.rglob('*')
                if q.is_file() and SENT.encode() in q.read_bytes()]
        rows.append({'id': ident, 'stdoutName': stdout_name, 'retained': retained,
                     'excludedPrivateSources': custody['excludedPrivateSources'],
                     'sentinelLeak': leak})
        return rows[-1]


# G1 target case: a Claude reviewer's authored summary.json / plan.json must be retained,
# while other conservative private names stay excluded.
a = run('claude-authored-reports', authored={
    'summary.json': '{"authored":"reviewer summary"}',
    'plan.json': '{"authored":"reviewer plan"}',
    'review.md': '# authored review\n',
    'system_prompt.txt': 'conservative private name\n',
    'events.jsonl': '{"private":1}\n',
    'work/probe.py': 'print(1)\n',
    'work/compaction/note.txt': 'nested private dir\n',
})
# Same-name stdout exclusion: launch.stdoutName == summary.json must still be excluded.
b = run('stdout-named-summary-json', stdout_name='summary.json', authored={
    'plan.json': '{"authored":"reviewer plan"}',
    'review.md': '# authored review\n',
})

checks = [
    ('authored-summary.json-retained', 'summary.json' in a['retained']),
    ('authored-plan.json-retained', 'plan.json' in a['retained']),
    ('authored-review.md-retained', 'review.md' in a['retained']),
    ('authored-work-probe-retained', 'work/probe.py' in a['retained']),
    ('system_prompt.txt-still-excluded', 'system_prompt.txt' in a['excludedPrivateSources']
     and 'system_prompt.txt' not in a['retained']),
    ('events.jsonl-still-excluded', 'events.jsonl' in a['excludedPrivateSources']
     and 'events.jsonl' not in a['retained']),
    ('nested-private-dir-still-excluded', 'work/compaction/note.txt' in a['excludedPrivateSources']
     and 'work/compaction/note.txt' not in a['retained']),
    ('raw-stdout-response.json-excluded-then-sanitised',
     'response.json' in a['excludedPrivateSources'] and 'response.json' in a['retained']),
    ('no-sentinel-leak-case-a', a['sentinelLeak'] == []),
    ('stdout-named-summary.json-excluded-then-sanitised',
     'summary.json' in b['excludedPrivateSources'] and 'summary.json' in b['retained']),
    ('plan.json-still-retained-when-stdout-is-summary',
     'plan.json' in b['retained']),
    ('no-sentinel-leak-case-b', b['sentinelLeak'] == []),
]
result = [{'id': i, 'passed': bool(v)} for i, v in checks]
(HERE / 'w03_g1_e2e.result.json').write_text(
    json.dumps({'observations': rows, 'checks': result}, indent=2) + '\n')
bad = [r['id'] for r in result if not r['passed']]
print('G1 end-to-end:', len(result), 'checks,', len(result) - len(bad), 'passed, failed=', bad)
for r in rows:
    print()
    print(r['id'], '| stdoutName =', r['stdoutName'])
    print('  retained :', r['retained'])
    print('  excluded :', r['excludedPrivateSources'])
    print('  leak     :', r['sentinelLeak'])

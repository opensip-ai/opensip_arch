"""V07: cohesion of the changed code.

(a) The F3 fix applies the Grok private-basename list to the Claude path too. Does that
    over-exclude a Claude reviewer's own authored output, and is any exclusion declared?
(b) The retained Claude envelope must still re-decode after sanitization.
(c) No __pycache__ or any other new entry was created inside either inputs tree.
"""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / 'inputs'
sys.path.insert(0, str(INPUTS))
import retain_public as P  # noqa: E402
import review_envelope as E  # noqa: E402

spec = importlib.util.spec_from_file_location(
    'retain_app', INPUTS / 'retain-application-review.successor.v1.py')
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
out = {}

DESIGN_S, BLIND_S, FRESH_S = ('aaaaaaaa-0000-4000-8000-000000000001',
                              'bbbbbbbb-0000-4000-8000-000000000002',
                              'ffffffff-0000-4000-8000-00000000000f')
CLAUDE_LOG = json.dumps({'uuid': 'u1', 'timestamp': 't1', 'message': {'content': [
    {'type': 'tool_use', 'id': 'tu1', 'name': 'Read', 'input': {'file_path': '/x'}}]}})


def retain_with(extra_files):
    td = tempfile.mkdtemp(prefix='opensip-cohesion-')
    base = Path(td)
    root, stage, src = base / 'root', base / 'stage', base / 'src'
    (stage / 'files/docs').mkdir(parents=True)
    (stage / 'files/docs/x.md').write_text('synthetic staged doc\n')
    src.mkdir(parents=True)
    sh = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    manifest = {'standing': 'SYNTHETIC', 'retainedManifestPath': 'm.json',
                'files': [{'path': 'docs/x.md', 'sha256': sh(stage / 'files/docs/x.md'),
                           'bytes': (stage / 'files/docs/x.md').stat().st_size}],
                'beforeImages': [], 'support': []}
    mp = stage / 'application-subject.v3.json'
    mp.write_text(json.dumps(manifest, indent=2) + '\n')
    digest = sh(mp)
    (root).mkdir(parents=True, exist_ok=True)
    (root / 'm.json').write_bytes(mp.read_bytes())
    (src / 'review.json').write_text(json.dumps({
        'verdict': 'ACCEPT', 'subjectManifestSha256': digest,
        'newMustIssues': [], 'newShouldIssues': []}))
    (src / 'response.json').write_text(json.dumps(
        {'is_error': False, 'session_id': FRESH_S, 'result': 'public', 'type': 'result',
         'thinking': 'SYNTHETIC-INVENTED-MARKER'}))
    (src / 'prompt.txt').write_text('p\n')
    for rel, body in extra_files.items():
        q = src / rel
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_text(body)
    bound = {'vendor': 'claude', 'launch': {'stdoutName': 'response.json'},
             'independentDesignReview': {'sessionId': DESIGN_S},
             'freshBlindConsumerReview': {'sessionId': BLIND_S}}
    res = R.run_retain(root=root, stage=stage, version='v3', bound=bound,
                       dest=base / 'dest', src=src, claude_log_text=CLAUDE_LOG)
    dest = base / 'dest'
    custody = json.loads((dest / 'custody.json').read_text())
    return {'retained': sorted(str(q.relative_to(dest)) for q in dest.rglob('*') if q.is_file()),
            'excludedPrivateSources': custody['excludedPrivateSources'],
            'destPath': str(dest), 'result': res}

# (a) authored outputs whose basenames collide with the Grok private list
r = retain_with({'summary.json': '{"authored":"reviewer summary"}',
                 'plan.json': '{"authored":"reviewer plan"}',
                 'review.md': '# authored review\n',
                 'work/probe.py': 'print(1)\n'})
out['a_claudeOverExclusion'] = {
    'retained': r['retained'],
    'excludedPrivateSources': r['excludedPrivateSources'],
    'authoredSummaryJsonRetained': 'summary.json' in r['retained'],
    'authoredPlanJsonRetained': 'plan.json' in r['retained'],
    'exclusionIsDeclaredInCustody': bool(r['excludedPrivateSources']),
    'reviewMdRetained': 'review.md' in r['retained'],
}

# (b) sanitized retained envelope must still re-decode as a public Claude envelope
env_path = Path(r['destPath']) / 'response.json'
body = json.loads(env_path.read_text())
try:
    decoded = E.decode_public(body, 'claude')
    ok, detail = decoded['sessionId'] == FRESH_S, decoded
except Exception as e:  # noqa: BLE001
    ok, detail = False, str(e)
out['b_sanitizedEnvelopeReDecodes'] = {'passed': bool(ok), 'keysRetained': sorted(body),
                                       'privateKeyGone': 'thinking' not in body, 'detail': str(detail)[:160]}

# (c) neither inputs tree gained any entry
V1I = Path('/tmp/opensip-design-corrections/claude-application-tools-review.v1/inputs')
checks = {}
for label, d, manifest_path in [
        ('v2', INPUTS, INPUTS.parent / 'input-manifest.json'),
        ('v1', V1I, V1I.parent / 'input-manifest.json')]:
    listed = {x['path'].split('/')[0] for x in json.loads(manifest_path.read_text())['files']}
    actual = set(os.listdir(d))
    checks[label] = {'unlistedEntries': sorted(actual - listed),
                     'pycachePresent': '__pycache__' in actual}
out['c_inputsTreesClean'] = checks

(HERE / 'v07_cohesion.result.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))

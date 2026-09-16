"""Compare this review's own six pinned groups and 17 evaluator3 children with the header-named current source43 reference
(codex-post-reset final-reference.v43; actual root execution root-source43-final-reference.v1), and with this reviewer's own
historical source42 receipts (read-only; never relabelled). Evidence comparison only; this review's own execution on the verified
source43 archive copy is the acceptance input. Writes only receipts/reference-comparison.json."""
import glob, hashlib, json, os
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
MINE = RT / 'receipts/reference'
CODEX = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v43')
ROOT = Path('/tmp/opensip-design-corrections/root-source43-final-reference.v1')
MINE42 = Path('/tmp/opensip-design-corrections/claude-independent-design.v42/receipts/reference')


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None


out = {'codexReferenceChecks': {'path': str(CODEX / 'reference-checks.json'), 'sha256': sha(CODEX / 'reference-checks.json'),
                                'expected': '213b81d0e17bc713a39e84941537935c33e5dc82283148cca915f994ea56aea7'},
       'codexFiles': sorted(os.listdir(CODEX)),
       'rootReferenceChecks': {'path': str(ROOT / 'reference-checks.json'), 'sha256': sha(ROOT / 'reference-checks.json')}}
out['codexEqualsRootReferenceChecks'] = sha(CODEX / 'reference-checks.json') == sha(ROOT / 'reference-checks.json')
codex = json.load(open(CODEX / 'reference-checks.json'))
root = json.load(open(ROOT / 'reference-checks.json'))
out['codexPassed'], out['codexSubjectManifestSha256'] = codex.get('passed'), codex.get('subjectManifestSha256')
out['rootPassed'], out['rootSubjectManifestSha256'] = root.get('passed'), root.get('subjectManifestSha256')
out['rootExecutionSourceRoots'] = sorted({c['command'][3].split('/docs/')[0] for c in root.get('commands', []) if len(c.get('command', [])) > 3})
cmds = root.get('commands', [])
mine = json.load(open(MINE / 'groups-report.all.json'))
mine42 = json.load(open(MINE42 / 'groups-report.all.json')) if (MINE42 / 'groups-report.all.json').exists() else {'rows': []}
out['mineRows'] = [(r['name'], r['exitCode'], r['stdoutSha256'], r['scriptMatchesManifest']) for r in mine['rows']]
out['mineCopyBefore'], out['mineCopyAfter'], out['minePassed'] = mine.get('before'), mine.get('after'), mine.get('passed')
cmp = {}
for name, code, s, _ in out['mineRows']:
    c = next((x for x in cmds if x.get('name') == name), None)
    m42 = next((x for x in mine42['rows'] if x['name'] == name), None)
    cmp[name] = {'mineExit': code, 'rootExit': (c or {}).get('exitCode'), 'rootSourceShaEqualsMineScript': (c or {}).get('sourceSha256') == next(r['scriptSha256'] for r in mine['rows'] if r['name'] == name),
                 'stdoutShaEqualRootRecord': (c or {}).get('stdoutSha256') == s,
                 'stdoutFileEqualRoot': sha(ROOT / (name + '.stdout')) == sha(MINE / (name + '.stdout')),
                 'stdoutFileEqualCodex': sha(CODEX / (name + '.stdout')) == sha(MINE / (name + '.stdout')) if (CODEX / (name + '.stdout')).exists() else None,
                 'historicalMine42Exit': (m42 or {}).get('exitCode'), 'stdoutEqualHistoricalMine42': (m42 or {}).get('stdoutSha256') == s}
out['groups'] = cmp
children = {}
for f in sorted(glob.glob(str(MINE / 'evaluator3' / '*.stdout'))):
    n = os.path.basename(f)
    children[n] = {'mine': sha(f), 'root': sha(ROOT / 'evaluator3' / n), 'historicalMine42': sha(MINE42 / 'evaluator3' / n)}
    children[n]['equalRoot'] = children[n]['mine'] == children[n]['root']
    children[n]['equalHistoricalMine42'] = children[n]['mine'] == children[n]['historicalMine42']
out['children'] = children
out['childCount'] = len(children)
out['childrenEqualRoot'] = sum(1 for v in children.values() if v['equalRoot'])
out['childrenEqualHistoricalMine42'] = sorted(k for k, v in children.items() if v['equalHistoricalMine42'])
out['childrenDifferingFromHistoricalMine42'] = sorted(k for k, v in children.items() if not v['equalHistoricalMine42'])
for label, path in (('mine', MINE / 'evaluator3/report.json'), ('root', ROOT / 'evaluator3/report.json')):
    try:
        rep = json.load(open(path))
        out['evaluator3Report_' + label] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__ + str(len(v))) for k, v in rep.items()}
    except Exception as exc:  # noqa: BLE001
        out['evaluator3Report_' + label] = 'unreadable:' + type(exc).__name__
for label, base in (('mine', MINE), ('root', ROOT)):
    try:
        qr = json.load(open(base / 'evaluator3/query-projection.receipt.json'))
        out['queryReceipt_' + label] = {k: qr.get(k) for k in ('total', 'passed', 'failed', 'checks', 'exitCode', 'count') if k in qr} or {k: type(v).__name__ for k, v in qr.items()}
    except Exception as exc:  # noqa: BLE001
        out['queryReceipt_' + label] = 'unreadable:' + type(exc).__name__
(RT / 'receipts/reference-comparison.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k not in ('children', 'mineRows')}, indent=1)[:9000])
print(json.dumps({k: (v['equalRoot'], v['equalHistoricalMine42']) for k, v in children.items()}))

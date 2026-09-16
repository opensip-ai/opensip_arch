"""Compare this review's own six pinned groups and 17 evaluator3 children with the header-named current source42 reference run
(codex-post-reset final-reference.v42, actual final execution root-source42-final-reference.v3). Evidence comparison only; this
review's own execution is the acceptance input. Writes only receipts/reference-comparison.json."""
import glob, hashlib, json, os
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
MINE = RT / 'receipts/reference'
CODEX = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v42')
ROOT3 = Path('/tmp/opensip-design-corrections/root-source42-final-reference.v3')


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None


out = {'codexReferenceChecks': {'path': str(CODEX / 'reference-checks.json'), 'sha256': sha(CODEX / 'reference-checks.json'),
                                'expected': 'd46d0bf272dbcc471e1d8d41c5a4eae9d2b8b864669c2c3c96d9cb58e814292b'},
       'codexFiles': sorted(os.listdir(CODEX)),
       'rootV3ReferenceChecks': {'path': str(ROOT3 / 'reference-checks.json'), 'sha256': sha(ROOT3 / 'reference-checks.json')}}
out['codexRunnerOriginalEqualsRootV3'] = sha(CODEX / 'runner-original-reference-checks.json') == sha(ROOT3 / 'reference-checks.json') if (CODEX / 'runner-original-reference-checks.json').exists() else None
codex = json.load(open(CODEX / 'reference-checks.json'))
root3 = json.load(open(ROOT3 / 'reference-checks.json'))
out['codexTopKeys'] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__ + str(len(v))) for k, v in codex.items()}
out['root3TopKeys'] = {k: (v if not isinstance(v, (list, dict)) else type(v).__name__ + str(len(v))) for k, v in root3.items()}
out['codexPassed'] = codex.get('passed')
out['codexSubjectManifestSha256'] = codex.get('subjectManifestSha256')
out['root3Passed'] = root3.get('passed')
out['root3SubjectManifestSha256'] = root3.get('subjectManifestSha256')
cmds = codex.get('commands', [])
out['codexCommands'] = [(c.get('name'), c.get('exitCode'), c.get('stdoutSha256')) for c in cmds]
mine = json.load(open(MINE / 'groups-report.all.json'))
out['mineRows'] = [(r['name'], r['exitCode'], r['stdoutSha256']) for r in mine['rows']]
cmp = {}
for name, code, s in out['mineRows']:
    c = next((x for x in cmds if x.get('name') == name), None)
    cmp[name] = {'mineExit': code, 'codexExit': c.get('exitCode') if c else None, 'stdoutShaEqualCodexRecord': (c or {}).get('stdoutSha256') == s,
                 'stdoutFileEqualCodex': sha(CODEX / (name + '.stdout')) == sha(MINE / (name + '.stdout')),
                 'stdoutFileEqualRootV3': sha(ROOT3 / (name + '.stdout')) == sha(MINE / (name + '.stdout'))}
out['groups'] = cmp
children = {}
for f in sorted(glob.glob(str(MINE / 'evaluator3' / '*.stdout'))):
    n = os.path.basename(f)
    children[n] = {'mine': sha(f), 'codex': sha(CODEX / 'evaluator3' / n), 'rootV3': sha(ROOT3 / 'evaluator3' / n)}
    children[n]['equalCodex'] = children[n]['mine'] == children[n]['codex']
    children[n]['equalRootV3'] = children[n]['mine'] == children[n]['rootV3']
    if not children[n]['equalRootV3'] and os.path.exists(ROOT3 / 'evaluator3' / n):
        try:
            a, b = json.load(open(f)), json.load(open(ROOT3 / 'evaluator3' / n))
            children[n]['differingTopKeys'] = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
        except Exception as exc:  # noqa: BLE001
            children[n]['differingTopKeys'] = 'nonjson:' + type(exc).__name__
out['children'] = children
out['childrenEqualCodex'] = sum(1 for v in children.values() if v['equalCodex'])
out['childrenEqualRootV3'] = sum(1 for v in children.values() if v['equalRootV3'])
(RT / 'receipts/reference-comparison.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ('codexReferenceChecks', 'codexFiles', 'codexPassed', 'codexSubjectManifestSha256', 'root3Passed', 'root3SubjectManifestSha256',
                                      'codexRunnerOriginalEqualsRootV3', 'groups', 'childrenEqualCodex', 'childrenEqualRootV3')}, indent=1))
print(json.dumps({k: (v['equalCodex'], v['equalRootV3'], v.get('differingTopKeys')) for k, v in children.items()}))

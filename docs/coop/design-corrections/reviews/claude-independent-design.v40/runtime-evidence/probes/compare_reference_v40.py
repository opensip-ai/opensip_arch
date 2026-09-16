"""Compare this review's own six pinned groups and 17 evaluator3 children with the header-named current source40 reference run
(codex-post-reset final-reference.v40, original execution root-source40-final-reference.v2). Evidence comparison only; this
review's own execution is the acceptance input. Writes only receipts/reference-comparison.json."""
import glob, hashlib, json, os
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40')
MINE = RT / 'receipts/reference'
CODEX = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v40')
ROOT2 = Path('/tmp/opensip-design-corrections/root-source40-final-reference.v2')


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None


out = {'codexReferenceChecks': {'path': str(CODEX / 'reference-checks.json'), 'sha256': sha(CODEX / 'reference-checks.json'),
                                'expected': '019c339765e3003d6a94bf95b8903d39caf01f7a04a1bba9e6b1d0549cfeb224'},
       'rootOriginal': {'path': str(ROOT2 / 'reference-checks.json'), 'sha256': sha(ROOT2 / 'reference-checks.json')},
       'codexRunnerOriginalEqualsRootOriginal': sha(CODEX / 'runner-original-reference-checks.json') == sha(ROOT2 / 'reference-checks.json')}
codex = json.load(open(CODEX / 'reference-checks.json'))
out['codexPassed'] = codex.get('passed')
out['codexSubjectManifestSha256'] = codex.get('subjectManifestSha256')
out['codexCommands'] = [(c.get('name'), c.get('exitCode'), c.get('stdoutSha256')) for c in codex.get('commands', [])]
mine = json.load(open(MINE / 'groups-report.all.json'))
out['mineRows'] = [(r['name'], r['exitCode'], r['stdoutSha256']) for r in mine['rows']]
cmp = {}
for name, code, s in out['mineRows']:
    c = next((x for x in codex.get('commands', []) if x.get('name') == name), None)
    cmp[name] = {'mineExit': code, 'codexExit': c.get('exitCode') if c else None, 'stdoutEqual': (c or {}).get('stdoutSha256') == s,
                 'codexStdoutFileEqual': sha(CODEX / (name + '.stdout')) == hashlib.sha256(open(MINE / (name + '.stdout'), 'rb').read()).hexdigest()}
out['groups'] = cmp
children = {}
for f in sorted(glob.glob(str(MINE / 'evaluator3' / '*.stdout'))):
    n = os.path.basename(f)
    children[n] = {'mine': sha(f), 'codex': sha(CODEX / 'evaluator3' / n), 'root': sha(ROOT2 / 'evaluator3' / n)}
    children[n]['equalCodex'] = children[n]['mine'] == children[n]['codex']
out['children'] = children
out['childrenEqual'] = sum(1 for v in children.values() if v['equalCodex'])
(RT / 'receipts/reference-comparison.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ('codexReferenceChecks', 'codexPassed', 'codexSubjectManifestSha256', 'codexRunnerOriginalEqualsRootOriginal', 'groups', 'childrenEqual')}, indent=1))
print(json.dumps({k: v['equalCodex'] for k, v in children.items()}))

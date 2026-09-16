"""p04 [final]: read-only deliverable summary.

- touched files: every byte difference between work/baseline and work/edited (added/removed included), with before
  (source38 manifest) and after SHA-256; the full unified correction diff written to proposed-edits.diff;
- frozen custody: touched and dependency files re-hashed in candidate-subject.v38 against the manifest; review and
  A5 inputs re-hashed against p00; edited dependency files equal to source38;
- binding drift: every non-review file in the baseline tree containing a touched file's before-hash, and the
  planning contract-section selectors (heading, line range, text) that change;
- results: latest p01 edited reports (run-termination rows incl. the composition cases, source38 carrier checks),
  p03 discrimination results, a5 receipts, and every receipt's exit.
With argv[1] == 'final', also digests review.md/review.json. Output: receipts/p04-summary[.final].json.
"""
import difflib, hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v38')
MAN = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json')
REV = Path('/tmp/opensip-design-corrections/claude-independent-design.v38')
A5 = Path('/tmp/opensip-design-corrections/root-consumer24-js-options.v1')
B, E = BASE / 'work' / 'baseline', BASE / 'work' / 'edited'
R = BASE / 'receipts'
final = len(sys.argv) > 1 and sys.argv[1] == 'final'
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(p.read_bytes())
manifest = {r['path']: r for r in json.loads(MAN.read_text())['files']}
out = {'standing': 'read-only summary of this runtime; not acceptance', 'manifestSha256': fsha(MAN)}

rel = lambda root: {str(p.relative_to(root)) for p in (root / 'docs').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
bset, eset = rel(B), rel(E)
touched = sorted(p for p in bset & eset if (B / p).read_bytes() != (E / p).read_bytes())
out['added'], out['removed'] = sorted(eset - bset), sorted(bset - eset)
rows, diff = [], ''
for p in touched:
    before, after = (B / p).read_bytes(), (E / p).read_bytes()
    rows.append({'path': p, 'beforeSha256': sha(before), 'afterSha256': sha(after), 'beforeBytes': len(before), 'afterBytes': len(after),
                 'beforeIsSource38Manifest': manifest[p]['sha256'] == sha(before), 'source38StillManifest': fsha(SRC / p) == manifest[p]['sha256']})
    diff += ''.join(difflib.unified_diff(before.decode('utf-8').splitlines(True), after.decode('utf-8').splitlines(True),
                                         'source38/' + p, 'edited/' + p))
(BASE / 'proposed-edits.diff').write_text(diff, encoding='utf-8')
out['touched'] = rows
out['proposedEditsDiff'] = {'sha256': sha(diff.encode()), 'lines': diff.count('\n')}

DEPS = ['docs/coop/artifacts/d9-exit-contract.v1.14.json',
        'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
        'docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json',
        'docs/coop/design-corrections/workflows/query_projection_model.v3.py',
        'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md',
        'docs/coop/design-corrections/workflows/command-inventory.v3.json',
        'docs/coop/design-corrections/workflows/workflow-cases.v1.json',
        'docs/coop/design-corrections/public-detail-registry.v1.json',
        'docs/coop/design-corrections/foundation/identity-schemas.v3.json',
        'docs/coop/design-corrections/foundation/identity-model.v3.py',
        'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md',
        'docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py',
        'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py',
        'docs/coop/design-corrections/native/native_evidence_model.v2.py',
        'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
        'docs/coop/design-corrections/native/native-cases.v2.json',
        'docs/v2/contracts/product-v1/native-evidence.md',
        'docs/v2/contracts/product-v1/identity-and-evidence.md',
        'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql',
        'docs/coop/design-corrections/security/carrier-migration.v1.md',
        'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
        'docs/coop/design-corrections/security/check-integrated-carrier.v1.py',
        'docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
        'docs/coop/completion/security-schemas.v2/grant-journal.sql',
        'docs/coop/completion/security-completion.v1.md',
        'docs/v2/architecture/attempt-custody.schema.v1.json',
        'docs/v2/architecture/carrier-fault-cases.v1.json',
        'docs/v2/architecture/commit-recovery-plan.v1.json',
        'docs/v2/architecture/implementation-boundaries-and-build-plan.md',
        'docs/v2/architecture/implementation-coverage.v1.json',
        'docs/v2/architecture/repository-file-inventory.v1.json',
        'docs/v2/architecture/store-instance-lineage.v1.json',
        'docs/operations/check_implementation_planning.py']
out['dependencies'] = [{'path': p, 'sha256': manifest[p]['sha256'], 'source38Unchanged': fsha(SRC / p) == manifest[p]['sha256'],
                        'editedEqualsSource38': fsha(E / p) == manifest[p]['sha256'], 'notTouched': p not in touched} for p in DEPS]
p00 = json.loads((R / 'p00-custody.json').read_text())
out['reviewInputsUnchanged'] = all(fsha(REV / n) == h for n, h in p00['reviewInputs'].items())
out['a5InputsUnchanged'] = all(fsha(A5 / n) == h for n, h in p00['a5Inputs'].items())

# binding drift
pins = {}
before_hashes = {r['beforeSha256']: r['path'] for r in rows}
for p in sorted(bset):
    if '/reviews/' in p or not p.endswith(('.json', '.md', '.py', '.txt')):
        continue
    text = (B / p).read_text(encoding='utf-8', errors='replace')
    for h, t in before_hashes.items():
        if h in text:
            pins.setdefault(t, []).append(p)
out['filesPinningTouchedBeforeHashes'] = pins


def section_values(text):
    lines = text.splitlines(keepends=True)
    heads = [i for i, line in enumerate(lines) if line.startswith('## ')]
    return [(i + 1, {'heading': lines[s].strip(), 'firstLine': s + 1, 'lastLine': e}, ''.join(lines[s:e]))
            for i, (s, e) in enumerate(zip(heads, heads[1:] + [len(lines)]))]


drift = []
for key, path in (('security-and-lifecycle', 'docs/v2/contracts/product-v1/security-and-lifecycle.md'),
                  ('workflows-and-surfaces', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'),
                  ('native-evidence', 'docs/v2/contracts/product-v1/native-evidence.md'),
                  ('identity-and-evidence', 'docs/v2/contracts/product-v1/identity-and-evidence.md'),
                  ('admission-and-qualification', 'docs/v2/contracts/product-v1/admission-and-qualification.md')):
    if path not in touched:
        continue
    bv, ev = section_values((B / path).read_text()), section_values((E / path).read_text())
    for (i, bs, btext), (_, es, etext) in zip(bv, ev):
        if bs != es or btext != etext:
            drift.append({'id': '%s:%d' % (key, i), 'heading': bs['heading'], 'textChanged': btext != etext,
                          'selectorBefore': [bs['firstLine'], bs['lastLine']], 'selectorAfter': [es['firstLine'], es['lastLine']]})
out['planningSectionDrift'] = drift


def latest(prefix):
    cands = sorted((p for p in R.iterdir() if p.is_dir() and (p.name == prefix or p.name.startswith(prefix + '.r'))),
                   key=lambda p: (len(p.name), p.name))
    return cands[-1] if cands else None


pe = latest('p01-edited')
out['p01EditedReportDir'] = str(pe)
rep = json.loads((pe / 'grok-native-replay.v1.json').read_text())
out['semanticReplay'] = {'passed': rep['passed'], 'count': rep['count'], 'blocked': rep['blocked'],
                         'runTerminationRows': {c['case']: len(c.get('faults', [])) for c in rep['checks'] if c['case'].startswith('run-termination')}}
comp = [c for c in rep['checks'] if c['case'] == 'run-termination:host-composition-boundary'][0]
out['compositionCases'] = [(c['label'], c.get('composition'), c.get('pureProjection'), c.get('schemaValid')) for c in comp['composition']]
car = json.loads((pe / 'carrier.json').read_text())
out['carrier'] = {'passed': car['passed'], 'failed': car['failed'],
                  'source38Checks': [(c['check'], c['pass']) for c in car['checks']
                                     if c['check'].startswith(('source38', 'source37 scenario: ADV38-02'))]}
out['discrimination'] = {}
for p in sorted(R.iterdir()):
    if p.is_dir() and p.name.startswith('p03-') and (p / 'result.json').exists():
        d = json.loads((p / 'result.json').read_text())
        out['discrimination'][p.name] = {k: d.get(k) for k in ('expectationMet', 'failRows', 'faultLabels', 'passed', 'failed', 'exit')}
out['a5'] = {n: json.loads((R / n).read_text()) for n in ('a5-cases.json',)}
am = json.loads((R / 'a5-amendment.r2.json').read_text())
out['a5Amendment'] = {k: am[k] for k in ('allOk', 'nativeCasesRoundTrip', 'files', 'proposedAmendmentDiff', 'lawRows',
                                          'amendedLawDisagreements', 'rootLawDisagreements')}
ex = json.loads((R / 'a5-extends.json').read_text())
out['a5Extends'] = {'compilerVersion': ex['compilerVersion'], 'node': ex['nodeVersion'], 'custody': ex['compilerCustody'],
                    'disagreements': ex['disagreements']}
out['receiptExits'] = {p.name: json.loads(p.read_text())['exit'] for p in sorted(R.glob('*.receipt.json'))}
out['receiptDigests'] = {p.name: fsha(p) for p in sorted(R.iterdir()) if p.is_file()}
if final:
    for n in ('review.md', 'review.json'):
        out.setdefault('review', {})[n] = fsha(BASE / n)
    json.loads((BASE / 'review.json').read_text())
name = 'p04-summary.final.json' if final else 'p04-summary.json'
(R / name).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('receiptDigests', 'a5', 'dependencies')}, indent=1)[:30000])
bad = [d['path'] for d in out['dependencies'] if not (d['source38Unchanged'] and d['editedEqualsSource38'] and d['notTouched'])]
ok = (not out['added'] and not out['removed'] and all(r['beforeIsSource38Manifest'] and r['source38StillManifest'] for r in rows)
      and not bad and out['reviewInputsUnchanged'] and out['a5InputsUnchanged'] and rep['passed'] and car['failed'] == 0
      and all(d['expectationMet'] for d in out['discrimination'].values()))
print('dependency problems:', bad, 'allOk:', ok)
sys.exit(0 if ok else 1)

"""p07 [final]: read-only v2 deliverable summary.

- total diff frozen source38 -> v2 edited (total-edits-vs-source38.diff) and incremental diff v1 edited -> v2 edited
  (incremental-v1-to-v2.diff), each with per-file hash maps (source38 / v1 / v2);
- custody: v1 edited tree unchanged against p00's per-file hashes; v1 review files and root's assessment files
  unchanged; touched and dependency files of source38 equal the manifest; v2 dependencies equal source38;
- binding drift: files in the source38 docs tree (minus reviews) pinning a touched file's source38 hash, and the
  planning contract-section selectors that change;
- results: latest p04 edited report, p05 discrimination, p01 measurement, receipt exits and digests.
With argv[1] == 'final', also digests review.md/review.json. Output: receipts/p07-summary[.final].json.
"""
import difflib, hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
V1R = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
V1 = V1R / 'work' / 'edited'
V2 = BASE / 'work' / 'edited'
SRC = Path('/tmp/opensip-design-corrections/candidate-subject.v38')
ROOT = Path('/tmp/opensip-design-corrections/root-source38-advisory-assessment.v1')
MAN = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json')
R = BASE / 'receipts'
final = len(sys.argv) > 1 and sys.argv[1] == 'final'
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(p.read_bytes())
manifest = {r['path']: r['sha256'] for r in json.loads(MAN.read_text())['files']}
p00 = json.loads((R / 'p00-custody.json').read_text())
v1hashes = json.loads((R / 'v1-edited-file-hashes.json').read_text())
out = {'standing': 'read-only v2 summary; not acceptance', 'manifestSha256': fsha(MAN)}

v2files = {str(p.relative_to(V2)): p for p in (V2 / 'docs').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
out['treeFileSetsEqual'] = set(v2files) == set(v1hashes)
total = sorted(p for p in v2files if manifest.get(p) != fsha(v2files[p]))
incremental = sorted(p for p in v2files if v1hashes.get(p) != fsha(v2files[p]))


def udiff(a, b, la, lb):
    return ''.join(difflib.unified_diff(a.decode('utf-8').splitlines(True), b.decode('utf-8').splitlines(True), la, lb))


tdiff, idiff, tmap, imap = '', '', [], []
for p in total:
    s38, v2 = (SRC / p).read_bytes(), v2files[p].read_bytes()
    tdiff += udiff(s38, v2, 'source38/' + p, 'v2/' + p)
    tmap.append({'path': p, 'source38': sha(s38), 'source38IsManifest': sha(s38) == manifest[p], 'v1': v1hashes[p], 'v2': sha(v2)})
for p in incremental:
    v1b, v2 = (V1 / p).read_bytes(), v2files[p].read_bytes()
    idiff += udiff(v1b, v2, 'v1/' + p, 'v2/' + p)
    imap.append({'path': p, 'v1': sha(v1b), 'v2': sha(v2)})
(BASE / 'total-edits-vs-source38.diff').write_text(tdiff, encoding='utf-8')
(BASE / 'incremental-v1-to-v2.diff').write_text(idiff, encoding='utf-8')
out['totalVsSource38'] = {'files': tmap, 'diffSha256': sha(tdiff.encode()), 'lines': tdiff.count('\n')}
out['incrementalV1ToV2'] = {'files': imap, 'diffSha256': sha(idiff.encode()), 'lines': idiff.count('\n')}

DEPS = ['docs/coop/artifacts/d9-exit-contract.v1.14.json',
        'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
        'docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json',
        'docs/coop/design-corrections/workflows/query_projection_model.v3.py',
        'docs/coop/design-corrections/public-detail-registry.v1.json',
        'docs/coop/design-corrections/foundation/identity-schemas.v3.json',
        'docs/coop/design-corrections/foundation/identity-model.v3.py',
        'docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py',
        'docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py',
        'docs/coop/design-corrections/native/native_evidence_model.v2.py',
        'docs/coop/design-corrections/native/protocol3-transitions.v1.json',
        'docs/v2/contracts/product-v1/identity-and-evidence.md',
        'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql',
        'docs/coop/design-corrections/security/carrier-migration.v1.md',
        'docs/coop/design-corrections/security/carrier-highwater.schema.v1.json',
        'docs/coop/design-corrections/security/check-integrated-carrier.v1.py',
        'docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
        'docs/coop/completion/security-schemas.v2/grant-journal.sql',
        'docs/coop/completion/security-completion.v1.md',
        'docs/coop/completion/security-completion.v8.md',
        'docs/v2/architecture/attempt-custody.schema.v1.json',
        'docs/v2/architecture/carrier-fault-cases.v1.json',
        'docs/v2/architecture/commit-recovery-plan.v1.json',
        'docs/v2/architecture/implementation-boundaries-and-build-plan.md',
        'docs/v2/architecture/implementation-coverage.v1.json']
out['dependencies'] = [{'path': p, 'sha256': manifest[p], 'source38Unchanged': fsha(SRC / p) == manifest[p],
                        'v2EqualsSource38': fsha(V2 / p) == manifest[p], 'notTouched': p not in total} for p in DEPS]
out['custody'] = {
    'v1EditedTreeUnchanged': all(fsha(V1 / p) == h for p, h in v1hashes.items()),
    'v1ReviewUnchanged': all(fsha(V1R / n) == h for n, h in p00['v1Review'].items()),
    'rootAssessmentUnchanged': all(fsha(ROOT / n) == h for n, h in p00['rootAssessment'].items()),
    'source38TouchedEqualManifest': all(fsha(SRC / r['path']) == manifest[r['path']] for r in tmap),
}

pins = {}
before = {r['source38']: r['path'] for r in tmap}
for p in sorted(p for p in v2files if '/reviews/' not in p and p.endswith(('.json', '.md', '.py'))):
    text = (SRC / p).read_text(encoding='utf-8', errors='replace')
    for h, t in before.items():
        if h in text:
            pins.setdefault(t, []).append(p)
out['filesPinningTouchedSource38Hashes'] = pins


def section_values(text):
    lines = text.splitlines(keepends=True)
    heads = [i for i, line in enumerate(lines) if line.startswith('## ')]
    return [(i + 1, lines[s].strip(), s + 1, e, ''.join(lines[s:e])) for i, (s, e) in enumerate(zip(heads, heads[1:] + [len(lines)]))]


drift = []
for key, p in (('security-and-lifecycle', 'docs/v2/contracts/product-v1/security-and-lifecycle.md'),
               ('workflows-and-surfaces', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md')):
    for a, b in zip(section_values((SRC / p).read_text()), section_values(v2files[p].read_text())):
        if a[2:] != b[2:]:
            drift.append({'id': '%s:%d' % (key, a[0]), 'heading': a[1], 'textChanged': a[4] != b[4],
                          'lines': [a[2], a[3], b[2], b[3]]})
out['planningSectionDrift'] = drift


def latest(prefix):
    c = sorted((p for p in R.iterdir() if p.is_dir() and (p.name == prefix or p.name.startswith(prefix + '.r'))),
               key=lambda p: (len(p.name), p.name))
    return c[-1] if c else None


pe = latest('p04-edited')
summary = json.loads((pe / 'summary.json').read_text())
car = json.loads((pe / 'carrier.json').read_text())
sem = json.loads((pe / 'grok-native-replay.v1.json').read_text())
out['ownerChecks'] = {'reportDir': str(pe), 'semanticPassed': sem['passed'], 'semanticRows': sem['count'],
                      'compositionCases': summary['semanticReplay']['compositionCases'],
                      'carrierPassed': car['passed'], 'carrierFailed': car['failed'],
                      'followUpCarrierChecks': [(c['check'], c['pass']) for c in car['checks']
                                                if 'absent' in c['check'] or 'unknown-custody' in c['check']]}
out['discrimination'] = {}
for p in sorted(R.iterdir()):
    if p.is_dir() and p.name.startswith('p05-') and (p / 'result.json').exists():
        d = json.loads((p / 'result.json').read_text())
        out['discrimination'][p.name] = {k: d.get(k) for k in ('expectationMet', 'failRows', 'faultLabels', 'passed', 'failed', 'failedChecks', 'exit')}
out['measurement'] = json.loads((R / 'p01-measure.json').read_text())
out['receiptExits'] = {p.name: json.loads(p.read_text())['exit'] for p in sorted(R.glob('*.receipt.json'))}
out['receiptDigests'] = {p.name: fsha(p) for p in sorted(R.iterdir()) if p.is_file()}
if final:
    out['review'] = {n: fsha(BASE / n) for n in ('review.md', 'review.json')}
    json.loads((BASE / 'review.json').read_text())
name = 'p07-summary.final.json' if final else 'p07-summary.json'
(R / name).write_text(json.dumps(out, indent=1, default=str) + '\n')
bad = [d['path'] for d in out['dependencies'] if not (d['source38Unchanged'] and d['v2EqualsSource38'] and d['notTouched'])]
ok = (out['treeFileSetsEqual'] and not bad and all(out['custody'].values()) and all(r['source38IsManifest'] for r in tmap)
      and sem['passed'] and car['failed'] == 0 and len(out['discrimination']) >= 7
      and all(d['expectationMet'] for d in out['discrimination'].values()))
print(json.dumps({k: v for k, v in out.items() if k not in ('receiptDigests', 'measurement', 'dependencies', 'ownerChecks')}, indent=1)[:20000])
print('ownerChecks:', {k: v for k, v in out['ownerChecks'].items() if k != 'compositionCases'})
print('dependency problems:', bad, 'allOk:', ok)
sys.exit(0 if ok else 1)

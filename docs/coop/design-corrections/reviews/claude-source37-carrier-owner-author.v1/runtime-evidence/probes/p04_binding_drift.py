"""Report, for root, every existing binding the changed bytes affect. Edits nothing.

Covers: the source37 manifest pins, implementation-normative-inputs.v5, implementation-coverage sources and the
contractSections rows the planning checker derives from security-and-lifecycle.md, every source-pins ledger, and
whether the generated commit-recovery section can change. Also re-verifies that frozen and baseline bytes are
unchanged.
"""
import hashlib, json, re
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v37')
MANIFEST = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json')
BL, ED = BASE / 'work/baseline', BASE / 'work/edited'
p02 = json.loads((BASE / 'receipts/p02-apply-edits.json').read_text())
p00 = json.loads((BASE / 'receipts/p00-copy-verify.json').read_text())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pins_in(doc):
    found = []

    def walk(o, ptr):
        if isinstance(o, dict):
            if isinstance(o.get('path'), str) and isinstance(o.get('sha256'), str):
                found.append((o['path'], o['sha256'], ptr))
            for k, v in o.items():
                walk(v, ptr + '/' + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, ptr + '/' + str(i))
    walk(doc, '')
    return found


manifest = pins_in(json.loads(MANIFEST.read_bytes()))
v5 = {r['path']: r['sha256'] for r in json.loads((BL / 'docs/v2/architecture/implementation-normative-inputs.v5.json').read_text())['files']}
coverage = json.loads((BL / 'docs/v2/architecture/implementation-coverage.v1.json').read_text())
ledgers = sorted(p for p in (BL / 'docs/coop/design-corrections').rglob('*source-pins*.json'))
ledger_pins = {str(p.relative_to(BL)): pins_in(json.loads(p.read_text())) for p in ledgers}
rows = []
for f in p02['files']:
    rel = f['path']
    rows.append({
        'path': rel, 'beforeSha256': f['beforeSha256'], 'afterSha256': f['afterSha256'],
        'manifestPins': sorted({s for p, s, _ in manifest if p == rel}),
        'normativeInputsV5': v5.get(rel),
        'coverageSources': [k for k, r in coverage['sources'].items() if r['path'] == rel],
        'sourcePinLedgers': sorted(l for l, ps in ledger_pins.items() if any(p == rel for p, _, _ in ps)),
        'checkIntegratedCarrierInput': rel in {x['path'] for x in json.loads((BASE / 'receipts/p03-integrated-carrier.edited.json').read_text())['inputCustody']},
    })


def digest(value):
    return sha(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode())


def section_values(text):
    lines = text.splitlines(keepends=True)
    heads = [i for i, line in enumerate(lines) if line.startswith('## ')]
    return [(i + 1, {'heading': lines[s].strip(), 'firstLine': s + 1, 'lastLine': e}, ''.join(lines[s:e]))
            for i, (s, e) in enumerate(zip(heads, heads[1:] + [len(lines)]))]


S = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
mapped = {r['id']: r for r in coverage['groups']['contractSections'] if r['id'].startswith('security-and-lifecycle:')}
section_drift = []
for i, selector, value in section_values((ED / S).read_text()):
    rid = 'security-and-lifecycle:' + str(i)
    row = mapped.get(rid)
    if row is None or row['source']['selector'] != selector or row['source']['valueSha256'] != digest(value):
        section_drift.append({'id': rid, 'heading': selector['heading'],
                              'selectorDrift': row is None or row['source']['selector'] != selector,
                              'valueDrift': row is None or row['source']['valueSha256'] != digest(value)})
baseline_sections_match = all(
    mapped['security-and-lifecycle:' + str(i)]['source'] == {'key': 'security-and-lifecycle', 'selector': sel, 'valueSha256': digest(v)}
    for i, sel, v in section_values((BL / S).read_text()))
unchanged_generated_inputs = {rel: sha((ED / rel).read_bytes()) == sha((BL / rel).read_bytes()) for rel in (
    'docs/v2/architecture/commit-recovery-plan.v1.json', 'docs/v2/architecture/carrier-fault-cases.v1.json',
    'docs/v2/architecture/implementation-boundaries-and-build-plan.md', 'docs/v2/architecture/implementation-coverage.v1.json',
    'docs/v2/architecture/implementation-normative-inputs.v5.json', 'docs/coop/completion/security-schemas.v2/grant-journal.sql',
    'docs/coop/design-corrections/security/source-pins.v1.json', 'docs/coop/design-corrections/current-source-map.proposed.md')}
frozen_unchanged = all(sha((FROZEN / r['path']).read_bytes()) == r['sha256'] for r in p00['rows'])
baseline_unchanged = all(sha((BL / r['path']).read_bytes()) == r['sha256'] for r in p00['rows'])
edited_other_files_equal = []
for p in sorted(ED.rglob('*')):
    if p.is_file():
        rel = str(p.relative_to(ED))
        if rel not in {f['path'] for f in p02['files']} and (BL / rel).read_bytes() != p.read_bytes():
            edited_other_files_equal.append(rel)
record = {'changedFiles': rows, 'planningContractSectionDrift': section_drift,
          'baselineSectionsMatchCoverage': baseline_sections_match,
          'generatedPlanningInputsAndLedgersUnchanged': unchanged_generated_inputs,
          'frozenKeyFilesUnchanged': frozen_unchanged, 'baselineKeyFilesUnchanged': baseline_unchanged,
          'editedFilesOutsideTheNineThatDifferFromBaseline': edited_other_files_equal}
out = BASE / 'receipts' / 'p04-binding-drift.json'
out.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
if not (frozen_unchanged and baseline_unchanged and baseline_sections_match and not edited_other_files_equal
        and all(unchanged_generated_inputs.values())):
    raise SystemExit(1)

"""p06 - Preservation: did the v10 delta perturb anything v9 independently confirmed?

Two independent lines of evidence:

  (1) MANIFEST-LEVEL: which deterministic reports are byte-identical between frozen v9 and
      frozen v10. A report that is byte-identical across the delta cannot contain a changed
      identity, count or verdict.

  (2) COMPUTATIONAL: load BOTH frozen source images and recompute representative Run/body
      identities and framing directly, comparing values rather than trusting the reports.
"""
import sys
sys.path.insert(0, '/tmp/opensip-design-corrections/post-reset-review.v10/probes')
import hashlib
import importlib.util
import json
import shutil
from pathlib import Path
import harness

R = Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
V9 = Path('/tmp/opensip-design-corrections/candidate-subject.v9')
V10 = Path('/tmp/opensip-design-corrections/candidate-subject.v10')

out = {}

# ------------------------------------------------------------------ (1) manifest-level invariance
m9 = {f['path']: f for f in json.loads((R / 'candidate-subject.v9.json').read_text())['files']}
m10 = {f['path']: f for f in json.loads((R / 'candidate-subject.v10.json').read_text())['files']}
changed = sorted(p for p in set(m9) & set(m10) if m9[p]['sha256'] != m10[p]['sha256'])
out['changedAcrossDelta'] = changed
out['removedAcrossDelta'] = sorted(set(m9) - set(m10))

DETERMINISTIC_REPORTS = [
    'docs/coop/design-corrections/integration-report.v1.json',
    'docs/coop/design-corrections/native/native-evidence-report.v2.json',
    'docs/coop/design-corrections/security/security-lifecycle-report.v1.json',
    'docs/coop/design-corrections/foundation/identity-report.json',
    'docs/coop/design-corrections/foundation/validation-report.json',
    'docs/coop/design-corrections/workflows/workflows-report.v1.json',
]
out['reportInvariance'] = {
    p: ('IDENTICAL' if (p in m9 and p in m10 and m9[p]['sha256'] == m10[p]['sha256'])
        else 'CHANGED') for p in DETERMINISTIC_REPORTS}

# every SCHEMA / REGISTRY / CONTRACT byte
normative = [p for p in m10 if p.endswith('.json') and
             ('schema' in p.lower() or 'registry' in p.lower()) and '/reviews/' not in p]
out['normativeSchemaRegistryFiles'] = len(normative)
out['normativeSchemaRegistryChanged'] = [p for p in normative if p in changed]

arch = [p for p in m10 if p.startswith('docs/v2/') or p.startswith('docs/catalog/')]
out['architectureAndCatalogFiles'] = len(arch)
out['architectureAndCatalogChanged'] = [p for p in arch if p in changed]

# ------------------------------------------------------------ (2) computational identity stability
WORK = Path('/tmp/opensip-design-corrections/post-reset-review.v10/work')


def load_image(subject, tag):
    dst = WORK / ('image-' + tag)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(subject / 'docs/coop/design-corrections', dst)
    spec = importlib.util.spec_from_file_location('img_' + tag, dst / 'foundation/identity-model.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._sha = hashlib.sha256((dst / 'foundation/identity-model.py').read_bytes()).hexdigest()
    return mod


i9 = load_image(V9, 'v9')
i10 = load_image(V10, 'v10')
out['imageSha'] = {'v9': i9._sha, 'v10': i10._sha}
out['imagesDiffer'] = i9._sha != i10._sha

# representative BODY identities through the framing/identifier surface
BODIES = [
    ('typescript-body', 'typescript', '5.4.5', b'export const a = 1;\n'),
    ('javascript-through-ts-engine', 'javascript', '5.4.5', b'const a = 1;\n'),
    ('rust-body', 'rust', '1.79.0', b'pub fn a() {}\n'),
    ('empty-body', 'typescript', '5.4.5', b''),
    ('unicode-body', 'typescript', '5.4.5', 'const s = "é中";\n'.encode()),
]
body_rows = []
for label, lang, ver, payload in BODIES:
    row = {'label': label}
    for tag, mod in (('v9', i9), ('v10', i10)):
        try:
            frame = mod.FRAME_PREFIX + json.dumps(
                {'language': lang, 'version': ver}, sort_keys=True,
                separators=(',', ':')).encode() + b'\0' + payload
            row[tag] = hashlib.sha256(frame).hexdigest()
            row[tag + '_prefix'] = mod.FRAME_PREFIX.decode('utf-8', 'replace')
        except Exception as exc:
            row[tag] = 'ERROR:' + str(exc)[:80]
    row['stable'] = row.get('v9') == row.get('v10')
    body_rows.append(row)
out['framedBodyIdentities'] = body_rows
out['framePrefixStable'] = i9.FRAME_PREFIX == i10.FRAME_PREFIX

# domain prefix / identifier tables must be unchanged
out['prefixTableStable'] = i9.PREFIX == i10.PREFIX
out['domainOfStable'] = i9.DOMAIN_OF == i10.DOMAIN_OF
out['prefixDomains'] = sorted(i10.PREFIX)

# identifier() over representative records in every registered domain
ident_rows = []
for domain in sorted(i10.PREFIX):
    rec = {'reviewer': 'probe', 'domain': domain, 'n': 1}
    r = {'domain': domain}
    for tag, mod in (('v9', i9), ('v10', i10)):
        try:
            r[tag] = mod.identifier(domain, rec)
        except Exception as exc:
            r[tag] = 'ERROR:' + type(exc).__name__
    r['stable'] = r['v9'] == r['v10']
    ident_rows.append(r)
out['identifierStability'] = ident_rows
out['allIdentifiersStable'] = all(r['stable'] for r in ident_rows)

# the relation law itself must still admit all 13 on BOTH images
out['relationLawBothImages'] = {}
for tag, mod in (('v9', i9), ('v10', i10)):
    res = {}
    for name in mod.RELATION_DOCUMENT['x-opensip-relation-registry']['relations']:
        try:
            mod.relation_annotation_closure(name, None)
            res[name] = 'ADMIT'
        except Exception as exc:
            res[name] = 'REFUSE:' + str(exc)[:60]
    out['relationLawBothImages'][tag] = res
out['shippedRelationsAdmitOnBoth'] = all(
    v == 'ADMIT' for side in out['relationLawBothImages'].values() for v in side.values())

out['ASSESSMENT'] = {
    'filesChangedAcrossDelta': len(changed),
    'filesRemovedAcrossDelta': len(out['removedAcrossDelta']),
    'normativeSchemaRegistryChanged': out['normativeSchemaRegistryChanged'],
    'architectureAndCatalogChanged': out['architectureAndCatalogChanged'],
    'reportInvariance': out['reportInvariance'],
    'framePrefixStable': out['framePrefixStable'],
    'prefixTableStable': out['prefixTableStable'],
    'allFramedBodyIdentitiesStable': all(r['stable'] for r in body_rows),
    'allIdentifiersStable': out['allIdentifiersStable'],
    'shippedRelationsAdmitOnBothImages': out['shippedRelationsAdmitOnBoth'],
}

harness.emit(out, '/tmp/opensip-design-corrections/post-reset-review.v10/work/p06.json')
print(json.dumps(out['ASSESSMENT'], indent=2))

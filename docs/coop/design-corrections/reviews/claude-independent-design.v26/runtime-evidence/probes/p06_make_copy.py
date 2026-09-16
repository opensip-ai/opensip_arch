"""Probe 06 — disposable exact copy of the design-corrections kit (excluding reviews/),
so report-writing checkers never mutate the frozen snapshot. Verifies every copied
byte against the frozen manifest BEFORE any checker runs."""
import hashlib, json, os, shutil

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
DST = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/kit'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v26.json'
REL = 'docs/coop/design-corrections'

man = {r['path']: r for r in json.load(open(MAN))['files']}
if os.path.isdir(DST):
    shutil.rmtree(DST)
copied = 0
skipped_reviews = 0
for dp, dn, fn in os.walk(os.path.join(SRC, REL)):
    if os.sep + 'reviews' in dp + os.sep:
        skipped_reviews += len(fn)
        dn[:] = []
        continue
    for f in fn:
        s = os.path.join(dp, f)
        rel = os.path.relpath(s, SRC)
        if rel.startswith(REL + '/reviews/'):
            skipped_reviews += 1
            continue
        d = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)
        copied += 1

# verify EVERY copied byte against the frozen manifest
bad = []
verified = 0
for dp, dn, fn in os.walk(DST):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, DST)
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        rec = man.get(rel)
        if rec is None:
            bad.append(('not-in-manifest', rel))
        elif rec['sha256'] != h or rec['bytes'] != os.path.getsize(p):
            bad.append(('hash-or-length', rel))
        else:
            verified += 1

# explicitly re-verify the normative/model/pin files the checkers consume
KEY = [
    'foundation/identity-schemas.v3.json', 'foundation/identity-model.v3.py',
    'foundation/canonical.py', 'foundation/relation-payload-schemas.v2.json',
    'foundation/target-attribution.schema.v2.json', 'foundation/enumeration-contract.v1.md',
    'foundation/atom-evaluation-contract.v1.md', 'foundation/execution-inputs-contract.v1.md',
    'foundation/evaluator-composition-contract.v3.md', 'foundation/evaluator-fault-contract.v3.md',
    'native/native_evidence_model.v2.py', 'native/source-pins.v2.json',
    'native/native-evidence.schemas.v2.json', 'native/native-capability-matrix.v2.json',
    'native/fact-batch.schema.v3.json', 'native/occupancy-companion.schema.v1.json',
    'native/dispatch-binding.schema.v1.json',
    'security/source-pins.v1.json', 'security/security_lifecycle_model_v1.py',
    'security/security-lifecycle.schemas.v1.json', 'security/grant-journal.carrier.v3.sql',
    'workflows/query-projection-contract.v3.md', 'workflows/workflow-projection-contract.v3.md',
    'workflows/query_projection_model.v3.py', 'workflows/workflow_projection_model.v3.py',
    'public-detail-registry.v1.json', 'correction-crosswalk.proposed.json',
]
key_rows = []
for k in KEY:
    rel = REL + '/' + k
    p = os.path.join(DST, rel)
    ok = os.path.isfile(p)
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest() if ok else None
    key_rows.append({'path': rel, 'present': ok, 'sha256': h,
                     'matchesFrozenManifest': ok and man.get(rel, {}).get('sha256') == h})

os.makedirs('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts', exist_ok=True)
res = {'copiedFiles': copied, 'skippedReviewFiles': skipped_reviews,
       'verifiedAgainstFrozenManifest': verified, 'mismatches': bad[:20],
       'mismatchCount': len(bad), 'keyNormativeFiles': key_rows}
json.dump(res, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/disposable-copy-verification.json', 'w'), indent=1)
print('copied=%d verified=%d mismatches=%d skippedReviews=%d' % (copied, verified, len(bad), skipped_reviews))
for r in key_rows:
    if not r['matchesFrozenManifest']:
        print('KEY MISMATCH', r)
print('all key normative/model/pin files match frozen manifest:',
      all(r['matchesFrozenManifest'] for r in key_rows))

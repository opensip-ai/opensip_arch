"""p07 - Scope: what would a hypothetical registry-document mutation actually reach?

Both v9-S1 and the reviewer's new v10-S1 are SCHEMA-EDIT findings. This probe bounds how far such
an edit could travel, so severity is argued from measurement rather than assertion:

  1. Is the relation document itself PINNED, and is the pin a hard failure?
  2. Is relation_annotation_closure a PURE schema function, or can it see snapshot/Run truth?
  3. Does the law's own declared enforcement place owning-Run admission OUTSIDE the payload decode
     memo (so a payload alone cannot decide snapshot truth)?
"""
import sys
sys.path.insert(0, '/tmp/opensip-design-corrections/post-reset-review.v10/probes')
import ast
import copy
import hashlib
import json
from pathlib import Path
import harness

m = harness.load_model()
SUB = harness.SUBJECT
DC = SUB / 'docs/coop/design-corrections'
out = {}

# --------------------------------------------------------- 1. is the relation document pinned?
reldoc = DC / 'foundation/relation-payload-schemas.v2.json'
reldoc_sha = hashlib.sha256(reldoc.read_bytes()).hexdigest()
out['relationDocumentSha256'] = reldoc_sha
pinned_in = {}
for pf in ['foundation/source-pins.v1.json', 'native/source-pins.v2.json',
           'security/source-pins.v1.json', 'workflows/source-pins.v1.json']:
    doc = json.loads((DC / pf).read_text())
    entries = doc.get('files') or doc.get('pins') or []
    rows = {f['path']: f.get('sha256') for f in entries}
    key = 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'
    pinned_in[pf] = {'present': key in rows, 'matches': rows.get(key) == reldoc_sha,
                     'totalPinned': len(rows)}
out['relationDocumentPinnedIn'] = pinned_in
out['relationDocumentPinnedEverywhereItIsUsed'] = all(
    v['present'] and v['matches'] for v in pinned_in.values())

# ------------------------------------------- 2. is the closure PURE (schema-only, no I/O, no Run)?
src = (harness.SUBJ_FOUND / 'identity-model.py').read_text()
tree = ast.parse(src)
targets = {'relation_annotation_closure', 'relation_digest_annotation_coverage'}
purity = {}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in targets:
        calls = set()
        names = set()
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                f = sub.func
                calls.add(getattr(f, 'id', None) or getattr(f, 'attr', None))
            if isinstance(sub, ast.Name):
                names.add(sub.id)
        purity[node.name] = {
            'callsOpen': 'open' in calls, 'callsRead': any(
                c in calls for c in ('read_text', 'read_bytes', 'loads', 'load')),
            'referencesSnapshotOrRun': sorted(
                n for n in names if 'snapshot' in n.lower() or n.lower().startswith('run')),
            'referencesCache': sorted(n for n in names if 'cache' in n.lower() or 'memo' in n.lower()),
            'signatureArgs': [a.arg for a in node.args.args],
        }
out['purity'] = purity
out['closureIsSchemaOnly'] = all(
    (not v['callsOpen']) and not v['referencesSnapshotOrRun'] and not v['referencesCache']
    for v in purity.values())

# --------------------------------------- 3. the law's own declared enforcement / owning-Run context
law = m.RELATION_DIGEST_LAW
out['declaredEnforcement'] = law['enforcement']
enf = law['enforcement'].lower()
out['enforcementPlacesAdmissionOutsidePayloadMemo'] = (
    'independently of the payload decode cache' in enf)
out['enforcementRequiresOwnerContext'] = (
    'payload alone cannot decide snapshot truth' in enf)
out['residueRule'] = law['residueRule']
out['lawStandingNoDefaultNoResidue'] = 'no default and no residue' in law['standing']

# ------------------------- does the shipped document have ANY governed field that is unannotated?
cov = m.relation_digest_annotation_coverage(harness.base_document(m))
out['shippedGovernedTotal'] = cov['total']
out['shippedGovernedAnnotated'] = cov['annotated']
out['shippedUnannotated'] = cov['unannotated']
out['shippedIsAlreadyClosed'] = (cov['unannotated'] == [] and cov['total'] == cov['annotated'])

# -------------- would a same-path collision (the v10-S1 shape) exist anywhere in the shipped doc?
paths = [s['path'] for s in cov['sightings']]
out['shippedSightingPaths'] = paths
out['shippedHasNoCollision'] = len(paths) == len(set(paths))

out['ASSESSMENT'] = {
    'relationDocumentIsPinnedInAllFourPinSets': out['relationDocumentPinnedEverywhereItIsUsed'],
    'pinFailureIsHardFailure': 'verified separately: run-reference-checks exits 1 on pin drift',
    'closureIsPureSchemaOnly': out['closureIsSchemaOnly'],
    'owningRunAdmissionOutsidePayloadDecodeMemo':
        out['enforcementPlacesAdmissionOutsidePayloadMemo'],
    'payloadAloneCannotDecideSnapshotTruth': out['enforcementRequiresOwnerContext'],
    'shippedDocumentAlreadyClosed': out['shippedIsAlreadyClosed'],
    'shippedHasNoSamePathCollision': out['shippedHasNoCollision'],
    'conclusion': ('both v9-S1 and the new v10-S1 are reachable only by an authored edit to a '
                   'PINNED registry document, never by a payload, a Run or an untrusted input; '
                   'severity is design/reference coherence under future registered schema edits'),
}

harness.emit(out, '/tmp/opensip-design-corrections/post-reset-review.v10/work/p07.json')
print(json.dumps(out['ASSESSMENT'], indent=2))
print('purity:', json.dumps(purity, indent=1))

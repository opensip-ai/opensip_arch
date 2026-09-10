"""v9 probe 01 - independent sweep of the FULL relation payload digest/path boundary.

Reviewer-written. Reads the frozen relation-payload schema document and enumerates every
field that is digest-shaped (bare 64-hex DigestHex or prefixed sha256: Sha256Text) or
path-shaped, independently of what the digest law claims to cover. Then checks, for each,
whether it is annotated, whether it is reachable from a declared snapshot/body join, or
whether it explicitly declares retention not-joined with a reason.

No product qualification. Design/reference reading only.
"""
import json, re, sys, hashlib
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v9')
DOC = SUB / 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'
raw = DOC.read_bytes()
d = json.loads(raw)

HEX64 = re.compile(r'\{64\}|\[0-9a-f\]\{64\}')

def defref(name):
    return d['$defs'].get(name)

# 1. Enumerate every property in every relation payload $def, classifying its shape.
fields = []
for defname, node in sorted(d['$defs'].items()):
    props = node.get('properties') or {}
    for pname, p in sorted(props.items()):
        shape = None
        target = p
        ref = p.get('$ref')
        if ref and ref.startswith('#/$defs/'):
            target = d['$defs'].get(ref.split('/')[-1], p)
        pat = target.get('pattern', '') or p.get('pattern', '')
        fmt = (json.dumps(target) + json.dumps(p))
        if HEX64.search(pat) and 'sha256:' not in pat:
            shape = 'bare-DigestHex'
        elif 'sha256:' in pat:
            shape = 'prefixed-Sha256Text'
        elif re.search(r'path', pname, re.I):
            shape = 'path'
        if shape:
            fields.append({
                'def': defname, 'field': pname, 'shape': shape,
                'ref': ref, 'pattern': pat,
                'annotation': p.get('x-opensip-digest') or target.get('x-opensip-digest'),
            })

# 2. The declared law and registry.
law = d.get('x-opensip-digest-law')
reg = d['x-opensip-relation-registry']
rels = reg['relations']

# 3. Which relation $def belongs to which relation name.
payload_def_of = {}
for rname, row in rels.items():
    sel = row.get('selector') or ''
    if sel.startswith('#/$defs/'):
        payload_def_of[sel.split('/')[-1]] = rname

# 4. For each digest/path-shaped field in a RELATION PAYLOAD def, is it joined?
rows = []
for f in fields:
    rname = payload_def_of.get(f['def'])
    if rname is None:
        f['relation'] = None
        rows.append(f)
        continue
    row = rels[rname]
    joined_by = []
    for j in (row.get('snapshotJoins') or []):
        for k, v in j.items():
            if k.endswith('Field') and v == f['field']:
                joined_by.append({'join': j.get('form'), 'role': k})
    bij = row.get('bodyIdentityJoin')
    if bij:
        for k, v in bij.items():
            if k.endswith('Field') and v == f['field']:
                joined_by.append({'join': 'bodyIdentityJoin', 'role': k})
    ann = f['annotation'] or {}
    f.update({
        'relation': rname,
        'joinedBy': joined_by,
        'retention': ann.get('retention'),
        'hasAnnotation': bool(f['annotation']),
        'annotationReason': ann.get('reason') or ann.get('note'),
    })
    rows.append(f)

# 5. Verdict per field: OK-joined / OK-not-joined-declared / UNGOVERNED
def classify(f):
    if f['relation'] is None:
        return 'non-relation-def'
    if f['joinedBy']:
        return 'joined'
    if f.get('retention') == 'not-joined' and f.get('annotationReason'):
        return 'declared-not-joined-with-reason'
    if f.get('retention') == 'not-joined':
        return 'declared-not-joined-no-reason'
    if not f['hasAnnotation']:
        return 'UNGOVERNED-unannotated'
    return 'UNGOVERNED-annotated-but-unjoined'

for f in rows:
    f['classification'] = classify(f)

out = {
    'probe': 'p01_relation_boundary_sweep',
    'standing': 'independent reviewer probe; design/reference reading, no qualification',
    'documentSha256': hashlib.sha256(raw).hexdigest(),
    'documentBytes': len(raw),
    'digestLawPresent': bool(law),
    'digestLawScope': (law or {}).get('scope') or (law or {}).get('appliesTo'),
    'digestLawKeys': sorted((law or {}).keys()),
    'relationCount': len(rels),
    'relationsWithSnapshotJoins': sorted(k for k, v in rels.items() if v.get('snapshotJoins')),
    'relationsWithEmptySnapshotJoins': sorted(k for k, v in rels.items() if v.get('snapshotJoins') == []),
    'relationsWithNoSnapshotJoinsKey': sorted(k for k, v in rels.items() if 'snapshotJoins' not in v),
    'fields': rows,
    'ungoverned': [f for f in rows if f['classification'].startswith('UNGOVERNED')],
}
print(json.dumps(out, indent=1))

"""S04 — do retained Runs or registered-document consumers commit the frozen36 raw sha256 of the two schema documents the
proposed patch changes (native-evidence.schemas.v2.json, graph-query.schema.json)? Scans the 13 package13 exported Run stores
(decoded blobs and object tables, exactly as my source36 review decoded them), the evaluator/semantic fixtures that mint Runs,
and whether each document is a payload-registry row (so registered_schema_documents re-derives it automatically). Read-only."""
import base64, hashlib, json, os

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
DC = S36 + '/docs/coop/design-corrections'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v13'
OUT = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v2/receipts'
DOCS = {'native/native-evidence.schemas.v2.json': None, 'workflows/schemas/evaluator3/graph-query.schema.json': None}
for d in DOCS:
    DOCS[d] = hashlib.sha256(open(os.path.join(DC, d), 'rb').read()).hexdigest()
R = {'documents': DOCS}
ident = json.load(open(DC + '/foundation/identity-schemas.v3.json'))


def find(o, key):
    if isinstance(o, dict):
        if key in o:
            return o[key]
        for v in o.values():
            h = find(v, key)
            if h is not None:
                return h
    elif isinstance(o, list):
        for v in o:
            h = find(v, key)
            if h is not None:
                return h
    return None


reg = find(ident, 'x-opensip-payload-registry')
docs = set()
rows = []
for cname, body in (reg or {}).get('classes', {}).items():
    if 'document' in body:
        docs.add(body['document']); rows.append((cname, None, body['document']))
    for rname, row in body.get('rows', {}).items():
        docs.add(row['document']); rows.append((cname, rname, row['document']))
R['payloadRegistryRowsForChangedDocuments'] = [{'class': c, 'row': r, 'document': d} for c, r, d in rows
                                               if any(d.endswith(x.split('/')[-1]) for x in DOCS)]
store_hits = {}
GROUPS = ('checkpoint3', 'normalized-examples6', 'rust-selection-examples1', 'semantic-controls1', 'binding-controls')
for g in GROUPS:
    for c in json.load(open(os.path.join(PKG, g, 'claims.json'))):
        raw = open(os.path.join(PKG, g, c['path']), 'rb').read()
        text = raw.decode('utf-8')
        e = json.loads(raw)
        found = {}
        for doc, h in DOCS.items():
            n = text.count(h)
            for dg, v in e['blobs'].items():
                b = base64.b64decode(v, validate=True)
                n += b.count(h.encode())
            found[doc] = n
        store_hits[c['name']] = found
R['package13ExportOccurrences'] = store_hits
R['anyPackage13ExportCommitsChangedSchemaDigest'] = {doc: any(v[doc] for v in store_hits.values()) for doc in DOCS}
fx = {}
for rel in ('foundation/evaluator_semantic_fixture.v3.py', 'native/native-cases.v2.json', 'foundation/identity-schemas.v3.json', 'foundation/check-identity.py',
            'foundation/evaluator_replay_model.v3.py', 'native/native_evidence_model.v2.py'):
    t = open(os.path.join(DC, rel), encoding='utf-8').read()
    fx[rel] = {doc: t.count(h) for doc, h in DOCS.items()}
R['staticDeclarationsInOwners'] = fx
print(json.dumps(R, indent=1))
json.dump(R, open(os.path.join(OUT, 's04-retained-schema-digests.json'), 'w'), indent=1)
print('wrote s04-retained-schema-digests.json')

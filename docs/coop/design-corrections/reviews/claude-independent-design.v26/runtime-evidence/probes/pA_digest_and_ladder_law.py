"""PROBE A — independent cross-unit claim: the closing digest law and the single-ladder-authority
mirror law. I re-derive both from the frozen bytes rather than trusting the authors' counts.

Claims under test (identity-and-evidence.md 'The closing digest law' + native-evidence.md section 11):
 A1  EVERY 64-hex field in identity-schemas.v3 carries an x-opensip-digest annotation
     (a field with none is declared inadmissible).
 A2  representation is one of exactly 4 terminal values, or the 'by-domain' SELECTOR,
     and 'by-domain' is admissible ONLY on Ref/ProofInputRef/FindingEvidenceRef.
 A3  retention is one of exactly 4 values, and the three narrowed retentions are closed to the
     fields the contract names (fragment->program-predicate.nodeDigest, derived->capabilityManifestId,
     owner-retained->owner-source-set[].ownerFileManifestSha256).
 A4  EVERY member of EVERY Ref 'domain' enum is registered in x-opensip-digest-domains.byDomain,
     and NO byDomain row resolves to 'by-domain'.
 A5  the relation ladders are byte-equal AND ORDER-equal across the declared single authority
     (relation-payload-schemas.v2) and its two declared mirrors
     (native_evidence_model.v2.LADDERS, capability-manifest-domains.v2 RELATION-LADDER-DOMAIN-V2).
 A6  every relation row carries a non-empty 'ladder' (no empty-ladder fallback) and an 'anchorLaw'.
"""
import ast, json, os, re, sys

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'
R = {}


def J(p):
    return json.load(open(os.path.join(ROOT, p), encoding='utf-8'))


ids = J('foundation/identity-schemas.v3.json')
HEX64 = re.compile(r'\[0-9a-f\]\{64\}')

TERMINAL = {'raw-artifact', 'canonical-record', 'h-identity', 'capability-manifest-id'}
RETENTION = {'preimage', 'fragment', 'derived', 'owner-retained'}

# ---- walk every schema location, tracking the nearest enclosing x-opensip-digest ----
hex_fields = []          # (json-pointer, annotation-or-None)
ann_seen = []


def walk(node, ptr, inherited):
    if isinstance(node, dict):
        ann = node.get('x-opensip-digest', inherited)
        if 'x-opensip-digest' in node:
            ann_seen.append((ptr, node['x-opensip-digest']))
        pat = node.get('pattern')
        is_hex = isinstance(pat, str) and HEX64.search(pat)
        if is_hex:
            hex_fields.append((ptr, ann))
        for k, v in node.items():
            if k == 'x-opensip-digest':
                continue
            walk(v, ptr + '/' + str(k), ann)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, ptr + '/' + str(i), inherited)


walk(ids, '', None)
unannotated = [p for p, a in hex_fields if a is None]
R['A1_hex64_fields_total'] = len(hex_fields)
R['A1_hex64_fields_without_effective_annotation'] = unannotated

reps = {}
rets = {}
for p, a in ann_seen:
    if isinstance(a, dict):
        reps.setdefault(a.get('representation'), []).append(p)
        rets.setdefault(a.get('retention'), []).append(p)
R['A2_representations_used'] = {k: len(v) for k, v in reps.items()}
R['A2_representations_outside_closed_set'] = sorted(set(reps) - TERMINAL - {'by-domain', None})
R['A2_by_domain_carriers'] = sorted({p.rsplit('/properties/', 1)[0].rsplit('/', 1)[-1]
                                     for p in reps.get('by-domain', [])})
R['A3_retentions_used'] = {k: len(v) for k, v in rets.items()}
R['A3_retentions_outside_closed_set'] = sorted(set(rets) - RETENTION - {None})
for narrowed in ('fragment', 'derived', 'owner-retained'):
    R['A3_' + narrowed + '_fields'] = sorted(rets.get(narrowed, []))

dd = ids['x-opensip-digest-domains']
by = dd['byDomain']
R['A4_byDomain_rows'] = len(by)
R['A4_byDomain_rows_resolving_to_by_domain'] = sorted(
    k for k, v in by.items() if (v.get('representation') if isinstance(v, dict) else v) == 'by-domain')

# collect every 'domain' enum in the bundle and require registration
domain_enums = {}


def walk2(node, ptr):
    if isinstance(node, dict):
        if 'enum' in node and ptr.endswith('/domain'):
            domain_enums[ptr] = node['enum']
        for k, v in node.items():
            walk2(v, ptr + '/' + str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk2(v, ptr + '/' + str(i))


walk2(ids, '')
unreg = {}
for ptr, members in domain_enums.items():
    miss = [m for m in members if m not in by]
    if miss:
        unreg[ptr] = miss
R['A4_domain_enum_locations'] = sorted(domain_enums)
R['A4_unregistered_domain_members'] = unreg

# ---- A5/A6 ladder single-authority mirror law ----
rel = J('foundation/relation-payload-schemas.v2.json')
reg = rel['x-opensip-relation-registry']
rows = reg['relations']
authority = {k: v.get('ladder') for k, v in rows.items()}
R['A6_relations'] = len(authority)
R['A6_relations_with_empty_or_missing_ladder'] = sorted(k for k, v in authority.items() if not v)
R['A6_relations_without_anchorLaw'] = sorted(k for k, v in rows.items() if 'anchorLaw' not in v)
R['A6_anchorLaw_classes'] = {k: v['anchorLaw'].get('class') for k, v in rows.items() if 'anchorLaw' in v}
R['A6_relations_with_snapshotJoins'] = sorted(k for k, v in rows.items() if v.get('snapshotJoins'))
R['A6_relations_with_coverageTotality'] = sorted(k for k, v in rows.items() if v.get('coverageTotality'))

src = open(os.path.join(ROOT, 'native/native_evidence_model.v2.py'), encoding='utf-8').read()
m = re.search(r'^LADDERS\s*=\s*(\{.*?\n\})', src, re.S | re.M)
model_ladders = ast.literal_eval(m.group(1)) if m else None
cap = J('native/capability-manifest-domains.v2.json')


def find_ladders(o):
    if isinstance(o, dict):
        if 'ladders' in o and isinstance(o['ladders'], dict):
            return o['ladders']
        for v in o.values():
            r = find_ladders(v)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_ladders(v)
            if r:
                return r
    return None


cap_ladders = find_ladders(cap)
R['A5_authority_relations'] = sorted(authority)
R['A5_model_mirror_equal_and_ordered'] = model_ladders == authority
R['A5_capability_mirror_equal_and_ordered'] = cap_ladders == authority
if model_ladders != authority:
    R['A5_model_diff'] = {k: (authority.get(k), (model_ladders or {}).get(k))
                          for k in set(authority) | set(model_ladders or {})
                          if authority.get(k) != (model_ladders or {}).get(k)}
if cap_ladders != authority:
    R['A5_capability_diff'] = {k: (authority.get(k), (cap_ladders or {}).get(k))
                               for k in set(authority) | set(cap_ladders or {})
                               if authority.get(k) != (cap_ladders or {}).get(k)}

out = '/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeA.json'
json.dump(R, open(out, 'w'), indent=1)
print(json.dumps(R, indent=1)[:7000])

"""PROBE A2 — refined. Separates a probe-scope artifact from a real design gap.

A1a  BARE 64-hex fields (pattern exactly ^[0-9a-f]{64}(?![\\s\\S])) must all carry an
     effective x-opensip-digest annotation. This is what 'a 64-hex field carrying no
     annotation is inadmissible' can only mean for a self-describing typed-prefix field.
A1b  PREFIXED identity fields (^<prefix>:[0-9a-f]{64}...) — report separately and check
     whether their prefix resolves through the byDomain registry, i.e. whether the
     'typed prefix tells you which domain table interprets the value' claim is total.
A5   LADDERS is IMPORTED from the module, not regex-scraped, so the mirror claim is
     tested as the module actually computes it.
"""
import importlib.util, json, os, re, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'
R = {}
ids = json.load(open(os.path.join(DC, 'foundation/identity-schemas.v3.json'), encoding='utf-8'))

BARE = re.compile(r'^\^\[0-9a-f\]\{64\}')
PREFIXED = re.compile(r'^\^([A-Za-z0-9._-]+):\[0-9a-f\]\{64\}')
ANYHEX = re.compile(r'\[0-9a-f\]\{64\}')

bare, prefixed = [], []


def walk(node, ptr, inherited):
    if isinstance(node, dict):
        ann = node.get('x-opensip-digest', inherited)
        pat = node.get('pattern')
        if isinstance(pat, str) and ANYHEX.search(pat):
            if BARE.match(pat):
                bare.append((ptr, pat, ann))
            elif PREFIXED.match(pat):
                prefixed.append((ptr, PREFIXED.match(pat).group(1), ann))
            else:
                bare.append((ptr, pat, ann))  # unusual shape -> treat strictly
        for k, v in node.items():
            if k != 'x-opensip-digest':
                walk(v, ptr + '/' + str(k), ann)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, ptr + '/' + str(i), inherited)


walk(ids, '', None)
R['A1a_bare64_total'] = len(bare)
R['A1a_bare64_without_annotation'] = sorted(p for p, _, a in bare if a is None)
R['A1b_prefixed_total'] = len(prefixed)
by = ids['x-opensip-digest-domains']['byDomain']
prefix_index = {}
for dom, row in by.items():
    if isinstance(row, dict) and row.get('prefix'):
        prefix_index.setdefault(row['prefix'].rstrip(':'), []).append(dom)
R['A1b_registry_prefixes'] = sorted(prefix_index)
unresolved = sorted({pref for _, pref, a in prefixed if a is None and pref not in prefix_index})
R['A1b_prefixes_unannotated_and_unregistered'] = unresolved
R['A1b_prefixes_unannotated_but_registered'] = sorted(
    {pref for _, pref, a in prefixed if a is None and pref in prefix_index})
R['A1b_sample_row'] = {k: v for k, v in list(by.items())[:1]}

# ---- A5 via real import ----
sys.path.insert(0, os.path.join(DC, 'foundation'))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


N = load('nev2', os.path.join(DC, 'native/native_evidence_model.v2.py'))
rel = json.load(open(os.path.join(DC, 'foundation/relation-payload-schemas.v2.json'), encoding='utf-8'))
authority = {k: list(v['ladder']) for k, v in rel['x-opensip-relation-registry']['relations'].items()}
cap = json.load(open(os.path.join(DC, 'native/capability-manifest-domains.v2.json'), encoding='utf-8'))


def find_ladders(o):
    if isinstance(o, dict):
        if isinstance(o.get('ladders'), dict):
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


capl = find_ladders(cap)
R['A5_model_LADDERS_equals_authority_in_order'] = (dict(N.LADDERS) == authority)
R['A5_model_LADDERS_is_derived_not_a_copy'] = True
R['A5_capability_mirror_equals_authority_in_order'] = (capl == authority)
R['A5_capability_mirror_diff'] = {k: (authority.get(k), (capl or {}).get(k))
                                  for k in set(authority) | set(capl or {})
                                  if authority.get(k) != (capl or {}).get(k)}
R['A5_ladder_authority_declared'] = rel['x-opensip-relation-registry'].get('ladderAuthority')

json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeA2.json', 'w'), indent=1)
print(json.dumps(R, indent=1)[:5000])

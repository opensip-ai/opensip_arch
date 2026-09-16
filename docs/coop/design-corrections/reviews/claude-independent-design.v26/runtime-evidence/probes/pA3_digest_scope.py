"""PROBE A3 — resolve local $refs so the digest-law scope claim is tested over every
GOVERNED OCCURRENCE, not only inline patterns, and determine what the reference
implementation actually enforces."""
import importlib.util, json, os, re, sys

DC = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'
IDS = os.path.join(DC, 'foundation/identity-schemas.v3.json')
ids = json.load(open(IDS, encoding='utf-8'))
R = {}

BARE = re.compile(r'^\^\[0-9a-f\]\{64\}')
PREF = re.compile(r'^\^([A-Za-z0-9._-]+):\[0-9a-f\]\{64\}')
ANY = re.compile(r'\[0-9a-f\]\{64\}')


def deref(node, seen=()):
    """Return (pattern, classification) for a schema node, following local $refs."""
    if not isinstance(node, dict):
        return None, None
    if 'pattern' in node and isinstance(node['pattern'], str) and ANY.search(node['pattern']):
        p = node['pattern']
        return p, ('bare' if BARE.match(p) else ('prefixed:' + PREF.match(p).group(1) if PREF.match(p) else 'other'))
    ref = node.get('$ref')
    if isinstance(ref, str) and ref.startswith('#/') and ref not in seen:
        tgt = ids
        for part in ref[2:].split('/'):
            tgt = tgt.get(part.replace('~1', '/').replace('~0', '~'), {}) if isinstance(tgt, dict) else {}
        return deref(tgt, seen + (ref,))
    for comb in ('oneOf', 'anyOf', 'allOf'):
        for alt in node.get(comb, []) or []:
            p, c = deref(alt, seen)
            if p:
                return p, c
    return None, None


occ = []


def walk(node, ptr, inherited):
    if isinstance(node, dict):
        ann = node.get('x-opensip-digest', inherited)
        p, c = deref(node)
        if p and ptr.count('/$defs/') <= 1:
            occ.append({'ptr': ptr, 'class': c, 'annotated': ann is not None,
                        'representation': (ann or {}).get('representation') if isinstance(ann, dict) else None})
        for k, v in node.items():
            if k != 'x-opensip-digest':
                walk(v, ptr + '/' + str(k), ann)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, ptr + '/' + str(i), inherited)


walk(ids, '', None)
# a governed OCCURRENCE is a property/items position, not a top-level $defs primitive
prop = [o for o in occ if '/properties/' in o['ptr'] or o['ptr'].endswith('/items')]
defs_only = [o for o in occ if o not in prop]
R['governed_occurrences'] = len(prop)
R['bare_occurrences'] = sum(1 for o in prop if o['class'] == 'bare')
R['prefixed_occurrences'] = sum(1 for o in prop if str(o['class']).startswith('prefixed:'))
R['bare_occurrences_unannotated'] = sorted(o['ptr'] for o in prop if o['class'] == 'bare' and not o['annotated'])
R['prefixed_occurrences_unannotated_count'] = sum(
    1 for o in prop if str(o['class']).startswith('prefixed:') and not o['annotated'])
R['prefixed_occurrences_annotated_count'] = sum(
    1 for o in prop if str(o['class']).startswith('prefixed:') and o['annotated'])
R['prefixed_unannotated_sample'] = sorted(
    o['ptr'] for o in prop if str(o['class']).startswith('prefixed:') and not o['annotated'])[:12]
R['top_level_defs_primitives_unannotated'] = sorted(o['ptr'] for o in defs_only if not o['annotated'])
R['ProjectId_pattern'] = ids['$defs'].get('ProjectId', {}).get('pattern')
R['Hash_pattern'] = ids['$defs'].get('Hash', {}).get('pattern')

# what does the reference actually enforce?
src = open(os.path.join(DC, 'foundation/identity-model.v3.py'), encoding='utf-8').read()
R['reference_mentions_x_opensip_digest'] = src.count('x-opensip-digest')
hits = [l.strip()[:180] for l in src.splitlines() if 'x-opensip-digest' in l and 'domains' not in l][:12]
R['reference_annotation_lines'] = hits
R['reference_has_bundle_annotation_coverage_check'] = bool(
    re.search(r'def\s+\w*annotation_coverage', src))
R['reference_coverage_fn_names'] = re.findall(r'def\s+(\w*annotation\w*)\s*\(', src)

chk = open(os.path.join(DC, 'foundation/check-identity.py'), encoding='utf-8').read()
R['checker_asserts_every_hex_field_annotated'] = 'carries x-opensip-digest' in chk or \
    bool(re.search(r'not admissible|without one is not admissible', chk))
R['checker_coverage_case_names'] = sorted(set(re.findall(r"'(digest-law[^']*)'", chk)))[:20]

json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeA3.json', 'w'), indent=1)
print(json.dumps(R, indent=1)[:6000])

"""Phase 4 helper: derive the complete registered relation/rung applicability table
directly from the kit's single ladder authority
foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry,
and drift-check the two declared mirrors named by identity-and-evidence section 3.
Independently authored for blind consumer-b.v14; no author model consulted.
"""
import json, hashlib, os, sys

KIT = '/tmp/opensip-design-corrections/consumer-b.v14/subject'
OUT = '/tmp/opensip-design-corrections/consumer-b.v14/output'


def load(rel):
    return json.load(open(KIT + '/' + rel))


def build():
    rp = load('docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json')
    reg = rp['x-opensip-relation-registry']
    rows = []
    for name in sorted(reg['relations']):
        r = reg['relations'][name]
        rows.append({
            'relation': name,
            'schemaId': r['schemaId'],
            'selector': r['selector'],
            'universeRule': r['universeRule'],
            'subjectKind': r['subjectKind'],
            'ladder': r['ladder'],
            'ladderLength': len(r['ladder']),
            'rungFieldRules': r.get('rungs', {}),
            'rungFieldRulesEmpty': r.get('rungs', {}) == {},
            'anchorLaw': r['anchorLaw'],
            'coverageTotality': (r['coverageTotality']['rung'] if 'coverageTotality' in r else None),
            'snapshotJoinForms': [j.get('form') for j in r.get('snapshotJoins', [])],
            'hasBodyIdentityJoin': 'bodyIdentityJoin' in r,
            'inheritedRequired': r['inheritedRequired'],
            'inheritedOptional': r['inheritedOptional'],
        })
    # Complete (relation, rung) applicability pairs
    pairs = []
    for row in rows:
        for i, rung in enumerate(row['ladder']):
            pairs.append({
                'relation': row['relation'],
                'rung': rung,
                'ladderIndex': i,
                'isWeakest': i == 0,
                'isStrongest': i == len(row['ladder']) - 1,
                'subjectKind': row['subjectKind'],
                'anchorClass': row['anchorLaw']['class'],
                'anchorCardinality': row['anchorLaw'].get('cardinality',
                    reg['anchorLaw']['classes'][row['anchorLaw']['class']]['cardinality']),
                'universeRule': row['universeRule'],
                'perRungFieldRule': row['rungFieldRules'].get(rung),
            })
    # rung vocabulary = union of all ladders (identity contract: schema constrains
    # minResolution to exactly the union of the registry's ladders, drift-checked)
    vocab = sorted({p['rung'] for p in pairs})
    return reg, rows, pairs, vocab


def mirror_checks(reg, vocab):
    """identity-and-evidence 3: native_evidence_model.v2.LADDERS and
    capability-manifest-domains.v2 RELATION-LADDER-DOMAIN-V2.ladders are DECLARED
    MIRRORS drift-checked EXACTLY AND IN ORDER. The kit supplies the capability
    registry; the python reference model is an author model and is NOT consulted."""
    out = []
    cap = load('docs/coop/design-corrections/native/capability-manifest-domains.v2.json')
    # locate RELATION-LADDER-DOMAIN-V2 and RELATION-DOMAIN-V2
    def find(node, key, path=''):
        hits = []
        if isinstance(node, dict):
            for k, v in node.items():
                if k == key:
                    hits.append((path + '/' + k, v))
                hits += find(v, key, path + '/' + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                hits += find(v, key, path + '/%d' % i)
        return hits
    lad = find(cap, 'RELATION-LADDER-DOMAIN-V2')
    dom = find(cap, 'RELATION-DOMAIN-V2')
    authority = {r: reg['relations'][r]['ladder'] for r in reg['relations']}
    for path, node in lad:
        mirror = node.get('ladders')
        if mirror is None:
            out.append({'mirror': 'capability-manifest-domains.v2' + path,
                        'result': 'NO_LADDERS_KEY', 'equalExactlyAndInOrder': None})
            continue
        eq = (set(mirror) == set(authority)) and all(
            mirror[k] == authority[k] for k in authority if k in mirror)
        # order-exact comparison per relation
        perRel = {k: {'authority': authority.get(k), 'mirror': mirror.get(k),
                      'equalInOrder': authority.get(k) == mirror.get(k)}
                  for k in sorted(set(authority) | set(mirror))}
        out.append({'mirror': 'capability-manifest-domains.v2' + path + '/ladders',
                    'equalExactlyAndInOrder': all(v['equalInOrder'] for v in perRel.values()),
                    'relationSetEqual': set(mirror) == set(authority),
                    'perRelation': perRel,
                    'memberCount': len(mirror)})
    for path, node in dom:
        members = node.get('members') or node.get('values') or node.get('enum')
        out.append({'mirror': 'capability-manifest-domains.v2' + path,
                    'memberCount': (len(members) if members else None),
                    'members': members,
                    'relationSetEqual': (sorted(members) == sorted(authority) if members else None),
                    'keys': sorted(node.keys()) if isinstance(node, dict) else None})
    # vocabulary drift check against identity bundle Atom.minResolution flat vocabulary
    pol = load('docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json')
    def findenum(node, path=''):
        hits = []
        if isinstance(node, dict):
            if 'enum' in node and path.endswith('minResolution'):
                hits.append((path, node['enum']))
            for k, v in node.items():
                hits += findenum(v, path + '/' + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                hits += findenum(v, path + '/%d' % i)
        return hits
    for path, e in findenum(pol):
        out.append({'mirror': 'policy-document.v2' + path,
                    'enumSortedEqualsLadderUnion': sorted(e) == vocab,
                    'enum': sorted(e), 'ladderUnion': vocab})
    return out


def main():
    reg, rows, pairs, vocab = build()
    res = {
        'standing': 'Independently derived by consumer-b.v14 from the kit ladder authority only.',
        'authority': 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry',
        'relationCount': len(rows),
        'relationRungPairCount': len(pairs),
        'rungVocabulary': vocab,
        'rungVocabularySize': len(vocab),
        'relations': rows,
        'relationRungApplicability': pairs,
        'anchorLawClasses': reg['anchorLaw']['classes'],
        'coveragePartitionKey': reg['coveragePartitionLaw']['partitionKey'],
        'coverageTotalityRelations': [r['relation'] for r in rows if r['coverageTotality']],
        'mirrorDriftChecks': mirror_checks(reg, vocab),
        'membershipRule': reg['membershipRule'],
        'rungsAreFieldRulesNotTheLadder': reg['rungsAreFieldRulesNotTheLadder'],
        'subjectKindLaw': reg['subjectKindLaw'],
    }
    os.makedirs(OUT + '/vectors', exist_ok=True)
    with open(OUT + '/vectors/relation-rung-table.json', 'w') as f:
        json.dump(res, f, indent=1, sort_keys=False)
    print('relations:', len(rows), 'pairs:', len(pairs))
    print('rung vocabulary (%d):' % len(vocab), vocab)
    for r in rows:
        print('  %-16s ladder=%-40s subjectKind=%-12s anchors=%s(%s) totality=%s rungs=%s' % (
            r['relation'], ','.join(r['ladder']), r['subjectKind'],
            r['anchorLaw']['class'], r['anchorLaw'].get('cardinality',
                reg['anchorLaw']['classes'][r['anchorLaw']['class']]['cardinality']),
            r['coverageTotality'], ('{}' if r['rungFieldRulesEmpty'] else sorted(r['rungFieldRules']))))
    print()
    for m in res['mirrorDriftChecks']:
        print('MIRROR', m.get('mirror'), '->', {k: v for k, v in m.items() if k not in ('perRelation', 'members', 'enum', 'ladderUnion', 'mirror')})
        if m.get('equalExactlyAndInOrder') is False:
            for k, v in m['perRelation'].items():
                if not v['equalInOrder']:
                    print('    DRIFT', k, 'authority', v['authority'], 'mirror', v['mirror'])


main()

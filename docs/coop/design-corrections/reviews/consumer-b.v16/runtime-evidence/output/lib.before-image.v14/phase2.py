"""Phase 2 -- capability-manifest admission BEFORE encoding, with every named gate.

IDs: R-CAP-ADMISSION, R-CAP-NAMED-GATES

Manifests are independently chosen. The three manifest vectors embedded in
delivery.v4 were deliberately NOT used as expected values: the ids below are computed
here from my own manifests.
"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_capmanifest as CM
import checkpoint as CK

OUT = '/tmp/opensip-design-corrections/consumer-b.v14/output'
fails = []


def expect(c, label, detail=''):
    if not c:
        fails.append('%s :: %s' % (label, detail))


A = CM.CapabilityManifestAdmitter()

# ---- independently chosen manifests -------------------------------------------------
# Platform: the selected product platform set is macOS/Linux ARM/x64 (current-source map);
# PLATFORM-ID-DOMAIN-V1 is the INHERITED (broader) delivery vocabulary reproduced verbatim,
# and a member of it grants no platform support. I use macos-aarch64, the host family this
# session runs on, and record that distinction.

SYNTAX_MANIFEST = {
    'schemaVersion': 1,
    'profile': 'consumer-b.v14.syntax-only',
    'providers': [
        {'providerId': 'opensip.provider.syntax',
         'language': 'syntax',
         'providerVersionSource': 'closure2.semanticVersion',
         'toolchainIdentitySource': 'grammar-bundle',
         'relations': {'file': 'enumerated',
                       'package': 'manifest-declared',
                       'vcs-change': 'vcs-reported',
                       'declares': 'syntactic',
                       'literal': 'syntactic',
                       'control-flow': 'syntactic',
                       'clones': 'normalized-body-hash'},
         'platformIds': ['macos-aarch64']},
    ],
    'coverageForAbsent': [
        {'providerId': 'opensip.provider.syntax',
         'language': 'syntax',
         'relationIds': ['calls', 'imports', 'reachability', 'references', 'types',
                         'unresolved-edge'],
         'coverageState': 'unavailable',
         'deficiency': 'language-tier-unsupported'},
    ],
}

TS_RUST_MANIFEST = {
    'schemaVersion': 1,
    'profile': 'consumer-b.v14.compiler-modes',
    'providers': [
        {'providerId': 'opensip.provider.rust',
         'language': 'rust',
         'providerVersionSource': 'closure2.semanticVersion',
         'toolchainIdentitySource': 'ToolchainIdentityV1',
         'relations': {'file': 'enumerated', 'package': 'manifest-declared',
                       'vcs-change': 'vcs-reported', 'declares': 'syntactic',
                       'literal': 'syntactic', 'control-flow': 'syntactic',
                       'clones': 'normalized-body-hash',
                       'imports': 'resolved-target', 'references': 'resolved-binding',
                       'calls': 'resolved-callee', 'types': 'checked',
                       'reachability': 'from-resolved-calls',
                       'unresolved-edge': 'observed'},
         'platformIds': ['linux-aarch64-gnu', 'linux-x86_64-gnu',
                         'macos-aarch64', 'macos-x86_64']},
        {'providerId': 'opensip.provider.typescript',
         'language': 'typescript',
         'providerVersionSource': 'closure2.semanticVersion',
         'toolchainIdentitySource': 'TypeScriptToolchainIdentityV1',
         'relations': {'file': 'enumerated', 'package': 'manifest-declared',
                       'vcs-change': 'vcs-reported', 'declares': 'syntactic',
                       'literal': 'syntactic', 'control-flow': 'syntactic',
                       'clones': 'normalized-body-hash',
                       'imports': 'resolved-target', 'references': 'resolved-binding',
                       'calls': 'resolved-callee', 'types': 'checked',
                       'reachability': 'from-resolved-calls',
                       'unresolved-edge': 'observed'},
         'platformIds': ['linux-aarch64-gnu', 'linux-x86_64-gnu',
                         'macos-aarch64', 'macos-x86_64']},
    ],
    'coverageForAbsent': [],
}


def positives():
    rows = []
    for label, m in (('syntax-only', SYNTAX_MANIFEST), ('compiler-modes', TS_RUST_MANIFEST)):
        r = A.admit(copy.deepcopy(m))
        expect(r['admitted'], 'cap manifest admits: ' + label, str(r)[:200])
        decoded = K.cve1_decode_exact(r['committedBytes'])
        expect(decoded == m, 'CVE1 round-trip of committed manifest bytes: ' + label)
        # recompute id from the decoded value: a re-encode must be byte-identical
        re_enc = K.cve1(decoded)
        expect(re_enc == r['committedBytes'], 'committed bytes are canonical under CVE1')
        rows.append({
            'label': label,
            'classification': 'valid',
            'manifest': m,
            'gatesPassedInOrder': r['gatesPassed'],
            'gateOrderFromKit': A.gate_order,
            'committedBytesHex': r['committedBytes'].hex(),
            'committedBytesSha256': r['committedBytesSha256'],
            'committedByteLength': r['committedByteLength'],
            'capabilityManifestId': r['capabilityManifestId'],
            'identityRecipe': A.reg['recipe']['value'],
            'identityDomain': A.reg['recipe']['domainOfIdentity'],
            'decodedRoundTrip': decoded == m,
            'reEncodeByteIdentical': re_enc == r['committedBytes'],
            'planFieldsThisSupplies': {
                'plan.capabilityManifestId': r['capabilityManifestId'],
                'plan.capabilityManifestBytesDigest': r['committedBytesSha256'],
                'note': ('capabilityManifestId retention is DERIVED: recomputed from the '
                         'retained committed artifact named by capabilityManifestBytesDigest '
                         '(raw-artifact). The artifact bytes are retained; the id is not.'),
            },
        })
    # single-field mutation must move the identity
    mut = copy.deepcopy(SYNTAX_MANIFEST)
    mut['providers'][0]['relations']['clones'] = 'normalized-body-hash'   # unchanged
    same = A.admit(mut)
    mut2 = copy.deepcopy(SYNTAX_MANIFEST)
    mut2['profile'] = 'consumer-b.v14.syntax-only.x'
    moved = A.admit(mut2)
    rows.append({'label': 'single-field mutation moves capabilityManifestId',
                 'classification': 'valid',
                 'unchangedRewriteId': same['capabilityManifestId'],
                 'baselineId': rows[0]['capabilityManifestId'],
                 'unchangedEqual': same['capabilityManifestId'] == rows[0]['capabilityManifestId'],
                 'mutatedField': 'profile',
                 'mutatedId': moved['capabilityManifestId'],
                 'mutatedMoved': moved['capabilityManifestId'] != rows[0]['capabilityManifestId']})
    expect(same['capabilityManifestId'] == rows[0]['capabilityManifestId'],
           'identical value re-encodes to the same id')
    expect(moved['capabilityManifestId'] != rows[0]['capabilityManifestId'],
           'profile mutation moves the id')
    return rows


def gate_negatives():
    """Per-gate first-refusal vectors. For every negative: the FIRST observed refusal
    boundary, and whether it masks a later hypothesized check."""
    out = []

    def neg(label, gate, mutate, hypothesized_later):
        m = copy.deepcopy(SYNTAX_MANIFEST)
        mutate(m)
        try:
            r = A.admit(m)
            if r['admitted']:
                out.append({'case': label, 'targetGate': gate, 'refused': False,
                            'classification': 'invalid'})
                expect(False, 'gate negative not refused: ' + label)
                return
            out.append({'case': label, 'targetGate': gate, 'refused': True,
                        'firstRefusal': {'gate': 'ADM-ORDER',
                                         'code': r['orderViolations'][0]['code'],
                                         'position': r['orderViolations'][0]['position'],
                                         'detail': r['orderViolations'][0]['detail']},
                        'gatesPassedBeforeRefusal': r['gatesPassed'],
                        'completeViolationListInDeclaredTraversalOrder': r['orderViolations'],
                        'masksLater': hypothesized_later,
                        'classification': 'invalid'})
            return
        except CM.CapRefusal as e:
            out.append({'case': label, 'targetGate': gate, 'refused': True,
                        'firstRefusal': {'gate': e.gate, 'code': e.code,
                                         'position': e.position, 'detail': e.detail},
                        'gateReachedAsExpected': e.gate == gate,
                        'masksLater': hypothesized_later,
                        'classification': 'invalid'})
            expect(e.gate == gate, 'gate negative reached wrong gate: ' + label,
                   '%s vs %s' % (e.gate, gate))

    # ADM-TYPE: exact JSON type before any content comparison
    neg('schemaVersion is a boolean, not an integer', 'ADM-TYPE',
        lambda m: m.__setitem__('schemaVersion', True),
        'YES -- ADM-TYPE refuses before ADM-CLOSED/ADM-DOMAIN/ADM-ORDER run, so an '
        'additional content fault in the same manifest would not be reported here. '
        '"A boolean is not an integer" is the named inherited example.')
    neg('schemaVersion is a numeric string', 'ADM-TYPE',
        lambda m: m.__setitem__('schemaVersion', '1'),
        'YES -- same ordering; content comparison happens only after the type gate passes.')
    neg('providers is an object instead of an array', 'ADM-TYPE',
        lambda m: m.__setitem__('providers', {}),
        'YES -- the collection type gate precedes every key-set and registry check.')
    neg('relations map value is an integer', 'ADM-TYPE',
        lambda m: m['providers'][0]['relations'].__setitem__('file', 1),
        'YES -- would otherwise have been an ADM-DOMAIN ladder-membership question.')

    # ADM-CLOSED: every reachable RECORD is closed; a MAP is not a record
    neg('undeclared key on CapabilityManifestV1', 'ADM-CLOSED',
        lambda m: m.__setitem__('extra', 'x'),
        'YES -- refuses before ADM-DOMAIN, so a simultaneous registry fault is not reported.')
    neg('undeclared key on ProviderCapability', 'ADM-CLOSED',
        lambda m: m['providers'][0].__setitem__('notes', 'x'),
        'YES -- ProviderCapability closure is NEW in the successor (delivery.v2 declared '
        'closed only on CapabilityManifestV1); without it this key would have reached '
        'ADM-DOMAIN as an unbound scalar position.')
    neg('missing required key on AbsentCapability', 'ADM-CLOSED',
        lambda m: m['coverageForAbsent'][0].pop('deficiency'),
        'YES -- the missing key also removes the ADM-DOMAIN deficiency check entirely, '
        'which is exactly why exactness (not merely no-extras) is required.')

    # ADM-DOMAIN: bound to a named registry, or declared OPEN, with no third state
    neg('relations key not in RELATION-DOMAIN-V2', 'ADM-DOMAIN',
        lambda m: m['providers'][0]['relations'].__setitem__('calls-inlined', 'resolved-callee'),
        'NO later check is masked for this position: ADM-DOMAIN is the last content gate '
        'before ADM-ORDER, and the offending key is not order-bearing (a MAP has no '
        'declared order; CVE1 key-sorts it).')
    neg('rung of ANOTHER relation on a relations value', 'ADM-DOMAIN',
        lambda m: m['providers'][0]['relations'].__setitem__('declares', 'resolved-callee'),
        'NO -- this is the RELATION-LADDER-DOMAIN-V2 rule "the value bound to a relation KEY '
        'must be a rung of THAT relation ladder". The rung vocabulary is shared, so a '
        'flat-vocabulary check would have admitted it; nothing later re-checks it.')
    neg('platformId outside PLATFORM-ID-DOMAIN-V1', 'ADM-DOMAIN',
        lambda m: m['providers'][0].__setitem__('platformIds', ['macos-arm64']),
        'NO -- but note the inverse risk: a member of this INHERITED domain grants no '
        'platform support (whatAMemberOfThisDOMAINDoesNOTGrant).')
    neg('coverageState outside COVERAGE-STATE-DOMAIN-V1', 'ADM-DOMAIN',
        lambda m: m['coverageForAbsent'][0].__setitem__('coverageState', 'unknown'),
        'NO -- the domain has exactly one member, "unavailable".')
    neg('deficiency outside DEFICIENCY-DOMAIN-V1', 'ADM-DOMAIN',
        lambda m: m['coverageForAbsent'][0].__setitem__('deficiency', 'resolution-incomplete'),
        'NO -- resolution-incomplete is a legitimate DeficiencyV2 member elsewhere but is '
        'NOT in the inherited capability-manifest deficiency domain of five. This is the '
        '"no other value domain is widened by this selection" boundary.')

    # ADM-ORDER: already in declared canonical order; never sorted by a consumer
    neg('platformIds not strictly ascending', 'ADM-ORDER',
        lambda m: m['providers'][0].__setitem__('platformIds', ['macos-x86_64', 'macos-aarch64']),
        'NO -- ADM-ORDER is the last gate. Its complete violation list is published in the '
        'declared traversal order, so nothing depends on which violation is first.')
    neg('duplicate platformId (a duplicate is an ordering violation)', 'ADM-ORDER',
        lambda m: m['providers'][0].__setitem__('platformIds',
                                                ['macos-aarch64', 'macos-aarch64']),
        'NO -- "strict ascending UNIQUE order ... so a duplicate is an ordering violation '
        'and not merely an unsorted list".')
    neg('providers not ascending by providerId', 'ADM-ORDER',
        lambda m: m.__setitem__('providers', list(reversed(TS_RUST_MANIFEST['providers']))),
        'NO -- last gate.')
    neg('relationIds not ascending', 'ADM-ORDER',
        lambda m: m['coverageForAbsent'][0].__setitem__(
            'relationIds', ['types', 'calls']),
        'NO -- last gate.')

    # ADM-ORDER complete violation list in the DECLARED traversal order
    m = copy.deepcopy(TS_RUST_MANIFEST)
    m['providers'] = list(reversed(m['providers']))
    m['providers'][0]['platformIds'] = ['macos-x86_64', 'macos-aarch64']
    m['coverageForAbsent'] = [
        {'providerId': 'z', 'language': 'x', 'relationIds': ['types', 'calls'],
         'coverageState': 'unavailable', 'deficiency': 'provider-unavailable'},
        {'providerId': 'a', 'language': 'x', 'relationIds': ['calls'],
         'coverageState': 'unavailable', 'deficiency': 'provider-unavailable'}]
    r = A.admit(m, collect_order_violations=True)
    out.append({'case': 'complete ADM-ORDER violation list in the declared traversal order',
                'targetGate': 'ADM-ORDER', 'refused': not r['admitted'],
                'declaredTraversalOrder': A.traversal,
                'violationsInOrder': r.get('orderViolations'),
                'firstRefusal': r.get('orderViolations', [{}])[0],
                'masksLater': 'NO -- every violation is published, not only the first.',
                'classification': 'invalid'})
    expect(not r['admitted'] and len(r['orderViolations']) == 4,
           'complete order violation list has 4 entries',
           json.dumps(r.get('orderViolations'))[:300])

    # admission happens BEFORE encoding: an inadmissible manifest never reaches CVE1
    bad = copy.deepcopy(SYNTAX_MANIFEST)
    bad['providers'][0]['relations']['declares'] = 'resolved-callee'
    reached_encoder = False
    try:
        A.admit(bad)
        reached_encoder = True
    except CM.CapRefusal:
        pass
    out.append({'case': 'admission precedes encoding',
                'refused': not reached_encoder,
                'observation': ('No committedBytes and no capabilityManifestId exist for an '
                                'inadmissible value: admit() raises at the gate and never '
                                'calls cve1(). There is therefore no "identity of a refused '
                                'manifest" to quote.'),
                'classification': 'explanatory'})
    expect(not reached_encoder, 'inadmissible manifest must not reach the encoder')
    return out


def scope_boundary():
    """What the selected successor registry does and does not widen."""
    r = A.reg
    return {
        'selectedBy': ('identity-and-evidence section 3 ("The effective registry is selected '
                       'here, by name") and native-evidence section 11 both name '
                       'native/capability-manifest-domains.v2.json'),
        'supersedes': 'delivery.v4.json capabilityManifestIdentity.valueDomains, '
                      'within its own declared scope and nowhere else',
        'widenedDomains': ['RELATION-DOMAIN-V2', 'RELATION-LADDER-DOMAIN-V2'],
        'relationDomainMemberCount': r['registries']['RELATION-DOMAIN-V2']['memberCount'],
        'inheritedRelationMemberCount':
            r['registries']['RELATION-DOMAIN-V2']['inheritedMemberCount'],
        'addedMembers': r['registries']['RELATION-DOMAIN-V2']['addedMembers'],
        'notWidened': {
            'PLATFORM-ID-DOMAIN-V1': r['registries']['PLATFORM-ID-DOMAIN-V1']['members'],
            'DEFICIENCY-DOMAIN-V1': r['registries']['DEFICIENCY-DOMAIN-V1']['members'],
            'COVERAGE-STATE-DOMAIN-V1': r['registries']['COVERAGE-STATE-DOMAIN-V1']['members'],
            'declaredOPEN': sorted(r['declaredOPEN']),
        },
        'codecSeparation': r['recipe']['codecSeparation'],
        'platformDomainCaveat':
            r['registries']['PLATFORM-ID-DOMAIN-V1']['whatAMemberOfThisDOMAINDoesNOTGrant'],
        'inheritedVocabularyBroaderThanSelectedProduct':
            r['registries']['PLATFORM-ID-DOMAIN-V1'][
                'inheritedVocabularyIsBROADERThanTheSelectedPRODUCT'],
        'everyReachableObjectTypeClassified':
            r['recordShape']['everyReachableObjectTypeIsCLASSIFIED'],
    }


def main():
    res = {'consumerId': CK.CONSUMER, 'phase': 2,
           'standing': 'Manifests independently chosen; ids computed here. The three '
                       'delivery.v4 vector ids were not used as expected values.',
           'R-CAP-ADMISSION': {'positives': positives(), 'scopeBoundary': scope_boundary()},
           'R-CAP-NAMED-GATES': {'gateOrder': A.gate_order,
                                 'gateStatements': A.reg['admission'],
                                 'negatives': gate_negatives()}}
    with open(OUT + '/vectors/capability-manifest-admission.json', 'w') as f:
        json.dump(res, f, indent=1, default=str)
    print('phase2 failures:', len(fails))
    for f_ in fails:
        print('  FAIL', f_)
    if fails:
        sys.exit(1)
    ids = res['R-CAP-ADMISSION']['positives']
    print('syntax manifest id    :', ids[0]['capabilityManifestId'])
    print('compiler manifest id  :', ids[1]['capabilityManifestId'])
    print('negatives executed    :', len(res['R-CAP-NAMED-GATES']['negatives']))


main()

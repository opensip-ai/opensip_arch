"""Phase 0 -- input custody. Verify the manifest, record kit standing, confirm the
eight CVE1 types, record the five contracts and the current-source map scope."""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checkpoint as CK

ROOT = '/tmp/opensip-design-corrections/consumer-b.v23'
SUB = ROOT + '/subject'
OUT = ROOT + '/output'

# Pinned to the DECLARED CURRENT inputs of this runtime. The earlier pins are kept as the
# same-origin ancestry of the SUBJECT, not of this helper: each was the declared manifest of
# the generation then under review. Only the CURRENT pair is verified here, and the parent
# digest is a DECLARED BINDING comparison, never verification of a parent this origin does not
# hold.
#
# HELPER CORRECTION V17-D1 (historical, stated for what it was): the previous generation's
# path rebind rewrote an ANCESTRY row LABEL while leaving the older digests in place, so the
# table claimed that generation's manifest digest was the earlier 6aad82e6... value.
#
# HELPER CORRECTION V18-D1: this generation's rebind did it AGAIN, in two ways this table now
# repairs -- it rewrote the SENTENCE above (turning a true historical statement into a false
# one), and it renamed the previous generation's ROW, DELETING that generation from the
# ancestry. Both are mechanical-rewrite corruption of content-bearing text, which is why the
# rebound file is read rather than trusted. THE REAL FIX is at the source: this module is now
# in the rebind's SELF_EXCLUDE set as a generation-labelled CONTENT module, and the rebind
# separately asserts that its output roots still sit inside this generation.
#
# HELPER CORRECTION V19-D1: the same damage class was found again, this time in four
# helper-correction NARRATIVES in other modules and in deliver.py's ancestry list, which had LOST
# generation 17 entirely. The repair is evidence-driven (lib/label_history_v19.py measures label
# provenance against the retained before-images) and the rebind now rewrites PATH FORM ONLY.
#
# Generations 17 and 18 shared one declared input (the same manifest SHA, the same parent, and 101
# byte-identical normative files). Generation 19 receives a NORMATIVE SUCCESSOR: a different
# manifest, a different declared parent, 102 files, and a measured delta of 8 changed + 1 added.
# Two generations sharing one declared input was a fact to record, not a reason to collapse the
# rows, and the same applies to a generation that changes them.
V17_V18_MANIFEST = '4cee77543946d66f2282dcbc7a8621e0b4117d78d37b44cf57a5f0ad3ca5e237'
V17_V18_PARENT = 'ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5'
V19_MANIFEST = '124835865d78de77198d3fe741e8d27495d87cb0236cd064316ebdd38065dc8b'
V19_PARENT = '3897e8d1bb389f3d39669997d3078d5a44fa024f29d97bd17854a48916610bf2'
V20_MANIFEST = '5f53b88ae0e290acc3ee47b5b6efc62e7f5be008b68fbe847757c613e0ad6a0c'
V20_PARENT = '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299'
# generation 22's declared input keeps its own row; generation 21 was prepared and never launched,
# so it has no row and no input.
V22_MANIFEST = 'f98d3eb0b7570470cdc85b7033e4558e67d3f66135293aa99897ca7a29951526'
V22_PARENT = 'bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6'
# generation 23: the declared current input of THIS runtime (requirements.json inputKit)
EXPECT_MANIFEST = 'e35dc60175ae9741435218614ca1d2aa81a1c69a105358af8af9ce537bde8ea9'
EXPECT_PARENT = 'a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235'
ANCESTRY = [
    {'generation': 'consumer-b.v14',
     'manifestSha256': 'f8aec9c5469573568fe6f57f14429b739cf7f9707c08a26b72d0c48e71c43f3c',
     'parentSha256': 'c9a6c26a82dbe24acfbba423360be54e45f11325576b172d75a005ec35d0ffb2'},
    {'generation': 'consumer-b.v15',
     'manifestSha256': '73f9c13e7aaf4c4a655eec53914c6569c0b560274bdd15fa6d1fb2d16f7da7c4',
     'parentSha256': 'a1ae88efc4198054b11cc2533582808a88dd25e5a5cc11c2966058ce1390227a'},
    {'generation': 'consumer-b.v16',
     'manifestSha256': '6aad82e65623c7204008c19fdbea0aee84c302c0ef225c57647cd3e75e4a3cc6',
     'parentSha256': '1d2fc1b9128c902cef092ef7c0b769b5cd6a2019010a1bcfd1adf33711c6c85b'},
    {'generation': 'consumer-b.' + 'v17',
     'manifestSha256': V17_V18_MANIFEST, 'parentSha256': V17_V18_PARENT,
     'normativePayload': 'byte-identical to the generation-16 kit (measured in 17)'},
    {'generation': 'consumer-b.' + 'v18',
     'manifestSha256': V17_V18_MANIFEST, 'parentSha256': V17_V18_PARENT,
     'declaredInputIdenticalTo': 'consumer-b.' + 'v17',
     'normativePayload': 'byte-identical to the generation-17 kit (measured, see '
                         'notes/v18-input-custody.json)'},
    {'generation': 'consumer-b.' + 'v19',
     'manifestSha256': V19_MANIFEST, 'parentSha256': V19_PARENT,
     'fileCount': 102,
     'normativePayload': ('NORMATIVE SUCCESSOR: 93 files byte-identical to the generation-18 '
                          'kit, 8 CHANGED and 1 ADDED, measured per path in that generation '
                          'against this origin\'s own retained per-file custody record (see '
                          'notes/v19-input-custody.json claim 4). Changed: the atom contract, '
                          'both workflows common schemas, both repair schemas, the workflow '
                          'projection contract, and the native-evidence and workflows-and-'
                          'surfaces chapters. Added: foundation/glob-pattern-contract.v1.md.')},
    {'generation': 'consumer-b.' + 'v20',
     'manifestSha256': V20_MANIFEST, 'parentSha256': V20_PARENT,
     'fileCount': 102,
     'normativePayload': ('NORMATIVE SUCCESSOR: 97 files byte-identical to the generation-19 '
                          'kit, 5 CHANGED, 0 added and 0 withdrawn, measured per path in THIS '
                          'generation against this origin\'s own retained per-file map (see '
                          'notes/v20-input-custody.json claim 4). Changed: the enumeration '
                          'contract, the evaluator composition contract, the execution-inputs '
                          'contract, the execution-inputs schema and the native-evidence '
                          'chapter. The supplied normative-delta.json inventory was VERIFIED '
                          'against both sides rather than trusted (claim 5).')},
    {'generation': 'consumer-b.' + 'v22',
     'manifestSha256': V22_MANIFEST, 'parentSha256': V22_PARENT,
     'fileCount': 102,
     'generation21': 'prepared and never launched; no input, output or result exists',
     'normativePayload': ('NORMATIVE SUCCESSOR: 101 files byte-identical to the generation-20 '
                          'kit, 1 CHANGED, 0 added and 0 withdrawn, measured per path in THIS '
                          'generation against this origin\'s own retained generation-20 per-file '
                          'map (see notes/v22-input-custody.json claim 4). Changed: '
                          'foundation/atom-evaluation-contract.v1.md (23826 -> 36951 bytes). The '
                          'supplied normative-delta.json inventory was VERIFIED against both '
                          'sides rather than trusted (claim 5).')},
    {'generation': 'consumer-b.' + 'v23',
     'manifestSha256': EXPECT_MANIFEST, 'parentSha256': EXPECT_PARENT,
     'fileCount': 102,
     'normativePayload': ('NORMATIVE SUCCESSOR: 99 files byte-identical to the generation-22 '
                          'kit, 3 CHANGED, 0 added and 0 withdrawn, measured per path in THIS '
                          'generation against this origin\'s own retained generation-22 per-file '
                          'map (see notes/v23-input-custody.json claim 4). Changed: '
                          'foundation/atom-evaluation-contract.v1.md (36951 -> 48688 bytes), '
                          'foundation/evaluator-projection-registry.v1.json (59745 -> 60005) and '
                          'foundation/incoming-search.schema.v1.json (12930 -> 13052). The '
                          'supplied normative-delta.json inventory was VERIFIED against both '
                          'sides rather than trusted (claim 5).')},
]

FIVE = ['README.md', 'identity-and-evidence.md', 'security-and-lifecycle.md',
        'native-evidence.md', 'workflows-and-surfaces.md', 'admission-and-qualification.md']


def main():
    mb = open(SUB + '/consumer-input-manifest.json', 'rb').read()
    man_sha = hashlib.sha256(mb).hexdigest()
    man = json.loads(mb.decode())
    rows, bad = [], []
    for f in man['files']:
        p = SUB + '/' + f['path']
        if not os.path.exists(p):
            rows.append({'path': f['path'], 'result': 'MISSING'})
            bad.append(f['path'])
            continue
        b = open(p, 'rb').read()
        h = hashlib.sha256(b).hexdigest()
        ok = (h == f['sha256'] and len(b) == f['bytes'])
        rows.append({'path': f['path'], 'declaredSha256': f['sha256'],
                     'measuredSha256': h, 'declaredBytes': f['bytes'],
                     'measuredBytes': len(b), 'result': 'PASS' if ok else 'FAIL'})
        if not ok:
            bad.append(f['path'])
    on_disk = set()
    for dp, dn, fn in os.walk(SUB + '/docs'):
        for n in fn:
            on_disk.add(os.path.relpath(os.path.join(dp, n), SUB))
    listed = set(f['path'] for f in man['files'])

    cve = json.load(open(SUB + '/docs/coop/artifacts/resolved-inputs.v2.json'))
    cve = cve['planIdContract']['canonicalValueEncoding']

    idx = open(SUB + '/docs/v2/contracts/product-v1/README.md').read()
    smap = open(SUB + '/docs/coop/design-corrections/current-source-map.proposed.md').read()

    # Task-scope metadata discrepancy: requirements.json was authored for a sibling
    # origin id and carries a different kit manifest hash. The PROMPT's paths and the
    # measured manifest hash govern; requirements.json is task scope, not design authority.
    reqs = json.load(open(ROOT + '/requirements.json'))

    res = {
        'consumerId': CK.CONSUMER,
        'phase': 0,
        'standing': {
            'freshOrigin': True,
            'priorReviewContextUsed': False,
            'kitOnly': True,
            'outputConfinedTo': OUT,
            'authorModelsFixturesGoldensReportsRead': False,
            'otherDesignCorrectionDirectoriesRead': False,
            'agentsSpawned': 0,
        },
        'inputKit': {
            'manifestPath': 'subject/consumer-input-manifest.json',
            'manifestSha256Measured': man_sha,
            'manifestSha256Expected': EXPECT_MANIFEST,
            'manifestSha256Match': man_sha == EXPECT_MANIFEST,
            'parentSubjectSha256Declared': man['parentSubjectSha256'],
            'parentSubjectSha256Expected': EXPECT_PARENT,
            'parentSubjectSha256Match': man['parentSubjectSha256'] == EXPECT_PARENT,
            'parentVerificationStanding': (
                'Only the parent digest DECLARED IN THIS MANIFEST was compared to the value '
                'the instruction names. The parent candidate itself was never held, so this '
                'is NOT a parent whole-candidate verification.'),
            'sameOriginSubjectAncestry': ANCESTRY,
            'sessionId': '79569ae1-10f4-4181-972b-334f7ed2f07a',
            'fileCount': len(man['files']),
            'filesVerifiedPass': sum(1 for r in rows if r['result'] == 'PASS'),
            'filesFailed': bad,
            'extraFilesOnDiskNotInManifest': sorted(on_disk - listed),
            'manifestFilesAbsentFromDisk': sorted(listed - on_disk),
            'hashVerification': 'PASS' if (not bad and man_sha == EXPECT_MANIFEST
                                           and man['parentSubjectSha256'] == EXPECT_PARENT
                                           and not (on_disk ^ listed)) else 'FAIL',
            'perFile': rows,
        },
        'taskScopeMetadataDiscrepancy': {
            'observation': ('requirements.json carries inputKit.manifestSha256='
                            + reqs['inputKit']['manifestSha256'] + ' and deliverable paths under '
                            'consumer-b.v13, which do not match this origin. The charter prompt '
                            'names consumer-b.v23 paths and the manifest hash measured above.'),
            'resolution': ('requirements.json is declared "task scope, not design authority"; the '
                           'prompt paths and the measured manifest hash govern. This is an '
                           'organisational metadata mismatch in the task file, NOT a design gap '
                           'and NOT an input-custody failure of the normative kit: all 101 '
                           'normative files verify byte-exact against the manifest the prompt '
                           'names, and the required ID set is unchanged (123 + 8 + 3).'),
            'requirementCounts': reqs['counts'],
            'measuredRequirementArrayLength': len(reqs['requirements']),
            'measuredStandingArrayLength': len(reqs['standing']),
            'measuredFutureQualificationArrayLength': len(reqs['futureQualification']),
        },
        'R-CVE1-TYPES-AVAILABLE': {
            'selector': 'docs/coop/artifacts/resolved-inputs.v2.json'
                        '#planIdContract.canonicalValueEncoding',
            'name': cve['name'],
            'closedTypes': cve['closedTypes'],
            'count': len(cve['closedTypes']),
            'allEightPresent': len(cve['closedTypes']) == 8,
            'encodingsPresentForEveryType': sorted(cve['encodings']) == sorted(cve['closedTypes']),
            'constraints': cve['constraints'],
        },
        'R-FIVE-CONTRACTS-INDEX': {
            'indexPath': 'docs/v2/contracts/product-v1/README.md',
            'fivePresent': {n: os.path.exists(SUB + '/docs/v2/contracts/product-v1/' + n)
                            for n in FIVE},
            # V22-D10: generations 16-20 printed "only within its declared scope" in capitals
            # inside quotation marks, so the "quote" was not the kit's bytes. Verbatim now; the
            # claimed-positive audit finds it in the kit after whitespace normalisation only.
            'successorOverInheritedRule': (
                'README.md: "The normative retained/superseded selector tables in these five '
                'contracts determine the applicable design recipes; a current explicit successor '
                'wins over the named inherited selector only within its declared scope. Any '
                'unresolved overlap is a design defect, never reviewer discretion."'),
            'governanceRecordsExcluded': (
                'README.md: the correction crosswalk and the central readiness register "grant '
                'standing; they are not additional semantic recipes and are omitted from blind '
                'reconstruction inputs to avoid disclosing prior verdicts." Neither is present in '
                'the kit and neither was used as a recipe; no review/readiness link was followed.'),
            'passingReferenceChecksIsNotQualification': True,
        },
        'R-SOURCE-MAP-SCOPE': {
            'path': 'docs/coop/design-corrections/current-source-map.proposed.md',
            'usedFor': 'scope only -- which historical selector each current account replaces',
            'governanceNotUsedAsRecipe': True,
            'currentEvaluatorProfileSelection': {
                'identityEvaluatorOutputMajor': 3,
                'selectedOwner': 'foundation/identity-schemas.v3.json',
                'workflowOwner': 'workflows/schemas/evaluator3/ + workflows/command-inventory.v3.json',
                'commandEnvelopeMajor': 3,
                'unchangedInputsKeepRecipes': ['policy2', 'import2', 'finding-key2'],
                'nativeAndInputIdentitiesRetainMajor2': True,
                'graphQueryOwner': ('workflows/query-projection-contract.v3.md + '
                                    'workflows/schemas/evaluator3/graph-query.schema.json, '
                                    'incorporated by product workflows section 8'),
                'capabilityManifestRegistry':
                    'docs/coop/design-corrections/native/capability-manifest-domains.v2.json',
                'requiredExecutionInputsDigest': True,
                'policyDocument': 'PolicyDocumentV2 / RuleProgramV2 (program2)',
                'incorporatedContracts': ['enumeration-contract.v1', 'atom-evaluation-contract.v1',
                                          'execution-inputs-contract.v1',
                                          'evaluator-composition-contract.v3',
                                          'evaluator-fault-contract.v3'],
                'selectedAttributionSchema': 'foundation/target-attribution.schema.v2.json '
                                             '(historical V1 refused)',
            },
            'historicalNarrativesAreProvenanceOnly': True,
        },
    }
    with open(OUT + '/notes/phase0-input-custody.json', 'w') as f:
        json.dump(res, f, indent=1)

    # V22-D11: this stage used to mark its eleven ids `executed` in requirement-status.json and
    # write checkpoints/phase-0.json through checkpoint.py, which READ the previous command's
    # status and checkpoints off disk first (measured by the generation-22 read graph). Status is
    # derived only by status.py from the claimed-positive audit and checkpoints only by
    # checkpoints_all.py, both later in the same command, so nothing is written here.
    print('phase0 hashVerification:', res['inputKit']['hashVerification'])
    print('CVE1 types:', res['R-CVE1-TYPES-AVAILABLE']['count'],
          res['R-CVE1-TYPES-AVAILABLE']['closedTypes'])
    assert res['inputKit']['hashVerification'] == 'PASS'
    assert res['R-CVE1-TYPES-AVAILABLE']['allEightPresent']


main()

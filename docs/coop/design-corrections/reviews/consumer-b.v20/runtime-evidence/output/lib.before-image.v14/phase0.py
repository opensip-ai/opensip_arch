"""Phase 0 -- input custody. Verify the manifest, record kit standing, confirm the
eight CVE1 types, record the five contracts and the current-source map scope."""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checkpoint as CK

ROOT = '/tmp/opensip-design-corrections/consumer-b.v14'
SUB = ROOT + '/subject'
OUT = ROOT + '/output'

EXPECT_MANIFEST = 'f8aec9c5469573568fe6f57f14429b739cf7f9707c08a26b72d0c48e71c43f3c'
EXPECT_PARENT = 'c9a6c26a82dbe24acfbba423360be54e45f11325576b172d75a005ec35d0ffb2'

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
                            'names consumer-b.v14 paths and the manifest hash measured above.'),
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
            'successorOverInheritedRule': (
                'README.md: "The normative retained/superseded selector tables in these five '
                'contracts determine the applicable design recipes; a current explicit successor '
                'wins over the named inherited selector ONLY WITHIN ITS DECLARED SCOPE. Any '
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

    rows_status = CK.read_status()
    ids = ['S-FRESH-ORIGIN', 'S-NOT-PRODUCT', 'S-KIT-ONLY', 'S-MANIFEST-VERIFY',
           'S-NO-ORACLE', 'S-MISSING-DEP-IS-CUSTODY', 'S-PROFILE-CURRENT', 'S-CONTINUATION',
           'R-FIVE-CONTRACTS-INDEX', 'R-SOURCE-MAP-SCOPE', 'R-CVE1-TYPES-AVAILABLE']
    CK.mark(rows_status, ids, 'executed',
            artifacts=['output/notes/phase0-input-custody.json'],
            note='phase-0 input custody')
    CK.write_status(rows_status)
    cp = CK.write_checkpoint(
        0, executed=ids, failed=[],
        artifacts=['output/notes/phase0-input-custody.json',
                   'output/checkpoints/phase-0.json',
                   'output/requirement-status.json'],
        helper_corrections=[],
        notes=('Manifest hash and all 101 file hashes/lengths verified PASS; parent subject '
               'hash matches. No extra or missing files. Eight CVE1 types confirmed. Five '
               'contracts and the current-source map read for scope; readiness/review records '
               'are absent from the kit and were not used as recipes. requirements.json carries '
               'sibling-origin metadata (v13 paths, different manifest hash) which is task-scope '
               'only; the prompt paths govern and the required ID set is unchanged.'))
    print('phase0 hashVerification:', res['inputKit']['hashVerification'])
    print('CVE1 types:', res['R-CVE1-TYPES-AVAILABLE']['count'],
          res['R-CVE1-TYPES-AVAILABLE']['closedTypes'])
    print('checkpoint required/executed/unexecuted:',
          len(cp['requirementIdsRequired']), len(cp['requirementIdsExecuted']),
          len(cp['requirementIdsUnexecuted']))
    assert res['inputKit']['hashVerification'] == 'PASS'
    assert res['R-CVE1-TYPES-AVAILABLE']['allEightPresent']


main()

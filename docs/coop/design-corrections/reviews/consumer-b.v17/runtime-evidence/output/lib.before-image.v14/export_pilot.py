"""Export the pilot syntax-only CODE Run: object table plus ALL blob/frame bytes keyed by
raw SHA-256, plus the schema-admission log and the closure report."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_closure as CL
import run_syntax_code as RSC
import run_syntax_code_full as F

OUT = '/tmp/opensip-design-corrections/consumer-b.v14/output'


def main():
    g = F.complete(RSC.build())
    st, out = g['st'], g['out']
    c = CL.Closure(st)
    rep = c.close_run(out['runId'], 'syntax-code')

    os.makedirs(OUT + '/runs', exist_ok=True)
    doc = st.export(OUT + '/runs/syntax-code.store.json', extra={
        'consumerId': 'consumer-b.v14',
        'runLabel': 'syntax-code',
        'kind': 'completeRun',
        'requirementIds': ['R-RUN-SYNTAX-CODE', 'R-RUN-NO-COMPILER-UNIT',
                           'R-RUN-FILE-FACT-INVENTORY', 'R-RUN-CLONES-L0-AND-NORMALIZED',
                           'R-RUN-CLONES-CUSTODY'],
        'claim': {'runId': out['runId'], 'sealId': out['sealId'],
                  'evidenceId': out['evidenceId'], 'proofId': out['proofId'],
                  'planId': g['plan_id'], 'snapshotId': g['snapshot_id'],
                  'verdict': out['proof']['verdict'],
                  'evaluationState': out['proof']['evaluationState'],
                  'policyDerivationId': out['policyDerivationId']},
        'syntheticObservationStanding': (
            'Every repository byte, grammar bundle, component manifest, provider return, '
            'subject inventory and host capture in this export is a SYNTHETIC TRUSTED '
            'OBSERVATION authored by consumer-b.v14. It is an assumption about a future '
            'host. It is never native enforcement proof and qualifies no parser, compiler, '
            'normalizer, OS, crypto or SQLite behaviour.'),
        'retainedSchemaDocuments': g['b'].retained_schema_docs,
        'selectedProviderAndCapabilityContext': {
            'languageMode': 'syntax-only',
            'nativeContextDomain': 'native.context.syntax.v2',
            'nativeContextDigest': g['ctx_hex'],
            'universeDomain': 'native.semantic-universe.syntax.v2',
            'universeDigest': g['uni_hex'],
            'providerClosure': g['closures']['provider'],
            'grammarClosure': g['closures']['grammar'],
            'evaluatorClosure': g['closures']['evaluator'],
            'detectorClosure': g['closures']['detector'],
            'selectedGrammarIds': st.objects[
                'native.semantic-universe.syntax.v2#' + g['uni_hex']]['selectedGrammarIds'],
            'capabilityManifestId': g['capres']['capabilityManifestId'],
            'capabilityManifestBytesDigest': g['capres']['committedBytesSha256'],
            'outputMajors': {'finding': 3, 'proof': 3, 'evidence': 3, 'seal': 3, 'run': 3,
                             'subject': 3, 'predicateWitness': 3, 'policyDocument': 2,
                             'ruleProgram': 2},
            'nativeAndInputIdentityMajors': {'snapshot': 2, 'plan': 2, 'scope': 2, 'fact': 2,
                                             'coverage': 2, 'view': 2, 'closure': 2,
                                             'executionPlan': 2, 'findingKey': 2,
                                             'nativeContext': 'v2', 'nativeUniverse': 'v2'},
        },
        'closureReport': rep,
        'schemaAdmissionLog': [{'label': a['label'], 'document': a['document'],
                                'documentSha256': a['documentSha256'],
                                'selector': a['selector'],
                                'stockSchemaErrors': a['stockSchemaErrors'],
                                'publishedKeywordRefusals': a['publishedKeywordRefusals'],
                                'admitted': a['admitted'],
                                'digestSiteCount': len(a['digestSites'])}
                               for a in g['b'].admissions],
        'digestSitesByRecord': {a['label']: a['digestSites'] for a in g['b'].admissions
                                if a['digestSites']},
    })
    with open(OUT + '/runs/syntax-code.closure.json', 'w') as f:
        json.dump(rep, f, indent=1)
    print('exported', OUT + '/runs/syntax-code.store.json')
    print('objects', doc['objectCount'], 'blobs', doc['blobCount'],
          'bytes', doc['totalBlobBytes'])
    print('closure admitted', rep['admitted'], 'passed', rep['checksPassed'],
          'refused', rep['checksRefused'])
    assert rep['admitted']


main()

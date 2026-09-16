"""Generic exporter: python3 run.py export_run.py <module> <label> [requirementIds...]

<module> must expose build() and complete(g) (or main-equivalent) returning the graph dict.
"""
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_closure as CL

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'

mod_name, label = sys.argv[1], sys.argv[2]
req_ids = sys.argv[3].split(',') if len(sys.argv) > 3 else []
mod = importlib.import_module(mod_name)
if hasattr(mod, 'graph'):
    g = mod.graph()
else:
    base = importlib.import_module(mod.BASE) if hasattr(mod, 'BASE') else mod
    g = mod.complete(base.build())
st, out = g['st'], g['out']
c = CL.Closure(st)
rep = c.close_run(out['runId'], label)

os.makedirs(OUT + '/runs', exist_ok=True)
uni = g.get('uni_hex')
extra = {
    'consumerId': 'consumer-b.v18',
    'runLabel': label,
    'kind': 'completeRun',
    'requirementIds': req_ids,
    'claim': {'runId': out['runId'], 'sealId': out['sealId'],
              'evidenceId': out['evidenceId'], 'proofId': out['proofId'],
              'planId': g['plan_id'], 'snapshotId': g['snapshot_id'],
              'verdict': out['proof']['verdict'],
              'evaluationState': out['proof']['evaluationState'],
              'policyDerivationId': out['policyDerivationId']},
    'syntheticObservationStanding': (
        'Every repository byte, toolchain/grammar observation, component manifest, provider '
        'return, subject inventory, imported payload and host capture in this export is a '
        'SYNTHETIC TRUSTED OBSERVATION authored by consumer-b.v18. It is an assumption '
        'about a future host, never native enforcement proof, and qualifies no compiler, '
        'cargo, parser, normalizer, OS, crypto or SQLite behaviour.'),
    'retainedSchemaDocuments': g['b'].retained_schema_docs,
    'selectedProviderAndCapabilityContext': {
        'nativeContextDigest': g.get('ctx_hex'),
        'universeDigests': g.get('universe_digests') or ([uni] if uni else []),
        'closures': g.get('closures'),
        'capabilityManifestId': g['capres']['capabilityManifestId'],
        'capabilityManifestBytesDigest': g['capres']['committedBytesSha256'],
        'outputMajors': {'finding': 3, 'proof': 3, 'evidence': 3, 'seal': 3, 'run': 3,
                         'subject': 3, 'predicateWitness': 3, 'policyDocument': 2,
                         'ruleProgram': 2},
        'nativeAndInputIdentityMajors': {'snapshot': 2, 'plan': 2, 'scope': 2, 'fact': 2,
                                         'coverage': 2, 'view': 2, 'closure': 2,
                                         'import': 2, 'executionPlan': 2,
                                         'findingKey': 2, 'nativeRecords': 'v2'},
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
}
if g.get('exhibits'):
    extra['exhibits'] = g['exhibits']
doc = st.export(OUT + '/runs/%s.store.json' % label, extra=extra)
with open(OUT + '/runs/%s.closure.json' % label, 'w') as f:
    json.dump(rep, f, indent=1)
print('exported', label, 'objects', doc['objectCount'], 'blobs', doc['blobCount'],
      'bytes', doc['totalBlobBytes'])
print('closure admitted', rep['admitted'], 'passed', rep['checksPassed'],
      'n/a', rep['checksNotApplicable'], 'refused', rep['checksRefused'])
for r in rep['refusals'][:20]:
    print('  REFUSE', r['check'], '|', json.dumps(r['detail'])[:240])
sys.exit(0 if rep['admitted'] else 1)

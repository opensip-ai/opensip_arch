"""READ-ONLY diagnostic (generation 23): the premises a comparison over the TypeScript Run can
lawfully use -- rule results, findings with their fingerprint subject keys, waivers, policy gates,
scope document, the runtime import wrapper and its recomputed import2 identity. Writes nothing."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'


def main():
    st, doc = ST.Store.load(OUT + '/runs/typescript.store.json')
    run = st.objects[doc['claim']['runId']]
    seal = st.objects[run['evaluationSealId']]
    proof = st.objects[seal['proofBundleId']]
    j = lambda label: json.loads(st.get_blob(st.labels[label]).decode())
    policy = j('policy')
    print('policy rules:')
    for r in policy['rules']:
        print('  %-36s enabled=%s severity=%s gate=%s evidenceUse=%s'
              % (r['ruleId'], r['enabled'], r['severity'], r['gate'], r['evidenceUse']))
    print('gateSeverityAtLeast', policy['gateSeverityAtLeast'])
    print('waivers', json.dumps(j('waivers')))
    print('scope-document', json.dumps(j('scope-document')), 'digest', st.labels['scope-document'])
    print('verdict', proof['verdict'], 'evaluationState', proof['evaluationState'])
    print('executionDeficiencies', json.dumps(proof['executionDeficiencies'])[:600])
    print('waivedFindingIds', proof['waivedFindingIds'])
    for rr in proof['ruleResults']:
        print('  rule %-36s outcome=%-13s findings=%d deficiencies=%s enumeration=%s'
              % (rr['ruleId'], rr['outcome'], len(rr['findingIds']),
                 sorted({d['cause'] for d in rr['deficiencies']}),
                 json.dumps(rr['enumeration'])[:160]))
    for fid in proof['findingIds']:
        f = st.objects[fid]
        key = st.objects.get(f['fingerprint']) or {}
        print('  finding %s fp=%s msg=%s subjectKey=%s keys=%s'
              % (fid[:18], f['fingerprint'][:22], f.get('messageCode'),
                 json.dumps(key.get('subjectKey')), sorted(f)))
    for t, w in st.objects.items():
        if t.startswith('import2:'):
            print('import', t, 'recomputed', K.ID('import', w) == t, sorted(w))


main()

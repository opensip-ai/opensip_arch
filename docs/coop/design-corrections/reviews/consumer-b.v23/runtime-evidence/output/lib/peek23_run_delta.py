"""READ-ONLY diagnostic (generation 23): predicate values, findings and deficiency causes of every
current Run against this origin's own generation-22 predecessor export. Writes nothing."""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']


def summary(path):
    st, doc = ST.Store.load(path)
    run = st.objects[doc['claim']['runId']]
    seal = st.objects[run['evaluationSealId']]
    proof = st.objects[seal['proofBundleId']]
    vals = {}
    causes = {}
    for pp in proof['predicateProofs']:
        k = (pp['ruleId'], pp['subjectId'][:18], pp['predicateId'])
        vals[k] = pp['value']
        w = json.loads(st.get_blob(pp['witnessDigest'].split(':')[-1]).decode())
        causes[k] = sorted({d['cause'] for d in w['deficiencies']})
    findings = [t for t in st.objects if t.startswith('finding3:')]
    return {'runId': doc['claim']['runId'], 'verdict': doc['claim'].get('verdict'),
            'findings': len(findings), 'values': vals, 'causes': causes,
            'ruleResults': {r['ruleId']: r.get('value', r.get('outcome'))
                            for r in proof['ruleResults']}}


def main():
    for label in RUNS:
        now = summary(OUT + '/runs/%s.store.json' % label)
        was = summary(OUT + '/predecessors.v22/runs/%s.store.json' % label)
        print('%-13s runId %s -> %s  findings %d -> %d  verdict %s -> %s'
              % (label, was['runId'][:14], now['runId'][:14], was['findings'], now['findings'],
                 was['verdict'], now['verdict']))
        for k in sorted(set(now['values']) | set(was['values'])):
            a, b = was['values'].get(k), now['values'].get(k)
            ca, cb = was['causes'].get(k), now['causes'].get(k)
            if a != b or ca != cb:
                print('   %-40s %-14s %s: %s -> %s | causes %s -> %s'
                      % (k[0][:40], k[1], k[2], a, b, ca, cb))


main()

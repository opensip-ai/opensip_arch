"""READ-ONLY diagnostic (generation 23): the TypeScript Run's graph-projectable premises -- binary
relation facts with their payload source/target ids and retained TargetAttributionV2 sidecars,
the subject-inventory rows (kind, nativeSubjectId, path) with their program binding, the views and
their scopes, and the proof executionDeficiencies. Writes nothing."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
PROJECTABLE = {('calls', 'resolved-callee'), ('references', 'resolved-binding'),
               ('imports', 'resolved-target'), ('control-flow', 'syntactic'),
               ('reachability', 'from-resolved-calls')}


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else 'typescript'
    st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
    run = st.objects[doc['claim']['runId']]
    proof = st.objects[st.objects[run['evaluationSealId']]['proofBundleId']]
    j = lambda d: json.loads(st.get_blob(d).decode())
    ei = j(st.labels['execution-inputs'])
    print('selectedRefs domains', sorted({r['domain'] for r in ei['selectedRefs']}))
    print('evaluationInputRefs domains', sorted({r['domain'] for r in proof['evaluationInputRefs']}))
    for r in proof['evaluationInputRefs']:
        if r['domain'] == 'subject-inventory':
            inv = j(r['digest'])
            print('inventory', r['digest'][:12], {k: inv[k] for k in inv if k not in ('rows',)})
            for row in inv['rows'][:12]:
                print('    ', row)
    for r in proof['evaluationInputRefs']:
        if r['domain'] == 'target-attribution':
            print('attribution', json.dumps(j(r['digest']))[:400])
    for t, f in sorted(st.objects.items()):
        if t.startswith('fact2:') and (f['relation'], f['resolution']) in PROJECTABLE:
            print('fact', t[:18], f['relation'], f['resolution'], f['sourceUniverse'][:8],
                  f['targetUniverse'][:8] if f['targetUniverse'] else None,
                  json.dumps(j(f['payloadDigest']))[:220])
    for t, v in sorted(st.objects.items()):
        if t.startswith('view2:'):
            print('view', t[:18], sorted(v), [(st.objects[s]['relation'], st.objects[s]['resolution'])
                                               for s in v.get('scopeIds', [])][:8])
    print('executionDeficiencies', json.dumps(proof['executionDeficiencies']))
    print('enumeration plan cells', json.dumps(j(st.labels['enumeration-plan'])['cells'])[:600])


main()

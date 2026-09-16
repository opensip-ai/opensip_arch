"""Read-only diagnostic (generation 22): recompose each exported Run's proof from its RETAINED
inputs with the current evaluator and list every predicate whose value, witness deficiencies,
coverageIds or scopeIds differ from the retained (generation-20) claim. Writes nothing.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_compose as CO
import opensip_closure as CL
import opensip_store as ST
import opensip_replay as RP

OUT = '/tmp/opensip-design-corrections/consumer-b.v22/output'
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']


def s(x):
    return x.split(':', 1)[-1][:8] if isinstance(x, str) else x


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for label in RUNS:
        if only and label != only:
            continue
        st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        cl = CL.Closure(st)
        cl.close_run(doc['claim']['runId'], 'peek22r:' + label)
        run = cl.resolved[doc['claim']['runId']]
        inp, emit_plan, xi, proof, seal, ev, _ = RP.reconstruct_inputs(st, cl, run)
        out = CO.compose(inp, st, emit_plan, xi, run['snapshotId'])
        new = {(p['ruleId'], p['subjectId'], p['predicateId']): p
               for p in out['proof']['predicateProofs']}
        old = {(p['ruleId'], p['subjectId'], p['predicateId']): p
               for p in proof['predicateProofs']}
        print('=' * 90)
        print('RUN %-13s verdict retained=%s recomputed=%s findings %d -> %d  execDefs %d -> %d'
              % (label, proof['verdict'], out['proof']['verdict'], len(proof['findingIds']),
                 len(out['proof']['findingIds']), len(proof['executionDeficiencies']),
                 len(out['proof']['executionDeficiencies'])))
        for rr_old, rr_new in zip(proof['ruleResults'], out['proof']['ruleResults']):
            if K.C(rr_old) != K.C(rr_new):
                print('  ruleResult %s outcome %s -> %s findings %d -> %d defs %d -> %d'
                      % (rr_old['ruleId'], rr_old['outcome'], rr_new['outcome'],
                         len(rr_old['findingIds']), len(rr_new['findingIds']),
                         len(rr_old['deficiencies']), len(rr_new['deficiencies'])))
        changed = 0
        for k in sorted(set(old) | set(new)):
            a, b = old.get(k), new.get(k)
            if a and b and K.C(a) == K.C(b):
                continue
            changed += 1
            wa = json.loads(st.get_blob(a['witnessDigest']).decode()) if a and st.get_blob(
                a['witnessDigest']) else None
            wb = out['witnesses'].get(b['witnessDigest']) if b else None
            print('  %s %s %s' % (k[0], s(k[1]), k[2]))
            print('     value %s -> %s   scopeIds %s -> %s'
                  % (a and a['value'], b and b['value'], a and [s(x) for x in a['scopeIds']],
                     b and [s(x) for x in b['scopeIds']]))
            if wa is not None or wb is not None:
                print('     coverageIds %s -> %s'
                      % (wa and [s(x) for x in wa['coverageIds']],
                         wb and [s(x) for x in wb['coverageIds']]))
                fmt = lambda w: sorted(((d['source'], d['cause'], s(d['universe']),
                                         d['nativeCause'],
                                         'EI' if len(d['inputRefs']) > 1 else
                                         [r['domain'] for r in d['inputRefs']])
                                        for d in w['deficiencies']), key=repr) if w else None
                print('     defs  %s' % fmt(wa))
                print('       ->  %s' % fmt(wb))
                if wa and wb and wa['matchingImportRows'] != wb['matchingImportRows']:
                    print('     matchingImportRows %s -> %s'
                          % (wa['matchingImportRows'], wb['matchingImportRows']))
        print('  predicate proofs changed: %d of %d' % (changed, len(new)))


main()

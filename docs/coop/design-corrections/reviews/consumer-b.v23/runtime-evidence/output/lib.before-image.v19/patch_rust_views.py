"""Thread the per-universe views through the Rust completer: receipts, selectedRefs, cell
outcomes, the evaluator input set and the retained-output pass all take the split views."""
import os

LIB = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(LIB, 'run_rust_full.py')
s = open(p, encoding='utf-8').read()

PAIRS = [
    # stage output refs: every view plus every Coverage
    ("""    stage_out = K.cset([{'domain': 'view', 'digest': st.suffix(view_id)}]
                       + [{'domain': 'coverage', 'digest': st.suffix(c)}
                          for c in g['view_parts']['coverages']])""",
     """    stage_out = K.cset([{'domain': 'view', 'digest': st.suffix(v)}
                        for v in views_by_uni.values()]
                       + [{'domain': 'coverage', 'digest': st.suffix(c)}
                          for c in g['view_parts']['coverages']])"""),
    # each binding's viewDigests name ONLY its own universe's view
    ("""                'inventoryDigests': invs, 'viewDigests': [st.suffix(view_id)],
                'candidateResultDigest': None})""",
     """                'inventoryDigests': invs,
                'viewDigests': [st.suffix(views_by_uni[uni])],
                'candidateResultDigest': None})"""),
    # the evaluator sees every view
    ("""                   {view_id: st.objects[view_id]}, g['facts'], g['scopes'], g['coverages'],""",
     """                   {v: st.objects[v] for v in views_by_uni.values()},
                   g['facts'], g['scopes'], g['coverages'],"""),
    # cov_by is keyed per universe already; keep
    ("""                  inventories=inventories, view_id=view_id, exec_inputs=exec_inputs,""",
     """                  inventories=inventories, view_id=view_id,
                  views_by_universe=views_by_uni, exec_inputs=exec_inputs,"""),
]
applied, missed = 0, []
for a, b in PAIRS:
    if a in s:
        s = s.replace(a, b)
        applied += 1
    else:
        missed.append(a.strip().split('\n')[0][:70])
open(p, 'w', encoding='utf-8').write(s)
print('run_rust_full.py %d/%d missed=%s' % (applied, len(PAIRS), missed))

"""Read-only diagnostic (generation 22): the inputs the atom law reads, per atom x subject, beside
the RETAINED predicate value and witness of each exported Run. Writes nothing; stdout only.

Used to plan the reconciliation with the atom-evaluation contract section 4 successor text. It
does not decide anything: the independent instrument (indep_atom_law.py) does that from clauses.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_eval as E
import opensip_compose as CO
import opensip_closure as CL
import opensip_store as ST
import opensip_replay as RP

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']


def short(x):
    return x.split(':', 1)[-1][:8] if isinstance(x, str) else x


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for label in RUNS:
        if only and label != only:
            continue
        st, doc = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        cl = CL.Closure(st)
        rep = cl.close_run(doc['claim']['runId'], 'peek22:' + label)
        run = cl.resolved[doc['claim']['runId']]
        inp, emit_plan, xi, proof, seal, ev, _ = RP.reconstruct_inputs(st, cl, run)
        scope_doc = CO.scope_document_parameter(inp, inp.analysis_spec, st)
        pp_by = {(p['ruleId'], p['subjectId'], p['predicateId']): p
                 for p in proof['predicateProofs']}
        print('=' * 100)
        print('RUN %s admitted=%s verdict=%s' % (label, rep['admitted'], proof['verdict']))
        cells = inp.enumeration_plan['cells']
        for ci, c in enumerate(cells):
            print('  cell %d cap=%-16s mode=%-18s required=%s bindings=%s'
                  % (ci, c['capabilityId'], c['languageMode'], c.get('required'),
                     [(b.get('universe') and short(b['universe']),
                       (b.get('enumerator') or {}).get('status')) for b in c['programBindings']]))
        for hx, (dom, _r) in sorted(inp.universes.items()):
            print('  universe %s -> %s' % (hx[:8], dom))
        for r in inp.policy['rules']:
            if not r['enabled']:
                print('  RULE %s disabled' % r['ruleId'])
                continue
            sel, unres, inv_refs, inc_refs, defs_, state = E.enumerate_subjects(inp, r, scope_doc)
            print('  RULE %s enum=%s selected=%d' % (r['ruleId'], state, len(sel)))
            for addr, node in E.address_nodes(r['emitWhen']):
                if node['op'] in ('and', 'or', 'not'):
                    continue
                rel, rung = node['relation'], node['minResolution']
                native = rel not in E.evidence_registry()['relations']
                print('    ATOM %s op=%s %s@%s native=%s filters=%s'
                      % (addr, node['op'], rel, rung, native, node.get('filters')))
                if native:
                    cap = inp.capability_for_relation(rel)
                    owed = [(ci, bi, b.get('universe') and short(b['universe']), c['languageMode'])
                            for ci, c in enumerate(cells) if c['capabilityId'] == cap
                            for bi, b in enumerate(c['programBindings'])]
                    print('      capability=%s owedBindings=%s' % (cap, owed))
                for sid, srec, row, uni, inv_ref in sel:
                    p = pp_by.get((r['ruleId'], sid, addr))
                    wit = None
                    if p:
                        wb = st.get_blob(p['witnessDigest'])
                        wit = json.loads(wb.decode()) if wb else None
                    line = '      subj %-40s U=%s value=%s' % (
                        srec['nativeSubjectId'][:40], short(srec['universe']),
                        p and p['value'])
                    if native:
                        U = srec['universe']
                        containing = sorted(
                            s for s, sr in inp.scopes.items()
                            if sr['relation'] == rel and sr['resolution'] == rung
                            and sr['sourceUniverse'] == U
                            and srec['nativeSubjectId'] in sr['subjects'])
                        paired = {s: sorted(c for c, cr in inp.coverages.items()
                                            if cr['scopeId'] == s) for s in containing}
                        line += ' scopes=%s' % {short(s): [short(c) for c in v]
                                                for s, v in paired.items()}
                        for s, cs in paired.items():
                            for c in cs:
                                e = inp.coverage_payloads[c]['entry']
                                k = inp.coverage_payloads[c]['key']
                                line += '\n        cov %s key=%s@%s S=%s T=%s coverage=%s def=%s nc=%s rc=%s' % (
                                    short(c), k['relation'], k['resolution'],
                                    short(k['sourceUniverse']), short(k.get('targetUniverse')),
                                    e['coverage'], e['deficiency'], e['nativeCause'],
                                    e['resolutionCompleteness']['state'])
                    if wit:
                        line += '\n        WITNESS cov=%s facts=%d uncertainRows=%s rows=%s defs=%s scopeIds=%s' % (
                            [short(c) for c in wit['coverageIds']], len(wit['matchingFactIds']),
                            wit['uncertainImportRows'], wit['matchingImportRows'],
                            [(d['source'], d['cause'], short(d['universe']), d['nativeCause'])
                             for d in wit['deficiencies']],
                            [short(s) for s in p['scopeIds']])
                    print(line)
        if 'clones' in {n['relation'] for r in inp.policy['rules']
                        for _, n in E.address_nodes(r['emitWhen']) if 'relation' in n}:
            decl = sorted(c for c, cr in inp.coverages.items()
                          if inp.coverage_payloads[c]['key']['relation'] == 'declares')
            print('  declares Coverage (clones DEPENDS_ON declares@syntactic):')
            for c in decl:
                k = inp.coverage_payloads[c]['key']
                e = inp.coverage_payloads[c]['entry']
                print('    %s S=%s T=%s res=%s coverage=%s def=%s nc=%s conf=%s' % (
                    short(c), short(k['sourceUniverse']), short(k.get('targetUniverse')),
                    k['resolution'], e['coverage'], e['deficiency'], e['nativeCause'],
                    e['confidenceMillionths']))


main()

"""Independent execution-inputs discrimination: source40 versus source41 versus source42, each tree's OWN owner modules in
its own process (verified disposable copies work/base40, work/base41, work/source42-pkg).

Worlds are reviewer-minted on the maintained owner fixtures (file fixture with the full-run none-file atom; the TypeScript
semantic fixture with a declares atom, whose symbol subjects are SubjectIdV1). New subject-scopes, native-owner-admitted
Coverage and views are minted into the graph's own store; views declared returned are added to the graph's view census and
evaluation refs (refs-only and census-only variants are separate). Admission columns: that tree's admit_execution_inputs over
that tree's shared builder manifest, optionally host-edited (store pointers recomputed by promised_pointers). Closed-run columns:
the same manifest (hashed into the graph exactly as attach_host_capture does when edited) through seed seal -> open_run_closure
-> derive -> seal -> replay -> close_run of that tree. Expected values are this reviewer's reading of each tree's contract.
usage: probe_view_attribution_x.py                     (parent: runs the three children, writes the receipt)
       probe_view_attribution_x.py --child ROOT LABEL OUT"""
import contextlib, copy, importlib.util, io, json, subprocess, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
TREES = [('source40', RT / 'work/base40'), ('source41', RT / 'work/base41'), ('source42', RT / 'work/source42-pkg')]
PY = '/tmp/opensip-architecture-review-env/bin/python'
OUT = RT / 'receipts/probes/view-attribution-x.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def child(root, label, outfile):
    K = load('vax_checker_' + label, Path(root) / 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py')
    M, F, S, R, ID = K.M, K.F, K.S, K.R, K.IDENTITY
    C = M.C
    NH = F.fixture_helpers()
    cov_schema = NH.N.schema_document_digest(NH.N.NATIVE_SCHEMA_DOC)
    res = {}

    def cset(xs):
        return M.canon_str_list(list(xs))

    class World:
        def __init__(self, graph):
            self.g, self.o, self.b = graph, graph['objects'], graph['blobs']
            first = self.o[graph['viewIds'][0]][1]
            self.provider = first['producerClosure']
            self.rel_schema = next(d for d in first['schemaDigests'] if d != cov_schema)
            self.paths = [r['path'] for r in graph['snapshot']['sourceInventory']]
            self.snapshot = graph['inputs']['plan']['snapshotId']
            self.plan_id = graph['inputs']['planId']

        def scope(self, rel, rung, uni, subjects=(), target=None):
            return K._mint(self.o, 'subject-scope', {'snapshotId': self.snapshot, 'sourceUniverse': uni, 'targetUniverse': target or uni,
                                                    'relation': rel, 'resolution': rung, 'enumeratorClosure': self.provider, 'subjects': cset(subjects)})

        def coverage(self, sid, uni):
            payload = NH.coverage_result(self.o[sid][1], uni, True, self.b, self.paths)
            adm = NH.N.admit_coverage_result_v3(payload, self.o[sid][1], [], cov_schema)
            if adm.get('result') != 'ADMIT':
                raise RuntimeError('probe coverage not admitted: ' + str(adm)[:300])
            return K._mint(self.o, 'coverage', {'scopeId': sid, 'payloadSchemaDigest': cov_schema, 'payloadDigest': K._blob(self.b, payload)})

        def view(self, scopes, facts=(), covs=(), producer=None, plan_id=None):
            return K._mint(self.o, 'view', {'planId': plan_id or self.plan_id, 'scopeIds': cset(scopes), 'facts': cset(facts),
                                            'coverageIds': cset(covs), 'producerClosure': producer or self.provider,
                                            'schemaDigests': cset([self.rel_schema, cov_schema])})

        def single(self, rel, uni):
            return next(k for k in self.g['viewIds']
                        if [(self.o[s][1]['relation'], self.o[s][1]['sourceUniverse']) for s in self.o[k][1]['scopeIds']] == [(rel, uni)])

        def universes(self):
            out = {}
            for cell in self.g['enumerationPlan']['cells']:
                for b in cell['programBindings']:
                    out.setdefault(cell['capabilityId'], []).append(b['universe'])
            return out

        def apply(self, retire=(), add=(), refs_only=()):
            g, retire = self.g, set(retire)
            g['viewIds'] = cset([v for v in g['viewIds'] if v not in retire] + list(add))
            refs = [r for r in g['inputs']['evaluationInputRefs'] if not (r['domain'] == 'view' and 'view2:' + r['digest'] in retire)]
            g['inputs']['evaluationInputRefs'] = K.canon_refs(refs + [{'domain': 'view', 'digest': K.hx(a)} for a in list(add) + list(refs_only)])
            kept = [self.o[v][1] for v in g['viewIds']]
            g['coverageIds'] = cset([c for v in kept for c in v['coverageIds']])
            g['scopeIds'] = cset([s for v in kept for s in v['scopeIds']])
            g['inputs']['coverageCount'] = len(g['coverageIds'])
            if g.get('viewId') in retire:
                g['viewId'] = list(add)[0]

    def run_file(graph):
        return K.full_run(graph)

    def run_sem(graph):
        seed, objects, blobs, _ = S.seed_seal(graph)
        _, owner = ID.open_run_closure(seed, objects, blobs)
        i = graph['inputs']
        out = R.derive(i['planId'], i['executionPlanId'], i['evaluatorClosure'], i['evaluationInputRefs'], objects, blobs, owner)
        run, objects, blobs = S.seal_derived(graph, out, objects, blobs)
        result = R.replay(run, objects, blobs)
        closed = ID.close_run(run, objects, blobs)
        if closed != result['runId']:
            raise RuntimeError('close_run runId mismatch')
        return result, out['proof']

    def case(name, world, runner, marks=None, edit=None, closed=True):
        graph = world.g
        rec = {'marks': {k: K.hx(v) for k, v in (marks or {}).items()}}
        ei = None
        try:
            kw = K.manifest_from_owner(copy.deepcopy(graph))
            ei = kw['execution_inputs']
            if edit is not None:
                edit(ei)
                kw['store_pointers'] = M.promised_pointers(ei, kw['plan'], kw['execution_plan'], kw['enumeration_plan'],
                                                           objects=kw['objects'], blobs=kw['blobs'])['store_pointers']
            adm = K.admit(kw)
            rec['admission'] = {'result': adm.get('result'), 'refusals': adm.get('refusals')}
            rec['executionInputsDigest'] = M.raw_digest(ei)
            rows = {r['capabilityId'] + '#' + str(r['programOrdinal']) + '@' + str(r['universe'])[:8]: list(r['viewDigests']) for r in ei['cellOutcomes']}
            captured = {x['digest'] for rc in ei['hostCapture']['stageReceipts'] if rc['state'] == 'complete' for x in rc['outputRefs'] if x['domain'] == 'view'}
            selected = {x['digest'] for x in ei['selectedRefs'] if x['domain'] == 'view'}
            rec['rowViewCounts'] = {k: len(v) for k, v in rows.items()}
            rec['marksOnRows'] = {k: sorted(rk for rk, vs in rows.items() if h in vs) for k, h in rec['marks'].items()}
            rec['marksCaptured'] = {k: h in captured for k, h in rec['marks'].items()}
            rec['marksSelected'] = {k: h in selected for k, h in rec['marks'].items()}
            rec['capturedCount'], rec['selectedViewCount'] = len(captured), len(selected)
        except Exception as exc:  # noqa: BLE001
            rec['admissionError'] = type(exc).__name__ + ':' + str(exc)[:600]
        if closed and ei is not None:
            try:
                rg = copy.deepcopy(graph)
                if edit is not None:
                    d = M.raw_digest(ei)
                    rg['blobs'][d] = C.canonical(ei)
                    rg['inputs']['executionInputsDigest'] = d
                    rg['inputs']['evaluationInputRefs'] = K.canon_refs(list(ei['selectedRefs']) + [{'domain': 'execution-inputs', 'digest': d}])
                    rg['executionInputs'] = ei
                    rg['executionInputsDigest'] = d
                result, proof = runner(rg)
                rec['fullRun'] = {'closed': True, 'verdict': result['verdict'], 'runId': result['runId'],
                                  'sameManifest': proof['executionInputsDigest'] == rec.get('executionInputsDigest')}
            except Exception as exc:  # noqa: BLE001
                rec['fullRun'] = {'closed': False, 'refused': type(exc).__name__ + ':' + str(exc)[:600]}
        res[name] = rec

    def capture(world, vids):
        def edit(ei):
            add = [{'domain': 'view', 'digest': K.hx(v)} for v in vids]
            for rc in ei['hostCapture']['stageReceipts']:
                if 'view' in rc['outputDomains']:
                    rc['outputRefs'] = K.canon_refs(rc['outputRefs'] + add)
            covs = [{'domain': 'coverage', 'digest': K.hx(c)} for v in vids for c in world.o[v][1]['coverageIds']]
            ei['selectedRefs'] = K.canon_refs(ei['selectedRefs'] + add + covs)
        return edit

    def drop_from_receipts(hexv):
        def edit(ei):
            for rc in ei['hostCapture']['stageReceipts']:
                rc['outputRefs'] = [x for x in rc['outputRefs'] if x['digest'] != hexv]
        return edit

    def drop_from_selected(hexv):
        def edit(ei):
            ei['selectedRefs'] = [x for x in ei['selectedRefs'] if not (x['domain'] == 'view' and x['digest'] == hexv)]
        return edit

    def rows_edit(pred, fn):
        def edit(ei):
            for r in ei['cellOutcomes']:
                if pred(r):
                    r['viewDigests'] = M.canon_str_list(fn(list(r['viewDigests'])))
        return edit

    def chain(*edits):
        def edit(ei):
            for e in edits:
                e(ei)
        return edit

    def guard(name, fn):
        try:
            fn()
        except Exception:  # noqa: BLE001
            res[name] = {'worldError': traceback.format_exc()[-1500:]}

    UM = {'atom_override': K.NONE_ATOM, 'unsupported_cell': 'required', 'multiple_universes': True}

    def fw(**kw):
        return World(F.build_file_inputs(**kw))

    def us(w):
        u = w.universes()
        u0 = u['references'][0]
        return u0, next(x for x in u['inventory'] if x != u0)

    def fw0():
        w = fw(**UM)
        u0, _ = us(w)
        case('FW0-unsupported-control', w, run_file, marks={'refsView': w.single('references', u0)})
        census_w = fw(**UM)
        cu0, cu1 = us(census_w)
        s = census_w.scope('references', 'resolved-binding', cu1)
        census = census_w.view([s], (), [census_w.coverage(s, cu1)])
        case('FW6-census-only-view-not-captured', census_w, run_file, marks={'census': census}, closed=False)
        case('FW8-reminted-receipt-omits-selected-attributed-view', w, run_file, marks={'refsView': w.single('references', u0)},
             edit=drop_from_receipts(K.hx(w.single('references', u0))))
        case('FW9-receipt-view-not-on-selectedRefs', w, run_file, marks={'refsView': w.single('references', u0)},
             edit=drop_from_selected(K.hx(w.single('references', u0))))
    guard('FW0', fw0)

    def fw_extra_scope(name, rel, rung, foreign, with_cov, target_foreign=False):
        def go():
            w = fw(**UM)
            u0, u1 = us(w)
            r = w.single('references', u0)
            rv = w.o[r][1]
            uni = u1 if foreign else u0
            extra = w.scope(rel, rung, uni, target=u1 if target_foreign else None)
            covs = [w.coverage(extra, uni)] if with_cov else []
            nv = w.view(rv['scopeIds'] + [extra], rv['facts'], rv['coverageIds'] + covs)
            w.apply(retire=[r], add=[nv])
            case(name, w, run_file, marks={'view': nv})
        guard(name, go)

    fw_extra_scope('FW1-unsupported-row-view-names-coverage-less-foreign-scope', 'declares', 'syntactic', True, False)
    fw_extra_scope('FW1c-unsupported-row-view-names-coverage-less-same-universe-scope', 'declares', 'syntactic', False, False)
    fw_extra_scope('FW2-unsupported-row-view-carries-foreign-universe-coverage', 'references', 'resolved-binding', True, True)
    fw_extra_scope('FW13-attributed-view-names-same-source-cross-target-scope', 'references', 'resolved-binding', False, False, target_foreign=True)

    def fw4():
        w = fw(**UM)
        u0, u1 = us(w)
        nv = w.view([w.scope('declares', 'syntactic', u0), w.scope('references', 'resolved-binding', u1)])
        w.apply(add=[nv])
        case('FW4-split-scope-view-universe-and-relation-on-different-scopes', w, run_file, marks={'split': nv})
    guard('FW4', fw4)

    def fw5():
        w = fw(**UM)
        u0, u1 = us(w)
        s = w.scope('references', 'resolved-binding', u1)
        nv = w.view([s], (), [w.coverage(s, u1)])
        w.apply(add=[nv])
        case('FW5-returned-view-no-row-owns-builder', w, run_file, marks={'unowned': nv})
        case('FW5h-returned-view-no-row-owns-explicit-capture', w, run_file, marks={'unowned': nv}, edit=capture(w, [nv]))
    guard('FW5', fw5)

    def fw7():
        w = fw(**UM)
        u0, u1 = us(w)
        s = w.scope('references', 'resolved-binding', u1)
        nv = w.view([s], (), [w.coverage(s, u1)])
        w.apply(refs_only=[nv])
        case('FW7-refs-only-returned-view-evidence-omits-it', w, run_file, marks={'refsOnly': nv})
    guard('FW7', fw7)

    def fw10():
        w = fw(**UM)
        u0, u1 = us(w)
        s = w.scope('references', 'resolved-binding', u1)
        nv = w.view([s], (), [w.coverage(s, u1)], plan_id='plan2:' + '9' * 64)
        w.apply(add=[nv])
        case('FW10-captured-unattributed-view-with-foreign-planId', w, run_file, marks={'foreignPlan': nv}, edit=capture(w, [nv]))
    guard('FW10', fw10)

    def fw11():
        w = fw(**UM)
        u0, u1 = us(w)
        s = w.scope('references', 'resolved-binding', u1)
        nv = w.view([s], (), [w.coverage(s, u1)], producer=w.g['inputs']['evaluatorClosure'])
        w.apply(add=[nv])
        case('FW11-captured-unattributed-view-whose-producer-is-not-the-receipt-producer', w, run_file, marks={'foreignProducer': nv},
             edit=capture(w, [nv]))
    guard('FW11', fw11)

    def fw12():
        w = fw(atom_override=K.NONE_ATOM, optional_unselected_cell=True)
        some = K.hx(w.g['viewIds'][0])
        case('FW12-unselected-null-universe-row-names-a-view', w, run_file,
             edit=rows_edit(lambda r: r['enumeratorStatus'] == 'unselected', lambda vs: vs + [some]))
    guard('FW12', fw12)

    DECL = {'op': 'exists', 'relation': 'declares', 'minResolution': 'syntactic', 'filters': []}

    def sw():
        return World(S.build_ts_semantic_graph(atom=DECL))

    def sem():
        w = sw()
        case('SW0-semantic-declares-control', w, run_sem)
        w1 = sw()
        u1 = w1.g['u1']
        f, d = w1.single('file', u1), w1.single('declares', u1)
        fv, dv = w1.o[f][1], w1.o[d][1]
        shared = w1.view(fv['scopeIds'] + dv['scopeIds'], fv['facts'] + dv['facts'], fv['coverageIds'] + dv['coverageIds'])
        w1.apply(retire=[f, d], add=[shared])
        case('SW1-two-cells-one-program-U-shared-view', w1, run_sem, marks={'shared': shared})
        case('SW2-syntax-row-omits-shared-view', w1, run_sem, marks={'shared': shared},
             edit=rows_edit(lambda r: r['capabilityId'] == 'syntax', lambda vs: [v for v in vs if v != K.hx(shared)]))
        case('SW5-reminted-receipt-omits-shared-view', w1, run_sem, marks={'shared': shared}, edit=drop_from_receipts(K.hx(shared)))
        w3 = sw()
        u1 = w3.g['u1']
        f, d = w3.single('file', u1), w3.single('declares', u1)
        fv, dv = w3.o[f][1], w3.o[d][1]
        shared3 = w3.view(fv['scopeIds'] + dv['scopeIds'], fv['facts'] + dv['facts'], fv['coverageIds'] + dv['coverageIds'])
        s = w3.scope('references', 'resolved-binding', u1, [w3.g['foo']])
        neither = w3.view([s], (), [w3.coverage(s, u1)])
        w3.apply(retire=[f, d], add=[shared3, neither])
        case('SW3-shared-view-plus-view-matching-neither-cell-builder', w3, run_sem, marks={'shared': shared3, 'neither': neither})
        case('SW3h-shared-view-plus-neither-view-explicit-capture', w3, run_sem, marks={'shared': shared3, 'neither': neither},
             edit=capture(w3, [neither]))
        case('SW4-inventory-row-names-neither-view', w3, run_sem, marks={'shared': shared3, 'neither': neither},
             edit=chain(capture(w3, [neither]), rows_edit(lambda r: r['capabilityId'] == 'inventory', lambda vs: vs + [K.hx(neither)])))
    guard('SW', sem)
    Path(outfile).write_text(json.dumps(res, indent=1, default=str))


# ---------------------------------------------------------------------------------------------------------- parent
def adm(rec):
    return (rec.get('admission') or {}).get('result')


def refused(rec, key):
    return key in ((rec.get('admission') or {}).get('refusals') or [])


def closed(rec):
    return (rec.get('fullRun') or {}).get('closed') is True and (rec.get('fullRun') or {}).get('sameManifest') is True


def run_refused(rec, key):
    fr = rec.get('fullRun') or {}
    return fr.get('closed') is False and key in str(fr.get('refused'))


def parent():
    sides, runs = {}, {}
    for label, root in TREES:
        out = RT / ('receipts/probes/view-attribution-x.side-' + label + '.json')
        p = subprocess.run([PY, '-I', '-B', __file__, '--child', str(root), label, str(out)], capture_output=True, text=True, timeout=5400)
        runs[label] = {'exitCode': p.returncode, 'stderrTail': p.stderr[-3000:]}
        sides[label] = json.loads(out.read_text()) if out.exists() else {}
    rows = []

    def row(case, ok, observed, expected=None, kind=None):
        r = {'case': case, 'ok': bool(ok), 'observed': observed}
        if expected is not None:
            r['expected'] = expected
        if kind:
            r['kind'] = kind
        rows.append(r)

    def get(label, name):
        return sides.get(label, {}).get(name, {})

    def obs(name, keys=('admission', 'fullRun', 'marksOnRows', 'marksCaptured', 'marksSelected', 'executionInputsDigest', 'admissionError', 'worldError')):
        return {lab: {k: get(lab, name).get(k) for k in keys if k in get(lab, name)} for lab, _ in TREES}

    for lab, _ in TREES:
        row('child-' + lab + '-completed', runs[lab]['exitCode'] == 0 and sides[lab], runs[lab])
    n = 'FW0-unsupported-control'
    row(n + ' closes on every tree and names the references view on the references row only',
        all(adm(get(l, n)) == 'ADMIT' and closed(get(l, n)) and get(l, n).get('marksOnRows', {}).get('refsView', [''])[0].startswith('references#0')
            and len(get(l, n).get('marksOnRows', {}).get('refsView', [])) == 1 for l, _ in TREES), obs(n))
    for n in ('FW1-unsupported-row-view-names-coverage-less-foreign-scope', 'FW2-unsupported-row-view-carries-foreign-universe-coverage'):
        a, b, c = get('source40', n), get('source41', n), get('source42', n)
        row(n + ': source40 admits and closes; source41 and source42 refuse COVERAGE_DERIVE at admission and in the Run',
            adm(a) == 'ADMIT' and closed(a) and all(refused(x, 'EXECUTION_INPUTS_COVERAGE_DERIVE') and run_refused(x, 'EXECUTION_INPUTS_COVERAGE_DERIVE') for x in (b, c)),
            obs(n))
    for n in ('FW1c-unsupported-row-view-names-coverage-less-same-universe-scope', 'FW13-attributed-view-names-same-source-cross-target-scope'):
        row(n + ': admits and closes on every tree', all(adm(get(l, n)) == 'ADMIT' and closed(get(l, n)) for l, _ in TREES), obs(n))
    n = 'FW4-split-scope-view-universe-and-relation-on-different-scopes'
    a, b, c = get('source40', n), get('source41', n), get('source42', n)
    row(n + ': source40 attributes it to the references row and closes; source41 attributes nothing and its builder drops it (EVALUATION_VIEW_ROOTS); source42 captures it on no row and closes under a different ExecutionInputsV1 digest',
        adm(a) == 'ADMIT' and closed(a) and any(k.startswith('references#0') for k in a.get('marksOnRows', {}).get('split', []))
        and not b.get('marksOnRows', {}).get('split') and b.get('marksCaptured', {}).get('split') is False and run_refused(b, 'EVALUATION_VIEW_ROOTS')
        and not c.get('marksOnRows', {}).get('split') and c.get('marksCaptured', {}).get('split') is True and closed(c)
        and a.get('executionInputsDigest') != c.get('executionInputsDigest'), obs(n))
    n = 'FW5-returned-view-no-row-owns-builder'
    a, b, c = get('source40', n), get('source41', n), get('source42', n)
    row(n + ': source40 and source41 builders drop it and the Run refuses EVALUATION_VIEW_ROOTS; source42 captures and selects it on no row and closes',
        all(x.get('marksCaptured', {}).get('unowned') is False and run_refused(x, 'EVALUATION_VIEW_ROOTS') for x in (a, b))
        and c.get('marksCaptured', {}).get('unowned') is True and c.get('marksSelected', {}).get('unowned') is True
        and not c.get('marksOnRows', {}).get('unowned') and closed(c), obs(n))
    n = 'FW5h-returned-view-no-row-owns-explicit-capture'
    row(n + ': explicit capture admits and closes on every tree (lawful on all); on source42 it equals the builder manifest',
        all(adm(get(l, n)) == 'ADMIT' and closed(get(l, n)) and not get(l, n).get('marksOnRows', {}).get('unowned') for l, _ in TREES)
        and get('source42', n).get('executionInputsDigest') == get('source42', 'FW5-returned-view-no-row-owns-builder').get('executionInputsDigest'),
        obs(n))
    n = 'FW6-census-only-view-not-captured'
    row(n + ': never captured and the digest equals the unmutated control on every tree',
        all(get(l, n).get('marksCaptured', {}).get('census') is False
            and get(l, n).get('executionInputsDigest') == get(l, 'FW0-unsupported-control').get('executionInputsDigest') for l, _ in TREES), obs(n))
    n = 'FW7-refs-only-returned-view-evidence-omits-it'
    a, b, c = get('source40', n), get('source41', n), get('source42', n)
    row(n + ': source42 captures the refs-only view and the Run whose evidence omits it refuses EVALUATION_VIEW_ROOTS; source40/41 drop it and close',
        c.get('marksCaptured', {}).get('refsOnly') is True and run_refused(c, 'EVALUATION_VIEW_ROOTS')
        and all(x.get('marksCaptured', {}).get('refsOnly') is False and closed(x) for x in (a, b)), obs(n))
    n = 'FW8-reminted-receipt-omits-selected-attributed-view'
    a, b, c = get('source40', n), get('source41', n), get('source42', n)
    row(n + ': source40 and source41 admit and close the internally inconsistent manifest; source42 refuses SELECTED_COVER at admission and in the Run',
        all(adm(x) == 'ADMIT' and closed(x) for x in (a, b)) and refused(c, 'EXECUTION_INPUTS_SELECTED_COVER')
        and run_refused(c, 'EXECUTION_INPUTS_SELECTED_COVER'), obs(n))
    n = 'FW9-receipt-view-not-on-selectedRefs'
    row(n + ': refuses SELECTED_COVER on every tree', all(refused(get(l, n), 'EXECUTION_INPUTS_SELECTED_COVER') for l, _ in TREES), obs(n))
    n = 'FW12-unselected-null-universe-row-names-a-view'
    row(n + ': VIEW_TOTALITY at admission and a refused Run on every tree',
        all(refused(get(l, n), 'EXECUTION_INPUTS_VIEW_TOTALITY') and (get(l, n).get('fullRun') or {}).get('closed') is False for l, _ in TREES), obs(n))
    for n in ('FW10-captured-unattributed-view-with-foreign-planId', 'FW11-captured-unattributed-view-whose-producer-is-not-the-receipt-producer'):
        row(n + ' (observation)', True, obs(n), kind='observation')
    n = 'SW0-semantic-declares-control'
    row(n + ': closes on every tree', all(adm(get(l, n)) == 'ADMIT' and closed(get(l, n)) for l, _ in TREES), obs(n))
    n = 'SW1-two-cells-one-program-U-shared-view'
    row(n + ': the shared view is on both the inventory and the syntax row of the same program/U and the Run closes, identically on every tree',
        all(adm(get(l, n)) == 'ADMIT' and closed(get(l, n))
            and sorted(k.split('#')[0] for k in get(l, n).get('marksOnRows', {}).get('shared', [])) == ['inventory', 'syntax'] for l, _ in TREES)
        and len({get(l, n).get('executionInputsDigest') for l, _ in TREES}) == 1 and len({(get(l, n).get('fullRun') or {}).get('runId') for l, _ in TREES}) == 1,
        obs(n))
    for n in ('SW2-syntax-row-omits-shared-view', 'SW4-inventory-row-names-neither-view'):
        row(n + ': VIEW_TOTALITY on every tree', all(refused(get(l, n), 'EXECUTION_INPUTS_VIEW_TOTALITY') for l, _ in TREES), obs(n))
    n = 'SW3-shared-view-plus-view-matching-neither-cell-builder'
    a, b, c = get('source40', n), get('source41', n), get('source42', n)
    row(n + ': source40/41 builders drop the neither-cell view (EVALUATION_VIEW_ROOTS); source42 captures it on no row, the shared view stays on both rows, and the Run closes',
        all(x.get('marksCaptured', {}).get('neither') is False and run_refused(x, 'EVALUATION_VIEW_ROOTS') for x in (a, b))
        and c.get('marksCaptured', {}).get('neither') is True and not c.get('marksOnRows', {}).get('neither')
        and sorted(k.split('#')[0] for k in c.get('marksOnRows', {}).get('shared', [])) == ['inventory', 'syntax'] and closed(c), obs(n))
    n = 'SW3h-shared-view-plus-neither-view-explicit-capture'
    row(n + ': with explicit capture every tree names the neither-cell view on no row and closes',
        all(adm(get(l, n)) == 'ADMIT' and closed(get(l, n)) and not get(l, n).get('marksOnRows', {}).get('neither') for l, _ in TREES), obs(n))
    n = 'SW5-reminted-receipt-omits-shared-view'
    a, b, c = get('source40', n), get('source41', n), get('source42', n)
    row(n + ': source40/41 admit and close; source42 refuses SELECTED_COVER at admission and in the Run',
        all(adm(x) == 'ADMIT' and closed(x) for x in (a, b)) and refused(c, 'EXECUTION_INPUTS_SELECTED_COVER')
        and run_refused(c, 'EXECUTION_INPUTS_SELECTED_COVER'), obs(n))
    errors = {l: {k: v.get('worldError') or v.get('admissionError') for k, v in sides[l].items() if v.get('worldError') or v.get('admissionError')} for l, _ in TREES}
    row('no world or admission construction errors', not any(errors.values()), errors)
    OUT.write_text(json.dumps({'standing': 'independent reviewer discrimination probe; each tree own owner modules in its own process; reviewer-minted worlds on maintained fixtures; closed-run columns are the same manifest through that tree Run driver',
                               'rows': rows, 'failed': [r for r in rows if not r['ok']], 'childRuns': runs}, indent=1, default=str))
    print(json.dumps({'total': len(rows), 'failed': [(r['case'], r['observed']) for r in rows if not r['ok']]}, indent=1, default=str)[:12000])


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--child':
        child(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        parent()

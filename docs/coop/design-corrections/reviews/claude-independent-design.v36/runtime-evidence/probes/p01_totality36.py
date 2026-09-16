"""P01 — source36 dependency totality, A-13 closure and every boundary on FINAL frozen bytes, run AFTER law-derivation36.json.

Models (all read-only; no source byte written; patches are in-process only):
  frozen35   disposable tree = frozen36 foundation/native/workflows with the 35 parent bytes of the changed files overlaid;
             EVERY file in the tree hash-checked against the frozen35 manifest
  depscope   tree35 + the dependency-scope successor's three files (the totality author's preserved 'before' bytes, digests checked)
  final36    the frozen36 snapshot itself (check-atoms builders from frozen36)
  protoA     depscope + MY focused-assessment prototype A (drop a non-total same-kind position), in-process
  protoAB    protoA + my prototype B on the attestation view, in-process
STANDING: synthetic atom-api (global atom-input admission + evaluate_atom). The depth-2 case is a synthetic helper graph.
Nothing here is native producer admission, closed enumeration, a retained Run or product behaviour."""
import ast, copy, difflib, hashlib, importlib.util, inspect, itertools, json, os, shutil, sys, traceback

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
OUT = os.path.join(BASE, 'receipts')
PAR = os.path.join(BASE, 'disposable/parent35-delta-files')
T35 = os.path.join(BASE, 'disposable/tree35')
TDS = os.path.join(BASE, 'disposable/tree-depscope')
AUTH = '/tmp/opensip-design-corrections/claude-dependency-totality-author.v1'
ROOTP = '/tmp/opensip-design-corrections/root-source36-prose-completion.v1'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
DC = 'docs/coop/design-corrections'
FND = DC + '/foundation'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
m35 = {f['path']: f['sha256'] for f in json.load(open(REV + '/candidate-subject.v35.json'))['files']}
m36 = {f['path']: f['sha256'] for f in json.load(open(REV + '/candidate-subject.v36.json'))['files']}
R = {'standing': __doc__.strip().splitlines()[-2].strip(), 'errors': []}
CHECK = {}


def check(name, cond, observed=None):
    CHECK[name] = {'passed': bool(cond), 'observed': observed}
    print('%-86s %s' % (name, 'PASS' if cond else 'FAIL'), flush=True)


def build_tree(dst, overlays):
    # models load siblings relative to their own directory (native loads DC/discovery-defaults.py), so copy the whole
    # design-corrections tree except reviews/
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(os.path.join(S36, DC), os.path.join(dst, DC), ignore=lambda d, names: ['reviews'] if os.path.normpath(d) == os.path.normpath(os.path.join(S36, DC)) else [])
    for rel, src in overlays.items():
        shutil.copyfile(src, os.path.join(dst, rel))


def in_tree(rel):
    return rel.startswith(DC + '/') and not rel.startswith(DC + '/reviews/')


def tree_files(root):
    out = {}
    for d, _, fs in os.walk(os.path.join(root, DC)):
        for fn in fs:
            p = os.path.join(d, fn)
            out[os.path.relpath(p, root)] = sha(p)
    return out


# ------------------------------------------------------------------ trees and byte provenance
over35 = {}
for d, _, fs in os.walk(PAR):
    for fn in fs:
        rel = os.path.relpath(os.path.join(d, fn), PAR)
        if in_tree(rel):
            over35[rel] = os.path.join(d, fn)
build_tree(T35, over35)
t35 = tree_files(T35)
R['tree35'] = {'files': len(t35), 'overlaid': sorted(over35), 'mismatchVs35Manifest': sorted(p for p, h in t35.items() if m35.get(p) != h),
               'manifest35FilesInTreeMissing': sorted(p for p in m35 if in_tree(p) and p not in t35)}
check('T0-tree35-equals-frozen35-manifest-for-design-corrections-minus-reviews', not R['tree35']['mismatchVs35Manifest'] and not R['tree35']['manifest35FilesInTreeMissing'], R['tree35']['files'])
BEFORE = {'atom-evaluation-contract.v1.md': '72986bd35f7f2b2cd5d4e5e989036a974744c682a9db877ca08bd9ac52aa2d5a',
          'atom_model.v1.py': '2c5fdabb93785349c9c9a77ddf253685309727724d98897f60a0e8abf7177dac',
          'check-atoms.v1.py': '67d8c656ff912e023bc00fb56825568bbae9a3c5641cd23e869c11e5c2f159f5'}
AFTER = {'atom-evaluation-contract.v1.md': '2d399ec91b14f22ccb7459d01ead6f54806747b24a9867cc8862fe84afa5b8c0',
         'atom_model.v1.py': '4477285c547d6697e8faefea15ed0d05e0f6f0b144e0e5e8706b532451089ade',
         'check-atoms.v1.py': 'ebb9da8cf07336104441f7ef4b12d0d6f5250ea87542489367cf255d171cae2d'}
aname = lambda stage, fn: os.path.join(AUTH, stage, 'docs__coop__design-corrections__foundation__' + fn)
prov = {}
for fn in BEFORE:
    prov[fn] = {'authorBefore': sha(aname('before', fn)), 'authorBeforeAsReported': sha(aname('before', fn)) == BEFORE[fn],
                'authorAfter': sha(aname('after', fn)), 'authorAfterAsReported': sha(aname('after', fn)) == AFTER[fn],
                'final36': m36[FND + '/' + fn], 'frozen35': m35[FND + '/' + fn]}
    rb, ra = os.path.join(ROOTP, 'before', FND, fn), os.path.join(ROOTP, 'after', FND, fn)
    if os.path.isfile(rb):
        prov[fn].update(rootBefore=sha(rb), rootAfter=sha(ra), rootBeforeEqualsAuthorAfter=sha(rb) == AFTER[fn], rootAfterEqualsFinal36=sha(ra) == m36[FND + '/' + fn])
    prov[fn]['finalEqualsAuthorAfter'] = m36[FND + '/' + fn] == AFTER[fn]
reg = FND + '/evaluator-projection-registry.v1.json'
prov['evaluator-projection-registry.v1.json'] = {'rootBefore': sha(os.path.join(ROOTP, 'before', reg)), 'rootAfter': sha(os.path.join(ROOTP, 'after', reg)),
                                                 'rootBeforeEqualsFrozen35': sha(os.path.join(ROOTP, 'before', reg)) == m35[reg],
                                                 'rootAfterEqualsFinal36': sha(os.path.join(ROOTP, 'after', reg)) == m36[reg]}
R['byteProvenance'] = prov
check('E14a-final-atom_model-is-exactly-the-totality-author-after-bytes', prov['atom_model.v1.py']['finalEqualsAuthorAfter'] and 'rootBefore' not in prov['atom_model.v1.py'])
check('E14b-root-post-author-delta-is-contract-checker-registry-only', all(prov[f].get('rootBeforeEqualsAuthorAfter') and prov[f].get('rootAfterEqualsFinal36') for f in ('atom-evaluation-contract.v1.md', 'check-atoms.v1.py'))
      and prov['evaluator-projection-registry.v1.json']['rootBeforeEqualsFrozen35'] and prov['evaluator-projection-registry.v1.json']['rootAfterEqualsFinal36'])


def strip_docstrings(src):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) and node.body and isinstance(node.body[0], ast.Expr) \
                and isinstance(getattr(node.body[0], 'value', None), ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body = node.body[1:] or [ast.Pass()]
    return ast.dump(tree)


ca_after, ca_final = open(aname('after', 'check-atoms.v1.py')).read(), open(os.path.join(S36, FND, 'check-atoms.v1.py')).read()
R['rootCheckerChange'] = {'astEqualIgnoringDocstrings': strip_docstrings(ca_after) == strip_docstrings(ca_final),
                          'changedLines': [l for l in difflib.unified_diff(ca_after.splitlines(), ca_final.splitlines(), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]}
check('E14c-root-check-atoms-change-is-docstring-only-no-assertion', R['rootCheckerChange']['astEqualIgnoringDocstrings'], R['rootCheckerChange']['changedLines'])
ds_over = {FND + '/' + fn: aname('before', fn) for fn in BEFORE}
build_tree(TDS, ds_over)
R['treeDepscope'] = {fn: sha(os.path.join(TDS, FND, fn)) for fn in BEFORE}
check('T1-depscope-tree-carries-the-reported-dependency-scope-successor-bytes', all(R['treeDepscope'][fn] == BEFORE[fn] for fn in BEFORE))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('chk36', os.path.join(S36, FND, 'check-atoms.v1.py'))
A36 = K.AM
A35 = load('am35', os.path.join(T35, FND, 'atom_model.v1.py'))
ADS = load('amds', os.path.join(TDS, FND, 'atom_model.v1.py'))
APA = load('amprotoA', os.path.join(TDS, FND, 'atom_model.v1.py'))
APAB = load('amprotoAB', os.path.join(TDS, FND, 'atom_model.v1.py'))
OLD_A = '''    paired = []
    for sid, sc in _scopes_exact(inputs, drel, drung, source_u):
        if not any(_scope_contains(sc, nid) for nid in current_subjects):
            continue
        paired.extend(_pair_scope_coverages(sid, sc, covs, inputs))
    return _unique_pairs(paired)
'''
NEW_A = '''    paired, covered = [], set()
    for sid, sc in _scopes_exact(inputs, drel, drung, source_u):
        if not any(_scope_contains(sc, nid) for nid in current_subjects):
            continue
        found = _pair_scope_coverages(sid, sc, covs, inputs)
        if found:
            covered.update(sc.get("subjects") or [])
        paired.extend(found)
    if not set(current_subjects) <= covered:
        return []
    return _unique_pairs(paired)
'''
OLD_B = '        covs = _select_dep_coverages(drel, drung, source_u, target_u, inputs, None, None)\n'
NEW_B = '''        named = set()
        for sid in att.get("scopeRefs") or []:
            named.update(((inputs.get("scopes") or {}).get(sid) or {}).get("subjects") or [])
        covs = _select_dep_coverages(drel, drung, source_u, target_u, inputs, named or None,
                                     _source_kind_for_relation(rel) if named else None)
'''
for mod in (APA, APAB):
    s = inspect.getsource(mod._select_dep_coverages)
    assert s.count(OLD_A) == 1
    exec(s.replace(OLD_A, NEW_A), mod.__dict__)
s = inspect.getsource(APAB._build_attestation_view)
assert s.count(OLD_B) == 1
exec(s.replace(OLD_B, NEW_B), APAB.__dict__)
final_sel, final_att = inspect.getsource(A36._select_dep_coverages), inspect.getsource(A36._build_attestation_view)
contract36 = open(os.path.join(S36, FND, 'atom-evaluation-contract.v1.md')).read()
R['authorshipOverlap'] = {
    'finalSelectDepCoveragesContainsUnpatchedText': OLD_A in final_sel, 'finalContainsMyPrototypeA': 'if not set(current_subjects) <= covered' in inspect.getsource(A36),
    'finalAttestationViewContainsUnpatchedCall': OLD_B in final_att, 'finalContainsMyPrototypeB': 'named = set()' in inspect.getsource(A36),
    'finalContractContainsMyProposedWording': 'those paired scopes must jointly contain' in contract36,
    'finalContractTotalityHeading': '**Dependency totality (same kind).**' in contract36}
check('X1-my-prototype-A-B-and-proposed-wording-are-absent-from-final-bytes', R['authorshipOverlap']['finalSelectDepCoveragesContainsUnpatchedText']
      and not R['authorshipOverlap']['finalContainsMyPrototypeA'] and R['authorshipOverlap']['finalAttestationViewContainsUnpatchedCall']
      and not R['authorshipOverlap']['finalContainsMyPrototypeB'] and not R['authorshipOverlap']['finalContractContainsMyProposedWording'], R['authorshipOverlap'])
MODELS = {'frozen35': A35, 'depscope': ADS, 'final36': A36, 'protoA': APA, 'protoAB': APAB}
R['modelSha256'] = {'frozen35': sha(os.path.join(T35, FND, 'atom_model.v1.py')), 'depscope': sha(os.path.join(TDS, FND, 'atom_model.v1.py')),
                    'final36': sha(os.path.join(S36, FND, 'atom_model.v1.py'))}
U1, U2 = K.U1, K.U2
F, G, H = K.F_SYM, K.G_SYM, K.H_SYM
FS = K.F_SUBJ
GS = {'universe': U1, 'kind': 'symbol', 'nativeSubjectId': G}
REACH = K.REACH_ALL
tag = lambda cid: cid.split(':')[1][0]


def ev(mod, atom, subj, inputs):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'value': 'REFUSE:' + e.key}
    return {'value': r['value'], 'causes': [[c['code'], c.get('universe') and c['universe'][:2], c.get('nativeCause')] for c in r['causes']],
            'nativeDeficiencies': r['nativeDeficiencies'], 'coverageIds': [tag(c) for c in r['coverageIds']], 'known': len(r['knownFactIds'])}


def section(name, fn):
    try:
        fn()
    except Exception:  # noqa: BLE001
        R['errors'].append({'section': name, 'traceback': traceback.format_exc()[-2500:]})
        print('SECTION ERROR', name, traceback.format_exc()[-1500:], flush=True)


IN = lambda op, **kw: dict(REACH, op=op, endpoint='target', **kw)
OPS = {'all-covered': IN('all-covered'), 'none': IN('none'), 'count<=1': IN('count-at-most', n=1)}
MISSING = {'g-absent': [K.F_DEP], 'g-scope-without-coverage': [K.F_DEP, ([G], '4', 'no-coverage')],
           'g-coverage-other-target': [K.F_DEP, ([G], '4', 'other-target')], 'g-wrong-universe-scope': [K.F_DEP, ([G], '4', 'wrong-universe')],
           'g-unrelated-h-only': [K.F_DEP, ([H], '5', 'paired')], 'f-absent-g-only': [K.G_DEP]}
FULL = {'disjoint': [K.F_DEP, K.G_DEP], 'spanning': [([F, G], '2', 'paired')], 'disjoint-plus-h': [K.F_DEP, K.G_DEP, ([H], '5', 'paired')]}


def e1():
    T = {}
    for label, deps in list(MISSING.items()) + list(FULL.items()):
        T[label] = {m: {o: ev(mod, a, FS, K.totality_inputs([[F, G]], deps)) for o, a in OPS.items()} for m, mod in MODELS.items()}
        print('E1 %-26s' % label, {m: [T[label][m][o]['value'] for o in OPS] for m in MODELS}, flush=True)
    R['E1'] = T
    f36 = {l: T[l]['final36'] for l in T}
    check('E1a-final36-every-missing-shape-unknown-for-all-covered-none-count', all(f36[l][o]['value'] == 'indeterminate' for l in MISSING for o in OPS))
    check('E1b-final36-missing-shapes-answer-required-relation-missing', all('required-relation-missing' in f36[l]['all-covered']['nativeDeficiencies'] for l in MISSING))
    check('E1c-final36-f-actual-dependency-stays-cited-when-present', all('2' in f36[l]['all-covered']['coverageIds'] for l in MISSING if l != 'f-absent-g-only'))
    check('E1d-final36-full-covers-true-no-deficiency-unrelated-h-uncited', all(f36[l][o]['value'] == 'true' for l in FULL for o in OPS)
          and all(not f36[l]['all-covered']['nativeDeficiencies'] and '5' not in f36[l]['all-covered']['coverageIds'] for l in FULL))
    check('E1e-frozen35-and-depscope-answered-true-on-merged-missing-shapes (defect reproduced)',
          all(T[l][m]['all-covered']['value'] == 'true' for l in ('g-absent', 'g-scope-without-coverage', 'g-wrong-universe-scope') for m in ('frozen35', 'depscope')),
          {l: [T[l]['frozen35']['all-covered']['value'], T[l]['depscope']['all-covered']['value']] for l in MISSING})


section('E1', e1)


def with_other_carrier(inputs, cid_tag, native_cause):
    cov = inputs['coverages'][K.cov2(cid_tag)]
    cov['entry']['coverage'], cov['entry']['deficiency'], cov['entry']['nativeCause'] = 'unknown', 'input-closure-incomplete', native_cause
    return inputs


SHAPES = {'f-only': ([K.F_DEP], None), 'g-only': ([K.G_DEP], None), 'f-and-g': ([K.F_DEP, K.G_DEP], None),
          'f-unknown+g-uncovered': ([([F], '2', 'unknown-carrier')], None), 'f-unknown+g-covered': ([([F], '2', 'unknown-carrier'), K.G_DEP], None),
          'f-unknown+g-unknown-other-carrier': ([([F], '2', 'unknown-carrier'), K.G_DEP], ('4', 'no-program-unit'))}


def grouped(deps, other, parts):
    i = K.totality_inputs(parts, deps)
    return with_other_carrier(i, *other) if other else i


def e2():
    T = {}
    for label, (deps, other) in SHAPES.items():
        T[label] = {}
        for m in ('frozen35', 'depscope', 'final36'):
            mg = ev(MODELS[m], OPS['all-covered'], FS, grouped(deps, other, [[F, G]]))
            sp = ev(MODELS[m], OPS['all-covered'], FS, grouped(deps, other, [[F], [G]]))
            T[label][m] = {'merged': mg, 'split': sp, 'valueEqual': mg['value'] == sp['value'], 'causesEqual': mg['causes'] == sp['causes'],
                           'deficienciesEqual': mg['nativeDeficiencies'] == sp['nativeDeficiencies']}
        print('E2 %-34s' % label, {m: [T[label][m]['merged']['value'], T[label][m]['split']['value'], T[label][m]['causesEqual']] for m in T[label]}, flush=True)
    R['E2'] = T
    f = {l: T[l]['final36'] for l in T}
    check('E2a-final36-regrouping-never-changes-the-value', all(f[l]['valueEqual'] for l in f), {l: [f[l]['merged']['value'], f[l]['split']['value']] for l in f})
    check('E2b-final36-complete-entry-shapes-equal-causes-and-deficiencies', all(f[l]['causesEqual'] and f[l]['deficienciesEqual'] for l in ('f-only', 'g-only', 'f-and-g')))
    cex = f['f-unknown+g-uncovered']
    cu = lambda r: sorted([c[2] for c in r['causes'] if c[0] == 'coverage-unknown'], key=str)
    check('E2c-root-counterexample-reproduced-split-adds-a-per-view-carrier-value-unchanged',
          cex['valueEqual'] and cex['merged']['value'] == 'indeterminate' and not cex['causesEqual'] and cu(cex['merged']) == ['lockfile-missing'] and cu(cex['split']) == [None, 'lockfile-missing'],
          {'merged': cu(cex['merged']), 'split': cu(cex['split'])})
    pre = T['f-unknown+g-unknown-other-carrier']['frozen35']
    check('E2d-per-view-carrier-divergence-predates-totality (frozen35 split vs merged with two partial carriers)',
          pre['valueEqual'] and not pre['causesEqual'], {'merged': cu(pre['merged']), 'split': cu(pre['split'])})


section('E2', e2)


def e3():
    T = {}
    for label, deps, attest in (('coverage-route/f-complete+g-uncovered', [K.F_DEP], False),
                                ('coverage-route/f-unknown+g-uncovered', [([F], '2', 'unknown-carrier')], False),
                                ('attestation-route/f-complete+g-uncovered', [K.F_DEP], True),
                                ('attestation-route/f-unknown+g-uncovered', [([F], '2', 'unknown-carrier')], True)):
        T[label] = {m: ev(MODELS[m], OPS['all-covered'], FS, K.totality_inputs([[F, G]], deps, attest=attest)) for m in ('final36', 'protoA', 'protoAB')}
        print('E3 %-44s' % label, {m: [v['value'], v['nativeDeficiencies'], [c[2] for c in v['causes'] if c[0] == 'coverage-unknown'], v['coverageIds']] for m, v in T[label].items()}, flush=True)
    R['E3'] = T
    fu = T['coverage-route/f-unknown+g-uncovered']
    check('E3a-final36-retains-partial-carrier-deficiency-and-citation-beside-required-relation-missing',
          set(fu['final36']['nativeDeficiencies']) == {'input-closure-incomplete', 'required-relation-missing'}
          and [c[2] for c in fu['final36']['causes'] if c[0] == 'coverage-unknown'] == ['lockfile-missing'] and '2' in fu['final36']['coverageIds'])
    check('E3b-my-prototype-A-drops-the-read-carrier-and-citation-same-value',
          fu['protoA']['value'] == fu['final36']['value'] == 'indeterminate' and fu['protoA']['nativeDeficiencies'] == ['required-relation-missing']
          and [c[2] for c in fu['protoA']['causes'] if c[0] == 'coverage-unknown'] == [None] and '2' not in fu['protoA']['coverageIds'])
    fa = T['attestation-route/f-unknown+g-uncovered']
    check('E3c-attestation-route-final36-unknown-and-retains-carrier; protoA-alone-would-answer-true', fa['final36']['value'] == 'indeterminate'
          and 'input-closure-incomplete' in fa['final36']['nativeDeficiencies'] and T['attestation-route/f-complete+g-uncovered']['protoA']['value'] == 'true',
          {m: T['attestation-route/f-complete+g-uncovered'][m]['value'] for m in ('final36', 'protoA', 'protoAB')})


section('E3', e3)


def e4():
    T = {}
    for dlabel, deps in (('f-only', [K.F_DEP]), ('f-unknown', [([F], '2', 'unknown-carrier')]), ('g-only', [K.G_DEP])):
        for slabel, subj in (('from-f', FS), ('from-g', GS)):
            T['%s/%s' % (dlabel, slabel)] = {m: ev(mod, dict(REACH, endpoint='source'), subj, K.totality_inputs([[F, G]], deps)) for m, mod in MODELS.items()}
    R['E4'] = T
    print('E4 outgoing', {k: {m: v['value'] for m, v in T[k].items()} for k in T}, flush=True)
    check('E4-outgoing-identical-frozen35-depscope-final36-in-value-causes-citations', all(T[k]['frozen35'] == T[k]['depscope'] == T[k]['final36'] for k in T))


section('E4', e4)


def e5():
    fid = K.fact2('1')
    T = {}
    for label, deps in (('f-only', [K.F_DEP]), ('f-and-g', [K.F_DEP, K.G_DEP])):
        i = K.totality_inputs([[F, G]], deps)
        i['facts'] = {fid: K.incoming_reachability_fact(fid, G)}
        T[label] = {m: {o: ev(mod, IN(op, **ex), FS, i) for o, op, ex in (('exists', 'exists', {}), ('none', 'none', {}), ('count<=0', 'count-at-most', {'n': 0}),
                                                                             ('count<=1', 'count-at-most', {'n': 1}), ('all-covered', 'all-covered', {}))}
                    for m, mod in MODELS.items()}
    R['E5'] = T
    print('E5 dominance', {l: {m: {o: v['value'] for o, v in T[l][m].items()} for m in T[l]} for l in T}, flush=True)
    f = T['f-only']['final36']
    check('E5-known-match-decides-exists-none-exceeded-bound; totality-only-bounds-need-completeness',
          [f[o]['value'] for o in ('exists', 'none', 'count<=0', 'count<=1', 'all-covered')] == ['true', 'false', 'false', 'indeterminate', 'indeterminate']
          and all(v['known'] == 1 for v in f.values()) and T['f-and-g']['final36']['count<=1']['value'] == 'true')


section('E5', e5)


def e6():
    T = {}
    for label, deps in (('none', []), ('f-only', [K.F_DEP]), ('f-and-g', [K.F_DEP, K.G_DEP]), ('spanning', [([F, G], '2', 'paired')]),
                        ('h-only', [([H], '5', 'paired')]), ('f+g-scope-without-coverage', [K.F_DEP, ([G], '4', 'no-coverage')])):
        T[label] = {m: ev(mod, OPS['all-covered'], FS, K.totality_inputs([[F, G]], deps, attest=True)) for m, mod in MODELS.items()}
    R['E6'] = T
    print('E6 attestation', {l: {m: v['value'] for m, v in T[l].items()} for l in T}, flush=True)
    f = {l: T[l]['final36']['value'] for l in T}
    check('E6a-final36-attestation-owes-owned-scope-subjects', f == {'none': 'indeterminate', 'f-only': 'indeterminate', 'f-and-g': 'true', 'spanning': 'true',
                                                                 'h-only': 'indeterminate', 'f+g-scope-without-coverage': 'indeterminate'}, f)
    check('E6b-frozen35-depscope-attestation-f-only-was-true (defect reproduced)', T['f-only']['frozen35']['value'] == T['f-only']['depscope']['value'] == 'true')


section('E6', e6)


def e7():
    T = {}
    for route in ('attestation', 'coverage'):
        for mode in ('null', 'absent'):
            for holder in ('f', 'h'):
                deps = [K.F_DEP, K.G_DEP] if holder == 'f' else [K.F_DEP, K.G_DEP, ([H], '5', 'paired')]
                i = K.totality_inputs([[F, G]], deps, attest=route == 'attestation')
                sc = i['scopes'][K.scope2('2' if holder == 'f' else '5')]
                if mode == 'null':
                    sc['enumeratorClosure'] = None
                else:
                    sc.pop('enumeratorClosure')
                T['%s/%s/%s' % (route, mode, holder)] = {m: ev(mod, OPS['all-covered'], FS, i) for m, mod in MODELS.items()}
    R['E7'] = T
    print('E7 carrier', {k: {m: v['value'] for m, v in T[k].items()} for k in T}, flush=True)
    check('E7a-attestation-route-now-refuses-an-owed-dependency-scope-failing-its-carrier (new consumption)',
          all(T['attestation/%s/f' % md]['final36']['value'] == 'REFUSE:ATOM_NATIVE_CARRIER' and T['attestation/%s/f' % md]['frozen35']['value'] == 'true' for md in ('null', 'absent')),
          {md: [T['attestation/%s/f' % md][m]['value'] for m in ('frozen35', 'depscope', 'final36')] for md in ('null', 'absent')})
    check('E7b-coverage-route-refusal-unchanged-frozen35-to-final36', all(T['coverage/%s/f' % md]['frozen35']['value'] == T['coverage/%s/f' % md]['final36']['value'] for md in ('null', 'absent')),
          {md: [T['coverage/%s/f' % md][m]['value'] for m in ('frozen35', 'final36')] for md in ('null', 'absent')})


section('E7', e7)


def empty_reach(calls_mode, attest):
    plan = K.plan_one(cap='reachability')
    plan['cells'].append(K.ref_cell('reachability', 'ts-tsconfig', U2, 'pkg-empty', K.C_PROV2, ['pkg-empty/src/index.ts']))
    empty = K.inv_symbol(universe=U2, nid='ts-symbol:pkg-empty/src/index.ts#unused', path='pkg-empty/src/index.ts', qn='unused')
    empty.update({'cellOrdinal': 1, 'rows': [], 'examinedPaths': ['pkg-empty/src/index.ts']})
    i = K.base_inputs(enumerationPlan=plan, inventories=[K.inv_symbol(), empty])
    K.install_pair(i, *K.paired('reachability', 'from-resolved-calls', U1, U1, [F], tag='1'))
    K.install_pair(i, *K.paired('calls', 'resolved-callee', U1, U1, [F], tag='2'))
    sid, sc = K.scope('reachability', 'from-resolved-calls', U2, U1, [], sid='7')
    sc['enumeratorClosure'] = K.C_PROV2
    i['scopes'][sid] = sc
    if attest:
        i['incomingSearchAttestations'] = [K.incoming_att('reachability', 'from-resolved-calls', U2, U1, [sid], [empty], providerClosure=K.C_PROV2)]
    else:
        cid, cov = K.coverage('reachability', 'from-resolved-calls', U2, U1, cid='7')
        i['coverages'][cid] = cov
        i['coverageScopes'][cid] = sid
    if calls_mode == 'explicit-empty-calls-partition':
        s8, sc8 = K.scope('calls', 'resolved-callee', U2, U1, [], sid='8')
        sc8['enumeratorClosure'] = K.C_PROV2
        c8, cv8 = K.coverage('calls', 'resolved-callee', U2, U1, cid='8')
        i['scopes'][s8] = sc8
        i['coverages'][c8] = cv8
        i['coverageScopes'][c8] = s8
    return i


def e8():
    T = {}
    for route in ('coverage', 'attestation'):
        for cm in ('no-calls', 'explicit-empty-calls-partition'):
            T['reachability/%s/%s' % (route, cm)] = {m: ev(mod, OPS['all-covered'], FS, empty_reach(cm, route == 'attestation')) for m, mod in MODELS.items()}
    for label, inp in (('references/coverage/empty-scope-paired', K.empty_program_inputs('empty-scope-paired')),
                       ('references/attestation/empty-scope', K.empty_program_inputs('empty-scope', attest=True))):
        T[label] = {m: ev(mod, {**K.REF_IN, 'op': 'none'}, FS, inp) for m, mod in MODELS.items()}
    R['E8'] = T
    print('E8 empty', {k: {m: [v['value'], v.get('nativeDeficiencies')] for m, v in T[k].items() if m in ('frozen35', 'final36')} for k in T}, flush=True)
    f = {k: T[k]['final36']['value'] for k in T}
    check('E8a-empty-coverage-route-reachability-conservative-even-with-explicit-empty-calls-partition',
          f['reachability/coverage/no-calls'] == f['reachability/coverage/explicit-empty-calls-partition'] == 'indeterminate'
          and 'required-relation-missing' in T['reachability/coverage/explicit-empty-calls-partition']['final36']['nativeDeficiencies'], f)
    check('E8b-empty-attestation-route-closes-only-with-explicit-empty-calls-partition',
          f['reachability/attestation/explicit-empty-calls-partition'] == 'true' and f['reachability/attestation/no-calls'] == 'indeterminate', f)
    check('E8c-references-empty-scope-closes-by-coverage-and-by-attestation', f['references/coverage/empty-scope-paired'] == f['references/attestation/empty-scope'] == 'true', f)
    check('E8d-empty-behaviour-unchanged-frozen35-to-final36', all(T[k]['frozen35']['value'] == T[k]['final36']['value'] for k in T))


section('E8', e8)


def clones(dep):
    i = K.base_inputs(enumerationPlan=K.plan_one(cap='clones-fact', kinds=['file']), inventories=[K.inv_file(), K.inv_symbol(), K.inv_symbol(nid=G, qn='g')])
    K.install_pair(i, *K.paired('clones', 'normalized-body-hash', U1, U1, ['src/a.ts'], tag='1'))
    if dep in ('declares-f-only', 'declares-f-and-g'):
        K.install_pair(i, *K.paired('declares', 'syntactic', U1, U1, [F], tag='5'))
    if dep == 'declares-f-and-g':
        K.install_pair(i, *K.paired('declares', 'syntactic', U1, U1, [G], tag='6'))
    return i


def e9():
    atom = {'op': 'all-covered', 'relation': 'clones', 'minResolution': 'normalized-body-hash', 'filters': []}
    FILE = {'universe': U1, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'}
    T = {d: {m: ev(mod, atom, FILE, clones(d)) for m, mod in MODELS.items()} for d in ('no-declares', 'declares-f-only', 'declares-f-and-g')}
    R['E9'] = T
    print('E9 clones->declares', {d: {m: v['value'] for m, v in T[d].items()} for d in T}, flush=True)
    check('E9-different-kind-whole-source-unchanged-and-unchecked', all(T[d]['frozen35'] == T[d]['final36'] for d in T)
          and T['declares-f-only']['final36']['value'] == 'true' and T['no-declares']['final36']['value'] == 'indeterminate')


section('E9', e9)


def e10():
    T = {}
    for endpoint in ('source', 'target'):
        atom = dict(REACH, endpoint=endpoint)
        absent = K.exact_dep_inputs()
        absent['scopes'].pop(K.scope2('2'))
        absent['coverageScopes'].pop(K.cov2('2'))
        T['%s/dependency-absent' % endpoint] = {m: ev(MODELS[m], atom, FS, absent) for m in ('frozen35', 'depscope', 'final36')}
        for field, mode, other in K.DEP_SCOPE_MUTATIONS:
            label = '%s/%s/%s%s' % (endpoint, field, mode, ('=' + str(other)[:12]) if other else '')
            T[label] = {m: ev(MODELS[m], atom, FS, K.mutate_dep_scope(K.exact_dep_inputs(), field, mode, other)) for m in ('frozen35', 'depscope', 'final36')}
        both = K.exact_dep_inputs()
        s3, sc3 = K.scope('calls', 'resolved-callee', U2, U1, [F], sid='3')
        c3, cv3 = K.coverage('calls', 'resolved-callee', U1, U1, cid='3')
        both['scopes'][s3], both['coverages'][c3], both['coverageScopes'][c3] = sc3, cv3, s3
        T['%s/exact-present-plus-mapped-wrong-universe-scope' % endpoint] = {m: ev(MODELS[m], atom, FS, both) for m in ('frozen35', 'depscope', 'final36')}
    R['E10'] = T
    healed35 = sorted(k for k, v in T.items() if 'dependency-absent' not in k and 'plus' not in k and v['frozen35']['value'] == 'true')
    R['E10-healedOnFrozen35'] = healed35
    print('E10 A-13: frozen35 healed %d of %d mutation rows' % (len(healed35), sum(1 for k in T if 'dependency-absent' not in k and 'plus' not in k)), flush=True)
    muts = [k for k in T if 'dependency-absent' not in k and 'plus' not in k]
    check('E10a-A13-every-non-exact-mapped-scope-is-absent-on-both-endpoints-final36',
          all(T[k]['final36'] == T[k.split('/')[0] + '/dependency-absent']['final36'] for k in muts)
          and all(T[k]['final36']['value'] == 'indeterminate' and '2' not in T[k]['final36']['coverageIds'] for k in muts))
    check('E10b-A13-reproduced-on-frozen35 (some mutation rows healed to true)', len(healed35) > 0, healed35)
    check('E10c-exact-scope-still-pairs-beside-a-mapped-non-exact-scope', all(T['%s/exact-present-plus-mapped-wrong-universe-scope' % ep]['final36']['value'] == 'true'
                                                                           and '3' not in T['%s/exact-present-plus-mapped-wrong-universe-scope' % ep]['final36']['coverageIds'] for ep in ('source', 'target')))
    check('E10d-final36-equals-depscope-on-every-A13-row (totality changes nothing here)', all(T[k]['final36'] == T[k]['depscope'] for k in T))


section('E10', e10)


def e11():
    shapes = {'merged-f-only': K.totality_inputs([[F, G]], [K.F_DEP]),
              'merged-f-unknown+g-uncovered': K.totality_inputs([[F, G]], [([F], '2', 'unknown-carrier')]),
              'split-two-carriers': grouped([([F], '2', 'unknown-carrier'), K.G_DEP], ('4', 'no-program-unit'), [[F], [G]]),
              'attested-f+g-scope-without-coverage': K.totality_inputs([[F, G]], [K.F_DEP, ([G], '4', 'no-coverage')], attest=True),
              'full-disjoint-plus-h': K.totality_inputs([[F, G]], [K.F_DEP, K.G_DEP, ([H], '5', 'paired')])}
    T = {}
    for label, base in shapes.items():
        for ep in ('target', 'source'):
            seen, n = set(), 0
            for order in itertools.permutations(('scopes', 'coverages', 'coverageScopes', 'inventories')):
                for rev in (False, True):
                    j = copy.deepcopy(base)
                    if rev:
                        for key in order:
                            v = j[key]
                            j[key] = list(reversed(v)) if isinstance(v, list) else dict(reversed(list(v.items())))
                    else:
                        for key in order[:2]:
                            v = j[key]
                            if isinstance(v, dict):
                                j[key] = dict(sorted(v.items(), key=lambda kv: hashlib.sha256((order[0] + kv[0]).encode()).hexdigest()))
                    seen.add(json.dumps(ev(A36, dict(REACH, endpoint=ep), FS, j), sort_keys=True))
                    n += 1
            T['%s/%s' % (label, ep)] = {'orderings': n, 'distinct': len(seen)}
    R['E11'] = T
    print('E11 orderings', T, flush=True)
    check('E11-final36-one-result-for-every-insertion-order', all(v['distinct'] == 1 for v in T.values()), T)


section('E11', e11)


def e12():
    reg = {}
    for m, mod in MODELS.items():
        K.AM = mod
        fails = []
        for fn in K.CASES:
            try:
                fn()
            except Exception as ex:  # noqa: BLE001
                fails.append({'case': fn.__name__, 'error': '%s: %s' % (type(ex).__name__, str(ex)[:220])})
        reg[m] = {'cases': len(K.CASES), 'failed': fails}
        print('E12 frozen36 check-atoms on %-9s %d cases, %d failed %s' % (m, len(K.CASES), len(fails), [f['case'] for f in fails]), flush=True)
    K.AM = A36
    R['E12'] = reg
    tot = sorted(f.__name__ for f in K.CASES if f.__name__.startswith('test_dependency_totality'))
    check('E12a-final36-passes-all-frozen36-check-atoms-cases', reg['final36']['cases'] == 101 and not reg['final36']['failed'])
    check('E12b-every-totality-control-discriminates-depscope-and-frozen35', set(tot) <= {f['case'] for f in reg['depscope']['failed']}
          and set(tot) <= {f['case'] for f in reg['frozen35']['failed']}, tot)
    check('E12c-checker-discriminates-my-prototype-A-and-AB (partial-carrier retention)',
          any(f['case'] == 'test_dependency_totality_keeps_partial_carrier' for f in reg['protoA']['failed'])
          and any(f['case'] == 'test_dependency_totality_keeps_partial_carrier' for f in reg['protoAB']['failed']),
          {m: [f['case'] for f in reg[m]['failed']] for m in ('protoA', 'protoAB')})


section('E12', e12)
R['checks'] = CHECK
R['failedChecks'] = sorted(k for k, v in CHECK.items() if not v['passed'])
R['frozen36AtomOwnersUnchanged'] = all(sha(os.path.join(S36, FND, fn)) == m36[FND + '/' + fn] for fn in BEFORE)
R['authorAndRootRuntimesUnchanged'] = all(sha(aname(st, fn)) == (BEFORE if st == 'before' else AFTER)[fn] for st in ('before', 'after') for fn in BEFORE)
print('\nchecks %d failed %s errors %d | frozen36 owners unchanged %s | author runtime unchanged %s' % (
    len(CHECK), R['failedChecks'], len(R['errors']), R['frozen36AtomOwnersUnchanged'], R['authorAndRootRuntimesUnchanged']))
json.dump(R, open(os.path.join(OUT, 'p01-totality36.json'), 'w'), indent=1, default=str)
print('wrote p01-totality36.json')

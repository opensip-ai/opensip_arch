"""Q09 — 'no owed binding' versus 'no binding at the SUBJECT universe', incoming endpoint.

Q05 A2/A4 showed incoming does not stop when the subject universe U has no owed binding. This probe
asks the consequential question: when OTHER programs are owed and fully evidenced, can incoming answer
a NEGATIVE (none=true / exists=false) although the subject's own program U was never bound for the
relation, so its own referrers were never searched?

Every case pairs the incoming answer with the outgoing answer on the same inputs and with a
discriminating variant where U IS bound, so the only difference is the binding at U.
STANDING: atom-api (global atom-input admission + evaluate_atom over synthetic inputs). The
enumeration-plan fixture is additionally checked against enumeration-plan.schema.v1.json; that is
schema admission only, not enumeration closed-world admission and not a retained Run.
"""
import copy, hashlib, importlib.util, json, os, sys

S34 = '/tmp/opensip-design-corrections/candidate-subject.v34'
F34 = S34 + '/docs/coop/design-corrections/foundation'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
OUT = os.path.join(BASE, 'receipts')
MAN34 = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v34.json'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


man = json.load(open(MAN34))
drift = lambda: sum(1 for f in man['files'] if sha(os.path.join(S34, f['path'])) != f['sha256'])
K = load('chk34', F34 + '/check-atoms.v1.py')
AM = K.AM
U1, U2, UR = K.U1, K.U2, K.UR
F_SYM = K.F_SYM
G_SYM = 'ts-symbol:pkg-b/src/b.ts#g'
F_SUBJ = K.F_SUBJ
R = {'frozen34DriftBefore': drift(), 'cases': {}}


def ev(atom, inputs):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(F_SUBJ), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key, 'detail': str(e)[:200]}
    return {'admission': 'ADMIT', 'value': r['value'],
            'causes': sorted([c['code'], c.get('universe')] for c in r['causes']),
            'coverageIds': r['coverageIds'], 'scopeIds': r['scopeIds']}


REF = {'relation': 'references', 'minResolution': 'resolved-binding', 'filters': []}


def plan(u1_references_binding, other='U2-evidenced'):
    """cell for the SUBJECT'S program (symbols of f at U1) comes from a calls cell, so f is a real
    inventoried subject even when U1 has no references binding."""
    cells = [{
        'capabilityId': 'calls', 'languageMode': 'ts-tsconfig', 'workspaceRoot': 'pkg-a', 'required': True,
        'kinds': ['symbol'],
        'programBindings': [{'ordinal': 0, 'provenance': 'default-unit',
                             'enumerator': {'status': 'selected', 'closureId': K.C_PROV},
                             'nativeContextDigest': K.H('0'), 'universe': U1, 'programEntry': None,
                             'extents': [{'kind': 'symbol', 'paths': ['src/a.ts']}]}]}]
    if other in ('U2-evidenced', 'U2-unevidenced'):
        cells.append(K.ref_cell('references', 'ts-tsconfig', U2, 'pkg-b', K.C_PROV2, ['pkg-b/src/b.ts']))
    elif other == 'rust-available':
        cells.append(K.ref_cell('references', 'rust-cargo', UR, 'crate', K.C_PROV2, ['crate/src/lib.rs']))
    if u1_references_binding == 'available':
        cells.append(K.ref_cell('references', 'ts-tsconfig', U1, 'pkg-a', K.C_PROV, ['src/a.ts']))
    elif u1_references_binding == 'unavailable':
        cells.append(K.ref_cell('references', 'ts-tsconfig', None, 'pkg-a', K.C_PROV, ['src/a.ts']))
    cells.sort(key=lambda c: (c['capabilityId'], c['languageMode'], c['workspaceRoot']))
    p = K.plan_one(cap='calls')
    p['cells'] = cells
    return p


def inputs_for(u1_references_binding, other='U2-evidenced', u1_evidenced=False):
    p = plan(u1_references_binding, other)
    ordinal = {(c['capabilityId'], c['workspaceRoot']): n for n, c in enumerate(p['cells'])}
    inv_f = K.inv_symbol(); inv_f['cellOrdinal'] = ordinal[('calls', 'pkg-a')]
    invs = [inv_f]
    i = K.base_inputs(enumerationPlan=p, inventories=invs)
    if other in ('U2-evidenced', 'U2-unevidenced'):
        inv_g = K.inv_symbol(universe=U2, nid=G_SYM, path='pkg-b/src/b.ts', qn='g')
        inv_g['cellOrdinal'] = ordinal[('references', 'pkg-b')]
        i['inventories'].append(inv_g)
        if other == 'U2-evidenced':
            s, sc = K.scope('references', 'resolved-binding', U2, U1, [G_SYM], sid='2')
            sc['enumeratorClosure'] = K.C_PROV2
            c, cv = K.coverage('references', 'resolved-binding', U2, U1, cid='2')
            K.install_pair(i, s, sc, c, cv)
    if u1_evidenced:
        K.install_pair(i, *K.paired('references', 'resolved-binding', U1, U1, [F_SYM], tag='1'))
    return i


CASES = {
    'U1-unbound__U2-same-family-fully-evidenced': inputs_for('none', 'U2-evidenced'),
    'U1-bound-and-evidenced__U2-same-family-fully-evidenced': inputs_for('available', 'U2-evidenced', u1_evidenced=True),
    'U1-bound-unavailable__U2-same-family-fully-evidenced': inputs_for('unavailable', 'U2-evidenced'),
    'U1-bound-but-unevidenced__U2-same-family-fully-evidenced': inputs_for('available', 'U2-evidenced'),
    'U1-unbound__only-foreign-family-available': inputs_for('none', 'rust-available'),
    'U1-unbound__no-references-binding-anywhere': inputs_for('none', 'none'),
}
for label, inp in CASES.items():
    row = {}
    for ep in ('target', 'source'):
        for op in ('none', 'exists'):
            row['%s/%s' % ('incoming' if ep == 'target' else 'outgoing', op)] = ev(dict(REF, op=op, endpoint=ep), inp)
    R['cases'][label] = row
    print('%-58s in:none=%-13s in:exists=%-13s out:none=%-13s | in causes %s' % (
        label, row['incoming/none'].get('value', row['incoming/none'].get('key')),
        row['incoming/exists'].get('value', row['incoming/exists'].get('key')),
        row['outgoing/none'].get('value', row['outgoing/none'].get('key')),
        row['incoming/none'].get('causes')), flush=True)

u = R['cases']['U1-unbound__U2-same-family-fully-evidenced']
b = R['cases']['U1-bound-but-unevidenced__U2-same-family-fully-evidenced']
R['finding'] = {
    'incomingNegativeWithSubjectProgramUnbound': u['incoming/none'].get('value') == 'true' and u['incoming/exists'].get('value') == 'false',
    'outgoingOnSameInputsIsUnknown': u['outgoing/none'].get('value') == 'indeterminate',
    'bindingU1WithoutEvidenceMakesIncomingUnknown': b['incoming/none'].get('value') == 'indeterminate',
    'citedEvidenceForTheNegative': {'coverageIds': u['incoming/none'].get('coverageIds'), 'scopeIds': u['incoming/none'].get('scopeIds')},
}
print('\nfinding:', json.dumps(R['finding'], indent=1))

from jsonschema import Draft202012Validator  # noqa: E402
schema = json.load(open(F34 + '/enumeration-plan.schema.v1.json'))
R['enumerationPlanSchema'] = {
    'sha256': sha(F34 + '/enumeration-plan.schema.v1.json'),
    'narrowedPlanErrors': sorted(e.message[:160] for e in Draft202012Validator(schema).iter_errors(plan('none', 'U2-evidenced')))[:6],
    'baselineFixtureErrors': sorted(e.message[:160] for e in Draft202012Validator(schema).iter_errors(K.plan_one()))[:6]}
print('enumeration-plan schema on the narrowed plan:', R['enumerationPlanSchema'])
R['frozen34DriftAfter'] = drift()
print('frozen34 drift before/after: %d/%d' % (R['frozen34DriftBefore'], R['frozen34DriftAfter']))
json.dump(R, open(os.path.join(OUT, 'q09-subject-universe.json'), 'w'), indent=1, default=str)
print('wrote q09-subject-universe.json')

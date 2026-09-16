"""P03 — root's source36 history-order and runtime-polarity prose/registry corrections, run AFTER law-derivation36.json.
Substantive owner review, not pin verification: (1) exact new registry strings and absence of the uniqueness claim;
(2) every owner consuming historySubjectOrder/observabilityFilter as a machine rule (text scan of frozen36 docs);
(3) stock-schema admission of duplicate paths in producer order; (4) atom retains every ordinal on frozen35 AND final36;
(5) repair targetSubjectProjection ambiguity refusal text still present; (6) runtime polarity matrix on frozen35 AND final36,
including 'relevant' (subject-matched) uncertain disclosure independent of every filter.
Requires p01's disposable tree35. STANDING: atom-api synthetic + stock schema + static owner text."""
import copy, hashlib, importlib.util, json, os, re, sys

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
T35 = os.path.join(BASE, 'disposable/tree35')
OUT = os.path.join(BASE, 'receipts')
DC = 'docs/coop/design-corrections'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('chk36h', os.path.join(S36, DC, 'foundation/check-atoms.v1.py'))
MODELS = {'frozen35': load('am35h', os.path.join(T35, DC, 'foundation/atom_model.v1.py')), 'final36': K.AM}
R = {'modelSha256': {'frozen35': sha(os.path.join(T35, DC, 'foundation/atom_model.v1.py')), 'final36': sha(os.path.join(S36, DC, 'foundation/atom_model.v1.py'))}}
CHECK = {}


def check(name, cond, observed=None):
    CHECK[name] = {'passed': bool(cond), 'observed': observed}
    print('%-84s %s' % (name, 'PASS' if cond else 'FAIL'), flush=True)


REG36 = json.load(open(os.path.join(S36, DC, 'foundation/evaluator-projection-registry.v1.json')))
REG35 = json.load(open(os.path.join(T35, DC, 'foundation/evaluator-projection-registry.v1.json')))
R['historySubjectOrder'] = {'35': REG35['historySubjectOrder'], '36': REG36['historySubjectOrder']}


def find_path(o, key, path='$'):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                out.append((path + '.' + k, v))
            out.extend(find_path(v, key, path + '.' + k))
    elif isinstance(o, list):
        for n, v in enumerate(o):
            out.extend(find_path(v, key, '%s[%d]' % (path, n)))
    return out


R['importQuantifiers'] = {'35': find_path(REG35, 'importQuantifiers'), '36': find_path(REG36, 'importQuantifiers')}


def flat(o, p='$'):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flat(v, p + '.' + k)
    elif isinstance(o, list):
        for n, v in enumerate(o):
            yield from flat(v, '%s[%d]' % (p, n))
    else:
        yield p, o


f35, f36 = dict(flat(REG35)), dict(flat(REG36))
R['registryJsonPathDelta'] = {'removed': sorted(set(f35) - set(f36)), 'added': sorted(set(f36) - set(f35)),
                              'changed': sorted(p for p in f35 if p in f36 and f35[p] != f36[p])}
print('registry delta 35->36:', R['registryJsonPathDelta'], flush=True)
hso = REG36['historySubjectOrder']
check('H0-registry-delta-is-exactly-the-two-texts-and-history-uniqueKey-removed',
      R['registryJsonPathDelta']['removed'] == ['$.historySubjectOrder.uniqueKey'] and R['registryJsonPathDelta']['added'] == ['$.historySubjectOrder.duplicatePaths']
      and len(R['registryJsonPathDelta']['changed']) == 2 and all(('historySubjectOrder.order' in p or 'observabilityFilter' in p) for p in R['registryJsonPathDelta']['changed']),
      R['registryJsonPathDelta'])
check('H1-historySubjectOrder-no-uniqueness-producer-sequence-no-pick-rule-repair-refusal-kept',
      'uniqueKey' not in hso and hso.get('order') == 'existing sequence (producer order)' and 'retain every matching row at its original ordinal' in hso.get('duplicatePaths', '')
      and 'No merge or pick rule' in hso.get('duplicatePaths', '') and 'ambiguity refusal' in hso.get('duplicatePaths', ''), hso)
consumers = {}
for d, _, fs in os.walk(os.path.join(S36, 'docs')):
    for fn in fs:
        if not fn.endswith(('.py', '.json', '.md')):
            continue
        p = os.path.join(d, fn)
        if '/reviews/' in p:
            continue
        try:
            t = open(p, encoding='utf-8').read()
        except Exception:  # noqa: BLE001
            continue
        for key in ('historySubjectOrder', 'observabilityFilter', 'strict unique path', 'HISTORY_SUBJECT_SEQUENCE_ORDINALS'):
            if key in t:
                consumers.setdefault(key, []).append(os.path.relpath(p, S36))
R['textConsumers'] = consumers
print('text consumers:', consumers, flush=True)
check('H2-no-owner-still-says-strict-unique-path; historySubjectOrder consumed only by registry/contract text',
      'strict unique path' not in consumers and set(consumers.get('historySubjectOrder', [])) <= {DC + '/foundation/evaluator-projection-registry.v1.json', DC + '/foundation/atom-evaluation-contract.v1.md'},
      consumers)
schema = json.load(open(os.path.join(S36, DC, 'workflows/schemas/imported-evidence.schema.json')))
sd = schema['$defs']['HistoryPayloadV1']['properties']['subjects']
R['schemaSubjects'] = {k: sd.get(k) for k in ('x-opensip-order', 'uniqueItems', 'minItems', 'maxItems')}
tsp = [(p, v) for p, v in flat(schema) if 'targetSubjectProjection' in p or (isinstance(v, str) and 'targetSubjectProjection' in v)]
R['repairProjection'] = [(p, v[:600] if isinstance(v, str) else v) for p, v in tsp][:12]
amb = [p for p, v in flat(schema) if isinstance(v, str) and re.search(r'(?i)ambigu', v) and ('subject' in v.lower())]
R['ambiguityRefusalTextPaths'] = amb[:12]
check('H3-repair-targetSubjectProjection-ambiguity-refusal-still-published', bool(tsp) and bool(amb), {'projectionPaths': [p for p, _ in tsp][:6], 'ambiguity': amb[:6]})
from jsonschema import Draft202012Validator  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
dup_payload = {'payloadDomain': 'workflow.import-payload.history.v1', 'vcsSystem': 'git',
               'revisionRange': {'from': None, 'to': 'b' * 40, 'commitCount': 3, 'truncated': False}, 'collectionScope': 'all-paths',
               'subjects': [{'path': 'src/z.ts', 'changeCount': 1, 'lastChangedCommit': 'a' * 40},
                            {'path': 'src/a.ts', 'changeCount': 1, 'lastChangedCommit': 'a' * 40},
                            {'path': 'src/a.ts', 'changeCount': 2, 'lastChangedCommit': 'c' * 40}]}
res = []
for fn in ('common.schema.json', 'imported-evidence.schema.json'):
    doc = json.load(open(os.path.join(S36, DC, 'workflows/schemas', fn)))
    if '$id' in doc:
        res.append((doc['$id'], Resource.from_contents(doc)))
v = Draft202012Validator({'$ref': schema['$id'] + '#/$defs/HistoryPayloadV1'}, registry=Registry().with_resources(res))
errs = sorted(e.message[:160] for e in v.iter_errors(dup_payload))
R['H4-schema'] = {'errors': errs, 'admitted': not errs}
check('H4-stock-schema-admits-duplicate-paths-in-non-sorted-producer-order', not errs and R['schemaSubjects'].get('uniqueItems') in (None, False)
      and R['schemaSubjects'].get('x-opensip-order') == 'sequence', {'errors': errs, 'subjects': R['schemaSubjects']})


def ev(mod, atom, subj, inputs):
    try:
        r = mod.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj), copy.deepcopy(inputs))
    except mod.AtomAdmissionError as e:
        return {'value': 'REFUSE:' + e.key}
    return {'value': r['value'], 'known': [a['ordinal'] for a in r['knownObservationAddresses']],
            'uncertain': [a['ordinal'] for a in r['uncertainObservationAddresses']], 'causes': sorted({c['code'] for c in r['causes']})}


def hist_inputs(subjects):
    iid = K.imp2('3')
    return K.base_inputs(enumerationPlan=K.plan_one(cap='inventory', kinds=['file']), inventories=[K.inv_file()],
                         planSelectedImportIds=[iid], evaluationInputRefs=[iid], imports={iid: K.wrap('history')},
                         importPayloads={iid: {'collectionScope': 'all-paths', 'subjects': subjects,
                                               'revisionRange': {'from': None, 'to': 'b' * 40, 'commitCount': 3, 'truncated': False}}},
                         importObservations={iid: {'window': None, 'population': None, 'selection': None, 'revisionRange': {'from': None, 'to': 'b' * 40}}})


FILE = {'universe': K.U1, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'}
HA = {'relation': 'history-change', 'minResolution': 'observed', 'filters': [], 'evidence': 'history'}
HOPS = (('exists', {'op': 'exists'}), ('none', {'op': 'none'}), ('count<=1', {'op': 'count-at-most', 'n': 1}),
        ('count<=2', {'op': 'count-at-most', 'n': 2}), ('all-covered', {'op': 'all-covered'}))
H5 = {m: {l: ev(mod, dict(HA, **o), FILE, hist_inputs(dup_payload['subjects'])) for l, o in HOPS} for m, mod in MODELS.items()}
R['H5-history'] = H5
print('H5 history', {m: {l: [x['value'], x.get('known')] for l, x in H5[m].items()} for m in H5}, flush=True)
check('H5-atom-retains-every-duplicate-ordinal-identically-on-frozen35-and-final36', H5['frozen35'] == H5['final36']
      and H5['final36']['exists']['known'] == [1, 2] and H5['final36']['count<=1']['value'] == 'false' and H5['final36']['count<=2']['value'] == 'true')

RT = {'relation': 'runtime-observation', 'minResolution': 'observed', 'evidence': 'runtime'}
SYM = {'universe': K.U1, 'kind': 'symbol', 'nativeSubjectId': 'ts-symbol:src/a.ts#f'}


def rt_inputs(rows):
    iid = K.imp2('1')
    return K.base_inputs(planSelectedImportIds=[iid], imports={iid: K.wrap('runtime')}, importPayloads={iid: K.rt_payload(rows)}, importObservations={iid: K.rt_obs()})


row = lambda obs, sym='f', hits=0: {'path': 'src/a.ts', 'symbol': sym, 'observability': obs, 'hits': hits}
FILTERS = {'unfiltered': [], 'eq observed-hit': [{'field': 'observability', 'cmp': 'eq', 'value': 'observed-hit'}],
           'eq observable-unhit': [{'field': 'observability', 'cmp': 'eq', 'value': 'observable-unhit'}],
           'eq unobservable': [{'field': 'observability', 'cmp': 'eq', 'value': 'unobservable'}],
           'eq unmapped': [{'field': 'observability', 'cmp': 'eq', 'value': 'unmapped'}],
           'neq observed-hit': [{'field': 'observability', 'cmp': 'neq', 'value': 'observed-hit'}]}
ROWSETS = {'observed-hit': [row('observed-hit', hits=3)], 'observable-unhit': [row('observable-unhit')], 'unobservable': [row('unobservable')],
           'unmapped': [row('unmapped')], 'unhit+unobservable': [row('observable-unhit'), row('unobservable')],
           'unobservable-other-subject-only': [row('unobservable', sym='g')]}
RQ = {}
for m, mod in MODELS.items():
    RQ[m] = {rs: {fl: {op: ev(mod, dict(RT, op=op, filters=flt), SYM, rt_inputs(rows)) for op in ('exists', 'none', 'all-covered')}
                  for fl, flt in FILTERS.items()} for rs, rows in ROWSETS.items()}
R['R-matrix'] = RQ
for rs in ROWSETS:
    print('R %-32s' % rs, {fl: [RQ['final36'][rs][fl][op]['value'] for op in ('exists', 'none', 'all-covered')] for fl in FILTERS}, flush=True)
q = RQ['final36']
check('R0-runtime-atom-behaviour-identical-frozen35-and-final36', RQ['frozen35'] == RQ['final36'])
check('R1-unfiltered-exists-true-on-observed-hit-and-on-observable-unhit', q['observed-hit']['unfiltered']['exists']['value'] == q['observable-unhit']['unfiltered']['exists']['value'] == 'true')
check('R2-observability-filter-restricts-polarity', q['observable-unhit']['eq observed-hit']['exists']['value'] == 'false' and q['observable-unhit']['eq observed-hit']['none']['value'] == 'true'
      and q['observed-hit']['eq observable-unhit']['exists']['value'] == 'false' and q['observed-hit']['eq observed-hit']['exists']['value'] == 'true')
check('R3-unobservable-and-unmapped-never-enter-R-never-make-exists-or-none-true', all(q[rs][fl][op]['value'] != 'true' for rs in ('unobservable', 'unmapped') for fl in FILTERS for op in ('exists', 'none', 'all-covered')))
check('R4-filter-naming-unobservable-or-unmapped-is-admitted-and-matches-nothing', all(not q[rs]['eq ' + rs]['exists']['value'].startswith('REFUSE') and q[rs]['eq ' + rs]['exists']['known'] == [] for rs in ('unobservable', 'unmapped')))
check('R5-relevant-unobservable-disclosed-uncertain-with-cause-under-every-filter', all(q['unobservable'][fl]['exists']['uncertain'] == [0] and 'unobservable-subject' in q['unobservable'][fl]['exists']['causes'] for fl in FILTERS)
      and all(q['unmapped'][fl]['exists']['uncertain'] == [0] and 'unmapped-subject' in q['unmapped'][fl]['exists']['causes'] for fl in FILTERS))
check('R6-non-matching-subject-unobservable-row-is-not-disclosed (relevance = subject occupancy)', all(q['unobservable-other-subject-only'][fl]['exists']['uncertain'] == [] for fl in FILTERS),
      {fl: q['unobservable-other-subject-only'][fl]['exists'] for fl in FILTERS})
check('R7-mixed-unhit-plus-unobservable: unhit row decides exists, unobservable still disclosed', q['unhit+unobservable']['unfiltered']['exists']['value'] == 'true'
      and 1 in q['unhit+unobservable']['unfiltered']['exists']['uncertain'], q['unhit+unobservable']['unfiltered'])
contract = open(os.path.join(S36, DC, 'foundation/atom-evaluation-contract.v1.md')).read()
para = next((l for l in contract.splitlines() if l.startswith('**Runtime polarity:**')), '')
R['contractRuntimePolarity'] = para
check('R8-contract-runtime-polarity-paragraph-states-exactly-the-measured-law', all(s in para for s in (
    'either `observed-hit` or `observable-unhit` can satisfy it', 'restricts the matching polarity set', 'unobservable and unmapped rows never enter that set',
    'disclosed as uncertain independently of that filter', 'an unhit observation is not an execution hit')), para)
R['checks'] = CHECK
R['failedChecks'] = sorted(k for k, v in CHECK.items() if not v['passed'])
print('\nchecks %d failed %s' % (len(CHECK), R['failedChecks']))
json.dump(R, open(os.path.join(OUT, 'p03-history-runtime36.json'), 'w'), indent=1, default=str)
print('wrote p03-history-runtime36.json')

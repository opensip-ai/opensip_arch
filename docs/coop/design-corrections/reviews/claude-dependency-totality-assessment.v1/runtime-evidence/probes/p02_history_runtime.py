"""P02 — root's two proposed text corrections, tested AFTER law-derivation-history-runtime.json.
Frozen35 atom API with frozen35 check-atoms builders; stock jsonschema over the payload owner schema.
STANDING: atom-api synthetic + stock schema; static owner text reads are labelled."""
import copy, hashlib, importlib.util, json, os, sys

F35 = '/tmp/opensip-design-corrections/candidate-subject.v35/docs/coop/design-corrections'
OUT = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1/receipts'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('chk35', F35 + '/foundation/check-atoms.v1.py')
AM = K.AM
R = {'atomModelSha256': hashlib.sha256(open(F35 + '/foundation/atom_model.v1.py', 'rb').read()).hexdigest()}


def ev(atom, subj, inputs):
    try:
        r = AM.evaluate_atom(copy.deepcopy(atom), copy.deepcopy(subj), copy.deepcopy(inputs))
    except AM.AtomAdmissionError as e:
        return {'admission': 'REFUSE', 'key': e.key}
    return {'value': r['value'], 'known': [a['ordinal'] for a in r['knownObservationAddresses']],
            'uncertain': [a['ordinal'] for a in r['uncertainObservationAddresses']], 'causes': sorted({c['code'] for c in r['causes']})}


# ---------------- history
REG = json.load(open(F35 + '/foundation/evaluator-projection-registry.v1.json'))
R['registryHistorySubjectOrder'] = REG['historySubjectOrder']
def find_key_row(o, key):
    if isinstance(o, dict):
        if o.get('key') == key:
            return o
        for v in o.values():
            hit = find_key_row(v, key)
            if hit:
                return hit
    elif isinstance(o, list):
        for v in o:
            hit = find_key_row(v, key)
            if hit:
                return hit
    return None


R['registryOrdinalRow'] = find_key_row(REG, 'HISTORY_SUBJECT_SEQUENCE_ORDINALS')
R['registryRuntimeDuplicateRow'] = find_key_row(REG, 'RUNTIME_SUBJECT_DUPLICATE_KEY')
print('registry historySubjectOrder:', R['registryHistorySubjectOrder'], '| ordinal row:', R['registryOrdinalRow'])
schema = json.load(open(F35 + '/workflows/schemas/imported-evidence.schema.json'))
subj_def = schema['$defs']['HistoryPayloadV1']['properties']['subjects']
R['schemaSubjects'] = {k: subj_def.get(k) for k in ('x-opensip-order', 'uniqueItems', 'minItems', 'maxItems')}
from jsonschema import Draft202012Validator  # noqa: E402
dup_payload = {'payloadDomain': 'workflow.import-payload.history.v1', 'vcsSystem': 'git',
               'revisionRange': {'from': None, 'to': 'b' * 40, 'commitCount': 3, 'truncated': False}, 'collectionScope': 'all-paths',
               'subjects': [{'path': 'src/z.ts', 'changeCount': 1, 'lastChangedCommit': 'a' * 40},
                            {'path': 'src/a.ts', 'changeCount': 1, 'lastChangedCommit': 'a' * 40},
                            {'path': 'src/a.ts', 'changeCount': 2, 'lastChangedCommit': 'c' * 40}]}
try:
    from referencing import Registry, Resource  # noqa: E402
    res = []
    for fn in ('common.schema.json', 'imported-evidence.schema.json'):
        doc = json.load(open(F35 + '/workflows/schemas/' + fn))
        if '$id' in doc:
            res.append((doc['$id'], Resource.from_contents(doc)))
    reg = Registry().with_resources(res)
    v = Draft202012Validator({'$ref': schema['$id'] + '#/$defs/HistoryPayloadV1'}, registry=reg)
    errs = sorted(e.message[:160] for e in v.iter_errors(dup_payload))
    R['H1-schemaAdmitsDuplicateAndNonUtf8OrderedPaths'] = {'errors': errs, 'admitted': not errs, 'method': 'stock jsonschema with local $id registry'}
except Exception as ex:  # noqa: BLE001
    errs = ['VALIDATOR SETUP FAILED: %s: %s' % (type(ex).__name__, str(ex)[:200])]
    R['H1-schemaAdmitsDuplicateAndNonUtf8OrderedPaths'] = {'errors': errs, 'admitted': None,
                                                           'staticRead': R['schemaSubjects']}
print('H1 schema admits duplicate paths in non-UTF-8 producer order:', R['H1-schemaAdmitsDuplicateAndNonUtf8OrderedPaths'].get('admitted'), errs[:2])


def hist_inputs(subjects):
    iid = K.imp2('3')
    return K.base_inputs(enumerationPlan=K.plan_one(cap='inventory', kinds=['file']), inventories=[K.inv_file()],
                         planSelectedImportIds=[iid], evaluationInputRefs=[iid], imports={iid: K.wrap('history')},
                         importPayloads={iid: {'collectionScope': 'all-paths', 'subjects': subjects,
                                               'revisionRange': {'from': None, 'to': 'b' * 40, 'commitCount': 3, 'truncated': False}}},
                         importObservations={iid: {'window': None, 'population': None, 'selection': None,
                                                   'revisionRange': {'from': None, 'to': 'b' * 40}}})


FILE = {'universe': K.U1, 'kind': 'file', 'nativeSubjectId': 'src/a.ts'}
H = {'relation': 'history-change', 'minResolution': 'observed', 'filters': [], 'evidence': 'history'}
inp = hist_inputs(dup_payload['subjects'])
H2 = {label: ev(dict(H, **over), FILE, inp) for label, over in (('exists', {'op': 'exists'}), ('none', {'op': 'none'}),
                                                               ('count<=1', {'op': 'count-at-most', 'n': 1}), ('count<=2', {'op': 'count-at-most', 'n': 2}),
                                                               ('all-covered', {'op': 'all-covered'}))}
R['H2-atomRetainsEveryDuplicateOrdinalInProducerOrder'] = H2
print('H2 duplicate path at ordinals 1 and 2 (non-sorted producer order):', {k: [x.get('value'), x.get('known')] for k, x in H2.items()})
R['H2-pass'] = (H2['exists']['value'] == 'true' and H2['exists']['known'] == [1, 2] and H2['none']['value'] == 'false'
                and H2['count<=1']['value'] == 'false' and H2['count<=2']['value'] == 'true' and H2['all-covered']['value'] == 'true')
R['H3-runtimeContrastDuplicateKeyRefusal'] = {'runtimeUniqueKey': REG['runtimeSubjectOrder']['uniqueKey'],
                                              'historyRegistryClaimsUnique': REG['historySubjectOrder'].get('uniqueKey')}

# ---------------- runtime quantifiers
RT = {'relation': 'runtime-observation', 'minResolution': 'observed', 'evidence': 'runtime'}
SYM = {'universe': K.U1, 'kind': 'symbol', 'nativeSubjectId': 'ts-symbol:src/a.ts#f'}


def rt_inputs(obs, hits=0):
    iid = K.imp2('1')
    row = {'path': 'src/a.ts', 'symbol': 'f', 'observability': obs, 'hits': hits}
    return K.base_inputs(planSelectedImportIds=[iid], imports={iid: K.wrap('runtime')},
                         importPayloads={iid: K.rt_payload([row])}, importObservations={iid: K.rt_obs()})


RQ = {}
for obs, hits in (('observed-hit', 3), ('observable-unhit', 0), ('unobservable', 0), ('unmapped', 0)):
    inp = rt_inputs(obs, hits)
    RQ[obs] = {}
    for flabel, flt in (('unfiltered', []), ('filter=observed-hit', [{'field': 'observability', 'cmp': 'eq', 'value': 'observed-hit'}]),
                        ('filter=observable-unhit', [{'field': 'observability', 'cmp': 'eq', 'value': 'observable-unhit'}]),
                        ('filter=' + obs, [{'field': 'observability', 'cmp': 'eq', 'value': obs}])):
        RQ[obs][flabel] = {op: ev(dict(RT, op=op, filters=flt), SYM, inp) for op in ('exists', 'none', 'all-covered')}
R['R-runtimeMatrix'] = RQ
for obs in RQ:
    print('R %-17s' % obs, {f: {op: x.get('value', x.get('key')) for op, x in d.items()} for f, d in RQ[obs].items()})
checks = {
    'unfilteredExistsTrueOnObservedHit': RQ['observed-hit']['unfiltered']['exists']['value'] == 'true',
    'unfilteredExistsTrueOnObservableUnhit': RQ['observable-unhit']['unfiltered']['exists']['value'] == 'true',
    'filterObservedHitRestrictsPolarity': RQ['observable-unhit']['filter=observed-hit']['exists']['value'] == 'false'
                                          and RQ['observable-unhit']['filter=observed-hit']['none']['value'] == 'true',
    'filterObservableUnhitRestrictsPolarity': RQ['observed-hit']['filter=observable-unhit']['exists']['value'] == 'false',
    'unobservableNeverInR': all(RQ['unobservable'][f]['exists']['value'] != 'true' and RQ['unobservable'][f]['none']['value'] != 'true'
                                for f in RQ['unobservable']),
    'unmappedNeverInR': all(RQ['unmapped'][f]['exists']['value'] != 'true' and RQ['unmapped'][f]['none']['value'] != 'true' for f in RQ['unmapped']),
    'filterNamingUnobservableIsAdmittedButMatchesNothing': RQ['unobservable']['filter=unobservable']['exists'].get('admission') != 'REFUSE'
                                                           and RQ['unobservable']['filter=unobservable']['exists']['known'] == [],
    'disclosureOfUnobservableIsUnconditional': RQ['unobservable']['unfiltered']['exists']['uncertain'] == [0]
                                               and RQ['unobservable']['filter=observed-hit']['exists']['uncertain'] == [0],
}
R['R-checks'] = checks
print('runtime checks:', checks)
json.dump(R, open(os.path.join(OUT, 'p02-history-runtime.json'), 'w'), indent=1, default=str)
print('wrote p02-history-runtime.json')

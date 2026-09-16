"""Run-termination source40 prose clarifications against the unchanged model/schema, an independent commit-inventory recompute
over a real closed Run, ADV39-01 registered-schema account, and the internal-key/public-code boundary.
Writes only receipts/probes/runterm-adv-v40-on43.json."""
import contextlib, hashlib, importlib.util, io, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
DC = RT / 'work/source43-pkg/docs/coop/design-corrections'
S38 = Path('/tmp/opensip-design-corrections/candidate-subject.v38/docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
S39 = Path('/tmp/opensip-design-corrections/candidate-subject.v39/docs/coop/design-corrections')
OUT = RT / 'receipts/probes/runterm-adv-v40-on43.json'
ROWS = []


def row(case, ok, observed=None, expected=None, kind=None):
    r = {'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    if kind:
        r['kind'] = kind
    ROWS.append(r)


def C(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def refusal(fn):
    try:
        fn()
        return None
    except Exception as exc:  # noqa: BLE001
        return str(exc)


def termination():
    T = load('rt40_model', DC / 'foundation/run_termination_model.v1.py')
    row('closed-candidate-comparison-fields-equal-section-6-step-2', set(T.PROJECTION_FIELDS) == {'class', 'runId', 'reasonCodes', 'coverageId', 'errorCode', 'faultCause', 'signal'},
        list(T.PROJECTION_FIELDS))
    row('delegated-members-equal-section-1-table', set(T.DELEGATED_FIELDS) == {'executionId', 'domainDetail', 'authority'}, sorted(T.DELEGATED_FIELDS))
    derived = {'class': 'indeterminate', 'runId': 'run3:' + 'a' * 64, 'reasonCodes': ['VERDICT.INDETERMINATE']}
    cases = {
        'non-object-candidate': ([derived], 'RUN_TERMINATION_CANDIDATE_NOT_OBJECT'),
        'unknown-member': (dict(derived, bogus=1), 'RUN_TERMINATION_UNKNOWN_FIELD'),
        'errorCode-reaches-not-derived': (dict(derived, errorCode='HOST.IO_FAILURE'), 'RUN_TERMINATION_NOT_DERIVED'),
        'faultCause-reaches-not-derived': (dict(derived, faultCause='host-io'), 'RUN_TERMINATION_NOT_DERIVED'),
        'signal-reaches-not-derived': (dict(derived, signal='SIGINT'), 'RUN_TERMINATION_NOT_DERIVED'),
        'unknown-member-precedes-forbidden-class-field': (dict(derived, bogus=1, errorCode='HOST.IO_FAILURE'), 'RUN_TERMINATION_UNKNOWN_FIELD'),
    }
    for name, (cand, key) in cases.items():
        got = refusal(lambda c=cand: T.check_projection(c, derived))
        row('check_projection-' + name, got is not None and got.split(':')[0] == key, got, key)
    got = refusal(lambda: T.check_projection(dict(derived), derived))
    row('check_projection-exact-derived-admits', got is None, got)
    text = (DC / 'foundation/run_termination_model.v1.py').read_text()
    row('unexplained-indeterminate-keys-are-the-model-keys (source text)', '"RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RULE:" + result["ruleId"]' in text
        and '"RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RUN"' in text, None, None, 'source-text')
    row('run-termination-model-and-schemas-unchanged-39-to-40',
        all(hashlib.sha256((DC / p).read_bytes()).hexdigest() == hashlib.sha256((S39 / p).read_bytes()).hexdigest()
            for p in ('foundation/run_termination_model.v1.py', 'foundation/identity-schemas.v3.json', 'foundation/identity-model.v3.py',
                      'workflows/schemas/evaluator3/common.schema.json', 'public-detail-registry.v1.json')))


def inventory():
    SR = load('rt40_semantic_replay', DC / 'foundation/check-semantic-replay.v3.py')
    M = SR.M
    _, (run, objects, blobs), _ = SR.case_incoming_known_hit()
    run_id = M.close_run(run, objects, blobs)
    # Attempt 1 of this probe assumed commit_inventory returns a digest; it returns (record, raw SHA-256 of C(record)).
    record = {'schemaVersion': 2, 'runId': run_id, 'objects': sorted(objects, key=C), 'blobDigests': sorted(blobs, key=C)}
    mine = hashlib.sha256(C(record)).hexdigest()
    owner_record, owner = M.commit_inventory(run_id, objects, blobs)
    row('commit-inventory-independent-recipe-equals-owner-over-a-closed-run', mine == owner and C(owner_record) == C(record),
        {'runId': run_id, 'objects': len(objects), 'blobs': len(blobs), 'digest': owner, 'mine': mine})
    row('commit-inventory-objects-are-the-typed-object-keys-and-blobs-the-raw-blob-keys',
        set(owner_record['objects']) == set(objects) and set(owner_record['blobDigests']) == set(blobs)
        and all(':' in k for k in owner_record['objects']) and all(':' not in k and len(k) == 64 for k in owner_record['blobDigests']))
    import copy as _copy
    schema = _copy.deepcopy(M.SCHEMA)
    schema['$ref'] = '#/$defs/commit-inventory'
    try:
        M.C.validate(schema, record)
        valid = True
    except Exception as exc:  # noqa: BLE001
        valid = type(exc).__name__ + ':' + str(exc)[:160]
    row('commit-inventory-record-validates-against-the-owning-schema (canonical-set orders)', valid is True, valid)
    shuffled = dict(record, objects=list(reversed(record['objects'])))
    try:
        M.C.validate(schema, shuffled)
        M.ordered(shuffled)
        order_refused = False
    except Exception:  # noqa: BLE001
        order_refused = True
    row('a-non-canonical-set-object-order-refuses', order_refused)
    extra = dict(objects)
    extra['finding3:' + 'f' * 64] = ('finding', {'schemaVersion': 3})
    row('an-extra-unpublished-object-changes-the-inventory-digest', M.commit_inventory(run_id, extra, blobs)[1] != owner)


def adv3901():
    NEWB = (DC / 'native/native-evidence.schemas.v2.json').read_bytes()
    OLDB = (S39 / 'native/native-evidence.schemas.v2.json').read_bytes()
    B38 = S38.read_bytes()
    row('registered-native-schema-bytes-unchanged-39-to-40', NEWB == OLDB, hashlib.sha256(NEWB).hexdigest())
    row('source38-and-source40-raw-digests-are-the-ones-section-10-names',
        hashlib.sha256(B38).hexdigest() == '3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0'
        and hashlib.sha256(NEWB).hexdigest() == '2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043')
    j38, j40 = json.loads(B38), json.loads(NEWB)
    path = ['x-opensip-deficiency-cause-registry', 'perRequirementConsumerBoundary', 'threeDistinctThingsNotToConflate', 'publicD9Termination']

    def get(d):
        for k in path:
            d = d[k]
        return d
    row('publicD9Termination-annotation-unchanged-38-to-40', get(j38) == get(j40), str(get(j40))[:160])

    def diff(a, b, p='#'):
        if type(a) is not type(b):
            return [p]
        if isinstance(a, dict):
            return sum((([p + '/' + k] if (k not in a or k not in b) else diff(a[k], b[k], p + '/' + k)) for k in sorted(set(a) | set(b))), [])
        if isinstance(a, list):
            return [p] if len(a) != len(b) else sum((diff(x, y, p + '/' + str(i)) for i, (x, y) in enumerate(zip(a, b))), [])
        return [] if a == b else [p]
    paths = diff(j38, j40)
    row('only-ResolvedNodeModulesLayoutV1-description-differs-38-to-40', paths == ['#/$defs/ResolvedNodeModulesLayoutV1/description'], paths)
    M = load('rt40_identity', DC / 'foundation/identity-model.v3.py')
    reg = M.registered_schema_documents()
    row('registry-registers-the-source39-digest-and-not-the-source38-digest',
        '2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043' in reg and '3e37c7b7a6a620dcadc0aaed862eed242065ebd0ce9910da16faa25464f8b0b0' not in reg)
    rb = json.loads(Path('/tmp/opensip-design-corrections/root-author-package-final40-rebuild.v1/rebuild-report.json').read_text())
    row('rebuilt-reference-exports-consume-the-source39-digest', rb['inputs']['registeredNativeSchemaSha256'] == '2d37b810bd9ffed741d74241fc8a11051606862d8af2f152eed16b92bdc66043')


def public_codes():
    reg = json.loads((DC / 'public-detail-registry.v1.json').read_text())
    codes = set()

    def walk(n):
        if isinstance(n, dict):
            if isinstance(n.get('code'), str):
                codes.add(n['code'])
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(reg)
    internal = ['EVALUATOR_POLICY_UNIVERSE_UNREGISTERED', 'ENUMERATION_MEMBERSHIP_ORDER', 'ENUMERATION_MEMBERSHIP_ROW_DERIVATION', 'RUN_TERMINATION_CANDIDATE_NOT_OBJECT',
                'RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RULE', 'RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_RUN', 'RUN_TERMINATION_UNKNOWN_FIELD', 'RUN_TERMINATION_NOT_DERIVED']
    row('internal-decision-keys-are-not-public-detail-codes', not (set(internal) & codes), {'registryCodes': len(codes), 'leaked': sorted(set(internal) & codes)})
    row('public-detail-registry-unchanged-39-to-40', (DC / 'public-detail-registry.v1.json').read_bytes() == (S39 / 'public-detail-registry.v1.json').read_bytes(), len(codes))


for fn in (termination, inventory, adv3901, public_codes):
    try:
        fn()
    except Exception:  # noqa: BLE001
        row(fn.__name__ + '-crashed', False, traceback.format_exc()[-2000:])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'standing': 'independent reviewer probe; unchanged model and schema against source40 prose; real closed Run for the inventory recipe',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']]}, indent=1, default=str)[:6000])

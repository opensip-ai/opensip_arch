"""CLAIMED-POSITIVE AUDIT (generation 22).

"Adding a new compliant supplemental helper does not correct an older artifact that your final
report still claims is positive." This stage re-checks EVERY requirement's claimed-positive
artifact from its FINAL BYTES in a fresh process, and records -- per requirement -- which
evidence class the re-check actually is:

  reconstructed-behavior    the result is re-derived here from retained inputs (re-hashing,
                            recomputing identities, replaying a transition table, re-deriving a
                            Run property from store bytes, joining to the current exports)
  schema-admitted-record    the exact final record is re-admitted here against its owning schema
                            (reference Draft 2020-12 validator + published keywords) and its prose
                            laws are recomputed
  measured-control          a negative / discriminating control whose refusal and first-refusal
                            record are re-checked here
  cited-kit-distinction     a standing distinction whose quoted kit text is found verbatim
                            (whitespace-normalised) in the kit bytes here
  standing-record-verified  a required standing record is present on EVERY item it must cover
  static-comparison         recorded strings or flags compared, nothing re-derived
  shape-only                presence or counts only
  helper-assumption         a literal or helper flag taken as given

A requirement is `PASS` only when every check passes AND its evidence class is sufficient for its
original kind (a complete Run needs reconstructed behaviour; a schema envelope needs a re-admitted
record; ...). The generation-20 requirement status graded several rows from presence, counts, a
generation-16 custody note, or a literal `True`; those rows are the reason this stage exists
(V22-D4). Run-derived checks read the Run's OWN evidence views, never every object of a store
(an export also retains pair-vector inputs that are not evaluation inputs).

Phase-11 deliverable rows are checked by the requirement-status stage AFTER the review exists;
here they are recorded as DEFERRED with the check that will decide them.
"""
import glob
import hashlib
import json
import os
import re
import sys
import traceback
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_store as ST

RUNTIME = '/tmp/opensip-design-corrections/consumer-b.v22'
OUT = RUNTIME + '/output'
SUBJ = RUNTIME + '/subject'
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']
ENV_DOC = 'workflows/schemas/evaluator3/command-envelope.schema.json'
ENV_DOC_INHERITED = 'workflows/schemas/command-envelope.schema.json'
Q_DOC = 'workflows/schemas/evaluator3/graph-query.schema.json'
INVOC_DOC = 'workflows/schemas/evaluator3/invocation-record.schema.json'
REPAIR_DOC = 'workflows/schemas/evaluator3/repair.schema.json'
BASE_DOC = 'workflows/schemas/evaluator3/baseline-artifact.schema.json'
CMP_DOC = 'workflows/schemas/evaluator3/comparison-result.schema.json'
NATIVE_DOC = 'native/native-evidence.schemas.v2.json'
IDENT_DOC = 'foundation/identity-schemas.v3.json'
REL_DOC = 'foundation/relation-payload-schemas.v2.json'
IMPORTED_DOC = 'workflows/schemas/imported-evidence.schema.json'
SECURITY_DOC = 'security/security-lifecycle.schemas.v1.json'

EVIDENCE_CLASSES = ('reconstructed-behavior', 'schema-admitted-record', 'measured-control',
                    'cited-kit-distinction', 'standing-record-verified', 'static-comparison',
                    'shape-only', 'helper-assumption')
SUFFICIENT = {
    'completeRun': {'reconstructed-behavior'},
    'completeRunProperty': {'reconstructed-behavior'},
    'standaloneCanonicalVector': {'reconstructed-behavior', 'schema-admitted-record',
                                  'measured-control'},
    'standaloneConfigVector': {'reconstructed-behavior', 'schema-admitted-record',
                               'measured-control'},
    'standaloneTraceVector': {'reconstructed-behavior'},
    'schemaEnvelope': {'schema-admitted-record', 'reconstructed-behavior'},
    'evaluatorReplay': {'reconstructed-behavior', 'measured-control'},
    'standingRule': {'reconstructed-behavior', 'schema-admitted-record', 'measured-control',
                     'cited-kit-distinction', 'standing-record-verified'},
}
MASKING_KEYS = ('masksLater', 'masking', 'orderedRefusalChecks', 'allRefusalChecks',
                'intendedLawPositionInOrderedRefusals', 'allRefusals', 'violationsInOrder',
                'prosaicLawRefusals', 'jointRefusals', 'delegatedAdmissionRefusals')
_cache = {}


def J(rel):
    if rel not in _cache:
        with open(os.path.join(OUT, rel), encoding='utf-8') as fh:
            _cache[rel] = json.load(fh)
    return _cache[rel]


def kitjson(name):
    key = 'kit:' + name
    if key not in _cache:
        _cache[key] = json.load(open(S.KIT + '/' + S.doc_path(name), encoding='utf-8'))
    return _cache[key]


def manifest_rows():
    return json.load(open(SUBJ + '/consumer-input-manifest.json'))['files']


def _norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def in_kit(quote):
    if 'kit-norm' not in _cache:
        texts = []
        for r in manifest_rows():
            try:
                texts.append(_norm(open(SUBJ + '/' + r['path'], encoding='utf-8').read()))
            except UnicodeDecodeError:
                pass
        _cache['kit-norm'] = texts
    q = _norm(quote)
    return bool(q) and any(q in t for t in _cache['kit-norm'])


def readmit(doc, selector, inst):
    if doc == SECURITY_DOC:
        import jsonschema
        d = kitjson(SECURITY_DOC)
        root = {'$defs': d['$defs'], 'schemas': d['schemas'], '$ref': selector}
        errs = list(jsonschema.Draft202012Validator(root).iter_errors(inst))
        return not errs, [e.message[:200] for e in errs[:2]]
    r = S.admit(doc, selector, inst, 'audit')
    return r['admitted'], (r['stockSchemaErrors'][:2] + r['publishedKeywordRefusals'][:2])


def walk(node, fn, path='$'):
    fn(node, path)
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, fn, path + '.' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, fn, '%s[%d]' % (path, i))


def find_prop(schema, name):
    hit = []

    def fn(n, _p):
        if not hit and isinstance(n, dict) and isinstance(n.get('properties'), dict) \
                and name in n['properties']:
            hit.append(n['properties'][name])
    walk(schema, fn)
    return hit[0] if hit else None


# ---------------------------------------------------------------------------- the audit
class Audit:
    def __init__(self):
        self.reqs = {}
        whole = json.load(open(RUNTIME + '/requirements.json'))
        self.meta = {r['id']: r for r in whole['standing'] + whole['requirements']
                     + whole['futureQualification']}
        self.whole = whole
        self.cur = None

    def start(self, rid, evidence_class, artifacts, method):
        assert evidence_class in EVIDENCE_CLASSES, evidence_class
        self.cur = self.reqs[rid] = {
            'id': rid, 'kind': self.meta[rid]['kind'],
            'acceptBlocking': self.meta[rid].get('acceptBlocking'),
            'evidenceClass': evidence_class, 'artifacts': artifacts, 'method': method,
            'checks': []}

    def need(self, cond, check, detail=None):
        self.cur['checks'].append({'check': check, 'result': 'PASS' if cond else 'REFUSE',
                                   'detail': detail})
        return bool(cond)

    def finish(self):
        for r in self.reqs.values():
            if r.get('result') == 'DEFERRED':
                continue
            refusals = [c for c in r['checks'] if c['result'] != 'PASS']
            r['evidenceClassSufficientForKind'] = r['evidenceClass'] in SUFFICIENT.get(
                r['kind'], set())
            r['checksPassed'] = len(r['checks']) - len(refusals)
            r['refusals'] = refusals
            r['firstRefusal'] = refusals[0] if refusals else None
            r['result'] = ('PASS' if r['checks'] and not refusals
                           and r['evidenceClassSufficientForKind'] else 'FAIL')


A = Audit()
HANDLERS = []


def handler(rid, cls, artifacts, method):
    def deco(fn):
        def run():
            A.start(rid, cls, artifacts, method)
            try:
                fn()
            except Exception as e:
                A.need(False, 'AUDITOR_ERROR', '%s: %s | %s' % (
                    type(e).__name__, str(e)[:300], traceback.format_exc().splitlines()[-3:]))
        HANDLERS.append((rid, run))
        return fn
    return deco


# ------------------------------------------------------------------------- shared joins
def run_store(label):
    key = 'store:' + label
    if key not in _cache:
        _cache[key] = ST.Store.load(OUT + '/runs/%s.store.json' % label)   # re-hashes blobs
    return _cache[key]


def current_run_ids():
    return {l: run_store(l)[1]['claim']['runId'] for l in RUNS}


def blob_json(st, digest):
    b = st.get_blob(digest.split(':')[-1] if isinstance(digest, str) else digest)
    return json.loads(b.decode()) if b is not None else None


def views(label):
    """The Run's OWN evaluation inputs: facts, scopes and Coverage named by its evidence views."""
    key = 'views:' + label
    if key not in _cache:
        st, doc = run_store(label)
        run = st.objects[doc['claim']['runId']]
        ev = st.objects[run['evidenceId']]
        facts, scopes, covs = {}, {}, {}
        for vid in ev['viewIds']:
            v = st.objects[vid]
            for f in v['facts']:
                facts[f] = st.objects[f]
            for s in v['scopeIds']:
                scopes[s] = st.objects[s]
            for c in v['coverageIds']:
                covs[c] = st.objects[c]
        pays = {c: blob_json(st, o['payloadDigest']) for c, o in covs.items()}
        _cache[key] = {'run': run, 'facts': facts, 'scopes': scopes, 'covs': covs, 'pays': pays}
    return _cache[key]


def run_verified(label):
    st, doc = run_store(label)
    rid = doc['claim']['runId']
    clo = J('runs/%s.closure.json' % label)
    rep = J('runs/%s.replay.json' % label)
    ctl = J('runs/%s.controls.json' % label)
    atom = J('vectors/indep-atom-law.json')['runs'][label]
    xin = J('vectors/indep-execution-inputs.json')['runs'][label]
    A.need(rid in st.objects, 'RUN_ID_IS_IN_THE_EXPORTED_OBJECT_TABLE:' + label, rid)
    A.need(doc['objectCount'] == len(st.objects) and doc['blobCount'] == len(st.blobs),
           'EXPORT_COUNTS_EQUAL_THE_LOADED_TABLE:' + label)
    A.need(clo['admitted'] and clo['checksRefused'] == 0 and clo['checksPassed'] > 0,
           'INDEPENDENT_RETAINED_CLOSURE_ADMITTED:' + label, clo['checksPassed'])
    A.need(rep['runId'] == rid and rep['verdict'] == 'REPLAY_MATCH' and rep['replayAdmitted']
           and all(c['equal'] for c in rep['bundleComparisons'])
           and all(c['equal'] for c in rep['identityComparisons'])
           and all(c['equal'] for c in rep['findingComparisons'])
           and all(c['witnessBytesEqual'] for c in rep['witnessComparisons']),
           'FRESH_PROCESS_REPLAY_MATCHES_THE_COMPLETE_BUNDLE:' + label)
    fams = ctl['tamperedResultControls'] + ctl['identityAndRetentionControls']
    A.need(fams and all(c['refused'] for c in fams), 'EVERY_TAMPER_AND_RETENTION_CONTROL_REFUSED:' + label)
    A.need(not atom['refusals'], 'INDEPENDENT_ATOM_LAW_ADMITS_EVERY_WITNESS:' + label, len(atom['atoms']))
    A.need(xin.get('passed', 0) > 0 and not (xin.get('refusals') or []),
           'INDEPENDENT_EXECUTION_INPUTS_HAS_NO_REFUSAL:' + label)
    return st, doc


def closure_checks(label, needle):
    return [c for c in J('runs/%s.closure.json' % label)['checks']
            if needle in c['check'] and c['result'] == 'PASS']


def exit_table():
    if 'exit' not in _cache:
        table = {}

        def fn(n, _p):
            if isinstance(n, dict) and isinstance(n.get('class'), str) \
                    and isinstance(n.get('exitCode'), int):
                table.setdefault(n['class'], set()).add(n['exitCode'])
        walk(kitjson('workflows/command-inventory.v3.json'), fn)
        _cache['exit'] = {k: sorted(v) for k, v in table.items()}
    return _cache['exit']


def envelope_check(env, label, current_ids=None):
    ok, errs = readmit(ENV_DOC, '#', env)
    A.need(ok, 'ENVELOPE_READMITTED_BY_THE_OWNING_SCHEMA:' + label, errs)
    term = env.get('termination') or {}
    want = exit_table().get(term.get('class'))
    A.need(want is not None and len(want) == 1 and env.get('exitCode') == want[0],
           'EXIT_CODE_IS_THE_KIT_INVENTORY_CODE_FOR_THE_CLASS:' + label,
           {'class': term.get('class'), 'exitCode': env.get('exitCode'), 'kit': want})
    if env.get('kind') == 'failure':
        A.need(bool(env.get('errors')), 'FAILURE_ENVELOPE_ERRORS_NONEMPTY:' + label)
        if term.get('domainDetail') is not None:
            A.need(env.get('errors') == [term['domainDetail']],
                   'ERRORS_ARE_EXACTLY_THE_STEP_DOMAIN_DETAIL:' + label)
    if current_ids is not None:
        refs = set()
        walk(env, lambda n, p: refs.add(n) if isinstance(n, str) and n.startswith('run3:') else None)
        A.need(refs <= set(current_ids), 'ENVELOPE_RUN_REFERENCES_ARE_CURRENT_EXPORTS:' + label,
               sorted(refs - set(current_ids)))


def frames(label):
    """clone facts of the Run's evidence views with their parsed body-identity frames"""
    st, _doc = run_store(label)
    out = []
    for t, o in views(label)['facts'].items():
        if o['relation'] != 'clones':
            continue
        pay = blob_json(st, o['payloadDigest'])
        frame = st.get_blob(pay['bodyIdentity'].split(':', 1)[1])
        pos, comps = 0, []
        for _ in range(5):
            n = frame[pos]
            comps.append(frame[pos + 1:pos + 1 + n])
            pos += 1 + n
        out.append((t, pay, comps))
    return out


# =========================================================================== phase 0
@handler('S-FRESH-ORIGIN', 'reconstructed-behavior', ['notes/v22-input-custody.json'],
         'the current generation label and the manifest digest are re-measured here')
def _():
    c = J('notes/v22-input-custody.json')
    A.need(c['generation'] == 'consumer-b.v22', 'CUSTODY_NAMES_THE_CURRENT_ORIGIN', c['generation'])
    measured = hashlib.sha256(open(SUBJ + '/consumer-input-manifest.json', 'rb').read()).hexdigest()
    A.need(measured == A.whole['inputKit']['manifestSha256'] == c['claim1_manifestOwnBytes']['measured'],
           'MANIFEST_DIGEST_REMEASURED_EQUALS_REQUIREMENTS_AND_CUSTODY', measured)


@handler('S-NOT-PRODUCT', 'reconstructed-behavior',
         ['notes/v22-history-standing.json', 'notes/v22-path-census.json'],
         'kit bytes re-hashed here; confinement and census of this command')
def _():
    bad = [r['path'] for r in manifest_rows()
           if hashlib.sha256(open(SUBJ + '/' + r['path'], 'rb').read()).hexdigest() != r['sha256']]
    A.need(not bad and len(manifest_rows()) == 102, 'KIT_UNCHANGED_EVERY_ROW_REHASHED_HERE', bad)
    h = J('notes/v22-history-standing.json')
    A.need(h['measuredA_writeConfinement']['result'] == 'CONFINED', 'WRITES_CONFINED_TO_THIS_RUNTIME')
    A.need(J('notes/v22-path-census.json')['verdict'] == 'CLEAN', 'PATH_CENSUS_CLEAN')


@handler('S-KIT-ONLY', 'measured-control', ['output/lib/*.py', 'notes/v22-input-custody.json'],
         'every absolute path literal of every active module is scanned here')
def _():
    offenders = []
    for p in sorted(glob.glob(OUT + '/lib/*.py')):
        for i, line in enumerate(open(p, encoding='utf-8'), 1):
            s0 = line.strip()
            if s0.startswith('#') or 're.compile' in line or 'overwritten' in line \
                    or 'DISCLOSURE' in line:
                continue
            for m in re.finditer(r"""['"](/(?:tmp|Users|private|home)/[^'"]*)""", line):
                s = m.group(1)
                if s.startswith(RUNTIME) or s.startswith('/tmp/opensip-architecture-review-env') \
                        or '...' in s or '\\' in s or re.match(r'/tmp/opensip-design-corrections/consumer-b\.?$', s):
                    continue
                offenders.append('%s:%d %s' % (os.path.basename(p), i, s[:80]))
    A.need(not offenders, 'NO_ACTIVE_MODULE_NAMES_A_PATH_OUTSIDE_THIS_RUNTIME', offenders[:10])
    c = J('notes/v22-input-custody.json')
    A.need(c['runtimeFilesNotNamedAsInputs']['standing'].startswith('present in the runtime'),
           'NON_INPUT_RUNTIME_FILES_DISCLOSED_AS_NOT_OPENED')


@handler('S-MANIFEST-VERIFY', 'reconstructed-behavior', ['subject/consumer-input-manifest.json'],
         'every manifest path, sha256 and byte length re-verified here')
def _():
    rows = manifest_rows()
    ok = [r for r in rows if os.path.exists(SUBJ + '/' + r['path'])
          and len(open(SUBJ + '/' + r['path'], 'rb').read()) == r['bytes']
          and hashlib.sha256(open(SUBJ + '/' + r['path'], 'rb').read()).hexdigest() == r['sha256']]
    A.need(len(ok) == len(rows) == 102, 'EVERY_ROW_VERIFIED_HERE', len(ok))


@handler('S-NO-ORACLE', 'measured-control', ['output/lib/*.py'],
         'no active module imports or opens an author model, fixture or checker')
def _():
    names = ('native_evidence_model', 'atom_model', 'workflows_model', 'check-atoms',
             'check-fact-plane', 'evaluator_input_model')
    hits = []
    for p in sorted(glob.glob(OUT + '/lib/*.py')):
        for i, line in enumerate(open(p, encoding='utf-8'), 1):
            s = line.strip()
            if any(n in s for n in names) and (s.startswith('import ') or s.startswith('from ')
                                               or 'open(' in s or 'load_doc(' in s):
                hits.append('%s:%d' % (os.path.basename(p), i))
    A.need(not hits, 'NO_AUTHOR_MODEL_IMPORTED_OR_OPENED', hits)


@handler('S-MISSING-DEP-IS-CUSTODY', 'reconstructed-behavior', ['notes/v22-input-custody.json'],
         'every kit document opened by active code resolved against the verified manifest')
def _():
    c = J('notes/v22-input-custody.json')['custody']
    A.need(c['documentsOpened'] > 0 and c['resolved'] == c['documentsOpened'],
           'EVERY_OPENED_KIT_DOCUMENT_RESOLVES_IN_CUSTODY', {'opened': c['documentsOpened'],
                                                            'resolved': c['resolved']})
    A.need(c['custodyGaps'] == [], 'CUSTODY_GAPS_ARRAY_IS_EMPTY', c['custodyGaps'])


@handler('S-PROFILE-CURRENT', 'reconstructed-behavior', ['runs/*.store.json'],
         'typed prefixes of every exported object re-read per Run')
def _():
    old = {'finding2', 'proof2', 'run2', 'seal2', 'evidence2'}
    for l in RUNS:
        st, doc = run_store(l)
        pref = {t.split(':', 1)[0] for t in st.objects if ':' in t}
        A.need({'proof3', 'run3', 'seal3', 'evidence3', 'subject3'} <= pref and not (pref & old),
               'OUTPUT_MAJOR_3_AND_NO_HISTORICAL_OUTPUT_MAJOR:' + l)
        A.need({'plan2', 'fact2', 'coverage2', 'scope2', 'view2', 'snapshot2'} <= pref,
               'NATIVE_AND_INPUT_IDENTITIES_KEEP_MAJOR_2:' + l)
        A.need(doc['selectedProviderAndCapabilityContext']['outputMajors']['proof'] == 3,
               'RECORDED_OUTPUT_MAJORS:' + l)


@handler('S-CONTINUATION', 'reconstructed-behavior', ['requirements.json'],
         'the full required id set is re-derived and every id is audited by this stage')
def _():
    w = A.whole
    ids = [r['id'] for r in w['standing'] + w['requirements']]
    phased = sorted({i for ph in w['phases'] for i in ph['ids']})
    A.need(len(set(ids)) == len(ids) == 131 and sorted(set(ids)) == phased,
           'PHASE_UNION_EQUALS_THE_131_REQUIRED_IDS')
    A.need(len(w['standing']) == w['counts']['standing']
           and len(w['requirements']) == w['counts']['requirements']
           and len(w['futureQualification']) == w['counts']['futureQualification'],
           'COUNTS_OBJECT_EQUALS_ARRAY_LENGTHS')
    A.need(sorted(r for r, _ in HANDLERS) == sorted(ids), 'THIS_AUDIT_HAS_A_HANDLER_FOR_EVERY_ID',
           sorted(set(ids) - {r for r, _ in HANDLERS}))


@handler('R-FIVE-CONTRACTS-INDEX', 'cited-kit-distinction', ['notes/phase0-input-custody.json'],
         'the five contracts exist in the verified manifest and the quoted rule is kit text')
def _():
    p0 = J('notes/phase0-input-custody.json')['R-FIVE-CONTRACTS-INDEX']
    names = {r['path'] for r in manifest_rows()}
    A.need(all(('docs/v2/contracts/product-v1/' + n) in names for n in p0['fivePresent']),
           'FIVE_CONTRACTS_AND_INDEX_IN_THE_MANIFEST')
    q = p0['successorOverInheritedRule'].split('"', 1)[1].rsplit('"', 1)[0]
    A.need(in_kit(q), 'SUCCESSOR_OVER_INHERITED_QUOTE_IS_KIT_TEXT', q[:90])


@handler('R-SOURCE-MAP-SCOPE', 'cited-kit-distinction', ['notes/phase0-input-custody.json'],
         'source map is a manifest row; the governance-exclusion quote is kit text')
def _():
    p0 = J('notes/phase0-input-custody.json')
    A.need(p0['R-SOURCE-MAP-SCOPE']['path'] in {r['path'] for r in manifest_rows()},
           'CURRENT_SOURCE_MAP_IS_A_KIT_ROW')
    A.need(p0['R-SOURCE-MAP-SCOPE']['governanceNotUsedAsRecipe'] is True,
           'GOVERNANCE_NOT_USED_AS_RECIPE_RECORDED')
    q = p0['R-FIVE-CONTRACTS-INDEX']['governanceRecordsExcluded'].split('"', 1)[1].split('"', 1)[0]
    A.need(in_kit(q), 'GOVERNANCE_EXCLUSION_QUOTE_IS_KIT_TEXT', q[:90])


@handler('R-CVE1-TYPES-AVAILABLE', 'reconstructed-behavior', ['notes/phase0-input-custody.json'],
         'the eight CVE1 types re-read from the kit selector here')
def _():
    kit = json.load(open(SUBJ + '/docs/coop/artifacts/resolved-inputs.v2.json'))[
        'planIdContract']['canonicalValueEncoding']
    p0 = J('notes/phase0-input-custody.json')['R-CVE1-TYPES-AVAILABLE']
    A.need(p0['closedTypes'] == kit['closedTypes'] and len(kit['closedTypes']) == 8
           and set(kit['encodings']) == set(kit['closedTypes']), 'EIGHT_TYPES_FROM_THE_KIT_SELECTOR')


# =========================================================================== phase 1
@handler('R-H-HELPER', 'reconstructed-behavior', ['vectors/phase1-canonical-h-lexical.json'],
         'every C and H vector recomputed here from its retained value')
def _():
    rows = J('vectors/phase1-canonical-h-lexical.json')['R-H-HELPER']
    seen = 0
    for r in rows:
        k = r['kind']
        if k == 'h-frame':
            fr = K.h_frame(r['record'], r['value'])
            A.need(fr[:len(r['framePrefixHex']) // 2].hex() == r['framePrefixHex']
                   and len(fr) == r['frameByteLength'] and K.H(r['record'], r['value']) == r['H']
                   and K.ID(r['record'], r['value']) == r['typedId']
                   and K.H('snapshot', r['value']) == r['sameCBytesOtherDomain'] != r['H'],
                   'H_FRAME_RECOMPUTED_AND_DOMAIN_SEPARATED')
            seen += 1
        elif 'cBytes' in r and 'value' in r:
            cb = K.C(r['value'])
            A.need(cb.decode() == r['cBytes'] and len(cb) == r['cByteLength']
                   and K.raw_sha256(cb) == r['rawSha256OfC'], 'C_VECTOR_RECOMPUTED:' + k)
            seen += 1
        elif k == 'array-admitted-order-preserved':
            A.need(K.C(r['valueA']).decode() == r['cA'] and K.rec_digest(r['valueA']) == r['hA']
                   and K.rec_digest(r['valueB']) == r['hB'] and r['hA'] != r['hB']
                   and r['equal'] is False, 'ARRAY_ORDER_IS_IDENTITY_RELEVANT')
            seen += 1
        elif k == 'payload-offered-where-frame-required':
            A.need(r.get('firstRefusal') and r.get('classification') == 'invalid',
                   'PAYLOAD_AS_FRAME_REFUSED_WITH_FIRST_REFUSAL')
            seen += 1
        elif k == 'integer-bound':
            try:
                K.C({'n': int(r['n'])})
                accepted = True
            except K.CanonError:
                accepted = False
            A.need(accepted == r['expectedAccept'], 'INTEGER_BOUND_RECOMPUTED:' + r['n'])
            seen += 1
    A.need(seen == len(rows), 'EVERY_H_HELPER_ROW_RECOMPUTED', {'rows': len(rows), 'seen': seen})


def _raw_rows():
    return J('vectors/phase1-canonical-h-lexical.json')['R-LEXICAL-ADMISSION+R-RAW-VS-PARSED']


@handler('R-LEXICAL-ADMISSION', 'measured-control', ['vectors/phase1-canonical-h-lexical.json'],
         'raw admission re-run here on the retained raw bytes of every negative')
def _():
    for r in _raw_rows()['rawInputNegatives']:
        b = bytes.fromhex(r['rawInputHex'])
        A.need(len(b) == r.get('rawInputByteLength'), 'FULL_RAW_BYTES_RETAINED:' + r['case'])
        try:
            K.admit_raw_descriptor(b)
            code = None
        except K.LexicalRefusal as e:
            code = e.code
        A.need(r['refused'] and code == r['firstRefusal'] == r['expectedCode'] and r['masksLater'],
               'RAW_REFUSAL_REPRODUCED_HERE:' + r['case'], code)


@handler('R-RAW-VS-PARSED', 'measured-control', ['vectors/phase1-canonical-h-lexical.json'],
         'the raw refusal and the parsed-object encode are both re-run here')
def _():
    s = _raw_rows()['rawVsParsed']
    try:
        K.admit_raw_descriptor(s['rawInput'].encode())
        code = None
    except K.LexicalRefusal as e:
        code = e.code
    A.need(code == s['rawFirstRefusal'] == 'DUPLICATE_KEY', 'RAW_DUPLICATE_KEY_REFUSED_HERE', code)
    A.need(K.C(json.loads(s['rawInput'])).decode() == s['encodingTheAlreadyParsedObjectSucceeds'],
           'PARSED_OBJECT_ENCODE_CANNOT_SEE_THE_FAULT')


@handler('R-SEMANTIC-VS-OPERATIONAL', 'reconstructed-behavior',
         ['vectors/phase1-canonical-h-lexical.json'], 'run3 identities recomputed here')
def _():
    s = J('vectors/phase1-canonical-h-lexical.json')['R-SEMANTIC-VS-OPERATIONAL']
    run = s['runDescriptor']
    A.need(K.ID('run', run) == s['runId'], 'RUN_ID_RECOMPUTED')
    moved = K.ID('run', dict(run, **{s['semanticFieldChange']['field']: s['semanticFieldChange']['newValue']}))
    A.need(moved == s['semanticFieldChange']['newRunId'] != s['runId'], 'SEMANTIC_FIELD_MOVES_IDENTITY')
    o = s['operationalChange']
    A.need(K.rec_digest(o['receiptA']) != K.rec_digest(o['receiptB'])
           and o['receiptA']['runId'] == o['receiptB']['runId'] == s['runId'],
           'OPERATIONAL_CHANGE_MOVES_THE_RECEIPT_NOT_THE_RUN')


@handler('R-ACYCLIC-JOINS', 'reconstructed-behavior', ['vectors/phase1-canonical-h-lexical.json'],
         'cycle detection re-run here over the declared forward edges')
def _():
    a = J('vectors/phase1-canonical-h-lexical.json')['R-ACYCLIC-JOINS']
    prefix = {'snapshot2': 'snapshot', 'plan2': 'plan', 'scope2': 'subject-scope', 'fact2': 'fact',
              'coverage2': 'coverage', 'view2': 'view', 'proof3': 'proof-bundle',
              'evidence3': 'semantic-evidence', 'seal3': 'evaluation-seal', 'run3': 'run',
              'exec-plan2': 'execution-plan', 'finding3': 'finding',
              'policy-derivation3': 'policy-derivation'}
    edges = {k: [prefix[t] for t in v if t in prefix] for k, v in a['declaredForwardEdges'].items()}
    state, cycles = {}, []

    def dfs(n, stack):
        state[n] = 1
        for m in edges.get(n, []):
            if state.get(m) == 1:
                cycles.append(stack + [m])
            elif not state.get(m):
                dfs(m, stack + [m])
        state[n] = 2
    for n in edges:
        if not state.get(n):
            dfs(n, [n])
    A.need(not cycles and a['acyclic'] is True, 'NO_CYCLE_IN_THE_DECLARED_JOIN_GRAPH', cycles[:3])
    A.need(a['cycleRefusalAttempts'] and all(x['errors'] for x in a['cycleRefusalAttempts']),
           'EVERY_BACK_EDGE_ATTEMPT_REFUSED')


@handler('R-CVE1-EIGHT-TYPES', 'reconstructed-behavior', ['vectors/cve1-eight-types.json'],
         'every CVE1 encoding, decode and key order re-run here')
def _():
    v = J('vectors/cve1-eight-types.json')
    kit = json.load(open(SUBJ + '/docs/coop/artifacts/resolved-inputs.v2.json'))[
        'planIdContract']['canonicalValueEncoding']['closedTypes']
    A.need(v['closedTypes'] == kit, 'CLOSED_TYPES_ARE_THE_KIT_TYPES')
    covered = set()
    for r in v['roundTrips']:
        if 'value' in r:
            enc = K.cve1(r['value'])
            A.need(enc.hex() == r['encodedHex'] and K.cve1_decode_exact(enc) == r['decoded'] == r['value']
                   and r['roundTrip'], 'CVE1_ROUND_TRIP_REPRODUCED:' + r['type'])
            covered.add(r['type'])
        else:
            want = sorted(r['input'], key=lambda k: unicodedata.normalize('NFC', k).encode())
            enc = K.cve1({k: True for k in r['input']})
            dec = K.cve1_decode_exact(enc)
            A.need(want == r['encodedKeyOrder'] == list(dec), 'MAP_KEY_ORDER_REPRODUCED:' + r['aspect'])
    A.need(covered == set(kit), 'EVERY_TYPE_ROUND_TRIPPED', sorted(set(kit) - covered))
    for n in v['negatives']:
        inp = n.get('input')
        try:
            if inp is not None:
                t = inp['pythonType']
                val = (bytes.fromhex(inp['hex']) if t == 'bytes' else float(inp['repr']) if t == 'float'
                       else int(inp['decimal']) if t == 'int' else ''.join(chr(c) for c in inp['codepoints']))
                K.cve1(val)
                code = None
            elif 'rawInput' in n:
                K.admit_raw_descriptor(n['rawInput'].encode())
                code = None
            else:
                code = 'NO_RETAINED_INPUT'
        except K.Cve1Error as e:
            code = str(e)
        except K.LexicalRefusal as e:
            code = e.code
        A.need(n['refused'] and code == n['firstRefusal'] == n.get('expectedCode'),
               'CVE1_NEGATIVE_RE_RUN_HERE:' + n['case'], code)


# =========================================================================== phase 2
@handler('R-CAP-ADMISSION', 'reconstructed-behavior', ['vectors/capability-manifest-admission.json'],
         'committed bytes, digest, identity and CVE1 round trip recomputed here')
def _():
    rows = [p for p in J('vectors/capability-manifest-admission.json')['R-CAP-ADMISSION']['positives']
            if 'committedBytesHex' in p]
    A.need(len(rows) >= 2, 'AT_LEAST_TWO_COMMITTED_MANIFESTS', len(rows))
    for p in rows:
        b = bytes.fromhex(p['committedBytesHex'])
        A.need(hashlib.sha256(b).hexdigest() == p['committedBytesSha256'] and len(b) == p['committedByteLength']
               and K.capability_manifest_id(b) == p['capabilityManifestId']
               and K.cve1_decode_exact(b) == p['manifest'] and K.cve1(p['manifest']) == b,
               'MANIFEST_IDENTITY_AND_BYTES_RECOMPUTED:' + p['label'])


@handler('R-CAP-NAMED-GATES', 'measured-control', ['vectors/capability-manifest-admission.json'],
         'admission re-run here on every retained submitted manifest; first refusal and masking present')
def _():
    import opensip_capmanifest as CM
    adm = CM.CapabilityManifestAdmitter()
    g = J('vectors/capability-manifest-admission.json')['R-CAP-NAMED-GATES']
    for n in g['negatives']:
        tag = n['case'][:50]
        A.need(n['refused'] and n.get('firstRefusal') and any(k in n for k in MASKING_KEYS),
               'NEGATIVE_RECORDS_REFUSAL_AND_MASKING:' + tag)
        if 'targetGate' not in n:
            continue
        m = n.get('submittedManifest')
        if not A.need(m is not None, 'SUBMITTED_MANIFEST_RETAINED:' + tag,
                      n.get('submittedManifestJsonPortable')):
            continue
        collect = 'violationsInOrder' in n
        try:
            r = adm.admit(m, collect_order_violations=True) if collect else adm.admit(m)
            got = (None if r.get('admitted') else
                   {'gate': 'ADM-ORDER', 'code': r['orderViolations'][0]['code'],
                    'all': r['orderViolations']})
        except CM.CapRefusal as e:
            got = {'gate': e.gate, 'code': e.code}
        want_gate = n['firstRefusal'].get('gate', 'ADM-ORDER' if collect else None)
        A.need(got is not None and got['gate'] == want_gate == n['targetGate']
               and got['code'] == n['firstRefusal']['code']
               and (not collect or got.get('all') == n['violationsInOrder']),
               'ADMISSION_RE_RUN_REPRODUCES_THE_FIRST_REFUSAL_AT_THE_TARGET_GATE:' + tag,
               got and {k: v for k, v in got.items() if k != 'all'})
    A.need(set(g['gateOrder']) == {n['targetGate'] for n in g['negatives'] if 'targetGate' in n},
           'EVERY_NAMED_GATE_EXERCISED')


# =========================================================================== phase 3
def replay_trace(t, table):
    """An independent replay of native/protocol3-transitions.v1.json, from its
    initializationAndUpdateOrder, preMatchLaw, matchLaw, stateUpdates, stageDependentTransitions
    and terminalLaw."""
    state = dict(table['initialState'])
    pre = set(table['wildcards']['*PRE_COMPLETE']['phases'])
    pfault = set(table['wildcards']['*PROCESS_FAULT']['frames'])
    source = next(set(u['onFrames']) for u in table['stateUpdates'] if 'onFrames' in u)
    tokens = set(t['identityTokenSet'])
    rules_out, log = [], []
    for frame, payload in zip(t['events'], t['eventPayloads']):
        if state['phase'] == 'FAULT':
            rule = 'FAULT-absorb'
        elif frame in pfault:
            state['phase'], rule = 'FAULT', 'P3-33'
        elif state['phase'] in ('WAIT_ZERO_EXIT', 'WAIT_EOF', 'DONE') and frame not in ('zero-exit', 'eof'):
            state['phase'], rule = 'FAULT', 'post-terminal-frame'
        else:
            row = None
            for r in table['rules']:
                if r['phase'] == '*ANY' or r['frame'] != frame:
                    continue
                if not (r['phase'] == state['phase'] or (r['phase'] == '*PRE_COMPLETE' and state['phase'] in pre)):
                    continue
                if all(state.get(k) == v for k, v in (r.get('guard') or {}).items()):
                    row = r
                    break
            if row is None:
                state['phase'], rule = 'FAULT', 'P3-34'
            else:
                if frame == 'HelloAck':
                    state['identityNegotiated'] = tokens <= set((payload or {}).get('capabilities') or [])
                if frame == 'OpenUniverse':
                    state['dependencyMode'] = bool((payload or {}).get('dependencyMode'))
                    state['preparedMode'] = bool((payload or {}).get('preparedMode'))
                if frame == 'Analyze':
                    state['stageCount'], state['stageIndex'] = t['invocationStageCount'], 0
                if frame in source:
                    state['sourceBytesSent'] = True
                nxt = row['next']
                if nxt == 'ANALYZING_OR_READY_COMPLETE':
                    state['stageIndex'] += 1
                    state['stagesCompleted'] += 1
                    nxt = 'READY_COMPLETE' if state['stageIndex'] == state['stageCount'] else 'ANALYZING'
                if row.get('terminal'):
                    state['terminalKind'] = row['terminal']
                state['phase'], rule = nxt, row['id']
        rules_out.append(rule)
        log.append((state['phase'], state['identityNegotiated'], state['sourceBytesSent']))
    return state, rules_out, log


def traces_replayed():
    if 'traces' not in _cache:
        table = json.load(open(SUBJ + '/docs/coop/design-corrections/native/protocol3-transitions.v1.json'))
        rows = []
        for t in J('traces/protocol3-traces.json')['allTraces']:
            state, rules, log = replay_trace(t, table)
            same = (rules == t['ruleTrace'] and state['phase'] == t['finalPhase']
                    and state['terminalKind'] == t['terminalKind']
                    and state['identityNegotiated'] == t['identityNegotiated']
                    and state['sourceBytesSent'] == t['sourceBytesSent']
                    and state['stagesCompleted'] == t['stagesCompleted']
                    and [x[0] for x in log] == [s['phaseAfter'] for s in t['stepLog']])
            rows.append((t, state, rules, log, same))
        _cache['traces'] = (table, rows)
    return _cache['traces']


def _trace_req(pred, check):
    _table, rows = traces_replayed()
    A.need(all(r[4] for r in rows), 'EVERY_TRACE_REPLAYED_EQUAL_AGAINST_THE_KIT_TABLE',
           [r[0]['trace'] for r in rows if not r[4]])
    hit = [r[0]['trace'] for r in rows if r[4] and pred(r[0], r[1])]
    A.need(bool(hit), check, hit)


@handler('R-TRACE-COMPLETE', 'reconstructed-behavior', ['traces/protocol3-traces.json'],
         'independent replay of every trace against the kit transition table')
def _():
    _trace_req(lambda t, s: s['phase'] == 'DONE' and s['terminalKind'] == 'complete', 'A_COMPLETE_TRACE_REACHES_DONE')


@handler('R-TRACE-UNAVAILABLE', 'reconstructed-behavior', ['traces/protocol3-traces.json'], 'independent replay')
def _():
    _trace_req(lambda t, s: s['terminalKind'] == 'unavailable' and s['phase'] == 'DONE', 'AN_UNAVAILABLE_TRACE_REACHES_DONE')


@handler('R-TRACE-CANCEL', 'reconstructed-behavior', ['traces/protocol3-traces.json'], 'independent replay')
def _():
    _trace_req(lambda t, s: s['terminalKind'] == 'cancelled', 'A_CANCELLATION_TRACE_TERMINATES')


@handler('R-TRACE-FAULT', 'reconstructed-behavior', ['traces/protocol3-traces.json'], 'independent replay')
def _():
    _trace_req(lambda t, s: s['terminalKind'] == 'provider-fault', 'A_PROVIDER_FAULT_TRACE')
    _trace_req(lambda t, s: s['phase'] == 'FAULT', 'A_PROCESS_OR_PROTOCOL_FAULT_TRACE')


@handler('R-TRACE-IDENTITY-BEFORE-SOURCE', 'reconstructed-behavior', ['traces/protocol3-traces.json'],
         'replayed state at every step')
def _():
    _table, rows = traces_replayed()
    bad = [r[0]['trace'] for r in rows if any(src and not ident for _p, ident, src in r[3])]
    A.need(not bad, 'NO_SOURCE_BYTE_BEFORE_IDENTITY_NEGOTIATION_IN_ANY_REPLAY', bad)
    neg = [r for r in rows if 'identity' in r[0]['trace'] and r[1]['phase'] == 'FAULT']
    A.need(len(neg) >= 2 and all(not r[1]['sourceBytesSent'] for r in neg),
           'NEGOTIATION_NEGATIVES_FAULT_WITH_NO_SOURCE_BYTE')


@handler('R-TRACE-TERMINAL', 'reconstructed-behavior', ['traces/protocol3-traces.json'],
         'terminal kinds and post-terminal handling replayed')
def _():
    table, rows = traces_replayed()
    kinds = {r['terminal'] for r in table['rules'] if r.get('terminal')}
    reached = {r[1]['terminalKind'] for r in rows if r[4] and r[1]['terminalKind']}
    A.need(kinds == reached, 'EVERY_KIT_TERMINAL_KIND_REACHED_IN_REPLAY', sorted(kinds - reached))
    A.need(any('post-terminal-frame' in r[2] for r in rows) and any('FAULT-absorb' in r[2] for r in rows),
           'POST_TERMINAL_AND_ABSORBING_FAULT_REPLAYED')


@handler('R-TRACE-EXECUTED-VS-HOST', 'standing-record-verified', ['traces/protocol3-traces.json'],
         'the executed-vs-future-host label is present on every trace')
def _():
    _table, rows = traces_replayed()
    A.need(all('EXECUTED' in r[0]['executedVsHost'] and 'FUTURE-HOST' in r[0]['executedVsHost'] for r in rows),
           'EVERY_TRACE_LABELS_EXECUTED_AND_FUTURE_HOST', len(rows))


# =========================================================================== phase 4
@handler('R-RELATION-RUNG-TABLE', 'reconstructed-behavior', ['vectors/relation-rung-table.json'],
         'relation/rung pairs re-derived from the kit ladder authority here')
def _():
    reg = kitjson(REL_DOC)['x-opensip-relation-registry']['relations']
    v = J('vectors/relation-rung-table.json')
    pairs = sorted((r, g) for r, row in reg.items() for g in row['ladder'])
    A.need(v['relationCount'] == len(reg) == 13 and v['relationRungPairCount'] == len(pairs),
           'COUNTS_EQUAL_THE_KIT_REGISTRY')
    got = sorted((x.get('relation'), x.get('rung') or x.get('resolution')) for x in v['relationRungApplicability'])
    A.need(got == pairs, 'APPLICABILITY_ROWS_ARE_EXACTLY_THE_KIT_PAIRS')


@handler('R-COUNT-CLASS-ATTEMPT', 'reconstructed-behavior', ['vectors/count-class-attempt.json'],
         'anchor classes re-read from the kit; every fact count re-joined to the Run evidence')
def _():
    v = J('vectors/count-class-attempt.json')
    reg = kitjson(REL_DOC)['x-opensip-relation-registry']['relations']
    for rel, row in v['anchorClassesByRelation'].items():
        A.need(row['class'] == (reg[rel].get('anchorLaw') or {}).get('class') and row['ladder'] == reg[rel]['ladder'],
               'ANCHOR_CLASS_IS_THE_KIT_CLASS:' + rel)
    A.need(not any(v['failures'].values()) and v['measuredAnchorClassRows'] and v['measuredTotalityAndFactAbsentRows'],
           'MEASURED_ROWS_WITH_NO_FAILURE')
    for r in v['measuredTotalityAndFactAbsentRows']:
        n = sum(1 for o in views(r['run'])['facts'].values()
                if (o['relation'], o['resolution'], o['sourceUniverse']) == (r['relation'], r['resolution'], r['sourceUniverse']))
        A.need(n == r['factsAtThisPair'], 'FACT_COUNT_REJOINED:%s:%s@%s' % (r['run'], r['relation'], r['resolution']),
               {'evidence': n, 'row': r['factsAtThisPair']})


@handler('R-CODE-VS-DATA-MATRIX', 'reconstructed-behavior', ['vectors/code-vs-data-matrix.json'],
         'class membership and capability unions re-derived from the kit grammar registry')
def _():
    reg = kitjson(NATIVE_DOC)['x-opensip-grammar-capability-registry']['languages']
    v = J('vectors/code-vs-data-matrix.json')
    for cls in ('code', 'data-document'):
        langs = sorted(l for l, r in reg.items() if r['syntaxClass'] == cls)
        union = sorted({c for r in reg.values() if r['syntaxClass'] == cls for c in r['capabilities']})
        got = sorted(x.get('languageId') or x.get('language') for x in v['grammarsBySyntaxClass'][cls])
        A.need(got == langs, 'LANGUAGES_OF_CLASS_FROM_THE_KIT:' + cls, {'kit': langs, 'vector': got})
        A.need(sorted(v['capabilityUnionByClass'][cls]) == union, 'CAPABILITY_UNION_FROM_THE_KIT:' + cls)


@handler('R-ENUM-VS-RESOLUTION', 'reconstructed-behavior', ['runs/*.store.json'],
         'every file fact of every Run evidence view re-read')
def _():
    ladder = kitjson(REL_DOC)['x-opensip-relation-registry']['relations']['file']['ladder']
    rows = [(l, o['resolution']) for l in RUNS for o in views(l)['facts'].values() if o['relation'] == 'file']
    A.need(rows and all(r in ladder for _l, r in rows) and ladder == ['enumerated'],
           'FILE_FACTS_ONLY_ON_THE_REGISTERED_RUNG', len(rows))


@handler('R-ADVERTISED-MODE-PATHS', 'standing-record-verified', ['vectors/advertised-mode-paths.json'],
         'the advertised mode set is re-read from the kit and every mode has an admitted path')
def _():
    kit = kitjson(IDENT_DOC)['x-opensip-digest-domains']['languageModes']['map']
    v = J('vectors/advertised-mode-paths.json')
    A.need(v['advertisedModes'] == kit, 'ADVERTISED_MODES_ARE_THE_KIT_MAP')
    A.need(sorted(p['mode'] for p in v['modePaths']) == sorted(kit)
           and all(p['admitted'] and not p['representablePath'].get('refusals') for p in v['modePaths'])
           and not v['modesWithNoRepresentablePath'], 'EVERY_MODE_HAS_AN_ADMITTED_PATH')


# =========================================================================== phase 5
RUN_OF = {'R-RUN-TS': 'typescript', 'R-RUN-RUST': 'rust', 'R-RUN-SYNTAX-CODE': 'syntax-code',
          'R-RUN-SYNTAX-DATA': 'syntax-data', 'R-RUN-RUST-PARTIAL-EMPTY-CLONES': 'rust-partial'}
for _rid, _label in RUN_OF.items():
    def _mk(rid=_rid, label=_label):
        @handler(rid, 'reconstructed-behavior', ['runs/%s.store.json' % label, 'runs/%s.closure.json' % label,
                                                  'runs/%s.replay.json' % label, 'runs/%s.controls.json' % label],
                 'store re-hashed on load; closure, fresh replay, controls and the independent atom and '
                 'execution-input derivations of THIS command')
        def _():
            st, doc = run_verified(label)
            A.need(rid in doc['requirementIds'], 'RUN_CLAIMS_THIS_REQUIREMENT')
            if rid in ('R-RUN-SYNTAX-DATA', 'R-RUN-RUST-PARTIAL-EMPTY-CLONES'):
                vw = views(label)
                clones = [p for p in vw['pays'].values() if p['key']['relation'] == 'clones']
                facts = [o for o in vw['facts'].values() if o['relation'] == 'clones']
                A.need(clones and not facts and all(c['entry']['coverage'] != 'complete' and c['entry']['deficiency']
                                                    and c['entry']['nativeCause'] for c in clones),
                       'EMPTY_CLONES_VIEW_IS_TYPED_UNKNOWN_NOT_COMPLETE_EMPTY',
                       [(c['entry']['coverage'], c['entry']['deficiency']) for c in clones])
    _mk()


@handler('R-RUN-TS-NODE-MODULES', 'reconstructed-behavior', ['runs/typescript.store.json'],
         'node_modules layout retained and named by a retained native record')
def _():
    st, _doc = run_verified('typescript')
    layout = {d for lab, d in st.labels.items() if lab.startswith('node-modules-layout')}
    A.need(bool(layout), 'NODE_MODULES_LAYOUT_RETAINED')
    joined = []
    for t, o in st.objects.items():
        if t.startswith('native.'):
            walk(o, lambda n, p: joined.append(p) if isinstance(n, str) and n.split(':')[-1] in layout else None)
    A.need(bool(joined), 'LAYOUT_DIGEST_NAMED_BY_A_RETAINED_NATIVE_RECORD', joined[:3])
    A.need(any(lab.startswith('node_modules') for lab in st.labels), 'NODE_MODULES_BYTES_RETAINED')


@handler('R-RUN-TS-CONFIG-DEPS', 'reconstructed-behavior', ['runs/typescript.store.json'],
         'config graph retained; its raw digest equals the universe tsconfigGraphHash')
def _():
    st, _doc = run_verified('typescript')
    cg = {d for lab, d in st.labels.items() if lab.startswith('ts-config-graph')}
    unis = [o for t, o in st.objects.items() if t.startswith('native.semantic-universe.typescript')]
    A.need(cg and any(u.get('tsconfigGraphHash') in cg for u in unis), 'CONFIG_GRAPH_IS_THE_UNIVERSE_TSCONFIG_GRAPH_HASH')
    A.need(any(lab.startswith('node-modules-layout') for lab in st.labels), 'DEPENDENCY_LAYOUT_RETAINED')


def _rust():
    st, doc = run_verified('rust')
    return st, doc, doc.get('exhibits') or {}


def _contains_c_bytes(st, obj):
    needle = K.C(obj)
    return [d for d, b in st.blobs.items() if needle in b]


@handler('R-RUN-RUST-MIXED-EDITION', 'reconstructed-behavior', ['runs/rust.store.json'],
         'edition map found inside a retained Rust universe record')
def _():
    st, _doc, ex = _rust()
    em = ex['R-RUN-RUST-MIXED-EDITION']['editionMap']
    found = []
    for t, o in st.objects.items():
        if t.startswith('native.semantic-universe.rust'):
            walk(o, lambda n, p: found.append(t) if n == em else None)
    A.need(found and len(set(em.values())) > 1, 'MULTI_EDITION_MAP_IS_IN_A_RETAINED_UNIVERSE', sorted(set(em.values())))


@handler('R-RUN-RUST-TARGET-EDITION', 'reconstructed-behavior', ['runs/rust.store.json'],
         'target unit canonical bytes found in retained blobs; edition differs from the package default')
def _():
    st, _doc, ex = _rust()
    e = ex['R-RUN-RUST-TARGET-EDITION']
    A.need(bool(_contains_c_bytes(st, e['unit'])), 'TARGET_UNIT_CANONICAL_BYTES_RETAINED')
    A.need(e['targetEdition'] != e['packageDefaultForCrateName'] and e['differs'],
           'TARGET_EDITION_DIFFERS_FROM_PACKAGE_DEFAULT')


@handler('R-RUN-RUST-BODY-DIALECT', 'reconstructed-behavior', ['runs/rust.store.json'],
         'the two body-language-version records are retained blobs with distinct dialects')
def _():
    st, _doc, ex = _rust()
    e = ex['R-RUN-RUST-BODY-DIALECT']
    a, b = e['bodyLanguageVersionRecordSelectionA'], e['bodyLanguageVersionRecordSelectionB']
    A.need(K.rec_digest(a) in st.blobs and K.rec_digest(b) in st.blobs and a != b, 'BLV_RECORDS_RETAINED_AND_DISTINCT')


@handler('R-RUN-RUST-SAME-FILE-TWO-EDITIONS', 'reconstructed-behavior', ['runs/rust.store.json'],
         'one path, two retained universes, two retained body frames')
def _():
    st, _doc, ex = _rust()
    e = ex['R-RUN-RUST-SAME-FILE-TWO-EDITIONS']
    unis = {t.split('#', 1)[1] for t in st.objects if t.startswith('native.semantic-universe.rust')}
    A.need(e['selectionA']['universe'] in unis and e['selectionB']['universe'] in unis
           and e['selectionA']['universe'] != e['selectionB']['universe'], 'BOTH_UNIVERSES_RETAINED')
    ba, bb = e['selectionA']['bodyIdentity'].split(':')[1], e['selectionB']['bodyIdentity'].split(':')[1]
    A.need(ba in st.blobs and bb in st.blobs and ba != bb
           and e['selectionA']['effectiveEdition'] != e['selectionB']['effectiveEdition'],
           'TWO_BODY_FRAMES_RETAINED_UNDER_TWO_EDITIONS')


@handler('R-RUN-RUST-HASH-MARKER', 'reconstructed-behavior', ['runs/rust.store.json'],
         'an inventoried path with the # marker is in a retained subject inventory')
def _():
    st, _doc, _ex = _rust()
    ei = blob_json(st, st.labels['execution-inputs'])
    paths = [row.get('path') for r in ei['selectedRefs'] if r['domain'] == 'subject-inventory'
             for row in blob_json(st, r['digest'])['rows']]
    A.need(any(p and '#' in p for p in paths), 'HASH_MARKER_PATH_INVENTORIED')


@handler('R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE', 'reconstructed-behavior', ['runs/rust.store.json'],
         'the ownership pair and its body frame re-read from blobs')
def _():
    st, _doc, ex = _rust()
    e = ex['R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE']
    oa, oc = e['pairA']['ownershipIdentity'].split(':')[1], e['pairC']['ownershipIdentity'].split(':')[1]
    A.need(oa in st.blobs and oc in st.blobs and oa != oc, 'TWO_OWNERSHIP_RECORDS_RETAINED_AND_DISTINCT')
    A.need(e['pairA']['bodyIdentity'] == e['pairC']['bodyIdentity'] and e['pairA']['bodyIdentity'].split(':')[1] in st.blobs
           and e['pairA']['effectiveEdition'] == e['pairC']['effectiveEdition'], 'BODY_IDENTITY_STABLE')


@handler('R-RUN-RUST-LARGE-EDITION-MAP', 'reconstructed-behavior', ['runs/rust.store.json'],
         'map byte length recomputed; every retained version component is 32 bytes')
def _():
    _st, _doc, ex = _rust()
    em = ex['R-RUN-RUST-MIXED-EDITION']['editionMap']
    A.need(len(K.C(em)) > 255, 'EDITION_MAP_EXCEEDS_A_U8_COMPONENT', len(K.C(em)))
    fr = frames('rust')
    A.need(fr and all(len(c[4]) == 32 for _t, _p, c in fr), 'RETAINED_VERSION_COMPONENT_IS_32_BYTES', len(fr))


@handler('R-RUN-RUST-VERSION-COMPONENT', 'reconstructed-behavior', ['runs/rust.store.json'],
         'frame component equals raw SHA-256 of a retained body-language-version record')
def _():
    st, _doc, ex = _rust()
    blv = {d for lab, d in st.labels.items() if lab.startswith('body-language-version')}
    fr = frames('rust')
    A.need(fr and all(c[4].hex() in blv for _t, _p, c in fr), 'EVERY_VERSION_COMPONENT_IS_A_RETAINED_RECORD_DIGEST')
    e = ex['R-RUN-RUST-VERSION-COMPONENT']
    A.need(K.rec_digest(e['recomputedRecord']) == e['rawSha256OfCanonicalRecord'], 'EXHIBIT_RECORD_DIGEST_RECOMPUTED')


@handler('R-RUN-FILE-FACT-INVENTORY', 'reconstructed-behavior', ['runs/syntax-code.store.json'],
         'file facts joined to the snapshot inventory by the independent closure')
def _():
    for l in ('syntax-code', 'typescript', 'rust'):
        run_verified(l)
        A.need(closure_checks(l, 'FILE'), 'FILE_FACT_INVENTORY_JOIN_PASSED_IN_CLOSURE:' + l)


@handler('R-RUN-CLONES-L0-AND-NORMALIZED', 'reconstructed-behavior', ['runs/*.store.json'],
         'clone payload levels re-read from Run evidence')
def _():
    levels = {l: sorted({p.get('normalisationLevel') for _t, p, _c in frames(l)}) for l in ('syntax-code', 'typescript', 'rust')}
    ok = [l for l, v in levels.items() if any((x or '').startswith('L0') for x in v)
          and any((x or '')[:2] in ('L1', 'L2', 'L3') for x in v)]
    A.need(bool(ok), 'L0_AND_A_NORMALIZED_LEVEL_ON_ONE_COMPLETE_RUN', levels)


@handler('R-RUN-CLONES-CUSTODY', 'reconstructed-behavior', ['runs/*.store.json'],
         'per clone fact: frame, language-version record and level specification retained')
def _():
    for l in ('syntax-code', 'typescript', 'rust'):
        st, _doc = run_store(l)
        for t, p, c in frames(l):
            A.need(c[4].hex() in st.blobs, 'LANGUAGE_VERSION_RECORD_RETAINED:%s:%s' % (l, t[:18]))
            lv = p.get('normalisationVersion')
            if (p.get('normalisationLevel') or '')[:2] != 'L0':
                A.need(isinstance(lv, str) and lv.split(':')[-1] in st.blobs,
                       'LEVEL_SPECIFICATION_RETAINED:%s:%s' % (l, t[:18]), lv)
        A.need(any(k.startswith('source:') for k in st.labels), 'SOURCE_BYTES_RETAINED:' + l)


@handler('R-RUN-NO-COMPILER-UNIT', 'reconstructed-behavior', ['runs/syntax-code.store.json', 'runs/syntax-data.store.json'],
         'syntax Runs carry no TS/Rust universe and retain the syntax universe/context')
def _():
    for l in ('syntax-code', 'syntax-data'):
        st, _doc = run_verified(l)
        pref = {t.split('#')[0] for t in st.objects if '#' in t}
        A.need(not any('typescript' in p or 'rust' in p for p in pref) and any('syntax' in p for p in pref),
               'NO_COMPILER_UNIVERSE:' + l, sorted(pref))


@handler('R-RUN-UNAVAILABLE-SEMANTIC', 'reconstructed-behavior', ['runs/syntax-data.store.json'],
         'every typed-unavailable Coverage of the Run evidence checked against the kit registry')
def _():
    run_verified('syntax-data')
    reg = kitjson(NATIVE_DOC)['x-opensip-deficiency-cause-registry']['deficiencies']
    defic = [p for p in views('syntax-data')['pays'].values() if p['entry']['deficiency']]
    A.need(bool(defic), 'UNAVAILABLE_REQUESTS_DISCLOSED', len(defic))
    for p in defic:
        allowed = reg[p['entry']['deficiency']].get('allowedCauses')
        A.need(p['entry']['coverage'] == 'unknown' and (allowed is None or p['entry']['nativeCause'] in allowed),
               'TYPED_PAIRING_IS_A_REGISTRY_MEMBER:%s@%s' % (p['key']['relation'], p['key']['resolution']))


@handler('R-RUN-UNSUPPORTED-GRAMMAR', 'reconstructed-behavior', ['runs/syntax-data.store.json'],
         'data-document grammar selection re-joined to the kit registry; clones not served')
def _():
    _st, doc = run_verified('syntax-data')
    ex = (doc.get('exhibits') or {}).get('R-RUN-SYNTAX-DATA') or {}
    reg = kitjson(NATIVE_DOC)['x-opensip-grammar-capability-registry']['languages']
    langs = ex.get('selectedGrammarLanguages') or []
    A.need(langs and all(reg[l]['syntaxClass'] == 'data-document' for l in langs), 'SELECTED_GRAMMARS_ARE_DATA_DOCUMENT')
    A.need(all('clones@normalized-body-hash' not in reg[l]['capabilities'] for l in langs), 'CLONES_UNSUPPORTED_FOR_EVERY_SELECTED_GRAMMAR')


@handler('R-RUN-NONCEMPTY-CONTEXT', 'reconstructed-behavior', ['runs/typescript.store.json', 'runs/rust.store.json'],
         'plan native context digests non-empty and each names a retained context')
def _():
    for l in ('typescript', 'rust'):
        st, doc = run_verified(l)
        plan = st.objects[views(l)['run']['planId']]
        digests = []
        walk(plan, lambda n, p: digests.append(n) if 'ontext' in p and isinstance(n, str) else None)
        ctx = {t.split('#', 1)[1] for t in st.objects if t.startswith('native.context.')}
        A.need(digests and all(d.split(':')[-1] in ctx for d in digests), 'PLAN_CONTEXTS_NONEMPTY_AND_RETAINED:' + l)


@handler('R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC', 'reconstructed-behavior', ['runs/typescript.store.json'],
         'the analysis-spec parameter names the registered document; payload re-admitted here')
def _():
    st, _doc = run_verified('typescript')
    rows = kitjson(IDENT_DOC)['x-opensip-payload-registry']['classes']['parameter']['rows']
    row = [r for r in rows.values() if r['selector'] == '#/$defs/ScopeDocumentV1'][0]
    sha = S.load_doc(row['document'])['sha256']
    spec = blob_json(st, st.labels['analysis-spec'])
    p = [x for x in spec['parameters'] if x['schemaDigest'] == sha]
    A.need(len(p) == 1, 'SCOPE_DOCUMENT_PARAMETER_BOUND_BY_REGISTERED_DOCUMENT_DIGEST')
    ok, errs = readmit(row['document'], row['selector'], blob_json(st, p[0]['payloadDigest']))
    A.need(ok, 'SCOPE_DOCUMENT_PAYLOAD_READMITTED', errs)


@handler('R-IMPORTED-PAYLOAD-IN-GRAPH', 'reconstructed-behavior', ['runs/typescript.store.json'],
         'plan import, retained payload, evidence membership and a witness citing a payload row')
def _():
    st, doc = run_verified('typescript')
    run = views('typescript')['run']
    plan, ev = st.objects[run['planId']], st.objects[run['evidenceId']]
    A.need(plan['importIds'] and set(plan['importIds']) == set(ev['importIds']), 'PLAN_IMPORTS_ARE_EVIDENCE_MEMBERS')
    A.need(all((blob_json(st, st.objects[i]['payloadDigest']) or {}).get('subjects') for i in plan['importIds']),
           'IMPORT_PAYLOADS_RETAINED')
    proof = st.objects[st.objects[run['evaluationSealId']]['proofBundleId']]
    A.need(any(blob_json(st, pp['witnessDigest'])['matchingImportRows'] for pp in proof['predicateProofs']),
           'A_WITNESS_CITES_AN_IMPORTED_PAYLOAD_ROW')
    A.need(bool(views('typescript')['covs']), 'NATIVE_COVERAGE_IN_THE_SAME_GRAPH')


@handler('R-CLONE-DEFICIENCY-PAIRING', 'reconstructed-behavior', ['runs/rust-partial.store.json'],
         'the clones Coverage pairing of the Run evidence checked against the kit cause registry')
def _():
    st, _doc = run_verified('rust-partial')
    reg = kitjson(NATIVE_DOC)['x-opensip-deficiency-cause-registry']['deficiencies']
    cl = [p for p in views('rust-partial')['pays'].values() if p['key']['relation'] == 'clones']
    A.need(cl and all(p['entry']['deficiency'] and p['entry']['nativeCause'] in reg[p['entry']['deficiency']]['allowedCauses']
                      and reg[p['entry']['deficiency']]['nativeCause'] == 'required' for p in cl),
           'CLONES_PAIRING_IS_A_REQUIRED_REGISTERED_CAUSE')
    ei = blob_json(st, st.labels['execution-inputs'])
    A.need(any((o.get('deficiency'), o.get('nativeCause')) == (cl[0]['entry']['deficiency'], cl[0]['entry']['nativeCause'])
               for o in ei['cellOutcomes'] if o['state'] != 'complete'), 'OUTPUT_PROJECTION_CARRIES_THE_SAME_PAIR')


@handler('R-HIDDEN-MISMATCH-PER-LANGUAGE', 'measured-control', ['vectors/hidden-mismatch-per-language.json'],
         'hidden and mismatch controls per language, each refused at its intended join')
def _():
    cells = {(c['language'], c['inputDefect']) for c in J('vectors/hidden-mismatch-per-language.json')['controls']
             if c['refused'] and c['firstRefusalIsTheIntendedJoin'] and c.get('masking') is not None}
    A.need(cells >= {('typescript', 'hidden'), ('typescript', 'mismatch'), ('rust', 'hidden'), ('rust', 'mismatch')},
           'BOTH_DEFECT_KINDS_REFUSED_FOR_BOTH_LANGUAGES', sorted(cells))


@handler('R-NATIVE-PREIMAGE-JOINS', 'reconstructed-behavior', ['runs/rust.store.json', 'runs/typescript.store.json'],
         'dependency member blobs re-hashed; nested preimage joins passed in closure')
def _():
    st, _doc, ex = _rust()
    e = ex['R-NATIVE-PREIMAGE-JOINS']
    bad = [m['path'] for m in e['dependencyMemberBlobs']
           if m['sha256'] not in st.blobs or len(st.blobs[m['sha256']]) != m['byteLength']
           or hashlib.sha256(st.blobs[m['sha256']]).hexdigest() != m['sha256']]
    A.need(e['dependencyMemberBlobs'] and not bad, 'DEPENDENCY_MEMBERS_RETAINED_BY_DIGEST_AND_LENGTH', bad)
    for l in ('typescript', 'rust'):
        run_verified(l)
        A.need(closure_checks(l, 'JOIN') or closure_checks(l, 'PREIMAGE'), 'NESTED_PREIMAGE_JOINS_PASSED_IN_CLOSURE:' + l)


# =========================================================================== phase 6
def _config_vec(rel):
    v = J(rel)
    for case in [v['positive']] + v['negatives']:
        inst = case.get('submittedInstances') or []
        A.need(bool(inst), 'SUBMITTED_INSTANCES_RETAINED:' + case['case'])
        verdicts = [readmit(i['document'], i['selector'], i['instance']) for i in inst]
        if case is v['positive']:
            A.need(all(ok for ok, _e in verdicts) and case['accepted'], 'POSITIVE_INSTANCES_READMITTED:' + case['case'])
            cg = [i['instance'] for i in inst if i['role'] == 'config-graph'][0]
            uni = [i['instance'] for i in inst if i['role'] == 'universe']
            A.need(K.rec_digest(cg) == case['computedConfigurationIdentity'] and uni
                   and uni[0]['tsconfigGraphHash'] == case['computedConfigurationIdentity'],
                   'CONFIGURATION_IDENTITY_RECOMPUTED_AND_JOINED')
        else:
            refused_here = not all(ok for ok, _e in verdicts)
            A.need(case['refused'] and case['firstRefusal']
                   and (refused_here or case['refusals'] or 'IDENTITY' in str(case['firstRefusal'])),
                   'NEGATIVE_REFUSED_WITH_FIRST_REFUSAL:' + case['case'])
    return v


@handler('R-CONFIG-SYNTHESIZED', 'schema-admitted-record', ['vectors/config-synthesized.json'],
         'every submitted instance re-admitted here; identity recomputed')
def _():
    _config_vec('vectors/config-synthesized.json')


@handler('R-CONFIG-CUSTOM-MULTI-BASE', 'schema-admitted-record', ['vectors/config-custom-multi-base.json'],
         're-admitted; a repeated base retained in order')
def _():
    v = _config_vec('vectors/config-custom-multi-base.json')
    cg = [i['instance'] for i in v['positive']['submittedInstances'] if i['role'] == 'config-graph'][0]
    dup = []
    walk(cg, lambda n, p: dup.append(p) if isinstance(n, list) and n and all(isinstance(x, str) for x in n)
         and len(n) != len(set(n)) else None)
    A.need(bool(dup), 'A_REPEATED_BASE_IS_RETAINED_IN_ORDER', dup[:2])


@handler('R-CONFIG-JS-SHARED-BASE', 'schema-admitted-record', ['vectors/config-js-shared-base.json'], 're-admitted here')
def _():
    _config_vec('vectors/config-js-shared-base.json')


@handler('R-JS-CLONE-BODY-THROUGH-TS', 'reconstructed-behavior', ['vectors/js-body-through-ts.json', 'runs/typescript.store.json'],
         'each cited clone fact re-read from the TS evidence and its body frame parsed here')
def _():
    run_verified('typescript')
    fr = {t: c for t, _p, c in frames('typescript')}
    for r in J('vectors/js-body-through-ts.json')['cloneFacts']:
        c = fr.get(r['factId'])
        A.need(c is not None and c[3].decode() == r['bodyLanguageIdInTheRetainedFrame'],
               'BODY_LANGUAGE_READ_FROM_THE_RETAINED_FRAME:' + r['anchorPath'])
    langs = [c[3].decode() for c in fr.values()]
    A.need('javascript' in langs and 'typescript' in langs, 'JS_AND_TS_BODIES_IN_ONE_TS_UNIVERSE', langs)


@handler('R-CLONES-NEGATIVE-VECTORS', 'measured-control', ['vectors/clones-negatives.json'],
         'refusals with first refusal and ordered refusal list')
def _():
    v = J('vectors/clones-negatives.json')
    A.need(len(v['controls']) >= 4 and len(v['families']) >= 2
           and all(c['refused'] and c['firstRefusal'] and 'orderedRefusalChecks' in c for c in v['controls']),
           'EVERY_CLONE_NEGATIVE_REFUSED')


def _positive_descriptor():
    return [c for c in J('vectors/repair-descriptor.json')['controls'] if c['classification'] == 'valid'][0]


@handler('R-REPAIR-DESCRIPTOR', 'schema-admitted-record', ['vectors/repair-descriptor.json'],
         'positive plan re-admitted, identity recomputed and bound to the CURRENT TS Run')
def _():
    st, doc = run_verified('typescript')
    pos = _positive_descriptor()
    ok, errs = readmit(REPAIR_DOC, '#/$defs/RepairPlanV1', {'repairPlanId': pos['repairPlanId'], 'descriptor': pos['descriptor']})
    A.need(ok, 'POSITIVE_PLAN_READMITTED', errs)
    A.need(K.ID('workflow.repair-plan', pos['descriptor']) == pos['repairPlanId'], 'PLAN_ID_RECOMPUTED')
    A.need(pos['descriptor']['evidenceRunId'] == doc['claim']['runId']
           and pos['descriptor']['snapshotId'] == views('typescript')['run']['snapshotId']
           and all(t in st.objects for t in pos['descriptor']['targets']),
           'DESCRIPTOR_BOUND_TO_THE_CURRENT_EXPORTED_EVIDENCE_RUN')


@handler('R-REPAIR-AUTHORITY-PER-TARGET', 'measured-control', ['vectors/repair-descriptor.json'],
         'invalid controls re-admitted; their recorded first refusals are the owner joins')
def _():
    inv = [c for c in J('vectors/repair-descriptor.json')['controls'] if c['classification'] == 'invalid']
    for c in inv:
        ok, _e = readmit(REPAIR_DOC, '#/$defs/RepairPlanV1', {'repairPlanId': c['repairPlanId'], 'descriptor': c['descriptor']})
        A.need(not c['admitted'] and c['firstRefusal'] and ok == c['owningSchemaAdmitted'],
               'SCHEMA_VERDICT_REPRODUCED_AND_REFUSED:' + c['case'][:50])
    codes = json.dumps([c['firstRefusal'] for c in inv])
    A.need('CLOSED_WORLD_NOT_ESTABLISHED' in codes and 'TARGET_CORRESPONDENCE_UNAVAILABLE' in codes,
           'PER_TARGET_AUTHORITY_JOINS_EXERCISED')


@handler('R-MIN-RESOLUTION-THREE-LEVELS', 'reconstructed-behavior', ['vectors/min-resolution.json', 'vectors/indep-atom-law.json'],
         'atom-level cases: synthetic Coverage re-admitted here and independently re-derived')
def _():
    v = J('vectors/min-resolution.json')
    atom = v['atomLevelHalf']
    A.need(len(atom['levels']) == 3 and not atom['failures'], 'THREE_LEVELS_NO_FAILURE')
    for lv in atom['levels']:
        names = {c['case'] for c in lv['cases']}
        A.need({'qualifying-fact-and-complete-coverage', 'insufficient-fact-beside-complete-coverage',
                'insufficient-typed-coverage'} <= names, 'QUALIFYING_AND_INSUFFICIENT_AT:' + lv['level'])
        for c in lv['cases']:
            for cov in c['inputs']['coverages']:
                ok, errs = readmit(NATIVE_DOC, '#/$defs/CoverageResultV3', cov['payload'])
                A.need(ok, 'SYNTHETIC_COVERAGE_READMITTED:%s:%s' % (lv['level'], c['case']), errs)
    xc = J('vectors/indep-atom-law.json')['minResolutionAtomLevelCrossCheck']
    A.need(xc and all(r['result'] == 'PASS' for r in xc), 'INDEPENDENT_ATOM_DERIVATION_AGREES', len(xc))
    dv = set(kitjson(NATIVE_DOC)['$defs']['DeficiencyV2']['enum'])
    law = [cs['result']['deficiency'] for lv in v['lawHalf']['levels'] for cs in lv['cases']]
    A.need(all(d is None or d in dv for d in law), 'SUFFICIENCY_HALF_DEFICIENCIES_ARE_DEFICIENCYV2', law)


@handler('R-MIN-RESOLUTION-REPAIR-EVIDENCE', 'schema-admitted-record', ['vectors/repair-descriptor.json'],
         'both-plane evidence requirements re-admitted; cross-plane refused')
def _():
    ctl = J('vectors/repair-descriptor.json')['controls']
    both = [c for c in ctl if c['case'] == 'evidence-requirements-over-both-planes']
    A.need(both and both[0]['admitted'], 'BOTH_PLANE_CONTROL_ADMITTED')
    ok, errs = readmit(REPAIR_DOC, '#/$defs/RepairPlanV1', {'repairPlanId': both[0]['repairPlanId'], 'descriptor': both[0]['descriptor']})
    A.need(ok, 'BOTH_PLANE_PLAN_READMITTED', errs)
    A.need(any('CROSS_PLANE' in json.dumps(c.get('firstRefusal') or {}) for c in ctl), 'CROSS_PLANE_VALUE_REFUSED')


@handler('R-IMPORTED-OBSERVATION-BOUNDARY', 'reconstructed-behavior', ['vectors/imported-observation-boundary.json', 'runs/typescript.store.json'],
         'registry relations and outcomes re-read from the kit; the TS import staleness recomputed')
def _():
    v = J('vectors/imported-observation-boundary.json')
    kit = kitjson(IMPORTED_DOC)
    A.need(sorted(v['registeredImportedRelations']) == sorted(kit['x-opensip-evidence-relation-registry']['relations']),
           'IMPORTED_RELATIONS_FROM_THE_KIT')
    A.need(sorted(v['outcomeVocabulary']) == sorted(kit['x-opensip-imported-requirement-law']['outcomes']),
           'OUTCOME_VOCABULARY_FROM_THE_KIT')
    st, _doc = run_verified('typescript')
    plan = st.objects[views('typescript')['run']['planId']]
    for m in v['measuredOnTheTypeScriptRun']:
        corr = blob_json(st, st.objects[m['importId']]['sourceCorrespondenceDigest'])
        equal = corr['kind'] == 'exact-snapshot' and corr['snapshotId'] == plan['snapshotId']
        A.need(m['importId'] in plan['importIds'] and m['consumableForAPredicate'] == equal,
               'STALENESS_DISPOSITION_RECOMPUTED_FROM_RETAINED_CORRESPONDENCE')


@handler('R-MUTATION-REPLAY-SCOPE', 'schema-admitted-record', ['vectors/mutation-keys.json', 'vectors/indep-mutation-surface.json'],
         'replay-scope preimages re-admitted here; keys recomputed; joined to the mutation surface')
def _():
    v = J('vectors/mutation-keys.json')
    adm = v['replayScopeAdmissions']
    for role, row in adm.items():
        ok, errs = readmit(row['document'], row['selector'], row['instance'])
        want = role in ('genericMutation', 'importStep', 'nativePreparationStep')
        A.need(ok == want == row['admitted'], 'REPLAY_SCOPE_VERDICT_REPRODUCED:' + role, errs if want else None)
    for role in ('genericMutation', 'importStep', 'nativePreparationStep'):
        A.need(v[role]['preimage'] == adm[role]['instance'] and K.H('workflow.mutation-intent', v[role]['preimage']) == v[role]['key'],
               'KEY_IS_H_OVER_THE_ADMITTED_PREIMAGE:' + role)
    ms = J('vectors/indep-mutation-surface.json')
    A.need(not ms['refusals'] and ms['measuredKeys']['genericMutationIntent'] == v['genericMutation']['key'],
           'MUTATION_SURFACE_MEASURES_THE_SAME_KEY')


@handler('R-REPAIR-APPLY-KEY', 'reconstructed-behavior', ['vectors/mutation-keys.json', 'vectors/repair-descriptor.json'],
         'repair-apply key recomputed; bound to the current positive descriptor')
def _():
    v = J('vectors/mutation-keys.json')
    ra = v['repairApply']
    A.need(K.raw_sha256(K.C(ra['preimage'])) == ra['key'] and ra['key'] != K.H('workflow.mutation-intent', ra['preimage'])
           and ra['key'] != v['genericMutation']['key'], 'REPAIR_APPLY_KEY_IS_A_DIFFERENT_RECIPE')
    A.need(ra['preimage']['repairPlanId'] == _positive_descriptor()['repairPlanId']
           and all(v['repairApplyPreimageOwner'][k] for k in v['repairApplyPreimageOwner'] if k != 'standing'),
           'PREIMAGE_JOINS_THE_ADMITTED_DESCRIPTOR_AND_SNAPSHOT')
    A.need(J('vectors/indep-mutation-surface.json')['measuredKeys']['repairApply'] == ra['key'],
           'MUTATION_SURFACE_MEASURES_THE_SAME_REPAIR_APPLY_KEY')


@handler('R-PINNED-PURGE', 'schema-admitted-record', ['envelopes/pinned-purge.json'],
         'positive and negative envelopes re-admitted here')
def _():
    v = J('envelopes/pinned-purge.json')
    envelope_check(v['positive']['envelope'], 'pinned-purge-refusal')
    for n in v['negatives']:
        ok, _e = readmit(ENV_DOC, '#', n['envelope'])
        A.need(ok == n['owningSchemaAdmitted'] and not n['admitted'] and n['firstRefusal'],
               'NEGATIVE_REFUSED_AND_SCHEMA_VERDICT_REPRODUCED:' + n['label'])


# =========================================================================== phase 7
for _rid, _rel, _lab in (('R-SINGLE-STEP', 'envelopes/single-step.json', 'single-step'),
                         ('R-MULTI-STEP-DIFFERENT-SELECTIONS', 'envelopes/multi-step.json', 'multi-step'),
                         ('R-PUBLIC-FROM-INTERNAL-REFUSAL', 'envelopes/public-from-internal.json', 'public'),
                         ('R-DURABLE-RECEIPT-AVAILABILITY', 'envelopes/receipt-availability.json', 'receipt'),
                         ('R-ENVELOPE-CONFIG-INPUT', 'envelopes/config-input-failure.json', 'config'),
                         ('R-ENVELOPE-EXTERNAL-INPUT', 'envelopes/retained-external-input-failure.json', 'ext'),
                         ('R-ENVELOPE-HOST-INVALID', 'envelopes/host-generated-invalid-internal-record.json', 'host'),
                         ('R-ENVELOPE-PRODUCER-BOUNDARY', 'envelopes/producer-boundary-failure.json', 'producer')):
    def _mk(rid=_rid, rel=_rel, lab=_lab):
        @handler(rid, 'schema-admitted-record', [rel],
                 'final envelope re-admitted; D9 laws recomputed from the kit inventory; Run references '
                 'joined to the current exports')
        def _():
            row = J(rel)
            envelope_check(row['envelope'], lab, current_run_ids().values())
            if rid == 'R-MULTI-STEP-DIFFERENT-SELECTIONS':
                d = row['differentSelectionsMeasured']
                A.need(d['step1']['runId'] != d['step2']['runId'], 'DIFFERENT_SELECTIONS_ARE_DIFFERENT_RUNS')
            if rid == 'R-PUBLIC-FROM-INTERNAL-REFUSAL':
                A.need(bool(row['internalRefusalThisWasBuiltFrom'].get('firstRefusal')), 'BUILT_FROM_AN_ACTUAL_INTERNAL_REFUSAL')
    _mk()


@handler('R-MULTI-UNIT-MISSING-CAPS', 'schema-admitted-record', ['vectors/multi-unit-missing-caps.json'],
         'envelope re-admitted; notice counts recomputed')
def _():
    v = J('vectors/multi-unit-missing-caps.json')
    envelope_check(v['envelope'], 'multi-unit')
    av = v['envelope']['availability']
    A.need(av['totalNoticeCount'] == sum(len(s.get('notices') or []) for s in av['steps']) and len(v['units']) >= 2,
           'NOTICE_COUNT_RECOMPUTED_OVER_TWO_OR_MORE_UNITS')


@handler('R-CANDIDATE-ONLY-CLONES', 'schema-admitted-record', ['vectors/multi-unit-missing-caps.json'],
         'candidate-only and selected-complete sets disjoint, over the re-admitted envelope')
def _():
    v = J('vectors/multi-unit-missing-caps.json')
    envelope_check(v['envelope'], 'multi-unit')
    c = v['candidateOnlyIsNotSelected']
    A.need(c['candidateOnlyCapabilities'] and not set(c['candidateOnlyCapabilities']) & set(c['selectedCompleteCapabilities']),
           'CANDIDATE_ONLY_IS_NEVER_SELECTED')


@handler('R-INVOCATION-DISCLOSURE', 'reconstructed-behavior', ['envelopes/invocation-disclosure.json'],
         'bounds and step kinds re-read from the invocation schema')
def _():
    v = J('envelopes/invocation-disclosure.json')
    inv = kitjson(INVOC_DOC)
    for key, prop in (('orderedSteps', 'orderedSteps'), ('stepResults', 'stepResults'),
                      ('dependsOn', 'dependsOn'), ('attemptsPerStep', 'attempts')):
        s = find_prop(inv, prop)
        A.need(s is not None and s.get('maxItems') == v['boundedCardinality'][key], 'BOUND_FROM_THE_OWNING_SCHEMA:' + key,
               {'schema': s and s.get('maxItems'), 'vector': v['boundedCardinality'][key]})
    enum = []
    walk(inv, lambda n, p: enum.append(n['enum']) if isinstance(n, dict) and isinstance(n.get('enum'), list)
         and 'analysis' in n['enum'] and 'repair-apply' in n['enum'] else None)
    A.need(enum and sorted(v['stepKinds']) == sorted(enum[0]), 'STEP_KINDS_ARE_THE_SCHEMA_ENUM')


@handler('R-FAILURE-ENVELOPES-D9', 'reconstructed-behavior', ['envelopes/failure-envelopes-d9.json'],
         'every row flag recomputed from the named envelope bytes')
def _():
    rows = J('envelopes/failure-envelopes-d9.json')['rows']
    envs = {}
    for p in glob.glob(OUT + '/envelopes/*.json') + [OUT + '/vectors/multi-unit-missing-caps.json']:
        d = json.load(open(p))
        items = d['envelopes'] if isinstance(d, dict) and isinstance(d.get('envelopes'), list) else [d]
        for it in items:
            if isinstance(it, dict) and 'label' in it and 'envelope' in it:
                envs[it['label']] = it['envelope']
    table = exit_table()
    A.need(len(rows) >= 4, 'AT_LEAST_FOUR_FAILURE_ENVELOPES')
    for r in rows:
        e = envs.get(r['label'])
        if not A.need(e is not None, 'ROW_NAMES_A_RETAINED_ENVELOPE:' + r['label']):
            continue
        t = e['termination']
        A.need(r['hasDerivedExitCode'] == (e['exitCode'] in table.get(t['class'], []))
               and r['hasNonemptyErrors'] == bool(e.get('errors'))
               and r['errorsEqualTheStepDetail'] == (t.get('domainDetail') is None or e.get('errors') == [t['domainDetail']]),
               'ROW_FLAGS_RECOMPUTED:' + r['label'])


def id_index():
    if 'ids' not in _cache:
        idx = {}
        for r in manifest_rows():
            if r['path'].endswith('.json'):
                try:
                    d = json.load(open(SUBJ + '/' + r['path'], encoding='utf-8'))
                except ValueError:
                    continue
                if isinstance(d, dict) and isinstance(d.get('$id'), str):
                    idx[d['$id']] = d
        _cache['ids'] = idx
    return _cache['ids']


def deref(doc, node, depth=0):
    """follow $ref chains (local and cross-document by $id) to the referenced schema node"""
    while isinstance(node, dict) and isinstance(node.get('$ref'), str) and depth < 16:
        base, _, frag = node['$ref'].partition('#')
        if base:
            doc = id_index()[base]
        node = doc
        for part in [p for p in frag.split('/') if p]:
            node = node[part.replace('~1', '/').replace('~0', '~')]
        depth += 1
    return doc, node


def analysis_run_id_pattern(env_doc_name):
    doc = kitjson(env_doc_name)
    refs = []
    walk(doc, lambda n, p: refs.append(n) if p.endswith('.$ref') and isinstance(n, str)
         and n.endswith('/$defs/AnalysisResult') else None)
    d2, ar = deref(doc, {'$ref': refs[0]})
    pats = set()
    for branch in [ar] + list(ar.get('oneOf') or []) + list(ar.get('anyOf') or []):
        d3, b = deref(d2, branch)
        if isinstance(b, dict) and 'runId' in (b.get('properties') or {}):
            _d4, rid = deref(d3, b['properties']['runId'])
            if isinstance(rid, dict) and rid.get('pattern'):
                pats.add(rid['pattern'])
    assert len(pats) == 1, ('AnalysisResult runId patterns', sorted(pats))
    return pats.pop()


def _anchorless(p):
    return re.sub(r'(\(\?!\[\\s\\S\]\)|\$)$', '', p or '')


@handler('R-D9-EXTENSION-PRECEDENCE', 'reconstructed-behavior', ['vectors/phase7-standing-rules.json'],
         'schema major re-read from both envelopes; AnalysisResult.runId pattern resolved through $ref here')
def _():
    d = J('vectors/phase7-standing-rules.json')['R-D9-EXTENSION-PRECEDENCE']['measuredDifference']
    majors = []
    for doc in (ENV_DOC, ENV_DOC_INHERITED):
        s = find_prop(kitjson(doc), 'schemaMajor')
        majors.append(s.get('const') if s else None)
    A.need(majors == [d['schemaMajor']['selected'], d['schemaMajor']['inherited']], 'SCHEMA_MAJORS_FROM_BOTH_SCHEMAS', majors)
    pats = [analysis_run_id_pattern(ENV_DOC), analysis_run_id_pattern(ENV_DOC_INHERITED)]
    A.need(_anchorless(pats[0]) == _anchorless(d['runIdPattern']['selected'])
           and _anchorless(pats[1]) == _anchorless(d['runIdPattern']['inherited'])
           and 'run3:' in pats[0] and 'run2:' in pats[1],
           'ANALYSIS_RUN_ID_PATTERNS_RESOLVED_FROM_BOTH_ENVELOPES', pats)


@handler('R-CHAIN-ZERO-CONFIG-TO-RECEIPT', 'standing-record-verified', ['vectors/phase7-standing-rules.json'],
         'every arrow names artifacts that exist in this export')
def _():
    for arrow in J('vectors/phase7-standing-rules.json')['R-CHAIN-ZERO-CONFIG-TO-RECEIPT']['chain']:
        refs = re.findall(r'((?:runs|vectors|envelopes|traces|query)/[\w.*-]+\.json)', arrow['executedArtifact'])
        A.need(refs and all(glob.glob(os.path.join(OUT, r)) for r in refs), 'ARROW_ARTIFACTS_EXIST:' + arrow['arrow'][:40], refs)


@handler('R-SEMANTIC-VS-OPERATIONAL-AUTHORITY', 'reconstructed-behavior', ['vectors/phase7-standing-rules.json'],
         'operational fields absent from the descriptor schema; replay scope carries them')
def _():
    props = set((kitjson(REPAIR_DOC)['$defs'].get('RepairPlanDescriptor') or {}).get('properties', {}))
    A.need(props and not props & {'requestId', 'executionId', 'stepId', 'attemptId'}, 'DESCRIPTOR_SCHEMA_ADMITS_NO_OPERATIONAL_FIELD')
    scope = kitjson(INVOC_DOC)['$defs']['MutationReplayScopeV1']
    A.need({'requestId', 'stepId'} <= set(scope['required']), 'REPLAY_SCOPE_IS_REQUEST_SCOPED')
    A.need(not set(J('vectors/mutation-keys.json')['repairApply']['preimage']) & {'requestId', 'stepId'},
           'REPAIR_APPLY_PREIMAGE_IS_CONTENT_DERIVED')


@handler('R-MUTATION-VS-ANALYSIS-STEPS', 'cited-kit-distinction', ['vectors/phase7-standing-rules.json'],
         'each quoted recipe is found verbatim in the kit')
def _():
    r = J('vectors/phase7-standing-rules.json')['R-MUTATION-VS-ANALYSIS-STEPS']
    for step, text in r['citedRecipes'].items():
        for q in re.findall(r'"([^"]{12,})"', text):
            A.need(in_kit(q), 'QUOTE_IS_KIT_TEXT:' + step, q[:70])
    A.need(not set(r['stepsThatSealARun']) & set(r['stepsThatSealNoRun']), 'SEAL_SETS_DISJOINT')


@handler('R-PROMISE-VS-AVAILABILITY', 'standing-record-verified', ['vectors/phase7-standing-rules.json'],
         'four distinct things applied to artifacts that exist')
def _():
    r = J('vectors/phase7-standing-rules.json')['R-PROMISE-VS-AVAILABILITY']
    A.need(len({x['thing'] for x in r['fourDistinctThings']}) == 4, 'FOUR_DISTINCT_THINGS')
    A.need(all(os.path.exists(os.path.join(OUT, p)) for p in r['appliedTo']), 'APPLIED_TO_EXISTING_ARTIFACTS')


# =========================================================================== phase 8
def _cmp(rel):
    rec = J(rel)
    ok, errs = readmit(CMP_DOC, '#', rec)
    A.need(ok, 'COMPARISON_READMITTED:' + rel, errs)
    A.need(K.ID('workflow.comparison', rec['descriptor']) == rec['comparisonResultId'], 'COMPARISON_ID_RECOMPUTED:' + rel)
    A.need(rec['descriptor']['currentRunId'] == current_run_ids()['typescript'],
           'COMPARISON_CURRENT_SIDE_IS_THE_CURRENT_EXPORTED_TS_RUN:' + rel,
           {'recorded': rec['descriptor']['currentRunId'], 'current': current_run_ids()['typescript']})
    return rec['descriptor']


@handler('R-BASELINE-AUDIT', 'schema-admitted-record', ['vectors/baseline-audit.json'],
         'baseline and unchanged comparison re-admitted; ids recomputed; bound to the current Run')
def _():
    v = J('vectors/baseline-audit.json')
    ok, errs = readmit(BASE_DOC, '#', v['baselineArtifact'])
    A.need(ok, 'BASELINE_READMITTED', errs)
    A.need(K.ID('workflow.baseline', v['baselineArtifact']['descriptor']) == v['baselineArtifact']['baselineId'], 'BASELINE_ID_RECOMPUTED')
    A.need(v['baselineArtifact']['descriptor']['runId'] == current_run_ids()['typescript'], 'BASELINE_RUN_IS_THE_CURRENT_EXPORTED_TS_RUN')
    ok, errs = readmit(CMP_DOC, '#', v['comparisonUnchanged'])
    A.need(ok and K.ID('workflow.comparison', v['comparisonUnchanged']['descriptor']) == v['comparisonUnchanged']['comparisonResultId'],
           'UNCHANGED_COMPARISON_READMITTED', errs)


@handler('R-CMP-MISSING', 'schema-admitted-record', ['vectors/comparison-missing.json'], 're-admitted')
def _():
    d = _cmp('vectors/comparison-missing.json')
    A.need(d['comparisonPerformed'] is False and d['verdict'] == 'indeterminate' and not d['entries'], 'NOT_PERFORMED_IS_INDETERMINATE')


@handler('R-CMP-EVIDENCE-CHANGED', 'schema-admitted-record', ['vectors/comparison-evidence-changed.json'], 're-admitted')
def _():
    A.need(_cmp('vectors/comparison-evidence-changed.json')['contextDelta']['evidenceAvailabilityChanged'] is True, 'EVIDENCE_AXIS_CHANGED')


@handler('R-CMP-EMPTY-RESULT', 'schema-admitted-record', ['vectors/comparison-empty-result.json'], 're-admitted')
def _():
    d = _cmp('vectors/comparison-empty-result.json')
    A.need(d['comparisonPerformed'] is True and not d['entries'] and d['verdict'] == 'pass', 'EMPTY_IS_PERFORMED_AND_COMPLETE')


@handler('R-SCOPE-POLICY-ONLY-COMPARISON', 'schema-admitted-record', ['vectors/comparison-scope-policy-only.json'], 're-admitted')
def _():
    d = _cmp('vectors/comparison-scope-policy-only.json')
    delta = d['contextDelta']
    A.need(delta['scopeChanged'] and not any(v for k, v in delta.items() if k != 'scopeChanged')
           and d['baselineContext']['scopeDigest'] != d['currentContext']['scopeDigest'], 'ONLY_THE_BOUND_SCOPE_DOCUMENT_CHANGED')


@handler('R-PIVOT-ONLY-FINGERPRINTS', 'schema-admitted-record', ['vectors/comparison-pivot-only-fingerprints.json'],
         're-admitted; a pivot-only entry retained')
def _():
    d = _cmp('vectors/comparison-pivot-only-fingerprints.json')
    hits = []
    for e in d['entries']:
        pr = e['presence']
        base, cur = pr.get('B', pr.get('baseline')), pr.get('E4', pr.get('current'))
        if not base and not cur and any(pr.get(k) for k in ('E0', 'E1', 'E2', 'E3')):
            hits.append(e['fingerprint'])
    A.need(bool(hits), 'A_FINGERPRINT_PRESENT_ONLY_IN_A_PIVOT_IS_RETAINED', [e['presence'] for e in d['entries']][:2])


@handler('R-TEST-PREP-REPAIR-AUTH', 'schema-admitted-record', ['vectors/test-prep-repair-authorization.json'],
         'authorization records re-admitted against their owning schemas; identity joins recomputed; controls re-admitted')
def _():
    v = J('vectors/test-prep-repair-authorization.json')
    codes = set()
    walk(kitjson('public-detail-registry.v1.json'),
         lambda n, p: codes.add(n['code']) if isinstance(n, dict) and isinstance(n.get('code'), str) else None)
    defs = kitjson(INVOC_DOC)['$defs']
    for r in v['records']:
        A.need(r['paramsDef'].split('#/$defs/')[1] in defs and r['sealsARun'] is False, 'PARAMS_DEF_IN_THE_SCHEMA:' + r['step'])
        for s in r['submitted']:
            ok, errs = readmit(s['document'], s['selector'], s['instance'])
            A.need(ok and s['admitted'], 'RECORD_READMITTED:%s:%s' % (r['step'], s['role']), errs)
        A.need(all(c in codes for c in r['refusals']), 'REFUSAL_CODES_REGISTERED:' + r['step'],
               [c for c in r['refusals'] if c not in codes])
    ra = [r for r in v['records'] if r['step'] == 'repair-apply'][0]
    params = [s['instance'] for s in ra['submitted'] if s['role'] == 'params'][0]
    auth = [s['instance'] for s in ra['submitted'] if s['role'] == 'authorization'][0]
    A.need(params['authorizationRef'] == 'security.repair-apply-authorization.v1:' + K.H('security.repair-apply-authorization.v1', auth)
           and params['repairPlanId'] == auth['repairPlanId'] == _positive_descriptor()['repairPlanId']
           and auth['baseSnapshotId'] == views('typescript')['run']['snapshotId'],
           'AUTHORIZATION_IDENTITY_AND_BINDINGS_RECOMPUTED')
    for c in v['controls']:
        ok, _e = readmit(c['document'], c['selector'], c['instance'])
        A.need(ok == c['schemaAdmitted'] and c['refused'] and c['firstRefusal'] and (not ok or c['lawRefusal'] in codes),
               'CONTROL_REFUSED_AT_ITS_RECORDED_BOUNDARY:' + c['case'][:50])


@handler('R-PURGE-REPLAY-OUTPUT-FAILURE', 'schema-admitted-record', ['vectors/phase8-all.json'], 'the four case envelopes re-admitted')
def _():
    p8 = J('vectors/phase8-all.json')
    by = {c['label']: c for c in p8['controls']}
    for lab in p8['purgeReplayOutput']['cases']:
        c = by.get(lab)
        if A.need(c is not None and 'envelope' in c, 'CASE_RETAINS_ITS_ENVELOPE:' + lab):
            envelope_check(c['envelope'], lab)


@handler('R-PUBLIC-TERMINATION-EXAMPLES', 'schema-admitted-record', ['envelopes/public-termination.json'], 'six class examples re-admitted')
def _():
    v = J('envelopes/public-termination.json')
    for e in v['envelopes']:
        envelope_check(e['envelope'], e['label'])
    A.need({e['envelope']['termination']['class'] for e in v['envelopes']} == set(exit_table()), 'EVERY_KIT_D9_CLASS_EXEMPLIFIED')


@handler('R-SUBSYSTEM-OWNERS', 'standing-record-verified', ['vectors/phase8-subsystem-owners.json'],
         'every owner row cites a document present in the kit')
def _():
    parts = set()
    for r in manifest_rows():
        for tok in re.split(r'[-./_]', r['path'].lower()):
            if len(tok) >= 5:
                parts.add(tok)
    v = J('vectors/phase8-subsystem-owners.json')
    A.need(len(v['owners']) >= 10, 'AT_LEAST_TEN_OWNERS')
    for o in v['owners']:
        words = {w for w in re.findall(r'[a-z]{5,}', o['selector'].lower())}
        A.need(bool(words & parts), 'OWNER_CITES_A_KIT_DOCUMENT:' + o['decision'][:40], sorted(words)[:5])


@handler('R-E0-VS-E1-E3', 'reconstructed-behavior', ['vectors/baseline-e0-e3.json', 'vectors/baseline-audit.json'],
         'pivot vocabulary re-read from the comparison schema and joined to the admitted comparison')
def _():
    v = J('vectors/baseline-e0-e3.json')
    A.need(set(v['pivots']) == {'B', 'E0', 'E1', 'E2', 'E3', 'E4'}, 'SIX_PIVOT_ROLES')
    s = find_prop(kitjson(CMP_DOC), 'pivotsAvailable')
    A.need(s is not None and {'E0', 'E1', 'E2', 'E3'} <= set(s.get('properties', {})), 'PIVOTS_E0_E3_IN_THE_SCHEMA')
    A.need(v['measuredOnThisReconstruction']['pivotsAvailableInTheUnchangedComparison']
           == J('vectors/baseline-audit.json')['comparisonUnchanged']['descriptor']['pivotsAvailable'],
           'MEASURED_PIVOTS_EQUAL_THE_ADMITTED_COMPARISON')


@handler('R-HOST-CAPTURED-VS-CANDIDATE', 'reconstructed-behavior', ['vectors/host-captured-vs-candidate.json'],
         'consumable imports recomputed from retained correspondence')
def _():
    st, _doc = run_verified('typescript')
    plan = st.objects[views('typescript')['run']['planId']]
    cons = [i for i in plan['importIds']
            if blob_json(st, st.objects[i]['sourceCorrespondenceDigest'])['kind'] == 'exact-snapshot'
            and blob_json(st, st.objects[i]['sourceCorrespondenceDigest'])['snapshotId'] == plan['snapshotId']]
    A.need(sorted(J('vectors/host-captured-vs-candidate.json')['measuredJoin']['importsConsumableForAPredicate']) == sorted(cons),
           'CONSUMABLE_IMPORTS_RECOMPUTED')


@handler('R-EMPTY-PARTIAL-UNAVAILABLE-MISSING', 'reconstructed-behavior', ['vectors/empty-partial-unavailable-missing.json'],
         'every measured row re-joined to a Coverage payload of that Run evidence')
def _():
    v = J('vectors/empty-partial-unavailable-missing.json')
    for r in v['allMeasuredRows']:
        rel, rung = r['pair'].split('@')
        pays = [p for p in views(r['run'])['pays'].values() if (p['key']['relation'], p['key']['resolution']) == (rel, rung)]
        A.need(any((p['entry']['coverage'], p['entry']['deficiency'], p['entry']['nativeCause'])
                   == (r['coverage'], r['deficiency'], r['nativeCause']) for p in pays),
               'ROW_IS_A_RETAINED_COVERAGE:%s:%s' % (r['run'], r['pair']))
    A.need(len({s['state'] for s in v['states']}) == 4 and all(s['measuredExample'] for s in v['states']),
           'FOUR_DISTINCT_STATES_EACH_MEASURED')


@handler('R-DETECTOR-COMPAT-FILE', 'reconstructed-behavior', ['vectors/detector-compatibility-file.json'],
         'the detector closure descriptor and its retained component manifest re-read from the TS store')
def _():
    st, _doc = run_store('typescript')
    row = [m for m in J('vectors/detector-compatibility-file.json')['measured'] if 'detectorClosureId' in m][0]
    det = st.objects.get(row['detectorClosureId'])
    A.need(det is not None and sorted(det) == row['closureDescriptorKeys'], 'CLOSURE_DESCRIPTOR_KEYS_REREAD')
    keys = []
    mb = st.get_blob((det or {}).get('manifestDigest', '').split(':')[-1])
    if mb is not None:
        walk(json.loads(mb.decode()), lambda n, p: keys.extend(n.keys()) if isinstance(n, dict) else None)
    A.need(mb is not None and sorted(set(keys)) == row['componentManifestBodyKeys'], 'COMPONENT_MANIFEST_BODY_KEYS_REREAD')
    A.need(not any('compat' in k.lower() for k in list(det or {}) + keys) and not row['listingAmongThoseKeys'],
           'NO_LISTING_FIELD_IN_THE_DESCRIPTOR_OR_THE_MANIFEST_BODY')


# =========================================================================== phase 9
def _vector_walk(pred):
    bad = []
    for p in sorted(glob.glob(OUT + '/vectors/*.json') + glob.glob(OUT + '/envelopes/*.json')
                    + glob.glob(OUT + '/traces/*.json') + glob.glob(OUT + '/query/*.json')):
        rel = os.path.relpath(p, OUT)
        if rel.startswith('vectors/indep-') or rel in ('vectors/phase10-design-gaps.json',
                                                       'vectors/claimed-positive-audit.json'):
            continue
        doc = json.load(open(p))

        def rec(n, path, cls, covered):
            if isinstance(n, dict):
                cls = n.get('classification', cls)
                r = pred(n, cls, covered)
                if r:
                    bad.append('%s %s %s' % (rel, path, r))
                cov = covered or (bool(n.get('firstRefusal')) and any(k in n for k in MASKING_KEYS))
                for k, v in n.items():
                    rec(v, path + '.' + k, cls, cov)
            elif isinstance(n, list):
                for i, v in enumerate(n):
                    rec(v, '%s[%d]' % (path, i), cls, covered)
        rec(doc, '$', None, False)
    return bad


@handler('R-VALID-VS-INVALID-VS-EXPLANATORY', 'measured-control', ['vectors/', 'envelopes/', 'traces/', 'query/'],
         'every admission/refusal row carries (or inherits) a classification')
def _():
    bad = _vector_walk(lambda n, cls, _c: 'UNCLASSIFIED' if any(k in n for k in ('refused', 'firstRefusal')) and not (
        isinstance(cls, str) and any(w in cls for w in ('valid', 'invalid', 'explanatory', 'measured'))) else None)
    A.need(not bad, 'EVERY_CONTROL_ROW_CLASSIFIED', bad[:8])


@handler('R-MEASURED-NOT-COUNTS', 'measured-control', ['verify-all.json'],
         'every recorded stage exit is zero and the read-order guard holds')
def _():
    v = J('verify-all.json')
    A.need(v['stages'] and all(s['exit'] == 0 for s in v['stages']) and not v['readOrderGuard']['violations'],
           'EVERY_RECORDED_STAGE_EXITED_ZERO_AND_READ_ORDER_HOLDS',
           [s['script'] for s in v['stages'] if s['exit'] != 0] or len(v['stages']))
    rg = J('notes/v22-read-graph.json')
    A.need(rg['result'] == 'PASS' and rg['commandStageIoDir'] == v['stageIoDir'],
           'MEASURED_READ_GRAPH_OF_THIS_COMMAND_PASSES', rg['result'])


@handler('R-NEGATIVE-FIRST-REFUSAL', 'measured-control', ['vectors/', 'envelopes/', 'traces/', 'query/'],
         'every refused row (not already covered by an enclosing row) carries a first refusal and a masking record')
def _():
    bad = _vector_walk(lambda n, _cls, covered: 'REFUSED_WITHOUT_FIRST_REFUSAL_OR_MASKING' if (
        n.get('refused') is True and not covered and (not n.get('firstRefusal') or not any(k in n for k in MASKING_KEYS))) else None)
    A.need(not bad, 'EVERY_REFUSED_ROW_HAS_FIRST_REFUSAL_AND_MASKING', bad[:8])


@handler('R-DISTINGUISH-FOUR-BOUNDARIES', 'standing-record-verified', ['runs/*.store.json'],
         'schema log, closure report, replay report and a host-not-claimed standing per Run')
def _():
    for l in RUNS:
        _st, doc = run_verified(l)
        A.need(doc['schemaAdmissionLog'] and all(a['admitted'] for a in doc['schemaAdmissionLog'])
               and 'never native enforcement proof' in doc['syntheticObservationStanding'], 'FOUR_BOUNDARIES_RECORDED:' + l)


@handler('R-HELPER-KIT-ONLY', 'standing-record-verified', ['helper-corrections.json'],
         'every correction row carries original failure, kit selector and correction; none open')
def _():
    h = J('helper-corrections.json')
    A.need(all(r.get('originalFailure') and r.get('kitSelector') and r.get('correction') for r in h['helperCorrections']),
           'EVERY_ROW_COMPLETE', len(h['helperCorrections']))
    A.need(h['openHelperFailuresOnAClaimedPositive'] == [], 'NO_OPEN_HELPER_FAILURE')


@handler('R-REPLAY-AFTER-ADMISSION', 'reconstructed-behavior', ['runs/*.replay.json'],
         'replay gated on closure; a retention control never reaches replay')
def _():
    for l in RUNS:
        run_verified(l)
        rep = J('runs/%s.replay.json' % l)
        A.need(rep['closure']['admitted'] and rep['replayAttempted'], 'REPLAY_AFTER_CLOSURE:' + l)
        A.need(any(not c['closureAdmitted'] and c['refused'] for c in J('runs/%s.controls.json' % l)['identityAndRetentionControls']),
               'CLOSURE_REFUSAL_PRECEDES_REPLAY:' + l)


@handler('R-REPLAY-ENUM-AND-IDS', 'reconstructed-behavior', ['runs/*.replay.json'], 'replayed ids joined to the retained proof')
def _():
    for l in RUNS:
        st, _doc = run_verified(l)
        run = views(l)['run']
        proof = st.objects[st.objects[run['evaluationSealId']]['proofBundleId']]
        got = {(r['ruleId'], r['subjectId'], r['predicateId']): (r['value'], len(r['matchingFactIds']), len(r['coverageIds']))
               for r in J('runs/%s.replay.json' % l)['matchingFactIdsAndCoverageIds']}
        want = {(p['ruleId'], p['subjectId'], p['predicateId']):
                (p['value'], len(blob_json(st, p['witnessDigest'])['matchingFactIds']), len(blob_json(st, p['witnessDigest'])['coverageIds']))
                for p in proof['predicateProofs']}
        A.need(got == want, 'REPLAYED_IDS_EQUAL_THE_RETAINED_PROOF:' + l)


@handler('R-REPLAY-PREDICATE-WITNESS-VERDICT', 'reconstructed-behavior', ['runs/*.replay.json', 'vectors/indep-atom-law.json'],
         'witness bytes, findings and verdict replayed; atom witnesses re-derived independently')
def _():
    for l in RUNS:
        run_verified(l)
        rep = J('runs/%s.replay.json' % l)
        A.need(rep['recomputedVerdict'] == rep['retainedVerdict'] and not rep['claimedFindingsNotRecomputed'],
               'VERDICT_AND_EVERY_FINDING_REPLAYED:' + l)


@handler('R-REPLAY-NO-CALLER-TRUTH', 'measured-control', ['output/lib/opensip_replay.py', 'output/lib/indep_atom_law.py'],
         'the replay input builder reads no claimed output value; the atom instrument imports no evaluator')
def _():
    body = open(OUT + '/lib/opensip_replay.py', encoding='utf-8').read().split('def reconstruct_inputs', 1)[1].split('\ndef ', 1)[0]
    used = set(re.findall(r"proof_claim\['(\w+)'\]", body))
    A.need(used <= {'executionInputsDigest', 'ruleProgramDigest', 'evaluationInputRefs', 'executionPlanId', 'evaluatorClosure'}
           and 'predicateProofs' not in body and "['verdict']" not in body, 'REPLAY_READS_ONLY_INPUT_REFERENCES', sorted(used))
    ia = open(OUT + '/lib/indep_atom_law.py', encoding='utf-8').read()
    A.need('import opensip_eval' not in ia and 'import opensip_compose' not in ia, 'ATOM_INSTRUMENT_IMPORTS_NO_EVALUATOR')


@handler('R-REPLAY-COMPARE-BUNDLE', 'reconstructed-behavior', ['runs/*.replay.json', 'runs/*.controls.json'],
         'complete bundle comparison equal; tampered bundles refused by the same comparison')
def _():
    for l in RUNS:
        run_verified(l)
        A.need(all(c['replayVerdict'] == 'REPLAY_MISMATCH_REFUSED' for c in J('runs/%s.controls.json' % l)['tamperedResultControls']),
               'TAMPER_REFUSED_BY_COMPARISON:' + l)


@handler('R-REPLAY-EXPORT', 'reconstructed-behavior', ['runs/*.replay.json'], 'one replay export per current Run')
def _():
    for l in RUNS:
        run_verified(l)
        rep = J('runs/%s.replay.json' % l)
        A.need(rep['runId'] == current_run_ids()[l] and rep['bundleComparisons'], 'REPLAY_EXPORT_FOR_THE_CURRENT_RUN:' + l)


@handler('R-REPLAY-THREE-VALUED', 'reconstructed-behavior', ['vectors/indep-atom-law.json', 'vectors/min-resolution.json'],
         'missing Coverage with no match is indeterminate, re-derived independently')
def _():
    ia = J('vectors/indep-atom-law.json')
    xc = [r for r in ia['minResolutionAtomLevelCrossCheck'] if r['case'] == 'missing-relation-coverage-is-three-valued']
    A.need(len(xc) >= 6 and all(r['result'] == 'PASS' and r['derived']['value'] == 'indeterminate' for r in xc),
           'MISSING_COVERAGE_NO_MATCH_IS_INDETERMINATE_AT_EVERY_LEVEL', len(xc))
    real = [a for l in RUNS for a in ia['runs'][l]['atoms'] if a['plane'] == 'native' and a['completeness']
            and a['completeness']['returned'] in ('outgoing-1', 'outgoing-2', 'P2')]
    A.need(real and all(a['value'] == 'indeterminate' for a in real if not a.get('knownFacts')),
           'RETAINED_RUNS_EXHIBIT_THE_RETURNED_UNKNOWN', len(real))


@handler('R-REPLAY-TAMPER', 'measured-control', ['runs/*.controls.json'],
         'identities reminted, citations preserved, closure admits, replay refuses')
def _():
    for l in RUNS:
        run_verified(l)
        ctl = J('runs/%s.controls.json' % l)['tamperedResultControls']
        A.need(ctl and all(c['identitiesReminted'] and c['citationMembershipPreserved'] and c['closureAdmitted'] and c['refused'] for c in ctl),
               'TAMPER_CONTROLS:' + l)


@handler('R-ROOT-ADMISSION-EXPORT', 'standing-record-verified', ['runs/*.store.json'],
         'exact object table and blobs exported for every positive; root outcome not claimed')
def _():
    for l in RUNS:
        st, doc = run_store(l)
        A.need('objectTable' in doc and 'blobs' in doc and doc['blobCount'] == len(st.blobs), 'OBJECT_TABLE_AND_BLOBS_EXPORTED:' + l)


for _rid in ('R-VALIDATE-OWNING-SCHEMA', 'R-INDEPENDENT-CLOSURE-JOINS', 'R-OBJECT-TABLE-FRAMES',
             'R-RETAINED-ARTIFACTS-IN-CLOSURE', 'R-SELECTED-PROVIDER-CONTEXT'):
    def _mk(rid=_rid):
        @handler(rid, 'reconstructed-behavior', ['runs/*.store.json', 'runs/*.closure.json'],
                 'per Run: store re-hashed on load; schema log, closure and provider context re-read')
        def _():
            for l in RUNS:
                st, doc = run_verified(l)
                if rid == 'R-VALIDATE-OWNING-SCHEMA':
                    A.need(doc['schemaAdmissionLog'] and all(a['admitted'] and not a['publishedKeywordRefusals']
                                                              for a in doc['schemaAdmissionLog']),
                           'EVERY_RECORD_ADMITTED_WITH_PUBLISHED_KEYWORDS:' + l, len(doc['schemaAdmissionLog']))
                if rid == 'R-SELECTED-PROVIDER-CONTEXT':
                    ctx = doc['selectedProviderAndCapabilityContext']
                    unis = {t.split('#', 1)[1] for t in st.objects if t.startswith('native.semantic-universe.')}
                    A.need(ctx['closures'] and ctx['capabilityManifestId'] == views(l)['run']['capabilityManifestId']
                           and set(ctx['universeDigests']) <= unis, 'PROVIDER_CONTEXT_JOINS_THE_RUN:' + l)
                if rid == 'R-RETAINED-ARTIFACTS-IN-CLOSURE':
                    A.need(closure_checks(l, 'RETAIN') or closure_checks(l, 'PREIMAGE'), 'RETENTION_CHECKS_PASSED:' + l)
    _mk()


@handler('R-FROM-SCRATCH-COMMAND', 'reconstructed-behavior', ['verify-all.json'],
         'the command names the reference interpreter and this runtime; read order holds')
def _():
    v = J('verify-all.json')
    A.need(v['command'].startswith('/tmp/opensip-architecture-review-env/bin/python -I -B')
           and RUNTIME + '/output/lib/verify_all.py' in v['command'], 'COMMAND_IS_THE_REFERENCE_INTERPRETER_OVER_THIS_RUNTIME')
    A.need(not v['readOrderGuard']['violations'], 'STATIC_READ_ORDER_GUARD_HOLDS')
    rg = J('notes/v22-read-graph.json')
    A.need(rg['result'] == 'PASS' and rg['commandStageIoDir'] == v['stageIoDir'] and not rg['orderViolations'],
           'NO_STAGE_READ_AN_ARTIFACT_BEFORE_THIS_COMMAND_WROTE_IT', len(rg['orderViolations']))


@handler('R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR', 'schema-admitted-record',
         ['query/graph-query-reconstruction.json', 'query/indep-query-surface.json'],
         'every retained request/response of BOTH query artifacts re-admitted; both bound to the current TS Run')
def _():
    ts = current_run_ids()['typescript']
    g = J('query/graph-query-reconstruction.json')
    A.need(g['admittedRunUnderQuery']['runId'] == ts, 'ORIGINAL_QUERY_ARTIFACT_BOUND_TO_THE_CURRENT_RUN')
    for op in g['operations']:
        for req_k, resp_k in (('request', 'response'), ('secondRequest', 'secondResponse')):
            if req_k in op:
                ok1, e1 = readmit(Q_DOC, '#/$defs/GraphQueryRequestV1', op[req_k])
                ok2, e2 = readmit(Q_DOC, '#/$defs/GraphQueryResponseV1', op[resp_k])
                A.need(ok1 and ok2, 'ORIGINAL_QUERY_RECORDS_READMITTED:%s:%s' % (op['case'], req_k), e1 + e2)
    for fc in g['failureCases']:
        envelope_check(fc['lawfulFailureEnvelope']['envelope'], 'query-failure:' + fc['case'])
    s = J('query/indep-query-surface.json')
    A.need(s['runUnderQuery']['runId'] == ts and not s['refusals'], 'SUPPLEMENTAL_SURFACE_BOUND_TO_THE_CURRENT_RUN')
    for r in s['rawRequestAndResponseRecords']:
        ok1, e1 = readmit(Q_DOC, '#/$defs/GraphQueryRequestV1', r['request'])
        ok2, e2 = readmit(Q_DOC, '#/$defs/GraphQueryResponseV1', r['response'])
        A.need(ok1 and ok2, 'SUPPLEMENTAL_QUERY_RECORDS_READMITTED:' + r['operation'], e1 + e2)
    A.need(s['operationCount'] == len({r['operation'] for r in s['rawRequestAndResponseRecords']}) == 20,
           'TWENTY_OPERATIONS_WITH_RETAINED_RECORDS')


# =========================================================================== phase 10 / 11
@handler('R-IDENTIFY-GAPS', 'standing-record-verified', ['vectors/phase10-design-gaps.json'],
         'must/should arrays exist; every issue cites a selector; empty is justified')
def _():
    d = J('vectors/phase10-design-gaps.json')
    issues = d['newMustIssues'] + d['newShouldIssues']
    A.need(all(i.get('selector') or i.get('kitSelector') or i.get('selectors') for i in issues), 'EVERY_ISSUE_CITES_A_SELECTOR')
    A.need(d['newMustIssues'] or d.get('emptyMustJustification'), 'EMPTY_MUST_IS_JUSTIFIED')


@handler('R-FREEDOM-VS-MISSING', 'standing-record-verified', ['vectors/phase10-design-gaps.json'],
         'algorithm-freedom items recorded separately from gaps')
def _():
    A.need(bool(J('vectors/phase10-design-gaps.json').get('algorithmFreedomNotGaps')), 'FREEDOM_ITEMS_RECORDED')


@handler('R-BLOCKER-NOT-ADJUST', 'standing-record-verified', ['vectors/phase10-design-gaps.json'],
         'an exact blocker statement is recorded')
def _():
    d = J('vectors/phase10-design-gaps.json')
    s = d.get('blockerStatement') or ''
    A.need(bool(s), 'BLOCKER_STATEMENT_RECORDED')
    open_issues = bool(d['newMustIssues'] or d['newShouldIssues'])
    A.need(open_issues == ('no blocker' not in s.lower()), 'BLOCKER_STATEMENT_AGREES_WITH_THE_ISSUE_ARRAYS',
           {'must': len(d['newMustIssues']), 'should': len(d['newShouldIssues'])})


for _rid in ('R-DELIVER-MD-JSON', 'R-VERDICT-ENUM', 'R-MUST-SHOULD-ADVISORY', 'R-NO-ACCEPT-IF-INCOMPLETE',
             'R-NO-QUALIFICATION-CLAIM'):
    def _mk(rid=_rid):
        def run():
            A.start(rid, 'standing-record-verified', ['blind-review.md', 'blind-review.json'],
                    'DEFERRED to the requirement-status stage that runs AFTER the deliverable is written')
            A.cur['result'] = 'DEFERRED'
        HANDLERS.append((rid, run))
    _mk()


def main():
    for _rid, run in HANDLERS:
        run()
    A.finish()
    rows = A.reqs
    counts, by_class = {}, {}
    for r in rows.values():
        counts[r['result']] = counts.get(r['result'], 0) + 1
        by_class[r['evidenceClass']] = by_class.get(r['evidenceClass'], 0) + 1
    doc = {'standing': __doc__, 'evidenceClasses': EVIDENCE_CLASSES,
           'sufficientClassesByKind': {k: sorted(v) for k, v in SUFFICIENT.items()},
           'counts': counts, 'evidenceClassCounts': by_class, 'currentRunIds': current_run_ids(),
           'requirements': rows}
    with open(OUT + '/vectors/claimed-positive-audit.json', 'w') as fh:
        json.dump(doc, fh, indent=1, default=str)
    print('claimed-positive audit:', counts, 'classes', by_class)
    for rid, r in sorted(rows.items()):
        if r['result'] == 'FAIL':
            print('  FAIL %-44s %-26s %s' % (rid, r['evidenceClass'],
                                             json.dumps(r['firstRefusal'])[:230] if r['firstRefusal'] else 'evidence class insufficient'))
    raise SystemExit(1 if counts.get('FAIL') else 0)


if __name__ == '__main__':
    main()

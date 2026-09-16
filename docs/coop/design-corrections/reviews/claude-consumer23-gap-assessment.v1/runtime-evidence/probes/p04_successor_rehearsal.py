"""P04 — one coherent successor for V23-S1/S2/S3, rehearsed ONLY in a disposable hash-verified copy of frozen candidate36 docs/.
Every edit is an exact, count-asserted replacement. Then: re-pin the five ledgers for exactly the changed files (disposable only),
re-measure S1/S2/S3 against the kit, run every affected suite in the kit, and write the reviewable patch into this runtime.
No frozen, live or other-evidence byte is written. This is a rehearsal of a proposed successor, not a successor and not acceptance."""
import copy, difflib, hashlib, importlib.util, json, os, shutil, subprocess, sys, time

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
BASE = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1'
OUT = os.path.join(BASE, 'receipts')
KIT = os.path.join(BASE, 'disposable/kit36-successor')
PATCH = os.path.join(BASE, 'successor-patch')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v36.json'
man = {f['path']: f['sha256'] for f in json.load(open(MAN))['files']}
DC = 'docs/coop/design-corrections'
R = {'standing': 'disposable rehearsal of a proposed successor; not source, not acceptance', 'edits': {}}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------ kit
if os.path.isdir(KIT):
    shutil.rmtree(KIT)
copied = verified = 0
for rel in man:
    if not rel.startswith('docs/') or (rel.startswith(DC + '/reviews/') and not any(
            rel.endswith(n) for n in ('native-author-feedback.v1.md', 'security-author-feedback.v1.md', 'workflows-author-feedback.v1.md'))):
        continue
    d = os.path.join(KIT, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(os.path.join(S36, rel), d)
    copied += 1
    verified += sha(d) == man[rel]
assert copied == verified
R['kit'] = {'copied': copied, 'verified': verified}
print('kit: %d files byte-equal to frozen36' % copied, flush=True)
K = lambda rel: os.path.join(KIT, rel)


def replace_once(rel, old, new, label):
    p = K(rel)
    t = open(p, encoding='utf-8').read()
    n = t.count(old)
    assert n == 1, '%s: anchor count %d' % (label, n)
    open(p, 'w', encoding='utf-8').write(t.replace(old, new))
    R['edits'].setdefault(rel, []).append(label)


def json_edit(rel, fn, indent, label):
    p = K(rel)
    raw = open(p, 'rb').read()
    obj = json.loads(raw)
    assert (json.dumps(obj, indent=indent, ensure_ascii=True) + '\n').encode() == raw, rel + ': format roundtrip'
    obj = fn(obj)
    open(p, 'wb').write((json.dumps(obj, indent=indent, ensure_ascii=True) + '\n').encode())
    R['edits'].setdefault(rel, []).append(label)


# ------------------------------------------------------------------ S1
GQS = DC + '/workflows/schemas/evaluator3/graph-query.schema.json'


def s1_schema(o):
    defs = o['$defs']
    base = defs['GraphEndpoint']
    req = {'description': ('Request-side graph endpoint (query-projection-contract.v3.md section 2). The closed GraphEndpoint shape, except that a '
                           'kind=package endpoint may omit packageManifestPath at closed-schema admission so that section 2 step 2 refuses it '
                           'QUERY.ENDPOINT_AMBIGUOUS; packageManifestPath on a non-package, or present but not a LogicalPath, stays malformed. '
                           'Response rows keep GraphEndpoint, which requires the coordinate.'),
           'type': base['type'], 'additionalProperties': base['additionalProperties'], 'required': list(base['required']),
           'properties': copy.deepcopy(base['properties']),
           'allOf': [{'if': {'properties': {'kind': {'const': 'package'}}, 'required': ['kind']}, 'else': {'not': {'required': ['packageManifestPath']}}}]}
    new = {}
    for k, v in defs.items():
        new[k] = v
        if k == 'GraphEndpoint':
            new['GraphRequestEndpoint'] = req
    for d, props in (('GraphNeighborsParams', ('endpoint',)), ('GraphPathParams', ('start', 'target')), ('GraphReachParams', ('start',))):
        for prop in props:
            assert new[d]['properties'][prop] == {'$ref': '#/$defs/GraphEndpoint'}, (d, prop, new[d]['properties'][prop])
            new[d]['properties'][prop] = {'$ref': '#/$defs/GraphRequestEndpoint'}
    o['$defs'] = new
    return o


json_edit(GQS, s1_schema, 2, 'S1: add $defs/GraphRequestEndpoint; request params endpoint/start/target reference it; response rows keep GraphEndpoint')
QC = DC + '/workflows/query-projection-contract.v3.md'
replace_once(QC, 'empty native id, `packageManifestPath` on a non-package) → `QUERY.PARAMS_MALFORMED`.',
             'empty native id, `packageManifestPath` on a non-package, or a present `packageManifestPath` that is not a LogicalPath) → `QUERY.PARAMS_MALFORMED`.',
             'S1: s2 step 1 names a present invalid coordinate as malformed')
replace_once(QC, '2. Package identity without `packageManifestPath`, or a well-formed tuple',
             '2. Package identity whose `packageManifestPath` is absent, or a well-formed tuple', 'S1: s2 step 2 says absent')
replace_once(QC, 'Unknown universe or absent native identity must not become a fabricated zero-hop member.',
             'Closed-schema admission deliberately leaves step 2\'s absent package coordinate to this precedence: request params use '
             '`graph-query.schema.json#/$defs/GraphRequestEndpoint`, which admits it, while response rows keep `GraphEndpoint`, which '
             'requires it. Every step-1 shape is refused by closed-schema admission itself, with the same detail.\n\n'
             'Unknown universe or absent native identity must not become a fabricated zero-hop member.', 'S1: s2 states the schema split')
replace_once(QC, '| malformed-complete but ambiguous endpoint |', '| package endpoint without its coordinate, or well-formed but ambiguous endpoint |',
             'S1: s7 row label')
replace_once(QC, '1. Admit request (schema major 3, closed params).',
             '1. Admit request (schema major 3, closed params). An absent package coordinate passes this admission and is refused '
             '`QUERY.ENDPOINT_AMBIGUOUS` by endpoint syntax (section 2 step 2) before any vertex lookup.', 'S1: s8 step 1')
QM = DC + '/workflows/query_projection_model.v3.py'
replace_once(QM, '''    if kind == "package":
        path = ep.get("packageManifestPath")
        if type(path) is not str or not path:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.ENDPOINT_AMBIGUOUS",
                "package endpoints require packageManifestPath to distinguish same-name manifests",
                label,
            )
''', '''    if kind == "package":
        path = ep.get("packageManifestPath")
        if "packageManifestPath" not in ep:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.ENDPOINT_AMBIGUOUS",
                "package endpoints require packageManifestPath to distinguish same-name manifests",
                label,
            )
        if type(path) is not str or not path:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.PARAMS_MALFORMED",
                "endpoint.packageManifestPath must be a LogicalPath",
                label,
            )
''', 'S1: helper distinguishes absent (ENDPOINT_AMBIGUOUS) from present-invalid (PARAMS_MALFORMED)')
CQ = DC + '/workflows/check-query-projection.v3.py'
replace_once(CQ, '''    refuse("non-object-request", lambda: Q.execute_graph_query("not-an-object", host=host_obs()), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
''', '''    refuse("non-object-request", lambda: Q.execute_graph_query("not-an-object", host=host_obs()), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")

    def pkg_request(endpoint):
        return request("graph.neighbors", project, {"runId": run_key}, {
            "relation": "references", "minResolution": "resolved-binding", "direction": "outgoing", "endpoint": endpoint,
        })

    no_coordinate = pkg_request({"universe": g["u1"], "kind": "package", "nativeSubjectId": "app"})
    ok_req, why_req = valid(GQ + "#/$defs/GraphQueryRequestV1", no_coordinate)
    check("closed-request-admission-leaves-absent-package-coordinate-to-section-2", ok_req, why_req)
    check("response-graph-endpoint-still-requires-package-coordinate", not valid(GQ + "#/$defs/GraphEndpoint", no_coordinate["params"]["endpoint"])[0])
    refuse("package-endpoint-without-coordinate-is-endpoint-ambiguous", lambda: ex(no_coordinate), "REQUEST.PRECONDITION_FAILED", "QUERY.ENDPOINT_AMBIGUOUS")
    refuse("empty-package-coordinate-is-params-malformed", lambda: ex(pkg_request({"universe": g["u1"], "kind": "package", "nativeSubjectId": "app", "packageManifestPath": ""})), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
    refuse("package-coordinate-on-file-endpoint-is-params-malformed", lambda: ex(pkg_request({"universe": g["u1"], "kind": "file", "nativeSubjectId": "a.ts", "packageManifestPath": "package.json"})), "REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED")
''', 'S1+regression: wrapper controls for absent, empty and misplaced package coordinate')

# ------------------------------------------------------------------ S3
replace_once(QC, '`purged` / `expired` / `unavailable` / `corrupt` **refuse** access (`HOST.IO_FAILURE` / `evidence.*`).',
             '`purged`, `expired`, `corrupt` and `unavailable` **refuse** access with `HOST.IO_FAILURE` (`faultCause=host-io`) and, respectively, '
             '`evidence.purged`, `evidence.expired`, `evidence.corrupt` and `evidence.missing`. There is no `evidence.unavailable` member: '
             '`evidence.missing` is the identity owner\'s detail for required retained evidence that cannot be supplied. `retained` and `partial` '
             'do not refuse by themselves; Run closure and retained-byte reads still decide, and missing or corrupt required bytes then refuse by '
             'the rows below.', 'S3: exact availability-to-detail mapping')
replace_once(QC, '| corrupt retained bytes | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.corrupt` |\n',
             '| corrupt retained bytes | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.corrupt` |\n'
             '| trusted availability `purged` | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.purged` |\n'
             '| trusted availability `expired` | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.expired` |\n'
             '| trusted availability `corrupt` | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.corrupt` |\n'
             '| trusted availability `unavailable` | operational-failed | `HOST.IO_FAILURE` (`faultCause=host-io`) | `evidence.missing` |\n',
             'S3: s7 table rows for each refusing availability state')
replace_once(CQ, '''    refuse("host-availability-expired-refuses", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="expired")), "HOST.IO_FAILURE", "evidence.expired")
''', '''    refuse("host-availability-expired-refuses", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="expired")), "HOST.IO_FAILURE", "evidence.expired")
    refuse("host-availability-unavailable-refuses-evidence-missing", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="unavailable")), "HOST.IO_FAILURE", "evidence.missing")
    refuse("host-availability-corrupt-refuses-evidence-corrupt", lambda: ex(out_req, host_obs(latestRunId=run_key, availability="corrupt")), "HOST.IO_FAILURE", "evidence.corrupt")
    partial_anyway = ex(out_req, host_obs(latestRunId=run_key, availability="partial"))
    check("host-availability-partial-does-not-refuse-by-itself", len(partial_anyway["items"]) == 1, partial_anyway["termination"])
''', 'S3+regression: controls for unavailable, corrupt and partial availability')

# ------------------------------------------------------------------ S2
NAT = 'docs/v2/contracts/product-v1/native-evidence.md'
p = K(NAT)
lines = open(p, encoding='utf-8').read().split('\n')
CODE = {'language-tier-unsupported': 'COVERAGE.LANGUAGE_TIER_UNSUPPORTED', 'confidence-floor-unmet': 'COVERAGE.CONFIDENCE_FLOOR_UNMET',
        'required-relation-missing': 'COVERAGE.REQUIRED_RELATION_MISSING'}
for name, code in CODE.items():
    idx = [i for i, l in enumerate(lines) if l.startswith('| `%s` | ' % name) and '| `VERDICT.INDETERMINATE` | coverage2 record |' in l]
    assert len(idx) == 1, (name, idx)
    assert lines[idx[0]].count('`VERDICT.INDETERMINATE`') == 1
    lines[idx[0]] = lines[idx[0]].replace('`VERDICT.INDETERMINATE`', '`%s`' % code)
    R['edits'].setdefault(NAT, []).append('S2: s10 %s Existing code -> %s' % (name, code))
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
replace_once(NAT, 'A `null` deficiency requires a `null` cause: a cause without a deficiency names\nwhy nothing went wrong.\n',
             'A `null` deficiency requires a `null` cause: a cause without a deficiency names\nwhy nothing went wrong.\n\n'
             '**The Existing code column is the D9 exit contract\'s own map, and there is one mapping.** For a native deficiency that is\n'
             'also a `D9Deficiency` member (`required-relation-missing`, `provider-unavailable`, `language-tier-unsupported`,\n'
             '`budget-exhausted`, `confidence-floor-unmet`) the code is `d9-exit-contract.v1.14.json#/codeMaps/deficiencyToReasonCode`,\n'
             'unchanged. The four native-only outcomes have no `D9Deficiency` member and take `verdict-indeterminate`, whose code is\n'
             '`VERDICT.INDETERMINATE`. A per-requirement outcome carries its `DeficiencyV2` value and no D9 code (§4.6); the Run or\n'
             'step that carries it terminates with this column, which is the whole-Run code the D9 goldens derive.\n',
             'S2: s10 states the single mapping to the D9 codeMaps')


def s2_schema(o):
    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == 'publicD9Termination':
                    old = '(indeterminate (3) with VERDICT.INDETERMINATE, COVERAGE.PROVIDER_UNAVAILABLE or COVERAGE.BUDGET_EXHAUSTED)'
                    assert v.count(old) == 1
                    x[k] = v.replace(old, "(indeterminate (3) with the D9 exit contract's deficiencyToReasonCode for a D9Deficiency member - "
                                          'COVERAGE.REQUIRED_RELATION_MISSING, COVERAGE.PROVIDER_UNAVAILABLE, COVERAGE.LANGUAGE_TIER_UNSUPPORTED, '
                                          'COVERAGE.BUDGET_EXHAUSTED or COVERAGE.CONFIDENCE_FLOOR_UNMET - and VERDICT.INDETERMINATE for the four native-only outcomes)')
                else:
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(o)
    return o


json_edit(DC + '/native/native-evidence.schemas.v2.json', s2_schema, 2, 'S2: publicD9Termination names the D9 map')
NM = DC + '/native/native_evidence_model.v2.py'
replace_once(NM, 'CLASS_TO_EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}\n',
             'CLASS_TO_EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}\n'
             '# d9-exit-contract.v1.14.json#/codeMaps/deficiencyToReasonCode for the native DeficiencyV2 values that are also D9Deficiency\n'
             '# members (section 10 Existing code column). The four native-only outcomes take verdict-indeterminate -> VERDICT.INDETERMINATE.\n'
             'D9_DEFICIENCY_REASON_CODE = {"required-relation-missing": "COVERAGE.REQUIRED_RELATION_MISSING", "provider-unavailable": "COVERAGE.PROVIDER_UNAVAILABLE",\n'
             '                             "language-tier-unsupported": "COVERAGE.LANGUAGE_TIER_UNSUPPORTED", "budget-exhausted": "COVERAGE.BUDGET_EXHAUSTED",\n'
             '                             "confidence-floor-unmet": "COVERAGE.CONFIDENCE_FLOOR_UNMET"}\n', 'S2: model constant mirroring the D9 map')
replace_once(NM, '"code": "COVERAGE.PROVIDER_UNAVAILABLE" if worst == "provider-unavailable" else "VERDICT.INDETERMINATE"}',
             '"code": D9_DEFICIENCY_REASON_CODE.get(worst, "VERDICT.INDETERMINATE")}', 'S2: run_termination uses the D9 map')
NC = DC + '/native/native-cases.v2.json'


def s2_cases(o):
    ents = [('rrm', 'references', 'required-relation-missing', None), ('lts', 'clones', 'language-tier-unsupported', 'capability-missing'),
            ('cfu', 'references', 'confidence-floor-unmet', None), ('be', 'references', 'budget-exhausted', None),
            ('pu', 'references', 'provider-unavailable', 'capability-missing'), ('ri', 'references', 'resolution-incomplete', None)]
    steps = [{'fn': 'stage_authority', 'args': {'terminal_kind': 'complete'}, 'bind': 'st'}]
    expect = {}
    for b, rel, d, cause in ents:
        steps.append({'fn': 'run_termination', 'args': {'stage': '$st', 'coverage_entries': [{'relation': rel, 'deficiency': d, 'nativeCause': cause}]}, 'bind': b})
        expect['$%s.d9.class' % b] = 'indeterminate'
        expect['$%s.d9.exitCode' % b] = 3
        expect['$%s.typedDetail.deficiency' % b] = d
    expect.update({'$rrm.d9.code': 'COVERAGE.REQUIRED_RELATION_MISSING', '$lts.d9.code': 'COVERAGE.LANGUAGE_TIER_UNSUPPORTED', '$cfu.d9.code': 'COVERAGE.CONFIDENCE_FLOOR_UNMET',
                   '$be.d9.code': 'COVERAGE.BUDGET_EXHAUSTED', '$pu.d9.code': 'COVERAGE.PROVIDER_UNAVAILABLE', '$ri.d9.code': 'VERDICT.INDETERMINATE'})
    o['cases'].append({'id': 'run-termination-derives-the-d9-exit-contract-reason-code-for-each-deficiency', 'feedback': ['R7'], 'kind': 'positive',
                       'steps': steps, 'expect': expect})
    return o


json_edit(NC, s2_cases, 1, 'S2+regression: native case over five D9Deficiency members and one native-only outcome')

# ------------------------------------------------------------------ re-pin (disposable only)
changed = sorted(R['edits'])
LEDGERS = [DC + '/foundation/source-pins.v1.json', DC + '/foundation/evaluator3-source-pins.v1.json', DC + '/native/source-pins.v2.json',
           DC + '/security/source-pins.v1.json', DC + '/workflows/source-pins.v1.json']
repin = {}
for led in LEDGERS:
    raw = open(K(led), 'rb').read()
    obj = json.loads(raw)
    fmt = next(((i, a) for i in (1, 2) for a in (True, False) if (json.dumps(obj, indent=i, ensure_ascii=a) + '\n').encode() == raw), None)
    assert fmt, led
    key = 'files' if 'files' in obj else 'pins'
    n = 0
    for e in obj[key]:
        if e['path'] in changed:
            e['sha256'] = sha(K(e['path']))
            n += 1
    open(K(led), 'wb').write((json.dumps(obj, indent=fmt[0], ensure_ascii=fmt[1]) + '\n').encode())
    repin[led] = n
R['repinned'] = repin
second = {led: sha(K(led)) for led in LEDGERS}
for led in LEDGERS:
    obj = json.load(open(K(led)))
    key = 'files' if 'files' in obj else 'pins'
    for e in obj[key]:
        if e['path'] in LEDGERS:
            e['sha256'] = second[e['path']]
    raw = open(K(led), 'rb').read()
    fmt = next(((i, a) for i in (1, 2) for a in (True, False) if (json.dumps(json.loads(raw), indent=i, ensure_ascii=a) + '\n').encode() == raw), (2, True))
    open(K(led), 'wb').write((json.dumps(obj, indent=fmt[0], ensure_ascii=fmt[1]) + '\n').encode())
R['changedSourceFiles'] = changed
print('edits:', json.dumps(R['edits'], indent=1), '\nrepinned:', repin, flush=True)
L4 = json.load(open(os.path.join(S36, 'docs/v2/architecture/implementation-normative-inputs.v4.json')))
l4paths = {f['path'] for f in L4['files']}
R['layer4InputsTouched'] = sorted(p for p in changed if p in l4paths)
print('layer4 planning inputs touched by the successor:', R['layer4InputsTouched'], flush=True)

# ------------------------------------------------------------------ patch
os.makedirs(PATCH, exist_ok=True)
chunks = []
for rel in changed:
    a = open(os.path.join(S36, rel), encoding='utf-8').read().splitlines(keepends=True)
    b = open(K(rel), encoding='utf-8').read().splitlines(keepends=True)
    chunks.extend(difflib.unified_diff(a, b, 'a/' + rel, 'b/' + rel, n=3))
open(os.path.join(PATCH, 'successor-v23-gaps.patch'), 'w', encoding='utf-8').write(''.join(chunks))
R['patch'] = {'path': 'successor-patch/successor-v23-gaps.patch', 'sha256': sha(os.path.join(PATCH, 'successor-v23-gaps.patch')), 'files': changed,
              'pinLedgersNotInPatch': 'the five ledgers need only digest re-sealing for these files and for each other; root re-seals'}

# ------------------------------------------------------------------ re-measure against the kit
spec = importlib.util.spec_from_file_location('ckq_kit', K(CQ))
CK = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CK)
Q = CK.Q
U1 = 'a' * 64
meas = {}
for label, ep in (('package-absent-coordinate', {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app'}),
                  ('package-empty-coordinate', {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app', 'packageManifestPath': ''}),
                  ('file-with-coordinate', {'universe': U1, 'kind': 'file', 'nativeSubjectId': 'a.ts', 'packageManifestPath': 'package.json'}),
                  ('kind-outside-set', {'universe': U1, 'kind': 'module', 'nativeSubjectId': 'x'}),
                  ('package-with-coordinate', {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app', 'packageManifestPath': 'app/package.json'})):
    params = {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'endpoint': ep}
    req = CK.request('graph.neighbors', CK.project_id(), {'runId': CK.run_id()}, params)
    row = {'rawRequestSchemaAdmits': CK.valid(CK.GQ + '#/$defs/GraphQueryRequestV1', req)[0], 'rawResponseEndpointAdmits': CK.valid(CK.GQ + '#/$defs/GraphEndpoint', ep)[0]}
    for name, fn in (('wrapperWithoutRun', lambda: Q.execute_graph_query(req, host=CK.host_obs())), ('helper', lambda: Q.parse_endpoint_syntax(ep, 'endpoint'))):
        try:
            fn()
            row[name] = 'not refused'
        except Q.QueryRefusal as exc:
            row[name] = exc.detail
    meas[label] = row
R['kitS1'] = meas
print('kit S1:', json.dumps(meas, indent=1), flush=True)
spec = importlib.util.spec_from_file_location('nat_kit', K(NM))
NK = importlib.util.module_from_spec(spec)
spec.loader.exec_module(NK)
d9 = json.load(open(os.path.join(S36, 'docs/coop/artifacts/d9-exit-contract.v1.14.json')))['codeMaps']['deficiencyToReasonCode']
kitS2 = {}
for d in ('input-closure-incomplete', 'resolution-incomplete', 'external-consumers-unknown', 'derivation-policy-unmet', 'provider-unavailable',
          'language-tier-unsupported', 'budget-exhausted', 'confidence-floor-unmet', 'required-relation-missing'):
    code = NK.run_termination(NK.stage_authority('complete'), [{'relation': 'references', 'deficiency': d, 'nativeCause': None}])['d9']['code']
    kitS2[d] = {'model': code, 'd9': d9.get(d, d9['verdict-indeterminate']), 'equal': code == d9.get(d, d9['verdict-indeterminate'])}
R['kitS2'] = kitS2
print('kit S2 all equal D9:', all(v['equal'] for v in kitS2.values()), flush=True)

# ------------------------------------------------------------------ suites in the kit
KDC = K(DC)
JOBS = [
    ('check-query-projection', K(CQ), ['--report', os.path.join(OUT, 'p04-kit-check-query-projection.json')], KDC + '/workflows', 900),
    ('native', K(DC + '/native/check_native_evidence.v2.py'), [], KDC + '/native', 900),
    ('foundation-reference', K(DC + '/foundation/run-reference-checks.py'), ['--report', os.path.join(OUT, 'p04-kit-foundation.json'), '--report-dir', os.path.join(OUT, 'p04-kit-foundation')], KDC + '/foundation', 3600),
    ('evaluator3-launcher', K(DC + '/foundation/run-evaluator3-checks.py'), ['--out', os.path.join(OUT, 'p04-kit-evaluator3')], KDC + '/foundation', 9900),
    ('integration', K(DC + '/check-integration.py'), ['--report', os.path.join(OUT, 'p04-kit-integration.json')], KDC, 900),
    ('security', K(DC + '/security/check-security-lifecycle.v1.py'), ['--report', os.path.join(OUT, 'p04-kit-security.json')], KDC + '/security', 900),
    ('workflows-reference', K(DC + '/workflows/run-reference-checks.py'), ['--report', os.path.join(OUT, 'p04-kit-workflows.json')], KDC + '/workflows', 900),
]
jobs = []
for name, path, args, cwd, tmo in JOBS:
    t0 = time.time()
    cmd = [PY, '-I', '-B', path] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=tmo)
        rc, so, se = r.returncode, r.stdout or '', r.stderr or ''
    except subprocess.TimeoutExpired:
        rc, so, se = None, '', 'TIMEOUT'
    open(os.path.join(OUT, 'p04-kit-%s.stdout' % name), 'w').write(so)
    open(os.path.join(OUT, 'p04-kit-%s.stderr' % name), 'w').write(se)
    tail = so.strip().splitlines()[-1:] or ['']
    jobs.append({'name': name, 'command': cmd, 'returncode': rc, 'seconds': round(time.time() - t0, 1), 'stdoutSha256': hashlib.sha256(so.encode()).hexdigest(),
                 'lastLine': tail[0][-300:], 'stderrTail': se[-1500:] if rc else ''})
    print('%-22s rc=%-4s %7.1fs %s' % (name, rc, jobs[-1]['seconds'], tail[0][-160:]), flush=True)
R['kitSuites'] = jobs
try:
    rep = json.load(open(os.path.join(OUT, 'p04-kit-check-query-projection.json')))
    NEW = ('closed-request-admission-leaves-absent-package-coordinate-to-section-2', 'response-graph-endpoint-still-requires-package-coordinate',
           'package-endpoint-without-coordinate-is-endpoint-ambiguous', 'empty-package-coordinate-is-params-malformed',
           'package-coordinate-on-file-endpoint-is-params-malformed', 'host-availability-unavailable-refuses-evidence-missing',
           'host-availability-corrupt-refuses-evidence-corrupt', 'host-availability-partial-does-not-refuse-by-itself')
    byid = {c['id']: c for c in rep['checks']}
    R['kitQueryControls'] = {'passed': rep['passed'], 'count': rep['count'], 'failed': rep['failed'], 'new': {n: byid.get(n, {}).get('ok') for n in NEW}}
    print('kit query controls:', R['kitQueryControls'], flush=True)
except Exception as exc:  # noqa: BLE001
    R['kitQueryControls'] = {'error': str(exc)}
lr = os.path.join(OUT, 'p04-kit-evaluator3', 'report.json')
if os.path.isfile(lr):
    d = json.load(open(lr))
    R['kitLauncher'] = {'sourcePinsValid': d.get('sourcePinsValid'), 'passed': d.get('passed'), 'children': [(c.get('name'), c.get('exitCode')) for c in d.get('checks', [])],
                        'changedOrMissing': d.get('changedOrMissing', [])}
nr = K(DC + '/native/native-evidence-report.v2.json')
try:
    n = json.load(open(nr))
    R['kitNativeNewCase'] = [c for c in n['cases']['results'] if c['id'] == 'run-termination-derives-the-d9-exit-contract-reason-code-for-each-deficiency']
except Exception as exc:  # noqa: BLE001
    R['kitNativeNewCase'] = {'error': str(exc)[:200]}
R['allKitSuitesExitZero'] = all(j['returncode'] == 0 for j in jobs)
R['kitFilesRewrittenByCheckers'] = sorted(rel for rel in man if os.path.isfile(K(rel)) and rel not in changed and rel not in LEDGERS and sha(K(rel)) != man[rel])
R['frozen36DriftAfter'] = sum(1 for rel, h in man.items() if sha(os.path.join(S36, rel)) != h)
print('all kit suites exit 0:', R['allKitSuitesExitZero'], '| kit files rewritten by checkers:', R['kitFilesRewrittenByCheckers'], '| frozen36 drift:', R['frozen36DriftAfter'])
json.dump(R, open(os.path.join(OUT, 'p04-successor-rehearsal.json'), 'w'), indent=1, default=str)
print('wrote p04-successor-rehearsal.json')

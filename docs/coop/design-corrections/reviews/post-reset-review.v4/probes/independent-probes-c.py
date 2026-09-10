"""Independent reviewer probes, part C: the newly re-entered SARIF/G17 surface,
plus the remaining joins named by the instruction. Same standing as parts A/B."""
import copy
import hashlib
import importlib.util
import json
import re
import traceback
from pathlib import Path

from jsonschema import ValidationError

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v4/scratch')
DC = ROOT / 'docs/coop/design-corrections'
CONTRACTS = ROOT / 'docs/v2/contracts/product-v1'
ARCH = ROOT / 'docs/v2/architecture'

spec = importlib.util.spec_from_file_location('probe_host_c', DC / 'integration-host-model.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
S, N, W, C = M.S, M.N, M.W, M.C
IM = N.IM
F = M.load('probe_fixtures_c', 'integration-fixtures.py')

results = []
ERRORS = (ValueError, ValidationError, C.AdmissionError, W.Refusal, N.C.AdmissionError,
          IM.C.AdmissionError, KeyError)


def rec(pid, title, status, detail):
    results.append({'probe': pid, 'title': title, 'status': status, 'detail': detail})
    print('%-6s %-14s %s' % (pid, status, title))
    if status != 'OK':
        print('        ' + json.dumps(detail, default=str)[:2500])


def probe(pid, title):
    def deco(fn):
        try:
            out = fn()
        except Exception as exc:
            rec(pid, title, 'PROBE-ERROR', {'exception': ''.join(
                traceback.format_exception_only(type(exc), exc)).strip(),
                'trace': traceback.format_exc()[-1000:]})
            return
        status, detail = out if isinstance(out, tuple) else (('OK' if out else 'COUNTEREXAMPLE'), out)
        rec(pid, title, status, detail)
    return deco


def refuses(fn):
    try:
        fn()
    except ERRORS:
        return True
    return False


def raised(fn):
    try:
        fn()
    except Exception as exc:
        return exc
    return None


WF = C.parse((DC / 'workflows/workflow-cases.v1.json').read_bytes())
INV = C.parse((DC / 'workflows/command-inventory.v1.json').read_bytes())
CMD = {c['name']: c for c in INV['commands']}
CONST = WF['constants']


def sub(v):
    if isinstance(v, str) and v.startswith('$'):
        return CONST[v[1:]]
    if isinstance(v, list):
        return [sub(x) for x in v]
    if isinstance(v, dict):
        return {k: sub(x) for k, x in v.items()}
    return v


# ===========================================================================


@probe('P61', 'SARIF re-entry: the reference renderer is exercised for only ONE of D-372\'s four commands')
def _():
    sarif_cmds = sorted(c['name'] for c in INV['commands'] if 'sarif' in c['formats'])
    exercised = sorted({c['command'] for c in WF['renderCases'] if 'sarif' in c['formats']})
    refused_case = [c for c in WF['renderCases'] if c['expect'].get('refusal')]
    return ('OK' if set(sarif_cmds) <= set(exercised) else 'COUNTEREXAMPLE'), {
        'commandsAdvertisingSarif': sarif_cmds,
        'commandsWithASarifRenderCase': exercised,
        'unexercised': sorted(set(sarif_cmds) - set(exercised)),
        'renderCaseCount': len(WF['renderCases']),
        'negativeSarifCase': [c['id'] for c in refused_case]}


@probe('P62', 'SARIF re-entry: what the reference renderer actually emits for each of the four commands')
def _():
    """Drive the real renderer exactly as the workflow checker does, for all four
    commands D-372 re-enters, and record verdict / deficiency / results."""
    rows = {}
    for name in sorted(c['name'] for c in INV['commands'] if 'sarif' in c['formats']):
        cmd = CMD[name]
        parity = {k: ('x-' + k) for k in cmd['parityFields']}
        parity['findings'] = [{'fingerprint': CONST['FP1']}]
        env = {'parity': parity, 'envelope': {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 2},
               'hints': []}
        renders = {f: W.render(env, f, cmd) for f in cmd['formats']}
        sarif = renders['sarif']
        rows[name] = {
            'declaredParityFields': cmd['parityFields'],
            'sarifRunProperties': sarif['runProperties'],
            'sarifResultsCount': len(sarif['results']),
            'findingsIsADeclaredParityField': 'findings' in cmd['parityFields'],
            'verdictIsADeclaredParityField': 'verdict' in cmd['parityFields'],
            'deficiencyIsADeclaredParityField': 'deficiency' in cmd['parityFields'],
            'parityHoldsAcrossRenderers': W.parity_holds(list(renders.values())),
            'sarifCarriesDataOutsideItsOwnParitySet':
                len(sarif['results']) > 0 and 'findings' not in cmd['parityFields'],
        }
    broken = {k: v for k, v in rows.items()
              if v['sarifRunProperties']['verdict'] is None or v['sarifCarriesDataOutsideItsOwnParitySet']}
    return ('OK' if not broken else 'COUNTEREXAMPLE'), {'rows': rows, 'affected': sorted(broken)}


@probe('P63', 'SARIF re-entry: the renderer reads results UNFILTERED but verdict FILTERED (one function, two rules)')
def _():
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    line = next(l for l in src.splitlines() if "'format': 'sarif'" in l)
    unfiltered = "envelope['parity'].get('findings', [])" in line
    filtered = "parity.get('verdict')" in line and "parity.get('deficiency')" in line
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    law = re.search(r'`sarif` v1 \(([^)]+)\)', prose)
    return ('OK' if not (unfiltered and filtered) else 'COUNTEREXAMPLE'), {
        'rendererLine': line.strip(),
        'resultsReadFromUnfilteredEnvelope': unfiltered,
        'verdictReadFromFilteredParity': filtered,
        'contractRendererLaw': law.group(1) if law else None}


@probe('P64', 'D-372 says advisory-only commands gain no SARIF or verdict; check the whole inventory')
def _():
    rows = {}
    for c in INV['commands']:
        if c.get('advisory'):
            rows[c['name']] = {'sarif': 'sarif' in c['formats'],
                               'verdictParity': 'verdict' in (c.get('parityFields') or [])}
    nonadvisory_sarif_without_verdict = sorted(
        c['name'] for c in INV['commands']
        if 'sarif' in c['formats'] and not c.get('advisory')
        and 'verdict' not in (c.get('parityFields') or []))
    ok = (not any(v['sarif'] or v['verdictParity'] for v in rows.values()))
    return ('OK' if ok and not nonadvisory_sarif_without_verdict else 'COUNTEREXAMPLE'), {
        'advisoryCommands': rows,
        'nonAdvisorySarifCommandsWithoutAVerdictParityField': nonadvisory_sarif_without_verdict,
        'd372Clause': 'advisory-only commands do not gain SARIF or a verdict'}


@probe('P65', 'G17 gate row: reactivated, unqualified, undemonstrated, with a named owner and harness')
def _():
    gates = C.parse((DC / 'qualification-gates.proposed.json').read_bytes())
    items = gates.get('gates') or gates.get('items') or []
    g17 = next((g for g in items if 'G17' in str(g.get('gate') or g.get('id'))), None)
    ids = sorted(str(g.get('gate') or g.get('id')) for g in items)
    return ('OK' if (g17 and g17.get('qualified') is False and g17.get('demonstrated') is False
                     and g17.get('owner') and g17.get('harness') and g17.get('currentContract'))
            else 'COUNTEREXAMPLE'), {'g17': g17, 'gateCount': len(items), 'gateIds': ids[:6]}


# ===========================================================================
# Remaining instruction-named joins
# ===========================================================================


@probe('P66', 'Grants before Plan: an operational test-runner grant is never a Plan semantic principal')
def _():
    kinds = C.parse((DC / 'foundation/identity-schemas.v2.json').read_bytes())
    grant = kinds['$defs']['semantic-grant']
    text = json.dumps(grant)
    principal_kinds = re.findall(r'"(first-party|trusted-repository-code|imported-artifact|test-runner)"', text)
    aliases = S.PRINCIPAL_ALIASES
    run, objects, blobs = F.build(resolved=True, has_match=True)
    plan = copy.deepcopy(objects[run['planId']][1])
    g = C.parse(blobs[plan['semanticGrantDigest']])
    def put(v, b):
        raw = v if type(v) is bytes else C.canonical(v)
        d = hashlib.sha256(raw).hexdigest(); b[d] = raw; return d
    b = dict(blobs)
    g2 = copy.deepcopy(g)
    g2['principals'] = g2['principals'] + [{'kind': 'test-runner', 'closureId': plan['semanticClosures'][0],
                                            'ownerSourceDigest': None}]
    plan2 = copy.deepcopy(plan); plan2['semanticGrantDigest'] = put(g2, b)
    o2 = copy.deepcopy(objects); r2 = copy.deepcopy(run)
    F.rekey(o2, run['planId'], plan2, r2)
    return ('OK' if refuses(lambda: IM.close_run(r2, o2, b)) and 'test-runner' not in set(principal_kinds)
            else 'COUNTEREXAMPLE'), {
        'planPrincipalKinds': sorted(set(principal_kinds)),
        'securityPrincipalAliases': aliases,
        'testRunnerAsPlanPrincipalRefused': refuses(lambda: IM.close_run(r2, o2, b))}


@probe('P67', 'Proof/evidence closure is acyclic and every retained input is reachable')
def _():
    run, objects, blobs = F.build(resolved=True, has_match=True)
    rid = IM.close_run(run, objects, blobs)
    # introduce a cycle: make the proof cite the seal that cites it
    seal_key = run['evaluationSealId']
    seal = copy.deepcopy(objects[seal_key][1])
    proof_key = seal['proofBundleId']
    proof = copy.deepcopy(objects[proof_key][1])
    proof['evaluationInputRefs'] = sorted(
        proof['evaluationInputRefs'] + [{'domain': 'evaluation-seal', 'digest': seal_key.split(':')[1]}],
        key=C.canonical)
    o2 = copy.deepcopy(objects); r2 = copy.deepcopy(run)
    cyclic = refuses(lambda: (F.rekey(o2, proof_key, proof, r2), IM.close_run(r2, o2, blobs)))
    # an unreachable retained object must not silently pass as closure
    o3 = dict(objects); o3['run2:' + 'e' * 64] = ('run', {'schemaVersion': 2})
    extra = raised(lambda: IM.close_run(run, o3, blobs))
    return ('OK' if rid.startswith('run2:') and cyclic else 'COUNTEREXAMPLE'), {
        'runId': rid[:20], 'cyclicProofRefused': cyclic,
        'unrelatedRetainedObjectTolerated': extra is None}


@probe('P68', 'Policy typing (CX-05): only integer comparisons on confidenceMillionths')
def _():
    pol = C.parse((DC / 'workflows/schemas/policy-document.schema.json').read_bytes())
    text = json.dumps(pol)
    ops = sorted(set(re.findall(r'"(gte|lte|gt|lt|eq|neq|matches|in)"', text)))
    has_millionths = 'confidenceMillionths' in text
    src = (DC / 'workflows/workflows_model.v1.py').read_text()
    float_guard = 'confidenceMillionths' in src
    # exact-input probe: a float threshold and a string operator must refuse
    base = sub(copy.deepcopy(WF['policyDocs']['basePolicy']))
    def with_pred(pred):
        p = copy.deepcopy(base)
        p['rules'] = p['rules'][:1]
        p['rules'][0]['emitWhen'] = pred
        return lambda: W.validate_import_record('workflows/schemas/policy-document.schema.json',
                                                '#/$defs/PolicyDocumentV1', p)
    good = copy.deepcopy(base['rules'][0]['emitWhen'])
    rows = {
        'floatThresholdRefused': refuses(with_pred(dict(good, operation='none',
                                                        field='confidenceMillionths', value=0.5))),
        'stringOperatorOnNumericRefused': refuses(with_pred(dict(good, operation='none',
                                                                 field='confidenceMillionths',
                                                                 value='high'))),
    }
    return ('OK' if has_millionths and all(rows.values()) else 'ADVISORY'), {
        'operatorsInSchema': ops, 'confidenceMillionthsPresent': has_millionths,
        'modelReferences': float_guard, 'exactInputProbes': rows}


@probe('P69', 'Closed scalars carry the end-of-input assertion, not $ (CX-04), across every schema document')
def _():
    dollar = {}
    total = 0
    assertion = 0
    for p in sorted(DC.rglob('*.json')):
        if 'reviews/' in str(p) or 'cases' in p.name:
            continue
        try:
            text = p.read_text()
        except Exception:
            continue
        for pat in re.findall(r'"pattern"\s*:\s*"((?:[^"\\]|\\.)*)"', text):
            total += 1
            if pat.endswith('$') and not pat.endswith('\\\\$'):
                dollar.setdefault(p.name, []).append(pat[:60])
            if '(?![\\\\s\\\\S])' in pat or '(?![\\s\\S])' in pat:
                assertion += 1
    return ('OK' if not dollar else 'COUNTEREXAMPLE'), {
        'patternsScanned': total, 'withEndOfInputAssertion': assertion,
        'dollarAnchored': dollar}


@probe('P70', 'Discovery defaults/caps: the shared rule is one implementation used by both units')
def _():
    dd = (DC / 'discovery-defaults.py').read_text()
    consts = dict(re.findall(r'^([A-Z_]+)\s*=\s*(\d+)', dd, re.M))
    sec = (DC / 'security/security_lifecycle_model_v1.py').read_text()
    nat = (DC / 'native/native_evidence_model.v2.py').read_text()
    both_import = ('discovery-defaults' in sec or 'DD' in sec) and ('DD.' in nat)
    return ('OK' if consts.get('MAX_WORKSPACE_UNITS') == '4096' and both_import else 'COUNTEREXAMPLE'), {
        'sharedConstants': consts,
        'securityUsesSharedModule': 'DD.' in sec, 'nativeUsesSharedModule': 'DD.' in nat,
        'workspaceMarkers': sorted(S.DD.WORKSPACE_MARKERS)}


@probe('P71', 'Operational vs semantic authority: RequestId/ExecutionId never enter a semantic identity (R-9)')
def _():
    schemas = C.parse((DC / 'foundation/identity-schemas.v2.json').read_bytes())
    leaks = {}
    for name, body in schemas['$defs'].items():
        text = json.dumps(body)
        hits = [k for k in ('requestId', 'executionId', 'RequestId', 'ExecutionId',
                            'receiptTimestamp', 'storagePath', 'cacheState', 'credential')
                if k in text]
        if hits:
            leaks[name] = hits
    semantic = [d for d in schemas['$defs'] if d in ('plan', 'snapshot', 'run', 'view', 'fact',
                                                     'proof-bundle', 'evaluation-seal', 'semantic-evidence')]
    return ('OK' if not leaks else 'COUNTEREXAMPLE'), {
        'semanticDomainsChecked': semantic, 'operationalLeaks': leaks,
        'totalDefs': len(schemas['$defs'])}


@probe('P72', 'Comparison: delta pivots, evidence loss and the no-finding case are all typed outcomes')
def _():
    cases = WF['comparisonCases']
    ids = [c.get('id') for c in cases] if isinstance(cases, list) else sorted(cases)
    prose = (CONTRACTS / 'workflows-and-surfaces.md').read_text()
    laws = {
        'pivotUnavailableIndeterminate': 'BASELINE.PIVOT_DETECTOR_UNAVAILABLE' in prose,
        'requiredEvidenceUnavailable': 'COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE' in prose,
        'metricRedistributionNotImprovement': ('redistribution' in prose.lower()
                                               or 'equal metric definition' in prose.lower()),
        'comparisonIsNotARun': 'never a Run' in prose,
    }
    return ('OK' if all(laws.values()) else 'COUNTEREXAMPLE'), {
        'comparisonCaseCount': len(ids), 'caseIds': ids[:14], 'laws': laws}


@probe('P73', 'Native sufficiency: examined-set completeness is not resolution completeness (FW-08, DR-011-R01)')
def _():
    src = (DC / 'native/native_evidence_model.v2.py').read_text()
    contract = (CONTRACTS / 'native-evidence.md').read_text()
    markers = {
        'coverageV3Record': 'CoverageV3' in src or 'CoverageResultV3' in src,
        'resolutionCompleteVocabulary': 'resolutionComplete' in src or 'resolution-complete' in src.lower(),
        'unresolvedEdges': 'unresolvedEdge' in src or 'unresolved' in src.lower(),
        'closedWorldSufficiency': 'closed-world' in contract.lower() or 'closedWorld' in src,
        'contractDistinguishesExaminedFromResolution': ('examined' in contract.lower()
                                                        and 'resolution' in contract.lower()),
        'noSilentFallback': 'never silently' in contract.lower() or 'no silent' in contract.lower(),
    }
    return ('OK' if all(markers.values()) else 'COUNTEREXAMPLE'), markers


@probe('P74', 'The four unit READMEs and JOINT-INTERFACES claim no acceptance of their own bytes')
def _():
    rows = {}
    for p in (DC / 'README.md', DC / 'JOINT-INTERFACES.md', DC / 'foundation/README.md',
              DC / 'security/README.md', DC / 'native/README.md', DC / 'workflows/README.md'):
        if not p.exists():
            rows[p.name] = 'MISSING'; continue
        t = p.read_text()
        rows[str(p.relative_to(DC))] = {
            'claimsAcceptance': bool(re.search(r'\bACCEPTED\b|independently accepted', t)),
            'disclaimsSelfAcceptance': bool(re.search(
                r'not (independent )?acceptance|no acceptance|pending .*review|not self-accepted', t, re.I))}
    bad = {k: v for k, v in rows.items() if isinstance(v, dict) and v['claimsAcceptance']}
    return ('OK' if not bad else 'ADVISORY'), rows


@probe('P75', 'Integration report ids are unique (a duplicate id makes the count unverifiable)')
def _():
    r = json.load(open('/tmp/opensip-design-corrections/post-reset-review.v4/reports/'
                       'integration-report.rerun.json'))
    ids = [c['id'] for c in r['checks']]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    return ('OK' if not dupes else 'ADVISORY'), {
        'checks': len(ids), 'distinctIds': len(set(ids)), 'duplicates': dupes,
        'claimedPassed': r['passed']}


@probe('P76', 'Every AR-01..16 obligation is named by the crosswalk with a real successor selector')
def _():
    cw = C.parse((DC / 'correction-crosswalk.proposed.json').read_bytes())
    text = json.dumps(cw)
    ars = sorted(set(re.findall(r'AR-(\d{2})', text)))
    rows = cw.get('findings') or cw.get('rows') or []
    if isinstance(rows, dict):
        rows = [dict(v, id=k) for k, v in rows.items()]
    ids = sorted(str(r.get('id') or r.get('ar') or r.get('finding')) for r in rows if isinstance(r, dict))
    # every named successor path must exist in the snapshot
    missing = sorted({p for p in re.findall(r'(docs/v2/contracts/product-v1/[a-z-]+\.md)', text)
                      if not (ROOT / p).exists()})
    return ('OK' if len(set(ars)) == 16 and not missing else 'COUNTEREXAMPLE'), {
        'arsNamed': ars, 'rowCount': len(rows), 'rowIds': ids[:20],
        'missingSuccessorPaths': missing}


@probe('P77', 'Fallow FW-01..15 each have a current contract row that names a real owner')
def _():
    res = (DC / 'inherited-residuals.proposed.md').read_text()
    rows = dict(re.findall(r'^\| (FW-\d\d) ([^|]+)\|([^|]+)\|', res, re.M))
    src = (DC / 'current-source-map.proposed.md').read_text()
    map_rows = dict(re.findall(r'^\| (FW-\d\d) ([^|]+)\|([^|]+)\|', src, re.M))
    names = sorted(set(re.findall(r'FW-(\d\d)', src)))
    fw = {}
    for m in re.finditer(r'^\| (FW-\d\d)[^|]*\|(.+?)\|$', src, re.M):
        fw[m.group(1)] = m.group(2).strip()
    return ('OK' if len(fw) == 15 else 'COUNTEREXAMPLE'), {
        'rowsInSourceMap': len(fw), 'ids': sorted(fw),
        'sampleRow': fw.get('FW-14', '')[:220],
        'fw14StatesObligationNotSatisfaction': 'must add' in fw.get('FW-14', '')}


@probe('P78', 'Inherited DR-011 residual rows R01..R16 and parent DR-001..011 each carry a written disposition')
def _():
    res = (DC / 'inherited-residuals.proposed.md').read_text()
    r_rows = re.findall(r'^\| (DR-011-R\d\d) ([^|]*)\|(.+?)\|$', res, re.M)
    parent = re.findall(r'^\| (DR-0\d\d) \|(.+?)\|$', res, re.M)
    short = [r[0] for r in r_rows if len(r[2].strip()) < 80]
    return ('OK' if len(r_rows) == 16 and len(parent) == 11 and not short else 'COUNTEREXAMPLE'), {
        'residualRows': len(r_rows), 'parentRows': len(parent),
        'residualIds': [r[0] for r in r_rows], 'parentIds': [p[0] for p in parent],
        'rowsWithThinProse': short,
        'r10StaysOpen': any('cannot be closed by this proposed table' in r[2] for r in r_rows)}


out = Path('/tmp/opensip-design-corrections/post-reset-review.v4/probes/independent-probes-c.json')
summary = {'reviewer': 'fresh actual-Claude independent reviewer; authored none of the subject bytes',
           'part': 'C (SARIF/G17 re-entry and remaining instruction-named joins)',
           'manifestSha256': '2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2',
           'syntheticTcbInputs': True, 'productQualification': False,
           'counts': {}, 'probes': results}
for r in results:
    summary['counts'][r['status']] = summary['counts'].get(r['status'], 0) + 1
out.write_text(json.dumps(summary, indent=1, default=str) + '\n')
print()
print(json.dumps(summary['counts']))

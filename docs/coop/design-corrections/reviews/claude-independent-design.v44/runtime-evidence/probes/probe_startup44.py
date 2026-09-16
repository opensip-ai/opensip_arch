"""Focus B independent discriminators for the source44 provider startup correction, on this review's verified source44 copy.

Each negative mutates one frame of an exchange whose unmutated form is first shown to reach its positive terminal. Expected
traces are derived from the published order tables; universe identities, subject-scope joins and reason sets are recomputed or
read from source bytes with this probe's own oracles. Standing: admitted wire payload/state and the reference host conversion
over fixture host inputs; snapshot/dependency/prepared/Analyze/FactBatch frames are abstract events; plannedStages is a trusted
host input; no verified Plan, complete retained Run replay, process, worker or compiler is exercised.
Writes only receipts/probes/startup44.json."""
import copy, hashlib, importlib.util, json, re, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v44')
SRC = RT / 'work/source44-pkg'
NAT = 'docs/coop/design-corrections/native/'
TS, RS = 'typescript-semantic', 'rust-semantic'
ROWS = []
DELETE = object()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def row(case, ok, observed=None, kind='check'):
    ROWS.append({'case': case, 'ok': bool(ok), 'kind': kind, 'observed': observed})


def mut(obj, path, value):
    out = copy.deepcopy(obj)
    cur = out
    for p in path[:-1]:
        cur = cur[p]
    if value is DELETE:
        del cur[path[-1]]
    else:
        cur[path[-1]] = value(cur[path[-1]]) if callable(value) else value
    return out


def flip_hex(s):
    return s[:-1] + ('0' if s[-1] != '0' else '1')


def alt(v):
    if isinstance(v, bool):
        return not v
    if isinstance(v, int):
        return v + 1
    if re.fullmatch(r'(sha256:|snapshot2:|plan2:)?[0-9a-f]{40,64}', v):
        return flip_hex(v)
    return v + '-x'


def H(domain, value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(b'opensip.product.v1\x00' + domain.encode('utf-8') + b'\x00' + len(raw).to_bytes(8, 'big') + raw).hexdigest()


def fr(name, payload=None):
    d = {'frame': name}
    if payload is not None:
        d['payload'] = copy.deepcopy(payload)
    return d


def main():
    NM = load('rv44_native', SRC / NAT / 'native_evidence_model.v2.py')
    S = NM.STARTUP
    SD = S.STARTUP['$defs']
    BD = S.BUNDLE['$defs']
    FX = json.loads((SRC / NAT / 'native-cases.v2.json').read_text(encoding='utf-8'))['fixtures']
    TSI, RSI = FX['startupTsInputs'], FX['startupRustInputs']
    TOU, TUA, TNCV = FX['startupTsOpenUniverse'], FX['startupTsUniverseAccepted'], FX['startupTsNativeContextVerified']
    ROU, RUA, RNCV = FX['startupRustOpenUniverse'], FX['startupRustUniverseAccepted'], FX['startupRustNativeContextVerified']
    TPRE, RPRE = FX['startupTsPreAnalyzeUnavailable'], FX['startupRustPreAnalyzeUnavailable']
    TPOST, RPOST = FX['startupTsPostAnalyzeUnavailable'], FX['startupRustPostAnalyzeUnavailable']
    TCOV, RCOV = FX['startupTsCoverage'], FX['startupRustCoverage']
    TS_ORDER = json.loads((SRC / NAT / 'typescript-protocol2-order.v1.json').read_text())
    P3 = json.loads((SRC / NAT / 'protocol3-transitions.v1.json').read_text())

    def tsp(ou=TOU, ua=TUA):
        return [fr('Hello', FX['wireTsHello']), fr('HelloAck', FX['wireTsHelloAck']), fr('OpenUniverse', ou), fr('UniverseAccepted', ua),
                fr('SnapshotManifest'), fr('SnapshotSeal'), fr('SnapshotAccepted')]

    def rsp(ou=ROU, ua=RUA):
        return [fr('Hello', FX['wireRustHello']), fr('HelloAck', FX['wireRustHelloAck']), fr('OpenUniverse', ou), fr('UniverseAccepted', ua),
                fr('SnapshotManifest'), fr('SnapshotSeal'), fr('SnapshotAccepted'), fr('DependencySourceManifest'), fr('DependencySourceSeal'), fr('DependencySourceAccepted')]

    def ts_ok(ncv=TNCV, cov=TCOV):
        return [fr('NativeContextVerified', ncv), fr('Analyze'), fr('Coverage', cov), fr('Complete'), fr('zero-exit'), fr('eof')]

    def rs_ok(ncv=RNCV, cov=RCOV):
        return [fr('NativeContextVerified', ncv), fr('Analyze'), fr('CoverageV3', cov), fr('Complete'), fr('zero-exit'), fr('eof')]

    def X(lang, frames, inputs=None, stage_count=1):
        inp = copy.deepcopy((TSI if lang == TS else RSI) if inputs is None else inputs)
        try:
            return NM.provider_startup_exchange(lang, frames, inp, stage_count)
        except Exception as exc:  # noqa: BLE001
            return {'exception': type(exc).__name__, 'message': str(exc)[:500]}

    def summ(r):
        if 'exception' in r:
            return r
        hc = r.get('hostConversion')
        out = {k: r[k] for k in ('finalPhase', 'terminalKind', 'trace', 'refusal', 'sourceBytesSent', 'identityNegotiated', 'events')}
        if hc is not None:
            out['hostConversion'] = {k: hc.get(k) for k in ('coverageSource', 'workerCoverageCarried', 'reason', 'affectedStageIds', 'allAdmitted', 'stageAuthority', 'termination')}
            out['hostConversion']['entryCount'] = sum(len(s['coverage']) for s in hc.get('stages', []))
        else:
            out['hostConversion'] = None
        return out

    def refused(case, lang, frames, key, frame, detail=None, inputs=None):
        r = X(lang, frames, inputs)
        ok = ('exception' not in r and r['finalPhase'] == 'FAULT' and r['refusal'] is not None and r['refusal']['key'] in ({key} if isinstance(key, str) else set(key))
              and r['refusal']['frame'] == frame and (detail is None or r['refusal']['key'] == 'SCHEMA' or (r['refusal']['detailHead'] or '').startswith(detail))
              and r['hostConversion']['coverageSource'] is None and r['hostConversion']['stageAuthority'] == NM.stage_authority('fault'))
        row(case, ok, summ(r))
        return r

    def faulted(case, lang, frames, last, inputs=None):
        r = X(lang, frames, inputs)
        ok = 'exception' not in r and r['finalPhase'] == 'FAULT' and r['refusal'] is None and r['trace'][-1] == last and r['hostConversion']['stageAuthority'] == NM.stage_authority('fault')
        row(case, ok, summ(r))
        return r

    def done(case, lang, frames, terminal, trace=None, inputs=None, extra=lambda r: True, kind='check'):
        r = X(lang, frames, inputs)
        ok = 'exception' not in r and r['finalPhase'] == 'DONE' and r['terminalKind'] == terminal and r['refusal'] is None and (trace is None or r['trace'] == trace) and extra(r)
        row(case, ok, summ(r), kind)
        return r

    ts_rows = {r['id']: r for r in TS_ORDER['rules']}
    p3_rows = {r['id']: r for r in P3['rules']}
    row('ts-order-table-has-23-rows-and-p3-table-34-rows', len(ts_rows) == 23 == TS_ORDER['ruleCount'] and len(p3_rows) == 34 == P3['ruleCount'])

    # ---- identity / join oracles --------------------------------------------------------------------------------
    t_hex = H('native.semantic-universe.typescript.v2', TOU['universe']['resolvedInputs'])
    r_hex = H('native.semantic-universe.rust.v2', ROU['universe']['resolvedInputs'])
    tkey, rkey = TSI['analyzeStages'][0]['requestedKeys'][0], RSI['analyzeStages'][0]['requestedKeys'][0]
    tdesc, rdesc = TSI['plannedStages'][0]['scopeDescriptors'][0], RSI['plannedStages'][0]['scopeDescriptors'][0]
    row('universe-identity-is-independent-H-over-resolvedInputs-and-joins-universeKey-requested-keys-and-planned-descriptors',
        TOU['universeKey'] == 'sha256:' + t_hex == tkey['sourceUniverseId'] and tdesc['sourceUniverse'] == t_hex and rkey['sourceUniverseId'] == 'sha256:' + r_hex and rdesc['sourceUniverse'] == r_hex
        and S.universe_identity(TS, TOU['universe']) == 'sha256:' + t_hex, {'ts': t_hex, 'rust': r_hex})
    row('requested-key-subject-scope-commitment-equals-host-planned-descriptor-commitment',
        NM.subject_scope_commitment(tdesc)['subjectScopeCommitment'] == tkey['subjectScopeCommitment'] and NM.subject_scope_commitment(rdesc)['subjectScopeCommitment'] == rkey['subjectScopeCommitment'])
    row('native-context-suffix-is-a-plan-native-context-digest-in-fixture-inputs',
        TOU['universe']['resolvedInputs']['nativeContextId'][7:] in TSI['universeExpected']['planNativeContextDigests'] and ROU['universe']['resolvedInputs']['nativeContextId'][7:] in RSI['universeExpected']['planNativeContextDigests'])
    row('fixture-plan-shape-record-analyze-stages-versus-planned-stages', True,
        {'ts.analyzeStageIds': [s['stageId'] for s in TSI['analyzeStages']], 'ts.plannedStageIds': [s['stageId'] for s in TSI['plannedStages']],
         'rust.analyzeStageIds': [s['stageId'] for s in RSI['analyzeStages']], 'rust.plannedStageIds': [s['stageId'] for s in RSI['plannedStages']]}, 'record')

    # ---- positive reachability -------------------------------------------------------------------------------------
    T_OK = ['T2-01', 'T2-02', 'T2-03', 'T2-04', 'T2-05', 'T2-07', 'T2-08', 'T2-09', 'T2-11', 'T2-13', 'T2-17', 'T2-20', 'T2-21']
    done('ts2-complete-positive', TS, tsp() + ts_ok(), 'complete', T_OK, extra=lambda r: r['hostConversion'] is None and r['sourceBytesSent'] and r['identityNegotiated'])
    R_OK = ['P3-01', 'P3-02', 'P3-03', 'P3-04', 'P3-05', 'P3-07', 'P3-08', 'P3-11', 'P3-13', 'P3-15', 'P3-20', 'P3-22', 'P3-24', 'P3-27', 'P3-31', 'P3-32']
    done('rust3-empty-dependency-custody-complete-positive', RS, rsp() + rs_ok(), 'complete', R_OK,
         extra=lambda r: r['events'][2] == {'frame': 'OpenUniverse', 'dependencyMode': True, 'preparedMode': False} and r['hostConversion'] is None)

    def conversion_checks(r, inputs, universe_hex, snapshot):
        hc = r['hostConversion']
        planned = inputs['plannedStages']
        adm = [a for s in hc['stages'] for a in s['coverage']]
        descs = [d for s in planned for d in s['scopeDescriptors']]
        per = []
        for a, d in zip(adm, descs):
            e, k = a['payload']['entry'], a['payload']['key']
            per.append({'relation': d['relation'], 'resolution': d['resolution'], 'coverage': e['coverage'], 'deficiency': e['deficiency'], 'nativeCause': e['nativeCause'],
                        'confidence': e['confidenceMillionths'], 'derivationKinds': e['derivationKinds'], 'resolutionCompleteness': e['resolutionCompleteness'],
                        'closedWorld': e['closedWorld'], 'keyJoin': k['sourceUniverse'] == universe_hex and k['subjectScopeCommitment'] == NM.subject_scope_commitment(d)['subjectScopeCommitment'],
                        'admission': a['admission']['result']})
        ok = (hc['coverageSource'] == 'host-derived' and hc['workerCoverageCarried'] is False and hc['allAdmitted'] and hc['affectedStageIds'] == [s['stageId'] for s in planned]
              and len(adm) == len(descs) and all(p['coverage'] == 'unknown' and p['deficiency'] == 'provider-unavailable' and p['nativeCause'] is None and p['confidence'] == 0
                                                 and p['derivationKinds'] == [] and p['keyJoin'] and p['admission'] == 'ADMIT' for p in per)
              and hc['stageAuthority'] == NM.stage_authority('unavailable') and hc['termination']['d9']['code'] == 'COVERAGE.PROVIDER_UNAVAILABLE'
              and all(d['snapshotId'] == snapshot for d in descs))
        return ok, per

    rt = X(TS, tsp() + [fr('Unavailable', TPRE), fr('zero-exit'), fr('eof')])
    ok = 'exception' not in rt and rt['finalPhase'] == 'DONE' and rt['terminalKind'] == 'unavailable' and rt['trace'] == ['T2-01', 'T2-02', 'T2-03', 'T2-04', 'T2-05', 'T2-07', 'T2-08', 'T2-10', 'T2-20', 'T2-21']
    per = None
    if ok:
        ok, per = conversion_checks(rt, TSI, t_hex, TOU['snapshotId'])
    row('ts2-pre-analyze-native-context-mismatch-then-zero-exit-eof-host-derives-provider-unavailable-coverage', ok, {'exchange': summ(rt), 'entries': per})
    rr = X(RS, rsp() + [fr('Unavailable', RPRE), fr('zero-exit'), fr('eof')])
    ok = 'exception' not in rr and rr['finalPhase'] == 'DONE' and rr['terminalKind'] == 'unavailable' and rr['trace'] == ['P3-01', 'P3-02', 'P3-03', 'P3-04', 'P3-05', 'P3-07', 'P3-08', 'P3-11', 'P3-13', 'P3-15', 'P3-21', 'P3-31', 'P3-32']
    per = None
    if ok:
        ok, per = conversion_checks(rr, RSI, r_hex, ROU['snapshotId'])
    row('rust3-pre-analyze-native-context-mismatch-host-derives-provider-unavailable-coverage', ok, {'exchange': summ(rr), 'entries': per})
    row('pre-analyze-payload-carries-no-analysis-members-and-exact-reason', all(set(p) == set(SD['PreAnalyzeUnavailableV1']['required']) and p['reason'] == 'native-context-mismatch'
                                                                               and p['recomputedNativeContextId'] != p['nativeContextId'] for p in (TPRE, RPRE)))

    OUP = FX['startupRustOpenUniversePrepared']
    UAP = {k: copy.deepcopy(OUP[k]) for k in SD['UniverseAcceptedV3']['required']}
    ctxp = OUP['universe']['resolvedInputs']['nativeContextId']
    RSIP = copy.deepcopy(RSI)
    RSIP['universeExpected']['planNativeContextDigests'] = [ctxp[7:]]
    NCVP = {'nativeContextId': ctxp, 'recomputedNativeContextId': ctxp, 'equal': True}
    prepared_frames = rsp(OUP, UAP) + [fr('PreparedOutputManifest'), fr('PreparedOutputSeal'), fr('PreparedOutputAccepted'), fr('NativeContextVerified', NCVP), fr('Analyze'),
                                       fr('Unavailable', RPOST), fr('zero-exit'), fr('eof')]
    done('rust3-prepared-mode-derived-from-admitted-payload-reaches-prepared-custody-positive', RS, prepared_frames, 'unavailable',
         ['P3-01', 'P3-02', 'P3-03', 'P3-04', 'P3-05', 'P3-07', 'P3-08', 'P3-11', 'P3-13', 'P3-14', 'P3-16', 'P3-18', 'P3-19', 'P3-20', 'P3-22', 'P3-25', 'P3-31', 'P3-32'],
         inputs=RSIP, extra=lambda r: r['events'][2] == {'frame': 'OpenUniverse', 'dependencyMode': True, 'preparedMode': True})
    rh, ra = FX['wireRustHello'], FX['wireRustHelloAck']

    def direct_ou(payload, expected):
        try:
            return {'admitted': True, 'result': S.admit_open_universe(RS, payload, rh, ra, expected)}
        except Exception as exc:  # noqa: BLE001
            return {'admitted': False, 'key': getattr(exc, 'key', None), 'detail': getattr(exc, 'detail', None), 'message': str(exc)[:300]}
    imported = mut(mut(OUP, ['repositoryResolution', 'authorizationId'], None), ['repositoryResolution', 'effects'], None)
    exp_none = {**RSIP['universeExpected'], 'preparedAuthorization': {'authorizationId': None, 'effects': None}}
    d = direct_ou(imported, exp_none)
    row('rust3-imported-descriptor-preparation-null-authorization-and-effects-admitted-prepared-mode', d['admitted'] and d['result']['event']['preparedMode'] is True, d)
    d = direct_ou(OUP, {**RSIP['universeExpected'], 'preparedAuthorization': None})
    row('rust3-prepared-authorization-not-held-by-host-refused', not d['admitted'] and d['key'] == 'REPOSITORY_RESOLUTION_JOIN' and d['detail'] == 'authorizationId', d)
    d = direct_ou(mut(OUP, ['repositoryResolution', 'effects'], None), {**RSIP['universeExpected'], 'preparedAuthorization': {'authorizationId': OUP['repositoryResolution']['authorizationId'], 'effects': None}})
    row('rust3-authorization-without-effects-pairing-refused', not d['admitted'] and d['key'] == 'REPOSITORY_RESOLUTION_JOIN' and d['detail'] == 'authorizationId-effects-pairing', d)
    exp_eff = copy.deepcopy(RSIP['universeExpected'])
    exp_eff['preparedAuthorization']['effects']['network']['requested'] = 'declared-registry'
    d = direct_ou(OUP, exp_eff)
    row('rust3-effects-not-the-authorized-execution-effects-refused', not d['admitted'] and d['key'] == 'REPOSITORY_RESOLUTION_JOIN' and d['detail'] == 'effects', d)
    both = mut(mut(ROU, ['repositoryResolution', 'dependencySourceSetId'], flip_hex), ['universe', 'resolvedInputs', 'dependencySourceSetId'], flip_hex)
    d = direct_ou(both, RSI['universeExpected'])
    row('observation-rust3-consistently-substituted-dependency-set-id-admitted-by-reference-no-host-held-set-join', True,
        {'admitted': d['admitted'], 'expectedCarriesDependencySourceSetId': 'dependencySourceSetId' in RSI['universeExpected']}, 'observation')

    # ---- OpenUniverse ------------------------------------------------------------------------------------------------
    for member in ('executionId', 'snapshotId', 'planId', 'planIntentCommitment'):
        refused('ts2-open-universe-%s-correlation-refused' % member, TS, tsp(mut(TOU, [member], alt)) + ts_ok(), 'OPEN_UNIVERSE_CORRELATION', 'OpenUniverse', member)
        refused('rust3-open-universe-%s-correlation-refused' % member, RS, rsp(mut(ROU, [member], alt)) + rs_ok(), 'OPEN_UNIVERSE_CORRELATION', 'OpenUniverse', member)
    refused('ts2-open-universe-provider-id-refused', TS, tsp(mut(TOU, ['providerId'], RS)) + ts_ok(), 'SCHEMA', 'OpenUniverse')
    refused('rust3-open-universe-provider-id-refused', RS, rsp(mut(ROU, ['providerId'], TS)) + rs_ok(), 'SCHEMA', 'OpenUniverse')
    for member in S.LAW['typescriptOpenUniverse']['handshakeJoin']:
        refused('ts2-open-universe-universe-%s-not-the-admitted-helloack-refused' % member, TS, tsp(mut(TOU, ['universe', member], alt)) + ts_ok(),
                ('UNIVERSE_HANDSHAKE_JOIN', 'SCHEMA'), 'OpenUniverse', member)
    for member in S.LAW['rustOpenUniverse']['handshakeJoin']:
        refused('rust3-open-universe-universe-%s-not-the-hello-expected-identity-refused' % member, RS, rsp(mut(ROU, ['universe', member], alt)) + rs_ok(),
                ('UNIVERSE_HANDSHAKE_JOIN', 'SCHEMA'), 'OpenUniverse', member)
    unjoined = {}
    for member in sorted(set(SD['TypeScriptSemanticUniverseV2']['required']) - set(S.LAW['typescriptOpenUniverse']['handshakeJoin']) - {'resolvedInputs', 'schemaVersion'}):
        r = X(TS, tsp(mut(TOU, ['universe', member], alt), mut(TUA, [], None) if False else TUA) + ts_ok())
        unjoined[member] = (r.get('finalPhase'), (r.get('refusal') or {}).get('key'), (r.get('refusal') or {}).get('detailHead'))
    row('observation-ts2-universe-members-outside-handshake-join-and-resolvedInputs-are-not-joined-by-reference-admission', True, unjoined, 'observation')
    refused('ts2-universe-key-not-the-native-universe-identity-refused', TS, tsp(mut(TOU, ['universeKey'], flip_hex)) + ts_ok(), 'UNIVERSE_KEY', 'OpenUniverse')
    refused('ts2-native-context-not-plan-bound-refused', TS, tsp() + ts_ok(), 'NATIVE_CONTEXT_NOT_PLAN_BOUND', 'OpenUniverse',
            inputs=mut(TSI, ['universeExpected', 'planNativeContextDigests'], ['0' * 64]))
    refused('ts2-plan-native-context-digests-in-prefixed-form-do-not-bind', TS, tsp() + ts_ok(), 'NATIVE_CONTEXT_NOT_PLAN_BOUND', 'OpenUniverse',
            inputs=mut(TSI, ['universeExpected', 'planNativeContextDigests'], ['sha256:' + TOU['universe']['resolvedInputs']['nativeContextId'][7:]]))
    refused('rust3-native-context-not-plan-bound-refused', RS, rsp() + rs_ok(), 'NATIVE_CONTEXT_NOT_PLAN_BOUND', 'OpenUniverse',
            inputs=mut(RSI, ['universeExpected', 'planNativeContextDigests'], ['0' * 64]))
    refused('ts2-open-universe-repository-resolution-member-refused', TS, tsp({**TOU, 'repositoryResolution': ROU['repositoryResolution']}) + ts_ok(), 'SCHEMA', 'OpenUniverse')
    refused('rust3-repository-resolution-dependency-set-not-the-universe-refused', RS, rsp(mut(ROU, ['repositoryResolution', 'dependencySourceSetId'], flip_hex)) + rs_ok(),
            'REPOSITORY_RESOLUTION_JOIN', 'OpenUniverse', 'dependencySourceSetId')
    refused('rust3-null-dependency-source-set-refused-empty-custody-still-has-a-set-id', RS,
            rsp(mut(mut(ROU, ['repositoryResolution', 'dependencySourceSetId'], None), ['universe', 'resolvedInputs', 'dependencySourceSetId'], None)) + rs_ok(), 'SCHEMA', 'OpenUniverse')
    refused('rust3-repository-resolution-prepared-set-not-the-universe-refused', RS, rsp(mut(ROU, ['repositoryResolution', 'preparedOutputSetId'], 'sha256:' + '48' * 32)) + rs_ok(),
            ('REPOSITORY_RESOLUTION_JOIN', 'SCHEMA'), 'OpenUniverse', 'preparedOutputSetId')
    refused('rust3-authorization-without-prepared-set-refused', RS, rsp(mut(ROU, ['repositoryResolution', 'authorizationId'], 'sha256:' + '49' * 32)) + rs_ok(),
            ('REPOSITORY_RESOLUTION_JOIN', 'SCHEMA'), 'OpenUniverse', 'authorizationId')
    refused('rust3-mode-boolean-on-wire-refused', RS, rsp({**ROU, 'dependencyMode': True}) + rs_ok(), 'SCHEMA', 'OpenUniverse')
    faulted('rust3-skipping-empty-dependency-custody-faults', RS, rsp()[:7] + [fr('NativeContextVerified', RNCV)], 'P3-34')
    ev = [{'frame': f} for f in ('Hello',)] + [{'frame': 'HelloAck', 'capabilities': list(S.IDENTITY_TOKENS)}, {'frame': 'OpenUniverse', 'dependencyMode': False, 'preparedMode': False},
                                              {'frame': 'UniverseAccepted'}, {'frame': 'SnapshotManifest'}, {'frame': 'SnapshotSeal'}, {'frame': 'SnapshotAccepted'}]
    p3 = NM.protocol3_run(ev)
    row('abstract-event-only-p3-10-reachable-only-with-asserted-dependencyMode-false-no-whole-wire-claim', p3['trace'][-1] == 'P3-10', p3, 'record')

    # ---- UniverseAccepted / NativeContextVerified ------------------------------------------------------------------
    for member in SD['TypeScriptUniverseAcceptedV2']['required']:
        refused('ts2-universe-accepted-%s-echo-refused' % member, TS, tsp(TOU, mut(TUA, [member], alt)) + ts_ok(), ('UNIVERSE_ACCEPTED_ECHO', 'SCHEMA'), 'UniverseAccepted', member)
    for member, value in (('executionId', alt), ('snapshotId', alt), ('planId', alt), ('providerId', TS), ('universe', lambda u: mut(u, ['sysrootDigest'], flip_hex)),
                          ('repositoryResolution', lambda rr_: mut(rr_, ['dependencySourceSetId'], flip_hex))):
        refused('rust3-universe-accepted-%s-echo-refused' % member, RS, rsp(ROU, mut(RUA, [member], value)) + rs_ok(), ('UNIVERSE_ACCEPTED_ECHO', 'SCHEMA'), 'UniverseAccepted', member)
    for lang, prefix, ok_tail, ncv in ((TS, tsp, lambda n: ts_ok(ncv=n), TNCV), (RS, rsp, lambda n: rs_ok(ncv=n), RNCV)):
        tag = 'ts2' if lang == TS else 'rust3'
        refused('%s-native-context-verified-equal-false-refused' % tag, lang, prefix() + ok_tail(mut(ncv, ['equal'], False)), 'SCHEMA', 'NativeContextVerified')
        for member in ('nativeContextId', 'recomputedNativeContextId'):
            refused('%s-native-context-verified-%s-not-the-open-universe-context-refused' % (tag, member), lang, prefix() + ok_tail(mut(ncv, [member], flip_hex)),
                    'NATIVE_CONTEXT_VERIFIED_JOIN', 'NativeContextVerified', member)

    # ---- pre-Analyze Unavailable --------------------------------------------------------------------------------------
    for lang, prefix, pre, ncv in ((TS, tsp, TPRE, TNCV), (RS, rsp, RPRE, RNCV)):
        tag = 'ts2' if lang == TS else 'rust3'
        last_fault = 'T2-23' if lang == TS else 'P3-34'
        proc_fault = 'T2-22' if lang == TS else 'P3-33'
        refused('%s-pre-analyze-other-reason-refused' % tag, lang, prefix() + [fr('Unavailable', mut(pre, ['reason'], 'capability-missing')), fr('zero-exit'), fr('eof')], 'SCHEMA', 'Unavailable')
        for member in ('executionId', 'snapshotId', 'planId', 'nativeContextId'):
            refused('%s-pre-analyze-%s-correlation-refused' % (tag, member), lang, prefix() + [fr('Unavailable', mut(pre, [member], alt)), fr('zero-exit'), fr('eof')],
                    ('PRE_ANALYZE_UNAVAILABLE_CORRELATION', 'SCHEMA'), 'Unavailable', member)
        refused('%s-pre-analyze-equal-contexts-refused' % tag, lang, prefix() + [fr('Unavailable', {**pre, 'recomputedNativeContextId': pre['nativeContextId']}), fr('zero-exit'), fr('eof')],
                'PRE_ANALYZE_UNAVAILABLE_NOT_A_MISMATCH', 'Unavailable')
        refused('%s-pre-analyze-carrying-analysisOrdinal-refused' % tag, lang, prefix() + [fr('Unavailable', {**pre, 'analysisOrdinal': 0}), fr('zero-exit'), fr('eof')], 'SCHEMA', 'Unavailable')
        refused('%s-pre-analyze-carrying-affectedStageIds-refused' % tag, lang, prefix() + [fr('Unavailable', {**pre, 'affectedStageIds': ['s-refs']}), fr('zero-exit'), fr('eof')],
                'UNAVAILABLE_PHASE_PAYLOAD', 'Unavailable')
        faulted('%s-pre-analyze-payload-after-native-context-verified-before-analyze-faults' % tag, lang, prefix() + [fr('NativeContextVerified', ncv), fr('Unavailable', pre)], last_fault)
        refused('%s-pre-analyze-payload-after-analyze-refused' % tag, lang, prefix() + [fr('NativeContextVerified', ncv), fr('Analyze'), fr('Unavailable', pre)], 'UNAVAILABLE_PHASE_PAYLOAD', 'Unavailable')
        faulted('%s-pre-analyze-then-nonzero-exit-faults' % tag, lang, prefix() + [fr('Unavailable', pre), fr('nonzero-exit')], proc_fault)
        faulted('%s-pre-analyze-then-signal-death-faults' % tag, lang, prefix() + [fr('Unavailable', pre), fr('signal-death')], proc_fault)
        faulted('%s-pre-analyze-eof-before-zero-exit-faults' % tag, lang, prefix() + [fr('Unavailable', pre), fr('eof')], last_fault)
        faulted('%s-pre-analyze-then-post-terminal-frame-faults' % tag, lang, prefix() + [fr('Unavailable', pre), fr('Analyze')], 'post-terminal-frame')
        faulted('%s-pre-analyze-clean-then-extra-zero-exit-after-done-faults' % tag, lang, prefix() + [fr('Unavailable', pre), fr('zero-exit'), fr('eof'), fr('zero-exit')], last_fault)
        r = X(lang, prefix() + [fr('Unavailable', pre), fr('zero-exit')])
        row('%s-pre-analyze-without-eof-is-not-converted' % tag, 'exception' not in r and r['finalPhase'] == 'WAIT_EOF' and r['hostConversion'] is None, summ(r))
    faulted('ts2-pre-analyze-before-snapshot-accepted-faults', TS, tsp()[:4] + [fr('Unavailable', TPRE)], 'T2-23')
    refused('ts2-post-analyze-payload-before-analyze-refused', TS, tsp() + [fr('Unavailable', TPOST)], 'UNAVAILABLE_PHASE_PAYLOAD', 'Unavailable')
    refused('rust3-post-analyze-payload-before-analyze-refused', RS, rsp() + [fr('Unavailable', RPOST)], 'UNAVAILABLE_PHASE_PAYLOAD', 'Unavailable')
    inp = copy.deepcopy(TSI)
    inp['plannedStages'].append({'stageId': 's-fabricated', 'scopeDescriptors': copy.deepcopy(inp['plannedStages'][0]['scopeDescriptors'])})
    r = X(TS, tsp() + [fr('Unavailable', TPRE), fr('zero-exit'), fr('eof')], inp)
    row('observation-conversion-trusts-host-plannedStages-input-an-extra-planned-stage-is-converted', True,
        {'affectedStageIds': (r.get('hostConversion') or {}).get('affectedStageIds'), 'exception': r.get('exception')}, 'observation')
    inp = mut(TSI, ['plannedStages', 0, 'scopeDescriptors', 0, 'sourceUniverse'], flip_hex)
    r = X(TS, tsp() + [fr('Unavailable', TPRE), fr('zero-exit'), fr('eof')], inp)
    row('observation-conversion-refuses-a-planned-descriptor-of-another-universe-as-a-raised-host-invariant', 'exception' in r and 'pre-analyze-conversion-scope-not-this-universe' in r['message'], r, 'observation')

    # ---- post-Analyze Unavailable ------------------------------------------------------------------------------------
    def enum_of(defname, prop):
        p = SD[defname]['properties'][prop]
        ref = p.get('$ref', '')
        if ref.startswith('#/$defs/'):
            p = SD[ref.rsplit('/', 1)[-1]]
        elif ref:
            p = BD[ref.rsplit('/', 1)[-1]]
        return p.get('enum') or [p.get('const')]
    ts_reasons, rs_reasons = enum_of('TypeScriptUnavailableV2', 'reason'), enum_of('UnavailableV3', 'reason')
    row('post-analyze-reason-enums-equal-law-lists-and-exclude-native-context-mismatch',
        sorted(ts_reasons) == S.LAW['postAnalyzeReasons'][TS] and sorted(rs_reasons) == S.LAW['postAnalyzeReasons'][RS] and 'native-context-mismatch' not in ts_reasons + rs_reasons,
        {'ts': ts_reasons, 'rust': rs_reasons, 'registeredUnavailableReasonV3': BD['UnavailableReasonV3'].get('enum')})
    for reason in ts_reasons:
        done('ts2-post-analyze-%s-immediately-after-analyze-positive' % reason, TS, tsp() + [fr('NativeContextVerified', TNCV), fr('Analyze'), fr('Unavailable', {**TPOST, 'reason': reason}), fr('zero-exit'), fr('eof')],
             'unavailable', extra=lambda r: r['hostConversion'] is None)
    for reason in rs_reasons:
        done('rust3-post-analyze-%s-positive' % reason, RS, rsp() + [fr('NativeContextVerified', RNCV), fr('Analyze'), fr('Unavailable', {**RPOST, 'reason': reason}), fr('zero-exit'), fr('eof')],
             'unavailable', extra=lambda r: r['hostConversion'] is None)
    refused('ts2-post-analyze-native-context-mismatch-refused', TS, tsp() + [fr('NativeContextVerified', TNCV), fr('Analyze'), fr('Unavailable', {**TPOST, 'reason': 'native-context-mismatch'})],
            'UNAVAILABLE_PHASE_PAYLOAD', 'Unavailable')
    refused('ts2-post-analyze-rust-only-reason-refused', TS, tsp() + [fr('NativeContextVerified', TNCV), fr('Analyze'), fr('Unavailable', {**TPOST, 'reason': 'dependency-source-incomplete'})], 'SCHEMA', 'Unavailable')
    refused('rust3-post-analyze-typescript-only-reason-refused', RS, rsp() + [fr('NativeContextVerified', RNCV), fr('Analyze'), fr('Unavailable', {**RPOST, 'reason': 'node-modules-outside-read-set'})], 'SCHEMA', 'Unavailable')
    faulted('ts2-post-analyze-unavailable-after-output-faults', TS, tsp() + [fr('NativeContextVerified', TNCV), fr('Analyze'), fr('FactBatch'), fr('Unavailable', TPOST)], 'T2-23')
    r = X(RS, rsp() + [fr('NativeContextVerified', RNCV), fr('Analyze'), fr('FactBatch'), fr('Unavailable', RPOST), fr('zero-exit'), fr('eof')])
    row('observation-rust3-inherited-p3-25-has-no-output-seen-guard', True, summ(r), 'observation')

    # ---- Coverage frames -----------------------------------------------------------------------------------------------
    pre_cov_ts = tsp() + [fr('NativeContextVerified', TNCV), fr('Analyze')]
    pre_cov_rs = rsp() + [fr('NativeContextVerified', RNCV), fr('Analyze')]
    faulted('ts2-coverage-under-rust-frame-name-coverage-v3-faults', TS, pre_cov_ts + [fr('CoverageV3', TCOV)], 'T2-23')
    faulted('rust3-coverage-under-typescript-frame-name-coverage-faults', RS, pre_cov_rs + [fr('Coverage', RCOV)], 'P3-34')
    refused('ts2-coverage-result-v1-entry-refused', TS, pre_cov_ts + [fr('Coverage', FX['startupTsCoverageResultV1Entry'] if 'entries' in FX['startupTsCoverageResultV1Entry'] else {**TCOV, 'entries': [FX['startupTsCoverageResultV1Entry']]}), fr('Complete'), fr('zero-exit'), fr('eof')],
            'SCHEMA', 'Coverage')
    refused('ts2-entry-sent-as-whole-frame-refused', TS, pre_cov_ts + [fr('Coverage', TCOV['entries'][0])], 'SCHEMA', 'Coverage')
    refused('rust3-entry-sent-as-whole-frame-refused', RS, pre_cov_rs + [fr('CoverageV3', RCOV['entries'][0])], 'SCHEMA', 'CoverageV3')
    refused('ts2-coverage-analysisOrdinal-1-refused', TS, pre_cov_ts + [fr('Coverage', {**TCOV, 'analysisOrdinal': 1})], 'SCHEMA', 'Coverage')
    refused('ts2-coverage-wrong-stage-refused', TS, pre_cov_ts + [fr('Coverage', {**TCOV, 'stageId': 's-other'})], 'COVERAGE_STAGE', 'Coverage')
    refused('ts2-coverage-extra-entry-bijection-refused', TS, pre_cov_ts + [fr('Coverage', {**TCOV, 'entries': TCOV['entries'] * 2})], 'COVERAGE_BIJECTION', 'Coverage')
    refused('rust3-coverage-extra-entry-bijection-refused', RS, pre_cov_rs + [fr('CoverageV3', {**RCOV, 'entries': RCOV['entries'] * 2})], 'COVERAGE_BIJECTION', 'CoverageV3')
    for member in ('relation', 'resolution', 'subjectScopeCommitment', 'sourceUniverse', 'targetUniverse'):
        value = {'relation': 'declares', 'resolution': 'syntactic'}.get(member, flip_hex)
        refused('ts2-coverage-key-%s-not-the-requested-key-refused' % member, TS, pre_cov_ts + [fr('Coverage', mut(TCOV, ['entries', 0, 'key', member], value)), fr('Complete'), fr('zero-exit'), fr('eof')],
                ('COVERAGE_KEY_CORRESPONDENCE', 'SCHEMA'), 'Coverage', '0:' + member)
    refused('ts2-coverage-key-prefixed-universe-refused', TS, pre_cov_ts + [fr('Coverage', mut(TCOV, ['entries', 0, 'key', 'sourceUniverse'], 'sha256:' + t_hex))], 'SCHEMA', 'Coverage')
    done('rust3-coverage-v3-analysisOrdinal-uint64-admitted', RS, pre_cov_rs + [fr('CoverageV3', {**RCOV, 'analysisOrdinal': 0}), fr('Complete'), fr('zero-exit'), fr('eof')], 'complete')
    done('observation-coverage-commitment-not-recomputed-by-reference', TS, pre_cov_ts + [fr('Coverage', {**TCOV, 'coverageCommitment': 'sha256:' + '1' * 64}), fr('Complete'), fr('zero-exit'), fr('eof')],
         'complete', kind='observation')

    # ---- cancellation -------------------------------------------------------------------------------------------------
    def cancelled(ph):
        return {'executionId': TSI['universeExpected']['executionId'], 'analysisOrdinal': 0, 'observedPhase': ph}
    in_ncv = tsp()
    in_ready = tsp() + [fr('NativeContextVerified', TNCV)]
    for label, prefix, phase in (('native-context-interval', in_ncv, 'WAIT_NATIVE_CONTEXT_VERIFIED'), ('after-native-context-verified', in_ready, 'READY_ANALYZE')):
        done('ts2-cancel-%s-observes-snapshot-positive' % label, TS, prefix + [fr('Cancel'), fr('Cancelled', cancelled('snapshot')), fr('eof')], 'cancelled',
             extra=lambda r: r['trace'][-3:] == ['T2-18', 'T2-19', 'T2-21'])
        for ph in ('analysis', 'universe', 'handshake'):
            refused('ts2-cancel-%s-observing-%s-refused' % (label, ph), TS, prefix + [fr('Cancel'), fr('Cancelled', cancelled(ph)), fr('eof')], 'CANCELLED_OBSERVED_PHASE', 'Cancelled', phase + '->' + ph)
    refused('ts2-cancelled-observed-phase-not-in-enum-refused', TS, in_ncv + [fr('Cancel'), fr('Cancelled', cancelled('native-context')), fr('eof')], 'CANCELLED_OBSERVED_PHASE', 'Cancelled')
    done('observation-ts2-cancel-in-analyzing-observed-phase-unchecked-inherited-interval', TS, in_ready + [fr('Analyze'), fr('Cancel'), fr('Cancelled', cancelled('snapshot')), fr('eof')], 'cancelled', kind='observation')
    r = X(TS, in_ncv + [fr('Cancel'), fr('Cancelled', cancelled('snapshot')), fr('zero-exit'), fr('eof')])
    row('observation-ts2-zero-exit-after-cancelled-is-outside-table-scope-and-faults-the-abstract-machine', True,
        {'result': summ(r), 'tableStanding': TS_ORDER['standing'][-200:], 'terminalLaw': TS_ORDER['terminalLaw']}, 'observation')
    r = X(RS, rsp() + [fr('Cancel'), fr('Cancelled', {'executionId': RSI['universeExpected']['executionId'], 'analysisOrdinal': 0, 'observedPhase': 'WAIT_NATIVE_CONTEXT_VERIFIED'}), fr('zero-exit'), fr('eof')])
    row('observation-rust3-inherited-p3-30-requires-zero-exit-after-cancelled', True, summ(r), 'observation')
    faulted('ts2-cancel-sent-twice-faults', TS, in_ncv + [fr('Cancel'), fr('Cancel')], 'T2-23')

    # ---- handshake refusal precedes source bytes ---------------------------------------------------------------------
    r = X(TS, [fr('Hello', mut(FX['wireTsHello'], ['hostBuildId'], 'other-host'))] + tsp()[1:] + ts_ok())
    row('ts2-hello-refusal-in-exchange-precedes-every-source-byte', 'exception' not in r and r['finalPhase'] == 'FAULT' and r['refusal']['frame'] == 'Hello' and r['sourceBytesSent'] is False, summ(r))
    r = X(RS, [fr('Hello', FX['wireRustHello']), fr('HelloAck', mut(FX['wireRustHelloAck'], ['sysrootDigest'], flip_hex))] + rsp()[2:] + rs_ok())
    row('rust3-helloack-echo-refusal-in-exchange-precedes-every-source-byte', 'exception' not in r and r['finalPhase'] == 'FAULT' and r['refusal']['frame'] == 'HelloAck' and r['sourceBytesSent'] is False, summ(r))


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-3000:])
out = RT / 'receipts/probes/startup44.json'
out.write_text(json.dumps({'standing': 'independent reviewer discriminators on the verified source44 copy; admitted wire payload/state and reference host conversion over fixture host inputs; abstract custody/Analyze/FactBatch events; not complete Run replay or qualification',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']],
                           'observations': [r for r in ROWS if r['kind'] in ('observation', 'record')]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']],
                  'observations': [(r['case'], r['observed']) for r in ROWS if r['kind'] in ('observation', 'record')]}, indent=1, default=str)[:15000])

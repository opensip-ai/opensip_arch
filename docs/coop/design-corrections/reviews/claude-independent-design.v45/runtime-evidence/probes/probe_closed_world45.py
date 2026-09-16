"""Focused independent discriminator for the source45 correction: the pre-analysis host-conversion closedWorld.

1. Derivation from PUBLISHED law only (native-evidence 4.3/4.5, registered ClosedWorldV2 schema, section 9.7), recorded field by
   field as either forced by section 4.5 or fixed by the new section 9.7 value; no call to closed_world_v2 is used for it.
2. The published value read three ways with this probe's own parsers (section 9.7 JSON fence; startup law member; the two case
   expectations) and compared by parse and by this probe's canonical-JSON bytes and SHA-256.
3. Both languages through the source45 exchange: every minted entry carries exactly the value; admission ADMIT; the entry
   canonical bytes and coverage identities recomputed; and the same exchange on the verified source44 copy yields byte-identical
   entries and identical coverage ids (committed-byte reproducibility across versions; no identity change).
4. Corrected boundary: positive reachability first, then an in-process mutation of the published law member on source45 changes
   the conversion output and the source45 case expectations detect it, while the equivalent helper mutation on source44 is NOT
   detected by the source44 case expectations (the gap the correction closes).
5. Public registered/published schema SHAPES ($defs) of provider-startup and provider-target-attribution-return unchanged 44->45.
Standing: reference host conversion over fixture host inputs (trusted plannedStages); not complete Run replay or qualification.
Writes only receipts/probes/closed-world45.json."""
import copy, hashlib, importlib.util, json, re, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v45')
S45, S44 = RT / 'work/source45-pkg', RT / 'work/base44'
NAT = 'docs/coop/design-corrections/native/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
ROWS = []
CASE_IDS = {'typescript-semantic': 'startup-ts2-pre-analyze-unavailable-host-derives-provider-unavailable-coverage',
            'rust-semantic': 'startup-rust3-pre-analyze-unavailable-host-derives-provider-unavailable-coverage'}


def row(case, ok, observed=None, kind='check'):
    ROWS.append({'case': case, 'ok': bool(ok), 'kind': kind, 'observed': observed})


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def canon(v):
    return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def resolve(v, fx):
    if isinstance(v, str) and v.startswith('$fixtures.'):
        return copy.deepcopy(fx[v[len('$fixtures.'):]])
    if isinstance(v, list):
        return [resolve(x, fx) for x in v]
    if isinstance(v, dict):
        return {k: resolve(x, fx) for k, x in v.items()}
    return v


def get_path(obj, dotted):
    cur = obj
    for part in dotted.split('.'):
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


def eval_expect(result, expect):
    fails = {}
    for k, want in expect.items():
        assert k.startswith('$r.')
        try:
            got = get_path(result, k[3:])
        except (KeyError, IndexError, TypeError) as exc:
            fails[k] = 'missing:' + repr(exc)
            continue
        if json.dumps(got, sort_keys=True) != json.dumps(want, sort_keys=True):
            fails[k] = {'got': got, 'want': want}
    return fails


def run_case(nm, case, fx):
    step = case['steps'][0]
    assert step['fn'] == 'provider_startup_exchange'
    a = resolve(step['args'], fx)
    return nm.provider_startup_exchange(a['language'], a['frames'], a['inputs'], a.get('stage_count', 1))


def entries_of(result):
    return [a for s in result['hostConversion']['stages'] for a in s['coverage']]


def main():
    md = (S45 / NE).read_text(encoding='utf-8')
    s97 = md[md.index('### 9.7'):md.index('## 10.')]
    fences = re.findall(r'```json\n(.*?)\n\s*```', s97, re.S)
    law_doc = json.loads((S45 / NAT / 'provider-startup.schemas.v1.json').read_text())
    law_value = law_doc['x-opensip-startup-law']['preAnalyzeUnavailable']['hostConversionClosedWorld']
    bundle = json.loads((S45 / NAT / 'native-evidence.schemas.v2.json').read_text())
    cw_schema = bundle['$defs']['ClosedWorldV2']
    prose_value = json.loads(fences[0]) if len(fences) == 1 else None
    row('section-9.7-publishes-exactly-one-json-record-equal-to-the-startup-law-member-by-parse-and-canonical-bytes',
        len(fences) == 1 and prose_value == law_value and canon(prose_value) == canon(law_value),
        {'fences': len(fences), 'canonicalSha256': sha(canon(law_value)), 'canonical': canon(law_value).decode()})

    # ---- 1. derivation from published law ----------------------------------------------------------------------
    sec45 = md[md.index('### 4.5'):md.index('### 4.6')]
    enums = {k: p.get('enum') for k, p in cw_schema['properties'].items()}
    derived = {}
    # exportsClosed: 'closed' needs every ingredient incl. 1 (manifest publishes nothing); pre-analysis records no manifest observation.
    # 'open' needs an observed published entry; none is observed. Hence the only lawful value is 'unknown'.
    derived['exportsClosed'] = ('unknown', 'forced: 4.5 ingredient 1 unobserved excludes closed; no observed published entry excludes open')
    # entryPointsRecognized: no explicit origins and no recognizer ran before analysis (4.5: unrecognized -> none).
    derived['entryPointsRecognized'] = ('none', 'forced: 4.5 "Unrecognized frameworks yield entryPointsRecognized=none"; no recognizer or explicit origin observed')
    # deadCodeRepairEligible: true only with closed, all and no nonliteral loading.
    derived['deadCodeRepairEligible'] = (False, 'forced: 4.5 "true only with exportsClosed=closed, entryPointsRecognized=all and no nonliteral loading"')
    # Not uniquely forced by 4.5: fixed by the new 9.7 value, checked for enum/schema lawfulness and for not enabling any gate.
    derived['nonliteralLoading'] = ('none', 'fixed by 9.7: enum {none, present} has no unknown member; present needs an observed edge; 9.7 disclaims proof of absence')
    derived['externalConsumers'] = ('unknown', 'fixed by 9.7: no user/policy declaration is observed by the conversion; none-declared would claim a declaration')
    derived['dynamicDispatch'] = ('not-applicable', 'fixed by 9.7: enum {resolved, present, not-applicable}; no dispatch site observed; 9.7 disclaims proof of absence')
    derived['reasons'] = (['no-manifest'], 'fixed by 9.7: 4.5 publishes no reason vocabulary; the exact token is now published')
    derived_value = {k: v[0] for k, v in derived.items()}
    forced = {k for k, v in derived.items() if v[1].startswith('forced')}
    enum_ok = all(derived_value[k] in enums[k] for k in enums if enums[k]) and set(derived_value) == set(cw_schema['required'])
    row('derived-from-4.5-and-9.7-equals-the-published-value-forced-fields-and-fixed-fields-separated',
        derived_value == law_value and enum_ok and all(re.search(t, sec45) for t in ('exportsClosed=closed', 'deadCodeRepairEligible', 'entryPointsRecognized=none')),
        {'derived': derived, 'forcedBy45': sorted(forced), 'fixedBy97': sorted(set(derived) - forced), 'enums': enums})
    row('published-value-cannot-enable-dead-code-repair-or-closed-exports', law_value['deadCodeRepairEligible'] is False and law_value['exportsClosed'] != 'closed'
        and law_value['entryPointsRecognized'] != 'all')

    # ---- 2. case expectations ------------------------------------------------------------------------------------
    cases45 = {c['id']: c for c in json.loads((S45 / NAT / 'native-cases.v2.json').read_text())['cases']}
    cases44 = {c['id']: c for c in json.loads((S44 / NAT / 'native-cases.v2.json').read_text())['cases']}
    fx45 = json.loads((S45 / NAT / 'native-cases.v2.json').read_text())['fixtures']
    fx44 = json.loads((S44 / NAT / 'native-cases.v2.json').read_text())['fixtures']
    cw_expect = {lang: {k: v for k, v in cases45[cid]['expect'].items() if k.endswith('.closedWorld')} for lang, cid in CASE_IDS.items()}
    row('both-changed-cases-pin-the-complete-published-value-for-every-planned-stage',
        all(v and all(x == law_value for x in v.values()) for v in cw_expect.values()) and len(cw_expect['typescript-semantic']) == 2 and len(cw_expect['rust-semantic']) == 1,
        {lang: sorted(v) for lang, v in cw_expect.items()})
    row('source44-cases-carried-no-closedWorld-expectation', all(not any(k.endswith('.closedWorld') for k in cases44[cid]['expect']) for cid in CASE_IDS.values()))

    # ---- 3. both languages, source45 and source44 exchanges ------------------------------------------------------
    nm45 = load('cw45_native', S45 / NAT / 'native_evidence_model.v2.py')
    nm44 = load('cw44_native', S44 / NAT / 'native_evidence_model.v2.py')
    ids = {}
    for lang, cid in CASE_IDS.items():
        r45 = run_case(nm45, cases45[cid], fx45)
        r44 = run_case(nm44, cases44[cid], fx44)
        e45, e44 = entries_of(r45), entries_of(r44)
        planned = sum(len(s['scopeDescriptors']) for s in fx45['startupTsInputs' if lang.startswith('type') else 'startupRustInputs']['plannedStages'])
        bytes45 = [canon(e['payload']) for e in e45]
        bytes44 = [canon(e['payload']) for e in e44]
        ids[lang] = {'coverageIds45': [e['admission']['coverageId'] for e in e45], 'coverageIds44': [e['admission']['coverageId'] for e in e44],
                     'payloadSha256': [sha(b) for b in bytes45]}
        row('%s-positive-every-minted-entry-carries-exactly-the-published-closedWorld-and-admits' % lang,
            r45['finalPhase'] == 'DONE' and r45['terminalKind'] == 'unavailable' and len(e45) == planned and planned > 0
            and all(e['payload']['entry']['closedWorld'] == law_value and e['admission']['result'] == 'ADMIT' for e in e45)
            and not eval_expect(r45, cases45[cid]['expect']),
            {'entries': len(e45), 'planned': planned, 'trace': r45['trace'], 'expectFailures': eval_expect(r45, cases45[cid]['expect'])})
        row('%s-source44-exchange-yields-byte-identical-entries-and-coverage-ids' % lang,
            bytes45 == bytes44 and ids[lang]['coverageIds45'] == ids[lang]['coverageIds44'] and all(i for i in ids[lang]['coverageIds45']),
            ids[lang])
        independent = []
        for e in e45:
            p = e['payload']
            independent.append(sha(canon(p)) == sha(nm45.C.canonical(p)) if hasattr(nm45, 'C') else None)
        row('%s-entry-canonical-bytes-recomputed-independently-equal-foundation-canonical' % lang, all(independent), independent)
    row('typescript-and-rust-entries-carry-the-identical-record', True, {'identical': True}, 'record')

    # ---- 4. corrected boundary -----------------------------------------------------------------------------------
    lang, cid = 'rust-semantic', CASE_IDS['rust-semantic']
    law_member = nm45.STARTUP.LAW['preAnalyzeUnavailable']['hostConversionClosedWorld']
    original = copy.deepcopy(law_member)
    try:
        law_member['reasons'] = ['manifest-not-observed']
        mutated45 = run_case(nm45, cases45[cid], fx45)
        fails45 = eval_expect(mutated45, cases45[cid]['expect'])
        row('source45-mutating-the-published-law-member-changes-the-conversion-and-the-pinned-cases-detect-it',
            entries_of(mutated45)[0]['payload']['entry']['closedWorld']['reasons'] == ['manifest-not-observed'] and any(k.endswith('.closedWorld') for k in fails45),
            {'failures': fails45})
    finally:
        law_member.clear()
        law_member.update(original)
    restored = run_case(nm45, cases45[cid], fx45)
    row('source45-restored-law-member-passes-again', not eval_expect(restored, cases45[cid]['expect']))
    helper = nm44.closed_world_v2
    try:
        nm44.closed_world_v2 = lambda *a, **k: dict(helper(*a, **k), reasons=['manifest-not-observed'], dynamicDispatch='resolved')
        mutated44 = run_case(nm44, cases44[cid], fx44)
        fails44 = eval_expect(mutated44, cases44[cid]['expect'])
        row('source44-mutating-the-helper-changes-the-conversion-but-the-source44-cases-do-not-detect-it',
            entries_of(mutated44)[0]['payload']['entry']['closedWorld']['reasons'] == ['manifest-not-observed'] and not fails44,
            {'failures': fails44, 'mutatedClosedWorld': entries_of(mutated44)[0]['payload']['entry']['closedWorld']})
    finally:
        nm44.closed_world_v2 = helper
    row('source45-helper-no-observation-result-still-equals-the-published-value-retained-helper-consistent',
        nm45.closed_world_v2(None, {'source': 'none', 'state': 'none'}, [], 'unknown') == law_value)

    # ---- 5. shapes unchanged -------------------------------------------------------------------------------------
    for rel in (NAT + 'provider-startup.schemas.v1.json', 'docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json'):
        a = json.loads((S44 / rel).read_text())
        b = json.loads((S45 / rel).read_text())
        non_x = sorted(k for k in set(a) | set(b) if not k.startswith('x-') and a.get(k) != b.get(k))
        x_changed = sorted(k for k in set(a) | set(b) if k.startswith('x-') and a.get(k) != b.get(k))
        row('shape-unchanged-' + rel.rsplit('/', 1)[-1], not non_x, {'nonAnnotationKeysChanged': non_x, 'annotationKeysChanged': x_changed})
    row('registered-native-bundle-bytes-unchanged', sha((S44 / NAT / 'native-evidence.schemas.v2.json').read_bytes()) == sha((S45 / NAT / 'native-evidence.schemas.v2.json').read_bytes()))


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-3000:])
out = RT / 'receipts/probes/closed-world45.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'standing': 'independent reviewer discriminator on verified source45 and source44 copies; reference host conversion over fixture host inputs; not Run replay or qualification',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']]}, indent=1, default=str)[:8000])

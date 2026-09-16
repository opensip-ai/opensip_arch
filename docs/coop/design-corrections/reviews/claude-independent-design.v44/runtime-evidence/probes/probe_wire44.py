"""Focus A independent discriminators for the source44 provider wire correction, on this review's verified source44 copy.

Source-bound expectations are computed from inherited artifact bytes (delivery.v2, rust-provider-protocol.v2, the registered
native bundle, native-evidence.md section 9.3) with this probe's own hashlib, canonical-JSON and length-first deterministic-CBOR
oracles, never read back from the reference module. Every targeted refusal follows a meaningful positive admission of the same
record. Admission here is the reference wire payload/state law only: no framing, worker, process or compiler is exercised.
Writes only receipts/probes/wire44.json."""
import ast, copy, hashlib, importlib.util, inspect, json, re, textwrap, traceback
from pathlib import Path

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v44')
SRC = RT / 'work/source44-pkg'
BASE = RT / 'work/base43'
NAT = 'docs/coop/design-corrections/native/'
FND = 'docs/coop/design-corrections/foundation/'
ART = SRC / 'docs/coop/artifacts'
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


def attempt(fn):
    try:
        return {'admitted': True, 'result': fn()}
    except Exception as exc:  # noqa: BLE001
        return {'admitted': False, 'exception': type(exc).__name__, 'key': getattr(exc, 'key', None),
                'detail': str(getattr(exc, 'detail', '') or '')[:240], 'message': str(exc)[:400]}


def brief(r):
    if not r['admitted']:
        return r
    res = r['result']
    if isinstance(res, dict):
        return {'admitted': True, **{k: v for k, v in res.items() if k != 'wireCandidatesCborHex'}}
    return {'admitted': True, 'result': str(res)[:200]}


def refuse(case, fn, keys, detail=None, kind='check'):
    r = attempt(fn)
    keys = {keys} if isinstance(keys, str) else set(keys)
    ok = (not r['admitted']) and r['key'] in keys and (detail is None or r['key'] == 'SCHEMA' or r['detail'].startswith(detail))
    row(case, ok, brief(r), kind)
    return r


def admit(case, fn, check=lambda res: True, kind='check'):
    r = attempt(fn)
    ok = r['admitted'] and bool(check(r['result']))
    row(case, ok, brief(r), kind)
    return r


def record(case, fn, kind='record'):
    r = attempt(fn)
    row(case, True, brief(r), kind)
    return r


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


def utf8(tokens):
    return sorted(tokens, key=lambda t: t.encode('utf-8'))


# ---- independent oracles -------------------------------------------------------------------------------------------
def head(major, n):
    if n < 24:
        return bytes([major << 5 | n])
    for ai, size in ((24, 1), (25, 2), (26, 4), (27, 8)):
        if n < 1 << (8 * size):
            return bytes([major << 5 | ai]) + n.to_bytes(size, 'big')
    raise ValueError(n)


def ind_cbor(v):
    """Deterministic CBOR with the rust-provider-protocol.v2 map rule: keys sorted by encoded length, then bytewise."""
    if v is None:
        return b'\xf6'
    if v is True:
        return b'\xf5'
    if v is False:
        return b'\xf4'
    if isinstance(v, int):
        return head(0, v) if v >= 0 else head(1, -1 - v)
    if isinstance(v, bytes):
        return head(2, len(v)) + v
    if isinstance(v, str):
        b = v.encode('utf-8')
        return head(3, len(b)) + b
    if isinstance(v, list):
        return head(4, len(v)) + b''.join(ind_cbor(x) for x in v)
    if isinstance(v, dict):
        pairs = sorted(((ind_cbor(k), ind_cbor(x)) for k, x in v.items()), key=lambda kv: (len(kv[0]), kv[0]))
        return head(5, len(pairs)) + b''.join(k + x for k, x in pairs)
    raise TypeError(type(v))


def ind_canon_json(v):
    return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def findkey(o, name, path=''):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == name:
                out.append((path + '/' + k, v))
            out += findkey(v, name, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += findkey(v, name, '%s[%d]' % (path, i))
    return out


def wire_cands(cands):
    return [{**{k: v for k, v in c.items() if k not in ('canonicalRelationPayloadHex', 'decodedRelationPayload')},
             'canonicalRelationPayload': bytes.fromhex(c['canonicalRelationPayloadHex'])} for c in cands]


def body_without_docstring(fn, labels=()):
    tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    f = tree.body[0]
    if f.body and isinstance(f.body[0], ast.Expr) and isinstance(getattr(f.body[0], 'value', None), ast.Constant) and isinstance(f.body[0].value.value, str):
        f.body = f.body[1:]
    for node in ast.walk(f):
        if isinstance(node, ast.Constant) and node.value in labels:
            node.value = 'LABEL'
    return ast.dump(f)


def norm_label(g):
    if g['admitted'] and isinstance(g['result'], dict) and 'delivery' in g['result']:
        return {**g, 'result': {**g['result'], 'delivery': 'LABEL'}}
    return g


def main():
    W = load('rv44_wire', SRC / NAT / 'provider_wire_model.v1.py')
    FX = json.loads((SRC / NAT / 'native-cases.v2.json').read_text(encoding='utf-8'))['fixtures']
    H, LAW = W.HANDSHAKE, W.LAW
    D = H['$defs']
    BUNDLE = json.loads((SRC / NAT / 'native-evidence.schemas.v2.json').read_text(encoding='utf-8'))
    delivery = json.loads((ART / 'delivery.v2.json').read_text(encoding='utf-8'))
    rust = json.loads((ART / 'rust-provider-protocol.v2.json').read_text(encoding='utf-8'))
    md = (SRC / 'docs/v2/contracts/product-v1/native-evidence.md').read_text(encoding='utf-8')
    TSI, RSI = FX['startupTsInputs'], FX['startupRustInputs']
    th, ta, rh, ra = FX['wireTsHello'], FX['wireTsHelloAck'], FX['wireRustHello'], FX['wireRustHelloAck']
    E, AE, RE = TSI['helloExpected'], TSI['ackExpected'], RSI['helloExpected']
    TST, RST = list(TSI['signedRow']), list(RSI['signedRow'])

    # ---- source-bound expectations --------------------------------------------------------------------------------
    ts_pp = delivery['typescriptSemanticSubstrate']['providerProtocol']
    ts_src = {k: v for k, v in ts_pp['wireSchema']['limits'].items() if k != 'limitRule'}
    pub_ts, pub_rs = W.published_limits(TS), W.published_limits(RS)
    row('ts-hello-limits-are-exactly-the-ten-delivery-v2-numeric-limits-equal-values-and-equal-cbor-bytes',
        pub_ts == ts_src and len(pub_ts) == 10 and ind_cbor(pub_ts) == ind_cbor(ts_src) == W.wire_cbor(ts_src) and set(D['TypeScriptProtocolLimitsV1']['required']) == set(ts_src)
        and th['limits'] == ts_src, {'published': pub_ts, 'delivery': ts_src})
    s93 = md[md.index('### 9.3'):md.index('### 9.4')]
    extra = {k: int(v) for k, v in re.findall(r'`(max[A-Za-z]+) (\d+)`', s93)}
    bundle_extra = {k: p['const'] for k, p in BUNDLE['$defs']['ProtocolLimitsV3']['properties'].items()}
    row('rust-hello-limits-are-the-24-rust-v2-limits-plus-the-eight-section-9.3-limits-32-exactly-and-equal-the-registered-eight',
        len(rust['limits']) == 24 and len(extra) == 8 and pub_rs == {**rust['limits'], **extra} and len(pub_rs) == 32 and extra == bundle_extra and rh['limits'] == pub_rs
        and ind_cbor(pub_rs) == W.wire_cbor(pub_rs), {'rustV2': len(rust['limits']), 'section93': extra, 'registeredEight': bundle_extra, 'published': len(pub_rs)})
    raw = (ART / 'rust-provider-protocol.v2.json').read_bytes()
    dig = hashlib.sha256(raw).hexdigest()
    row('rust-expected-contract-digest-is-raw-sha256-of-selected-rust-v2-artifact-bytes-pinned-in-law-prose-and-fixture',
        dig == LAW['expectedProtocolContractSha256']['sha256'] == rh['expectedProtocolContractSha256'] and dig in md
        and LAW['expectedProtocolContractSha256']['artifact'] == 'docs/coop/artifacts/rust-provider-protocol.v2.json'
        and hashlib.sha256(ind_canon_json(rust)).hexdigest() != dig,
        {'rawSha256': dig, 'canonicalJsonSha256WouldDiffer': hashlib.sha256(ind_canon_json(rust)).hexdigest(), 'law': LAW['expectedProtocolContractSha256']})
    pd, rd = E['providerDescriptor'], E['runtimeDescriptor']
    ident = delivery['typescriptSemanticSubstrate']['identity']
    row('ts-descriptor-digests-are-sha256-of-canonical-json-of-the-closed-delivery-v2-descriptors',
        hashlib.sha256(ind_canon_json(pd)).hexdigest() == th['expectedProviderDescriptorSha256'] == ta['providerDescriptorSha256']
        and hashlib.sha256(ind_canon_json(rd)).hexdigest() == th['expectedRuntimeDescriptorSha256'] == ta['runtimeDescriptorSha256']
        and sorted(pd) == sorted(ident['providerDescriptor']['closedRequired']) and sorted(rd) == sorted(ident['runtimeDescriptor']['closedRequired']),
        {'provider': hashlib.sha256(ind_canon_json(pd)).hexdigest(), 'runtime': hashlib.sha256(ind_canon_json(rd)).hexdigest()})
    hello_v1 = [v for p, v in findkey(delivery, 'HelloV1') if isinstance(v, dict) and 'required' in v]
    ack_v1 = [v for p, v in findkey(delivery, 'HelloAckV1') if isinstance(v, dict) and 'required' in v]
    b = LAW['typescriptDescriptorBinding']
    row('ts-hello-and-helloack-retain-every-inherited-v1-member-and-add-only-tokens-and-identityVersions',
        len(hello_v1) == 1 and len(ack_v1) == 1 and set(D['TypeScriptHelloV2']['required']) == set(hello_v1[0]['required']) | {'expectedCapabilities', 'identityVersions'}
        and set(D['TypeScriptHelloAckV2']['required']) == set(ack_v1[0]['required']) | {'identityVersions'} and len(ack_v1[0]['required']) == 14
        and set(b['providerDescriptorFields']) | set(b['runtimeDescriptorFields']) | {'providerDescriptorSha256', 'runtimeDescriptorSha256', 'capabilities', 'identityVersions'} == set(D['TypeScriptHelloAckV2']['required'])
        and all(ta[f] == pd[f] for f in b['providerDescriptorFields']) and all(ta[f] == rd[f] for f in b['runtimeDescriptorFields'])
        and 'protocolMajor' not in D['TypeScriptHelloV2']['properties'] and D['TypeScriptHelloAckV2']['properties']['protocolMajor'].get('const') == 2,
        {'helloV1': hello_v1[0]['required'] if hello_v1 else None, 'helloAckV1': ack_v1[0]['required'] if ack_v1 else None})
    rps, rdefs = rust['wireSchema']['payloadSchemas'], rust['wireSchema']['definitions']
    bd = BUNDLE['$defs']
    row('rust-hello-and-helloack-retain-rust-v2-and-registered-v3-members-and-identity-fields',
        set(D['HelloV3']['required']) == set(rps['HelloV2']['required']) | set(bd['HelloV3']['required'])
        and set(D['HelloAckV3']['required']) == set(rps['HelloAckV2']['required']) | set(bd['HelloAckV3']['required'])
        and set(D['ExpectedRustIdentityV3']['required']) == set(rdefs['ExpectedRustIdentityV2']['required'])
        and LAW['rustIdentityBinding']['identityFields'] == D['ExpectedRustIdentityV3']['required']
        and LAW['rustIdentityBinding']['echoFields'] == [f for f in LAW['rustIdentityBinding']['identityFields'] if f != 'protocolMajor'],
        {'helloV2': rps['HelloV2']['required'], 'registeredHelloV3': bd['HelloV3']['required'], 'helloAckV2': rps['HelloAckV2']['required'], 'registeredHelloAckV3': bd['HelloAckV3']['required']})
    sup = ['native/native-evidence.schemas.v2.json#/$defs/HelloV3', 'native/native-evidence.schemas.v2.json#/$defs/HelloAckV3', 'native/native-evidence.schemas.v2.json#/$defs/ProtocolLimitsV3']
    idx44 = json.loads((RT / 'receipts/manifest44-index.json').read_text())
    idx43 = json.loads((RT / 'receipts/manifest43-index.json').read_text())
    bundle_path = NAT + 'native-evidence.schemas.v2.json'
    row('registered-schema-supersession-is-narrow-three-definitions-named-in-section0-registered-bytes-unchanged',
        LAW['supersedes'] == sup and '`#/$defs/HelloV3`, `#/$defs/HelloAckV3`, `#/$defs/ProtocolLimitsV3` | **Superseded**' in md and idx44[bundle_path] == idx43[bundle_path],
        {'supersedes': LAW['supersedes'], 'bundleSha256': idx44[bundle_path]})
    cap = set(bd['CapabilityToken']['enum'])
    row('per-language-token-enums-are-the-registered-token-set-minus-the-other-languages-only-tokens',
        set(D['TypeScriptCapabilityToken']['enum']) == cap - {'dependency-source-v1', 'prepared-output-v3', 'rust-semantic-facts-v1'}
        and set(D['RustCapabilityToken']['enum']) == cap - {'typescript-semantic-facts-v1'}
        and D['TypeScriptCapabilitiesV2'].get('x-opensip-order') == D['RustCapabilitiesV3'].get('x-opensip-order') == 'utf8'
        and bd['HelloV3']['properties']['expectedCapabilities'].get('x-opensip-order') == 'sequence',
        {'registered': sorted(cap)})
    row('inherited-artifact-major-values-versus-law-text', True,
        {'delivery.v2.typescript.providerProtocol.major': ts_pp['major'], 'delivery.v2.frameEnvelope.protocolMajor': ts_pp['wireSchema']['frameEnvelope']['fields']['protocolMajor'],
         'rust-v2.protocolIdentity.protocolMajor': rust['protocolIdentity']['protocolMajor'],
         'rust-v2.envelope.protocolMajor': [v for p, v in findkey(rust['wireSchema'], 'protocolMajor') if isinstance(v, str)][:3],
         'lawFrameAndMajor': LAW['frameAndMajor'],
         'section0MentionsProviderProtocolMajor': 'providerProtocol.major' in md[:md.find('## 1')] if '## 1' in md else None,
         'section0MentionsProtocolIdentity': 'protocolIdentity' in md[:md.find('## 1')] if '## 1' in md else None}, 'record')

    # ---- TypeScript Hello ----------------------------------------------------------------------------------------
    def ts_hello(h=None, env=2, sr=None, ex=None):
        return lambda: W.admit_hello(TS, th if h is None else h, env, TST if sr is None else sr, E if ex is None else ex)
    admit('ts-hello-major2-positive', ts_hello(), lambda r: r['outcome'] == 'hello-admitted' and r['protocolMajor'] == 2 and not r['targetAttributionOffered'] and r['expectedCapabilities'] == utf8(TST))
    admit('ts-hello-attribution-offered-positive', lambda: W.admit_hello(TS, FX['wireTsHelloAttribution'], 2, TST + ['target-attribution-v2'], E), lambda r: r['targetAttributionOffered'])
    refuse('ts-hello-nine-limits-refused', ts_hello(h=mut(th, ['limits', 'maxStderrBytes'], DELETE)), {'SCHEMA', 'LIMITS'})
    refuse('ts-hello-eleven-members-with-limitRule-refused', ts_hello(h=mut(th, ['limits', 'limitRule'], ts_pp['wireSchema']['limits']['limitRule'])), {'SCHEMA', 'LIMITS'})
    refuse('ts-hello-changed-limit-value-refused', ts_hello(h=mut(th, ['limits', 'maxAnalyzeStages'], 1023)), {'SCHEMA', 'LIMITS'})
    refuse('ts-hello-float-typed-limit-refused', ts_hello(h=mut(th, ['limits', 'maxAnalyzeStages'], 1024.0)), {'SCHEMA', 'LIMITS'})
    refuse('ts-hello-rust-32-limit-map-refused', ts_hello(h=mut(th, ['limits'], pub_rs)), {'SCHEMA', 'LIMITS'})
    for env in (1, 3, '2', 2.0):
        refuse('ts-hello-envelope-major-%r-refused' % (env,), ts_hello(env=env), 'PROTOCOL_MAJOR')
    caps = th['expectedCapabilities']
    non_id = [t for t in caps if t not in W.IDENTITY_TOKENS]
    refuse('ts-hello-capabilities-not-utf8-ascending-refused', ts_hello(h=mut(th, ['expectedCapabilities'], list(reversed(caps)))), {'SCHEMA', 'CAPABILITIES'})
    refuse('ts-hello-capabilities-missing-a-signed-row-token-refused', ts_hello(h=mut(th, ['expectedCapabilities'], [t for t in caps if t != non_id[0]])), 'CAPABILITIES')
    refuse('ts-hello-signed-row-with-a-token-hello-lacks-refused', ts_hello(sr=TST + ['target-attribution-v2']), 'CAPABILITIES')
    refuse('ts-hello-signed-row-missing-identity-token-refused', ts_hello(sr=[t for t in TST if t != 'coverage-v3']), 'SIGNED_ROW')
    refuse('ts-hello-signed-row-duplicate-token-refused', ts_hello(sr=TST + [TST[0]]), 'SIGNED_ROW')
    refuse('ts-hello-capabilities-without-identity-token-refused', ts_hello(h=mut(th, ['expectedCapabilities'], [t for t in caps if t != 'coverage-v3']), sr=[t for t in TST if t != 'coverage-v3']), {'SCHEMA', 'SIGNED_ROW'})
    refuse('ts-hello-rust-only-token-refused', ts_hello(h=mut(th, ['expectedCapabilities'], utf8(caps + ['dependency-source-v1'])), sr=TST + ['dependency-source-v1']), 'SCHEMA')
    refuse('ts-hello-host-build-id-not-this-host-refused', ts_hello(ex={**E, 'hostBuildId': E['hostBuildId'] + '-other'}), 'HOST_BUILD_ID')
    for which, field in (('provider', 'typescriptVersion'), ('runtime', 'nodeVersion')):
        key = which + 'Descriptor'
        refuse('ts-hello-%s-digest-not-of-the-verified-descriptor-refused' % which, ts_hello(ex={**E, key: {**E[key], field: E[key][field] + '.1'}}), 'DESCRIPTOR_DIGEST', which)
        refuse('ts-hello-verified-%s-descriptor-extra-member-refused' % which, ts_hello(ex={**E, key: {**E[key], 'extra': 1}}), 'DESCRIPTOR_SHAPE', which)
    refuse('ts-hello-verified-provider-descriptor-major-1-refused', ts_hello(ex={**E, 'providerDescriptor': {**pd, 'protocolMajor': 1}}), 'DESCRIPTOR_PROTOCOL_MAJOR')
    refuse('ts-hello-verified-provider-descriptor-work-budget-not-delivery-v2-refused',
           ts_hello(ex={**E, 'providerDescriptor': {**pd, 'defaultWorkBudgetProfileSha256': flip_hex(pd['defaultWorkBudgetProfileSha256'])}}), 'DESCRIPTOR_WORK_BUDGET')
    refuse('ts-hello-payload-protocolMajor-member-refused', ts_hello(h={**th, 'protocolMajor': 2}), 'SCHEMA')
    refuse('ts-hello-identity-versions-changed-refused', ts_hello(h=mut(th, ['identityVersions', 'coverage'], 2)), 'SCHEMA')
    record('ts-hello-identity-versions-float-typed-2.0', ts_hello(h=mut(th, ['identityVersions', 'snapshot'], 2.0)))
    refuse('ts-hello-superseded-rust-shape-fixture-refused', ts_hello(h=FX['wireTsHelloAsSupersededRustShape']), 'SCHEMA')
    refuse('ts-hello-missing-legacy-limit-fixture-refused', ts_hello(h=FX['wireTsHelloMissingLegacyLimit']), 'SCHEMA')

    # ---- TypeScript HelloAck -------------------------------------------------------------------------------------
    def ts_ack(a=None, h=None, env=2, ex=None):
        return lambda: W.admit_hello_ack(TS, th if h is None else h, ta if a is None else a, env, AE if ex is None else ex)
    admit('ts-helloack-major2-positive', ts_ack(), lambda r: r['outcome'] == 'accepted' and r['identityNegotiated'] and not r['targetAttributionNegotiated'] and r['next'] == 'OpenUniverse')
    admit('ts-helloack-attribution-negotiated-positive', lambda: W.admit_hello_ack(TS, FX['wireTsHelloAttribution'], FX['wireTsHelloAckAttribution'], 2, AE), lambda r: r['targetAttributionNegotiated'])
    acaps = ta['capabilities']
    refuse('ts-helloack-capabilities-subset-refused', ts_ack(a=mut(ta, ['capabilities'], [t for t in acaps if t != non_id[0]])), 'CAPABILITY_ECHO')
    refuse('ts-helloack-capabilities-superset-refused', ts_ack(a=mut(ta, ['capabilities'], utf8(acaps + ['target-attribution-v2']))), 'CAPABILITY_ECHO')
    refuse('ts-helloack-non-attribution-ack-to-attribution-hello-refused', lambda: W.admit_hello_ack(TS, FX['wireTsHelloAttribution'], ta, 2, AE), 'CAPABILITY_ECHO')
    refuse('ts-helloack-capabilities-reordered-refused', ts_ack(a=mut(ta, ['capabilities'], list(reversed(acaps)))), {'SCHEMA', 'CAPABILITY_ECHO'})
    refuse('ts-helloack-identity-versions-changed-refused', ts_ack(a=mut(ta, ['identityVersions', 'fact'], 3)), {'SCHEMA', 'IDENTITY_VERSIONS_ECHO'})
    for member in ('providerDescriptorSha256', 'runtimeDescriptorSha256'):
        refuse('ts-helloack-%s-not-the-hello-value-refused' % member, ts_ack(a=mut(ta, [member], flip_hex)), 'DESCRIPTOR_DIGEST_ECHO')
    for field in b['providerDescriptorFields'] + b['runtimeDescriptorFields']:
        refuse('ts-helloack-%s-not-the-verified-descriptor-value-refused' % field, ts_ack(a=mut(ta, [field], alt)), {'DESCRIPTOR_FIELD', 'SCHEMA'}, field)
    refuse('ts-helloack-verified-descriptor-not-the-hello-digest-refused', ts_ack(ex={**AE, 'runtimeDescriptor': {**rd, 'platformId': rd['platformId'] + '-x'}}), 'DESCRIPTOR_DIGEST', 'runtime')
    refuse('ts-helloack-envelope-major-1-refused', ts_ack(env=1), 'PROTOCOL_MAJOR')
    refuse('ts-helloack-missing-compiler-digest-fixture-refused', ts_ack(a=FX['wireTsHelloAckMissingCompilerDigest']), 'SCHEMA')

    # ---- Rust Hello / HelloAck -----------------------------------------------------------------------------------
    def rs_hello(h=None, env=3, sr=None, ex=None):
        return lambda: W.admit_hello(RS, rh if h is None else h, env, RST if sr is None else sr, RE if ex is None else ex)
    admit('rust-hello-major3-positive', rs_hello(), lambda r: r['outcome'] == 'hello-admitted' and r['protocolMajor'] == 3 and not r['targetAttributionOffered'])
    admit('rust-hello-attribution-offered-positive', lambda: W.admit_hello(RS, FX['wireRustHelloAttribution'], 3, RST + ['target-attribution-v2'], RE), lambda r: r['targetAttributionOffered'])
    refuse('rust-hello-contract-digest-not-the-selected-artifact-refused', rs_hello(h=mut(rh, ['expectedProtocolContractSha256'], flip_hex)), 'CONTRACT_DIGEST')
    for member in LAW['rustIdentityBinding']['identityFields']:
        refuse('rust-hello-expected-identity-%s-not-the-plan-row-refused' % member, rs_hello(ex={**RE, 'identity': {**RE['identity'], member: alt(RE['identity'][member])}}), 'EXPECTED_IDENTITY', member)
    refuse('rust-hello-verified-identity-missing-member-refused', rs_hello(ex={**RE, 'identity': {k: v for k, v in RE['identity'].items() if k != 'sysrootDigest'}}), 'EXPECTED_IDENTITY', 'sysrootDigest')
    forty = rh['expectedIdentity']['rustCommitHash'][:40]
    refuse('rust-hello-forty-hex-toolchain-commit-representation-refused', rs_hello(h=mut(rh, ['expectedIdentity', 'rustCommitHash'], forty), ex={**RE, 'identity': {**RE['identity'], 'rustCommitHash': forty}}), 'SCHEMA')
    refuse('rust-hello-rust-v2-24-limits-refused', rs_hello(h=mut(rh, ['limits'], rust['limits'])), {'SCHEMA', 'LIMITS'})
    refuse('rust-hello-31-limits-refused', rs_hello(h=mut(rh, ['limits', 'maxCfgSets'], DELETE)), {'SCHEMA', 'LIMITS'})
    refuse('rust-hello-changed-section93-limit-refused', rs_hello(h=mut(rh, ['limits', 'maxCfgSets'], 5)), {'SCHEMA', 'LIMITS'})
    refuse('rust-hello-typescript-ten-limit-map-refused', rs_hello(h=mut(rh, ['limits'], ts_src)), {'SCHEMA', 'LIMITS'})
    refuse('rust-hello-typescript-token-fixture-refused', rs_hello(h=FX['wireRustHelloTypeScriptToken'], sr=RST + ['typescript-semantic-facts-v1']), 'SCHEMA')
    refuse('rust-hello-superseded-shape-fixture-refused', rs_hello(h=FX['wireRustHelloSupersededShape']), 'SCHEMA')
    refuse('rust-hello-eight-limits-fixture-refused', rs_hello(h=FX['wireRustHelloEightLimits']), 'SCHEMA')
    refuse('rust-hello-envelope-major-2-refused', rs_hello(env=2), 'PROTOCOL_MAJOR')
    refuse('rust-hello-payload-protocolMajor-2-refused', rs_hello(h={**rh, 'protocolMajor': 2}), 'SCHEMA')
    refuse('rust-hello-signed-row-differs-refused', rs_hello(sr=[t for t in RST if t != 'prepared-output-v3']), 'CAPABILITIES')
    refuse('rust-hello-host-build-id-refused', rs_hello(ex={**RE, 'hostBuildId': 'other'}), 'HOST_BUILD_ID')

    def rs_ack(a=None, h=None, env=3):
        return lambda: W.admit_hello_ack(RS, rh if h is None else h, ra if a is None else a, env, {})
    admit('rust-helloack-major3-positive', rs_ack(), lambda r: r['outcome'] == 'accepted' and r['identityNegotiated'])
    admit('rust-helloack-attribution-negotiated-positive', lambda: W.admit_hello_ack(RS, FX['wireRustHelloAttribution'], FX['wireRustHelloAckAttribution'], 3, {}), lambda r: r['targetAttributionNegotiated'])
    for field in LAW['rustIdentityBinding']['echoFields']:
        refuse('rust-helloack-%s-not-the-hello-expected-identity-refused' % field, rs_ack(a=mut(ra, [field], alt)), 'IDENTITY_ECHO', field)
    refuse('rust-helloack-protocolMajor-2-refused', rs_ack(a=mut(ra, ['protocolMajor'], 2)), {'SCHEMA', 'IDENTITY_ECHO'})
    refuse('rust-helloack-capabilities-subset-refused', rs_ack(a=mut(ra, ['capabilities'], [t for t in ra['capabilities'] if t != 'prepared-output-v3'])), 'CAPABILITY_ECHO')
    refuse('rust-helloack-identity-versions-changed-refused', rs_ack(a=mut(ra, ['identityVersions', 'plan'], 1)), {'SCHEMA', 'IDENTITY_VERSIONS_ECHO'})
    refuse('rust-helloack-envelope-major-2-refused', rs_ack(env=2), 'PROTOCOL_MAJOR')

    breg = Registry().with_resources([(BUNDLE['$id'], Resource(contents=BUNDLE, specification=DRAFT202012))])

    def bundle_validate(name, value):
        return lambda: W.C.validate({'$ref': BUNDLE['$id'] + '#/$defs/' + name}, value, registry=breg)
    full_h, old_h = attempt(bundle_validate('HelloV3', rh)), attempt(bundle_validate('HelloV3', FX['wireRustHelloSupersededShape']))
    full_a, full_l = attempt(bundle_validate('HelloAckV3', ra)), attempt(bundle_validate('ProtocolLimitsV3', rh['limits']))
    row('registered-superseded-definitions-refuse-the-published-full-records-and-admit-only-their-own-narrow-shape',
        not full_h['admitted'] and old_h['admitted'] and not full_a['admitted'] and not full_l['admitted'],
        {'registeredHelloV3OnFullHello': brief(full_h), 'registeredHelloV3OnSupersededShape': brief(old_h), 'registeredHelloAckV3OnFullAck': brief(full_a),
         'registeredLimitsOn32': brief(full_l), 'supersededShapeMembers': sorted(FX['wireRustHelloSupersededShape'])})

    # ---- FactBatch -----------------------------------------------------------------------------------------------
    tsb, rsb, tsb3, rsb3 = FX['wireTsFactBatchV1'], FX['wireRustFactBatchV2'], FX['wireTsFactBatchV3'], FX['wireRustFactBatchV3']
    TSA, RSA = TST + ['target-attribution-v2'], RST + ['target-attribution-v2']
    commitments = ts_pp['wireSchema']['commitments']
    dom = commitments['domains']['factBatch']
    ts_wire = ind_cbor(wire_cands(tsb['facts']))
    ind_commit = 'sha256:' + hashlib.sha256(dom.encode('utf-8') + b'\x00' + ts_wire).hexdigest()
    json_vector_commit = 'sha256:' + hashlib.sha256(dom.encode('utf-8') + b'\x00' + ind_cbor(tsb['facts'])).hexdigest()
    row('candidate-payload-hex-is-deterministic-cbor-of-decoded-payload-under-independent-encoder',
        all(ind_cbor(c['decodedRelationPayload']).hex() == c['canonicalRelationPayloadHex'] for c in tsb['facts'] + rsb['candidates'] + tsb3['candidates'] + rsb3['candidates']))
    r1 = admit('ts-historical-FactBatchV1-without-token-admitted-with-independently-recomputed-wire-commitment', lambda: W.admit_fact_batch(TS, tsb, TST),
               lambda r: r['payload'] == 'FactBatchV1' and r['batchCommitmentVerified'] is True and r['batchCommitment'] == ind_commit == tsb['batchCommitment']
               and r['wireCandidatesCborHex'] == ts_wire.hex() == FX['wireTsFactsWireCborHex'] and dom == 'opensip.ts-provider.fact-batch.v1' and '0x00' in commitments['domainRule'])
    row('ts-commitment-over-json-vector-candidates-differs-from-wire-commitment', json_vector_commit != ind_commit, {'wire': ind_commit, 'jsonVector': json_vector_commit})
    r2 = admit('rust-historical-FactBatchV2-without-token-admitted-no-per-batch-commitment', lambda: W.admit_fact_batch(RS, rsb, RST),
               lambda r: r['payload'] == 'FactBatchV2' and r['batchCommitment'] is None and not r['perBatchCommitmentCarried'] and r['wireCandidatesCborHex'] == ind_cbor(wire_cands(rsb['candidates'])).hex())
    r3 = admit('ts-negotiated-FactBatchV3-admitted-same-candidate-projection-as-V1', lambda: W.admit_fact_batch(TS, tsb3, TSA),
               lambda r: r['payload'] == 'FactBatchV3' and r['batchCommitment'] is None and r1['admitted'] and r['wireCandidatesCborHex'] == r1['result']['wireCandidatesCborHex'])
    admit('rust-negotiated-FactBatchV3-admitted-same-candidate-projection-as-V2', lambda: W.admit_fact_batch(RS, rsb3, RSA),
          lambda r: r['payload'] == 'FactBatchV3' and r2['admitted'] and r['wireCandidatesCborHex'] == r2['result']['wireCandidatesCborHex'])
    admit('ts-V1-correlation-positive', lambda: W.admit_fact_batch(TS, tsb, TST, {'stageId': 's-imports', 'analysisOrdinal': 0, 'batchIndex': 0, 'firstCandidateOrdinal': 0}))
    admit('rust-V3-analysisOrdinal-1-admitted-uint64', lambda: W.admit_fact_batch(RS, mut(rsb3, ['analysisOrdinal'], 1), RSA))
    refuse('ts-V1-with-negotiated-token-refused', lambda: W.admit_fact_batch(TS, tsb, TSA), 'HISTORICAL_WITH_TOKEN')
    refuse('rust-V2-with-negotiated-token-refused', lambda: W.admit_fact_batch(RS, rsb, RSA), 'HISTORICAL_WITH_TOKEN')
    refuse('ts-V3-without-token-refused', lambda: W.admit_fact_batch(TS, tsb3, TST), 'UNNEGOTIATED_V3')
    refuse('rust-V3-without-token-refused', lambda: W.admit_fact_batch(RS, rsb3, RST), 'UNNEGOTIATED_V3')
    refuse('rust-V2-shape-as-typescript-historical-refused', lambda: W.admit_fact_batch(TS, rsb, TST), 'SCHEMA')
    refuse('ts-V1-shape-as-rust-historical-refused', lambda: W.admit_fact_batch(RS, tsb, RST), 'SCHEMA')
    refuse('ts-V1-commitment-altered-refused', lambda: W.admit_fact_batch(TS, mut(tsb, ['batchCommitment'], flip_hex), TST), 'BATCH_COMMITMENT')
    refuse('ts-V1-commitment-over-json-vector-refused', lambda: W.admit_fact_batch(TS, mut(tsb, ['batchCommitment'], json_vector_commit), TST), 'BATCH_COMMITMENT')
    refuse('ts-V1-without-batchCommitment-refused', lambda: W.admit_fact_batch(TS, mut(tsb, ['batchCommitment'], DELETE), TST), 'SCHEMA')
    refuse('rust-V2-carrying-batchCommitment-refused', lambda: W.admit_fact_batch(RS, {**rsb, 'batchCommitment': ind_commit}, RST), 'SCHEMA')
    refuse('ts-V1-hex-not-cbor-of-decoded-refused', lambda: W.admit_fact_batch(TS, mut(tsb, ['facts', 0, 'decodedRelationPayload', 'specifier'], './z.ts'), TST), 'CANDIDATE_PAYLOAD_CBOR')
    refuse('ts-V1-analysisOrdinal-1-refused', lambda: W.admit_fact_batch(TS, mut(tsb, ['analysisOrdinal'], 1), TST), 'SCHEMA')
    refuse('ts-V3-analysisOrdinal-1-refused', lambda: W.admit_fact_batch(TS, mut(tsb3, ['analysisOrdinal'], 1), TSA), 'ANALYSIS_ORDINAL')
    refuse('ts-V1-correlation-batchIndex-refused', lambda: W.admit_fact_batch(TS, tsb, TST, {'batchIndex': 1}), 'CORRELATION', 'batchIndex')
    refuse('ts-V1-candidate-ordinal-contiguity-refused', lambda: W.admit_fact_batch(TS, tsb, TST, {'firstCandidateOrdinal': 3}), 'CANDIDATE_ORDINAL_CONTIGUITY')
    many = [mut(tsb['facts'][0], ['candidateOrdinal'], i) for i in range(4097)]
    at_cap = {**tsb, 'facts': many[:4096]}
    at_cap['batchCommitment'] = 'sha256:' + hashlib.sha256(dom.encode() + b'\x00' + ind_cbor(wire_cands(at_cap['facts']))).hexdigest()
    admit('ts-V1-exactly-4096-facts-admitted', lambda: W.admit_fact_batch(TS, at_cap, TST), lambda r: r['candidateCount'] == 4096)
    over = {**tsb, 'facts': many}
    over['batchCommitment'] = 'sha256:' + hashlib.sha256(dom.encode() + b'\x00' + ind_cbor(wire_cands(over['facts']))).hexdigest()
    refuse('ts-V1-4097-facts-refused', lambda: W.admit_fact_batch(TS, over, TST), {'SCHEMA', 'BATCH_CANDIDATE_CAP'})
    keys = ['a', 'bb', 'b', 'x' * 23, 'y' * 24, 'z' * 255, 'w' * 256, 'é', 'aa', 'A']
    probe_map = {k: i for i, k in enumerate(keys)}
    row('text-key-map-order-bytewise-encoded-equals-length-first-rule', W.wire_cbor(probe_map) == ind_cbor(probe_map) and W.wire_cbor(wire_cands(tsb['facts'])) == ts_wire)

    # ---- occupancy gate omission is not historical validation ----------------------------------------------------
    A44 = load('rv44_attr', SRC / FND / 'provider_attribution_return_model.v2.py')
    A43 = load('rv43_attr', BASE / FND / 'provider_attribution_return_model.v2.py')
    samples = {'junk-map': {'junk': 1}, 'rust-v2-shape-under-typescript': rsb, 'ts-v1-wrong-commitment': mut(tsb, ['batchCommitment'], flip_hex),
               'ts-v1-hex-not-cbor': mut(tsb, ['facts', 0, 'decodedRelationPayload', 'specifier'], './z.ts'), 'not-a-map': [1, 2], 'ts-v1-valid': tsb}
    for name, sample in samples.items():
        g44 = attempt(lambda: A44.buffer_fact_batch_occupancy(sample, negotiated_tokens=TST, dispatch=None))
        g43 = attempt(lambda: A43.buffer_fact_batch_occupancy(sample, negotiated_tokens=TST, dispatch=None))
        c44 = attempt(lambda: A44.capture_occupancy(sample, negotiated_tokens=TST, plan_id='plan2:' + '0' * 64, execution_plan={}, stage_specs={}, closures={}, views={},
                                                    minted_by_ordinal={}, inventories=[], enumeration_plan={}))
        w = attempt(lambda: W.admit_fact_batch(TS, sample, TST))
        omitted = g44['admitted'] and g44['result']['status'] == 'omitted' and c44['admitted'] and c44['result']['status'] == 'omitted'
        # attempt1 compared whole gate outputs; source44 renamed only the omitted-delivery label, so behaviour is compared
        # with that label normalized and both labels are recorded.
        same = norm_label(g43) == norm_label(g44)
        row('occupancy-gate-omits-%s-while-wire-law-%s' % (name, 'admits' if name == 'ts-v1-valid' else 'refuses'),
            omitted and (w['admitted'] if name == 'ts-v1-valid' else not w['admitted']) and same,
            {'gate44': brief(g44), 'capture44': brief(c44), 'wire': brief(w), 'gate43': brief(g43), 'gate43EqualsGate44ExceptDeliveryLabel': same})
    v3g = attempt(lambda: A44.buffer_fact_batch_occupancy(tsb3, negotiated_tokens=TST, dispatch=None))
    v3w = attempt(lambda: W.admit_fact_batch(TS, tsb3, TST))
    row('unnegotiated-v3-refused-by-both-gate-and-wire-law', not v3g['admitted'] and 'UNNEGOTIATED_V3' in v3g['message'] and not v3w['admitted'] and v3w['key'] == 'UNNEGOTIATED_V3',
        {'gate': v3g, 'wire': v3w})
    lab44 = A44.buffer_fact_batch_occupancy({'junk': 1}, negotiated_tokens=TST, dispatch=None)['delivery']
    lab43 = A43.buffer_fact_batch_occupancy({'junk': 1}, negotiated_tokens=TST, dispatch=None)['delivery']
    row('token-gate-executable-body-unchanged-from-source43-except-docstring-and-omitted-delivery-label',
        body_without_docstring(A44._token_gate, {lab44}) == body_without_docstring(A43._token_gate, {lab43}) and A44._token_gate.__doc__ != A43._token_gate.__doc__,
        {'doc44': A44._token_gate.__doc__, 'doc43': A43._token_gate.__doc__, 'label44': lab44, 'label43': lab43,
         'rawBodyEqual': body_without_docstring(A44._token_gate) == body_without_docstring(A43._token_gate)})


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-3000:])
out = RT / 'receipts/probes/wire44.json'
kept = RT / 'receipts/probes/wire44.attempt1-gate-label-expectation-too-narrow.json'
if out.exists() and not kept.exists():
    out.rename(kept)  # preserve the failed first attempt verbatim
out.write_text(json.dumps({'standing': 'independent reviewer discriminators on the verified source44 copy; reference wire payload law only; no framing, process, worker or compiler; not qualification',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']], 'records': [r for r in ROWS if r['kind'] == 'record']}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']],
                  'records': [(r['case'], r['observed']) for r in ROWS if r['kind'] == 'record']}, indent=1, default=str)[:12000])

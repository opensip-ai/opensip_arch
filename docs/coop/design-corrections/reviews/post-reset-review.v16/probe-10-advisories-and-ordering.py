#!/usr/bin/env python3
"""Probe 10 (independent): CB5-ADV-1..4, V15-ADV-1 and CX-BV5-02/05, measured
against the exact frozen bytes.

ADV-1  four concrete digest representations vs the `by-domain` SELECTOR
ADV-2  LogicalPath: direct $ref vs joined vs imperative-only enforcement
ADV-3  L0 inner+outer length framing, and the historical policy bytes untouched
ADV-4  inherited platform vocabulary vs the four selected product platforms
V15-ADV-1 / CX-BV5-02  cardinality-first ordering and which inputs reach the
       schema step; the retained-Run payload boundary stays distinct
"""
import hashlib, importlib.util, itertools, json, os, re, sys

ROOT = '/tmp/opensip-design-corrections/post-reset-review.v16/copy-B-probes'
OUT = '/tmp/opensip-design-corrections/post-reset-review.v16'
DC = os.path.join(ROOT, 'docs/coop/design-corrections')
V2 = os.path.join(ROOT, 'docs/v2/contracts/product-v1')

def sha256b(b):
    return hashlib.sha256(b).hexdigest()

def sha256(p):
    return sha256b(open(p, 'rb').read())

sp = importlib.util.spec_from_file_location('rev16_n10', os.path.join(DC, 'native/native_evidence_model.v2.py'))
N = importlib.util.module_from_spec(sp); sys.modules['rev16_n10'] = N
sp.loader.exec_module(N)

IDS = json.load(open(os.path.join(DC, 'foundation/identity-schemas.v2.json')))
COMMON = json.load(open(os.path.join(DC, 'workflows/schemas/common.schema.json')))
CAPDOM = json.load(open(os.path.join(DC, 'native/capability-manifest-domains.v2.json')))
MATRIX = json.load(open(os.path.join(DC, 'native/native-capability-matrix.v2.json')))

checks = []
def check(cid, group, expected, observed, why):
    checks.append({'id': cid, 'group': group, 'expected': expected, 'observed': observed,
                   'agrees': expected == observed, 'why': why})

# ---------------------------------------------------------------- ADV-1
byd = IDS['x-opensip-digest-domains']['byDomain']
terminal = sorted({v['representation'] for v in byd.values()})
reps_in_use = set()
def walk_reps(o):
    if isinstance(o, dict):
        if 'x-opensip-digest' in o and isinstance(o['x-opensip-digest'], dict):
            r = o['x-opensip-digest'].get('representation')
            if r:
                reps_in_use.add(r)
        for v in o.values():
            walk_reps(v)
    elif isinstance(o, list):
        for v in o:
            walk_reps(v)
walk_reps(IDS)
check('ADV1-terminal-set-is-four', 'ADV-1 four concrete representations', 4, len(terminal),
      'every registered byDomain row resolves to one of exactly four TERMINAL representations')
check('ADV1-bydomain-never-a-byDomain-row-value', 'ADV-1 by-domain is a SELECTOR',
      True, 'by-domain' not in terminal,
      'no byDomain row may name by-domain; it is not admissible as a terminal value')
check('ADV1-bydomain-is-in-use-as-annotation', 'ADV-1 by-domain is a SELECTOR',
      True, 'by-domain' in reps_in_use,
      'reference fields DO annotate representation by-domain, which is the fifth token the '
      'blind review observed')
check('ADV1-tokens-in-use-are-five', 'ADV-1 five tokens in practice', 5, len(reps_in_use),
      'four terminal + the by-domain selector, exactly the shape the advisory described')
adv1_prose = open(os.path.join(V2, 'identity-and-evidence.md'), encoding='utf-8').read()
check('ADV1-selector-published', 'ADV-1 published clarification', True,
      'selector, not a fifth terminal' in adv1_prose,
      'the owning contract now names by-domain a selector rather than a fifth representation')

# ---------------------------------------------------------------- ADV-2
lp = IDS['$defs']['LogicalPath']
common_lp = COMMON['$defs']['LogicalPath']
check('ADV2-byte-identical-constraint', 'ADV-2 LogicalPath grammar',
      True,
      (lp['pattern'], lp.get('not'), lp['minLength'], lp['maxLength'])
      == (common_lp['pattern'], common_lp.get('not'), common_lp['minLength'], common_lp['maxLength']),
      'identity and workflow LogicalPath are byte-identical in constraint, which is what makes '
      'the import-blob rows an exact mirror')
direct_refs = []
def find_refs(o, p=''):
    if isinstance(o, dict):
        if o.get('$ref', '').endswith('/LogicalPath'):
            direct_refs.append(p)
        for k, v in o.items():
            find_refs(v, p + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            find_refs(v, p + f'[{i}]')
find_refs(IDS)
check('ADV2-exactly-two-direct-refs', 'ADV-2 direct $ref inventory',
      ['/$defs/Blob/properties/path', '/$defs/import-blob/properties/path'],
      sorted(direct_refs),
      'the description claims exactly two direct $ref fields; measured')
# the imperative check: ordered() does NOT enforce the 255 per-segment bound, and DOES refuse dot-dot
IM_spec = importlib.util.spec_from_file_location('rev16_im10', os.path.join(DC, 'foundation/identity-model.py'))
IM = importlib.util.module_from_spec(IM_spec); sys.modules['rev16_im10'] = IM
IM_spec.loader.exec_module(IM)
def ordered_admits(value):
    try:
        IM.ordered({'logicalPath': value})
        return True
    except Exception:
        return False
check('ADV2-ordered-admits-300-char-segment', 'ADV-2 enforcement (3) is NOT equivalent to (1)',
      True, ordered_admits('a' * 300),
      'ordered() does not enforce the per-segment 255 maximum, exactly as the description now says')
check('ADV2-ordered-refuses-dotdot', 'ADV-2 enforcement (3) still refuses traversal',
      False, ordered_admits('a/../b'), 'the imperative check does refuse a dot-dot segment')
check('ADV2-ordered-refuses-backslash', 'ADV-2 enforcement (3)', False, ordered_admits('a\\b'),
      'and a backslash')
check('ADV2-ordered-refuses-leading-slash', 'ADV-2 enforcement (3)', False, ordered_admits('/a'),
      'and a leading slash')
check('ADV2-declarative-refuses-300-char-segment', 'ADV-2 enforcement (1) IS stronger',
      False, bool(re.match(lp['pattern'], 'a' * 300)),
      'the declarative grammar DOES bound each segment at 255, so (1) and (3) genuinely differ')
check('ADV2-no-snapshot-join-claimed', 'ADV-2 no overstated adoption', True,
      'NO snapshot join' in lp['description'],
      'the fingerprint field is stated to have no snapshot join')

# ---------------------------------------------------------------- ADV-3
body = b'a=1\n'
l0_payload = len(body).to_bytes(4, 'big') + body
frame_component = len(l0_payload).to_bytes(4, 'big') + l0_payload
check('ADV3-l0-payload-bytes', 'ADV-3 worked example reproduces',
      '00000004' + body.hex(), l0_payload.hex(), 'inner u32be raw_byte_len || span bytes')
check('ADV3-frame-component-bytes', 'ADV-3 worked example reproduces',
      '00000008' + '00000004' + body.hex(), frame_component.hex(),
      'outer u32be payload_len || payload; payload_len == raw_byte_len + 4')
check('ADV3-payload-len-relation', 'ADV-3 both prefixes meant', True,
      len(l0_payload) == len(body) + 4, 'the stated arithmetic relation holds')
check('ADV3-worked-example-published', 'ADV-3 published byte vector', True,
      '00 00 00 08 00 00 00 04 61 3d 31 0a' in adv1_prose,
      'the resolution the advisory asked for (one explicit byte vector) is published')
POLICY = os.path.join(DC, 'foundation/fact-identity-policy.v2.json')
policy_sha = sha256(POLICY) if os.path.exists(POLICY) else None
check('ADV3-historical-policy-bytes-unchanged', 'ADV-3 no historical rewrite', True,
      'bytes are unchanged' in adv1_prose,
      'the inherited fact-identity-policy.v2 byteGrammar bytes are stated unchanged; the contract '
      'states which of the two grammatically available readings is admitted rather than editing it')

# ---------------------------------------------------------------- ADV-4
plat = CAPDOM['registries']['PLATFORM-ID-DOMAIN-V1']['members']
selected = MATRIX['platformFamilies']
sec = open(os.path.join(V2, 'security-and-lifecycle.md'), encoding='utf-8').read()
adq = open(os.path.join(V2, 'admission-and-qualification.md'), encoding='utf-8').read()
check('ADV4-inherited-vocabulary-is-eight', 'ADV-4 inherited vocabulary retained', 8, len(plat),
      'the inherited encoding domain is NOT narrowed')
check('ADV4-four-selected-platforms', 'ADV-4 selected product platforms', 4, len(selected),
      'the native matrix platformFamilies carries exactly the four selected machine ids')
check('ADV4-outside-product', 'ADV-4 members of no product promise',
      ['linux-x86_64-musl', 'windows-aarch64-msvc', 'windows-x86_64-msvc'],
      sorted(set(plat) - set(selected) - {'all-supported'}),
      'exactly the three the blind review measured')
check('ADV4-s8-carries-all-four', 'ADV-4 owning authority is S8', True,
      all(('`%s`' % p) in sec for p in selected),
      'security S8 names all four selected machine ids')
check('ADV4-s8-excludes-windows', 'ADV-4 owning authority is S8', True,
      'Windows) the core' in sec,
      'S8 is where Windows is named among the excluded populations')
check('ADV4-original-citation-was-wrong', 'ADV-4 the citation correction is REAL', 0,
      len(re.findall(r'(?i)windows', adq)),
      'admission-and-qualification.md contains no mention of Windows, so the blind review\'s '
      'citation was mistaken and the correction to S8 is factually right')
check('ADV4-blind-citation-retained-as-history', 'ADV-4 original review history preserved', True,
      'blind consumer-B v5 review cited admission-and-qualification section 5 item 1'
      in json.dumps(CAPDOM),
      'the original citation is retained as explicit history, not silently dropped')

# --------------------------------------------- V15-ADV-1 / CX-BV5-02 ordering
BOUND = N.MAX_REQUESTED_CAPABILITIES if hasattr(N, 'MAX_REQUESTED_CAPABILITIES') else 1024
def valid_row(i=0):
    # the real analysis-spec capability row: four required members. My first attempt
    # (failed-attempt-05) used a two-field row and a schemaVersion of 1, so the two
    # POSITIVE controls refused on my fixture rather than on the design.
    return {'capabilityId': 'imports', 'languageMode': 'ts-tsconfig',
            'workspaceRoot': '.', 'required': True}

def classify(spec):
    try:
        N.admit_analysis_spec(spec)
        return 'ADMIT', None
    except Exception as e:
        t = type(e).__name__
        s = str(e)
        if 'SCOPE_LIMIT' in s or 'ScopeRefusal' in t:
            return 'CARDINALITY', s[:160]
        if t in ('ValidationError',):
            return 'SCHEMA', s[:120]
        return t, s[:160]

order_rows = []
def order_case(cid, spec, exp, why):
    got, detail = classify(spec)
    order_rows.append({'id': cid, 'expected': exp, 'observed': got, 'agrees': got == exp,
                       'detail': detail, 'why': why})

BASE = {'schemaVersion': 2, 'requestedCapabilities': [valid_row()],
        'policyPackIds': [], 'parameters': []}
import copy as _c
def spec(**over):
    s = _c.deepcopy(BASE); s.update(over); return s

def canon_set(rows):
    # requestedCapabilities carries x-opensip-order canonical-set, so a distinct-row
    # array must ALSO be in canonical order or it refuses at the schema step. My first
    # attempt left it unsorted (failed-attempt-06).
    return sorted(rows, key=lambda r: N.C.canonical(r))

OVER = canon_set([dict(valid_row(), workspaceRoot='ws%d' % i) for i in range(BOUND + 10)])
# a. shapes that are NOT an array all reach the schema step
for label, value in [('absent', '__DROP__'), ('null', None), ('bool', True), ('number', 7),
                     ('string', 'x' * (BOUND + 10)), ('object', {'a': 1})]:
    s = spec()
    if value == '__DROP__':
        s.pop('requestedCapabilities')
    else:
        s['requestedCapabilities'] = value
    order_case(f'O-nonarray-{label}', s, 'SCHEMA',
               'step 1 is conditional on an actual JSON array, so this reaches step 2 untouched; '
               'a 1034-character string is NOT published as 1034 capabilities')
# b. an in-bound array malformed some other way reaches the schema step
order_case('O-inbound-unknown-property',
           spec(requestedCapabilities=[valid_row()], unknownProperty=1), 'SCHEMA',
           'an in-bound array malformed some other way still refuses at the schema step')
order_case('O-inbound-missing-schemaVersion',
           {k: v for k, v in BASE.items() if k != 'schemaVersion'}, 'SCHEMA',
           'a missing schemaVersion still refuses at the schema step exactly as before')
# c. only an actual over-bound array refuses at step 1
order_case('O-oversized-array-alone', spec(requestedCapabilities=OVER), 'CARDINALITY',
           'step 1 refuses ONLY an actual JSON array over its bound')
# d. V15-ADV-1's counterexample: oversized AND otherwise malformed -> cardinality preempts
order_case('O-oversized-and-missing-schemaVersion',
           {'requestedCapabilities': OVER, 'policyPackIds': [], 'parameters': []}, 'CARDINALITY',
           'V15-ADV-1: cardinality-first, so the schema fault is deferred to a narrowed request')
order_case('O-oversized-and-unknown-property',
           spec(requestedCapabilities=OVER, unknownProperty=1), 'CARDINALITY',
           'same, with an unknown property')
order_case('O-oversized-and-wrong-schemaVersion',
           spec(requestedCapabilities=OVER, schemaVersion='two'), 'CARDINALITY',
           'same, with a wrong schemaVersion type')
# e. V15-ADV-1's control: the same four specs at small cardinality DO reach the schema step
order_case('O-control-small-missing-schemaVersion',
           {'requestedCapabilities': [valid_row()], 'policyPackIds': [], 'parameters': []}, 'SCHEMA',
           'V15-ADV-1 CONTROL: narrowing the selection reveals the underlying schema fault')
order_case('O-control-small-unknown-property',
           spec(unknownProperty=1), 'SCHEMA', 'V15-ADV-1 CONTROL')
order_case('O-control-small-wrong-schemaVersion',
           spec(schemaVersion='two'), 'SCHEMA', 'V15-ADV-1 CONTROL')
# f. positive control
order_case('O-valid-spec-admits', spec(), 'ADMIT', 'POSITIVE CONTROL: a valid spec admits')
# g. exactly at the bound
order_case('O-exactly-at-bound', spec(requestedCapabilities=canon_set([dict(valid_row(), workspaceRoot='ws%d' % i) for i in range(BOUND)])),
           'ADMIT', 'the bound itself is admissible; only OVER the bound refuses')

nat = open(os.path.join(V2, 'native-evidence.md'), encoding='utf-8').read()
check('ORD-prose-scopes-the-sentence', 'V15-ADV-1 published scoping', True,
      'for every input that reaches that step' in nat,
      'the unqualified summarising sentence is now scoped, which is the repair V15-ADV-1 suggested')
check('ORD-prose-names-origin-dependent-routing', 'CX-BV5-02 published routing', True,
      'SYSTEM.OUTCOME.ILLEGAL_STATE' in nat and 'host-invariant' in nat,
      'section 10 origin-dependent routing is stated, not flattened into one route')
check('ORD-retained-boundary-distinct', 'retained Run payload corruption stays distinct', True,
      'corruption rather than an oversized request' in nat,
      'the retained-payload boundary is explicitly a different question with a different answer')
check('ORD-docstring-matches-prose', 'CX-BV5-02 docstring corrected', True,
      'REACHES step 2' in N.admit_analysis_spec.__doc__
      and 'operational-failed / exit 4' in N.admit_analysis_spec.__doc__,
      'the model docstring carries the same scoping and routing as the prose')

res = {
    'probe': 'probe-10-advisories-and-ordering',
    'copyName': 'copy-B-probes',
    'boundSourceSha256': {
        'foundation/identity-schemas.v2.json': sha256(os.path.join(DC, 'foundation/identity-schemas.v2.json')),
        'foundation/identity-model.py': sha256(os.path.join(DC, 'foundation/identity-model.py')),
        'native/native_evidence_model.v2.py': sha256(os.path.join(DC, 'native/native_evidence_model.v2.py')),
        'native/capability-manifest-domains.v2.json': sha256(os.path.join(DC, 'native/capability-manifest-domains.v2.json')),
        'native/native-capability-matrix.v2.json': sha256(os.path.join(DC, 'native/native-capability-matrix.v2.json')),
        'workflows/schemas/common.schema.json': sha256(os.path.join(DC, 'workflows/schemas/common.schema.json')),
        'docs/v2/contracts/product-v1/identity-and-evidence.md': sha256(os.path.join(V2, 'identity-and-evidence.md')),
        'docs/v2/contracts/product-v1/native-evidence.md': sha256(os.path.join(V2, 'native-evidence.md')),
        'docs/v2/contracts/product-v1/security-and-lifecycle.md': sha256(os.path.join(V2, 'security-and-lifecycle.md')),
        'docs/v2/contracts/product-v1/admission-and-qualification.md': sha256(os.path.join(V2, 'admission-and-qualification.md')),
    },
    'terminalRepresentations': terminal,
    'representationTokensInUse': sorted(reps_in_use),
    'boundedSelectionLimit': BOUND,
    'staticChecks': len(checks), 'staticAgree': sum(1 for c in checks if c['agrees']),
    'staticDisagree': [c for c in checks if not c['agrees']],
    'orderingCases': len(order_rows), 'orderingAgree': sum(1 for r in order_rows if r['agrees']),
    'orderingDisagree': [r for r in order_rows if not r['agrees']],
    'checks': checks, 'orderingRows': order_rows,
    'notProductQualification': True,
}
with open(os.path.join(OUT, 'probe-10-advisories-and-ordering.result.json'), 'w') as f:
    json.dump(res, f, indent=2, sort_keys=True, default=str)
print(json.dumps({k: v for k, v in res.items() if k not in ('checks', 'orderingRows')},
                 indent=2, sort_keys=True, default=str))

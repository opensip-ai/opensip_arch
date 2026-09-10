"""Post-reset author (Claude) schema edits for security-lifecycle.schemas.v1.json.
Round-trip verified: json.dumps(indent=2, ensure_ascii=False) + newline reproduces the current bytes.
Edits: MUST-2 profile-set keys / displayAlias; MUST-3 prunedTrees + typed cap refusal; SHOULD-2 projection records;
SHOULD-6 lease namespaces / core transitions. Codex's strict end assertions are preserved untouched."""
import json, sys
P = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json'
raw = open(P, 'rb').read()
doc = json.loads(raw)
assert (json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode() == raw
S = doc['schemas']
END = '(?![\\s\\S])'
PLATFORM_IDS = ['linux-aarch64-gnu', 'linux-x86_64-gnu', 'macos-aarch64', 'macos-x86_64']

# --- MUST-2: one machine vocabulary keys the signed profile set; aliases are display only
pps = S['PlatformProfileSetV1']
pps['title'] = ('metadata: signed release profile population keyed by the ONE machine platform vocabulary '
                '(linux-aarch64-gnu, linux-x86_64-gnu, macos-aarch64, macos-x86_64; the same ids as RepoExecutionGrantV2.platformId, '
                'the native matrix platformFamilies and the workflow test-execution schema); display aliases (macos-arm64, linux-x86_64, '
                'linux-arm64) never key it; per platform: measured lanes + supported baseline; values in fixtures are SYNTHETIC')
pps['properties']['platforms']['properties'] = {
    'macos-aarch64': {'$ref': '#/schemas/PlatformProfileSetV1/$defs/macos'},
    'macos-x86_64': {'$ref': '#/schemas/PlatformProfileSetV1/$defs/macos'},
    'linux-x86_64-gnu': {'$ref': '#/schemas/PlatformProfileSetV1/$defs/linux'},
    'linux-aarch64-gnu': {'$ref': '#/schemas/PlatformProfileSetV1/$defs/linux'},
}
pa = S['PlatformAdmissionV1']
pa['required'].insert(pa['required'].index('platform') + 1, 'displayAlias')
props = {}
for k, v in pa['properties'].items():
    props[k] = v
    if k == 'platform':
        props['platform'] = {'type': 'string', 'maxLength': 64,
                             'description': 'the observed platform id as presented; on ADMIT always one of the four machine ids'}
        props['displayAlias'] = {'$ref': '#/$defs/NullableString',
                                 'description': 'human display alias of an admitted machine id (macos-arm64, macos-x86_64, linux-x86_64, linux-arm64); null when the presented platform is not a machine id; never an input'}
pa['properties'] = props

# --- MUST-3: pruned trees recorded once; typed cap refusal
dp = S['DiscoveryProvenanceV1']
dp['required'].insert(dp['required'].index('excludedUnits') + 1, 'prunedTrees')
dp['properties']['prunedTrees'] = {
    'description': 'anchors of dependency (node_modules), VCS (.git/.hg/.svn/.jj) and Cargo build-output (target directly under a Cargo.toml directory) trees observed under the selected root; pruned by exact path segment per ../discovery-defaults.py; one record per tree, never per package',
    'type': 'array', 'maxItems': 65536,
    'items': {'type': 'object', 'additionalProperties': False, 'required': ['path', 'reason', 'markerCount'],
              'properties': {'path': {'type': 'string', 'maxLength': 4096},
                             'reason': {'enum': ['dependency-tree', 'vcs-tree', 'cargo-build-output']},
                             'markerCount': {'$ref': '#/$defs/I64NonNegative'}}}}
dr = S['DiscoveryResultV1']['oneOf'][1]['properties']['refusal']
dr['enum'] = ['CONFIG.CUSTODY_REFUSED', 'PROJECT.ROOT_CUSTODY_REFUSED', 'PROJECT.EXPLICIT_PATH_INVALID', 'PROJECT.WORKSPACE_UNIT_LIMIT']

# --- SHOULD-6: namespaces and core transitions in the lease trace
lt = S['LeaseTraceV1']
item = lt['properties']['trace']['items']
item['required'] = ['actor', 'op', 'mode', 'namespace', 'result']
item['properties']['op']['enum'] = ['fence-acquire', 'fence-release', 'lease', 'lease-release', 'gc-census', 'trust-write',
                                    'core-transition-acquire', 'core-transition-release']
newprops = {}
for k, v in item['properties'].items():
    newprops[k] = v
    if k == 'mode':
        newprops['namespace'] = {'$ref': '#/$defs/NullableString'}
item['properties'] = newprops
fin = lt['properties']['final']
fin['required'] = ['fence', 'readers', 'writer', 'exclusive', 'namespaces', 'coreTransitions']
fin['properties']['namespaces'] = {
    'type': 'object',
    'additionalProperties': {'type': 'object', 'additionalProperties': False, 'required': ['readers', 'writer', 'exclusive'],
                             'properties': {'readers': {'$ref': '#/$defs/StringList'}, 'writer': {'$ref': '#/$defs/NullableString'},
                                            'exclusive': {'$ref': '#/$defs/NullableString'}}}}
fin['properties']['coreTransitions'] = {'type': 'object', 'additionalProperties': {'$ref': '#/$defs/StringList'}}
S['CoreTransitionScopeV1'] = {
    'title': 'S7 core-transition lease set decided from the intent and the host namespace registry (never user input)',
    'type': 'object', 'additionalProperties': False, 'required': ['affects', 'namespaces'],
    'properties': {'affects': {'enum': ['all-registered', 'none']}, 'namespaces': {'$ref': '#/$defs/StringList'}}}

# --- SHOULD-2: Plan-time projection records
S['SemanticProjectionV1'] = {
    'title': 'S10 principals a consuming analysis must project into plan2 for the preparation grants it consumes (test-runner grants project nothing)',
    'type': 'object', 'additionalProperties': False, 'required': ['principals'],
    'properties': {'principals': {'type': 'array', 'maxItems': 4096, 'items': {
        'type': 'object', 'additionalProperties': False, 'required': ['kind', 'closureId', 'ownerSourceDigest'],
        'properties': {'kind': {'const': 'trusted-repository-code'}, 'closureId': {'$ref': '#/$defs/ClosureId'},
                       'ownerSourceDigest': {'$ref': '#/$defs/Hex64'}}}}}}
S['ExecutionProjectionAdmissionV1'] = {
    'title': 'S10 Plan-time join: plan2 semantic-grant projection versus the consumed preparation grants; never derived from a grant',
    'type': 'object', 'additionalProperties': False,
    'required': ['result', 'refusals', 'd9', 'preparedResolution', 'requiredPrincipals', 'projectionSource', 'testRunnerProjected'],
    'properties': {'result': {'enum': ['ADMIT', 'REFUSE']},
                   'refusals': {'type': 'array', 'maxItems': 4096, 'items': {'type': 'string', 'pattern': '^PLAN\\.[A-Z_]+(:[^ ]+)?' + END}},
                   'd9': {'$ref': '#/$defs/NullableD9'},
                   'preparedResolution': {'type': 'string', 'maxLength': 64},
                   'requiredPrincipals': {'$ref': '#/schemas/SemanticProjectionV1/properties/principals'},
                   'projectionSource': {'type': 'string'},
                   'testRunnerProjected': {'const': False}}}
open(P, 'wb').write((json.dumps(doc, indent=2, ensure_ascii=False) + '\n').encode())
print('ok', len(S), 'schemas')

"""Build contract successor B-S1 (law M3-B r2 successor S3, with M3-C's SX-1). S9 is split into unit B-S9.

Writes, deterministically:
- b-s1/schemas/security-lifecycle.schemas.v1.b-s1-additions.json and
  b-s1/schemas/native-evidence.schemas.v2.b-s1-additions.json, each derived from the
  accepted version-2 records by an explicit delta, so the V2 -> V3 relation is mechanical;
- b-s1/PASSAGES.md, a readable rendering of every override;
- b-s1/successor.json and ../b-s1-subject.json.
Hand-written inputs it pins but never writes: README.md, the reader registry and the
three evidence scripts. Run with python3 -I -B from any directory; rerunning reproduces
the same bytes. It reads only the architecture repository."""
import copy, hashlib, json
from pathlib import Path

A = Path(__file__).resolve().parents[6]
B = 'docs/implementation/m3/config-discovery-b/'
D = B + 'b-s1/'
SL = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
SLS = 'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json'
NES = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
SLS_ADD = D + 'schemas/security-lifecycle.schemas.v1.b-s1-additions.json'
NES_ADD = D + 'schemas/native-evidence.schemas.v2.b-s1-additions.json'
REGISTRY = D + 'registry/workspace-declaration-readers.v1.json'
HAND = [D + 'README.md', REGISTRY, D + 'evidence/build_b_s1.py', D + 'evidence/check_b_s1.py',
        D + 'evidence/verify_scratch.py']


def pin(p):
    b = (A / p).read_bytes()
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def load(p):
    def unique(pairs):
        out = {}
        for k, v in pairs:
            assert k not in out, (p, k)
            out[k] = v
        return out
    return json.loads((A / p).read_bytes(), object_pairs_hook=unique)


def dump(p, value):
    (A / p).parent.mkdir(parents=True, exist_ok=True)
    (A / p).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


REL = '^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])'
REASONS_V3 = ['dependency-tree', 'vcs-tree', 'cargo-build-output', 'opensip-custody-state']
READERS = ['cargo-config-patch', 'npm-workspaces-members']
UNRESOLVED_WITH_SUBJECT = ['member-excluded', 'link-manifest-unusable']
UNRESOLVED_PLAIN = ['workspace-glob-crosses-repository', 'entry-path-grammar', 'entry-path-outside-root',
                    'entry-path-absent', 'entry-not-in-a-member', 'dropped-workspace-roots-present',
                    'patch-entry-not-path', 'patch-target-name-mismatch', 'ambiguous-provider',
                    'provided-version-unusable']
SX1 = ('VERSION 3 (contract successor B-S1, successor SX-1 of law M3-C): adds exactly the reason '
       'opensip-custody-state, the anchor of the exact path .opensip at the selected root and at each admitted '
       'D15 member root, observed only as an entry of its parent and never opened, listed or entered. ')


def member_paths(order):
    return {'type': 'array', 'maxItems': 64, 'uniqueItems': True,
            'items': {'type': 'string', 'minLength': 1, 'maxLength': 4096, 'pattern': REL},
            'x-opensip-order': order}


# ---- security-lifecycle additions -------------------------------------------------------
sls = load(SLS)
row3 = copy.deepcopy(sls['$defs']['PrunedTreeRowV2'])
row3['properties']['reason']['enum'] = REASONS_V3
row3['description'] = SX1 + row3['description']
abs_path = {'type': 'string', 'minLength': 1, 'maxLength': 4096}
declaration = {
    'description': 'One source that declared a D15 member (law M3-B item 22). An explicit tier names the exact root, as an absolute locator, that lies inside the member; a reader names its carrier and the SHA-256 of the carrier bytes it read.',
    'oneOf': [
        {'type': 'object', 'additionalProperties': False, 'required': ['source', 'path'],
         'properties': {'source': {'enum': ['explicit-joins', 'config-workspace-roots']}, 'path': abs_path}},
        {'type': 'object', 'additionalProperties': False,
         'required': ['source', 'readerId', 'readerVersion', 'path', 'contentSha256'],
         'properties': {'source': {'const': 'reader'}, 'readerId': {'enum': READERS},
                        'readerVersion': {'const': 1}, 'path': abs_path,
                        'contentSha256': {'$ref': '#/$defs/Hex64'}}}]}
member = {
    'type': 'object', 'additionalProperties': False, 'required': ['path', 'declaredBy'],
    'description': 'An admitted D15 member repository (security S3): its root as an absolute locator, and every source that declared it.',
    'properties': {'path': abs_path,
                   'declaredBy': {'type': 'array', 'minItems': 1, 'maxItems': 4096,
                                  'items': {'$ref': '#/$defs/MemberDeclarationV1'},
                                  'x-opensip-order': {'by': ['source', 'path']}}}}
unresolved = {
    'description': 'One reader entry that declared no member and yielded no link, with its closed reason (registry docs/implementation/m3/config-discovery-b/b-s1/registry/workspace-declaration-readers.v1.json). entry is the entry as written: patch.<source>.<name> for Cargo, the workspaces string for npm.',
    'oneOf': [
        {'type': 'object', 'additionalProperties': False, 'required': ['entry', 'reason', 'subject'],
         'properties': {'entry': {'type': 'string', 'minLength': 1, 'maxLength': 4096},
                        'reason': {'enum': UNRESOLVED_WITH_SUBJECT},
                        'subject': {'type': 'string', 'minLength': 1, 'maxLength': 256}}},
        {'type': 'object', 'additionalProperties': False, 'required': ['entry', 'reason', 'subject'],
         'properties': {'entry': {'type': 'string', 'minLength': 1, 'maxLength': 4096},
                        'reason': {'enum': UNRESOLVED_PLAIN}, 'subject': {'type': 'null'}}}]}
wd_common = {'readerId': {'enum': READERS}, 'readerVersion': {'const': 1}}
unresolved_list = {'type': 'array', 'maxItems': 65536, 'items': {'$ref': '#/$defs/UnresolvedDeclarationEntryV1'},
                   'x-opensip-order': {'by': ['entry']}}
workspace_declaration = {
    'description': 'What one registered declaration reader did. absent: no carrier at W. read: the carrier was admitted and parsed, and its undeclared entries are listed. refused: carrier custody, parse, shape or ambiguity failure; nothing was declared and nothing is listed. A refusal here is a disclosure, never a public refusal.',
    'oneOf': [
        {'type': 'object', 'additionalProperties': False,
         'required': ['readerId', 'readerVersion', 'state', 'path', 'contentSha256', 'stateSubject', 'unresolved'],
         'properties': {**wd_common, 'state': {'const': 'absent'}, 'path': {'type': 'null'},
                        'contentSha256': {'type': 'null'}, 'stateSubject': {'type': 'null'},
                        'unresolved': {**unresolved_list, 'maxItems': 0}}},
        {'type': 'object', 'additionalProperties': False,
         'required': ['readerId', 'readerVersion', 'state', 'path', 'contentSha256', 'stateSubject', 'unresolved'],
         'properties': {**wd_common, 'state': {'const': 'read'}, 'path': abs_path,
                        'contentSha256': {'$ref': '#/$defs/Hex64'}, 'stateSubject': {'type': 'null'},
                        'unresolved': unresolved_list}},
        {'type': 'object', 'additionalProperties': False,
         'required': ['readerId', 'readerVersion', 'state', 'path', 'contentSha256', 'stateSubject', 'unresolved'],
         'properties': {**wd_common, 'state': {'const': 'refused'}, 'path': {'$ref': '#/$defs/NullableString'},
                        'contentSha256': {'oneOf': [{'type': 'null'}, {'$ref': '#/$defs/Hex64'}]},
                        'stateSubject': {'type': 'string', 'pattern': '^(custody:[A-Z_]+|parse|carrier-ambiguous|workspaces-shape-unsupported)(?![\\s\\S])'},
                        'unresolved': {**unresolved_list, 'maxItems': 0}}}]}
d9 = copy.deepcopy(sls['$defs']['D9'])
d9['properties']['code']['enum'] = d9['properties']['code']['enum'] + ['REQUEST.UNSATISFIABLE']
d9['description'] = ('The D9 branch of a discovery refusal. It is the bundle D9 with REQUEST.UNSATISFIABLE added, '
                     'which PROJECT.WORKSPACE_UNIT_LIMIT (security S3) and PROJECT.SCOPE_LIMIT (members:<n>>64) carry '
                     '(security S12). The bundle D9 itself is unchanged.')

prov3 = copy.deepcopy(sls['schemas']['DiscoveryProvenanceV2'])
prov3['properties']['schemaVersion'] = {'const': 3}
prov3['properties']['prunedTrees']['items'] = {'$ref': '#/$defs/PrunedTreeRowV3'}
prov3['properties']['prunedTrees']['description'] += (' VERSION 3 (B-S1, SX-1): also the opensip-custody-state anchor.')
prov3['properties']['memberRepositories'] = {
    'type': 'array', 'maxItems': 64, 'items': {'$ref': '#/$defs/MemberRepositoryV1'}, 'x-opensip-order': 'path',
    'description': 'D15 member repositories admitted under the selected root (security S3), ascending by path. A member is not in nestedRepositories and is not a boundary. Empty for a project with no member.'}
prov3['properties']['workspaceDeclarations'] = {
    'type': 'array', 'minItems': 2, 'maxItems': 2, 'items': {'$ref': '#/$defs/WorkspaceDeclarationV1'},
    'x-opensip-order': {'by': ['readerId']},
    'description': 'Exactly one row per registered declaration reader, in readerId order, whatever the branch.'}
prov3['properties']['memberConfigs'] = {
    'type': 'array', 'maxItems': 64, 'uniqueItems': True,
    'items': {'type': 'string', 'minLength': 1, 'maxLength': 4096}, 'x-opensip-order': 'utf8',
    'description': 'Each admitted member root that holds opensip.json, as the absolute locator of that file. It is disclosed as not consulted: never read, never a configuration layer of the selected root and never a nested-project boundary (law M3-B item 22).'}
prov3['required'] = prov3['required'] + ['memberRepositories', 'workspaceDeclarations', 'memberConfigs']
prov3['description'] = ('Discovery provenance VERSION 3 (contract successor B-S1): version 2 with PrunedTreeRowV3 rows '
                        '(SX-1) and the D15 fields memberRepositories, workspaceDeclarations and memberConfigs. '
                        'Version-1 and version-2 records keep their bytes and are read under their own versions.')

result3 = copy.deepcopy(sls['schemas']['DiscoveryResultV2'])
for branch in result3['oneOf']:
    branch['properties']['provenance'] = {'$ref': '#/schemas/DiscoveryProvenanceV3'}
refuse = result3['oneOf'][1]['properties']
refuse['refusal']['enum'] = refuse['refusal']['enum'] + ['PROJECT.SCOPE_LIMIT']
refuse['d9'] = {'$ref': '#/$defs/DiscoveryD9V1'}
result3['description'] = ('Discovery result VERSION 3 (contract successor B-S1): version 2 with a version-3 provenance '
                          'record, the D15 member cap refusal PROJECT.SCOPE_LIMIT (detail members:<n>>64) and a D9 '
                          'branch that admits REQUEST.UNSATISFIABLE.')

abi3 = copy.deepcopy(sls['schemas']['AdmittedBoundaryInventoryV2'])
abi3['properties']['schemaVersion'] = {'const': 3}
abi3['properties']['prunedTrees']['items']['properties']['reason']['enum'] = REASONS_V3
abi3['properties']['memberRepositories'] = member_paths('utf8')
abi3['required'] = abi3['required'] + ['memberRepositories']
abi3['title'] = ('S3 export, VERSION 3 (contract successor B-S1): the admitted authority boundaries of the selected '
                 'root as relative scope paths, produced only by boundary_inventory over an ACCEPTed '
                 'DiscoveryResultV3 and consumed unchanged by the native unit instrument. memberRepositories are '
                 'D15 member roots: not boundaries, never in excludedPathPrefixes.')

sls_add = {
    'artifact': 'opensip.security-lifecycle.schemas.additions',
    'successor': 'B-S1',
    'status': 'PROPOSED-NOT-SELF-ACCEPTED',
    'base': pin(SLS),
    'mergeRule': 'Every $defs and schemas member below is ADDED to the base bundle under the same key; no base member is replaced or removed. Every #/ reference resolves in the merged bundle. Version-1 and version-2 records are unchanged.',
    'standing': 'Closed Draft 2020-12 records added to the security-lifecycle bundle by contract successor B-S1 (law M3-B r2 successor S3, with successor SX-1 of law M3-C) for security-and-lifecycle S3. Design evidence, not a product implementation.',
    '$defs': {'PrunedTreeRowV3': row3, 'MemberDeclarationV1': declaration, 'MemberRepositoryV1': member,
              'UnresolvedDeclarationEntryV1': unresolved, 'WorkspaceDeclarationV1': workspace_declaration,
              'DiscoveryD9V1': d9},
    'schemas': {'DiscoveryProvenanceV3': prov3, 'DiscoveryResultV3': result3, 'AdmittedBoundaryInventoryV3': abi3},
}

# ---- native-evidence additions ----------------------------------------------------------
nes = load(NES)
pt3 = copy.deepcopy(nes['$defs']['PrunedTreeV2'])
pt3['properties']['reason']['enum'] = REASONS_V3
pt3['description'] = SX1 + pt3['description'].replace('PrunedTreeRowV2', 'PrunedTreeRowV3')
nabi3 = copy.deepcopy(nes['$defs']['AdmittedBoundaryInventoryV2'])
nabi3['properties']['schemaVersion'] = {'const': 3}
nabi3['properties']['prunedTrees']['items'] = {'$ref': '#/$defs/PrunedTreeV3'}
nabi3['properties']['memberRepositories'] = member_paths('utf8')
nabi3['required'] = nabi3['required'] + ['memberRepositories']
nabi3['description'] = ('TRUSTED ADMITTED INPUT (P3), VERSION 3 (contract successor B-S1): version 2 converted from the '
                        'ACCEPTed DiscoveryProvenanceV3, with PrunedTreeV3 rows (SX-1) and memberRepositories, the '
                        'relative roots of the admitted D15 member repositories. A member is not a boundary: it enters '
                        'no excludedPathPrefixes and excludes no unit or file (native section 1.4 U-8). Never authored by a caller.')
ub2 = copy.deepcopy(nes['$defs']['UnitBoundariesV1'])
ub2['properties']['memberRepositories'] = member_paths('utf8')
ub2['required'] = ub2['required'] + ['memberRepositories']
ub2['description'] = ('boundary provenance of a unit discovery, VERSION 2 (contract successor B-S1): version 1 plus '
                      'memberRepositories, the admitted D15 member roots carried beside the boundary rows (empty with '
                      'source none and for a project with no member)')
ud3 = copy.deepcopy(nes['$defs']['UnitDiscoveryV2'])
ud3['properties']['prunedTrees']['items'] = {'$ref': '#/$defs/PrunedTreeV3'}
ud3['properties']['boundaries'] = {'$ref': '#/$defs/UnitBoundariesV2'}
ud3['description'] = ('Unit discovery output VERSION 3 (contract successor B-S1): version 2 with PrunedTreeV3 rows '
                      '(SX-1) and UnitBoundariesV2 (D15 memberRepositories). Versions 1 and 2 remain the historical '
                      'records for their own bytes.')
nes_add = {
    'artifact': 'opensip.native-evidence.schemas.additions',
    'successor': 'B-S1',
    'status': 'PROPOSED-NOT-SELF-ACCEPTED',
    'base': pin(NES),
    'mergeRule': 'Every $defs member below is ADDED to the base bundle (urn:opensip:product-v1:native:evidence-schemas:v2) under the same key; no base member is replaced or removed. Every #/ reference resolves in the merged bundle.',
    'standing': 'Closed Draft 2020-12 records added to the native evidence bundle by contract successor B-S1 for native-evidence section 1.4 (U-4a and U-8). PrunedTreeV3 mirrors the security bundle PrunedTreeRowV3 and AdmittedBoundaryInventoryV3 mirrors its security namesake, as their version-2 pairs do. Design evidence, not a product implementation.',
    '$defs': {'PrunedTreeV3': pt3, 'AdmittedBoundaryInventoryV3': nabi3, 'UnitBoundariesV2': ub2,
              'UnitDiscoveryV3': ud3},
}

# ---- passage overrides -------------------------------------------------------------------
X = 'docs/implementation/m3/config-discovery-b/b-s1/'
D15 = (
    '\n\n**Multi-repository workspaces (D15; contract successor B-S1, under law M3-B r2 items 19 to 24).** One project '
    'may span several Git repositories. Its selected root W is then in no repository, and the declared **member '
    'repositories** below W are entered as ordinary directories of W. W keeps the only ProjectId, marker, registry row '
    'and lease namespace. A member is never an authority root: it is analysed alone only through its own launch or '
    '`--project`, and a launch inside a member selects that member alone, because the upward walk is unchanged.\n\n'
    '*Shape.* W is selected in `config`, `explicit` or `cwd-default` mode; project-root law X2\'s tracking observation '
    'of W is "no repository" (no VCS marker at W or at any ancestor up to `/`); and W passes project-root custody '
    'unchanged. A member M is a directory strictly below W, reached without a symlink or a device change and at most 256 '
    'segments below W. M holds `.git` as a directory and no other VCS marker; no directory strictly between W and M '
    'holds a VCS marker or `opensip.json`; M is not at or below `W/.opensip`; no member is at or below another; and M '
    'passes X2 r9 item 6b\'s member observation, which admits `M/.git`, `M/.git/config` and `M/.git/index` only, under '
    'the closed conventional layout of an enclosing repository. A project has at most 64 members (S12).\n\n'
    '*Declaration.* One fact chooses the branch: whether the resolved configuration holds an admitted '
    '`discovery.workspaceRoots` array, from the project or interactive local layer or from `--workspace-root`, which is '
    'the flags layer of the same field. **With the array**, it alone decides membership. Each exact root that lies '
    'inside a nested conventional repository below W makes that repository a member. Discovery is restricted to exactly '
    'the array\'s roots, inside members as anywhere else, and is never widened into a scan. The declaration readers '
    'declare no member and record only links into members the array admitted. **Without the array**, the closed '
    'declaration readers declare members, reading only W\'s own native files, as data, and running nothing: '
    '`cargo-config-patch@1` (`[patch.<registry>]` path entries in `W/.cargo/config.toml`, or the legacy '
    '`W/.cargo/config`) and '
    '`npm-workspaces-members@1` (literal `workspaces` paths in `W/package.json`; a glob never declares a member). Their '
    'grammar, dispositions and outputs are the reader registry `' + X + 'registry/workspace-declaration-readers.v1.json`. '
    'An entry declares a member by its placement alone, never by package metadata, and a reader link counts only when '
    'its directory lies inside an admitted member. There is no Python reader, and no other file declares a member.\n\n'
    '*What a member changes.* A member is neither a nested repository nor a boundary. Automatic discovery enters it like '
    'any directory of W; its `.git` is an ordinary pruned `vcs-tree` anchor; and repositories, `opensip.json` projects '
    'and custody exclusions inside it stay boundaries. A member\'s own `opensip.json` at its root makes it neither a '
    'nested project nor a configuration layer of W: it is recorded in `memberConfigs` and never read for configuration. '
    'Membership is selection, not authorization: no flag or consent admits a member, and no custody check is waived for '
    'one. `--trust-group` applies to member directories and member Git evidence as it does to an enclosing '
    'repository\'s; `--trust-project-owner`, with an explicit `--project W`, waives the owner check on member '
    'directories only, never on member Git evidence. Nothing is written in a member.\n\n'
    '*Refusals and disclosures (no new code).* For a member named by the array or by `--workspace-root`, a layout or '
    'placement failure refuses `PROJECT.ROOT_CUSTODY_REFUSED` with subject `member-vcs-unsupported:<reason>` or '
    '`member-outside-volume`; a member directory\'s custody failure refuses with its existing custody subject; and a '
    'crossing into a repository that cannot become a member refuses `JOIN_CROSSES_NESTED_REPOSITORY` (above). A '
    'candidate that a reader declared and that fails any of these is not refused: it stays a nested repository and a '
    'boundary, and its reason is disclosed in `workspaceDeclarations[].unresolved`. When W is itself in a repository, '
    'the readers declare nothing, and each reader entry inside a nested repository is disclosed with subject '
    '`workspace-root-inside-repository`. Reader entries that are globs crossing a repository, ambiguous providers, name '
    'mismatches or non-path patches are disclosed there as well, with no member and no link. More than 64 members '
    'refuses `PROJECT.SCOPE_LIMIT` (`members:<n>>64`, S12) in either branch.\n\n'
    '*Records.* The provenance is `DiscoveryProvenanceV3`, which adds `memberRepositories` (each with its `declaredBy` '
    'sources), `workspaceDeclarations` (one per reader, with its `unresolved` entries) and `memberConfigs`. The '
    'boundary export is `AdmittedBoundaryInventoryV3`, which adds `memberRepositories`. A project with no member '
    'carries these lists empty. Schemas: `' + X + 'schemas/security-lifecycle.schemas.v1.b-s1-additions.json`.')

SL_OVERRIDES = [
    (109, 'from the account database). Output is the closed `DiscoveryProvenanceV3` (contract successor B-S1: the '
          'OpenSIP custody-state anchor of successor SX-1, and the D15 member repositories below). '
          '`DiscoveryProvenanceV1` and `DiscoveryProvenanceV2` records keep their bytes and are read under their own '
          'versions.'),
    (166, 'it are other custody roots, except the declared member repositories of a D15 multi-repository workspace '
          '(below): they are recorded as `nestedRepositories`, never'),
    (168, 'one refuses `PROJECT.EXPLICIT_PATH_INVALID` (`JOIN_CROSSES_NESTED_REPOSITORY`) whenever that repository '
          'cannot become a D15 member, because it lies inside another nested repository or because the selected root '
          'is itself in a repository.'),
    (180, 'An explicit source suppresses automatic discovery and, for a D15 workspace, declaration-reader membership '
          '(below): discovery is then restricted to exactly the explicit roots and never widened into a scan. Every '
          'directory from the'),
    (185, 'workspace globs and never writing source.' + D15),
    (195, '`src/target`, is ordinary source), and OpenSIP custody state (successor SX-1, landed with contract successor '
          'B-S1): the exact path `.opensip` at the selected root and at each admitted D15 member root, an exact anchor '
          'and never a segment matched at any other depth (a directory named `.opensip` anywhere else is ordinary '
          'source). Whatever its entry type, that path is never entered, never source and never inventoried; it is '
          'observed only as an entry of its parent directory and is never opened or listed; when it is observed as a '
          'directory it is recorded once in `prunedTrees` with reason `opensip-custody-state`; and it is always a '
          'conventional excluded prefix. Native §1.4 U-4a governs this anchor where the reference '
          '`discovery-defaults.py` does not yet carry it. A pruned tree yields no unit, no marker,'),
    (205, 'the closed `{path, reason, markerCount, markerCountBasis}` (version 2; version 3, `PrunedTreeRowV3`, adds '
          'only the reason `opensip-custody-state` for the SX-1 anchor, beside `dependency-tree`, `vcs-tree` and '
          '`cargo-build-output`).'),
    (215, 'bytes and are read as version 1, and version-2 records keep theirs and are read as version 2. A `Cargo.toml` '
          'inside a pruned'),
    (262, 'mode: `discovery.workspaceRoots` is the only configuration carrier. A D15 multi-repository workspace (above) '
          'is one project with one authority root; its members are not projects, and its declaration readers read the '
          'root\'s own native files as data and are not configuration carriers. Cases'),
    (274, 'authorizes it. VCS trees and Cargo build output are never reads, at any depth, and neither is OpenSIP '
          'custody state (SX-1), which is never source.'),
    (286, '`prunedTrees`, and from version 3 `memberRepositories`) into the closed `AdmittedBoundaryInventoryV3` '
          '(contract successor B-S1; `AdmittedBoundaryInventoryV1` and `AdmittedBoundaryInventoryV2` records keep '
          'their bytes) of relative scope'),
    (298, 'into the Plan scope descriptor\'s `excludedPathPrefixes`. D15 `memberRepositories` are not boundaries: they '
          'enter no `excludedPathPrefixes`, and the native instrument discovers their contents as ordinary directories '
          'of the root (native §1.4 U-8). An inventory whose'),
    (1323, None),  # appended below
]
SL_1323_APPEND = (
    ' D15 member repositories (S3) are bounded at 64 per project: more refuses PROJECT.SCOPE_LIMIT with '
    'REQUEST.UNSATISFIABLE (exit2) and subject `members:<n>>64`, in either declaration branch, where n counts the '
    'distinct repositories that the admitted declarations name after the placement checks and before any member\'s Git '
    'configuration or index is read. Members are never dropped to fit. That subject\'s remedy is: "This workspace '
    'declares more than 64 member repositories, the most one project admits. Name at most 64 members in '
    'discovery.workspaceRoots or --workspace-root, or select a narrower project root." It is that subject\'s remedy '
    'only; the registry-capacity subjects keep project-root law X2\'s remedy (contract successor B-S1).')

NE_U8 = (
    '\n\n  **D15 member repositories (contract successor B-S1, under law M3-B r2 item 22).** From version 3 the admitted '
    'inventory also carries `memberRepositories`: the relative roots of the D15 member repositories that security '
    'admitted (security S3). A member is not a boundary. It enters no `excludedPathPrefixes`, excludes no unit and no '
    'file, and its markers, units, folding and membership follow U-1 to U-4b exactly as for any other directory of the '
    'root. Nested repositories, nested projects and custody exclusions inside a member stay boundaries with their '
    'reasons. The subset test over `(path, reason)` is unchanged and covers boundaries only. In addition, a `vcs-tree` '
    'anchor `D/.git`, `D/.hg`, `D/.svn` or `D/.jj` that this instrument derives, or carries from the admitted inventory, '
    'with D strictly below the root and not at or below an admitted boundary, names a member path: if D is not in '
    '`memberRepositories`, the inventory refuses `native.boundary-inventory-mismatch` (`REQUEST.PRECONDITION_FAILED`). '
    'An explicit root inside a member is an ordinary explicit root; one inside a nested repository that is not a member '
    'still refuses `native.explicit-root-crosses-boundary`. `UnitDiscoveryV3.boundaries` (`UnitBoundariesV2`) carries '
    '`memberRepositories` beside the boundary rows. U-9 is unchanged: it still keys off no explicit roots and no '
    'surviving `rust` or `tsjs` unit, units inside members are surviving units, its one fallback unit is at the root '
    '`""`, and a member root is never a second fallback site. U-6 is unchanged: an edge between units in different '
    'members is an `external-module-boundary` edge like any cross-unit edge. Schemas: `' + X +
    'schemas/native-evidence.schemas.v2.b-s1-additions.json`.')
NE_CONFIG2 = (
    '\n\n**D15 under the Config2 join (contract successor B-S1, under law M3-B r2 items 20 and 22).** Explicit roots '
    'stay exact roots: discovery is restricted to exactly those roots and is never widened into a scan. The successor '
    'adds only that an exact root may lie inside an admitted D15 member repository (security S3). Under a root that is '
    'in no repository, a `discovery.workspaceRoots` root or `--workspace-root` root inside a nested conventional '
    'repository declares that repository a member, and the member contributes exactly the units its named roots are. '
    'A present array, from any layer or from `--workspace-root`, suppresses declaration-reader membership: the readers '
    'then declare no member, and every reader entry outside the members the array admitted is recorded as dropped. '
    'Exactness is not relaxed, and an explicit root inside a repository that is not a member still refuses '
    '`native.explicit-root-crosses-boundary`.')
NE_OVERRIDES = [
    (714, '  from the units: workspace root or folded member package), and OpenSIP custody state (successor SX-1, '
          'landed with contract successor B-S1): the exact path `.opensip` at the project root `""` and at each '
          'admitted D15 member root (U-8), an exact anchor and never a segment matched at any other depth, with reason '
          '`opensip-custody-state` (a directory named `.opensip` anywhere else is ordinary source). '
          '`packages/target/index.ts`'),
    (719, '  `UnitDiscoveryV3.prunedTrees` (`PrunedTreeV3 {path, reason, markerCount,'),
    (730, '  or scope input. `PrunedTreeV1`/`UnitDiscoveryV1` and `PrunedTreeV2`/`UnitDiscoveryV2` remain the '
          'historical'),
    (731, '  records for their own version-1 and version-2 bytes; version 3 (contract successor B-S1) adds only the '
          'reason `opensip-custody-state` and, in `UnitDiscoveryV3.boundaries`, `memberRepositories` (U-8). Pruning is '
          'a discovery rule, not a'),
    (822, '  `AdmittedBoundaryInventoryV3` from security (`boundary_inventory(result)`;'),
    (824, '  `nestedProjects`, `custodyExcludedUnits`, `prunedTrees` and, from version 3, `memberRepositories`) and '
          'passes it'),
    (863, '  runs the P3 fixture through both instruments.' + NE_U8),
    (931, 'permission.' + NE_CONFIG2),
    (939, 'root; `target` under every Cargo root only; `.opensip` at the project root and at each admitted D15 member '
          'root, SX-1) ∪ the admitted boundary anchors'),
    (940, '(U-8: nested repositories, nested projects, directory-custody exclusions; admitted D15 member repositories '
          'are not boundaries and add no prefix; the'),
    (4135, '  security\'s decision; this instrument consumes its `AdmittedBoundaryInventoryV3` (contract successor B-S1; '
           'version-1 and version-2 inventories keep their bytes)'),
]
IE_OVERRIDES = [
    (552, '`target` directly under a Cargo root; `.opensip` at the project root and at each admitted D15 member root, '
          'which is OpenSIP\'s own custody state and never source, successor SX-1; native §1.4 U-4a), **plus** (2) '
          'exactly the'),
]

def overrides_for(path, rows):
    parent = pin(path)
    lines = (A / path).read_bytes().decode('utf-8').splitlines()
    out = []
    for line, after in rows:
        before = lines[line - 1]
        if line == 1323 and path == SL:
            assert before.endswith('native internal aliases do not create a second public code.'), before
            after = before + SL_1323_APPEND
        assert after != before and after, (path, line)
        out.append({'parent': parent, 'selector': {'line': line}, 'before': before, 'after': after})
    return parent, out


EXPECT_BEFORE = {
    (SL, 109): 'from the account database). Output is the closed `DiscoveryProvenanceV1`.',
    (SL, 166): 'it are other custody roots: they are recorded as `nestedRepositories`, never',
    (SL, 168): 'one refuses `PROJECT.EXPLICIT_PATH_INVALID` (`JOIN_CROSSES_NESTED_REPOSITORY`).',
    (SL, 180): 'An explicit source suppresses automatic discovery. Every directory from the',
    (SL, 185): 'workspace globs and never writing source.',
    (SL, 195): '`src/target`, is ordinary source). A pruned tree yields no unit, no marker,',
    (SL, 205): 'the closed `{path, reason, markerCount, markerCountBasis}` (version 2).',
    (SL, 215): 'bytes and are read as version 1. A `Cargo.toml` inside a pruned',
    (SL, 262): 'mode: `discovery.workspaceRoots` is the only configuration carrier. Cases',
    (SL, 274): 'authorizes it. VCS trees and Cargo build output are never reads, at any depth.',
    (SL, 286): '`prunedTrees`) into the closed `AdmittedBoundaryInventoryV1` of relative scope',
    (SL, 298): "into the Plan scope descriptor's `excludedPathPrefixes`. An inventory whose",
    (NE, 714): '  from the units: workspace root or folded member package). `packages/target/index.ts`',
    (NE, 719): '  `UnitDiscoveryV2.prunedTrees` (`PrunedTreeV2 {path, reason, markerCount,',
    (NE, 730): '  or scope input. `PrunedTreeV1` and `UnitDiscoveryV1` remain the historical',
    (NE, 731): '  version-1 records for version-1 bytes. Pruning is a discovery rule, not a',
    (NE, 822): '  `AdmittedBoundaryInventoryV2` from security (`boundary_inventory(result)`;',
    (NE, 824): '  `nestedProjects`, `custodyExcludedUnits`, `prunedTrees`) and passes it',
    (NE, 863): '  runs the P3 fixture through both instruments.',
    (NE, 931): 'permission.',
    (NE, 939): 'root; `target` under every Cargo root only) ∪ the admitted boundary anchors',
    (NE, 940): '(U-8: nested repositories, nested projects, directory-custody exclusions; the',
    (NE, 4135): "  security's decision; this instrument consumes its `AdmittedBoundaryInventoryV1`",
    (IE, 552): '`target` directly under a Cargo root; native §1.4 U-4a), **plus** (2) exactly the',
}

parents, overrides = [], []
for path, rows in ((SL, SL_OVERRIDES), (NE, NE_OVERRIDES), (IE, IE_OVERRIDES)):
    parent, out = overrides_for(path, rows)
    for o in out:
        key = (path, o['selector']['line'])
        if key in EXPECT_BEFORE:
            assert o['before'] == EXPECT_BEFORE[key], key
    parents.append(parent)
    overrides.extend(out)

# ---- write generated candidates ----------------------------------------------------------
dump(SLS_ADD, sls_add)
dump(NES_ADD, nes_add)


def render():
    out = ['# B-S1 passages (generated)', '',
           'Generated by `evidence/build_b_s1.py` from the same data as `successor.json`; do not edit by hand. Each '
           'entry gives the parent, the selector, the exact accepted `before` and the candidate `after`.', '']
    for kind, rows in (('Passage overrides', overrides),):
        out += ['## ' + kind, '']
        for o in rows:
            where = '`%s` line %d' % (o['parent']['path'], o['selector']['line'])
            out += ['### ' + where, '', 'Before:', '', '```text', o['before'], '```', '', 'After:', '', '```text',
                    o['after'], '```', '']
    return '\n'.join(out)


(A / D / 'PASSAGES.md').write_text(render(), encoding='utf-8')

candidates = sorted([pin(p) for p in HAND + [SLS_ADD, NES_ADD, D + 'PASSAGES.md']], key=lambda r: r['path'])
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED B-S1 contract successor (law M3-B r2 successor S3, with law M3-C successor SX-1): the '
                 'security S3, native section 1.4 and identity section 3 passages for D15 multi-repository workspaces '
                 'and the .opensip custody-state anchor; the security and native V3 discovery records as additions to '
                 'their bundles; and the closed workspace declaration reader registry. S9, the CONFIG.INVALID remedy, '
                 'is split into unit B-S9. No code, class, exit, route, public code, inventory or product change. The '
                 'exact frozen candidate requires actual independent review and root assent.'),
    'parents': sorted(parents, key=lambda r: r['path']),
    'passageOverrides': overrides,
    'candidates': candidates,
}
dump(D + 'successor.json', record)
subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(D + 'successor.json')], key=lambda r: r['path'])}
dump(B + 'b-s1-subject.json', subject)
print(json.dumps({'overrides': len(overrides), 'parents': len(parents), 'candidates': len(candidates),
                  'subject': pin(B + 'b-s1-subject.json')}, indent=1))

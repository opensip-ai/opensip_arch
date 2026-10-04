"""Build contract successor B-S2 (law M3-B r2 successor S4): identity vcs-observation schema 3.

Writes, deterministically:
- b-s2/schemas/identity-schemas.v3.b-s2-additions.json, whose vcs-observation-v2 is copied
  from the accepted bundle, so schema 2 is unchanged by construction;
- b-s2/PASSAGES.md, a readable rendering of the two overrides;
- b-s2/successor.json and ../b-s2-subject.json.
Hand-written inputs it pins but never writes: README.md and the three evidence scripts.
Run with python3 -I -B from any directory; rerunning reproduces the same bytes."""
import copy, hashlib, json
from pathlib import Path

A = Path(__file__).resolve().parents[6]
B = 'docs/implementation/m3/config-discovery-b/'
D = B + 'b-s2/'
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
IDS = 'docs/coop/design-corrections/foundation/identity-schemas.v3.json'
IDS_PRODUCT_COPY = 'docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json'
ADD = D + 'schemas/identity-schemas.v3.b-s2-additions.json'
HAND = [D + 'README.md', D + 'evidence/build_b_s2.py', D + 'evidence/check_b_s2.py', D + 'evidence/verify_scratch.py']


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


ids = load(IDS)
v2 = copy.deepcopy(ids['$defs']['vcs-observation'])
assert load(IDS_PRODUCT_COPY)['$defs']['vcs-observation'] == v2, 'the product copy differs'
v3 = {
    'type': 'object', 'additionalProperties': False,
    'required': ['schemaVersion', 'kind', 'commitId', 'dirty', 'sourceInventoryDigest', 'members'],
    'description': ('Schema 3 (contract successor B-S2, law M3-B r2 successor S4): the VCS observation of a project '
                    'with at least one admitted D15 member repository. The top level is the selected root\'s own '
                    'observation, which is kind none because a workspace root is in no repository (security S3); '
                    'sourceInventoryDigest covers the whole snapshot inventory. members holds one row per admitted '
                    'member, ascending by path. A project with no member uses schema 2.'),
    'properties': {
        'schemaVersion': {'const': 3},
        'kind': {'const': 'none'},
        'commitId': {'type': 'null'},
        'dirty': {'const': False},
        'sourceInventoryDigest': copy.deepcopy(v2['properties']['sourceInventoryDigest']),
        'members': {'type': 'array', 'minItems': 1, 'maxItems': 64, 'uniqueItems': True,
                    'items': {'$ref': '#/$defs/vcs-member-observation'}, 'x-opensip-order': 'path'},
    },
}
member = {
    'type': 'object', 'additionalProperties': False, 'required': ['path', 'kind', 'commitId', 'dirty'],
    'description': ('One admitted D15 member repository: its root as a logical path relative to the project root, '
                    'kind git (the only member layout admitted), its resolved HEAD commit as 40 lowercase hexadecimal '
                    'digits (object format sha1; project-root law X2 refuses extensions.*), and dirty under the same '
                    'rule as a single repository\'s.'),
    'properties': {
        'path': {'$ref': '#/$defs/LogicalPath'},
        'kind': {'const': 'git'},
        'commitId': {'type': 'string', 'pattern': '^[0-9a-f]{40}(?![\\s\\S])'},
        'dirty': {'type': 'boolean'},
    },
}
fragment = {
    'artifact': 'opensip.identity-schemas.additions',
    'successor': 'B-S2',
    'status': 'PROPOSED-NOT-SELF-ACCEPTED',
    'base': pin(IDS),
    'alsoAppliesTo': [pin(IDS_PRODUCT_COPY)],
    'mergeRule': ('The base bundle\'s #/$defs/vcs-observation is REPLACED by this fragment\'s, which admits exactly '
                  'schema 2 or schema 3. vcs-observation-v2 is the base bundle\'s vcs-observation, copied unchanged, '
                  'so schema-2 admission and canonical bytes do not change. vcs-observation-v3 and '
                  'vcs-member-observation are ADDED. The record name, the snapshot\'s vcsDigest selector '
                  '#/$defs/vcs-observation and every other base member are unchanged. Hash and LogicalPath resolve '
                  'in the merged bundle. The same merge applies to the product copy named in alsoAppliesTo, whose '
                  'vcs-observation equals the base\'s.'),
    'standing': ('Closed Draft 2020-12 records for identity-and-evidence section 3 (vcsDigest), contract successor '
                 'B-S2. Design evidence, not a product implementation; C1b materializes it.'),
    '$defs': {
        'vcs-observation': {
            'description': ('The closed vcs-observation record that snapshot2.vcsDigest names: schema 2 for a project '
                            'with no admitted D15 member, schema 3 for a project with at least one (contract '
                            'successor B-S2).'),
            'oneOf': [{'$ref': '#/$defs/vcs-observation-v2'}, {'$ref': '#/$defs/vcs-observation-v3'}]},
        'vcs-observation-v2': v2,
        'vcs-observation-v3': v3,
        'vcs-member-observation': member,
    },
}

L542_BEFORE = '`vcsDigest` hashes the closed `vcs-observation` record: schemaVersion 2,'
L542_AFTER = ('`vcsDigest` hashes the closed `vcs-observation` record (contract successor B-S2 adds schema 3 for a D15 '
              'workspace, below): schemaVersion 2,')
L547_AFTER = (
    '\n**D15 workspaces: `vcs-observation` schema 3 (contract successor B-S2, under law M3-B r2 item 22).** A project '
    'with at least one admitted D15 member repository (security S3) hashes schema 3 instead: `{schemaVersion: 3, kind: '
    '"none", commitId: null, dirty: false, sourceInventoryDigest, members}`. The top level is the selected root\'s own '
    'observation. It is always `kind: none`, because a workspace root is in no repository (security S3), and '
    '`sourceInventoryDigest` keeps its meaning: the whole snapshot inventory, members\' files included. `members` has '
    'one row `{path, kind: "git", commitId, dirty}` per admitted member, 1 to 64 rows, strictly ascending by the UTF-8 '
    'bytes of `path`, which is the member root as a logical path relative to the project root. `kind` is `git`, the '
    'only member layout admitted; `commitId` is the member\'s resolved HEAD commit as 40 lowercase hexadecimal digits; '
    'and a member\'s `commitId` and `dirty` follow the same rules as a single repository\'s. The host emits schema 3 '
    'exactly when the project has an admitted member and schema 2 otherwise, so a project with no member, including a '
    'workspace root whose every declared candidate was excluded, keeps schema 2 and its exact bytes, and no existing '
    '`snapshot2` changes. Like the custody walk, that choice is a host observation (below). A schema-3 observation '
    'establishes no `vcs-revision` source correspondence: its top level names no revision, and a per-member '
    'correspondence needs its own successor. In the identity bundle, `#/$defs/vcs-observation` admits exactly the two '
    'records, and the record name and the snapshot\'s `vcsDigest` selector are unchanged: '
    '`' + ADD + '`.\n')

lines = (A / IE).read_bytes().decode('utf-8').splitlines()
assert lines[541] == L542_BEFORE and lines[546] == '' and lines[545] == 'runtime-to-source correspondence.'
assert lines[547].startswith('**What `sourceInventory` contains')
parent = pin(IE)
overrides = [
    {'parent': parent, 'selector': {'line': 542}, 'before': L542_BEFORE, 'after': L542_AFTER},
    {'parent': parent, 'selector': {'line': 547}, 'before': '', 'after': L547_AFTER},
]

dump(ADD, fragment)


def render():
    out = ['# B-S2 passages (generated)', '',
           'Generated by `evidence/build_b_s2.py` from the same data as `successor.json`; do not edit by hand. '
           'Line 547 is the blank line between the `vcsDigest` paragraph and "What `sourceInventory` contains"; its '
           'replacement keeps a blank line on each side of the new paragraph. Lines 543 to 546 are not overridden: '
           'they are left to law M3-C\'s successor VCS-1 (the meaning of `dirty`).', '']
    for o in overrides:
        out += ['## `%s` line %d' % (o['parent']['path'], o['selector']['line']), '', 'Before:', '', '```text',
                o['before'] if o['before'] else '(empty line)', '```', '', 'After:', '', '```text', o['after'], '```', '']
    return '\n'.join(out)


(A / D / 'PASSAGES.md').write_text(render(), encoding='utf-8')
candidates = sorted([pin(p) for p in HAND + [ADD, D + 'PASSAGES.md']], key=lambda r: r['path'])
record = {
    'schemaVersion': 1,
    'standing': ('PROPOSED B-S2 contract successor (law M3-B r2 successor S4): identity vcs-observation schema 3 for '
                 'D15 multi-repository workspaces, with per-member Git rows; schema 2 and every single-root snapshot2 '
                 'keep their exact bytes. Two text overrides of identity-and-evidence section 3 and one schema '
                 'fragment for the identity bundle. No code, class, exit, route, public code, inventory or product '
                 'change; C1b implements it. The exact frozen candidate requires actual independent review and root '
                 'assent.'),
    'parents': [parent],
    'passageOverrides': overrides,
    'candidates': candidates,
}
dump(D + 'successor.json', record)
subject = {'schemaVersion': 1, 'files': sorted(candidates + [pin(D + 'successor.json')], key=lambda r: r['path'])}
dump(B + 'b-s2-subject.json', subject)
print(json.dumps({'overrides': len(overrides), 'candidates': len(candidates),
                  'subject': pin(B + 'b-s2-subject.json')}, indent=1))

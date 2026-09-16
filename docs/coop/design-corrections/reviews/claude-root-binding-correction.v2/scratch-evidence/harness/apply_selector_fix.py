"""Apply the corrected F-04 selectors to the v2 scratch schema. Touches ONLY the two new
selectors added in v1; the historical CanonicalPath is left byte-identical."""
import collections
import hashlib
import json

S = '/private/tmp/opensip-design-corrections/claude-root-binding-correction.v2/scratch'
P = S + '/src25/docs/coop/design-corrections/native/native-evidence.schemas.v2.json'

NUL = '\\u0000'
BS = '\\\\'
SEG = '(?!\\.\\.?(?:/|(?![\\s\\S])))[^' + NUL + BS + '/]+'
DIR = '^' + SEG + '(/' + SEG + ')*(?![\\s\\S])'
ROOT = '^(?:|' + SEG + '(/' + SEG + ')*)(?![\\s\\S])'

SEGMENT_LAW = (
    'Segments are decided by SPLITTING ON "/" and testing EXACT equality, which is the'
    ' decision procedure the house already implements identically in two independent places:'
    ' foundation/identity-model.v3.py `ordered()` (rejects a leading "/", a backslash, a NUL'
    ' and any segment in ["", ".", ".."] for every `path`/`logicalPath` string) and'
    ' discovery-defaults.py `normalize_explicit_root()` (same four tests over `spec.split("/")`).'
    ' The negative test is therefore attached PER SEGMENT and ends with a strict'
    ' end-of-input assertion rather than "$": "$" also matches before a trailing newline, and'
    ' a ".*"-prefixed lookahead does not cross a newline at all, so a single whole-string'
    ' lookahead both accepts "a\\n/../b" (an exact ".." segment) and rejects "a/.\\n" (whose'
    ' final segment is ".\\n", not "."). No character beyond "/", backslash and NUL is'
    ' excluded, because the owning grammar excludes none: a literal newline or other'
    ' non-dot character inside a segment stays admissible. The declarative'
    ' at-most-255-characters-per-segment bound of #/$defs/LogicalPath is deliberately NOT'
    ' imported here; identity-schemas.v3 records it as a different, explicitly'
    ' non-equivalent enforcement that reaches only two Blob path fields, and neither'
    ' `ordered()` nor `normalize_explicit_root` imposes it.'
)

DIR_DESC = (
    'INTERNAL relative DIRECTORY form: one or more slash-joined non-empty segments, no'
    ' leading or trailing slash, no empty segment, no "." or ".." segment, no NUL and no'
    ' backslash. ' + SEGMENT_LAW +
    ' CanonicalPath is deliberately NOT this grammar: it admits a trailing slash and an'
    ' interior empty segment ("a//b"), neither of which is canonical for a directory used as'
    ' a membership prefix. The project root is NOT spelled here; see InternalUnitRootV1.'
)

ROOT_DESC = (
    'INTERNAL unit root: the EMPTY STRING for the project root, otherwise a'
    ' CanonicalRelativeDirV1. The external sentinel "." is NEVER a value of this field. "."'
    ' is the EXTERNAL spelling only: Config2 discovery.workspaceRoots and CLI'
    ' --workspace-root inbound (discovery-defaults.normalize_explicit_root, "." -> ""), and'
    ' the outward workspaceRoot of the shared scope record and of enumeration cells'
    ' (discovery-defaults.spell_root, "" -> "."), whose type is WorkspaceRootText and which'
    ' states that it MAY be "." and is NOT LogicalPath. A retained WorkspaceUnitV2 carries'
    ' the internal form and is never silently normalized after retention: _under_unit, _rel'
    ' and the deepest-unit length ranking all read this field as an exact prefix. '
    + SEGMENT_LAW
)


def main():
    raw = open(P, 'rb').read()
    before = hashlib.sha256(raw).hexdigest()
    d = json.loads(raw, object_pairs_hook=collections.OrderedDict)
    defs = d['$defs']

    canon_before = json.dumps(defs['CanonicalPath'], sort_keys=True)

    cd = defs['CanonicalRelativeDirV1']
    assert cd['minLength'] == 1 and cd['maxLength'] == 4096, cd
    cd['pattern'] = DIR
    cd['description'] = DIR_DESC

    ir = defs['InternalUnitRootV1']
    assert 'minLength' not in ir and ir['maxLength'] == 4096, ir
    ir['pattern'] = ROOT
    ir['description'] = ROOT_DESC

    assert json.dumps(defs['CanonicalPath'], sort_keys=True) == canon_before, 'CanonicalPath must not move'

    out = json.dumps(d, indent=1) + '\n'
    open(P, 'w', encoding='utf-8').write(out)
    after = hashlib.sha256(out.encode()).hexdigest()
    print('CanonicalPath unchanged   :', json.dumps(defs['CanonicalPath'], sort_keys=True) == canon_before)
    print('CanonicalRelativeDirV1    :', DIR)
    print('InternalUnitRootV1        :', ROOT)
    print('schema before sha256      :', before)
    print('schema after  sha256      :', after)


if __name__ == '__main__':
    main()

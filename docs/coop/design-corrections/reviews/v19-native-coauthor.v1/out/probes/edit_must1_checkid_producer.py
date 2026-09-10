"""CB7-MUST-1: the identity unit keeps its OWN copy of the producer helper; mirror the same branch.

The duplication of `coverage_result` between integration-fixtures.py and foundation/check-identity.py
is pre-existing. It is mirrored rather than unified because unifying two fixture producers is a
refactor this finding did not ask for and would move unrelated fixture identities. Soundness of the
mirror is proved, not assumed: the SAME two textual replacements are applied to the check-identity
copy, and the result is asserted equal to the already-patched integration-fixtures copy.
"""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
SRC = W / 'docs/coop/design-corrections/integration-fixtures.py'
DST = W / 'docs/coop/design-corrections/foundation/check-identity.py'

TAIL = "'confidenceMillionths':1000000,**disclosure}}"


def slice_fn(text):
    start = text.index('def coverage_result(scope_descriptor,universe,resolved,')
    end = text.index(TAIL, start) + len(TAIL)
    return start, end, text[start:end]


a = SRC.read_text(encoding='utf-8')
b = DST.read_text(encoding='utf-8')
_, _, want = slice_fn(a)
bstart, bend, have = slice_fn(b)

OLD1 = """    unavailable=None
    if blobs is not None and inventory_paths is not None:
        try:_d,_u,_r=M.parse_h_frame(blobs[universe],'native-semantic-universe')
        except Exception:_d,_u,_r=None,None,None
        if _d=='native.semantic-universe.syntax.v2':
"""
NEW1 = """    unavailable=None
    if blobs is not None:
        try:_d,_u,_r=M.parse_h_frame(blobs[universe],'native-semantic-universe')
        except Exception:_d,_u,_r=None,None,None
        if _d=='native.semantic-universe.syntax.v2' and inventory_paths is not None:
"""
assert have.count(OLD1) == 1
got = have.replace(OLD1, NEW1)

OLD2 = """                unavailable=N.syntax_capability_support(_rows,scope_descriptor['relation'],
                    scope_descriptor['resolution'],_paths,_all)
"""
i = want.index(OLD2)
j = want.index("    # A producer cannot honestly claim a COMPLETE examination", i)
NEW2 = want[i:j]
assert got.count(OLD2) == 1
got = got.replace(OLD2, NEW2)

assert got == want, 'the two copies were NOT identical before this change; mirror is unsound'
DST.write_text(b[:bstart] + got + b[bend:], encoding='utf-8')
print('mirrored ok')

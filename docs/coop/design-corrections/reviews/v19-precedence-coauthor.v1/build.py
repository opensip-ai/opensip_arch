"""Extract the exact S1.2 paragraph under review and emit the proposed replacement.

Bounded source assessment: no model, checker or schema is read for mutation and none is
written. The contract copy under inputs/ is a PROPOSED SNAPSHOT of the main coauthor's
in-progress M1 work, not a published or released contract.
"""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'inputs/docs/v2/contracts/product-v1/native-evidence.md'
raw = SRC.read_bytes()
lines = raw.split(b'\n')

# paragraph is lines 406..418 inclusive (1-based), bounded by blank lines
start, end = 406, 418
assert lines[start - 2] == b'', repr(lines[start - 2])
assert lines[end] == b'', repr(lines[end])
BEFORE = b'\n'.join(lines[start - 1:end]) + b'\n'
assert BEFORE.startswith(b'It is **not** the only scope-capability guard')
assert BEFORE.endswith(b'answered by.\n')
assert raw.count(BEFORE) == 1

AFTER = (
    b"It is **not** the only scope-capability guard, and an earlier revision of this\n"
    b"paragraph read as if it were. A separate and weaker law, stated in \xc2\xa710 and\n"
    b"published as\n"
    b"`identity-schemas.v2.json#/x-opensip-digest-domains/scopeCapabilityLaw`, applies\n"
    b"to **any** universe whose dialect form is a closed suffix table \xe2\x80\x94 TypeScript and\n"
    b"the syntax universe both \xe2\x80\x94 and asks only whether a scoped path's own suffix\n"
    b"selects a variant in the table that universe published. For the syntax universe\n"
    b"that condition is strictly weaker than the grammar law above and is implied by\n"
    b"it, because the capability registry's `data-document` class law already states\n"
    b"that **no suffix of a data grammar appears in the syntax dialect table**. For\n"
    b"TypeScript it is the *only* such law, and it is what a `clones` scope over\n"
    b"`package.json` is now answered by. Which guard reaches a given scope first,\n"
    b"however, is decided by what each boundary can see, not by which law is stronger.\n"
    b"The suffix law needs nothing but the scope's own paths, so the native Coverage\n"
    b"producer boundary already applies it to the one case it can judge from a single\n"
    b"record \xe2\x80\x94 a `source-path` relation carrying a body-identity join, which is\n"
    b"`clones` \xe2\x80\x94 whenever the caller hands it the owning universe's dialect, as Run\n"
    b"closure does. Closure runs that producer admission **before** any of its own\n"
    b"prerequisites, so a `clones` scope over a path no dialect table lists is refused\n"
    b"there, as a producer-admission failure naming the source variant, and not by the\n"
    b"grammar guard. The grammar law is neither weakened nor reordered: among\n"
    b"closure's own prerequisites it is still applied ahead of the suffix backstop,\n"
    b"and it remains the sole owner, under its own refusal names, of everything a\n"
    b"suffix table cannot see \xe2\x80\x94 the `symbol` relations, the other syntax relations,\n"
    b"and the selection case where a path's suffix *is* in the table but no selected\n"
    b"grammar row owns it. The disclosed outcome is the same published\n"
    b"`language-tier-unsupported` / `capability-missing` pair at whichever boundary\n"
    b"saw the defect; only the internal name of the first boundary changes.\n"
)

(HERE / 'before-paragraph.md').write_bytes(BEFORE)
(HERE / 'after-paragraph.md').write_bytes(AFTER)

# the replacement is a drop-in for exactly this paragraph
spliced = raw.replace(BEFORE, AFTER)
assert spliced.count(AFTER) == 1
assert spliced.replace(AFTER, BEFORE) == raw

def rep(tag, b):
    print(tag, 'bytes=%d' % len(b), 'lines=%d' % b.decode().count('\n'),
          'chars=%d' % len(b.decode()), 'sha256=' + hashlib.sha256(b).hexdigest())
    b.decode('utf-8')  # exact UTF-8 validity

rep('BEFORE', BEFORE)
rep('AFTER ', AFTER)
print('max line width before/after:',
      max(len(l) for l in BEFORE.decode().splitlines()),
      max(len(l) for l in AFTER.decode().splitlines()))
print('contract sha256 (unmodified input):', hashlib.sha256(raw).hexdigest())
print('spliced-contract sha256 (NOT written, shown for rebase):',
      hashlib.sha256(spliced).hexdigest())
print('non-ascii preserved:', sorted({c for c in AFTER.decode() if ord(c) > 127}))

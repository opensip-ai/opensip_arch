"""Integrate the repair unmet-precondition mapping clarification into S6's per-requirement
projection paragraph. PURE INSERTION: NO pre-existing byte is changed, removed or reordered;
the only change is added lines continuing that one paragraph (no blank line, so markdown
keeps it a single paragraph)."""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
before = (HERE / 'workflow.before.md').read_bytes()

ANCHOR = b"to the value mints a different `repairPlanId` that no authorization names.\n"

ADDED = (
    b"That unmet precondition is emitted once per unsatisfied requirement and carries\n"
    b"the existing `REPAIR.EVIDENCE_RUN_UNAVAILABLE` code, which here says that the\n"
    b"evidence Run cannot supply what this repair requires and asserts nothing about the\n"
    b"Run having been purged or lost \xe2\x80\x94 `evidence.purged` and `evidence.missing` keep\n"
    b"their own distinct meaning in query results. Preview therefore reaches that one\n"
    b"code by two routes, the retained-availability and replayable-assurance failure of\n"
    b"the first paragraph above and this per-requirement insufficiency, and the two are\n"
    b"told apart by the remedy, which names that requirement's `relation`,\n"
    b"`minResolution`, evidence plane and exact `deficiency`.\n"
    b"`EvidenceRequirement.deficiency` remains the typed cause carrier: no\n"
    b"per-deficiency detail code is minted, because the closed public registry is not\n"
    b"where a per-requirement outcome vocabulary belongs. An unsatisfied requirement\n"
    b"with an empty `unmetPreconditions` is **not** a conforming projection \xe2\x80\x94 the schema\n"
    b"alone admits that shape, and the emission is decided at admission, the same\n"
    b"division of labour already stated for the deficiency vocabulary.\n"
)

assert before.count(ANCHOR) == 1, before.count(ANCHOR)
after = before.replace(ANCHOR, ANCHOR + ADDED)

# byte-preservation proof: removing exactly the inserted block restores the original
assert after.replace(ADDED, b'') == before
assert len(after) == len(before) + len(ADDED)
# and the insertion is contiguous: before-prefix + ADDED + before-suffix
i = before.index(ANCHOR) + len(ANCHOR)
assert after == before[:i] + ADDED + before[i:]
# no blank line introduced: the added block continues the same markdown paragraph
assert b'\n\n' not in ADDED and after[i - 1:i] == b'\n'

out = HERE / 'workflow.proposed.md'
out.write_bytes(after)
print('before sha256:', hashlib.sha256(before).hexdigest())
print('after  sha256:', hashlib.sha256(after).hexdigest())
print('bytes before/after:', len(before), len(after), '(+%d)' % (len(after) - len(before)))
print('inserted at byte offset:', i, '(after S6 per-requirement projection paragraph tail)')
print('max added line width:', max(len(l) for l in ADDED.decode().splitlines()))

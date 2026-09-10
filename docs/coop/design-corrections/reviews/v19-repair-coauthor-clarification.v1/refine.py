"""Bounded wording refinement: resolve the scope ambiguity in ONE sentence of the S6
per-requirement projection paragraph. Every other byte of the v19 repair coauthor
proposal is copied through unchanged.

The published clause attached 'which names that requirement's relation, minResolution,
evidence plane and exact deficiency' to 'the remedy' after 'the remedy' had been
introduced as the discriminator for BOTH routes. That admits a reading requiring the
RETENTION entry's remedy to carry requirement fields, which the actual retention remedy
does not (it is a Run-level restore/regenerate), and whose 'that requirement's' has no
antecedent on a route that fires with every requirement satisfied.

The refinement keeps the discriminator claim, splits the two remedies, and attributes
the four named fields specifically to the PER-REQUIREMENT entry. It deliberately does
NOT pin the retention entry's literal string: `remedy` is BoundedText, and the contract
should not mandate fixture wording.
"""
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path('/tmp/opensip-design-corrections/v19-repair-coauthor.v1/workflow.proposed.md')
before = SRC.read_bytes()

OLD = (
    b"the first paragraph above and this per-requirement insufficiency, and the two are\n"
    b"told apart by the remedy, which names that requirement's `relation`,\n"
    b"`minResolution`, evidence plane and exact `deficiency`.\n"
)

NEW = (
    b"the first paragraph above and this per-requirement insufficiency, and the remedy\n"
    b"is what tells them apart: the retention entry's remedy names the Run-level\n"
    b"restoration that route needs, while the per-requirement entry's remedy names that\n"
    b"requirement's `relation`, `minResolution`, evidence plane and exact `deficiency`.\n"
)

assert before.count(OLD) == 1, before.count(OLD)
after = before.replace(OLD, NEW)

# exactly one contiguous region changed; everything else is byte-identical
i = before.index(OLD)
assert after == before[:i] + NEW + before[i + len(OLD):]
assert after.replace(NEW, OLD) == before
# the untouched neighbours of the edited sentence are preserved verbatim
for probe in (b"their own distinct meaning in query results. Preview therefore reaches that one\n"
              b"code by two routes, the retained-availability and replayable-assurance failure of\n",
              b"`EvidenceRequirement.deficiency` remains the typed cause carrier: no\n",
              b"to the value mints a different `repairPlanId` that no authorization names.\n"):
    assert after.count(probe) == before.count(probe) == 1

out = HERE / 'workflow.proposed.md'
out.write_bytes(after)
print('before sha256:', hashlib.sha256(before).hexdigest())
print('after  sha256:', hashlib.sha256(after).hexdigest())
print('bytes before/after:', len(before), len(after), '(%+d)' % (len(after) - len(before)))
print('max refined line width:', max(len(l) for l in NEW.decode().splitlines()))

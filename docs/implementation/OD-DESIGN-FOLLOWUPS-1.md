# OD-DESIGN-FOLLOWUPS-1: three follow-ups from the 2026-11-10 design assessment

Status: accepted owner decision; effective 2026-11-10.
Scope: priority of three items already named in accepted plans. It accepts no
contract text and changes no product law. Each item still goes through its own
authoring and review.

## Owner instruction

An independent read-only assessment of the intended final-product design was
made on 2026-11-10 at the owner's request (report:
[`design-assessment-2026-11-10.md`](design-assessment-2026-11-10.md)). It
recommended three things to do now. The owner answered:

> lets follow the reviewers recommendations

and quoted them:

> 1. Write the finding-explanation successor before M4 renderer work, with a display position and related locations.
> 2. Measure replay on the first real graph, with a stated threshold for reworking it.
> 3. Note for M5 that repair preview needs to show the change.

The details below are the lead's. They are not further quotations from the owner.

## 1. Finding-explanation successor (the quality plan's D8)

**What.** The contract successor that
[`m3/analysis-quality/PLAN.md`](m3/analysis-quality/PLAN.md) §6 calls for and
lists as D8: reason, evidence path, scope statement, suggested action and
limitations on every finding, rendered by every advertised renderer. To that it
adds what the assessment found missing: a display position, related locations,
and a region in the SARIF output. The successor also covers the advisory
candidate kinds, not only findings.

**Constraint kept.** Line offsets stay out of the finding fingerprint. A display
position is for showing a finding, not for identifying it.

**When.** Drafted now. Accepted before any M4 renderer work starts.

**Review.** It is a new contract choice, so it gets its own review
([OD-PACE-1](OD-PACE-1.md), dropped rule 2, last sentence).

## 2. Replay measurement on the first real graph

**What.** The M3-M-TS1 record (PATH row 18) reports, for each fixture
(body-parser, then constructs): the time of the admission and replay phase on
its own, the source-file count, and the size of the admitted graph (facts,
findings and retained predicate nodes).

**Threshold for reworking the replay implementation.** Either of:

- replay alone takes more than a quarter of the warm budget for the
  repository's size class in the quality plan's §5.2: 0.5 s for small, 2 s for
  medium, 7.5 s for large;
- replay time per retained predicate node on the larger fixture is more than
  1.5 times that on the smaller one, which is the superlinear growth the
  preliminary measurement showed.

A quarter, because the approved single-file edit target is 2 s on a medium
repository against an 8 s warm budget, and replay runs before every sealed
result.

**If the threshold is still missed at real volume after an implementation
rework,** it becomes a design question about complete replay
(`docs/v2/contracts/product-v1/identity-and-evidence.md` §4), brought to the
owner. Not before.

**Also to settle with the measurement:** whether `--ephemeral` analysis runs
replay. The assessment could not find it stated.

The threshold is the lead's proposal. The owner can change it. The approved
budgets themselves, and the 2026-10-14 decision to re-test on the reference
runner, are unchanged.

## 3. Repair preview must show the change (for M5)

**What.** `repair preview` returns paths, digests and byte counts per file. No
contracted surface returns the new content or a diff, so a person asked to
consent to an apply sees hashes. The repair successor written for M5 adds a
way to see the change before consenting to it.

**When.** At M5 planning. Nothing is authored now.

## Not decided here

The assessment's other points wait for measurements: the share of dead-code
findings that are repair-eligible, brief ranking and reason codes, a yield
target, and closed-loop tasks in the qualification successor.

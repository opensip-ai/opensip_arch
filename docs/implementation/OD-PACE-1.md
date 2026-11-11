# OD-PACE-1: minimal process, product delivery first

Status: accepted owner decision; effective 2026-11-10.
Scope: how OpenSIP implementation work is planned, checked, reviewed and
recorded from this date. It changes process, not product law. It is not a
technical acceptance verdict for any pending subject.

## Owner instruction

> we need to be delivering on the code pushing the project ahead with minimal process to slow us down. we should keep process where it is needed, but our pace is too slow and we need to move much faster

The lead then proposed the rules below and asked whether the owner accepted
them as written. The owner answered "yes". The rules are the lead's wording.

## Why

Between 2026-11-02 and 2026-11-10 the product repository received no commits.
The work in that period went to custody commitments, authority handoffs and
checkpoint records around three test files that had not been run. When a
worker ran them on 2026-11-10 it took about five minutes.

## Rules kept

1. **The full test lane is green before anything merges to main.** The lane
   commands of an accepted plan are run unchanged.
2. **One Codex review per change**, of the actual diff and the test output.
   The reviewer gives its first verdict before it sees the author's
   explanations.
3. **Nobody accepts their own work.**
4. **Two reviewers** only for security-boundary code, signing, durable on-disk
   formats and final qualification.
5. **The owner decides** signing and notarization, pushing and publishing, and
   changes to product scope.

   **Standing permission to push, given 2026-11-10.** The lead asked for
   "standing permission to push after each green, reviewed integration". The
   owner answered: "Standing permission to push after is granted". The lead
   pushes `main` of the product and architecture repositories after an
   integration whose lane is green and whose review is accepted, and reports
   each push. Anything else that publishes still needs the owner.

## Rules dropped

1. **Custody intervals and human commitments** for reading or running local
   tools. The run log records the tool versions and the hashes of the binaries
   used. That log is the admission record where a check asks for one.
2. **Separate plan reviews** for a unit that implements an already-accepted
   design. A plan of about a page is reviewed together with the code. A new
   architecture or contract choice still gets its own review.
3. **The initial-then-final double review cycle.** One review; the author fixes
   the findings; the reviewer confirms the fix.
4. **Per-step authority handoffs, one-attempt-no-retry rules and checkpoint
   files.** A unit has one brief. A run that fails for an infrastructure reason
   is rerun and the rerun is noted. The live map gets one line per state
   change.
5. **Hash manifests of every input.** Work is pinned by git commit.

## Effect on accepted plans

Accepted plans, sources and review verdicts stand. Where an accepted plan
requires a step these rules drop, the step is not performed and the unit's
brief says so. Where it requires a product check — a test, a lint, a boundary
check, a probe — that check is still run and still has to pass.

The effort targets and the two-failed-rounds rule in the adopted
delivery-priority amendment remain. [OD-LEAD-1](OD-LEAD-1.md) and
[OD-REVIEW-1](OD-REVIEW-1.md) remain; where OD-REVIEW-1 or an older plan asks
for more reviewers than rule 4 above, rule 4 governs.

## Cost accepted

A thinner evidence trail and fewer independent reviews of each step. The full
lane and a review on every merge remain, and M6 qualification still gathers
its evidence in full.

# Correction to grok-creation-budget412 advice (after runtime35 primary report)

Root disposition `docs/implementation/m2/reviews/grok-creation-budget412-advice/root-assessment.md` was read after this 35/410 review. Original 412 `ADVICE.md` / `advice.json` are **not** mutated.

**Acknowledge.**

1. **`actualModelIdentity`.** Root is right that 412 `advice.json` `actualmodel` stored a placement sentence. That field should have been a model identifier (as `review.json` `actualModelIdentity` is here: `independent-grok-runtime35-source410`). Placement belongs under recommendations.

2. **Do not pre-set `failed=true` before the closure.** Nested `charge`/`scope` on the same attempt would immediately `Closed`. The draft Drop guard already latches unsuccessful exit, unwind, and swallowed nested `Err` while allowing nested calls during an open scope. That 412 advice item is **withdrawn**.

3. **Zero-cost at capacity is not a reset.** After a real failure the existing scope already returns `Closed`. Successful reservations stay charged. Withdrawn as a defect.

4. **`LIMIT - used` underflow.** With `new()` at zero and charge-before-increment, underflow is not reachable on the private type. `checked_sub` is defense-in-depth, not a demonstrated bug. Withdrawn as a reachable defect.

5. **Public trait.** A trait is not itself a boolean receipt; using an arbitrary impl as native proof would be the flaw. Narrow the warning to that misuse.

6. **Platform `new()`.** Placement cannot by itself stop a helper from constructing a second ledger. One-instance protocol belongs to the attempt/capability composition. Agree.

**Contest / keep.**

- Host-only budget type still cannot be named by security; a lower-crate ledger **borrowed** by `Budget` remains the right direction (root accepted that).
- `record()` vs retained-object slot is still a join question (root asked to distinguish retained records from temp buffers).
- Live `Budget::scope` still latches inner `Err` only if the **return** is `Err`; a caller that catches and returns `Ok` leaves `failed` set (inner already set it) — unless the inner path never used `guard`. Root’s separate finding on that existing helper is outside 412 draft tests; do not claim Grok tested a fix.
- `HostCapture` ignoring `&mut Budget` stands as a legacy adapter, not a creator producer.
- Counters still do not mint first-party creator eligibility, ACL bounds, or account-service allocations.

No creator approval follows from this note.

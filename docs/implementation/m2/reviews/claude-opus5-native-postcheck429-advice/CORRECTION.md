# Correction to the 429 composition advice — API sketch

Actual Claude Opus 5, 2026-09-21. Bounded, read-only, advisory. No native jobs (root owns the lane),
no repository edits, no delegation. The original `ADVICE.md`, `advice.json` and `hashes.txt` are
preserved byte-for-byte and pinned below; this file corrects them, it does not replace them.

**Root is right on all three points. I verified each against source rather than taking them on
report, and root's executable counterexamples (431) then demonstrated all three at runtime.** The
conclusions of the original advice stand — provisional ordinary I/O outcome, whole original bracket,
terminal budget failure, standalone-wrapper limit, and "existing law suffices". The errors were
confined to the API sketch, and one of them made the sketch actively unsound.

### Root's 431 counterexamples, independently checked

I read `probe_postcheck431.py` and its logs rather than accepting the summary. All three tests pass
(`exitCode 0`, `3 passed; 0 failed`), the probe was appended to a **copy** of the product — live
`crates/security/src/journal_store.rs` contains zero occurrences of the probe module and the product
is clean at `5b42fd6` — and the probe is scoped inside the crate-private `journal_store` module, so
root correctly claims no external public-type access and no authority. No native capture was tested.

| Counterexample | What it demonstrates |
| --- | --- |
| `effect_cost_is_not_available_from_postcheck_allowance` | `effect(edges 3, edges 2)` then `post.spend(edges 3)` ⇒ `ReservedPostcheck`, `used == 5`, latched. The effect portion is charged but not spendable from `remaining`. |
| `total_prepaid_allowance_does_not_partition_body_from_postchecks` | pooled `effect(default, edges 5)` lets a 4-edge body spend first, so the intended 2-edge postcheck is refused and never runs (`after == false`). |
| `actual_owned_provisional_enum_can_escape_as_success_without_finalizer` | my exact proposed signature returns an owned `Unreadable(Bound)` **out of** `effect` as a success value with `!owner.is_failed()`. |

The third is the sharpest: it uses my proposed signature verbatim, `WorkFailure<Infallible>` error
slot included, and shows a *failure* outcome escaping as a *success* value while the owner stays
unfailed — precisely the "callers mistaking pending bytes for admitted evidence" hazard root's audit
named. The `Infallible` slot does do what I claimed of it (only a budget refusal can be `Err`); my
mistake was treating that as if it also addressed escape. Two unrelated properties, conflated.

One thing worth stating because it is load-bearing for what I now recommend: **counterexamples 1 and
2 refute the pooled and handle-passing designs, and the shape recommended below is immune to both** —
the reader holds no spending handle at all, so it can neither draw on the effect portion (case 1) nor
consume pooled postcheck space (case 2), and `remaining` stays equal to the derived postcheck
allowance for the whole bracket. Case 2 in particular rules out the "sum the costs then spend the
read portion first" variant, which is why I do not propose it.

## 1. The allowance was not partitioned — sketch unsound as written

Confirmed in `crates/platform/src/work_ledger.rs`:

```rust
let total = effect.checked_add(postchecks)…?;
s.charge(total)?;
action(&mut ReservedPostchecks { ledger: s.ledger, remaining: postchecks })
```

`effect` charges `effect + postchecks` but exposes **only `postchecks`** as `remaining`. My sketch
then passed that same `post` to `read_bounded_provisional`, so the read would have spent from the
postcheck allowance. The effect reservation would sit charged and unusable while the read consumed
the space the checks depend on — the precise failure the bracket exists to prevent. Prepayment alone
neither partitions the work nor proves the checks cannot be refused. That part of my advice was
wrong.

**The fix is to remove a privilege, not to add machinery.** The reader should never receive a
spending handle. `effect(read_cost, postcheck_cost, …)` is already correct and already disjoint the
moment the reader takes a **derived bound** instead of `&mut ReservedPostchecks`:

```
budget.work_in::<_, directory_record_capture::Error>(|platform| {
    platform.effect(read_cost, postcheck_cost, |post| {
        // remaining == postcheck_cost, established before any native work and
        // untouchable by the reader, which holds no spending handle at all.
        let read: OperationalBytesObservation =
            read_bounded_provisional(&mut file, read_bound);   // bound, not a ledger
        post.spend(inspect_cost)?;  let after = inspect_operational_file(&file, uid, groups)?;
        post.spend(dir_cost)?;      directory_policy::inspect(directory, uid, groups)?;
        post.spend(name_cost)?;     check_name(directory, leaf, &file)?;
        if before != after { return Err(Operation(Error::Changed)); }
        match read { Present(raw) => Ok(raw), Unreadable(e) => Err(Operation(Error::Read(e))), … }
    })
})
```

This is the codebase's existing idiom, not a new one: `Budget::capture`'s callback already receives
`cap: usize`, and `read_one` already takes `cap: usize` and already returns
`Error::Read(OperationalReadFailure::Bound)` when the size exceeds it. Exceeding `read_bound` stays an
**operational** bound failure carried as provisional data; it is not a ledger failure, so terminal
budget semantics are untouched. Disjointness is structural — the reader cannot spend postcheck space
because it cannot spend at all.

**Evaluating root's two options, as asked.**

- **B — upfront read reservation plus a private bounded read counter (recommended).** What is
  sketched above. No new ledger API, no new privilege, disjoint by construction. The cost is
  precision: the read is prepaid at its worst case and actual consumption is not separately metered,
  exactly like the accepted 427 `account_observation_cost` precharge, with no refund. That trade is
  forced by root's own requirement that the checks cannot be refused.
- **A — protected child allowance.** A `ReservedPostchecks::split(&mut self, cost) -> Result<ReservedPostchecks<'_>, …>`
  that carves `cost` out of `remaining` into a child borrowing the same ledger. This keeps
  per-attempt metering *and* disjointness, and is the better long-term shape. It is genuinely new API
  on a security-sensitive type and carries its own proof obligations: the parent's `remaining` must
  decrement atomically at split time, the child must not outlive or escape the parent, and a child
  failure must still latch the one ledger. It needs its own review; I do not recommend it as the
  first step.

Either way, **no second `WorkLedger`** and no reset — and note that a private bounded counter is not
a ledger: it cannot latch, refund, or grant work, and it performs no branch-local reset of anything
already charged.

## 2. The claimed type barrier does not exist — retracted

Confirmed in `crates/security/src/journal_store.rs:1068`:

```rust
pub enum OperationalBytesObservation { Absent, Present(Vec<u8>), Unreadable(OperationalReadFailure) }
```

An owned enum whose variants are constructible anywhere the type is nameable, already constructed and
matched in `installation_observation.rs`. It is `pub` within the crate-private `journal_store`
module, so it is not part of the crate's external surface — but that is irrelevant to the problem,
because the native owner lives inside this crate, which is exactly the scope where the escape is
reachable. Root's counterexample 3 demonstrates it directly.

**I retract these claims from the original advice:** that taking `&mut ReservedPostchecks` means "a
provisional value can only exist inside a prepaid bracket", that the type has "no public
constructor", and that it is non-escaping. None holds. A borrowed argument constrains borrowed
returns, not an owned `T`; my runtime39 escape probe applied to a borrowed `&mut WorkScope`, and I
over-generalized it to an owned value. `non-Clone` alone would not help either, and the type is not
even non-Clone today.

**Corrected position.** Keep the entire provisional outcome **inside the private native owner** —
which is what `read_one` already does with a plain local `let read = …`. That needs no type-system
cleverness and no new public type, and it is the minimal correct path.

If a type barrier is genuinely wanted later, it is a real design with a real proof obligation: an
invariant brand tied to the bracket (`Provisional<'brand>`), constructible only by the bracket,
consumed by a finalizer that also takes the postcheck evidence, plus a compile-fail test that it
cannot escape the closure. Making `OperationalBytesObservation` itself opaque would additionally be a
cross-module change, since other modules construct and match it today. I state that as an obligation,
not as something the sketched signature achieved.

## 3. The error type does not flow — corrected, with a small concrete fix

Confirmed: `Budget::work` fixes its callback to
`Result<T, WorkFailure<retained_metadata_index::Error>>`, while the sketch's `Error::Read`,
`Error::Changed`, `Error::File` and `Error::Directory` are `directory_record_capture::Error`
variants. Those cannot flow through the existing signature, so my `?` operations would not compile.

The fix is smaller than root's note implies, because the conversion direction already exists.
`directory_record_capture::Error` has a `Budget(BudgetError)` variant with
`impl From<BudgetError> for Error` where `BudgetError = retained_metadata_index::Error`, and
`native_record_capture` has the matching `impl From<M::Error> for Error`. So one generic parameter
suffices:

```rust
pub(super) fn work_in<T, E: From<Error>>(
    &mut self,
    action: impl FnOnce(&mut opensip_platform::WorkScope<'_>) -> Result<T, opensip_platform::WorkFailure<E>>,
) -> Result<T, E>
```

mapping `WorkFailure::Operation(e) => e` and `WorkFailure::Budget(b) => E::from(work_error_budget(b))`,
with the existing `work_error` retained for today's callers. Both native owners already satisfy the
bound. No new error variant and no wrapper type — but it *is* additional API work that needs review,
and I should have said so rather than implying the existing `work_error` mapping settled it.

## What follows from law, and what does not

Unchanged and still my position, with root agreeing: **existing law suffices; no amendment.** §8
requires the rechecks after read/parse failure on the same budget with no branch-local reset and
makes budget failure incomplete/unavailable; §4 makes the raw syscall error preserved but not
decisive; §6 dispositions Indeterminate as unavailable with no retry.

What does **not** follow from law, and which I should have separated more clearly in the original:

- Law mandates the *outcome* (required checks must run and be accounted; they must not be refused),
  not any particular **allowance-partitioning mechanism**. Disjoint allowances are an engineering
  consequence of meeting that outcome, not a rule quoted from §8.
- Law says nothing about **type-level opacity** of provisional data. That is API hygiene from root's
  audit, not law, and the original advice blurred the two.

## Retained limitations, unchanged

Native cost derivation remains the real blocker: there is still no derivation for
`inspect_operational_file`, `directory_policy::inspect` or `check_name`, so `read_cost`,
`read_bound` and `postcheck_cost` cannot be sized yet; the 427 account precharge (derived constant
plus a test pinning observed call counts) is the model. ACL, name-service and OS-profile opaque
allocations, latency, cache effects and allocator overhead stay outside these counters. One generic
read wrapper qualifies no custody, creator, InitialActor, permit, P0 or current authority. A supplied
result is not authority. The nine tests listed in the original advice still apply, with two additions
drawn from root's counterexamples: **assert that `remaining` equals the derived postcheck allowance
immediately before the read and that the read cannot reduce it**, and **keep root's three 431 cases
as standing regression tests**, since each pins a property the corrected shape depends on.

**No approval is implied.** This corrects an advisory sketch. It approves no unit, no source, no law
change, and it is not a review of source427, the 425 experiment or the unfrozen 428 reader.

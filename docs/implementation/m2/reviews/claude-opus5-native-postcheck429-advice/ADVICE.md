# Composition advice — budgeted native bounded reads with mandatory postchecks (429)

Actual Claude Opus 5, 2026-09-21. Bounded, read-only, advisory. **This approves nothing**: not
source427, not the unfrozen 428 reader, not any unit, and it amends no law. No native, Cargo or Node
jobs were run — root owns the serial lane. No repository edits. Output only under
`/tmp/opensip-implementation/reviews/claude-opus5-native-postcheck429-advice`.

## Answer in one paragraph

The selected law already settles the disposition; what is missing is a **primitive**, not a rule. The
governing shape is: *the raw operation result is a premise, not a conclusion — the conclusion is the
conjunction of (raw result, required postcheck results), and the guarded boundary belongs to the
owner's whole bracket, never to the raw read.* An ordinary I/O or parse failure must therefore be
carried as **provisional data** inside a prepaid bracket so the mandatory rechecks can run and be
accounted; a **budget/limit failure is terminal at the instant it occurs** and forbids the rechecks,
yielding incomplete/unavailable. Those two failure kinds need distinct types, not distinct
conventions. No law amendment is required.

## Why naive substitution is wrong, mechanically

Root's audit is correct and I can name the exact mechanism. The 428 helpers are

```rust
pub fn read_bounded_reserved(reader, max, post: &mut ReservedPostchecks<'_>)
    -> Result<Vec<u8>, WorkFailure<ReadFailure>> {
    post.scope(|post| read_charged(reader, max, |cost| post.spend(cost)))
}
```

Both wrappers return **every** failure — including `WorkFailure::Operation(ReadFailure::Io(_))`, an
ordinary I/O error — as an `Err` out of a guarded boundary. The guard's `Drop` then sets
`ledger.failed = true`. That is correct standalone behavior, and I verified the same guard shape at
runtime37/38/39. But dropped into `directory_record_capture::read_one`, it latches the owner at
line 153, before lines 155–157 run. The consequence is a fork with no good branch: either the
mandatory rechecks are skipped, or they run while every `charge`/`spend` returns `Closed` — so they
are unaccounted. Both branches contradict selected law §8, quoted below. Reserved allowance cannot
be spent after closure and a replacement ledger is forbidden, so there is no escape at that point.

## The law, and whether it suffices

**It suffices. I recommend no amendment.** Three passages settle it between them.

`initial-root-binding-owner-selection-v1/owner.md` §8:

> A fenced observation session retains originals and rechecks all relevant contributing owners **even
> after later read/parse failures**; any observed failure latches unavailability. … All name
> enumeration, captures, graph edges/bytes and original-owner checks use the **same authoritative
> operation budget; no branch-local reset**. **Budget/limit failure is incomplete/unavailable, never
> 'no ancestor' or permission to repair.**

That is the whole asymmetry: read/parse failure ⇒ rechecks still required, on the same budget;
budget failure ⇒ incomplete/unavailable, and "never … permission to repair" forbids further work.

§4 supplies the same composition one level up, for effects, in the law's own words:

> The raw EEXIST/AlreadyExists error alone is insufficient: **a failed original-stage postcheck makes
> the outcome Indeterminate even when the primary syscall error is preserved.**

and §6 dispositions it: *"Any Indeterminate publication result, including AlreadyExists with failed
postcheck | Latch unavailable, no winner shortcut, retry, deletion, registration or success
receipt."*

So "hold the raw result, finish the required checks, then conclude" is not a new idea needing
sanction — it is the published rule for publication, and §8 states its observation-session analogue.
The live `read_one` already implements it: it stores `read`, runs the after-checks with `?`, and only
then matches on the held outcome.

One consequence worth making explicit to root, because it is easy to miss: on the **effect** path,
pre-reserving the postchecks is not hygiene, it is what makes the §4 loser route *reachable at all*.
The no-publication loser route requires a **complete typed** `AlreadyExists AND Unchanged` result. If
budget exhaustion can prevent the postcheck from running, every contended publication degrades to
Indeterminate ⇒ unavailable. Under-reservation is therefore not merely unsafe, it is
self-defeating.

If root nonetheless wants the bracket rule stated rather than derived, the minimal edit is to §8's
budget sentence — adding that an owner which must recheck after a fallible operation reserves those
checks **before beginning it**. I would call that optional clarification, not a required amendment,
and I would not amend §4 or §6 at all.

## Concrete minimal API and ownership path

Everything below uses existing accepted APIs except **one** new primitive.

**The one new primitive — a provisional read.** The public 428 wrappers stay as they are; they are
right for standalone use. The native owner needs a variant whose only `Err` is a budget failure:

```rust
// The I/O outcome is DATA; only a budget refusal is an error out of this call.
fn read_bounded_provisional(
    reader: impl Read, max: usize, post: &mut ReservedPostchecks<'_>,
) -> Result<OperationalBytesObservation, WorkFailure<Infallible>>;
```

That signature is the whole design. It makes the law's distinction **type-level** rather than
conventional: a budget failure cannot be mistaken for data, and an I/O failure cannot latch. The
existing private `read_charged` already has the right internal shape — a charge closure and a bounded
loop — so this is an outcome-type split, not a new algorithm. It must take `&mut ReservedPostchecks`,
which means a provisional value can only come into existence inside a prepaid bracket.

**The bracket, using only existing APIs.** `Budget::work` already lends `&mut WorkScope<'_>`, and
`WorkScope::effect` already prepays a two-part reservation and hands back the non-constructible
`ReservedPostchecks`:

```
budget.work(|platform| platform.effect(read_cost, postcheck_cost, |post| {
    let read = read_bounded_provisional(&mut file, cap, post)?;   // budget failure only
    post.spend(inspect_cost)?;  let after = inspect_operational_file(&file, uid, groups)?;
    post.spend(dir_cost)?;      directory_policy::inspect(directory, uid, groups)?;
    post.spend(name_cost)?;     check_name(directory, leaf, &file)?;
    if before != after { return Err(Operation(Error::Changed)); }
    match read { Present(raw) => Ok(raw), Unreadable(e) => Err(Operation(Error::Read(e))), … }
}))
```

Four properties fall out, and each is already enforced by machinery I verified rather than by
convention: the postchecks are prepaid, so they cannot be refused by exhaustion mid-bracket; a
postcheck failure is a real `Err` and latches, which is correct; the held read failure is reported
only after every check passes, preserving `read_one`'s existing precedence; and 427's
`ReservedPostchecks::scope` means a helper failure **caught inside** the callback still closes the
owner, so no adapter can swallow a postcheck failure and claim a clean result.

**Ownership placement.** The bracket must open **outside** `Budget::capture`. That callback
deliberately receives only `cap: usize` and no budget handle, so a prepaid bracket cannot live inside
it without changing that signature — which I would not do. Open the bracket at the
`native_record_capture::capture_with` level, which already holds `b: &mut Budget` and already calls
`b.scope(...)`. Retention then follows the admitted outcome: `b.retain(collection, &raw)` still
charges object+bytes **before** `Arc::from`. Note the read buffer and the retained record are two
real allocations and are charged twice on purpose; that is not double counting and should not be
"optimized" away.

**Provisional-value hygiene.** Root's audit requires that callers cannot mistake pending bytes for
admitted evidence. Minimum: keep `OperationalBytesObservation` non-`Clone`, non-serde, with no public
constructor, obtainable only from a call that takes `&mut ReservedPostchecks`. Optional hardening, if
the type ever becomes public: make it consumable only by a finalizer that also takes the postcheck
result, and add a negative compile test that it cannot escape the closure — the same probe shape that
already rejects `WorkScope` escape.

## Disposition of each failure kind, and precedence

| Failure kind | Mandatory postchecks | Reported outcome | Latch |
| --- | --- | --- | --- |
| Budget/limit refusal (charge or spend) | **not run** — running them is work after terminal failure | incomplete/unavailable; never absence, "no ancestor" or permission to repair (§8) | immediately |
| Raw read I/O failure | **must run**, from the prepaid allowance | held as data; reported only if every postcheck passes | on bracket exit |
| Parse/bound failure (size > cap, no terminator) | **must run** | same as I/O | on bracket exit |
| Postcheck failure (file, directory, name, ACL, changed) | is itself the check | **takes precedence** over the held raw failure — preserve `read_one`'s current order | yes |
| Effect postcheck failure or unknown visibility | reservation already spent | Indeterminate ⇒ unavailable; no retry, no loser route (§4, §6) | yes |

Precedence in one line: **budget failure is terminal in time; postcheck failure outranks the held raw
failure in reporting; the raw failure is reported only when all required checks pass.** The existing
`Budget::work_error` mapping already keeps budget outcomes in their own variants
(`ObjectLimit`/`EdgeLimit`/`ByteLimit`/`Cap`/`Closed`/`Profile`), distinct from `Read`/`Changed`/
`File`/`Directory`, so no new error variant is needed and §8's "never 'no ancestor'" is representable
today. That match is exhaustive with no wildcard, so a future platform variant is a compile error
rather than a silent mis-map.

## Tests to require before any native wiring

1. After a raw read I/O failure, **every** mandatory postcheck executes — assert via the existing
   `Phase` interpose seam — and each is charged against the same ledger.
2. Precedence, both directions: raw failure reported when all postchecks pass; postcheck error
   reported (and raw failure discarded) when one fails.
3. Budget exhausted **before** the read: zero native callbacks, outcome unavailable/limit, never
   absence. (The 427 `account_reservation_refuses_before_any_native_callback` pattern.)
4. Budget exhausted **during** the bracket: no postcheck runs afterwards; every later `spend` returns
   `Closed`.
5. Prepaid postchecks spend only from `remaining` and add nothing to `used` — no second charge.
6. A recreated cache or second ledger cannot reduce `used` or reopen the bracket. (The runtime38
   `recreated_cache_cannot_reset_work` pattern applied to the reader.)
7. Unwind through the bracket latches and leaves the reservation spent, with no refund.
8. Effect path: an indeterminate postcheck after a write yields unavailable — **not** the loser route
   and **not** a retry.
9. Negative compile test: the provisional outcome cannot escape the bracket.

## Open questions and unqualified premises

- **Cost derivation is the real blocker.** The bracket shape is implementable with today's APIs; its
  *numbers* are not. No derivation exists for `inspect_operational_file`, `directory_policy::inspect`
  or `check_name`. The 427 account precharge is the model to copy: a derived constant plus a test
  that pins observed call counts against the real algorithm, so the bound cannot drift.
- ACL, name-service and OS-profile opaque allocations, latency and cache effects remain outside these
  counters, as does allocator overhead. The reservation bounds requested caller-owned work only.
- Whether the provisional primitive belongs in platform (public, opaque) or private to security.
- The `edges` dimension now carries native API-call counts and traversal steps on one ledger; adding
  postcheck syscalls sharpens that overlap and affects how operation-wide limits should be chosen.
- Whether a *partially* completed postcheck set after a budget refusal should be distinguishable from
  none in diagnostics. Law makes both unavailable; only observability differs.

**No approval is implied by any of the above.** One generic read wrapper qualifies no custody, no
creator, no InitialActor, no P0 and no current authority; a supplied result is not authority; and
none of this constitutes review of source427, the 425 reader experiment or the unfrozen 428 file,
which I read only as reference.

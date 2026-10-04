CODEX2 re-review: law X4 r8, round 3. It follows your round-2 review (`reviews/codex2-x4-r8-round2`; REQUIRED-FINDINGS: RF-X4R8-R2-1 and NB-X4R8-R2-1). r8 is still J1's successor **S11**, the gate word, with the total first-cause rule.

This is a **law review**. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-x4-r8-round3.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- No product builds or test runs. Timing-sensitive lanes may be using this machine. Do not run any lead set.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What is asked

RF-X4R8-R2-1 found that I1 was not established at the guard's entry. `StopOnUnwind` can latch a successful lease-free first read bare, and `start` would then install a guard with no cause.

The lead's decision is LD8-10: **refuse before any guard exists**.
- **Where.** `OperationGuard::start` creates the empty stop-cause record, rebinds the monitor to the stop handle bound to it, and reads the gate under that record's lock.
- **If the gate is latched,** it refuses on the existing `OperationRefusal::Live(FailStop { latched })` row, with no guard and no observer.
- **If it is clear,** it installs the guard, and I1 holds at entry.

NB-X4R8-R2-1 qualifies "no wait" into three properties.

**The questions:**
1. Is RF-X4R8-R2-1 closed? Is NB-X4R8-R2-1 addressed?
2. Does round 3 keep everything you passed in round 2? That covers FC once I1 holds, `CertainRefusal`, X4-F3's scope (X3d's call sites and the X3d record note) and the lock order.
3. Does round 3 change any accepted outcome, apart from S11's declared changes?
4. Is anything else wrong?

## Pins

The pins are in `hashes.txt`. Apart from the subject and this request, every pin is an accepted snapshot, a round snapshot, or a review record.
- **The subject:** `docs/implementation/m2/live-guards-x4/PROPOSAL.md`, X4 r8 round 3. It is the subject of `subjectSha256`.
- **The diff base: `live-guards-x4/PROPOSAL-r8-round2.md`** (`eb3bd04c…`, 84,067 bytes, = `reviews/codex2-x4-r8-round2/review.json`'s `subjectSha256`). These are your round-2 subject bytes. Diff PROPOSAL-r8-round2.md against PROPOSAL.md.
- **Earlier rounds and the accepted predecessor:**
  - `PROPOSAL-r8-round1.md` (`ee758471…`);
  - `PROPOSAL-r7.md` (`fc8490f4…`, = `reviews/grok-live-guards-x4-r7/review.json`'s `subjectSha256`). Against it, round 3 still changes only the title and the history line's 35-byte acceptance note.
- **Your reviews:** `reviews/codex2-x4-r8/review.json` (round 1) and `reviews/codex2-x4-r8-round2/review.json` (round 2).
- **Sources and consumers** (accepted snapshots, unchanged from round 2):
  - J1 r5, `m3/host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`);
  - X3d r9, `m2/commit-session-x3d/PROPOSAL-r9.md` (`c727001a…`);
  - X7 r7, `m2/finalization-x7/PROPOSAL-r7.md` (`7757935c…`);
  - M3-L r5, `m3/provider-protocol-l/PROPOSAL-r5.md` (`f654ee4e…`).
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `cca4fe4`, read-only. Main is now `d2c00a9`, and none of the cited files changed. Neither X4-F3 nor J3b is integrated. The lines round 3 adds:
  - `crates/security/src/revocation.rs`:
    - `:80-91`, `StopOnUnwind`, whose comment covers a successful read made from a destructor during unrelated unwinding;
    - `:129-152`, the guard that drops before `read_sampled_with` returns.
  - `crates/security/src/custody/operation_guard.rs`:
    - `:148-171`, `LeaseFree` and its three bare handles;
    - `:174-189`, `first_read`, which accepts `Ok` without checking the gate;
    - `:372-406`, `OperationGuard::start`, which creates `cause: None` and spawns the observer.
  - `crates/security/src/custody/operation_handoff.rs`:
    - `:110` and `:139`, `OperationRefusal::Live` and its row;
    - `:1015-1044`, the first read;
    - `:1077-1099`, where `FirstRead::Monitor(reason)` maps to `Live(FailStop { reason.subject() })` at `:1085-1088`;
    - `:1218-1233`, `start`'s call and its `Observer` refusal.

## The shape of the diff (round 2 to round 3)

- **The r8 header.**
  - "What it adds" gains the entry check.
  - Row 11 of "r8 changes" gains a round-3 sentence.
  - A new "Round 3" paragraph and a "Round 3 changes" table, R3-1 to R3-8 (`:93-113`), come before "## Problem".
- **Item 2's r8 note** gains a round-3 sentence: a latched first read does not reach a guard.
- **S11.6.**
  - I1's base case is rewritten (`:403`).
  - New bullet, "The guard's entry" (`:405-429`), with the five-step entry rule, the proof of I1 at the actual entry, and what the rule preserves.
  - The placeholder-withdrawal text rests on the entry rule.
  - Source 4 now covers every `StopOnUnwind` trigger (`:448`).
  - A new "What 'no wait' means" bullet (`:463-469`).
- **S11.8.**
  - W-9 gains the entry order.
  - W-10 is rewritten into the three qualified properties (`:563-568`).
  - New: W-11, a lease-free first read during unrelated unwinding (`:569-576`), and W-12, the entry race (`:577-581`).
- **S11.9.** X4-F3 gains the entry rule in `start`, and one mapping arm in the handoff onto the existing `Live` row. Its tests gain W-11 and W-12.
- **S11.10.**
  - LD8-2's "never waits" and its rejected "lock around the word" are qualified.
  - LD8-6's "must not wait" now reads "must not wait for a monitor read".
  - LD8-8 rests on the entry rule.
  - New: LD8-10 (`:722-737`), with its table of rejected alternatives.
- **S11.11 and S11.12.** S11.11 gains "Round 3: the entry gap" (`:750`). S11.12 gains an X2 item (`:766`): X2's law is unchanged, and X4-F3's one mapping arm in X2e's handoff code is recorded.
- **Forbidden substitutes.** A new group, "The guard's entry (r8 round 3, LD8-10)" (`:810`).

## The entry rule, as round 3 states it (S11.6, LD8-10)

`OperationGuard::start` runs five steps, in this order:
1. **Create the record.** The new stop-cause record holds no cause.
2. **Rebind the monitor.** It takes `LeaseFree` apart and rebinds the monitor's stop to the operation's stop handle, bound to that record. After this step, no bare `StopObserver` or `OperationGate` latch is reachable outside the guard's stop transitions.
3. **Check the gate.** It takes the record's lock and reads the gate's word (`SeqCst`).
4. **If `LATCHED` is set, refuse.** It releases the lock and refuses. The handoff maps the refusal to the existing `OperationRefusal::Live(StopCause::FailStop { subject: "latched" })`: `OBSERVER.FAIL_STOP` 4, subject `latched`, the value of `:1085-1088`.
   - No guard is created and no observer thread is spawned.
   - The latch is not cleared, the monitor history is kept, and nothing is recorded.
   - It is made at the same point as `start`'s existing thread-spawn refusal. No session exists, so no end-path `REV` is appended.
5. **If `LATCHED` is clear, install.** It releases the lock, spawns the observer, and returns the guard. I1 holds at entry.

**The argument that I1 holds at the guard's actual entry:**
- **Nothing can latch bare after the check.** No bare latch exists after step 2, and the observer starts only at step 5.
- **A bare latch before the check is caught at step 3.** That includes the first read's unwind latch, and any latch through the other lease-free handles.
- **From step 5 on,** every latch is a stop transition.

**Rejected, as recorded in LD8-10's table:**
- carrying a pre-creation cause into the guard;
- clearing or re-arming the latch;
- recording the bare latch as `CertainRefusal`;
- creating the guard, with an invariant-row exception;
- checking only at `first_read`'s return;
- removing `StopOnUnwind`'s latch on success.

## Decide

1. **RF-X4R8-R2-1.**
   - **Your counterexample.** Under the entry rule, does it now end in the `Live(FailStop { latched })` refusal with no guard? The counterexample is a destructor's successful first read during unrelated unwinding, `StopOnUnwind`'s bare latch, then `first_read` returning `Ok`.
   - **The proof.** Is the step order (record, rebind, check under lock, spawn), with its argument, a sound proof of I1 at the guard's actual entry?
   - **Completeness.** Does any bare-latch path reach `start`'s installed guard that round 3 misses? Check the three lease-free handles at og:148-171, and the handoff between `:1044` and `:1233`.
2. **What is preserved.** Are `StopOnUnwind`'s conservative behaviour, the monitor history, never-reset and the existing vocabulary all preserved? In particular:
   - no clearing;
   - no `CertainRefusal`;
   - no invariant-row exception;
   - the `Live` row and its `latched` subject unchanged.

   Is "no end-path `REV` at the handoff" right?
3. **Source 4.** Does it now describe every `StopOnUnwind` trigger, both before the guard's entry and after it?
4. **X4-F3's scope.** Is adding the entry rule in `start`, and one mapping arm in X2e's handoff code (`:1224-1233`) onto the existing `Live` row, acceptable as X4-F3 scope? Is the X2 record item enough, with no change to X2's law?
5. **NB-X4R8-R2-1.** Are LD8-2, LD8-6, S11.6's "What 'no wait' means" and W-10 now limited to the three properties? Those are no wait for the monitor's mutex, no I/O or wait under the cause lock, and no added cause-lock wait on a successful admission. Is native scheduling still excluded?
6. **Controls.**
   - **W-11:** a lease-free first read during unrelated unwinding refuses on `FailStop { latched }`, with no guard.
   - **W-12:** a bare latch on each lease-free handle just before `start` never yields a cause-less guard.
   - **W-9:** the entry order.

   Do these cover the entry rule? Are their seams outside any critical section?
7. **Round 2's passes still hold.** FC with I1, `CertainRefusal`, X4-F3's scope with X3d's call sites, and the lock order.
8. **Preservation.**
   - Against PROPOSAL-r7.md, does every r7 sentence survive verbatim, apart from the title and the acceptance note?
   - Apart from S11's declared changes, does any accepted outcome of X4 r7, X3d r9, J1 r5, X7 r7 or X2 change?
9. **Anything else wrong.**

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with an id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"priorFindings"`: RF-X4R8-1, NB-X4R8-1, RF-X4R8-R2-1 and NB-X4R8-R2-1, each closed or open, with a reason;
- `"noAcceptedOutcomeChanged"`: true or false, judged apart from S11's declared changes;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"preservedSnapshot"`: PROPOSAL-r7.md's path, bytes and sha256;
- `"diffBase"`: PROPOSAL-r8-round2.md's path, bytes and sha256.

Do not commit.

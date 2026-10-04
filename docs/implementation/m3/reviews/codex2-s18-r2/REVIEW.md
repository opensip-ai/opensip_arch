# S18 r2 — ACCEPT-DESIGN-UNIT

Reviewer GROK2. Design unit S18, the final-output-section contract successor of law M3-J1 r4. This round answers r1's RF-1. The review directory keeps the name the builder emits.

Subject `docs/implementation/m3/host-pipeline-j/s18-subject.json`, 1621 bytes, sha256 `d22282a3e91728256ba509e0976f9bf4f1fa2b0fb58bb2fc3318a5a236ffc403`. Eight members. Successor `docs/implementation/m3/host-pipeline-j/s18/successor.json`, 15617 bytes, sha256 `e83430adfb20730566721274e9ef5e6688adca6b743039d16a5baf881f0e1503`. `s18-unit.json` is the lead draft and is not part of the subject. No cargo. `~/Library/Application Support/OpenSIP` is absent.

## Verdict

ACCEPT-DESIGN-UNIT. No required findings.

RF-1 is resolved. Where the final output section applies, *before-settle*, *final-output* and *after-settle* are disjoint and cover every signal, an interrupted invocation included. Where the section does not apply, both definitions reduce to the readings r1 left in place. NBO-1 and NBO-2 are recorded for their owners and are not applied here. The record selects at `392499e` on top of CRC-1.

## RF-1

The after-settle parenthetical spans two lines on each parent. r2 overrides all four. Each `before` is that parent line, and each `after` is the line plus one insertion.

| Line | Insertion |
|---|---|
| WS:227, WSE:229 | `*after-settle* (every required step` becomes `*after-settle* (after the settlement point: every required step` |
| WS:228, WSE:230 | `already terminal):` becomes `already terminal and, where the final output section below applies, the required output returned):` |

Read across the pair, both parents say: *after-settle* (after the settlement point: every required step already terminal and, where the final output section below applies, the required output returned): the aggregate is **not reclassified**; the settled class stands.

WSE:229 still begins "status affects gating, not commit identity." WSE:230 still ends "Settled aggregates retain the required-step D9", and the next line still supplies "Run-selection rule".

The paragraph on WS:231 and WSE:235 changes in one place. "and not earlier, so *after-settle* begins only then" becomes "and not earlier: that return is its settlement point, so *after-settle* begins only then". The rest of both `after`s is the r1 text. The `before`s are unchanged.

That is the same settlement point LD-4 already used for the section: the invocation settles when the decided envelope's output returns, and not earlier. The parenthetical now uses it. The wording differs from r1's suggested "only once that section's required output has returned" by also naming the settlement point on the opening line, and by saying "the required output returned". The condition is the same. The plan copy's row E already says "Every required step terminal and the required output returned", and that copy is unchanged.

For an interrupted invocation the render step is `cancelled` at the output decision point, and `cancelled` is a terminal step outcome. While the termination output is still being written, every required step is already terminal and the output has not returned. The new conjunct keeps that interval out of after-settle. The paragraph classifies a signal there as *final-output*. After the output returns, the parenthetical and the settlement sentence both place the signal in after-settle.

## The partition

A signal is classified by the phase in which it arrives.

Where the section applies:

- *before-settle* (WS:225 and WSE:225, unchanged from r1) requires some required step not yet terminal and a signal observed no later than the output decision point. At that check the render step is not yet cancelled, so the first conjunct holds, and the paragraph names the signal before-settle.
- *final-output* is the interval the paragraph already defined: from the decision, once the envelope is fixed, until that envelope's output returns. A signal in that interval is deferred. It does not reclassify the aggregate, select an interrupted form, or cancel a step.
- *after-settle* begins at the return. That is the settlement point. Both conjuncts hold only then: the required steps are terminal, and the required output has returned.

During the write, before-settle's first conjunct is false once the render step has been cancelled, and after-settle's output conjunct is false until the return. The signal has one phase. After the return, before-settle is false because the steps are terminal, and the section has ended because it runs until the return. A signal then is after-settle.

On the non-cancelled path the render step stays non-terminal until the output returns, so a signal during the write is still not before-settle: the r1 conjunct requires the signal no later than the decision point. It is not after-settle until the return. It is final-output.

Where the section does not apply, both "where the final output section below applies" conjuncts add nothing. Before-settle remains "some required step not yet terminal". After-settle remains "every required step already terminal", which the colon names as the settlement point. No output-returned wait is added for an invocation the section does not cover.

## The observations

NBO-1 is cross-law item 4 and LD-5. INV5 is not a candidate. At `392499e` its `Cancellation.phase` description still says after-settle is every required step already reached a terminal outcome. The item tells the invocation-record owner to add "and, where the final output section applies, the required output returned" when that description is restated. Until then a phase-O signal stays out of the record.

NBO-2 is cross-law item 2 and LD-9. S-OP-2 r6:653 still says "200 ms after it starts on normal exit, 100 ms on cancellation". The item tells O1 that "on cancellation" means a decided `interrupted` envelope, so an O signal during a success envelope keeps the normal drain. The plan copy's row O already says that, and `operability/PLAN.md` is the r1 bytes, 74185 bytes, sha256 `69af0f1b…`.

## What else changed

Against `r1-members/` (r1 subject `9d184011…`):

- The six r1 selectors, their parents and their `before`s are unchanged. The four `after`s other than WS:231 and WSE:235 are byte-identical. Those two `after`s differ only by the settlement-point insertion above.
- Four selectors are new: WS:227, WS:228, WSE:229, WSE:230.
- Parents are unchanged. `standing` now counts ten overrides and names the after-settle lines. Candidate pins moved with the regenerated members.
- `PASSAGES.md` is the regenerated ten-override text, and its header names `392499e`.
- `copies-report.json` changes `productRev` to `392499e`, adds the four after-settle roles, records CRC-1's bound entries at WS:308 and WSE:312, and retargets the plan parent's standing sentence to `392499e`.
- `build_s18.py` emits the insertions, defaults to `392499e`, and names `codex2-s18-r2`. `check_s18.py` defaults to `392499e` and checks ten overrides, one insertion per after-settle line, and the parenthetical read across both lines. `verify_scratch.py` expects ten overrides, and its docstring's example base is `392499e`.
- README.md carries the r2 table, the reviewer, the base, LD-2, LD-4, LD-5, LD-9, cross-law items 1d, 1g, 2 and 4, the review points, binding and the evidence runs.
- The plan copy is unchanged.

No other passage text moved.

## Selection at 392499e

The lock pin matches `git show 392499e3a42ab9f45d517b8c267a83031abf3863:design-lock.json`, 335667 bytes, sha256 `d1b2a5d1…`, 83 contract successors. From `cd5958b` to that commit only `design-lock.json` changed. `verify_design.py`, INV5, `bootstrap.rs` and `delivery.rs` match the pins, which are the bytes r1 cited.

CRC-1's selectors are WS:308 and WSE:312. S18's ten lines are 225, 227, 228, 231 and 1393 on WS, and 225, 229, 230, 235 and 1466 on WSE. None is CRC-1's.

`build_s18.py --check` reports identical bytes, including the unit draft. `check_s18.py --rev 392499e` passes 133 checks and reports no failures: the ten `before`s equal the parent lines, no bound entry and no in-flight record touches a selector, and the plan copy still touches only r3 lines 293, 328, 335, 336 and 433. `verify_scratch.py --rev 392499e` passes, design-only: 83 to 84 successors, ten overrides, no supersession, inventory v134, 55 inheritance rows. A later conflicting override of WS:231 is refused.

All 35 pins in `hashes.txt` match, including the eight subject members.

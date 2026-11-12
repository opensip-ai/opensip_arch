# X12-A r1 — record amendment to X12's X12d text (corpus target)

2026-11-11. Drafted by a lead-dispatched design author (Claude Opus 5.5, route R2-DEEP, effort medium) from
`LC/x12d-ts/SCOPE-r1.md` §1 and the lead's rulings of 2026-11-12 (`LC/x12d-ts/QUESTIONS.md`).
Status: **PROPOSED, r1.** It needs one independent Claude review, then the cross-vendor review, before X12d-TS's C1
freezes (PA1's premise rule, PA1:330-333). It binds nothing and changes no existing file, registry or lock.
Marks: **SETTLED-BY-TEXT** (restates accepted law), **PROPOSED** (needs review).

## Short names

Architecture main `fa6fa0fba`; product main `1bd328f3` (paths without prefix). `LC` = `.opensip-implementation-cache/lead-2026-10-25`.
Lines are those of the accepted bytes; the banner file `PROPOSAL.md` is offset by the number in brackets.

| Name | Document |
|---|---|
| **X12** | `docs/implementation/m2/policy-admission-x12/PROPOSAL-r4.md` (accepted, Grok) [+2] |
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md` (accepted, CODEX2) [+4] |
| **X5** / **I1** | `m2/replay-join-x5/PROPOSAL-r4.md` [+2] / `m3/preview-pack-i1/PROPOSAL-r3.md` [+2] |
| **PA1** | `LC/pa1/PLAN-AMENDMENT-TS1-r3.md` |

**Amended selectors.** (1) X12:266, the units bullet: "regeneration of the synthetic replay corpus onto the bundled test
pack, with the M3 Plan builder (item 9)". (2) X12 item 9 (X12:214-224) gains one note; its text is kept as X12's own
state. This is the amendment MC8 item 19 part 4 names: "This is a record amendment to X12 r3's X12d text" (MC8:1101;
X12-A in MC8's successor table, MC8:1152; edge of C4b, MC8:1187).

## Clauses

**A1. The corpus target. SETTLED-BY-TEXT (MC8:1101).** X12:266 reads, after amendment: "**X12d (M3), inventory
successor.** The Run-closure application of `check_plan_pack` inside replay, and regeneration of the synthetic replay
corpus onto the release preview pack `opensip.preview.typescript.pack:1`, with an empty `typescript` file population, so
the rule evaluates nothing, with the M3 Plan builder (item 9; X12-A). Its parts are MC8 item 19. It must land before any
analysis producer can reach X5." Basis: "When S = 0, nothing is evaluated (COMP:26)" (I1:237). "With the M3 Plan
builder" keeps its r4 sense of placement: X12d is C4's inventory successor (MC8:1097), not a Plan the builder produces (A8).

**A2. The reason. SETTLED-BY-TEXT (MC8:1101).** `check_plan_pack` always uses `RELEASE_PACKS`, and the test registry is
`cfg(test)`-private to the evaluator, so storage, host and crash-matrix builds never see it. **Citation correction:**
MC8:1101's `policy.rs:1361-1367` is now `evaluator/src/policy.rs:1410-1416` (`check_plan_pack_in(&RELEASE_PACKS, …)` at
:1415), and its `policy.rs:1412` is now `:1461-1463` (`#[cfg(test)] mod pack_tests`), which includes `TEST_PACKS`
(`policy_pack_tests.rs:20`).

**A3. Rejected: a test registry reachable downstream. SETTLED-BY-TEXT (MC8:1108; X12:276).** A feature-gated test
registry is a new cfg seam on admission needing an X8/X9 site amendment; X12 forbids "a `cfg(test)` row or test registry
reachable from a release build".

**A4. The pins are amended, not deleted. SETTLED-BY-TEXT (MC8:1100; MC8:1114).** After X12d they pin that
`check_plan_pack` is wired exactly once, in replay. **Citation correction:** MC8:1100's `fact_admission_tests.rs:661-668`
is now the forbidden list at `host/src/fact_admission_tests.rs:665-681` (`"check_plan_pack"` at :671); its
`configuration_tests.rs:449-450` is now `:507`, in the configuration projection's forbidden list, whose meaning X12d does
not change (the projection still never calls it).

**A5. Item 9 keeps its text. PROPOSED (form; lead ruling).** X12:220 ("X12 does not insert `check_plan_pack` into
`replay_run` …") stays as the history of X12's state at r4. Note added after X12:224: "*X12-A:* X12d inserts
`check_plan_pack`, and MC8 item 9's detector join, into `replay_run` after the Plan is read and before
`derive_evaluation` (MC8:1098-1099)."

**A6. Item 10's `check_plan_pack` tests stand. SETTLED-BY-TEXT (X12:245; MC8:1101 amends only the corpus).** They are
evaluator unit tests over `TEST_PACKS` and never pass through `replay_run`. (The scope's "X12:272-ish" is X12:245.)

**A7. Every replayed corpus. SETTLED-BY-TEXT for the scope; PROPOSED for the negative-case reading.** 19.1 wires the join
into `replay_run` itself (MC8:1098), and MC8 forbids "a corpus Plan naming `"fixture"` after X12d" without qualifier
(MC8:1112). So once wired, every Run any test or tool replays through `replay_run` names the release pack; none is
exempt. The control "no replayed corpus Plan names a non-release pack" covers every fixture file and every test-built Run.
The corpora found so far (scope §1; the pack counts are the scope's decode): `security/tests/fixtures/journal-seal-replay.native-owner-r1.json`
(1 Run, `fixture.file-observed`); `host/tests/fixtures/replay-fixtures.native-owner-r1.json` (36 `fixture.file-observed`,
1 `fixture.semantic-atom`); storage's crash-matrix synthetic `storage/src/crash_matrix_support/run_candidate.rs`, built
from the first (:2-4); the evaluator's test-built Runs (`evaluator/src/atoms.rs:4467`). Callers of `replay_run(` also sit
in host `native_owner_tests.rs`, `tests/admission_tests.rs`, security `journal_store.rs` and storage `commit_tests.rs`.
**This list is what X12d-TS's C0 census will confirm; it is not closed.** *Proposed reading:* a Plan built to be refused
(C4-T14's re-pointed Runs, MC8:1117; item 10's "corpus Plan naming `"fixture"` is refused", X12:245) is a negative case,
not a corpus Plan, and the control requires it to be refused.

**A8. What a corpus Plan must carry. PROPOSED.** A regenerated corpus Plan must pass the pack join (19.1), the detector
join (19.2; MC8:474-476) and whatever `derive_evaluation` itself requires for the release pack with an empty `typescript`
file population (at least `policy.rs:588-596` and `composition.rs:765-778`: a `kind: detector` closure that is a
`semanticClosures` member). It need not meet item 18 (MC8:1075-1094) in full: item 18 binds C4, the builder ("When the
selection admits …, C4: …", MC8:1076), and MC8 itself holds a Plan without `typescript.imports` lawful (C4-T13, MC8:1094).
- **What a corpus Plan does not show:** it is a synthetic fixture, not a Plan the product would build. It shows nothing
  about item 18's EnumerationPlan, the imports request, the symbol inventories or any evaluation of the rule; C4-T11,
  C4-T12 and C4-T14's TS leg are the controls that do.
- **Stop.** One accepted sentence may require more: X12 forbids "a Plan whose `policyPackIds` or `policyDigest` did not
  come from an `AdmittedPack`" (X12:288). A8 covers what the Plan carries, not where those two fields come from (O2).

**A9. The generator. PROPOSED.** Pinned records change only by their generators, under either outcome; X12d-TS's first
worker establishes which holds before regenerating anything.
- **(a) The original runner,** if it can be parameterized to target the release pack: the architecture runner that
  materialized the corpora (`docs/implementation/m3/native-publication/native-owner-patterns-materialization-r2/runners/`;
  product commit `a62fbd7c`), changed on a reviewed architecture branch. Condition: it reproduces today's corpora
  byte-for-byte before the change.
- **(b) Otherwise,** a drift-checked generator in product test support, labelled synthetic, as `run_candidate.rs` already
  is (:15-19). Condition: the worker records exactly why (a) fails.

**A10. Edges. SETTLED-BY-TEXT (MC8:1102), already met.** I1-c and I1-b2 are integrated (`m3/IMPLEMENTATION-STATUS.md:249`).

**A11. The refusal row and carrier.** Row **SETTLED-BY-TEXT**: X5 item 5's structural row, `EVALUATION.INPUT_REFUSED`
(MC8:1098-1099; X12:218; X5:77). Carrier **PROPOSED** (lead ruling Q1): the existing `ReplayError::Structure(
RetainedWalkError::Policy(e))` (`evaluator/src/replay.rs:20`, `full_walk.rs:40`) for both joins; no new variant.

## What this record does not do

It adds no law beyond MC8 item 19. It does not cover Rust Plans (X12d-RS; PA1 §1.2, "Must not claim: X12d complete; the
join exercised on a Rust Plan"). It does not settle how the Plan build receives the pack: that is the provider-request
unit's, by a separate lead ruling (the owner's typed `&AdmittedPack`, not strings).

## Open points

- **O1. Today nothing checks the pack at replay, and the first Run waits for X12d-TS.** `replay_run` reads the Plan
  (`replay.rs:177-180`) and calls `derive_evaluation` (:202) with no pack check between. The Plan build compares the
  Plan's pack fields with caller-supplied strings (`host/src/plan.rs:156-157`, :312-340); its `check_plan_pack` call is
  `#[cfg(test)]` (:968, :1024). No TS1 Run counts as M3-M-TS1 before X12d-TS lands: the join "must land before any
  analysis producer is wired" (X12:222; X12:266); MC8 forbids "a replay path without the join" (MC8:1113) and rejects
  "leaving replay unwired until J" (MC8:1109); J2b-TS consumes X12d-TS (PA1 §1.2).
- **O2. Does X12:288 reach a synthetic corpus Plan?** If it does, the corpus Plan's pack id and digest must be the
  accessors of `admit_pack(Named("opensip.preview.typescript.pack:1"))` (`policy.rs:836-842`); a Rust generator (A9 (b))
  can take them so, and a Python runner (A9 (a)) cannot without a product-side source. Needs review or a lead ruling.

## Consequences

X12d-TS (C0 census, C1 corpus, C3 wiring, C4 pins) works under A1-A11; its C1 may be drafted, not frozen, before this
record is accepted. The provider-request unit and J2b-TS own the Plan-build pack carrier.

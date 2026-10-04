# Native ProjectId registry owner selection v3 (record)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. **Proposed r2, not accepted.** Not code.

v3 is a record successor to the selected registry owner v2 (`project-registry-owner-selection-v2`). It takes v2's own form: a successor record (`successor.json`) that amends v2's `owner.md` by exact passages. It decides nothing new. It records, in the registry owner's own text, what accepted law J-RW r4 decided.

## r2 changes

r1 was reviewed by CODEX2 (`docs/implementation/m2/reviews/codex2-jrw-successors-r1/registry-owner-selection-v3/review.json`; REQUIRED-FINDINGS, one required finding). r1's exact reviewed bytes are kept, as a record only, in `r1-snapshot/`: the subject manifest (`0bd640d3…`, 454 bytes), `README.md` (`4ec39357…`, 7,654 bytes) and `successor.json` (`c6d860cf…`, 12,684 bytes). They are not subject members.

| Finding | Change |
|---|---|
| **RF-JRW-S2-1** (REG:9 already has a selected override) | **Accepted, as CODEX2's fix states it.** REG:9's current meaning is not v2's raw line. It is the override that `initial-root-binding-owner-selection-v1` selected, bound at product `d2c00a9` (`design-lock.json:4051-4071`; that record's `passageOverrides`, `:333-344`). r1's raw-parent override of the same line conflicts with it (`verify_design.py:409-411`), and r1's text dropped that unit's accepted initial-root clarification.<br>- **REG:9 is now a contract passage supersession** of that selected override, in law VD2's form, as SD-7 first did (`m3/supervisor-d/sd-7/successor.json`). `supersedes` names the selected record by exact pin, with its parent and line selector. `before` is that override's full `after`. `after` is the same text plus the J-RW append, so every accepted initial-root sentence stays.<br>- **REG:60, :74 and :76** stay raw-parent overrides, unchanged from r1. No selected unit touches them.<br>- **Updated:** V3-1, V3-2, the change table below, the standing text, and the manifest pins: three overrides and one supersession.<br>- **The review.** The independent design-unit review must list that exact target in `supersededPassages` (`verify_design.py:420-426`).<br>- **Not done:** removing the selected unit, or changing the verifier. |

## Where it comes from

J-RW r4, the accepted resume/repair writer law, names this record as its successor RW-S2 (JRW:680):

> J-RW is the operation owner that authorizes ordinary, random-kind reservation completion (REG:9, :74). Completing a strict-prefix marker in place is the reservation's own interrupted step, not an overwrite (REG:60). **(r2)** It is lawful only with the complete namespace present; REG:76's order covers every present-marker form, not only the exact one. Adoption, move and abandonment are unchanged.

| Name | Document | sha256 |
|---|---|---|
| **REG** | `docs/implementation/m2/project-registry-owner-selection-v2/owner.md`, the selected v2 owner. REG:NNN is its line. | `2d4b65c9…` |
| **IRB** | `docs/implementation/m2/initial-root-binding-owner-selection-v1/successor.json`, the selected record whose override is REG:9's current meaning (43,921 bytes) | `3a713c5c…` |
| **JRW** | `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, the J-RW r4 bytes Codex accepted (`m3/reviews/codex-resume-repair-jrw-r4`) | `9c53bce7…` |

The owner law that implements the completion is X2. Its revision r10, item 6c, was accepted by CODEX2 beside r1 (`m2/project-root-x2/PROPOSAL-r10.md`).

## What it changes

Three line overrides and one passage supersession on REG.
- **REG:60, :74 and :76 (overrides).** Each keeps its v2 line whole and appends one space and the text below. So each override's `after` equals its `before`, a space, then that text.
- **REG:9 (supersession).** Its `before` is IRB's selected `after` for REG:9: v2's line plus IRB's initial-root-binding sentences. Its `after` equals that `before`, a space, then the text below.

`successor.json` holds the exact strings.

| # | REG line | Form | What the appended text records | JRW |
|---|---|---|---|---|
| 1 | :9, scope | supersession of IRB's override | J-RW is the operation owner that authorizes ordinary, random-kind reservation completion, and what its authorization is. IRB's initial-root text stays whole. | :680; item 2 (:189-193); X-RW-1 (:696-698) |
| 2 | :60, marker publication | override | Completing a strict-prefix marker in place is the reservation's own interrupted step, not an overwrite. It is lawful only inside an authorized completion, with the complete namespace present. | :680; item 3.2 (:242-250); X-RW-2 (:699-701) |
| 3 | :74, explicit reservation recovery | override | J-RW is that independently authorized operation. It never runs in the crashed process, never as the constructor's fallback, and never on a read. | :680; item 2 (:174-176, :189-192) |
| 4 | :76, completion | override | Completion may find a strict-prefix marker and complete it in place, only with the complete namespace present. The ordering rule covers every present-marker form, not only the exact one. | :680; item 3.4 (:346-371); LD-13 (:781) |

### The appended text

1. **REG:9:** (v3, J-RW RW-S2) For ordinary, allocationKind=random reservation completion, that operation owner is law J-RW, M3's resume/repair writer (`docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, item 2). Its authorization is the write gate's ordinary write admission for a durable request on the same root, whose recorded locator and incarnation agree with the row: the authorization class, on the same root, that created the reservation. It adds no CLI surface. Adoption, move, fork, retirement and abandonment keep their own owners, unchanged.
2. **REG:60:** (v3, J-RW RW-S2) Completing a marker in place is not an overwrite when its bytes are a strict prefix (the empty prefix included) of the RESERVED row's own marker frame. It is the reservation's own interrupted create-new step. It writes only the missing suffix at the existing length, rewrites no existing byte, and then makes the file and parent durable. It is lawful only inside an authorized reservation completion, with the complete namespace present (below).
3. **REG:74:** (v3, J-RW RW-S2) For an allocationKind=random row, J-RW is that independently authorized operation. Completion runs as its own classified step inside a later, separately admitted durable write, under the installation fence. It never runs in the process that crashed, never as the constructor's fallback, and never on a read.
4. **REG:76:** (v3, J-RW RW-S2) Ordinary reservation completion of an allocationKind=random row may also find a marker that is a strict prefix (the empty prefix included) of the row's own marker frame. It completes that marker in place, as the marker publication paragraph above states, and only when the reservation's complete initial namespace footprint is admitted present. The ordering rule above covers every present-marker form, not only the exact one: RESERVED plus a present marker of any form (exact, zero-length, a strict prefix, ACL-omitted or private) and an absent namespace is not a lawful crash prefix, and ordinary reservation completion refuses it before any effect. This changes no row of the observation table above, which classifies without writing.

## Lead decisions

Each is made under the owner's standing direction of 2026-09-30, and each names the alternative it rejects.
- **V3-1. The form is v2's, with VD2's supersession where a passage is already selected (r2).** v2 is a bound contract successor in the product's design lock (`design-lock.json`, `contractSuccessors`, at product main `d2c00a9`). So v3 is one too: a successor record that amends its parent by exact passages, a subject manifest (`project-registry-owner-selection-v3-subject.json`), and a design-unit review.
  - **Raw-parent overrides** carry a line that no selected unit has given a meaning: REG:60, :74 and :76.
  - **A contract passage supersession** carries REG:9, whose current meaning is IRB's selected override. It names IRB's record, parent and selector exactly, as SD-7 named SD-5's (`verify_design.py:348-369`), and its review lists that target in `supersededPassages` (`:420-426`).
  - **Rejected:** a PROPOSAL-style revision that edits `owner.md` in place, because a selected candidate's bytes are never edited; a full new copy of `owner.md`, which v2 needed for its carrier change, but which four passages do not need (the S21 form, `m3/host-pipeline-j/s21`); and **(r2)** r1's raw-parent override of REG:9, which conflicts with IRB's selected override (`verify_design.py:409-411`).
- **V3-2. Append to the current meaning, never rewrite it (r2).** Each passage keeps its current meaning whole and appends to it. For REG:60, :74 and :76 that meaning is v2's line. For REG:9 it is IRB's selected `after`, so IRB's accepted initial-root sentences stay word for word.
  - **Rejected:** rewriting REG:76's "RESERVED plus an exact marker and absent namespace is NOT its lawful crash prefix" to name every marker form, which would change accepted words when the appended sentence states the wider rule; and **(r2)** appending to v2's raw REG:9, which withdraws IRB's text, a withdrawal RW-S2 does not authorize.
- **V3-3. The observation table and the reference model stay as they are.**
  - **The table (REG:37-44).** A strict-prefix marker still reads as malformed evidence on every read (REG:44), as J-RW requires on every path but its own step (JRW:371).
  - **The model (REG:96, `reference/`).** Its ordinary durable-prefix table gains no row. J-RW's strict-prefix marker states are tested natively, by J4b's controls (JRW RW-C1, RW-C16), not by REG's labelled model.
  - **Rejected:** extending `registry_model.py` and its results. That reopens v2's frozen evidence, for a state whose labels the model cannot make real.
- **V3-4. This is the selection's v3, not a registry v3.** The carrier stays `I/project-registry.v2`, `schemaVersion` 2. REG:1, the title, is not overridden, so nothing reads as a new carrier.
  - **Rejected:** retitling REG as v3, which would read as a carrier or schema change.

## What does not change

Everything else in v2, and IRB's selected unit: the carrier and its schema; the physical placement; the reference model and its results; the observation table; allocation, adoption, move, abandonment and retirement; the S9 bridge; IRB's initial-root text at REG:9; and every other line of `owner.md`. No public command, wire field, error code, schema, inventory, verifier or product change.

## Binding

- **Review.** v3 needs an independent design-unit review: `ACCEPT-DESIGN-UNIT`, its `subjectManifestSha256`, and `supersededPassages` equal to the record's one `supersedes` entry, in record order. Then the lead's root assent goes in `project-registry-owner-selection-v3-unit.json`.
- **Product.** Binding v3 into the product's `design-lock.json` is product work. It belongs to J-RW unit J4b, which RW-S2 gates (JRW:663, :680).

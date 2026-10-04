# Native ProjectId registry owner selection v3 (record)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the autonomous run. **Proposed, not accepted.** Not code.

v3 is a record successor to the selected registry owner v2 (`project-registry-owner-selection-v2`). It takes v2's own form: a successor record (`successor.json`) whose exact line overrides amend v2's `owner.md`. It decides nothing new. It records, in the registry owner's own text, what accepted law J-RW r4 decided.

## Where it comes from

J-RW r4, the accepted resume/repair writer law, names this record as its successor RW-S2 (JRW:680):

> J-RW is the operation owner that authorizes ordinary, random-kind reservation completion (REG:9, :74). Completing a strict-prefix marker in place is the reservation's own interrupted step, not an overwrite (REG:60). **(r2)** It is lawful only with the complete namespace present; REG:76's order covers every present-marker form, not only the exact one. Adoption, move and abandonment are unchanged.

| Name | Document | sha256 |
|---|---|---|
| **REG** | `docs/implementation/m2/project-registry-owner-selection-v2/owner.md`, the selected v2 owner. REG:NNN is its line. | `2d4b65c9…` |
| **JRW** | `docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, the J-RW r4 bytes Codex accepted (`m3/reviews/codex-resume-repair-jrw-r4`) | `9c53bce7…` |

The owner law that implements the completion is X2. Its revision r10, item 6c, is reviewed beside v3, and v3 does not rely on its bytes.

## What it changes

Four line overrides on REG. Each keeps its v2 line whole and appends one space and the text below. So each override's `after` equals its `before`, a space, then that text. `successor.json` holds the exact strings.

| # | REG line | What the appended text records | JRW |
|---|---|---|---|
| 1 | :9, scope | J-RW is the operation owner that authorizes ordinary, random-kind reservation completion, and what its authorization is. | :680; item 2 (:189-193); X-RW-1 (:696-698) |
| 2 | :60, marker publication | Completing a strict-prefix marker in place is the reservation's own interrupted step, not an overwrite. It is lawful only inside an authorized completion, with the complete namespace present. | :680; item 3.2 (:242-250); X-RW-2 (:699-701) |
| 3 | :74, explicit reservation recovery | J-RW is that independently authorized operation. It never runs in the crashed process, never as the constructor's fallback, and never on a read. | :680; item 2 (:174-176, :189-192) |
| 4 | :76, completion | Completion may find a strict-prefix marker and complete it in place, only with the complete namespace present. The ordering rule covers every present-marker form, not only the exact one. | :680; item 3.4 (:346-371); LD-13 (:781) |

### The appended text

1. **REG:9:** (v3, J-RW RW-S2) For ordinary, allocationKind=random reservation completion, that operation owner is law J-RW, M3's resume/repair writer (`docs/implementation/m3/resume-repair-jrw/PROPOSAL-r4.md`, item 2). Its authorization is the write gate's ordinary write admission for a durable request on the same root, whose recorded locator and incarnation agree with the row: the authorization class, on the same root, that created the reservation. It adds no CLI surface. Adoption, move, fork, retirement and abandonment keep their own owners, unchanged.
2. **REG:60:** (v3, J-RW RW-S2) Completing a marker in place is not an overwrite when its bytes are a strict prefix (the empty prefix included) of the RESERVED row's own marker frame. It is the reservation's own interrupted create-new step. It writes only the missing suffix at the existing length, rewrites no existing byte, and then makes the file and parent durable. It is lawful only inside an authorized reservation completion, with the complete namespace present (below).
3. **REG:74:** (v3, J-RW RW-S2) For an allocationKind=random row, J-RW is that independently authorized operation. Completion runs as its own classified step inside a later, separately admitted durable write, under the installation fence. It never runs in the process that crashed, never as the constructor's fallback, and never on a read.
4. **REG:76:** (v3, J-RW RW-S2) Ordinary reservation completion of an allocationKind=random row may also find a marker that is a strict prefix (the empty prefix included) of the row's own marker frame. It completes that marker in place, as the marker publication paragraph above states, and only when the reservation's complete initial namespace footprint is admitted present. The ordering rule above covers every present-marker form, not only the exact one: RESERVED plus a present marker of any form (exact, zero-length, a strict prefix, ACL-omitted or private) and an absent namespace is not a lawful crash prefix, and ordinary reservation completion refuses it before any effect. This changes no row of the observation table above, which classifies without writing.

## Lead decisions

Each is made under the owner's standing direction of 2026-09-30, and each names the alternative it rejects.
- **V3-1. The form is v2's.** v2 is a bound contract successor in the product's design lock (`design-lock.json`, `contractSuccessors`, at product main `d2c00a9`). So v3 is one too: a successor record with exact line overrides on its parent, a subject manifest (`project-registry-owner-selection-v3-subject.json`), and a design-unit review.
  - **Rejected:** a PROPOSAL-style revision that edits `owner.md` in place, because a selected candidate's bytes are never edited; and a full new copy of `owner.md`, which v2 needed for its carrier change, but which four appended passages do not need (the S21 form, `m3/host-pipeline-j/s21`).
- **V3-2. Append, never rewrite.** Each override keeps its v2 line whole and appends to it.
  - **Rejected:** rewriting REG:76's "RESERVED plus an exact marker and absent namespace is NOT its lawful crash prefix" to name every marker form. It would change accepted words, and the appended sentence states the wider rule.
- **V3-3. The observation table and the reference model stay as they are.**
  - **The table (REG:37-44).** A strict-prefix marker still reads as malformed evidence on every read (REG:44), as J-RW requires on every path but its own step (JRW:371).
  - **The model (REG:96, `reference/`).** Its ordinary durable-prefix table gains no row. J-RW's strict-prefix marker states are tested natively, by J4b's controls (JRW RW-C1, RW-C16), not by REG's labelled model.
  - **Rejected:** extending `registry_model.py` and its results. That reopens v2's frozen evidence, for a state whose labels the model cannot make real.
- **V3-4. This is the selection's v3, not a registry v3.** The carrier stays `I/project-registry.v2`, `schemaVersion` 2. REG:1, the title, is not overridden, so nothing reads as a new carrier.
  - **Rejected:** retitling REG as v3, which would read as a carrier or schema change.

## What does not change

Everything else in v2: the carrier and its schema; the physical placement; the reference model and its results; the observation table; allocation, adoption, move, abandonment and retirement; the S9 bridge; and every other line of `owner.md`. No public command, wire field, error code, schema, inventory or product change.

## Binding

- **Review.** v3 needs an independent design-unit review, `ACCEPT-DESIGN-UNIT` with its `subjectManifestSha256`, and the lead's root assent in `project-registry-owner-selection-v3-unit.json`.
- **Product.** Binding v3 into the product's `design-lock.json` is product work. It belongs to J-RW unit J4b, which RW-S2 gates (JRW:663, :680).

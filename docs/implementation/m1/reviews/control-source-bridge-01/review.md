# Independent review: common-control source-selection bridge

**Verdict: ACCEPT-DESIGN-UNIT** — required findings: none; 8 advisories.

- Reviewer: actual Claude (Opus 5, `claude-opus-5`), who authored none of the subject bytes.
- `subjectManifestSha256` (the v4 contract subject):
  `6d42ebf3734499c6432ee02269fde65ef6a2340c6d622db87b01c164a80e70b9`. This is
  `selection-subject.json`, 586 bytes, and contains exactly:
  - `docs/coop/completion/control-completion.schema.v3.json` `2929de62…` (22476 bytes)
  - `docs/implementation/m1/control-source-v1/successor.json` `1b34da5c…` (5341 bytes)
- `reviewClosureManifestSha256` (the full frozen 10-file closure):
  `cb17f5cc72ec511f42442e88292b4d335a07142ba768f5fda1bf49f8450567c1`. The exact set
  was verified before and after the review.

## Scope accepted

This unit selects the exact existing schema3 bytes as one v4 contract-successor
candidate, for generation-source provenance only. The path, the `$id`
`urn:opensip:design:control-schema:3` and the bytes stay unchanged. The parent is
`architecture-application.v1.json` (`15b3932a…`), and there are no passage
overrides. The only effect is one staged `contractSuccessors` append.

Nothing else follows from it: no change to semantics, framing, state, sequence,
correlation, authorization, effects or durable outcomes, and no M1, product,
platform or release qualification.

## Authority chain (independently verified)

1. **Base.** The live lock approvals pin source45 `8b4efbb0…` and application46
   `dab6e00f…`.
   - Source45 has exactly one row for the application path at `15b3932a…`/443974.
   - Application46 does not override it.
   - The record's `parents` and `baseApproval` equal the lock.
2. **Historical status versus actual later approval.** The application's own
   status says `WORKING-INTEGRATION-NOT-FROZEN-OR-ADOPTED`. That is its pre-adoption
   label. The later approval record shows it was actually adopted:
   - **D-369** (in `COORDINATOR-DECISIONS.md`, selected by application46) was adopted
     on 2026-09-05. It binds this exact SHA `15b3932a…` after whole-review v5
     ACCEPT 0/0 (`f35454e6…`) and v6 ACCEPT 0/0 (`260c8291…`).
   - D-371/D-372 keep the preview as a completed historical scope. D-372 says
     existing compatible constraints remain binding through source45.
   - The live register (application46) retains the design at **DR-102** "Retain
     byte-opaque common control framing" and **DR-125** "Retain common
     SDK/control/broker contract".
   - `control-protocol-contract.v2.json` (source45) owns framing, and schema3
     supplies the closed bodies. These owners complement each other, and no
     superseding body-schema owner exists.
3. **Selectors.** `/units/control` has standing `NO-OBJECTION-WITHIN-REPAIR-SCOPE`
   and pins review5 `dc31dd4d…` and freeze5 `0e4a020f…`.
   `/evidenceTargets/C.BODIES` has unit `control`, and `/sources/1` pins schema3
   `2929de62…`.
4. **Review5 and freeze5.**
   - Review5 has `mustFindings: []` and `subjectUnchanged: true`.
   - Its freeze digest, subject files and post-review hashes equal the eight files
     in freeze5.
   - The replay passed 484/484 and matches the frozen report digest.
   - All eight members are byte-verified and equal the record's `frozenMembers`.
5. **Substantive schema evidence.** Review5 is repair-scoped, so I traced the
   chain back:
   - schema3 has been byte-identical since freeze v2.
   - Review v3 was the bounded schema/framing/state review. Its only findings were
     checker-only: CCR-1 (MUST) and CCR-S1 (SHOULD).
   - Review v4 repaired those and raised CCR4-1, again checker-only.
   - Review v5 resolved CCR4-1.
   - No review found a schema3 defect. The pending security/journal and host joins
     are carried as limits.
6. **Generation join.** `control-generation-unit.v1.json` is `ACCEPTED-UNIT`, with
   `integrationApproved: false` and inert-carrier scope. Its first open obligation
   is exactly this promotion, with the strong preflight retained.

## Evidence reproduced

These ran with Python 3.14.6 and `-B`, TMPDIR under this review directory, from a
byte-verified copy of the closure.

- **`check_bridge.py`.** Exit 0, and the checker reports that 46 lock inputs verify.
  - The live preflight refuses with exactly `generation source is not selected by
    accepted design`.
  - With only the control row removed, 28 sources verify.
  - 140 declared reads; `acceptance` and `productQualification` are both false.
- **`--discover-inputs`.** It returns 140 pins, exactly equal to `inputs.json`.
- **`test_bridge.py -v`.** Ran 15 tests in 8.596s, OK.
- **Audit-hook probe (hidden or transitive reads).** 140 distinct architecture
  opens, with none undeclared or unused, and no subprocess or socket events.
- **Staged probes** on a mirror holding only the declared inputs:
  - Real mode refuses the synthetic marker, both at a synthetic path and at a
    neutral path.
  - An unmarked neutral-path probe passes. The refusal is a guard, not
    authentication.
  - The staged unit selects exactly `[schema3]`, and 29 sources verify. The record,
    subject and review5 are not selected as sources.
  - A review naming the 10-file SHA is refused ("contract review names a different
    manifest").
  - A double append is refused as path reuse.
  - Staged record byte drift is refused.
  - No accepted row reuses the schema path or its bytes.
  - Review5 drift after binding is refused by the bridge but not by the product
    verifier (see A4).
  - Binding order is not enforced (see A7).

## Advisories (non-blocking)

- **A1.** `successor.json` scope says "no … lock … change". The unit's single
  effect is a lock append, so read the phrase as no change to existing lock content
  and state that in the assent.
- **A2.** Cite D-369 and the DR-102/DR-125 retention as the actual adoption basis,
  not source45 membership alone. The whole-reviews are not source45 rows, and
  whole-review v5 never mentions control: `units.control` was adopted as a recorded
  standing.
- **A3.** The checker joins only review5, which is repair-scoped. Record in the
  assent that the substantive schema review is v3, and that the schema was
  unchanged through v4 and v5.
- **A4.** The v4 verifier does not bind the evidence fields. Retain this review,
  `check_bridge` and the snapshot evidence with the assent.
- **A5.** Bind only the actual retained review and substantive assent. Never place
  synthetic or probe documents in the architecture checkout.
- **A6.** source45/application46, the generation unit, the binding4 integration
  record and the route note are untracked (CA5 remains open). Keep them in custody.
- **A7.** Append after metadata-v2 exactly as staged; the verifier does not enforce
  order.
- **A8.** Non-qualification carries forward:
  - Rust `Control3Root` is looser than the schema (CA4) and is never admission.
  - `control_protocol.rs` is unwritten.
  - CA2, CA3, CA5, candidate02, native/report owners, output drift and the
    security/journal joins all remain open.

## Limits

- Pins were verified by hash in a dirty checkout, not by commit history.
- I did not reread the whole application, source45 or the D-372 corpus.
- I did not rerun the v5 484-case replay.
- Snapshot provenance rests on the pinned binding4 records.
- Probe fixtures existed only under TMPDIR and were deleted.
- Disclosure: the harness auto-backgrounded one read-only grep after a timeout. I
  terminated it unused. There were no agents, commits, pushes or writes outside
  this directory.
- This review is not root assent, a lock change, integration or qualification.

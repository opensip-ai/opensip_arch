# RESUMED INDEPENDENT DELTA REVIEW: interruption correction07 (m1-interruption-envelope-subject-07)

This continues review01/02/04/05/06; it is not a fresh session. Reviewer: actual Claude (claude-opus-5). No subagents, network, background tasks, commits, pushes or private-session inspection.

## Verdict
**Accept (narrow delta).** Review06 F1 and N1 are fixed, and the N2, N3 and N4 dispositions are accepted. There are no new findings, only three low observations.

**Acceptance scope.** Only the correction06→07 delta:
- the revised failure-paragraph override (1340–1349);
- the new availability-section override (1302–1338);
- the attempt prerequisite in `validate_availability_join`;
- the corrected rejected-attempt fixture and the two new unstarted refusals;
- the checker's prose assertions;
- the N4 rename.

This is design/reference standing only. Schema6 bytes are unchanged from correction06. The cancellation override, the model successor and the error/payload/optional-Run rules are unchanged and keep their earlier standing.

**Not included:** selection or promotion; envelope5 (still unaccepted); report07 or report features; generator, product or source rebases; M1 qualification; live signals or D9 delivery; host selection custody; and envelope capacity (L02).

## Custody
- Manifest `bcc63f22…a1a1` verified. Closure is **51/51 exact** on the original and my copy, before and after.
- **38/38 pins** match sources and copies, before and after; the set is identical to subject06.
- Delta from subject06 (7 files changed, none added or removed): `availability_probes.py`, `check.py`, `contract.md`, `ledger_join.py`, `passage-overrides.json`, `root-result.json`, `successor.json`. Schema6 is byte-identical.
- Evidence read, read-only:
  - `root-validation-07/initial-prose-wrap-check.stderr` shows the assertion failure on "at least one recorded attempt", consistent with the line-wrap explanation.
  - `m1-envelope-capacity-audit-01/result.json`: 995 notices × 4096-character roots is schema-admitted but canonical 4,231,826 B > 4,194,304 (BYTE_LIMIT).
- Execution:
  - Runs only from my copy: reference env `-I -B`.
  - Private pycache; own TMPDIR.
  - Verified bytes compiled directly. No pyc in either subject tree afterwards.
- Writes: only this directory.

**Root checker:** exit 0, and its output equals `root-result.json`:
- 42 shape;
- 59 narrow join;
- 43 metadata;
- 102 owner scenarios (9 changed, 12 wrong-kind refusals);
- **36** composite availability cases;
- 3 prose spans.

## What changed
- **Join:** a selected step must now also have `len(attempts) > 0`.
- **Failure prose (1340–1349):** "no findings or advisoryReport payload is carried. Invocation-scoped availability follows the release-availability rule above even without a committed Run." The old "Run-availability" ban is gone.
- **Availability section (1302–1338):** the original text is kept, with three paragraphs appended:
  - the composite entry points, which the narrower helpers alone do not satisfy;
  - retained selections, including ones from cancelled or rejected attempts, with **at least one recorded attempt**, never skipped, and the exact skipped termination with no detail;
  - completeness as a **host custody duty**, not inferred from a Run;
  - the presence law for builtins (parity), **profiles (explicit owner addition)**, other commands with selections, and preplanning (empty account only).
- **Checker:** asserts the old phrase is absent and the duty phrases are present after whitespace normalization; the N4 probe is renamed.

## Independent evidence
**`work/probes07.py`: 22 rows, all as designed.**
- **F1 prose.**
  - All three before-images equal the pinned owner lines, and the spans are disjoint.
  - After applying all three overrides to the pinned source, **no availability ban remains anywhere**.
  - Eleven duty phrases are present: both entry points; helpers insufficient; availability not tied to a Run; the attempt prerequisite; the exact skipped termination; custody completeness; the profile addition; the preplanning empty account; no non-empty preplanning account; findings/advisoryReport still banned.
- **N1 attempt binding.**
  - Refused: an owner-model unstarted cancelled step (`attempts: []`), a rejected step with no attempts, and an owner-model skipped step.
  - Accepted: a started-then-cancelled step (one cancelled attempt), and owner-model rejected, operationally failed and completed attempts.
  - An unstarted cancelled step still permits the parity empty account.
  - Selected-empty stays distinct from no selection.
  - `attempts: null` gives a typed refusal.
- **N2.** Omitting a completed analysis from the context is still admitted. This matches the published custody-only duty.
- **N4.** The renamed case is present. `{}` is shape-refused, and the native empty account is shape-valid on the empty form.
- **L02 sanity.** One step × 995 notices × 4096-character roots: the join accepts and the shape is admitted, but the pinned canonical codec refuses it (BYTE_LIMIT). Capacity is outside this join, as root states.

**Regression (`work/probes06_regression.py`, a byte-identical copy of review06's probes):** of 34 rows, **exactly B1 and B3 flip to refused**, as N1 requires. The other 32 are unchanged:
- the schema delta;
- the 20 owner ledgers;
- the presence law;
- all 45 preplanning commands;
- bounds and correlation;
- errors and skips.

## Previous findings
| | Disposition |
|---|---|
| F1 | **Fixed.** The selected prose no longer bans availability and publishes the complete availability duties in the owner section. |
| N1 | **Fixed.** Unstarted selections are refused; lawful started, rejected, failed and completed selections are kept. |
| N2 | **Accepted** as an explicit host completeness duty. |
| N3 | **Accepted** as an explicit profile owner addition. |
| N4 | **Fixed.** |

## Observations (low, non-blocking)
- **O1.** The retained section says "an omission is a required-delivery operational fault". For an interrupted invocation, the prose doesn't say whether delivery stays 130 or becomes 4. This predates the delta; resolve it with L02.
- **O2.** L02 appears in the subject only as a generic codec sentence (`contract.md:43`), and `successor.json` duties don't name it. At selection, record L02 in the integration register, covering the capacity/admission or delivery owner decision, no silent truncation, and precedence against interrupted/130 given the existing `OUTPUT.SERIALIZATION_FAILED` overflow law. It is correctly not absorbed here.
- **O3.** The checker verifies after-text only by phrase presence. Pinning the selected after-text sha256 at re-freeze would prevent silent drift. I independently verified disjointness, full application and eleven phrases.

## Limits
- Selection contexts, undeclared rows and repair/verify results are synthetic. No native selection execution, RequestContext custody or retention is proven.
- The started-then-cancelled attempt is a host-recorded shape that the owner model itself never emits.
- Capacity and full native/parameter/Run admission are unproven.

## Remaining duties
- Select an accepted parent. Apply together: schema6, all three prose overrides, model line 380, the error/payload/availability joins and the composite entry points.
- L02 capacity qualification and owner decision, including precedence (O1/O2).
- Rebase report07 onto correction07, and bind the output kind per command.
- Host: immutable per-step selection retention, a complete selection context, and always using the composite entry points.
- Bind metadata/CLI/generated sources and inventory/registry/closure to the selected major.

## Not claimed
- Selection, promotion or product/source adoption.
- Report, report-feature, generator or M1 qualification.
- Live signals, D9 delivery or browser rendering.
- Capacity, native selection or Run admission completeness.

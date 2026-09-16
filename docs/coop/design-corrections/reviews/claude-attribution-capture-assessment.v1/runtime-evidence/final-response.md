**Disposition: CORRECTION_REQUIRED, with one wording clarification bundled in.** Frozen41 matched its manifest before and after (12912 members, 0 missing, mismatched or extra). All writes went to the new runtime, and every subprocess has finished.

## 1. Capture: does the builder discard a returned view no cell owns?
Yes. On frozen41, a view declared returned in `graph['viewIds']` (with or without an evaluation ref) that no cell owns is left off the receipt and off `selectedRefs`. The builder's manifest still admits, but the same graph's Run fails `EVALUATION_VIEW_ROOTS`.

**Census versus explicit ids.**
- **Store census:** a view present only in the store (`objects`) is correctly ignored, and the manifest digest is unchanged.
- **Explicit ids:** `viewIds`/`viewId` and evaluation-ref views are builder inputs (§8), and the builder already merges them for attribution. It then captures only the attributed subset (`execution_inputs_fixture.v3.py:341`).

§8's "selectedRefs = attributed views" row describes that behaviour accurately, so this isn't an implementation slip. The row itself contradicts published law:
- §1 says capture is an observation of stage returns, with exact totality.
- The new §3 text says a captured view attributed to no row stays lawful and stays on `selectedRefs`.
- §7 names `attach_host_capture` as the host adapter's capture step (`:263`, `:280`).
- The graph fixture's own comment treats the drop as a hazard to design around (`evaluator_graph_fixture.v3.py:293-296`).

The mechanism for building capture from the same stage returns is specified in §1 and §3, but the builder doesn't implement it faithfully.

**Second gap, in the model.** A host manifest whose `selectedRefs` and row name a view that is on no complete receipt admits and closes a Run on that exact manifest. That contradicts §1's rule that stage-produced refs equal the union of complete receipts. It is one internally inconsistent manifest, not two differing observations.

## 2. Two cells sharing a view on the same program and universe
File-fixture symbol worlds can't close a Run even unmodified. With the checker's `"x"` id they fail `DeclaresPayloadV1`; with a lawful `symbol:x` they fail `POLICY_RULE_NOT_ADMISSIBLE`. I preserved both failures and didn't correct that helper. The maintained semantic `declares` fixture is a lawful alternative: inventory and syntax cells on one binding.

On that world, current law already decides the cases:
- a view carrying file and declares partitions appears on both rows and closes on the exact builder manifest;
- omitting it from one row refuses `VIEW_TOTALITY`;
- naming the view that matches neither cell on a row refuses the same way.

On frozen41, the builder drops the view matching neither cell, so that Run can't close. A host capturing it exactly closes it. The maintained suite simply had no such control.

## 3. Matrix wording and schema
- **Wording:** §3's `S.relation ∈ …/relations` can never match literally, because entries are `[relation, resolution]` pairs. The two readings behave differently: a references scope at `syntactic-name-match` is attributed and closes under the model's relation-column reading, while the pair-reading encoding refuses. The patch pins the text to relation-column membership, with no behaviour change.
- **Schema:** no change needed. Its `viewDigests` description matches the corrected §3, and the contract paragraph names the field. Adding a selector would change registered bytes and force a repin for a cosmetic gain.

## Proposed delta (not applied anywhere)
- **Builder:** capture the explicit returned views on the view stage matching each view's producer.
- **Model:** stage-produced views must be exactly the complete-receipt views, otherwise the existing `SELECTED_COVER` refusal.
- **Contract:** §3 candidate-set and relation-column wording, plus a corrected §8 builder row.
- **Checker:** 9 cases, 6 of which close real Runs, including the two-cell semantic control and the rung control.

The patch is `correction.patch` (sha256 `92aa515f…`); base and after hashes for the four files are in `delta-manifest.json`. Only the owning checker was run:

| Run | Cases | Mismatches |
|---|---|---|
| Unpatched copy | 86 | 0 |
| Patched copy | 95 | 0 |
| Patched checker only, on unpatched model and builder | 95 | 4, exactly the capture defects |

The 86 shared cases are field-identical between base and patched, with identical Run ids. Manifest digests are also identical for all 18 maintained graph constructors swept.

## Consequences and limits
- **Changed behaviour:**
  - graphs that declare a returned view no cell owns now capture it and their Runs close;
  - host manifests naming a selected view absent from every receipt now refuse `SELECTED_COVER`;
  - a view named only in `evaluationInputRefs` but missing from the graph's `viewIds` is now captured, and that inconsistent graph fails `EVALUATION_VIEW_ROOTS`. No maintained graph has one. Restricting capture to `viewIds` alone would avoid this; that's your call.
- **Not run:** the other `attach_host_capture` callers, pins, reports or the full suite.
- **Standing:** admission results show reference self-consistency; closed-Run results use reference drivers.
- **Preserved failures:** the symbol-world baselines, my extra file-partition probe (A5, which failed a Coverage totality rule of its own construction), and the frozen41 closure failures that evidence the defect.

Files are in `/private/tmp/opensip-design-corrections/claude-attribution-capture-assessment.v1`:
- review.md
- review.json
- correction.patch
- delta-manifest.json
- hash-index.json
- receipts/
- tools/

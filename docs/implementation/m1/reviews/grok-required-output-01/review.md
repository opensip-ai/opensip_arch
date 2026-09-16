# Independent Grok review: required-output01 original unit

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-required-output-subject-01`
**Manifest SHA-256:** `a79c086020daf34e7fa106ef9489c4ca3691fc8dc0244b0454dbd0ed0aee1f3e`
**Members:** 43
**Verdict:** **ACCEPT WITHIN STATED REFERENCE SCOPE**

This is the original 43-file L02 proposal. Combined joint10 acceptance does **not** waive it. Later root selection of complete-output-or-operational-failure does **not** complete the D9/source bridge or product implementation. No accepted D9/source byte in this freeze was changed.

## Policy (not undecided)

**Selected product policy** (later owner decision in `m1-report-joint-candidate-12/L02-policy-selection.json`, pinning Grok joint10 review `21d885a5…9d45`): complete required envelope or explicit operational failure. Useful work may already be committed. Capacity/serialization/write/flush failure is existing `OUTPUT.SERIALIZATION_FAILED` / operational-failed / exit 4. No truncation, substitution, or invented atomic stdout.

**Original stronger criterion** from envelope-capacity-01 / RP-OBL-L02 — preflight rejection before retained selection, or a complete bounded output profile preserving required parity — is **not met**. It was **explicitly superseded, not passed**. Historical `issue.json` and `originalClosureCriterion` remain.

This 43-file freeze is that selected policy’s original proposal. It honestly does not claim the stronger law. Large lawful invocations can fail output after committing useful work; that is explicit product behavior under the selected policy, not a silent waiver of the old criterion.

Representability is **not** required to be reserved before selection/commit under the selected policy. Exact D9/source binding and product codec/stream/file/signal integration remain.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not executed against and not written. No modes or symlinks listed.

| Check | Result |
| --- | --- |
| Manifest | `a79c0860…1f3e` matches declared and adjacent copy |
| Files | 43 listed = 43 walk |
| Pins | **29/29** (path and `owner/` copy) |
| After | frozen hash unchanged |

## Documented checker and controls

Private copy, reference Python `-I -B`:

- `check.py`: **13/13** groups, 29 pins, D9 v1.14 full authority OK
- `mutants.py`: **9/9** killed (capacity disabled / off-by-one, interrupted-overrides-output-fault, flush omitted, partial write treated complete, termination/exit joins, second delivery, diagnostic on normal stream)

## Independent probes (17/17)

Not only author tests.

| Probe | Result |
| --- | --- |
| D9 fault derived from v1.14 `derive_class`/`derive_codes` on `machine-output-serialization-failed` | `operational-failed` / `OUTPUT.SERIALIZATION_FAILED`; axes `interruption=none`, `faultCause=output-serialization`; `preservesSettledRun` |
| v1.14 `invariant-envelope-parity` | still the old success-only sentence; this freeze does not edit accepted v1.14 |
| Later proposed v1.15 clarification | exists in joint-candidate-12, **not** in this 43-file freeze |
| Interrupted aggregate + successful write | exit **130**, Run id kept in envelope |
| Interrupted + capacity fail | exit **4**, no stdout, fixed diagnostic, no token leak |
| Required renderer `DELIVERY.REQUIRED_FAILED` | preserved on successful write of that failure envelope; later flush fail becomes `OUTPUT.SERIALIZATION_FAILED` |
| Stream prefix / full-write-then-flush | prefix or complete bytes may be visible; no second envelope; process still exit 4 |
| Byte preflight | exact 4 MiB stand-in completes; 4 MiB+1 never writes |
| One commit | after-commit events cannot reclassify; second `deliver` refused |
| Unknown `RuntimeError` | not mapped to serialization-failed |

Diagnostic is exactly `opensip: OUTPUT.SERIALIZATION_FAILED\n`. Writer OSError text containing `/secret/path` never appears. interruption07’s “Failure to record or deliver keeps its own existing operational fault law” is preserved: successful interruption delivery is 130; later output failure owns 4.

## D9 / source binding

This unit proposes an explicit successor clarification of `invariant-envelope-parity` and does **not** apply it. Checker imports unchanged 27-file D9 v1.14 closure and derives the output fault from real class/code functions. No new D9 class, map entry, or public detail.

Joint10 later composed `d9-exit-contract.proposed.v1.15.json` carries the clarification prose. Root selected that policy with `sourcePromoted: false`. That later composition is not this freeze and does not close RP-OBL-L02 integration.

## Must-fix / should-fix

None in the stated reference scope.

The reference still length-checks trusted encoder output after the callback returns. Contract already says an unbounded allocate-then-measure is not a product implementation. Not a silent codec claim.

## Remaining duties

Bind the selected policy through an exact reviewed D9/source successor (v1.15 remains unpromoted). Product bounded encoder (resource bounds during encoding), private RequestContext/aggregate, live signal arbitration before the single commit, pipe prefix/flush failures, file staging/fsync/rename, and consumers requiring successful delivery termination plus an admitted complete document. L01 retained InvocationRecord capacity is a different open obligation. No full oversized Run, live filesystem, or signal qualification is claimed here.

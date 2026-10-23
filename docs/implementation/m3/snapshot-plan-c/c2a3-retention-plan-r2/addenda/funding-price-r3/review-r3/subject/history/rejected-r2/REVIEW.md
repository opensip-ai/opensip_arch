# Review verdict: REQUIRED-FINDINGS

The frozen `subject.json` rehashes to `34a5fd28c6c495a15ad72e784239dff3e5dc5f7751c7ed039ff3dc3cd580d0c4`, and all 53 declared ordinary files match their recorded sizes and SHA-256 values.

R2 makes the R1 correction substantive: it defines a finite, one-time instrumentation bootstrap rather than claiming that a later debit can fund its own prefix. I found no scoped owning-law prohibition against proposing that exact bootstrap as a new policy boundary. The revised tree arithmetic also reconciles to 768 fixed visits and 163 visits per Blob, selecting fixed 1024 and scan 256F. One source boundary remains uncovered.

## Required finding

### C2A3-FUND-R2-RF-1 — High — the bootstrap and ledger both stop before the actual caller's question-mark propagation

**Locations:** `MODEL.md:9-11`; `ERROR-PREFIX.md:3,9,11`; `LEDGER.json:52-57,94`; `proposed-component_admission.rs:345` (identical current source at that line)

The declared bootstrap covers `fund_representation` entry, the first `work.charge(...)?`, and the function's immediate return when that charge refuses. The real source then evaluates a second question mark at:

```rust
let count = fund_representation(candidate, scope)?;
```

That caller-side `?` is outside the stated bootstrap. On a successful `fund_representation` return it executes the same successful `Try::branch`/caller match/extract sequence that the model prices as `try_success` (7 visits), but `LEDGER.json` includes only one visit for the function's non-bootstrap return transport. The reported fixed total of 768 therefore omits this successful source path.

On an initial debit refusal, `fund_representation` returns the typed error inside the proposed bootstrap, but line 345 must then perform another failed `Try::branch`, residual extraction, `FromResidual`/identity propagation, and return from `admit_component_inner`. This occurs after the bootstrap's stated refusal endpoint and before any M debit has succeeded. The post-bootstrap 128-visit reserve is unavailable on that path. Thus `ERROR-PREFIX.md`'s claim that no application-M work follows the initial refusal is not established by the defined boundary.

Correct the exact source model in both directions:

- add the line-345 successful caller question-mark path to `CALL-TREE.json` and the paid fixed ledger; and
- either extend the explicitly proposed bootstrap through line 345's failed question-mark propagation (and state its precise refusal endpoint), or prove a previously paid enclosing allowance covers that propagation.

Then reconcile `MODEL.md`, `ERROR-PREFIX.md`, `ERROR-CALL-TREE.json`, `LEDGER.json`, the derived totals, and the frozen controls. Counting the missing successful `try_success` path would raise the demonstrated fixed candidate from 768 to at least 775, so the selected power-of-two fixed fee may remain 1024; that numerical slack does not cure the unfunded initial-refusal path without an explicit boundary correction.

## Evidence assessment

Apart from this finding, the frozen evidence supports the claimed source relationship: the proposal changes exactly the three pricing literals; the 32 fixed and 5 per-Blob helper counts reconcile; candidate order remains a private permutation of the Blob vector; the LP64 conversion premise and final `None` path are represented; and the post-bootstrap error tree's 52-visit maximum fits its 128-visit reserve. I inspected but did not execute the supplied checker or report, as required.

This verdict is limited to the funding-price addendum. It does not adopt the global M model, establish the complete M bound, authorize native execution, accept an implementation unit, or qualify the product. The separately owed map, local-52F, drop, slot, ABI, runtime-debit, census, fit, and complete source/operand work remain outside this review and are not additional findings.

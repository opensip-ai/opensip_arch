# Review verdict: REQUIRED-FINDINGS

The frozen subject manifest rehashes to `713a50c3e383bf05a3f87b5ca85d9a254587877858bd5ebc91f93de3fbe8cb94`, and all 42 declared ordinary files match their recorded sizes and SHA-256 values.

## Required finding

### C2A3-FUND-R1-RF-1 — High — the first fixed debit does not prepay its own caller-side work or refusal path

**Locations:** `MODEL.md:9`; `ERROR-PREFIX.md:3,7,9`; `LEDGER.json:28-45,60-61`; `product/crates/lifecycle/src/component_admission.rs:212`; `proposed-component_admission.rs:212`

The proposed source constructs the first `WorkCost` value and evaluates the call before `work.charge(...)` can successfully debit the proposed fixed 1024 units. If that initial charge refuses, the immediate caller-side `?` propagation also executes without any paid fixed block or error reserve. The ledger nevertheless includes all three `WorkCost` record writes and their constant operations in the fixed allowance, and its `meter_call` model includes caller transport and successful `Try` handling. `MODEL.md` excludes the `WorkScope::charge` and `WorkLedger` implementation bodies as trusted metering machinery, but expressly says the caller tuple and caller question-mark are counted. Consequently, the work performed to attempt the first debit lies outside the stated mechanism exclusion while occurring before the allowance intended to fund it.

Increasing the fixed price does not repair this temporal gap. Correct the model and evidence in one of these ways:

- extend the explicitly reviewed trusted-metering boundary to the caller-side construction, argument evaluation, invocation transport, and immediate refusal propagation for the initial debit; distinguish that first call from the later two calls and remove its excluded nodes from the funded ledger; or
- identify a previously funded enclosing allowance that is already available before `fund_representation` begins and prove that it covers the first `WorkCost` construction, call transport, and refusal propagation.

Whichever boundary is selected must be reflected consistently in `MODEL.md`, `ERROR-PREFIX.md`, `CALL-TREE.json`, `LEDGER.json`, the price formulas, and the frozen controls. A later successful fixed debit cannot retroactively fund this prefix.

## Evidence assessment

Apart from the finding, the proposed values reconcile with the supplied model: the expanded ledger totals 781 fixed units and 163 units per blob, the selected powers of two are 1024 and 256, the three proposed source changes are exactly the three pricing-literal replacements, and the formulas and 32 fixed/5 per-blob helper-site counts are internally consistent. I inspected the supplied checker and report but did not execute them, as required.

This verdict covers only the funding-price addendum. It does not adopt the global M model, establish the complete M bound, authorize native execution, accept an implementation unit, or qualify the product. The separately identified map, local-52F, drop, slot, operand, ABI, runtime-debit, census, and fit obligations remain outside this review and are not additional findings here.

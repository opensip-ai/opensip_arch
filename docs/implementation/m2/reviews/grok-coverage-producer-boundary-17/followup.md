# Follow-up: carrier-name split (advisory 17 finding 1)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Reassessment of finding 1 only. Original `advisory.md` / `advisory.json` bytes **unchanged**.
**Original pins:** `advisory.md` 14107 / `30ea10dc0f3708ce0ba975072d31f595e1f018f50a752562bf29e7e7ba209ac4`; `advisory.json` 3439 / `236f88e236a15ce275891af813a78a0f3542e350610137c337a5e5b2b557f758`.

## Disposition

**Finding 1 is not a selected-function contradiction.** It is an **intentional layer split**: internal validation causes versus host operational DomainDetail / D9 routing. **No bounded selection correction** is required for the producer owner to keep `refusals[]` / `faults[]` as selected `admit_coverage_result_v3` emits them, or for identity to wrap producer REFUSE as `COVERAGE_PRODUCER_ADMISSION:` (1936).

What remains is a **future host presentation mapping** (section 10 / D9), not an internal exception-string identity.

## Controlling text

**Producer docstring (native 1549–1553).** Refusals of this boundary **are** the public class, not a demand that each internal string equal a DomainDetailCode:

> Refusals are `PROVIDER.PROTOCOL_VIOLATION` (operational-failed 4, section 10 fault law): a faulting or lying worker mints no coverage2 and no Run.

That matches `stage_authority` (3711–3723): protocol violation → no facts, no Coverage, no Run; diagnostics **operational-record-only**; D9 `{class: operational-failed, exitCode: 4, code: PROVIDER.PROTOCOL_VIOLATION}`.

**D9_MAP 3612** (keyed by **public DETAIL code**, comment 3596–3598 / 3634 — not by exception string):

```
"native.coverage-bijection-mismatch": {
  "class": "operational-failed", "exitCode": 4,
  "code": "PROVIDER.PROTOCOL_VIOLATION",
  "typedDetailCarrier": "operational record"
}
```

Contrast admitted incomplete Coverage (3601–3606): `typedDetailCarrier` is the **coverage2** deficiency/nativeCause. Bijection disagreement is **not** that carrier.

**Native-evidence §4.3 RC-6 (2171–2177), the sentence the original finding over-read:**

> It is enforced by `coverage_bijection` at **both** boundaries — the producer boundary (`admit_coverage_result_v3`) and retained Run closure, which re-runs that same admission — so a contradictory entry can neither be minted nor carried into a sealed Run. A disagreement is `PROVIDER.PROTOCOL_VIOLATION` on the existing `native.coverage-bijection-mismatch` carrier: **no new internal key** and **no new public detail code**.

“No new internal key” forbids adding an internal refusal equal to the DomainDetail member. “Carrier” here is the **existing public/D9 detail**, not `AdmissionError('native.coverage-bijection-mismatch')`.

**Section 10 table (3529, 3538, 3541):**

| Condition | D9 | Code | Typed detail carrier |
| --- | --- | --- | --- |
| coverage bijection faults (RC-0/1/2), **and** subject-scope/key/examined mismatches, **and** `coverage_view_use` keys, **and** worker fault (3529) | operational-failed (4) | `PROVIDER.PROTOCOL_VIOLATION` | operational record |
| contradictory completeness RC-6 (3538) | same | same | operational record, **on the existing `native.coverage-bijection-mismatch` carrier; no new key** |
| producer cause/carrier refusals `native.coverage-cause-*` (3541) | same | same | operational record |

**How internal keys reach the public surface (3546–3558).** The carrier is `StepTermination` (`class` + `errorCode`/`faultCause`; `domainDetail` **optional**). Prose “operational record” is **not** itself a DomainDetailCode (3550–3551). Where a closed DomainDetailCode names the condition it is carried; otherwise `domainDetail` is absent and **the internal decision key is retained in the operational diagnostic record**.

Public-route registry (native schema `x-opensip-public-route-registry`, coop extract 400–503): `native.coverage-cause-*` keys route to `PROVIDER.PROTOCOL_VIOLATION` with `domainDetail: null` and `envelopeDetail: native.coverage-cause-unsupported`; `operationalCarrier` = internal key in the operational record. `public_termination_for` (1053–1067): **guards emit only the internal key**; an earlier revision wrongly published “operational record” as if it were a public detail code.

Live `common-v4` DomainDetailCode enum **does** include `native.coverage-bijection-mismatch` (618). Live native-v2 public-route `keys` object does **not** register `RC-6:` / `RC-2:` strings as internal keys.

## What each string is

| String | Layer |
| --- | --- |
| `RC-0` / `RC-6` / `RC-1` / `RC-2: …` | bijection **faults[]** (internal validation cause) |
| `native.coverage-key-scope-mismatch:…`, `native.subject-scope-commitment-mismatch`, `native.coverage-cause-*`, … | producer **refusals[]** (internal keys; cause-* have public-route rows) |
| `COVERAGE_PRODUCER_ADMISSION:` + joined lists (identity 1936) | identity wrap of producer REFUSE (same pattern as `NATIVE_CONTEXT_ADMISSION`) |
| `PROVIDER.PROTOCOL_VIOLATION` + exit 4 | host D9 **errorCode/class** for that REFUSE class |
| `native.coverage-bijection-mismatch` | host **DomainDetailCode** / D9_MAP detail for bijection/RC-6 presentation; typedDetailCarrier **operational record** |

Prose does **not** require the identity exception or `faults[].fault` to equal `native.coverage-bijection-mismatch`.

## Missing binding?

**Not a missing producer/identity binding.** Selected admit already splits `refusals` vs `faults`; identity already re-runs admit and refuses `COVERAGE_PRODUCER_ADMISSION`.

**Host mapping (not this producer unit):** map `result==REFUSE` from `admit_coverage_result_v3` (any refusals or bijection faults) onto section 10 operational-failed 4 / `PROVIDER.PROTOCOL_VIOLATION`, with DomainDetail `native.coverage-bijection-mismatch` where the condition is bijection/RC-6 (3538), and with public-route `envelopeDetail` `native.coverage-cause-unsupported` where the internal key is `native.coverage-cause-*` (3541 / registry 400–503). Do **not** pass raw `RC-*` strings to `public_termination_for` (those are not registered internal keys; 1048 would raise `native.public-route-key-unregistered`).

That mapping is owed by the **D9/exit-contract / host presentation** surface when Coverage producer REFUSE is shown as a StepTermination. It is not owed by changing selected admit/identity strings.

## Original finding 1

Withdrawn as a **specification contradiction / required bounded selection correction**. Retained only as a **trap**: do not equate internal exception text with the DomainDetail code; do not treat `native.coverage-bijection-mismatch` as a new internal refusal key (2176–2177 forbids that).

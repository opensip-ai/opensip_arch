Bounded correction complete. Summary:

## Frozen source33 verified
Manifest SHA matches `1cf3db70…`; all **12 899 files / 736 764 309 bytes** re-hashed — 0 mismatched, 0 missing, 0 extra.

## Diagnosis — one field, one stale helper rule
The TS positive and both positive binding controls refused with `EVALUATOR_COMPLETE_PROOF_REPLAY`. Exactly **one proof field differed: `executionDeficiencies`**. A Coverage record that retains `(complete, null, null)` had been given its *sibling's* `language-tier-unsupported` while keeping its own null `nativeCause` — an unzipped, re-paired carrier — where source33 derives `required-cell-unsatisfied`.

Cause: the bundled `author-helpers/evaluator.py` kept the pre-source33 rule
`fallback = records[0].deficiency or "provider-unavailable"` / `e["deficiency"] or fallback`.

**This is not a source defect.** Frozen source33 refused correctly under its published no-invention and exact-per-record-pair law. I changed **no frozen byte** and adjusted no fixture to make an old artifact pass — only the helper, to `(hx, e["deficiency"], e["nativeCause"])` with `(None, None, None)` when a record carries none.

## Reconstruction
- **Reminted on source33**: checkpoint3, binding-controls, semantic-controls1 — new proofs, new retained bytes, owner-derived proof equals retained, `compare_complete_replay` ADMIT.
- **Reused exact source30 bytes**, re-verified against frozen33 in the same pass: normalized-examples6, rust-selection-examples1.
- **Byte-identical reproduction**: `author-properties.json`, `mixed-universe-view.probe.json`.
- `collapsed-deficiencies` keeps its run id while its store bytes differ — both recorded.

## A second defect this exposed
In v9 the semantic negative group reported *pass* with **no discriminating power**: the base proof was itself stale, so all three refused regardless of their mutation. Measured both ways — v9 base REFUSE (not attributable), v10 base ADMIT (each refusal isolates its own tamper).

## Verifier reporting
`verify-package.py` asserted mid-flight, which is why root got no `verification.json`. It now **records** group crashes and query failures and always writes the report before exiting non-zero. **No expectation weakened** — every admission/refusal clause, the `ENUMERATION_BINDING_PROGRAM_ENTRY` and `EVALUATOR_COMPLETE_PROOF_REPLAY` conditions, the 7-check query rule and the final assert are unchanged. Demonstrated with a disposable broken copy: exit 1, report written, `passed: false`, failure recorded.

## Fresh verification on final bytes
Exit **0**, `passed: true`, 12 899 source files, 305 package files, **13 Run/control cases + 7 queries**. The required negative still refuses *first* at `ENUMERATION_BINDING_PROGRAM_ENTRY`.

Package manifest `88c38b16…` (305 files, does not list itself). v9 untouched (`55066ece…`, matches `MF55066ece…`), 0 files removed, all historical directories and the 30 PENDING residuals byte-identical, superseded bytes preserved under `historical-source33-before-remint/`.

**No independent assent is claimed.** The remint changed which deficiency is cited, not the verdict; the TS helper remains partial; source33 acceptance, whole-design review and blind acceptance remain outstanding.

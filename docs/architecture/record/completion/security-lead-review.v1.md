# LEAD-CORRECTION-REVIEW 1 — OBJECT

**2 MUST-FIX, 1 SHOULD-FIX.** The security unit remains CONTESTED.

Reviewer: Codex `/root/security_lead_review`, a fresh independent reviewer who authored none of the 72 subject files. Subject: `security-freeze.v6.json`, SHA-256 `3ecd4ad53eaeb875b3e0f43f76ac8d60614f14d6e1860b988d47b8a9e5a05370`. Dispatch: `security-lead-review-dispatch.v1.md`, SHA-256 `784612ebd419c0478c28107c0a96b9fb096815cae2eb890b1e158f0a25be1f40`. All subject, authority and direct dependency pins matched before and after review; frozen bytes and report were preserved. No commit or register edit was made.

Cumulative history: **three ordinary exchanges, one UPHOLD, two FAILED bounded confirmations (v4/v5), and LEAD-CORRECTION-REVIEW 1 OBJECT**. This is not another bounded confirmation and not a reset. The pinned lead-correction v2 decision, Claude procedural CONSENT and recorded addendum authorize independent review; they confer no technical acceptance.

## Remaining findings

1. **SEC6-LR1-M1 — MUST: floating envelope version verifies.** Change only `envelopeSchema: 2` to `2.0` in the retained valid manifest envelope. `verify_envelope` returns `VERIFIED`, `valid=2 threshold=2`, while canonicalizing that envelope raises `FLOAT_FORBIDDEN`. The schema's numeric const equality and the omission of envelopeSchema from the canonicalized signed-subject projection leave the complete admission boundary open to a forbidden scalar. Validate the full envelope's canonical data model and strict version inside the boundary; preserve integer-version success and routing/refusal precedence. See `security_unit_lib_v6.py:355`, `:439`, and inherited canonical rules in `security-completion.v2.md:124`.

2. **SEC6-LR1-M2 — MUST: project policy creates a state class absent globally.** Global grants for the broker and host-state-write tokens have `scope: {}`; project grants for the same pairs add `stateClass: SC-OPS`. Both policies validate, but `merge_policy` returns SC-OPS grants with no refusal. Projecting those scopes into the retained HE1 context admits SC-OPS, whereas the global scopes refuse. The `stateClass` branch compares equality only when both values are present (`security_unit_lib_v6.py:1221`), violating §6.11's project-only-narrows rule. Require a globally present equal class before the project may name it. Preserve same-class, omission/inheritance, absence, deny, traversal and N1 controls. This is a design-model authority counterexample, not a production exploit claim.

3. **SEC6-LR1-S1 — SHOULD: exact context names disagree.** §7.5 documents `scratchDirStat`/`fileStat`; the enforcing API requires `scratchDirSt`/`fileSt`. Supplying the documented names with otherwise valid context returns `RESULT.CONTEXT_ABSENT`; the fixture names return the expected bytes. Align the normative paragraph and API/consumer names and retain a documented-shape positive control. A prose correction suffices if current API names remain authoritative.

## Evidence and repair disposition

The frozen checker replay passed **751 checks, 0 failures**, identical to its frozen report except `ranAt`. Independent probes ran **121 checks: 117 expected results and 4 counterexamples**, grouped into the findings above. The JSON verdict embeds exact runnable source and every result. Eight additional policy observations independently reproduce Claude's disclosed advisory leads: malformed strings/unknown members can pass the pure merge, and malformed types can raise. Their shaped-input precondition limits the claim; they are not separately counted. A complete source-policy admission wrapper is the preferred systemic repair, while the schema-valid stateClass widening independently establishes the MUST finding.

Original SEC3-M1 root/wrapper/canonical-exception, M3 witness, M4 context/scope/result, and M5 journal-order/recovery counterexamples now resolve. RA without intent lawfully yields REV `process-death`, then CLN `not-begun`; it never fabricates an outcome without intent. Original M2 traversal and M6 measured Linux identity dispositions, policy duplicate N1 and the separate HE1/HE2 caps remain tested and preserved. New envelope and stateClass findings are separately counted, not rewrites of earlier verdicts.

Replay report SHA-256: `955aaea60efe7ee71d7e7c82c38e2309a0016663aa37697afcc772abbab1f0bf`. Independent probe report SHA-256: `418325ebe9902922528f67558366d2efecb969cd87ecf4f4fbc0f2cd0586bc97`. Full subject/authority/dependency pins, sources, controls, results and prior-finding dispositions are retained in `security-lead-review.v1.json`.

This is design evidence only: no native platform qualification, implementation authorization, unit adoption or satisfied readiness row follows. **Report this failed lead review to the user before any further repair round**, preserve the frozen v6 subject and cumulative history, and submit any repair as a numbered digest-pinned successor for independent review.

# Independent Grok review: config-disclosure02 original unit

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-config-disclosure-subject-02`
**Manifest SHA-256:** `bb48c14e0b8c4195c7f81af694b897dc3badd1b84626a40ec478426155a12fa5`
**Members:** 11
**Verdict:** **ACCEPT WITHIN STATED REFERENCE SCOPE**

Root correction02 for CFG-F1–F4 (RP-DO-04). Synthetic Plan shape checks. Not Run custody, report-carrier integration, HTML leakage, or product selection. Later joint13 composition of this schema is **not** a waiver.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not executed against and not written. Product/architecture/historical bytes untouched. No modes or symlinks listed.

| Check | Result |
| --- | --- |
| Manifest | `bb48c14e…2fa5` matches declared and adjacent copy |
| Files | 11 listed = 11 walk |
| Pins | **8/8** |
| After | frozen hash unchanged |

## CFG-F1–F4 (presentation review01 → this freeze)

Independently reproduced (**14/14**), not only author tests.

| Id | This freeze |
| --- | --- |
| **F1** | `admitted_plan` is validated as identity `#/$defs/plan`. PlanId must equal `plan2:` + canonical H(`plan`, plan), which matches `identity-model.identifier('plan', …)`. A caller `plan2:aaa…` is `CONFIG-DISCLOSURE.PLAN-ID`. Incomplete Plan dicts refuse. Historical **subject01** still emits the caller PlanId for the same dict (original defect preserved, not this freeze). |
| **F2** | Closed provenance: document checks public types and complete 13 slots; host-asserted covers digest/PlanId/Run association, policy, and public-value equality. Digest equality is **not** `verifiedInDocument`. Extra provenance members refuse. |
| **F3** | `components.request` `itemCount.minimum` is **1**, copied from owner `minItems`. Present empty request cannot be a lawful configuration; `itemCount` 0 on a present request refuses. |
| **F4** | `unavailable_source` maps missing/purged/expired → unavailable; corrupt/digest/plan-id/budget/shape → corrupt/`retained-bytes-corrupt`; unsupported schema → incompatible. All validate pinned report07 `PanelNotPresentV1` with no `detail`. Unknown/`secret source error`/`policy-invalid` are `DisclosureRefusal`, not empty or current-settings panels. |

**Noninterference.** Two configs that differ only in redacted values have different PlanId and digest (those commitments move with configuration) and identical remaining carrier bytes, including the 13 field slots. Secrets do not enter canonical output. A different digest on the same Plan is `SOURCE-DIGEST` (no current-settings fill).

Synthetic `plan_for` is a shape-admitted example. Full retained digest closure, semantic admission, and Plan/Run association remain host duties.

## Reproduction

Private copy, reference Python `-I -B`: `check.py` **13/13**, 8 pins, `selected: false`. Schema regenerates from pinned identity v3 `semantic-configuration`.

## Joint13

`composed-sources/configuration-disclosure.schema.json` is byte-identical (`0584bf2f…ef659`, 17322 B). Combined later composition does not rewrite or close this original-owner unit.

## Must-fix / should-fix

None in the stated reference scope.

## Remaining duties

Admitted Plan/Run handles; report carrier successor, byte accounting, and placeholder replacement; source/inventory/generator selection; browser and final serialized-HTML leakage. RP-DO-04 remains open until that integration. This unit does not qualify product configuration disclosure.

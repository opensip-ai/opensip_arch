# Schemas v5 repair plan (not a subject)

Codex REJECT of v4 `63ea2c47…` at
`component-manifest-schemas.v4.review-independent.codex.json`.
Do not edit frozen v4. Do not author v5 until Claude 2's v4 verdict is written.

## V4-B1

`dependencies: []` on every member still allows a multi-root exact-pin lock.
Do not claim "single-component only" while request is an array of pairs.

Intended repair: **no lock is producible until DR-111**.

- TC-ACCEPT lock member becomes: required class, DEFERRED to DR-111.
- Present evidence is index custody of admitted ACCEPT fixtures, not a lock.
- Remove the "sole presently producible lock" claim.
- Restore ID-DEP-4 to full width: no lock over any request, including
  exact-pin, until DR-111, because resolutionInputs include
  hostCoreVersion/platform and compatibility meaning is DR-111-owned (V4-B2).

## V4-B2

Even one exact-pin still records host/platform and ignores required
compatibility data. Do not invent a secret compatibility evaluator.
Do not call a non-validating pin a lock.

If a later successor wants a non-lock custody record, name it as such
and keep it out of lockSchema.

## V4-S1

`basedOn.method` must name only real repairLog finding ids.

## V4-S2

Either add a Codex-S2 entry that scopes v2 measurement fields as
historical, or add v5 authoring custody without claiming v2
whole-document pins are this authoring.

## After dual ACCEPT of that successor

Review corpus v2 (`19d6706f…` draft). Drop or relabel
`TC-ACCEPT.lock-single-component` to match "no lock until DR-111".

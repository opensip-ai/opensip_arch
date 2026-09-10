I'll read the root grouping experiment and the executed probe results, then reassess GR1/GR2 against those arguments instead of defending the prior uniqueness claim.# GR1/GR2 disposition (corrected)

**Standing.** Coauthor correction of my v2 GR1/GR2 text after Codex’s 18-case grouping experiment (`evaluator-grouping-experiment.v1`, `execution.json` exit 0, `probe.py` SHA-256 `b83d9c48…`). Hypothetical composition only: not schema admission, native population, waiver resolution, or Run replay. Frozen21 selectors cited below. GR1/GR2 remain **open for wire integration**.

## Retract / defend

**Retract.** (1) The claim that baseline unique fingerprints, SARIF 1:1, and boolean comparison presence **force** one `finding2` per `finding-key2`. That was a false uniqueness theorem. Baseline uniqueness is a **projection** law (`baseline-artifact.schema.json#/$defs/BaselineDescriptor/properties/entries`). `proof-bundle.findingIds` is unique on `finding2` identities, not fingerprints. SARIF 1:1 is with the findings array (`workflows-and-surfaces.md` §8), so two findings ⇒ two SARIF results. Comparison `PivotPresence` is boolean per fingerprint; “any admitted occurrence” is a **new aggregation reading**, not an existing schema sentence. (2) Treating disagreeing `parameterDigest` / message / `evidenceRefs` as `FINDING_OCCURRENCE_CONFLICT`. Count=1 vs count=2 under two configs is ordinary per-universe evidence. (3) Obligation clause that `none` / `count-at-most` / `all-covered` promotes an advisory rule to a gating deficiency. No identity §4 or workflows §5 citation requires that; those texts make **gating** / **required** predicates a typed deficiency, and optional import absence already non-gating (`IMPORT.ABSENT_FOR_PREDICATE`). (4) Dropping enumeration uncertainty once emitWhen is true, including after waiver. (5) Synthetic per-subject predicates for zero selected subjects. (6) Bundling omitted pointer / lost bytes / hash-corrupt bytes as `HOST.IO_FAILURE`. (7) “GR2 resolved.”

**Defend.** Universe-qualified **proof** subjects; volatile universe H stays out of `finding-fingerprint`. One logical baseline row per fingerprint when `BaselineEntry` fully agrees. Duplicate evaluation occurrence ≠ declaration ambiguity. Known selected subjects evaluate under existing per-subject sufficiency. Enumeration uncertainty is its own retained record. Fail ≻ required-unknown ≻ pass. Waivers need an explicit target and cannot complete membership. Operational faults stay outside this 3-value law.

## GR1 — choose (b)

Keep **one evidence-complete `finding2` per configuration occurrence**. Group **only** the baseline (and, separately specified, comparison presence) by recomputed fingerprint **descriptor + digest**.

Occurrence identity: `(ruleId, universe, nativeSubjectId)`. Exact duplicate ⇒ refuse. Distinct declarations remain identity §3 / GR6 (signature/anonymous collision). Grouping **assumes** independently established equal fingerprint descriptors; it does not invent correspondence from a shared path.

**Baseline projection** (`#/$defs/BaselineEntry`): `fingerprint`, `ruleId`, `detectorId`, `stabilityClass`, `subjectPath`, `waived`, and **presence and value** of optional `legacyFingerprint`. Any disagreement ⇒ refuse projection (no encounter-order merge). Agreed groups ⇒ one sorted unique entry. Non-baseline fields (message, parameters, `evidenceRefs`) **may differ** and stay on each `finding2`. Replay compares full occurrence content, not counts (the probe’s four same-count mutants illustrate the *composition* intent only).

**Tradeoff vs (a) with per-occurrence params inside one finding.** (b) keeps frozen finding semantics (one `parameterDigest`, one `evidenceRefs` bag per `finding2`) and avoids a representative occurrence. Cost: envelope/SARIF may repeat a fingerprint; repair/review remain fingerprint-keyed and must **disclose occurrence cardinality** rather than imply one citation. (a) would make SARIF/baseline/finding all 1:1 on fingerprint but would invent an occurrences payload and collapse config-specific metrics. Root’s preference for (b) is the better fit to current finding identity. I adopt it on that tradeoff, not because uniqueness forbids (a).

Comparison presence = any admitted occurrence of that fingerprint at that pivot, **provided** this is written as a comparison extension. Mixed `waived` on one fingerprint is a baseline-field conflict (fingerprint/path waivers have no universe axis today). Do not claim one gate projection for every audit profile (`gateRuleUnder` `baseline-or-current` vs `current-only`, §3).

`finding.subjectId` can stay the evaluation-qualified id so two configs remain distinct `finding2`s; fingerprint remains the logical key. That is the subjectId split worth keeping from v2, without stuffing evaluation-H into the fingerprint.

## GR2 — enumeration record, not a predicate

Export/population uncertainty selects **who is in S**. It does not rewrite exists/none on `s ∈ S`. No synthetic subject for unresolved or for `|S|=0`.

Every **enabled** rule retains a `RuleEnumerationV2` (insertion still `proof-bundle.enumerationIds` + inventory `ProofInputRef`s) even if `selected=[]`. Disabled-rule omission is a G6 choice the probe assumed, not a closed law.

```
live = ∃ finding: enabled ∧ effectiveGating ∧ ¬waived
reqUnknown = requiredExecutionIncomplete
          ∨ ∃ enabled rule: effectiveGating ∧ (exportUnresolved ∨ populationUnavailable)
          ∨ existing required-evidence / required-coverage unknowns
verdict = fail if live else indeterminate if reqUnknown else pass
```

Advisory unresolved ⇒ disclose only (`RuleDeficiency.gating` stays independent at comparison). Required **execution** selection can still indeterminate an all-advisory policy. Waiver of `live` does not clear `reqUnknown`.

**Bytes vs structure (not one IO code):** omitted required `enum2:` pointer → structural proof refusal; listed digest with missing bytes → retention loss; supplied bytes that fail hash/schema → existing admission/hash fault.

**Carrier not complete** until field set, joins, limits, and GR3 expected partitions exist. `population: complete` in the probe is an **input**, which the design-note already says must not be a producer assertion.

## Probe limits (18 PASS ≠ conformance)

ASCII `json.dumps` ≠ C; fingerprints are fixture strings, not recomputed descriptors; `waived` is an occurrence flag, not Plan waiver resolution; no native inventory/export, no `evidenceUse`, no `gateSeverityAtLeast`, no SARIF/comparison entry build, no identity-graph retention. `complete-empty`→pass only because findings were pre-decided. Useful as a composition sketch; **not** qualification.

**Remaining schema work:** `enum2:` `$def` + H domain + `byDomain`; `proof-bundle.enumerationIds`; occurrence-duplicate refusal; baseline grouping + comparison presence sentences; SARIF/envelope occurrence-vs-logical counts; byte-fault routes; GR3 population; G6 disabled rules; G9 profile-specific gating. Stop.

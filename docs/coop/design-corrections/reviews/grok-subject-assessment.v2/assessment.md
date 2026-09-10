I'll start from the retained root assessment and the frozen proof/finding/baseline schemas, then settle GR1 and GR2 with concrete record shapes.Root refinements are in: GR1 is fingerprint/baseline collision, GR2 is a missing enumeration-result carrier. I’ll read the frozen proof, finding, and baseline definitions next.# GR1/GR2 continuation — finding aggregation and enumeration carrier

**Standing.** Actual Grok coauthor continuation. Resolves GR1 and GR2 only. Frozen21 pin unchanged (`candidate-subject.v21`, manifest `360c2758c0409ebc307966c7a385c385c2d7f580b4623dd760b7ba0e26bf18c1`). No source assent, no implemented patch, no executed examples. Prior qualified evaluation subjects and “universe H stays out of fingerprints” remain. GR3–GR8 are interactions, not closures.

## GR1 — pick (a): one logical finding, configuration-qualified occurrences

**(b) is incompatible with published uniqueness.** `BaselineDescriptor.entries` is sorted strictly by `fingerprint` and **duplicates rejected** (`workflows/schemas/baseline-artifact.schema.json#/$defs/BaselineDescriptor/properties/entries`). Comparison `Entry.presence` is **boolean** at B/E0–E4 (`comparison-result.schema.json#/$defs/PivotPresence`); classification is the first axis at which that fingerprint’s presence/waiver changes (workflows-and-surfaces §3). Repair targets, review `candidateId`, and `legacyFingerprint` migration are fingerprint-keyed. SARIF v1 results equal envelope findings **one-to-one** (§8). Two `finding2` rows that share `finding-key2` would either fail baseline adoption, fork comparison into a count/any/all law the schema does not have, or emit two SARIF results for one comparison entry. That is a silent semantic change. Reject (b).

**(a)** keeps the existing 1:1 chain:

`finding-key2` → one `finding2` → one baseline entry → one comparison entry → one SARIF result → one repair/review target.

Per-universe evaluation stays in **proofs**, not in extra fingerprints.

### Split the two `subjectId` meanings

| Record | `subjectId` | Why |
|---|---|---|
| `predicateProofs[]` | evaluation-qualified: 64-hex `H("evaluation-subject", {schemaVersion:2, universe, nativeSubjectId})` | Unique `(ruleId,subjectId,predicateId)` (`identity-schemas.v2.json#/$defs/proof-bundle` `x-opensip-order: predicate`); completeness stays per `sourceUniverse`/`targetUniverse`. |
| `finding.subjectId` | **logical native spelling only** (file: `LogicalPath`; symbol: `SubjectIdV1`; package: package-name) | Same string the fingerprint is built from. **Not** evaluation-H. **Not** universe H. |

This **corrects** the earlier proposal that stuffed evaluation-H into `finding.subjectId`. That field’s *meaning* changes relative to that draft; relative to frozen `finding.subjectId` (`Text` 1–4096) it stays “logical subject,” which is what baseline `subjectPath` and fingerprint `logicalPath` already assume.

Fingerprint recipe unchanged: `finding-fingerprint.subjectKey = {language, kind, logicalPath, qualifiedName, discriminator}` with discriminator = raw SHA-256 of canonical JSON of declaration-signature tokens (identity §3). Universe resolved-input H never enters it, so tsconfig/graph churn does not mint a new `finding-key2`.

**Occurrences are not ambiguous declarations.** Identical signatures in one collision class still refuse correspondence (identity §3). Two overloads with different tokens → two discriminators → two fingerprints → two findings. Two universes with the *same* language/kind/path/name/tokens → **one** fingerprint with two occurrences.

### Finding payload (bounded)

Keep `finding` required fields. Add:

```
occurrences: array, minItems 1, maxItems 128, unique by universe
  x-opensip-order: { by: ["universe"] }
  items: { universe: DigestHex, nativeSubjectId: Text, witnessDigest: Hash }
```

`witnessDigest` names the emitWhen-root `predicate-witness` for that evaluation subject (`#/$defs/predicate-witness`). `finding.evidenceRefs` remains the existing closed union (facts, coverage, imports, those witnesses, explicit blobs) — no new hidden root. `finding-parameters` stays message scalars; do **not** smuggle universes there.

**Minting.** For each enabled rule, take evaluation subjects whose emitWhen root is `true`. Reconstruct `finding-key2` from the inventory row (GR4 language split still open; use the row’s source/body language once GR4 exists). Group by fingerprint.

**Full-content equality (merge).** Members of a group must agree on `ruleClosure`, `finding.subjectId`, `messageCode`, `parameterDigest`, `severity`. Then one finding: `occurrences` = the group, `evidenceRefs` = set-union. **Conflict** (any of those differ, or reconstructed fingerprints collide while `logicalPath`/`qualifiedName`/tokens disagree): refuse `FINDING_OCCURRENCE_CONFLICT` as a schema/identity fault (identity §4: not a fourth truth value). No last-write, no encounter-order suffix.

**Waivers.** Fingerprint target matches the one logical finding (all occurrences). `(ruleId, subjectPath)` matches `subjectKey.logicalPath` only. A waiver never deletes `occurrences`, never flips enumeration `membershipState`, never satisfies required coverage/evidence. Completeness is not waived.

**Surfaces (no silent semantic change).**

- Baseline: still unique fingerprint; `subjectPath` = `logicalPath`. Per-universe *no-match* and incomplete proofs are **not** baseline entries (they never were findings).
- Comparison: boolean presence = “this fingerprint has a finding on that pivot.” Per-universe residual stays on the sealed proof/enumeration, which comparison already treats as rule-level coverage via `ruleDeficiencies` (zero findings never prove complete analysis, §3).
- SARIF: still 1 result per envelope finding. `result.fingerprints` carries `finding-key2`. `result.locations` lists occurrence paths (same `logicalPath` if they agreed; universe hex only in **properties**, not in the location URI). Do not emit one result per universe.
- Source-qualified evidence: facts/anchors/inventory paths remain the location; occurrence.universe is provenance of which native configuration produced the true predicate, not a second identity.

Replay reconstructs groups and the full finding records (occurrences + evidenceRefs + parameterDigest), not a finding **count**.

## GR2 — retained `RuleEnumerationV2`

Frozen `proof-bundle` has only per-subject `predicateProofs` plus aggregate `verdict`. Zero candidates ⇒ zero proofs ⇒ no carrier. That hole is GR2.

### Record (new H domain `rule-enumeration`, prefix `enum2:`)

```
RuleEnumerationV2
  schemaVersion: 2
  planId: plan2:
  ruleId
  ruleProgramDigest          // same hex as proof.ruleProgramDigest
  selector: { universe, subjectKind, include, exclude }  // copy of Rule.subjectEnumeration
  boundUniverses: DigestHex[]  // U(R), canonical-set; may be empty
  inventoryRefs: ProofInputRef[]  // domain subject-inventory only
  expectedPartitions: [{ universe, inventoryDigest|null, populationState }]
  selected: [{ universe, nativeSubjectId, path, exported: true|false|null }]
  unresolved: [{ universe, nativeSubjectId, path|null, cause }]
  membershipState
  obligation
```

`populationState ∈ {observed, unavailable, unestablished}`. **`unestablished` is the GR3 residual** — listing a partition does **not** prove Plan-cell population. Do not infer complete empty from “no rows.”

`membershipState ∈ {determinate, unknown-membership, selector-unbound, population-unestablished}`.

`unresolved.cause ∈ {export-unknown, glob-undecidable, inventory-unavailable}`.

Bounds: `selected`/`unresolved` `maxItems` 100000 (same as `subject-scope.subjects`). Do not retain the excluded-known set; replay recomputes exclusion from inventories + selector.

`obligation ∈ {required, optional}` — **not** `Rule.gate` alone:

- **required** if any of: (1) `RuleCoverage.gating` on this side (effective severity vs policy gate, already not a raw `gate` bit); (2) any `evidenceUse.requirement = required`; (3) emitWhen uses `none` / `count-at-most` / `all-covered` (incomplete case is indeterminate, identity §4 table); (4) a **required** selected capability is what would determine membership (export/inventory). Exact capability-cell map is GR3.
- **optional** otherwise, parallel to optional import: disclose, do not mint comparison `RuleDeficiency`.

### Where it enters proof

Add `proof-bundle.enumerationIds`: canonical-set of `enum2:` ids, **one per evaluated rule** (G6 which rules are evaluated is still open; this requires a slot even when `selected` is empty). Inventories stay in `evaluationInputRefs` (new `ProofInputRef.domain: subject-inventory`). Enumeration is an **output**: producer-supplied bytes are not authority.

**Replay (identity §4 “complete normalized result”).** For each evaluated rule, recompute the entire `RuleEnumerationV2` from retained inventories, Plan-bound universe frames, and selector; compare canonical bytes / `enum2:` identity. Also recompute predicate proofs and finding groups. Agreement on `selectedCount` alone is not replay.

### Absent promised record vs observed unknown

| Situation | Carrier | Class |
|---|---|---|
| Enabled/evaluated rule with no `enumerationIds` member, or `enum2:` listed but bytes missing/corrupt | none | Retention/operational (`HOST.IO_FAILURE`); not a predicate value (identity §4 missing-witness law) |
| Record present, `membershipState = unknown-membership` (incl. **0 selected, unresolved > 0**) | `enum2:` | Observed unknown evidence |
| Record present, `boundUniverses = []`, `selector-unbound` | `enum2:` | Observed unknown (valid portable selector, this Plan bound none) |
| Record present, `determinate`, `selected = []`, `unresolved = []` | `enum2:` | Observed empty set — `exists` false only if coverage for those universes is complete; **not** from “no record” |
| `expectedPartitions[].populationState = unestablished` | `enum2:` | GR3; must not be treated as determinate empty |

### Known-true findings survive unresolved siblings

Evaluate emitWhen **per evaluation subject** on `selected` only.

Identity §4 incomplete cases, with unresolved treated as incomplete membership of the intended set:

- `exists`: true on a known match **even if** unresolved remain → those trues still aggregate to findings (GR1). If no known match and unresolved remain → indeterminate, not false.
- `none` / `count-at-most` (when known count ≤ N) / `all-covered`: unresolved ⇒ indeterminate (cannot prove the negative/bound).
- Zero known exported + unresolved: `selected=[]`, `unknown-membership` → `exists` indeterminate; **not** pass.

**Verdict (sealed 3-value, identity §4):** fail ≻ indeterminate ≻ pass. Unwaived control-bearing true findings still **fail**. A required enumeration unknown projects to existing comparison `RuleDeficiency.cause = required-coverage-unknown` (`comparison-result.schema.json#/$defs/RuleDeficiency`) when `obligation=required` and emitWhen is not already true; it does **not** delete findings or downgrade fail. Optional obligation: retain `enum2:`, no `RuleDeficiency`, same as `IMPORT.ABSENT_FOR_PREDICATE`. Waivers do not clear `unknown-membership`.

## GR3–GR8 (flags only)

- **GR3.** `expectedPartitions` is a slot, not a Plan-cell obligation map. Empty `selected` is determinate only when every listed partition is `observed` — which GR3 must define.
- **GR4.** Fingerprint `language` must not be engine `syntax` / TS-engine-for-JS; occurrences do not fix that.
- **GR5.** `enum2:` + inventory refs + evaluation-subject H still need registry rows, closure traversal, multi-provider mismatch.
- **GR6.** Empty `signatureTokens` for symbols still cannot widen anonymous matching; GR1 grouping uses the existing discriminator.
- **GR7.** Qualified proofs + logical findings is a **choice** (baseline uniqueness + Kleene), not a uniqueness theorem. A union *with* per-universe proofs is a different design, not shown sound here.
- **GR8.** Majors (`proof-bundle`/`finding` 2→3 vs in-place v2), `ProofInputRef`/`byDomain` rows, `FINDING_OCCURRENCE_CONFLICT` routing, `enum2:` size limits: not a patch.

## Four conceptual examples (not executed)

**C1 — two TS universes, same logical symbol, both true, equal message/severity.** Selector `native.semantic-universe.typescript.v2`. Two `predicateProofs` (`subjectId` = two evaluation-H). One `finding-key2`, one `finding2` with `occurrences.length=2`, one baseline row, one comparison entry, one SARIF result with two location properties. (b) would be schema-refused at baseline unique fingerprint.

**C2 — same reconstructed fingerprint, `messageCode` differs across universes.** `FINDING_OCCURRENCE_CONFLICT`; no merged finding; not two baseline entries.

**C3 — `subjectKind: export`, 0 `exported=true`, 5 `unknown`, gating `exists`, `obligation=required`.** `enum2:` present, `selected=[]`, `unknown-membership`. No findings. Predicate incomplete → Run **indeterminate** (`required-coverage-unknown`), not pass, not missing-bytes operational. If another rule already fails, verdict remains **fail**; this `enum2:` still retained.

**C4 — 2 known exported trues + 3 unknown.** Two occurrence-merged findings (or two fingerprints if they differ). `exists` true; fail if those findings control-bear and are unwaived. `enum2:` still `unknown-membership`. Fingerprint waiver suppresses findings, **does not** make membership determinate or mint observed-empty.

Stop.

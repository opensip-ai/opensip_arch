# Advisory: next native relation / capability / coverage-prerequisite owner

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded owner/API map after installed runtime v4. **Not ACCEPT-DESIGN-UNIT. Not live install. Not body15 source acceptance. Not full Run.**
**Live lock independently observed:** **12 inventory / 17 contract** (last contract `native-runtime-selection-v4`). Body-identity inventory v15 remains private testing.
**Work tree:** `/tmp/opensip-implementation/m2-grok-native-relation-boundary-16`. No live/frozen/history edits.

Selected references: identity `619d6e3c…41e6` / 158555; native `e6784aa1…e2b9` / 319944. Plan-native-boundary-14 is an advisory, not a selected-pair token.

## Actual caller order (`open_run_closure`)

Schema-driven `walk(run)` runs **first**. A fact’s relation payload then fires `relation_payload_rules`:

1. `syntax_capability_supported(fact)` — `syntax_universe_selection` **does** `admit_frame` the named context (identity 1143–1148). That follow is correct **here** and forbidden on the Plan census path.
2. Rung fields / universe rule / NFC.
3. `relation_source_joins` then, if the relation registry carries `bodyIdentityJoin` (today `clones` only), `body_identity_join` → `body_language_version` (ownership / suffix dialect, L0 span or L1–L3 tokens).

**Then** the Plan-native block (1689–1749; installed `inspect_plan_native`). `PlanNativeChecks` is `{context_count, universe_count}` only. It is **not** a selected (universe, context) pair, not an ADMIT, and not a prerequisite token for the body join that already ran.

**Then** the view/coverage loop (1917–1948), most-specific first:

1. `admit_coverage_result_v3` (producer may also apply `source_variant_capability_support` for `source-path` + caller-supplied dialect).
2. `coverage_dialect_prerequisite` → `clone_ownership_disclosure`.
3. `syntax_capability_prerequisite` → `syntax_capability_support` (`require_all` from `subjectKind`).
4. `coverage_source_variant_prerequisite` → `source_variant_capability_support` over `body_eligibility_table` (backstop; total over published universes).
5. `coverage_inventory_totality`.

Do not invert this. Do not wait for Plan-native counts before fact-time syntax/body joins.

## Two owners, not one

| Owner | Inventory 15 | When | Selected functions |
| --- | --- | --- | --- |
| Clone **body** join | already `body_identity.rs` + `body-registry.json` | fact walk, before Plan-native | `body_identity_join`, `body_language_version`, `admit_normalization_specification` |
| Relation **capability / coverage prerequisite** | **not named** in v15 | fact walk (`syntax_capability_supported`) **and** coverage loop (three prerequisites) | `syntax_universe_selection`, `syntax_capability_support`, `source_variant_capability_support`, `clone_ownership_disclosure` |

v15 descriptions cover clone frames / normalization / dialect identity. They do not own grammar-capability or coverage-disclosure law. Folding the latter into `body_identity.rs` would mix call times, inputs (fact vs scope+Coverage), and metadata, and would invite treating Plan-native counts as a pair token.

## Evaluator API (concrete)

Identity frames; evaluator derives. Identity must not depend on evaluator. No caller ADMIT of Coverage or PlanNativeChecks.

```
inspect_syntax_capability_fact(inputs, universe_digest, relation, rung, anchor_paths, work)
  -> Result<(), NativeCapabilityError>
  // require_all=true; empty anchors unsupported; compiler universes no-op

inspect_syntax_capability_scope(inputs, universe_digest, snapshot_id, relation, rung, subjects, subject_kind, work)
  -> Result<Option<UnsupportedDisclosure>, …>
  // source-path: ALL subjects; else inventory, ANY path; inventory relations never gated

inspect_clone_ownership_disclosure(ownership, subjects, edition_map)
  -> Option<OwnershipDisclosure>
  // missing → unenumerated → ambiguous; not-compiled/not-selected: None (complete lawful)

inspect_source_variant_capability(eligibility_table, relation, rung, paths, require_all)
  -> Option<UnsupportedDisclosure>
```

Coverage-time composition (same order as identity 1938–1947): dialect ownership, then syntax grammar registry, then source-variant backstop. Each keeps its own refusal names. A disclosed unsupported scope is admitted; only false `complete` / wrong deficiency / wrong cause refuse.

`syntax_universe_selection` belongs to this owner, **not** to `inspect_plan_native`. Plan census must keep frame-only universe retain.

## Schema / closed metadata

Authorities (extract, do not restate):

- `native-v2.schema.json#/x-opensip-grammar-capability-registry` (also already copied into live `native-context-registry.json` `grammarCapabilities` — drift-control if both are kept).
- `identity-v3` `scopeCapabilityLaw.onUnsupportedScope` = `{coverage: unknown, deficiency: language-tier-unsupported, nativeCause: capability-missing}`.
- `identity-v3` `bodyEligibilityLaw` / per-universe `languageVersionBinding.bodyEligibility`.
- `relation-payload-v2` `bodyIdentityJoin` + `subjectKindLaw`.
- Native `CLONE_OWNERSHIP_DISCLOSURE` and `INVENTORY_CAPABILITIES` (`file@enumerated`, `package@manifest-declared`, `vcs-change@vcs-reported`).

`native-plan-registry.json` is Plan **request** vocabulary (`capabilityId` / `NOT-SELECTED` cells), not grammar-borne `relation@rung` support. Do not reuse it as this registry.

## Additional filenames vs inventory 15

Keep v15 as body join. Add:

- `crates/evaluator/src/capability_support.rs` (`role: validator`, snake_case)
- `crates/evaluator/src/capability-support-registry.json` (`role: registry`, kebab, `generated: false`) — inventory capabilities, unavailable pair, clone-ownership disclosure table, and grammar language/capability/suffix rows (or a documented single-reader of the native-v2 registry with a byte drift check against `native-context-registry.json`).

Host tests/fixtures can extend `native_owner_tests.rs` / `native-context-fixtures.json` rather than new packages. No new crate, edge, or identity→evaluator.

## Adversarial tests (minimum)

**Fact-time (walk, before Plan-native):** Markdown-anchored `declares@syntactic` under syntax universe → `SYNTAX_CAPABILITY_UNSUPPORTED_FACT` even if a `.rs` grammar is also selected; unanchored code fact (`require_all`, empty paths) unsupported; `references@resolved-binding` under `resolutionAttempted: false` unsupported; inventory `file@enumerated` on `.md` supported; compiler-universe fact skips syntax grammar gate.

**Do not** require `inspect_plan_native` Ok-counts before these. A fact whose universe context is later not Plan-selected still runs the fact-time gate, then fails `NATIVE_CONTEXT_SET_JOIN`.

**Coverage-time order:** Rust clones + missing ownership + `complete` → `COVERAGE_DIALECT_PREREQUISITE` / `body-language-ownership-missing`, not source-variant; partial enumeration before any row is read; selected owners disagreeing on edition → ambiguous; `not-compiled` / `not-selected` path + `complete` **lawful**. Syntax clones over data-only snapshot + `complete` → `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` (syntax name, not source-variant). TypeScript clones over `package.json` + `complete` → `COVERAGE_SOURCE_VARIANT_*` / `capability-missing`. Mixed `src/a.ts` + `package.json` discloses. Empty source-path subjects unsupported. Wrong deficiency `budget-exhausted` with null cause refuses. `file`/`package`/`vcs-change` never dialect-gated. Symbol subjects are **not** parsed as paths. Do not mint Coverage for `clones-cross-tsjs`.

**Producer vs closure names:** `native.coverage-source-variant-*` can fire first at `admit_coverage_result_v3` for source-path; closure names are not always reached (`scopeCapabilityLaw.refusals`).

## Traps

- Treating `PlanNativeChecks` as a selected pair / ADMIT.
- Using `syntax_universe_selection` (context follow) inside Plan census.
- Putting coverage/capability law in `body_identity.rs`.
- `all([])` vacuous support.
- Grammar-gating inventory relations.
- Collapsing `OWNER_NOT_COMPILED` into missing capability.
- Running source-variant before dialect/syntax guards.
- Catching native `AdmissionError` with identity’s class.
- Caller-supplied Coverage ADMIT skipping derived disclosure.

## Verdict

**NOT ACCEPTANCE.** Next bounded evaluator owner after runtime v4 is the **capability/coverage-prerequisite** slice, sibling to private body15, not a substitute for it. Additional inventory files beyond v15 are required. No full Run or coverage authority from caller ADMIT or Plan-native counts.

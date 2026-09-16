# Blind review — consumer-b.v24, source39 continuation

**Verdict: CHANGES_REQUIRED**

**Standing.** This is an independent blind consumer reconstruction of the selected source39 kit only. It continues the same original fresh origin `9d3dfb70-b2d3-498c-a3c1-f8de9e488514` in runtime `consumer-b.v24-source39.v1`.
- This review makes **no product qualification claim** and grants no implementation authorization.
- External root admission of the exported bytes is a separate gate; its outcome is unobserved here.
- The following are future qualification, explicitly unperformed and not counted as design omissions:
  - real OS/compiler/crypto/SQLite measurement;
  - native compiler/provider execution as enforcement;
  - host authentication;
  - synthetic TCB enforcement.

The prior runtime `/tmp/opensip-design-corrections/consumer-b.v24` is read-only own history. Only its helper source code was ported (`port-manifest.json`), and none of its measurements is used as current conformance.

## 1. Input custody

- `subject/consumer-input-manifest.json`: SHA-256 `c2f2f88d2e3bebfa8fa1b521cb76d2584483eb922973d6e555fe05a15da4ad80`, parent subject `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`.
- All 104 members are hash- and length-exact, with no unlisted file, both at phase 0 (`vectors/phase0-custody.json`) and again at the end (`runs/final-custody.json`, PASS, rows identical).
- The kit delta from my own prior custody rows (orientation only): 2 files added and 32 changed.
- No custody gap. `docs/coop/design-corrections/discovery-defaults.py` is named by native U-4a only as a reference implementation that the text governs.
- Read: charter, requirements, the new subject, my own old and new outputs, and the installed Python stdlib/jsonschema. Nothing else.

## 2. What was reconstructed and executed

**Original failure, preserved.** The ported helpers were run unchanged against source39 first, and every one of the 26 Runs refused at owning-schema admission: `SCHEMA_REFUSED:execution-inputs /nativeCoverageAccounts/0/targetUniverse` (`logs/s39-original-closure.0.from_scratch.log`). The original sources and stores are preserved byte-exact in `preserved/s39-original/` with a SHA-256 manifest. Corrections HC-14..HC-32 follow, each tied to a kit selector (`tools/hc_source39.py`; per-phase `checkpoints/phase-N.json#/helperCorrections`):

- account `targetUniverse` null, and a body-eligible clones census (execution-inputs s5, `bodyEligibilityLaw`);
- stage output schemas registered by the producer closure tree (identity s3; `STAGE_OUTPUT_SCHEMA_*`);
- the normalization specification map in the interpreting closure (`normalizationSpecificationLaw`; `BODY_NORMALIZATION_*`);
- the scope-capability law for every universe via `bodyEligibility`, in the published guard order and with the published refusal names;
- U-4b discovery/membership order, ordinals and row decision, and the U-9 zero-config syntax-only fallback. Closure now enforces `ENUMERATION_MEMBERSHIP_ORDER` / `_ROW_DERIVATION` over the retained record;
- snapshot rows read from `node_modules` joined to the committed layout (`SNAPSHOT_PRUNED_TREE_NOT_A_READ`);
- one parameter per registered row (`ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS`); stage parameters as spec rows (`STAGE_SPEC_HIDDEN_PARAMETER`);
- the TS universe flags (native lines 537-540);
- tool-level fixes: from-scratch roles, query carrier, comparison presence/absence law, envelope goldens, mutation base variants, custody constants.

Several corrections themselves failed on first run: the stage-spec digest (HC-15b), wrong mutation bases (HC-27), a circular vector record (HC-28), the golden runId (HC-29) and a golden key (HC-32). Each failing log is retained.

**Complete positive Runs.** 27 claimed complete positives are admitted by independent retained closure and replayed from scratch in a fresh process each (`runs/from-scratch.summary.json`):
- **TypeScript:** `ts-pass`, `ts-fail`, `ts-clones-required`.
  - `node_modules` bare specifier and layout, with the read manifest as a snapshot row.
  - Config extends graph and lockfile.
  - `ScopeDocumentV1` in the analysis-spec.
  - Imported runtime payload in the graph.
- **Rust:** `rust-mixed`, `rust-mixed-clones-required`, `rust-extra-unit`, `rust-same-file-2021`, `rust-ambiguous`, `rust-partial`.
  - Mixed and target editions, per-body dialect, the same file under two selections, the `#` marker, a 302-entry edition map.
  - Version component derived from the admitted rustc context.
  - Stable body identity on an ownership change.
  - Partial enumeration with empty clones and the published disclosure pair.
- **Syntax-only:** `syntax-code` (L0 and L1 clone bodies with map custody), `syntax-data` (data grammars: syntax/clones unknown `language-tier-unsupported`), `syntax-mixed-disclosed`, `syntax-mixed-omitted`. Each carries the U-9 DEFAULTED fallback unit.
- **Comparison family:** 14 `cmp-*` Runs, including the source39 work-budget Run `cmp-budget`.

The designed negative `syntax-mixed-falsecomplete` refuses `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`. All 62 exported stores (positives, designed negative and input mutations) are replayed in fresh processes (`runs/replay-all.summary.json`). Every mutation refuses at its owning boundary, except the lawful controls `syntax-code~budget-exhausted` and `syntax-code~explicit-endpoint-source`.

**Four boundaries kept distinct for every positive** (`runs/<run>.records.json#/boundaries`):
1. Owning-schema admission including published kit keywords (`x-opensip-order`, the `x-opensip-digest` closing law with source39 annotations).
2. Helper predicates.
3. Retained closure joins followed by complete semantic replay: C(recomputed proof) byte-equal plus proof/evidence/seal/Run identity equality (`runs/replay-export.summary.json`).
4. Host enforcement, which is not claimed.

The discriminating tamper controls on `syntax-code`, `ts-pass` and `rust-mixed` keep identities and citations valid while changing the logical result. Replay refuses every one (`runs/*.tamper-outputs.json`).

**Exact export.** `runs/<run>.store.json` holds the object table and every blob/frame keyed by digest, including closure tree members (stage-output schemas, normalization maps).

**From-scratch command.**
```text
cd /private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1/output
/tmp/opensip-architecture-review-env/bin/python -I -B tools/from_scratch.py
/tmp/opensip-architecture-review-env/bin/python -I -B tools/replay_export.py
```
The full command set is in `notes/09-reconstruction.md`.

**Standalone, schema-envelope and query vectors (all asserting, 0 failures).**
- **Phases 1–3:** canonical/H/lexical, CVE1 capability manifests, protocol3 traces.
- **Phase 4:** relation/rung and state rules (`vectors/phase4-tables.json`); the rust-cargo-prepared mode path (`vectors/mode-rust-cargo-prepared.json`).
- **Phase 6:** config, clone-body, clones negatives, repair, min-resolution, imported boundary, mutation keys, pinned purge. Under the map law the not-retained control now refuses `EVIDENCE_UNAVAILABLE`, and a another-level control refuses `BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH`.
- **Phase 7:** zero-config chain, multi-unit availability, public-from-internal envelopes, D9 extension, receipts. New: `vectors/discovery-membership.json`, 16 vectors covering U-4b, U-8, U-9, default selection, `NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT`, and retained-record enforcement controls.
- **Phase 8:**
  - Baseline audit and missing / evidence-changed / empty / scope-only comparisons, E0 vs E1..E3, pivot-only fingerprints, authorization, and purge/replay/output failures.
  - 45/45 public termination goldens with complete envelopes.
  - New: `vectors/comparison-absence-knowledge.json`, which measures `current-absence-unknown` and `baseline-absence-unknown` under the closed reason order.
  - New: `vectors/run-termination.json`. Terminations are derived by the source39 owner over 28 closed Runs; the D9 golden `analysis-budget-exhausted` is reproduced, with 9 candidate checks and 30 host-composition cases.
- **Phase 9:** `vectors/graph-query.json`, 53 vectors over admitted Runs. The public carrier is CommandEnvelope major 3 `querySurface=graph-query-response` with `queryResponse`, and parity is read at the inventory `parityPaths`.

## 3. Required finding

### s39-M1 (MUST): U-4b assigns no `unitKind` to a tsjs unit, although UnitMembershipV1 is identity

**Selectors**
- `docs/v2/contracts/product-v1/native-evidence.md` lines 730-732: U-4b states that `UnitMembershipV1` enters PlanId, so every choice is identity and none is left to an implementation.
- Lines 744-748 (U-4b.2): a tsjs unit gets marker, mode, recognizerId and recognizerVersion, but no `unitKind`.
- Lines 739-740 and 854-855 do assign the rust and fallback kinds.
- Line 622 and `native/native-evidence.schemas.v2.json#/$defs/WorkspaceUnitV2/properties/unitKind` publish `ts-program|js-program` with no mapping.
- `membershipDigest` → analysis-spec parameter → PlanId.

**Measured** (`vectors/discovery-membership.json#u4b-tsjs-unit-kind-not-assigned`)
- One `tsconfig.json` with `allowJs` gives a `js-allowjs` unit.
- Its membership record spelled `js-program` and spelled `ts-program`:
  - both admit against the schema;
  - both pass every published U-4b enforcement check;
  - they mint different `membershipDigest` values (`34d0e48f…` vs `52a0e505…`), hence different PlanIds.

**Invention required.** This reconstruction chose `ts-tsconfig` → `ts-program` and `js-allowjs`/`js-synthesized` → `js-program`, recording the alternative. The remedy belongs to the kit: one mapping row in U-4b.2.

**SHOULD:** none remain.

## 4. Disposition of this origin's prior issues

All five prior MUSTs and seven prior SHOULDs are resolved by source39 current owners, each re-verified and measured:
- **M1** census: `ts-clones-required` and `syntax-mixed-omitted` now seal pass.
- **M2** `nodeDigest` Predicate: `syntax-code~explicit-endpoint-source` admits.
- **M3** membership order: `membership-reordered` refuses `ENUMERATION_MEMBERSHIP_ORDER`. Only the narrower tsjs `unitKind` remainder (s39-M1) is new.
- **M4** `detectorId` = `contributionId`.
- **M5** query carrier.
- **S1** stage output registration.
- **S2** normalization map.
- **S3** U-9.
- **S4** `targetUniverse` null.
- **S5** argvDigest.
- **S6** goldens: 45/45 with details.
- **S7** absence reasons.

Of the prior advisories, A1–A7, A9 and A11–A13 are resolved; A8 is partly carried; A10 and A14 are carried. The full table with source39 selectors is in `notes/10-gaps.md` and `blind-review.json#/priorIssueDisposition`.

## 5. Advisories (nonblocking)

- **A-c1** Unpublished internal refusal names still carried as cb24: the syntax grammar-capability scope mismatch/undisclosed variants, E0 pivot joins, detector listing refusals, the test consent relabel, and native-preparation grant joins.
- **A-c2** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination; this is a live successor-artifact obligation (native s10 lines 3285-3299).
- **A-c3** Exact-snapshot import correspondence changes `import2` on every source change, so gating evidence rules attribute `INDETERMINATE` `evidence-content-changed` (workflows s3 lines 440-449).
- **A-n1** Under the closed per-entry IndeterminateReason order (workflows s3 lines 402-411), reason (3), the detector disposition, is unreachable for entries: an indeterminate detector leaves the changed-detector E0 null, so (1) applies first. The disposition keeps its reason, and the recipe termination is read from dispositions (`vectors/baseline-e0-e3.json`).
- **A-n2** In the run-termination contract, s6 lines 168-176 conflict with s1 lines 34-35: `errorCode`/`faultCause`/`signal` can be refused as UNKNOWN_FIELD or as NOT_DERIVED. Both refuse.
- **A-n3** Run-termination: a non-object candidate has no published key, and `RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_*` is a wildcard.
- **A-n4** Run-termination s7.3 fixes the `commit_inventory` member set only "as the reference commit path inventories them". The receipt is operational and excluded from Run identity.
- **A-n5** Native U-4b.2 "folded into the DEEPEST such workspace" is self-referential for nested workspaces. Cargo rejects nested workspaces; not measured.
- **A-n6** Native U-4b does not restate a rust unit's `languageMode`; it is derivable from the mode table (lines 165-166).

## 6. Limitations

- Run-termination s7.5 row 2 and s5 stage-terminal carriers are exercised only through the law's code paths. No built Run has a `provider-unavailable` primary or a retained stage terminal.
- The synthetic trusted observations are assumptions, not enforcement.
- Root admission is unobserved.

## 7. Requirement status

- 123 requirements plus 8 standing rules are accounted in `requirement-status.json` and `blind-review.json#/requirementStatus`.
- Every accept-blocking ID is executed with a measured artifact; none failed.
- The 3 future-qualification items are unperformed and not claimed.
- Checkpoints `checkpoints/phase-0.json` … `phase-11.json` carry the unioned ID sets, artifacts and helper corrections.

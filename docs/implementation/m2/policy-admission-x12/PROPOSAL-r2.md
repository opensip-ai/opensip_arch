# Configuration and policy-pack admission — proposal X12 r2

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X12 of `EXIT-PLAN.md`, release gate DR-G24 PREVIEW-ANALYZE-WELL-FORMED-ADMISSION. X5 r1 split this gate out of X5 (`replay-join-x5/PROPOSAL.md` item 1, "Correction to EXIT-PLAN"). The governing documents are:
- the register's DR-G24 row (`08-decision-and-readiness-register.md` line 369: "Host admission of preview analyze requests refuses a non-bundled pack identity and a non-declarative pack or contribution"; retained evidence "pack-identity refusal before evaluation; imperative-pack refusal; no user or third-party pack"; "no waiver for silent admission"), and DR-131 (line 320, SATISFIED at D-369);
- the DR-131 contract `docs/coop/artifacts/preview-analyze-contract.v2.json`: `$.pack` (`opensip.preview.typescript.pack`, version 1, "Exactly one pack. Host-owned. Bundled. First-party. Declarative-only. … No user packs. No third-party packs.", rule IR not frozen), `$.planIdMembership`, and `$.negativeTests` NT-1 and NT-2;
- the G24 harness occupancy `harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json` and `g24-input-corpus.v1.json` (the four initial states `G24.nt1.wrong-pack-identity`, `G24.nt1.user-pack`, `G24.nt1.third-party-pack` and `G24.nt2.non-declarative-pack`);
- the build plan's gate routing (`implementation-boundaries-and-build-plan.md` line 1028: DR-G24, M2, `crates/evaluator/src/policy.rs`, `crates/host/src/configuration.rs`) and its M2 and M3 rows (lines 886 and 887);
- the module layout (`14-repository-and-module-layout.md` lines 364 and 478) and `13-evidence-workflows-and-product-contracts.md` §10 ("The preview accepts only its bundled cycle pack");
- the product contracts: admission-and-qualification §1 (external input versus host-generated layer), §1.1 (policy is "registered pack/waiver IDs"; "Both pack and waiver IDs require registry admission") and §5 items 1, 3 and 5; workflows-and-surfaces §5 (the closed `PolicyDocumentV2` DSL, the `POLICY.IMPERATIVE_KEY_REFUSED` classifier and the D9 table row "duplicate waiver / imperative policy key"); native-evidence's route row for an invalid capability request (the precedent for an unregistered id under external configuration); and `public-detail-registry.v1.json`;
- the accepted laws X5 r2 (items 1, 3 and 5) and 468 r5 item 6 (the termination vocabulary).

Items 1 to 5 and 7 to 9 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. r2 answers Grok X12 r1. RF-1: an imperative key in a bundled row is row 4, the host-invariant fault, and row 3 covers only a document the caller presents (items 6 and 7). RF-2: the claim that the registered `CONFIG.INVALID` detail already states the pack condition is withdrawn, and a remedy-text contract successor, X12-0, must precede X12b (item 7 and "Units after the law"). r1 bytes are preserved in PROPOSAL-r1.md. Not code. Library only: no CLI command is wired.

## Problem

DR-G24 requires that host admission refuse, before any evaluation, a pack identity that is not bundled, a user or third-party pack, and a pack or contribution that is not declarative-only.

At product fc7dce7 nothing does this:
- `crates/host/src/configuration.rs` does not exist.
- `crates/evaluator/src/policy.rs` (686 lines) has the portable glob predicate and three retained-input inspectors: `inspect_policy_program`, `inspect_evaluator_parameters` and `compile_plan_policy`. They check a Plan's `PolicyDocumentV2`, `WaiverSetV1` and compiled `RuleProgramV2` against the closed schema, the rule and atom laws (`POLICY.UNKNOWN_RULE`, `IMPORT.ABSENT_FOR_PREDICATE`) and the compilation join.
- No code reads `analysis-spec.policyPackIds`. The identity-v3 schema types it only as `Text`, and the synthetic corpus carries the value `"fixture"`.
- No code asks where a policy document came from. A closed-schema failure surfaces as a generic `GraphError`, never classified as an imperative key.
- No pack registry exists, bundled or otherwise.

The product contract leaves four things open for this gate:
- where "bundled" lives;
- how a pack version is spelled;
- what a pack's bytes are, given that DR-131 freezes the identity but not the rule IR;
- which existing codes carry each refusal.

## Decisions

1. **Scope: the M2 slice of `configuration.rs` is pack admission only (lead decision).** The layout gives `configuration.rs` the whole configuration resolver: layers, registry selections and provenance (line 478). Discovery and configuration belong to M3 (build plan line 887), and DR-G20 routes that file again at M5. X12 creates `configuration.rs` with one job, admitting the policy selection of an analysis request. Layer merge, discovery folding, waiver IDs, profiles, capabilities and the `resolvedConfigDigest` arrive with M3 in the same module.
   - `evaluator/policy.rs` gains the bundled pack registry, the declarative-only content law and the retained Plan join (items 2, 6 and 8), all pure.
   - **Rejected:** building the full Config2 resolver now. It would pull M3 discovery and layer custody into M2 for a gate that needs only the policy selection.
   - **Rejected:** a separate `packs.rs`. The layout names exactly these two owners for DR-G24, and a third file would split one admission boundary.

2. **"Bundled" means compiled into the signed core (lead decision).** The bundled registry is `crates/evaluator/src/pack-registry.json`, included with `include_bytes!` exactly like `atom-registry.json` and `import-registry.json`. Its rows are `{packId, name, version, policyDocument, policySha256, contributions[]}`, where:
   - `policyDocument` is a sibling file, also included with `include_bytes!`;
   - `policySha256` is the raw SHA-256 of its canonical bytes, which is the digest `plan.policyDigest` names (workflows-and-surfaces §5);
   - `contributions` is the closed set of `ruleProgramRef.contributionId` values that pack's rules may name.

   No pack is read at run time from the project, the installation, the account, an environment variable, a flag or the network. Admission against the registry is the only admission (admission-and-qualification §5 item 1: "Unknown contributions refuse through the closed registry; declaring an id does not establish trust").

   **Rejected:** rows in the authenticated release declaration registry. Its published schema (`ReleaseCapabilityRegistryV1`) has capability rows only. Pack rows there would need a contract successor and would add an authenticated-input trust path for content that the signed core can carry itself.

3. **Identity spelling: `name:version` (lead decision).** A pack ID is the exact string `<name>:<version>`, where:
   - `name` is the registry row's name;
   - `version` is the row's version in decimal, with no sign and no leading zero.

   The DR-131 pack is `opensip.preview.typescript.pack:1`. This spelling satisfies both carriers that already hold pack IDs: product-configuration v2 `policy.packIds` (pattern `^[a-z][a-z0-9._:-]*(?![\s\S])`) and identity-v3 `analysis-spec.policyPackIds` (`Text`). So no schema changes.

   Matching is byte-exact against `packId`, with no normalization. Each of the following is not a registered ID:
   - a bare name;
   - `:01`;
   - an uppercase letter;
   - surrounding or trailing whitespace, including a final newline.

   Name and version enter PlanId through the existing `analysisSpecDigest`, and the content enters through the existing `policyDigest`. That satisfies DR-131's `planIdMembership` without inventing a producing rule.

   **Rejected:** name-only IDs. NT-1's "wrong version" limb could not be expressed, and a content change could keep the same ID.

   **Rejected:** a structured `{name, version}` field. It would need schema successors to product-configuration v2 and identity-v3 for no extra guarantee.

4. **Content and the M2 registry state (lead decision).** A pack's content is one `PolicyDocumentV2`, the closed declarative DSL (workflows-and-surfaces §5). DR-131 does not freeze the preview pack's rule IR (`$.pack.notFrozenHere`). The atom registry has no relation that expresses a module import cycle. So the preview pack's rule bytes cannot be authored in M2 without inventing IR.

   The release registry at X12a therefore has **zero rows**, and in M2 every named pack is refused as not bundled. That is lawful: nothing can reach analysis before M3 (X11 ends on the existing not-implemented refusal). The DR-131 row arrives with its content in unit X12c (see "Units after the law").

   Tests use a separate registry compiled only under `cfg(test)`. It has one synthetic row, `opensip.test.fixture.pack:1`, whose document is drawn from the existing `plan-policy-fixtures.json` corpus and labelled synthetic (build plan line 886). A source pin shows that the release build contains no test row and that no production path can select the test registry.

   **Rejected:** shipping the DR-131 identity row with placeholder content, or with no content. That is a bundled identity with nothing bundled behind it.

   **Rejected:** inventing a cycle atom or relation to author the rule now. That is the rule IR DR-131 leaves open.

5. **One inert request and one opaque result (lead decision).** The boundary input is inert and claims nothing:

   `enum PackSource<'a> { Named(&'a str), Supplied { bytes: &'a [u8], provenance: SuppliedProvenance } }`, with `SuppliedProvenance { User, ThirdParty }`.

   `Supplied` exists only to be refused, with a recorded refusal. It models a policy document found in the project, named by a flag or offered by a component. There is no admission path for supplied bytes: a user-authored policy's admission keeps its scope re-entry requirement (`13-…` §10). Without the variant, NT-1's second limb and NT-2 could not be presented at the boundary, and their refusal would leave no evidence.

   The functions are:
   - **Evaluator:** `policy::admit_pack(source: &PackSource<'_>) -> Result<AdmittedPack, PackRefusal>`. `AdmittedPack` has private fields: the row's `packId`, the policy digest, and the compiled `RuleProgramV2` and its digest. It has no `Default`, no `Clone`, no deserialization and no public constructor, and a `compile_fail` doctest guards against forging it.
   - **Host:** `configuration::admit_policy_selection(selection: &[PackSource<'_>]) -> Result<AdmittedPack, PolicySelectionRefusal>`, `pub(crate)`. It returns the evaluator's own type unchanged.

   **Rejected:** a host wrapper type, for X5 item 2's reason: a second unforgeable-looking type with no extra guarantee.

6. **The declarative-only law.** Every document presented to `admit_pack` goes through the same ordered checks. The first failure ends admission.
   1. **Lexical and canonical admission.** The existing identity `parse_json`: duplicate keys, number tokens, depth and size.
   2. **The imperative classifier.** This is workflows-and-surfaces §5's rule, applied exactly. A member that no closed `PolicyDocumentV2` alternative declares at its position, or a string where every closed alternative at that position is an object (a string expression), is `POLICY.IMPERATIVE_KEY_REFUSED`. Its subject is the JSON Pointer of the first such member in canonical order. This covers `script`, `hook`, `exec` and `include` keys, and a string `emitWhen`.
   3. **Closed-schema validation** against `#/$defs/PolicyDocumentV2`. Any other shape failure, including a `schemaMajor` other than 2, is `CONFIG.INVALID`.

   After these checks a `Supplied` source is refused, whatever its bytes (item 7, row 2). That includes the exact bytes of a bundled pack: admission is by identity only. A `Named` source continues:

   4. **Registry match** (item 3), otherwise not bundled.
   5. **Bundled bytes and digest.** The bundled document's canonical bytes hash to the row's `policySha256`.
   6. **Rule and atom law.** The existing `check_program_laws` over the policy and its compiled program, which gives `POLICY.UNKNOWN_RULE` or `IMPORT.ABSENT_FOR_PREDICATE`.
   7. **The contribution law.** Every rule's `ruleProgramRef.contributionId` is a member of the row's `contributions`. Otherwise the detail is `POLICY.UNKNOWN_RULE`.

   A contribution is admissible only as a rule row of a bundled document that names a registered contribution. An executable, a script, WASM or a component closure offered as a pack or contribution has no carrier at this boundary. It can arrive only as `Supplied` bytes, and it is refused at step 1, 2 or 3 or after step 3 (admission-and-qualification §5 items 3 to 5).

   Steps 4 to 7 run on bundled bytes. For a `Named` source, the document checked at steps 1 to 3 is the bundled document, not caller input. So a failure of a `Named` source at step 1, 2, 3, 5, 6 or 7 is a defect in the signed core, not bad input (item 7, row 4; r2, RF-1). Only a step 4 failure (an unregistered ID) is the caller's. A unit test also runs steps 1 to 7 over every release row, so a defective row cannot ship.

7. **Refusal rows (existing codes only).** The admission contract governs these rows: "Invalid external input is an admission rejection with the existing carrier's D9 code; an invalid host-generated internal layer is a host invariant fault" (admission-and-qualification §1). Every refusal maps by an exhaustive match with no wildcard arm into 468 r5 item 6's termination shape:

   | # | Situation | Class / exit | Code / fault | Detail | Subject |
   |---|---|---|---|---|---|
   | 1 | A `Named` ID not in the bundled registry: wrong name, wrong version, unversioned, non-canonical spelling, or (in M2) any ID; or a selection of zero, or more than one, sources | request-rejected / 2 | `CONFIG.INVALID` / none | `CONFIG.INVALID` | the presented ID, or `count:<n>` |
   | 2 | A `Supplied` pack that passes items 6.1 to 6.3 | request-rejected / 2 | `CONFIG.INVALID` / none | `CONFIG.INVALID` | `supplied:<user\|third-party>:sha256:<hex>` |
   | 3 | A `Supplied` source (a document the caller presents) failing item 6.2 | request-rejected / 2 | `CONFIG.INVALID` / none | `POLICY.IMPERATIVE_KEY_REFUSED` | the member's JSON Pointer |
   | 3a | A `Supplied` source failing item 6.1 or 6.3 | request-rejected / 2 | `CONFIG.INVALID` / none | `CONFIG.INVALID` | `supplied:<provenance>:sha256:<hex>` |
   | 4 | A bundled row failing item 6.1, 6.2, 6.3, 6.5, 6.6 or 6.7, a self-inconsistent registry, or a traversal limit | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / `host-invariant` | `HOST.INVARIANT_VIOLATED` | `pack:<packId>` |

   - **Row 1** follows the native precedent exactly: an invalid capability request under external configuration is request-rejected 2, `CONFIG.INVALID`, detail `CONFIG.INVALID`. Row 3 is workflows-and-surfaces' "duplicate waiver / imperative policy key" row.
   - **Registry rows.** All five codes have rows in `public-detail-registry.v1.json`: `CONFIG.INVALID`, `HOST.INVARIANT_VIOLATED`, `POLICY.IMPERATIVE_KEY_REFUSED`, `POLICY.UNKNOWN_RULE` and `IMPORT.ABSENT_FOR_PREDICATE`. The D9 error codes and fault cause are members of the generated `Common4D9ErrorCode` and `Common4D9FaultCause`. **No new code is added.**
   - **Row 3 is for caller documents only (r2, RF-1).** Its detail carries the caller remedy "the policy DSL is declarative data only". An imperative member in a bundled document is signed-core bytes, an invalid host-generated layer under admission-and-qualification §1, so it is row 4 with subject `pack:<packId>`, like any other bundled defect. The release self-check of item 10 still refuses to ship such a row.
   - **Remedy keying (r2, RF-2).** The published remedy `PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]` (`native/native_evidence_model.v2.py`) is the capability-selection string: "the configured capability selection is invalid: name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot)". native-evidence's remedy-keying constraint keys that table by public code, so one string must stay true for every key that reaches the code. As published, that string is not a true next step for rows 1, 2 and 3a, which are an unregistered pack ID, a supplied pack and a selection count.
     - The remedy-text contract successor **X12-0** widens that one string so it stays true for the existing capability keys and for these pack rows.
     - Its content is fixed by X12-0's own review. It must say three things in substance: name a registered capability id and state at most one row per (capabilityId, languageMode, workspaceRoot); name exactly one bundled policy pack id; supply no policy document of your own.
     - X12-0 precedes X12b. No row 1, 2 or 3a is emitted before it lands.
     - The public code stays `CONFIG.INVALID`. No code is minted.
   - **Traversal limits.** These are named constants sized to the DSL's own bounds (512 rules, 64 nodes, depth 8), so a document that passes the schema never reaches a limit. A limit is therefore row 4.

   **Rejected:** minting `POLICY.PACK_UNREGISTERED` or `PACK.NOT_BUNDLED`. The native route already uses `CONFIG.INVALID` for an id the closed registry does not admit under external configuration. The remedy-keying constraint allows a new key to reuse a code when its author widens the code's remedy so the one string is true for every key, and that is X12-0. A new detail would add a public code for a condition the existing code covers once its remedy is widened.

8. **Order: pure, and before everything (lead decision).** Pack admission does no I/O, takes no lock and is not charged to any ledger. The host runs `admit_policy_selection` first in an analysis request, before:
   - X1 write admission, X2 project admission or any fence;
   - any provider spawn, snapshot or semantic-universe construction;
   - consuming facts or Coverage;
   - Plan construction;
   - any evaluation.

   A refusal therefore leaves the record DR-G24 asks for: no core evaluation, no `policyOutcome`, no facts or Coverage consumption and no semantic universe. It has nothing to clean up.

   The future M3 Plan builder takes the policy only from an `AdmittedPack`. It writes `analysis-spec.policyPackIds = [packId]` and `plan.policyDigest` from it, never from a configuration string or a file.

   **Correction to EXIT-PLAN.** X12 does not depend on X1: it is pure and runs before any custody. Its only dependency is the current product.

   **Rejected:** admitting packs inside Plan construction. Plan construction already sits behind snapshot and provider work, so a refused pack would cost those effects and blur "refusal before evaluation".

9. **The retained Plan join is provided, not yet wired into replay (lead decision).** `policy::check_plan_pack(inputs: &RetainedInputs<'_>, plan_id: &str, budget: TraversalBudget)` is a pure function. It requires that:
   - the retained analysis-spec's `policyPackIds` is exactly one bundled `packId`;
   - `plan.policyDigest` equals that row's `policySha256`.

   Over a Plan the host has just built, a mismatch is row 4. Over a retained candidate it is X5 item 5's structural row, `EVALUATION.INPUT_REFUSED`.

   X12 does not insert `check_plan_pack` into `replay_run` or into X5's `replay_candidate`. The existing replay corpus is synthetic and labelled. Its Plans name `"fixture"` and carry policies from no pack, so the join would refuse the whole corpus and X3d's and X5's tests with it. Corpus regeneration belongs with the M3 Plan builder, the first producer of real Plans.

   Until M3 no analysis producer exists, so no real Run with a non-pack policy can reach X5. The Run-closure join is an M3 obligation (X12d), and it must land before any analysis producer is wired.

   **Rejected:** wiring the join into replay now and regenerating the synthetic corpus in M2. That rebuilds fixtures for a producer that does not exist yet, and it reopens X5's accepted tests.

10. **Tests.**
    - **NT-1, first limb** (`G24.nt1.wrong-pack-identity`), all row 1 with the presented ID as subject:
      - a wrong name;
      - `opensip.preview.typescript.pack:2`;
      - the bare name;
      - `:01`;
      - an uppercase variant;
      - a trailing newline;
      - in the release registry, `opensip.preview.typescript.pack:1` itself (not bundled in M2).
    - **NT-1, second limb** (`G24.nt1.user-pack`, `G24.nt1.third-party-pack`): `Supplied` sources of both provenances, one of them byte-identical to the test pack's bundled document, are row 2.
    - **NT-2** (`G24.nt2.non-declarative-pack`):
      - `Supplied` documents with top-level and in-rule `script`, `hook`, `exec` and `include` members, and with a string `emitWhen`, are row 3 with the pointer;
      - a non-JSON blob offered as a component contribution is row 3a.
    - **Selection count:** a selection of zero sources, and one of two, is row 1.
    - **Positive case:** under the `cfg(test)` registry, `opensip.test.fixture.pack:1` admits, and its digest equals `policySha256`.
    - **Bundled defects:** a `cfg(test)` registry with a digest mismatch, an unregistered contribution, a rule-law failure or an imperative member (an `exec` key in a rule) gives row 4, subject `pack:<packId>`, never row 3 (RF-1).
    - **Remedy:** the `CONFIG.INVALID` remedy emitted on rows 1, 2 and 3a is the X12-0 string, byte for byte (RF-2).
    - **Release registry self-check:** every release row passes item 6, and in M2 there are zero release rows.
    - **No evaluation:** source pins show that `configuration.rs` calls only `policy::admit_pack`, and that the refusal paths reach no evaluation, provider, facts, Coverage or custody call. A refusal returns before any `AdmittedPack` exists, and nothing downstream accepts anything else.
    - **`check_plan_pack`:** a corpus Plan naming `"fixture"` is refused; a test-pack Plan with the matching digest admits; and a test-pack Plan with any other policy digest is refused.
    - **Exhaustive mapping:** the termination mapping is exhaustive, and every row's code parses as its generated enum member.

## Units after the law

- **X12-0, contract successor (remedy text, RF-2).** Widens the one `PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]` string in `native/native_evidence_model.v2.py` and every published copy of that remedy, so it stays true for the existing capability keys (`native.requested-capability-unregistered`, `-mode-unregistered` and `-duplicate-ownership-tuple`) and for item 7's rows 1, 2 and 3a. The public code stays `CONFIG.INVALID`, and no detail or alias is added. It is reviewed on its own. It depends on nothing, and it precedes X12b.
- **X12a (evaluator), inventory successor.** Covers items 2 to 7 and 9:
  - `pack-registry.json`, with zero release rows, and the `cfg(test)` registry;
  - `PackSource`, `AdmittedPack`, `admit_pack` and the imperative classifier;
  - `check_plan_pack`;
  - the evaluator tests of item 10.

  It depends on nothing beyond fc7dce7.
- **X12b (host), inventory successor.** Covers items 1, 5, 7 and 8:
  - `crates/host/src/configuration.rs` with `admit_policy_selection`;
  - the termination mapping into 468 r5 item 6's shape;
  - emitting the X12-0 remedy on rows 1, 2 and 3a;
  - the host tests.

  It depends on X12a and X12-0.
- **X12c (M3), contract successor.** The DR-131 pack row `opensip.preview.typescript.pack:1` and its bundled bytes. It needs the preview rule IR frozen. If the import-cycle rule needs a relation or atom that the atom registry and `PolicyDocumentV2` do not have, that is a policy-language contract successor, owned by DR-131's execution remainder, before the row can ship. It is not M2 work.
- **X12d (M3), inventory successor.** The Run-closure application of `check_plan_pack` inside replay, and regeneration of the synthetic replay corpus onto the bundled test pack, with the M3 Plan builder (item 9). It must land before any analysis producer can reach X5.
- **No public-code contract successor is needed** (item 7). The only contract successor is X12-0's remedy text.
- **EXIT-PLAN corrections:** X12 depends on nothing (item 8), and the X12 row should read "LAW r2 PROPOSED (policy-admission-x12); units X12-0 (remedy text), X12a, X12b; X12c and X12d at M3".

## Forbidden substitutes

- **Bundling:**
  - a pack, policy or registry read at run time from the project, installation, account, environment, flag or network;
  - a pack registry row in the release declaration registry;
  - a placeholder or contentless row;
  - a `cfg(test)` row or test registry reachable from a release build.
- **Identity:**
  - normalizing a pack ID (case, whitespace, leading zeros, a missing version);
  - a name-only match;
  - admission by digest or bytes instead of by identity;
  - admitting a `Supplied` source for any bytes, including the bundled pack's bytes.
- **Declarativeness:**
  - an imperative member or string expression surfacing as anything but `POLICY.IMPERATIVE_KEY_REFUSED`;
  - a contribution outside the row's set;
  - a script, hook, WASM or component closure as a pack contribution.
- **Order:**
  - admitting packs after any provider spawn, snapshot, facts consumption or evaluation;
  - a Plan whose `policyPackIds` or `policyDigest` did not come from an `AdmittedPack`;
  - more than one pack, or a merged policy.
- **Types and codes:**
  - a host wrapper around `AdmittedPack`;
  - a boolean or string standing in for admission;
  - a silent admission, or a waiver of a refusal;
  - a new public code;
  - an imperative member of a bundled document surfacing as row 3;
  - emitting row 1, 2 or 3a before X12-0 lands.

## Not claimed

- **DR-G24 qualification** (M6), and authored, digest-pinned G24 fixture bytes on the D-002 platforms. The tests of item 10 are library tests over synthetic inputs, not the harness.
- **The DR-131 pack's rule and content** (X12c), and the Run-closure join in replay (X12d).
- **The rest of the configuration resolver:** layer merge, discovery, profiles, capabilities, waiver IDs and `resolvedConfigDigest` (M3), and DR-G20 (M5).
- **Policy commands:** `policy show`, `init` and `test` and `waive` (M5), and admission of any user-authored policy, which keeps its scope re-entry requirement.
- **Excluded forms:** third-party publisher-form refusal (G29), useful-install advertisement (G30), and FactCandidate and Coverage admission (G23).
- **CLI enablement.**

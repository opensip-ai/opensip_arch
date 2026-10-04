# Configuration and policy-pack admission — proposal X12 r4

2026-10-01. Claude Opus 5.5, implementation lead. Law for unit X12 of `EXIT-PLAN.md`, release gate DR-G24 PREVIEW-ANALYZE-WELL-FORMED-ADMISSION. X5 r1 split this gate out of X5 (`replay-join-x5/PROPOSAL.md` item 1, "Correction to EXIT-PLAN"). The governing documents are:
- the register's DR-G24 row (`08-decision-and-readiness-register.md` line 369: "Host admission of preview analyze requests refuses a non-bundled pack identity and a non-declarative pack or contribution"; retained evidence "pack-identity refusal before evaluation; imperative-pack refusal; no user or third-party pack"; "no waiver for silent admission"), and DR-131 (line 320, SATISFIED at D-369);
- the DR-131 contract `docs/coop/artifacts/preview-analyze-contract.v2.json`: `$.pack` (`opensip.preview.typescript.pack`, version 1, "Exactly one pack. Host-owned. Bundled. First-party. Declarative-only. … No user packs. No third-party packs.", rule IR not frozen), `$.planIdMembership`, and `$.negativeTests` NT-1 and NT-2;
- the G24 harness occupancy `harness.DR-G24.preview-analyze-well-formed-admission.preview.v3.json` and `g24-input-corpus.v1.json` (the four initial states `G24.nt1.wrong-pack-identity`, `G24.nt1.user-pack`, `G24.nt1.third-party-pack` and `G24.nt2.non-declarative-pack`);
- the build plan's gate routing (`implementation-boundaries-and-build-plan.md` line 1028: DR-G24, M2, `crates/evaluator/src/policy.rs`, `crates/host/src/configuration.rs`) and its M2 and M3 rows (lines 886 and 887);
- the module layout (`14-repository-and-module-layout.md` lines 364 and 478) and `13-evidence-workflows-and-product-contracts.md` §10 ("The preview accepts only its bundled cycle pack");
- the product contracts: admission-and-qualification §1 (external input versus host-generated layer), §1.1 (policy is "registered pack/waiver IDs"; "Both pack and waiver IDs require registry admission") and §5 items 1, 3 and 5; workflows-and-surfaces §5 (the closed `PolicyDocumentV2` DSL, the `POLICY.IMPERATIVE_KEY_REFUSED` classifier and the D9 table row "duplicate waiver / imperative policy key"); native-evidence's route row for an invalid capability request (the precedent for an unregistered id under external configuration); and `public-detail-registry.v1.json`;
- the accepted laws X5 r2 (items 1, 3 and 5) and 468 r5 item 6 (the termination vocabulary).

Items 1 to 5 and 7 to 9 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. r2 answers Grok X12 r1. RF-1: an imperative key in a bundled row is row 4, the host-invariant fault, and row 3 covers only a document the caller presents (items 6 and 7). RF-2: the claim that the registered `CONFIG.INVALID` detail already states the pack condition is withdrawn, and a remedy-text contract successor, X12-0, must precede X12b (item 7 and "Units after the law"). r1 bytes are preserved in PROPOSAL-r1.md. r3 answers Grok X12 r2 RF-1: the declarativeness prohibition is scoped to a document the caller presents; a bundled imperative member surfaces as row 4. r2 bytes are preserved in PROPOSAL-r2.md. r3 ACCEPTED by Grok on 2026-10-01. Not code. Library only: no CLI command is wired.

**r4 (2026-10-04) is an amendment made as lead decisions under the owner's standing direction of 2026-09-30.** r3 bytes are preserved in PROPOSAL-r3.md (sha256 `11628912…`, the subject Grok accepted in `reviews/grok-policy-admission-x12-r3`).

- **Where it comes from.** The accepted M3 law **M3-B r2**, configuration and discovery (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`). GROK2 accepted it on 2026-10-04 (`docs/implementation/m3/reviews/grok2-config-discovery-b-r2`, subject `92e65825…`, preserved as `PROPOSAL-r2.md`).
  - M3-B item 25 names this amendment as its successor S2, and M3-B item 10 gives S2's exact text. r4 carries that text and adds one lead decision to it: the first-use clause, with the dependents its withdrawal record names (below). M3-B item 10's own text is not changed; the addition is this law's.
  - GROK2's r1 finding RF-2 on M3-B shaped the withdrawal record (`docs/implementation/m3/reviews/grok2-config-discovery-b-r1`).
- **Why the order must change** (M3-B "Problem" and item 10). A pack ID can come from the project layer of the configuration, Config2's `policy.packIds` (admission-and-qualification §1.1, AQ:47-52). The project carrier is located and custody-judged only by S3's selection walk, which X2 runs charged and under the fence (X2:68, X2:74). So pack admission cannot run before every fence, as r3's item 8 required.
- **No product code changed.** `admit_policy_selection` has no caller yet (X11 r1). M3-B's unit B1-a places its caller in r4's order (M3-B item 25: S2 lands with B1-a).
- **How it edits r3.** S2's text replaces r3 item 8's opening paragraph and its five bullets (X12:125-130), where they stood. The lead decision adds two passages inside it, each marked "r4, lead decision": the first-use clause, after S2's first paragraph, and the dependents, at the end of the withdrawal record. X12:136 keeps its words and is followed by a short "r4" note. Nothing else is edited.

It changes the following and nothing else.

- **Item 8's order.** Pack admission stays pure: no I/O, no lock and no ledger charge.
  - It now runs immediately after configuration resolution, which runs immediately after S3's selection walk and the configuration carrier captures.
  - It runs before X2's registry capture and every later step of project admission, before any effect, and before everything r3 listed after the fence.
  - It may follow the fence acquisition, the selection walk and the carrier reads, which write nothing.
- **The first-use clause (lead decision; below).** On the first-use creator route, "before any effect" reads "before any project-scoped effect".
- **The withdrawal record** (in item 8). r4's order supersedes r3's "before … X1 write admission, X2 project admission or any fence" (X12:126) and the ordering sense of X12:136. It withdraws the clause "the order" from M3-I1 r2 item 7's "Everything else in X12 r3 stands" (I1:388). By the lead decision, it also supersedes two dependents: X11 r1 item 1a and I1:404.
- **X12:136's reading.** "it is pure and runs before any custody" now means that admission itself performs no custody, because S3's selection judgment precedes it. Its correction that X12 does not depend on X1 stands.

**Lead decision: first use (r4, under the owner's standing direction of 2026-09-30).** It was found while drafting r4.
- **The gap.** S2 lets pack admission follow "the fence acquisition of the 458c read session or of the 468/X1 write gate", and requires it "before any effect".
  - On first use, 468 r5 item 1 has the creator publish the installation before the invocation continues through the 468 gate with a fresh fence.
  - The project carrier can be read only after that fence and S3's selection walk.
  - So on the first-use creator route, S2's literal order cannot be met.
- **Decision.** On that route, "before any effect" reads "before any project-scoped effect".
  - The creator's installation effects come first, then pack admission, then every project-scoped effect: registration (X2 item 6), any lease (X2 item 7), the project ledger and journal, and every later project effect.
  - A refused pack on first use leaves an empty, valid installation and no project effect. This is disclosed in the refusal and is never hidden.
  - On every other route, S2's "before any effect" stands as written.
- **Rejected:** reading the project configuration before its custody judgment, so that pack admission could precede the creator. It would break X2 r9 item 3a, which reads each carrier only from the descriptor S3's selection judged under the fence.
- **Dependents.** The withdrawal record names two dependents that S2 supersedes:
  - **X11 r1 item 1a** rejected "creating I first" on r3's order. That conflict is routed to the X11 successor that M3-J1 owns. X11's M2 decision does not rest on item 1a alone: X11 calls its four reasons "each sufficient on its own".
  - **I1:404**, "J2 calls `admit_policy_selection` first (X12:125-132)". J2 calls it in r4's order.
- **Not law, so not withdrawn here.** Row 1 of the order table in M3-C's draft (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`) still carries r3's order. It is a dependent to update in M3-C's next revision.
- **Control** (the X11 successor's, M3-J1). On first use, a refused project-layer pack ID leaves:
  - a complete installation;
  - no registry row, namespace, `.opensip`, marker, lease or journal;
  - the refusal's disclosure of the creation.

**What stands** (M3-B item 10):
- the rest of item 8 (X12:132-138), including the rule that the Plan builder takes the policy only from an `AdmittedPack` (X12:134), "nothing to clean up" (X12:132) and the rejection of admission inside Plan construction (X12:138);
- item 8's rule that admission is pure, with no I/O, no lock and no ledger charge (X12:125);
- everything else in r3: rows 1 to 4, the `Supplied` refusal of bundled bytes, the `cfg(test)` registry, `check_plan_pack` and X12d;
- of M3-I1 r2's amendments to X12 r3 (I1:381-388): the three row-count changes (I1:383-386), and I1:388's other clauses (rows 1 to 4, the `Supplied` refusal, the `cfg(test)` registry, `check_plan_pack` and X12d).

**Basis** (M3-B item 10). The pack ID can come from the project layer (AQ:47-52, the `policy` section). The project carrier is located and judged only by the selection walk, which runs under the fence (X2:68, X2:74). X12's rationale still holds: a refusal leaves DR-G24's record, with no evaluation, no `policyOutcome`, no facts or Coverage and no universe, and "nothing to clean up" (X12:132). Selection and the carrier reads write nothing, and dropping the session releases the fence. GROK2's r1 review of M3-B checked this (its R2): `ObservationSession::begin` and `DurableWriteGate::begin` write no registry row, RESERVED document, lease or journal.

**Rejected** (M3-B item 10):
- **Reading the carriers before the fence.** That reverses X2's charged, fenced selection (X2:68) and opens a gap between the read and the fenced admission.
- **Allowing policy selection only from defaults and flags.** It contradicts Config2's project-level `policy.packIds` (AQ:47-52).
- **Admitting twice,** once before the fence for flags and once after selection. It doubles the path and needs the same amendment anyway.

**Controls** (M3-B item 10; B1-a's test). For a refused project-layer pack ID: no registry read, no RESERVED row, no lease, no journal, the session released, and X12 row 1 returned.

**Reconciliations with r3's text.** Each one states how S2's text reads in this law. None changes S2's words.
- **Format.** S2 writes item 8's number inside its bold heading (`**8. Order: …**`). r4 writes it as this law's list marker (`8. **Order: …**`), so item 8 stays the eighth item of the list. The "Withdrawal recorded" paragraph is indented as part of item 8. Apart from the two passages marked "r4, lead decision", every word of item 8's opening is as M3-B item 10 gives it.
- **Names in S2's text.**
  - "S3" is the security contract's S3 (discovery and custody), not M3-B's successor S3.
  - In "(registration, item 6; any lease, item 7)", the items are X2's, as the preceding "X2 item 5" says. They are not this law's items 6 and 7.
  - "I1" is M3-I1 r2 (`docs/implementation/m3/preview-pack-i1/PROPOSAL.md`), and I1:NNN are its live lines.
- **X12:132 follows S2's last sentence.** S2's paragraph ends "A refusal therefore still leaves the record DR-G24 asks for and has nothing to clean up", and X12:132 then states that record in full. M3-B item 10 keeps both.
- **M3-I1's amendments live in I1.** I1 r2 item 7 amended r3 for M3 by statement, without revising this file. Item 4's "zero rows" (X12:67) and item 10's two release-row sentences (X12:160, X12:169) change when unit I1-c lands.
  - r4 does not restate them. They stand, and they read on r4's text, which is identical at those places.
  - I1's file is not edited. S2 records the withdrawal of I1:388's "the order" here, in item 8.
- **Item 10's source pin.** X12:170 requires that the refusal paths "reach no evaluation, provider, facts, Coverage or custody call". That stays true. Admission itself performs no custody (X12:136's reading), and the custody that precedes it is not on its refusal path.
- **Forbidden substitutes.** The "Order" bullets stand and stay true. M3-B item 10's own forbidden substitute, "pack admission after any registry capture, registration, lease or effect", is r4's item 8 read negatively. On the first-use creator route, "effect" there means a project-scoped effect. r4 adds no bullet for it.
- **X2 r9's order.** X2 r9 item 3a (a lead decision) runs X2 item 2's placement check and item 3's chain walk after S3's selection walk and before the carrier reads. S2's "immediately after S3's selection walk and the configuration carrier captures" therefore reads as immediately after the captures, which follow those two checks. Both checks only read, under the fence.
- **Line citations.** Citations of the form X12:NNN, in M3-B, in M3-I1, in other laws and in r4's own text, are to r3's lines, preserved in PROPOSAL-r3.md. This file's lines move with r4's header.

**Unchanged from r3:** everything else. That includes items 1 to 7, 9 and 10, the rest of item 8, the units after the law, the forbidden substitutes and "Not claimed". No public code, row, detail or remedy changes.

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

8. **Order: pure, and before every effect (X12 r4, by M3-B item 10).** Pack admission does no I/O, takes no lock and is not charged to any ledger. The host runs `admit_policy_selection` immediately after configuration resolution, which runs immediately after S3's selection walk and the configuration carrier captures. It runs before X2's registry capture (X2 item 5) and every later step of project admission (registration, item 6; any lease, item 7), before any effect, and before any provider spawn, snapshot or semantic-universe construction, consumption of facts or Coverage, Plan construction and evaluation. It may follow the fence acquisition of the 458c read session or of the 468/X1 write gate, the selection walk and the carrier reads, all of which write nothing. A refusal therefore still leaves the record DR-G24 asks for and has nothing to clean up.

   **First use (r4, lead decision; see the r4 header).** On the first-use creator route (468 r5 item 1), "before any effect" reads "before any project-scoped effect".
   - The creator's installation effects come first. The invocation then continues through the 468 gate, and pack admission follows the selection walk, the carrier captures and configuration resolution as above.
   - Pack admission precedes every project-scoped effect: registration (X2 item 6), any lease (X2 item 7), the project ledger and journal, and every later project effect.
   - A refused pack on first use leaves an empty, valid installation and no project effect. This is disclosed in the refusal and is never hidden. 464 item 3's first-write disclosure has already preceded the installation effects.

   **Withdrawal recorded.** This r4 order supersedes X12 r3 item 8's "before … X1 write admission, X2 project admission or any fence" (X12:126) and the ordering sense of X12:136's "runs before any custody". It also **withdraws the clause "the order" from M3-I1 r2 item 7's statement that "Everything else in X12 r3 stands"** (I1:388). The rest of I1:388's list, and I1:383-386, stand. **Dependents (r4, lead decision).** This order also supersedes two dependents that rest on r3's order:
   - X11 r1 item 1a, which rejected "creating I first" because it "would break item 8's order". Its reconciliation with the first-use clause is routed to the X11 successor that M3-J1 owns.
   - I1:404, "J2 calls `admit_policy_selection` first (X12:125-132)". J2 calls it in this order.

   A refusal therefore leaves the record DR-G24 asks for: no core evaluation, no `policyOutcome`, no facts or Coverage consumption and no semantic universe. It has nothing to clean up.

   The future M3 Plan builder takes the policy only from an `AdmittedPack`. It writes `analysis-spec.policyPackIds = [packId]` and `plan.policyDigest` from it, never from a configuration string or a file.

   **Correction to EXIT-PLAN.** X12 does not depend on X1: it is pure and runs before any custody. Its only dependency is the current product. **r4:** "it is pure and runs before any custody" now means that admission itself performs no custody, because S3's selection judgment precedes it. Its ordering sense is superseded by the order above. The correction that X12 does not depend on X1 stands (M3-B item 10; see the r4 header).

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
  - an imperative member or string expression in a document the caller presents surfacing as anything but row 3 (`POLICY.IMPERATIVE_KEY_REFUSED`, with the member's pointer); a bundled imperative member surfaces as row 4;
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

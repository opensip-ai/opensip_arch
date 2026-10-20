# D4 implementation plan r1: manifest admission, request predicates and the session factory (M3-D items 24-26)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.**

**Bases:**
- product main `5de9fd4` (C2a-2 integrated at `1749259`, inventory v226 bound; 176 contract successors);
- architecture `dc96415fa` (inventory v226 recorded), and the files the subject manifest names.

**What precedes it.** D4's row in M3-D r5's units table is "`components/manifest.rs` at R10a, `components/session_factory.rs` and the `host/request.rs` predicates at R1: items 24-26", depending on D3a, SD-2 and SD-6 (met, r4), with "its own (a) check, not C2a (r5)", size M, control DR-G29 (`PROPOSAL-r5.md`:1262). The order is D1a → D2a ∥ D2b → D3a → D3b ∥ D4 → D5 (:1265).
- **Met:** D1a (`crates/platform/src/process.rs`); D2a (`crates/components/src/control_protocol.rs`); D3a-1 and D3a-2 (`crates/components/src/supervisor.rs`: `SessionSpec`, `PreSpawnRefusal`, `decline`); SD-2 (bound; the select tuple record); SD-5 (bound; row 56's route); SD-6 (J1 r4, R10a and ER10a); SD-7 (bound; row 57's NE row and the widened `PROVIDER.NOT_SELECTED` remedy); S19 (M3-C r7's row 8); CR-1 (bound at `3fe7eb5`) **and its materialization** (`d579140`, the "CR-1 component role materialization" unit, status record E033); C2a-1 (the trust owner's bridge, `trust_admitted_components.rs`) and C2a-2 (the shared signed fixtures of every role); J2a (R1's typed request, `crates/host/src/invocation.rs`).
- **Not met:** D3a-3 (in its lane; D4 needs nothing of it); D2b-3b and D2b-4 (the TS2 send side and the Rust3 codec, which the factory's Hello and identity inputs come from); CI-2 and CI-3 (the installed store and the retained-tree capability, which the factory's spawn recheck reads through); C4a (the Plan, whose universe rows the factory's expected identities come from); J3d and J2c (the R10a and ER10a wiring); and **R10a's production work profile**, which no accepted law selects (§4, X-D4P-1).

**Authority:**
- **The law:** M3-D r5 items 24-26 (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`:752-878, accepted by Grok `224b9228…`), with controls D4-T1 to D4-T4, the r4 and r5 changes tables (:24-46), items 2 and 12 for the recheck and the `Prepared` state (:204-222, :425), item 22's rows 28 and 30 (:714), and item 30's cross-law records (:1211-1216).
- **Its short names** (:94-140), cited as the law cites them: PPBS (v10), AQ, DR103, CD, CMS, NE, NES, NEM, SL, WS, J1, MC, CR-1, SD5, CH14, COV, QG, REG, BP.
- **J1 r7** (`host-pipeline-j/PROPOSAL-r7.md`), which supersedes the r4 bytes M3-D cites with the same rows: R1 (:382), R10a (:392, :404-416), ER10a (:493, :498), row 56 (:826), row 57 (:833), S20 (:914), J-C10b (:410-416) and J-C20 (:840).
- **The accepted plans** whose interfaces D4 meets: C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`: LD-C2A-1's order within R10a, :86-96; the Q5 ruling, :19; LD-C2A-10's scope, :168); the component installation law r5 (`component-install/PROPOSAL-r5.md`, item 6's retained-tree capability, :280-302, and item 7's pin, :304-312) and its plan r3; the D2b plan r3 with amendments A1 and A2 (`d2b/`; `DispatchContext`, LD-D2B-15); the D3a plan r4.
- **The product interfaces** on main `5de9fd4`:
  - **security** (`crates/security/src/component_manifest.rs`): `Validated` (:35-55) and its `closure_kind` (:41-50); `command_checks` (:180), with the one-root check (:192) and the root-name binding (:196); `name_checks` (:283), with the reserved-name check (:301) and the live-name check (:304); `validate` (:433) and `validate_inventory` (:436), both reaching the role-dispatched checks (:452-457). Since `d579140` the generated shape admits the four closure-only roles and refuses `commands` on each of them as `Schema`, in both entry points (`cr1_closure_commands_are_absent_and_analyzer_commands_required`, :752).
  - **the ordinary reader** (`trust_ordinary_metadata.rs`): the reserved list the manifests are validated against is the authenticated catalog's `reservedRootCommands` (:88); `provenance.publisher` must equal the verified envelope's namespace (:121-123).
  - **C2a-1's bridge** (`trust_admitted_components.rs`): `AuthenticatedComponent` (:13-62) lends the body, envelope, validated manifest, kind and release row, `pub(crate)`.
  - **platform:** `ClosureRecheck` (`process.rs`:335) and `VerifiedLaunch::from_recheck` (:346-358), whose only production caller must be D4's factory (LD-D1A-3); `WorkScope` and `WorkLedger` (`work_ledger.rs`), with the global caps (:12-14) and the discovery and snapshot profiles (:223, :242).
  - **components:** `SessionSpec {launch, selection, needs_d3b_ladders, memory_budget_bytes}` (`supervisor.rs`:723); `PreSpawnRefusal {ClosureRecheckFailed, SessionSpecInconsistent}` (:344); `Supervision::decline` (:1246); `AdmittedSelection` and `ControlContext::for_session` (`control_protocol.rs`:1020-1044); TS2's `DispatchContext` (`provider_protocol/ts2.rs`:100), "built by D4's session factory from the admitted Plan before spawn (no producer exists yet)".
  - **host:** R1's `AnalysisRequest`, `RequestFlags` and `AdmittedRequest::admit` (`invocation.rs`:31-127); the native capability matrix (`native_capability_matrix.v2.json`, embedded at `discovery.rs`:30).
  - **The package policy** permits `opensip-host → opensip-components` (inventory v226's `opensip-host` row). D4 adds that edge.

## 0. What D4 delivers, and what it does not

**Delivers:**
- **`components/manifest.rs`** (item 24): the manifest-class excluded-form predicates EE-1, EE-3b, EE-4's manifest part and EE-5a, with EE-5a's root-command predicate (a), (b) and (c), over a pure borrowed projection of security's validated value; the internal refusal `ExcludedForm {class, subject}`; the deterministic choice of the projected refusal among several; every check charged on the caller's borrowed `WorkScope`.
- **The R10a and ER10a lending** (item 24's inputs): the trust owner's public, read-only lend of each verified component's claim fields and the policy inputs it was validated against, and the host function that turns them into D4's projection and runs D4's checks. No caller in the request pipeline until J3d and J2c.
- **`host/request.rs`'s R1 classification** (item 25): the place where a request-class excluded form is judged, against M3's typed request, which has no carrier for any of the three forms (LD-D4-7).
- **`components/session_factory.rs`** (item 26): the session spec from an admitted selection, the spawn binding recheck through the closure owner's seam, and the two host-observed pre-spawn refusals. Library only; its production caller is J2b.

**Not delivered:**
- **The R10a and ER10a wiring** in the request pipeline: J3d's and J2c's, with C2a-4 (J1 S20, :914; C2a plan r4, :82). D4 supplies the function they call first (LD-C2A-1 step 2).
- **R10a's production work profile** (§4, X-D4P-1). D4 charges the caller's borrowed scope and selects no profile.
- **The public projections:** row 56 and row 57's envelopes, and the operational record of every `ExcludedForm`, are J1's projection through J2a (S20; LD-D4-9). D4 returns the internal refusals, all of them, in their order.
- **The provider-spoken substitution cases** of item 26 (the control `helloAck` echoes, HelloAck's identity and token echo, an `effectRequest`): D2a, D2b and D3a observe them. D4-T3's provider-spoken half runs once D2b-3b and D2b-4 exist (§1).
- **C2a's admission** (C2a-1, C2a-3), **MC row 8's selection** and **J2b's closure selection**.
- **Linux:** the factory's recheck and launch are D1a's macOS family only, as D1a is (LD-D1A-1).

## 1. The split (LD-D4-1): four sub-units, each its own review and lane

| Sub-unit | Content | Controls | Depends on |
| --- | --- | --- | --- |
| **D4-1** | `components/manifest.rs`: `ManifestClaims<'a>` and `AdmissionPolicy<'a>` (LD-D4-2); the four predicates (LD-D4-3 to LD-D4-6); `ExcludedForm`; the order and projected pair (LD-D4-8); the published prices (LD-D4-10) | D4-T4 at D4's interface; D4-T1's interface half (every class, two manifests, two classes, the order) | D3a (met) |
| **D4-2** | The lend and the host adapter: security's public `AdmittedComponentClaims` view over C2a-1's bridge, with the catalog's reserved list and the verified envelope namespace; host's `component_admission.rs`, which builds `AdmissionPolicy` and the claims and calls D4-1; the host → components edge | D4-T4's positive case and source pins on real signed fixtures of every role; EE-1 end to end on a signed `explicitly-trusted` fixture; the no-trust-view case | D4-1; C2a-1 and C2a-2 (met) |
| **D4-3** | `host/request.rs`: `request_excluded_form(&AdmittedRequest) -> Option<ExcludedForm>`, exhaustive over M3's typed request, and the closed-world pins (LD-D4-7) | D4-T2 as the record of an unrepresentable class (LD-D4-7) | D4-1 (the type); J2a (met) |
| **D4-4** | `components/session_factory.rs`: the spec, the recheck seam (LD-D4-11), the host-observed refusals; the host's recheck implementation over CI-3's capability | D4-T3's host-observed half; D5-S1's constructor pin for `VerifiedLaunch::from_recheck` | D4-1; D2b-3b; D2b-4 for Rust3; CI-3 and X-D4P-2 |

**Order:** D4-1, then D4-2 and D4-3 in either order, then D4-4.
- **Why four.** D4-1 is one pure module with no other crate touched. D4-2 crosses the security and host public surfaces and adds a package edge. D4-3 is a host-only R1 change. D4-4 waits on three units that are not built (D2b-3b, D2b-4, CI-3) and on X-D4P-2.
- **What D4 cannot claim without others.** D4-T1's path assertions (the reservation registry sampled at R10a's and ER10a's return, on paths 3a, 3b × {`Published`, `LostRace`, `NotPristine`} and the ephemeral path) are J1's J-C10b, "the placement half of M3D's D4-T1" (J1:410). They run when J3d and J2c wire R10a and ER10a. D4 records D4-T1 as **interface-complete, path-owed**, and never as complete (§5).

## 2. Lead decisions

- **LD-D4-1. The split** (§1).
- **LD-D4-2. D4 judges a pure borrowed projection, built by the host from security's value.** CH14:288 gives components no security dependency, and item 24 forbids "a second manifest parser in components" (:804). So `manifest.rs` defines:
  - **`ManifestClaims<'a>`:** `manifest_digest: [u8; 32]`; `role: Role` (`Analyzer`, `Toolchain`, `Stdlib`, `RustDevLlvm`, `Grammar`, DR103:891-897 as CMS materializes it); `name: &'a str`; `aliases: &'a [&'a str]`; `commands: Option<Commands<'a>>` (absent, or the tree's entries as `(name, parent: Option<&'a str>, aliases)`); `capabilities: &'a [CapabilityClaim<'a>]` (`capabilityId`, and `declarationData`'s `relation` and `rung`); `provenance: (publisher: &'a str, source_class: SourceClass)` with `SourceClass {FirstParty, ExplicitlyTrusted}` (CMS's closed enum);
  - **`AdmissionPolicy<'a>`:** `reserved_roots: &'a BTreeSet<String>`, the list the security owner validated against (`trust_ordinary_metadata.rs`:88); `matrix_relations: &'a BTreeSet<(String, String)>`, the native capability matrix's `(relation, rung)` pairs (LD-D4-4); `explicitly_trusted: &'a BTreeSet<String>`, the explicit-trust list (LD-D4-3).

  Neither type parses anything. The host builds both from security's validated value and the authenticated catalog (D4-2), never from manifest bytes. In tests, D4-1 builds claims directly, as CR-T8 presents a closure-only tree to D4 (:818).
- **LD-D4-3. EE-1: the publisher.** PPBS's input is a component "whose component publisher is not first-party and not on the explicit-trust list" (PPBS:670), and AQ:341 says the selected product has "one signed first-party component/recipe/schema registry" and "no … third-party publisher admission".
  - **What reaches D4.** The ordinary reader admits a manifest only when its `provenance.publisher` equals the verified envelope's namespace (`trust_ordinary_metadata.rs`:121-123). That namespace must be one the authenticated root delegates to the signing role (`verified_envelopes.rs`:71-72). So every value at R10a has a root-delegated publisher, and `sourceClass` is `first-party` or `explicitly-trusted` (CMS's closed enum).
  - **The decision.** D4 refuses `ExcludedForm {class: EE-1}` when `source_class` is `ExplicitlyTrusted` and `publisher` is not in `policy.explicitly_trusted`.
  - **No accepted law or product carrier defines an explicit-trust list at M3**, and AQ:341 excludes third-party publisher admission. So at M3 the host passes the **empty** list, and every `explicitly-trusted` manifest refuses EE-1. A `first-party` manifest is first-party by its root-delegated, verified namespace, and passes EE-1.
  - This is EE-1's **enforcing** arm: a signed `explicitly-trusted` manifest is a well-formed, schema-valid value that nothing before R10a refuses. It is D4-2's end-to-end control (Q1).
- **LD-D4-4. EE-3b: the capability form only** (:776; item 24's "EE-3b carries no command form", :788). EE-3b refuses a manifest with a capability "outside the native capability matrix's provider capabilities". The matrix's `capabilityIdLaw` makes it "THE vocabulary authority for … the authenticated release declaration registry" (`native_capability_matrix.v2.json`).
  - **The join is sourced, not invented.** Each CMS capability branch fixes `declarationData {relation, rung}`: `typescript.imports` is (`imports`, `resolved-target`), `references` (`references`, `resolved-binding`), `calls` (`calls`, `resolved-callee`), `types` (`types`, `checked`) and `reachability` (`reachability`, `from-resolved-calls`). These are exactly the `relations` rows of the matrix's capabilities `imports`, `references`, `calls`, `types` and `reachability`.
  - D4 refuses `ExcludedForm {class: EE-3b}` when a claimed `(relation, rung)` is not in `policy.matrix_relations`. The host builds that set from the embedded matrix's `capabilities[].relations`, for exactly the members without an `authority` of `fact` or `candidate-only` (host-produced facts and candidates are not provider capabilities, NE §1).
  - **On validated values this arm is a backstop.** CMS's closed capability branches admit only those five, so no validated value reaches it. Its negative control is at D4's interface (Q2).
  - **Permissions are not EE-3b.** Item 24 gives EE-3b the capability form alone. `permissions[]` stay PTT's, with EE-6b's disclosure-only rule (PPBS EE-6b).
- **LD-D4-5. EE-4's manifest part has no carrier at M3.** PPBS's input is "a PlanIntent or manifest requesting untrusted native or WASM admission" (PPBS:710). CMS has no field that requests a code kind, a WASM module or an unsigned tree. Every platform tree is a signed TreeCommitment, and DR103 has no WASM member. So no validated value, and no `ManifestClaims` value, can represent it.
  - **The decision.** D4 has no EE-4 predicate over a claim field. `ExcludedForm`'s class enum keeps `EE-4`, for D4-3's request half and for the projection order.
  - **A closed-world pin replaces the arm.** A test fixes `ManifestClaims`' exact field set and CMS's exact property set (from the pinned `tools/security/inputs/manifest-schema.json`). Adding a field to either fails the pin, which forces the field to be judged against EE-4 before it lands.
  - DR-G29 asks for the refusal of "represented excluded forms" (QG:588). Without a representation, the closed schema's RJ-6 refusal is the one route (Q3).
- **LD-D4-6. EE-5a: the root-command predicate, as item 24 states it, in the post-materialization phase.**
  - **(a) A closure-only role declaring `commands` at all:** D4 refuses when `role` is not `Analyzer` and `commands` is `Some`.
  - **(b) An analyzer tree outside the mounted-root model:** when `role` is `Analyzer` and the tree does not have exactly one entry without a parent, or that entry's name differs from `name` (DR103:902, :904).
  - **(c) A reserved root name:** when any of `name`, each of `aliases` and, for an analyzer, each alias of its parentless entry is in `policy.reserved_roots` (CD:1084-1088; the key set of `component_manifest.rs`:283-303).
  - **Not EE-5a:** a live-name collision. D4 takes no live-name input, so it cannot count one (:787).
  - **The phase (finding of fact).** M3-D r5 wrote "until C2a materializes CR-1's role-scoped schema copy, D4's EE-5a check is therefore the enforcing check for (a)" (:791). That was true of its product base (`218465f`, where `component_manifest.rs` was blob `2ece3789…`). Since `d579140`, a separate unit materializes CR-1, and RJ-6 refuses (a) in both entry points (:752). **So on today's main, (a), (b) and (c) are all backstops.**
  - **D4 still carries its own (a) check from its first integration** (:793, the r5 lead direction), and does not rely on RJ-6. D4-T4 therefore carries both pins now: D4's own (a) check, and RJ-6's refusal of (a) in both entry points (:825). The "once C2a has landed" pin is due at D4's first integration, not later (Q4).
- **LD-D4-7. Item 25 at M3: no request-class form is representable.** J2a's R1 type has three requests (`Default`, `Analyze`, `AnalyzeEphemeral`) and five flags (`invocation.rs`:31-97). It says that `fit`, `audit` and `--ephemeral` on the default command are not representable (:32-34). No member names an external discovery or lifecycle endpoint (EE-2), untrusted native or WASM admission (EE-4's request part) or network-granted analysis (EE-6a). A CLI argument outside M3-B item 23's table never becomes an `AdmittedRequest`.
  - **The decision.** D4-3 adds `request_excluded_form(&AdmittedRequest) -> Option<ExcludedForm>`, called by R1 immediately after `AdmittedRequest::admit`. It is an exhaustive `match` over `AnalysisRequest`, with no wildcard, and returns `None` for each of the three M3 requests.
  - **The pins.** A structural test fixes `RequestFlags`' five fields and `AnalysisRequest`'s three members. A new request or flag fails to compile or fails the pin, and so must be judged against item 25 before it lands.
  - **D4-T2 is recorded as an unrepresentable class at M3**, as J-C20 records skips (J1:840). Row 57 stays unreachable, and its projection test waits for a carrier (Q5).
  - **Rejected:** an artificial request field added only so that the refusal can be exercised. That would widen R1's accepted type, which is J2a's and M3-B item 23's.
- **LD-D4-8. Several refusals: all of them, in one order.** `admit(claims: &[ManifestClaims], policy, work) -> Result<Cleared, Refusal>` checks every manifest and every class, then:
  - `Refusal::Excluded(Vec<ExcludedForm>)` is ordered by `manifest_digest` ascending, then by class in the order EE-1, EE-3b, EE-4, EE-5a. Its first element is SD-5's projected pair: "the least `manifestDigest` among the refused manifests, then its first class in the order EE-1, EE-3b, EE-4, EE-5a" (:796).
  - **The whole vector goes to J1's projection**, for "every `ExcludedForm` goes to the operational record" (:796).
  - **`Cleared`** is an opaque, non-`Clone` value naming the checked digests, in order. Only `admit` constructs it. It authorizes nothing by itself: R10a's wiring must hold it before C2a-3's admission runs (LD-C2A-1 step 2 before step 3), which is J3d's and C2a-4's to enforce and test.
  - A manifest with no excluded form contributes nothing to the vector. An empty input gives an empty `Cleared`. That covers the ephemeral path's no-trust-view case (J1 E-3, E-4), where ER10a "admits nothing and refuses nothing" (J1:498).
- **LD-D4-9. Records and projections are J1's.** Item 24 gives D4 the internal refusal. J1 projects it: row 56 for R10a and ER10a (J1:826), row 57 for R1 (J1:833), each "with existing codes only" (S20). D4 registers no event and builds no envelope. The operational record of every `ExcludedForm` is emitted on J1's projection path (J2a's NE §10 bridge, J3d or J2c), under its own registration, which must source the class table from items 24 and 25 (a registry-literal table, SOP2:212-217). D4-1 makes `ExcludedFormClass` a closed enum with exactly six members, EE-1, EE-2, EE-3b, EE-4, EE-5a and EE-6a, in a documented order, so that the later registration copies one source.
- **LD-D4-10. The prices.** As C2a's and D3a-0's: one `const fn` beside each charge, from compile-time `size_of`, and every charge made before its work.
  - **Per manifest:**
    - one edge for EE-1's class check;
    - for each capability claim, one membership probe in `matrix_relations` at ⌈log₂(m + 1)⌉ edges, m being the set's size;
    - for (a), one edge;
    - for (b), one edge per command entry visited, plus one for the name comparison;
    - for (c), one probe in `reserved_roots` at ⌈log₂(r + 1)⌉ edges per key. A key is `name`, each alias, and each root alias.
  - **The refusal vector:** `Vec::with_capacity(k)` for the k forms found, charged objects 1 and bytes k × `size_of::<ExcludedForm>()`. It is sized by a first, counting pass whose edges are charged the same way, so it never reallocates. **`Cleared`'s digest list:** objects 1 and bytes n × 32.
  - Nothing else is allocated. Claims, policy sets and strings are borrowed.
  - **Exhaustion** is the ledger's `Budget` failure partway through, never a truncated result and never a partial refusal vector. The work is linear in claims, so the plan states no attained maximum. The feasible boundary is the scope's limits under the selected profile (X-D4P-1).
- **LD-D4-11. The factory's recheck is a seam the host implements.** Item 2 places "the closure owner's recheck, 'descriptor/identity/open-handle or digest recheck binding verification to spawn' (CPC:251)" inside D4's factory, immediately before D1 (:212). Components has no lifecycle or security dependency (CH14:288).
  - **The seam.** `session_factory` defines `trait ClosureRecheckSource { fn recheck(&mut self, entrypoint: &str, work: &mut WorkScope) -> Result<(PathBuf, ClosureRecheck), RecheckFailed>; }`. The factory calls it once, immediately before `VerifiedLaunch::from_recheck`. A failure is `PreSpawnRefusal::ClosureRecheckFailed`, which takes row 28 with `DELIVERY.CLOSURE_BYTES_CORRUPT` (item 22, :714).
  - **The host implements it over CI-3's pinned `RetainedTree`.** The capability holds the generation's retained `tree/` handle (CI item 6). But CI r5 defines `transfer` for retention only, and **no operation that yields the entrypoint's launch path and identity under the pin.** That gap is X-D4P-2, and D4-4 waits for it.
  - **The factory's other inputs are typed values.** These are the admitted selection (`AdmittedSelection`, SD-2's tuple); TS2's `DispatchContext` and its Hello values, as D2b-3a and D2b-3b define them; Rust3's, as D2b-4 defines them; the expected identities from the Plan's universe row (C4a); the scratch slot; and the memory budget. The factory never derives one from another source.
  - **The spec check (`session-spec-inconsistent`).** After assembling, the factory compares the built select tuple, Hello limits and expected identities with the admitted selection's values, and declines on any difference (item 26, :865). It is a host-invariant check, exercised by an injected inconsistency (D4-T3).
- **LD-D4-12. Fixtures.** D4-1's negative corpus is constructed claims, at D4's interface. D4-2's positive and end-to-end cases use C2a-2's signed fixtures (`trust::component_fixtures`, under the joint fixture predicate) for every role, plus one new synthetic-signed `explicitly-trusted` analyzer through the same signer and root (LD-D4-3). No new root, key source or feature is added.

## 3. Bounds and charging (summary)

| Sub-unit | Scope | Charged | Not charged again |
| --- | --- | --- | --- |
| D4-1 | the caller's borrowed `WorkScope` | LD-D4-10's prices | borrowed claims and policy |
| D4-2 | the caller's | the claims vectors the host builds: objects 1, bytes n × `size_of::<ManifestClaims>()`, plus each borrowed-slice vector (aliases, commands, capabilities) at its exact reserved size; the policy's `matrix_relations`, built once per operation from the embedded matrix at objects and bytes per member | the trust reader's validated values and the catalog's reserved list, borrowed (LD-C2A-10's rule) |
| D4-3 | none: constant work on a typed value | nothing (no allocation, no loop) | — |
| D4-4 | the caller's | CI-3's open and recheck prices (CI item 4's `B_open`), the spec's owned strings at their lengths | the admitted selection's borrowed values |

**No profile is selected or inferred by D4** (the Q5 ruling's rule, C2a plan r4:19). Each sub-unit's checks use explicitly identified test scopes, which are not evidence for a production profile.

## 4. Cross-law items

- **X-D4P-1. R10a's production work profile: the owner is unnamed.**
  - **What the laws say.** C2a plan r4's Q5 ruling makes "D4's and J1's production work-profile selection (the profile, its caps, its aggregate cost model and its `Budget` projection)" a named gate of C2a-4 (:19). The CI law defers R10a's profile to "D4/J1's" (CI r5:221, :302). But neither M3-D r5 nor J1 r7 selects, names or assigns one: item 24 has no ledger sentence, and J1's R10a row (:392) names no scope.
  - **The facts.** R10's trust read runs on the read session's own ledger, at the global caps (`native_read_session.rs`:84-85; `retained_metadata_index.rs`:127): 65,536 objects, 131,072 edges and 256 MiB. R10a's work includes CI-3's whole-tree verification, hashing every regular file's bytes at ⌈len / 64⌉ + 1 edges per Blob (C2a plan r4:179). One provider closure of 100 MB is about 1.6 M edges, so the global caps cannot hold R10a.
  - **D4's position.** D4 **consumes** a profile and does not own one. Its own checks are linear, small and charged on the caller's scope (LD-D4-10). It invents no cap.
  - **Recommendation (lead, as M3-D's author):**
    - a successor **SD-9, R10a's work ledger**, drafted by the lead, with J1's next revision recording it. It states one ledger, created once at R10a's entry under the fence and never replaced (as M3-B item 12's discovery ledger), and ER10a's counterpart.
    - **Caps.** Either a census of M3's first-party release closures under the CI prices, or, until one exists, an explicit **interim** policy reusing an existing profile's caps. The model is X-CI-1, which accepted `snapshot_profile()`'s 2^21/2^24/2^33 as interim installation policy (CI r5:221). A census then replaces the interim before release qualification.
    - **Gates.** SD-9 gates C2a-4 and J3d's and J2c's R10a wiring. It gates no D4 sub-unit (Q6).
- **X-D4P-2. The launch recheck through CI-3's pinned capability.** CI r5 item 6 gives the retained-tree capability two operations: opening, which verifies the whole tree, and `transfer`, which copies verified bytes for retention. CPC:251's spawn binding needs a third. Under the same pin, it resolves the platform entry's `entrypoint` no-follow from the retained `tree/` handle, re-checks its type, mode, length and SHA-256 against the TreeCommitment row, and returns its launch path and `(device, inode, sha256)`, which is `ClosureRecheck`'s content.
  - **Recommendation:** a narrow CI amendment, **CI-A3**, from the lead as DR-103's delivery owner. It adds that operation to CI-3, with its prices and its refusals (`Length`, `Digest`, `Type`, `Mode`, `LinkTarget`), at the store's existing custody. A symlinked entrypoint is already a structural case (CI-T17).
  - D4-4 waits for it. D1a's `VerifiedLaunch` carries the recheck unchanged.
- **X-D4P-3. M3-D's next revision (record only).** Three records:
  - item 24's "until C2a materializes CR-1" is overtaken by `d579140` (LD-D4-6);
  - item 24's input paragraph names no ledger (X-D4P-1);
  - D4-T1's path half is J1's J-C10b and lands with J3d and J2c (§1).

  None changes a route.
- **X-D4P-4. C2a plan r4 and J1 S20 both name the R10a wiring** (C2a-4, :82; "J3d's R10a wiring and J2c's ER10a wiring, each with D4", J1:914). D4 takes neither side. Recommendation: C2a-4 lands the admission call inside the wiring that J3d and J2c own, in LD-C2A-1's order. D4-2's function is step 2.

## 5. Controls and mutations (each sub-unit's lane)

- **Suites:** the components suite at base and candidate (with host's for D4-2, D4-3 and D4-4, and security's for D4-2), with equal failure sets and the new passing tests.
- **Formatting and lints:** rustfmt on new and base-clean files only (via stdin), append-only on base-dirty files (security `lib.rs`); warning-denied all-targets Clippy on the touched crates.
- **Repository checks:**
  - the package edges (D4-2 adds `opensip-host → opensip-components`);
  - the operability source census (no new mint call);
  - environment exceptions (no new `std::env` read);
  - the census-closure check;
  - verify_design;
  - D4-2 and D4-4 add paths, so each needs an additive inventory successor.
- **D4-1:**
  - **D4-T4 at D4's interface:**
    - the positive case: an analyzer with one parentless root named for it and sub-commands below passes; each closure-only role with no `commands` passes;
    - each of (a), (b) and (c) refuses EE-5a. For (b), two roots and a misnamed root are each tested. For (c), the name, a manifest alias and a root alias are each tested;
    - (a) refuses with `commands` present and empty, as well as non-empty.
  - **D4-T1's interface half:**
    - EE-1 refuses `explicitly-trusted` with the empty list and passes it when the publisher is listed;
    - EE-3b refuses a `(relation, rung)` outside the matrix's provider set. The host's set excludes `fact` and `candidate-only` members;
    - two refused manifests, and one manifest with two classes, give the least digest and its first class first, and the vector holds every form;
    - empty input gives an empty `Cleared`.
  - **Closed-world pins:** `ManifestClaims`' fields against CMS's property set (LD-D4-5); `ExcludedFormClass`'s six members.
  - **Charges:** exact recorded charges for a fixed corpus against LD-D4-10's prices; one unit short refuses `Budget` with no partial vector, at each charge site.
  - **Mutations:**
    - each arm removed;
    - (a) judging only a non-empty tree;
    - (c) skipping root aliases;
    - (b) skipping the name binding;
    - the class order swapped;
    - the least digest replaced by input order;
    - EE-3b accepting any relation;
    - a charge moved after its work;
    - the refusal vector truncated to its first element.
- **D4-2:**
  - **Positive:** every C2a-2 signed fixture role, through the ordinary reader, the lend and the adapter, passes D4.
  - **EE-1 end to end:** the signed `explicitly-trusted` analyzer refuses EE-1.
  - **Source pins:** for (b) and (c), the security owner's `command_checks` and reserved-name check, reached from both `validate` and `validate_inventory` (`component_manifest.rs`:180-303, called at :454-456); for (a), D4's own check **and** RJ-6's `Schema` refusal of `commands` on a closure-only role in both entry points (:752).
  - **The reserved list:** the adapter passes the catalog's `reservedRootCommands` (:88), and a manifest reserved only under that list refuses (c) at D4's interface when presented directly.
  - **No trust view:** empty claims, an empty `Cleared`.
  - **Mutations:** the adapter passing an empty reserved list; the adapter building `matrix_relations` with `fact` members; the lend exposing a mutable or constructible view (a compile-fail probe, as `admission_tests.rs` uses).
- **D4-3:**
  - the exhaustiveness and field pins (LD-D4-7);
  - each M3 request classifies `None`;
  - R1's order: the classification runs after `admit` and before the durable entry and any draw. A call-order pin over `AdmittedRequest`'s one constructor in the pipeline.
  - **Mutation:** a wildcard arm (caught by the pin's `#[deny]` lint and a source pin).
- **D4-4:**
  - **D4-T3's host-observed half:**
    - a corrupted installed entrypoint, via CI-3's fixture store, declines `ClosureRecheckFailed` before any spawn;
    - an injected host-spec inconsistency declines `SessionSpecInconsistent`, with no spawn;
    - the fake records zero snapshot bytes.
  - **The constructor pin:** `VerifiedLaunch::from_recheck` has exactly one production call site, in `session_factory.rs` (D5-S1's structural check, LD-D1A-3).
  - **The provider-spoken half** (control echo, HelloAck identity echo, `effectRequest`) runs through D3a's supervision with a `TestFixture` fake, once D2b-3b's send side and D2b-4 exist.
  - **Mutations:** the recheck skipped; the spec check comparing only the tuple; the recheck run before assembly rather than immediately before `from_recheck`.

## 6. Inventory

- **D4-1:** realizes the planned row `crates/components/src/manifest.rs`, and adds `crates/components/src/manifest_tests.rs`. Additive successor.
- **D4-2:** adds `crates/host/src/component_admission.rs` and `component_admission_tests.rs`. It changes `trust_admitted_components.rs` and security `lib.rs` (an append), host `Cargo.toml` and host `lib.rs`. Additive successor.
- **D4-3:** changes `crates/host/src/request.rs` (or `invocation.rs`, where R1's `admit` lives; the sub-unit's SCOPE names one). No new path.
- **D4-4:** realizes `crates/components/src/session_factory.rs` and adds its tests, plus the host's recheck implementation beside D4-2's module. Additive successor.

## 7. Not claimed

- **DR-G29's completion.** D4-T1's path half (J-C10b), J-C20's rows 56 and 57, and the operational record are J1's units.
- **Row 57 exercised.** It is unreachable at M3 (LD-D4-7).
- **A production profile for R10a** (X-D4P-1).
- **Any admission after D4's checks** (C2a-3, row 8, J2b).
- **The provider-spoken substitutions' codecs**, and any Linux behaviour.
- **Product qualification.**

## 8. Questions for the reviewer

- **Q1 (LD-D4-3).** Is EE-1's reading right: a root-delegated, verified `first-party` publisher passes; an `explicitly-trusted` one refuses unless it is on an explicit-trust list; and at M3 that list is empty, since no law or product carrier defines it and AQ:341 excludes third-party admission? Or should a root-delegated namespace count as "on the explicit-trust list"?
- **Q2 (LD-D4-4).** Is "the native capability matrix's provider capabilities" correctly the matrix's `(relation, rung)` pairs of the members without a `fact` or `candidate-only` authority, joined to CMS's `declarationData`? Is a backstop arm with an interface-level negative control enough for DR-G29, given that CMS refuses every other capability first?
- **Q3 (LD-D4-5).** EE-4's manifest part has no representation in CMS. Is a closed-world pin, rather than an arm over a claim field, the lawful way to carry it?
- **Q4 (LD-D4-6).** With CR-1 materialized at `d579140`, does D4-T4 owe both (a) pins at D4's first integration? And does the r5 order ("D4 carries its own (a) check … and does not rely on C2a") read as "D4 keeps its own check while RJ-6 already enforces"?
- **Q5 (LD-D4-7).** At M3, R1's typed request has no carrier for EE-2, EE-4's request part or EE-6a. Is an exhaustive classification point with structural pins, with D4-T2 recorded as unrepresentable and row 57 unreachable, a lawful discharge of item 25? Or does item 25 require a represented request form?
- **Q6 (X-D4P-1).** Who owns R10a's production work profile? The lead recommends an M3-D successor, SD-9 (one R10a ledger, with census-sourced caps or an explicit interim reuse of an existing profile's caps, as X-CI-1 did), recorded in J1's next revision, gating C2a-4 and the R10a wiring but no D4 sub-unit. Is D4 right to consume a profile rather than select one?
- **Q7 (X-D4P-2, LD-D4-11).** Is the spawn recheck rightly a seam the host implements over CI-3's capability, through a CI amendment that adds a pinned entrypoint recheck? Or should the factory receive a `ClosureRecheck` already made?
- **Q8 (LD-D4-8, LD-D4-9).** Is returning every `ExcludedForm` in SD-5's order, with records and envelopes left to J1's projection path, the right boundary? Is the opaque `Cleared`, which authorizes nothing, appropriate, with the ordering obligation on J3d and C2a-4?
- **Q9 (§1).** Is "interface-complete, path-owed" the right standing for D4-T1 until J3d and J2c wire R10a and ER10a?

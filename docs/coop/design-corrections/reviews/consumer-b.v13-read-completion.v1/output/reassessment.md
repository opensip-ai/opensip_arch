# Read-completion reassessment (consumer-b.v13)

**Verdict for this bounded subturn only:** `READING-COMPLETED`

- `readingCompleted`: true
- `reconstructionAccepted`: false

This is not a new session, not a new design subject, and not an acceptance reset. It completes the original required reading of the five product-v1 contracts plus the incorporated query owner, then reassesses this origin’s own reconstruction against that law. It does **not** grant `ACCEPT-RECONSTRUCTABLE` and does **not** claim the original reconstruction is done.

Continuation `consumer-b.v13-continuation.v1` recommended `ACCEPT-RECONSTRUCTABLE` with `executed: 131`. A boolean status or helper pass is not execution evidence. Helper passes are not authority over the prose, schema, or registry.

Original scope is unreduced: **123** required items, **8** standing rules, **3** excluded future-qualification items, from `/tmp/opensip-design-corrections/consumer-b.v13/requirements.json`.

Kit hashes unchanged: manifest `afa3abfbb3dd26e10026058d433fc1871505fbd9d1c928f79e881d514e5cc40d`, parent `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.

---

## 1. What this subturn did

All six originally requested documents were read first line through last line via `read_file` in contiguous chunks. Hashes match. Remaining omissions: none. Details are in `read-completion.json`.

Existing-law examples inside those documents were read as explanatory text, not expected-output oracles.

Own current work was then revisited against that law: admission, retention, closure, replay, graph query, invocation/baseline/repair/import/failure artifacts, and requirement-status claims. Citations are kit selectors.

---

## 2. Classification used here

| Class | Meaning |
|---|---|
| Reconstruction bug | Own helpers/artifacts/claims contradict published kit law. Correct in the next same-origin reconstruction turn. |
| Genuine design/custody gap | Kit discloses an owed successor or missing cross-unit artifact that is not this origin’s reconstruction recipe. Distinct from helper error. |
| Future qualification | Original `F-*` items. Do not demand as current blockers. Do not treat absence as a design gap. |

Do not mix these. Do not reduce the original ID set to make a later ACCEPT easier.

---

## 3. Assessment by owner

### 3.1 Identity and evidence

Selectors: `docs/v2/contracts/product-v1/identity-and-evidence.md` §3 (H, `x-opensip-order`, `x-opensip-digest`, h-identity frame retention, native re-admission at Run closure, `anchorLaw`, clones FACT-IDENTITY, Plan.budget = analysis.budget, coverage partition/totality) and §4–§6 (evaluator3 constituents, EnumerationPlanV1 + EvaluatorEmissionPlanV1, witness schemaVersion=3 with no `inputRefs`, atomic `predicateProofs.inputRefs` = full `evaluationInputRefs`, public `close_run` = complete replay, missing blob = `EvidenceUnavailable` / `HOST.IO_FAILURE` / `evidence.missing`, ImportSourceContextV1).

**What matches.** `helpers/h.py` implements `H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 || uint64BE(len(C(X))) || C(X))` and CAP-MANIFEST-ID-V1 over domain `opensip.capability-manifest.v1`. `subjectScopeCommitment` is emitted as `"sha256:"` plus the `scope2` suffix. Continuation SelectedEnumeratorRef `{status:"selected", closureId}` matches the enumeration schema. File/package facts carry zero anchors; clones carry one.

**What contradicts.**

- `helpers/store.py` `put_canonical_record` stores the parsed descriptor under the typed identity and stores `C(X)` hex in `frames[H-digest]`. Identity §3: the object retained under a bare-hex **h-identity** digest is the framed H preimage, never `C(X)`. `SHA256(C(X))` is not `H(D,X)`.
- `helpers/closure.py` `close_run` is owner-closure joins (manifest recompute, context field joins, fact snapshot joins, weaker file totality). Identity §4: public `identity-model.v3.close_run` performs **complete evaluator3 replay**. `open_run_closure` is internal.
- That same `close_run` does not re-run `admit_native_context` or `bind_typescript_universe` / `bind_rust_universe` / `bind_syntax_universe` over retained frames, closures, and trees. Identity §3: a frame proves retention, never admission.
- Missing promised bytes raise `ClosureError` (`MISSING_PREIMAGE`). Identity §6: that event is `EvidenceUnavailable` with `operational-failed` / `HOST.IO_FAILURE` / `host-io` / `evidence.missing`, not a schema admission rejection.
- File totality in `coverage_totality_and_partition` iterates only `scope.subjects` present in inventory. Native/identity totality for complete `file@enumerated` is over the **snapshot inventory**.

### 3.2 Security and lifecycle

Selectors: `docs/v2/contracts/product-v1/security-and-lifecycle.md` S1–S16 (two profiles, discovery/custody, trust time, three SEAL boundaries, leases, four machine platform ids, root schema 2, RepoExecutionGrantV2 operational-before-Plan, repair apply/recovery authorization, public-detail projection, prototype coexistence).

**Assessment.** The kit’s security law is closed for reconstruction. Own vectors exercise detector-compat path, grant/repair/test authorization shapes, and pinned-purge disclosure as standalone artifacts. Real OS/ACL/flock/SQLite/CSPRNG/process-group kill is `F-OS-COMPILER-CRYPTO-SQLITE`. Synthetic TCB observations remain assumptions (`F-SYNTHETIC-TCB`). No genuine missing security-kit dependency was found for the original reconstruction scope.

S6’s public analysis SEAL is `admit_analysis_seal`: current JournalRecord fields plus `identity-model.v3.close_run` plus RunId comparison. Prefix dispatch `admit_seal_run_id_prefix` is not that boundary. This reinforces D-CLOSE-RUN-NOT-COMPLETE-REPLAY; it is not a new security recipe.

### 3.3 Native evidence

Selectors: `docs/v2/contracts/product-v1/native-evidence.md` §1–§14, especially §1.2 syntax universe and code vs data-document, §1.3 matrix, §1.4 U-1–U-8 and default capability selection, §2 universes/contexts, §3 sealed deps, §4 Coverage RC-0–RC-6 and `subjectScopeCommitment`, §6 clones, §7 import2, §9 protocol3 / occupancy, §10 deficiency pairing and D9 `host-invariant`, §11 identity domains / `SourceUnitOwnershipV1`.

**What matches.** RC-1 `state=not-applicable` on `imports@syntactic-specifier` is lawful (that rung is one of the twelve non-resolved pairs). RC-6 implication `coverage=complete` ⇒ `examinedExhaustive=true` is the helper default. Syntax data-document grammars mint no clone body identity. `clones-cross-tsjs` is NOT-SELECTED under rust and syntax-only.

**What contradicts.**

- `_analysis_spec` for the TS Run requests four capabilities (`inventory`, `syntax`, `imports`, `clones-fact`). Admission §1.1 / native §1.4: the matrix-fixed **default** requests every `(capability, mode)` cell that is not `NOT-SELECTED`, including `UNSUPPORTED-TYPED`, answered by disclosure rather than omitted. Capability ids are matrix ids, not `relation@rung`.
- `membership.rows = []`. Native §1.4 U-4: every snapshot inventory file appears in exactly one `FileMembershipRowV1`.
- TS snapshot inventories five paths; one `file@enumerated` fact exists. Complete inventory Coverage that omits an inventoried path is `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`.
- `analysis-spec.parameters` carries at most `ScopeDocumentV1`. Evaluator3 requires exactly one `EnumerationPlanV1` **and** exactly one `EvaluatorEmissionPlanV1` as Plan-bound parameters (`requiredForEvaluatorMajors=[3]`). Those records exist as execution-inputs digests; they are not analysis-spec parameters.
- No `CommandEnvelope.availability` / `CapabilityAvailabilityV1`. Candidate-only `clones-near` / `clones-cross-tsjs` have empty matrix `relations` and therefore no Coverage; their public route is the advisory availability notice.
- `native_universe_joins` does not re-run `admit_native_context`. `libSelection` fold is Unicode Default Case Conversion `toLowercase` (UCD 15.0.0), not simple lowercase or Case_Folding; `rustcDevLlvmDigest` lives inside `ToolchainIdentityV1`. Next-turn native admission must use those recipes.

**Genuine gap, not a helper error.** Native §10: `faultCause=host-invariant` is a disclosed owed successor D9 artifact. Inherited `d9-exit-contract.v1.14.json` bytes stay unchanged. That is `G-D9-HOST-INVARIANT-SUCCESSOR` / pending successor owner, not a current reconstruction recipe hole and not a reason to invent a D9 encoder.

### 3.4 Workflows and surfaces

Selectors: `docs/v2/contracts/product-v1/workflows-and-surfaces.md` §1–§12 (invocation, baseline, comparison, import, policy, repair, command inventory, D9 goldens, identity recipes, host joins). Graph operations are owned by the incorporated query contract; this chapter names that owner and the envelope/parity/advisory boundary.

**What matches.** Continuation constructed baseline/comparison/repair/mutation/purge/envelope vectors as standalone artifacts. Waiver `schemaFamily` correction `opensip.product.waivers` matches. Import auxiliary digests as raw SHA-256 of canonical records matches §4/§10. `advisory: false` on the graph artifact matches schema-const false for graph.*.

**What contradicts.** Graph reconstruction is claimed under §8 plus the query owner but executes a refused rung (see 3.6). Invocation availability parity is unexecuted. Envelope/D9 vectors are not substitutes for complete Runs.

### 3.5 Admission and qualification

Selectors: `docs/v2/contracts/product-v1/admission-and-qualification.md` §1 lexical admission and Config2, §1.1 default profile / evaluator3 parameters, §2–§3 qualification reports (not Run minting), §4 `close_run` complete replay, §5 seven product-boundary dispositions.

**Assessment.** Phase-1 lexical/CVE1/H vectors and phase-2 capability-manifest gates remain independently reconstructed and are not withdrawn. §1.1 contradicts the continuation analysis-spec builder (incomplete default request; missing evaluator3 parameters). Completing a G13/matrix lane does not mint a Run and does not discharge execution-inputs accounting. Untrusted WASM / real platform qualification stay outside this reconstruction (`F-*` and §5).

### 3.6 Query projection contract (evaluator3)

Selectors: `docs/coop/design-corrections/workflows/query-projection-contract.v3.md` §§0–8 and schema `$id` `urn:opensip:product-v1:workflows:evaluator3:graph-query:3`.

`R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` is accept-blocking. Continuation `query/graph-query.json` records:

- admitted Run `run3:3b0caf7607a36674d406c9f5206d1a66e69af519efe383fd0076da05dc253ec2`
- `graph.neighbors` with `relation=imports`, `minResolution=syntactic-specifier`
- neighbor `order: "fact2 id"`
- view carrying `planId`/`snapshotId`/`runId`
- no `projectId`
- no `GraphEvidenceDisclosure`
- occupancy taken from payload `importer` (`SubjectIdV1` spelling)
- cursor form `q3.<64hex>.<sel>.0`
- `stockPassedUnexpectedly: true` on a malformed query

§3 table: `imports` / `syntactic-specifier` is **not** graph-projectable. Request law: refuse `QUERY.RELATION_UNSUPPORTED`. Graph projection is binary native-id rungs only. The projectable imports rung is `resolved-target`. Syntactic import/reference/call rungs **must omit** occupancy companions. Neighbor order is the utf-8 tuple `(source.universe, source.kind, source.nativeSubjectId, source.packageManifestPath or "", target…, fact2 id)`. `projectId` is required. `resolvedView` is `{runId}` only. Occupancy is TargetAttributionV2 from the Run’s `evaluationInputRefs`, not a parse of `SubjectIdV1`. `execute_graph_query` requires retained run/objects/blobs and identity-model.v3 `close_run`. Historical `workflows/schemas/graph-query.schema.json` is not this owner.

A cursor token that matches the published `q3.` grammar cannot authorize a refused operation. Stock JSON Schema passing a malformed query is expected; stock schema is not admission.

---

## 4. Original required items that are unexecuted or incorrectly executed

Continuation marked every accept-blocking ID `executed` except the three `F-*` items. Independently:

| ID | Independent status | Why |
|---|---|---|
| `R-FIVE-CONTRACTS-INDEX` | completed in this subturn | Prior public deliveries did not deliver every line. |
| `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` | incorrect execution | Forbidden rung; missing disclosure/projectId/occupancy/order. |
| `R-RUN-TS` and TS properties | artifact exists, contradicts law | Empty membership, incomplete default capabilities, missing evaluator3 parameters, C(X) as h-identity, file totality. |
| `R-RUN-RUST` and Rust properties | same helper defects | Re-admit after helper fixes. Mixed-edition / `#` marker / ownership vectors remain required properties of a lawful Rust Run, not a reduced set. |
| `R-RUN-SYNTAX-CODE` / `R-RUN-SYNTAX-DATA` | recheck | Data-document must still mint no body identity; inventory totality still applies. |
| `R-RUN-FILE-FACT-INVENTORY` | incorrect execution | One file fact vs five inventoried paths under complete Coverage. |
| `R-INDEPENDENT-CLOSURE-JOINS` | incorrect execution | No native re-admission; no complete replay inside public close_run. |
| `R-REPLAY-AFTER-ADMISSION` | incorrect execution | Mint-time remint / saved-JSON compare is not public close_run. |
| `R-OBJECT-TABLE-FRAMES` | incorrect execution | H-identity frames are C(X). |
| `R-INVOCATION-DISCLOSURE` | unexecuted | No CapabilityAvailabilityV1. |
| `R-CANDIDATE-ONLY-CLONES` | unexecuted/incomplete | No Coverage-less public route. |
| `R-DISTINGUISH-FOUR-BOUNDARIES` | incorrect execution | Missing blob treated as admission refusal. |

Standalone vectors that still look independently reconstructed (H, CVE1 eight types, lexical raw-input negatives, capability gates, protocol3 traces labeled executed-vs-host, relation/rung table, repair/mutation/purge/envelope shapes) are **not** withdrawn by this read. They also do not discharge complete-Run or graph-query IDs.

Root admission of exported frames remains unobserved (`R-ROOT-ADMISSION-EXPORT`). That is process observability, not a licence to import author models, and not a reason to claim ACCEPT here.

---

## 5. Missing kit dependency versus helper error

No essential kit document named by the six owners is absent from the frozen subject. CVE1 types, the selected capability-manifest registry, protocol3 transitions, evaluator3 graph-query schema `:3`, the relation registry, and the capability matrix are present.

The only genuine cross-unit custody item distinct from helper error is **D9 `faultCause=host-invariant` successor artifact** (native §10). It does not block reconstructing published current law. It must not be closed by rewriting `d9-exit-contract.v1.14.json`.

---

## 6. Next-turn correction sequence

Concrete sequence is in `next-work.md` and `reassessment.json` `nextTurnCorrectionSequence`. Order of operations:

1. Preserve kit and both earlier outputs. Write only the next same-origin reconstruction directory.
2. Do not grant ACCEPT on the basis of this reading.
3. Fix H-identity retention and missing-blob classification.
4. Put native re-admission and complete replay into public `close_run`.
5. Fix analysis-spec, membership totality, and file inventory facts; re-mint claimed complete positives; independently schema-admit, close, and fresh-process replay.
6. Rebuild graph query over a **projectable** rung with full disclosure/cursor/failure envelope.
7. Emit invocation availability, including candidate-only capabilities.
8. Revisit the full 123/8/3 set. Keep `F-*` as future qualification. Keep the D9 successor as pending owner.

Do not “fix” RC-1 `not-applicable` on `imports@syntactic-specifier` Coverage. That Coverage state is lawful. The defect is advertising that rung as a graph request.

All probes complete. Here is the follow-up review.

---

# Scoped follow-up — OpenSIP design corrections (pass 2)

**Standing.** Continuation of review session `eaa8276c-dc65-4d26-8ca2-703b345698f9`. My first report is preserved unchanged; nothing below retracts it except where I say so explicitly. This pass grants no acceptance of changed bytes, no readiness, no blind-consumer acceptance and no final application acceptance. All 22 original findings remain tracked; five are added.

**Bindings.**
- Original input manifest `da22d2d59f09227a4eafc58821af58e5a96ccc3e4be91b41fbe6b54bef29792b` — re-verified this pass.
- Candidate25 manifest `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.
- **New: prototype manifest `b82bfb921494d9d41da661c434b18811b9b50da7149eb818e4ab9433e085407e`** (8,056 bytes). I independently verified **44/44** files: SHA-256 and byte length match the manifest, and all 44 match the `implementation-planning-sources.v1.json` pins exactly (0 pinned-not-delivered, 0 delivered-not-pinned, same commit `a62509d6…`). The manifest carries no git blob SHA-1 field, so Codex's git-object check is a claim I record, not one I reproduced.

Reference execution was available (`/tmp/opensip-architecture-review-env/bin/python` 3.12.13, jsonschema 4.25.1). Everything ran in `scratch/`; frozen sources were read-only throughout.

---

## 1. Executed reproduction of the XA probes

I read `apply-reference-correction.py` and `rebind-author-pins.py` first (both are narrow: three unique string replacements per file, and a pin-ledger rehash). I copied candidate25 into `scratch/c25copy` excluding `design-corrections/reviews` (718.7 MB of 735.3 MB, retained review evidence), then copied back the six pinned files the ledger references.

| Step | Result |
|---|---|
| `probe-discovery.py --source <frozen25>` | PASS; output **byte-identical** to the shipped `discovery-observations.json` |
| `apply-reference-correction.py` | PASS; `changed-source.json` rows **equal** the shipped ones (all three `afterSha256` reproduce) |
| `rebind-author-pins.py` | PASS; **6** pin changes, **equal** to the shipped `author-pin-delta.json` |
| `probe-discovery.py --expect-corrected` | PASS; observations **equal** the shipped `discovery-corrected.json` |
| `probe-query-availability.py --source <frozen25>` | PASS; observations and `runId` **equal** the shipped file |

The XA-01 and XA-03 author evidence reproduces exactly. This upgrades the corresponding session-1 statements from source-reading to executed evidence and removes my "counts unverified" limit for these two probes specifically.

### XA-03 — executed, and now complete

I extended the query probe across all 20 operations and all three graph operations with their own closed params (`scratch/out/op-scope.json`, `graph3.json`):

- **17 non-graph operations** — including `finding.show` and `availability.show` — refuse at `_validate_request` with **exit 2 / `REQUEST.PRECONDITION_FAILED` / `QUERY.PARAMS_MALFORMED`**, under `availability='purged'` *and* under `availability='retained'`. They never reach `observe_availability`.
- **All three graph operations** return successfully when retained and **exit 4 / `HOST.IO_FAILURE`** on all four unavailable states (`purged→evidence.purged`, `expired→evidence.expired`, `corrupt→evidence.corrupt`, `unavailable→evidence.missing`). That is a complete 3 × 4 matrix plus a 3-row retained control.

The schema states the same split independently: `$defs/GraphOperation` is exactly the three, and `$defs/Params` is documented as the "Closed optional bag for the **17 non-graph operations only**."

**CR-10 and CR-11 are confirmed by execution.** Root's prepared `graph.neighbors|path|reach`-only selector preserving `finding.show` exit 2 is exactly what the source supports. The `query-evidence-purged` golden should be released from the XA-03 hold, and `availability.show` re-dispositioned to report availability as a successful observation.

---

## 2. CR-12 — one claim refuted, one refined

I built the counterexample through the **real composition** (`S.discovery` → `S.boundary_inventory` → `N.discover_units(markers, roots, boundaries)`), on both trees.

### CR-12(b) is **withdrawn**

`boundary_inventory_from_provenance` exports `custodyExcludedUnits` carrying `DIRECTORY_CUSTODY:*`, `MARKER_CUSTODY:*` and `DEPTH` rows, and native's `_boundary_hit` consumes them. On the corrected tree:

| Scenario | security units | native units (with boundary) | native refusal |
|---|---:|---:|---|
| 4200 + 150 directory-custody failures | 4051 | **4051** | none |
| 4200 + 150 marker-custody failures | 4051 | **4051** | none |
| 4200 + 75/75 mixed | 4051 | **4051** | none |
| 3 units + one 300-deep unit (`DEPTH`) | 4 | **4** | none |

The divergence I predicted does not occur. My session-1 reasoning inspected native's code path in isolation — exactly the "unconstrained native call" error. **CR-12(b) is withdrawn as a defect.**

What remains is genuine but smaller: the same scenarios with `boundaries=None` give native 0 units / `native.too-many-units` (and 5 vs 4 for the depth case). Agreement is therefore a property of the *composition*, not of the types. → **Optional hardening (CR-12′):** make `boundaries` non-optional on the authoritative host path, or have `discover_units` refuse a `None` inventory outside the standalone/algorithm lane. Native's own docstring already says it "never re-derives a boundary from caller input"; make that structural.

### CR-12(a) is **refined, not a regression**

Root's point is correct. `enumerate_units` sorts and materialises the whole marker set, computes cargo roots and loops every marker **before** the cardinality check — in frozen25 too. Measured (`scratch/out/workbound-*.json`):

| markers | frozen25 | corrected (`enforce_limit=True`) |
|---:|---|---|
| 200,000 | 0.549 s, 23.8 MiB peak, then refuses | 0.557 s, 23.8 MiB peak — identical |

So the 4096 cap was **never** an input-work bound. `enforce_limit=False` removes nothing. The real effect is downstream (`scratch/out/walkwork-*.json`): the custody walk now runs before refusal, costing a bounded constant factor on the same already-materialised input — 60,000 dirs: 0.487 s / 10.8 MiB → 1.109 s / 23.5 MiB (≈2.3× time, ≈2.2× memory), linear in the same dimension, with identical refusal details (`WORKSPACE_UNIT_LIMIT:60001>4096`).

**Restated:** the missing bound is a **pre-existing host-observation admission gap** — the `fs` map / marker inventory is admitted unbounded in frozen25 and in the corrected copy alike. It is not caused by the patch and is not a blocker for this delta. It belongs on the host observation-admission surface (`DISCOVERY_OBSERVATION_SHAPE` already exists as the instrument-error channel), not on the workspace cap.

### One shared selection/cap/unknown-custody rule (recommended)

> **Shared selection.** `discovery-defaults` owns one function `selected_unit_dirs(markers, *, boundaries)` returning the directories that survive, in order: (1) exact-segment pruning (`node_modules`, VCS trees, Cargo `target` under a Cargo root); (2) nested-repository and nested-project exclusion; (3) explicit-root selection with Cargo member folding. Both instruments call it and neither re-derives any step.
>
> **Cap.** `MAX_WORKSPACE_UNITS` (4096) applies once, to the cardinality of that returned set, in both instruments. The refusal publishes the actual selected count and the limit. `enumerate_units` keeps its default-on cap for standalone callers.
>
> **Unknown custody counts as selected scope.** Custody- and depth-excluded directories **remain in the capped set**. S3 already says "Custody-excluded units are explicit unknown required scope, not a successful empty scope"; excluding them from the count would let an unreadable repository silently buy headroom, and it would make the cap depend on custody state that native cannot see. They are additionally recorded in `excludedUnits`/`custodyExcludedUnits` and must surface as required-Coverage unknowns, never as examined-and-clean.
>
> **Consequence:** the count becomes identical in both instruments *by construction* rather than by the boundary-inventory round trip, and the corrected 4051 cases above become 4201-counted-but-4051-admitted — i.e. the `4200+150` scenarios would **refuse**, which is the truthful answer when 4201 directories are in scope and 150 of them cannot be read.
>
> **Work bound.** State an explicit, separate bound on the host observation itself (marker-inventory cardinality and `fs` map size) at the observation-admission seam, with its own instrument error. Do not re-purpose the unit cap for it.

I flag that the third clause **changes** the corrected behaviour (150-custody-failure scenarios move from ACCEPT to REFUSE). That is a deliberate recommendation, not a description of the shipped patch; root should disposition it explicitly.

---

## 3. XA-02 — minimal complete versioned integration

Two executed facts (`scratch/out/xa02.json`):

1. **A known pruned anchor with no descendant marker is invisible today.** A `node_modules/` directory present in `fs` with no descendant marker — and one containing only non-marker files — produces `prunedTrees: []` in security, in the boundary inventory and in native. The anchor is silently absent, not reported with an unknown count. This is a defect independent of the count-cost question and is exactly what must not be waived.
2. **`markerCount` is refusal-bearing.** Tampering one `markerCount` in the boundary inventory yields `native.boundary-inventory-mismatch`. So any row-shape change touches a cross-instrument refusal.

### Minimal complete surface

Five artefacts, versioned together in one successor:

| # | Artefact | Change |
|---|---|---|
| 1 | `native-evidence.schemas.v2.json#/$defs/PrunedTreeV1` | → `PrunedTreeV2 {path, reason, markerCount: integer|null, markerCountBasis: "not-enumerated"|"observed-inventory"}`; `markerCount` null **iff** basis is `not-enumerated` |
| 2 | `security-lifecycle.schemas.v1.json#/schemas/DiscoveryProvenanceV1/properties/prunedTrees` (inline) | same row, version the owning record |
| 3 | `security-lifecycle.schemas.v1.json#/schemas/AdmittedBoundaryInventoryV1/properties/prunedTrees` (inline mirror) | same row; bump `schemaVersion` const 1 → 2 and the `AdmittedBoundaryInventoryV1` mirror in `native-evidence.schemas.v2.json` together |
| 4 | `discovery-defaults.py` — `enumerate_units` (producer) and `boundary_inventory_from_provenance` (converter) | anchors come from the admitted directory observation, not only from marker paths |
| 5 | `native_evidence_model.v2.py` — `discover_units` equality | replace whole-list equality with the subset rule below |

**Fix the domain mismatch while versioning:** native's `markerCount` is `integer 0..2^64-1`, security's is `I64NonNegative` (0..2^63-1). The mirrors must agree; `I64NonNegative` is the safer choice.

### Provenance-only comparison semantics

> Native no longer requires `boundaries.prunedTrees == marker_derived_pruned_trees`. Instead:
>
> 1. **Anchor subset.** Every anchor native derives from markers must appear in the admitted inventory with the same `reason`. A marker-derived anchor absent from the inventory is `native.boundary-inventory-mismatch` (unchanged severity — the security instrument saw fewer boundaries than the marker set implies).
> 2. **Extra admitted anchors are lawful.** An admitted anchor native cannot derive (no descendant marker observed) is **accepted and carried through**, never a mismatch. This is the whole point: a `node_modules` with no manifest inside it is still a pruned tree.
> 3. **Counts are provenance, never a comparison key.** `markerCount` and `markerCountBasis` are excluded from the equality predicate entirely. Comparing `not-enumerated` with `observed-inventory` is therefore not a question that arises — which is the only way to avoid an artificial refusal when one side enumerated and the other did not.
> 4. **Zero observed is not zero hidden.** `{basis: observed-inventory, markerCount: 0}` means "zero markers in the supplied inventory under this anchor", and must render as such. `{basis: not-enumerated, markerCount: null}` renders as unknown. Neither may render as "empty tree".
> 5. **Provenance-only, everywhere.** Neither field may enter source scope, unit selection, Coverage, Plan bounds, Run identity or any digest. State this for `markerCountBasis` as well as `markerCount` — the shipped proposal states it only for the count.

---

## 4. The four hard refinements

### 4.1 CR-02 — inference withdrawn; API selected (journal-first)

**Withdrawn:** my claim that journal-first "contradicts chapter 14's security public-API rule by exposing an unchecked journal checkpoint". Root is right. An opaque, non-cloneable, write-method-free guard is not a checkpoint: the level-4 append lock and the S6 re-read are taken *inside* the security call and never escape. I had conflated "holds an open DB transaction" with "holds an authority token".

**Retained, and it is a real specification gap:** step 4 mandates "If either acquisition fails, release the earlier transaction" without naming who holds the journal transaction across the evidence acquisition or by what API it is released. That is unimplementable as written.

**Selected API — journal-first (root's ordering, unchanged):**

```
// opensip-contracts  (both crates may depend on it; security must not depend on storage)
pub struct SealBinding { /* read-only accessors for the 13 association values */ }
pub enum EvidenceCommitOutcome { Committed, Undetermined }
pub trait SealedEvidenceCommit {
    /// Called at most once, under the held append lock, after the SEAL record
    /// and its COMMITTED witness are durable.
    fn commit_prepared(&mut self, bound: &SealBinding)
        -> Result<EvidenceCommitOutcome, EvidenceCommitError>;
}

// opensip-security
pub struct JournalWriteTxn<'s>(/* private */);        // !Clone !Copy !Default, no Serialize,
                                                      // no public write method, lifetime-bound to the session
impl<'s> JournalWriteTxn<'s> { pub fn abort(self); }  // the ONLY other public operation
impl<'s> Drop for JournalWriteTxn<'s> { /* rollback; fail-stop on leak */ }

pub fn begin_journal_txn<'s>(session: &'s CommitSession) -> Result<JournalWriteTxn<'s>, S7Busy>;
pub fn seal_under_append_lock(
    txn: JournalWriteTxn<'_>,            // consumed
    session: CommitSession,              // consumed  -> no further effect from this session
    replayed: &ReplayedRun,
    evidence: &mut dyn SealedEvidenceCommit,
) -> SealOutcome;                        // Committed | Undetermined | Refused{cause, sealDurable}
```

Why this satisfies every constraint you set:

- **Private SQL and session authority stay inaccessible.** The guard has no write method; the session is moved, not borrowed.
- **Security does not depend on storage.** The callback trait lives in `contracts`; security takes `&mut dyn SealedEvidenceCommit`.
- **Both transactions precede the append lock.** Storage: `begin_journal_txn` (L3) → open its own evidence transaction (L3) → `seal_under_append_lock` (takes L4 internally). If the evidence acquisition fails, storage calls `txn.abort()` — which is why `abort` must exist.
- **The callback cannot mint `PublishedCommit`.** It returns a plain enum. `PublishedCommit`'s constructor stays private to storage and is reachable only from storage's own `commit()` after `SealOutcome::Committed`.
- **The callback cannot bypass the S6 checkpoint.** It is unreachable except from inside `seal_under_append_lock`, after the checkpoint and after witness COMMITTED.
- **The association values come from the owners.** `SealBinding` is constructed only by security; storage reads the 13 values from it rather than asserting them — which is the plan's own stated requirement, now enforced by construction.

**Release / REV cleanup.** On a failed final checkpoint with SEAL already durable: latch fail-stop on the session; do **not** invoke the callback; return `Refused{sealDurable: true}`; security releases L4 on return; storage aborts its evidence transaction; then the host — with L4 released — calls a fresh `security::record_revocation(...)` which takes a new L3 journal transaction and then L4. No L3 is ever acquired under L4. The moved `CommitSession` guarantees no further effect from that session.

**Typed capacity refusal (answers CR-19).** `seal_under_append_lock` reads the tail under the already-open journal transaction, *before* taking L4. If `tail + 1 == 9007199254740991` it returns `Refused{cause: CarrierCapacityExhausted{grantGeneration, provenTailSeq}}` and appends nothing. Storage maps it to a typed storage error; host maps it to the D9 refusal and, **after releasing the operation lease**, routes a lifecycle `close_generation` that takes the fence and appends TERMINAL. This is F32 satisfied with an owner, and it needs no fence acquisition inside commit.

**Observer latching during the evidence commit syscall.** You are right that types cannot stop an in-flight syscall, and this case is currently unhandled — see **CR-23** below.

### 4.2 CR-08 — refined, and one new fact

Your objection is correct and the answer is narrower than I implied. Three source facts settle it:

1. The chain is `prev_sha256[k] = SHA256(body_sha256[k-1] ‖ (k-1))` (v1 §5.4 DDL comment), and `body_sha256[k] = SHA256(body[k])` is a **separate column**. Rewriting an interior body and fixing the successor's `prev_sha256` leaves the tail's `body_sha256` unchanged.
2. The contract says so itself: *"Hash chain. Tamper-evidence for audit, **not tamper-proof**; the chain head is in the witness."*
3. **New and load-bearing:** in the `PENDING n+1, tail n` state the witness's `bodySha256` names the record that was *never appended*. The prior `COMMITTED n` witness has been overwritten. **During a PENDING append the carrier has no live witnessed anchor for its durable prefix at all.** (The reconciliation table confirms the reading: the ADVANCE row compares hashes at `PENDING n = tail n`; the REVERT row at `PENDING n+1, tail n` compares nothing.)

So a walk "through k" proves nothing on its own, and neither does a walk to the tail when the witness is PENDING-ahead.

**The custody-qualified retained anchor that suffices is the SC-TRUST high-water record** `{project, grantGeneration, lastSeq, tailSha256}`. It is written under the **fence** at operation start and end, is never written under a lease, and is **not** overwritten by a PENDING witness. That is the only retained anchor that survives a later in-flight append.

> **Confirm-an-earlier-receipt predicate (read-only, no repair, no waiting):**
>
> Let `A` = the private association, `k = A.journalSeq`, `t` = observed journal tail, `W` = live witness, `H` = SC-TRUST high-water for `(A.journalCarrierDigest, A.grantGeneration)`.
>
> **Common checks (all required):** carrier naming — `W.projectKeyDigest == A.journalCarrierDigest` and `W.grantGeneration == A.grantGeneration`; contiguity of seq 1..t; chain consistency `prev_sha256[j] == SHA256(body_sha256[j-1] ‖ (j-1))` for all `j` in 2..t and `body_sha256[j] == SHA256(body[j])`; record join at `k` — `record_type == SEAL`, `body_sha256[k] == A.journalBodySha256`, `operationRef == A.operationRef`, record `runId == A.runId`; and `t >= H.lastSeq` (a lower tail is F22 quarantine, never a confirmation).
>
> **Anchor selection:**
> - `W` is **COMMITTED n** with `n == t` and `W.bodySha256 == body_sha256[t]` → anchor is the tail. Confirm for any `k ≤ t`.
> - `W` is **PENDING n == t** with `W.bodySha256 == body_sha256[t]` (journal durable, witness not yet advanced) → the witness still anchors the tail. **Confirm for any `k ≤ t`.** Report `witnessPendingAdvanceable` as diagnosis; perform no ADVANCE.
> - `W` is **PENDING n == t+1** (append not durable) → **no tail anchor exists.** Fall back to the SC-TRUST floor: confirm only if `k ≤ H.lastSeq` **and** `body_sha256[H.lastSeq] == H.tailSha256`. If `k > H.lastSeq`, the outcome is **`unknown`** — not confirmed, and explicitly **not** invalidated. The earlier committed prefix is never falsely invalidated by a newer PENDING append.
> - Any other witness state (`COMMITTED n > t`, equal seq different hash, non-adjacent PENDING, foreign carrier, malformed) → F20/F21/F22 quarantine/indeterminate.
>
> **No repair, no waiting:** no INIT/REVERT/ADVANCE, no witness write, no high-water raise, no lock acquisition, no wait on the writer.
>
> **Honest bound:** the conclusion class is **`confirmed-under-retained-custody`**, never "cryptographically proven". This establishes retained-carrier internal consistency plus non-rollback below the last *observed* floor. It does **not** detect a coherent whole-carrier rewrite performed while no operation was running with the witness and floor rewritten consistently — precisely the limit §5.4 "Detection bound (honest)" and §5.5 already state. Do not let the recovery prose imply more than the carrier provides.

### 4.3 CR-06 — **withdrawn as a defect**

Root is right on both sub-points, and the contract settles it. Identity §3 closes the representation vocabulary to four members, one of which is **`canonical-record` = "raw SHA256 of `C(record)`"** — i.e. raw SHA-256 over canonical bytes with no H framing is a first-class, already-registered representation. And the confusion risk I raised is precluded by rule, not by wording:

> "a raw canonical payload is never admissible [where `h-identity` is required], because `C(X)` does not begin with the framing prefix and `SHA256(C(X))` is not `H(D, X)`… Offering a frame where a `canonical-record` is required fails parsing; offering a payload where a frame is required fails the prefix."

Frame admission is exact (literal prefix, domain membership, declared length, byte-identical remainder, payload validates under the registered record). So confusion is governed by the **typed field annotation**, not by whether a digest is framed. `storeGenerationDigest` is a private storage column, never annotated `h-identity`, never in a semantic hash, never in a public schema; two bindings collide only on a SHA-256 collision. And using `C()` plus the one SHA-256 helper introduces **no second serializer** — my objection was about a second serializer and does not apply.

**Remaining, as precision (low, optional):** `StoreGenerationBindingV1` is not a *registered* record in any bundle, so it is not a `canonical-record` in the contract's sense either. State plainly that it is a **private local digest outside the four public representations**, that no `x-opensip-digest` annotation may name it, and that it carries no schema-major authority. If a discriminator is added, it must **not** reuse the `opensip.product.v1` prefix (that would make the value frame-shaped in a context expecting a frame); a distinct local literal such as `ASCII("opensip.local.store-generation.v1") ‖ 00 ‖ C(binding)` is safe and cheap. Adopt or skip — either is defensible.

### 4.4 COV-01 / CR-14 — root's proposal is compatible, with exact joins

Candidate25 **already specifies the syntax producer identity laws** (native §, the `native.semantic-universe.syntax.v2` section), which I had not surfaced in pass 1. Assessed against root's proposal:

**Compatible.** `closure2.kind` is a closed enum `['provider','evaluator','detector','toolchain','stdlib','rust-dev-llvm','grammar','adapter']` — `grammar` is already a member. Static linking of the parser code is an implementation placement choice; it does not conflict, **provided the `kind=grammar` closure identity and its retained tree still exist and are admitted**. "No new wire protocol, no dynamic executable loading" is consistent: the contract never asks for a syntax provider process, and it explicitly says the syntax context has "no toolchain, no stdlib, no lockfile, no `node_modules` layout and no config graph".

**Exact joins required (all already normative; the plan must name them):**

1. `native.context.syntax.v2` carries exactly one thing: the installed `SyntaxGrammarBundleV1`, an **admitted `kind=grammar` closure**, with `parserVersion == ` that closure manifest's `semanticVersion` (refusal `native.syntax-grammar-version-not-from-manifest`). **Do not collapse `parserVersion` into the host release version** — static linking makes that mistake easy.
2. Every grammar definition, the bundle manifest and the normalizer specification must be **present in the retained tree**. Since the default authoritative profile requires *replayable* retention at seal, those bytes must be committed as part of the producer closure, not merely compiled in.
3. The universe commits the admitted context **plus the selected grammar set**; a different selection is a different universe. Selection naming an unbundled grammar refuses `native.syntax-grammar-not-in-bundle`. Constant `resolutionAttempted=false` rides so no consumer reads it as a resolution claim.
4. Body dialect uses the `{grammarVariant}` branch. One suffix → one grammar (`native.syntax-grammar-suffix-ambiguous`), longest match, unbundled suffix → `unsupported-file` / `no-bundled-grammar`. **A grammar-parsed body never mints the same identity as a compiler-parsed one over the same bytes** — this is what `crates/host/src/syntax.rs`'s "bind code/data grammar distinctions" must implement.
5. Bundle is closed at **seven** languages / fourteen suffixes: `code` = rust, typescript, javascript (bear clone body identity and code-construct relations; `languageId` **must** be in the `body-language-version` enum); `data-document` = json, toml, markdown, yaml (inventory evidence only; mint no body identity; `languageId` **must not** be in that enum). Both directions refuse at bundle admission.
6. Capability is not widened: only inventory rungs, `syntactic` rungs and `clones@normalized-body-hash`. The registry is consulted **at every admitted fact** (`SYNTAX_CAPABILITY_UNSUPPORTED_FACT` when an anchor path's selected grammar lacks that `relation@rung`) and at the scope boundary — not only at descriptor validation.

**Architecture verdict.** With those joins, root's split is sound and my CR-14 concern is answered: a pure `crates/syntax` producer (contracts/identity only, byte inputs, no I/O ports) is the producer; `crates/host/src/syntax.rs` selects grammars and dispatches; `crates/host/src/fact_admission.rs` validates candidates against the universe/registry. The producer/admitter collapse I objected to is resolved by moving production out of the host crate. `crates/syntax` must be added to the inventory and to the pure-layer dependency rule in `check_repository_file_inventory.py`. **Third-party grammars:** they ride the same `kind=grammar` closure admission — signed manifest, TreeCommitment, `semanticVersion`, retained tree — so "existing exact artifact provenance rather than ambient plugins" is already the only admissible path; no new mechanism is needed. Note that adding a third-party grammar **changes the universe**, hence changes RunId, by design.

---

## 5. Task-4 joins (the omitted item)

### 5.1 Separate provider release and toolchains

The mechanism exists and needs no invention:

- **Identity.** `closure2 = H` over `{kind, manifestDigest, tree, semanticVersion, protocolMajor, platform}`. `kind ∈ {provider, evaluator, detector, toolchain, stdlib, rust-dev-llvm, grammar, adapter}`.
- **Authentication.** `opensip-signature-envelope.2`, subject `kind=manifest`, domain `opensip.metadata.manifest.1`, `storedSha256` equal to identity `closure.manifestDigest` (raw-artifact); plus catalog `opensip-catalog.1` `releases[] {manifestDigest, manifestPreimageSha256, envelopeDigest, artifacts[{platform, archiveProfileId, archiveDigest, sha256}]}` signed TR-INDEX.
- **Delivery selector.** `component-manifest-schemas.v11` `manifestSchema.platforms[]` (`os`, `arch`, `tree` TreeCommitment, `entrypoint`) with RJ-3 — **not** `DetectorManifestV1`, which is only `{schemaFamily, schemaMajor, compatibleClosures}` and must never occupy `closure.manifestDigest`.
- **Tree→identity projection.** `type=file` rows map to identity `Blob {path, sha256, bytes}`; `dir`/`symlink` stay delivery rows, are not identity members, are never followed. Mode bits stay on the TreeCommitment. Listing bytes are never executed.
- **Admission origins.** `trustOrigin ∈ {retained-generation, installed-signed-release, signed-closure-bundle}`.
- **Compatibility inheritance.** Listings inherit tree, platform and protocol **from the already-admitted `closure2`**, never from listing body fields.

**Toolchain separation is contract-bound, not a build preference.** `TypeScriptToolchainIdentityV1.compilerVersion` **must equal** the `semanticVersion` of the admitted signed compiler closure named by `toolClosure.closureId`; `compilerPackageDigest` is a member digest of that retained `kind=toolchain` tree; `typescriptStdlibMerkleRoot` is the bare 64-hex suffix of the admitted `kind=stdlib` `closure2`; `standardLibraryComponentDigests` is the **complete** `.d.ts` inventory, selected or not. Rust has the parallel `ToolchainIdentityV1` with `rustcDevLlvmDigest`.

**Consequences for chapter 14 / the build plan that must be written down:**
1. The provider's pinned `rust-toolchain.toml` / TS compiler version is simultaneously a **release-artifact decision** (it fixes `semanticVersion` on an admitted closure). "Select supported toolchain versions" is therefore not a free tool choice for the provider lane.
2. Independence is per-`protocolMajor`: `typescript-semantic` **2**, `rust-semantic` **3** (current; DR-G10's acceptance line saying "TS major 1 and Rust merged major 2" is inherited text, and its `productExpansion` correctly states "TS protocol major2 and Rust major3" — no defect, but the plan should not cite the acceptance line as the current majors).
3. DR-G14's expansion — "Bundled TS/JS and Rust analyzer/runtime/toolchain dependency closure on all four platform families… **no PATH/system runtime fallback**" — is the acceptance criterion for the "Rust workspace policy" and "TypeScript policy" sections. State that a provider build that resolves a compiler from `PATH` fails G14 regardless of whether the Rust workspace isolates cleanly.
4. The **platform key must be the machine vocabulary** (`linux-x86_64-gnu`, `linux-aarch64-gnu`, `macos-aarch64`, `macos-x86_64`) everywhere in release assembly — the same vocabulary whose absence from the inherited carrier is CR-04.

### 5.2 Schema generation and SDK reuse

- **One owner per contract, generation is downstream.** `schemas/registry.json` must key each entry by the schema document's **`raw-artifact`** digest — identity §3 defines `raw-artifact` as "raw SHA256 of the exact retained artifact bytes… a **complete registered schema document**". That is the join that prevents a schema change being laundered through a regenerated binding: the registry row names the exact document bytes, the generator closure and options, the output targets, and the **semantic validator owner** separately.
- **Generated types are shape, never admission.** Identity §3's exact-integer, duplicate-key and lexical-admission laws are the real gate; a generated Rust/TS carrier that parses through a permissive JSON layer has not admitted anything. The registry row must state, per target, whether the generated code performs exact admission (it must not be assumed to).
- **SDK reuse — decidable now, and the answer is "no shared SDK yet".** The two providers do not share a protocol: different majors (2 vs 3), different capability token sets, different context records (`TypeScriptNativeContextV2` vs `NativeContextV2`), different toolchain identity records. The only genuinely shared surfaces are the four identity tokens (`source-identity-snapshot2`, `plan-identity-plan2`, `fact-identity-fact2`, `coverage-v3`) and `HelloV3`/`HelloAckV3` framing. Those are already owned by `opensip-contracts` (Rust) and the generated TS protocol binding. **Recommendation: do not add a provider SDK package.** Revisit only if a third provider appears or the majors converge; the plan's "compare actual protocol obligations first" is satisfied — the comparison has now been done and it comes out negative.

### 5.3 Report asset closure owner — a real gap (**CR-24**)

`closure2.kind` is a **closed enum with no report/asset member**. The implementation plan's asset policy says a release "must fail assembly if its selected report asset closure is missing or incompatible" — using "closure" without saying which mechanism. There are only three consistent options and the plan must pick one:

| Option | Cost |
|---|---|
| (a) Add a `kind` member | Widens a **closed identity vocabulary** for a presentation artifact; schema-major decision; drags report assets into `closure2` identity for no semantic benefit |
| (b) Carry assets inside an existing kind's tree | Misuses `provider`/`adapter` semantics; the assets are not an analyzer |
| **(c) Release artifact, not a `closure2`** | **Recommended.** |

**Recommended (c):** the report asset bundle is a **release artifact** with its own manifest of exact asset bytes and a catalog `releases[].artifacts[]` row (`platform`-independent or per-platform as the bundle requires), verified by digest at assembly and again at load by `crates/reporting/src/assets.rs`. It is **not** a `closure2`, never enters identity, Run hashes, the native context or any semantic digest. Failure to verify at render time is the existing required-delivery operational failure (`DELIVERY.REQUIRED_FAILED`, exit 4) — never a silent degraded report. This keeps `assets.rs`'s stated responsibility ("versioned built report assets supplied by the signed release closure") truthful while leaving the closed identity vocabulary alone, and it needs no new signing scheme, consistent with the plan's own constraint.

### 5.4 What can safely remain a tool choice

You asked me to separate these, and most of them can.

**Behaviour fully specified — tool selection may be deferred to its milestone:**
- TS package manager and lock topology (behaviour: independent lane install/build, no cross-lane scripts or toolchains, offline input materialisation — build-lane table + enforcement item 3).
- Rust and TS dependency checkers (behaviour: the declared edge graph plus refusal of forbidden normal/build/dev/target/feature edges and provider-compiler leakage — enforcement items 1–2).
- Browser harness (behaviour: file-based offline open, blocked egress, no service worker, hostile text, large/partial payloads, keyboard/focus, optional-renderer loss — R01/R16/R17/R18 plus the tool-matrix acceptance column).
- Compile-fail harness (behaviour becomes fully specified once §4.1's API is fixed: raw DTO, forged receipt, cloned/reused session, leaked `JournalWriteTxn`, private-constructor attempts).
- Storage/process fault harness (behaviour: F00–F35 plus the new cases below).
- Release orchestration adapter (behaviour: exact inputs/outputs, signed assembly contract, licence/TCB inventory, no hidden downloads).
- Frontend framework and bundler (behaviour: R01–R24 plus no external fetch; size/startup are *measurement* obligations, not design blockers).

**Not yet a pure tool choice — a design decision is still owed:**
- **Schema generator + runtime validator.** Undecidable until `schemas/registry.json`'s row shape is fixed (§5.2): which digest keys a row, and where exact admission lives relative to generated shape validation. Fix the registry first, then "Typify vs custom" is answerable on evidence.
- **Provider toolchain versions.** Not free — see §5.1(1); they fix `semanticVersion` on an admitted closure.
- **Graph renderer.** The *library* is a tool choice; the accompanying product decisions (exact symbol identity keys, call-vs-import relation distinction, keyboard-accessible alternative per R18) are design and must precede it.

I have not treated any absent code as a blocker; every item above is a statement about design bytes that exist.

---

## 6. Prototype R01–R24 — now verified against source

All 44 files verified and read where relevant. Tests were treated as source evidence only.

**Claims confirmed exactly:**

| Claim | Evidence |
|---|---|
| R01 offline, no script-fetched data | Across all 44 files there is **exactly one** network-capable reference: a static `<a href="https://opensip.ai">` footer link in `generator.ts:329`. No `fetch`, `XMLHttpRequest`, `WebSocket`, CDN asset, `importScripts` or service worker |
| R04 message suppressed when a metric looks redundant | `session-detail.ts:43-44, 95-96` — "the finding message just repeats the file + the metric, so we DROP the Message column" |
| R09 formula-safe CSV | `view-coupling.ts:222-230` — leading `= + - @ TAB CR` neutralised with `'`, RFC-4180-ish quoting. Export carries **no** Run/view identity header, confirming the gap the disposition addresses |
| R11 body-hash collapse | `function-card.ts` keys on `graphIndexes.byBodyHash`. Refinement: line 264 already provides a non-collapsing qualified-occurrence entry point — the migration should preserve it, not rebuild it |
| R12 entry-point heuristic | `trace.ts` — "any function in `packages/cli/src/index.ts`, plus any exported function with no callers". The path is **hardcoded to the prototype's own repo**; the disposition is if anything understated |
| R14 built-in audit special case and 20-run cap | `report-history-selection.ts` throws `CLI.REPORT.RUN_UNAVAILABLE` (`change-impact-unavailable`) unless `name === 'audit' && source === 'built-in-suite'`; `report-compose.ts:133,136` `limit: 20` for sessions and runs. It also **already has no latest-run fallback** — it throws |
| R15 8 MiB budget | `bound-catalog.ts:48` `MAX_GRAPH_CATALOG_BYTES = 8_388_608`, with explicit `omittedFunctions` disclosure ("Truncation is a VISIBLE state, never a silent one") |
| R16 optional degradation | `graph-visualization-degradation.ts` has exactly **two** conditions (`catalog-projection-failed`, `renderer-asset-unavailable`); the proposed four-way absent/incompatible/corrupt/omitted split is a real expansion |
| R17 script-safe embedding | `script-context-json.ts` escapes `<`/`>` to `\u003c`/`\u003e` |
| R20 scheme allowlist and absolute-root disclosure | `editor-link.ts` — closed allowlist `{vscode, cursor}`, copy-path fallback, and the link **requires** an embedded absolute `PROJECT_ROOT` |
| R21 guarded opening | `open-report.ts` — opt-in, hard-skips json-mode, non-TTY, `CI`, SSH-without-display; launch failure never fails the run |
| Filter drawer removed | `filters.ts` header — "was removed — the Visualization view owns its own controls" |
| R24 tabs | `tool-tabs-registrations.ts` — `fitness`/`fit`, `simulation`/`sim`, `code-paths`/`graph`, `yagni`/`yagni`, plus a host-owned External Tools catch-all |

**Corrections and additions to the dispositions:**

- **CR-26 (new).** `filters.ts` exposes a module-level `filterState` with `includeTests: false` and the comment "Nothing mutates it now" — the Functions table and Coupling drilldown apply a **hidden, non-interactive default filter that silently drops test-file occurrences**. R07/R08 say results "describe the embedded projection only" but never flag this. A silent scope reduction with no visible control is exactly the class the completeness rules forbid. Required: either surface it as a visible, disclosed filter or remove the default; R07 and R08 must state the disposition.
- **CR-27 (new).** R24 blends four named tabs plus the external catch-all into one row and disposes only `simulation`. `fit` maps to the selected `fit` command and `graph` to the graph query operations, but **`yagni` has no selected command** and its mapping (to advisory candidates, via `candidates`/`inspect`/`review-brief`) is left implicit. Give R24 five explicit per-tab rows so no tab is silently dropped and `sim` is the only deferral. My pass-1 conclusion that the simulation deferral removes no product scope stands — `sim` has no selected contract.
- **R02 refinement.** `report-compose.ts` already has two behaviours worth preserving that the inventory does not name: a host-reserved top-level key set ("a tool that returns one is ignored with a warning"), and **bundled-vs-external isolation** (an external tool's `collectReportData` runs in a forked hook worker, "NEVER an in-host fallback"). A naive "host owns the projection" migration could regress the fork isolation. State both as required preserved properties.
- **R15 refinement.** Two further inherited numbers exist beyond the named 8 MiB: `MAX_CHANGE_IMPACT_MODELS_BYTES = 2_097_152` and the 20/20 history caps. Name all three in the measurement plan.
- **R20 refinement.** `generator.ts` takes `editorProtocol` and `projectRoot` as **independent** options (both default `null`). A caller can embed the absolute root with no link feature at all. Bind the disclosure to the enabled feature as one switch, default the shareable report to relative-path/copy-path, and surface the disclosure in the report.
- **R21 refinement.** `decideReportOpen` reads ambient `CI`, `SSH_CONNECTION`, `DISPLAY`, `WAYLAND_DISPLAY`. State that these become **admitted host presentation observations** (there is precedent: `DiscoveryProvenanceV1.ci`), not ambient inputs to any admission decision, and that the launcher is `crates/platform/src/process.rs`, not an npm dependency.
- **R17 optional hardening.** The escape set covers the `</script>` breakout but not U+2028/U+2029. Cheap to add for an artifact opened in arbitrary browsers.
- **CR-22 stands.** Five pinned files remain uncited, including `filters.ts` — which is now more clearly a defect, since it is the sole evidence for a stated migration boundary *and* the source of CR-26.

---

## 7. New findings this pass

- **CR-23 (medium-high, defect).** No fault case covers **an observer latch during or after the evidence-commit syscall**. F19 is scoped to "after SEAL but before evidence commit" and concludes `uncommitted`; F12 covers a commit-syscall error without a concurrent latch; F26 covers revocation after a *confirmed* commit. The gap in between would mislabel an already-linearised or durability-undetermined attempt as `uncommitted`. Required: (i) record a `linearizationPoint` at callback entry — a latch at or after it can never yield `refused`; (ii) commit confirmed → `committed`, with the latch refusing only *subsequent* effects, producing `committed-delivery-failed`; (iii) commit error or unconfirmed barrier → `durability-undetermined` with ExecutionId, no write retry, latch does not convert it to `uncommitted`; (iv) REV appended after L4 release must record the SEAL `journalSeq` and its evidence outcome so a later reader cannot read REV-after-SEAL as a refusal; (v) state plainly that the S6 observer bound bounds *admitting new effects*, not aborting an in-flight syscall.
- **CR-24 (medium, defect).** Report asset "closure" is unowned — `closure2.kind` is closed with no asset member. See §5.3; recommend option (c).
- **CR-25 (medium, defect).** A known pruned anchor with **no descendant marker** is invisible in all three artefacts (demonstrated). Must be reported with `markerCountBasis: not-enumerated`, never waived.
- **CR-26 (medium, defect in the disposition).** Hidden `includeTests: false` default filter, unflagged in R07/R08.
- **CR-27 (low, defect in the disposition).** R24 needs per-tab rows; `yagni` mapping is implicit.

## 8. Status of all 27 findings

| Status | IDs |
|---|---|
| **Withdrawn** | CR-06 (defect claim; residual precision only), CR-12(b) |
| **Refined** | CR-02 (inference withdrawn, specification gap retained, API selected), CR-08 (strengthened with the PENDING-n+1 anchor fact), CR-12(a) (pre-existing gap, not a regression), CR-14 (root's proposal compatible; joins now exact), CR-19 (owner named in §4.1) |
| **Upgraded to executed evidence** | CR-10, CR-11, CR-13, CR-04 (pass 1), CR-18 (pass 1) |
| **Unchanged and open** | CR-01, CR-03, CR-05, CR-07, CR-09, CR-15, CR-16, CR-17, CR-20, CR-21, CR-22 |
| **New** | CR-23, CR-24, CR-25, CR-26, CR-27 |

Blocking set for the commit/recovery section is now **CR-01, CR-03, CR-04, CR-05, CR-07, CR-23** (CR-02 downgraded to a specification gap with a selected remedy). Blocking for XA is **CR-10** (golden release) and **CR-25** (pruned-anchor waiver); CR-12 is no longer blocking.

## 9. Remaining limits

- The prototype delivery is 44 files, the report surface only. The R01 "no network" result is scoped to those 44 files; I cannot speak for the rest of the prototype. No prototype execution was performed — tests were read as intent, not result.
- Codex's git-object verification is recorded, not reproduced: no git repository was present and the manifest carries no blob SHA-1.
- I excluded `design-corrections/reviews` from the scratch copy (restoring the six pinned files the ledger needs). Every probe I ran passed, but a probe depending on other review-tree bytes would not have been exercised.
- The `codex-author-followup.v2` package remains **PENDING**: I used `check-export.v4.py`, `checkpoint3/` and `query-checks1/purged.json` as probe fixtures only. Its seven Runs, three negative controls and thirty residuals are unreviewed and unaccepted.
- I did not re-run the author's 464/375/412 reference-check counts; the discovery and query probes are what I reproduced.
- Nothing here establishes OS durability, process isolation, compiler correctness, browser behaviour, accessibility or any gate qualification.

---

```json
{
  "pass": "claude-return-followup.v1",
  "continues": "eaa8276c-dc65-4d26-8ca2-703b345698f9",
  "bindings": {
    "inputManifestSha256": "da22d2d59f09227a4eafc58821af58e5a96ccc3e4be91b41fbe6b54bef29792b",
    "candidateManifestSha256": "fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d",
    "prototypeManifestSha256": "b82bfb921494d9d41da661c434b18811b9b50da7149eb818e4ab9433e085407e",
    "prototypeCommit": "a62509d623173155d0946e9f5d5ca90c839893e0",
    "prototypeFilesVerified": "44/44 sha256+bytes, 44/44 equal to implementation-planning-sources.v1.json pins",
    "gitBlobVerification": "recorded from Codex, not reproduced (no git repository present; manifest carries no blob sha1)"
  },
  "standing": {
    "acceptanceOfChangedBytes": false,
    "readiness": false,
    "blindConsumerAcceptance": false,
    "finalApplicationAcceptance": false,
    "codexAuthorFollowupV2": "PENDING - used only as probe fixtures"
  },
  "executedEvidence": [
    {"probe": "probe-discovery.py --source frozen25", "result": "PASS; output byte-identical to shipped discovery-observations.json", "artifact": "scratch/out/original.json"},
    {"probe": "apply-reference-correction.py", "result": "PASS; changed-source rows equal shipped; all three afterSha256 reproduce", "artifact": "scratch/out/proposal/changed-source.json"},
    {"probe": "rebind-author-pins.py", "result": "PASS; 6 pin changes equal to shipped author-pin-delta.json", "artifact": "scratch/out/pin-delta.json"},
    {"probe": "probe-discovery.py --expect-corrected", "result": "PASS; observations equal shipped discovery-corrected.json", "artifact": "scratch/out/corrected.json"},
    {"probe": "probe-query-availability.py --source frozen25", "result": "PASS; observations and runId equal shipped", "artifact": "scratch/out/query-avail.json"},
    {"probe": "probe-op-scope.py (20 operations, availability=purged and retained control)", "result": "17 non-graph ops refuse at exit 2 QUERY.PARAMS_MALFORMED under purged AND retained; only graph ops reach observe_availability", "artifact": "scratch/out/op-scope.json"},
    {"probe": "probe-graph3.py (3 graph ops x 5 availability states)", "result": "all three return on retained; all three exit 4 HOST.IO_FAILURE on purged/expired/corrupt/unavailable", "artifact": "scratch/out/graph3.json"},
    {"probe": "probe-cr12.py (security -> boundary_inventory -> native, both trees)", "result": "corrected tree: security 4051 == native 4051 for 150 dir-custody, 150 marker-custody and 75/75 mixed; frozen25 refuses all at enumerate_units", "artifact": "scratch/out/cr12-frozen25.json, scratch/out/cr12-corrected.json"},
    {"probe": "probe-composition.py", "result": "custody150 with boundary 4051==4051; without boundary native.too-many-units. depth300 with boundary 4==4; without boundary 5", "artifact": "scratch/out/composition.json"},
    {"probe": "probe-workbound.py (enumerate_units, both trees)", "result": "frozen25 at 200k markers: 0.549s / 23.8MiB peak then refuses; corrected enforce_limit=True identical (0.557s / 23.8MiB). Cap was never an input-work bound", "artifact": "scratch/out/workbound-*.json"},
    {"probe": "probe-walkwork.py (S.discovery, both trees)", "result": "identical refusal details; corrected costs ~2.3x time and ~2.2x peak at 60k dirs (0.487s/10.8MiB vs 1.109s/23.5MiB), linear in the same dimension", "artifact": "scratch/out/walkwork-*.json"},
    {"probe": "probe-xa02.py", "result": "node_modules present with no descendant marker (and with only non-marker files) yields prunedTrees [] in security, boundary inventory and native; tampering markerCount yields native.boundary-inventory-mismatch", "artifact": "scratch/out/xa02.json"},
    {"probe": "prototype network scan (44 files)", "result": "exactly one network-capable reference: static footer link generator.ts:329; no fetch/XHR/WebSocket/CDN/service worker"}
  ],
  "dispositionChanges": [
    {"id": "CR-02", "change": "refined", "withdrawn": "the inference that journal-first exposes an unchecked journal checkpoint and contradicts chapter 14's security public-API rule", "retained": "the specification gap: step 4 mandates releasing the earlier transaction without naming an owner or an API", "selectedRemedy": "journal-first with an opaque lifetime-bound non-cloneable JournalWriteTxn exposing only abort(self), plus a contracts-owned SealedEvidenceCommit callback returning a plain enum; SealBinding constructed only by security; PublishedCommit constructor stays private to storage", "severityNow": "medium (specification gap, not architectural violation)"},
    {"id": "CR-06", "change": "withdrawn-as-defect", "reason": "identity S3's closed representation vocabulary already includes canonical-record = raw SHA256 of C(record); frame admission is exact so SHA256(C(X)) can never be accepted where h-identity is required, and vice versa; confusion is governed by the typed field annotation. Using C() plus the one SHA-256 helper introduces no second serializer", "residual": "state that StoreGenerationBindingV1 is a private local digest outside the four public representations and that no x-opensip-digest annotation may name it; any optional discriminator must not reuse the opensip.product.v1 prefix", "severityNow": "low (optional hardening)"},
    {"id": "CR-08", "change": "refined-and-strengthened", "newFact": "in the PENDING n+1 / tail n state the witness bodySha256 names a record that was never appended and the prior COMMITTED witness is overwritten, so the carrier has no live witnessed anchor for its durable prefix", "remedy": "confirm-an-earlier-receipt predicate with three witness cases; SC-TRUST high-water {project, grantGeneration, lastSeq, tailSha256} is the custody-qualified retained anchor for the PENDING n+1 case; k > high-water lastSeq yields unknown, never invalidation", "honestBound": "confirmed-under-retained-custody only; a coherent whole-carrier rewrite while no operation was running remains undetectable per S5.4/S5.5"},
    {"id": "CR-12", "change": "split", "partA": "refined - enforce_limit=False removes no input-work bound (frozen25 already materialises and sorts before the cardinality check); the missing bound is a pre-existing host-observation admission gap; the patch adds only a bounded ~2.2x downstream custody-walk factor", "partB": "WITHDRAWN - empirically refuted; boundary_inventory_from_provenance exports custody/depth exclusions and native consumes them, so security and native agree exactly", "residual": "CR-12-prime, optional hardening: make boundaries non-optional on the authoritative host path", "severityNow": "low; no longer blocking"},
    {"id": "CR-14", "change": "refined", "assessment": "root's pure crates/syntax producer with statically linked grammar code is COMPATIBLE; closure2.kind already contains 'grammar'; static linking is a placement choice provided the kind=grammar closure identity, retained tree and parserVersion==manifest semanticVersion still exist", "requiredJoins": 6, "additionalRequirement": "add crates/syntax to the inventory and to the pure-layer dependency rule in check_repository_file_inventory.py"},
    {"id": "CR-19", "change": "refined", "remedy": "seal_under_append_lock detects the reserved terminal slot before taking level 4 and returns Refused{CarrierCapacityExhausted}; host routes lifecycle close_generation after releasing the operation lease"},
    {"id": "CR-10", "change": "confirmed-by-execution"},
    {"id": "CR-11", "change": "confirmed-by-execution"},
    {"id": "CR-13", "change": "confirmed-by-execution", "evidence": "markerCount tamper yields native.boundary-inventory-mismatch"}
  ],
  "newFindings": [
    {
      "id": "CR-23",
      "severity": "medium-high",
      "class": "defect",
      "path": "inputs/docs/v2/architecture/commit-recovery-plan.v1.json (cases F12, F19, F26); implementation-boundaries-and-build-plan.md 'Publication sequence and lock discipline' steps 5-6",
      "evidence": "F19 is scoped to 'after SEAL but before evidence commit' and concludes uncommitted. F12 covers a commit-syscall error without a concurrent latch. F26 covers revocation after a CONFIRMED commit. No case covers an observer latch during or after the evidence-commit syscall, where the SEAL is durable, the witness is COMMITTED and the attempt is already linearized at the journal because REV cannot be appended while level 4 is held.",
      "correction": "Record a linearizationPoint at callback entry; a latch at or after it can never yield refused. Commit confirmed -> committed, with the latch refusing only subsequent effects (committed-delivery-failed). Commit error or unconfirmed barrier -> durability-undetermined with ExecutionId, no write retry, and the latch does not convert it to uncommitted. REV appended after level-4 release must record the SEAL journalSeq and its evidence outcome. State that the S6 observer bound bounds admitting new effects, not aborting an in-flight syscall.",
      "status": "open-blocking"
    },
    {
      "id": "CR-24",
      "severity": "medium",
      "class": "defect",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md 'Asset policy'; chapter 14 crates/reporting/src/assets.rs row",
      "evidence": "identity-schemas.v3.json $defs/closure/properties/kind is a closed enum ['provider','evaluator','detector','toolchain','stdlib','rust-dev-llvm','grammar','adapter'] with no report or asset member. The plan requires a release to 'fail assembly if its selected report asset closure is missing or incompatible' without naming the mechanism.",
      "correction": "Select option (c): the report asset bundle is a release artifact with its own manifest of exact asset bytes and a catalog releases[].artifacts[] row, verified at assembly and at load by crates/reporting/src/assets.rs. It is NOT a closure2 and never enters identity, Run hashes, the native context or any semantic digest. Load-time verification failure is DELIVERY.REQUIRED_FAILED exit 4. Do not widen the closed kind vocabulary for a presentation artifact.",
      "status": "open"
    },
    {
      "id": "CR-25",
      "severity": "medium",
      "class": "defect",
      "path": "candidate25 docs/coop/design-corrections/discovery-defaults.py enumerate_units; security-and-lifecycle.md S3 pruned-tree paragraph; crosscut design-corrections.proposed.md section XA-02",
      "evidence": "Executed: a node_modules directory present in fs with no descendant marker, and one containing only non-marker files, both yield prunedTrees [] in DiscoveryProvenanceV1, in AdmittedBoundaryInventoryV1 and in native UnitDiscoveryV1. The known pruned anchor is silently absent rather than reported with an unknown count.",
      "correction": "Anchors must come from the admitted bounded directory observation, not only from marker paths. A pruned anchor with no observed descendant marker is reported with markerCountBasis 'not-enumerated' and markerCount null. Never waive a known anchor because no descendant marker was observed.",
      "status": "open-blocking"
    },
    {
      "id": "CR-26",
      "severity": "medium",
      "class": "defect-in-disposition",
      "path": "inputs/docs/v2/architecture/prototype-report-inventory.md R07 and R08",
      "evidence": "prototype packages/dashboard/src/client/filters.ts declares a module-level filterState with includeTests:false and states 'Nothing mutates it now'; passesFilter is applied by the Functions view and the Coupling drilldown. Test-file occurrences are silently dropped with no visible control. R07 and R08 do not flag it.",
      "correction": "Either surface it as a visible, disclosed filter or remove the default. State the disposition explicitly in R07 and R08; a silent scope reduction with no control is the class the completeness rules forbid.",
      "status": "open"
    },
    {
      "id": "CR-27",
      "severity": "low",
      "class": "defect-in-disposition",
      "path": "inputs/docs/v2/architecture/prototype-report-inventory.md R24",
      "evidence": "tool-tabs-registrations.ts declares four first-party tabs (fitness/fit, simulation/sim, code-paths/graph, yagni/yagni) plus a host-owned External Tools catch-all. R24 blends them into one row and disposes only simulation. 'fit' and graph query operations are selected product capabilities; 'yagni' has no selected command and its mapping to advisory candidates is implicit.",
      "correction": "Give R24 five explicit per-tab rows (four named tabs plus the external catch-all) so no tab is silently dropped and sim is the only deferral. Name yagni's mapping to the advisory candidate/inspect/review-brief surfaces.",
      "status": "open"
    }
  ],
  "task4Joins": {
    "providerReleaseAndToolchains": {
      "identity": "closure2 = H over {kind, manifestDigest, tree, semanticVersion, protocolMajor, platform}",
      "authentication": "opensip-signature-envelope.2 subject kind=manifest domain opensip.metadata.manifest.1 storedSha256 == closure.manifestDigest, plus catalog opensip-catalog.1 releases[] signed TR-INDEX",
      "deliverySelector": "component-manifest-schemas.v11 manifestSchema.platforms[] (os, arch, tree TreeCommitment, entrypoint) with RJ-3; never DetectorManifestV1",
      "treeProjection": "type=file rows map to identity Blob {path, sha256, bytes}; dir and symlink stay delivery rows, never identity members, never followed; mode bits stay on the TreeCommitment; listing bytes never executed",
      "trustOrigins": ["retained-generation", "installed-signed-release", "signed-closure-bundle"],
      "toolchainBinding": "TypeScriptToolchainIdentityV1.compilerVersion == semanticVersion of the admitted signed compiler closure named by toolClosure.closureId; compilerPackageDigest is a member digest of that retained kind=toolchain tree; typescriptStdlibMerkleRoot is the bare 64-hex suffix of the admitted kind=stdlib closure2; standardLibraryComponentDigests is the complete .d.ts inventory. Rust parallel via ToolchainIdentityV1.rustcDevLlvmDigest",
      "currentProtocolMajors": {"typescript-semantic": 2, "rust-semantic": 3, "note": "DR-G10's inherited acceptance line says TS 1 / Rust 2; its productExpansion correctly states TS 2 / Rust 3. No defect; do not cite the acceptance line as current"},
      "consequence": "provider toolchain version selection is simultaneously a release-artifact decision and is not a free tool choice; DR-G14 requires no PATH or system runtime fallback; the platform key must be the machine vocabulary throughout release assembly"
    },
    "schemaGenerationAndSdkReuse": {
      "registryKey": "each schemas/registry.json row keys the schema document by its identity raw-artifact digest (raw SHA256 of the complete registered schema document bytes)",
      "separation": "generated carriers provide shape only; exact-integer, duplicate-key and lexical admission remain the identity S3 gate and the semantic validator owner is a separate registry column",
      "sdkDecision": "DO NOT add a provider SDK package. The two providers share no protocol (majors 2 vs 3, different capability token sets, different context and toolchain identity records). The only shared surfaces are the four identity tokens (source-identity-snapshot2, plan-identity-plan2, fact-identity-fact2, coverage-v3) and HelloV3/HelloAckV3 framing, already owned by opensip-contracts and the generated TS binding. Revisit only on a third provider or converged majors."
    },
    "reportAssetClosure": {"finding": "CR-24", "recommendation": "release artifact with catalog artifacts[] row; not a closure2; never in identity"}
  },
  "toolChoicesSafeToDefer": [
    "TS package manager and lock topology",
    "Rust and TS dependency checkers",
    "browser harness",
    "compile-fail harness (once the CR-02 API is fixed)",
    "storage and process fault harness",
    "release orchestration adapter",
    "frontend framework and bundler"
  ],
  "decisionsStillOwedBeforeToolSelection": [
    "schemas/registry.json row shape - which digest keys a row and where exact admission lives relative to generated shape validation; blocks the schema generator and runtime validator choice",
    "provider toolchain versions - fix semanticVersion on an admitted closure, not a free choice",
    "graph renderer product decisions - exact symbol identity keys, call-vs-import relation distinction, keyboard-accessible alternative (R18) - must precede library selection"
  ],
  "prototypeVerification": {
    "confirmedExactly": ["R01", "R04", "R09", "R11", "R12", "R14", "R15", "R16", "R17", "R20", "R21", "R24-tab-inventory", "filter-drawer-removal"],
    "refinementsRequired": {
      "R02": "name the existing host-reserved key guard and the bundled-vs-external fork isolation as required preserved properties",
      "R11": "the prototype already has a non-collapsing qualified-occurrence entry point; preserve rather than rebuild",
      "R15": "name all three inherited numbers: 8 MiB catalog, 2 MiB change-impact, 20/20 history caps",
      "R17": "optional hardening - add U+2028/U+2029 to the escape set",
      "R20": "editorProtocol and projectRoot are independent options; bind the absolute-root disclosure to the enabled feature as one switch and surface it in the report",
      "R21": "state that CI/SSH_CONNECTION/DISPLAY/WAYLAND_DISPLAY reads become admitted host presentation observations, and that the launcher is crates/platform/src/process.rs not an npm dependency"
    },
    "newDefects": ["CR-26", "CR-27"],
    "executionPerformed": false
  },
  "findingStatus": {
    "withdrawn": ["CR-06 (defect claim)", "CR-12b"],
    "refined": ["CR-02", "CR-08", "CR-12a", "CR-14", "CR-19"],
    "confirmedByExecution": ["CR-10", "CR-11", "CR-13"],
    "unchangedOpen": ["CR-01", "CR-03", "CR-04", "CR-05", "CR-07", "CR-09", "CR-15", "CR-16", "CR-17", "CR-18", "CR-20", "CR-21", "CR-22"],
    "new": ["CR-23", "CR-24", "CR-25", "CR-26", "CR-27"],
    "blockingNow": ["CR-01", "CR-03", "CR-04", "CR-05", "CR-07", "CR-10", "CR-23", "CR-25"],
    "totalTracked": 27
  },
  "limits": [
    "prototype delivery is the 44-file report surface only; the no-network result is scoped to those files",
    "no prototype execution; tests read as intent, not result",
    "git blob verification recorded from Codex, not reproduced",
    "scratch copy excluded design-corrections/reviews (six pinned files restored); a probe depending on other review-tree bytes was not exercised",
    "codex-author-followup.v2 used only as probe fixtures; its seven Runs, three negative controls and thirty residuals remain unreviewed and unaccepted",
    "the author's 464/375/412 reference-check counts were not re-run",
    "no OS durability, process isolation, compiler correctness, browser, accessibility or gate qualification is established"
  ]
}
```

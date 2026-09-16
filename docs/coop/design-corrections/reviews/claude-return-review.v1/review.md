# Independent NONBLIND Review — OpenSIP architecture/design author delta (first pass)

**Bindings.** input-manifest SHA-256 `da22d2d59f09227a4eafc58821af58e5a96ccc3e4be91b41fbe6b54bef29792b` (matches `verification.json`); candidate25 manifest SHA-256 `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d` (matches the prompt and `implementation-planning-sources.v1.json`). I independently re-hashed all **136/136** input files (0 bad, 0 missing) and all **15/15** selected candidate25 sources against both the frozen snapshot on disk and the candidate manifest (all OK). The `codex-author-followup.v2/source-manifest.json` is byte-identical to the candidate manifest. Nothing frozen was modified; all work was done in `scratch/`.

**Verdict on this delta: not acceptable as a completed delta; acceptable in direction.** The layout work, the two-prerequisite commit API, the 13-field private association and the F00–F35 inventory are substantive and mostly well-grounded in the selected sources. Both checkers pass and reject meaningful negative controls. But five blocking findings sit in the commit/recovery core (CR-01…CR-05) and two in the XA dispositions (CR-10, CR-12). No product qualification is claimed or implied by anything below.

---

## 1. What I executed

Both checkers pass on a scratch copy of `inputs/` (with the candidate manifest placed at the path the checker expects):

```
PASS: 190 unique paths, naming/ownership checks, acyclic package dependencies, chapter matches
PASS: 320 source-bound mappings, 36 planned failure cases, private schema, owners and generated plan
```

I then ran my own controls rather than trusting the author's counts.

- **Inventory checker — 8/8 controls rejected**: cycle `storage→host`; `evaluator→storage`; factory suffix dropped; file assigned to a non-most-specific package; blank responsibility; generated file outside `generated/`; duplicate path; and a semantically wrong-but-legal role (caught only as generated-table drift, which is the correct limit).
- **Planning checker — 12 controls, 11 rejected on their merits**: `M7`; `executionStanding: executed`; `journalSeq` max raised to the reserved terminal slot; dropped `operationRef`; `additionalProperties: true`; `commitSequence` as `integer`; owner outside the inventory; gate qualification before M6; rewritten golden exit code; tampered working-tree source; tampered subject manifest. The 12th (absurd gate owner) is caught only as rendered-table drift.
- **Demonstrated checker limits (all ACCEPTED)**: `queryOperations:graph.path` owned by `docs/README.md`; a `planned-behavioral-test` whose `verification.owner` is `docs/README.md` with `method: "look at it"`; `DR-G11` owned by `docs/README.md` after `--write`; `analyze` moved M3→M1 after `--write`. See **CR-17**.
- **SQLite probe on the frozen carrier DDL** (`security-schemas.v2/grant-journal.sql`) — see **CR-04**.
- **SQLite probe on the proposed association table** — see **CR-18**.
- **Could not execute** the candidate25 Python reference models: `jsonschema` is absent (Python 3.14.6, no network). `probe-discovery.py` and `probe-query-availability.py` were therefore **not re-run**; XA-01/XA-03 reference behavior was established by exact source reading plus mechanical call-order extraction. The crosscut README's `464/375/412` reference-check counts are **unverified by me**.

---

## 2. Lock ordering, two-carrier crash protocol, witness/high-water, recovery

**The protocol is coherent in outline and does not deadlock**, because S7 makes level 3 non-waiting (`BEGIN IMMEDIATE, busy_timeout 0`). Holding level 4 through the evidence commit genuinely strengthens S6 linearization ("after `REV` no … `SEAL` is appended"). Witness handling is correctly aligned with §5.4: reconciliation stays at operation open under the fence, read-only paths report *would-REVERT*/*would-ADVANCE* only, and no SC-TRUST high-water is raised during commit. The `journalSeq ≤ 9007199254740990` cap is the right reading of "the grant-journal `seq` alone is uint53" plus the reserved terminal slot, against the broader `I64Positive` in the schema-3 record.

**But it is not complete, and one framing claim is false.**

- **CR-01 (high).** The plan states it "does not change … the required commit order". Identity §5's commit order is four steps with **no journal SEAL phase**, and says "A failure before step 3 publishes no authoritative Run." The proposal inserts a durable SEAL plus two witness barriers between steps 2 and 3, creating a durable artifact (an orphan SEAL) that identity §5 does not contemplate. This is an *extension* requiring a frozen, reviewed normative amendment — which the plan is willing to do elsewhere, but the summary claim must be withdrawn.
- **CR-02 (high).** "Grant-journal first, evidence ledger second, then level 4" forces storage (the coordinator) to hold a security-owned journal write transaction across its own critical section — against chapter 14's rule that security must "never expose an unchecked operational grant or journal checkpoint". Because both level-3 acquisitions are non-waiting **and target different databases**, the intra-level-3 order buys nothing for deadlock freedom. Invert control instead (see the correction in the JSON).
- **CR-03 (high).** Level 4 is an in-process mutex held across a journal `F_FULLFSYNC`, a witness write+barrier and the evidence commit+barrier. S6 requires the observer to append `REV(observer-fail-stop)` on a 5 s tick / 10 s staleness discipline. The plan honestly notes it "cannot bound an OS syscall" but never says what the *observer* does when it cannot take the lock. It must latch fail-stop outside the lock; the writer's F19 recheck must read that latch, not only the counter.
- **CR-07 (medium-high).** Read-only recovery's cross-carrier read order is unspecified, and the natural order produces a false contradiction: the writer makes SEAL(k) durable *before* the evidence commit, so a reader sampling the journal first and the ledger second can observe tail `k-1` together with a committed receipt naming `journalSeq = k` — a state the writer never produced.
- **CR-08 (medium).** "Snapshot readers verify its retained durable prefix" is asserted but undefined. §5.4's witness certifies only the tail; SC-TRUST certifies the last observed boundary. Neither certifies interior seq *k*.
- **CR-09 (medium).** No case covers an orphan SEAL surviving into later operations. `admit_analysis_seal` validates a SEAL record without consulting the evidence ledger, so that boundary alone would admit it.

**Numbers and domains check out** against the sources: `commitSequence` 0..2⁶⁴−1, `namespaceId` 1..4096, `executionId ^exec1_[0-9a-f]{32}$`, `runId ^run3:[0-9a-f]{64}$`, `grantGeneration` i64-positive — all exact. One exception, **CR-05**: `StoreGenerationBindingV1.stateSchema` is specified as `1..2^64-1` while the owning contract's `$defs/StateSchema` is a closed `{1, 2}` enum, and the binding introduces a random `storeInstanceId` alongside — without reconciling — the contract's existing `from/toStoreGeneration` (`I64NonNegative`, admitted under S9.2 with `CURRENT_STORE_MISMATCH`).

---

## 3. COV-03 is real, and understated

Executed against the frozen inherited DDL:

```
1. current schema-3 SEAL record      -> REJECTED: CHECK record_type IN (...)   [no SEAL]
2. GRANT platform linux-x86_64-gnu   -> REJECTED: CHECK platform IN (...)
3. GRANT platform macos-aarch64      -> REJECTED
4. GRANT platform linux-aarch64-gnu  -> REJECTED
5. GRANT platform macos-x86_64       -> ACCEPTED   (display alias)
6. GRANT platform macos-arm64        -> ACCEPTED   (display alias)
```

`PlatformProfileSetV1` states the ONE machine vocabulary is `linux-aarch64-gnu, linux-x86_64-gnu, macos-aarch64, macos-x86_64` and that "display aliases (macos-arm64, linux-x86_64, linux-arm64) **never key it**". So the carrier blocks **ordinary GRANT appends on three of four supported platforms**, not just SEAL. Separately, neither `JournalRecord` (schema 3) nor `JournalRecordV2` defines `TERMINAL`/`CHECKPOINT`/`MIGRATION`/`NARROW`/`EXPIRY`/`AUD`, yet §5.4 WA-13 requires `TERMINAL` for the uint53 rollover and F32 depends on it. The same stale DDL is embedded in `security_unit_lib_v8.py`. See **CR-04**.

---

## 4. Explicit dispositions

| Item | Disposition |
|---|---|
| **XA-01** | **CONFIRMED, required.** Genuine contract/reference divergence: S3 caps "**first-party** unit directories" and says nested repositories/projects are "never entered", yet `enumerate_units` caps before `_boundary_hit`/nested exclusion (native line 3600) and before the nested-repo/nested-project/depth/custody loop (security line 733). The three-file reference proposal's `beforeSha256` values match candidate25 exactly, the `afterSha256` values match the shipped files, and my independent diff shows **only** the three patch hunks — nothing hidden. **Not accepted as final:** two gaps remain (**CR-12**) — the cap becomes an output bound with no input bound (both real callers pass `enforce_limit=False`), and the two instruments now count at *different stages*, so a repo with 4200 marker dirs of which 150 fail custody admits in security (4050) and refuses in native (4200) — the same admit/refuse split XA-01 exists to remove. |
| **XA-02** | **CONFIRMED as a real prose/feasibility gap; advisory severity agreed.** S3 promises the pruned anchor carries "the number of markers it hid" while also promising no walk of that tree; the reference count is exact only over a supplied inventory (0/1/4200 in → 0/1/4200 out). The `{path, reason, markerCount, markerCountBasis}` row is sound. **Not integrated**; two requirements missing (**CR-13**): `prunedTrees` participates in the cross-instrument equality check (`native.boundary-inventory-mismatch`) and in provenance digests, so both records plus the equality rule must be versioned together with a defined `not-enumerated` vs `observed-inventory` comparison; and `markerCountBasis` (not just the count) must be declared provenance-only. |
| **XA-03** | **Underlying ambiguity CONFIRMED; the author's scoping is WRONG.** The genuine residue is narrow and real: `observe_availability` runs *before* `close_retained_run`, so for `graph.neighbors|path|reach` a known-unavailable observation is made "before evaluation" — which identity §5's literal words assign exit 2, while §7 returns exit 4. Amend identity §5, naming the exact three operations (`$defs/GraphOperation`), not "explicit graph operations". **Reject the golden overlap claim (CR-10):** `query-projection-contract.v3` line 5 says "`finding.show` remains `workflow_projection_model.v3.query_finding`"; workflows §8 says the graph contract "does not replace the artifact-specific owners of the other seventeen operations"; and mechanically, `GRAPH_OPS` (line 43) = the three graph ops, `_validate_request` refuses everything else (line 1227), and `execute_graph_query` calls it (1445) **before** `observe_availability` (1452). `finding.show` can never reach the availability route. The author's own `queryOperations` flags are correctly scoped to the three graph ops — flagging a `finding.show` golden is internally inconsistent. Release the golden from the hold. **Also (CR-11):** `availability.show` must not inherit the refusal — identity §5 says query of the retained manifest after purge "states evidence unavailable"; refusing would make availability unqueryable exactly when it matters. |
| **COV-01** | **CONFIRMED gap; routing accepted as interim, backend NOT resolved.** `syntax`, `clones-fact`, `clones-near` are `SUPPORTED-DESIGN` in `syntax-only` with no prior file owner. But `crates/host/src/syntax.rs` makes the host both **producer and admitter** of syntax/clone facts, collapsing the separation `fact_admission.rs` exists to enforce — the matrix draws the "produced by host" distinction only for `inventory`. **CR-14** is required before M3. |
| **COV-02** | **CONFIRMED exactly.** Four `cli` example strings carry `run2:` (`baseline adopt`, `repair preview`, `test run`, `purge`); the file contains 4 `run2` occurrences and 1 `run3`. Disposition accepted: correct in a reviewed successor, never edit candidate25, infer no run2 admission. |
| **COV-03** | **CONFIRMED and understated** — see §3 and **CR-04**. |
| **R24 (simulation)** | **Deferral acceptable.** No `simulation`/`fitness`/`YAGNI` capability exists anywhere in the five product contracts or the 45-command inventory. Reword from "defer" to "no selected product capability exists" so it cannot later be cited as an owed deliverable. This does **not** remove existing product scope. |

---

## 5. Read/execution coverage and honest limits

**Fully read:** chapter 14 (703 lines), `implementation-boundaries-and-build-plan.md` (696), `commit-recovery-plan.v1.json` (461, all 13 fields + all 36 cases), `prototype-report-inventory.md` (221, all 24 R-rows), `implementation-planning-sources.v1.json`, both checkers in full, and the crosscut `README.md` / `review-queue.json` / `design-corrections.proposed.md` plus `changed-source.json`, all three `.patch` files, `discovery-observations.json`, `discovery-corrected.json`, `pruning-observation.json`, `query-availability-observations.json`, `probe-query-availability.py`.

**Audited programmatically, not read row-by-row:** `implementation-coverage.v1.json` (358 KB / 320 rows) — I read the metadata, all sources, all four `reviewIssues`, every `owners`/`verification` pair, every gate row against its acceptance text, all renderers/sharedFlags, the three query goldens and every flagged row; I did **not** read all 320 rows' prose individually. `repository-file-inventory.v1.json` (190 rows) — the generated chapter tables reproduce every row's path/role/description and I read those in full.

**Candidate25:** read the exact cited sections (identity §5 retention/commit; security S3, S6, S7, S9, S9.2; `security-completion.v8` §5.4/§5.5/§5.6 and numeric ranges; `grant-journal.sql`; `JournalRecord`/`V2`/`StateSchema`/`PlatformProfileSetV1`/`commit-receipt`; `graph-query` `Operation`/`GraphOperation`; `query-projection-contract.v3` §0/§1/§7/§8; workflows §8; the full command inventory; native-matrix `syntax-only` cells and platform families; all 32 gate acceptance lines plus six full records; and the reference code at the XA-01 sites). I did **not** read the other ~12,850 candidate25 files.

**Not read this pass:** the `codex-author-followup.v2` package beyond its verified file list/hashes and one fixture (`query-checks1/purged.json`) used as probe input — its seven Runs, three negative controls and thirty residuals are **PENDING and carried forward**; `author-workspace-history.tar.gz` (17.8 MB) was not opened. Also unread: `native-correction-report.json`, `integration-correction-report.json`, `security-correction-report.json`, `contract-structure.json`, `author-pin-delta.json`, `apply-reference-correction.py`, `rebind-author-pins.py`, `probe-discovery.py`, `probe-pruning-observation.py`.

**Hard limits:** (a) the candidate25 reference models are not executable here (`jsonschema` absent), so no reference suite was re-run; (b) the prototype at commit `a62509d6…` is **absent from both the inputs and candidate25** (0 of 44 basenames found), so all 24 R-disposition *source* claims are unverified — only the 53 links / 39 distinct paths ⊆ 44 pinned files and internal consistency were checked; (c) all local documentation links in the three architecture documents resolve against inputs+candidate25 (8/7/4, none missing); (d) nothing here establishes OS durability, process isolation, compiler correctness, browser behavior or any gate qualification.

---

## 6. Unresolved decisions (carried)

Schema generator + runtime validator; TS package manager/lock topology; frontend/bundler and graph renderer; compile-fail, browser and OS harnesses; dependency checkers; release adapter; grammar backend placement and signed grammar closure (CR-14); provider SDK reuse; the `schemas/` migration mapping; the XA-02 representation; crate-count assessment against real public interfaces. The tool matrix is candidate decision work — no tool is installed or selected, and I did not treat it as one. `apps/cli` (`opensip-cli` → `opensip`), `apps/report` and `crates/reporting` are present as agreed; no existing product scope was removed by this delta.

---

```json
{
  "review": {
    "standing": "independent nonblind first-pass review; no acceptance, no readiness, no product qualification",
    "inputManifestSha256": "da22d2d59f09227a4eafc58821af58e5a96ccc3e4be91b41fbe6b54bef29792b",
    "candidateManifestSha256": "fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d",
    "inputFilesVerified": "136/136",
    "selectedCandidateSourcesVerified": "15/15 (disk and manifest)",
    "deltaAcceptable": false,
    "deltaDirectionAcceptable": true,
    "blocking": ["CR-01","CR-02","CR-03","CR-04","CR-05","CR-10","CR-12"]
  },
  "findings": [
    {
      "id": "CR-01",
      "severity": "high",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md",
      "section": "header paragraph ('does not change ... the required commit order') and '### Witness-aware publication and read-only recovery'",
      "evidence": "candidate25 docs/v2/contracts/product-v1/identity-and-evidence.md lines 1526-1539 define a four-step commit order with no grant-journal SEAL phase and state 'A failure before step 3 publishes no authoritative Run.' The proposal inserts a durable SEAL plus PENDING/COMMITTED witness barriers between steps 2 and 3, producing a durable orphan SEAL in F07-F11 and F19 that identity S5 does not contemplate.",
      "correction": "Withdraw the 'does not change the required commit order' claim. State that the proposal extends identity S5 with a security SEAL/witness phase between steps 2 and 3, enumerate the new durable artifact class (orphan SEAL), and record it as a normative amendment to be frozen and reviewed in a successor.",
      "status": "open-blocking"
    },
    {
      "id": "CR-02",
      "severity": "high",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md",
      "section": "'Publication sequence and lock discipline' step 4; 'Witness-aware publication...' ('orders both level-3 write transactions before the level-4 append lock: grant journal, then evidence ledger')",
      "evidence": "Storage commit.rs is the coordinator (chapter14 crates/storage/src/commit.rs) while the journal carrier is owned by crates/security/src/journal_store.rs. Journal-first therefore requires security to hand storage a held journal write transaction across storage's critical section, contradicting chapter14 crates/security/src/lib.rs ('never expose an unchecked operational grant or journal checkpoint') and the plan's own 'A short-lived checkpoint is never serialized as a reusable authority token.' S7 level 3 is BEGIN IMMEDIATE with busy_timeout 0 and the two carriers are separate databases, so the intra-level-3 order has no deadlock significance.",
      "correction": "Invert control: storage opens the evidence-ledger level-3 transaction first, then calls a single security-owned barrier seal_and_linearize(replayed, session, evidence_commit_fn) that internally opens the journal level-3 transaction, takes level 4, performs the S6 checkpoint, writes witness PENDING, appends SEAL, commits the journal with its barrier, writes witness COMMITTED, invokes the supplied closure against the already-open evidence transaction, then releases level 4. Both level-3 acquisitions still precede level 4 and no journal transaction or lock guard crosses the crate boundary. If journal-first is retained instead, define an opaque single-use non-cloneable JournalWriteGuard and state it is not an authority token.",
      "status": "open-blocking"
    },
    {
      "id": "CR-03",
      "severity": "high",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md",
      "section": "'Publication sequence and lock discipline' steps 5-6; failure case F19",
      "evidence": "candidate25 security-and-lifecycle.md S6 lines 425-433: observer ticks every 5 s and appends REV(observer-fail-stop) when the last successful read is older than 10 s; line 440-441: linearization is under the single journal append lock. The proposal holds that in-process mutex from the S6 checkpoint through journal commit+F_FULLFSYNC, witness write+barrier and the evidence-ledger commit+barrier, so the observer cannot append REV inside its bound. The plan states no observer behavior for that case.",
      "correction": "Require the observer to latch a fail-stop flag outside the append lock as soon as its bound is exceeded, and to append REV once the lock is released. Require the writer's post-blocking recheck (step 5 / F19) to read that latched flag, not only the trust counter, and state that the latch - not the REV append - is what prevents the evidence commit.",
      "status": "open-blocking"
    },
    {
      "id": "CR-04",
      "severity": "high",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md; inputs/docs/v2/architecture/implementation-coverage.v1.json",
      "section": "'Witness-aware publication...' COV-03 paragraph; reviewIssues COV-03; cases F31, F32",
      "evidence": "Executed SQLite probe on frozen candidate25 docs/coop/completion/security-schemas.v2/grant-journal.sql: SEAL REJECTED by the record_type CHECK; GRANT with platform 'linux-x86_64-gnu', 'linux-aarch64-gnu', 'macos-aarch64' all REJECTED; display aliases 'macos-x86_64' and 'macos-arm64' ACCEPTED. security-lifecycle.schemas.v1.json PlatformProfileSetV1 title: the ONE machine vocabulary is linux-aarch64-gnu, linux-x86_64-gnu, macos-aarch64, macos-x86_64, and display aliases 'never key it'. $defs/JournalRecord (schema 3) and JournalRecordV2 both enumerate only GRANT/RA/ICI/RCI/ICO/RCO/REV/CLN/SEAL - no TERMINAL/CHECKPOINT/MIGRATION/NARROW/EXPIRY/AUD - while security-completion.v8 S5.4 WA-13 requires TERMINAL for the uint53 rollover and F32 depends on it. The same stale DDL is embedded in docs/coop/completion/security_unit_lib_v8.py lines 537-563.",
      "correction": "Expand COV-03's stated scope to: (a) admit SEAL; (b) replace the platform CHECK with the machine vocabulary while preserving historical display-alias rows; (c) decide TERMINAL's schema-3 representation or state that TERMINAL/CHECKPOINT/MIGRATION/NARROW/EXPIRY/AUD remain carrier-only types outside JournalRecord; (d) reconcile the three operationRef domains (JournalRecord 1..128 free string, SQL length-35 GLOB, security-owned ^op-[0-9a-f]{32}$) and state which one the private association binds; (e) note that gj_no_delete already forbids row deletion, so F28 'pruning' means carrier-level removal, not row removal.",
      "status": "open-blocking"
    },
    {
      "id": "CR-05",
      "severity": "high",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md",
      "section": "'Private recovery record and storage-generation binding'",
      "evidence": "The plan specifies stateSchema as 'the admitted positive state schema number in 1..2^64-1'. candidate25 security-lifecycle.schemas.v1.json $defs/StateSchema = {\"enum\": [1, 2]}, referenced by InstallationTransitionIntentV1.fromStateSchema/toStateSchema. The same schema defines from/toStoreGeneration as I64NonNegative, and S9.2 requires currentStoreGeneration admission with refusal CURRENT_STORE_MISMATCH - yet the binding introduces an independent random storeInstanceId without relating the two.",
      "correction": "Constrain stateSchema to the owning contract's admitted domain (currently {1,2}) with an explicit rule for how it widens when that contract widens. Include the contract's storeGeneration in StoreGenerationBindingV1 so the digest is derivable from admitted lifecycle state, or state explicitly why a separate random storeInstanceId is required in addition and how both are jointly validated at S9 lineage.",
      "status": "open-blocking"
    },
    {
      "id": "CR-06",
      "severity": "medium-high",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md",
      "section": "'Private recovery record and storage-generation binding' ('storeGenerationDigest is raw SHA-256 of its canonical bytes')",
      "evidence": "chapter 14 assigns crates/identity/src/digests.rs 'registered digest framing and domain dispatch without a second serializer'. storeGenerationDigest mints a new digest over a new canonical record with no domain tag, from storage, and is then used as a primary-key component and a cross-recovery join key. receiptBytesSha256 and journalBodySha256 are not affected - they hash already-existing bytes, matching the carrier's own body_sha256.",
      "correction": "Mint storeGenerationDigest through the registered framing with a private domain tag (e.g. H(\"storage.store-generation-binding.v1\", record)) using the single canonicalizer/serializer, or state explicitly that storage owns a second hashing path and justify it against the digests.rs responsibility.",
      "status": "open"
    },
    {
      "id": "CR-07",
      "severity": "medium-high",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md; inputs/docs/v2/architecture/commit-recovery-plan.v1.json",
      "section": "'Witness-aware publication and read-only recovery'; cases F23, F29, F33",
      "evidence": "Counterexample: the writer makes SEAL(k) durable before the evidence-ledger commit. The grant journal and the evidence ledger are separate SQLite databases with no cross-database snapshot. A read-only recovery that samples the journal first and the ledger second can observe journal tail k-1 together with a committed receipt naming journalSeq = k - a state the writer never produced - and would report a contradiction (false negative). The plan specifies no cross-carrier read order.",
      "correction": "Specify that read-only recovery samples the evidence-ledger snapshot first and the journal second; that on observing a receipt whose journalSeq exceeds the observed tail it must re-read the journal once before concluding; and that only a post-re-read tail below journalSeq, with F22 rollback rules applied, is a contradiction. Add this as an explicit fault case.",
      "status": "open"
    },
    {
      "id": "CR-08",
      "severity": "medium",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md",
      "section": "'Witness-aware publication and read-only recovery' ('snapshot readers verify its retained durable prefix'); case F29",
      "evidence": "candidate25 security-completion.v8 S5.4: the witness is a single {seq, bodySha256} pair certifying the tail; the SC-TRUST high-water certifies the last observed operation boundary. Neither certifies an interior sequence k named by a committed receipt's association.",
      "correction": "Name the exact prefix predicate: hash-chain walk over prev_sha256 from the generation's first record to journalSeq; observed tail >= SC-TRUST high-water for that carrier; witness state in {COMMITTED n >= k with matching body hash, PENDING n+1 adjacent to tail n >= k}. Every other witness state yields indeterminate, never confirmed.",
      "status": "open"
    },
    {
      "id": "CR-09",
      "severity": "medium",
      "path": "inputs/docs/v2/architecture/commit-recovery-plan.v1.json; inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md",
      "section": "cases F00-F35; 'Required API and fault-injection checks'",
      "evidence": "F19 produces a durable SEAL with no ledger row while the session latches fail-stop. No case or required test covers that SEAL surviving into later operations. candidate25 security-and-lifecycle.md S6 line 461-464: admit_analysis_seal validates record fields, close_run and byte-equal RunId without consulting the evidence ledger, so that boundary alone would admit an orphan SEAL as a valid analysis SEAL.",
      "correction": "Add a case (F36) and a required test: an orphan SEAL from an aborted attempt must not appear as a committed Run in any query, history, receipt or availability surface, including after a later successful commit at seq k+1. State that admit_analysis_seal establishes record validity only, never commitment.",
      "status": "open"
    },
    {
      "id": "CR-10",
      "severity": "medium",
      "path": "inputs/docs/v2/architecture/implementation-coverage.v1.json (reviewIssues XA-03; groups.workflowGoldens 'query-evidence-purged'); inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md ('Implementation coverage account' XA-03 row); inputs/docs/coop/design-corrections/reviews/codex-crosscut-audit.v1/design-corrections.proposed.md section XA-03",
      "evidence": "The golden query-evidence-purged is 'finding.show on a purged Run's proof' (request-rejected, exit 2). candidate25 query-projection-contract.v3.md line 5: 'finding.show remains workflow_projection_model.v3.query_finding'. workflows-and-surfaces.md S8 lines 850-851: the graph contract owns graph.neighbors|path|reach and 'does not replace the artifact-specific owners of the other seventeen operations'. Mechanically, query_projection_model.v3.py line 43 GRAPH_OPS = {graph.neighbors, graph.path, graph.reach}; line 1227 refuses any other operation; execute_graph_query calls _validate_request (line 1445) before observe_availability (line 1452). finding.show can never reach the availability route. The author's own queryOperations XA-03 flags are scoped to the three graph ops plus availability.show, which is internally inconsistent with flagging a finding.show golden. The author's evidence probe (probe-query-availability.py) uses a graph.neighbors request only.",
      "correction": "Remove XA-03 from workflowGoldens:query-evidence-purged and release the exit-2 golden as a usable implementation expectation. Withdraw 'the graph-specific owner currently returns exit4' as applied to finding.show. Restate the identity S5 amendment to name graph.neighbors|graph.path|graph.reach exactly (graph-query.schema.json $defs/GraphOperation), not 'explicit graph operations'. Note separately that the exit-2 route in that golden currently has no reference owner (query_finding performs no availability observation), so crates/host/src/query.rs owns it at M4 with no reference precedent.",
      "status": "open-blocking"
    },
    {
      "id": "CR-11",
      "severity": "medium",
      "path": "inputs/docs/v2/architecture/implementation-coverage.v1.json (groups.queryOperations 'availability.show')",
      "evidence": "availability.show carries the XA-03 hold as if it shared the graph availability route. candidate25 workflows S8 assigns the other seventeen operations their own owners, and identity-and-evidence.md line 1582-1583 states 'Query of retained manifest is allowed after purge and states evidence unavailable.' Applying observe_availability's HOST.IO_FAILURE refusal to availability.show would make availability unqueryable precisely when it reports purged/expired/corrupt/unavailable.",
      "correction": "Re-disposition availability.show: it must report purged/expired/corrupt/unavailable as a successful observation, never HOST.IO_FAILURE. Replace the XA-03 hold with that explicit requirement in its coverage row.",
      "status": "open"
    },
    {
      "id": "CR-12",
      "severity": "medium",
      "path": "inputs/docs/coop/design-corrections/reviews/codex-crosscut-audit.v1/design-corrections.proposed.md section XA-01; reference-proposal/{discovery-defaults.py,security_lifecycle_model_v1.py,native_evidence_model.v2.py}",
      "evidence": "XA-01 itself is confirmed (candidate25 native_evidence_model.v2.py line 3591/3600 caps before _boundary_hit at 3609-3612 and before explicit-root selection at 3615-3637; security_lifecycle_model_v1.py line 731/733 caps before the nested-repo/nested-project/depth/custody loop at 736-757), the before-hashes match candidate25 exactly, the after-hashes match, and my independent diff shows only the three patch hunks. Two residual gaps: (1) both real callers now pass enforce_limit=False, so nothing bounds enumeration or custody-walk work before refusal - the 4096 cap changes from an input bound to an output bound; (2) the instruments count at different stages - security counts prov['units'] (post custody, post MAX_WALK_DEPTH=256 exclusion, a constant that exists only in security and is reused there as a downward unit bound S3 documents only as an upward ancestor bound), native counts by_dir (post boundary and explicit-root selection, with no custody or depth notion). Counterexample: 4200 first-party marker directories of which 150 fail directory custody - security admits 4050, native refuses 4200 with native.too-many-units, reproducing the exact admit/refuse split XA-01 exists to remove.",
      "correction": "Move the selection set into the shared docs/coop/design-corrections/discovery-defaults.py - pruning, nested-repository and nested-project exclusion, boundary exclusion and depth - and cap that one identical set in both instruments. Keep custody results instrument-specific, recorded in excludedUnits and counted, consistent with S3 ('Custody-excluded units are explicit unknown required scope, not a successful empty scope'). State an explicit enumeration/observation work bound separate from the 4096 unit cap, and document the downward use of MAX_WALK_DEPTH in S3.",
      "status": "open-blocking"
    },
    {
      "id": "CR-13",
      "severity": "medium",
      "path": "inputs/docs/coop/design-corrections/reviews/codex-crosscut-audit.v1/design-corrections.proposed.md section XA-02",
      "evidence": "candidate25 security-and-lifecycle.md S3 lines 193-196 promise the pruned anchor is recorded once 'with the number of markers it hid' while also promising the tree yields 'no custody walk'. pruning-observation.json shows the count is exact only over a supplied inventory (0/1/4200 in -> 0/1/4200 out). native_evidence_model.v2.py line 3598-3599 compares boundaries['prunedTrees'] != pruned_trees and refuses native.boundary-inventory-mismatch, so the row shape participates in a cross-instrument equality and in provenance digests.",
      "correction": "Version DiscoveryProvenanceV1 and AdmittedBoundaryInventoryV1 together with the native boundary-inventory equality rule, and define comparison when one side reports not-enumerated and the other observed-inventory. State that markerCountBasis, not only markerCount, is provenance-only and excluded from source scope, unit selection and Run identity.",
      "status": "open"
    },
    {
      "id": "CR-14",
      "severity": "medium",
      "path": "inputs/docs/v2/architecture/14-repository-and-module-layout.md (crates/host/src/syntax.rs row); inputs/docs/v2/architecture/implementation-coverage.v1.json (reviewIssues COV-01; qualificationGates DR-G13)",
      "evidence": "The inventory gives crates/host/src/syntax.rs both 'Own compiler-free syntax/clone dispatch over the exact admitted grammar closure' and 'route results through ordinary host fact admission' - the same crate produces and admits the facts that crates/host/src/fact_admission.rs exists to police. candidate25 native-capability-matrix.v2.json marks syntax/syntax-only, clones-fact/syntax-only and clones-near/syntax-only as SUPPORTED-DESIGN ('bundled grammars only'), and draws the 'produced by host discovery and enumeration, not by a language provider' distinction only for inventory/syntax-only. DR-G13 lists crates/host/src/syntax.rs alongside the two provider compiler adapters.",
      "correction": "Separate production from admission. Either (a) a providers/syntax component using the ordinary negotiated protocol and an authenticated signed grammar closure, or (b) a pure crates/syntax producer crate (no OS or effect authority; depends only on contracts/identity) whose candidates pass through host/fact_admission.rs, with crates/host/src/syntax.rs reduced to dispatch and selection. Name the grammar closure's authentication owner and state whether grammars are statically linked TCB or loaded artifacts under the component/closure authority path. Update DR-G13 owners to name the production owner.",
      "status": "open"
    },
    {
      "id": "CR-15",
      "severity": "medium",
      "path": "inputs/docs/v2/architecture/implementation-coverage.v1.json (groups.qualificationGates DR-G18, DR-G19, DR-G26)",
      "evidence": "DR-G18 acceptance is 'Activation, migration, rollback, locks, leases, and removal are journaled and crash-safe', but its owners are crates/lifecycle/src/transitions.rs and crates/security/src/journal_store.rs - omitting crates/lifecycle/src/journal_store.rs, which S9.2 makes the InstallationTransitionJournalV1 journal of record, and crates/lifecycle/src/leases.rs. COV-03 explicitly created the security journal owner 'distinct from lifecycle's transition journal', so this routing names the wrong journal. DR-G19 acceptance is 'Every durable/rebuildable state byte has one declared class, owner, writer, and lifecycle' but owners are only ledger_store.rs and index_store.rs, while the plan itself places the recovery association 'under G19'. DR-G26 (refuse or do not offer a non-applicable format) is owned solely by crates/reporting/src/renderer_factory.rs, whose chapter14 row says it must 'never choose policy or public termination'; the same behavior's golden sarif-not-applicable (REQUEST.UNKNOWN_OPTION / OUTPUT.FORMAT_NOT_APPLICABLE / exit 2) is routed to crates/host/src/query.rs.",
      "correction": "DR-G18: add crates/lifecycle/src/journal_store.rs and crates/lifecycle/src/leases.rs. DR-G19: add at least crates/storage/src/availability.rs, crates/storage/src/blob_store.rs, crates/security/src/journal_store.rs and crates/lifecycle/src/journal_store.rs. DR-G26: add the request-admission owner(s) (apps/cli/src/arguments.rs and the host command owner), since format applicability and typed refusal are admission decisions, not renderer selection.",
      "status": "open"
    },
    {
      "id": "CR-16",
      "severity": "medium",
      "path": "inputs/docs/v2/architecture/implementation-coverage.v1.json (groups.commands help/version/completion; groups.renderers json); inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md (milestone table, M1)",
      "evidence": "command-inventory.v3.json gives help formats [human,json] with parityFields [command-names] and version formats [human,json] with parityFields [host-release, closure-ids]; workflows S8 makes 'json v3 (the CommandEnvelope major 3 is the parity reference)'. The coverage rows for help/version at M1 list owners apps/cli/src/arguments.rs and apps/cli/src/bootstrap.rs only, while renderers:json maps to crates/reporting/src/json_renderer.rs at M4. Chapter 14 states the CLI directory 'does not move semantic authority into argument parsing or presentation code'. No owner is assigned anywhere for producing version's closure-ids under DR-G03's 'load no components/project' constraint.",
      "correction": "Either add crates/reporting/src/json_renderer.rs and the envelope/outcome owner to the M1 help/version rows, or move those rows' json format to M4 and state that M1 delivers human only. Assign an explicit owner and source for version's closure-ids consistent with DR-G03 and with bootstrap.rs's 'must not open a project, store or component session'.",
      "status": "open"
    },
    {
      "id": "CR-17",
      "severity": "medium",
      "path": "inputs/docs/operations/check_implementation_planning.py (validate_coverage)",
      "evidence": "Demonstrated by executed negative controls, all ACCEPTED: queryOperations:graph.path owned by docs/README.md; a planned-behavioral-test row whose verification.owner is docs/README.md with method 'look at it'; DR-G11 owned by docs/README.md after --write; analyze moved from M3 to M1 after --write. The checker enforces only owners <= inventory paths, verification.owner in paths and method.strip(). This bounds what 'both checkers pass' means, and the first two directly undercut the plan's own statement that 'a README path is not a test' and that the milestones are 'dependency-ordered work packages'. Eleven other planning controls and all eight inventory controls were correctly rejected.",
      "correction": "(a) Require verification.owner's inventory role == 'test' when verification.kind == 'planned-behavioral-test'; permit a documentation role only for kinds qualification-harness-specification, section-owner-routing and independent-review-scope (which currently cover 108/42/5 rows and the seven tools/README.md gate owners). (b) Forbid documentation-role paths in owners for commands, queryOperations and renderers. (c) Add a milestone-ordering invariant - declare M0<M1<...<M6 prerequisites in the JSON and require each row's milestone to be >= the milestone of every module it owns - so dependency ordering is enforced rather than asserted.",
      "status": "open"
    },
    {
      "id": "CR-18",
      "severity": "medium",
      "path": "inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md ('Private recovery record...'); inputs/docs/v2/architecture/commit-recovery-plan.v1.json (extraAdmissionRules)",
      "evidence": "Executed on the proposed association table: MAX(commitSequence) over {'2','9','10','100'} returns '9'; ORDER BY commitSequence yields 10,100,2,9; ORDER BY length(commitSequence), commitSequence yields 2,9,10,100; CAST('18446744073709551615' AS INTEGER) silently saturates to 9223372036854775807 with no error; the REAL round-trip yields 1.8446744073709552e+19. The plan states the length-then-bytes rule in prose only, with no mechanism preventing a bare ORDER BY, MAX or CAST.",
      "correction": "Encode the rule rather than only stating it: add CHECK (length(commitSequence) BETWEEN 1 AND 20), and either a fixed-width zero-padded ordering column or a single private accessor that is the only path permitted to order or take a maximum, with a test asserting that a bare ORDER BY / MAX / CAST on that column fails review. State that no allocation or ordering decision is taken from this private column; the receipt's numeric value remains the allocator.",
      "status": "open"
    },
    {
      "id": "CR-19",
      "severity": "low-medium",
      "path": "inputs/docs/v2/architecture/commit-recovery-plan.v1.json (case F32); inputs/docs/v2/architecture/14-repository-and-module-layout.md (storage and lifecycle rows)",
      "evidence": "F32 requires 'Pause/close generation through the owner lifecycle outside the held operation lease', but the declared graph gives opensip-storage no dependency on opensip-lifecycle (correctly, to avoid a cycle), so storage cannot invoke lifecycle. The inherited DDL already provides carrier_capacity_pause. No typed storage refusal or host routing owner is named.",
      "correction": "Name the typed storage refusal (e.g. CarrierCapacityExhausted) and the host module that routes it to lifecycle outside the held lease; record both in the inventory and in F32.",
      "status": "open"
    },
    {
      "id": "CR-20",
      "severity": "low",
      "path": "inputs/docs/v2/architecture/repository-file-inventory.v1.json (apps/cli/Cargo.toml row); inputs/docs/v2/architecture/14-repository-and-module-layout.md ('CLI names' table)",
      "evidence": "The agreed executable name 'opensip' appears only in hand-written chapter prose outside the generated markers. The apps/cli/Cargo.toml inventory row carries the shared boilerplate 'Declare this package, explicit dependencies and build targets.' (one of 12 identical manifest descriptions), so the inventory checker's drift check cannot protect the agreed name.",
      "correction": "Record the [[bin]] name = \"opensip\" requirement in the apps/cli/Cargo.toml inventory row so it is machine-owned and covered by the regeneration check.",
      "status": "open"
    },
    {
      "id": "CR-21",
      "severity": "low",
      "path": "inputs/docs/v2/architecture/prototype-report-inventory.md ('Explicit migration boundaries'); inputs/docs/v2/architecture/implementation-boundaries-and-build-plan.md (M4 demonstration row)",
      "evidence": "The document says 'Required HTML supports the selected analysis and query surfaces.' candidate25 command-inventory.v3.json advertises html for exactly default, analyze, fit, audit, candidates, inspect, review-brief and repair-preview; the query command advertises human, json, agent only; sarif is advertised only by default, analyze, audit and repair-verify.",
      "correction": "Name the exact applicability sets. State that the report's graph and history data reach the browser through those eight commands' embedded projections, not through an HTML output of the query command, and reflect the sarif applicability set in the M4 parity demonstration row.",
      "status": "open"
    },
    {
      "id": "CR-22",
      "severity": "low",
      "path": "inputs/docs/v2/architecture/implementation-planning-sources.v1.json (prototype.files); inputs/docs/v2/architecture/prototype-report-inventory.md",
      "evidence": "44 prototype files are pinned; 53 links resolve to 39 distinct paths, all within the pinned set. The five pinned-but-never-cited files are the four packages/dashboard/src/__tests__ files and packages/dashboard/src/client/filters.ts - while the document asserts 'The old shared graph filter drawer is not a retained feature: its source says it was removed', leaving that migration boundary without a followable citation.",
      "correction": "Cite filters.ts at the filter-drawer claim and the four test files where they evidence intended coverage, or remove them from the pin set so the pinned set equals the cited set.",
      "status": "open"
    }
  ],
  "dispositions": {
    "XA-01": {"finding": "confirmed", "priority": "required", "proposedFixAssessment": "accepted in direction; reference patch verified byte-exact, minimal and correctly bound (before-hashes match candidate25, after-hashes match shipped files, diff contains only the three hunks)", "accepted": false, "blockedBy": ["CR-12"]},
    "XA-02": {"finding": "confirmed", "priority": "advisory design question (agreed)", "proposedFixAssessment": "closed row {path, reason, markerCount, markerCountBasis} is sound in direction", "accepted": false, "blockedBy": ["CR-13"], "note": "integration requires versioned successors to DiscoveryProvenanceV1 and AdmittedBoundaryInventoryV1 plus the native boundary-inventory equality rule"},
    "XA-03": {"finding": "confirmed but mis-scoped by the author", "priority": "required clarification", "proposedFixAssessment": "amendment direction correct; must name graph.neighbors|graph.path|graph.reach exactly; the workflow-golden overlap claim is contradicted by the source and must be withdrawn", "accepted": false, "blockedBy": ["CR-10", "CR-11"]},
    "COV-01": {"finding": "confirmed", "proposedFixAssessment": "file-owner routing accepted as interim; backend placement unresolved and the host is left as both producer and admitter", "accepted": "partial", "blockedBy": ["CR-14"], "requiredBefore": "M3"},
    "COV-02": {"finding": "confirmed exactly (4 cli strings carry run2:; the file contains 4 run2 and 1 run3)", "proposedFixAssessment": "correct in a reviewed successor, never edit candidate25, infer no run2 admission", "accepted": true},
    "COV-03": {"finding": "confirmed and understated", "proposedFixAssessment": "migration obligation correct but incomplete", "accepted": false, "blockedBy": ["CR-04"]},
    "R24-simulation": {"finding": "deferral acceptable", "evidence": "no simulation, fitness or YAGNI capability exists in the five product contracts or the 45-command inventory", "correction": "reword from 'defer' to 'no selected product capability exists' so it cannot later be cited as an owed deliverable", "accepted": "with-rewording", "scopeRemoved": false}
  },
  "coverage": {
    "checkersExecuted": ["check_repository_file_inventory.py --check (PASS, 190 paths)", "check_implementation_planning.py --source <candidate25> --check (PASS, 320 mappings, 36 cases)"],
    "negativeControls": {"inventoryChecker": "8 attempted, 8 rejected", "planningChecker": "12 attempted, 11 rejected on merits, 1 rejected only as rendered-table drift", "limitProbes": "4 attempted, 4 accepted (demonstrating CR-17)"},
    "independentProbes": ["SQLite execution of the frozen grant-journal.sql (SEAL and 3 of 4 machine platform ids rejected)", "SQLite execution of the proposed CommitRecoveryAssociationV1 table (decimal-text ordering, u64 CAST saturation, REAL precision loss)", "mechanical call-order extraction from query_projection_model.v3.py", "byte-exact diff of the three XA-01 reference-proposal files against candidate25", "hash verification of 136 input files, 15 selected candidate25 sources, 44 prototype pins and 53 prototype links"],
    "fullyRead": ["14-repository-and-module-layout.md", "implementation-boundaries-and-build-plan.md", "commit-recovery-plan.v1.json", "prototype-report-inventory.md", "implementation-planning-sources.v1.json", "check_implementation_planning.py", "check_repository_file_inventory.py", "codex-crosscut-audit.v1/README.md", "codex-crosscut-audit.v1/review-queue.json", "codex-crosscut-audit.v1/design-corrections.proposed.md", "reference-proposal/changed-source.json", "the three reference-proposal .patch files", "discovery-observations.json", "discovery-corrected.json", "pruning-observation.json", "query-availability-observations.json", "probe-query-availability.py"],
    "auditedProgrammaticallyNotRowByRow": ["implementation-coverage.v1.json (320 rows: metadata, sources, all 4 reviewIssues, all owners/verification pairs, all 32 gate rows against acceptance text, renderers, sharedFlags, query goldens and every flagged row)", "repository-file-inventory.v1.json (190 rows; all descriptions read via the generated chapter tables)"],
    "candidate25SectionsRead": ["identity-and-evidence.md S5 retention/commit (1505-1599)", "security-and-lifecycle.md S3, S6, S7, S9, S9.2", "security-completion.v8.md S5.4, S5.5, S5.6 and numeric ranges", "security-schemas.v2/grant-journal.sql", "security-lifecycle.schemas.v1.json (JournalRecord, JournalRecordV2, StateSchema, PlatformProfileSetV1, transition intent/journal)", "identity-schemas.v3.json commit-receipt", "graph-query.schema.json Operation/GraphOperation", "query-projection-contract.v3.md sections 0,1,7,8", "query_projection_model.v3.py and workflow_projection_model.v3.query_finding", "workflows-and-surfaces.md section 8", "command-inventory.v3.json (commands, goldens, renderers, sharedFlags)", "native-capability-matrix.v2.json syntax-only cells and platform families", "qualification-gates.proposed.json (all 32 acceptance lines, 6 full records)", "discovery-defaults.py, security_lifecycle_model_v1.py and native_evidence_model.v2.py at the XA-01 sites"],
    "notRead": ["codex-author-followup.v2 beyond its verified file list/hashes and one fixture used as probe input", "author-workspace-history.tar.gz (17.8 MB, not opened)", "native-correction-report.json", "integration-correction-report.json", "security-correction-report.json", "contract-structure.json", "author-pin-delta.json", "apply-reference-correction.py", "rebind-author-pins.py", "probe-discovery.py", "probe-pruning-observation.py", "the other ~12,850 candidate25 files"],
    "hardLimits": [
      "jsonschema is not installed (Python 3.14.6, no network), so candidate25 reference models could not be executed; probe-discovery.py and probe-query-availability.py were not re-run and the crosscut README's 464/375/412 counts are unverified by me",
      "the prototype at commit a62509d623173155d0946e9f5d5ca90c839893e0 is absent from both inputs and candidate25 (0 of 44 basenames found), so all 24 R-disposition source claims are unverified; only link/hash pinning and internal consistency were checked",
      "no OS durability, process isolation, compiler correctness, browser behavior, accessibility or gate qualification is established by anything in this pass"
    ]
  },
  "pendingObligations": [
    {"item": "codex-author-followup.v2 (seven Runs, three negative controls, thirty residuals)", "status": "PENDING - not reviewed this pass; not accepted"},
    {"item": "original blind consumer requirements reconstruction", "status": "PENDING - separate obligation"},
    {"item": "successor byte review", "status": "PENDING - separate obligation"},
    {"item": "final application and readiness review", "status": "PENDING - separate obligation"},
    {"item": "chapter 14 'Claude task' items 1-6", "status": "PARTIAL - items 1,2,3,5(partial),6(partial) addressed; item 4 (provider releases/toolchains, schema generation, SDK reuse, asset closure joins) and executed report parity not covered this pass"}
  ],
  "unresolvedDecisions": ["schema generator and runtime validator", "TS package manager and lock topology", "frontend/bundler and graph renderer", "compile-fail, browser and OS test harnesses", "Rust and TS dependency checkers", "release adapter", "grammar backend placement and signed grammar closure (CR-14)", "provider-side SDK reuse", "schemas/ source and generation migration mapping", "XA-02 representation integration", "R24 simulation UI (pending a selected simulation contract)", "crate count assessed against real public interfaces"]
}
```

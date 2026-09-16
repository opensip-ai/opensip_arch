# Independent planning-successor review — scoped acceptance with changes required

## 0. Custody and what I actually ran

All nine inputs hash-match `input-manifest.json` (verified before and after; no input byte modified). Frozen candidate25 verified in full against manifest `fa8cdc79…a536d`: **12869 members, 0 missing, 0 mismatches**. Retained exact44 prototype files: **44/44** match `implementation-planning-sources.v1.json`, and the 15 architecture sources all match candidate25 *and* its manifest rows.

I copied the inputs to `scratch/work/` and placed the candidate25 manifest at its expected relative path so both checkers run:

```
PASS: 198 unique paths, naming/ownership checks, acyclic package dependencies, chapter matches
PASS: 320 source-bound mappings, 38 planned failure cases, private schema, owners and generated plan
```

I did not treat those passes as agreement. Both checkers are bookkeeping; three of my eight findings are invisible to them by construction.

**Executed probes** (all in `scratch/`, rerunnable): two Python join probes; a compiled multi-crate Rust miniature of the proposed API (`rustc 1.95.0`, edition 2021) with eight negative compile probes, a 200 000-round two-thread latch/admission race probe, and an end-to-end scenario binary.

---

## 1. The commit API: ownership, visibility and cycles hold up

I built the proposal as six real crates and compiled them in dependency order. The decisive evidence: **`security` compiles with no `--extern storage` at all.** The security-owned `CommitStaging`/`PreparedLedgerCommit` traits with a storage-private implementation genuinely need no security→storage edge, so `storage → {evaluator, security}` is acyclic in fact, not just in the declared graph.

The full path compiles and runs:

```
S1 clean publish:   attempt_state_after=1   PUBLISHED run=run3:00000006 seq=42 seal=41
S2 observer latched: attempt_state_after=2   REFUSED Latched
S3 substituted claim:                        REFUSED Replay
```

`PreparedCommit::publish(self)` destructures, hands `CommitSession` **by value** to `begin_journal_txn`, opens the evidence transaction second, hands security a storage-private adapter holding `&mut LedgerTxn`, and regains the transaction after the call. No `E0505`, no `E0499`.

Negative probes, all behaving as the design claims:

| probe | result | claim tested |
|---|---|---|
| n1 forge `ReplayedRun` in host | **E0451** | private replay constructor |
| n2 forge `PublishedCommit` | **E0451** | private durable-commit constructor |
| n3 reuse consumed session | **E0382** | single-use session |
| n4 borrow-then-move sketch | **E0505** | root's rejection of the earlier sketch reproduces exactly |
| n6 clone `CommitSession` | **E0599** | non-cloneable |
| n8 forge `SealOutcome` | **E0451** | storage facade accepts no external outcome |

Two things the probes surfaced that the text should say (observations, not blockers):

- **n5 reproduces `E0509`.** If `PreparedCommit` itself implements `Drop`, `publish(self)` cannot move its fields out. "Drop is best-effort rollback" has to attach to the inner guards and the ledger transaction, not to the commit-state type.
- **n7 compiles (rc 0).** Because storage implements the trait cross-crate, `CommitStaging` must be `pub` — so any security-dependent crate can drive `seal_under_append_lock` with its own adapter and produce a durable SEAL with no ledger participation. That is exactly the F36 orphan and no authority breach (the text's "not a sandbox" caveat covers it), but the consequence for carrier-capacity/witness accounting isn't stated.

**Witness ordering: cleared.** I checked the claim that the PENDING→commit→COMMITTED sequence needs no journal-transaction reacquisition under level 4. Security v8 §5.6 lists "witness write" as its own durability boundary, separate from "journal append", and the §5.4 reconciliation table (`PENDING n+1 with tail n → REVERT`) only makes sense if the witness is outside the journal's SQLite transaction. F07/F08/F10 map onto that table correctly. No contradiction.

**COV-03: factually exact.** `security-schemas.v2/grant-journal.sql` has no `SEAL` in its `record_type` CHECK, and its `platform` CHECK names `macos-arm64/linux-arm64` against the current S8 ids. Seq cap and reserved terminal slot `9007199254740991` match.

**CR-18 verified by execution.** The `commitSequence` pattern rejects leading zeroes, signs, decimals, exponents, whitespace and trailing newline (the `(?![\s\S])` anchor defeats `$`-before-newline). Length-then-bytes ordering equals numeric ordering on the exact F37 set `{0,2,9,10,100,u64max}` where bare lexical ordering does not; u64max round-trips. And `99999999999999999999` is pattern-valid but over range — precisely what the `extraAdmissionRules` upper-bound entry exists for.

---

## 2. Per-CR reassessment

| CR | Standing | Basis |
|---|---|---|
| CR-01 | **addressed** | "does not change the required commit order" now occurs **0 times**; replaced by an explicit identity §5 extension + orphan-SEAL artifact class + successor requirement |
| CR-02 | **addressed by alternative** | Control not inverted as proposed; instead one security-owned barrier owns the whole checkpoint/witness sequence, order is fixed globally (journal→ledger, both non-waiting), no level-3 under level-4. Miniature shows it is expressible. Constraint met |
| CR-03 | **addressed** | Latch outside the append mutex; atomic arbitration; F19 rechecks after blocking work. Residual → PS-05 |
| CR-05 | **partially addressed** | `stateSchema` enum == owner (adding `type:integer`, a narrowing); `storeGeneration` == owner `I64NonNegative` byte-for-byte; instance id justified. New defect in the justification → **PS-01** |
| CR-09 | **addressed** | F36 present, exactly on point |
| CR-10 | **addressed** | `query-evidence-purged` clean (M4, exit 2, no reviewIssues); XA-03 now only on the three graph ops |
| CR-11 | **addressed** | `availability.show` requires successfully reporting retained/purged/expired/corrupt/unavailable |
| CR-14 | **addressed** | Option (b): pure `crates/syntax` ⊆ {contracts, identity}, enforced by the checker |
| CR-15 | **addressed** | DR-G18/G19/G26 owner sets all now contain the named modules |
| CR-16 | **partially addressed** | JSON owners added; the human side of the same rows is inconsistent → **PS-02** |
| CR-17 | **addressed** | Checker enforces both halves |
| CR-18 | **addressed** | Verified by execution (above) |
| CR-19 | **mostly addressed** | `CarrierCapacityExhausted{grantGeneration, provenTailSeq}` → `host/finalization.rs` named in prose and the module is in the inventory; but the **F32 row still names neither**, and `finalization.rs`'s description doesn't record the capacity route. The correction asked for both |
| CR-20 | **addressed** | `[[bin]] name = "opensip"` in the inventory row |
| CR-21 | **addressed** | Both applicability sets byte-exact against `command-inventory.v3.json`; `query` explicitly gains no HTML; M4 row reflects both |
| CR-22 | **addressed** | 44 pinned == 44 cited, zero either way |
| CR-24 | **addressed with residual** | `closure2.kind` claim correct (enum has exactly 8 members; `platform-independent` absent). Anchor precision → **PS-04** |
| CR-26 | **addressed** | Verified against pinned `filters.ts`, whose own comment describes the hidden non-interactive production-only default |
| CR-27 | **addressed** | Five explicit per-tab rows; YAGNI now explicit |

Recipes I checked against frozen bytes and found **source-accurate**: seven families / fourteen suffixes / code vs data-document / relation-at-rung; `parserVersion == closure semanticVersion`; closure2 seven-field identity, `opensip.metadata.manifest.1`, TR-INDEX catalog, RJ-3, regular-files-only Blob projection, `DetectorManifestV1` as compatibility listing; the four machine platforms; DR-G26's applicability successor (`"no broad SARIF drop"`). Prototype dispositions R07/R08/R11/R12/R14/R15/R20/R21 all verified against the exact pinned sources (8 MiB / 2 MiB caps, `limit: 20` twice, the `audit`+`built-in-suite` special case, `openCodePathsFunction` requiring `matches.length === 1` vs the collapsing `byBodyHash` lookup, `RESERVED_DASHBOARD_KEYS`, forked hook worker).

---

## 3. Changes required (8)

**PS-01 (high) — the store binding claims an S9 validation S9 cannot perform.**
The plan says S9 validates the old/new `(storeInstanceId, storeGeneration, stateSchema)` tuple against the transition intent and registry. In frozen candidate25, the substring `storeInstance` **does not occur anywhere** in `security-lifecycle.schemas.v1.json`. `InstallationTransitionIntentV1` (11 props) and `InstallationTransitionJournalV1` (20 props) are both `additionalProperties:false` with no such field, and the S9.2 `registry` is a `NamespaceList` of namespace strings. Separately, `security-and-lifecycle.md:654-655` says rollback "re-selects the retained old store" while the plan says a "newly created/restored store instance receives a new storeInstanceId" — the package never says which applies, and the two readings differ in whether pre-migration associations still join to the active binding after a rollback.
*Required:* withdraw/restate the S9 claim as a new private lifecycle obligation needing an explicit S9 owner successor (naming it as a dependency of the separately active carrier/migration task), and state the rollback instance-id rule with its join consequence. **Uniqueness is not at risk** under either reading — the PK and both unique keys stay collision-free.

**PS-02 (medium-high) — six commands are scheduled before the renderers they advertise.**
`help`/`version`/`completion` are M1 and advertise `human`, but the `human` renderer row and `crates/reporting/src/human_renderer.rs` are **M4**; `completion` advertises human only and names no renderer owner at all. `default`/`analyze`/`recommend` (M3) advertise `agent` (+`sarif`/`html`) at M4. The M1 table row names only the "JSON renderer" as its deliverable while its own demonstration column requires "help/version **human** and JSON metadata". The checker can't see this: its delivery rule compares a row's milestone only against `moduleFirstMilestone` of that row's own owners.
*Required:* move `human` to M1 and add the owner, or restate M1 as JSON-only and move `completion`; and add the missing rule (row milestone ≥ every advertised renderer's milestone) or state that intermediate milestones may ship a strict format subset.

**PS-03 (medium) — the closed generation-registry row cannot express the package's own generated inventory.**
`outputs` rows are closed `{path, language, role}` with `role ∈ {carrier, shape-validator}` and globally unique paths. But `crates/contracts/src/generated/mod.rs` is `generated:true` with role `public-api` (neither value), and `apps/report/src/generated/report.ts` is one path declared to provide **both** carriers and shape-validation. So either those files escape the byte-comparison drift check or the row shape is wrong. The lane table also claims Rust "runtime validators" that no inventory row provides.

**PS-04 (medium) — the report-asset anchor is not resolvable in the frozen source.**
The recipe binds the private manifest to "the signed host release artifact tree" whose "existing authenticated artifact/catalog association commits an exact asset-manifest regular file and every asset member." In candidate25 the per-file TreeCommitment path is the **component** manifest (DR-103 `kind` enum initial vocabulary `component`), the TR-INDEX catalog row commits only `{platform, archiveProfileId, archiveDigest, sha256}`, and the core/host release manifest is described as **prospective** (`CoreProfileBindingV2` is two fields). No host-release per-member listing is published. Name which anchor applies and record the core-release-manifest dependency.

**PS-05 (medium) — the post-admission latch is unrecorded.**
The text says both "a single atomic attempt state arbitrates latch versus commit admission" *and* "an observer latching after admission blocks subsequent effects." Executed probe under the literal reading:

```
AS-PROPOSED admitted=true post_latch_recorded=false final_state=1
CORRECTED  admitted=true post_latch_state=3 commit_permitted=false further_effects_permitted=false
```

A tri-state CAS loses the post-admission latch entirely, so nothing blocks subsequent effects. A four-state machine satisfies both sentences. The arbitration itself is sound — 200 000 rounds, exactly one winner per attempt, **0 mutual-exclusion violations**.

**PS-06 / PS-07 / PS-08 (low).** The plan's own Author verification reports 186/190 paths and **36** fault cases while the same file renders F00–F37 and the inventory holds 198 (chapter 14 was updated, the plan wasn't; ch14's update carries two missing-space byte defects `has198`/`and38` despite a claimed whitespace pass). Chapter 14's hand-written tree block omits `crates/syntax/` though its own generated table lists it with nine files. R21's enumerated launcher env set omits `SSH_CLIENT`, which `open-report.ts:45` reads.

---

## 4. Verdict

**Scoped acceptance with changes required**, limited to the exact nine reviewed files against frozen candidate25.

The commit/recovery core is materially stronger than the prior round and now survives compilation of its own API shape: the ownership, visibility and acyclicity claims are true, not aspirational, and the two rejections (E0505, E0451) are correct rejections. The syntax, release-join, report-applicability and prototype-disposition recipes are byte-accurate against the frozen source and sufficiently specified for implementation planning with library/version selection left to M1/M2 — I did not treat missing tool choices as defects.

PS-01 through PS-05 should be fixed before this package is rebound; PS-06 through PS-08 are byte-level corrections.

**Not covered by this verdict:** no source successor acceptance, no carrier/migration acceptance, no readiness, no implementation authorization. Source pins remain candidate25 intentionally. CR-04/07/08/23 (versioned carrier/migration/read-only anchors, additional race cases), XA02/CR-13/25 (discovery mirror/anchor) and F04–F06 (internal source roots/cell view bindings) remain separately active and are **not** closed here — PS-01 and PS-04 name explicit dependencies on that work rather than duplicating it. Final successor/source rebind, a fresh blind consumer review and independent application review all remain mandatory.

One caveat on counts: 42 of the 55 `contractSections` rows share one verification owner and one identical method string (including a row spanning source lines 87–1349), and 98 of the 320 rows name `tests/qualification/README.md`, which the plan itself says is not a test. The 320 figure is owner routing, as the package states — I did not let it stand in for verification depth.

Artifacts are in `scratch/`: `findings.json` (verdict, per-CR reassessment, 8 findings, 4 observations), `probe-evidence.json` (all executed outputs), `probes/`, `rustprobe/`, `work/`, `README.md`. The Rust miniature is a scratch API-shape experiment for design review only — not product implementation, and it establishes nothing about durability or OS behaviour.

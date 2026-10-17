# Component installation implementation plan r1: the profile codec, the store and installer, the retained-tree capability, and the command (law CI r5)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** It implements the accepted law "component release installation and tree custody" (`component-install/PROPOSAL.md`, which is r5 under its acceptance note). The law was accepted by Codex in `codex-component-install-r5` after rounds 1 to 4, and published at ARCH `4088af76`. It also carries that review's three NBOs, which are answered in §3 (LD-CIP-4 to LD-CIP-6).

**Bases:** product main `3742822e`, and architecture `4088af76` together with the files the subject manifest names.

**Short names** are as in the law. In addition:
- **LAW** is `component-install/PROPOSAL.md`. Its items and controls are cited as LAW item n and CI-Tn.
- **C2a** is the C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`).

## 1. What exists, and what is missing

**What exists on main:**
- **The trust owner's ordinary reader**, which joins a validated manifest to its catalog release, envelope and preimage (`crates/security/src/trust_ordinary_metadata.rs`:90-160).
- **The manifest and catalog shapes:** CM (`component_manifest.rs`, with its generated shape) and RC (`trust/recovery_catalog.rs`).
- **Custody:** security's `admit_custody_directory` (`snapshot_source.rs`:444), which charges `descriptor_acl_capture_cost()`.
- **The platform's staging and publication primitives:** `create_private_directory_stage_accounted`, `publish_exclusive_reserved` and their law-467 route classes (`filesystem/directory_publication.rs`). Also the exclusive creates (`file_effects.rs`:24, `directory_effects.rs`:49), the directory barriers (`directory_effects.rs`:28, :103-112), and `WorkLedger::effect` and `ReservedPostchecks` (`work_ledger.rs`:388-400).
- **The snapshot read discipline** (`crates/host/src/snapshot.rs`:33-70), and D3a-0's descent recipe (`crates/platform/src/process.rs` `descend_cost`, `READ_COST`).
- **`FileLock`** with shared and exclusive modes (`crates/platform/src/locks.rs`).
- **`RetainedDirectory::as_file`** (`filesystem.rs`:340), the public descriptor access that `custody_entry.rs` builds on.
- **The lifecycle crate**, with `leases.rs`, `locations.rs`, `selection.rs` and `lineage.rs`. Its planned inventory rows include `installation.rs` ("Stage and publish authorized immutable component generations.") and `catalog.rs`.
- **The pinned archive profile:** PKG-AP, in `component-packaging-contract.v14.json` at its pinned SHA-256.

**What is missing:**
- the profile-1 codec;
- the component store and the installer transaction;
- platform primitives P-1 to P-7 (LAW item 4);
- the retained-tree capability and its transfer;
- lifecycle's dependency edge to security, which the O1-a package policy permits;
- the fixture store;
- the command surface;
- the controls.

## 2. The split

| Sub-unit | Delivers | Depends on |
| --- | --- | --- |
| **CI-1** | **The profile-1 codec**, pure and fed hostile input: a new `crates/security/src/archive_profile.rs`. It provides PKG-AP admission as a streaming verifier: headers are recomputed from TreeCommitment rows and compared octet for octet; the member/entry bijection, `archiveLength` and every capacity are checked (LAW item 3). It also provides PKG-AP's byte-algorithm emitter, **for fixtures only**, under the joint fixture predicate. No allocation is proportional to the archive. Headers are parsed inside the caller's read buffer. | nothing |
| **CI-2** | **The store and the installer.** It realizes the planned row `crates/lifecycle/src/installation.rs` and the transaction (LAW item 4, steps 1 to 6), with V1, V2, the funded suffix, the outcomes and LD-CI-12. It adds the store location to `crates/lifecycle/src/locations.rs`. It provides platform primitives **P-1 to P-6** in a new platform module, `crates/platform/src/component_tree.rs`, declared in `lib.rs` as `custody_entry.rs` is (LD-CIP-1). **P-7** is an equal published status price in that module (LD-CIP-2). Lifecycle's manifest gains `opensip-security`. | CI-1; C2a-1's `trust::admitted_components` bridge and `ClosureCandidate` |
| **CI-3** | **The retained-tree capability** (LAW item 6): `open_retained_tree`, `RetainedTree` (holding the retained generation, `tree/` and `pin.lock` handles and the buffer), `transfer`, and the typed `TreeReadFailure`. It also provides the pin (LAW item 7) and `ComponentStore::fixture` under the joint fixture predicate. It lives in a new `crates/lifecycle/src/retained_tree.rs`. **C2a-3 binds CI-3** (C2a §2). | CI-2 |
| **CI-4** | **The command surface** (LAW item 4's handoff; item 8's terminations). J1 exposes `install` with the operator-supplied archive file, under WS's command inventory. It maps every LAW item 8 row to its schema-valid termination, carrier and remedy (CI-T16). | CI-2; J1 |

**Order.** CI-1 first. Then CI-2 and CI-3: CI-3's capability needs CI-2's generations, and both may share one lane when their reviews come together. C2a-2's generator gains profile-1 archive emission through CI-1's emitter, so its synthetic releases install through CI-2. Then C2a-3 binds CI-3. CI-4 lands with J1.

## 3. Lead decisions

- **LD-CIP-1. The platform primitives live outside the census closure.** P-1 to P-6 go in a new top-level platform module, `component_tree.rs`, declared in `crates/platform/src/lib.rs` with `#[allow(unsafe_code)]`, as `custody_entry.rs` is (lib.rs:62-63). They are built on public filesystem API only: `RetainedDirectory::as_file` and `File`, with their own native calls:
  - **P-1:** a positioned chunk write (`pwrite`), one charged attempt per chunk, never retried;
  - **P-2:** `fchmod`;
  - **P-3:** the file barrier (`F_FULLFSYNC` on macOS, `fsync` on Linux, with no fallback);
  - **P-4:** `symlinkat`, `readlinkat` and the no-follow `openat` for reading;
  - **P-5:** the no-follow regular open of the operator path;
  - **P-6:** a charged wrapper over `FileLock::try_acquire` in shared or exclusive non-blocking mode.

  Each primitive publishes its price as the law states it: one edge per native call, plus copies as owned records. **Rationale:** the discovery census closure pins `filesystem.rs`, `filesystem/{descriptor_acl_capture, descriptor_filesystem, directory_entries, directory_open, path_binding}.rs`, `work_ledger.rs` and `work_reader.rs` (`tools/security/discovery_census.py`'s `CLOSURE`). A primitive placed in any of them would make the discovery receipt stale for no semantic reason.
- **LD-CIP-2. P-7 is an equal published price, not an exposure.** `path_binding.rs`'s `status_read_cost()` is `pub(super)` and in the closure. `component_tree.rs` therefore publishes `status_read_cost()` with **the identical expression**: one edge, and bytes equal to the larger of `size_of::<libc::stat>()` and `size_of::<std::fs::Metadata>()` (`path_binding.rs`:118-126). A source-pin control (CI-PT-1, §4) reads both definitions and asserts that their expressions are byte-identical. LAW item 4 permits this ("or of an equal published price"), and no closure file changes.
- **LD-CIP-3. The fixture predicate in lifecycle.** `ComponentStore::fixture` and CI-1's emitter are under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` (MC item 8). Lifecycle gains the two features, forwarding to `opensip-security/crash-matrix` and `opensip-security/scenario-fixtures`, never default. A release-build source pin (CI-T11) shows that neither is reachable.
- **LD-CIP-4. The finalization walk's source (`codex-component-install-r5` NBO-1).** LAW item 4's step-4 post-order is **driven by the borrowed authenticated TreeCommitment**, not by a fresh filesystem enumeration:
  - the walk orders the committed rows deepest first;
  - it keeps the current parent stack of handles, opening each directory by `desc` and each file by `fopen` exactly as LAW's `B_install` step-4 rows price them;
  - it makes no `readdir` call. The structure was already checked at V1, and is re-checked at V2.
  So `B_install` needs no listing row for step 4, and CI-T22's call log must show none.
- **LD-CIP-5. Record length `R` (NBO-2).** `R` is the exact canonical-JSON length of `generation.json`'s closed record (LAW item 5): `{archiveDigest, archiveProfileId, catalogRelease: {envelopeDigest, manifestDigest, stableId, version}, closureId, componentManifestDigest, platform}`, with keys in canonical order.
  - **When.** It is computed before acquisition from the authenticated values: `closureId` from C2a-1, and the others from the ordinary reader's release, manifest and artifact row.
  - **How.** CI-2 computes it with a hand length function in the style of C1a3's sealing encoders (`snapshot_seal.rs` `string_len`/`decimal_len`), applying the identity crate's canonical escaping and UTF-8 rules. A control checks it against `opensip_identity::canonical_bytes(..).len()` on every fixture.
  - **The encoder.** The bytes are hand-encoded into one buffer reserved at exactly `R` (the C2a r4 R3-RF-1 lesson: no `canonical_bytes` temporaries).
- **LD-CIP-6. The finalization handle's access mode is selected before the charged open (NBO-3).** For P-2 and P-3 in step 4, CI-2 selects one access mode per supported platform at build time: read-only or read-write, no-follow. It records the choice in a platform table, and qualifies it by a control on each S8 platform it supports (macOS here; LD-D3A-1's macOS-first).
  - **No retry.** CI-2 never tries one mode, fails, and reopens in another: that would add unfunded calls, and break the failure latch and the no-retry rule.
  - **Price.** The `fopen` price is the same for both modes.
  - **Failure.** If the selected mode fails on a supported platform, that is an I/O failure (`EXTENSION.INSTALL_IO_FAILED`), not a retry.
- **LD-CIP-7. The bridge to trust evidence.** CI-2 and CI-3 take the ordinary reader's evidence through C2a-1's `trust::admitted_components` bridge (C2a §2). Its `AdmittedRelease` value is the release row, the retained manifest body and the selected-platform TreeCommitment, all borrowed. CI adds no second trust interface. If C2a-1 lands later than CI-1, CI-2 waits for it.
- **LD-CIP-8. The census and receipt impact, per receipt** (the C1b plan r3 rules: generated-output checks pass after any re-pin; stale receipts are recorded separately from public fields):

  | Sub-unit | Discovery receipt | Companion snapshot receipt |
  |---|---|---|
  | CI-1 | unchanged: a new security file, not in `CLOSURE` | unchanged |
  | CI-2 | unchanged: new files in lifecycle and platform `component_tree.rs`, plus edits to `lib.rs`, lifecycle's `locations.rs` and its `Cargo.toml`, none of them in `CLOSURE` (LD-CIP-1, -2) | unchanged: CI-2 reuses `WorkLedger::snapshot_profile()` by call, and does not edit `work_ledger.rs` or any snapshot model source |
  | CI-3 | unchanged | unchanged |
  | CI-4 | unchanged: host command files | unchanged |

  **The receipts' bound sources at this plan's base** (`3742822e`, after the C1a4-blind gate):
  - **The discovery receipt** binds `discovery_census.py`'s `CLOSURE`, through `receipt_bindings`.
  - **The companion snapshot receipt** binds the discovery bindings, plus its four tools, plus `snapshotSources` (`snapshot_ledger_census.py` `sources()`). Those are `crates/host/src/{candidate_custody, snapshot, snapshot_tests, snapshot_seal}.rs`, `crates/platform/src/{custody_entry, work_ledger}.rs`, `crates/platform/src/filesystem/file_effects.rs`, `crates/security/src/{private_access, snapshot_source, snapshot_walk}.rs`, and the identity bound and encoding sources the tool anchors (`ANCHORED`).

  **So CI must not edit any of them.** In particular, P-1 to P-6 go in the new `component_tree.rs`, **not** in `custody_entry.rs` or `file_effects.rs`, and CI calls `admit_custody_directory` without editing `snapshot_source.rs` or `private_access.rs`.

  **Every sub-unit's lane asserts its "unchanged" claim:** the census-closure check finds no closure file changed, and both census `--check`s pass with their receipts byte-equal to base. **If an implementation needs a closure-file edit,** that sub-unit stops and is re-planned into a census batch, joining one before its freeze or opening its own interval, with receipt-specific deltas.
- **LD-CIP-9. The X-CI-1 gate.** The installer's interim ledger is `WorkLedger::snapshot_profile()` (LAW item 4; accepted interim in `codex-component-install-r2` Q9). X-CI-1's owner is the lead, as DR-103's delivery owner. **The gate:** before any first-party component release is qualified, or before CI-4's command is enabled for production use, whichever comes first, a sourced installation profile replaces the interim. It is derived by the r9 2× rule over a census of the first-party releases' `B_install` values, or by an explicit law revision.
  - **Its census impact.** The sourced profile needs a new `WorkLedger` constructor, which edits `work_ledger.rs`. That file is in the discovery `CLOSURE` and among the companion snapshot receipt's pins. **So X-CI-1's resolution changes both receipts.** It must be sequenced into a reviewed census batch, before that batch's freeze or with its own interval, with a fresh baseline, a pre-run review, the frozen-input blind refresh and a post-run review.
  - **The plan names this unit X-CI-1-a.** It is not part of CI-1 to CI-4.

## 4. Controls, mapped to sub-units

| Control (LAW) | Sub-unit | Notes |
|---|---|---|
| CI-T1, CI-T2, CI-T5 | CI-1 | PKG-AP's exact 15 cases, as codec outcomes. The size-max and mode-field cases are labelled metadata-only. A length mismatch refuses before any write. Capacity refusals happen before any read. |
| CI-T3, CI-T4, CI-T6 | CI-2 | digest, profile and digest-split refusals; the platform-token lookup; `archive-changed` and `archive-read-attempts` |
| CI-T7, CI-T8, CI-T9 | CI-2 (CI-T9's read side is CI-3's) | nothing installed at every step 1-5 failure point; re-install no-op and corrupt refusal; immutability |
| CI-T10, CI-T11, CI-T12 | CI-3 | every typed failure, and exact charges; the fixture store and its release pin; revocation |
| CI-T13 | CI-1, CI-2, CI-3 | source pins: no socket, URL or spawn |
| CI-T14, CI-T15 | CI-2, CI-3 | foreign ACL refuses `Custody`; the ephemeral path writes nothing |
| CI-T16 | CI-4 | every item 8 row's class, code, detail, carrier and remedy, on both paths |
| CI-T17 | CI-3 (CI-2's V1 and V2 for the stage side) | structure: extra, absent, type, link target, association |
| CI-T18 | CI-2 | modes, and bottom-up finalization |
| CI-T19 | CI-2 | crash prefixes through the post-rename barrier, after each `fchmod` and each barrier |
| CI-T20, CI-T21 | CI-3 | pins and GC probes; transfer and its sink gating |
| CI-T22 | CI-2 (`B_install`), CI-3 (`B_open`, `B_transfer`) | independent call-log enumeration over the file-only, nested, metadata-heavy and pre-existing trees; root-level and nested transfers; the custody call chain; the handle discipline at 100,000 entries; and **no `readdir` in step 4** (LD-CIP-4) |
| CI-T23, CI-T24, CI-T25, CI-T26 | CI-2 | the layout; V1 and V2; `LostRace`; the funded suffix, with its split and routes |
| **CI-PT-1** (plan) | CI-2 | P-7's expression identical to `path_binding.rs`'s (LD-CIP-2) |
| **CI-PT-2** (plan) | CI-2 | `R` equals `canonical_bytes(..).len()` on every fixture, and the record is hand-encoded with no temporaries (LD-CIP-5) |
| **CI-PT-3** (plan) | CI-2 | the finalization access mode is selected per platform before the open; a failure is an I/O failure, never a reopen (LD-CIP-6) |
| **CI-PT-4** (plan) | every sub-unit | the census closure is unchanged; no file in the companion receipt's `snapshotSources` or `ANCHORED` set has changed; and both receipts are byte-equal to base (LD-CIP-8) |

## 5. Mutations

Each must fail the controls:
- **CI-1:** a header compared only by its decoded fields; the alternate regular-file typeflag `0x00` accepted; the length checked after reading; a PAX or GNU extension accepted; a pad byte unchecked.
- **CI-2:**
  - a stage created outside the store, or under a subdirectory;
  - a final mode applied after its barrier;
  - V2 skipped;
  - `LostRace` followed by winner verification;
  - cleanup attempted after a failure;
  - the suffix not reserved, or the rename charged twice;
  - `B_install` checked after acquisition;
  - a write retried;
  - a symlink followed;
  - a handle held per entry;
  - `readdir` in step 4;
  - the access mode retried after a failure.
- **CI-3:** a missing `pin.lock` recreated; `generation.json` trusted as authority; an extra entry ignored; a transfer opening `tree/<path>` in one `openat`; a sink committed before verification; an ephemeral read creating a pin; the fixture store reachable without the predicate.
- **CI-4:** a corrupt tree routed as not installed; an ephemeral detail emitted; the in-operation budget routed as `install-budget`.

## 6. Checks

Each sub-unit's lane covers:
- the touched crates' suites at base and candidate: platform serially, as D3a-0's lane does;
- warning-denied all-targets Clippy, rustfmt and the focused tests;
- the release-build source pins;
- the environment exceptions and the operability source census with its mint audit;
- **the census-closure check, and both census `--check`s with byte-equal receipts** (CI-PT-4);
- verify_design;
- the package edges, where CI-2 adds the lifecycle→security edge;
- the mutations.

## 7. Open questions

- **Q1.** Should CI-2 and CI-3 share one package and lane (one review), or go separately? I recommend sharing, since CI-3's controls need CI-2's generations.
- **Q2.** LD-CIP-6's macOS-only qualification. The Linux rows wait for Linux support (LD-D3A-1). Is that acceptable for the law's S8 platform table?

## 8. Not delivered

- X-CI-1-a, the sourced installation profile (LD-CIP-9).
- C2a-3's binding (C2a's), and C2b-1.
- GC's inert-stage removal: the GC owner's (LAW item 7).
- Updates, migration, multi-platform installation and network acquisition (LAW's exclusions).

## 9. Not claimed

- No trust-owner change, and no new key, root or role. The only new features are lifecycle's forwarders of the existing fixture features (LD-CIP-3).
- No public code, no qualification, and no release.

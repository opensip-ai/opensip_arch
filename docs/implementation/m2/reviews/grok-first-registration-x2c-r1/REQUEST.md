Grok review: X2c, first project registration (law X2 r8 item 6) with the registry replacement primitive and the create-or-admit of `I/host`, `I/host/projects` and `.opensip`, plus the write-gate entries for items 2 to 5 and 6a, with inventory v105 (parent v104). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-first-registration-x2c-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/project-root-x2/PROPOSAL.md` r8 (accepted), item 6 with items 1, 3 to 5, 6a, 8 and 9 as they bear on it, and item 10's X2c row. The registry owner is `project-registry-owner-selection-v2/owner.md` ("States and durability", "Initial namespace publication profile"). Integrated predecessors: X2a (8bfc78a, chain walk), X2b-1 (451838d, selection, R0 capture, `ProjectRootAdmission`), X2b-2 (66bdd05, tracking), X1a (ordinary writer), X3a-1 (store endpoint). X2d (leases) and X2e (handoff) are later units and are not built.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x2c`, detached at b642c45 (X12a integrated, inventory v104 selected). Save `git -C <worktree> diff` (the two new files are intent-to-add) as product.diff and report its sha256. Lead's value: 7a211a71e9b0b5f772934c2beec6d845f110fa4d8aeea05e16fbafe61ff905d5, 144097 bytes; 7 files, 3642 insertions, 6 deletions.
- **Arch:** v105 (parent v104: `repository-file-inventory.v104.json`, 355127 bytes, sha256 `1c8dbb12bbede3304b66e378b8565f51811660cd9e8836f0e05729eb721eda7c`), `first-registration-x2c-inventory-v105-subject.json` and `first-registration-x2c-inventory-v105/`.

## What it does

New code: `crates/security/src/custody/first_registration.rs` (macOS module of custody.rs) and its tests. Everything is crate-private, runs on the 468 gate's one ledger under the held fence, and is charged before it runs.

- **Write-gate entries** on `OrdinaryWriteAdmission` (ordinary_writer.rs): `admit_project_root` (X2b-1's items 2 to 5 with the write receipt's premise, then the admission recheck and the gate's recheck), `observe_project_tracking(_with)` (item 6a and its recheck), `register_first_use(_with)`, `recheck_registered`. After each, the write receipt is rechecked. Any refusal spends the gate's ledger (`DurableWriteGate::spend`), so every later step refuses `Latched`. Production passes the process environment and `SYSTEM_SOURCES`; the `_with` forms are the crate seam.
- **Preconditions (before any effect), in order:** FirstUseCandidate with the marker positively absent; `ProjectRootAdmission::recheck` (chain, incarnation, marker, R0 sample, v1 absence); `recheck_tracking` against this admission's chain; the active-transition gate (judgment call 4); a present `host`/`projects` judged private; ProjectId candidates (≤ 8, independent 32-byte draws) against every history row; UUIDv4 N candidates (≤ 8, 16-byte draws) against every recorded N and a no-follow lookup at `I/host/projects/N`; capacity; RESERVED built and validated. Then the gate's full recheck.
- **Capacity (item 8 row `PROJECT.SCOPE_LIMIT`):** `registry-rows:<n>>4096`; `registry-bytes:<n>>4194304` for the RESERVED document, the ACTIVE document and the worst later terminal spelling (every RESERVED row ABANDONED, every ACTIVE row RETIRED, the new row ABANDONED); `registry-transition-rows:<n>>4096` for all non-ABANDONED rows plus the new one. Lengths are exact: each row encoded once, the envelope plus commas added; R0's rows must re-encode to R0's exact bytes.
- **Replacement primitive (`replace`), for RESERVED and ACTIVE:** (1) reconfirm R by its retained descriptor's full sample, then by a no-follow reopen by name with the same sample, and v1 still absent; (2) the `Built` document, made only by `build`, canonical and decoded by `ProjectRegistryDocument::decode`; (3) `project-registry.v2.<32 hex>` created exclusively in I, 0600 with the zero-rights owner allow, written with `F_FULLFSYNC` (`write_new_regular`), receipt checked, then confirmed by a reopen with the same sample and exact bytes; (4) `rename_replace` over the registry; (5) I's directory barrier (receipt `is_for` I, policy kind accepted) and a reopen by name with the new file's sample. The new owner is the temporary file's own descriptor, its post-rename sample and the built document. Steps 3 and 4–5 each reserve their whole work before the effect (`work.effect` + `prepaid`). Temporary files are never removed.
- **R advances only through confirmed publications.** R0 is X2b-1's capture, which now retains its descriptor. After each confirmed publication the gate's retained `project-registry.v2` sample moves by `DurableInstallation::advance_registry(from, to)`, only when it still equals the reconfirmed predecessor. R0 and R1 are dropped as provenance and never rechecked.
- **Step 3:** `I/host` then `I/host/projects`, each created (0700 + zero-rights allow) or, on raw `EEXIST` only, admitted private; then exact name, H's volume and the parent's device, its own barrier and its parent's barrier. Then a private stage under `projects` (the platform's stage primitive) gets the allow; `writer.lease` and `readers.lease` are created 0600 with the allow and written empty with `F_FULLFSYNC`; the stage's barrier; `publish_exclusive` to N (`LostRace` is a change); `projects`' barrier on the publication's parent handle; the exact-name recheck; the footprint confirmed (private dir, exactly the two names, both empty private files).
- **Step 4:** `.opensip` created (0700 + allow) or admitted on `EEXIST`, then S3 directory custody with item 1's premise (`judge_project_object`), exact name, H's volume, `.opensip`'s barrier, the root's barrier. A reused `.opensip` is never changed.
- **Step 5:** the 92-byte marker created no-replace (`EntryExists` is a change), allow, bytes with `F_FULLFSYNC`, `.opensip`'s barrier, confirmed by reopen and bytes.
- **Step 6:** recheck the chain (names, custody, volume, birth) and incarnation, `.opensip` (rebind + custody), the marker (descriptor sample and name), `host`, `projects`, N (rebind + footprint), R1 (inside `replace` step 1), tracking; the transition gate again; ACTIVE built from R1's document (exactly one RESERVED random row at N becomes ACTIVE; never from the candidate IDs); `replace`.
- **Final:** R2 must classify the root `Eligible{N, ProjectId}` with the marker's sample, `RegisteredProject` (non-Clone: chain, selection, incarnation, `.opensip`, marker, `host`, `projects`, the namespace publication, R2, the ACTIVE row, tracking) is rechecked, and the gate's full recheck runs.
- **Rows (item 8), named for the composition owner:** `RegistrationRow` and `ProjectWriteRow` (468 rows through `gate_refusal`, X2 rows, budget). No public projection is built.
- **Supporting edits:** `platform::project_id_draw()`; `DurableInstallation` accessors and `advance_registry`; `DurableWriteGate::{scope, is_spent, spend}`; `RegistryCapture` retains its file; `ProjectRootAdmission::into_parts`; a few `pub(super)` helpers.
- **Test seam (`cfg(test)`):** a hook at eleven points (it may also change the filesystem; `true` injects an I/O failure) and scripted candidate draws.

## Judgment calls: please rule on each

1. **Only the ordinary writer's entry is wired.** Item 6 says "under X1's `OrdinaryWriteAdmission` …, or under the creator's `AdmittedInstallation`". 468c's `route` drops its gate, so an `AdmittedInstallation` has no ledger to charge. The core functions take `(gate, installation, qualification)`, so a creator entry is thin wiring once a composition keeps the gate (X11).
2. **R0 retains its descriptor.** Item 5 says the capture "retains the original file descriptor"; X2b-1's `RegistryCapture` kept only the sample. Step 1 needs it, so the capture now keeps the file it read.
3. **The gate's retained registry sample advances** with each confirmed publication (`advance_registry(from, to)`). Without it the gate's recheck set, which compares `project-registry.v2` by full sample, would fail after RESERVED. Any other change still fails.
4. **The active-transition-recovery gate.** No transition carrier exists in the product, and the active-slot layout is not selected law. P0's `transitions` holds only `lineage`, so any other entry there might be a slot: it refuses as unavailable (468's incomplete row), before RESERVED and again before ACTIVE. An absent `transitions` has no slot.
5. **No interrupted-finish for `host`/`projects`.** Item 6 cites 465 item 3, not item 5. A reused directory must already be private (0700 with a readable ACL). A crash between `mkdirat` and the allow therefore leaves a directory that refuses as `InstallationCustody("private")` until a separately authorized recovery.
6. **Parents judged before RESERVED.** A present `host` or `projects` that is foreign refuses before any effect, rather than after RESERVED in step 3. Step 3 still create-or-admits them with both barriers.
7. **Entropy.** ProjectIds use a new `project_id_draw()` (one 32-byte draw per candidate), because `request_entropy` documents "never an input to semantic identity" and `recovery_nonce` is a recovery challenge. N (a locator) and temporary-name nonces use `request_entropy`. Failure or exhaustion is the host I/O row.
8. **Capacity arithmetic.** Exact per row, as described. The transition-wrapper check is subsumed by the row check at 4096 but kept explicit. The order is rows, bytes (RESERVED, ACTIVE, terminal), then wrapper.
9. **Namespace staging.** The platform's stage primitive (fixed `.opensip-stage-install-` prefix, random name, no recovery authority). The leases get file barriers through `write_new_regular(b"")`.
10. **Row choices.** `NotFirstUse(Eligible)` is invariant (a broken composition). RecoveryNeeded and OneSided are `identity-recovery-required`; Contradiction is `identity-contradiction`. A changed owner is X2b-1's `required-files-changed`. Installation-private custody is 468's custody row. Project objects use `PROJECT.ROOT_CUSTODY_REFUSED` (`marker-directory-custody`, as X2b-1). Entropy, exhaustion, I/O and barriers are host I/O, and a receipt for another handle is invariant.
11. **Changed before custody.** A retained file whose sample differs (unlinked or replaced included) is a change, judged before privacy, so a replaced marker reads as a change, not as `LinkCount`.
12. **Binding the tracking observation.** `TrackingObservation` carries no chain identity, so registration rechecks it against this admission's chain before any effect and again in step 6.
13. **Latch without release.** The entries take `&mut self` and spend the gate on any refusal (including the receipt's recheck). The fence stays held until the caller drops or releases the writer, unlike X3a's consuming `admit_store_endpoint`. X2d/X2e decide the release.
14. **Reservations.** Each effect reserves the sum of the published costs of its effect and confirmations. Create-or-admit reserves both branches, and some fixed charges are the lead's (`EXACT_NAME`, scans, read-back). Coverage is shown by the success paths: a short reservation would fail closed.
15. **Stale description.** `ordinary_writer.rs`'s row ("no … project … standing") is now further out of date. v105 carries it by value and defers it to the description-only successor already named at inventory97, 102 and 101.

## Tests

`first_registration_tests.rs`, 13 tests, on `ReadFixture` scratch homes (`<temp>/opensip-test/<pid>-<nanos>/…`), with an ordinary writer over signed test trees, an empty environment and no system sources:
- **Pure parts:** UUIDv4 version and variant, decoded by the registry decoder; exact document lengths, later spellings exactly one byte longer for live rows, and exact re-encoding; S12 subjects and identity rows.
- **Whole act:** one ACTIVE random row with the root's path and incarnation; `host`, `projects` and N at 0700; exactly two empty 0600 leases; `.opensip` 0700 holding only the exact 0600 marker; no temporary file left; `recheck_registered` passes (the gate's sample advanced); after release a read session classifies Eligible; a second writer's registration refuses (invariant) with one row.
- **Reuse:** a 0755 no-ACL `.opensip` and existing private parents (with another N) are admitted, and `.opensip`'s mode is unchanged.
- **Before any effect:** Eligible (invariant), RESERVED and one-sided (recovery-required); a `.hg` created after the observation (`vcs-unsupported`); `transitions/active.slot` (incomplete); a 0755 `host` (installation custody `private`). The registry bytes are unchanged and nothing is created.
- **Candidates:** eight ProjectId draws colliding with a RETIRED row's id; eight N draws hitting an occupied path (9 draws in total); failed entropy. All are host I/O with the registry unchanged.
- **Capacity:** 4096 RETIRED rows (`registry-rows:4097>4096`); a registry 64 bytes under the cap (`registry-bytes:n>4194304`); ACTIVE rows where RESERVED fits but the terminal spelling does not (the exact `registry-bytes` subject).
- **Stops:** at each of the eleven points: host I/O, the writer spent, the exact durable prefix (registry status, parents, stage, N, `.opensip`, marker size), the read classification (FirstUse at the first stop, RecoveryNeeded, Contradiction for the empty marker, Eligible after ACTIVE's rename), and a temporary file only where its rename did not run.
- **Changes:** the registry rewritten in place before step 6 (changed, RESERVED stays); the marker replaced after it was written (changed, no ACTIVE); the marker replaced after ACTIVE's temporary file (the final recheck refuses); a registry change after registration seen by `recheck_registered`.

## Checks

- X2c tests 13/13.
- Full workspace at b642c45 plus this diff, two runs: 1379 passed, 0 failed, 3 ignored each time.
- Clippy `--workspace --all-targets --offline --locked -D warnings`, `cargo fmt --all --check`, and `rustfmt --check` on both new files are clean.
- `~/Library/Application Support/OpenSIP` is absent.
- `check_package_edges --lane host` against v105 passes.
- verify_scratch (v105 appended over the real lock at b642c45) passes: 70 inventory successors, 71 contract successors, 16 inheritance rows, v105 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v105.py` reruns produce the same bytes.

## Decide

- Does X2c implement item 6 exactly? In particular:
  - every precondition before any effect;
  - the five-step replacement primitive, with the file barrier before the rename and never no-replace on the registry name;
  - R0 to R1 to R2 only through confirmed publications, R0 never reconfirmed after RESERVED, and ACTIVE built from R1;
  - the namespace's complete two-file footprint, published no-replace with its parent's barrier;
  - `.opensip` and the marker with their barriers;
  - step 6's recheck of the current owners;
  - latching with no retry and no deletion;
  - the durable prefixes.
- Rule on the judgment calls, in particular 1, 3, 4, 5 and 10.
- Is v105 right on v104?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `first-registration-x2c-inventory-v105-subject.json`;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v105, parent (the v104 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

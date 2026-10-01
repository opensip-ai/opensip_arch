# Review: first registration X2c r1

Verdict: ACCEPT-UNIT.

Worktree `/Users/sb/code/opensip-ai/opensip-x2c` is detached at `b642c45a77cf38a0ab8ebf949548ce4eca1f410d`. `product.diff` is 144097 bytes, sha256 `7a211a71e9b0b5f772934c2beec6d845f110fa4d8aeea05e16fbafe61ff905d5`, 7 files, 3642 insertions, 6 deletions. The seven product files match hashes.txt. Subject manifest `docs/implementation/m2/first-registration-x2c-inventory-v105-subject.json` is 2162 bytes, sha256 `968030e99bf7069f948cefd6f4f934dcd76a1617a0112adffd25d7b60e8692e0`. Inventory v105 is 359222 bytes, sha256 `ebd9cf3361d4f854adcfbe8fcffd8e6e5ca9bd0af38315f950638212b5934a08`, parent v104 `1c8dbb12bbede3304b66e378b8565f51811660cd9e8836f0e05729eb721eda7c` (355127 bytes). `~/Library/Application Support/OpenSIP` is absent.

## Item 6

`register_on_gate` runs the preconditions on the gate's ledger before any publication, then the gate's full recheck. The order is: FirstUseCandidate with the marker positively absent; `ProjectRootAdmission::recheck` (chain, incarnation, marker, R0 sample, v1 absence); `recheck_tracking` against this admission's chain; the active-transition gate; a present `host` or `projects` judged private; at most eight ProjectId draws and eight UUIDv4 namespace draws against every history row and a no-follow occupancy lookup; capacity; RESERVED built and decoded. A refusal from any of those returns with the registry bytes unchanged.

The replacement primitive is `replace`, used for RESERVED and ACTIVE. It reconfirms R by the retained descriptor's full sample and by a no-follow reopen under I, and rechecks that `project-registry.v1` is absent. The document is the `Built` value from `build`, which canonical-encodes and decodes with `ProjectRegistryDocument::decode`. The temporary name `project-registry.v2.<32 hex>` is created exclusively in I, mode 0600 with the zero-rights owner allow, written through `write_new_regular` (`F_FULLFSYNC`), and confirmed by a reopen with the same sample and exact bytes. `rename_replace` then replaces a regular `project-registry.v2`. I's directory barrier follows, and the name is reopened against the temporary file's own descriptor. The temporary file is never removed. Each of those two effects reserves its whole cost before it starts.

R0 is the capture's retained descriptor (`RegistryCapture` now keeps the file it read). After RESERVED is confirmed, `advance_registry` moves the gate's retained `project-registry.v2` sample only when it still equals that predecessor, and R0 is dropped. ACTIVE is `plan_active` over R1's decoded document: the one RESERVED random row at N becomes ACTIVE. R1 is dropped after that publication is confirmed. R2's row is what `RegisteredProject::classification` reads.

Step 3 create-or-admits `I/host` then `I/host/projects` (0700 and the zero-rights allow on creation; raw `EEXIST` admits a private directory and changes nothing). Each gets its own barrier and its parent's. A private stage under `projects` receives the allow; `writer.lease` and `readers.lease` are created 0600, written empty with `F_FULLFSYNC`; the stage is barriered; `publish_exclusive` to N treats `LostRace` as a change; `projects` is barriered on the publication's parent handle; the exact name and the two-file empty footprint are confirmed.

Step 4 create-or-admits `.opensip` and judges it with `judge_project_object`, then `.opensip`'s barrier and the root's. A reused directory is not restated. Step 5 creates the 92-byte marker no-replace (`EntryExists` is a change), writes it with `F_FULLFSYNC`, barriers `.opensip`, and confirms the bytes.

Step 6 rechecks the chain and incarnation, `.opensip`, the marker by descriptor and by name, `host`, `projects`, N's footprint, R1, and the tracking observation, runs the transition gate again, then replaces. The final scope requires `Eligible { N, ProjectId }` with an ACTIVE row, rechecks `RegisteredProject`, and the gate's full recheck runs. `settle` spends the gate on every refusal, including the receipt's recheck, and leaves the fence held.

The eleven stop points in `each_stop_leaves_its_durable_prefix_and_spends_the_writer` cover the durable prefixes: before RESERVED's rename the predecessor is still the registry name; after each confirmed publication the new owner is what the later recheck sees.

## Judgment calls

1. Only the ordinary writer's entry is wired. `installation_routing::route` admits on a gate and returns `AdmittedInstallation` with the installation alone, so that gate's ledger is dropped. `register_on_gate` already takes `(gate, installation, qualification)`.
2. `RegistryCapture` retains the descriptor `capture_registry` read, and `into_parts` hands that file to R0.
3. `DurableInstallation::advance_registry` replaces the retained `project-registry.v2` sample only when it still equals `from`. The final gate recheck compares that sample.
4. `transitions_quiet` treats an absent `transitions` as no slot. Any directory entry other than `.`, `..`, and `lineage` refuses as the incomplete row, before RESERVED and again before ACTIVE.
5. Create-or-admit applies the allow only on the created branch. A directory left between `mkdirat` and the allow fails `observe_private_directory` as installation custody `private`.
6. `observe_parents` judges a present `host` and `projects` private during the preconditions. Step 3 still create-or-admits them with both barriers.
7. ProjectIds come from `project_id_draw` (one 32-byte `getrandom` fill). Namespace candidates and the temporary-name nonce come from `request_entropy`. A short draw is `Entropy` and eight collisions are `Exhausted`; both are the host I/O row.
8. Capacity is rows, then the exact canonical lengths of the RESERVED document, the ACTIVE document, and the worst later terminal spelling (every RESERVED row ABANDONED, every ACTIVE row RETIRED, the new row ABANDONED), then the non-ABANDONED wrapper count. R0's rows are re-encoded and must equal R0's bytes, and the built RESERVED length must equal the predicted length. The wrapper count is at most the row count, and the check still runs.
9. The namespace stage is `create_private_directory_stage_accounted`. The two leases get their file barriers from `write_new_regular(b"")`.
10. `NotFirstUse(Eligible)` and a FirstUseCandidate whose marker observation is not absence are `Invariant`. RecoveryNeeded and OneSided are `identity-recovery-required`. Contradiction is `identity-contradiction`. `Changed` is `ProjectAdmissionRow::RequiredFilesChanged`. Installation-private custody is `InstallationCustody`, and project objects use `PROJECT.ROOT_CUSTODY_REFUSED` with `marker-directory-custody` for `.opensip`. Entropy, exhaustion, I/O, and barriers are host I/O. A barrier receipt for another handle is `Invariant`.
11. `same_private` returns `Changed` when the full sample differs, and judges privacy only after that comparison.
12. `recheck_tracking` runs against `admission.chain()` in the preconditions and again in `recheck_current`.
13. The four writer entries take `&mut self` and `settle` spends the gate without releasing the fence. `admit_store_endpoint` remains the path that releases on refusal.
14. `effect` reserves the declared sum and `prepaid` runs the body inside it. Create-or-admit's cost includes both the create branch and the admit branch. The thirteen success and refusal tests run inside that reservation; a short reserve fails closed before the effect.
15. v105's row for `ordinary_writer.rs` is the v104 row by value. The description still says the writer grants no project standing. The same later description-only successor remains the place that refreshes it.

## Inventory v105

v105 keeps all 783 v104 file rows by value, in path order, and adds `first_registration.rs` and `first_registration_tests.rs`. `packages` and `pendingDecisions` are unchanged. The standing text names this unit. The successor's parent pin is v104, and its sixteen description-override rows are the projection bound to that parent. `verify_projection.py` against the worktree lock reports 16 rows and 83 corruptions refused. `verify_scratch.py` on this worktree passes: 70 inventory successors, 71 contract successors, 16 inheritance rows, v105 selected. `check_package_edges.py --lane host` against v105 passes. No new crate edge.

## Replay

`opensip-security` lib filter `first_registration::tests`: 13 passed, 0 failed. `rustfmt --check --edition 2024` on both new files is clean. `verify_scratch`, `verify_projection`, and `check_package_edges --lane host` passed as above. The full workspace suite and workspace clippy were not replayed. No product cargo ran outside `CARGO_TARGET_DIR` under this review directory.

Required findings: none.

Grok review 467a and 467b (stage, validate, publish, routes and handoff) and inventory74, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-publication467ab-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

**SAFETY: never run the creator against the real home. Every effecting test uses a scratch chain. After your replay, confirm ~/Library/Application Support/OpenSIP still does not exist.**

Law: docs/implementation/m2/initial-publication-467/PROPOSAL.md items 1–11 and the P0 tree (accepted), with owner §1a step 6, §2–§6, and 465 items 9–11. Product HEAD f0a29bc. hashes.txt pins every uncommitted file:
- new: custody/installation_stage.rs (S0–S7), custody/installation_publication.rs (S8–S10, Outcome, `create_initial_installation`), custody/installation_publication_tests.rs;
- edits: custody.rs; initial_installation.rs (`recheck_handoff_storage`, `recheck_storage_in`, `recheck_actor_in`); installation_parent.rs (`recheck_names_in`, test-only `prepare_installation_parent_at`); initial_core.rs and initial_platform.rs (`recheck_in` made `pub(crate)`); trust.rs and root_payload.rs (StateWriter export); clock_observation.rs (`project_creation_observation`); initial_manifest.rs (`Manifest::reread`).

## Summary

S0–S10 follow the law. There are 44 barrier slots, each checked with `is_for`:
- stage 0/1;
- directory i: own 2+2i, parent 3+2i;
- file j: containing directory 30+j;
- pre-rename 41/42;
- I-parent 43.

The fence is first and locked until S9 completes. S8 uses the typed classification:
- LostRace: the lock is released, `Outcome::Existing(LostRace)`, and the stage stays;
- NotPerformed: refuse;
- Indeterminate: latch, release the lock, no barrier.

S9 order: the name, then the I-parent barrier, the fence identity, I dev/ino equals the stage's, a filesystem sample of I, then the chain names and core, platform, actor and storage rechecks inside `prepaid(2 × Δ_owner)`. S10 releases the lock and returns `Published{target, S, K, closure, invocation ids, command}`: no handles, locks or authority. The top-level `create_initial_installation` maps NotPristine to `Outcome::Existing(NotPristine)`. Library only.

Deviations for your judgement:
1. The fence's name and identity recheck runs before the flock; the locked descriptor is then checked again, all in the same effect.
2. The chain-name recheck is inside `prepaid`, and Δ_owner measures the same five rechecks.
3. The stage-parent barriers use `stage.parent_directory()`.
4. `publish_exclusive_reserved` closes the ledger on every failure, so LostRace also latches.
5. A budget failure after the rename is reported as `AfterRename(Budget)`.
6. There is no end-attempt API; the caller drops the attempt.
7. Uncharged platform calls (`recheck_exact_name`, flock, the locked-descriptor observation) are charged by conservative security-side constants. S1's entropy, clock and copies share `INPUTS_COST`.
8. Indeterminate is exercised by a security seam that spends the rename cost without renaming.
9. In tests `Published.target` is the disclosed real I path, while the act ran on the scratch chain.

## Tests

There are 12 (see the implementer report). They cover: the happy path, with an exact tree, modes, ACLs, 44 FullFlush barriers, the fence busy during the act and free after, and existing readers reading the pair, marker, node and state.v1; the loser route; a moved stage; Indeterminate; barrier failures at 0, 9, 30, 40, 41 and 43; the Fsync fallback; short ledgers before the stage, directory 0, the fence and the rename; validation refusals; an owner change before the rename; a two-thread race giving exactly one Published and one LostRace; and NotPristine.

Not covered: NotPristine at mint, a prepaid overrun after the rename, `recheck_handoff_storage` refusing, read I/O errors, and a real OS Indeterminate.

Budget for one full creation: an attempt total of about 5.6k objects, 59.5k edges and 40 MB, against caps of 65,536, 131,072 and 256 MiB. The rename reservation is 930 objects, 8,295 edges and 924 KB.

## Inventory74

v73 plus installation_stage.rs and installation_publication.rs (service) and installation_publication_tests.rs (test): 731 rows, the helper is byte-identical and gives PASS, and a scratch verify_design passed.

## Lead's replay

The workspace, with `--no-fail-fast`, is 1066/0. Clippy and fmt pass. ~/Library/Application Support/OpenSIP is absent before and after.

## Decide

Does the composition implement 467 items 1–11 exactly? Specifically:
- Is every effect reserved first?
- Is the rename classification handled exactly, and is Indeterminate never treated as success or as a loss?
- Is the lock lifetime right?
- Is `Published` inert?
- Is validation complete before the rename?
- Is the post-rename order barrier first, then rechecks?
- Are the deviations acceptable?

Is v74 exactly v73 plus three rows?

**Output format:** review.json must contain:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectManifestSha256": a single string, from subjects.txt;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of repository-file-inventory.v74.json, parent (v73 pin), successorRecord (the pin of the v74 unit's successor.json)}.

Replay the security and platform libs, the workspace, clippy and fmt. Write REVIEW.md and review.json. Do not commit.

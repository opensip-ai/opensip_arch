# C1b-1 r2: the snapshot's Git reads (M3-C r8 item 4; C1b plan r6, sub-unit C1b-1)

**Unreviewed candidate, round 2.** It answers Codex `codex-c1b-1-r1` (REQUIRED-FINDINGS: C1B1-R1-RF-1, with rulings on Q1 and Q2). The plan is C1b plan r6 (`c1b/PLAN-r6.md`; `codex-c1b-plan-r6`, ACCEPT; published ARCH `ad85d0b8`). Round 1's package (`c1b-1-r1/`) is history and unchanged. Nothing is submitted, committed or integrated.

## r1 dispositions

| Finding or ruling | r2 | Where |
| --- | --- | --- |
| **C1B1-R1-RF-1** (repository-proof construction allocated, uncharged) | **The proof is built with no allocation, so nothing is left to charge.** r1's `RepositoryProof::retained` collected the spelling's components into a `Vec<&[u8]>`, built two owned labels per candidate ancestor, and cloned X2's sample. r2 compares each candidate in place:<br>- **the label:** `components_prefix` borrows the spelling's first `i` components, and `is_dot_git_label` tests item 6a's label of that `.git` (`<prefix>/.git`, as `repositories` builds it) by length, prefix and suffix;<br>- **the sample:** the proof holds `&'a DescriptorMetadata`, borrowed from the operation's own observation, which outlives the lending;<br>- **unchanged:** the identity binding, the `Untracked` precondition and the innermost-first order.<br>No charge site is added, so the model, the vectors and the derivation are unchanged (§ The derivation). | `custody/git_tracking.rs` (the appended block) |
| (RF-1) the harness | **The exact-charge test builds the subject and the lent root inside the ledger's scope** (`Observed::vcs`). The 9 cases' charges are unchanged: the proof's construction charges nothing because it allocates nothing. | `snapshot_vcs_tests.rs` |
| (RF-1) controls | **Two controls are added** (24 tests in all):<br>- `the_proof_selects_the_innermost_repository_at_every_depth`: three nested repositories, and roots 40 directories below the innermost, at the innermost, below and at the middle one, and between and at the outer one. Each names the innermost repository's own chain index and resolves its commit;<br>- `the_subject_is_built_without_allocating`: a source control. Over the proof, its two helpers, `snapshot_source.rs`'s `repository_proof` and `from_operation`, no allocating construct appears in code (`Vec`, `vec!`, `collect`, `label`, `to_vec`, `clone()`, `format!`, `String`, `Box`, `to_owned`, `concat`, `join(`), and the sample is borrowed.<br>**Two mutations are added** (13 in all): an allocation reintroduced into the proof (`proof-allocates-a-label`, caught by the source control) and the borrowed prefix one component short (`components-prefix-off-by-one`, caught by the nested-selection control). A label-length mutation was tried first and dropped as an equivalent mutant: item 6a's evidence holds no longer `.git` label below a chain directory, so the length check changes no outcome (`evidence/c1b1-checks-r2-void-attempt1/`). | § Tests; § Checks |
| **Q1 ruling** (accepted) | **Recorded as an explicit adjustment to PLAN-r6 §4's one-over control** (LD-C1B1-5): S3 config-file custody refuses a stable file over 4 MiB before any read, as `head-custody`, `loose-ref-custody` or `packed-refs-custody`. A file of exactly 4 MiB is read under the shared budget and parsed. `<file>-oversized` remains for growth after judgment. No cap is raised and no custody bypassed. | LD-C1B1-5 |
| **Q2 ruling** | **The separate VCS derivation suffices;** per-entry census rows need not price the VCS envelope (LD-C1B1-8). The row model identifies what it prices. All work that is not a row, VCS included, shares r9's remaining margin. | LD-C1B1-8 |

## Base and interval

- **Product base:** main as `source.json` records it (`productBase`, the lane's own base). It holds:
  - C1a4's blind refresh (`0772eb7`), the C1b batch's accepted baseline;
  - C1b-0 (`c9c18f7`, contract 176 at `9ea2d4a`), which opened the C1b census batch;
  - C1c-0 (`813d559`), which joined it;
  - C2a-1 with inventory v223 (`01769e9`), D2b-3a (`feb7739`) with inventory v224 (`59144e0`), CI-1 (`f05c5d5`) with inventory v225 (`50f1ac1`), C2a-2 (`1749259`) with inventory v226 (`5de9fd4`), D3a-3's supervisor and operability units (`d704ed4`), and C2a-3k (`274dccc`), the lane's base.

  None of these touches a C1b-1 path or a census input. C2a-1 and CI-1 each appended to security `lib.rs`, and C1b-1's append follows theirs. The lane moves the worktree onto main itself once it holds the lock, only when nothing main changed is a candidate path, and re-runs the preparation there (`worktree-base.json`, `preparation.json`). (Round 1's lane had two void attempts that stopped at that precondition before running any check; they are in `c1b-1-r1/evidence/`.)
- **The interval (LD-C1B-7):** C1b-1 is the batch's second C1b sub-unit. Both receipts stay stale until the batch's one reviewed refresh after C1b-2. The integrate script requires the batch to be open and unfrozen.
- **Candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1b1`, detached at the product base, holding exactly the bytes `product-map.json` lists: 13 files, 3 of them new.

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/snapshot_vcs.rs` (new) | `observe_vcs`: the subject's repository or members; `HEAD` in its closed forms; loose refs; `packed-refs`; the ref grammar; per-read custody; the evidence recheck; the record's canonical length; typed `VcsRefusal`. |
| `crates/security/src/snapshot_vcs_tests.rs` (new) | 24 controls (§ Tests). |
| `crates/security/src/snapshot_vcs_vectors.json` (new) | The model's VCS predictions: 9 native cases, 2 reach pricing cases, the largest record. |
| `crates/security/src/custody/git_tracking.rs` (base-dirty; appended) | `RepositoryProof` with `retained` (r2: allocation-free, with `components_prefix` and `is_dot_git_label`), `directory` and `sample`; X2's helpers exposed `pub(crate)` with no change; `reach_member`; `NoRepository::chain`. |
| `crates/security/src/lib.rs` (base-dirty; appended) | `pub mod snapshot_vcs`, after C2a-1's own append. |
| `crates/security/src/snapshot_source.rs` (base-clean) | `VcsSubject` in `SnapshotRoot`, set by `from_operation` from the operation's own proofs. `repository_proof`. `tracking()` is unchanged. |
| `tools/security/snapshot_ledger_model.py` | The VCS term: `VcsModel`, `vcs_envelope`, `vcs_record_max`, its anchors, cases and the third output. |
| `tools/security/discovery_census.py` | The CLOSURE row for `git_tracking.rs`, re-pinned. |
| `crates/security/src/custody/discovery_census.json`, `discovery_census_vectors.json`, `discovery_workspace_ledger.json`, `snapshot_ledger_census.json`, `snapshot_ledger_vectors.json` | Regenerated by the tools' own `--write` modes. Only pins move (§ Census). |

No caller is added. `operation_handoff.rs` is not edited: the proof is taken in `snapshot_source.rs` (LD-C1B1-1).

## Lead decisions (implementation)

- **LD-C1B1-1. Where the subject is built.** PLAN-r6's LD-C1B-1 builds the subject "as `NoRepository::retained` is (`operation_handoff.rs`:391)". An `impl ProjectOperation` appended to the base-dirty `operation_handoff.rs` would fall after its test module, which Clippy's `items_after_test_module` refuses, and the module cannot be moved without editing base bytes. So `snapshot_source.rs` takes the proof itself, through the existing `ProjectOperation::subject()`, from the subject's own chain and tracking observation, exactly as `member_precondition` does. `RepositoryProof::retained` is the only constructor. It returns the proof only for an `Untracked` observation over this very chain, by its identity, naming the first `.git` sample in X2's evidence, which X2 records walking upward from the root: the innermost repository.
- **LD-C1B1-2. W is the `NoRepository` proof's own root.** Members are reached from `proof.chain().root()` (`NoRepository::chain`, appended), as item 6b takes W from its proof. A member's `.git` must be on W's device, or it refuses `member-outside-volume`.
- **LD-C1B1-3. `packed-refs` duplicates, with no per-line allocation.** LD-C1B-6 forbids a per-line allocation beyond the charged buffer, and LD-C1B-2 refuses a duplicate name. Names must therefore be in strictly ascending byte order, which also refuses a duplicate. This is how Git writes the file: its `sorted` trait (`git pack-refs` here writes `# pack-refs with: peeled fully-peeled sorted `, with a trailing space, which the header rule admits). An out-of-order file refuses `packed-refs-malformed`. This narrows the closed subset; it admits nothing Git would reject.
- **LD-C1B1-4. Ref names are UTF-8.** The leaf is opened through `RetainedDirectory::open_regular(&str)`, so a target or packed name that is not UTF-8 refuses `ref-name`. This is a narrowing too.
- **LD-C1B1-5. One byte over the cap is refused by custody, before the read (r2: accepted by the Q1 ruling, an explicit adjustment to the plan control).** S3 config-file custody already refuses a file over `MAX_CONFIG_BYTES` = 4 MiB (`custody.rs`:4; `project_chain.rs`:849), which equals `INDEX_CAP`. A file at exactly 4 MiB is read. One byte more refuses `<file>-custody` (`head-custody`, `loose-ref-custody`, `packed-refs-custody`) before any byte is read. The read cap's `<file>-oversized` is reached only by a file that grows between its judgment and its read. PLAN-r6 §4 names `-oversized` for the one-over control; the controls assert what the code does. Codex accepted this (`codex-c1b-1-r1`, Q1) as an explicit adjustment to that control.
- **LD-C1B1-6. Refusal spellings the plan leaves open,** each in X2's form:
  - `head-missing`;
  - `loose-ref-malformed`, a loose ref neither `<40hex>\n` nor symbolic;
  - `ref-not-directory`, a link or non-directory ref segment;
  - `ref-custody`, `head-custody`, `loose-ref-custody`, `packed-refs-custody`;
  - `git-custody`, `git-not-directory`, `repository-off-home-volume` and `evidence-off-home-volume`, X2's own;
  - `evidence-changed`, X2's.

  A member's refusals keep the member projection: `member-vcs-unsupported:<reason>`, or `member-outside-volume`. The lone `@` and a leading `/` as `HEAD`'s target are not `ref: refs/` forms, so they refuse `head-malformed`; as `packed-refs` names they refuse `ref-name`.
- **LD-C1B1-7. The public refusal type.** `MemberRefusal` is crate-private, so `VcsRefusal::Member { index, refusal: MemberVcsRefusal }` carries a public mirror with the identical `subject()`, and the index of the member in the record's `memberRepositories`. `Internal` reasons are `cross-root-record`, `members-over-limit`, `members-without-no-repository`, `member-path` and `marker-tracked`. The same-root check runs whenever a record is passed, with or without members.
- **LD-C1B1-8. The census prices no VCS read.** The snapshot census's per-entry pricing and its source bindings are unchanged. The VCS term is bounded by the derivation (§ Derivation), not measured per T2 entry, and the companion receipt changes only through its tool pins. Codex ruled (`codex-c1b-1-r1`, Q2) that the separate VCS derivation suffices and per-entry rows need not price it.

## The derivation (LD-C1B-6)

`evidence/vcs_derivation_c1b1.py` takes the term from the product model itself (`vcs_costs` and `vcs_envelope`, never restated). It adds the term to the accepted cumulative subtotal: r9's adopted subtotal plus C1c-0's retention term, 776,740 objects, 6,218,464 edges and 2,539,929,154 bytes. It then searches as PLAN-r6 does. The lane's `vcs-derivation.json` records:
- **D\* is reproduced: 226** ref directories per repository. Edges bind it.
- **The model's H\* is larger than the plan's: 1,363,957 bytes, against 1,048,575.** The difference is reported here, as LD-C1B-6 requires:
  - the plan priced a retained copy of `HEAD`'s target, `owned(H)` per repository, and a status read after each Git file's judgment;
  - the code makes neither. It resolves the target from the charged read buffer, and its file custody takes no status sample.

  So at every point the model charges no more than the plan priced.
- **At the plan's coordinates** (D = 226, H = 1,048,575), the model's term is 173,706 objects, 2,164,854 edges and 1,577,723,559 bytes. That is within the plan's 173,770, 2,165,048 and 1,645,984,870 in every component (`modelTermWithinPlanTerm`), and the plan's coordinates hold under the model.
- **The record's maximum** is 1,573,798 bytes (`vcs_record_max`), equal to the plan's.

## Census (LD-C1B-7)

- **The closure re-pin:** `discovery_census.py`'s CLOSURE row for `git_tracking.rs`, to the candidate's bytes. It is the only closure file changed (`census-closure-changed-as-expected`).
- **The regenerated outputs:** `prepare_c1b1.py` runs the model's and the three census tools' ordinary `--write` modes over the lead-readable cache. They never open a held-out store, and both receipts' bytes stay unchanged. Each output differs from main's in its pins only. Main's records already render every held-out row `outstanding: held-out (blind receipt stale)` (since C1b-0).
- **The `--check`s pass:** model, discovery census, workspace ledger and snapshot census.
- **The stale record, separate and cumulative** (`evidence/receipt_specific_record_c1b1.py`), from public receipt fields only, per receipt:
  - the baseline bytes equal the refresh's (`0772eb7`) and C1b-0's recorded pins;
  - the batch so far (main's bindings against the receipt) is exactly C1b-0's and C1c-0's together;
  - C1b-1's own delta (the candidate against main) is exactly:
    - for discovery, `closure: [git_tracking.rs]` and `tool`;
    - for the companion, that nested `discovery` delta, `tools: [discovery_census.py, snapshot_ledger_model.py]` and `snapshotSources: [snapshot_source.rs]`;
  - the cumulative delta is their union;
  - every held-out row renders stale, with `heldOutMargin: outstanding`.

## Tests (`snapshot_vcs_tests.rs`, 24)

Each is mapped to PLAN-r6 §4 for C1b-1:
- **r2 (RF-1):** `the_proof_selects_the_innermost_repository_at_every_depth`; `the_subject_is_built_without_allocating`.
- **C1-T15:**
  - `no_repository_and_no_member_is_none`: no charge;
  - `head_through_a_loose_ref`;
  - `head_through_packed_refs_with_and_without_the_header_and_with_peels`;
  - `a_detached_head`;
  - `an_unborn_head_refuses_unborn_head`;
  - `the_innermost_of_nested_enclosing_repositories`.
- **Loose over packed:** `a_loose_ref_wins_over_packed_refs`.
- **Closed-form refusals:** `each_closed_form_refusal`, covering `head-malformed` (CRLF, uppercase, no LF, not `refs/`, lone `@`, leading `/`, empty), `symbolic-ref-chain`, `loose-ref-malformed`, `packed-refs-malformed` (garbage, duplicate, out of order, orphan peel, double peel, no final LF, header not first) and `head-missing`.
- **Grammar:** `every_ref_name_rule_refuses_ref_name_in_head_and_in_packed_refs`, one case per rule, as `HEAD`'s target and as a packed name, including `a..b` and `topic.` and non-UTF-8.
- **r6 long components and the FIFO:** `a_too_long_target_component_refuses_ref_name` (300 bytes as a directory and as the leaf, `ENAMETOOLONG`; 1,100 bytes, `InvalidInput`); `a_fifo_as_head_refuses_head_not_file`.
- **Custody:** `custody_refusals`: a group-writable `HEAD`, a hard-linked `packed-refs`, a symlinked `refs` directory and ref segment, a symlinked loose ref, and a group-writable ref directory.
- **Evidence:** `evidence_changed_when_dot_git_is_replaced`.
- **Caps:** `each_git_file_at_exactly_the_cap_is_read_and_one_over_refuses` (LD-C1B1-5).
- **r4 regime:** `a_deep_target_past_the_remaining_budget_refuses_budget`. With each component one under the native charge, the refusal is typed `Budget`, never an observation.
- **Join:** `a_cross_root_record_and_members_under_a_repository_refuse_internal`.
- **Members:**
  - `two_members_resolve_one_loose_and_one_packed`, then a moved `.git` (`member-vcs-unsupported:evidence-changed`) and a marker between W and M (`vcs-other`);
  - `a_members_refusals_keep_the_member_projection`;
  - `a_member_reached_through_a_deep_multibyte_path`: the r5 review's 256-segment path of four-byte scalars, made one relative step at a time.
- **R4-RF-1:** `the_record_length_equals_the_canonical_encoding`: every escape class, DEL, C1, 2- to 4-byte UTF-8, and the 64-member maximum, 1,573,798 bytes.
- **Charges:** `the_observation_charges_exactly_the_models_vcs_term`.
  - Each of the 9 vector cases is built and observed natively, and its charge equals the model's exactly (C1a2's method).
  - The reach pricing control compares the model's reach with the platform's own `open_child_directory_cost`, status and `child_absence_observation_cost` over the 16 × 255 four-byte path and the 256-segment path. The 16 × 255 path cannot exist on APFS (NAME_MAX), so it is priced, not built.
- **Source pin:** `the_module_reads_no_environment`, which also pins `size_of::<MemberCommit>()`.

## Checks (`evidence/c1b1-checks-r2/`)

`run_c1b1_checks.py`, one lane hold, nice 10, private TMPDIR. Results are in `checks.json`.
- **Suites:** security and host at base and candidate, with equal failure sets after isolated reruns; 24 new passing security tests and 0 host.
- **Formatting:** rustfmt on the new and base-clean files.
- **Append-only:** `git_tracking.rs` and `lib.rs`, each candidate its base followed by an appended block.
- **Lints:** warning-denied all-targets Clippy on both crates.
- **Focused tests:** the VCS tests, and the Git tracking and snapshot source tests.
- **Model:** the model `--check`; the vector moves (walk, opener and session predictions unchanged); the derivation.
- **Census:** the three census `--check`s; the closure change as expected; the cumulative receipt record.
- **Rules:** FW-01, the environment exceptions, the operability source census (mint census included), and verify_design.
- **Mutations: 13**, each caught by its focused tests:
  - PLAN-r6 §5's seven: a symbolic chain followed; `packed-refs` read before the loose ref; unborn taken as a null commit; custody skipped for `HEAD`; the evidence recheck skipped; the outermost repository taken; a read uncharged;
  - r4's: the budget refusal taken as `unborn-head`;
  - r6's: a refused long component taken as a link;
  - R4-RF-1's: the record's member syntax miscounted;
  - LD-C1B-5's: a member's marker checks dropped;
  - r2's (RF-1): an allocation reintroduced into the proof; the borrowed prefix one component short.

## Rules

- No new `from(`, `into(`, `line(`, `pid(` or `issue(` call.
- No environment read; no `let _ =`.
- rustfmt only on new and base-clean files; base-dirty files are appended only.
- No held-out material opened; no blind run.

## Open questions for review

None. r1's Q1 and Q2 are ruled (§ r1 dispositions).

## Not delivered

- Sealing and the `kind: git` and schema-3 records: C1b-2.
- J2's route.
- The batch's refresh.
- The inventory successor for the three new paths, prepared separately after acceptance.
- No caller and no product qualification.

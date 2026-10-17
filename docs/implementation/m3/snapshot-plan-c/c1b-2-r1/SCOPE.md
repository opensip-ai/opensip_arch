# C1b-2 r1: sealing the VCS observation (M3-C r8 items 4 and 6; C1b plan r6, sub-unit C1b-2)

**Unreviewed candidate, round 1.** The plan is C1b plan r6 (`c1b/PLAN-r6.md`; `codex-c1b-plan-r6`, ACCEPT). C1b-2 is the C1b batch's last unit (LD-C1B-7). Nothing is submitted, committed or integrated.

## Base and interval

- **Product base:** main as `source.json` records it, with C1b-1 integrated (`c1b-1-r2-unit.json`). It holds C1a4's refresh (`0772eb7`), C1b-0, C1c-0 and C1b-1, every earlier unit of the open C1b batch.
- **The interval (LD-C1B-7):** C1b-2 joins the open batch before its freeze, as its last input. After C1b-2 integrates, the batch's one reviewed blind validation and refresh follows:
  1. a pre-run review of the frozen inputs, their order and the blind mode;
  2. the mechanical blind run;
  3. a post-run review.

  The integrate script requires the batch still open and unfrozen, and C1b-1 on main.
- **Candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1b2`, detached at the product base, holding exactly the bytes `product-map.json` lists: 4 files, none new.

## What changes

| Path | Change |
| --- | --- |
| `crates/host/src/snapshot_seal.rs` (base-clean) | Step 4 of item 6's order:<br>- `observe_vcs` on the sealing ledger, with the lending's own subject and discovery's record;<br>- `SealInputs.boundaries` (`Option<&AdmittedBoundaries>`, LD-C1B-3) in place of `members: &[String]`;<br>- `seal` takes the invocation's `SnapshotCustody`, as `CaptureSession::walk` does;<br>- `SealError::Vcs(VcsRefusal)`, and `VcsPending` narrowed to the unobserved lending;<br>- the member path-order check;<br>- the three record shapes, counted, charged and hand-encoded (`vcs_record_len`, `charged_vcs_record`);<br>- `SealedSnapshot.vcs_record`. |
| `crates/host/src/snapshot_seal_tests.rs` (base-clean) | The call sites follow the new signature. The member test now expects schema 3, where it expected `VcsPending`. Six new controls are added (§ Tests). |
| `tools/security/snapshot_ledger_census.py` | The VCS record's charge site is anchored at its new text, and the sealing envelope prices the record at the model's `vcs_record_max`, 1,573,798 bytes, instead of the fixed 160. The companion's sources add the VCS anchors' files. |
| `crates/security/src/snapshot_ledger_census.json` | Regenerated: `afterWalk` and each row's margin move by the record's maximum less 160; the pins move. |

C1b-2 adds no model term (LD-C1B-6), so every vector file is unchanged.

## Lead decisions (implementation)

- **LD-C1B2-1. One buffer, charged at the length C1b-1 priced.** Sealing counts the record's canonical length itself (`vcs_record_len`) and refuses `Internal("vcs record length")` unless it equals C1b-1's `VcsObservation::encoded_len()`. `encoded_len()` is the formula C1b-1's term prices at its maximum. Sealing then charges `owned_record(len)`, allocates `Vec::with_capacity(len)` once, writes the record, and checks the written length. This is the plan's "charge-site equality with C1b-1's derivation": the census and the derivation price the same maximum (`charge-site-equality`).
- **LD-C1B2-2. No temporaries.**
  - The record's shape borrows the observation's member slice (`VcsRecord::Members(&[M])`, through a small `VcsMember` trait), so it is iterated twice, for the length and the writing, without a clone.
  - Member paths are borrowed from discovery's record through C1b-1's `MemberCommit`.
  - Each commit's 40 digits are copied onto the stack (`commit_digits`).
  - The digest's hex is written from a stack array, as C1a3's encoders are.
  - The allocation pin is extended to the record's one buffer.
- **LD-C1B2-3. Members in path order.** B-S2 (LD-4) requires schema 3's members ascending by `path`. Discovery's record admission already refuses a member list out of order (`scenario.rs`'s record admission, as discovery's own). Sealing also refuses `Internal("member order")` if the list is not strictly ascending by path bytes. That check is defence in depth: `AdmittedBoundaries::new` does not sort, and no admitted record reaches it out of order. Sealing never sorts, because a sort would be a second order and an allocation.
- **LD-C1B2-4. `VcsPending` is only the unobserved lending.** `encoded_len()` is `None` only for `Unobserved`, and `seal` returns `VcsPending` from that one place (a source pin). The durable route's other refusals are C1b-1's typed `VcsRefusal`, wrapped as `SealError::Vcs`, whose route is J2's (LD-C1B-8).
- **LD-C1B2-5. The census prices the record at the model's maximum.** The plan says C1b-2 changes no model term; its census re-pin "closes the batch's inputs". The sealing envelope now reads the record's maximum from the model C1b-1 extended, not from a literal in the source.

## Tests (`snapshot_seal_tests.rs`, 7 new; 1 replaced)

Mapped to PLAN-r6 §4's C1b-2 controls and B-S2's "Controls owed by C1b" (README:127-132):
- **Replaced:** `a_root_with_an_admitted_member_is_schema_3`, which expected `VcsPending` before C1b.
- **C1-T16 and C1-T17:** `every_git_record_is_canonical_with_dirty_true_and_the_inventory_digest`.
  - It covers an enclosing repository, the innermost of nested repositories (through `packed-refs`), and a two-member workspace (loose and packed).
  - Each record is the canonical encoding, with `dirty: true` for every Git case. It admits as `vcs-observation`, and as the pre-S4 `vcs-observation-v2` for schema 2.
  - Each is named by the descriptor's `vcsDigest`, and `snapshot2` is the descriptor's id.
  - `sourceInventoryDigest` appears once and is the inventory's digest.
- **B-S2 preservation, and changes across kinds:** `schema_2_is_unchanged_by_s4_and_changes_only_with_the_observation`.
  - With the tree fixed, it covers no repository, one repository and nested repositories.
  - Each record admits under the pre-S4 and the S4 definitions with the same bytes (154 and 190).
  - The descriptors differ only in `vcsDigest`, and `snapshot2` differs with it.
- **B-S2's workspaces:** `two_and_sixty_four_member_workspaces_record_schema_3_in_path_order`. Members alternate between loose and packed refs. A record out of path order is refused at discovery's record admission.
- **B-S2's all-excluded workspace:** `a_workspace_whose_candidates_were_all_excluded_records_schema_2_none`.
- **R4-RF-1's encoder and charge:** `the_record_encoder_is_canonical_and_charged_at_its_length`.
  - It uses C1b-1's record-length cases: every escape class, DEL, C1, 2- to 4-byte UTF-8, and the 64-member maximum of 1,573,798 bytes.
  - It checks the hand encoding against `canonical_bytes`, and the length against `167 + Σ(91 + e(P)) + (n − 1)`.
  - A ledger one byte short refuses `Budget` before the buffer exists; the exact allowance succeeds.
- **LD-C1B-10 and `VcsPending`:** `dirty_is_a_constant_and_vcs_pending_is_only_unobserved`. `dirty` appears in code only as the two `true` and two `false` literals, and `VcsPending` has its one site.
- **C1b-1's refusals through sealing (LD-C1B-8):** `a_vcs_refusal_seals_nothing_and_keeps_its_subject`. An unborn `HEAD` refuses `Vcs(Unsupported("unborn-head"))`, never `VcsPending`.
- **The allocation pin** (`sealing_allocates_only_what_it_charges`) is extended to the record's buffer.

## Census (LD-C1B-7)

- **Re-pin and regeneration:** `prepare_c1b2.py` regenerates the snapshot census record by its tool's ordinary `--write` mode over the lead-readable cache, and never opens a held-out store. The model `--check` and the discovery census `--check` must pass unchanged. Both receipts stay byte-unchanged.
- **The stale record, cumulative** (`evidence/receipt_specific_record_c1b2.py`), per receipt, from public fields only:
  - the batch so far is exactly C1b-0's, C1c-0's and C1b-1's;
  - C1b-2's own delta is:
    - none for discovery;
    - for the companion, `tools: [snapshot_ledger_census.py]`, `snapshotSources: [snapshot_seal.rs, snapshot_vcs.rs, snapshot_vcs_tests.rs]` and `afterWalk`;
  - the cumulative delta is their union;
  - every held-out row renders stale.

## Checks (`evidence/c1b2-checks-r1/`)

`run_c1b2_checks.py`, one lane hold, nice 10, private TMPDIR:
- **Suites:** host and security at base and candidate, with equal failure sets; 7 new host tests and 0 security.
- **Preparation** on main.
- **Formatting and lints:** rustfmt on the edited files; warning-denied all-targets Clippy.
- **Focused tests:** the sealing tests.
- **Model:** the model `--check`, with every vector file unchanged.
- **Charge-site equality:** the model's record maximum equals C1b-1's `recordMax`; the census prices it, and sealing cross-checks the priced length.
- **Census:** the three census `--check`s; no closure file changed; the cumulative receipt record.
- **Rules:** FW-01, the environment exceptions, the operability source census (mint census included), and verify_design.
- **Mutations:** 6 in all.
  - PLAN-r6 §5's four:
    - `dirty` computed (taken as `false`) for one Git case;
    - schema 3 written for a zero-member project;
    - members out of path order (written reversed: an admitted record is never out of order);
    - the inventory digest recomputed.
  - the self-review's two:
    - the record's buffer allocated before its charge;
    - the charge taken at the 1,573,798-byte bound.
- **A void attempt:** `evidence/c1b2-checks-r1-void-attempt1/`. It passed every row but one, `vector-moves`, which failed because of a defect in the check itself: it compared a stripped `git show` text with the file's bytes. The vector files were unchanged, and the check now asks git (`git diff --quiet`). The self-review then added a test and two mutations, so the lane was run again.

## Self-review (PRE-SUBMISSION-CHECKLIST.md, 2026-10-17)

1. **Charge before work, with the order proved.**
   - The record's one buffer is charged before it is allocated. The charge, `owned_record(len)`, is the line immediately before `Vec::with_capacity(len)` in `charged_vcs_record`.
   - The allocation pin is a complete source-order guard: each allocation's nearest preceding charge must be its own.
   - The mutation `record-allocated-before-charge` swaps the two lines, and the pin catches it.
   - A ledger one byte short refuses `Budget` before the buffer exists.
   - **Disclosed as uncharged, by the accepted sealing convention:**
     - the record's length count over the member paths;
     - the member-order comparisons;
     - the record's SHA-256.

     They are computation over values already held, as C1a3's inventory count, order check and digests are. The census's sealing envelope prices exactly those accepted sites and the record buffer. PLAN-r6 says C1b-2 adds no model term, so charging them would add one. They are bounded by the 64 members and the 1,573,798-byte record.
   - No predicate is precomputed ahead of a charge.
2. **Exact charges against bounds.**
   - **E,** the executed charge, is the record's exact canonical length, counted from the observation (`vcs_record_len`).
   - **B,** C1b-1's priced formula for that observation (`encoded_len`), must equal E, or sealing refuses `Internal`.
   - **B̂** is the term's maximum, 1,573,798 bytes, which only the census envelope and the derivation use.
   - So E = B ≤ B̂. The bound is never precharged, and the mutation `record-precharged-at-bound` is caught by the exact-allowance encoder test and the pin.
3. **System-call conventions:** not applicable. C1b-2 makes no system call; C1b-1's reads are its own.
4. **Pinned-source equality:**
   - the record's keys and constants are tested against the identity schema, not against a copy. Each record admits as `vcs-observation` (`additionalProperties: false`, every field required), and schema 2 also as the pre-S4 `vcs-observation-v2`. A renamed or substituted key, or a field the schema adds, fails admission;
   - the canonical byte comparisons check the key order.
5. **Immutable context pins:** the package pins only accepted or committed bytes: C1b plan r6, C1b-1 r2's unit record, derivation and receipt record, and B-S2's records.
6. **Time and measurement:** not applicable. No duration is recorded.
7. **Failure latching:** a VCS refusal or a budget failure ends sealing, and nothing is sealed after it. The ledger latches its own failure (`WorkLedger::is_failed`).
8. **Disclosure, the untested paths:**
   - `Internal("member order")`: unreachable through any admitted record, because admission refuses the order;
   - both `Internal("vcs record length")` checks: unreachable while C1b-1's formula and sealing's agree, which the encoder test shows for every record-length case;
   - `VcsPending` for an unobserved lending: the host tests have only the durable route, so a source pin stands in.
9. **Mutations:** six. Each is caught by a failing test, never a compile error (`controls.json`).

## Rules

- No new `from(`, `into(`, `line(`, `pid(` or `issue(` call.
- No environment read; no `let _ =`.
- rustfmt only on base-clean files.
- No held-out material opened; no blind run.

## Not delivered

- The batch's refresh, a separate reviewed unit.
- J2's route for `SealError::Vcs` and `VcsPending`.
- The ephemeral route's observation (J2c).
- No caller and no product qualification.

# Review request: C1B-2-r1 (sealing the VCS observation; M3-C r8 items 4 and 6, C1b plan r6 sub-unit C1b-2), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1b-2-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store, overlay or held-out entry, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, each writing under `/tmp`:
    - `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`;
    - `python3 -I -B tools/check_operability.py source --repository .`;
    - the package's `evidence/receipt_specific_record_c1b2.py <worktree> /Users/sb/code/opensip-ai/opensip <architecture> <out>`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1b-2-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 19,617 bytes, SHA-256 `cf9ab20c35a92f76eeb133d66855454df3771046ad6a8a0b4ec603be2df1eb7f`, 83 members. Rehash every member.
- **The lane base and candidate base:** product main `114d2ac9708cca10563316a0cb11f09b30d1b919`. It holds:
  - C1b-1 (`ae141a3`; your `codex-c1b-1-r2`, ACCEPT-UNIT) with its inventory v228 (`2ead5cf`);
  - and so every earlier unit of the open C1b batch: C1b-0 and C1c-0.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1b2`, detached at that base, holding the exact bytes `product-map.json` lists (4 files, none new).
- **This is your first review of C1b-2,** the C1b batch's last unit.

## Authority

- **The plan:** C1b plan r6 (`docs/implementation/m3/snapshot-plan-c/c1b/PLAN-r6.md`; your `codex-c1b-plan-r6`, ACCEPT), with:
  - sub-unit C1b-2 (§2);
  - LD-C1B-3, LD-C1B-6 (the record's maximum and the charge-site equality), LD-C1B-7, LD-C1B-8 and LD-C1B-10;
  - §4's C1b-2 controls and §5's C1b-2 mutations.
- **B-S2's "Controls owed by C1b"** (`config-discovery-b/b-s2/README.md`:127-132) and VCS-1.
- **C1b-1 as integrated:** `snapshot_vcs.rs`, its `encoded_len` and its derivation (`c1b-1-r2/evidence/c1b1-checks-r2/vcs-derivation.json`).
- **C1a3's sealing encoders and allocation rule** (`snapshot_seal.rs`).

## What to review

`SCOPE.md` states the change table, five lead decisions (LD-C1B2-1 to LD-C1B2-5), the tests, the census accounting and the checks. Judge:
1. **Step 4 of item 6's order:**
   - `observe_vcs` on the sealing ledger, with the lending's subject and discovery's `AdmittedBoundaries` (LD-C1B-3);
   - `VcsPending` only for the unobserved lending (LD-C1B2-4);
   - `SealError::Vcs`.
2. **The records:**
   - schema 2 `none` and `git` and schema 3, hand-encoded to the canonical bytes;
   - `dirty` a constant (LD-C1B-10);
   - the inventory digest once (C1-T17);
   - members in path order (LD-C1B2-3).
3. **The charge (LD-C1B2-1, LD-C1B2-2):**
   - the length counted, cross-checked against C1b-1's `encoded_len`, and charged first;
   - one buffer and no temporaries;
   - the allocation pin extended;
   - the charge-site equality with C1b-1's derivation (`charge-site-equality`).
4. **B-S2's controls owed by C1b:**
   - preservation and the changes across kinds;
   - the 2- and 64-member workspaces;
   - the all-excluded workspace;
   - the encoder at C1b-1's record-length cases, with one byte short refusing `Budget`.
5. **The census (LD-C1B-7, LD-C1B2-5):**
   - the anchor and the envelope at the model's maximum;
   - the regenerated record, every row still passing 2×;
   - every `--check` passing;
   - **the cumulative receipt record:** the batch so far (C1b-0, C1c-0, C1b-1), C1b-2's own delta, their union, and the stale rendering.

   After C1b-2, the batch's inputs are complete and its refresh follows.
6. **The lane** (`evidence/c1b2-checks-r1/`):
   - suites with equal failure sets and 6 new host tests;
   - the preparation;
   - Clippy and rustfmt;
   - the focused tests and the unchanged vectors;
   - the census checks, no closure change and the receipt record;
   - FW-01, the environment exceptions, operability and verify_design;
   - the 4 mutations.
7. **Rules:** no new mint-census call, no environment read, no `let _ =`.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1B2-R1-RF-n` / `C1B2-R1-NBO-n`.

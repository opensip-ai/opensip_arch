# Review request: C1C-0-r2 (the read set's preparatory primitives; M3-C r8 items 1 and 3, C1c sub-unit C1c-0), round 2: the rebased round in the C1b batch

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1c-0-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store, overlay or held-out entry, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, `python3 -I -B tools/check_operability.py source --repository .`, and the package's `evidence/retention_cap_evidence.py <worktree> <architecture> <out>` and `evidence/receipt_specific_record.py <worktree> /Users/sb/code/opensip-ai/opensip <architecture> <out>`, each writing under `/tmp`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1c-0-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 15,582 bytes, SHA-256 `3c9447301b151ed4d18faa7bf34f522ebefd297bfdd756f1c84e54880d5db43a`, 67 members. Rehash every member.
- **The lane base and candidate base:** product main `caa71e2fd481977d066d67465add64f4393334f9` (D3a-2). It holds C1a4's blind refresh (`0772eb7`), then C1b-0 (`c9c18f7`), which opened the C1b batch interval, then its contract-176 lock (`9ea2d4a`).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1c0`, detached at `caa71e2`, holding the exact bytes that `product-map.json` lists (17 files, 1 new).
- **This is your first review of C1c-0.**
  - Round 1 was packaged on `72e0787`, ahead of C1b-0, and was never submitted.
  - This round is the mechanical rebase onto C1b-0's main. Every hand-written file is byte-identical to round 1's, every generated output is regenerated on top of C1b-0's, and the receipt record is cumulative (SCOPE, "Base and sequencing", LD-C1C0-5).
- **The interval (LD-C1C-9; SCOPE, "Which interval"):** C1c-0 joins the open C1b batch before its freeze. The integrate script requires the batch open and unfrozen, and records the join.

## Authority

- the C1c plan r4 (`docs/implementation/m3/snapshot-plan-c/c1c/PLAN-r4.md`; your `codex-c1c-plan-r4`, ACCEPT): sub-unit C1c-0, LD-C1C-2, -5, -9 and -13, with the folded Q1 to Q5 rulings, §4's C1c-0 controls and §5's C1c-0 mutations;
- law M3-C r8 items 1 and 3, and the M3-C r9 law record's caps (`c1a-r9/RECORD-r9.md`);
- C1a1 to C1a4 as integrated, the blind run's acceptance (`c1a4-blind-run-r1-unit.json`), the C1b plan r3's receipt rules (LD-C1B-7), and C1b-0 r2 as integrated (`c1b-0-r2-unit.json`, its `census-regeneration.json`), which opened the batch.

## What to review

`SCOPE.md` states the change table, five lead decisions (LD-C1C0-1 to 5), the tests and the checks. Judge:
1. **The pruned-tree opener** (`open_pruned`, `capture_pruned`): S3 custody above the dependency anchor only; descriptor discipline below; no config-file custody; the rule's placement (outside, VCS, custody anchor) before any open; symlinked components refused; the charge model and its exact `prunedOpeners` cases; LD-C1C0-2.
2. **`read_set_path`**, beside an unchanged `classify_path`: the full-path check, first-party and dependency-tree Cargo roots, the exact custody anchors, VCS segments, nested packages, and the lookalikes. It must reuse the rule's tables and duplicate none, and the module must stay pure and crate-private. Also judge `authorize_read`'s public `ReadAuthorization` mapping and `read_set_path_cost`.
3. **`WalkEvidence`** (LD-C1C-13 r4):
   - the Cargo roots moved, not copied, with no charge, and the classification unchanged;
   - the member roots copied and charged;
   - the opaque type and `walk_snapshot`'s unchanged signature (LD-C1C0-1);
   - the model's retention term, anchors and `known.remove` refusal;
   - the vector moves: only the member case, by its one copy;
   - the retention's r9 fixed-cap and 2× evidence.
4. **The dependency-tree Cargo marker observation:** no read, regular files only.
5. **The census accounting:**
   - the `discovery_rule.rs` CLOSURE re-pin and the records regenerated on top of C1b-0's, with every `--check` passing, and each record differing from main's only as SCOPE lists;
   - the snapshot census's all-mounts-as-members rows moving by the member copies, with every row still passing 2×;
   - **the cumulative receipt record** (`evidence/receipt_specific_record.py`), per receipt:
     - the batch's baseline equal to the refresh's bytes and C1b-0's recorded pins;
     - the batch so far exactly C1b-0's delta;
     - C1c-0's own delta exactly what it edits;
     - the cumulative delta their union;
     - the stale rendering, with both receipts' bytes unchanged;
   - the join before the freeze, LD-C1C0-5, and the integrate script's open-and-unfrozen precondition.
6. **The lane** `evidence/c1c0-checks-r2/`: host and security with equal failure sets and the new passing tests; Clippy and rustfmt; the focused tests; the model and census checks; the retention evidence; FW-01, the environment exceptions, operability, the closure change as expected, and verify_design; 14 mutations.
7. **Rules:** no new mint-census call, no environment read, no `let _ =`, and security `lib.rs` appended only.
8. **Inventory:** one new path.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1C0-R2-RF-n` / `C1C0-R2-NBO-n`.

# Review request: C1A4-r1 (the snapshot ledger's caps, their T2 margins and the constructor; M3-C r8 item 2 as M3-C r9 amends it), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a4-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane. Do not take the shared lane lock.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store, the T2 cache or any held-out material. The census records are the lead's runs over the lead-readable entries only: judge their method and their recorded output, and do not re-run them.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip` and `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a4-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 23182 bytes, SHA-256 `65124de040d5b858e7f6f289ed2afc5bbd6ac1c60ca6f2b01e9b77b6db70b90a`, 99 members. Rehash every member.
- **The candidate base:** product main `4ece8495b3a599dbd1f14009458c94b60d1836c8` (D2b-1 and D2b-0 integrated, contract successor 174 and inventory v219 bound).
- **The lane base:** `23b3871269c6553c96097084dd412b3aa95dec68`. Main differs from it by D2b-0's code `50f64cb` (schemas, identity `schema.rs` and `schema_registry.rs`, host and storage `schema_sources.rs`, host `tests/admission_tests.rs`), the contract-174 lock `2b24f31` and the v219 lock `4ece849` (`source.json`: `laneBase`, `baseDifference`, `baseDifferencePaths`). The lane was not repeated. The model check, operability and verify_design were rerun on `4ece849` (`evidence/rebase-4ece849/`). Judge whether any of the difference touches this unit.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a4`, detached at `4ece849`, holding the exact bytes that `product-map.json` lists (14 files, 2 new).

## Authority

- **M3-C r8** (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`), item 2 ("Ledger") and C1-T27, as amended by **the accepted M3-C r9 law record** (`docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md`; your `codex-m3c-r9-r2`, ACCEPT, and its NBO-1). r9's caps are conditional on this unit landing remedies (a) and (b-prime) exactly as its section 6 states them.
- **The C1a plan r6** (`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r6.md`; your `codex-c1a-plan-r6`): its C1a4 section, RF-1 (the gate) and RF-3 (the non-circular blind protocol, steps 1 to 4).
- **M3-B's shared rule and census:** `crates/security/src/custody/discovery_rule.rs` and `tools/security/discovery_census.py`, with the owner's held-out protocol (`docs/implementation/m3/owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`).
- **The accepted C1a1 to C1a3 units** and their native-verified vectors.

## What to review

Judge the following.

1. **Remedy (a)** in `crates/security/src/snapshot_walk.rs` against RECORD-r9 section 6.
   - Is the anchor scan's classification reused exactly, and is the reuse argument sound?
   - Is the recorded index safe? Consider the anchor's removal, the at-most-one `.opensip` per listing, and the `Level` field.
   - Is nothing retained or allocated uncharged (LD-C1A4-1)?
2. **Remedy (b-prime)** in `crates/security/src/custody/discovery_rule.rs`.
   - Is `custody_state`'s in-place comparison equivalent to the collected one for every caller, including multi-segment and shared-prefix member roots?
   - Is no allocation left per member?
   - Is `classify_cost`'s member term rightly removed?
   - Is r9 section 7's discovery undercharge thereby corrected with no change to discovery's charges?
   - The lead accepts it as M3-B's law owner, and states that it resolves r9 section 7's M3-B finding (LD-C1A4-2). Is that right, and does the change need anything further as an M3-B file?
3. **The profile and C1-T27** in `crates/platform/src/work_ledger.rs`:
   - the constants and `snapshot_profile()` beside `discovery_profile`;
   - the exact-cap and one-over test;
   - the payload controls on the snapshot profile (LD-C1A4-5), including the 4 GiB lane probe.
4. **The model and vectors** in `tools/security/snapshot_ledger_model.py`:
   - its re-anchored and new anchors, and its classification and reuse terms;
   - the caps read from the profile by anchor;
   - the regenerated `crates/security/src/snapshot_ledger_vectors.json`, where only `opensip-anchors-root-and-member` moves, by r9's −12 objects and −1,726 bytes; and the session vectors, byte-equal.
5. **The companion census and its margin test**:
   - `tools/security/snapshot_ledger_census.py` (lead-readable only, through `discovery_census.py`'s own path; r9's pricing and eligibility; item-5 bounds and sealing by anchor);
   - its record `crates/security/src/snapshot_ledger_census.json`;
   - the Rust test in `crates/security/src/snapshot_walk_tests.rs` that classifies the record again against the compiled profile;
   - LD-C1A4-3, the lead's reading of PLAN-r6:11's "the companion census's tool bytes": pinned in the record's own `pins`, for the blind unit's companion receipt to bind, rather than added to `discovery_census.py`'s `CLOSURE`. Is that reading right?
6. **The census closure and the blind receipt** (LD-C1A4-4; PLAN-r6:11).
   - Are the two `CLOSURE` re-pins and the regenerated `discovery_census.json`, `discovery_census_vectors.json` and `discovery_workspace_ledger.json` right? Their diffs should be only the closure rows, the stale held-out rows and the census tool's pin.
   - Is it right that the held-out receipt goes stale here, untouched, with the reviewed blind validation run as a separate unit?
7. **The exhaustive displacement list** (`SCOPE.md`, *What it displaces*; your M3CR9-R2-NBO-1): is it complete?
8. **The lane** `evidence/c1a4-checks-r1/`: attempt 2, the lane of record (attempt 1, `evidence/c1a4-checks-r1-attempt1/`, is history: its parallel platform run hit the recorded base race). Check the suites (host 8 = 8, security 14 = 14 with 3 new passing tests, platform 0 = 0 with 1 new, run serially on both sides as D1a and B2-b1 do), Clippy and rustfmt, the focused tests and the 4 GiB probe, the model check and the vector moves, the three census checks, the closure changed exactly as expected, the stale receipt, FW-01, the environment exceptions, operability, verify_design and the eight mutations.
9. **The rules:** no new mint-census call, no environment read, no `let _ =`, rustfmt only on base-clean files, no T2 held-out, store or overlay read outside `discovery_census.py`'s lead-readable path.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A4-R1-RF-n` / `C1A4-R1-NBO-n`.

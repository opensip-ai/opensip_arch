# Review request (round 4): B3-B2B2B-r4 (the native workspace observation and the D15 discovery composition; M3-B unit B3-b, sub-unit B3-b2b2b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b2b-r4/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds, the lane or the census tool.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry, store or overlay.
- Do not use other panes and do not delegate.
- **Permitted:** as in round 3:
  - read-only reading, hashing, JSON parsing and Git queries;
  - `tools/check_operability.py source`;
  - the two vector tools' `--check` in the candidate worktree.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2b2b-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 21093 bytes, SHA-256 `e20a637d387a33b7c3b35eed9ed002a43f6629ebc310c7b1e4ae19d483f0a02b`, 86 members. Rehash every member.
- **Bases:** unchanged:
  - product main `92624ae00f242d9a56e4305146e1d69665e2ecc5`, clean;
  - architecture `271d7eee4759799e9a731c34ff1d2517f2862727`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2b2b`, detached at the product base. It holds the exact bytes `product-map.json` lists (21 files).
- **Round 3's package** (`b3-b2b2b-r3/`) is unchanged at its reviewed bytes.

## Authority

As in round 3:
- the B3-b plan r2 with amendments A1 to A4;
- law M3-B r9 items 19 to 24;
- B3-b0 r4 (contract successor 169);
- B3-b2a, B3-b2b1 and B3-b2b2a, as bound on main.

## Round 4

Your `codex-b3b2b2b-r3` raised:
- **RF-1:** a cached copy was cloned before its charge;
- **RF-2:** the identity collector's storage was uncharged, including on the legacy path;
- **NBO-1:** attempt 2's history.

`SCOPE.md`'s "r4 changes" table resolves them:
- **RF-1:** `copy_kept` charges `owned(len)` before cloning. Its control shows a refused charge copies nothing (a test-only trace) and an ample one is charged exactly. Two mutations.
- **RF-2:**
  - identity collection is opt-in (`Option<&mut MemberIdentities>`), so `observe` and `observe_members` build nothing and their charges are unchanged by construction;
  - `push_identity` charges `identity_cost`, the path bytes plus list slot, before building, with the length computed from the segments and debug-asserted;
  - a deep shared-prefix accounting control: the used cost equals `observe`'s plus each record's cost;
  - a refused-charge control: the build closure never runs;
  - two mutations.

Everything else is round 3's. The diff from round 3 is in `git_tracking.rs`, `git_tracking_member_tests.rs`, `workspace_observation.rs`, `workspace_discovery_tests.rs`, SCOPE and the lane scripts.

**Judge first** whether RF-1 and RF-2 are resolved, and whether `identity_cost` is a sound bound for one record, given `owned`'s 128-byte record allowance. Then confirm round 3's other judgments still hold.

**Evidence** (`evidence/b3b2b2b-checks-r4/`):
- 14 = 14 base failures and fourteen new tests;
- Clippy with and without `scenario-fixtures`;
- every vector check, the census and its equality projection, operability and verify_design;
- thirty-four mutations, all caught.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2B2B-R4-RF-n` / `B3B2B2B-R4-NBO-n`.

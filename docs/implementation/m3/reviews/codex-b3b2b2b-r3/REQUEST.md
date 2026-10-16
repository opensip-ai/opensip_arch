# Review request (round 3): B3-B2B2B-r3 (the native workspace observation and the D15 discovery composition; M3-B unit B3-b, sub-unit B3-b2b2b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b2b-r3/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds, the lane or the census tool.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry, store or overlay.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository <tree>`;
  - in the candidate worktree, `python3 -I -B tools/security/workspace_discovery_vectors.py --check ...` and `python3 -I -B tools/security/workspace_member_vectors.py --check ...`, each with `--architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`; they read no filesystem tree.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2b2b-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 48640 bytes, SHA-256 `9cf1081d5d4b13ddf583e84f2aa110730c94183cf772fe672f9aa7ee46c03c38`, 194 members. Rehash every member.
- **Bases:**
  - product main `92624ae00f242d9a56e4305146e1d69665e2ecc5`, clean (B3-b0 r4 bound as contract successor 169, inventory v205);
  - architecture `271d7eee4759799e9a731c34ff1d2517f2862727`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2b2b`, detached at the product base. It holds the exact bytes `product-map.json` lists (21 files).

## Authority

- The B3-b plan r2 with amendments A1 to A4:
  - A3-1's B3-b2b2b;
  - **A4-2's branch-A order and public priority, and A4-4's product controls** (your `codex-b3b-plan-a4-r2`, ACCEPT).
- Law M3-B r9 items 19 to 24.
- **B3-b0 r4** (`b3-b-reference-r4/`, contract successor 169, your `codex-b3b0-reference-r4-r2`) at its bound bytes. It replaces B3-b0 r3 as the vectors' source.
- As bound on main: B3-b2a, B3-b2b1 and B3-b2b2a.

## Round 3

Your `codex-b3b2b2b-r2` raised:
- **RF-1:** the trial crossed index-only boundaries;
- **RF-2:** item 6b's reopened ancestors and Git evidence were unbound;
- **RF-3:** a manifest could be read only once per phase;
- **NBO-1 and NBO-2.**

`SCOPE.md`'s "r3 changes" table resolves them:
- **RF-1, by A4 and B3-b0 r4:**
  - the core's `branch_a` runs the array gate (`Decision::ArrayRefused`), then the member decisions (`PhaseOne::Admitted`);
  - the composition walks once with members and gitlinks, and `links` follows an accepted walk;
  - the trial, `phase_two`, the re-walk and LD-10 are removed;
  - the vectors are regenerated from r4;
  - new controls, with walker-trace assertions.
- **RF-2:** every object item 6b opened is bound before admission. Three race controls, each in both branches, assert the change is found inside item 6b's verdict. Four independent mutations.
- **RF-3:** a validated-read map, with three vector cases.

The lane needed three attempts; SCOPE says why, and the first two are archived.

**Judge first** whether each finding is resolved. Then judge:
1. **The core restructure** against B3-b0 r4's `discover` and A4-2:
   - the gate's records and their provenance;
   - the short circuit;
   - `Admitted` and `links`;
   - LD-B3B2B2B-12, the links after the walk.
2. **The vector tooling:**
   - `walk` and `sixB` in the member vectors;
   - the `forbidden` / `forbiddenReads` split (LD-15);
   - the non-string arrays listed by id (LD-14);
   - the tripwire scoped to the custody-and-6b phase (LD-13).
3. **The composition controls:**
   - `check_gitlinks_not_entered` over the walker's own trace;
   - `check_gate`;
   - the paired unlistable-subtree test;
   - `changed_before_admission`;
   - LD-16's member-configuration vector.

   Is anything in A4-4's list, or RF-1 to RF-3's validation, missing?
4. **What is kept from rounds 1 and 2:**
   - the binding table;
   - the custody-bound reads;
   - the census re-pins: `equality-projection.json` must show only `closure/0`, `/4` and `/6`;
   - the scenario path.
5. **Evidence** (`evidence/b3b2b2b-checks-r3/`):
   - 14 = 14 base failures and eleven new tests;
   - Clippy with and without `scenario-fixtures`;
   - every vector check, the census, operability and verify_design;
   - thirty mutations, all caught.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2B2B-R3-RF-n` / `B3B2B2B-R3-NBO-n`.

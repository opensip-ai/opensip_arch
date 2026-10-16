# Review request (round 5): B3-B2B2B-r5 (the native workspace observation and the D15 discovery composition; M3-B unit B3-b, sub-unit B3-b2b2b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b2b-r5/`).

## Boundaries

As in round 4:
- no edits to either repository, the worktree or the control files;
- no Cargo, rustc, tests, builds, lane or census tool;
- no network;
- no protected fixture, installation directory, signing key, held tree or T2 held-out data;
- no other panes and no delegation.

**Permitted:**
- read-only reading, hashing, JSON parsing and Git queries;
- `tools/check_operability.py source`;
- the two vector tools' `--check` in the candidate worktree.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2b2b-r5-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 39004 bytes, SHA-256 `70e1024afbd4ca80ce72f3e7e2ab865567daed417149a391044187aca07cdccf`, 156 members. Rehash every member.
- **Bases:** unchanged:
  - product main `92624ae00f242d9a56e4305146e1d69665e2ecc5`, clean;
  - architecture `271d7eee4759799e9a731c34ff1d2517f2862727`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2b2b`, at the bytes `product-map.json` lists.
- **Rounds 3 and 4's packages** are unchanged.

## Round 5

Your `codex-b3b2b2b-r4` raised RF-1: the identity charge did not bound the buffers its builders allocate. `SCOPE.md`'s "r5 changes" table resolves it:
- **The list:** `reserve_identities` charges it as one owned record of its final capacity (segments plus `GIT_IDENTITIES` = 3), then allocates it. It never grows, which is debug-asserted.
- **Each path:** `push_identity` charges the sum of its parts, then builds one buffer at exactly that capacity. `label_in_git` and the prefix `join` are gone, and layout labels are matched exactly.
- **Every identity allocation goes through `allocated`,** whose test-only counter sits at the allocation.
- **Controls:**
  - the flow control (deep, shared and 405-byte spellings) asserts each list's capacity and fill, each path's capacity equal to its length, and the ledger's use equal to `observe`'s plus the storage actually requested (from real capacities);
  - the order control asserts a refused charge allocates nothing.
- **Seven mutations,** including undercharged list and path costs, growth, and both orders.
- **Lane:** attempt 1 (archived) showed the counter had to sit at the allocation.

The diff from round 4 is in `git_tracking.rs`, `git_tracking_member_tests.rs`, SCOPE and the lane scripts.

**Judge first** whether RF-1 is resolved:
- Is `owned(capacity × slot size)` a sound bound for the list allocation?
- Is `owned(len)` sound for an exact-capacity path?
- Is any remaining identity allocation uncharged?

Then confirm round 4's other judgments still hold.

**Evidence** (`evidence/b3b2b2b-checks-r5/`):
- 14 = 14 base failures and fourteen new tests;
- Clippy;
- every vector check, the census and its projection, operability and verify_design;
- thirty-nine mutations, all caught.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2B2B-R5-RF-n` / `B3B2B2B-R5-NBO-n`.

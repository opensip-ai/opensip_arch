# Review request: CI-A3 r2 (the launch member, a pinned entrypoint recheck; amendment to the component installation law r5), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-ci-a3-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries, including read-only reading of the CI-2/CI-3 worktree `/Users/sb/code/opensip-ai/opensip-ci2`.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/ci-a3-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1,075 bytes, SHA-256 `e2a4223229e03bbb553aa3b919f12a98668b744c950a70af7e9a4780788c1997`. It has 4 members:
  - `CI-A3-r2.md`, the subject;
  - `CI-A3-r1.md`, history, unchanged since round 1;
  - `PROPOSAL-r5.md` and `ci-2-r1/SCOPE.md`, context, the same bytes as round 1.
- Rehash them.
- **Bases:** product main `d704ed4`; architecture `b1f80423cce08310972106fad62536773b0cd75d` (the D4 plan r2 published).
- **Round 1:** `/tmp/opensip-implementation/reviews/codex-ci-a3-r1/REVIEW.md` and `review.json` (REQUIRED-FINDINGS: CIA3-R1-RF-1; NBO-1; Q1 to Q6 ruled).

## Round 1 disposition (to verify)

| Round 1 item | r2's answer | Where in CI-A3-r2 |
| --- | --- | --- |
| CIA3-R1-RF-1 (content versus path length; native spellings) | Distinct symbols: `c` (content) for `env(c)`; `p`, `b`, `k` (final path, basename, components); `h` hops and `h + 1` lookups; `q_i` (joined paths); `L` (store path); `P` (launch path). Priced: each hop temporary; each descent's name, inside `desc`; the basename's `b + 1`; one shared NUL-terminated launch-path buffer `P + 1`, reused as the result's path. The store-path record is charged once at `ComponentStore::open_in`. `Directory("")` has zero lookups, hops and descents. A separate dominating pre-bound `B̂_launch`. CI-T28 extended with the requested shapes, independent enumeration and per-site exhaustion. | "r2 changes"; CI-A3-b; CI-A3-d; CI-T28 |
| CIA3-R1-NBO-1 (the absolute-path identity observation) | Two new platform primitives, owned by the platform owner and added by CI-3L: `path_status_no_follow` (`lstat`, identity, `{Absent, NotDirectory, Io}`, `st` charged first) and `directory_identity` (`fstat` of a retained directory). The r1 claim "adds no platform primitive" is withdrawn. | CI-A3-a; Interaction |
| Q1 to Q6 conditions | The entrypoint is taken from the capability's own association; the bounded hop rule; the seam's binding outcomes partitioned; the D1a suggestion withdrawn; the directory-attestation wording; CI-3L covers a to f; operation ownership through settlement stated as the mechanism | CI-A3-a, -c, -f; Not claimed |

## What to review

1. Is RF-1 resolved: is every quantity distinct, every owned representation and terminator priced before use, the store record charged once at a stated site, and the pre-bound conservative?
2. Is NBO-1 addressed accurately against the CI-2 candidate's actual helpers?
3. Is each Q condition of round 1 applied, with no regression to round 1's accepted parts?
4. Answer CI-A3-r2's Q1 to Q3 with explicit rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", ...}}`, with ids `CIA3-R2-RF-n` / `CIA3-R2-NBO-n`.

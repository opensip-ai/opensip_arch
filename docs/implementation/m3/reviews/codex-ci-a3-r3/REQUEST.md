# Review request: CI-A3 r3 (the launch member; amendment to the component installation law r5), round 3

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-ci-a3-r3/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries, including read-only reading of `/Users/sb/code/opensip-ai/opensip-ci2`.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/ci-a3-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1,693 bytes, SHA-256 `22726fc07d84f0ac237f59512aec2a0722b0dcec98062b32a68640b1e1debda8`. It has 6 members:
  - `docs/implementation/m3/component-install/CI-A3-r3.md`, 34,241 bytes, `5aa50d9dd0e2a2f51bf239c37c9247f9c6d31b41422e81f91cffe0387b0b31ac` (the subject)
  - `docs/implementation/m3/component-install/CI-A3-r2.md`, 24,960 bytes, `fd2b7ef49ff43387f0e4130d5c8d6f7c99a97f80bf7a396abc89faab0b524095` (history)
  - `docs/implementation/m3/component-install/CI-A3-r1.md`, 16,045 bytes, `afe383537a88f690cf75f48f5b1b9df2219994ee08a807c82a9f457aa02551d1` (history)
  - `docs/implementation/m3/component-install/PROPOSAL-r5.md`, 63,707 bytes, `efdbf7e70ab48522fec855bbb74f144a5c695c27eefc194b2de000e8e3a54333` (context: the law amended)
  - `docs/implementation/m3/component-install/ci-a3-r3/context/ci-2-r2-SCOPE.md`, 37,281 bytes, `d79e838a4c63383a22e3090290d6feb309b776187afd3ab0f3fa0e49f7e2c4b8` (context: CI-A2 as pinned by docs/implementation/m3/component-install/ci-2-r2-subject.json (byte copy of docs/implementation/m3/component-install/ci-2-r2/SCOPE.md))
  - `docs/implementation/m3/component-install/ci-2-r2-subject.json`, 20,548 bytes, `988d53cc816e76523ac3a72299ef04f3b5c137e89e0ed64c06eb14dc099f452e` (context: the codex-ci-2-r2 review subject manifest)
- Rehash every member.
- **Bases:** product main `114d2ac9708cca10563316a0cb11f09b30d1b919`; architecture `339d9dc56939b805c662398a8a946941fe3839cf`.
- **Rounds 1 and 2:** `/tmp/opensip-implementation/reviews/codex-ci-a3-r1/` and `/tmp/opensip-implementation/reviews/codex-ci-a3-r2/` (REQUIRED-FINDINGS: CIA3-R2-RF-1 and RF-2; round 2's Q1 to Q3 ruled).

## Round 2 disposition (to verify)

| Round 2 item | r3's answer | Where |
| --- | --- | --- |
| CIA3-R2-RF-1 (the CI-A2 context pin) | Lead decision LD-CIA3-R3: CI-A2 is pinned from the immutable `codex-ci-2-r2` review subject, `docs/implementation/m3/component-install/ci-2-r2-subject.json` (SHA-256 `988d53cc816e76523ac3a72299ef04f3b5c137e89e0ed64c06eb14dc099f452e`). Its SCOPE.md pin is byte-copied into CI-A3's own context path `docs/implementation/m3/component-install/ci-a3-r3/context/ci-2-r2-SCOPE.md`, so the CI fork's working file is neither pinned live nor edited. Round 2's live-file pin is history. CI-A2-b and CI-A2-c are rechecked against those bytes. | Bases; Interaction |
| CIA3-R2-RF-2 (exact charges versus bounds) | `E_launch` (exact, in observed counts `s_j` and `a`; an empty file is one EOF attempt), `B_launch` (per member: `⌈log₂ n⌉ + 1` per lookup, `env(c)` reads) and `B̂_launch` (request), with `E ≤ B ≤ B̂`; every charge at its actual operation; CI-T28 requires equality to `E_launch` and the inequalities separately, with an empty file, a one-chunk file and lookups matching at different depths | CI-A3-b; CI-T28 |
| Round 2 Q1's conditions | maxima over empty sets are `0`; the `Directory("")` special case; bounded segment lengths; checked arithmetic before allocation | CI-A3-b |
| CI-A2's revision in CI-2 r2 | CI-A2-h: the basename row now charges nothing (the primitive's stack buffer, no allocation), so nothing is precharged; the heap launch-path buffer stays priced at `P + 1`. CI-A2-e's single reservation does not change `launch_member`. The capability's failure latch extends to `launch_member`, with a CI-T27 control. Self-review (checklist items 2 and 5). | r3 changes table; CI-A3-b; Interaction; Self-review |

## What to review

1. Is each round 2 finding resolved, with no regression to rounds 1 and 2's accepted parts?
2. Do the subject's members all match, and is the CI-A2 context exact and immutable?
3. Are `E_launch`, `B_launch` and `B̂_launch` well defined, with the inequalities true and no precharge or extra read?
4. Answer CI-A3-r3's Q1 to Q3 with explicit rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", "Q2": "...", "Q3": "..."}}`, with ids `CIA3-R3-RF-n` / `CIA3-R3-NBO-n`.

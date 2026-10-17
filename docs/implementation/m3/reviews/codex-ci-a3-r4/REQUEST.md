# Review request: CI-A3 r4 (the launch member; amendment to the component installation law r5), round 4

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-ci-a3-r4/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries, including read-only reading of `/Users/sb/code/opensip-ai/opensip-ci2`.

## Subject

- **Manifest:** `docs/implementation/m3/component-install/ci-a3-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 1,906 bytes, SHA-256 `2d1bfd96c483564538bc10d3d8a877858409f2d8c2f51edf3fd40d79d1b41454`. It has 7 members:
  - `docs/implementation/m3/component-install/CI-A3-r4.md`, 39,140 bytes, `8a27100bf6093223fa97f7893d19f052b650bd21b15289bad8c9b8b401254cc4` (the subject)
  - `docs/implementation/m3/component-install/CI-A3-r3.md`, 34,241 bytes, `5aa50d9dd0e2a2f51bf239c37c9247f9c6d31b41422e81f91cffe0387b0b31ac` (history)
  - `docs/implementation/m3/component-install/CI-A3-r2.md`, 24,960 bytes, `fd2b7ef49ff43387f0e4130d5c8d6f7c99a97f80bf7a396abc89faab0b524095` (history)
  - `docs/implementation/m3/component-install/CI-A3-r1.md`, 16,045 bytes, `afe383537a88f690cf75f48f5b1b9df2219994ee08a807c82a9f457aa02551d1` (history)
  - `docs/implementation/m3/component-install/PROPOSAL-r5.md`, 63,707 bytes, `efdbf7e70ab48522fec855bbb74f144a5c695c27eefc194b2de000e8e3a54333` (context: the law amended)
  - `docs/implementation/m3/component-install/ci-a3-r3/context/ci-2-r2-SCOPE.md`, 37,281 bytes, `d79e838a4c63383a22e3090290d6feb309b776187afd3ab0f3fa0e49f7e2c4b8` (context: CI-A2 as pinned by docs/implementation/m3/component-install/ci-2-r2-subject.json (byte copy of docs/implementation/m3/component-install/ci-2-r2/SCOPE.md))
  - `docs/implementation/m3/component-install/ci-2-r2-subject.json`, 20,548 bytes, `988d53cc816e76523ac3a72299ef04f3b5c137e89e0ed64c06eb14dc099f452e` (context: the codex-ci-2-r2 review subject manifest)
- Rehash every member. The CI-A2 context is round 3's, unchanged: the byte copy of the SCOPE.md that `codex-ci-2-r2`'s subject pins. That unit and CI-A2 are now accepted.
- **Bases:** product main `114d2ac9708cca10563316a0cb11f09b30d1b919`; architecture `339d9dc56939b805c662398a8a946941fe3839cf`.
- **Prior rounds:** `/tmp/opensip-implementation/reviews/codex-ci-a3-r1/` to `-r3/` (round 3: REQUIRED-FINDINGS, CIA3-R3-RF-1 and RF-2; Q2 accepted; Q3 accepted for spelling and reservation).

## Round 3 disposition (to verify; narrow)

| Round 3 item | r4's answer | Where |
| --- | --- | --- |
| CIA3-R3-RF-1 (the early refusal for the no-matching-kind pre-bound) | A charged kind check, one edge comparing the capability's held `F` (or `D` for `Directory`) against zero, comes before any lookup, symlink hop or joined-path allocation. A zero count refuses `Association` there. `Directory("")` makes no kind check. The refusal-prefix accounting is explicit: the executed rows before the stop, no final-row row when no member resolved, each within `B̂_launch`'s counts. CI-T28 gains the `f` + `l` → `f`, no-`dir` tree with `Directory("l")`, at one edge. | "r4 changes"; CI-A3-a ("The kind check"); CI-A3-b (the kind-check row, "The refusal prefix", the pre-bound bullets); CI-T28 |
| CIA3-R3-RF-2 (latch `Budget` on the capability) | Every failure of `launch_member` or `transfer`, `Budget` included, latches the capability. Later calls on any scope refuse before any charge, and a latched `Budget` gives `Budget(Closed)`, as CI-2 r2's `Latched::Budget` does. The rule is now normative in CI-A3-a, and round 3's `Budget` exception is withdrawn. CI-T27 gains the exhausted-launch case: a launch and a transfer on a fresh funded scope, with no charge and no observation. | CI-A3-a ("Latching"); CI-T27; Interaction |

## What to review

1. Is each round 3 finding resolved, with no regression to rounds 1 to 3's accepted parts?
2. Do the subject members all match?
3. Answer CI-A3-r4's Q1 and Q2 with explicit rulings.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "rulings": {"Q1": "...", "Q2": "..."}}`, with ids `CIA3-R4-RF-n` / `CIA3-R4-NBO-n`.

# Review request: D2A-r2 (the common control codec, `crates/components/src/control_protocol.rs`; M3-D r5 item 9), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2a-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; running `docs/coop/completion/control-completion.check.v5.py` with `python3 -I -B` against the architecture's own corpus; and, in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2a-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 9929 bytes, SHA-256 `1b633d2db9cfac5294715407f73215085dbb8b30a44e5851f647b5830409cb2a`, 44 members. Rehash every member.
- **The candidate base and lane base:** product main `56d0eb53a888572dd0129fbc595d0c1be16eaf3a`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2a`, detached at `56d0eb5`, holding the exact bytes `product-map.json` lists (7 files). Round 1's `crates/components/tests/control_protocol_tests.rs` no longer exists: the tests moved in-crate.
- **Main may move while you review,** by C1a2's integration and its lock-only inventory commit, if C1a2 is accepted first. Nothing there touches `opensip-components`.
- **Your round 1:** `codex-d2a-r1` (REQUIRED-FINDINGS: D2A-R1-RF-1 to RF-3, NBO-1, NBO-2), archived at `docs/implementation/m3/reviews/codex-d2a-r1/`. The r1 package is history.

## Authority

As in round 1: the D2a plan r1 (your `codex-d2a-plan-r1`, with NBO-1 and NBO-2 in the lead assent); law M3-D r5 item 9; CC v5; the product schema and the generated `Control3Root`.

## What to review

`SCOPE.md` opens with the r2 changes table. Judge:
1. **RF-1.** `encode` refusing the eight component-only types before writing, with one guard (the body writer's arm is unreachable), and the control over all sixteen corpus-accepted types.
2. **RF-2.** `validate_outgoing` (strict JSON, the integer domain, the closed schema member with no identity substitution, the UTF-8 bounds), `NullMember`, `bounded`, and `ControlSession::send` as the selection-bound sending boundary (the policy's identities, platform, offer and tuples; then the session's acceptance, with nothing advanced on refusal). Are all of round 1's constructible-but-invalid cases now refused, and is anything else constructible that the receiver would refuse?
3. **RF-3.** The private `ControlPolicy` and public `ControlObservations`; `for_session` as the only constructor outside the module's tests; `observations_mut`; the test-only `ControlContext::reference`, with the corpus tests moved in-crate; and the three compile-fail doc tests (and the `policy-made-public` mutation showing they fail only for privacy). Can production code still widen the bound or the offer set?
4. **The NBOs.** The root keyword closure, and SCOPE's record of the stream-acquisition boundary (D3a's).
5. **No regression:** the corpus still replays byte for byte, and round 1's other controls hold.
6. **The lane** `evidence/d2a-checks-r2/`: components base no tests, candidate 16 new passing (13 unit, 3 doc), equal failure sets, the same two suites; Clippy and rustfmt; CC v5's source pins; the package edges; the environment exceptions, operability, closure-unchanged and verify_design; 16 mutations.
7. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call; no new environment read; no `let _ =` in product files; no census-closure file changed.
8. **Inventory:** `control_protocol.rs` realizes its planned row; three new paths (`src/control_protocol_tests.rs` and the two data files).

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D2A-R2-RF-n` / `D2A-R2-NBO-n`.

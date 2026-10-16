# Review request: B3-B1-r1 (X2 r9 item 6b, the member observation; M3-B unit B3-b, sub-unit B3-b1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b1-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; `python3 -I -B tools/check_operability.py source --repository <tree>` in the candidate worktree.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b1-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 6307 bytes, SHA-256 `545c8ec8af428a7d1a3b4a7e87e038a5ad106c9005b84925899661a8b0243594`, 27 members. Rehash every member.
- **Bases:** product main `2b297e68e07aeae31a3fe71b6fb227f9758dcc5a`, clean (167 contract successors, inventory v202); architecture `67b8f8bcaa6e25804a61b56693a87b6b39da311e`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b1` (detached at the product base). It holds the exact bytes `product-map.json` lists.

## Authority

- Law M3-B r9 item 21 (X2 r9; successor S1, accepted), items 8, 19 (M1, M2), 23 (no waiver on member Git evidence) and 24 (`config-discovery-b/PROPOSAL-r9.md`).
- The B3-b plan r2, section 2 (`b3-b/PLAN-r2.md`; your `codex-b3b-plan-r2`).
- Item 6a as built: `crates/security/src/custody/git_tracking.rs` at the product base (X2b-2).

## What to review

`SCOPE.md` describes the unit and lead decisions LD-B3B1-1 to LD-B3B1-5. Judge:
1. **Fidelity to item 21.**
   - The `NoRepository` precondition, by type.
   - The pass-level environment, global and system sources.
   - Each member reached from W's retained descriptor by no-follow opens, with positive marker lookups between W and M and at M, and the device check.
   - Item 6a's layout unchanged, over `M/.git`, `M/.git/config` and `M/.git/index` only.
   - The gitlinks.
   - No write and no recheck evidence.
   - The subjects.

   Is anything read under `M/.git` beyond the three objects?
2. **The 6a refactor.** Is item 6a's behaviour exactly unchanged: the same steps, charges, evidence order and refusals? `layout` is factored out of `repository`, and `ConfigCheck` is a parameter, with 6a passing its existing `config`. Diff against the base.
3. **The ledger.** Is `config_decided` (and the decided environment and index-decode checks) the right answer to the ledger's latch? Are the charges the same, and is the refusal still the same refusal? Can any other 6b path still latch on a per-member refusal: custody judgments, reads, or the placement opens?
4. **The lead decisions,** especially:
   - LD-B3B1-1: pass-level refusals refuse every member;
   - LD-B3B1-3: `evidence-changed` for changed placement;
   - LD-B3B1-5: a real split index is refused as `index-malformed` by 6a's unchanged decoder.
5. **The controls and evidence.**
   - Do the seven tests cover law item 21's control list?
   - `evidence/checks-r1/`: the security suite, with 14 equal pre-existing failures on base and candidate and 7 new passing tests; Clippy; the census check (`git_tracking.rs` is outside its closure); 9 caught mutations.
   - Are the mutations meaningful?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B1-R1-RF-n` / `B3B1-R1-NBO-n`.

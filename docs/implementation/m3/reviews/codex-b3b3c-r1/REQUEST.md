# Review request: B3-B3C-r1, the D15 workspace margins (M3-B unit B3-b, sub-unit B3-b3c)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b3c-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- Do not run any tool with `--held-out-blind`.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- Never open a T2 held-out entry's store or overlay.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/tests/test_discovery_workspace_ledger.py` (synthetic, hermetic);
  - in the candidate worktree, `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/security/discovery_workspace_ledger.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1`, which opens only lead-readable stores and overlays.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b3c-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 7948 bytes, SHA-256 `91b0ea21228cf12812dded61de03c8c428a2a6b2ce4b554c86749167aef3b313`, 34 members. Rehash every member.
- **Bases:**
  - product main `fb63a93adb77f7ef50663be41241edba4c3f966d`, clean (B3-b3b bound; inventory v208, 170 contract successors);
  - architecture `f6b561d75e70c34d010a76dd11e9ecc1047e2cb8`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b3c`, detached at the product base. It holds the exact bytes `product-map.json` lists.

## Authority

- **The B3-b plan r2 §4.3, B3-b3c:** each T2 workspace row's full ledger, the walker with members entered plus the reader term plus the member term at its member count, at 2× under the r7 caps; any failure returns the caps to the law.
- **Plan §3's control (b)** and your `codex-b3b2b2c-r1`: members as synthetic conventional Git repositories, and the carrier rendered from the overlay.
- **Amendment A1:** one gated blind refresh over the final closure. **Amendment A5,** and your `codex-b3b3a1-r1`, `codex-b3b3a2-r1` and `codex-b3b3b-r1`.
- **Law M3-B r9 item 12.**

## What to review

`SCOPE.md` describes the unit and lead decisions LD-B3B3C-1 to 3. Judge:
1. **LD-B3B3C-1: a companion record rather than a census change,** so that the B3-b3b receipt (which binds the census tool) stays current. Is that a faithful implementation of §4.3's "workspace row"? Is leaving the census record's superseded walker-only string acceptable, given the Rust tie between the two records? Or is a plan amendment required?
2. **LD-B3B3C-2: both declaration branches, with the verdict on both.** Is that the right reading of "the member term at its member count"? Is any dearer composition of a T2 workspace left out?
3. **LD-B3B3C-3: the D15 shape.** Conventional `.git` members, W in no repository, the carrier rendered as the link controls render it, and no carrier for Python. Is it the workspace as D15 discovers it? Does the model's handling of `.git` (pruned, item 6b at ceilings) make the shape's lack of `.git` contents safe?
4. **Fidelity.** Does the tool add no charge of its own and reuse the census's model, verification and composition exactly? Are the branch-A refusal and the Cargo carrier byte check right?
5. **The classification.** Does the Rust test tie the record to the census (inputs, workspaces, members), recompute every sum and verdict, and make the joint caps claim? Are the four mutations and ten controls adequate?
6. **The result and the evidence:**
   - every workspace holds under both branches, the tightest being smithy-sdk's branch B at 2,630‰ edges;
   - the census, its vectors and the receipt are byte-identical to the base, and the census `--check` holds;
   - equal base failure sets, with one new test;
   - Clippy, rustfmt and verify_design.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B3C-R1-RF-n` / `B3B3C-R1-NBO-n`.

# Review request: D3A-2-r1 (item 16's ceilings and bounds, and item 12's tool class; M3-D r5 items 12, 14, 16, 17 and 22's tool row; D3a plan r4 sub-unit D3a-2), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-2-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-2-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 13196 bytes, SHA-256 `253eeb316d4e24ad30b16a4dd5dd4456704f6ecd8f4f9dcc6dfb3111fb832be7`, 56 members. Rehash every member.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a2`, detached at product main `72e078799b201709b2545ba58cdce3fcd62a933e` (D3a-1 r3 integrated, your `codex-d3a-1-r3`), holding the exact bytes `product-map.json` lists (3 modified files, no new path). **Review D3a-2's own diff** (`git diff HEAD` in the candidate worktree); D3a-1's content is not re-reviewed here.
- **History (LD-D3A2-5):** D3a-2 was first built on a local WIP baseline commit carrying D3a-1 r3's bytes while that unit was under review; its lane passed and is history. The baseline was dropped once main held those bytes, and the lane of record ran on main.

## Authority

- M3-D r5 (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`): item 1 (:186-188), item 5 (:274), item 12 (:423-449, the tool path at :434), item 14 (:490), item 16 (:526-551), item 17, item 19, item 22 (:722).
- The D3a plan r4 (`docs/implementation/m3/supervisor-d/d3a/PLAN-r4.md`), accepted with LD-D3A-17: §3's D3a-2 row, its controls and its mutations; LD-D3A-3, LD-D3A-7, LD-D3A-8, LD-D3A-12 and LD-D3A-16.
- **The lead's allocation of the tool class to D3a-2:** item 12's tool path (fds 0 to 2, fd0 at EOF, skipping `Handshaking`, :434), with the tool output bound and the materialization accounting that own it (the tool rows of items 16, 17 and 22).

## What to review

1. **Item 16's constants**, each against its row (:528-549), and `Limits::RELEASE` as the only production value (LD-D3A2-6).
2. **The sampled ceiling:** the observed sum over the group's members and the asserted `resourceReport.residentBytes`, either above the ceiling a breach, and an asserted value below never clearing an observed one (:531); sampling only while the root runs.
3. **The process count:** one for a provider, 16 for a tool (:533), and LD-D3A2-4's test seam for D3a-1's member-spawning fixtures.
4. **TS2's response bound** from the participant's accounting (LD-D3A-3), and Rust3's totals left to its codec.
5. **The scratch at settlement** (LD-D3A-12): the bounded walk before removal, `scratch-bound` at the limit's passing, at exhaustion or on I/O failure, a clean end becoming it (DRJ2:125); provider only.
6. **Zero fit** (:534), for a provider and (LD-D3A2-7) a tool.
7. **Tool materialization** (LD-D3A-16): the checked charge before each write, the exact refusal with nothing charged, and the distinct limit.
8. **The tool class** (SCOPE's "The tool class" table; LD-D3A2-1 to LD-D3A2-3): one state machine, provider-only parts as `Option`s and the uninhabited `NoProvider`; `Handshaking` skipped; fd1 read by the loop and charged before it is kept; the bound's refusal, fd1 closed and `byte-bound(tool-output)`; the tool's wall clock; the ladder from T-2; a tool's end at fd1's EOF and `clean` with its own exit; `unexpected-exit` with fd1 held past the drain; `take_tool_output` and `tool_output_bound`; never `admissible()`; the descriptor-set check.
9. **No regression** in D3a-1's provider path: the `Option` reads of the control plane and participant, the moved `Delivered` append (now after the participant call, before its step is applied), and D3a-1's tests unchanged but for the four adaptations SCOPE lists.
10. **The lane** `evidence/d3a2-r1-checks/`: components 77 → 93 with equal failure sets, the base on main's checkout; Clippy, rustfmt and the workspace check; the fixture record in both checkouts; edges, feature scope, environment exceptions, operability, the unchanged closure and verify_design; the 14 mutations.
11. **The rules:** no new mint-census call, no environment read, no `let _ =`, no new dependency, no invented constant.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A2-R1-RF-n` / `D3A2-R1-NBO-n`.

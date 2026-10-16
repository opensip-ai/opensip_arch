Codex review: M3-B r9, configuration and discovery. A **law review**, round 1 of r9. r9 amends one bullet of item 14a (the pre-Plan TypeScript configuration graph's reading grammar) in answer to your B2C2-R1-RF-1, and adds two controls. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-m3b-r9-r1.

**Rules:** read-only; no repository edits, commits, pushes or delegation; no product build, test or generator run (reading, hashing and `git show` / `git diff` are fine). Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys or any held-out store. No network is needed.

## Subject

- **Subject manifest:** `docs/implementation/m3/config-discovery-b/m3-b-r9-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `940fefbea8c9e6533c0511015971bde37f20e6dc067750866aa88865945ad528`. It pins `PROPOSAL-r9.md`.
- **Diff base:** `PROPOSAL-r8.md` (`58adf8f0…`), the r8 bytes you accepted in `reviews/codex-m3b-r8-r3`. Every change must appear in r9's "r9 changes" section.
- **Context:** your `/tmp/opensip-implementation/reviews/codex-b2c2-r1/review.json` (B2C2-R1-RF-1) and the B2-c2 r1 package `config-discovery-b/b2-c2-r1/SCOPE.md` (LD-B2C2-2(a), (h)). B2-c2 r2 will follow this law's outcome: with r9 accepted it keeps the empty-document reading; otherwise it refuses such files.

## What r9 changes

1. Item 14a, "The grammar": a file holding only whitespace and comments reads as an empty object; the root value and `compilerOptions` (where present) must be objects, `null` included as the wrong type, so `malformed`.
2. Item 14a's controls: empty and comment-only files (entry and base) read as an empty object; `null` roots (with or without comments) and a `null` `compilerOptions` are malformed.
3. Banner, the "r9 changes" section with its basis (TypeScript's documented acceptance of an empty `tsconfig.json`, microsoft/TypeScript PR #1692, cited as supporting evidence), and one Not claimed line.

## Decide

1. **Soundness.** Is admitting the empty document a sound law decision for the pre-Plan reader, consistent with item 14a's purpose (no TypeScript runs; effective `allowJs` of an ordinary project) and with NE:527-545 (a `jsconfig` read as empty still supplies `allowJs: true`)? Does it weaken any refusal item 14a needs?
2. **The object requirement.** Is stating it a faithful completion of r8 (which named the wrong-typed fields and "not JSONC") rather than a new refusal? Is the public termination (S10's alias rows, D9 row, remedy) still true for every case, so no S10 successor is needed?
3. **Scope and fidelity.** Does r9 change anything beyond what its section lists? Is the TypeScript citation used only as supporting evidence?
4. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `M3BR9-R1-RF-n` / `M3BR9-R1-NBO-n`.

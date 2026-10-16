# Review request (round 2): B3-B0-REFERENCE-r4 (the members-and-readers reference with index gitlinks; contract successor 169)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b0-reference-r4-r2/`).

## Boundaries

- Do not edit either repository or the control files.
- Do not run Cargo, tests, the census or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - running the checker, `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/config-discovery-b/b3-b-reference-r4/evidence/check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --reference /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/config-discovery-b/b3-b-reference-r4/reference/member_reader_reference.py --packages-root /Users/sb/code/opensip-ai/opensip --out <a path outside the repositories>`;
  - importing the reference read-only, and in-memory mutants of it, as in round 1.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b-reference-r4-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `da0ee22dfe5876d2e1c3d3fe1f86d4cbe1e5ba4a8a6aee1def19561f71fceff3`, with the same 6 members as round 1.
- **Bases:** unchanged, product main `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2` and architecture `16de973a1986ac07277df1ee6e7b9421cb430ff3`.
- **The lead's scratch binding:** `lead-verify-scratch.json` in this directory. It still passes at successor 169.

## Round 2

Your `codex-b3b0-reference-r4` raised B3B0REF-R4-RF-1 (the gitlink validator related elements before validating them all) and NBO-1 (no-member equality is regression coverage). The README's "r4 round 2" table resolves both.

**What changed since round 1:**
- `_member_gitlinks` validates in two passes, with a container diagnostic.
- The checker has nine new `raises` controls.
- Its `raises` path asserts the exact type and diagnostic, and that no reader lookup, item-6b consultation or walk happened first.
- There are two more negative-control mutants.
- The evidence, the successor record and the manifest are refreshed.

Nothing else in the reference changed: `diff` it against your round-1 reading.

**Judge first** whether RF-1 is resolved, re-running your `["sub", 17]` and reversed reproductions, the non-list values and the non-mapping table. Then confirm that your round-1 judgments still hold for these bytes:
- the gitlink semantics;
- branch A's order;
- LD-B3B0-14 to 16;
- the controls and spies;
- the successor.

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B0REF-R4R2-RF-n` / `B3B0REF-R4R2-NBO-n`.

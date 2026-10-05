Codex review: law **HSR r1** and design unit **HSR-1**, together. Grok leads as of 2026-10-04. You are the single reviewer.

**Lead note (reviewer change).** This package was drafted for a Grok review. Codex reviews it. The directory stays `grok-hsr-r1`, because `build_hsr_1.py` emits that review path and `hsr-1-unit.json` names `reviews/grok-hsr-r1/hsr-1/review.json`. Do not rename it.

Two verdicts, in two `review.json` files:

1. **Law HSR r1.** `ACCEPT` or `REQUIRED-FINDINGS`. `subjectSha256` is the sha256 of `docs/implementation/m3/syntax-e/hsr/PROPOSAL.md` (`19770e3541f71139b2771350399e7967df6da8c6517b747e07d4a435d2d5ae6e`, 44788 bytes).
2. **HSR-1.** `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`, with `subjectManifestSha256` `6017c4a2f615ed7be16cff491d4b9d94c1984275cd04c4bc17d6d82809c204d3` (the subject manifest, 1216 bytes). The design-unit file must carry `supersededPassages`, exactly the one entry below.

Write only under `/tmp/opensip-implementation/reviews/grok-hsr-r1/`:

- `review.json` and `REVIEW.md` for the law. `REVIEW.md` also covers HSR-1.
- `hsr-1/review.json` for the design unit.

No repository edits, commits, pushes, or delegation. No cargo, build, test, or crash-matrix run. This review does not take the lane lock.

**Rules:**

- Git is read-only. Product main is `/Users/sb/code/opensip-ai/opensip` at `43ea32a`. Arch is `/Users/sb/code/opensip-ai/opensip_arch`. Both are uncommitted for this package; do not stage or edit them.
- Python only, if you rerun evidence: `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`.
- `verify_scratch.py` rewrites the worktree `design-lock.json` and refuses a lock that is already edited. Do not run it in the main checkout. Do not reuse `/Users/sb/code/opensip-ai/opensip-hsr-check`: that throwaway still exists and its lock is already dirty. A rerun needs a fresh detached worktree of `43ea32a`.
- Never touch `~/Library/Application Support/OpenSIP`. Never read the private 413 UUID fixture.
- Pin accepted snapshots only. Every pin is in `hashes.txt`.

## Subjects

Law: `docs/implementation/m3/syntax-e/hsr/PROPOSAL.md`. Draft r1, not accepted. It names historical schema readers (decision B on E2s's stop), successor HSR-1, code unit HSR-a, and a re-scope of E2s. It touches no product file. Lead decisions LD-H1 to LD-H12 are in the proposal. Answer Q1 to Q5.

HSR-1 subject manifest: `docs/implementation/m3/syntax-e/hsr/hsr-1-subject.json`. Six members, all under `hsr-1/`: `README.md`, `PASSAGES.md`, `successor.json`, and `evidence/{build_hsr_1.py,check_hsr_1.py,verify_scratch.py}`. `hsr-1-unit.json` is the lead's draft and is not part of the subject. Answer R1 to R5 in the HSR-1 README.

HSR-1 is one VD2 contract passage supersession of I1-L's IE:214 override, three plain IE overrides (lines 662, 678, 808), and two JSON Pointer overrides of SYN-1F's selected identity-schema copy. It binds only after this law is accepted, in a binding-only product commit, before HSR-a.

`supersededPassages` on `hsr-1/review.json`, exactly:

```json
[
  {
    "record": {
      "path": "docs/implementation/m3/preview-pack-i1/i1-l/successor.json",
      "bytes": 35443,
      "sha256": "9c490137998222627a011eec72af8c0ed3bb568e3085725fdf11b8610d42c6a1"
    },
    "parent": {
      "path": "docs/v2/contracts/product-v1/identity-and-evidence.md",
      "bytes": 135448,
      "sha256": "c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f"
    },
    "selector": { "line": 214 }
  }
]
```

## Lead evidence

`evidence/local-binding-check.json` is the lead's `verify_scratch.py` run on a throwaway of `43ea32a`. Baseline 101 contract successors and 5 passage supersessions. With HSR-1, 102 and 6, PASS with and without the worktree as implementation. The six refusals match the messages in the HSR-1 README. The extension route (one further row by superseding IE:808) reaches 103 and 7. The literal CLI on the appended lock stops at `SCRATCH-HSR1/review.json`. You may rerun `build_hsr_1.py --check`, `check_hsr_1.py`, and `verify_scratch.py` on a fresh worktree. The pinned check is the lead's result either way.

## Decide

- Law: do Q1 to Q5 hold, and is anything else blocking `ACCEPT`?
- HSR-1: do R1 to R5 hold, is the record exactly items 3 to 8, and does `supersededPassages` match the record?
- A disagreement with a lead decision is a finding.

When you finish, reply with two lines: the law verdict and its `review.json` path, then the HSR-1 verdict and its `review.json` path.

Do not commit.

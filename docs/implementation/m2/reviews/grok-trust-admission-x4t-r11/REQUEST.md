Grok re-review: law X4T r11, after your r10 RF-1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-admission-x4t-r11.

Subject: `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/trust-admission-x4t/PROPOSAL.md`, r11, sha256 7fe098fd30de298cf1e09ca6514d8a50eef6a328cb25bda6ebcf4398353cd384. r10 is preserved as PROPOSAL-r10.md. Your r10 review is `/tmp/opensip-implementation/reviews/grok-trust-admission-x4t-r10/`.

Change: item 4 now verifies `heads.revocation`'s stored body and envelope against the signing root, `heads.root` (root M), with the keys revoked before it, instead of against the accepted root. The header gains the r11 note and the title says r11. Diff r10 to r11 and confirm that nothing else changed.

Decide whether RF-1 is closed, and whether anything new is wrong. Also confirm that the rest of r10 raised no other required finding: the two roots, the closure join, and X4T-a3.

review.json must contain "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.

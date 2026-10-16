Codex review: the B2-d implementation plan **r3** (framework recognition host side, the YAML subset reader, the recommendation evidence; M3-B items 16 and 18). A **plan review**, round 3. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-b2d-plan-r3.

**Rules:**
- Read-only: no repository edits, commits, pushes or delegation.
- No product build, test, generator or census run. Reading, hashing and `git show` / `git diff` are fine.
- Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys, or any T2 store or overlay.
- No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/config-discovery-b/b2-d-plan-r3-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `45440a5090d27db5c462c516f18c08d9522d12b7784566eab14bd64c0a32c0c8`. It pins `b2-d/PLAN-r3.md`, with r1 and r2 as history.
- **Bases:** product main `a50ae96`; architecture `4415adb5051de65c8e2b0e0ce493d1a59f2941c6`.
- **Your earlier reviews:** `codex-b2d-plan-r1` (RF-1 to 6) and `codex-b2d-plan-r2` (RF-1 and 2), under `/tmp/opensip-implementation/reviews/`.

## Decide

1. **The two r2 findings.** Does the "r3 changes" table, with sections 3 and 4, resolve them?
   - **RF-1:** the bound on retained recognition holds under an explicit override, and only the effective entry points are explicit.
   - **RF-2:** absence is no field and no provenance entry, there is no `Defaulted` branch, and the controls run on actual `resolve` outputs.
2. **New problems.** Do the r3 revisions introduce any? Is anything else blocking?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B2DPLAN-R3-RF-n` / `B2DPLAN-R3-NBO-n`.

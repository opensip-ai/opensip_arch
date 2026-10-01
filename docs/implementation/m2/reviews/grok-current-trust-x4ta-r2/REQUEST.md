Grok re-review, two subjects: the law X4T r6 amendment, and the X4T-a r2 code. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-current-trust-x4ta-r2. If you build, use a CARGO_TARGET_DIR under it.

## Subject 1: X4T r6

The law is `trust-admission-x4t/PROPOSAL.md`. Diff it against PROPOSAL-r5.md, which equals the accepted r5.

Item 11's cost pin is replaced (lead decision). A lawful generated store cannot reach the 40 MiB closure total. So X4T-a pins three things:
- the linear charge: one object and its stored bytes per distinct record read;
- a measured native read within `TRUST_VIEW_COST`;
- boundary tests of the closure check.

The rejected alternative is a padded, chained 40 MiB generator.

## Subject 2: X4T-a r2

Product: the worktree `/Users/sb/code/opensip-ai/opensip-x4ta` (base 5b5f04c). Pins are in hashes.txt. Save the diff as product.diff and report its sha256. The r1 review is `reviews/grok-current-trust-x4ta-r1/`. v90 is unchanged.

**Changes:**
- **RF-1.** Only the P0 shape is F absent: both heads and history null, every role `ST-UNBOOTSTRAPPED`, no acceptance. Any other null, or a non-retained clock, takes the incomplete row.
- **RF-2.** The 40 MiB total is closure bytes only, excluding the stored root documents other than the root head. `Cap` takes the incomplete row. The full-size pin follows X4T r6.
- **RF-3.** `nested_input` is gone. Owner errors are matched on their typed variants. `trust_ordinary_metadata.rs` exposes its `catalog` module within root_payload.
- **RF-4.**
  - `core_closure` is required.
  - Revocation entries refuse with `CONTINUE-CORE-NOT-TRUSTED` and subject `kind:subject` when both the kind and the subject name a closure component (`release`, `keyId`, `namespace`, `catalogSnapshot`).
  - Signers are collected before filtering.
  - The catalog and revocation quorums are rechecked with revoked keyIds excluded.
  - X4T-0's `Spec` gains `revocations`.
  - Each of the four kinds is tested on both reads.
- **RF-5.** Recovery goes through `standing_of`, the role-machine join, right after the `accepted.by` check, giving subjects `core:recovery` and so on. This moves standing before authentication, so a continuation refusal now wins over a later signature or time refusal. A Recovery bundle, profile or repair fails authentication on the incomplete row.
- **Inventory RF-1.** The stale `accepted_store_fixture_tests.rs` description is deferred to D1, and v90 is not rebuilt. Avoiding the pin change would weaken the pin.

**Checks.**
- X4T-a and fixture tests: 28/28. Clippy, fmt, `check_package_edges` and verify_scratch pass.
- Workspace: 1227/0 on one run. Another run failed only known F3 interference.

**Please rule on:** standing before authentication; deferring the description to D1.

## Verdict files

Write one REVIEW.md, and two verdict files:
- `x4t/review.json`: "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings", "subjectSha256" of X4T r6;
- `x4ta/review.json`: "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS), "requiredFindings", "subjectManifestSha256" (the sha256 of current-trust-inventory-v90-subject.json), "inventoryCandidateAssessment" {verdict, requiredFindings, path, bytes, sha256 of v90, parent (the v87 pin), successorRecord}.

Do not commit.

REVIEWER review: law X4T r1, native current-trust admission. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/REVIEWDIR. Law review; no product cargo. Product HEAD is f7acb6d.

Subject: docs/implementation/m2/trust-admission-x4t/PROPOSAL.md r1 (pin in hashes.txt). Context:
- X4 r2 (`live-guards-x4/PROPOSAL.md`, RF-1 created X4T);
- laws 463 and 466, X3a r3, X3b r1 and X2 r4;
- security model S4 to S6 and the trust sections;
- product `trust/` modules: `native_current`, `native_record_capture`, `root_payload`, `revocation.rs` and `trust_policy`;
- owner.md §7.

## Decide

- **Items 1 and 2 (lead decisions).** Is the `AdmittedCurrentTrust` view and its read set and order sound: reference-only reads with a 4 MiB cap, `state.v1` read again at the end, and no full census?
- **Item 3 (lead decision).** Authentication: from the installation's accepted root, with S5 root chains and every signature re-verified. Is it right that the embedded root authenticates only the release?
- **Items 4 and 5.** Revocation through `verify_revocation`, and policy through the merge, with the digest in the epoch.
- **Item 6 (lead decision).** Time: S4 applied on the first read only. Observer rereads use the start time advanced by elapsed monotonic time.
- **Item 7 (lead decision).** The X4T-b floor publication under the fence, reusing 467's producers. Is it consistent with X3b's carrier floor, with X2e's handoff order, and with X2's rule that the retained record advances only through a confirmed publication?
- **Items 8 and 9.** One read of `state.v1`, reused from X3a; the reread protocol with one retry.
- **Item 10.** Check every row against S12. In particular: the role-state rows on `CONTINUE-CORE-NOT-TRUSTED`, `TRUST.NO_ADMITTED_TIME_CONTEXT` for "Unbootstrapped", and the new custody subject `trust-rollback`.
- **Item 11.** The `TRUST_VIEW_COST` ceiling and how it is measured.
- **The X4B finding.** A fresh installation's trust is Unbootstrapped, so a separate bootstrap-acceptance unit (X4B) must come before X11. Is that correct and correctly scoped?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.

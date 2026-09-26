Grok review law proposal 462 r1 (InitialPlatform). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-initial-platform462-r1. Law review. You may read code; do not run product cargo. Do not read or print the private 413 UUID fixture.

Subject: docs/implementation/m2/initial-platform-462/PROPOSAL.md (pin in hashes.txt). It closes points owner.md §1a step 4 leaves open, found while designing 462:

- Item 1 (profile location): the inventory pins only a body digest (platformProfileBinding), and 463 opens no other name.
- Item 2 (authentication path): `verify_profile_set_with` refuses non-schema-2 roots (admitted_profiles.rs about 74–84), while owner step 4 and contract §S9.1 (security-and-lifecycle.md about 849–853) use the core-pinned copy under a schema-1 root.
- Item 3 (observations): the boot, process and loader observers are not ledger-charged today.
- Item 4 (home-base premise).
- Item 5 (rename and barriers, 462 versus 465 and 467).
- Item 6 (Evidence B minting and its citation).
- Item 7 (SYNTHETIC profiles).
- Item 8 (BASELINE-ATTESTED consequence).
- Item 9 (receipt and recheck).

Relevant code:
- native_platform.rs (the fenced factory; `machine`, `filesystems`)
- root_payload.rs (`platform_decision`, `install_acl_omission`)
- custody/installation_root.rs:206–237 (`AclOmissionPremise`) and 460's use at about 460–506
- initial_core.rs
- core_authentication.rs `EmbeddedRelease`

Decide: is each item sound and minimal against owner.md §1a step 4 and §3, laws 458/458b/469/463, and contract §S8/§S9.1? In particular:
- Is the pin-only path under schema-1 or typed-absent TR-PROFILE right, and chosen only by the final root?
- Is H's fstatfs the right pre-installation fsType?
- Is deferring rename and barrier receipts to 465 and 467 consistent with owner step 4's "including exclusive same-parent directory rename, exact supported directory barriers"?
- Is anything missing?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" (id, title, failureScenario) and "subjectSha256". Write REVIEW.md and review.json. Do not commit.

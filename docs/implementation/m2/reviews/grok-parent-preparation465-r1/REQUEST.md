Grok review law proposal 465 r1 (parent preparation and creation permit). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-parent-preparation465-r1. Law review. You may read code; do not run product cargo. Do not read or print the private 413 UUID fixture.

Subject: docs/implementation/m2/initial-parent-preparation-465/PROPOSAL.md (pin in hashes.txt). **Items 4 and 5 are owner decisions made on 2026-09-27.** The owner chose them over the listed alternatives: for item 4, adding a zero-rights allow to new external ancestors; for item 5, refusing an interrupted OpenSIP with a manual remedy. Review how they are written and scoped, not whether to take them.

Governing text: owner.md §1a steps 5–6, §1b, §2, §3 (the finite base-to-parent confirmation sequence), §4, §5 (§5.6 barrier fallback), §6 and the storage paragraph; laws 458 (§5), 460, 462 (items 4 and 5) and 464.

Relevant code:
- platform filesystem.rs: `confirm_directory_barrier` (about 101; uncharged today), `DirectoryBarrierReceipt<'d>` (about 61–73), `create_exclusive_directory` (about 324) and its synthetic AlreadyExists (about 180–184), the barrier fallback (about 984–1000);
- installation_root.rs: the 460 walk;
- private_access.rs: `prepare_fresh_private_sample_reserved`, `observe_private_directory`;
- initial_installation.rs: `recheck_intent_target`, `consume`;
- initial_platform.rs.

## Decide

- Is the effect order right against owner §3? Is the seven-barrier count right, including H counted again as Library's parent?
- Item 2: are the accepted receipt kinds right? Is the in-memory barrier record a faithful "typed receipt retained" given receipts borrow their directory?
- Item 3: is it right that only a raw EEXIST gives fresh admission?
- Items 4 and 5: are they scoped tightly, and does item 5 avoid being a permission repair under §1b and §6?
- Item 6: is the per-effect reservation enough for owner §2?
- Items 7–11: are they right? Is anything missing, for example how the permit binds the intent to the preparation, or crash states?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" (id, title, failureScenario) and "subjectSha256". Write REVIEW.md and review.json. Do not commit.

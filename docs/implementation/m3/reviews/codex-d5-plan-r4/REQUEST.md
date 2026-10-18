# Independent review request: D5-PLAN-r4

The implementation lead is now Codex. This revision requires an independent reviewer; its author must not supply its acceptance verdict.

Write only REVIEW.md and review.json in /tmp/opensip-implementation/reviews/codex-d5-plan-r4. Do not edit either repository, worktree, control file or staged subject. Read-only file inspection, hashing, JSON parsing and Git queries only. No builds, Cargo, rustc, lanes, network, other panes or delegation. Do not access private 413 fixtures, installation directories, signing/private keys, held trees or entries, T2 stores/overlays/cache.

Subject root: /tmp/opensip-implementation/codex-takeover-2026-10-17/d5-plan-r4/architecture
Manifest: /tmp/opensip-implementation/codex-takeover-2026-10-17/d5-plan-r4/architecture/docs/implementation/m3/supervisor-d/d5-plan-r4-subject.json (933 bytes, SHA-256 6a57ec202520eadb301eeba104e312b06a3b245469867e5c615a0fb004542048). Verify all four members. PLAN-r4 is the subject; r1-r3 are unchanged history. Other referenced authorities remain in /Users/sb/code/opensip-ai/opensip_arch at the same opening hash pins. Product base is 4e475c753002d21ed99e0d53e64218e55af0cb1f; architecture base e9474b1fe502c82a477ddafe15cf16ad0a92766a.

Read the prior review /tmp/opensip-implementation/reviews/codex-d5-plan-r3/REVIEW.md and review.json. Verify the r4 changes: build targets including custom/disabled build roots receive no policy exemption; Boolean path conditions, inline/item gates, mixed paths and unknown syntax cannot grant an unsound test/feature exemption. Check matching controls and any regression from r3's accepted portions. Answer Q10 explicitly. Q9's accepted D1b ownership remains unchanged.

Return review.json as {"verdict":"ACCEPT"|"REQUIRED-FINDINGS","subjectManifestSha256":"6a57ec202520eadb301eeba104e312b06a3b245469867e5c615a0fb004542048","requiredFindings":[],"nonBlockingObservations":[],"rulings":{"Q10":"..."}}. Use D5PLAN-R4-RF-n and D5PLAN-R4-NBO-n ids as needed. This is a plan review, not implementation/runtime acceptance.

# M3-B r6 law review

Verdict: **REQUIRED-FINDINGS**. One correction is required to the new D15 member-observation term. No non-blocking observations.

## Exact subject and scope

Independently rehashed the 440-byte subject.json to SHA-256 `34c1004c1fe9088ba88d7159edf7709305302a494da729308e6e6a71e203bee9` and verified its sole member: PROPOSAL-r6.md, 115,991 bytes, SHA-256 `b5bb4744e1ee3f05f682dced633c35b0951e8cd1466fe0a32497b8f26e5dcc2f`.

Both repository HEADs match the requested bases; product main is clean and its lock selects inventory v197. Diffed against live PROPOSAL.md. Apart from the proposal title/banner and r6 change record, substantive edits are confined to item 12's caps/measuring/storage text and its matching Not claimed line. All other law text is unchanged.

## M3BR6-R1-RF-1 — Derive a ledger bound for member observation

Location: item 12, PROPOSAL-r6.md:429-430.

Adding D15 work to the workspace row is necessary because it shares the discovery ledger. The proposed bullet, however, identifies that work's bound only as item 19's per-member ceilings, 4 MiB per index and 64 KiB per Git config. X2:272 caps file lengths; it separately requires all work to be charged. Payload ceilings are not themselves cumulative ledger-cost bounds.

The distinction is concrete in the existing product. work_reader.rs:156-168 charges each complete requested buffer, retaining all previous charges. Reading a file of length 4 MiB and probing EOF can charge the 4096-doubling sequence through 4 MiB plus the max+1 buffer: 12,578,817 bytes, before custody or decoding. git_tracking.rs:837-846 then charges another twice raw.len() for index decoding. Its config parser also charges raw.len(), in addition to the config reader's buffer growth. Directory/file opens, metadata/ACL/filesystem observations and retained records add costs in all dimensions. Read-attempt edges also need the same explicit structural/retry envelope discipline as the walker model.

Consequently, adding only member count times those two file ceilings does not establish a 2x margin on the shared ledger. The new rule correctly notices the missing work but has not defined its sound bound; memberObservationBoundIncluded is false for a complete ledger bound, not because the candidate omits a member bullet altogether. Likewise the power-of-two rounding formula is mathematically sound, but capRuleSound is false for the complete operational rule until its cost input is sound.

Required correction: require a reviewed D15 upper bound in objects, edges and cumulative charged bytes, derived from the member count and every charged operation. Add that bound to each workspace's discovery cost before taking dimensional maxima and applying the 2x rule. Use the X2 ceilings as inputs to the reader/decode/custody model, not as a substitute for it. Pin the relevant cost closure and controls, or explicitly leave full-invocation margin outstanding until the member producer/model is reviewed. Label the current option (a)/(b) arithmetic as walker-only unless the full added term has been evaluated.

This correction can remain within item 12. It does not require implementing D15 or changing either repository during this review.

## Evidence and options

Checked the bound product census and its probe cross-check. The r6 figures for the existing walker are accurate:

- Largest objects: aws-sdk-rust 2,611,910; twice is 5,223,820, rounded up to 2^23.
- Largest edges: 1,007,224; twice is 2,014,448, which fits 2^21.
- Largest bytes at R=1024: 1,215,655,148; twice is 2,431,310,296, rounded up to 2^32.
- Largest bytes at R=4096: 3,204,428,012; twice is 6,408,856,024, rounded up to 2^33.

The affine aws-sdk-rust expression 552,730,860 + 647,387*R matches all displayed values. Its byte margin fails at all three reported R points. The other two named object/long-root byte failures match the census. Edges pass throughout the currently modeled population. All four archived probe comparisons equal the recorded walker costs at their measured root. optionArithmeticCorrect therefore records the arithmetic for these stated walker inputs; it is not approval of a complete D15-inclusive cap calculation.

Option (c)'s approximately 1.97M objects/443 MB figure and resulting example caps are explicitly a counterfactual estimate, not census evidence. The normative text requires the successor's bound census, including residual root costs, before final caps. No estimate is substituted for that evidence.

## Recommendation, margin and owner scope

The storage recommendation is sound as a separately reviewed successor requirement: relative scope keys, descriptor-relative child observation/opening, single-pass listing conversion and observation-only slots remove avoidable duplication. The population, evidence and records must remain equal to the reference and charges must precede allocations. It does not assume that relative keying alone removes every root-dependent charge; residual costs remain a census result.

Keeping current caps provisional with no margin claimed until that successor is accepted and censused is honest. Byte census at R=4096 matches the current project-root spelling bound. Replacing the old objects/edges-only premise is justified by the walker's independent charged storage, while retaining the old ceilings as file-read bounds is appropriate. Final cap arithmetic must use the complete costs required by RF-1.

The options cover unchanged storage with higher caps, a new root-spelling refusal, and a storage redesign. Their memory tradeoffs are clearly framed; RF-1 supplies the missing shared-ledger accounting. Choosing (c) as a lead decision is consistent with plan r4 section 2.4 when observable population, records and refusal policy are preserved beyond the explicitly permitted memory/cap changes. A new user-visible root refusal would require owner escalation, as stated. Any successor discovering another behavioral change must respect that boundary.

Held-out margin remains outstanding for an authorized non-disclosing harness. Neither the storage choice nor a lead-readable census closes B2-b or establishes qualification. The proposed recording revision may record final arithmetic only after its reviewed census exists; no product cap change or binding is made here.

Only read-only reading, hashing, JSON parsing and Git queries were used. No compiler, Cargo, tests, builds, lane, network, other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or T2 held-out entry was accessed; no T2 stores or overlays were read. Only REVIEW.md and review.json were written. Neither repository, stage nor controls were edited.

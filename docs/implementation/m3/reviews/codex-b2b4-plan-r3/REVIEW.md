# B2-b4 plan r3 amendment review

Verdict: **REQUIRED-FINDINGS**. Two corrections are required in the amendment. One non-blocking metadata observation is recorded. The accepted section 1 is not reopened.

## Exact subject and scope

Independently rehashed the 452-byte subject.json to SHA-256 `600a96562995574ff015be9224b69da2448da9e7e9e740d4f9f8a4ba6d322f64` and verified its sole member: PLAN-r3.md, 24,034 bytes, SHA-256 `d72a87ec3721092fba389a87da21bed70f7039e2606af96a80399702208e29f1`.

Both HEADs match the subject's full product/architecture hashes, and product main is clean. The actual lock selects inventory v196 and has 164 contract successors. Compared the revision with published PLAN-r2.md: section 1 and the complete LD-B2B4-1..7 block are byte-identical. The substantive changes are the stated section-2 amendment and new LD-8/9, with its explanatory recording text. The introductory historical bases are addressed in NBO-1 below.

Verified the accepted B2-b4a subject pin and the two probe artifacts' member pins before relying on them. Read their archived bytes and the relevant native charge formulas; no probe or census was rerun and no stores were inspected.

## B2B4PLAN-R3-RF-1 — Pin the word size used by classification bytes

Plan location: section 2.1, line 151.

The proposed native type-size list contains stat, Metadata, ObservedEntry, the name/observation tuple, CapturedAclEntry, DescriptorAclCapture, statfs, DescriptorFilesystem and attrlist. It omits usize. discovery_walk.rs:99-100 charges classification temporaries as segments multiplied by two times size_of::<usize>(), in addition to relative-path and record terms. This size therefore contributes directly to the byte model's base coefficient.

Whole-file hashes preserve that source expression but do not resolve its target-dependent value. The security/platform split is otherwise appropriate, but the enumerated checks are not a complete size inventory.

Required correction: add usize to the recorded/native-asserted sizes, or pin/assert the supported pointer width and derive its byte size from that checked value. Make completeness explicit: every size_of operand used by a modeled charge must be covered. The implementation must not silently supply an assumed word size outside that checked contract.

## B2B4PLAN-R3-RF-2 — Measure option (c)'s residual root-length terms

Plan location: section 2.2, lines 164-167.

Relative scope keys are a reasonable optimization candidate. They do not, by themselves, justify the stated result that R disappears from bytes and per-name objects decrease.

The native ledger charges cumulative allocation requests, not only retained storage. For example, spell() at discovery_walk.rs:342-344 charges an absolute joined spelling before allocation, independently of the scope key. walk() at lines 988, 993, 1011 and 1022 charges root-spelling records; frame and verdict records also contain absolute spellings. Removing retained absolute scope keys still leaves R-dependent charges unless the successor also changes those paths. Replacing an absolute key allocation with a relative key allocation shortens its bytes while retaining its object count.

Required correction: describe option (c) as a redesign with a measured residual affine cost and object count. Do not assume a zero root coefficient merely from relative keying. If eliminating R entirely is the objective, include the corresponding transient/root/frame/verdict allocation changes, with the successor's charge audit and re-census proving that result. Before that successor exists, clearly distinguish an estimate or justified counterfactual model from measured code costs. Final caps must use the accepted successor's actual census.

This does not reject option (c), require a particular storage design or reopen B2-b3b. It corrects the quantitative promise used to compare the amendment's options.

## Supported facts and method

The byte-storage concern is supported. The accepted probe reports aws-sdk-rust completing with 639,480,718 charged bytes at a 134-byte root spelling, using the disclosed throwaway tree with higher limits. Its diff changes only discovery limits and adds the ignored probe. Those temporary probe limits are not accepted caps or changes on product main.

Item 19's member limits, index/config read ceilings and S3 file-custody bounds do not bound the number and spelling lengths of the walker's own per-name records. The source explicitly charges raw names, owned name/path/validator copies, absolute spellings, observed records, observation slots, classification temporaries, captures and frames. The census has 270,995 listed names in aws-sdk-rust; population size and root spelling can dominate cumulative requested bytes independently of file reads.

For a fixed population/traversal, the current byte formulas are compatible with an affine upper bound in R: each absolute spelling is the root prefix plus fixed relative bytes; the remaining type, relative-path and fixed-buffer terms are independent of R. Anchoring each full formula in the pinned closure is appropriate. The existing structural/read-interruption envelope remains in force; this is not allocator RSS or an arbitrary-I/O completion guarantee.

The capture-branch comparison is arithmetically sound at the stated sizes: 128 * 16 + 128 = 2,176, less than the stated FS cost 2,368. The new native pins must verify those operand sizes and derived formulas, rather than treating the displayed figures as invented constants. Charging the complete bounded-reader growth sequence to the ceiling is conservative.

Extending the existing completed-walk soundness checks to used.bytes, evaluated at each scratch root's actual UTF-8 byte length, is an appropriate control alongside formula inspection. The planned dropped-scope-entry-byte mutation targets a material per-name term. The R=134 comparison ties the model to the accepted probe; R=1024 is a useful macOS pathname-scale reporting point, not a new admission bound; path_binding.rs::components explicitly rejects project-root spellings longer than 4096 bytes. Descriptor-relative traversal means PATH_MAX alone should not be substituted for that code limit. No optional store counting was needed.

## Amendment sequence and owner gate

Options (a), (b) and (c) cover the principal choices of retaining current behavior with larger caps, adding a root-spelling refusal, or changing storage. Their quantitative comparison needs RF-2's correction. The evidence-first sequence and rule that final caps come from a census with shown 2x arithmetic are retained; no numerical caps are selected here.

The cap step follows the accepted law amendment and, for option (c), the accepted walker successor and re-census. It updates the code caps and their tests, refreshes closure pins and then asserts the lead-readable margin. A passing lead-readable margin still does not close the all-entry held-out gate.

Section 2.4 correctly raises a recommendation that changes behavior beyond caps to the owner, particularly a new root-spelling refusal. Held-out margin remains an owner escalation under LD-B2B-4, and no approval is inferred. The proposed byte-census work changes the future plan; it does not itself amend current M3-B item 12, change code caps, bind anything or qualify the product.

## Non-blocking observation

**B2B4PLAN-R3-NBO-1:** The retained introductory product/inventory/architecture values describe r2, while the exact r3 subject bases and bound B2-b4a state are newer. Label those introductory values as historical or refresh the metadata. The request also carries stale v195/shared-r95 prose. The actual reviewed bases are product ec2d655d (v196) and architecture a84239c2.

Only REVIEW.md and review.json were written. Neither repository, stage nor controls were edited. No Cargo, tests, builds, lane, network, other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or T2 store/overlay was accessed. No code, binding, law change or qualification is claimed.

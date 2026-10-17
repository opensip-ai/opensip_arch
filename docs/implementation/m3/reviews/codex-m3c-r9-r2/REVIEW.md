# M3-C r9, round 2 review

**Verdict: ACCEPT.** All six round-1 findings/observations are resolved. One new nonblocking documentation observation. Acceptance covers this conditional law record; it does not accept C1a4 implementation or establish its blind-validation result.

## Exact subject and execution boundary

Verified the 4,602-byte manifest SHA-256 `6bfde0782224ae7f800044ea9b559fa1146fbc01066da7629a2f7616506498cf` and all 21 members. RECORD-r9.md is 29,463 bytes, SHA-256 f360d1aa9eb5b68c5ef36d1250548b60424f4c204673c73ff10ac51906d39b29. The sealing copy matches the 16,400-byte C1a3 r2 file and its recorded 7ad4593b… pin. The census-tool copy is byte-identical to the C1a4 candidate. The recorded census's tool hashes match those sources. Product HEAD remains e937dac74c8e529fee3efb6f84439d05280e48ea and architecture HEAD 27bb4ec8164aad77aeb11aa1e7b6fa24e9c3c769.

Ran the four expressly permitted model-only scripts with python3 -I -B from product main, supplying explicit product, architecture and packages-root arguments, plus the sealing copy and recorded census where required. **All four reproduce their recorded outputs byte for byte:** term_a_r2.py, option3_r2.py, term_a_discovery_bound.py and captures_term.py. The census itself was not rerun. No T2 cache, store or held-out material was read.

## Round-1 findings

| ID | Status | Basis |
|---|---|---|
| M3CR9-R1-RF-1 | RESOLVED | Snapshot LogicalPath and descriptor bounds replace discovery depth; beyond-256 regression reproduced |
| M3CR9-R1-RF-2 | RESOLVED | As-built member terms and double classification included; adopted nonallocating comparison removes the member term |
| M3CR9-R1-RF-3 | RESOLVED | Eligibility uses an admitted-extent lower bound, separate from enlarged conservative pricing |
| M3CR9-R1-NBO-1 | RESOLVED | Complete sealing source pinned, copied and checked by both new derivation scripts |
| M3CR9-R1-NBO-2 | RESOLVED | Every census margin includes sealing and the leftover-path upper bound |
| M3CR9-R1-NBO-3 | RESOLVED | New-blob branch described as conservative; infeasible 100,000-row example replaced |

**RF-1 / Q1.** The revised argument is sound for the stated bounded row term. LogicalPath supplies 4,096 scalars and 255 per segment, giving at most 585 target segments without importing discovery's depth policy. A row frame is at least 98 bytes plus its UTF-8 path, and the descriptor leaves 4,193,931 bytes for these frames. Thus the componentwise ratio bound D × max(charge/frame) bounds any admitted row collection. Escaping or wider size integers only increase the denominator. The source charge expressions are affine for fixed target count and leaf class; their nonnegative coefficients support the segment/leaf relaxations, and each resulting linear-fractional interval is maximized at an endpoint or the leaf-length breakpoint. All target counts and relevant leaf/marker classes are considered. The model checks reinforce, rather than replace, that source argument.

The regression reproduces a 4,162,373-byte descriptor, 2,453,360,000 classification bytes, 2,464,997,670 row-part bytes and a 2,967,670,057-byte full ledger including the conservative sealing/leftover terms. Its row part fits the corrected adopted row bound of 2,530,317,371 bytes; its full ledger fits the proposed cap. No new snapshot depth exclusion is introduced.

**RF-2.** MAX_MEMBERS=64 and candidate MAX_DEPTH=256 are enforced in workspace_declarations.rs. The as-built variant charges each member list on each classification, including the extra .opensip classification. The census invokes discovery_census.d15_terms over each tree/composed workspace. Its zero-admitted-member result is supported by candidate_failure requiring a .git directory and verified_tree rejecting every .git path component; workspace overlays use the same verified path. The all-mounts-as-members sensitivity is additionally recorded. Under the adopted nonallocating comparison, the member allocation term vanishes rather than being silently assigned to unbounded work.

**RF-3 / Q5.** Pricing without boundaries remains a work upper bound, while exclusion now requires a lower bound on the admitted extent. The discovery-model boundary recording observes the actual subtree decision; removing every marker and every too-deep row only reduces the eligible row set. The reference installation's modeled directories are owned by the invoking user with mode 0755, files mode 0644 and one link, and no extra custody rejection is introduced in that reference premise. This is an explicit reference-population premise, not a claim about arbitrary physical checkouts or unread cache metadata.

All recorded entries have zero admitted members, boundaries and depth-limit directories. The five lower-bound descriptors independently exceed 4 MiB: 40,190,661; 6,489,994; 8,262,274; 4,217,533; and 10,096,694 bytes. The Rust SDK also exceeds the row limit. The narrowest exclusion, Home Assistant, remains 23,229 bytes over after dropping its marker. These exclusions no longer follow merely from an oversized no-boundary superset.

## Adopted remedies and caps

**Q2: the proposed model and code changes agree.** Remedy (a) preserves the anchor scan's charged classification and moves its result into the existing directory level; the later loop skips the second charge and call. Between those two points the only persistent Cargo-root change is the current directory's own push. Every Cargo prefix examined for a target segment in x/.opensip is a strict ancestor of x, so that push cannot change the result. Child traversal restores its own Cargo pushes; member roots remain fixed. The one-.opensip-per-listing argument makes the recorded index compatible with anchor removal.

Remedy (b′) is behavior-preserving when implemented exactly as stated: a nonempty member matches a whole byte prefix followed by '/', and the next complete segment must be .opensip. Empty/root handling, smallest matching segment index and outermost-anchor precedence are retained. This is equivalent to the former segment-prefix equality for the callers' logical paths, including prefix lookalikes and nested members; it requires no list allocation. The unchanged classify_path interface covers the snapshot, discovery walk/scan, workspace, export and host callers. C1a4 still needs to demonstrate that equivalence in its implementation review and obtain M3-B owner's reviewed acceptance of the shared-file change.

The model removes exactly the member terms and reused second classification, while retaining segment, target-prefix and anchor charges. It reproduces all 35 baseline vectors. Under (a)+(b′), only opensip-anchors-root-and-member changes prediction: −12 objects, zero edges, −1,726 bytes. Session predictions and discovery charge predictions remain unchanged; pins and generated artifacts must still be refreshed.

The adopted subtotal is **776,676 objects / 6,218,464 edges / 2,538,872,386 bytes**. Full-ledger census maxima are **529,529 / 1,488,056 / 220,027,344**. Twice the larger component is 1,553,352 / 12,436,928 / 5,077,744,772, so the smallest powers of two are correctly **2^21 / 2^24 / 2^33**. Recomputed minimum census margins are **3,960 / 11,274 / 39,040 per mille**, with no failure among the 39 measured entries. The five over-item-5 entries are excluded only by the proof above. The over-item-5 workspace is not included in the assertion about measured all-mount sensitivities.

These caps are explicitly conditional on C1a4 landing both remedies, with native/model/vector review. As-built memberBounded work needs the larger 2^24 / 2^24 / 2^36 result under the same rule; the smaller caps cannot be applied to it. The declined alternatives are coherently distinguished: larger charged-storage exposure, assigning bounded member costs to refusal, a new walk-wide member structure, or an additional target-prefix optimization. Charged storage is not a peak-RSS measurement.

**Q6.** The remaining directories, non-row names and path-copy work has no item-5 population bound; typed exhaustion beyond the remaining margin is an explicit law choice. The guarantee is conditional on that additional work fitting the margin, not universal admission of every tree whose regular rows fit item 5. The 1,000-row regression plus 263,000 links is a feasible object-cap refusal example. C2's outstanding layout reads remain separately identified.

## Census, discovery finding and blind protocol

The census uses the ordinary integrity-verifying store/workspace path, filters heldOut:false before opening entries and retains the store_path held-out guard. The evidence exposes ids, counts, charges and margins rather than tree contents. Its 44 entries split into 39 measured and five proven over item 5. Independently checked the full-ledger additions and recorded maxima/margin arithmetic. The sealing-plus-leftover addition is 12 objects, 68 edges and 8,406,975 bytes for each entry. No held-out statistic enters cap selection.

**Q4: discovery's member undercharge is real.** At discovery_walk.rs:943, :1036 and :1073 the charge takes only rel, while the corresponding shared-rule calls receive self.members. custody_state constructs a Vec of segments per nonempty member. The walk constructor borrows request.member_roots and adds no member-list charge; the model likewise omits it. Removing those actual allocations through (b′) fixes this particular undercharge without raising discovery's charge constants, predictions or caps. This does not amend M3-B's other policy or resolve its separately recorded pre-walk-capture exposure.

**Q3: the closure consequence is correct.** discovery_rule.rs is pinned whole, and receipt_bindings includes both the closure and discovery tool pin. Updating that row and tool invalidates the discovery receipt even though charge predictions stay constant. The reviewed refresh and C1a4's frozen-cap snapshot validation are distinct obligations. The retained r6 procedure can perform both in one reviewed mechanical run writing both receipts; the record does not authorize using held-out results to choose these caps. Required pre-run and post-run reviews remain. A failure returns the choice to a law successor.

The operative supersession and C1a4 obligations are clear; the locator list can be made more complete as noted below. No constructor, completed C1a4, blind pass or qualification follows from this law acceptance.

## Nonblocking observation

### M3CR9-R2-NBO-1 — Make the supersession and downstream file list exhaustive

RECORD-r9.md:292.

The operative choice and conditional implementation obligations are clear, but section 9 is not a complete locator for every displaced formula or downstream file. C1a/PLAN-r6.md:165 still states the former linear-program bound within the old object/edge caps; the historical changes table at :51 also repeats it. Section 9 lists several displaced r6 passages but omits these. It also mentions that work_ledger.rs has no snapshot profile rather than explicitly listing its forthcoming constructor/constants change, and does not enumerate the refreshed discovery_census.json and receipt artifacts required by the retained C1a4 protocol.

Add the old formal-bound passage to the supersession locators (mark repeated change-table text as history), and explicitly distinguish changed/new implementation files, regenerated census/vector artifacts, and discovery/snapshot receipts. This is documentation completeness: sections 5-6 and the retained r6 gate already make the intended rule and validation obligations unambiguous.

## Boundaries

Only REVIEW.md and review.json in the requested directory were written. Neither repository, worktrees nor control files were edited. No Cargo, rustc, build, lane or shared lane lock, network, other pane or delegation was used. No private 413 fixture, installation directory, signing key, held tree, T2 store/cache or held-out material was read. Only the four explicitly permitted model-only scripts were executed beyond read-only inspection, hashing, JSON parsing and Git queries.

# C2B0-PLAN-r2 review

**Verdict: REQUIRED-FINDINGS — one required finding, three non-blocking observations.**

## Subject and scope

The manifest is 767 bytes, SHA-256 `69965663f63834ffd4a1c69a2fd8308596b800175a9e90576bd77054bbd2f7b7`. All three members match:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `c2b/PLAN-r2.md` | 31494 | `9bf36cadb9b93cee3fea2cf0baf22a6e765f3cdf75e5b588d807dd6b39f53dc2` |
| `c2b/PLAN-r1.md` (history) | 17274 | `e936a273c2ea15f0033045b7035392ac7d0ee6e60bef018b280208c2bffa0ccc` |
| `c2b/C2B-GATING-r1.md` (context) | 5508 | `18e18bec084b0f0fad32404c7fa024e0f50752d337786c0c10302e55c3529b9b` |

The manifest names product `b7538549b727e13013f36d3b7c2e2917e767f3f2` and architecture `7e8f5377373a0b35a3ee15fa8424feb3c3733f59`. The product diff from `3d1d771` was inspected: D2b-0b generation and its binding do not change the cited snapshot, custody, identity canonical parser, native layout schema or evaluator consumer sources.

The review compared r2 with the round-1 findings/rulings, M3-C items 1/3/10, the C1a r6/r9 statements being amended, C1c r4's interfaces, the layout schema and the product consumers. Read-only arithmetic on inert JSON records independently checked the row-size formula; no project code or tests were executed. No Cargo, rustc, build, lane, network, delegation, private fixture, installation, key, held tree or T2 access was used. Only REVIEW.md and review.json were written.

## Required finding

### C2B0PLAN-R2-RF-1: Provide a standalone shared layout check without requiring a native universe

`docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r2.md:136`

LD-C2B0-9 and the agreement control require the layout-only unit to run the evaluator check at native_universe.rs:235-252 before returning. Those lines are inside inspect_typescript_universe; there is no callable layout-only entry point. Its public signature at :142 takes RetainedInputs, a semantic-universe digest, snapshot id and work, and its preceding code admits a TypeScript universe and native context before reaching the layout. C2b-0 explicitly has no context/universe and must integrate without C2a or C2b-1. Calling that function as written therefore adds precisely the dependency this split removes; fabricated unsigned context/universe fixtures would not resolve it.

Required change: Explicitly factor the context-independent realPath/installPath membership check into one bounded shared helper, used by both the existing evaluator consumer and C2b-0 after layout schema/order admission. Include the evaluator helper/export and regression controls in scope, preserving existing refusal semantics at the consumer. Keep retained-context/digest/Plan-selection checks with C2b-1 and later composition, and do not introduce a fake native identity or a second divergent layout predicate.

## Round-1 disposition and requested assessments

| Item | Disposition |
| --- | --- |
| RF-1: pnpm traversal | Resolved. The ancestor search-directory rule now includes the virtual-store parent and `.pnpm/node_modules`, including scoped siblings and workspace ancestor lookup. It never lists `.pnpm` wholesale. Exact visited-set controls are required alongside rows. |
| RF-2: graph state | Resolved at plan level. `searched`, `real_seen` and the installPath map give distinct search/real/row identities; identical repeats reuse, conflicting observations refuse Inconsistent, aliases remain distinct, and package cycles terminate. The shared-target, diamond and A→B→A controls cover the former gap. |
| RF-3: exclusions and reach | Resolved at plan level. C2b-0 owns a no-follow directory reach and a full-path non-dependency exclusion predicate. Workspace targets retain S3/Walk custody; dependency paths use descriptor discipline below the anchor. Extent, VCS, Cargo and exact custody-anchor exclusions remain before opens/reads. C1c's eligibility API and discovery classification semantics remain distinct. |
| RF-4: receipt interval | Resolved. Joining stops at the final-input freeze; otherwise C2b-0 owns a fresh reviewed interval. Baselines, cumulative receipt-specific deltas, pre/post review and a frozen-input refresh are explicit. Discovery and snapshot receipts both change, for different reasons. Passing generated-output checks is separate from freshness. |
| NBO-1: parser profile | Substantively resolved. The exact profile and typed variant are selected, including rejection of unrelated float fields without mislabelling them malformed JSON. See NBO-2 for two omitted control cases. |
| NBO-2: record bounds | Substantively resolved. The 100,000-row predicate is isolated from whole-record admission; 4 MiB encoding failure is typed Encoding and the model covers construction/encoding. The claimed attained maximum needs the qualification in NBO-1. |
| Q4: refused capture set | Resolved as a composition obligation. Returning exact captures, no partial layout, no deletion/concealment and no session/ledger reset preserves the boundary. C4a/J2 still must define a lawful no-layout dependency disposition; the library does not claim that fallback is implemented. |
| Q5: ledger routing | Reconciled explicitly by A-C2B0-1. The full layout term, anchors, vectors and cumulative fixed-cap 2× derivation are required before implementing-unit acceptance. An earlier receipt or model cannot stand in for the revised recipe. |

The four-statement A-C2B0-1 amendment is coherent in substance: B2 remains discovery-ledger work, C2 layout work moves after the walk onto the session's snapshot ledger, and r9's caps stay fixed. Item 1 enumerates the session's reads without mandating layout-before-walk order. The layout term must include reach, listings/status/link reads, graph bookkeeping, capture/parse, sorting/schema checks, retained output and encoding, with reused captures charged once and additional operations still charged. A failed fixed-cap derivation stops for a reviewed law revision.

**The combined plan/amendment package is not accepted by this verdict.** The required finding concerns the layout-only agreement interface, not rejection of the proposed ledger/order amendment on its merits. No accepted C1a/r9 text or repository was changed by this review.

The absent/empty policy is sound: no eligible existing search directory gives None; an observed eligible empty directory gives Some([]), with a non-null layout digest when selected; a wholly excluded directory cannot authorize a layout. None is not a successful partial layout or a recovery from Budget. Existing Q1's manifest-free-package subset, Q2's escaping-link refusal and Q3's explicit manifest-profile subset remain intact.

## Q6 and Q7 rulings

**Q6: The after-walk order is lawful with the stated amendment and observation duties.** It supplies same-session WalkEvidence and retained first-party manifests without borrowing another discovery derivation. The layout-capture/change/read-set-reach control replaces the former layout-before-walk timing for pruned manifests. First-party walk-capture/change/layout-reuse is the corresponding observation point for workspace targets. Neither uses a second source read. LD11's required first-party refusal must use a file observation, as NBO-3 explains. B2's original before-walk control remains unchanged, and successful layout dependencies must still be inventoried before sealing; an exclusion does not turn a leftover into an authorized row.

**Q7: A session-owned parse handoff is appropriate.** It keeps parsing attached to the exact custody bytes whose raw digest the capture holds and prevents reopening the project file. Keep the helper internal and bounded, with parsing/allocation charged before use and the capture unchanged on parser failure. The layout module can own the product-profile field projection while the session owns verified-byte access; a bounded borrowed/callback handoff would also be lawful. No general raw-project-path parser or unbounded retained-byte copy is authorized. Repeated aliases may reuse parsed results under the ledger, but never bypass observation consistency or substitute newly read source bytes.

## Non-blocking observations

### C2B0PLAN-R2-NBO-1: Describe 26,715 as a loose byte upper bound, not an attainable maximum

`docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r2.md:131`

The arithmetic is correct for an abstract minimum row: 152 fixed bytes plus four one-byte string payloads gives 156 bytes, and N nonempty rows encode in 31 + 157*N bytes. N=26,715 gives 4,194,286; N=26,716 gives 4,194,443. But 26,715 distinct installPath values cannot all be one-byte paths, and emitted installed-package paths also have structural prefixes. Unique installPath admission therefore prevents the claimed attainment. Unicode and JSON escaping further increase byte costs. This does not invalidate the conservative upper bound or the Encoding refusal.

Suggested change: Call 26,715 a conservative ceiling from per-row minimum encoding size. Remove the claim that it is reached, and use actual unique, schema-valid layouts for the complete-record byte boundary controls. State the arithmetic in terms of encoded string payload lengths, including escapes and UTF-8, rather than raw character counts.

### C2B0PLAN-R2-NBO-2: Complete the promised parser-variant controls

`docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r2.md:204`

The selected canonical::parse profile and Manifest(Profile(variant)) are correctly specified. However, the seven listed cases do not cover all nine parser variants: InvalidUnicode (for example an unpaired escaped surrogate) and InvalidJson are separate from InvalidUtf8 and are missing from the stated one-case-per-variant controls.

Suggested change: Add distinct InvalidUnicode and InvalidJson vectors while preserving the explicit valid-general-JSON subset refusals. A malformed JSON case may be identified as such; a valid JSON float elsewhere must retain FloatForbidden rather than being described as malformed.

### C2B0PLAN-R2-NBO-3: Make the replacement C1-T24 observations explicit in the implementation controls

`docs/implementation/m3/snapshot-plan-c/c2b/PLAN-r2.md:148`

The post-walk ordering is compatible with item 1, but its promised first-party rewrite refusal needs a new charged observation. Existing CaptureSession::capture returns a kept capture without re-observation (snapshot.rs:204-220), and parse_captured is described as reading custody bytes. Reaching a directory alone does not detect an in-place rewrite of its package.json. C1c-1 also keeps first-party captures as Walk rows rather than turning them into ReadSet rows. LD11 already requires the refusal; it should be backed by explicit controls and the intended observation handoff.

Suggested change: Add separate rewrite controls for a pruned manifest changed between layout capture and read-set reach, and a first-party workspace manifest changed between walk capture and layout reuse. Specify charged fstatat(AT_SYMLINK_NOFOLLOW) through the held enumerating parent, compare the complete stored observation, and refuse without a second source read. Do not interpret ordinary cached-byte reuse or directory metadata as the required file observation.


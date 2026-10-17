# C2B0-PLAN-r3 review

**Verdict: ACCEPT.** No required findings or non-blocking observations. This accepts the implementation plan and its explicitly proposed amendment **A-C2B0-1**; it does not accept implementation code, a model derivation, refreshed receipts or production composition.

## Subject and verification

The manifest is 956 bytes, SHA-256 `9fa287f4c070d3c6415597c582feb6a2ba247a4968ecb33850f70ce82c094a5d`. All four members match:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `c2b/PLAN-r3.md` | 39652 | `1392af25896e55c42034e1f390833039df395f23f7e6e97f982fd2d77bfaa709` |
| `c2b/PLAN-r2.md` (history) | 31494 | `9bf36cadb9b93cee3fea2cf0baf22a6e765f3cdf75e5b588d807dd6b39f53dc2` |
| `c2b/PLAN-r1.md` (history) | 17274 | `e936a273c2ea15f0033045b7035392ac7d0ee6e60bef018b280208c2bffa0ccc` |
| `c2b/C2B-GATING-r1.md` (context) | 5508 | `18e18bec084b0f0fad32404c7fa024e0f50752d337786c0c10302e55c3529b9b` |

The bases remain product `b7538549b727e13013f36d3b7c2e2917e767f3f2` and architecture `7e8f5377373a0b35a3ee15fa8424feb3c3733f59`. The r2-to-r3 document diff was inspected. Seven relevant evaluator/identity/census/model sources were compared byte-for-byte with the product base and match.

This was a read-only plan/source review, including independent arithmetic on inert JSON values. No builds, Cargo, rustc, tests, lanes, network, delegation, installation/private fixtures, signing keys, held trees or T2 data were accessed. Only REVIEW.md and review.json were written.

## Round-2 disposition

**R2-RF-1 is resolved.** LD9/LD14 now explicitly scope one exported evaluator helper, `layout_real_path_faults`, and make both the layout producer and existing TypeScript-universe consumer call it after schema/order admission. The helper operates on the admitted layout alone. It does not require a native context, universe, snapshot identity or C2a closure, and no fabricated identity or duplicate predicate is proposed. Retained-record lookup, digest association, missing-layout handling and later Plan/context checks stay with their existing owners.

The membership predicate matches the existing inline code: form the installPath set, and report a realPath only when it differs from its row's installPath and is absent from that set. The fault text remains exactly `native.universe-retained-input-mismatch:nodeModulesLayout.realPath:<realPath>`. Inserting the helper's results into the consumer's existing BTreeSet preserves deduplication and ascending refusal order, including multiple orphan rows naming one missing target. The separate missing-layout fault remains in place.

The proposed entry-count check before helper allocation gives a bounded standalone call and a typed `LayoutBound`. Passing the row count from C2b-0 is legitimate because schema admission and the snapshot WorkScope charge precede the call. Passing the existing `work` bound from the consumer is compatible with its current development-budget convention: the retained nested layout first passes `inspect_current_record` with that work bound for both traversal and descriptor/schema work. Those existing traversals already visit the layout's entries. The helper does not replace or replenish those budgets. Existing low-budget failures and the promised byte-identical consumer regressions remain implementation checks, alongside the direct helper bound control.

**R2-NBO-1 is resolved.** The minimum row encoding is 152 fixed bytes plus four encoded string payloads, hence at least 156 bytes. Including record framing and commas gives at least `31 + 157*N` bytes for nonempty layouts. The stated values, 4,194,286 at 26,715 rows and 4,194,443 at 26,716, are correct. R3 now explicitly calls 26,715 a conservative unattainable ceiling, accounts for UTF-8/escaping, and requires actual unique schema-valid records for the encoder-boundary controls. The isolated 100,000/100,001 count predicate is no longer confused with whole-record admission.

**R2-NBO-2 is resolved.** Controls now cover all nine canonical parser variants, including separate InvalidUnicode and InvalidJson cases. A valid JSON float retains FloatForbidden; unsupported profile values are not generally relabelled malformed JSON. The 4 MiB parser and encoder limits keep their distinct typed ownership.

**R2-NBO-3 is resolved.** First-party reuse and later alias meetings explicitly require a charged no-follow file status observation through the held parent, compared with the complete capture observation. Directory metadata and cached-byte reuse cannot substitute for this check. The in-place rewrite controls require Changed without another source read. The layout-capture/read-set-reach rewrite remains C1c-1's ChangedSinceCapture control and is carried in the C2b lane when that interface exists. No dependency cycle is introduced by requiring C1c-1 to precede its layout producer.

## Census, amendment and prior rulings

The current discovery census, snapshot model and snapshot census tool contain no evaluator source pin. Thus extracting the helper alone does not change their current evaluator-file bindings. This is not a claim that the complete C2b-0 unit leaves either receipt current: excluded_path changes the discovery closure, and the layout term, vectors and new source change the companion recipe/pins. LD7's exact receipt deltas and cumulative freshness interval still apply. The stated companion-receipt caveat covers any evaluator binding introduced by its defining refresh or the final model inputs; the implementing lane must inspect those final public bindings rather than infer an empty delta from today's tool list.

**A-C2B0-1 is accepted as proposed.** Its four replacements reconcile the C1a r6/r9 statements for C2 layout reads only: B2 remains pre-walk discovery-ledger work; C2 layout reads run after the walk on the same session's snapshot ledger; r9's caps remain unchanged. The full layout/helper/capture/parse/graph/record cost term, soundness vectors, aggregate ledger derivation and fixed-cap 2× evidence remain required before implementing-unit acceptance. Failure of that derivation requires a law-record revision, not an increased cap or a fresh ledger that erases spent work.

**Q6 remains resolved:** walk, layout, read set, sealing is lawful with the replacement file-observation controls. B2's original before-walk control stays intact. Boundaries, ignorePaths, VCS/Cargo exclusions and exact custody anchors still apply before opens and reads; an excluded capture cannot become an authorized inventory row.

**Q7 remains resolved:** use the session-owned internal bounded parse handoff over exact custody bytes. Charge parsing/allocations before use, preserve the capture on failure, and permit bounded parsed-result reuse for aliases without skipping their file observations. No raw-project-path parser, second source read or unbounded byte copy is selected.

## No regression and remaining implementation gates

R3 preserves the earlier fixes: project-bounded ancestor node_modules searches including pnpm virtual-store siblings and `.pnpm/node_modules`; no wholesale store scan; charged visited sets and installPath row merging; distinct aliases and terminating dependency cycles; safe directory reach separated from non-dependency exclusions; first-party Walk custody; per-receipt frozen refresh intervals; exact capture sets on refusal; no partial layout or silent Budget success; and the absent-versus-observed-empty layout policy.

The layout remains a library unit integrating after C1c-0 and unblocking C1c-1. C2b-1, the suffix-table owner, successful native context/universe/Plan composition and the no-layout fallback's dependency disposition remain with their named owners. The helper/export, evaluator regression controls, model pricing and receipt work are commitments for the implementing review, not results established by this plan review. No qualification or reference-derived layout oracle is claimed.

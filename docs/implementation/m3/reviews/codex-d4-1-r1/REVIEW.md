# D4-1-r1 review

**Verdict: REQUIRED-FINDINGS.** One required validation finding; no non-blocking observations. The inspected admission logic and accounting amounts are consistent with the accepted plan, but the submitted controls do not establish its before-work requirement or catch its expressly planned charge-after-comparison mutation.

## Subject verification

Independently verified the 9,803-byte manifest, SHA-256 `5b80d96dbaba2d2e4c949828e5adda6ec36603c21d014cdae8c06d1a9a199eb6`, and all 43 member lengths and hashes. All match. Verified all three product-map candidate/archive entries and the existing lib.rs parent at the specified product base `ae141a389b21997fb654f372a06c22cbeb2cc9d5`. The worktree HEAD and changed/new path set match the request exactly.

Verified source.json's product-lock pin and all five authority pins, including the accepted D4 plan review and lead assent. Read the complete production module, controls, closed-world pins, mutation definitions/outcomes and integration/inventory preparation scripts. The scripts were inspected only, not executed. Read the base through Git where relevant rather than treating moving main as the review base.

Executed only the two permitted live project checks. Operability source returns passed, 114 rows and no findings. verify_design returns passed, inventory v227 and productQualification false. Neither result is implementation-test or product-qualification evidence.

## Required finding

### D41-R1-RF-1 — Verify that exhaustion precedes work, not only that it preserves the ledger prefix (P2)

**Location:** `crates/components/src/manifest_tests.rs:494`.

The independent model and per-site accounting loops compare totals and WorkLedger::used, but do not record allocations, comparisons or pushes actually performed. A comparison moved before compare(work)? has the same successful total and the same used prefix when the subsequent charge refuses; the extra unfunded comparison is invisible to these tests. The submitted 20 mutations remove charges or change prices, but omit the accepted plan's explicit mutation of a probe charged after its comparison. No production-source charge-order guard is present either. Thus the submitted controls establish charge amounts/prefixes but not the plan's required before-work property, despite SCOPE's claim that the per-site tests establish it.

**Required change:** Add an operation-order oracle for the production allocation/comparison/fill sites, or a complete reviewed source-order guard in the style of the existing kernel controls, alongside the independent accounting model. Require exhaustion before the corresponding work, including both predicate passes and policy probes/order checks. Add the planned probe-charge-after-comparison mutation and an allocation-before-charge mutation; both must fail assertions without relying on compile failure. Retain the current exact-total and prefix tests, and describe precisely what each control proves.

**Validation:** A mutant that stores slice[mid].borrow().cmp(key) before compare(work)? and matches on the stored result afterward must be caught. Likewise catch allocating a result/index buffer before its refused charge. On the unmutated candidate, per-site short allowances must show no operation at or past the refused site, not merely no further ledger debit. Supply the corresponding successful controls and mutation evidence through the authorized implementation lane.

The independent model is useful: it computes sizes and counts from input rather than calling the production cost functions. Its totals and one-unit-short prefix assertions catch removed/underpriced charges. They cannot by themselves distinguish work-then-charge from charge-then-work. The charge-after-comparison counterexample above is a static control-gap analysis; I did not edit the worktree or run a mutation during this review. The accepted plan explicitly requires that mutation and an assertion that the refused site's work does not occur.

## Implementation assessment

ManifestClaims and its nested command/capability/release-provenance values are borrowed projections. Components introduces no manifest parser or security dependency. Public construction of these data projections does not establish authenticated provenance: D4-2 still must obtain the host projection from the ordinary reader's authenticated release association, as the plan requires.

AdmissionPolicy keeps its three slices private and validates strict ascending uniqueness with charged adjacent comparisons. EE-1 checks explicitly-trusted against the explicit-trust slice; first-party classification remains an input of the authenticated association, not derived from a namespace spelling. EE-3b probes relation/rung pairs, returns one form for the class at its first unmatched capability and does not treat a command tree as capability authority. The matrix test/input vocabulary contains the intended nine pairs; the host's authoritative pinned static projection remains D4-2's implementation duty.

EE-5a follows (a), (b), (c): any commands member on a closure-only role refuses, including an empty tree; an analyzer must have exactly one parentless name-bound root; reserved-name probes cover its name, manifest aliases and root aliases. An analyzer's lawful mounted root passes. Live-name collisions are not reclassified by this module. EE-4 has no invented predicate or artificial carrier.

ExcludedFormClass has the six documented members with the manifest-relative class order preserved. The per-manifest judge returns one form per represented class, retaining an internal arm key without inventing public codes. The same judge serves count and fill, so the predicates and short-circuit behavior have identical charges on those two passes.

admit converts the claim count to u32 before any charge, funds its two exact-capacity index buffers, merge-sorts digest indices, rejects repeated digests after charged adjacent comparisons, and then allocates either the exact refusal vector or the sorted Cleared digest list. No hidden sort scratch is present. Empty/singleton behavior is explicit in the implementation and controls. Cleared is opaque/non-Clone and authorizes nothing by itself; the host wiring still owes the exact authenticated-set join before C2a.

Allocation cost products saturate rather than wrap. At the selected platform ledger limits a saturated size is refused by the checked charge before allocation. This does not add a profile or cap. The actual accepted-size loops are bounded by funded capacities and u32 indexing; no new unbounded input-processing allocation was found. The implementation's direct allocation/comparison sites place their charges before the substantive work on inspection. RF-1 concerns the missing executable regression evidence for that ordering, not a claim that those visible calls currently reverse it.

## Closed-world and functional controls

The schema pin checks the top-level and provenance property sets; five capability branches and their declarationData fields; platform; the three entry branches; command; and dependency fields. Exhaustive patterns pin ManifestClaims and nested projected fields. The six-class exhaustive match and order assertion pin the excluded-form vocabulary. These are closed-world safeguards, not an executed EE-4 negative or DR-G29 completion.

The fifteen focused tests cover all roles, EE-5a arms and aliases, listed/unlisted explicit trust, allowed and fact/outside relation pairs, digest/class ordering, sorted Cleared/empty input, duplicate digests, unordered/empty policies, independent accounting/reference bounds and schema/type pins. Their accounting reference uses its own index sort/search and type-derived result sizes, rather than reusing production price functions. It still needs RF-1's separate work-order oracle.

All 20 submitted mutation logs contain actual failing tests and no compile-failure substitution. They cover the described semantic weakenings, removed charges, underpriced vector and class/order/policy defects. This valid 20-of-20 result does not cover the omitted planned ordering mutant; removing a charge is a different weakening from moving it after work. The planned count-pass/growing-vector mutation should likewise be retained in the implementation owner's complete coverage map when extending the controls.

## Lane evidence and integration boundary

The recorded components suite increases from 73 to 88 passing tests, with the same 54 supervisor failures on base and candidate. The logs contain the expected missing lane-built supervisor-fixture-path failure; D4-1 changes no supervisor file. This is equal-failure-set evidence, not an all-green components suite. The new manifest tests pass in the focused run.

Recorded rustfmt is clean on lib.rs and both new files. Warning-denied all-targets Clippy, workspace check, components release build, focused tests, environment exceptions, source census, census-closure check and verify_design report success. These are inspected lane artifacts; no compiler, tests or lane was run here. The production changes introduce no environment read, let-underscore discard or new mint-census call.

The integration script checks review/subject identity and exact candidate bytes, rejects main changes overlapping its three paths since the lane base, checks parent bytes and absence of new paths on main, advances the isolated worktree only over disjoint changes, and stages only its three product paths. Architecture publication scopes its staged/remaining-untracked checks to this unit, allowing unrelated untracked work. No integration, assent or publication was performed by this review.

The preparation script distinguishes realization of planned manifest.rs from addition of manifest_tests.rs and preserves inherited rows; lib.rs's inherited description remains generic. The separately reviewed inventory successor remains owed after integration. Neither inventory preparation nor its generated request is acceptance evidence now.

D4-2's authenticated host adapter, D4-T1/J-C10b's durable/first-use/ephemeral path half, public projection/records, SD-9 production profile gates and product qualification remain outside this unit. No production caller is added.

Only REVIEW.md and review.json were written in the requested directory. Neither repository, worktree nor control file was edited. No Cargo, rustc, build, tests, lane, network, prohibited private fixture/key/installation material, held tree or entry, T2 store/overlay/cache, other pane or delegation was used.

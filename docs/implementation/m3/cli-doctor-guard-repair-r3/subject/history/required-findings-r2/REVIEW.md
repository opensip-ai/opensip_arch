# CODEX2 review — CLI doctor guard repair r2

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### DOCTOR-GUARD-R2-RF-1 — Bind each accepted source exception to its owning path

The source fence still selects some exceptions by text alone rather than by the exact accepted file site. `strip_known_test_tail` accepts any member of `KNOWN_TEST_TAILS` for every source passed to it. Both `production_source` and `production_feature_sites_are_closed` call it without a path or an expected-tail identity. As a result, an exact accepted `outcomes.rs`, `doctor_ingress.rs`, or `request.rs` test tail copied to any other scanned CLI or host source is removed before the `cfg(test)`, `#`, attribute, and forbidden-token checks. The copied gate therefore passes even though that site was never accepted.

The controls do not close this case. `production_projection_excludes_only_the_exact_logging_test_module` deliberately treats all three tails as accepted with the same pathless `outcomes = false` argument. The `foreign-path-exception` mutant covers only the middle `logging_tests` exception, while `blind-tail-truncation` proves that production after a tail remains visible; neither checks that each exact tail is allowed only at its original path. The analogous `KNOWN_CLI_MAIN_SOURCE` fast path is also keyed only by text and the `outcomes` boolean, rather than `apps/cli/src/main.rs`.

Make source admission path-aware. Map each removable EOF tail to its exact owning file, bind the full-main-source exception to `apps/cli/src/main.rs`, and refuse those same bytes at every other scanned path. Add pure swap/copy controls across the scanned path identities and a separately compiled runtime weakening that removes this path binding, followed by exact restoration and a fresh positive run.

## DOCTOR-GUARD-R1-RF-1 disposition

R2 substantively fixes the R1 metadata defects. The eight selected packages have closed feature maps and exact manifest and bin/library source roots. Forwarding aliases are normalized and joined through unique resolve edges to the intended selected package IDs, and the normal declaration kind and target must occur in the resolved edge's `dep_kinds`. The full metadata traversal refuses guarded forwarding through a foreign intermediate and refuses ordinary or build direct activation of the six guarded features, while the existing development fixture activations remain admitted. Missing, ambiguous, retargeted, default, and changed selected maps are refused.

The lexical mask and token fence also close the R1 alternate-feature-spelling cases: strings, raw strings, characters, and nested comments cannot create false source authority; `cfg`, `cfg_attr`, expression macros, spaced forms, unknown attributes, module/import/macro definitions, qualified macros, Unicode macro names, and non-bare `env!` forms remain visible and fail. The accepted middle logging block is still tied to `outcomes.rs`, its exact complete prefix, unique bytes, and surrounding production.

However, R1 required lawful source uses to be constrained to exact accepted sites. The pathless tail and main exceptions leave that predicate incomplete, so DOCTOR-GUARD-R1-RF-1 is not fully closed by this subject.

## Authority ruling

No new design selection is required. Accepted X10 r4, O1 r2, S-OP-2 r6, and S-OP-2b already identify the permitted doctor boundary, opt-in feature graph, test-only features, and absence from ordinary/default/release paths. DOCTOR-GUARD-R2-RF-1 is an implementation and control correction under those authorities.

## Frozen subject and remaining assessment

The requested `subject.json` SHA-256 is exact: `969248f6be6b849dc06428716cda2335f2f20d5dfa508fa7d83c9ad88e091a1e`. All 362 declared subject members are present and unique, every byte count and SHA-256 matches, and there are no undeclared frozen members. The product and architecture heads match the requested parents. The candidate worktree has only `apps/cli/tests/doctor_tests.rs` modified, and that file is byte-identical to the frozen 65,771-byte product member and product map.

The original three doctor binary tests remain intact. The source projection continues to remove only the exact unique accepted middle logging module after the pinned prefix and preserves production before and after it. The current locked offline metadata is pinned, and the inspected feature declarations, target roots, forwarding edges, and four existing guarded development activations agree with the selected graph.

Owning r7 accurately records seven doctor tests and warning-denied CLI all-target Clippy passing. Its 11 mutations were fresh compiled artifacts, failed at their stated runtime witnesses, restored the exact candidate source, and were each followed by a fresh seven-test positive. Post-base r2 preserves the same candidate bytes and records the seven tests and Clippy passing at the current parent. The earlier r4 literal false positive, r5 malformed fixture, and r6 Clippy failure are preserved and are not counted as runtime kills.

This one-path test-only subject changes no production file, dependency, or inventory. The separate platform descriptor repair remains unaccepted, and the inherited broad workspace failures are not waived. No integration, status reconciliation, release qualification, or product qualification follows from this review.

## Non-blocking observations

None.

# D4-1-r2 review

**REQUIRED-FINDINGS.** D41-R1-RF-1 is substantially addressed, but remains open for eager boolean predicate evaluation. One required finding; no non-blocking observations.

## Subject and verification

The 11,810-byte manifest hashes to `b37bdf11cbbfbbc57162d8892e15cf8dbe789f57df4892636e1eebab168096bf`. All 51 members rehash exactly. The three product-map candidate/archive entries and their parent states match, with manifest.rs and manifest_tests.rs new. The candidate HEAD is `2ead5cf1796bb85f363c34fa8ff8fba715462369`, and the changed set is exactly the three mapped paths. Authority pins, the product design lock and the round-1 subject pin match. All 43 historical round-1 package members still match their manifest.

Both permitted live checks passed: operability source reports 114 rows and no findings; verify_design reports passed=true, inventory v228 selected and productQualification=false. No Cargo, rustc, builds, tests or lanes were run by this reviewer. All other work was read-only reading, hashing, JSON parsing or Git queries. No network, other panes, delegation or prohibited private/store material was used. Only this directory's REVIEW.md and review.json were written; neither repository, worktree nor control file was edited.

## Required finding

### D41-R2-RF-1 (P2): Observe the boolean predicate evaluation, not only tested() receiving its result

Location: `crates/components/src/manifest.rs:321-324, 417-420, 450-470; crates/components/src/manifest_tests.rs:685-712`.

The ordered/reserve wrappers and their mutations fix the named probe and allocation counterexamples. The boolean-predicate part of D41-R1-RF-1 remains incomplete: tested(outcome: bool) receives an already-evaluated result and records Compared afterward. A predicate can be computed before compare(work) and then passed to tested after the charge. If that charge refuses, the predicate already ran but no Compared entry is emitted. The new source guard counts work.charge, Vec::with_capacity, .cmp and pushes; it does not constrain these boolean predicate computations or their order. Thus its token counts and the oracle/model prefixes are unchanged by this counterexample, including in both judge passes. This is a remaining acceptance-control gap; the submitted candidate itself currently places the charges before these evaluations.

A concrete counterexample is:

```rust
let explicitly_trusted = claim.provenance.source_class == SourceClass::ExplicitlyTrusted;
compare(work)?;
if tested(explicitly_trusted)
    && !probe(policy.explicitly_trusted, claim.provenance.publisher, work)?
{
    found(form(ExcludedFormClass::Ee1, Arm::UnlistedPublisher));
}
```

The boolean is computed before the potentially refused charge. Successful results and both recorded sequences remain identical; on exhaustion, tested is never reached, so the oracle misses the extra work. I constructed this replacement only as an in-memory source string and verified that every source-guard token count remains unchanged. I did not mutate the worktree or execute the hypothetical mutant. Its indistinguishable oracle trace follows from tested's eager argument and the control flow.

Required: Make boolean predicate evaluation itself occur in an observed site, or add complete reviewed source-order guards for the actual predicate expressions and their charges. A lazy predicate helper can bring the operation into the wrapper, but also guard against precomputing and passing a captured boolean. Add a mutation that precomputes the predicate before compare while leaving tested after it; it must fail an assertion rather than compilation. Retain the current exact totals, per-site prefixes, ordered-comparison oracle, allocation controls and all passing mutations.

Validation: Supply authorized-lane evidence that this stored-result-before-charge mutation is caught, with no predicate evaluation at or past a refused site. No new price, predicate, projection or production behavior is requested.

## Round-1 disposition and regression assessment

The explicitly requested probe counterexample is now covered: ordered records the actual comparison site, so computing ordered(slice[mid].borrow(), key) before compare emits an operation before its charge. The supplied mutation produces assertion failures in the accounting controls. Policy and duplicate comparisons use the same observed wrapper and have their own before-charge mutations.

The allocation counterexamples are also covered: reserve records allocation before Vec::with_capacity, blocks requires the preceding accepted charge, and the per-site short allowances compare both the ledger prefix and complete operation blocks with the independent model prefix. The three allocation-before-charge mutations fail tests. Exact result capacities and the grown-vector mutation address hidden result-vector growth. These improvements resolve the specific probe/allocation examples from round 1. The remaining boolean gap is the finding above.

The production comparison with r1 preserves the accepted predicates, their class/arm ordering, borrowed projection, policy and prices. EE-1 remains tied to release provenance and the explicit-trust list; EE-3b to relation/rung membership; EE-5a retains all three arms. Sorting, adjacent duplicate rejection, count/fill passes, exact refusal allocation and opaque sorted Cleared remain unchanged in meaning. No EE-4 carrier or admission authority is invented. Production note is a no-op; the thread-local log exists only under cfg(test). No new dependency, environment read, let-underscore assignment or mint-census call is introduced. Existing closed-world schema and claim-type pins remain in the focused controls.

## Lane evidence

The archived r2b lane has all twelve checks passing. Components reports 73→90 passing tests, with exactly the same 54 failure names on base and candidate and seventeen focused manifest tests passing. The shared failures are the disclosed supervisor fixture-path environment failures; this is not a claim that the whole components suite passed. Formatting reports lib.rs base/candidate clean and both new files candidate clean. Clippy, workspace all-targets check, release build, focused tests, environment exceptions, source census, closure check and verify_design pass in the archived evidence.

I checked every one of the 28 mutation logs: each contains runtime test failures, with nonempty failing-test lists and no compile-failure result. In particular, the named probe, policy, duplicate, whole-tested-call and allocation reorderings are caught. The whole-tested-call mutation moves the log with the predicate; it does not exercise the stored-boolean counterexample above. The earlier r2 attempt's stray-doc-comment Clippy failure is disclosed history outside the subject; r2b is the full rerun of record. No lane was rerun for this review.

## Integration path

I inspected integrate_d4_1_r2.py and prepare_d4_1_inventory.py without executing them. The integration script requires ACCEPT-UNIT, no required findings and the exact reviewed subject hash, rehashes all subject members and product candidates, checks disjoint movement since the lane base, stages only the three reviewed product paths, fast-forwards main and runs fresh verify_design. Its architecture record is round 2 and carries round-1 history. The assessment prose still says r1 in its opening phrase, while its identifiers and pins select r2; that label should be corrected when preparing the eventual assent.

The inventory preparation derives its version and successor counts from main's live lock, requires the accepted integrated unit, checks the exact mapped bytes, realizes manifest.rs's inherited planned row and adds only manifest_tests.rs, preserving inherited rows by value. That inventory remains a separate successor and review. The present REQUIRED-FINDINGS verdict does not authorize integration, publication, inventory binding or qualification.

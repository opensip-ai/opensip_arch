# CODEX2 Review — D2b3c FA-2 Owner Source Preflight r1

## Verdict

**PREFLIGHT-CLEAR**

No required findings or non-blocking observations.

This verdict is limited to the frozen two-file source preflight identified by subject-manifest SHA-256 `972f9ceec0a26438b8ec685e501b70d6920621e0258ac7a53862c968641f7813`. It does not accept D2b3c as a unit, the other eleven draft paths, the still-running complete owning lane, mutation evidence, inventory, integration, status publication, or product qualification.

## Authority ruling

The accepted FA-2 and D2b plan r3/A2 authorities are sufficient for this exact implementation. FA-2 already makes the symbol-census `LogicalPath` a schema-enforced protocol field and gives it the same logical-path constraint as the previously selected owner form. D2b-3c already owns FA-2 census admission, malformed-census refusal, and trial-07 replay. Reusing the existing ECMA-native dot-segment predicate for that document's already published exact keyword implements those obligations; it does not select a new schema language, regex form, generic matcher policy, or fourth native-owner profile.

No further design selection is required for the reviewed branch. Any later change that broadens the census owner to additional patterns, changes the shared matcher, or applies this behavior to another schema owner would fall outside this authority and require its own selection and review.

## Scope ruling

- The candidate changes exactly `crates/identity/src/schema.rs` and `crates/identity/src/schema_tests.rs`. The production change is one branch in `Program::pattern_matches`, gated by registered-native-owner compilation, the actual resolved owner `opensip.product.symbol-census.1`, and the exact existing pattern `(^|/)\.\.?(/|$)`. It delegates to the already accepted native predicate.
- `RegisteredSchemas::from_sources` verifies the complete 52-source set, including every document's length, SHA-256, and `$id`, before compiling with the registered-owner flag. Generic `Program::compile` does not enable the branch. External references pass the resolved target document identity into pattern evaluation, so a foreign-to-census reference selects the branch and a census-to-foreign reference returns to inherited behavior.
- The other six symbol-census pattern forms remain on the inherited matcher. `patternProperties` continues to call the inherited matcher directly. Generic programs, foreign owners, nonmatching census keywords, all shared 72 forms, and the accepted three-owner/26-form native profile are unchanged.
- The registry, 52 source pins, 15 aliases, raw symbol-census source, source map, carrier, shared pattern implementation, and TypeScript sources are byte-exact. The candidate adds no source, alias, entry point, source-39 admission, caller, cost, population, or disclosure change.
- The three added controls cover twelve line/dot inputs across registered, generic, and foreign programs; both directions of external-reference owner transfer; other census patterns; and `patternProperties` isolation. The archived pre-change actual-path replay fails at the final-LF dot-segment case. The exact candidate is pinned by the archived fresh evidence recording 81 identity tests, one accepted-native startup control, and the formerly blocked actual path replay as passing. I did not rerun any build, test, or lane.

## Binding-drift ruling

I independently ran only the permitted pure `--bindings` computation with the pinned Python and the declared worktree, architecture, and product roots. Both computed public binding objects equal the current discovery and companion receipt bindings. No receipt-binding drift is introduced by these two identity-source edits, and no mode or blind census was invoked.

## Package integrity and remaining boundary

All ten manifest members, all six authority pins, all invariant pins, all eleven context-source pins, and both actual candidate files match their declared byte counts and SHA-256 values. The frozen stage contains no undeclared member. The accepted status-only architecture publication changed the architecture head after preparation but left every pinned authority and input byte unchanged.

The remaining eleven D2b3c paths are context only and remain unaccepted. Complete owning evidence, mutations, full unit review, inventory and bindings, integration, status reconciliation, and qualification remain required separately.

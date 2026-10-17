# D4-1-r3 review

**ACCEPT-UNIT.** No required findings; one non-blocking integration-record correction. D41-R2-RF-1 and the underlying D41-R1-RF-1 are resolved for this pinned unit.

## Subject and boundaries

The 12,736-byte manifest hashes to `fee39eead3461350b4a4bb9e3e1fd59ee228214858cb5c83059cce26bf1dbd8a`. All 55 members rehash exactly. The three product-map candidates and archived copies match; lib.rs matches its base parent, and the two manifest files are absent at the base. The candidate is detached at `2ead5cf1796bb85f363c34fa8ff8fba715462369`, with exactly the three mapped changed paths. All authority, design-lock and prior-subject pins match. Both historical packages still match their complete subject manifests.

Both permitted live checks passed: operability source reports 114 rows with no findings; verify_design reports passed=true, inventory v228 selected and productQualification=false. No Cargo, rustc, builds, tests or lanes were run by this reviewer. Other review work was read-only reading, hashing, JSON parsing and Git queries. No network, other pane, delegation or prohibited private/store material was used. Only REVIEW.md and review.json in this directory were written; neither repository, worktree nor control file was edited.

## Findings disposition

`tested` now accepts `impl FnOnce() -> bool`, records Compared, and invokes the predicate inside the observed wrapper. The four claim predicates therefore evaluate after their accepted charge. The empty-probe marker is lazy too. The new guard pins all five call-site expressions, their immediately preceding compare(work)? lines, and the unique occurrence of the claim operands. Precomputing a predicate and passing a captured boolean changes those pinned expressions, even when tested remains after the charge.

The four new mutations reproduce that stored-result pattern at EE-1, EE-5a (a), the parentless-entry test and the root-name test. Each archived mutation fails `rf1_every_predicate_is_evaluated_inside_its_wrapper_after_its_charge` by assertion. This closes the precise counterexample from r2; a lazy helper alone would not have sufficed without these call-site guards.

The r2 charge, ordered and reserve wrappers, operation-log grammar, independent charge model, per-site short allowances, policy checks, source guard and exact-capacity assertions are retained. Ordered comparisons and allocations remain observed where performed. The oracle requires funded blocks, and its prefixes stop before each refused site. The earlier probe-before-charge and three allocation-before-charge mutations remain caught. This supplies evidence of work order alongside totals and ledger prefixes.

The r2→r3 production change is confined to the lazy predicate helper, its documentation and the five closure call sites. The predicates, class/arm order, projection, policy, prices, sort, duplicate refusal, count/fill passes and opaque Cleared retain their accepted behavior. The additional operation recording remains test-only; the non-test note is a no-op.

## Self-review and prices

The stated bookkeeping does not require a new price:

- Loop bounds and index arithmetic operate on traversal state, not comparisons of manifest keys or digests.
- `windows(2)` creates borrowed adjacent views; the actual policy/digest comparisons are separately charged and observed.
- `roots != 1` checks the counter produced by the already charged per-command parent tests; it is not another traversal or root-name comparison.
- The analyzer dispatch selects the branch using the same role already examined by EE-5a (a)'s charged predicate. The per-entry and root-name tests inside that branch still carry their own charges.
- `slice.is_empty()` is the length dispatch selecting the probe route. The empty route still consumes LD-D4-10's one edge before returning its empty lookup result, and that route is in the oracle/model and empty-probe mutation. This acceptance does not mean an empty probe is free. Nonempty probes charge each actual key comparison; their loop/length dispatch does not add another comparison price.

These distinctions preserve the accepted operation recipe rather than claiming that every machine-level branch is a charged comparison. Actual sort/search charges remain separate from their published worst-case reference bounds. There are no owned name/string copies, computed digests or native calls in this module. The TooManyClaims branch and non-test runtime recording behavior remain disclosed as unexercised; the release build compiles the latter. The closed-world CMS/claim/class pins remain present. D4-2 still owns the authenticated adapter and pinned provider projection; this unit chooses no ledger profile or production caller.

## Lane evidence

The archived r3 lane reports all twelve check rows passing. Components passes increase 73→91, with eighteen focused manifest tests passing. Base and candidate have the exact same 54 failure names, the disclosed supervisor fixture-path failures. This is equal-failure evidence, not a claim of an entirely passing components suite.

I checked all 32 mutation logs: each contains actual failing tests and a nonempty failing-test list, without a compilation failure. The prior 28 mutation cases remain, with the tested-related anchors adjusted to closures, plus the four new precomputed-predicate cases. The archived checks include warning-denied Clippy, workspace all-targets check, release build, focused tests, environment exceptions, source/mint census, unchanged census closure and verify_design. Formatting reports lib.rs base/candidate clean and both new Rust files candidate clean. No dependency or new mint/environment/let-underscore behavior is introduced by the narrow revision. None of these lane commands was rerun for this review.

## Integration and remaining scope

The inspected integration script selects r3, requires ACCEPT-UNIT with no required findings and the matching subject hash, rehashes the subject and product candidates, checks disjoint main movement since the lane base, stages only the three reviewed paths, fast-forwards main and verifies design again. It preserves both prior rounds in the architecture record. NBO-1 corrects an obsolete label in its assent prose; the selected hashes and unit identifiers are already r3.

The inventory preparation derives the actual accepted round from the integration report, checks the accepted review/subject and mapped product bytes, derives the successor version from the current lock, realizes manifest.rs's inherited planned row and adds only manifest_tests.rs while preserving inherited rows by value. That successor still needs its own review and binding. This review performs no integration, publication or inventory mutation, and establishes no R10a/ER10a production wiring, path-half control, EE-4 negative, profile or qualification.

## Non-blocking observation

**D41-R3-NBO-1 (P3): Correct the round label in the prepared assent prose.** ROUND, subject/review paths, historical rounds and exact-hash checks correctly select r3, but ASSESSMENT still opens with “the exact reviewed D4-1 r1”. This does not change the selected bytes or integration guards, but would put an obsolete round label in the persisted r3 lead assessment.

Requested: Change that opening label to r3 before the lead executes the integration script. Keep the r3 subject/review pins and the historical round records unchanged.

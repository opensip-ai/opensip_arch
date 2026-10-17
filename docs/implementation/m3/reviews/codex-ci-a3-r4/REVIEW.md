# CI-A3 r4 review

**Verdict: ACCEPT.** No required findings or non-blocking observations. This accepts the amendment design; implementation and qualification remain separate work.

## Subject verification

Rehashed the 1,906-byte manifest (`2d1bfd96c483564538bc10d3d8a877858409f2d8c2f51edf3fd40d79d1b41454`) and all seven members. Every byte count and SHA-256 matches. The subject is the 39,140-byte `CI-A3-r4.md`, SHA-256 `8a27100bf6093223fa97f7893d19f052b650bd21b15289bad8c9b8b401254cc4`. The archived CI-A2 SCOPE matches its CI-2-r2 manifest entry and corresponding SCOPE bytes. The candidate `retained_tree.rs` inspected for latching also matches its CI-2-r2 manifest entry.

Manifest bases: product `114d2ac9708cca10563316a0cb11f09b30d1b919`; architecture `339d9dc56939b805c662398a8a946941fe3839cf`.

## Findings disposition and rulings

### CIA3-R3-RF-1 — resolved; Q1: ACCEPT

CI-A3-a places the charged F/D comparison before resolution and allocation, exempting Directory(""). A funded absent-kind request executes exactly one edge; an exhausted charge stops before its operation. CI-A3-b explicitly counts refusal prefixes: no final-member work before resolution, at most S + 1 lookups and S hop temporaries bounded by Q-hat, and resolved-member work bounded by the requested-kind maxima. Latched calls execute no charged work. Thus E_launch <= B-hat_launch covers successful and refused runs. CI-T28 includes the original file-plus-link/no-directory counterexample and independent accounting.

The new comparison appears in the executed-charge table and pre-bound. The root-directory special case retains its two status operations, path buffer and result, without a kind check, lookup, hop or descent. Per-member bounds remain conservative envelopes rather than substituted actual charges.

### CIA3-R3-RF-2 — resolved; Q2: ACCEPT

The first failure of launch_member or transfer, including Budget, latches the capability. Later calls on any scope refuse before charging or observing, with latched Budget yielding Budget(Closed). This matches pinned CI-2-r2 retained_tree.rs:151,167,422-428. Binding joins the latched causes. CI-T27 requires an exhausted launch followed by both launch and transfer on a fresh funded scope, with unchanged used and no observation.

## Regression and limits

The r3-to-r4 changes preserve the accepted CI-A2 context, stack basename treatment, shared owned launch-path buffer, actual comparison/read accounting, store-opening path charge and CI-A2 reservation alignment. Binding error partition, retained-base observations, capability lifetime through child settlement and the disclosed same-principal residual window remain intact. CI-3L remains a separate implementation unit after CI-2/CI-3 integration; D4-4 still requires that implementation.

Review used read-only document/source inspection, hashing, JSON parsing and comparison. No Cargo, rustc, build, lane, project checker, network, other pane or delegation was used; neither repository was edited. CI-T27/CI-T28 controls were reviewed as requirements, not executed or claimed as passing.

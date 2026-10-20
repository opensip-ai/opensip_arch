# D4-3 final unit review

**Verdict: ACCEPT-UNIT**

**Subject manifest SHA-256:** `9faadfbb00eb417880725563f40b2feed8a36503820560676aa03668b0c7d274`

The 17,437-byte subject manifest and all 81 declared members match their recorded sizes and SHA-256 digests. Every architecture authority, product authority, and the product design lock matches `source.json` at architecture commit `540d527a67f41554a8a05b776312e61647ae52fb` and product commit `3c02526e5fc6e3de83eec8abf04ecdb669a6ca11`. The product diff applies cleanly to that product base and changes exactly `crates/host/src/invocation.rs` and `crates/host/src/invocation_tests.rs`. The archived candidate files match the final candidate worktree and `product-map.json` at `81143ba4146990a9bc0d90e7bab4dcb59a29de702a9c732cf5be40c28e724db9` and `dbac511cfcad6b7d4a5576cc9946c3961e685711005995ea93bf671c4719fa51`. The test-source difference from cleared preflight r2 is rustfmt layout only; production source is byte-identical.

## Plan and source assessment

The exact candidate implements accepted D4 PLAN-r2's D4-3 boundary and inherited LD-D4-7 without adding a request form or production path. I1 remains permitted: the existing J1 `RequestExcludedClass` is the closed request-domain carrier for EE-2, EE-4's request part, and EE-6a, while the manifest carrier cannot represent those request classes. I2 remains permitted: `AdmittedRequest::admit` validates the step list, constructs the typed request, classifies it, and only then returns the opaque token. It draws no request identity, begins no durable entry, and performs no I/O or workflow composition.

`request_excluded_form` closes every relevant dimension. It destructures all five `AdmittedRequest` fields, all five request flags, the complete mode, and the sole JSON format without `..`; its exhaustive request match returns `None` for `Default`, `Analyze`, and `AnalyzeEphemeral` without a wildcard. The value control covers all three requests, both mode values, and all 32 flag presence/boolean combinations. No request representing an excluded form exists, so D4-T2 remains unrepresentable and row 57 remains unreachable from this admission path.

The opaque-token guarantee is complete for the reviewed module. `AdmittedRequest` has private fields, one impl, one fresh `Self { ... }` construction in that impl, no alias/macro/unsafe/conversion/deserialization constructor, and no production child module. Derived `Clone` preserves an already admitted value. The full production-module SHA-256 assertion exactly pins `81143ba4146990a9bc0d90e7bab4dcb59a29de702a9c732cf5be40c28e724db9`; the retained scoped `Self` count and source-order proof require validation, construction, classification, and handover in order. Thus an added `Self` constructor, alias, impl, child module, or alternative spelling changes the reviewed bytes and fails before the narrower textual checks can be relied on. This resolves D4-3-PRE-R1-RF-1.

## Evidence assessment

The initial shared-target candidate is correctly marked invalid and supplies no candidate evidence. Its completed baseline is reusable: the base compiler artifacts are `fresh:false`, identify the exact base source paths, and the preserved components and host executables rehash to the reported `2b14a7124f8a2963912fcd41ff7c18e751fc21077c918a9cd1db23b39a616c3e` and `d6b452e0dfe451ee9a9e09ec557754c306bcc3a83dfad307de68d8aed2741d0f`. Those exact images passed components 194/194 and host 419/419 with four unchanged ignored host controls and no failures.

The final candidate used the separate lane-r2 target. Its host and components compiler artifacts are `fresh:false`, point to the candidate worktree source paths, and their preserved executables rehash to the reported `b590ca1cfa965249923afcc6f3f92a7d52bdc6895ef834aeed50447737e8d7c0` and `16e78855e1a2f8a60fd8f1859cbd7a481899e3e3ca26f54ffc7d670820f1f95d`. The exact host image lists 425 tests, includes both new controls, and passes those two controls before the full run. The full candidate suites pass host 421/421 with four ignored and components 194/194 with none ignored or failed.

All owning checks pass: warning-denied all-target host/components Clippy, doctests, the workspace all-target check, changed-file rustfmt, environment exceptions, operability source and lock, and design verification. The restored focused invocation set passes after mutation work.

The five mutations have the claimed division and fail for the intended control:

- replacing the request match with a wildcard, skipping classification, and adding an unclassified internal `Self` constructor compile and fail the reviewed-source runtime guard;
- appending a wildcard is refused by `deny(unreachable_patterns)`;
- adding a flag carrier is refused by the closed `RequestFlags` destructure, with the existing complete initializers also refusing the missing field.

The lane restores both final source files exactly after the mutations, and their live and archived hashes match the subject. The evidence does not reuse the earlier preflight run or invalid candidate as final-source validation.

## Non-blocking observations

### D4-3-R1-NBO-1 — Preserve item-25 review on every invocation-module edit

The complete-module hash is deliberately conservative. Any future production edit to `invocation.rs`, including an unrelated edit, must trigger item-25 review before the hash is deliberately updated. This acceptance does not authorize a mechanical pin refresh.

Acceptance is limited to this D4-3 library unit. It grants no full-D4 completion, production caller or workflow composition, row-57 reachability, inventory successor, integration, platform qualification, or product qualification.

No tests, builds, cargo commands, lanes, network access, private data access, other panes, delegation, or repository changes were used during this review.

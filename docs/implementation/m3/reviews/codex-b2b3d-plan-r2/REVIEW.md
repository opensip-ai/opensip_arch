# B2B3D-PLAN-r2 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: none.

Independently verified `subject.json`: 455 bytes, SHA-256 `02c1b88377e5814be38cac3a8df4942b543c7ee2468f8ea062cd79f34418c8fa`. Rehashed its sole member, `docs/implementation/m3/config-discovery-b/b2-b3d/PLAN-r2.md`: 11,781 bytes, SHA-256 `e713f78fa6846dbb9ba19fe467061eb65bad10db96d73f0c43669bfd15ab8e2b`.

Product HEAD matches the requested clean `84caf3f58d8379c9386fda42a41e5513ac81ebbb`; architecture HEAD matches `194fcad1d89f20db50491e3a574342ff608ace50`. Compared the complete r2 plan with r1 and the prior review. Checked the relevant law, plan, bound walker unit/review pin, current core/walker/platform listing behavior, grammar vectors, trace helpers and census source. Prior inspection of the unchanged pinned base also covers the reference, walker controls and census soundness controls.

## Round-1 resolution

- **B2B3DPLAN-R1-RF-1 resolved.** Section 1.1 reconstructs only fields that already contain resolved absolute paths. Raw rejected specifications and absent paths retain their current construction. This agrees with `discovery_scan.rs` returning `Some(spec.clone())` on `JOIN_PATH_GRAMMAR` and the unchanged vectors expecting `../other`, `crates\core` and `packages/./web`. The general byte-identical-record requirement governs both invocation modes and overrides the request's shorthand about absolute output paths.
- **B2B3DPLAN-R1-RF-2 resolved.** The visitor retains only the first invalid name as a bounded, precharged copy, stops converting, and continues listing and charging. Listing native/limit/close failures win; the saved invalid name becomes a terminal absolute refusal only after listing succeeds. No partially listed directory is observed. This preserves the relevant failure order in the current `visit_entry_names`/`list` composition without retaining the old raw-name vector. Planned `ListingConversion` controls cover entry-limit, native-error and close-failure precedence, successful listing with an invalid name, and a mutation reversing the priority; a native invalid-name control supplements them.
- **B2B3DPLAN-R1-NBO-1 addressed.** Lazy spelling closures are not invoked by production trace/hook stubs. The planned structural check inspects call sites and production spelling construction, with comments/literals blanked and a planted direct-string negative. This replaces the insufficient claim that a unit-test allocation probe alone exercises cfg(not(test)) code.

## Design assessment

Root-relative keys are sound with the empty string representing the selected root. Removing a common absolute prefix preserves key order, and the root remains first. The plan covers custody, marker and unit-chain reads as well as enumeration; resolved record fields and `UnobservedAcl.path` are rebuilt with the root `/` special case. Boundary comparisons must consistently use their intended coordinate system. The scan-vector adapter may discard entries outside the selected root because existing enumeration ignores them and normalized explicit roots cannot escape it; conversion retains the root itself and uses slash-delimited descendants.

The proposed walker removes absolute per-entry paths from frames, listed/verdict maps, scope keys and `spell`. Keeping one root spelling is compatible with the law. Child names can be borrowed from the last segment of their single owned relative path, with observations held in an aligned parallel vector. Scope-owned relative keys remain separately charged records, as the plan explicitly states. Conversion/validation temporaries and collection records retain charge-before-allocation requirements. Residual root-length coefficients and actual successor costs are measured rather than assumed away.

Terminal Changed/name-refusal details may remain absolute under the accepted terminal exemption. Test-only root reconstruction preserves trace and before-open hook expectations. Passing a relative `at` to the downward VCS helpers is sound because it serves tracing, while descriptor-relative operations determine the actual observations and opens; absolute upward-selection arguments remain unchanged. No gitdir target is followed.

Existing behavioral vectors, population/evidence comparisons, trace/hook assertions and record expectations remain unchanged. Storage-key adapters and exact charge-count arithmetic may change for the redesigned layout while retaining their per-child/per-spec accounting purpose. New mutation controls target absolute-key regression, missing parallel observations, name-error priority and eager trace spelling. Together with the retained suites, soundness controls, formatting, warning-denied Clippy, pins and design verification, these are sufficient planned checks. They remain future implementation obligations; none was executed during this review.

Updating the census in the same unit avoids a stale model. Whole-file closure pins, anchored charge formulas, the closed native size inventory and predictions must be regenerated for the successor, while integrity checks, reference population, composed-workspace handling and native soundness checks carry over. Retiring the old walker's probe dependency is sound; the new four-store probe is supporting evidence for the redesigned walker, not a margin claim. Read together, section 1.4 replaces the old probe rather than retaining stale measurements. Likewise, regenerated census prediction values necessarily change; unchanged behavioral vectors and expected records remain the equality oracle.

The plan implements r6's storage requirements and preserves population, evidence and records as an implementation contract. This ACCEPT approves that plan, not an already implemented successor. No code, inventory binding, cap or law change is made. Recording census-derived caps and changing constants follow separately. Held-out and workspace full-ledger margins remain outstanding; B2-b and product qualification remain incomplete.

## Boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, tests, builds, lane or network was run. No other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or held-out entries were accessed. Neither repository, the stage nor control files was edited. Only `REVIEW.md` and `review.json` in the requested directory were written.

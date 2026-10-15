# B2B3D-PLAN-r1 review

Verdict: **REQUIRED-FINDINGS**

Subject: `subject.json`, 454 bytes, SHA-256 `28ab1aee4880ba4730d54429e5c403ddd810875c83c9faaf851ec485065d1b1f`. Its sole member, `docs/implementation/m3/config-discovery-b/b2-b3d/PLAN-r1.md`, is 8,002 bytes with SHA-256 `dece6664ff66f23e56fe867f784b44d5fe2d7266286f8b0a03a7eb50eb3407ca`. Both pins match independently read bytes.

Product HEAD is the requested clean `84caf3f58d8379c9386fda42a41e5513ac81ebbb`; architecture HEAD is `194fcad1d89f20db50491e3a574342ff608ace50`. Inspected law r6 item 12 and its accepted review, B2-b4 plan r4 sections 2.1–2.3, the bound B2-b3 walker plan and unit, the original charge-before-allocation finding, the reference and current implementation/tests/census source. The reference hash matches the scan vectors' pin. This is a plan review, not implementation acceptance.

## Required findings

### B2B3DPLAN-R1-RF-1: Preserve raw specification paths on grammar refusals

Location: `docs/implementation/m3/config-discovery-b/b2-b3d/PLAN-r1.md:25-29 (section 1.1)`.

The blanket rule that every output path, including refusal paths, is absolute and rebuilt from the root contradicts existing records. discovery_scan.rs:623-629 returns Some(spec.clone()) for JOIN_PATH_GRAMMAR. The unchanged vector explicit-join-escaping-the-root-refuses expects path ../other; the backslash and dot-segment vectors likewise expect the original specification. Root-prefixing or normalizing these fields changes the accepted record and loses the rejected input spelling.

Required change: Restrict absolute reconstruction to fields that currently contain resolved absolute paths. Explicitly preserve raw rejected specifications (and absent paths) unchanged, including JOIN_PATH_GRAMMAR in both explicit-joins and config-workspace-roots modes. Retain the existing vector expectations.

### B2B3DPLAN-R1-RF-2: Specify listing-failure precedence during visitor conversion

Location: `docs/implementation/m3/config-discovery-b/b2-b3d/PLAN-r1.md:48-51,59-64 (sections 1.2 and 1.3)`.

The plan moves validation into the visitor without saying how its errors interact with completion of the listing. At the pinned base, discovery_walk.rs:618-645 completes visit_entry_names and handles its native, entry-limit, name-byte-limit and close failures before listed_name validation at 646-655. directory_entries.rs:58-69,81-91 propagates a visitor error immediately. Returning NAME_UNREPRESENTABLE from the new visitor on an early bad name therefore masks a later listing limit, native read error or close failure that previously won. This changes refusal behavior beyond the redesigned storage, while the plan promises unchanged details and behavioral assertions. Existing single-invalid-name controls do not settle the combined case.

Required change: Define how one-pass conversion preserves the existing priority of listing failures over name-validation failures. For example, retain a bounded, precharged description of the first invalid name, finish the listing without observing children, propagate listing errors first, and materialize the terminal absolute refusal only after listing success. Add focused controls for an invalid name followed by a listing limit/native error and for successful listing with an invalid name; preserve charge-before-allocation and fail closed on partial listings. An intentional behavior change would require separate authority rather than being implicit in this storage plan.

## Assessment of the remaining design

The root-relative representation itself is sound: the empty key represents the selected root, descendant keys retain their segment spelling, and removing one common prefix preserves BTreeMap order. A scan-runner conversion that retains exactly the root and slash-delimited descendants is sound because current enumeration filters outside entries and normalized explicit roots cannot escape the root. It must use a component boundary, retain the root as the empty key, and preserve the `/` special case. Core custody reads, marker lookup, unit chains, automatic enumeration and nested-boundary comparisons must consistently use the intended coordinate system. Resolved output paths and `UnobservedAcl.path` are reconstructed absolutely; RF-1 covers the raw-input exception.

Removing `Frame.abs`, absolute listed/verdict keys and `spell` eliminates the identified per-entry absolute spelling stores and temporaries. The scope may own its relative key separately from the level path, as the plan explicitly states; this is distinct from retaining a separate child-name String. A sorted vector of relative child paths, borrowing each last segment for descriptor-relative operations, plus a parallel observation vector can preserve visitation and evidence order. Conversion and sorting must keep the vectors aligned; directory paths can move out on descent as today. The stated requirement to charge every owned record and validator temporary before allocation remains necessary; the regenerated model and size inventory must describe the actual successor layout.

Absolute trace/hook reconstruction under cfg(test), with absolute upward-selection arguments left alone, is sound in principle: project_admission.rs uses `at` only for the test trace and never to open or follow the gitdir target. Absolute Changed and name-refusal details can remain terminal exemptions. RF-2 must be resolved before name-refusal timing is considered preserved.

Keeping behavioral vectors, trace expectations, identity/ACL controls and output records unchanged is the right validation boundary. Updating direct scope reads and the two storage charge-count tests is appropriate; their new arithmetic must still catch missing per-child and per-spec charges. Unchanged vectors establish equality for their cases, but do not cover the newly relevant combined listing/name failure in RF-2.

Moving the census with the walker is sound. Rebuild the whole-pinned closure, anchored charge formulas, closed native size inventory, predictions and generated records against the successor. Preserve integrity verification, reference-population checks, composed-workspace treatment, uninterrupted-read envelope, native completion requirement, three-dimensional soundness comparisons and the five model mutations. The old probe belongs to the old walker; a new four-store probe can be archived as supporting evidence without claiming a margin. Section 1.4's wording that the probe cross-check both carries over and is retired should be read as retiring the old probe dependency, not retaining stale measurements. Census prediction values necessarily change; the unchanged-vector requirement applies to behavioral inputs/expected records, not old ledger predictions.

No cap, law or caller change is authorized by this plan. Held-out and workspace full-ledger margins remain outstanding, B2-b remains incomplete, and product qualification is not claimed. The positive JSON fields describe sound proposed mechanisms; false equality/authority fields reflect the unresolved plan issues, not an executed candidate.

## Non-blocking observation

**B2B3DPLAN-R1-NBO-1** (`docs/implementation/m3/config-discovery-b/b2-b3d/PLAN-r1.md:98`): Specify the build configuration exercised by the production-trace allocation mutation. A security unit test compiles cfg(test) tracing, whereas the production trace stub is cfg(not(test)); a test-only allocation probe alone does not establish that the production branch was exercised. Identify a production-configuration harness or a structural negative control that detects construction at production call sites. This is a validation-detail clarification for implementation review.

## Boundaries

Only read-only reading, hashing, JSON parsing and Git queries were used. No Cargo, tests, builds, lane or network was run. No other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or held-out entries were accessed. Neither repository, the stage nor control files were edited. Only `REVIEW.md` and `review.json` in the requested directory were written.

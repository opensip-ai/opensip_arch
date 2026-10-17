# C1a1 r3 review

**Verdict: ACCEPT-UNIT.** C1A1-R2-RF-1 and C1A1-R2-NBO-1 are resolved. No required findings or new non-blocking observations.

## Subject and review boundaries

Manifest `docs/implementation/m3/snapshot-plan-c/c1a1-r3-subject.json`: 10,701 bytes, SHA-256 `fdcbe0148ef3c5bcfe66bde3d31d1c8eb8906e5ad9effb19f677b265bded7188`, 46 members. Independently rehashed every member successfully. All seven product-map rows match candidate/archive bytes; existing-file parents match Git base.

Candidate HEAD is the declared lane base, `e4e715845d2d0579060709898892d3d5fd93e49e`, with only the seven declared changed/new paths. Product main is clean at `a3cef6bf8d9c1a92940aa6ef01e690524bbaa2a9`: exactly one intervening commit, changing only design-lock.json as the request permits. The recorded candidate lane selects inventory v212 and 173 contract successors; this is not a claim that integration against main's newer lock has already been verified.

Reviewed the revision against the accepted C1a plan r4 as amended by r6, M3-C r8 items 1–2 and prior review dispositions. Only the two permitted checks were executed in the candidate: the snapshot model --check passes, and operability source passes with zero findings and 114 rows. No Cargo, rustc, build, lane, network, delegation, other-pane access, private fixture, installation, signing keys, held trees, T2 store or T2-cache access occurred. Runtime and T2 results below are pinned evidence, not reviewer reruns.

## Allocation accounting

SnapshotRoot::open now charges one owned path before calling the shared LogicalPath parser. It retains that parser's validated String and moves it into SourceFile with into_string; there is no second path allocation or trailing charge. Components remain borrowed, each intermediate relative key is charged before construction, and root/child observations, opens, metadata and ACL custody retain their owner charges. This resolves the remaining successful-path validator omission without copying the grammar.

SnapshotExtent::new likewise charges each ignorePaths validator copy before parsing, borrows the supplied collection, and propagates budget failures as WorkFailure. The revised control checks two valid entries cost exactly two objects and their eleven path bytes plus two record allowances. Invalid-path diagnostic copies remain terminal refusal details under the audit's stated convention.

The expanded audit now accounts for the in-scope successful opener/extent allocations as well as the previously corrected walk allocations: listing/validation copies, observation slots, frames including the root, Cargo keys, shared-rule classifier temporaries and member lists, report slots, descriptor operations and ACL captures. Moved paths and borrowed names/parents avoid the earlier extra copies; boundary lookups remain non-copying. No additional missing charge was identified in this surface. The audit is an independent source-level justification; native/model counter equality alone is not treated as proof of allocation coverage.

## Model, controls and visible evidence

opener_cost follows the native opener's explicit charge order: validated path; root status/custody; each directory key, observation, open, status and custody; leaf observation/open/status; and marker custody when applicable. Its constants come from the unchanged census owner prices, with opener anchors and whole snapshot source pins guarding the implementation. The same conservative ACL-branch rule governs its exact flag.

The new native control checks a root-level regular file, a nested regular file and a nested marker, including the returned logical path and exact ledger totals. The archived triples are:

| Path | Native and model (objects, edges, bytes) |
| --- | --- |
| a.txt | (7, 139, 11765) |
| src/lib/main.rs | (19, 413, 34278) |
| pkg/package.json | (15, 409, 33346) |

The opener-validator-uncharged and extent-validation-uncharged mutants fail their intended native controls. The regenerated model-opener-validator-free mutant fails the opener accounting control. The model remains preparatory evidence, not an accepted snapshot cap or proof over every possible tree.

The runner's focused step now uses --nocapture. The pinned snapshot-walk-tests.log contains all 35 walk soundness triples, the summary `35 cases, 35 exact`, and the three opener triples. Independently parsed all 38 native/predicted pairs: every pair is equal. This resolves the prior evidence-reporting observation.

## Regression, lane and remaining scope

The r2 boundary adapter and lib.rs are byte-identical to their reviewed r2 versions. The walk changes only extent validation accounting; its earlier fixes remain intact: exact OpenSIP anchors are removed before observation, boundaries apply before kind dispatch, marker-custody exclusions remain marker-specific, and root S3 judgment precedes both traversal routes. Same-parent observation/open binding, no-follow access, no retries, test-only hooks and the absence of a source-content read in the non-test security modules are preserved. Passing the same WorkScope to the visitor continues to support C1a2's later read accounting without recreating the invocation ledger.

Pinned r3 lane evidence establishes:

- Identical sets of 14 security failures at base and candidate, with no differing failures. Across two suites, passes increase from 1,167 to 1,183: 16 additional tests. Each lib suite retains seven ignored tests. This is an equal-failure-set result, not an all-green security suite.
- The focused snapshot suite passes all 16 tests. The oracle still requires 28 exact automatic reference matches. Walk soundness and the three opener controls pass as described above.
- All thirteen native mutations produce actual test failures without compilation failures; all seven regenerated model mutants are caught. Twenty controls in total report caught=true.
- Warning-denied all-targets Clippy passes. The new Rust files and discovery_export.rs are rustfmt-clean; existing lib.rs is dirty at both base and candidate and excluded under the recorded policy. Model --check, T2 census --check, operability, closure-unchanged and verify_design record success.
- Independently rehashed all 19 census-closure files and compared them with candidate Git base; all match. No candidate path intersects that closure. No new prohibited from/into/pid/line/issue call, non-test environment read or Linux claim was identified.

Acceptance is limited to C1a1's preparatory library and model work. C1A-T2/T3 remain explicitly owed by C1a2 before production use; the read/custody model, sealing, cap selection, snapshot_profile and M3-C r9 gate remain later work. The separately routed discovery-classifier undercharge is not fixed or qualified by this acceptance; unchanged closure pins preserve binding, not proof that that separate accounting issue is resolved.

The five new inventory paths remain snapshot_source.rs, snapshot_walk.rs, snapshot_walk_tests.rs and snapshot_ledger_vectors.json under crates/security/src, plus tools/security/snapshot_ledger_model.py. Existing discovery_export.rs and security lib.rs retain their rows. Integration, its fresh verification and the subsequent inventory successor remain outside this review. No product qualification or overall C1a completion is claimed.

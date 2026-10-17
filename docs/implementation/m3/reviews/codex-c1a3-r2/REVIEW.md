# C1A3-r2 review

**Verdict: ACCEPT-UNIT.** Both round-1 required findings are resolved. No new required findings or nonblocking observations. The previously recorded successful-walk provenance obligation remains explicitly assigned to J2b/J2c; acceptance is limited to this preparatory library unit.

## Exact subject

Verified the 11,313-byte manifest SHA-256 `7eaf9547216d078a913345d54e72f93b61a1ba6aa5e363986768eeb99135b941` and rehashed all 49 members successfully. The ten candidate files and their archived copies match every product-map size and SHA-256; all eight existing parent files match the pinned product base. The candidate remains detached at `e937dac74c8e529fee3efb6f84439d05280e48ea`, with exactly the mapped changes and two new paths. The authorities and historical review/manifest pins listed by source.json also match.

Compared all ten current files against the archived round-1 candidate. Only snapshot_seal.rs and snapshot_seal_tests.rs change between rounds. The other eight files, including both ledger vector outputs, are byte-identical to round 1. Read the revised scope, accepted C1a r6 controls, prior findings, implementation, added tests, lane runner and recorded results. M3-C r9 remains a separate law review; this verdict does not accept it.

## RF-1: digest conversions and allocation accounting

Resolved. Production sealing no longer imports or calls digest_hex. hex_digits produces a lowercase 64-byte stack array, with high and low nibbles in the correct positions. Inventory rows and the none-observation record append those digits directly to the destination buffers. The outer VCS digest is also a stack array, and push_descriptor takes &[u8; 64] rather than a heap string. No replacement conversion introduces a temporary allocation.

The five sealing-owned allocation sites remain covered by preceding charges:

| Allocation | Preceding charge |
|---|---|
| Refused leftover path copy | owned_record(leftover.len()) |
| Inventory buffer | owned_record(inventory_len) |
| none-observation buffer | owned_record(160), before the helper call |
| Descriptor buffer | owned_record(descriptor_bytes) |
| Returned snapshot2 identifier copy | owned_record("snapshot2:".len() + 64) |

The fixed VCS buffer requests capacity 160 and is charged for 160; its encoded record occupies 154 bytes and does not grow it. Inventory and descriptor lengths account for escaped strings, decimal widths, separators and digest hex before allocation. The reviewed append paths fit those capacities. Custody retains its own separately charged operations, and IdentityCandidate admission retains the stated descriptor/schema-budget boundary; LD-C1A3-4 does not claim those delegated internals have no allocations. No change to the sealing charge terms is needed for the removed hex temporaries.

sealing_allocates_only_what_it_charges is adequate as the requested focused regression guard for these exact bytes: it compares stack hex with identity's hex, forbids the allocating conversion spellings, pins the five allocation sites, and checks each site's nearest preceding charge (the VCS helper at its call site). It is a source-shape control supported by code inspection, not a general runtime heap tracer or a proof about arbitrary future helper implementations. The two new mutants demonstrate its intended sensitivity: swapped high nibbles fail hex/canonical equality, and reintroducing the otherwise byte-equivalent digest_hex temporary fails the allocation pin. Both are actual test failures in the logs, not compiler failures.

## RF-2: mixed-error precedence and provenance

Resolved. over_bound_then_walk preloads a reached synthetic capture above 8 GiB, then runs the actual CaptureSession::walk. Only its successful report reaches seal. The four cases now establish the requested composition behavior:

- No injection completes the walk and reaches the step-5 totalBytes refusal.
- A later read error on z.txt returns Read with that subject; no sealing result exists.
- Appending before z.txt's second read changes its observed length and returns ChangedDuringRead(z.txt); no sealing result exists.
- The two-byte z.txt chunk triggers the custody write failure after the one-byte a.txt capture, returns Custody, and never reaches sealing.

The hooks exercise the real read/custody paths; the synthetic capture avoids materializing or writing 8 GiB. The no-total source pin and exact/one-over step-5 bound controls remain. LD-C1A3-5 now correctly states that the report's provenance is a composition precondition. It does not claim a public Default/Clone report proves successful traversal of this root and session. SCOPE explicitly carries C1A3-R1-NBO-1 to J2's production composition through a session-bound completion token or a walk-then-seal helper, with session freezing considered there. This is not a new API enforcement claim.

## Lane and verification

The pinned r2 lane supports its reported comparison, with known baseline failures preserved:

- Host: 397 base / 407 candidate passing tests, and the same eight failures on both sides; ten new passing tests.
- Security: 15 base / 14 candidate failures. The sole differing test, custody::git_tracking::tests::every_member_refusal_has_its_subject, passes all six isolated runs (three per side), supporting the runner's flaky classification and adjusted zero-new-test comparison. This is not a claim that the complete suites are green.
- Focused sealing: 10 passed. Session/custody: 19 passed, one ignored. Walk/source: 17 passed.
- Warning-denied all-targets Clippy passes for host/security. Every new or base-clean edited Rust file is rustfmt-clean; there are no base-dirty exclusions.
- Model, recorded T2 census check, FW-01 (8 tests), environment exceptions (10 tests), operability, closure-unchanged and verify_design all pass in the evidence. verify_design reports productQualification false.
- All thirteen mutants compile and produce the expected focused test failures. The runner restores the original bytes after each mutation. The current product-map checks confirm the restored candidate.

Independently ran only the two permitted commands in the candidate:

1. snapshot_ledger_model.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip: both snapshot_ledger_vectors.json and snapshot_session_vectors.json verified.
2. check_operability.py source --repository .: passed, 114 rows, no findings.

The T2 census and Rust lane results were inspected as recorded evidence, not rerun. No T2 cache or store was accessed.

## Regression and scope

No regression identified in the round-1 conclusions: inventory ordering and leftovers precede the carrier join and authenticated VCS gate; bounds run in rows/descriptor/totalBytes order before constructing sealing output; the canonical inventory is retained under its raw digest; and identity admission constructs snapshot2 from the six-member canonical descriptor. The carrier classification, tracking proof over the retained operation chain, admitted-member VcsPending gate and ephemeral Unobserved refusal are unchanged.

The mapped additions introduce no mint-census call, environment read or let-underscore discard. Independently compared the ten mapped paths with the 19-file census closure: the intersection is empty. The only new inventory paths are snapshot_seal.rs and snapshot_seal_tests.rs. No snapshot_profile, production snapshot-ledger cap, production caller, Git/member VCS implementation, read-set implementation or qualification is delivered by this acceptance. C1a4's r9 gate remains separate.

## Boundaries

Only REVIEW.md and review.json in the requested directory were written. Neither repository, worktree nor control files were edited. No Cargo, rustc, build, lane, network, other pane or delegation was used. No private 413 fixture, installation directory, signing keys, held trees, T2 store or T2 cache was read.

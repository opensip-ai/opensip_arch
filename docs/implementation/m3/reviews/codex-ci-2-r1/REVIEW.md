# CI-2-r1 review

**REQUIRED-FINDINGS. CI-A2: REQUIRED-FINDINGS.** Three required findings and one non-blocking observation. This verdict accepts neither the combined CI-2/CI-3 unit nor CI-A2; it accepts no CI-4 code.

## Subject and verification

The 18,829-byte manifest hashes to `56228f5744839f4fb563daa67286d912f2d448cbf5e6bf73f5d544d2d80e89d2`. All 81 members rehash exactly. The candidate is detached at `2ead5cf1796bb85f363c34fa8ff8fba715462369`. All 16 product-map candidate/archive entries and their parent states match; six paths are new. The changed-file set is exactly the map. All seven authority pins and the product design-lock pin match. Security's `lib.rs` preserves its parent's complete byte prefix.

I ran only the two permitted project checks. Operability source passes with 114 rows and no findings. The packaged receipt-input checker passes: 23 discovery-bound files, 37 companion-bound files, no changed bound inputs or receipt files, and all four receipt files byte-equal to base. Its temporary JSON output occupied REVIEW.md and is replaced by this review. No build, test, compiler, lane, network access, shared lock, or prohibited private/store material was used. Neither repository was edited.

## Required findings

### CI2-R1-RF-1 (P2): Charge the native component-name copies and include them in all affected recipes

Locations: `crates/platform/src/component_tree.rs:179-184, 253-254, 308-309, 425-427, 462-463`; `crates/lifecycle/src/installation.rs:989-1100, 637-640`; `crates/lifecycle/src/retained_tree.rs:134-193, 413-414`.

component() constructs a fresh CString, but open_regular_no_follow, entry_status, create_symlink and read_link charge only the native/status price and delegate copied-name accounting to callers. Most callers do not fund that copy. A root-level transfer is a minimal example: transfer_bound and the actual transfer charge zero objects, yet open_regular_no_follow allocates its basename CString before its own charge. V1/V2/open status reads and file opens, plus symlink basename copies, have the same omission. The target record does not fund the separate symlink basename. Thus exact object/byte equality in CI-T22 currently confirms an underpriced ledger, rather than complete work accounting. LAW item 4 explicitly prices copied native names as owned records; CI-A2 does not amend these omissions.

Required: Fund each actual name copy before allocation, or use a previously funded reusable/stack representation that avoids the allocation. State the ownership and NUL-byte convention explicitly, update the affected B_install/B_open/B_transfer rows and CI-A2 as needed, and independently verify allocations and refusal before an unfunded copy. Avoid double charging the existing generation-name, archive-path and descent records.

### CI2-R1-RF-2 (P2): Make CI-A2-e consistently amend LAW reservation semantics

Locations: `docs/implementation/m3/component-install/ci-2-r1/SCOPE.md:72`; `docs/implementation/m3/component-install/PROPOSAL.md:122, 212-216`; `crates/lifecycle/src/installation.rs:1316-1322, 1366-1370`.

CI-A2-e changes the admission sentence to reserve the whole transaction with effect/prepaid, while expressly saying nothing else changes. LAW line 212 still says only step 6 is reserved and every other row is executed and charged in its step. That is incompatible with install reserving the entire bound up front. The shortfall text also continues to name B_install instead of the proposed maximum. In addition, CI-A2-e describes the reinstall bound as the existence check and store custody, then B_open; B_open already contains store custody, whereas reinstall_bound correctly adds only the existence check/name to B_open. The amendment as written therefore describes a different custody count from the code.

Required: Quote and replace the reserved-versus-executed paragraph and affected shortfall/bound references as well as line 122. Explain the outer reservation, prepaid execution, nested publication reservation and single ledger debit. Define the reinstall bound with store custody exactly once, matching implementation and independent controls.

### CI2-R1-RF-3 (P2): Complete the promised independent operation and allocation controls

Locations: `crates/lifecycle/src/installation_tests.rs:941-1027, 1180-1249`; `crates/lifecycle/src/retained_tree_tests.rs:359-419`; `docs/implementation/m3/component-install/PLAN-r3.md:169, 178`; `docs/implementation/m3/component-install/ci-2-r1/SCOPE.md:98-114`.

The implemented checks do not provide the full independent accounting evidence required by CI-T22/CI-PT-7. The B_open test compares used counters only to production open_bound; B_transfer likewise compares counters to production transfer_bound and checks the descent object count. Neither independently enumerates the complete operation recipe. CI-PT-7 independently counts comparator calls, which does catch comparison-after-charge, but observes no allocations: its short-scratch case only checks that no comparator ran. Moving Vec::with_capacity before its still-present charge can preserve every assertion while performing an unfunded allocation. The packaged scratch mutation deletes a charge, so it does not demonstrate allocation-before-charge detection. The required 100,000-entry handle-discipline control and per-entry-handle mutation are also explicitly unmeasured. These are acceptance-plan obligations, not merely an unreported performance benchmark.

Required: Add an independent operation/allocation oracle or sufficiently complete source-order guards with adversarial controls: enumerate B_open and B_transfer fixed rows independently; detect scratch allocation before its charge with the charge retained; and demonstrate bounded live handles on the specified large tree, catching a handle-per-entry implementation. Instrumentation may live in the platform test owner rather than adding unsafe code to lifecycle. Keep comparisons/read attempts as upper bounds and objects/bytes exact, including RF-1 corrections.

## Other review conclusions

The native mechanisms otherwise follow the intended discipline: no-follow/CLOEXEC/nonblocking regular opens and kind checks; charged single native attempts without fallback; P-7's matching status expression; an opaque barrier receipt bound by exact handle-object identity; and one nonblocking flock, busy returning the file, released by close. Unsupported targets refuse before their charge/native call. The missing copied-name funding is RF-1, not an extra native-call retry.

The transaction performs capacity/bound admission before acquisition, stages directly under the store, adds the owner ACL sentinel, streams positioned 64 KiB file chunks through one retained buffer, samples archive identity, rereads every staged file in V1, applies each mode before its barrier, verifies V2, and funds publication and the parent barrier. LostRace and other publication classes remain failures; a failed parent barrier takes the uncertain route. There is no cleanup path, and reinstall verifies the existing generation without replacing it. The outer effect/prepaid structure is mechanically coherent; its authority wording needs RF-2.

The structural count rule is sound under the specified custody assumptions: unique expected immediate children are each found by their own no-follow status read, so matching their count against the bounded directory listing excludes extras. The component order keeps subtrees contiguous, enabling one branch-local descent per directory and a listing at its pop. This is not a guarantee against an owner concurrently rewriting the tree outside those assumptions.

The capability checks candidate Blob association and exact generation-record bytes, checks custody, opens the existing empty 0600 pin and acquires it before reading record/tree content, and retains generation/tree/pin handles, buffer and index. Transfer resolves each parent component separately, rechecks file type/mode/length, hashes streamed bytes and commits the verified sink only after successful completion. PinRequest is retained as the caller's fence declaration. Absence, corruption, custody, budget and I/O causes remain distinguished.

CI-A2-a/b/c/d/f/g address actual ordering, association, lookup, tree-mode, index-sharing and ACL work. Their quoted source rows agree with LAW. The amendment remains incomplete because of RF-1 and RF-2. The existing C2a-1 bridge is the appropriate authority path: constructors remain trust-owned; the candidate remains unadmitted. Shared fixture gates 7 (TestComponent and reexports) and 8 (ComponentStore::fixture) are named and use the joint predicate; lifecycle forwards nondefault fixture features and carries the crash-matrix release guard.

The packaged lane, not a fresh run by this reviewer, reports all 25 check rows passing. The archived suite comparison shows lifecycle 32→73, platform 331→340 (serial), security 1281→1281 with the same 14 failures, and equal suite counts. The evidence includes warning-denied Clippy for all three crates, workspace/four feature checks, release/fixture symbol checks selecting each build's own rlib, package-edge policy, formatting with security lib append-only, environment exceptions, operability, census closure/receipt inputs and verify_design. All 27 packaged mutations have nonempty failing-test sets. Those results do not establish the missing controls in RF-3.

The attempt history explicitly records the D3a-3 Cargo.lock, C2a-3k component_closure and C1b-1 lib rebases, along with the attempt-2 casting/feature-guard/symbol-selection and surviving-mutation fixes and attempt-4 lint/rlib-selection fixes. The final packaged files reflect those changes; earlier attempts were not rerun.

No new third-party dependency is introduced: Cargo.lock adds only lifecycle→security, with the policy allowing lifecycle's identity/platform/security edges. Source inspection and the live checker find no new environment read, `let _ =`, or mint-census call in the production additions. Bound census files remain unchanged. After acceptance, the inventory successor must add the six new paths and realize installation.rs's planned row; this review does not perform that successor or integration.

## Non-blocking observation

**CI2-R1-NBO-1: Keep the disclosed integration and fault-injection gaps explicit.** CI-T16 belongs to CI-4. The signed half of CI-T11 still needs profile-1 signed fixture integration; fixture/release symbol separation is already evidenced. Crashed-holder release and an injected parent-barrier failure remain unexercised; the inspected close-only pin and explicit uncertain-barrier route are consistent with their platform contracts. I do not add separate required findings for those four disclosed gaps in this library unit. They must not be reported as exercised, and this review accepts no CI-4 code or production qualification.

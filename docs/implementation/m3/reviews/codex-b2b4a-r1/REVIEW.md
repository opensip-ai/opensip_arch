# B2-b4a r1 review

Verdict: **REQUIRED-FINDINGS**. Three corrections are required; one non-blocking scope observation is recorded.

## Exact subject

Independently verified the 7,385-byte manifest SHA-256 `855606055a7c20bb00e0ad5d6d0e2a2a820f1516dc64b354d82131d49632fc2c` and all 33 members' lengths and hashes. Verified all ten source authority pins, the product lock, and all six product-map paths against candidate, archived and parent bytes. The complete candidate changed/untracked path set equals the product map. Product and architecture HEADs match the requested bases. The lock remains inventory v195 with 164 contract successors.

## B2B4A-R1-RF-1 — Verify the pinned workspace layout before modeling it

Location: `tools/security/discovery_census.py:624-648,757-770`.

The workspace code checks that each symlink target resolves lexically to a lead-readable store and that the resulting member-ID multiset equals `memberIds`. It never checks the mount-to-member mapping in the pinned overlay. It reads `workspace-overlay.json` only to hash its current bytes into the output, without comparing those bytes with the archived record or canonical manifest overlay.

For example, renaming a valid member symlink to `node_modules` preserves the member-ID multiset and keeps the original overlay record bytes. The current code accepts that layout and composes the verified member under the renamed mount; the normal reference rule then prunes it. A workspace margin can consequently be computed for a different, smaller population than its pinned checkout. A swapped member mapping or altered overlay record also lacks an independent integrity rejection. Byte-comparing generated output during --check is not verification of the input layout; --write would bless the altered layout.

In addition, `overlay_root_tree` immediately calls scandir on its root without a root lstat/type check, so a symlink overlay root is followed. Its child checks do not establish the stated no-follow root boundary.

Required correction: verify the overlay record against pinned archived bytes or canonical manifest authority and check the exact mount-to-entry/digest mapping. Reject unexpected/renamed/swapped mounts and non-directory or symlink roots before traversal. Preserve the lead-readable-only rule and use the guarded store helper for digest joins; the current by_store comprehension is a second direct digest-to-store join despite the sole-join claim. Add focused changed-layout/record and symlink-root controls.

## B2B4A-R1-RF-2 — Check gitlink placeholder modes

Location: `tools/security/discovery_census.py:567-570`.

The gitlink branch checks only directory kind and emptiness and does not recurse through visit. It bypasses the 0555 check that visit applies to ordinary directories. An empty 0755 or 0777 placeholder therefore retains exactly the same Git-tree and QD-22 pins and is admitted. This contradicts the exact store-mode contract; the model's optimistic custody treatment does not repair integrity verification.

Required correction: require STORE_DIR_MODE on each placeholder before listing it. Keep the kind, emptiness and pinned-commit checks. Add an independently pinned synthetic gitlink control with a passing 0555 case and writable, nonempty and symlink refusal cases. Existing synthetic integrity controls cover only ordinary blobs/directories.

## B2B4A-R1-RF-3 — Reject aborted native soundness measurements

Location: `crates/security/src/custody/discovery_census_tests.rs:378`.

The ordinary-vector test discards the completion flag from charged. An operation that stops on budget exhaustion, host I/O or an instrument failure can report only a cheap prefix, satisfy used <= predicted, and pass without completing the intended measurement. The composed-workspace test already asserts completed.

Required correction: assert completion for the 52 synthetic vectors before accepting their usage, or explicitly match independently expected infrastructure failures. A typed DiscoveryResultPending::Refuse still returns Ok and is a completed discovery outcome. Add a control that an aborted measurement is rejected, rather than accepted merely because its usage is below the prediction. This finding concerns the control's acceptance condition, not evidence that the supplied lane actually aborted.

## Model and closure assessment

Checked the Model methods against the native charge sites: root records/status; listing and both dot names; owned name/path/validator copies; spellings, observations and new scope records; observation tuples; classification/target temporaries; directory opens and status; VCS/config probes and boundaries; frames, listed/Cargo records and depth-limit probes; memoized chain judgments; marker spellings/opens/status/captures; named-root/spec/chain work; and gitdir open/custody/read/final-status/target storage. The model follows the native ordering and accounts for repeat observations separately from unique scope entries.

Unknown captures and chain judgments are taken at their dearer branch. The filesystem branch dominates the alternative ACL-entry record in objects/edges at these pinned costs. The uninterrupted gitdir read envelope is explicit; verified T2 stores refuse .git components. The model itself is a structural upper bound, not a measurement of ACL state or byte use.

All 15 whole-file closure pins and 23 anchors are exercised by the permitted census controls. Delegated path_binding status cost is included. Adding custody.rs is appropriate because it supplies MAX_CONFIG_BYTES. The only custody.rs diff is the test-only, macOS-only include module. No production caller, profile cap change or law change is added. The compiled closure-pin control checks both records against include_bytes of the current code.

Every modeled population is compared with the bound reference's walker_population and differences refuse. Composed workspaces use the same model/reference path, correcting the old member-sum problem; their input integrity still needs RF-1. Scratch materialization helpers match the closed walk tests except for the scratch-name prefix and omitted comments. The margin classifier charges twice each modeled cost to a fresh discovery-profile ledger and independently probes the record's stated limits, so it classifies against code limits rather than trusting the JSON copy.

## Executed checks and supplied evidence

Independently ran only expressly permitted commands:

- Source operability: passed, 114 rows, no findings.
- Environment-exception controls: 10 passed.
- FW-01 controls: seven passed.
- Census-tool controls: nine passed.
- Census --check with the requested architecture/packages/cache arguments: both generated files verified.

Before cache regeneration, checked that the cache/store/workspace roots and the five lead-readable overlay roots were actual directories. No held-out path was queried. Repository iteration skips held-outs before store lookup, and overlay members are matched only against lead-readable stores. The successful run is evidence for the current cache; it does not resolve the missing input rejection described in RF-1. No held-out store or overlay was opened.

Hash-pinned supplied lane-r2 evidence reports 15 successful check rows. Security passes rise from 1118 to 1122 with the same 14 named failures, not a wholly green suite. All-targets locked/offline Clippy for host and security uses -D warnings and reports success. Both edited/new Rust files are format-clean, with the inherited file base-clean and no exclusions. Vector checks, configuration tables and verify_design report success; design evidence selects v195 and qualification false. All four model mutation logs contain the declared failing native tests after regenerating predictions.

The supplied soundness log contains 52 walk and four workspace comparisons, all used <= predicted, and four passing census tests. These are supplied Rust results; no Cargo, rustc, Rust tests, builds, lane, Clippy, rustfmt, vector tools or verify_design were executed during review.

The independently regenerated record has 39 readable repository rows, five workspace rows and ten outstanding held-out rows. The three failing object margins are exactly:

- rs-very-large-aws-sdk-rust: 2,611,910 objects, 1,007,224 edges.
- ts-very-large-aws-sdk-js-v3: 540,986 objects, 403,655 edges.
- mr-ts-very-large-smithy-sdk: 572,330 objects, 439,389 edges.

All edges pass the 2x comparison. Each passes2x flag agrees with the current limits. The record returns caps to law and keeps held-out margin outstanding. No failing entry's margin is claimed. The supporting real-store probe is inspected evidence only; its byte observation is not a byte census, cap authorization or qualification. B2-b4b remains a separate reviewed amendment, and B2-b is incomplete.

## Non-blocking observation

**B2B4A-R1-NBO-1:** SCOPE.md reports 45 exact matches, but the log has 46 of 56. Over-counting is not limited to custody refusal before capture: nested-gitdir-file-repository has 440 actual versus 475 predicted edges, and some ACL cases differ after capture. Keep the general result as an upper bound and describe the three large native-store matches as those individual checks, rather than proving all T2 costs exact. Correct the tightness description on republication.

Only REVIEW.md and review.json were written. Neither repository, candidate, stage nor controls were edited. No network, other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or T2 held-out store/overlay was accessed. No binding, commit, push, cap change, product qualification or entire-plan completion is claimed.

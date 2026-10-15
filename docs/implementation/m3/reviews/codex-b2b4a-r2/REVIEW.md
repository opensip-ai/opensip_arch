# B2-b4a r2 review

Verdict: **ACCEPT-UNIT**. All three round-one required findings are resolved and NBO-1 is addressed. No new findings or non-blocking observations.

## Exact subject

Independently rehashed the 7,387-byte manifest to SHA-256 `4a549b669136d0cd18e81e7485ce764de53dc70d74a58fe02fb47c3135f4cb05` and verified all 33 members' lengths and hashes. Verified all ten authority pins, the product-lock pin and all six product-map paths against candidate, archived and parent bytes. The complete candidate changed/untracked path set is exactly the product map. Product and architecture HEADs match the requested bases. Inventory remains v195 and contract successors remain 164.

Compared the complete r1/r2 product changes. The cost model, custody module and both generated records are unchanged; the revision corrects workspace/gitlink integrity and native soundness acceptance, adds controls and corrects the scope description.

## Round-one resolutions

**B2B4A-R1-RF-1 — resolved.** `verified_workspace` requires the observed record to equal the canonical manifest overlay, match overlayDigest and equal the archived acquisition copy. The actual symlink mount-name set must equal the pinned mount set; each mount must identify its own declared member and digest and link to that entry's guarded store_path. The final member-ID comparison remains. Renaming a mount to node_modules, swapping targets and changing the record now refuse. `overlay_root_tree` lstat-checks the root as a directory before scandir, refusing a symlink root. The second direct digest-to-store join is removed. A valid synthetic overlay passes; all four negative controls pass.

**B2B4A-R1-RF-2 — resolved.** Gitlink placeholders must now be empty directories with STORE_DIR_MODE, 0555, before their contents are listed. Symlinks fail the kind check. Independent synthetic Git-tree/QD-22 pins cover a valid placeholder and writable, nonempty and symlink refusals.

**B2B4A-R1-RF-3 — resolved.** Both native soundness tests call the shared soundness verdict, which rejects incomplete discovery before comparing usage. Typed discovery refusals are completed Ok outcomes. The new aborted-measurement control deliberately exhausts a small ledger, verifies that its cheap usage is below prediction, and requires soundness to refuse it. The submitted lane reports this control and both full native comparison tests passing.

**B2B4A-R1-NBO-1 — addressed.** SCOPE now correctly reports 46 exact comparisons out of 56 and explains the other ten, including uninterrupted read-envelope overestimation and capture-branch differences. It states the T2 claim as an upper bound and limits exactness claims to the individually probed stores.

## Integrity, population and costs

The store verifier reconstructs the Git tree from blob bytes/modes and pinned gitlink commits, and separately computes QD-22's sorted canonical blob array and count. Symlink content is read as target text, not followed. Directory and file modes, single-link files, placeholder kind/mode/emptiness, unsupported objects and .git components are checked. Unexpected content changes the pins and refuses. The successful independent census check verifies the current lead-readable stores against both pins.

Held-out repository/workspace rows are skipped before lookup. store_path checks heldOut is exactly false before digest joining. Workspace targets are compared with guarded paths and use already verified member trees; symlink mounts themselves are not followed. No held-out store or overlay was opened during review.

The composed checkout includes the overlay's own entries and members as ordinary directories at their verified mount names. It follows the same model/reference path as repositories. Every modeled population is compared with bound walker_population; a difference refuses.

Checked the walker charge sites against Model: root ownership/status; listing, raw names and dot entries; owned name/path/validator records; spellings, observations and new scope records; observation tuples; classification and target temporaries; directory opens/status; VCS/config probes and boundaries; non-boundary frames, listed/Cargo records and depth-limit probes; memoized judgments; marker spellings/open/status/capture; named-root/spec/chain paths; and gitdir open/custody/read/post-status/target storage. The phase ordering, repeat observations and memoized judgments match the native walker, with conservative continuation where custody can refuse earlier.

Capture and chain unknowns take the dearer branch. The fixed ACL allowance is included; the filesystem branch dominates the alternative owned ACL-entry record at these pinned costs. The read envelope explicitly excludes interruptions, and T2 store integrity excludes .git components. This is a structural objects/edges bound, not a byte census or an arbitrary-I/O completion guarantee.

Independently verified all 15 whole-file closure pins and all 23 uniquely matching anchors. Delegated status costs are included, and custody.rs appropriately supplies MAX_CONFIG_BYTES. Whole-file refusal catches changes outside anchors. The core/rule add no discovery-ledger charges. Native helpers retain the closed walk tests' materialization semantics, with the dedicated scratch prefix and the new optional small-ledger control.

The compiled closure test checks both generated records against current include_bytes inputs. The margin test charges twice each cost to a fresh discovery-profile ledger and independently checks the record's stated limits at their exact boundary. It does not use the JSON limits as its authority.

## Verification and outcome

Independently executed only the expressly permitted Python checks:

- Source operability: 114 rows, no findings, passed.
- Environment-exception controls: 10 passed.
- FW-01 controls: seven passed.
- Census-tool controls: 16 passed.
- Full requested census --check: both generated files verified.

The submitted, hash-pinned lane-r3 evidence is consistent. All 15 check rows report exit zero. Security passes increase from 1118 to 1123 with the same 14 named failures; these are unchanged baseline failures, not a wholly green suite. The supplied native soundness log reports five passing tests, all 52 walk vectors and four composed workspaces completing within prediction, and 46 exact object/edge matches. All four regenerated-model mutation logs contain the declared failing native tests. All-targets locked/offline host/security Clippy uses -D warnings and reports success. Both Rust paths are format-clean, the inherited file is base-clean, and no formatting exclusions are taken. Supplied vector/configuration checks and verify_design report success, with v195 selected and qualification false.

No Cargo, rustc, Rust tests, builds, lane, Clippy, rustfmt, other vector tools or verify_design were executed during this review. Their results above are inspected submitted evidence.

The regenerated record contains 39 verified readable repositories, five composed workspaces and ten outstanding held-outs. The failing entries are unchanged:

- rs-very-large-aws-sdk-rust: 2,611,910 objects and 1,007,224 edges.
- ts-very-large-aws-sdk-js-v3: 540,986 objects and 403,655 edges.
- mr-ts-very-large-smithy-sdk: 572,330 objects and 439,389 edges.

All passes2x classifications agree with twice the modeled cost against current limits. These three fail objects; edges pass throughout. The record states caps returned-to-law and held-out margin outstanding. It claims no margin for a failing entry. The supporting probe's byte observation is evidence for a later amendment, not a byte census or authority to change caps in this unit.

The only existing product-file change is the test-only macOS module include in custody.rs. No production caller, cap change, production environment read or law change is added. Lead assent/publication, product integration and the separately reviewed inventory successor remain subsequent steps. B2-b4b requires its own accepted amendment; B2-b remains incomplete pending the all-entry margin gate. No product qualification or entire-plan completion is claimed.

Only REVIEW.md and review.json were written. Neither repository, candidate, stage nor controls were edited. No network, other panes or delegation were used; no private fixture, installation directory, signing keys, held trees or T2 held-out store/overlay was accessed.

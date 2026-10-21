# CI-3L-DESCRIPTIONS-r1 review

**Verdict: ACCEPT-DESIGN-UNIT.** No required findings or non-blocking observations.

## Exact subject and authorities

Independently verified the 705-byte subject manifest at SHA-256 `9620dfe2f8678cea6e624ed94bbd428d0f37e394e65520f5973dbd92e0e53515` and all three declared members. The frozen stage contains exactly those members plus the manifest. The selected `repository-file-inventory.v233.json` is 763,031 bytes at SHA-256 `39e8291cc028a154736f2c8119a16aa4cab62c8000d5e19d318291d796e9fe8d`, and the 711,307-byte product lock matches SHA-256 `22201d0b0414ee78f3ce83c6a2d59fcaeaa6f0ddd063109e33d71956d568c108`.

Product HEAD is the declared integrated CI-3L commit `2b27854b2129e6750c95d83357eb15f013a0979e`; architecture HEAD is `fbb56c1b31365dea2e070f5d752f57c618aaf8f7`. All five source-authority pins match current architecture bytes: the accepted CI-3L unit and subject, its exact seven-path product map, the accepted CI-2 inventory-v230 unit, and the independent CI-3L review. Every mapped product file matches both its integrated candidate pin and archived accepted bytes.

## Passage accuracy

All four `before` texts exactly equal the selected v233 descriptions, and their JSON Pointers select the intended rows:

| Pointer | File |
| --- | --- |
| `/files/450/description` | `crates/lifecycle/src/retained_tree.rs` |
| `/files/451/description` | `crates/lifecycle/src/retained_tree_tests.rs` |
| `/files/533/description` | `crates/platform/src/component_tree.rs` |
| `/files/534/description` | `crates/platform/src/component_tree_tests.rs` |

The retained-tree description preserves CI-3's custody, authenticated association, generation, pin, whole-tree verification, verified transfer, bounds and library-only standing. It accurately adds CI-3L's selected Entrypoint and requested file/directory/root resolution, `S+1` lookup and `S` funded-hop limits, retained-handle mode/type/length/digest or directory-identity checks, one funded absolute path, final no-follow kind/device/inode binding, capability-borrowed result lifetime and cross-operation failure latch. Its explicit D4-4 production-composition and same-principal-race limits agree with the accepted unit.

The test description accurately combines the inherited CI-3 controls with the accepted CI-3L coverage: bounded and cyclic resolution, exact refusal prefixes, binding/error partitions, charge-before-work and one-unit-short behavior, independent `E_launch`, `B_launch` and `B_hat_launch` accounting, the final 144-byte C ABI equality, arithmetic propagation without impossible allocation, funded-copy controls, lifetime compile controls, isolated capabilities, pin/GC continuity and bounded handles. It does not turn synthetic or saved evidence into installation, private-corpus or platform qualification.

The two platform descriptions accurately add the borrowed-`CStr` final-component `lstat` and retained-directory `fstat`, each charged at `status_read_cost()` before its sole native call. They preserve no retry/fallback, no-follow behavior, exact identity observations and refusal before charge/call on unsupported targets. The allocation wording now has the required scope: copied names, paths and link targets use no heap allocation on the measured routes, while error/refusal carriers may allocate after refusal. This carries and discharges the description obligation from `CI2-R2-NBO-1` through `CI2INV230-R1-NBO-1` without asserting that every primitive path is universally allocation-free.

The other three paths changed by CI-3L need no passage correction. `installation.rs` remains accurately described by its general stage-and-publish responsibility; `installation_tests.rs` already names the funded-allocation and charge-before-work guards that were extended for the stored path; and the operability-exceptions row remains an accurate source/call-audit description. None makes the broad allocation claim corrected here.

## Successor mechanism and preserved inventory

Inspected all 177 existing contract-successor records, comprising 381 direct overrides and 32 supersessions, and resolved their inventory selectors to physical file paths. Also inspected all 113 inventory-passage-inheritance rows. None directly or transitively overrides or supersedes any of these four descriptions. They are first passage overrides on the selected v233 inventory, so four direct overrides and no supersession links are correct.

The proposed successor has the exact selected parent, sorted unique candidates covering the reviewed subject except the record itself, four distinct selectors, closed override fields, exact nonempty changed texts and new architecture paths. Applying it in memory changes only the four description strings. Every other row and field, all 1,362 file rows, 20 packages and nine pending decisions remain equal by value. The raw selected inventory, 193 inventory-successor entries and 113 inherited passages remain untouched. The record therefore belongs as contract successor 178 after review and assent; it requires neither an additive inventory successor nor a verifier change.

Acceptance covers this complete description unit and these exact bytes. It does not change product code, add a production caller, close D4-4 or CI-4 work, close the same-principal window, or establish product/platform qualification. Publication, substantive assent, contract-successor binding and subsequent verification remain separate integration steps.

Review used only read-only file inspection, hashing, JSON parsing, Git queries and source inspection. No tests, builds, Cargo commands, lanes, network, other panes, delegation, private fixture/data, installation, held-out or T2 access occurred. Neither repository, any worktree, the frozen stage, controls nor evidence was edited. Only `REVIEW.md` and `review.json` were written in the requested directory.

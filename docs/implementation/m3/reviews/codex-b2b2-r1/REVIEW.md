# B2-B2-r1 review

**Verdict: REQUIRED-FINDINGS.** One required correction: discovery marker custody is not reference-equivalent when ACL and linkage/size failures coexist.

## Subject verification

Rehashed the 6,710-byte manifest, SHA-256 `7e36bb72e49511f59352542127f310a5cb5f7b98d8e24bdbdad357bc7600f520`, and all 30 members. Every size and digest matches. Verified every product-map candidate against archived and worktree bytes, existing parents against product-base Git bytes, and absence of new paths at base. Candidate changes are exactly the two modified and four new mapped paths.

Product and worktree HEADs match `f51769f885dc786168e487033645ad1a4e0ae699`; architecture HEAD matches `588e3e847379e871d9b86d73c4b86a27f08f9998`. Main product and architecture tracked states are clean. The pre-existing untracked architecture E2s directory was left uninspected and untouched. All source authority and product-lock pins match. Inventory remains v191 and contract successors remain 164.

## Required finding B2B2-1: ACL refusal order differs from the bound reference

`project_chain.rs` passes an empty known ACL to `super::check` before examining the actual captured ACL. For configuration-file objects, that shared check reaches link-count and size checks before returning. Its early failure therefore prevents the later captured-ACL judgment. SLM `_file_custody`, used by successor 164, checks actual ACL before links and size.

Read-only calls to the bound reference over synthetic owned, regular, mode-0644 `package.json` observations produced:

| Combined marker failures | Bound reference reason | Rust reason from source inspection |
|---|---|---|
| nlink 2 and write ACL to uid 4242 | `WRITABLE_BY_ACL` | `HARD_LINKED` |
| nlink 2 and unreadable ACL | `ACL_UNREADABLE` | `HARD_LINKED` |
| size 4,194,305 and write ACL to uid 4242 | `WRITABLE_BY_ACL` | `TOO_LARGE` |

The invoker is uid 1000 and ownership/mode checks pass. In each reference run discovery accepts with a marker-custody exclusion on `/h/w`; the corresponding reason is prefixed `MARKER_CUSTODY:package.json:`. The Rust path is established from the exact call sequence, not by executing Rust. Both versions exclude the marker, but the required provenance and boundary-inventory bytes differ.

**Required correction:** implement the discovery file judgment in reference order—kind, owner, mode, actual ACL, links, size—while preserving the accepted legacy `check_project_object` judgment. Do not silently change legacy refusal priority to repair the new core. Add reference vectors and product controls covering ACL-write/unreadability combined with hard links and oversize, plus marker-waiver negatives; rerun checks and regenerate evidence/pins. The existing 71 vectors do not exercise these combined failures.

## Other implementation assessment

The core otherwise follows the bound finish flow: repository/project boundaries, the exclusive source enum, explicit path grammar and crossing/pruning checks, automatic shared-rule enumeration, ordered exclusions and post-exclusion cap. Upward provenance passes through and the 19 cases that refuse before finish properly remain B2-b3's. D9 mappings match the relevant discovery refusal branches.

The normalized ObservedAcl interface is sound for readable captured entries or an explicitly unreadable state; a premise-admitted omission can be represented as an empty readable list. The issue above is judgment order, not the interface's ability to represent ACL state.

The typed waiver is confined by the core to directory-chain checks; marker calls always pass no waiver. It skips only the owner comparison. The legacy entry point delegates with None and retains the previous judgment. No serializer/completion or declaration type is added for pending provenance; the only production JSON projection is the complete V3 boundary inventory. That converter rejects non-accepted results, uses relative ordered locators and filters exclusions already explained by nested boundaries. The core has no I/O, environment, descriptor, ledger or public export/caller.

## Vectors and evidence

The generator pins the accepted reference, checker and case bytes, checks the provisioned package closure, and regenerates without writes in check mode. The Rust test converts the supplied native-shaped synthetic metadata and reconstructs all result fields and inventories. The fixture contains 45 finish-reaching historical cases plus 26 controls, with 57 accepts and 14 refusals; the 19 upward-only cases are listed separately. This verifies the supplied vectors, not equivalence for the missing combined-failure cases.

Independently ran only the three permitted offline checks:

- Operability source census: passed, 114 rows, no findings.
- Environment exceptions: 10 checks passed.
- Discovery-scan vectors: exact regeneration from the bound reference passed.

Inspected the remaining evidence without running its driver or compiler. Security retains the same 14 named failures, with 1078 → 1085 passing tests; host retains the same eight failures and 336 passing tests. Suite counts agree. These are equal failure sets, not fully passing suites. All-targets locked/offline Clippy for host/security with warnings denied is recorded successful. Formatting covers the base-clean/new files; `project_chain.rs` is explicitly classified base-dirty and excluded, consistent with the declared policy. Configuration-table checks are recorded passing. Parsed design verification is passing with v191 and 164 successors.

All eight mutation logs reach the stated failing tests rather than compilation failure. The added nested-exclusion inventory test catches the previously missed filter mutation. The planted environment read fires `disallowed_methods`, giving nine caught controls in total.

## Boundaries and remaining work

Used permitted read-only inspection, hashing, JSON parsing, Git queries, the three offline checks and bound-reference imports over synthetic inputs. Ran no Cargo, rustc, builds, lane or other tests; used no network, other panes or delegation; accessed no private fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, worktree, stage nor control files were edited. Wrote only `REVIEW.md` and `review.json` in this directory.

No acceptance, product integration or inventory binding is made by this review. Corrected implementation evidence and independent review remain required before lead assent, publication, product commit and separately reviewed inventory v192. The walker, owner integration, T2 margin, readers and qualification remain outside this unit.

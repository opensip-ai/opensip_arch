**Verdict: ACCEPT-UNIT. Inventory candidate v134: ACCEPT. Required findings: none.**

L1 faithfully implements owner decision D14 for the product Apache-2.0 licence. The reviewed change is limited to the declared licence text, package metadata, README section and two exact local-source pin updates. Native lanes were rerun within the requested write restrictions; their failures are explicitly retained below and reproduce at base. This verdict accepts the bounded L1 subject and inventory candidate; it does not certify a clean full native run or product qualification.

**Exact subject and inventory pins**

Product worktree: `/Users/sb/code/opensip-ai/opensip-l1`, detached at `91cb45aa023ecc5deeebad93cc782144ea86235c`. The diff is exactly 18 files, +224/-4. All 37 supplied byte/hash pins matched independently, including a final recheck. [pin-check.json](pin-check.json) contains the complete input pins.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `git diff 91cb45a` | 18165 | `d2b605ef4c852681b1c977de92fb94150ae3aa9e027b14739bbbf25e3f26d7aa` |
| `docs/implementation/m2/licence-l1-inventory-v134-subject.json` | 2055 | `04659e4758ec5c6ddac525948606c8dd96c3aae099c4d8e06bd08b75b6a4946c` |
| `docs/implementation/m2/repository-file-inventory.v134.json` | 552176 | `626cd71996d79de5c0efd914438dd65b3123e701e774ccdad1f8f9681466c58a` |
| Parent `docs/implementation/m2/repository-file-inventory.v133.json` | 551621 | `36ffd87a7cadb8b551e2c9e1816160a68fd0df42339f2595bb5644b015f775e1` |
| `docs/implementation/m2/licence-l1-inventory-v134/successor.json` | 145062 | `8193a7d22ca4fa07540a42616b1af7015a45b24d5d5873d64793fee126a37986` |
| Product/architecture/official `LICENSE` | 11358 | `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` |

The licence matches both architecture's root copy and [Apache's published text](https://www.apache.org/licenses/LICENSE-2.0.txt) byte for byte. No substituted wording or product-specific legal terms were added.

**Faithfulness and pins**

All eleven product Cargo manifests declare `Apache-2.0` in `[package]`, including the separately owned Rust provider workspace. Removing only that field yields each base manifest's identical parsed value. The three product npm manifests similarly differ only by `license`; the README is exactly its base content plus the requested linked Licence section. Placement and spacing match the request.

The contracts policy changes only its `Cargo.toml` row from 250 to 273 bytes, `6bd8e0bd912e78c29e56e4c2efea76af0f6d9729b306c908701f292962b48270` to `c9831759469a81087c40e264647b7c45cbbcc13a714a5396006db4dde5c0a040`. The identity policy changes only its `Cargo.toml` row from 750 to 773 bytes, `876739b9d5a7be6a8aee5eb3379e6f543425d67594acf40a411af1146c73dff9` to `8fec4be95051c64bf8b864e79b0020bb32ada345b3e50547c2b7ff35a84aea5c`. Both new pins match the actual manifests. No other policy row changes.

Cargo locks, npm locks, design-lock, generated files and the verifier remain base bytes. Searches for all 17 changed existing files' old SHA-256 values found no remaining tracked-product references. The X10, X8 and X9 manifest helpers constrain features/feature mentions; the new `[package]` metadata does not change their inputs' feature declarations. Relevant positive manifest checks passed during native testing. Negative controls that need blocked scratch paths are covered by the validation limitation below. See [static-assessment.json](static-assessment.json), [old-pin-search.json](old-pin-search.json) and [unchanged-pins.json](unchanged-pins.json).

The real verifier confirms the exclusion chains: `generator-closure.json` is selected by `existing-root-diagnostics-468a`, `build-receipt.json` by `native-repin-selection-v1`, and `typescript-lanes.json` by `typescript-closure-selection-v2`. Their pinned tooling manifest/lock bytes are unchanged and match the selected entries, including the build receipt's relative `Cargo.toml` row. Source inspection confirms that generator and TypeScript entry points require accepted design-selected registry bytes. Changing those tooling manifests now would require successors; the pinned EXIT-PLAN carries the deferred metadata follow-up. See [selection-audit.json](selection-audit.json) and [tooling-pins.json](tooling-pins.json).

**Independent verification**

Cargo resolution/build lanes used `--locked --offline`, isolated Cargo/npm caches, and targets beneath this review directory. The private TMPDIR is 0700 beneath `getconf DARWIN_USER_TEMP_DIR`; its exact path is in [run-context.json](run-context.json). A macOS sandbox denies writes outside the review directory/private TMPDIR and denies all access to the real OpenSIP installation home. HOME was not changed. No private 413 fixture, lead run set, repository edit or commit was used.

| Check | Reviewer result |
|---|---|
| Workspace tests, all targets, no fail fast | Exit 101: **1694 passed, 32 failed, 3 ignored** |
| Four-crate crash-matrix feature tests, all targets | Exit 101: **1576 passed, 45 failed, 3 ignored** |
| Workspace, crash-matrix and scenario-fixtures clippy, `-D warnings` | All passed |
| Workspace formatting | Passed |
| Rust provider test, clippy and formatting | Passed; 0 tests |
| Host package edges against v134 | Passed |
| Focused Python tests: package edges / crash checker / TypeScript checker | 14 / 18 / 3 passed |
| Real verifier with unchanged design-lock | Passed: v133 selected, 93 inventory / 75 contract successors, 55 inheritance rows, 40 generation / 48 admission sources |
| In-memory candidate selection | Passed: v134 selected, 94 inventory / 75 contract successors, 55 inheritance rows |
| Projection verifier | Passed: 55 rows, all 278 corruptions refused |
| Deterministic builder body replay in scratch | Candidate and successor reproduced byte for byte |
| Licensed TypeScript provider `npm ci --offline --ignore-scripts --no-audit --no-fund` | Passed |
| Deliberate TypeScript dependency drift with the same lock | Expected EUSAGE sync refusal |
| Unchanged contracts npm tooling offline install | Passed |

**Native validation limitation.** All native failed test names reproduce on an archived base checkout's platform/storage library targets under the same restrictions: exactly 32 plain failures and 45 feature failures, with no new failed names. Fixtures in the unchanged tests hard-code `/tmp` or the OS account temp directory outside the private TMPDIR, so sandbox EPERM prevents their setup. One private fixture's non-UTF8 APFS name probe receives sandbox EPERM instead of the EILSEQ the test expects. The feature failures include 13 barrier self-tests using the same blocked fixture. These runs do not independently confirm the lead's zero-failure native counts. The failure comparison and unchanged source boundary support treating them as review-environment limitations rather than L1 defects. [native-failure-comparison.json](native-failure-comparison.json) records every failure and the exact base comparison. Storage commit tests (6) and host commit-matrix tests (4) passed without a lead run set.

**Other baseline limitations.** Offline report candidate and base installs, and unchanged TypeScript-boundary tooling, refuse with ENOTCACHED for `esbuild-0.28.2.tgz`. The actual TypeScript wrapper first fails on the missing boundary `node_modules/.package-lock.json`; it did not reach a successful typecheck. The generator candidate first lacks pinned Python `attr`, while the archived base lacks pinned TypeScript dependency files. Both generator closure and TypeScript registry also retain a 33654-byte pre-VD1 verifier pin (`2764cf7b5e3aaa7fb1722bab6714fe1eed4a350867f4cc369d0490342527325c`), whereas the unchanged live verifier is 40714 bytes (`c13d231eb755a08a33fae674426861145758c5ec136ba2cd6dd4b0f1020f8f08`). The review confirms these stale pins but does not claim the end-to-end wrappers reached that refusal on this checkout.

Contracts refuse the unchanged stale `src/generated/evidence.rs` row. Identity has six additional Rust sources and stale rows for `src/lib.rs` and `src/schema_registry.rs`. Correctly invoked policy suites produce the same candidate/base counts as reported: contracts 2 failures/2 errors; identity 2 failures/1 error. All other existing local-source rows match, including both newly licensed manifests. Refreshing only the contracts evidence row in a review scratch policy makes its security-crypto-workspace checker pass (11 dependencies, 8 source files). Initial unittest-discovery invocations lacked the scripts' CLI-defined globals; those harness errors were corrected by rerunning each documented CLI entry point. See [local-source-audit.json](local-source-audit.json), [supplemental-status.json](supplemental-status.json), [extra-status.json](extra-status.json), and their full logs.

**Judgment calls 1–8**

1. Accept the three tooling exclusions within L1. The selected pins and explicit follow-up justify preserving their bytes; the metadata debt remains recorded.
2. Accept per-crate fields and the eleven-package scope, including the separate Rust provider workspace.
3. Accept placement after publish/private and each file's existing spacing.
4. Accept the hand edits: exactly two observed manifest pin rows change. Baseline source-policy repairs stay outside the subject.
5. Accept unchanged npm locks. The licensed provider's offline install and dependency-drift control verify npm's distinction here; report validation remains cache-limited.
6. Accept the existing intent-to-add subject mechanism. No reviewer staging or index mutation occurred.
7. Accept the in-memory verifier as a structural integration simulation. Synthetic review/assent are not actual acceptance authority or on-disk integration.
8. Accept omitting lead crash-matrix run sets for metadata alone. The ordinary feature lane was executed, with restricted failures and passing commit targets reported accurately.

**Inventory candidate**

v134 has 968 rows: v133's 967 rows remain equal by value and only `LICENSE` is added, as non-generated, proposed repository documentation. All other top-level values except standing/files are unchanged. The repository package has no dependencies, so no package edge is added. All 55 inherited descriptions retain exact before/effective text and map to their new selectors; zero additional supersessions are folded. Carried obligations and pending decisions remain intact.

The original builder cannot be run unchanged within this review: it runs Git against architecture and writes its two architecture outputs. Instead, the review replay preserves its deterministic body, redirects the architecture root to scratch, and bypasses only the off-worktree Git guard. The guard was inspected statically; it was not executed. Exact output equality, the real projection verifier and the in-memory verifier establish candidate consistency. See [builder-replay-result.json](builder-replay-result.json).

The actual design-lock still selects v133. Lead completion of the draft unit/assent and integration remain outside this review. No full M2, runtime, release or distribution qualification is asserted.

**Review-process exception**

Before reading REQUEST.md's worktree-only Git restriction, two initial read-only `git rev-parse HEAD` queries targeted the main product and architecture checkouts. This departed from that restriction and changed nothing. Every subsequent Git operation targeted only `opensip-l1` with `GIT_OPTIONAL_LOCKS=0`. No repository edits, delegation or commits occurred. The real OpenSIP home was not independently probed for absence; all run-time attempts to access it were denied by the sandbox.

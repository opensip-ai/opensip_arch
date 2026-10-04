Codex review: unit F8a r1, the refresh of OpenSIP's stale dependency-policy rows. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** on the diff. This is a product unit with no inventory successor and no design selection.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex-policy-refresh-f8a-r1`.
- Run git read-only, and only against the worktree named below.
- **No cargo build, test or clippy lanes.** Crash-matrix lead sets are running on this machine, and their 5 s timing guard fails under load. This unit changes no byte that Rust reads; the lead runs the workspace lanes at integration, after those sets. The only cargo invocation you need is `cargo metadata --locked --offline`, which the two checkers and their suites run themselves. It compiles nothing.
- Run every command at `nice -n 19`, with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-f8`, detached at product main `30c5db1` (X9-6 and D3 integrated). Nothing is committed or staged. It holds no untracked or ignored files, which matters because both suites copy the whole tree into a temp directory.
- **Diff:** `git -C /Users/sb/code/opensip-ai/opensip-f8 diff 30c5db1` is 2602 bytes, sha256 `4a3285004ce163e55d56a03aa40315344a577954b809cd69b01105bec65dd1f8`. It covers 2 files, +36 −6.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, cargo `/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`. The identity crate archives are in `~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`.
- **Evidence:** `evidence/` in this directory. Every file is pinned in `hashes.txt`.

## Why the checks failed

L1 found these checks failing at `91cb45a` (EXIT-PLAN, "Stale dependency-policy rows"). The policy rows went stale earlier than that bullet says. Replaying each policy's census at each commit with git alone (no cargo) shows:

| Policy | Last passing | First stale | Later drift |
|---|---|---|---|
| contracts (`src/generated/evidence.rs`) | `b3af5e8` (2026-09-21) | `7e1e18b` (2026-09-21, the initialization-owner unit appends `INSTALLATION.DURABILITY_NOT_CHECKED` and `INSTALLATION.NOT_INITIALIZED`) | `f482f98` (468a appends three more codes) |
| identity (local sources) | `b3af5e8` (2026-09-21) | `bcd8208` (2026-09-21, ProjectId registry codec) | `b8732e8`, `526a186`, `7e1e18b`, `b230250`, `f482f98`, `99f1c35` |

So both checks, and both suites, have refused since 2026-09-21. No unit between then and L1 ran them. Each refusal is one cause:
- **Contracts:** `local contracts source bytes differ: src/generated/evidence.rs`.
- **Identity:** `source census differs`. Six files are unpinned and two pinned files changed. No registry crate, archive checksum, resolved feature or `Cargo.toml` row is stale.

Neither failure needs a design unit. Neither policy has a generator, and no design-selected file pins either policy's bytes (L1 checked this; `git grep` finds the policy paths only in the checkers and their tests). The inventory rows for both policies pin no bytes, and their descriptions stay true.

## What F8a changes

The edit was made by `evidence/refresh_f8a.py`. It refuses unless every replaced row still holds its base value, and every added path is unpinned. It changes only `localSources`. Both policy files round-trip byte-for-byte through `json.dumps(indent=2) + "\n"` at base, so no other byte moves. After the edit, it asserts that each `localSources` list equals the observed census exactly. `evidence/refresh-report.json` is its output.

| Policy | Row | Before | After |
|---|---|---|---|
| `tools/contracts/dependency-policy.json` | `src/generated/evidence.rs` | 1569029, `8b269f8b…` | 1570438, `9fcce094…` |
| `tools/identity/dependency-policy.json` | `src/lib.rs` | 1739, `f08e459f…` | 3231, `271551e4…` |
| | `src/schema_registry.rs` | 26808, `bc6b9143…` | 26806, `82ae11b3…` |
| | `src/project_registry.rs` (new row) | none | 12368, `0805e375…` |
| | `src/project_registry_tests.rs` (new row) | none | 10630, `8c7cc2de…` |
| | `src/store_identity.rs` (new row) | none | 630, `ea7128cc…` |
| | `src/store_lineage.rs` (new row) | none | 8286, `c269883f…` |
| | `src/store_marker.rs` (new row) | none | 1644, `8bc552f3…` |
| | `src/store_selection.rs` (new row) | none | 3290, `734cfe93…` |

The policies go from 5199 B (`779597a2…`) to 5199 B (`353c2af7…`) for contracts, and from 55526 B (`b45a06f5…`) to 56471 B (`ae739105…`) for identity. The contracts policy still has 8 local rows and identity now has 20 (was 14). Every other field is unchanged: dependencies, checksums, resolved features and profiles, root features, inactive optional edges, licences, unsafe accounting, standing and review links.

## What a row asserts, and how each new row was audited

A row is not a cache of current bytes. The checkers say what it means:
- **Contracts** (`check_sources`): "Enforce the exact previously reviewed local source set, not a text lint." `tools/README.md` calls it the gate on "changes to the reviewed inert source set". `test_added_effectful_code_refuses` shows the intent: an added `std::fs::read` must refuse.
- **Identity** (module docstring): "Verify the exact reviewed pure-identity production dependency/source closure." The selected closure is a parse-only TOML graph of 8 exact registry crates. The local source census is what keeps the crate's own code inside that closure.

So a refreshed row is honest only if the file at those bytes is inert, or pure, and reaches no crate outside the selected closure. Each new row was audited for that, not merely re-hashed.

### Contracts: `evidence.rs`

- **What changed since the pinned bytes:** 28 added lines, nothing removed (`evidence/evidence-rs-since-pin.diff`). There are five new `Common4DomainDetailCode` variants, each with its serde rename, `Display` arm and `FromStr` arm. They reach no new path or crate: the arms use the `::std::fmt` and `::serde` paths that the file already uses.
- **Provenance:** the current bytes are byte-identical to the accepted candidate `docs/implementation/m2/existing-root-diagnostics-468a/product/crates/contracts/src/generated/evidence.rs` (sha `9fcce094…`). That is the output of the selected generator pipeline in 468a's `evidence/generation-summary.json`, under Grok's ACCEPT-DESIGN-UNIT. The two codes from `7e1e18b` came from the reviewed initialization-owner unit and are inside the same bytes.

### Identity: two changed files and six new files

**Structural guarantee.** `crates/identity/src/lib.rs` keeps `#![no_std]`, `#![forbid(unsafe_code)]` and `extern crate alloc;` as its only extern crate. These lines are unchanged since the pinned version. `Cargo.toml` also sets `unsafe_code = "forbid"`, and its dependency table is unchanged since the pin; L1 added only `license`. A `no_std` crate cannot name `std` without declaring `extern crate std`, and no file in the crate does. So no file in the census can reach the filesystem, network, process, environment or clock, and none can use `unsafe`. Cargo allows only the 8 selected registry crates to be imported. The checker confirms that closure is exactly the selected one.

**Per-file audit.** `evidence/audit_identity.py` strips comments and string and char literals, then reports:
- every path root, including absolute `::crate` roots;
- `extern crate` and `extern "…"`;
- `unsafe` and `allow(unsafe…)`;
- `include!`, `include_bytes!` and `include_str!`;
- `#[path]`, `env!` and `option_env!`;
- FFI attributes, `asm!`, `cfg_attr` and `std::`.

`evidence/audit-identity.json` covers all 19 identity sources.

**Controls.** In the files that were already pinned, the scanner finds the expected external roots:
- `capability_codec.rs` and `relations.rs`: `unicode_normalization`;
- `digests.rs`: `sha2_const_stable`;
- `toml.rs`: `serde_spanned` and `::toml`.

In `evidence/audit-control.rs.txt` (results in `audit-control.json`), it flags every planted escape: `extern crate std`, `std::fs`, `unsafe`, `include_bytes!`, `#[path]`, `env!`, `#[no_mangle]` with `extern "C"`, and `allow(unsafe_code)`. It also reports the planted `toml` and `::winnow` roots, and it ignores the same tokens inside a comment and a string.

| File | Audit result | Provenance |
|---|---|---|
| `lib.rs` (changed) | The diff since the pin (`evidence/identity-changed-since-pin.diff`) adds only `mod` declarations, `#[cfg(test)] mod project_registry_tests;` and `pub use` re-exports of the new local modules. The one non-local-looking root, `toml`, is the pre-existing `mod toml;` / `pub use toml::{…}` on unchanged lines 52–53. | `bcd8208`, `b8732e8`, `526a186` |
| `schema_registry.rs` (changed) | The only change is the common-v4 `SourcePin` length and digest. The new value (65062, `661b9fda…`) equals `schemas/sources/common-v4.schema.json` exactly. No import changes. The bytes equal 468a's accepted candidate (`82ae11b3…`). | `7e1e18b`, `f482f98` (468a) |
| `project_registry.rs` | Roots: `crate`, `alloc`, `core::str::from_utf8`, primitives and local types. No hits. | `bcd8208`, `b8732e8` (registry codec and registry-v2 decoder reviews) |
| `project_registry_tests.rs` | Test-only (`#[cfg(test)]` in `lib.rs`). Roots: `crate`, `alloc`. No hits. | same |
| `store_identity.rs` | Root: `alloc::string::String`. No hits. | `526a186` (shared store codecs, inventory 58) |
| `store_lineage.rs` | Roots: `crate`, `alloc`, `super` (inner test module). No hits. | `526a186`, `b230250` (F2), `99f1c35` (X3a-1) |
| `store_marker.rs` | Roots: `crate`, `alloc`. No hits. | `526a186` |
| `store_selection.rs` | Roots: `crate`, `alloc`. No hits. | `526a186` |

None of the six new files names an external crate. They are inert codecs over `alloc` and the crate's own canonical JSON parser, which is already pinned. Their module comments say the same ("Pure…; no native existence or authority"). With these rows the checker verifies 305 identity sources (20 local and 285 registry), up from 299 at the cumulative-368 review. That is +6.

**Not claimed.** The scanner is a lexical aid; the `no_std` + `forbid(unsafe_code)` crate root is the actual guarantee. The audit does not re-review the codecs' logic, which their own units reviewed. It is not a memory-safety proof or product qualification, the same limits both checkers print.

## Not in F8a (F8b)

Two checks still refuse after F8a. Both refuse for one reason: the generator closure and the TypeScript lane registry pin the pre-VD1 `tools/verify_design.py` (33654 B, `2764cf7b…`). The live file is 40714 B, `c13d231e…`.
- **`generate_contracts.py`**'s drift check refuses with "input digest mismatch: tools/verify_design.py".
- **`check_typescript.py`** is the second. L1 attributed it only to the missing esbuild archive, which does make it refuse first. But `tools/typescript-lanes.json` (selected by `typescript-closure-selection-v2`) also pins the same stale `verify_design.py`, so with the tree provisioned it would refuse "input bytes differ: tools/verify_design.py". Its other 11 tracked rows match.

Both files are selected by accepted contract successors, so changing them needs a new contract successor (ACCEPT-DESIGN-UNIT). That is F8b, drafted separately at `docs/implementation/m2/generator-closure-f8b/PROPOSAL.md`. F8a does not depend on F8b.

## No inventory

The diff adds, removes and renames no file, so the file set and v134 are unchanged. Inventory rows carry path, package, role, description, generated flag and standing, but no bytes. The two policy rows' descriptions remain accurate ("Pin the reviewed inert contracts dependency/feature profile and exact local library source set…" and "Pin the reviewed identity source and production dependency closure…"). The F3–F7 and X4B-b precedent applies: no inventory successor and no `inventoryCandidateAssessment`. `verify_design.py`'s output is byte-identical before and after the diff (sha `c9920693…`, 1150435 B).

## Lead results

All runs were at `nice -n 19` with a private 0700 TMPDIR. Raw summaries are in `evidence/results.json`.

| Check | Before (`30c5db1`) | After (this diff) |
|---|---|---|
| `check_dependencies.py --feature-profile security-crypto-workspace` (the workspace's selected profile) | refuses: `evidence.rs` bytes differ | passes: 11 dependencies, 8 local sources |
| `check_dependencies.py`, `standalone` and `toml-workspace` profiles on the workspace | refuse on `evidence.rs` | refuse with the expected feature errors (`serde_core`, `quote`), which `test_workspace_needs_explicit_profile` asserts |
| `check_identity_dependencies.py` | refuses: source census differs | passes: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, 2 failures, 2 errors | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, 2 failures, 1 error | 5 run, OK |
| `verify_design.py --architecture ../opensip_arch --implementation .` | passes: v134, 40 generation and 48 admission sources, 46 inputs, 76 contract and 94 inventory successors, 55 inheritance rows, 21 supersessions | identical output |

The before-failures match L1's report exactly.

Commands, from the worktree, with `PY=/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`, `CARGO=/opt/homebrew/Cellar/rust/1.95.0/bin/cargo` and `AR=~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f`:

```sh
nice -n 19 $PY -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --feature-profile security-crypto-workspace
nice -n 19 $PY -I -B tools/check_identity_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo $CARGO --archives $AR --policy tools/identity/dependency-policy.json
nice -n 19 $PY -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo $CARGO -v
nice -n 19 $PY -I -B tools/tests/test_identity_dependencies.py --target aarch64-apple-darwin --cargo $CARGO --archives $AR -v
nice -n 19 $PY -I -B tools/verify_design.py --architecture ../opensip_arch --implementation .
```

To reproduce the exact bytes without touching the worktree, extract the base first: `git -C /Users/sb/code/opensip-ai/opensip-f8 archive 30c5db1 | tar -x -C <scratch>`. Then run `python3.14 -I -B evidence/refresh_f8a.py <scratch>` and compare both policy files with the worktree's. To rerun the audit, run `python3.14 -I -B evidence/audit_identity.py <worktree>/crates/identity $(cd <worktree>/crates/identity && ls src/*.rs)`.

## Judgment calls

1. **Refresh, not a design unit.** Both policies are hand-maintained developer checks with no generator and no design-selected pin. The rows are refreshed by hand (L1 call 4's precedent), and the refresh is gated by the audit above.
2. **Audit standard.** "Pure" means:
   - a `no_std` + `forbid(unsafe_code)` crate root;
   - no external crate root outside the selected closure;
   - no include, `#[path]`, env, FFI or `asm` escape.

   The six new files' logic is not re-reviewed; their units reviewed it.
3. **Test files are pinned like production files.** `project_registry_tests.rs` is `cfg(test)`, but the census covers everything under `src/`. The existing policy already pins `canonical_tests.rs` and `schema_tests.rs`.
4. **Record correction.** The EXIT-PLAN bullet dates the contracts staleness to `f482f98`. It started at `7e1e18b`, and the identity staleness at `bcd8208`, both on 2026-09-21. The lead corrects the bullet at integration. It is a record-only change, outside this diff.
5. **Process follow-up (lead, outside this diff).** Add both checkers and both suites to the Python lanes of any unit that touches `crates/contracts/src` or `crates/identity/src`, so the next drift fails in that unit's own review.

## Decide

- **Diagnosis:** is it right? Are both refusals plain row staleness, with no dependency, feature, archive or manifest change hidden behind them?
- **Audit:** is each of the nine changed or added rows audited to the standard the policy requires? Is the audit standard in call 2 the right one? Spot-check the six new files yourself.
- **Exactness:** confirm that the diff changes only `localSources` rows, and that the rows equal the census.
- **Rerun:** run the five commands above and confirm the before and after results.
- **No inventory:** confirm that no inventory successor is owed.
- **Judgment calls:** are calls 1 to 5 acceptable?

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `4a3285004ce163e55d56a03aa40315344a577954b809cd69b01105bec65dd1f8`, the diff's sha256, as a single string.

No `subjectManifestSha256` or `inventoryCandidateAssessment` is needed, because this unit is neither a design successor nor an inventory candidate. Do not commit.

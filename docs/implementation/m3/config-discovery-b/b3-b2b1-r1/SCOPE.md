# B3-b2b1 r1: the D15 readers and membership decision core (M3-B unit B3-b, sub-unit B3-b2b1)

**Lead scope record, 2026-10-16. Unreviewed candidate, round 1.** It implements B3-b2b1 of the B3-b plan r2 amendment A2 (`../b3-b/PLAN-r2-A2.md`; Codex `codex-b3b-plan-a2-r2`, ACCEPT), under law M3-B r9 items 19 to 24.

**Base.** Product main `0387653`: B3-b2a bound, inventory v204, 168 contract successors. Architecture is at `6666ae1a`, which publishes A2.

## What changes

| Path | Change |
| --- | --- |
| `crates/security/src/custody/workspace_declarations.rs` | **New.** The decision core: B3-b0's `discover` without SLM's two passes, over `WorkspaceObservation` (below). |
| `crates/security/src/custody/workspace_declarations_tests.rs` | **New.** Three tests: every vector, the forbidden-access seam, and the TOML bounds. |
| `crates/security/src/custody/workspace_member_vectors.json` | **New, generated.** 146 cases: 116 from B3-b0's checker and the discovery cases, and 30 parser controls. |
| `tools/security/workspace_member_vectors.py` | **New.** It generates and checks the vectors from B3-b0 at its bound bytes. |
| `crates/security/src/custody.rs` | One module declaration (`workspace_declarations`), as `discovery_walk` is declared. **A closure file:** re-pinned (LD-B3B2B1-1). |
| `tools/security/discovery_census.py`, `crates/security/src/custody/discovery_census.json`, `discovery_census_vectors.json` | The `custody.rs` closure row is re-pinned, and both files are regenerated over the lead-readable stores (A1-2). |
| `crates/identity/src/toml.rs` | `TomlTableView` gains `len`, `is_empty` and `iter`, which are read-only (A2-1). |
| `tools/identity/dependency-policy.json` | The `src/toml.rs` local-source pin is updated, as toml-views-r1 did (LD-B3B2B1-7). |

## The core

**`WorkspaceObservation`** is what the core may observe below W, and nothing else. Every path is W-relative.
- `entry(rel)`: the observed entry (metadata, ACL state, VCS evidence), or absent;
- `markers(rel)`: the VCS markers a directory holds, each with its kind;
- `children(rel)`: a directory's child names, for the visible-repository classification;
- `bytes(rel)`: a file's bytes after its custody passed, or `TooLarge` past 4 MiB;
- `member_verdicts(candidates)`: item 6b's verdict on each counted candidate, in path order.

**`phase_one`, then `phase_two`, give the `Decision`:**
- **`Members`:** the final member set with `declaredBy`, the `workspaceDeclarations` rows and the links;
- **`Refuse`:** a member-rule refusal, `PROJECT.ROOT_CUSTODY_REFUSED` or `PROJECT.SCOPE_LIMIT`, with its path and detail and the rows of the discovery without members (LD-B3B0-5);
- **`TrialRefused`:** branch A's trial walk refused, so its result stands, with the rows it carried.

`phase_one` decides when W is in a repository and in branch B. In branch A it returns the provisional members, which are the trial walk's member roots. `phase_two` then makes the member decisions, given the trial's verdict.

**What it decides, in B3-b0's order:**
- carrier selection, the ambiguity of `.cargo/config.toml` against `.cargo/config`, carrier custody and the 4 MiB cap;
- the parsers: Cargo through `parse_toml`, and npm through `parse_json`. Every `parse_toml` error is `parse` (A2 r2);
- entry shapes and the entry-path grammar, and npm globs over the lawfully visible repositories;
- placement, candidate failures, the 64-member cap, branches A and B, and root-in-repository;
- directory custody of member directories, under the owner waiver;
- item 6b's verdicts;
- links and their dispositions: name mismatch, unusable version, unusable manifest, ambiguous provider, and entries inside an inner boundary or a pruned anchor.

Custody is judged by the scan core's own `judge_entry`, so the custody code strings are the product's.

## Vectors and controls

`tools/security/workspace_member_vectors.py` runs B3-b0's `discover`, unchanged, over every discovery case of `discovery-cases.v1.json` and every D15 case of B3-b0's checker. It wraps the reference's `_finish` and `_refuse`, without changing their bytes, to record the decision. **Per case:**
- the observation below W and the facts (W2, user, groups, waiver, array);
- branch A's provisional members and the trial's status;
- the expected outcome;
- the reference's access record (A2 r2, Codex B3BA2-R1-RF-2). That is every path its reader code looked up (`_entry`) or read (`contents`), plus the case's own `notRead` and `notObserved` lists.

**Not vectors:**
- 20 cases select no root, so no carrier is observed, and they are listed by id;
- the side-table consistency control is input validation, not a decision.

**The tests:**
- **Every case.** The core's outcome equals the reference's, field by field. The test adapter records every lookup and read. The core touches nothing the reference did not, and nothing on the forbidden lists. These cover a member's SX-1 anchor, the dependency, VCS and Cargo `target` anchors, hidden glob repositories, and visible enclosing boundaries.
- **The forbidden-access seam.** A lookup below a member's anchor is made and discarded, so no output changes, and it is caught. The lane's `anchor-looked-up-before-classifying` mutation does the same in the core.
- **The TOML bounds (A2 r2, B3BA2-R1-RF-1).** Four controls give a Cargo carrier, or a provider `Cargo.toml`, an unrelated 128-deep array or an unrelated 1,100,001-element array within 4 MiB.
  - `tomllib` reads all four (`referenceExpected`).
  - The product's expectation is the existing `parse` disposition: the carrier `refused/parse`, and the manifest `link-manifest-unusable/parse`. It is computed by the reference over the same input, with that file replaced by unparseable TOML. The carrier's digest is the real bytes'.
  - The test asserts that the two outcomes differ, that the product matches its expectation, and that `parse_toml` reports `RecursionLimit` and `NodeLimit` on those inputs.
- **JSON alignment (26 controls).** npm carriers and provider `package.json` files, each with one probe value:
  - at and past depth 32;
  - at and past each integer bound;
  - negative zero, a float and an exponent;
  - a lone surrogate escape and a surrogate pair;
  - a duplicate key, top-level and nested.

  The reference's dispositions are the expectations, and the product equals each.

## Lead decisions

- **LD-B3B2B1-1. The plan's path, with the `custody.rs` re-pin.** The core is `custody/workspace_declarations.rs`, as plan r2 section 3 names it. It reuses `custody`'s private `Refusal::code` through `judge_entry`. `custody.rs` declares every custody module, so its one new declaration changes a closure file. Under A1-2 this unit re-pins that one row and proves the equality projection (`evidence/b3b2b1-checks-r1/equality-projection.json`). Both census files differ from the base only in `closure/6`. The held-out rows were already outstanding at the base, from B3-b2a, and they stay so. **Rejected:**
  - a crate-root module, which would have duplicated the custody code table;
  - widening `Refusal::code`, which also edits `custody.rs`.
- **LD-B3B2B1-2. W2 is an input.** The reference derives it from the synthetic markers of W and its ancestors. The product takes item 6a's `NoRepository`, which B3-b2b2 supplies with the proof. The vectors carry the reference's W2.
- **LD-B3B2B1-3. Entry order.**
  - `parse_toml` gives a table's keys in key order, while `tomllib` gives document order. No disposition depends on the order of Cargo patch entries. Every record list is sorted or deduplicated by its full key. The ambiguity and first-wins checks are per package name or per entry, never across order.
  - npm's array order and branch A's array order are kept: branch A's first other-volume path is the array's first.
- **LD-B3B2B1-4. Bytes only after custody.** B3-b0 consults its contents table before it judges custody. The core reads a carrier's or a manifest's bytes only once its custody has passed. So its read set is a subset of the reference's, which is what the test asserts.
- **LD-B3B2B1-5. Item 6b is consulted once per decision,** over the counted candidates that pass directory custody, in path order. Branch B excludes the rest with their subjects. In branch A only the candidates before the first custody failure are observed. The first refusal in path order wins, which is the reference's per-candidate order.
- **LD-B3B2B1-6. An uncaptured ACL is never a pass.** A judgment that needs an ACL the observation did not capture reads `ACL_UNREADABLE`. B3-b2b2's native observation captures every ACL it judges.
- **LD-B3B2B1-7. The identity view and its pin.** `TomlTableView::iter`, `len` and `is_empty` are read-only views over the parser's table. Grammar, bounds and every other API are unchanged. The `src/toml.rs` pin in `tools/identity/dependency-policy.json` is updated, as toml-views-r1 updated it. **Pre-existing:** `check_identity_dependencies.py` already fails at the base, with "source census differs: crates/identity". Its local-source census predates later identity files. `tools/tests/test_identity_dependencies.py` also fails at the base (2 failures, 1 error). The lane shows the identity check's outcome equal at base and candidate. Refreshing that policy is a separate, reviewed decision, for the status round to route.
- **LD-B3B2B1-8. Paths are W-relative;** the composition spells them under W. `PROJECT.SCOPE_LIMIT`'s path is `""`, which is W.

## Checks

Lane r1, `evidence/b3b2b1-checks-r1/`:
- the security and identity suites at base and candidate, with equal failure sets and three new security tests;
- the equality projection;
- rustfmt on the new and base-clean edited files;
- Clippy, warnings denied, all targets, on security and identity;
- the `workspace_declarations`, `discovery_` and `git_tracking` tests;
- the workspace and member vectors, and the walk, scan, upward and rule vector checks;
- FW-01, walk storage, the census-tool controls and the census `--check`;
- the identity dependency check at base and candidate;
- the environment exceptions, the operability source census and verify_design.

**Mutations,** each in the core. The `workspace_declarations` tests must fail on each:
- the cap off by one;
- a lookup below an anchor before classifying it (forbidden access, no output change);
- the glob walk entering anchors;
- extra patch keys allowed;
- an inner entry linked;
- the ambiguity threshold;
- a reader declarer duplicated;
- the root-in-repository subject altered;
- the trial verdict ignored;
- member directories judged without the waiver;
- the candidate depth unbounded.

## Inventory

New paths for the inventory after acceptance:
- `crates/security/src/custody/workspace_declarations.rs`;
- `crates/security/src/custody/workspace_declarations_tests.rs`;
- `crates/security/src/custody/workspace_member_vectors.json`;
- `tools/security/workspace_member_vectors.py`.

## Not claimed

- No native observation, item 6b composition, walk composition or serialized `workspaceDeclarations`: those are B3-b2b2's.
- No T2 link-map control and no joint sweep.
- No production caller.
- No census model extension (B3-b3a).
- No qualification.

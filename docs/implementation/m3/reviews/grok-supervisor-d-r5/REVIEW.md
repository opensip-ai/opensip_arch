# M3-D r5 review

**Verdict: ACCEPT.**

Subject `docs/implementation/m3/supervisor-d/PROPOSAL.md`, 209266 bytes, sha256 `224b9228e9d7c0bc11c848c88cd2ed7fa7da8734208c45d70fbb678a97afec6d`. Base `PROPOSAL-r4.md` is `114e9e10…`, 202935 bytes. The diff is 18 hunks. The r3 and r2 history sections are byte-identical to r4. Every other change is in the r5 changes table: the round banner and review-history paragraph, the two marked rows of the r4 table, the product line, the who-refuses bullet, the projection sentence, item 24's forbidden substitute, D4-T4's pins, item 25's warrant and host-invariant bullet, the SD-5 cell, X-D4-J1-1, X-D4-J1-2, X-D4-CR1, X-D4-SL, row 57's heading and source column, and the D4 gate and row. Section F is unchanged and remains an O7 placeholder.

## RF-1

Resolved. On `crates/security/src/component_manifest.rs` at `052d3cb` (21818 bytes, sha256 `d70c75b1…`, blob `2ece3789…`, the same blob at `218465f`):

- (b) is `roots.len() != 1` and a parentless name that differs from `manifest.name` (`:178-184`), returned as `Error::Command`.
- (c) is the reserved-name check over the manifest name, manifest aliases and the parentless entry's aliases (`:257-270`).
- `validate` (`:395-396`) and `validate_inventory` (`:398-402`) both call `validate_inner`, which calls `command_checks` at `:414`.
- The live-name loop (`:271-276`) runs only when a context is passed. `validate_inventory` passes none.
- Nothing in the file checks a closure-only role. The generated shape's only role string is `analyzer` (`component_manifest_shape.rs:35`, sha256 `efb068ac…`, same blob at `218465f`). A shape failure returns `Error::Schema` at `:410-411`, which is the schema refusal CR-1 calls RJ-6, so no closure-only manifest is a validated value.

The who-refuses bullet (PROPOSAL.md:789-794) matches that split. (b) and (c) stay the security owner's, now and after C2a, with D4 as DR-G29's backstop. (a) has no check in those bytes. Until C2a materializes CR-1's role-scoped schema, D4's own EE-5a check is the enforcing check for (a). Once C2a lands, the schema refuses a closure-only manifest that declares `commands` (CR-T7: a tree, `[]` or `null` refuses RJ-6 at admission) and D4 becomes the backstop CR-T8 exercises by presenting the tree to D4. CR-T7 names no entry point. Both entry points already run the shape check at `:410`, which is where that schema lands, so the "both entry points" clause matches the call. D4-T4 pins (b) and (c) to `:178-184` and `:268-270`, pins (a) to D4's own check, and adds the RJ-6 pin only once C2a has landed. The live-name check is excluded from the pin.

No condition has two routes. In production a manifest meets the security owner's refusal first where one exists: RJ-2 for (b) and (c), the shape's role refusal before C2a, and RJ-6 on `commands` after C2a. D4's arm is the backstop, and CR-T8's direct presentation is that backstop. For (a) before C2a the security owner has no check of the predicate, so D4's check is the one route for a value presented to D4. The order is stated as law (`:793`), as a forbidden substitute (`:811`: D4 integrated without its own (a) check, or relying on C2a's RJ-6 for (a)), and as a unit gate (`:1249` and the D4 row at `:1262`). That matches CR-1's D4 join and CR-T8: the schema refuses at admission once it exists, and a tree presented to D4 still refuses through EE-5a. D4 does not wait for C2a.

## NBO-1 and NBO-2

Both applied. Item 25's warrant (PROPOSAL.md:838) is the NOT-SELECTED-cell precedent from NE:3577-3579, which names the cell, and this law reuses that class and code for the three request-class forms and the detail only once SD-7 widens the remedy. The D9 `nonAnalysisDerivation` rule 2 parenthetical was already in the r4 sentence; rule 2 is the request-rejected class for those non-analysis failures, and it now qualifies the reuse. The r4 table's X-SD5-1 row and row 57's source column carry the replacement text. The host-invariant bullet (`:844`) no longer treats NE:3577 as already naming these forms. The route is unchanged.

Rows 56 and 57 are cited as owed via J1's next revision, in item 24, the SD-5 cell, X-D4-J1-1, X-D4-J1-2 and row 57's heading. J1 r4's matrix ends at row 55 (J1:701). S20 (J1:774) says that until S20 lands, item 10 has no row for the projection. The live J1 r5 draft, which is in review and not cited as authority, carries row 56 and leaves item 25's row unwritten. D4's envelope remains SD-5's bound row.

## Record

The product line matches `218465f`. Head is that commit. `design-lock.json` has 85 contract successors at `052d3cb` (sha256 `2357d475…`) and 91 at `218465f` (sha256 `ac1449a6…`). The seven commits since `052d3cb` are FA-2, RUST3-LIM, P0, S18, CR-1, SYN-1 and SYN-1F. Each changes only `design-lock.json`, except P0 (`5e25d04`), which adds the `crates/components` and `crates/syntax` scaffolds, their workspace members and the host dependency-policy rows. Nothing in that range changes `crates/platform`, `crates/contracts`, `crates/security`, `crates/identity` or `schemas/`. FA-2 overrides NE:2990 and RUST3-LIM overrides NE:2942, both inside NE §9 ranges this law cites (`NE:2989-2990`, `NE:2929-2942`). SYN-1's native-evidence overrides are outside §9, and SYN-1F overrides a foundation file. The law still reads the cited product bytes at `052d3cb`.

## One observation

X-D4-J1-2 still tells J1's next revision that its M3D short name cites D r4 once r4 is accepted. r4 was not accepted, and J1 r5's short name cites r3. The sentence should say that the short name cites this law once it is accepted. It does not change a route.

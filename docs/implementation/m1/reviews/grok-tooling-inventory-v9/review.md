# Independent Grok review: tooling inventory v9 (two-path additive layout)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/tooling-inventory-v9-subject.json`
**Manifest SHA-256:** `ccfa6e348d24b3dbd631372e0bdab78b5db0893c2ce515e58775205194686c0e`
**Members:** 3
**Verdict:** **ACCEPT-UNIT**

Additive file-inventory layout only. It reserves `crates/platform/build.rs` and `tools/tests/test_entropy_backend.py`. It does not approve the guard implementation, bootstrap, M1, or release. Filename approval is not implementation acceptance.

## Custody

3/3 subject members match architecture bytes before and after. Paths are POSIX-sorted unique.

Parent inventory v8 is Grok ACCEPT-UNIT with root assent and is **installed** in the live lock (6 inventory / 6 contract):

- candidate `docs/implementation/m1/repository-file-inventory.v8.json` `c4a1242c…2611` / 119982
- review `ca5afc20…ea6032` / 4716
- unit `ACCEPTED-UNIT`, `rootSubstantiveAssent: true`

v9 is not in the live lock. This review does not rewrite the v8 verdict.

## Additive layout

Parent v8 has 328 files and 20 packages. Candidate v9 has 330 files. **328 inherited rows are byte-equal.** Removed: none. Added, matching `successor.json`:

- `crates/platform/build.rs` — package `opensip-platform` (most-specific `crates/platform`), role `entrypoint`
- `tools/tests/test_entropy_backend.py` — package `tooling`, role `test`

`schemaVersion`, `packages`, and `pendingDecisions` are unchanged. Paths are sorted unique. Neither new file is in the live product tree.

## Passage remapping (activation duty, not a layout defect)

Inherited `apps/cli/src/bootstrap.rs` remains `files[7]`. `apps/report/package.json` remains `files[13]`. Root `package.json` shifts **157 → 158** because `crates/platform/build.rs` sorts before it.

Live `inventoryPassageInheritance` currently has **only** the CLI overlay on v8 `/files/7`. Bootstrap root/report description overrides live as **contract** passages on the v8 parent, not as inventory inheritance. When selecting v9, activation must re-project **all** ancestor description overlays (CLI plus bootstrap root/report) onto v9 **by path**, not by copying the old `/files/157` pointer. The platform-backend selection README states this. This layout unit does not bake those after-texts into v9 JSON (inherited rows stay byte-equal to v8).

## Must-fix / should-fix

None in this additive-layout scope. Required findings remain empty.

## Remaining

Selecting v9 into the live lock with full ancestor passage re-projection; materializing the two paths; the separate platform-backend design unit; M1; release.

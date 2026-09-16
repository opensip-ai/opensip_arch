# Independent Grok review: tooling inventory v5 (additive layout)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/tooling-inventory-v5-subject.json`
**Manifest SHA-256:** `87689124f9538b906bd521929d696bd7460913c0a5b2dcfb4c6a007bb1c00b27`
**Members:** 6
**Verdict:** **ACCEPT-UNIT**

Additive file-inventory layout only. It does not install product files, activate generator/checker packages, select npm/bootstrap policy, or approve unimplemented orchestration behavior.

## Custody

6/6 subject members match architecture bytes before and after. Paths are POSIX-sorted unique. Live accepted parent inventory v4 in product `design-lock.json` is `docs/implementation/m1/repository-file-inventory.v4.json` `c6c85fb8…fe84f5` / 87766 bytes and matches the architecture file and this successor’s `parent` pin. Current lock `verify_design.py` still passes without this unit (v5 is not selected).

## Additive layout

Parent v4 has 246 files and 20 packages. Candidate v5 has 323 files. **246 inherited rows are byte-equal by value.** All inventory keys other than `standing`/`files` (including the 20 packages, dependency edges, and policy lists) are unchanged. Candidate file paths are sorted unique. The 77 additions equal `successor.json` `addedFiles` and `validation.json`.

Classification:

| Group | Count | Paths |
| --- | ---: | --- |
| Generator/provisioning | 36 | `tools/build_contracts.py` … `tools/provision_python.py` (authored generator04 modules and receipts) |
| Checker package/test/support/fixture | 37 | `tools/typescript-boundary/**` authored package, tests, helpers, fixtures, staging-map |
| Independent locks | 2 | `apps/report/package-lock.json`, `providers/typescript/package-lock.json` |
| Orchestration reservations | 2 | `tools/check_typescript.py`, `tools/typescript-lanes.json` |

`generator-additions.json` (36) and `checker-bootstrap-additions.json` (41 = 37+2+2) union to the 77 rows and match the v5 inventory rows exactly.

## Ownership, naming, closures

Every new row’s `package` is the most-specific package whose path prefix contains it (`report` / `typescript-provider` / `tooling`). No `node_modules` or `tools/contracts/python-packages/` members are inventoried as first-party modules; those remain dependency closures behind lock/wheel/package manifests.

Python maintenance entries use underscores (`generate_contracts.py`, `provision_python.py`, `native_guard.py`). JavaScript tests use hyphenated `.test.mjs`. Package/lock filenames stay standard. No new factory.

Filenames do not grant semantic code or activation approval. Generator snapshot/receipt rows describe inputs. Checker fixture copies of historical inventory/review JSON are regression inputs under `tests/fixtures/`, not live approvals.

## Unimplemented orchestration

`tools/check_typescript.py` and `tools/typescript-lanes.json` are **not present in the product tree**. This inventory only reserves those names. It does not approve unimplemented checker-bootstrap behavior. Generator04 and checker08 package sources exist as reviewed implementation subjects; this unit still does not install them.

## CLI / deferred metadata

`apps/cli/src/bootstrap.rs` is still `files[7]` with the same parent description as v4, so the existing metadata-v2 passage inheritance can continue through v5 by path. Root `package.json` still says the package manager/lock remain to be selected. Report `package.json` still says frontend/bundler remain undecided. This unit does not silently settle those deferred bootstrap decisions.

## Must-fix / should-fix

None in this additive-layout scope.

## Remaining

Selecting this inventory into the live lock, materializing owned files, generator design-unit activation, checker bootstrap/policy, npm/root bootstrap, M1, and release are separate.

Later unbound generator discovery (tsconfig, external-by-path, computed-require) is **not** a required finding against these 77 additions. A future `tools/contracts/tsconfig.json` (or generator05) is a later additive inventory path, not an omitted member of this layout.

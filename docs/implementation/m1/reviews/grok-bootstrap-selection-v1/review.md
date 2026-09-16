# Independent Grok review: bootstrap selection v1 (development design unit)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/bootstrap-selection-v1-subject.json`
**Manifest SHA-256:** `410bfd59ed87392598f8329d591ed24545b59bb56d814c04fc0617659d6cd9d5`
**Members:** 106
**Verdict:** **ACCEPT-DESIGN-UNIT**

Narrow **design selection** of development bootstrap/tooling bytes: 52 owned product files, 160 checker execution pins, three lanes (report/provider/generator), Node 24.16.0 / npm 11.13.0 independent locks, native DOM + esbuild 0.28.2 report, explicit `tools/check_typescript.py` wrapper. Checker10 and Cargo checker02 implementation verdicts are reused, not re-run. Root substantive assent, live-lock selection, public wrapper positives, and `evidence/activation-plan.py` remain separate. Not product install, M1, release, or fresh blind consumer B.

## Custody and verifier-definition joins

106/106 subject members match architecture bytes before and after. Paths are POSIX-sorted unique. Frozen selection was not executed against; private copy under `review/copy`.

Using product `verify_design.py` `pin_rows` (read-only):

- `successor.candidates` (105) and `successor.parents` (3) are sorted unique.
- Candidates **cover** every subject member except the successor record, with identical pins.
- Six `passageOverrides` match parent bytes (`before`) on inventory v8 `/files/157` (root `package.json`), `/files/13` (`apps/report/package.json`), and chapter 14 lines 316, 550, 105, 106. After-text differs. Old parent bytes are preserved.
- No candidate path reuses a currently accepted live-lock input.

Parents pin to architecture bytes:

| Parent | Standing |
| --- | --- |
| `generator-selection-v2/successor.json` `aee8e370…de5a1` / 12258 | live contract successor |
| `repository-file-inventory.v8.json` `c4a1242c…2611` / 119982 | archived ACCEPTED-UNIT (inventory8); **not** in live lock |
| `docs/v2/architecture/14-repository-and-module-layout.md` `c7b10bf6…287e` / 65207 | live architecture input |

Live lock is still **4 inventory / 5 contract** (`2d96b8c2…4c77` / 20329): inventory through v6, contracts through generator-selection-v2. Inventory 7/8 genuine approvals are archived, not installed. CLI `/files/7` remains `apps/cli/src/bootstrap.rs`; when v8 is selected, existing metadata-v2 passage must continue by stable path (activation-plan remaps by filename).

## 52 owned files and 160 execution pins

Materialization map has **52** destinations, all pin-match architecture product bytes, all present in inventory v8. 20 packages unchanged. Composition: checker10 **38** authored files (runtime/tests/config/lock byte-identical to frozen10; **only README** reconciles 233→234), Cargo checker02 entry+test byte-identical to `package-boundaries-02` subject, plus wrapper/registry/helper test, tools README, root/report/provider npm+tsconfig, `.gitignore`.

`tools/typescript-lanes.json` is one of the 52. Its `files` array is **160** sorted-unique pins: 12 first-party (`check_typescript.py`, `verify_design.py`, checker `bin`/`src`/`package.json`/`package-lock.json`) plus 148 `node_modules` trusted-tool bytes. Checker tests/fixtures are **not** execution inputs (checker is a trusted tool, not an analyzed product lane). `verify_design.py` is pinned in the 160 but not re-owned here (already selected by generator). Node pin `120573328` / `1ee75375…c4b8` matches the live selected Node v24.16.0 binary.

Three lanes: report (`report.ts` + `help-view.ts`, `toolPolicy` null), provider (`protocol.ts`, null), generator (seven contracts sources, **generator-selection-v2** policy path). Live report/provider trees contain exactly those TypeScript sources. No new package DAG edges.

## Wrapper semantics

`check_typescript.py` loads `verify_design.py` from the trusted checkout (`HERE`), verifies the actual lock, then requires the registry digest to appear **exactly once** among accepted contract inputs. It pins the 160 files (canonical relative regular files, no symlinks), own/helper/checker bytes, and explicit `--node`. Ambient `NODE_OPTIONS`/`NODE_PATH`/`ESBUILD_BINARY_PATH` are stripped. Child timeout 300s; `killpg` + reap on timeout/interrupt. `bin/check-boundary.mjs` re-execs with `--experimental-import-meta-resolve`. No installer/network. Supported commands and Cargo `--locked --offline` metadata limits are in `product/tools/README.md`.

Independent private controls (`review/probes/wrapper_controls.py`) **7/7**:

- `--node` required (omit → argparse exit 2)
- `tests/test_typescript_check.py` **3/3** (exact pins, escaping/linked/non-regular paths, process-group kill/reap)
- Private live-product overlay with registry file present but **not** lock-selected: `ValueError: TypeScript lane registry is not selected exactly once by an accepted design unit` (matches `activation-refusal03`)
- Selected Node bytes match the registry pin

No public positive. Current 4/5 chain cannot select this registry.

## Activation plan vs this selection

`evidence/activation-plan.py` is a **post-assent** private activation script: it refuses missing ACCEPT-DESIGN-UNIT / root assent (no fixture approvals), binds archived inventory 7+8 then this successor, remaps CLI passage by stable path, materializes the 52 files, `npm ci --offline` on four lanes, then wrapper clean/built, ambient-override, unknown-lane, registry/code change, browser-node, undeclared source, wrong Node. That is activation, not this design verdict. Material gap: it cannot run until this review is archived and root assents; npm cache path is an explicit prior provision store. Historical refusal01/02, empty Cargo metadata, and missing `r-efi` fetch remain qualifications, not passes.

## Must-fix / should-fix

None in this design-selection scope. Required findings remain empty.

## Remaining (not waived)

Root ACCEPTED-DESIGN-UNIT assent; selecting inventory 7 then 8 then this successor into a lock; `activation-plan.py` public positives/provisioning; product install of the 52 files; M1; report application/provider behavior; release; fresh blind consumer B. Cargo checker does not authenticate caller metadata or qualify the unimplemented Rust provider. Whole-tooling source purity and complete dynamic closure remain unqualified.

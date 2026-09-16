# Independent Grok review: TypeScript checker packaging08

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-typescript-boundary-package-subject-08`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/typescript-boundary-package-08/subject.json`
**Manifest SHA-256:** `6882249d85a9136ff343b2e3824e812c50124b59445ea1ed2c0b9bc337fa54ff`
**Entries:** 247 (202 files, 42 directories, 3 symlinks)
**Archive:** `27c5fa56ee3c2fcc47678032824c5f4329a048adad83ffb5aff8c7e47c35cb93` / 9010135 bytes
**Verdict:** **ACCEPT-UNIT**

Narrow packaging delta of actual Grok-accepted checker07. Seven `src` modules and `bin/check-boundary.mjs` are byte-identical to `/tmp/opensip-implementation/m1-typescript-boundary-subject-07/checker`. This is not a checker semantic change. Original checker07 remains unchanged. Runtime policy semantic acceptance remains upstream `verify_design`; no production policy is selected here. Not inventory/bootstrap/policy activation, product install, M1, blind consumer B, or release.

## Custody

247/247 entries match path/type/mode/bytes/sha256 or symlink target before and after. Three `.bin` links (`esbuild`, `tsc`, `tsserver`) keep relative targets. Archive digest matches. Frozen subject was not executed against. Private copy of listed entries only under `review/copy`.

## What changed vs checker07

| Area | Finding |
| --- | --- |
| Runtime | 7 src + bin **identical** to checker07 |
| Manifest | `@opensip/typescript-boundary` `0.1.0`; checker07 was `opensip-ts-boundary-trial` `0.4.0` |
| Lock packages | Non-root `package-lock.json` records **identical**; TS 6.0.3 / esbuild 0.28.2 unchanged |
| Hidden lock | `node_modules/.package-lock.json` root name/version updated to current package metadata (npm-provision02) |
| Tests | 5 stable names, 10 helpers, 9 fixtures via `tests/fixtures/staging-map.json` |
| Runner | New `tests/run.mjs`; `npm test` → `node tests/run.mjs` |

Ephemeral staging copies helpers to historical harness aliases (`checker/test/…`, `harness/…`, `baseline/…`, `inputs/…`) then deletes the directory. Old comparator implementations, dependency trees, and historical outputs are not product modules. Two helpers (`amd-cases.mjs`, `browser-cases.mjs`) replace an author home-directory Node path with `process.execPath`; the map records `upstreamSha256` matching checker07 review harness bytes.

Fixture architecture/inventory/approval JSON is **regression-only**. Fixture `design-lock.json` `ac65d09c…9143` is **not** the live product lock `37169104…afef`.

## Runner

`tests/run.mjs` requires macOS + Node v24.16.0. It `realpathSync`s a `/tmp/opensip-boundary-tests-*` directory (not `os.tmpdir()`, which on this host is `/var/folders/...` and broke `/tmp` alias CLI checks). It creates `results/`, copies src/bin/package files, **symlinks** already-provisioned `node_modules` (no install), verifies every map row’s sha256/bytes, rejects absolute/`..` paths and duplicate `stagePath`, then `spawnSync(process.execPath, ['--experimental-import-meta-resolve', '--no-warnings', '--test', ...])` with `OPENSIP_BOUNDARY_CHECKER` pointing at the staged CLI. `finally` `rmSync`s the staging tree. `process.exitCode = result.status ?? 1`.

Preserved first attempt (`tests01-runner.mjs` / `tests01.stdout`): **218/224**. Six failures were harness setup: missing `results/`, `os.tmpdir()` vs `/tmp` alias, and missing `--experimental-import-meta-resolve`. `tests02` **224/224**. npm-provision01 default-cache **ENOTCACHED** retained; npm-provision02 explicit prior-cache offline `ci` succeeded; lock package records unchanged.

## Reproduction (private copy)

Node v24.16.0, no installs:

```
node tests/run.mjs   # package.json "test" script
```

**224/224 pass, fail 0, exit 0.** No leftover `/tmp/opensip-boundary-tests-*`. Installed typescript 6.0.3 and esbuild 0.28.2.

Independent runner controls **12/12**: map 5+10+9 and unique relative paths; two execPath adaptations and no `/Users/` in those files; runner has `results/`, `/tmp`, import-meta-resolve flag, `finally` cleanup, and `exitCode` from spawn status; a failing `node --test` is nonzero; staging is removed after a thrown error.

## Must-fix / should-fix

None in this packaging-delta scope.

## Advisories

- **P-01:** Staging is always deleted, including on failure, so a failed run leaves no on-disk harness tree. Acceptable for a disposable alias stage; debug from captured stdout.
- **P-02:** Developer regression profile is macOS + Node 24.16.0 only, including real `/tmp` alias behavior.

## Remaining (not completed)

Tooling inventory/bootstrap/compiler-loader policy selection; product installation of `@opensip/typescript-boundary`; M1; fresh blind consumer B; release. Generator04 root reproduction is a separate archive/integration track and is not public activation of this checker.

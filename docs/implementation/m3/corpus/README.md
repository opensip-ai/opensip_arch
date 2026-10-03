# M3 T2 corpus manifest: draft (unit M3-T2a)

2026-10-03 (UTC). Drafted by the M3-T2a implementer for Claude Opus 5.5, the implementation lead. **Draft for review.** D3, the T2 selection, is lead work and needs owner sign-off (AQP:524). Nothing here is signed off.

**Authority:** AQP §4.1 and §4.2 (`docs/implementation/m3/analysis-quality/PLAN.md` r4, AQP:199-224), D3, D9 and D15 (AQP:524-537), and the M3-T2 row of `docs/implementation/m3/M3-PLAN.md` r4 (line 156). Neither plan names a manifest path or schema, so this unit proposes both:
- `t2-corpus-manifest.draft.json`, kind `opensip-t2-corpus-manifest`, schema `1-draft`;
- this README.

## What is pinned

There are 36 repositories and 4 multi-repo workspaces. Every repository is pinned to its default-branch HEAD as observed at 2026-10-03T06:09:17Z. For each repository:
- **Five-way pin agreement.** `git ls-remote`, a shallow clone, and the GitHub REST commit endpoint agree on the commit SHA. The clone and the API agree on the git tree SHA. All 36 match.
- **Licence:** GitHub's `license.spdx_id`, plus the SPDX expression read from the root licence files and the manifest `license` fields.
- **Size:** counted from the blobs at that commit (method below).

T2a is the **medium** class: 19 repositories and one workspace. Everything else is pinned as a **T2b candidate**, which was cheap to add, and T2b can still change it.

| Group | Small | Medium (T2a) | Large | Very large |
|---|---|---|---|---|
| Rust | tower (dev), anyhow (**held-out**) | serde, serde-json, tokio, axum, aws-lambda-rust-runtime, hyper (dev); ripgrep (**held-out**) | smithy-rs (dev), rust-analyzer (**held-out**) | aws-sdk-rust (dev) |
| TS/JS | constructs, Next.js commerce (dev); body-parser (**held-out**) | express, vite, umami (Next.js), smithy-typescript, powertools-lambda-typescript (dev); axios (**held-out**) | typescript-eslint (dev), vitest (**held-out**) | aws-cdk, aws-sdk-js-v3 (dev) |
| Polyglot Rust+TS/JS | — | napi-rs (dev), tauri (**held-out**) | — | deno (dev) |
| Python (pinned, not analyzed; D9) | itsdangerous (dev), httpx (**held-out**) | boto3, botocore, fastapi (dev); healthchecks, a Django app (**held-out**) | netbox, a Django app (dev); zulip, a Django app (**held-out**) | none |

**Counting rule.** A polyglot entry counts toward both Rust and TS/JS.
- **Rust:** small 2, medium 9, large 2, very large 2.
- **TS/JS:** small 3, medium 8, large 2, very large 3.
- **Python:** small 2, medium 4, large 2, very large 0.

**Multi-repo workspaces (D15).** Cross-repository edges are taken from the member manifests at the pinned commits.

| Workspace | Members | Edges | Class | Tranche |
|---|---|---|---|---|
| `mr-rs-medium-serde-json` | serde, serde-json | json → serde, serde_core, serde_derive (Cargo version) | medium (65.8k) | T2a |
| `mr-rs-large-aws-lambda-tokio` | aws-lambda-rust-runtime, tokio, tower, hyper, axum | the Lambda runtime → all four; axum → tokio, tower, hyper; tower, hyper → tokio | large (316k) | T2b candidate |
| `mr-ts-large-smithy-powertools` | smithy-typescript, powertools-lambda-typescript | powertools → five `@smithy/*` packages (npm range) | large (227k) | T2b candidate |
| `mr-ts-very-large-sdk-cdk` | smithy-typescript, aws-sdk-js-v3, constructs, aws-cdk | sdk → `@smithy/*`; cdk → `@aws-sdk/*`, `@smithy/*`, constructs | very large (2.4M) | T2b candidate |

These are the T2 approximation that AQP:217 asks for: "the Rust and TS AWS SDK and runtime repositories". All members of a workspace share one role, and no held-out repository is a member of a dev workspace. The builder asserts this.

## Selection rationale against AQP §4.2

**Rust shapes (AQP:214).**
- **Single crate:** hyper, serde-json, anyhow.
- **Mid-size Cargo workspace:** serde, axum, ripgrep, aws-lambda-rust-runtime.
- **Large workspace with proc-macros and build scripts (L-RS3):** smithy-rs and rust-analyzer. tokio, axum, serde, napi-rs and tauri add proc-macro crates at medium size.
- **cfg- and feature-heavy:** aws-lambda-rust-runtime (72 cfg sites/kloc; event types are feature-gated), hyper, serde-json and napi-rs. tokio's gating goes through `cfg_*!` macro wrappers, which the site count understates, so its tag is a judgement.
- **Trait and generic dispatch (L-RS2):** tower, axum and serde. This is a judgement; it can't be measured from the tree.
- **Generated code:** aws-sdk-rust, where 34.3M lines are marked `@generated`.
- **Broken or partial build:** this is a harness control (AQP §5.1), derived from a pinned tree, not a selected repository.

**TS/JS shapes (AQP:215).**
- **Project references:** vite, powertools, typescript-eslint, vitest, aws-cdk, napi-rs and deno.
- **Workspace monorepos:**
  - pnpm: vite, umami, typescript-eslint, vitest, tauri;
  - npm: powertools;
  - yarn: smithy-typescript, aws-cdk, aws-sdk-js-v3, napi-rs.
- **Framework entry points (L-FW1):** umami and commerce (Next.js App Router), and vite's `playground/`, which has 134 `vite.config` files.
- **JS with no tsconfig (L-JS1):** express (CommonJS only) and body-parser.
- **Mixed CJS/ESM** in non-test sources: smithy-typescript, napi-rs, vitest, typescript-eslint, aws-cdk and aws-sdk-js-v3.
- **`allowJs`/`checkJs`:** vite and typescript-eslint.

**Polyglot (AQP:216).** napi-rs and tauri pair a Cargo workspace with a JS workspace at medium size, and deno does so at very large size. The `mixed-native-partial` reference (NE:1233) needs one of them run with one half's inputs withheld; that is a harness control.

**Held-out (AQP:219).** At least one per language per class, small to large, as listed above. Two rules guided the choices:
- the held-out set is kept out of every dev workspace;
- it is spread across distinct shapes: ripgrep (a self-contained workspace), axios (ESM with hand-written `.d.ts`), tauri (polyglot with mobile glue), rust-analyzer, vitest and body-parser.

The very-large class has no held-out entry, because AQP:219 asks only for small to large.

**Lead additions.** AQP:221 says the candidates are "for review", so these repositories, which are not on its list, are proposed: hyper, axios, smithy-typescript, powertools-lambda-typescript, napi-rs, tauri, deno, aws-sdk-rust, constructs, body-parser, vitest, itsdangerous, httpx, healthchecks, netbox and zulip.
- **For the AWS multi-repo shape:** smithy-typescript, powertools, aws-sdk-rust and constructs.
- **For the polyglot shape:** napi-rs, tauri and deno.
- **To meet two per class and a held-out entry:** the rest.

Express and a "Next.js application" come from the plan's own list.

## Size method

Physical lines of git blobs at the pinned commit, read with `git cat-file --batch`, so no checkout, filter or hook is involved.
- **The size basis** is the hand-written lines of the entry's language group: `.rs` for Rust; `.ts .tsx .mts .cts .js .jsx .mjs .cjs` for TS/JS (including `.d.ts`); `.py .pyi` for Python. A polyglot entry counts both Rust and TS/JS.
- **Classes** follow AQP:218: < 20k, 20k–200k, 200k–1M, and > 1M.
- **Vendored and generated** lines are classified by path, root `.gitattributes` `linguist-*` rules and first-KiB markers, then reported separately and excluded from the basis.
- **Tests and examples** are counted within hand-written lines and also reported on their own line.

`sizeMethod` in the manifest gives the exact rules. The classifier is a heuristic. Two consequences:
- **One manual override:** aws-sdk-rust is wholly codegen, but 285.6k of its lines lack the `@generated` marker.
- **Not yet recorded:** the workload-manifest fields from AQP §5.1 (files, packages, edges, dependency count) need the harness, so they are not here.

## How the harness fetches and verifies

This follows AQP:207: `corpus fetch` is a harness step, never a product command.
1. **Fetch.** For each entry, fetch exactly `commit` from `url`. A fetch by SHA (`git fetch --depth 1 <url> <commit>`) works against GitHub.
   - No checkout filters or hooks run, and LFS smudge is off.
   - Submodules are not materialized: deno's 5 gitlinks are pinned by SHA inside the tree.
   - The bytes go only into the runner's content-addressed corpus store. Nothing is vendored into any repository.
2. **Verify** both digests, and refuse the entry on any mismatch:
   - the git tree SHA-1 of the fetched commit must equal `gitTree`;
   - `opensip-t2-content-sha256/1-draft`, recomputed from the stored blobs, must equal `contentDigest.value`.

   The content digest is defined in the manifest, and adds a SHA-256 check over the same bytes the tree SHA-1 commits to. It was cross-checked with a second, independent implementation by SHA fetch on anyhow, and both the tree and the digest matched.
3. **Run.** Exploratory and qualification runs then read the store read-only and offline (AQ:346; QG:117). A run whose bytes don't match refuses.
4. **Workspaces.** These are assembled by a harness-generated overlay (Cargo `[patch]` or package-manager link overrides), recorded by digest. T2b defines it, and no member source is copied or edited.

## Licences

All 36 are permissive. Each entry records its SPDX expression, GitHub's detection and the evidence. Flags:
- **ripgrep:** `Unlicense OR MIT`. OpenSIP relies on the MIT branch.
- **powertools-lambda-typescript:** MIT-0 (no attribution clause). Its private root `package.json` says MIT.
- **aws-lambda-rust-runtime:** `Apache-2.0 AND MIT`, because the `lambda-events` crate is MIT.
- **napi-rs:** GitHub reports NOASSERTION, but the LICENSE text is MIT.
- **deno:** MIT, but its 5 submodules (deno_std, wpt, node_test, lsp_benchdata, lzld) carry their own licences and are not fetched. A WTFPL `left-pad` sits under `tests/testdata`.
- **GitHub reports only one side of these dual licences:** anyhow, serde, serde-json, rust-analyzer and tauri. Each is `MIT OR Apache-2.0` per its own files.
- **Fixture-only licence fields,** not substantive: CC0-1.0 and ISC in vite's licence-plugin fixtures, MIT in aws-cdk's snapshot assets, and UNLICENSED on the private root packages of smithy-typescript and aws-sdk-js-v3.

## Open items

1. **Python very large:** no candidate is pinned. django/django measured 531k, which is large. AQP:218's two-per-class rule is not met here.
2. **Rust very large** is only aws-sdk-rust plus deno, the polyglot entry. aws-sdk-rust is all codegen, so a hand-written very-large Rust repository is still missing.
3. **Boundary entries.** Each is classed by the measured count; T2b may re-balance:
   - tokio (185k) and napi-rs (167k) sit near the medium/large line;
   - boto3 (20.7k) and serde-json (23.2k) sit near the small/medium line;
   - express is medium by lines, but 87% of it is tests and examples.
4. **Judged shape tags** (`shapeTagsJudged`) need review: L-RS2 dispatch, cfg macro wrappers, and the Next.js App Router.
5. **aws-lambda-rust-runtime** now lives at `github.com/aws/aws-lambda-rust-runtime`; the API redirects. The manifest keeps the awslabs URL as `url` and records `canonicalUrl`. T2b should switch to the canonical URL.
6. **Fetch costs:** aws-cdk has 1.19 GB of blobs and Git LFS rules for snapshot zips (pointers only are pinned); aws-sdk-js-v3 has 615 MB; aws-sdk-rust took about 55 s to clone.
7. **GitHub signature checks:** the GitHub API reports the boto3 and botocore HEAD commits as unsigned. This is informational only, because the pin is the SHA.
8. **Still to do:** D3 owner sign-off, the T2b review of every candidate, and the FW-14 outputs (M3-PLAN line 156).

## Reproducing

The metadata came from GitHub only:
- `git ls-remote`;
- a shallow `--no-checkout` clone into a private temp dir under `$(getconf DARWIN_USER_TEMP_DIR)`, deleted afterwards;
- unauthenticated REST calls to `/repos/{o}/{r}` and `/repos/{o}/{r}/commits/{sha}`.

No repository code was executed, and nothing was cloned into any repository. The measuring and builder scripts were session tooling and are not committed. The manifest's `sizeMethod`, `tagMethod` and `contentDigestAlgorithm` define every computed field.

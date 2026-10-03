# GROK2 review: M3-T2a T2 corpus manifest, r1

**Verdict: ACCEPT.**

Fact review of the draft T2 manifest for the M3-T2 row's T2a sub-unit (M3-PLAN.md:156, r4 accepted) under AQP §4.1–4.2 (analysis-quality/PLAN.md:199-224, r4 accepted) and D3, D9, and D15 (AQP:524-537). No product cargo or test run. `~/Library/Application Support/OpenSIP` is absent. Fetches used a private directory under `DARWIN_USER_TEMP_DIR`, with `core.hooksPath` empty of repository hooks, no checkout, and no repository code. That directory was deleted after the checks below.

## Subjects

| File | Bytes | SHA-256 |
|---|---:|---|
| `docs/implementation/m3/corpus/t2-corpus-manifest.draft.json` | 113550 | `09fef028463e13e8cad35bec98749ea44e33e0c2b2b2212d1f93ecd41829bca5` |
| `docs/implementation/m3/corpus/README.md` | 12017 | `2f169042017ff9f5fb6233ce4e3be0b48f3e3f8a613557bc4ac3d8e913523160` |

## Pins

All 19 repositories with `tranche` = `T2a` were fetched with `git fetch --depth 1 <url> <commit>`. For each one, the fetched commit equals `commit`, `FETCH_HEAD^{tree}` equals `gitTree`, and `git ls-remote` HEAD equals `commit`. The awslabs URL recorded for `rs-medium-aws-lambda-rust-runtime` fetched that pinned commit.

The same three checks matched this T2b sample: anyhow, tower, body-parser, constructs, itsdangerous, httpx, rust-analyzer, deno, and aws-sdk-rust. Deno and aws-sdk-rust were blob-filtered fetches; their commits and trees still matched. Deno's five gitlinks are `tests/util/std` (deno_std), `tests/wpt/suite` (wpt), `tests/node_compat/runner/suite` (node_test), `tests/bench/testdata/lsp_benchdata`, and `tools/lzld`.

`contentDigest.value`, `treeEntries`, and `blobBytes` were recomputed from `contentDigestAlgorithm` and matched for:

- anyhow: `ffcc085dc35e13c6bc9a568f116f593866d9b5a922ad1a05e762f9c2634b1074`, 54 entries, 222831 bytes
- serde-json: `99f3b49def0190d344be0cfa65ac5e14dce4d8e8c971117a92d971d54071a869`, 92 entries, 737131 bytes
- express: `0b5fa65cd5a8be9280736a25dedc3f50cf993d41ba297a2b07ff845c03ca0e11`, 214 entries, 717115 bytes

## Selection

T2a is those 19 medium repositories and `mr-rs-medium-serde-json`. The other three workspaces are T2b candidates. Member hand-written lines sum to the workspace totals 65778, 316001, 227156, and 2402399. Every workspace role is dev, and no held-out id is a member.

Counting a polyglot entry toward both Rust and TS/JS, as the README states, gives Rust 2/9/2/2, TS/JS 3/8/2/3, and Python 2/4/2/0 for small, medium, large, and very large. Held-out coverage is at least one repository per language for small through large. `analyzedAtM3` is false on all eight Python repositories. `productExecution` is false. Fetch is a separate harness step, vendoring is none, and every entry records an SPDX expression.

The §4.2 shapes named in the README are on the measured tags, or on `shapeTagsJudged` where the README calls the tag a judgement. The two `tagMethod` predicates agree with `shapeEvidence` on every entry. `rs-cfg-feature-heavy` is present only at or above 15 cfg sites per 1,000 hand-written Rust lines or 75 Cargo feature declarations. `js-mixed-cjs-esm` is present only on tsjs and polyglot entries whose non-test evidence includes both module styles. Tokio's cfg tag is judged: 11.4 sites per 1,000 lines and 49 features. The four workspaces are the D15 approximation, including the Rust Lambda/tokio stack and the TypeScript smithy/sdk/cdk stack. `mixed-native-partial` (NE:1233) is left as a harness control, which matches the README.

## Size

Recounts with the stated physical-line rules matched the manifest for serde-json (23217), boto3 (20745), express (21492, of which 18717 are tests or examples, 87%), and anyhow (5857). serde-json's cfg and feature counts matched (376 and 15), as did anyhow's (113 and 6). Tokio and napi-rs stay medium; the bucket split is NBO-2. aws-sdk-rust is very-large with `classOverride` true. Its hand-written Rust count, 285639, would be large, and the manifest records 34257272 generated Rust lines. The pin and the Apache-2.0 `LICENSE` were checked. The generated-line total was not recounted. Open item 2 already says a hand-written very-large Rust repository is still missing, and open item 1 is right that Python very large is unmet.

## Licences

Root licence files and manifest `license` fields support `licence.spdx` for every T2a entry and for the T2b sample. Each recorded expression is permissive: MIT, MIT-0, Apache-2.0, BSD-3-Clause, `Unlicense OR MIT`, `MIT OR Apache-2.0`, `Apache-2.0 OR MIT`, or `Apache-2.0 AND MIT`.

The README flags match the files and, where the flag is about GitHub's detection, the licence API:

- ripgrep has `UNLICENSE`, `LICENSE-MIT`, and a `COPYING` that states the dual licence. Cargo.toml says `Unlicense OR MIT`. The API reports Unlicense.
- powertools `LICENSE` is the MIT grant without an attribution clause. Seventeen `package.json` files say MIT-0. The root `package.json` says MIT.
- aws-lambda-rust-runtime: `lambda-events` is MIT and the other five crates are Apache-2.0.
- napi-rs `LICENSE` is MIT text. The API reports NOASSERTION.
- deno `LICENSE.md` is MIT. The five gitlinks above were not materialized. `tests/testdata/commonjs/node_modules/left-pad/package.json` says WTFPL.
- anyhow, serde, serde-json, and rust-analyzer are `MIT OR Apache-2.0` in their own files. Tauri's files and Cargo.toml say `Apache-2.0 OR MIT`. The API reports Apache-2.0 for all five.
- vite's CC0-1.0 and ISC texts are under `packages/vite/src/node/__tests__/plugins/fixtures/license/`.
- smithy-typescript's root `package.json` is UNLICENSED and the other 64 say Apache-2.0.
- aws-sdk-js-v3's root `package.json` at the pinned commit is private and UNLICENSED.
- aws-cdk's root `package.json` at the pinned commit is Apache-2.0. The snapshot asset `packages/@aws-cdk-testing/framework-integ/test/aws-lambda-nodejs/test/integ.latest.js.snapshot/asset.2729d9b4af60cbbbe3182f0002dec1747647eedd8de3761325aa38f7ddf73f24/node_modules/delay/license` is MIT.

A `(MIT OR GPL-3.0-or-later)` string in powertools is in `package-lock.json`. That is dependency metadata. The repository licence is MIT-0.

## Open items

Open items 1 through 8 match the manifest: Python very large is unmet, Rust very large has no hand-written repository, the four boundary counts sit inside medium, judged tags are marked as judgements, the awslabs URL still fetches the pinned commit, and D3 is unsigned. Those disclosures are not required findings.

Required findings: none.

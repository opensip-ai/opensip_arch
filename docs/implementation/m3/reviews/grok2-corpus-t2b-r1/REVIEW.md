# GROK2 review: M3-T2b corpus manifest, r1

**Verdict: ACCEPT.**

Subjects, re-hashed at the close of this review:

| File | Bytes | SHA-256 |
|---|---:|---|
| `docs/implementation/m3/corpus/t2-corpus-manifest.draft.json` | 322483 | `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578` |
| `docs/implementation/m3/corpus/README.md` | 26701 | `3d355e72466e228f2021c0b6386b2d04576f44cf11637e9880edfa859ae5b2ac` |
| `docs/implementation/m3/corpus/FETCH-SPEC.md` | 10659 | `4ebe90a491721e48d252f11e6378b6c73312b506b59af89b24c03829416f8858` |

Context copies match the accepted T2a files: `t2-corpus-manifest-T2a.draft.json` 113550 bytes `09fef028463e13e8cad35bec98749ea44e33e0c2b2b2212d1f93ecd41829bca5`, `README-T2a.md` 12017 bytes `2f169042017ff9f5fb6233ce4e3be0b48f3e3f8a613557bc4ac3d8e913523160`. The manifest is `opensip-t2-corpus-manifest` schema `2-draft`, unit `M3-T2b`, 49 repositories, 5 workspaces, 33 families. `productExecution` is false. `~/Library/Application Support/OpenSIP` was absent. No cargo, tests, or repository code ran. Fetches were `nice -n 19` into a private 0700 directory under `DARWIN_USER_TEMP_DIR`, with `HOME` redirected and hooks off, and that directory was deleted after these checks.

## 1. Pins

All 13 new entries (`tranche` T2b, `observedAt` on 2026-10-04) were fetched and the commit and `gitTree` matched: webpack, rspack, node-rs, django, requests, airflow, home-assistant/core, http, http-body, hyper-util, sui, zustand, vscode. vite, vitest, aws-cdk, and aws-sdk-js-v3 were fetched the same way and matched. aws-lambda-rust-runtime's new `https://github.com/aws/aws-lambda-rust-runtime` URL and the awslabs alias URL both serve commit `5670a2ed2efae728bf01b4de78297b670696d225` and tree `a823c8d43083dd8eeea36f79b15bdf3577b4635f`.

The 36 ids shared with T2a keep T2a's commit, `gitTree`, and `contentDigest`. The only field change among them is that lambda URL.

Licence files and the GitHub licence API match `licence.spdx` for the 13 new entries. http is `MIT OR Apache-2.0` with both licence files present, and the API reports Apache-2.0. django is BSD-3-Clause plus `LICENSE.python` (PSF-2.0). home-assistant/core is Apache-2.0 plus `homeassistant/backports/LICENSE.Python` (PSF-2.0). requests' `ext/` is `ext/LICENSE` ("All rights reserved") plus logo images only (`kr.png`, `psf.png`, and the requests logos). `docs/_themes/LICENSE` is the two-clause redistribution text the README calls a BSD Flask theme. webpack's seven gitlinks are exactly `submodulePolicy.gitlinks`. rspack's only non-MIT `package.json` `license` fields are three ISC files, all under `tests/rspack-test/`. django's admin tree has `vendor/jquery`, `vendor/select2`, and `vendor/xregexp`. vscode's `extensions/copilot/LICENSE.txt` begins "MIT License", and the three notebook fixture `LICENSE` files begin "Apache License". ansible's API result is GPL-3.0 and servo's is MPL-2.0. All 49 recorded `licence.permissive` values are true and every `licence.spdx` is a permissive expression. sui's docs CC-BY-4.0/CC0 claim and the "3 MIT / 2 ISC example manifests" count were not re-scanned file by file.

## 2. Digests

Recomputed from blob bytes with `git cat-file --batch`, SHA-256 of the raw bytes, and `json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(',', ':'))` without CAN's 4 MiB cap. `canonical()` in `foundation/canonical.py` is that serializer plus `MAX_BYTES = 4 * 1024 * 1024`. Importing the module needs `jsonschema`, which is not installed here, so the tree preimages used the same dumps parameters directly.

| Entry | Why | treeDigest | contentDigest | blobs / entries / bytes / symlinks |
|---|---|---|---|---|
| `rs-medium-serde` | symlinks (14) | match | match | 361 / 361 / 1331523 / 14 |
| `rs-medium-hyper` | symlink (1) | match | match | 139 / 139 / 1447869 / 1 |
| `js-large-webpack` | 7 gitlinks | match | match | 20693 / 20700 / 57599308 / 0 |
| `rs-small-http` | new entry | match | match | 48 / 48 / 588072 / 0 |

Webpack's seven gitlinks are the policy list, path and commit. Gitlinks are omitted from the QD-22 array and enter `contentDigest` as the recorded SHA-1.

`familyMapDigest` `686234c705735f960fc7299adeb74ee4040ce07bbccf58cb6876b0c1191d6ce7` and `heldOutSetDigest` `111902cc0bba91769dd6f8096bedf0cd705b5940b67d43391cd529c01147ebbc` match the same serializer. All five `overlayDigest` values match: serde-json, aws-lambda-tokio, smithy-powertools, smithy-sdk, and boto.

## 3. Selection

Under `languageClasses`, a polyglot entry counts toward Rust at its Rust class and toward TS/JS at its TS/JS class. The stored counts meet AQP6:224-226: at least two dev repositories per language in every class from small through very large, and at least one held-out repository per language from small through large. No held-out entry is very large. All 12 Python entries have `analyzedAtM3` false. sui's Rust hand-written basis is 1,253,517 (`classOverride` false). home-assistant/core (3,779,784) and airflow (1,743,284) are the two Python very-large entries. Polyglot entries sit in every combined class: node-rs small, napi-rs and tauri medium, rspack large, deno very large. No hand-written basis sits on 19999, 20000, 199999, 200000, 1000000, or 1000001. The only `classOverride` is aws-sdk-rust, whose hand-written Rust lines would be large and whose class is very large because of the generated Rust lines.

## 4. Families

Nine families have more than one member and 24 are single. Membership matches each repository's `family` field. No family contains both a held-out repository and a dev repository. The held-out set is anyhow, ripgrep, rust-analyzer, tauri, zustand, axios, vitest, httpx, healthchecks, and zulip, and none of those is a workspace member.

HD:516 puts repositories in one family when they are parts of one multi-checkout workspace assembly, and the parenthetical calls the D15 approximation one family. Read against AQP6:223, that parenthetical is the then-single candidate, and the bullet is per assembly. T2b has five assemblies. The two TypeScript assemblies share smithy-typescript, so transitive closure puts them in `fam-smithy-typescript`. The serde assembly stays separate from the AWS Rust assembly. That reading holds.

Grounds that were checked against the trees:

- express at `7ef98448f8b38099ab1ded55e458538ad47a51e7` depends on `body-parser` `^2.3.0` and `lib/express.js` re-exports `bodyParser.json`, `raw`, `text`, and `urlencoded`. Merging them, and moving body-parser to dev so the family stays unmixed, is the rule the manifest states. zustand is the TS/JS small held-out replacement.
- constructs at `8264e196c3593a192dc79991f4d97c22ab4c08bf` has `"version": "0.0.0"`. Treating it as the CDK base library is a stated judgment (README open item 3). The version fact that blocks it as a workspace provider is true.
- rspack/webpack: 2978 shared source blob SHAs, of which 1896 have at least 3 physical lines, summing to 20179 lines once per SHA. Both recorded figures match. The two example path pairs are byte-identical (`cb0662ef…` and `deccad21…`). Material at 20,179 lines.
- vite/vitest: 4 shared source blobs of at least 3 lines, 16 lines total. The recorded pair matches. See NBO-1 for the README's "1-line" wording. Leaving them unmerged is within the stated thresholds (1,000 lines or 10,000 ppm).
- boto3 requires `botocore>=1.43.108,<1.44.0` and botocore's `__version__` is `1.43.108`. One shared blob of 43 lines is under the threshold; the family rests on the lockstep versions plus the workspace, which is what the manifest says.

The other shared-blob pairs (aws-sdk-rust/smithy-rs, aws-sdk-js-v3/smithy-typescript, napi-rs/node-rs, deno/rspack, lambda/smithy-rs, serde-json/anyhow) were not re-summed from blobs. Their recorded file and line counts are the manifest's, and the materiality rule as written is a defensible cutoff.

rust-lang/rust at `56343b1a7d3fed3f349a5c2dc474f65b504f5221` has `src/tools/rust-analyzer` as a tree (`040000`), not a gitlink. Excluding that repository because the analyzer is a subtree at that commit is correct.

## 5. Workspaces

Edges checked against the pinned manifests:

- lambda-runtime depends on tokio `1.46` with features; tokio's version is `1.53.1`.
- hyper-util depends on `tower-layer` `0.3` and `tower-service` `0.3`; both crates at tower `df06d70d` are version `0.3.3`. hyper is `1.11.1`. http is `1.5.0`.
- powertools `packages/testing/package.json` depends on `@smithy/util-utf8` `^4.5.2`; smithy `packages/util-utf8/package.json` is `4.5.2`.
- The boto3/botocore pair above is satisfied.

`mr-ts-very-large-smithy-sdk` has 58 edges: 8 `all`, 12 `some`, 36 `none`, 2 `unknown`. Every `none` edge is a dependency from aws-sdk-js-v3 on a `@smithy/*` package. Across all 604 `package.json` files, every declaring path for those 36 packages is under `reserved/packages/`, the declaration counts equal `declaringManifests`, and the requirement strings equal the recorded requirements (all unsatisfied `^1.0.x` against provided 4.x/5.x). None are declared outside that directory.

aws-cdk and constructs are absent from that workspace. The pin facts are in NBO-2: the bulk of `@aws-sdk/*` is exact `3.632.0` against aws-sdk-js-v3 at `3.1146.0` (`clients/client-s3` and `clients/client-inspector2` are both `3.1146.0`), `@smithy/*` is exact 3.x, and constructs is `0.0.0`. Those are sufficient reasons for the recorded edges not to resolve inside a workspace that also contains current aws-sdk-js-v3 and smithy-typescript. The one `^3` range is the dependency a "1 of 34" resolvable edge would be. This review did not rebuild the dropped workspace's 34 edges from scratch.

Hand-written line sums of the five overlays match `sizeBasisHandWrittenLines` (65840, 356703, 227434, 1160901, 127608).

## 6. NBO-1 and NBO-2 from T2a

AQP6:224 says small (&lt; 20k lines), medium (20k–200k), large (200k–1M), and very large (&gt; 1M). The manifest's integer intervals keep the two strict bounds: small is 0–19,999, very large starts at 1,000,001, and 1,000,000 is large. The shared endpoint 200,000 is assigned to large, by the same lower-inclusive step that puts 20,000 in medium, and the manifest says so. No entry lies on either endpoint. That is a correct disclosed reading. T2a's table had put 1,000,000 in very large; the basis changes in the README do not move any T2a class.

`generatedMarkerRule` id `opensip-t2-generated-marker/2` was applied to tokio and napi-rs. Tokio Rust hand-written is 185,227, generated 0, vendored 0, over 808 files. napi-rs TS/JS hand-written is 72,694 and generated 8,032 over 232 files. Both stored buckets match. tokio has no `.gitattributes`. napi-rs's only linguist attribute is `linguist-detectable=false` on `.yarn/releases/*.js`, so those stay hand-written, as the README says.

The five files the README names as rule-1-only were fetched and matched rule 1 in the first 1,024 bytes and none of M1–M6:

- `sui-execution/src/lib.rs`: `// DO NOT MODIFY, Generated by ./scripts/execution-layer`
- `crates/sui-fork/src/gql/queries.rs`: `//! Most of these query types are generated by cynic`
- `crates/rspack_cacheable/src/utils/owned_or_ref.rs`: `// The following code is generated by`
- rspack and webpack `harmony-commonjs/index.js`: a comment that the following is generated code by babel

M2 is the phrase "do not edit", so "DO NOT MODIFY" does not fire, and M4 requires `generated by` at the comment start. Classifying these five as rule-1-only is what the published regexes do. The corpus-wide totals (146 files / 37,883 lines / 25 repositories, and 36 files / 28,191 lines / 6 repositories) were not re-walked. That walk would read the aws-sdk-rust and aws-cdk blobs. The named files and the two full-repo buckets agree with the rule.

## 7. Fetch spec

`FETCH-SPEC.md` matches AQP6:213 and HD:1117-1133 on the points this review was asked to check. `corpus fetch` is a harness step outside every measured run, the only networked corpus step. It runs no repository code, smudge filters, or submodule update, and it writes only to the runner's content-addressed store. Submodules and LFS are explicit: deno's 5 and webpack's 7 are `exclude-pinned` (webpack's 7 were checked above), and LFS stays pointer text. A run re-verifies `store/<treeDigest>/` before starting and has no network. HD §9.1 fields beyond the corpus-side `workloadSeed` are deferred by README open item 7; the spec does not pretend they are in this manifest.

**QD-22 and the 4 MiB limit.** Acceptable, and not a required finding. HD:1126 defines `treeDigest` as the SHA-256 of the canonical JSON array of `[path, mode, sha256(content)]`, sorted by path bytes. It does not say the preimage must pass CAN admission. CAN's 4 MiB cap is the admission limit in `canonical()` (`MAX_BYTES`). A digest preimage is not an admitted record. Applying the cap would make the aws-cdk and aws-sdk-rust digests uncomputable by that function, which the manifest and FETCH-SPEC §4 both say, with the sizes 5,942,722 and 35,318,302. Those two byte lengths were not re-derived here; serde's preimage was 45,341 bytes and webpack's was 2,862,134, under the cap, and both matched. Open item 4 correctly leaves a chunked form to K1a or the DR-G13 successor if that successor decides the preimage is bounded. The manifest does not amend HD.

## 8. Anything else

README open items 1–9 are disclosures. D3 is unsigned, the held-out set is too small for a Q2 PASS, npm and Python renderings are deferred, and the unsigned-commit note is informational. None of those claims was found false.

The judged calls in open item 3 are defensible on the facts above: constructs with aws-cdk, express with body-parser, vite kept apart from vitest, the 1,000-line / 1% copy threshold, and body-parser moving to dev.

NBO-1 and NBO-2 are wording in the README. The manifest numbers they sit next to are the ones the checks reproduced.

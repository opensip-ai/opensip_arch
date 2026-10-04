# M3 T2 corpus manifest: draft (units M3-T2a and M3-T2b)

2026-10-04 (UTC). Drafted by the M3-T2b implementer for Claude Opus 5.5, the implementation lead. **Draft for review.**
- **T2a** (the medium class and `mr-rs-medium-serde-json`) was accepted by GROK2 (`reviews/grok2-corpus-t2a-r1/`).
- **T2b** completes the manifest. It is a new review subject.
- **D3**, the T2 selection, still needs owner sign-off (AQP6:541). Nothing here is signed off.

**Short names:**
- **AQP6:** `docs/implementation/m3/analysis-quality/PLAN-r6.md`, the accepted r6 snapshot (sha256 `8aed6eb8…`).
- **HD:** `docs/implementation/m3/harness/DESIGN-r13.md`, the accepted r13 snapshot (sha256 `37438317…`).
- **M3-PLAN:** `docs/implementation/m3/M3-PLAN.md` (r4, accepted). The M3-T2 row is line 156.
- **CAN:** `docs/coop/design-corrections/foundation/canonical.py`.

**Authority:**
- AQP6 §4.1–4.2 (AQP6:205-230);
- D3, D9 and D15 (AQP6:541, 548, 554), and D9's timing (AQP6:463);
- the M3-T2 row (M3-PLAN:156);
- the harness design's requirements on the manifest: HD §1.4 (`family`, `heldOut`; HD:253-255), §5.3 (families; HD:511-523), §9.1 (workloads; HD:776-787) and §10 (`corpus fetch`, QD-22; HD:1117-1135).

## Files

| File | What it is |
|---|---|
| `t2-corpus-manifest.draft.json` | The manifest: kind `opensip-t2-corpus-manifest`, schema `2-draft`, unit `M3-T2b`. It holds 49 repositories, 5 multi-repo workspaces and 33 independence families. |
| `FETCH-SPEC.md` | The harness-only `corpus fetch` specification, including workspace assembly |
| `README.md` | This file |
| `t2-corpus-manifest-T2a.draft.json`, `README-T2a.md` | Byte copies of the accepted T2a files (sha256 `09fef028…` and `2f169042…`; git `b680a21a5`), kept as snapshots like `PLAN-r6.md` |

## What is pinned

**Pins.**
- T2a's 36 pins are unchanged.
- Each of the 13 new repositories is pinned to its default-branch HEAD as observed between 2026-10-04T06:48:51Z and 06:49:35Z. `git ls-remote`, the fetched commit and the REST commit endpoint agree on the commit; the fetch and the API agree on the tree.
- All 49 pins were then fetched again by SHA and re-digested, three times; the final run was 07:06:34Z to 07:10:24Z. All three runs gave identical commits, trees and digests. Every T2a `contentDigest`, entry count and byte count reproduced exactly.

**Each entry carries:**
- `commit` and `gitTree`;
- the QD-22 `treeDigest`, which is what `corpus fetch` keys and verifies on (HD:1126);
- T2a's `contentDigest`;
- licence, `family`, `heldOut`, `submodulePolicy` and `lfsPolicy`;
- size, per-language classes, shape tags and evidence;
- a corpus-side `workloadSeed`.

Roles are in parentheses; HO means held-out. A polyglot entry is listed under its combined class.

| Group | Small | Medium | Large | Very large |
|---|---|---|---|---|
| Rust | tower, **http, http-body, hyper-util** (dev); anyhow (HO) | serde, serde-json, aws-lambda-rust-runtime, hyper, axum, tokio (dev); ripgrep (HO) | smithy-rs (dev); rust-analyzer (HO) | aws-sdk-rust, **sui** (dev) |
| TS/JS | constructs, Next.js commerce, body-parser (dev); **zustand** (HO) | express, vite, umami, smithy-typescript, powertools-lambda-typescript (dev); axios (HO) | typescript-eslint, **webpack** (dev); vitest (HO) | aws-cdk, aws-sdk-js-v3, **vscode** (dev) |
| Polyglot Rust+TS/JS | **node-rs** (dev) | napi-rs (dev); tauri (HO) | **rspack** (dev) | deno (dev) |
| Python (pinned, not analyzed; D9) | itsdangerous, **requests** (dev); httpx (HO) | boto3, botocore, fastapi (dev); healthchecks (HO) | netbox, **django** (dev); zulip (HO) | **home-assistant/core, airflow** (dev) |

New in T2b in **bold**. body-parser moved from held-out to dev (see Families).

### Counts per language and class

**Counting rule (changed in T2b).** A polyglot entry counts toward Rust at the class of its own Rust lines, and toward TS/JS at the class of its own TS/JS lines (`languageClasses`). T2a counted it at the combined class.
- deno now counts as Rust large (680k) and TS/JS large (534k), not very large in both.
- tauri counts as Rust medium (106k) and TS/JS small (14k).

Each cell gives dev repositories (dev families) / held-out repositories.

| Language | Small | Medium | Large | Very large |
|---|---|---|---|---|
| Rust | 5 (2) / 1 | 7 (3) / 2 | 3 (3) / 1 | 2 (2) / 0 |
| TS/JS | 4 (4) / 2 | 6 (5) / 1 | 4 (3) / 1 | 3 (3) / 0 |
| Python | 2 (2) / 1 | 3 (2) / 1 | 2 (2) / 1 | 2 (2) / 0 |

**The rules the counts meet:**
- **Two dev repositories per language per class, small to very large.** The T2b brief asks for two *dev* repositories, which is stricter than AQP6:224's two in total.
- **One held-out repository per language per class, small to large** (AQP6:225).
- AQP6:225 asks for no held-out repository at very large.

The builder refuses a manifest that misses either rule. `counts` in the manifest lists the ids.

**Held-out set (10):** anyhow, ripgrep, rust-analyzer, tauri, zustand, axios, vitest, httpx, healthchecks and zulip. Each is its own family, contains no dev repository, and is in no workspace. `heldOutSetDigest` is offered for cross-checking; the freeze's own digest is K1a's (HD:269).

## Selection rationale

T2a's §4.2 coverage stands (see `README-T2a.md`). T2b adds the following.

**Rust (AQP6:220).**
- **Very large, hand-written: MystenLabs/sui.** It has 1,253,517 hand-written Rust lines in a 220-manifest Cargo workspace, with proc-macros, build scripts and 123 feature declarations. This closes T2a open item 2.
- **Very-large candidates screened** by GitHub's languages API, in bytes of Rust:

  | Repository | Rust bytes | Outcome |
  |---|---|---|
  | rust-lang/rust | 148.5 MB | not selected (below) |
  | sui | 45.8 MB | selected |
  | aptos-core | 32.3 MB | — |
  | risingwave | 31.3 MB | — |
  | tikv | 26.7 MB | — |
  | agave | 25.2 MB | — |
  | servo | 21.3 MB | MPL-2.0, flagged |
  | bevy | 20.5 MB | large, not very large (about 0.55M lines) |

- **Why not rust-lang/rust.** At HEAD `56343b1a` (ls-remote 2026-10-04, trees-only fetch), `src/tools/rust-analyzer` is a tree, not a gitlink: a subtree copy of rust-lang/rust-analyzer, which is held-out. Under HD §5.3 that is a vendored copy, so the two would share a family, and a held-out family may not contain a dev repository. It is also atypical: an unstable-feature compiler with a bootstrap build. It is recorded in `selectionRules.consideredNotSelected`.
- **Large: rspack** (polyglot; 371k Rust).
- **Small: hyperium/http, http-body and hyper-util**, chosen for D15 (below).

**TS/JS (AQP6:221).**
- **vscode** (4.49M lines) is a hand-written, non-AWS very-large entry. The other two very-large entries are AWS, and aws-sdk-js-v3 is mostly codegen.
- **webpack** is large JavaScript with JSDoc types checked by `tsc` (`checkJs`), mixed CommonJS/ESM, and 7 test submodules.
- **zustand** replaces body-parser as the small held-out entry (see Families). tj/commander.js was measured at 20,642 lines, just medium, and was not selected.

**Polyglot (AQP6:222).** The shape is now present at every class:
- node-rs (small; napi bindings);
- napi-rs and tauri (medium);
- rspack (large);
- deno (very large).

**Python (D9; AQP6:463).** Pinned only; `analyzedAtM3` is false on all 12 Python entries.
- **Small:** requests.
- **Large:** django (527k).
- **Very large:** home-assistant/core (3.78M; `Apache-2.0 AND PSF-2.0`) and apache/airflow (1.74M; Apache-2.0). This closes T2a open item 1.
- **Screened** (bytes of Python):

  | Repository | Python bytes | Outcome |
  |---|---|---|
  | home-assistant/core | 126.3 MB | selected |
  | airflow | 70.4 MB | selected |
  | salt | 34.5 MB | borderline |
  | sympy | 27.7 MB | large |
  | pandas | 25.2 MB | large |

- **ansible/ansible** is GPL-3.0 per GitHub's licence API, so it is flagged and not used. It is recorded in `selectionRules.consideredNotSelected`, with servo (MPL-2.0) and rust-lang/rust.

## Independence families (HD §5.3)

The cluster-aware bound counts families, not repositories (HD:492). Acceptance counts only held-out families (HD:600). T2b assigns every entry a `family` and closes OI-16 (HD:1258) for review.

**Rules** (HD:511-519). Repositories share a family when any of these holds:
- one is a fork, mirror, vendored copy or split of another;
- they share generated code from the same generator;
- they are parts of one multi-checkout workspace;
- they share an upstream project.

Sharing an organization alone does not merge. The builder takes the transitive closure.

**Lead readings:**
- **A shared generator merges only when its output is material.** That covers aws-sdk-rust, aws-sdk-js-v3 and node-rs. Glue under 1% of a repository's analyzed lines does not merge: rspack's napi bindings are an example.
- **A byte-identical copy counts only when material:** at least 1,000 lines, or 1% of the smaller repository's analyzed lines.
- **No family mixes held-out and dev repositories.** The builder refuses one that would.

**Shared-blob check.** Every pair of the 49 repositories was compared by git blob SHA, over Rust, TS/JS and Python files of 3 or more lines in any path. `familyRules.sharedBlobPairs` lists all 9 pairs that share anything.

| Pair | Files | Lines | Material |
|---|---:|---:|---|
| aws-sdk-rust / smithy-rs | 565 | 166,470 | yes |
| rspack / webpack | 1,896 | 20,179 | yes |
| aws-sdk-js-v3 / smithy-typescript | 47 | 10,530 | yes |
| napi-rs / node-rs | 3 | 1,008 | yes |
| boto3 / botocore | 1 | 43 | no; merged on other grounds |
| vite / vitest | 4 | 16 | no |
| deno / rspack | 1 | 11 | no |
| aws-lambda-rust-runtime / smithy-rs | 1 | 8 | no |
| serde-json / anyhow | 1 | 7 | no |

Held-out repositories share at most 16 lines with anything: vitest's three tiny test fixtures and a 1-line `import-meta.d.ts` shim from vite.

**Multi-member families.** The other 24 families are single repositories.

| Family | Members | Grounds |
|---|---|---|
| `fam-rust-aws-runtime` | aws-lambda-rust-runtime, tokio, tower, hyper, axum, http, http-body, hyper-util | workspace `mr-rs-large-aws-lambda-tokio` |
| `fam-serde` | serde, serde-json | workspace `mr-rs-medium-serde-json` |
| `fam-smithy-rs` | smithy-rs, aws-sdk-rust | shared generator; vendored copy (166k identical lines) |
| `fam-smithy-typescript` | smithy-typescript, powertools-lambda-typescript, aws-sdk-js-v3 | both TS workspaces; shared generator |
| `fam-aws-cdk` | aws-cdk, constructs | shared upstream project (judged: constructs is the CDK project's base library) |
| `fam-express` | express, body-parser | shared upstream project (judged): express depends on body-parser ^2.3.0 and re-exports its parsers (`lib/express.js`: `exports.json = bodyParser.json`) |
| `fam-napi-rs` | napi-rs, node-rs | shared generator (51% of node-rs's analyzed lines are napi-rs CLI output); shared upstream |
| `fam-webpack` | webpack, rspack | vendored copy (rspack's tests copy 1,896 webpack files) |
| `fam-boto` | boto3, botocore | shared upstream (lockstep releases, both 1.43.108); workspace `mr-py-medium-boto` |

**Consequence.** body-parser was a T2a held-out candidate. Its family now contains express, a dev repository, so body-parser moves to dev and zustand becomes the TS/JS small held-out entry.

**Pairs considered and not merged.** These are in `familyRules.notMerged`, each with its reason:
- vite and vitest: separate project, no copy, 16 boilerplate lines;
- napi-rs and tauri: no committed napi output, dependency only;
- serde and anyhow: same author only;
- Django and the Django applications;
- requests and httpx;
- the four trivial shared-blob pairs.

`familyMapDigest` is offered for cross-checking only.

## Multi-repo workspaces (D15)

AQP6:223 asks for "a pinned multi-checkout workspace built from several public repositories with cross-repository package references", with "the Rust and TS AWS SDK and runtime repositories" as the candidate.

**How edges are found.** T2b computes every edge from the member manifests at the pinned commits:
- An edge is a registry dependency in member A on a package that member B provides. Path, git and `workspace:` dependencies are not edges, nor are manifests under fixture paths.
- Each requirement is checked against B's pinned version: Cargo semver for Rust, node-semver for npm, PEP 440 for Python.
- An edge's status is `all`, `some`, `none` or `unknown`. `unknown` means a `latest` tag.

| Workspace | Members | Edges (all / some / none / unknown) | Links | Class (hand-written lines) | Tranche |
|---|---|---|---:|---|---|
| `mr-rs-medium-serde-json` | serde, serde-json | 3 / 0 / 0 / 0 | 3 | medium (65,840) | T2a |
| `mr-rs-large-aws-lambda-tokio` | aws-lambda-rust-runtime, tokio, tower, hyper, axum, **http, http-body, hyper-util** | 47 / 0 / 0 / 0 | 16 | large (356,703) | T2b |
| `mr-ts-large-smithy-powertools` | smithy-typescript, powertools-lambda-typescript | 5 / 0 / 0 / 0 | 5 | large (227,434) | T2b |
| `mr-ts-very-large-smithy-sdk` | smithy-typescript, aws-sdk-js-v3 | 8 / 12 / 36 / 2 | 20 | very large (1,160,901) | T2b |
| `mr-py-medium-boto` | boto3, botocore | 1 / 0 / 0 / 0 | 1 | medium (127,608; Python, not analyzed) | T2b |

**What changed from T2a's candidates:**
- **The Rust stack is closed.** T2a left hyper-util, http and http-body as registry dependencies. They are now members, so every edge on the stack's core path resolves inside the workspace.
- **The TS very-large workspace drops aws-cdk and constructs.** At the pinned HEADs, 33 of aws-cdk's 34 edges cannot resolve:
  - aws-cdk pins `@aws-sdk/*` to exactly `3.632.0`, while aws-sdk-js-v3 is at `3.1146.0`;
  - it pins `@smithy/*` to exact `3.x` versions, while smithy-typescript is at `4.x`/`5.x`;
  - constructs' in-repo version is `0.0.0`.

  The workspace is renamed `mr-ts-very-large-smithy-sdk`. aws-cdk and constructs remain standalone entries.
- **The 36 `none` edges** that remain come from aws-sdk-js-v3's private `reserved/packages/*` shims, which still require `@smithy/* ^1`.
- **The powertools workspace gains `@smithy/util-utf8`**, from `packages/testing`.
- **Python pair added.** `mr-py-medium-boto` is pinned for the third-language readiness review, not analyzed.

**Assembly.** This was T2a's "defined in T2b".
- **The overlay.** Each workspace carries a normative `overlay`: members with their mounts and tree digests, and a link map from each package to `<entry id>/<dir>`. It also carries `overlayDigest`, the SHA-256 of the canonical JSON.
- **Which edges link.** Only `all` and `some` edges contribute links. An unsatisfied requirement keeps resolving outside the workspace.
- **Rendering.** `FETCH-SPEC.md` §6 defines the Cargo rendering, `.cargo/config.toml` `[patch.crates-io]`. The npm and Python renderings are left to the discovery successor (open item 5).
- **No member file is written.**

## Size method

The method is T2a's (`sizeMethod` in the manifest), with these T2b changes:

- **Class boundaries (GROK2 NBO-1).** The classes are integer intervals read from AQP6:224's strict bounds, "< 20k" and "> 1M":

  | Class | Lines |
  |---|---|
  | small | 0–19,999 |
  | medium | 20,000–199,999 |
  | large | 200,000–1,000,000 |
  | very large | 1,000,001 or more |

  T2a's table said very large was 1,000,000 or more. No entry lies on a boundary, so no class changes. The shared endpoint 200,000 goes to large, the same lower-inclusive reading as 20,000.
- **Generated-code marker rule 2 (GROK2 NBO-2).**
  - **Rule 1 (T2a)** matched its phrases case-insensitively anywhere in the first KiB. So prose counted: tokio's `ctrl_c.rs` ("a signal generated by \"CTRL+C\""), smithy-rs runtime crate docs ("for smithy-rs generated code"), Django docstrings.
  - **Rule 2** is case-insensitive over the first 1,024 bytes, as rule 1 was. `@generated` and `do not edit` match anywhere there. The other phrases count only at the start of a comment line: "auto-generated", "generated by/from/with/using/via", "this file is/was generated", and "<tool> generated code". `generatedMarkerRule` gives the exact regexes.
  - **Effect.**
    - Rule-1-only matches: 146 files (37,883 lines) in 25 repositories. All but five are prose, string literals or identifiers. The five arguable ones are:
      - `sui-execution/src/lib.rs` ("DO NOT MODIFY, Generated by ...");
      - `sui-fork/src/gql/queries.rs` ("Most of these query types are generated by cynic");
      - rspack's `owned_or_ref.rs` ("The following code is generated by");
      - the two babel-output `harmony-commonjs/index.js` fixtures in webpack and rspack.
    - Rule-2-only matches: 36 files (28,191 lines) in 6 repositories, all real headers. Examples: "// generated with @7nohe/openapi-react-query-codegen", "// This file has been generated using ../suffixes/build-map.py" and "# Generated with `generate_emoji_names`".
    - No class or measured tag of a T2a entry changes. Basis changes are listed under Changes.
  - **Known residue:**
    - generated files without any header still count as hand-written (aws-sdk-rust, and aws-sdk-js-v3's `clients/`);
    - `.yarn/releases` bundles count as hand-written JS;
    - the five arguable files above now count as hand-written.
- **Symlinks** are no longer counted as source files. T2a counted each as one line, which is the whole of hyper's −1, vite's −2 and deno's −1.
- **Per-language classes:** see Counts.

## Fetch and verify

`FETCH-SPEC.md` is the harness specification. In brief:
- **Fetch.** Fetch by SHA; refuse on any mismatch of commit, git tree, QD-22 `treeDigest` or `contentDigest`.
- **Structural checks.** UTF-8 paths, no case-fold collisions, declared gitlinks only, no escaping symlinks.
- **Store.** Materialize read-only into `store/<treeDigest>/`, re-verify, and admit.
- **Submodules and LFS** are explicit, as HD:1128 requires:
  - deno's 5 gitlinks and webpack's 7 are pinned by SHA and not materialized (`exclude-pinned`);
  - aws-cdk's 234 LFS pointers and vscode's 98 are pinned as pointers (`pointers-only`).
- **Runs** re-verify before starting, read the store only, and have no network.

**QD-22 reading.** `treeDigest` is the QD-22 digest exactly as HD:1126 states it. Gitlinks are listed, not hashed. CAN's 4 MiB admission limit is not applied to the digest preimage. Two preimages exceed it: aws-cdk's is 5,942,722 bytes, and `canonical()` refuses it; aws-sdk-rust's is 35,318,302 bytes. That reading is open item 4.

**Cross-checks.** A second implementation fetched six entries afresh, read each blob with `git cat-file blob`, and serialized with the foundation `canonical()` (unlimited only for aws-cdk). Its values equal the manifest's for anyhow, hyper, deno, webpack, zustand and aws-cdk. The six cover symlinks, gitlinks, LFS pointers and an over-limit preimage. The overlay, family-map and held-out-set digests were also recomputed with `canonical()`, and match.

## Licences

All 49 entries are permissive. Each records its SPDX expression, GitHub's detection and the evidence.

**T2a flags, unchanged:**
- ripgrep is `Unlicense OR MIT`;
- powertools is MIT-0;
- aws-lambda-rust-runtime is `Apache-2.0 AND MIT`;
- napi-rs is detected as NOASSERTION, though its text is MIT;
- deno has 5 submodules and a WTFPL `left-pad` fixture;
- GitHub reports one side of the dual licences;
- fixture-only licence fields.

**New in T2b:**
- **GitHub reports only one side** for hyperium/http (`MIT OR Apache-2.0`; it reports Apache-2.0).
- **django** is `BSD-3-Clause AND PSF-2.0`. `LICENSE.python` covers code taken from the Python standard library. Its vendored admin JS (jQuery, Select2, XRegExp) is MIT and is excluded as vendored.
- **home-assistant/core** is `Apache-2.0 AND PSF-2.0`. `homeassistant/backports/LICENSE.Python` is PSF-2.0.
- **requests:** `ext/LICENSE` says "All rights reserved". It covers `ext/`, which holds only logo images, no source. `docs/_themes` is a BSD Flask theme.
- **webpack:** 7 test submodules under `test/external` (oxc, swc, terser, test262, wpt and others) have their own licences and are not materialized.
- **rspack:** ISC appears only in test fixture `package.json` files. Its website docs are CC-BY-4.0.
- **sui:** `LICENSE-docs` and `docs/site` are CC-BY-4.0, and the `docs/subtree` lists are CC0. These are documentation, not source. Its examples and tooling include 3 MIT and 2 ISC manifests.
- **vscode:** the Copilot extension's `package.json` says "SEE LICENSE IN LICENSE.txt", and that file is MIT. Three test notebook fixtures carry Apache-2.0.
- **Considered, not used:** ansible (GPL-3.0) and servo (MPL-2.0), per GitHub's licence API.

## Open items

1. **D3 owner sign-off** (AQP6:541), for the whole selection, the held-out set and the families.
2. **Scale (HD OI-3).** There are 10 held-out families, one or two per language per class. A gating Q2 PASS needs 299 held-out families per stratum, and an advisory one needs 29 (HD §5.8). T2 at this size gives INSUFFICIENT-EVIDENCE by design. Growing it is the D4 revisit or D3 sizing (HD:1245), not this unit.
3. **Judgements to review:**
   - the family merges for constructs/aws-cdk and express/body-parser;
   - vite/vitest not merged;
   - the materiality thresholds (1% for generated glue; 1,000 lines or 1% for copies);
   - `shapeTagsJudged`.
4. **QD-22 and CAN's byte limit.** If K1a or the DR-G13 successor holds the digest preimage to CAN's 4 MiB limit, aws-cdk and aws-sdk-rust need a chunked QD-22 form.
5. **npm and Python workspace renderings.** These belong to the M3 discovery successor that D15 names (AQP6:554). The link maps are pinned in the overlays.
6. **FW-14 outputs (M3-PLAN:156).** The pinned shapes are delivered here. Reproducible workarounds, manual-correction counts and positive and negative fixtures need M3 discovery and the harness (`config-shape` cases, HD §1.1).
7. **Workload manifests (HD §9.1).** `workloadSeed` holds only the corpus side: files, packages and external dependency names. Import and reference edges, rules, cells, configuration, reset steps and run events are K1/S-M outputs.
8. **A version-skewed workspace.** aws-cdk at HEAD against aws-sdk-js-v3 at HEAD is a realistic negative D15 case (33 unresolvable edges). It is recorded, not built.
9. **GitHub signature checks.** The API reports 7 HEAD commits as unsigned: aws-sdk-rust, aws-sdk-js-v3, itsdangerous, boto3, botocore, zulip and django. T2a's README named only boto3 and botocore, though its manifest recorded all six of its own. This is informational; the pin is the SHA.

## Reproducing

All metadata came from GitHub:
- **Git.** `git ls-remote` and `git fetch --depth 1 <url> <sha>` into private 0700 bare repositories under `$(getconf DARWIN_USER_TEMP_DIR)`, deleted afterwards. Hooks were off, global and system config ignored, `HOME` redirected and LFS smudge off. All of this ran at `nice -n 19`.
- **REST.** Unauthenticated calls:
  - `/repos/{o}/{r}` and `/repos/{o}/{r}/commits/{sha}` for the 13 new pins;
  - `/repos/{o}/{r}/languages` for 17 screened candidates;
  - `/repos/{o}/{r}` for the licences of servo and ansible.
- **Trees only.** One fetch of rust-lang/rust with `--filter=blob:none`, used only to read its `src/tools` tree.

No repository code ran, and nothing was cloned into any repository. The scripts are session tooling and are not committed: measurement, the edge and version matchers, the shared-blob check and the builder. The manifest's `sizeMethod`, `generatedMarkerRule`, `tagMethod`, `treeDigestAlgorithm`, `contentDigestAlgorithm` and `familyRules` define every computed field.

## Changes in T2b

**Schema** `1-draft` → `2-draft`, unit `M3-T2a` → `M3-T2b`, plus `supersedes`.

**New per-entry fields:**
- `treeDigest` (QD-22);
- `family` and `heldOut` (HD §1.4);
- `submodulePolicy` and `lfsPolicy` (HD:1121, 1128);
- `languageClasses`, `symlinks` and `workloadSeed`;
- `pinEvidence.refetch`.

**New top-level fields:**
- `treeDigestAlgorithm`;
- `sizeMethod.generatedMarkerRule` and `sizeMethod.classBoundaries`;
- `familyRules`, `familyMap` and `familyMapDigest`;
- `heldOutSet` and `heldOutSetDigest`;
- `families`;
- `observedAt` as an object;
- the workspace edge records, `overlay` and `overlayDigest`.

**Tranches.** Every `T2b-candidate` is now `T2b`. T2a entries keep `T2a`.

**Added (13).**

| Group | Entries |
|---|---|
| Rust | http, http-body, hyper-util, sui |
| TS/JS | zustand (held-out), webpack, vscode |
| Polyglot | node-rs, rspack |
| Python | requests, django, home-assistant/core, airflow |

**Role change.** body-parser moved from held-out to dev, because of the express family.

**URL.** aws-lambda-rust-runtime's `url` is now `https://github.com/aws/aws-lambda-rust-runtime`; the awslabs URL is kept as `aliasUrl`. ls-remote HEAD there equals the pin, and a fetch by SHA gives the same tree and digests. This closes T2a open item 5.

**Workspaces:**
- Rust: added http, http-body and hyper-util;
- `mr-ts-very-large-sdk-cdk` → `mr-ts-very-large-smithy-sdk`, without aws-cdk and constructs;
- added `mr-py-medium-boto`;
- edges are computed, with per-requirement satisfaction.

**Sizing:**
- class boundaries (NBO-1);
- marker rule 2 (NBO-2);
- symlinks are not counted;
- per-language classes for counting.

**Size-basis changes on T2a entries.** They come from marker rule 2 and from no longer counting symlinks: hyper −1, vite −2, and −1 within deno's change. No class or measured tag changes.

| Entry | T2a | T2b | Change |
|---|---:|---:|---:|
| serde | 42,561 | 42,623 | +62 |
| hyper | 34,634 | 34,633 | −1 |
| axum | 47,407 | 47,483 | +76 |
| tokio | 185,165 | 185,227 | +62 |
| ripgrep | 56,354 | 56,386 | +32 |
| smithy-rs | 281,865 | 286,870 | +5,005 |
| rust-analyzer | 544,056 | 545,206 | +1,150 |
| aws-sdk-rust | 285,639 | 286,929 | +1,290 |
| axios | 46,174 | 46,201 | +27 |
| vite | 106,387 | 106,385 | −2 |
| powertools-lambda-typescript | 129,274 | 129,552 | +278 |
| typescript-eslint | 343,403 | 343,489 | +86 |
| aws-cdk | 1,239,642 | 1,236,831 | −2,811 |
| napi-rs | 167,383 | 169,634 | +2,251 |
| tauri | 119,235 | 119,759 | +524 |
| deno | 1,206,522 | 1,214,571 | +8,049 |
| netbox | 407,400 | 407,452 | +52 |
| zulip | 393,264 | 392,186 | −1,078 |

`rustCfgSites` moves by the same files on serde, tokio, smithy-rs, rust-analyzer, aws-sdk-rust, tauri and deno, and axios gains one ESM file.

**Notes updated:** tokio, napi-rs, aws-sdk-rust, aws-sdk-js-v3, constructs, aws-lambda-rust-runtime and body-parser.

**T2a open items:**
- 1 and 2 are closed: Python very large and hand-written Rust very large.
- 3: the boundary entries keep their measured classes under explicit boundaries.
- 5 is closed: the canonical URL.
- 6 moves to `FETCH-SPEC.md` §5.
- 4 and 7 continue as open items 3 and 9.
- 8 continues as open items 1 and 6.

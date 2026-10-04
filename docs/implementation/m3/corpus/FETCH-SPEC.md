# T2 `corpus fetch`: harness specification (M3-T2b)

2026-10-04 (UTC). Drafted by the M3-T2b implementer for Claude Opus 5.5, the implementation lead. **Draft for review**, with the T2b manifest.

**Standing.** This is a harness specification, not product code and not a product command. It refines HD §10 (`harness/DESIGN-r13.md:1117-1135`, QD-22) for the T2 manifest in this directory, which is what HD §10 consumes. K1a implements it (HD §13). Nothing here changes an accepted contract, gate or the harness design. Where this spec reads the design, it says so.

**Authority:**
- AQP6:213 (`analysis-quality/PLAN-r6.md`): acquisition is outside the run. `corpus fetch` is an explicit, networked harness step. Runs take the store as a pinned, read-only input with no network, and a run whose bytes don't match refuses.
- HD:1121-1128: per-entry steps, the QD-22 tree digest, and explicit submodule and LFS handling.
- HD:1130-1133: run-time re-verification, per-run `HOME`/XDG/`CARGO_HOME`/npm cache, no network code on the run path.
- `M3-PLAN.md:156` (the M3-T2 row) and `M3-PLAN-r4.md:353`: no repository code executes at M3.

## 1. Boundaries

- **Harness-only and outside every measured run.** `corpus fetch` is never invoked by, or during, an exploratory, qualification or performance run. It is the only networked corpus step.
- **No repository code.** No checkout, no hooks, no clean/smudge filters, no LFS smudge, no `submodule update`, and no build, package or install scripts. The fetch never runs `cargo`, `npm`, `pnpm`, `yarn`, `pip` or any repository tool.
- **Nothing vendored.** Bytes go only into the runner's content-addressed store. Nothing is copied into any repository, including OpenSIP's own.
- **Never the real home.** The fetch runs with `HOME` and `XDG_CONFIG_HOME` set to a private scratch directory, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_TERMINAL_PROMPT=0`, no credential helper, and `GIT_LFS_SKIP_SMUDGE=1`.
- **Held-out entries are fetched like any other.** Fetching and digesting is not inspection under QD-23 (HD:254). The fetch logs ids and digests only, never file contents or paths from a held-out tree.

## 2. Inputs

**The manifest.** `t2-corpus-manifest.draft.json` (kind `opensip-t2-corpus-manifest`, schema `2-draft`). The runner records its SHA-256, and every admission record names it.

**Fields used, per repository entry** (HD:1121 lists the first seven):

| Field | Use |
|---|---|
| `url` | fetch source. Only `https://github.com/...` URLs appear. |
| `commit` | the exact commit fetched |
| `treeDigest.value` | QD-22 digest; the store key |
| `licence` | recorded in the admission record |
| `family`, `heldOut` | recorded in the admission record; not used by the fetch itself |
| `submodulePolicy` | the gitlinks expected in the tree, each with its pinned commit; policy `exclude-pinned` or `none` |
| `gitTree` | git tree SHA-1 cross-check |
| `contentDigest.value` | T2a's SHA-256 digest; a second cross-check |
| `lfsPolicy` | `pointers-only` or `none` |

**Fields used, per workspace:** `id`, `memberIds`, `overlay` and `overlayDigest`.

## 3. Fetching one entry

1. **Work directory.** Create a private directory (mode 0700) under the runner's temporary root, and `git init --bare` in it.
2. **Fetch by SHA.** Run `git -c core.hooksPath=/dev/null fetch --depth 1 --no-tags <url> <commit>`. GitHub serves a commit by SHA. Require `FETCH_HEAD` = `commit` and `<commit>^{tree}` = `gitTree`.
3. **List the tree.** Run `git ls-tree -r -z --full-tree <commit>`. Refuse the entry unless all of these hold:
   - every entry is a blob with mode `100644`, `100755` or `120000`, or a gitlink with mode `160000`;
   - every path is valid UTF-8;
   - no two paths, or directory prefixes, are equal after Unicode NFC normalization and case folding. The store may sit on a case-insensitive volume, such as default APFS.
   - the gitlinks are exactly `submodulePolicy.gitlinks`, path for path and commit for commit;
   - every symlink target is relative and, once resolved against its directory, stays inside the tree.
4. **Digest.** Stream every blob with `git cat-file --batch`, in ascending path-byte order, and compute both digests from the raw blob bytes:
   - `treeDigest`, as defined in the manifest's `treeDigestAlgorithm` (QD-22, below);
   - `contentDigest`, as defined in `contentDigestAlgorithm`.

   Refuse on any mismatch.
5. **Materialize** into `store/<treeDigest>.partial/`:
   - regular blobs become files of mode 0444, or 0555 for `100755`;
   - symlinks become symlinks with the same target text;
   - a gitlink becomes an empty directory, as a checkout without `submodule update` leaves it;
   - an LFS pointer stays a pointer file. LFS objects are never fetched.
   - directories become 0555 once filled.
6. **Re-verify the materialized tree.** Walk it and recompute `treeDigest` from file bytes, modes and `readlink` targets. Then rename it atomically to `store/<treeDigest>/` and write `store/<treeDigest>.admission.json`. That record holds:
   - the manifest SHA-256, entry id, `url`, `commit`, `gitTree`, `treeDigest`, `contentDigest`, licence SPDX, family and `heldOut`;
   - the fetch time and the git version.
7. **Clean up.** Delete the work directory, including after a refusal. A refused entry leaves no `store/` path.

An entry whose `store/<treeDigest>/` already exists is re-verified (step 6's walk), not fetched again.

**Refusal codes:**
- `MANIFEST-UNREADABLE`, `NETWORK-FAILURE`;
- `FETCH-COMMIT-MISMATCH`, `GIT-TREE-MISMATCH`, `TREE-DIGEST-MISMATCH`, `CONTENT-DIGEST-MISMATCH`;
- `UNEXPECTED-ENTRY-TYPE`, `NON-UTF8-PATH`, `CASEFOLD-COLLISION`, `UNDECLARED-GITLINK`, `ESCAPING-SYMLINK`;
- `STORE-VERIFY-MISMATCH`.

A refusal affects only its entry. `corpus fetch` exits non-zero if any requested entry was refused.

**At the T2b pins, no entry trips a structural check.** No path is non-UTF-8 and no path collides under case folding. All 121 symlinks stay inside their trees. The gitlinks are deno's 5 and webpack's 7, and the LFS pointers are aws-cdk's 234 and vscode's 98.

## 4. The tree digest (QD-22)

HD:1126 defines `treeDigest` as "the SHA-256 of the canonical JSON array of `[path, mode, sha256(content)]`, sorted by path bytes". The manifest's `treeDigestAlgorithm` (`opensip-qd22-tree-sha256/1`) fixes the details this needs:

- **Elements.** One element per blob entry (modes `100644`, `100755`, `120000`):
  - `path` is the full path as a UTF-8 string;
  - `mode` is git's six-digit octal string;
  - the hash is the lowercase hex SHA-256 of the raw blob bytes. For a symlink that is its target text; for an LFS pointer, its pointer text.
- **Gitlinks** have no content and are not elements. `submodulePolicy.gitlinks` pins each one, and `gitTree` binds them.
- **Order** is ascending by the UTF-8 bytes of `path`.
- **Serialization** is the foundation canonicalization (CAN:67-74): `json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))`, UTF-8.
- **Byte limit (lead reading).** CAN's 4 MiB limit is an admission limit for records. A digest preimage is not an admitted record, so it is streamed without that limit. This matters in practice:
  - aws-cdk's preimage is 5,942,722 bytes, and `canonical()` itself refuses it with `BYTE_LIMIT`;
  - aws-sdk-rust's is 35,318,302 bytes, over 245,250 blobs.

  If K1a or the DR-G13 successor reads HD:1126 as bounded by CAN's limit, QD-22 needs a chunked form for these entries. That is open item 4 in the README.

**Cross-checks.** Every manifest value comes from a streaming implementation. A second implementation fetched hyper, deno, webpack, zustand, anyhow and aws-cdk afresh, read each blob with its own `git cat-file blob`, and serialized the list with the foundation `canonical()`. For aws-cdk it used the same serializer without the byte limit. Its values equal the manifest's for all six. The six cover symlinks, gitlinks, LFS pointers and an over-limit preimage.

## 5. At run time

This section restates HD:1130-1133 for this store.

- A run lists the entries it uses by `treeDigest`. Before it starts, it re-verifies each one with step 6's walk, and refuses on a mismatch.
- A run reads `store/<treeDigest>/` paths only, read-only. It has no network code and sets per-run `HOME`, XDG, `CARGO_HOME` and npm cache directories.
- Re-verification hashes every byte. The largest entries are:
  - aws-sdk-rust: 2.07 GB, 245,250 blobs;
  - aws-cdk: 1.19 GB;
  - aws-sdk-js-v3: 615 MB;
  - vscode: 287 MB.

  The whole corpus is 5.69 GB of blobs.

## 6. Multi-checkout workspaces (D15)

A workspace is assembled under `ws/<workspace id>/`, outside the store and outside every repository:

1. **Mounts.** `ws/<id>/<entry id>` is a read-only view of `store/<treeDigest>/` for each member: a symlink, a read-only bind mount, or a copy-on-write clone that is re-verified like a store tree.
2. **The overlay is normative.** Write the manifest's `overlay` object to `ws/<id>/workspace-overlay.json` as canonical JSON (CAN:67-74). Its SHA-256 must equal `overlayDigest`; refuse otherwise.
   - `overlay.links` maps each package that a member provides, and another member requires, to `<entry id>/<package directory>`.
   - Only edges with status `all` or `some` contribute a link. A requirement that the pinned member version does not satisfy keeps resolving outside the workspace. Each edge records which of its requirements are satisfied.
3. **Cargo rendering (defined).** Write `ws/<id>/.cargo/config.toml`, with one `[patch.crates-io]` line per Cargo link, sorted by package name, for example `tokio = { path = "rs-medium-tokio/tokio" }`.
   - Cargo resolves config-relative `[patch]` paths from the directory that holds `.cargo`, which is `ws/<id>/`.
   - Each member keeps its own Cargo workspace, and nothing nests.
   - The file is generated from the overlay and is not separately pinned.
4. **npm and Python renderings (not defined here).** The link maps for `mr-ts-large-smithy-powertools`, `mr-ts-very-large-smithy-sdk` and `mr-py-medium-boto` are pinned in the overlay. Which native file OpenSIP's multi-repo discovery reads (a pnpm workspace file, package-manager overrides, or a source path) belongs to the discovery successor that D15 names (AQP6:554). That is open item 5 in the README.
5. **Nothing runs.** No install, build or lockfile update runs, and no member file is written.

## 7. Not specified here

T3 has its own local manifest and fetches from local paths (HD:1135). Workload priming and reset steps belong to HD §9.2. The freeze's `familyMapDigest` and `heldOutSetDigest` belong to K1a (HD:269). The manifest offers values for cross-checking only.

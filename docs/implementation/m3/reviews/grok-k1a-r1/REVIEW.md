# K1a r1 — ACCEPT-UNIT

Product unit for Q0 r13 sections 1, 3 and 10 and the accepted T2b fetch specification: case and ledger libraries, canonical digests, the freeze, corpus fetch, and the store, plus additive inventory v143. Acceptance is the reviewed product bytes and that inventory candidate. There is no contract successor, no design-lock edit, and no owner sign-off. K1b confidence and K1c running, adjudication, and report consumption stay outside this unit. The libraries preserve input records and chain integrity.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1a` is detached at `c664356b289f202cbcf8dad34f56cd85c68a7e25`. The only dirty path is the untracked directory `tools/quality/`. `evidence/k1a.diff` is the seven-file addition, 56199 bytes, sha256 `241c76d3f9f20ac5e2274b161e94e4081eaaef02c657b0449db57a40346c5c3a`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/README.md` | 2227 | `5353c46d0382fdf8b2fad19ccbf08e1e4b146c1bcdab562186972161c4203bef` |
| `tools/quality/canonical.py` | 2463 | `98579f7d151ed35e50b5a8e5d56f015d8fd86861676378135e69a36f617d2876` |
| `tools/quality/corpus.py` | 2968 | `195d996e166ee9d799d426b76bbac16e7a4d811974e10344025f6733bf986443` |
| `tools/quality/fetch.py` | 9051 | `acc9639eef4435b36794ce5b31c8896e50d5fa75ea0e8ad5bbd2d94350fea76e` |
| `tools/quality/records.py` | 11416 | `1e753f5701278e463d390b4006d4076b7b59cca53626a3a6672413138d49a744` |
| `tools/quality/store.py` | 9504 | `5fd74f14479a3e502dcf763ca3b52094f2da5c5385f28dab50fb7cc18aee0f28` |
| `tools/quality/test_quality.py` | 15504 | `5c8c7e3573b2bf69256a785be08d8e8d8058914d0fc4dbb4b0b05c46f37537de` |

Authorities, read at the pinned bytes: `DESIGN-r13.md` sections 0, 1, 3, 10, 13 and 14 (151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`); `FETCH-SPEC.md` (10659 bytes, sha256 `4ebe90a491721e48d252f11e6378b6c73312b506b59af89b24c03829416f8858`); foundation `canonical.py` (6465 bytes, sha256 `d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442`). The content-digest sentence used below is the manifest field `contentDigestAlgorithm` for `opensip-t2-content-sha256/1-draft`. Q0 standing allows K1 to be implemented from these mechanisms.

## Canonical bytes

`canonical.py` reimplements the foundation admission used for harness records. Floats and non-finite numbers are refused. Duplicate keys, `-0`, and a non-byte input are refused. Integers outside `-(2^63) .. 2^64-1`, depth past 32, non-string keys, and values outside the exact JSON types are refused. `canonical` is `json.dumps` with `ensure_ascii=False`, `sort_keys=True`, separators `(',', ':')`, and `allow_nan=False`, then UTF-8, then the 4 MiB record limit. Digests are unframed SHA-256. That matches CAN:61 and CAN:67–74.

The QD-22 preimage is streamed one canonical element at a time. The 4 MiB limit stays on admitted records and is not applied to that preimage.

## Cases, freeze, and the ledger

A case set is canonical JSON Lines, sorted by `caseId` UTF-8 bytes, with a trailing newline. `caseDigest` is SHA-256 of the canonical body with `caseDigest` removed. Admission requires the §1.4 top-level fields, the six case kinds, tier `T1`/`T2`/`T3`, the six origins, and a boolean `heldOut`. T2 and T3 require a non-empty `family`. T1 requires `inputs.fixtureManifestDigest`. T2 and T3 require repository, commit, and `treeDigest`. A validated seed requires `controlTreeDigest` and `mutantPatchDigest`. The rule requires `ruleId` and `ruleSpecDigest`. Determinate-positive requires `expectedFinding`. Must-abstain requires `expectedDeficiency` and boolean `positiveSoundUnderDeficiency`. A cell-observation requires `cell`. `subject`, `requirement`, `configuration`, `provenance`, and those nested answer objects are admitted as non-empty objects. Their interior keys are preserved and are not a closed schema. QD-2 scoring is not implemented.

The ledger is one append-only JSON Lines file. `append_record` opens `O_RDWR|O_CREAT|O_APPEND|O_NOFOLLOW|O_CLOEXEC` at mode `0600`, takes `LOCK_EX`, refuses a caller-supplied `recordDigest` or `prevRecordDigest`, re-validates the prospective file, writes, and `fsync`s. There is no truncate or repair. The first record must be `freeze`; a later freeze is refused. A freeze takes the seven raw byte sets, checks that the case-set bytes re-parse, requires the other six inputs to already be canonical, and stores the SHA-256 of each byte set. A torn or reordered file refuses the next append and is left unchanged. A `supersede` must name a digest already in that ledger and give a reason. An exposure requires scope `case`, `repository`, or `family`, plus who, when, and what.

`held_out_eligible` returns false when `heldOut` is false. Otherwise it returns false when any caller-supplied ledger contains an exposure whose scope subject equals the case id, `inputs.repository`, or `family`. A later supersede leaves the exposure record in place, so eligibility stays lost. A new freeze in a new file does not clear history. The caller supplies every historical ledger.

Carry compares the eight hard components plus `truthInputDigest` by canonical equality. `treeDigest` stays covered by the truth-input closure in §3.3 and is not a separate hard component. The label carries only when every one of those inputs matches and the recorded outputs match. A changed input or a changed output requeues. Equal inputs with different outputs also set `determinismDefect`. A prior-round `sourceResolution` on a carry record is stored as a pin. This chain does not prove that pin's provenance.

A resolution's `voteRecords` must be digests already present in that same ledger. The check does not also require each cited record's kind to be `vote`. Agreement and drift-audit records are admitted with their required fields present. The §4 statistic, the §3.5 sample draw, and a T3 rationale's freedom from source text are left to the caller and to the separate T3 ledger.

## Fetch and the store

`corpus.py` is the harness command. It parses one manifest, requires unique repository and workspace ids, and requires the QD-22 and T2 content algorithm ids. One entry's refusal does not stop the others. The process exits non-zero if any requested entry was refused. Logs are ids, digests, and refusal codes. Verify and workspace do not import `fetch`.

Default acquisition admits `https://github.com/...` with no user, password, query, or fragment. `local=True` admits `file:` with an empty netloc for synthetic fixtures. An existing store directory is re-verified and not fetched again. The fetch uses a private 0700 work directory, `git init --bare`, and `git fetch --depth 1 --no-tags` by commit. `FETCH_HEAD` must equal the commit and `<commit>^{tree}` must equal `gitTree`. Paths must be UTF-8. Blobs are `100644`, `100755`, or `120000`; gitlinks are `160000` and must equal `submodulePolicy.gitlinks`. NFC plus case-fold collisions, including directory prefixes, are refused. A path that is also a directory prefix of another path is refused. Symlink targets must be relative and must stay inside the tree after `normpath` against their directory. The stored walk also resolves the link and refuses a target that leaves the tree.

Git runs with `--git-dir` as an argument. The child environment drops inherited `GIT_*`, sets `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`, `GIT_LFS_SKIP_SMUDGE=1`, `GIT_ALLOW_PROTOCOL=https:file`, and `XDG_CONFIG_HOME` to the private work directory. Hooks, the credential helper, `protocol.ext.allow`, and `init.templateDir` are disabled on the command. HOME is left untouched, which is the session owner's rule for this implementation. No LFS object is fetched and no submodule command runs. A backslash in a path or link target is refused as well.

Blobs are hashed while they are written. The tree digest is the SHA-256 of the streamed canonical array of `[path, mode, sha256(content)]` for blobs only, sorted by path bytes. Symlink content is the target text. An LFS pointer contributes its pointer bytes. Gitlinks are absent from that array. The content digest is SHA-256 of `<mode> <type> <hash> <path>` plus NUL for every `ls-tree -r` row in path order. For a gitlink, the hash is the recorded commit. That is the manifest's `opensip-t2-content-sha256/1-draft` definition. Both digests must match before publication.

Materialized files are `0444` or `0555`. Symlinks are created after the regular files. Directories, including the stage root and an excluded gitlink's empty directory, are `0555`. The published tree is walked again and both digests are recomputed from file bytes and `readlink` targets, without following links. The stage is then renamed to `store/<treeDigest>/` and `store/<treeDigest>.admission.json` is written exactly once. A failure after publication removes that tree and a receipt this call created. The partial stage is always removed. Reuse of a corrupt tree is `STORE-VERIFY-MISMATCH`. Extra directories and mode changes fail the same way.

No public corpus was fetched. The synthetic tests show a wrong content pin is refused, and that a 4600001-byte QD-22 preimage (50000 elements, above 4 MiB) equals an independent `json.dumps` of the same array. They do not recompute the pinned public trees.

Workspace assembly checks `overlayDigest`, mounts each member as a symlink to its verified store tree, and writes the overlay as canonical JSON. Cargo links become `[patch.crates-io]` lines sorted by package name, with the name and path quoted by `canonical`. npm and Python link keys are returned in `undefinedRenderings` and are not rendered. Nothing is installed. Non-symlink files are `0444` and directories are `0555`. Removing a workspace stage does not follow member symlinks into the store: Python 3.14 `rmtree` of a directory that contains a store symlink left the store bytes in place, and `rmtree` of a symlink root raises rather than deleting the target.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1a`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_quality.py`

23 tests passed, 0 failed, 2.173s. The clock immediately after that run was 2026-10-06T03:05:31Z. The run covers local pinned acquisition and reuse, full stored-byte rehash, path and prefix case-fold and symlink checks, read-only modes, excluded pinned gitlinks, an independent content-digest refusal, the over-4 MiB QD-22 comparison, receipt-failure cleanup, ledger tamper, chain and freeze pins, permanent exposure across a supersede and a new freeze, and each hard-input and truth-input carry component. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v143

Staged outside both repositories. Parent v142 in the architecture tree matches the pin (585522 bytes, sha256 `2745e424f78185a4cda1da3dc573e753356a43a5985059d847dc5c5f44299acc`).

Candidate `docs/implementation/m2/repository-file-inventory.v143.json` is 588871 bytes, sha256 `4f896b9612f831f05d4b2b37cef6b370b962db36819d1c67d49ca0f8fde22271`. Successor record is 307664 bytes, sha256 `6bd47e90e97ce5b814664635d9e6d284d1c49cbfd90d9a5cffc769a0fe66322c`. Subject manifest is 647 bytes, sha256 `adbe63a624f0502e8aab4552e33650287e1633690f4356d671b22f1e15f92e72`. Its three members hash to the staged README, successor, and candidate.

The candidate has the parent's keys. `packages` and `pendingDecisions` are equal. `standing` is still the v142 sentence for I1-b2. The additive profile allows standing to stay equal; the successor record's own standing names K1a. `files` grows from 1016 to 1023, stays sorted and unique, and adds only the seven `tools/quality/` paths, each `generated: false`, package `tooling`, standing `proposed`. Every inherited row is equal by value. `plannedRowsChanged` is empty. The two carried pending-decision obligations are unchanged.

The 103 description projections resolve to the same paths as the selected v142 `inventoryPassageInheritance`. Each `before` equals that row's `before`, and each `effectiveDescription` equals that row's `after`. The before and after text multisets are unchanged. The seven new files occupy indexes 955–961, so 102 selectors stay and `tools/tests/test_check_crash_matrix.py` moves from 963 to 970.

Inventory verdict: ACCEPT. No required findings.

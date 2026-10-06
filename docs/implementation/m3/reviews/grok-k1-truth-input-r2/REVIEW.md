# K1 default truth-input closure r2 — ACCEPT-UNIT

r1 required finding TRI-INV-01 is closed. The successor standing now names the K1 default truth-input closure. The product files, the v155 candidate, the v154 parent, `addedFiles`, and all 103 projection rows are unchanged.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1-truth-input` is detached at `f2159063607cb709f1fab61b575f71d84599e539`. The only untracked paths are the two product files. `evidence/k1-truth-input.diff` is 9060 bytes, sha256 `82df353eb9744efb7162f916ef80ff500689c3e9a38608d990d2d121e202110e`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/truth_input.py` | 2852 | `462d12eeaa105ad75e2ae871638536a95783b38d90c4609cf31555f8eab31710` |
| `tools/quality/test_truth_input.py` | 5390 | `da1f71925f6eb3011450d656b05e3e6d248b0fddec472c2e3ba69d51c3bb247d` |

`DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. `native-evidence.md` is 329013 bytes, sha256 `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. `dependencySourceSetId` is `Sha256Text` (NE:1265). `preparedOutputSetId` is `Sha256Text | null` (NE:1274). The native spelling is `sha256:` plus 64 lowercase hex (NE:1899, NE:3926).

## Closure

`truth_input` hashes one canonical object: the caller’s QD-22 blob rows plus `configurationDigest`, `dependencySourceSetId`, `preparedOutputSetId`, and `resolutionEnvironmentDigest`. Each row is `[path, Git mode, content SHA-256]`, already sorted by UTF-8 path bytes. Modes are `100644`, `100755`, and `120000`. Content digests are bare 64-hex pins. Directory prefixes stay implicit. Gitlink mode `160000` is refused.

Dependency and prepared identifiers keep the `sha256:` prefix. Absent preparation is JSON null. A missing dependency id is refused. Configuration and resolution-environment digests are bare pins. `snapshotAdmissionEstablished`, `resolutionAdmissionEstablished`, and `productQualification` are false. Detector outputs, witnesses, and a narrowed-closure switch are not parameters. `canonical` refuses a preimage over 4 MiB with `BYTE_LIMIT`.

`records.carry_comparison` matches `HEAD`. An added `missing.ts` changes the digest and the existing comparison requeues. Equal records still carry.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1-truth-input`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_truth_input.py`

The clock before the run was 2026-10-06T08:14:05Z. The module ran 13 tests, 0 failed, 0.063s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent. The Darwin temp `opensip-lanes.lock` was absent.

## Inventory v155

Candidate `docs/implementation/m2/repository-file-inventory.v155.json` is 602922 bytes, sha256 `1ff84a2db8345ca5ef731842f93df0ff5bd684d879fa6e7aec56d5f1c4c189a2`, byte-identical to the r1 candidate. Parent v154 is 601587 bytes, sha256 `0cc15aa3909688c73a95c9fcc40fa4c2031040d1e8a462b3b4eed66378babea6`. Successor record is 307530 bytes, sha256 `ecaf70445d8638a49a8c23444b3dce4a2e0ff1450a9a3f6bf44da2e6bb59ee91`. Subject manifest is 670 bytes, sha256 `ed26b5df485523bb91a05005e66cf63bfb684dc10e4df060b02a3b5c3590e350`. Its three member hashes match the staged README, successor, and candidate.

Against the r1 successor, every field matches except `standing`. The new standing is `PROPOSED additive K1 default truth-input closure component inventory; actual Grok unit review and lead assent required`. The README is byte-identical to r1.

v155 adds exactly `tools/quality/test_truth_input.py` (index 984, package `tooling`, role `test`, `generated: false`, `standing: proposed`) and `tools/quality/truth_input.py` (index 985, package `tooling`, role `validator`, `generated: false`, `standing: proposed`). Files stay sorted and unique. All 1045 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v154 I1-b2 sentence. The 103 design-lock passages, parented on v154, keep their before and effective text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/992/description` to `/files/994/description`. `design-lock.json` is unchanged in the worktree (`9d2e1bcf4ed8de7f74996c3d733b0fac9c4d3f025c9524a1add0f50b89efd9a1`). No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Snapshot admission, resolution admission, label carry authority, and qualification remain outside this function.

# M1 generator adapter review 04: narrow delta review

**Verdict: ACCEPT-UNIT.** Review03's RF1 is closed on the frozen subject-04 bytes, and there are no new required findings. The acceptance covers only the concrete adapter and its fixed macOS development host profile. It does not cover hermeticity, product integration or install, runtime/release qualification, or M1 acceptance.

`subjectManifestSha256` is `d25b7713ca29296df964497a75c6bef205edf5f08ac13f6b533dc99fd02d3f2f`. All 87 files match exactly (none unlisted or linked), checked both before and after all probing.

## Delta from subject-03

- No files were added or removed.
- **`tools/generate_contracts.py`** changed in three ways:
  - Node/Rust write grants now exclude the root literal.
  - The parent records `directory_identity` (lstat dev/ino, must be a directory) for `output`, `runtime-scratch` and `home`, and checks it before rendering each profile and after each child.
  - `owners.json` must equal the parent's options mapping byte-for-byte.
- **`tools/tests/test_generation_execution.py`** has three new tests.
- **`GENERATOR-UNIT.md`** has new documentation.
- **`generator-closure.json`** changed only that one pin.
- **`registry.json`** changed only the closure digest, now `2d64a8d8…`; the registry itself is now `4b1b4915…`.
- **The 8 outputs** differ only in header lines 2-3; their bodies are byte-identical to subject-03.

## RF1: closed

| Run | Result |
|---|---|
| subject-03, root-replacing generator stub + probe TS child (positive control, this session) | **Exploit reproduces:** victim read, outside file written, canary overwritten |
| subject-04, same stub + same TS child | Stub report: root `chmod`, `rename`, `rmdir` and `symlink` all **EPERM**. Victim read/write/overwrite **EPERM**. Nothing changed. |
| Real generator + probe TS child (03 and 04) | Victim access EPERM |
| Stub unconfined | chmod, rmdir and symlink succeed, and the root becomes a symlink to the victim |
| Native effects probe under the new `child_profile` | Root rmdir and chmod now EPERM. All other review03 denials unchanged; collector still refuses links and fifos. |

**Parent custody.** Children cannot replace roots, so I simulated a sandbox bypass: real sandboxed steps ran, then the harness mutated a root outside the sandbox. In each case below the parent refused immediately with a controlled `GenerationError`, no later sandboxed step ran, and outputs and victim stayed unchanged:
- output symlinked after the generator step
- output inode replaced after the generator step
- scratch symlinked after the validate step
- home replaced after the validate step

(My first harness run stacked wrappers across scenarios; I fixed that and reran each scenario in isolation.)

## Advisories from review03

- **ADV3: closed.** The confined Python step was run with a rebound `prepare.py` that reorders owners, changes modules, or reformats identical data (`indent=1`). Every variant refuses with "prepared owner mapping differs", and outputs are unchanged.
- **ADV1: closed as documentation.** Generic runtime exports are documented as inert, and only `createReportShapeRegistry` is the selected facade.
- **ADV6: closed.** The architecture record `generator-witness-source-correction.v1.json` names the historical record `4d8e46ed…` and the derived corpus `d79f78e0…` (1338 cases), and both match the actual files.
- **ADV2: accepted as the frozen-manifest route.** The binding4 source preflight is under separate review and was not assessed here. Product install still requires an accepted integration manifest that selects registry `4b1b4915…` and closure `2d64a8d8…`.
- **ADV4 / ADV5:** unchanged limits, now documented.

## Other delta evidence

- **Tests:** 78 pass (review03's 75 plus the 3 new ones), none skipped.
- **Drift check:** a fresh 4-step run with the build-04 generator, node and python (all hash-matched) and the 140-file TS tree is clean at `4b1b4915…`, with one JSON line on stdout.
- **Publishing:** `--write` restores two corrupted outputs to the exact subject-04 bytes, and the following drift check is clean.

## New advisories (non-blocking)

- **DA1:** the real-sandbox regression test skips silently when no C compiler or `sandbox-exec` is present. A qualification run should treat that skip as a failure.
- **DA2:** the Python `prepared_output` root isn't in the identity set. No grant is derived from it, and the root literal is already excluded, so this is only for uniformity.

## Remaining integration obligations

- An accepted integration manifest selecting the registry, closure and architecture anchor.
- Complete protocol/report source-closure owners.
- The inventory/design bootstrap binding.
- Other platform, resource-limit and release qualification.

## Limits

- Delta scope only.
- Only the macOS 26.6.2 aarch64 host was tested; the sandbox, kernel and pinned interpreters are trusted.
- Timeout and resource limits were not triggered.
- No rebuild was done, because the generator binary is unchanged.

Evidence is in `logs/`, scripts and copies in `work/`. All mutations stayed in this directory, and nothing was committed or pushed.

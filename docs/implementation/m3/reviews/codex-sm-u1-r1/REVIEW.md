# Codex review: SM-U1-BUILD-SCRIPT-OUTPUTS-ABSENT-r1 (U-1, PLAN-r3)

**Verdict: REQUIRED-FINDINGS.** One required finding, **SM-U1-R1-RF-01**, for the inaccurate numerical comparison in PLAN-r3's D-5 justification. No nonblocking observations. The implementation variant and retained measurements otherwise check out; the finding requires a record correction, not a compiler rerun.

## Exact subject and boundaries

Stage: `/tmp/opensip-implementation/sm-u1-r1-stage`.

`subject.json`: 12346 bytes, SHA-256 `65884c39a0de99f8ca30d90cd33bd800d1d51fbc6a28684ebb88821c240eca0c`. Independently rehashed all **49 members**; every size and digest matches. Live bases match clean product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` and architecture `9e3492c05fa3cdf77fbabb594470b37e91f81f40`. Architecture's existing untracked held E2s directory was not read or changed.

Only read-only inspection, hashing, JSON/source parsing, Git queries, in-memory archive reading and the expressly permitted audit were used. No Cargo, compiler, image, driver, runner, tests, lane, network, other pane or delegation. No private 413 fixture, installation directory, signing keys or held-tree content was read. Neither repository, stage, other working files nor control state was edited. The authorized audit-output rewrite was byte-identical. Only REVIEW.md and review.json were otherwise written.

## Required finding: SM-U1-R1-RF-01

PLAN-r3:15 says the static-profile whole-graph spans agree with the package-context series “within about 1%,” giving Napi and Axum examples. The authoring script reproduces that statement. Axum's quoted values already contradict it: 4061.596 ms versus3920.591 ms differs by **3.597%** relative to context.

Independently compared every row against the accepted static-profile samples and the accepted remaining/axum-tokio context samples:

| Ordinal | Static-profile median ms | Context median ms | Difference relative to context |
|---|---:|---:|---:|
| 0 | 8069.737 | 8036.631 | +0.412% |
| 1 | 5349.708 | 5373.543 | −0.444% |
| 2 | 4061.596 | 3920.590 | +3.597% |
| 3 | 738.521 | 731.949 | +0.898% |
| 4 | 69.862 | 64.823 | +7.774% |
| 5 | 140.140 | 140.853 | −0.507% |
| 6 | 1226.191 | 1202.608 | +1.961% |
| 7 | 72.280 | 71.741 | +0.751% |
| 8 | 141.990 | 141.020 | +0.687% |

This is a descriptive comparison, not a demonstrated tolerance or statistical equivalence. The largest difference is about7.8%, not1%.

**Required correction:** correct or remove the assertion in PLAN-r3 and make_plan_r3.py. If retaining numbers, cite the accepted series, state the denominator and actual range/per-row differences, and keep the comparison descriptive. Preserve the independent rationale for static command data and the actual measurement boundary, along with the exact implementation/measurement bytes and other plan definitions. No rerun is needed.

`planR3D5DeltaSound=false` records this defective stated justification, rather than rejection of the static-profile path itself. Moving to the static-command-data series is otherwise coherent with the producer variant. The corrected producer-block account is accurate. Rejecting the framed whole-graph span for this defined SM-4 boundary is also supported: it includes repeated same-child map transfer; it is not the chosen file-map static-profile span. The preserved framed observations remain useful information rather than discarded measurements.

## Plan, producer and collection

Independently reconstructed PLAN-r3 from its declared literal replacements without executing the author script. It matches exactly. Differences from the accepted PLAN-r2 are the revision heading/change table, D-5 and its consequential U-1 wording; other definitions and gate authority remain unchanged.

The accepted producer and image remain at their accepted pins. Compared complete producer file populations: **3130 files**, no extra or missing variant file, and exactly the two named Rust files differ. The compiler change preserves the original unavailability seeds, excludes only build-script edges from propagation, records whether a command exists solely because of that relaxation, and removes OUT_DIR/*_OUT_DIR only on those new commands. Cargo prepare_rustc remains the command constructor; no compile/dry-run queue is invoked. The second source file only adds the stated control. Retained checks/logs show all four command_data controls pass, including the build-script-only consumer with its build script unavailable. The fresh variant image rehashes to its record; the closed accepted image remains unchanged.

For all nine collections, the permitted audit confirms successful receipts and graph equality modulo packet roots, with old constructed commands equal modulo packet/image roots. Independently recomputed both producer unavailability fixed points from each graph: the new constructed commands are exactly the difference produced by ignoring build-script edges. Counts are **36,19,18,0,9,3,11,9,3**. All new environments omit OUT_DIR and *_OUT_DIR, and build-script units themselves have no constructed command. Existing commands retain their content and get only the false disclosure flag; other unavailable rows retain their old standing.

Compared all nine maps' logical-path/content-pin populations modulo packet roots. File counts, content byte totals and hashes agree with accepted inputs; no source trimming supplies the newly available commands.

## Executors and series

Inspected both executor diffs against the accepted sources. They exclude build-script edges consistently from argument validation, dependency blocking, extern bindings and transitive metadata search, and add the disclosure flag. Target/mode validation still excludes build scripts, proc macros and unsupported targets. Both variants preserve the closed observation/driver paths and bounds.

The static-profile series has nine entries, ten graphs each, three warmups and seven measured samples. Independently checked sample ordinals, population repetition, recorded prepared-read audit repetition, metadata-hash repetition and retention of every previously analysed unit. Recomputed all median/maximum whole-graph spans. There are **2690 launched compiler children** in this successful series. Every launched target is a supported library; build-script and proc-macro targets are not executed. Recorded prepared-read observations are not a claim of complete runtime/sysroot read sealing or filesystem confinement.

Incomplete units remain preserved. Read the retained serde_core stderr: compile-time env!("OUT_DIR") is absent at the include of private.rs. Dependants consequently remain incomplete, including axum, axum_extra, serde and serde_json. The retained serde_derive_internals stderr explicitly refuses src/mod.rs as outside the prepared map. Neither cause is repaired or converted to success. New first-party successes remain Napi's napi_sys and napi_derive_backend unit instances, rather than the formerly blocked main libraries being claimed complete.

The metadata-path explanation is supported directly by retained Hyper metadata: both old and new files contain their packet root **54 times**; the new root is **nine bytes longer**, and the metadata-size difference is **486 bytes**. Both binaries rehash to their recorded metadata pins. This explains why cross-root hash equality is inappropriate; within-series repetition and retained accepted-unit analysis remain the controls. It does not establish semantic equivalence of every byte across roots.

## History, archive and audit

Read all three large-records.tar.xz members in memory. Each matches the index size/hash and the named external original: maps, static-profile series and framed series. Archive SHA-256 is `3ca1fe4456b72e9f413286ad223d7cbc40e003196fb95da6beb32049f082cebc`. Nothing was extracted.

The framed path and its runner/logs remain history, not the selected SM-4 series. The r79 integration commit is 2026-10-13T23:18:56-07:00; retained Napi warmup output timestamps place it in warmup1, before measured samples beginning about23:20:57. This supports the disclosed warmup overlap. The report keeps concurrent work disclosed and does not use that framed path for SM-4.

The first static-profile attempt log records all ten entry0 graphs followed by KeyError for analysisElapsedNanos. Its runner is retained. The successful runner correctly treats the plain driver's absent instrumented interval as absent; the whole-graph timing boundary remains unchanged. Failed attempt evidence is not upgraded into a successful final series.

Ran exactly the permitted command:

`nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-command-data-bsabsent-2026-10-13/audit_u1_r1.py`

It exited zero and reproduced u1-checks-r1.json byte-for-byte: **51860 bytes**, SHA-256 `d194ede2d7346213bacd7526a8d214384aa3866f92667833530565c6479e4c15`. Reproduction validates its custody/comparison checks; it does not check the erroneous plan percentage.

No SM-4 value, F, T or outcome is formally recorded. SMComplete, LG1Met, effectiveL and productQualification remain false. O7, D3 and D13 remain closed; only L-G1 remains open among L's gates. Native admission is not an additional experiment gate. Nothing was pushed. Exact lead assent and fresh design verification before publication remain separate lead work.

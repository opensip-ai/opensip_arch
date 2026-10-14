# Codex review: SM-COLD-TS-r1 (U-5a), round 2

**Verdict: ACCEPT.** No required findings or nonblocking observations. **SM-COLD-TS-R1-RF-01 is resolved.** The current interpretation explicitly supersedes the inherited replay classifications while preserving the measurements. Acceptance establishes the cold-reset component evidence, not F/T, a real-workload replay bound or complete S-M.

## Exact subject and preservation

Stage: `/tmp/opensip-implementation/sm-cold-ts-r1-stage`.

`subject.json`: 139512 bytes, SHA-256 `0c39c9ec154f1592332159032cf1940e72fe7dc31629a350fcba24f9f7158974`. All **614 members** independently rehashed and match.

The original 137997-byte manifest is retained as history/round1-subject.json, SHA-256 `6d04c3812e79538a1a94e97468adcb016d17679853995946be15c219ff3d0a21`. Rechecked all 607 original pins against unchanged current members or exact historical copies. Only REPORT.md, audit_cold_ts.py and cold-ts-checks.json change among original paths. Their originals remain as history/round1-REPORT.md and the top-level round1-audit_cold_ts.py / round1-cold-ts-checks.json. All measurement bytes, cold runners, reset module, helper/template inputs, result files, reset records, raw archive/index, logs and retained attempt0 are unchanged. The round-1 review remains untouched.

Live bases match clean product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` and architecture `32b4ba9bdd352c41e28d3761a3e53c49b0ebea3c`. Architecture's existing untracked held E2s directory was not read or changed.

## Finding resolution

cold-ts-interpretation.json is expressly the **current interpretation** and pins each of the six verbatim generated result files by hash. All six pins match. Each component receives the cold label “cold OpenSIP state, page cache recorded,” with no flush claim.

The replay entry identifies the exact inherited standing, SM9LowerBoundOnly=true and no-page-cache resetLabel as **obsoleteInheritedFields**. Those copied values match the retained raw result. Its current standing instead names synthetic D-1 source-count scenarios at the six TS sizes, establishes no real-workload bound and makes any later F/T/outcome conditional on D-1. Current SM9LowerBoundOnly, lowerBoundEstablished and realWorkloadInference are all false.

REPORT.md now explains the supersession and labels every replay table row as a synthetic D-1 scenario. The audit requires the interpretation record, verifies its six result hashes and cold labels, rejects a current lower-bound flag, and pins the interpretation in its output. The original writer was inspected, not run. The retained historical fields no longer serve as the current interpretation. This implements the preservation-and-override correction allowed by RF-01 without rerunning measurements or modifying closed accepted source.

## Reset, placement and recipes

The reset module and six runner variants retain their round-1 reviewed bytes. Q0 §9.2's required absence/deletion of OpenSIP state, fresh process and disposable-cache reset are implemented by the recorded state-absence assertion, previous-run TMPDIR deletion, fresh empty private per-run directory and subsequent new child. The actual components declare no persistent analyzer cache; sealed inputs and runtime files remain inputs rather than disposable caches. Page-cache state is recorded through vm_stat, never purged or claimed flushed. The reset module itself was not executed in this review.

Rechecked each runner's parsed measured loop: reset remains its first statement, before child launch and measured timestamps, once per sample including warmups. Every reset record's call-site line agrees. The transfer refusal controls remain outside the sample loop and unchanged.

The accepted runner/source hashes and diff results in the updated checks equal the preserved round-1 checks. Cold runners remain confined to import/reset/write insertions and replay's size restriction/output redirect. Input/helper bytes, timing recipes, bounds and pins remain unchanged. The sealing attempt0 retains its empty stdout, missing-control-template failure before probe timing, runner/probe and logs; it is not promoted to a successful sample.

## Independent records and archive checks

Independently checked all **390 successful series children**, including warmups, and matching ordered reset records:

| Component | Children/reset records |
|---|---:|
| SM1 | 10 |
| Sealing | 130 |
| Transfer | 120 |
| Cohort | 60 |
| Synthesized Express | 10 |
| Replay | 60 |

Records have contiguous indexes, unique per-run TMPDIRs, empty-directory and absent-state observations. Raw vm_stat page sizes and file-backed/purgeable/free counters match parsed fields. Available start timestamps follow the reset-record timestamp; source placement keeps the completed reset outside the timed span.

All series retain ordinals0–9, three warmups and seven measured runs. Independently recomputed medians/maxima from the appropriate timed fields and matched the updated checks. All sixty replay children fully replay with findings equal count at sizes141,193,678,936,1159,1381. The component numerical checks equal round 1. Warm medians remain informational, with no budget, ratio or outcome inference.

Revalidated raw-evidence.tar.xz directly in memory against the index: **269 regular members**, exact membership, no duplicates or extras, every size and digest matching, totaling **105629308 logical bytes**. Archive SHA-256 remains `598f316c182892e061ec6b1c1050d12aad891b994a667c0f3cf96f86bac0aad0`. No member was extracted to the filesystem.

## Permitted audit and standing

Checked the working audit, interpretation and expected output against the stage before executing exactly:

`nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-cold-ts-2026-10-13/audit_cold_ts.py`

It exited zero and reproduced cold-ts-checks.json byte-for-byte: **10973 bytes**, SHA-256 `dd850eec7a97c15a1b1ce05076071c90f81fa534094b9e997e438d9000e834d4`.

No F, T, outcome or placeholder is recorded. SMComplete, LG1Met, effectiveL and productQualification remain false. Rust cold work follows U-1/U-2, and other report duties remain owed. O7, D3 and D13 remain closed; only L-G1 remains open among L's gates. The host remains preliminary, not D12.

Only read-only inspection, hashing, JSON/source parsing, Git queries, in-memory archive reading and the expressly permitted audit were used. Its authorized output rewrite was byte-identical. No Node, compiler, Cargo, runner, tests, lane, network, other pane or delegation. No private 413 fixture, installation directory, signing keys or held-tree content was read. Neither repository, stage, other working files nor control state was edited. Only REVIEW.md and review.json were otherwise written. Nothing was pushed. Exact lead assent and fresh design verification before publication remain separate lead work.

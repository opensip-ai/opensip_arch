# Codex review: SM-COLD-TS-r1 (U-5a)

**Verdict: REQUIRED-FINDINGS.** One required finding, **SM-COLD-TS-R1-RF-01**, concerning the current replay result's inherited but incorrect interpretation fields. The reset implementation, runner placement, retained measurements, statistics and archive otherwise check out. No nonblocking observations.

## Exact subject and boundaries

Stage: `/tmp/opensip-implementation/sm-cold-ts-r1-stage`.

`subject.json`: 137997 bytes, SHA-256 `6d04c3812e79538a1a94e97468adcb016d17679853995946be15c219ff3d0a21`. Independently rehashed all **607 members**; every size and digest matches. Live bases match clean product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` and architecture `32b4ba9bdd352c41e28d3761a3e53c49b0ebea3c`. Architecture's existing untracked held E2s directory was not read or changed.

Only read-only inspection, hashing, JSON/source parsing, Git queries, in-memory archive reading and the expressly permitted audit were used. No Node, compiler, Cargo, runner, tests, lane, network, other pane or delegation. The reset module was inspected, not executed. No private 413 fixture, installation directory, signing keys or held-tree content was read. Neither repository, stage nor control files were edited. The authorized audit-output rewrite was byte-identical. Only REVIEW.md and review.json were otherwise written.

## Required finding: SM-COLD-TS-R1-RF-01

The new replay/sized-replay-results-cold-ts.json presents its current standing as **LABELLED SYNTHETIC LOWER-BOUND GRAPHS**, sets **SM9LowerBoundOnly=true**, and carries resetLabel **fresh process per sample; no page-cache record; no Q0 9.2 cold label claimed**. The new variant emits those fields from its copied runner.

The accepted replay round-2 record withdrew the real-workload lower-bound interpretation after SM-REPLAY-SIZED-R1-RF-01. PLAN-r2 D-1 adopts a labelled source-count synthetic benchmark convention, with any later F/T/outcome conditional on that convention, not a real-workload bound. This cold series uses those same synthetic graphs. It does not establish the withdrawn bound. Its sixty new replay children also have actual cold-reset/page-cache records, so the resetLabel directly contradicts the current evidence.

The original runner's legacy text could remain as closed historical source. Here it is freshly emitted into a new result and is not marked obsolete or overridden. The top-level report does not explicitly withdraw these inherited fields, and the audit preserves no corrected replay-standing record. Downstream readers therefore receive two conflicting current interpretations.

**Required correction:** preserve the accepted closed runner and all raw measurement bytes. Correct the current replay interpretation across the new variant/result/derived record and report: synthetic D-1 source-count scenarios, no established real-workload bound, and “cold OpenSIP state, page cache recorded,” never claimed flushed. If keeping the generated result verbatim, explicitly classify its inherited fields as obsolete and provide a corrected current interpretation, retaining the original as history. This requires no measurement rerun or change to replay inputs, algorithms, limits, timing boundaries or owned parameters.

The requested structural checks remain true: actual page-cache records exist, resets precede samples and permitted runner edits are confined. Those verified facts do not make the conflicting current classification acceptable. No F, T or outcome has been computed.

## Reset and runner checks

Q0 DESIGN.md:798-807 requires absent/deleted OpenSIP state, deleted disposable caches, a fresh process and page-cache state recorded before every run, including warmups; flushing is not required. cold_reset.py asserts state absence, deletes the previous per-run TMPDIR, creates a fresh empty private directory, updates the child's TMPDIR and records raw vm_stat plus parsed counters. Each runner subsequently launches a new child.

A fresh per-run TMPDIR is a sound disposable-cache boundary for these components: the one-shot TS scripts make no persistent analyzer-cache claim and emit no repository code; the Python probes use isolated, no-bytecode execution; the replay state is rebuilt in a fresh process. Retained sealed read sets/runtime inputs are measurement inputs, not disposable analyzer caches. The reset does not purge the OS cache and claims no flush.

Inspected each sample loop through parsed source: the unique `for n in range(10)` loop starts with `_cr.reset(env,T)`, before child launch and measured timestamps. Reset-record callSiteLine matches the actual inserted statement for every recorded sample. The transfer refusal controls remain outside the measurement loop, as in the accepted recipe; they are not counted as cold measured samples.

Independently reversed each transformation to its accepted source. All six runners equal the committed accepted runner after removing the import, reset and record-write insertions, plus replay's six-size restriction and output redirection. Every copied ready/probe/receiver/compiler script, control template and packet-metadata file equals its accepted input. Recipes, pins, bounds and measurement spans are otherwise unchanged.

## Records, statistics and archive

There are **390 successful series children**, including warmups, and exactly one reset record per child: SM1 10, sealing130, transfer120, cohort60, synthesized10 and replay60. Records are ordered, indexes contiguous and per-run directories unique. All record absent OpenSIP state and an empty TMPDIR. Independently parsed each raw vm_stat and checked page size and file-backed/purgeable/free counters against the recorded fields. Available parent start timestamps follow the reset-record timestamp; source placement excludes the completed reset and vm_stat call from timing.

Every series has ordinals0–9, with exactly three warmups and seven measured samples. Independently recomputed medians and maxima from the designated timed fields and matched the audit. Replay sizes are exactly141,193,678,936,1159,1381. All sixty replay stdout records match their result rows, stderr is empty, complete replay passes and findings equals count. This confirms synthetic measurements, not a real-workload bound. The accepted warm column is informational; no ratio, budget comparison or outcome is derived.

Checked raw-evidence.tar.xz against its index: **269 regular members**, exact membership without duplicates or extras, and every size/hash matches, totaling **105629308 logical bytes**. Archive SHA-256 is `598f316c182892e061ec6b1c1050d12aad891b994a667c0f3cf96f86bac0aad0`. Members were read in memory without filesystem extraction.

The retained sealing attempt0 has empty stdout and a FileNotFoundError for control-template.json before the probe's timing begins. Its runner/probe equal the successful copies; the missing sibling template explains the failed launch. The successful copy's template equals the accepted one. Failed evidence remains historical and is not upgraded to a measured sample.

## Audit and standing

Ran exactly the permitted command:

`nice -n 10 python3 -I -B /tmp/opensip-implementation/sm-cold-ts-2026-10-13/audit_cold_ts.py`

It exited zero and reproduced cold-ts-checks.json byte-for-byte: **10771 bytes**, SHA-256 `052b417d787518f9307a581e678333a9a080b097348c47d393c2dd8b881a1017`. The audit correctly confirms runner diffs, reset counts and statistics; it does not detect the inherited replay interpretation defect.

No placeholder, F, T or outcome is recorded. SMComplete, LG1Met, effectiveL and productQualification remain false. Rust cold work follows U-1/U-2; remaining report duties remain open. O7, D3 and D13 stay closed, and only L-G1 remains open among L's gates. The host remains preliminary, not D12. Nothing was pushed; exact lead assent and fresh design verification before publication remain separate lead work.

# Review: SM-COLD-RUST-r1 (U-5b)

**Verdict: ACCEPT.** No required findings or nonblocking observations.

## Exact subject and boundaries

Rehashed subject.json in `/tmp/opensip-implementation/sm-cold-rust-r1-stage`:9412 bytes, SHA-256 `5029df9179126074eafc49b09f58d61df7541c437448df8803a4e5a051b77707`. All **43 members** match declared sizes and hashes.

Read all **601 archive members** in memory. Each matches its index size/hash and named external working original. Archive SHA-256 is `dabe906668ed9cca2f75510699759c4842d963f1fb66bbc66686cca8536b728d`. Nothing was extracted.

Live product HEAD is clean `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture HEAD is `d7abc70d0886ff8a66bb82f76d066a99a6dd54ac`. Its existing held E2s tree was not read or changed. Neither repository, stage, working directories nor control files were edited.

Only read-only file reading, hashing, parsing, source inspection and Git queries were used. No runner, audit script, image, Cargo, tests, lane, network, other panes or delegation. No private413 fixture, installation, signing keys or held-tree contents were read. Only this directory's REVIEW.md and review.json were written.

## Method and runner confinement

cold_reset.py is byte-identical to accepted U-5a's module. It asserts state absence, removes the previous disposable per-run directory, creates a fresh private0700 TMPDIR, updates the caller environment and records vm_stat. It makes no page-cache flush claim. This review inspected that code and its recorded results; it did not inspect the installation directory itself.

Verified every ACCEPTED-RUNNER-SOURCE hash and diff. Each runner adds only the import, one reset as the measured loop's first statement and the record write before lane release, plus the declared SM-4/replay redirections. AST inspection confirms a single reset-bearing measured loop in each runner, with its reset first; recorded callSiteLine values match. Timed operations remain after the reset.

SM-5 and SM-7 source pins are the published accepted U-2c two-part r2 and field-carrying r3 runners respectively. The copied probe and receiver match published sources byte for byte. Replay is restricted to exactly the eight Rust sizes and redirects its outputs; its measurement behavior remains unchanged.

The SM-4 exception is accurately disclosed: reset uses a placeholder parent environment and fresh output root, while compiler children use their constructed command environments rather than inheriting TMPDIR. The accepted executor passes constructedEnvironment to observation. The report does not claim a per-run child cache reset that this path does not apply; its reset contributes state absence and page-cache recording.

## Reset records and controls

There are **360 ordered reset records**: SM-3 10, replay80, SM-4 90, SM-5 90 and SM-7 90. These correspond to the measured series iterations, including warmups; SM-4 resets once per whole graph, not separately for each compiler subprocess, and untimed controls are outside this count.

Each component's indices are contiguous, monotonic timestamps increase, and TMPDIR names are unique. Every record reports state absent and a fresh empty per-run directory. Page size and file-backed-page values agree with the recorded vm_stat text; no record claims a flush.

SM-4's warm U-1 result rehashes to its accepted large-records index pin. Cold analysed/incomplete populations and newly analysed indices match U-1; every entry records population, read-set and metadata repetition. Independently checked unit-result index/standing/reason populations across all runs.

SM-5 shapes equal accepted U-2c shapes. Raw children reproduce their elapsed/part split and successful shape evidence. SM-7 snapshot and dependency manifest hashes and seals equal U-2c; all raw responses record digest/header verification and the expected seal. The positive control passes and all20 refusal controls remain present with nonzero exits.

All80 raw replay children report full replay passed and exactly one finding per source at sizes **71,98,192,208,239,279,301,808**. SM-3 raw ready markers and empty stderr match retained run observations, and ready-start equals the recorded duration.

## Statistics and interpretation

Independently recomputed seven-sample medians/maxima for all component rows, plus SM-5 part statistics, from raw children and result records. They match cold-rust-checks.json and report rounding. Every series retains three warmups followed by seven measured iterations.

R8 sums reproduce (median sum / maximum sum, ms): **SM-4 2216.124/2227.599; SM-5 250.833/253.218; SM-7 95.621/96.897**. These are sums of the separate entry statistics under D-3. Warm medians remain informational comparisons, not ratios or evidence of a cache-performance guarantee.

cold-rust-interpretation.json pins all five result files and exactly identifies their inherited standing text. Each inherited label is obsolete and superseded by the current cold label and preliminary scope. SM-4's environment limitation is explicitly recorded. Replay sets SM9LowerBoundOnly=false and lowerBoundEstablished=false and carries D-1's synthetic source-count scenario label. No real-workload bound is inferred from the inherited raw wording.

## Scope

This accepts cold-reset inputs for U-6, preserving the accepted component measurement boundaries and generated-input limitations. It computes no F or T, records no outcome, fills no placeholder and grants no admission or qualification. O7, D3 and D13 stay closed; only L-G1 remains open among L's gates. Full S-M, L-G1, effective L and productQualification remain false.

Nothing was pushed. Exact lead assent and fresh design verification before architecture-only publication remain lead work.

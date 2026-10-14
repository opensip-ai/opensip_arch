# Codex review: SM-REPLAY-SIZED-r1

**Verdict: REQUIRED-FINDINGS.** One required finding: **SM-REPLAY-SIZED-R1-RF-01**, the unsupported lower-bound sizing and resulting real-workload F/outcome inference. No nonblocking observations. The measurements, preserved transport refusal and separately pinned rows variant otherwise check out.

## Exact subject and boundaries

Manifest: `/tmp/opensip-implementation/sm-replay-sized-r1-stage/subject.json`, 116,787 bytes, SHA-256 `8db34d129e7458c3eb11c4f4fdf7582e8967496a6a7628d809671904729adcf0`. All **507 members** independently rehashed and matched. Bases remain product `95279fa8ae086f98bd221cd827f6c0efc156c0c5`, clean, and architecture `a208594febcad2e08439f379a50bb4e78b473ca9`.

No replay image, generator, converter, runner, Cargo, tests, lane, compiler, network, other pane or delegation was used. No private 413 fixture, installation directory, signing key or held-tree content was read. No repository, stage, working input or control file was edited. The expressly permitted audit rewrote its designated output byte-identically. Archive members were read and hashed directly without filesystem extraction. Only the two requested review outputs were otherwise written.

## Required finding: SM-REPLAY-SIZED-R1-RF-01

The recorded lead decision's sizing premise is not sound as a lower bound. REPORT.md:10 claims that one synthetic fact/finding per analysed source understates the real graph. The audit at :96 explicitly assumes that real graphs carry at least one fact **and one finding** per analysed source and uses monotone medians of the fourteen synthetic sizes as the replay-time ordering premise.

The generator at prepare_packet.py:8 deliberately applies an `exists` predicate over enumerated files and asserts exactly one finding per source. This is the fixture's chosen behavior. At the measured product commit `37581132`, evaluator composition.rs:871–894 evaluates a selected rule predicate and at :887–888 skips finding emission unless the result is true. Real rules can therefore emit zero findings for a source. The 208-source synthetic packet contains 208 fact, 208 finding and 208 finding-fingerprint objects; their existence in a real replay graph is not guaranteed by the source count.

Nor does the empirical monotonicity establish a timing order across different graph shapes, predicate work, descriptor/byte populations, rules or coverage. `replay_run` reconstructs and checks those semantic outputs, not merely a source counter. No graph embedding or work-dominance argument links the synthetic fixture to each real workload. The current-head replay is explicitly unmeasured, so the historical image also cannot silently supply a current-product timing bound.

The algebraic implication is correct **if** `SM9_lb <= actual SM9` is established for the relevant boundary/graph and all other F terms are nonnegative. The submitted sizing evidence establishes no such workload bound. Consequently, the nine synthetic scenarios whose every measured sample exceeds 2 s do not establish F>2 s or failure of (A) for the corresponding real workloads. The qualification “if the boundary and sizing stand” does not establish the unsupported premise.

**Required correction:** preserve the raw series, closed pieces, refused packet and transport variant. Relabel the results as workload-sized synthetic replay/scaling scenarios and remove the lower-bound/workload F/outcome implications from report, audit and derived labels, or supply an independently reviewable conservative sizing/work-dominance argument tied to the actual selected workload graph and replay boundary. A lead assumption plus monotone synthetic medians is insufficient.

The independently checked output differences are:

- `lowerBoundLabelSound=false`.
- `workloadsWhereLowerBoundAloneExceeds2s=[]`: no justified workload-level lower bound is established.
- `workloadsWhereANotEstablished`: all fourteen workload rows, because neither a measured full F nor a valid lower-bound failure establishes (A) or its failure for them.

The numerical nine/five split in the submitted audit remains correct **for the synthetic scenarios**, not for justified workload lower bounds. The review JSON's changed lists refer to established real-workload inference, not a change to those retained measurements.

## Closed pieces and historical product boundary

`prepare_packet.py` and `remint_selected_schema.py` are byte-identical to the accepted native-spike copies. Both raw and selected packet193 reproduce the accepted packet bytes; selected193 SHA-256 is `f33da67037c8bf6d67b2694ce7f4833f70f78549ace1bcf6ca4cded88d593e32`.

The closed release image rehashes to its unchanged `native/build-release.json` pin `e82a4e2f5f487c7c9d272f4a9af5c337d61ff6868eaa165c8ea277f876b8a843`. The selected native-v2 schema exactly equals the Git blobs at both `2fbb75c^` and `37581132`; its SHA-256 is `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773`. The schema-difference record changes only its source pathname from the accepted spike.

Series1 retains nine completed sizes, exactly the selected packets fitting 4,194,304 bytes. At size678, child0 has empty stdout and the retained `ByteLimit` panic at main.rs:9, before `replay_run`. Product canonical.rs at37581132:5 retains its 4 MiB MAX_BYTES. Larger whole packets are over that transport cap; they are not represented as completed series1 runs. No bound was raised.

## Rows variant and export

The rows main differs from the closed main only in input loading, replacing whole-document parsing with header/object/blob lines and checking header counts. Every row uses the same product `parse_json` cap. Registry construction, retained inputs, traversal/replay budgets and the timed `replay_run` interval are unchanged.

Cargo.toml changes only the three product dependency roots to the historical export; Cargo.lock equals the accepted lock. The release build recipe keeps the build command, flags and lane behavior, adding variant/product-export recording fields and labels. The retained first build has a shortened recorded productCommit; the corrected record pins the full historical commit. Both records have the same image digest. The final staged image equals the original built executable: 5,553,280 bytes, SHA-256 `7635c002b2ed877f89582360b6eae54e8de1a6c91811a4f188b083919609fc24`.

The permitted audit checks the complete product export against `git ls-tree 37581132`. An additional independent check confirms **1,082 export files** match Git blob bytes and file/symlink/executable modes. No exported product source was edited or built in this review.

The converter copies replay input values rather than deriving new identities. Independently reassembled every row set: runId, ordered objects and blobs equal the selected packet's consumed inputs. Unused top-level documentary keys are explicitly disclosed as ignored. All row maxima are below the unchanged cap; largest is 1,776,379 bytes.

## Packets, samples and audit

The xz archive hash matches packets-index.json. All **42 regular members** match exact membership, sizes and digests, totaling 203,895,879 logical bytes. Every archived raw/selected packet and rows member matches the packet metadata and conversion record. No missing, extra, duplicate or nonregular member was accepted.

Independently compared every completed child stdout with its result row, checked empty stderr, three warmups plus seven measurements, priority readback10, `fullReplayPassed=true`, findings equal count, repeated object/blob populations and whole-process intervals containing the replay interval. Recomputed replay medians/maxima and whole-process medians.

Series1 has 90 successful children over nine sets plus the retained failed child at678. Series2 has **140 successful children over fourteen sets**. The runners retain the closed recipe's priority, private TMPDIR, owned lane and binary/input rehashing; their parameterization/transport changes do not alter the timed replay computation.

For the nine overlapping sizes, object/blob populations match and every child fully replays. Median ratios range 0.96513–1.03585: descriptive agreement, not a statistical equivalence or lower-bound proof. The fourteen series2 medians are monotone; the slope remains descriptive with no extrapolation.

Ran exactly the permitted read-only audit. It exited0 and reproduced the frozen 16,963-byte output exactly, SHA-256 `4354c12e071d8f2518381b805601ff42d9e24c41ef7dea0ce89b95a7493a6632`. This reproduction validates the recorded arithmetic and custody, not the unsupported lower-bound premise.

The workload sizing numbers match the earlier cohort reports and RUST3-LIM counts. Napi has separate TS193 and Rust239 rows; Express uses its141 synthesized-program roots; the Serde/JSON overlay is279. The synthetic threshold comparison uses the minimum of all seven measured samples, rather than the median alone. All seven exceed2s for the reported nine scenarios; the remaining five do not. These observations remain valid as synthetic measurements.

## Disclosures and standing

The measured code is historical product37581132. The report explicitly discloses current-head registry/schema/data-module changes and no current-head replay timing. Source comparison supports its unchanged production replay/composition logic and evaluator include-source changes. Synthetic findings are not compiler outputs or admitted sources. Fresh-process samples on the lead macOS host have no page-cache reset record, so neither Q0 cold/warm nor D12 qualification is established. No total F/T value, formal S-M outcome, SM9 placeholder or complete figure is recorded; the disputed inference must still be corrected.

Product, lock, inventory187 and contracts161 remain unchanged. O7/D3/D13 remain closed, L-G1 remains open, and full S-M, effective L, native admission and qualification remain open. `SM9FigureComplete=false`, `FComputed=false`, `TComputed=false`, `outcomeRecorded=false`, `SMComplete=false`, `LG1Met=false`, `effectiveL=false` and `productQualification=false` remain the actual formal standing. This review rejects the lower-bound interpretation; it does not discard the useful measured series or reopen accepted predecessors.

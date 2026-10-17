# M3-C r9 item-2 law record review

Verdict: **REQUIRED-FINDINGS** — three required corrections and three non-blocking observations.

## Exact subject and permitted verification

Verified the 2,718-byte manifest SHA-256 `243c91b2440d4084055fd7bd0675645313fadabb108736d5f9681f4028161eb3` and all 12 members. The record is 16,096 bytes, SHA-256 `26e22d1b2063875639db225af96b876619a708f7b6cca425fd50892c2fcaecae`. Rehashed all members again before writing. Product HEAD is the manifest's `e937dac74c8e529fee3efb6f84439d05280e48ea`; architecture HEAD is `3f930927dc288f6bdbd9fe9ec826564ad2f74081`.

Read M3-C item 2 and the C1a r6 gate/derivation/blind protocol, the native/model charging paths, the candidate sealing charge sites, the census script and its recorded ids/counts. The archived census script is byte-identical to the C1a4 candidate. The recorded model/tool hashes match the inspected main inputs.

Ran only the three expressly permitted model-only scripts, with `python3 -I -B` from product main and explicit product/architecture/sealing or packages-root arguments. All completed successfully and reproduced the recorded numerical results. No census was executed. Model-only arithmetic is reproducible; the findings concern its claimed coverage and assumptions, not a transcription error in those results.

## Required findings

### M3CR9-R1-RF-1 — Discovery depth 256 does not bound the snapshot row charge

Location: `docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md:35`.

term_a.py reads MAX_LISTED_DEPTH from the discovery model and uses it to bound target counts and the rowPathByteDearest coefficient (267), then calls the row subtotal a worst-branch bound. The snapshot walk has no such depth limit, as section 2 itself establishes; LogicalPath allows 4096 scalars. A concrete coefficient counterexample is 580 successive target directories, no Cargo marker, and 1000 empty leaves n000..n999. Each row path has 4064 scalars. The record's own canonical descriptor recipe gives 4162373 bytes, below 4194304, with only 1000 rows and zero payload bytes. Native classify_cost alone charges 584 objects and 2453360 bytes per leaf: 581*16 + 4064*(3+580) + 584*128. The 1000 leaf classifications therefore cost 2453360000 bytes, exceeding the entire stated row-byte bound of 2318979168 before listing/open/custody/session charges. This is a synthetic arithmetic counterexample, not a corpus access. It invalidates the worst-branch proof, even if corrected arithmetic ultimately rounds to the same caps.

Required change: Derive snapshot depth and target-count envelopes from the actual snapshot/LogicalPath rules, not discovery's listing policy. Recompute the per-row and cap-bounded terms (including object costs of target classifications), the subtotal and rounded recommendation; add a model-only beyond-256 regression case. Alternatively explicitly move the extra classification work into the typed-refusal regime and revise the claimed bounded term/guarantee accordingly. Do not silently impose a new snapshot depth exclusion.

### M3CR9-R1-RF-2 — Include D15 member-root classification charges in the derivation and workspace census

Location: `docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md:130`.

Both term_a.py and the census instantiate SnapshotModel without members. snapshot_ledger_census.py:150 composes workspace trees but never passes their member roots to price or SnapshotModel. The accepted model's classify and native snapshot_walk.rs::classify_cost explicitly add one object per nonempty member root and 16 bytes per member-root segment on every classification, and perform an additional charged classification for .opensip names. Omitting boundaries may enlarge the extent, but it does not make omission of this positive per-name work conservative. Neither the universal worst-branch subtotal nor the workspace margin evidence currently covers those charges.

Required change: Price each lead-readable workspace with its actual admitted member-root set, or prove a conservative upper charge that includes it. Bound the member-root terms using their owner's limits, or explicitly assign them to the additional-work refusal regime rather than calling the zero-member subtotal universal. Account for the .opensip double-classification branch. Have the lead regenerate the affected evidence; retain the no-held-out/no-tuning protocol and reassess the caps after correcting the model inputs.

### M3CR9-R1-RF-3 — An enlarged no-boundary inventory cannot prove an entry is over item 5

Location: `docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md:157`.

The census deliberately applies no admitted boundaries, then labels an enlarged inventory over-item-5 and excludes it from maxima. Section 6 strengthens that result to cannot seal. Boundary removal is conservative for positive work when the enlarged tree remains within item 5; it is not conservative for deciding which samples may be discarded. Nested repository/project or custody/depth boundaries can remove enough regular rows for the actual admitted inventory to fit while leaving substantial listing work. The record gives no boundary comparison or proof that the five oversized enlarged trees also exceed item 5 under their actual admitted extent. Thus their exclusion does not establish the claimed coverage of every lead-readable entry within item 5.

Required change: Separate conservative work pricing from eligibility classification. Prove over-item-5 against each entry's actual admitted extent, or conservatively retain an enlarged-but-oversized entry as unclassified/covered rather than discarding it from the margin population. Record the evidence for every exclusion and recompute maxima/margins where necessary. Do not assert cannot seal solely from a no-boundary superset, and do not inspect held-out inputs to resolve the issue.

## Findings, recommendation and reviewer questions

**The two findings.** Charging 100,000 rows at the recorded 18-object new-blob branch gives 1,800,000 objects, exceeding r8's 1,048,576. That arithmetic correctly refutes the stated coverage premise for that componentwise reference calculation, with NBO-3's cheapest-row qualification. The cap-limited terms also reproduce the reported tens-of-gigabytes effect: `(a)` is `(4,230,998 objects, 17,499,108 edges, 37,517,042,501 bytes)` under the script's assumptions. It is a conservative sum of separately bounded terms, not an attained adversarial tree or a proved global supremum. RF-1 and RF-2 prevent accepting it as the complete worst-branch derivation as written.

**Q1's refutation.** The beyond-discovery-depth synthetic case reproduces snapshot marginal `(8, 2, 20,107)` against discovery `(0, 0, 0)`. This suffices to refute any finite discovery-charge multiplier over that whole extent. The within-tested-envelope classification asymmetry is real: non-directory names are classified by snapshot while discovery classifies child directories. The reported factors and hypothetical `(a')` reproduce, but are not universal maxima over deeper paths or omitted member inputs. Closing only the extent would still require a fresh bound rather than treating those sampled factors as a proof.

**Recommendation / record Q1.** Using bounded intrinsic terms plus an empirical coverage test and typed refusal for additional work is a reasonable proposed law choice. It is an explicit revision to RF-2's cap-bounded derivation, not an unchanged consequence of that requirement. The gate permits a separately reviewed law decision; the departure must remain explicit. It cannot yet be accepted on a worst-branch subtotal and census coverage that omit admitted cases.

For the numbers presently printed, doubling the componentwise larger of the subtotal and recorded census maxima and rounding up gives exactly `2^22`, `2^25`, `2^33`. Their arithmetic is correct. The empirical figures also reproduce: 44 priced entries/workspaces, 39 measured and five classified oversized; measured maxima `(529,517, 1,487,988, 211,620,369)`; webpack and rspack fail the recorded r8 2x tests. Against the recommended caps, these recorded measured values have minimum margins of 7,920 / 22,550 / 40,591 per mille. These statements describe the recorded zero-member, no-boundary model runs; RF-2 and RF-3 block extending them to complete admitted-population coverage.

Rejecting unchanged r8 caps and a census-only derivation is well motivated; neither establishes the desired reference coverage. Rejecting `(a')` as unsound is justified by the zero-discovery-charge counterexample. A 2^37 charged-byte cap can be rejected as a lead resource-policy choice, but cumulative charged storage is not peak RSS, and an infeasible componentwise sum is not a measured memory-exhaustion case. Do not claim that numerical alternative alone proves actual memory behavior.

**Pre-walk captures / record Q3.** The ledger separation is correct under PLAN-r6: B2/C2 pre-walk capture opening/read/record work goes to discovery, while snapshot pays its later walk; reached captures avoid a second read/record. Sealing's first leftover refusal adds at most one owned path copy. The permitted captures script reproduces the stated opener and discovery-exposure numbers. Future B2 routing through the session must return to M3-B's pricing/census and review; this record cannot silently enlarge discovery caps or settle C2's currently open read-count bound. Memoizing directory judgments needs its own custody/change argument.

**Record Q2.** Neither proposed code remedy is automatically required merely to choose a finite refusal budget. Correct the bound and census first. Flattening classification would require updated native/model equivalence. Adding a snapshot depth cutoff changes the reached extent and needs explicit authority; it cannot be introduced as a cap-only optimization.

**Supersession / section 7.** The list correctly distinguishes the effective item-2 caps/derivation and C1a r6 recommendation from immutable historical snapshots, and correctly schedules the main model constants/docstring for C1a4. Discovery's caps remain separate. Keep C1-T27, typed exhaustion, the all-three-cap census obligation and the full RF-3 blind-validation sequence: choose caps without held-out data, freeze constructor and final closure, then one separately reviewed blind validation; failures return to the law. This review neither accepts a snapshot profile nor refreshes a receipt.

## Non-blocking observations

**M3CR9-R1-NBO-1 — Pin the candidate sealing input and keep its acceptance dependency explicit** (`docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md:15`). The manifest pins the scripts and outputs but not the live C1a3 snapshot_seal.rs whose coefficients enter the law. On this review it is 15993 bytes, SHA-256 bf009872fb5ab0bcc5789665a78a6905df33d39ab459e2df122fdf2dbacb8289. Anchor matches alone do not freeze the complete sealing charge sequence. Record the exact candidate pin and require re-derivation if C1a3 review changes the charged sites; this law review does not accept that candidate implementation.

**M3CR9-R1-NBO-2 — Distinguish walk-plus-session margins from the completed ledger margin** (`docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md:104`). The census honestly prices walk plus session, but sealing is also snapshot-ledger work and the leftover refusal can add one path copy. Include or explicitly upper-bound those terms when claiming the full ledger has a 2x margin. With the current recorded inputs, adding the stated worst sealing term alone gives maxima 529528 objects, 1488056 edges and 220010832 bytes, still far below the proposed caps; this observation alone does not require changing those caps.

**M3CR9-R1-NBO-3 — Use feasible examples and distinguish worst-branch charges from cheapest rows** (`docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md:56`). The 18-object row uses the new-blob session branch; repeated empty files take the cheaper duplicate branch, so it is not literally the cheapest repeated empty row. The conservative reference-population calculation can use the dearer branch, but should say so. Also section 5's example of a tree within item 5 with 100000 rows is infeasible under the same 4 MiB descriptor argument already given in section 1. Use a feasible row count when illustrating listing-budget refusal.

## Census custody and review boundaries

The lead-only filter and discovery_census.store_path rejection precede store access. verified_tree rechecks the pinned store representation; verified_workspace verifies overlays, mounts and member links through that path. Outputs contain ids, charges, bound/status/margin data and pins, not tree paths or contents. Distinct stand-in file contents intentionally select the new-blob branch. These aspects of the method are appropriate; the coverage defects above are separate from corpus custody.

No held-out material, private 413 fixture, installation, signing key, held tree, T2 store or T2 cache was read. No corpus manifest contents were needed beyond the pin already present in recorded evidence. No census, compiler, Cargo, build, lane, network, other pane or delegation was used. Neither repository, worktrees nor control files were edited. Only the requested REVIEW.md and review.json were written.

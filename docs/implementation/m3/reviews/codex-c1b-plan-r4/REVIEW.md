# C1B-PLAN-r4 review

**Verdict: REQUIRED-FINDINGS — one required finding, no non-blocking observations.** The revised pricing approach and normal typed-refusal mechanism are reasonable, but the evidence does not yet price its claimed maximum VCS record correctly. No code is accepted.

## Subject and verification

The manifest is 1,802 bytes, SHA-256 `c462ecae40f662794297b253972d1d8df9bfdcbec668ce83e7be7892de025025`. All eight members match their declared lengths and hashes, including PLAN-r4.md (44,459 bytes), both scripts and outputs, and unchanged historical plans r1–r3. Live product `caa71e2fd481977d066d67465add64f4393334f9` and architecture `9cf1c10db88e1c78d87b2666f53440593ab8a7da` match the manifest bases.

Read the plan and r3/r4 diff, prior acceptance, r9 guarantee/refusal text and subtotal evidence, source pricing/reader definitions, LogicalPath and canonical encoder rules, and both local Git manual pages. The discovery cost closure’s 19 source pins were checked against current bytes. Independent read-only arithmetic from those source constants reproduces the published r4 term vectors at the derived boundary, one directory past, one HEAD byte past, and uniform INDEX_CAP HEAD. The evidence scripts themselves were not executed.

No Cargo, rustc, build, lane, evidence script, network, private fixture, installation directory, key, held tree or T2 store/cache was accessed or run. No other pane or delegation was used. Neither repository, worktree nor control file was edited. Only REVIEW.md and review.json were written.

## Required finding

### C1BPLAN-R4-RF-1 — Price the VCS record’s canonical encoding, including escaped member paths

P2; `c1b/r4-evidence/vcs_term_r4.py:109`; corresponding claim in PLAN-r4.md:159.

The purported maximum record allocation is `owned(MAX_MEMBERS * (LOGICAL_PATH_MAX + RECORD))`: 270,336 payload bytes plus 128 bytes of owned-record overhead. It substitutes raw path length plus fixed slack for canonical encoded length.

LogicalPath permits quote characters and non-NUL control characters. The canonical encoder, and C1a3’s string_len/push_string, expand quotes and controls. An independently constructed schema-3 record with 64 distinct, sorted, 4,096-character paths encodes to **529,190 bytes** using the canonical JSON rules for these ASCII inputs. Each path has 17 segments of 240 characters, with quote characters and distinct two-hex-character suffixes. They obey the per-segment bound and contain no backslash, NUL, empty, dot or dot-dot segment. This is already **258,854 bytes more** than the claimed maximum payload allowance; it is a counterexample, not a claimed true maximum. Control-character cases can require still more escaping.

Consequently the printed arithmetic is reproducible, but the asserted complete term, total and residual byte margin are not a sound maximum for the admitted record. The future C1b-2 charge-site equality cannot repair an underpriced C1b-1 derivation after acceptance.

**Required change:** derive the allocation from the actual schema-3 canonical encoding, including fixed syntax, top-level/member fields, separators and the maximum encoded path payload under canonical escaping and UTF-8 rules. State borrowed/temporary ownership explicitly. Update the script, outputs, search and residual-margin figures, and require encoded-length/allocation controls with quote/control/non-ASCII paths. Revisit the caps/law gate if the corrected complete derivation requires it; do not assume the current D*/H* or byte-margin figures survive unchanged.

## Requested dispositions

1. **Exact-format pricing and Q7.** The existing closed supported forms justify pricing a successful loose ref at 40 lowercase hex plus LF (41 bytes) and symbolic HEAD at `ref: ` plus its target plus LF; detached HEAD is 41 bytes. The local repository-layout and symbolic-ref manuals support the direct/symbolic-ref structure. The exact newline/lowercase/one-level policy is also the plan’s explicit closed subset, rather than a claim that every possible Git layout is supported. X2’s refusal of extensions keeps the selected object names SHA-1. Packed-refs remains priced at 4 MiB. Keeping the Q1 refusal caps while pricing admitted forms at their actual lengths is coherent; malformed inputs are charged and refused, never observations. Q7 is ruled below.

2. **D*/H* and arithmetic.** The script searches D first at its shortest HEAD, then H at that D, checking all three 2x inequalities. These are derived coordinates of a conservative pricing envelope, not product constants. The independent source-derived calculations match the published term `(173770, 2165048, 1643899072)` and total `(950446, 8383512, 4182771458)` under the script’s current allocation assumption. Doubling gives the printed component values. At D+1 the edge total doubled is 16,783,794, above 2^24; at H+1 the buffer growth makes the byte total doubled 8,638,173,066, above 2^33. Member reach, .git reopen, custody captures, ref-directory work, all three file reads/parses and retained target/commit values are enumerated. RF-1 concerns the remaining record allocation and invalidates completeness of the whole derivation. Neither “one more fails” result proves immediate runtime budget exhaustion; it proves loss of this 2x envelope.

3. **Q6 and r9.** R9 already makes fit conditional on aggregate non-row work staying in the remaining margin, and the main law requires typed exhaustion rather than truncation. Adding charged VCS work consumes that allowance. It does not establish an unconditional fit promise for every file below its refusal cap. The plan’s claim that no owner bounds HEAD’s length should be qualified: the reviewed Q1 read cap does bound it at 4 MiB. That refusal bound is not a guarantee that all associated work fits at 2x. Operational exhaustion may occur before malformed-layout/oversized classification, and must produce no partial observation. No cap or law-record revision is necessary merely for that existing operational behavior; the complete corrected derivation is still required before its quantitative guarantee is accepted.

   The subtraction used for the displayed residual margin is arithmetically correct under the supplied total: caps minus subtotal minus VCS term. It is not a new unconditional guarantee or a reservation of a separate ledger. RF-1 requires the byte figure to be recomputed. The original conditional guarantee must continue to count VCS and all other non-row work together.

4. **ENAMETOOLONG.** Mapping a target component rejected by its native no-follow open to ref-name, never absent/unborn-head, is consistent with the existing malformed-name distinction. It imposes no invented name-length constant and must retain the member-specific refusal projection where applicable.

5. **Controls/mutation.** The added remaining-work-budget and too-long-component controls target the new distinctions. The budget-to-truncation/unborn-head mutation is meaningful. They correctly exercise actual remaining allowance rather than branching on D*/H*. Add RF-1’s encoding/allocation controls to the implementation gate. Nothing was run here.

6. **Regressions.** The diff preserves the lending/same-root join, no-follow per-read custody/evidence recheck, innermost selection, one-level symbolic resolution, loose-ref precedence, dirty meaning, schema preservation, typed J2 projection and combined census-batch protocol. C1b-1 still owns the complete model/vectors/derivation before its acceptance; C1b-2 owns exact sealing and charge-site equality without inventing a second term. Output checks remain separate from freshness, and the blind refresh stays after C1b-2. The historical r2 table’s obsolete statements remain superseded by the current split and r3/r4 rules. No caller, qualification or new product bound follows from this plan review.

## Rulings

**Q6:** No law-record revision is needed merely to charge VCS work to the existing snapshot ledger and return WORK.BUDGET_EXHAUSTED when the aggregate remaining allowance is exhausted. R9’s guarantee is conditional on all non-row work, including VCS, fitting its remaining margin; the VCS charge consumes part of that margin rather than changing the caps. D* and H* are evidence-envelope coordinates, not runtime thresholds: exceeding either does not itself require refusal or prove exhaustion. Do not justify this by saying HEAD has no owner length bound: Q1 supplies the 4 MiB refusal cap, which is distinct from a guaranteed 2x-fit envelope. The current numerical guarantee remains unaccepted until RF-1 corrects the complete term. A broader unconditional guarantee or a cap change would require a reviewed law-record revision.

**Q7:** Retain INDEX_CAP as the reviewed 4 MiB read/refusal bound for HEAD, loose refs and packed-refs. Accepted closed forms can be priced at their actual lengths while malformed/long symbolic inputs consume charged work and refuse through the existing unsupported-layout or budget route. Reducing the loose-ref cap to 41 bytes would change the already selected symbolic-ref-chain versus oversized classification. Preserve exact-cap/one-over controls and never treat a budget failure as a partial observation or unborn HEAD.

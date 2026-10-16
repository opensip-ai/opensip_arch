# REQUIRED-FINDINGS — C1a implementation plan, round 3

Subject manifest SHA-256: `c3b9e01cec0491c5bb6fbf73f65c2a1d8c404130562ba94f71761bcd95e23f10`. All three members match their declared byte counts and hashes. r1 and r2 remain byte-identical to their reviewed subjects. r3 is 33,746 bytes, SHA-256 `0da453d240e73f56eb0aa888f721dd488fdfea29cbd42d58d13d88a97ce7d97b`. Product HEAD is clean at `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `43402bbc8543b0e4f265bcb4fd482c1c113f562c`.

## Prior findings and Q4

- **C1APLAN-R2-RF-1:** Substantially addressed by charge-type coverage, a finite per-file attempt envelope, charge-before-attempt, explicit terminal exhaustion, duplicate handling and worst-envelope controls. The object/edge-constrained maximization is a useful conservative approach. Its name-cost coefficient is still wrong (R3-RF-1), so the maximum and margin claims are not yet established. The finite envelope limits short reads and interruptions; it cannot guarantee completion for every possible short-read sequence, and the explicit exhaustion outcome must remain terminal.
- **C1APLAN-R2-RF-2:** Resolved at plan scope. The walk now holds the enumerating parent, performs observation and open relative to that same descriptor, compares identity/type and checks child directories before descent. Pre-captures retain their separate root-relative traversal, but reuse joins to the walk's parent-relative observation. C1A-T5 supplies the ancestor replacement control.
- **C1APLAN-R2-RF-3:** The incorrect inventory-only descriptor check and LD-C1A-8 are withdrawn. Full canonical descriptor admission and the inventory-fits/envelope-does-not control resolve that part. Restoring semantic checks to step 5 is correct. However, the new payload optimization does not preserve all walk-phase observations (R3-RF-2).

**Q4: a law clarification is needed first.** The 8 GiB bound establishes admissibility; it does not, by itself, authorize replacing later content reads with metadata-only observations while claiming the same refusal behavior. The proposed bounded-disk objective is reasonable, but its incomplete-capture state and precedence need an explicit owner decision in the law.

## Required findings

### C1APLAN-R3-RF-1 — The name-cost coefficient uses a byte limit the law does not impose

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r3.md:111`. The per-listed-entry type prices owned(name bytes) with names at most 255 bytes. M3-C item 2 instead permits 255 Unicode scalars per segment; such a UTF-8 name can exceed 255 bytes. The existing walker explicitly uses MAX_COMPONENT_BYTES = 1023, and invalid raw names also require charged capture before their eventual Name refusal. Therefore the proposed coefficient is not an upper bound for every listed entry. An exact optimizer and a 2x multiplier cannot establish the claimed maximum when its input cost bound is wrong.

Required change: Derive name/path byte envelopes from the actual platform observation limits and the logical scalar limits at their respective stages, including invalid names retained for an escaped refusal. Price actual byte copies and classification temporaries with those envelopes. Add multibyte 255-scalar and oversized/raw-name model controls and a mutant restoring the 255-byte assumption. Feed the corrected bounds into the exact solver before accepting the cap.

### C1APLAN-R3-RF-2 — The payload guard still changes walk-phase observations and needs a law decision

`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r3.md:211`. Q4 cannot be answered yes from item 2's payload-volume sentence alone. LD-C1A-10 stops content reads but claims every walk-phase refusal is preserved by continuing opens and metadata samples. A later file can open and have stable metadata while its Read operation would fail; the guard suppresses that read failure and instead reaches SnapshotBound. It likewise omits the actual read interval whose metadata comparison normally detects ChangedDuringRead. Samples around no read do not prove observational equivalence to the law's walk/read phase. The quoted 8 GiB admission bound does not specify this replacement algorithm or its failure precedence.

Required change: Obtain an explicit M3-C clarification or amendment authorizing the over-volume incomplete-capture state, the observations skipped, and the resulting refusal precedence before implementing LD-C1A-10. Define bounded actual-byte handling for a file that grows or whose stat size is stale, and ensure no partial capture can seal. Include mixed-error controls with a later content-read I/O failure and changes during the would-be read, in addition to custody/open failures. Alternatively remove the optimization and retain the currently authorized walk semantics.

## Other requested decisions

The full r2-to-r3 diff was inspected. The new retained-parent opening rule, custody duplicate decision, cost model, read-attempt envelope, withdrawn incremental bounds, payload guard and added controls are all included in the r3 change record. Historical r2 prose remains historical where r3 explicitly withdraws it.

**Q1 / split:** Security can open and judge descriptors without reading source content, while `snapshot.rs` owns the sole source-read loop and custody accepts chunks. The expanded source pin and pre-capture/reuse control remain appropriate. The new parent binding preserves the law's same-parent discipline without copying the shared extent rule.

**Q2 / profile and receipt:** The separate constructor is still justified: global `with_limits` cannot provide the required caps, and the discovery profile has a different object cap and separately fixed bytes. The recipe must precede C1a1's constructor. The planned whole-file re-pin, explicit stale state, unchanged discovery-cost projection and pre-/post-reviewed C1a4 refresh remain a sound sequence. Failed margins return to the law, with any later cap change causing another re-pin and reviewed refresh. No corpus measurement or run execution is authorized or claimed by this review.

For the mathematical implementation, an exact continuous relaxation can upper-bound integer operation counts; fractional vertices must be represented exactly or rounded upward, never truncated into an alleged upper bound. Any additional population constraints must be proved for the whole walk being bounded, including walks that will fail at final sealing, rather than assumed from the final 100,000-row admission limit. These are proof obligations for the planned model/solver evidence, not completed results.

**Q3 / interim VCS:** The authenticated NoRepository/no-member gate and internal `SnapshotVcsPending` remain appropriate. Git roots and D15 members wait for C1b. The I-complete released-read constructor is separate from writer authority; the I-absent route remains explicitly gated on E-1/S7b and J2c.

**LD-C1A-2 to 6 and 9:** Shared extent reuse, a single reused buffer, caller-supplied private custody, no ambient TMPDIR selection, and empty read-set support pending C1c remain sound directions. In-memory duplicate resolution is supportable under the stated fresh, exclusively owned, immutable-per-digest invocation custody premise: the incoming bytes are still hashed/length-checked, committed entries are not overwritten, and later consumers verify custody on their own ledgers. The pending implementation must enforce that premise and cannot generalize it to pre-existing or externally writable custody.

**Carrier and sealing:** Building the presence/digest observation from B1's captured project carrier remains correct. The seven-row join stays complete, with local/member carriers outside the root join, no X2 bytes used as source, no retry, and no partial snapshot minted. Full descriptor admission through `IdentityCandidate::from_json`, canonical source-inventory hashing and operational-field exclusion remain appropriate. C1b, C1c and J retain their VCS, read-set, composition, public-projection and end-to-end duties.

Planned suites, warning-denied Clippy, formatting, vectors, source pins, FW-01/environment checks, design verification, soundness comparisons and mutations remain necessary implementation checks. They were not run in this plan review, and they must include the additional controls in the findings.

No non-blocking observations. This is a plan review, not implementation acceptance, product qualification or C1 completion. Review used only file reading, hashing, JSON parsing and Git queries. No build, test, generator, network, delegation or prohibited private-data access occurred. Only this directory's `REVIEW.md` and `review.json` were written; neither repository was edited.

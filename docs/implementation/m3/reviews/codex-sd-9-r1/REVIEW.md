# SD-9-r1 review

**Verdict: REQUIRED-FINDINGS.** Two required findings; no non-blocking observations. The ledger lifetime, interim constructor choice and row-11 projection are acceptable in principle. The census landing rule and the numerical model's feasibility claims need correction. Q-SD9-1 through Q-SD9-6 are ruled below.

## Subject and permitted verification

Independently verified the 977-byte subject manifest, SHA-256 `de7db21190f3d9b1d2c2d1e5f062f179843f2a09bcb418f25d7b7b1c9aabaf4a`, and all four member lengths and hashes:

- README.md: 22,187 bytes, `3be5e1fe4f9e7dcf8418914fce61ff28e48968c6c2cf0d0a9ca0bbf9834805e4`.
- evidence/build_sd9.py: 3,665 bytes, `e6ee6ccbfbea48dc2c292a7e2a4e459fccc16ee6a3aa57f5632cde047780cd19`.
- evidence/check_sd9.output.json: 8,693 bytes, `ceb5964f88774cb3b1a9af3fd17ef0f054d90a0e00b66e401546739895412dbc`.
- evidence/check_sd9.py: 13,420 bytes, `c6cb0efe033595ecd1d1f3fcade51ba32e070680f1c1eb7a9fcba505580e460a`.

Inspected the record and both scripts, their cited C2a/D4/CI/J1 authorities, R9's cap rule and RTC section 7.4. Product source inspection uses the exact base `274dccc5eced53828f444fa44e62cdeffabc2d0c`. The builder verifies that architecture base `c6c7d4acf0d4836ef3bb72cb2bcb8950a75530a2` exists.

Ran both expressly permitted commands from opensip_arch. check_sd9.py succeeds and its stdout is byte-identical to the archived report. build_sd9.py --check succeeds and compares the manifest and draft unit record without writing either. The draft unit record is not included in this review subject.

The checker reads and records 12 architecture authority hashes and nine product-source hashes, checks its anchors, extracts existing caps and relevant price expressions, and reproduces the table. The checker alone records hashes; the builder's equality check against the pinned archived report supplies the drift comparison. These checks establish reproducibility and source identity, not completeness of the accounting formula or production qualification.

## Required findings

### SD9-R1-RF-1 — Make confirmation of the existing caps consistent with the census rule (P2)

**Location:** `docs/implementation/m3/supervisor-d/sd-9/README.md:113-119`.

LD-S9-5 says the procedure derives, rather than chooses, each cap as the smallest power of two at least twice its census maximum. The next step permits keeping all snapshot_profile caps whenever those derived values are merely less than or equal to them. Strict inequality selects larger caps than that rule derives. For example, a census yielding a 2^20 edge rule value does not derive the existing 2^24 edge cap. The cited R9 rule uses an exact minimum-power derivation, not an arbitrary larger existing profile. The unchanged-constructor branch therefore cannot be described as application of the stated rule or as replacing the interim with those rule-derived caps.

**Required change:** Require equality of all derived coordinates to confirm snapshot_profile under the stated exact rule; otherwise land the derived profile with the appropriate census-batch treatment. Alternatively, explicitly propose a different accepted rule that allows retaining an existing larger cap after a census proves its margin, distinguish census-validated reused policy from exact census-derived caps, and update the landing/control/gate text consistently. Do not silently treat a successful margin check as an exact derivation.

**Validation:** Specify controls for derived coordinates equal to, below and above the interim, including mixed-coordinate cases. The selected constructor/caps and recorded source must follow the accepted rule exactly; no constructor change may be claimed only in the equality case unless an explicit alternative retention policy is selected.

### SD9-R1-RF-2 — Describe the numerical model as a partial edge boundary rather than full R10a feasibility (P2)

**Location:** `docs/implementation/m3/supervisor-d/sd-9/README.md:94-106`.

The checker omits D4-1, D4-2 and all of M, and computes no byte coordinate. Its object counts exclude even the retained-slice allocations that the record itself says M needs. Nevertheless section 4 calls its values the largest sizes whose R10a edges fit, states that one R10a can verify 0.75 to 1.0 GB across the admitted set, and asserts that the object and byte coordinates stay within their caps. These full-admission claims do not follow from the reported subtotal. At each reported edge boundary the modeled subtotal already consumes all 2^24 edges, leaving no room for the omitted, nonzero D4 work. Per-component fixed costs also mean a one-component illustrative size is not a generally established capacity for arbitrary selectable sets. A reproducible subtotal is not a complete A(Sigma) bound.

**Required change:** Keep M owed to its owner; do not invent its price to close this review. Label the figures and output as edge-only boundaries of the explicitly named subtotal and the object figures as partial counts. Remove or qualify the full-admission, all-coordinate and arbitrary-aggregate feasibility claims. Explicitly require the priced M representation and the finalized accepted CI/D4 bounds before a complete A(Sigma) census or production fit claim; keep that completion gate distinct from acceptance of the interim policy. Extend wiring controls to exhaustion in D4-2 and M as well as the currently listed terms. Do not equate a conservative owner bound with an exact executed charge total where the owner charges actual comparisons.

**Validation:** Show that the reported subtotal is reproduced without calling it complete R10a capacity. A full-bound control must include all terms, including nonzero D4 and priced M, before asserting fit in all three coordinates. Demonstrate that a subtotal at the edge cap does not itself establish full admission, and retain multi-component aggregate exhaustion with no partial admitted set.

## Ledger, aggregate and scope

One R10a ledger constructed once after the trust-read handoff, while the fence remains held, is consistent with D4's and C2a's ownership. ER10a's counterpart belongs under its read-session fence. Helpers borrow scopes of that same ledger; no fresh ledger after failure and no per-component reset is permitted. The trust read retains its separate existing budget, and immutable authenticated evidence is not copied or charged again merely because it is handed over.

The aggregate's owner partition is useful: D4 admission and projection; C2a candidate construction; CI's whole-tree open; verified transfers into the kernel's retained-byte representation; kernel verification; and that representation's M allocation/management cost. M is explicitly owed rather than assigned a made-up total. Its exact representation, including map insertion/comparison and owned key/slice handling where present, must be priced by C2a-3 before the complete aggregate is available. An assumption of one buffer allocation per file is a possible shape, not a representation-independent minimum that SD-9 can impose on any future implementation.

The existing C2a-3k signature consumes an in-memory map. Counting CI's verifying open, then verified transfer, then the kernel's block-priced hash is correct for that proposed shape. It avoids erasing either custody verification or the kernel's accepted checks. It is not a proof that this is the largest possible implementation cost: M is unknown and any alternative must be measured against its own reviewed algorithm. A streaming kernel would require an accepted interface/accounting change; it cannot silently replace the integrated map kernel on the ground that it seems cheaper.

D4-4's later launch recheck and the Run owner's later retention copies are correctly outside R10a's lifetime. Their owning caller ledgers must still fund them. Pins may outlive the admission ledger without transferring later charges back to it. No new profile for those later operations is selected here.

The excluded identity-admission internals retain only their previously accepted bounded exception. All arithmetic in owner bounds must remain checked. No partial admitted set may reach selection after any failure, including one after earlier components have verified.

## Caps and numerical evidence

The only selected interim caps are the existing snapshot_profile values: 2^21 objects, 2^24 edges and 2^33 bytes. They are sourced to the existing constructor/constants and R9. The global/discovery alternatives are also extracted from product sources. No new cap is selected; 2^25 is a rejected example, not policy. Reusing the constructor requires no work_ledger.rs edit and by itself causes no receipt-input change. This does not certify that unrelated later changes leave receipt bindings fresh.

The table's snapshot subtotal edge boundaries reproduce exactly: 1,069,536,384; 1,064,704,785; 1,010,568,235; and 796,181,735 bytes for its four illustrative shapes. The reported kernel shares are 99.61%, 99.19%, 94.50% and 75.62%. They are shares of the modeled subtotal, not independently established shares of complete A(Sigma). The corresponding partial object counts are 19, 6,319, 93,119 and 612,019. The checker does not compute the byte coordinate. RF-2 preserves these illustrations while correcting the claims made from them.

Explicit interim reuse on X-CI-1's precedent is reasonable policy, without treating snapshot census coverage as R10a coverage. X-SD9-1 appropriately requires a complete sourced policy before first-party release qualification or production R10a composition, whichever comes first. C2a-3's missing price and the unaccepted CI-A2 additions remain completion dependencies. Adding proposed rows because they add work does not prove conservatism against an arbitrary future accepted interface change; revalidate the aggregate against the final accepted CI bounds before the census/composition claim.

## Explicit rulings

**Q-SD9-1 — form: accepted.** A reviewed law record, with root assent and explicit incorporation by J1 and M3-D, is the appropriate form for ledger ownership, profile policy and an existing projection row. No contract passage or schema needs amendment for that choice, and no lock binding is implied. The next-revision cross-law records remain owed; the draft unit is not evidence of assent or completed incorporation.

**Q-SD9-2 — interim: accepted in principle, subject to RF-2's claim correction.** snapshot_profile is an explicit existing finite allowance, not an inferred cap or evidence of production coverage. It can fund development/wiring under the stated interim standing. Production use remains gated by X-SD9-1 and completion of all aggregate prices. The illustrative size range alone cannot establish the full production boundary.

**Q-SD9-3 — census: population/aggregate/batch approach accepted; confirmation rule requires RF-1.** Census every relevant first-party release for every platform over the largest simultaneously admissible/selectable set; count common D4 work once and component terms across the entire set. Use complete published owner bounds, including M, and signed/admitted metadata rather than a held-out workspace corpus. Combining with the X-CI-1 installation census is reasonable while retaining each distinct quantity/profile. A constructor change must follow the reviewed receipt-specific census batch and blind-refresh process. Under the exact minimum-power rule, only coordinate-wise equality can confirm the existing caps without changing that rule. A merely smaller derived value proves margin, not equality of derivation. An explicit alternate retention policy is possible, but must be stated and reviewed as such.

**Q-SD9-4 — ephemeral projection: accepted.** Exhaustion before ER10a returns and before the ephemeral attempt starts is the existing operational row 11, SYSTEM.OUTCOME.ILLEGAL_STATE/host-invariant with registered WORK.BUDGET_EXHAUSTED, no runId or analysis-attempt executionId. RTC 7.4 forbids committed-Run analysis details on ephemeral attempt terminations; it does not remove this earlier owner-projected operational failure detail. Preserve every owner's typed Budget until J2 projection; never turn it into not-installed, corruption, missing bytes or an excluded form. Controls must inspect the actual pre-attempt failure envelope and its carrier, rather than feed it through the committed-analysis detail composer.

**Q-SD9-5 — hashing: accepted for the named provisional shape, subject to RF-2.** Count the open verification, transfers and kernel rehash separately. K's block price dominates the listed shapes' edge subtotals; the 40,000-file shape is about 76%, so “about 99%” is not a universal result. C2a-3 owns the eventual transfer/map shape and its prices. No redundant-check removal or custody/admission shortcut follows from this record.

**Q-SD9-6 — scope: accepted.** The launch recheck and Run retention transfers occur later, on their owners' ledgers. They remain required charged work and do not disappear because R10a already verified the tree. The operation must keep the necessary pinned capabilities alive for later reads and spawn/settlement while their original ledger may have ended.

## No pre-bound, controls and remaining gates

Choosing per-operation charging and row-11 failure without an install-budget preflight is coherent: R10a installs nothing and its failed work is read-only/pin-only. Keep successful-substep capabilities private until admission completes and drop them on failure; a fresh scope cannot retry a failed ledger. The explanation should be understood as the selected policy, not a general claim that every possible metadata-derived work preflight necessarily requires a new request-rejection route.

SD9-T1, T3 and T5 capture the right one-ledger, typed-route and no-trust-view properties. Extend exhaustion coverage to the omitted D4-2/M terms when they exist. T2 should distinguish exact executed charges from conservative owner bounds: C2a's merge sort charges comparisons actually made, which may be below its published worst-case bound. T4 cannot use the incomplete illustrative boundary to assert admission; it needs complete priced owner functions. T6 must select the final caps consistently with RF-1 and preserve typed refusal beyond the accepted margin.

J-C10b's reservation property must hold on durable 3a, all first-use 3b outcomes and ER10a: no analysis reservation at return, creation-prelude standing retained when applicable, no draw/handoff/capture/spawn/source disclosure on refusal. No public code or new matrix row is required for the stated Budget route. J1's and M3-D's record updates and C2a-3's completed representation/prices remain explicit dependencies. SD-9 acceptance would resolve policy selection, not discharge those implementation or production gates by itself.

Only REVIEW.md and review.json were written in this request directory. Neither repository, worktree nor control file was edited. No Cargo, rustc, build or lane was run, and the lane lock was not taken. No network, prohibited fixture/key/installation material, held trees or entries, T2 store/overlay/cache, other pane or delegation was used. The two permitted read-only checks were the only project scripts executed.

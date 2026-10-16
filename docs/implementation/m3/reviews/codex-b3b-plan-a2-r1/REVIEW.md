# B3-b plan amendment A2 review

Verdict: **REQUIRED-FINDINGS**.

Subject: `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A2.md`, 6,749 bytes, SHA-256 `68efabebe8dc02ec42003ed7ed69e868145f777514819c82786ab45bbe43dfd8`. Size and hash verified. Architecture HEAD matches `1f3f2b1ea4d019a1f24980f05cb2d2ef2501d766`; clean product main matches `03876532b54d8327db96091fababb1fd994a83d2`. The amendment is uncommitted as stated.

## Required findings

**B3BA2-R1-RF-1 (P2): The frozen checker-case set misses known TOML parser resource differences.**

A2 lines 38–40 prescribe B3-b0's existing D15 cases, state that no case is invented, and compare final outcomes. That is a useful baseline but insufficient for the stated parser substitution.

The product's `crates/identity/src/toml.rs` has explicit recursion and one-million-node limits. Its existing tests document a 128-deep array returning RecursionLimit and a sub-4-MiB array returning NodeLimit. The reference calls Python tomllib.loads without those product limits. These are differences in the admitted execution profile, even where the TOML syntax/calendar profile agrees. The D15 checker cases contain syntax/shape failures but no corresponding parser resource-limit controls.

For example, an unrelated deeply nested value in an otherwise usable Cargo carrier or provider manifest can exhaust the product parser before exposing the patch or package fields. The reference has no matching fixed limit. The resulting reader/link disposition therefore needs an explicit compatibility ruling rather than an assumption that existing output vectors prove the parsers interchangeable. This finding is based on source and the existing parser-test definitions; no parser/test execution was performed during this review.

Required: retain every bound D15 case, permit targeted additional parser differential controls, and state how product resource failures are represented relative to the reference and existing carrier/provider dispositions. Cover failures in unrelated document fields as well as selected fields. Do not silently narrow the contract or invent a public refusal code. For exact JSON, preserve the shared 4-MiB/32-container profile, integer limits, duplicate-key, float/negative-zero and Unicode behavior; the product canonical parser is the appropriate implementation, but that is more precise than a generic JSON-parser equivalence claim.

**B3BA2-R1-RF-2 (P2): The vector projection drops forbidden-access assertions.**

A2 lines 39–41 enumerate final member sets, refusals, declaration rows and links. B3-b0's checker verifies more than those outputs: check_case installs SpyContents and OBSERVED, then checks notRead and notObserved assertions. Those controls were introduced to close the literal-anchor and hidden-glob metadata findings.

A WorkspaceObservation implementation can serve a forbidden metadata lookup or manifest read, whose result the decision core discards, while all proposed output comparisons still pass. B3-b2a's existing walker vectors cannot catch a new reader/placement core accessing its observation interface incorrectly. Keeping the same synthetic trees without keeping their access assertions weakens the accepted reference coverage.

Required: preserve the checker cases' forbidden metadata/content-access assertions in the pure-core vector adapter and controls. Cover member SX-1 and other pruned anchors, hidden glob repositories, and crossings proved by visible enclosing repositories without consulting their interiors. Add a mutation that makes a forbidden access while preserving the final output, and require it to fail. This need not freeze all internal query ordering or require identical traces; the safety-relevant negative assertions must survive extraction.

## Split, observation interface and order

The proposed split otherwise preserves A1's remaining section-3 obligations. B3-b2b1 owns reader parsing, dispositions, placement and membership decisions; B3-b2b2 owns charged native observation, actual 6b, the operation handoff, complete V3 composition, scenario use, both T2 link-map controls and the joint sweep. Item 24 remains applicable to both branches and root-in-repository. The existing link-stage supplied-member seam is explicitly retained as a test seam, with no production placement bypass.

WorkspaceObservation's metadata, bytes, marker kinds, child listings and supplied 6b results are the right families of observations. The implementation must retain enough custody data and invocation context for the existing pure checks, rather than reducing a full ACL/grant judgment to a boolean or omitting trusted-group/waiver facts. It must also distinguish absence, refused evidence and host/budget failure where the native composition requires it. The plan need not specify a complete Rust trait signature at this stage.

The branch-A trial-walk boundary is faithful to the reference's SLM-first correction: provisional members precede the trial, and placement/cap/6b terminal decisions cannot override an earlier trial refusal. Branch B must finalize members only after placement, the cap and supplied/actual 6b verdicts; links follow final membership. The phase-one wording calling branch B's result final is read in that sense, not as permission to admit candidates before 6b. B3-b2b2 still owns the integrated behavior and no-member refusal provenance. Reusing existing cases is appropriate; making them the exclusive coverage and projecting away access assertions is what requires correction.

## Retained identity across the handoff

The recommended identity can satisfy the retained-root requirement. The built operation subject moves the admission/RegisteredProject chain and TrackingObservation together, while observe_tracking_on_gate produces and rechecks tracking under the gate. An immutable, privately minted, process-unique and never-reused identity on each ProjectChain can survive those moves and let the proof constructor compare the observation with the exact retained chain, then return a proof borrowing that chain.

Implementation must ensure identities are not pathname/descriptor-number/address substitutes, cannot be assigned by callers, do not wrap or reset into reuse, and are preserved by moves. A separately retained chain receives a different identity even at the same spelling. Tests must keep the prior different-spelling and replacement-root substitution controls and check rechecking/moving the same chain. ProjectChain being non-Clone supports this construction. Recording the identity in TrackingObservation must preserve existing 6a native steps, charges, refusals and recheck semantics apart from the intentional subject binding.

Rejecting a fresh unfenced 6a pass as the source of this proof is appropriate: the handoff already carries the fenced observation, and a new observation is a different authority for the precondition. No extra Git pass is needed to bind the existing evidence to its retained object.

## Census and remaining gates

Changing project_chain.rs requires A1-2's exact closure re-pin and equality projection in B3-b2b2. The held-out margin remains outstanding until the accepted B3-b3a tool, single blind run and post-run review in B3-b3b; workspace full-ledger margins and the failure-to-law rule remain B3-b3c obligations. The native reader and placement work belongs in the later complete bound and its actual-versus-predicted/under-count controls. Nothing in A2 authorizes held-out access during either implementation step.

**B3BA2-R1-NBO-1:** A2 assigns native reader observation to the member term while section 4.2 retains a separate reader term payable at n=0. Keep those terms disjoint when deriving B3-b3a, assigning each charge once and preserving the n=0 reader cost. This carries the earlier plan's cost-accounting clarification rather than changing the gates.

Review used only read-only reading, hashing and Git queries, followed by writing these review outputs. No Cargo, rustc, tests, builds, lane or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry was read. No panes or delegation were used. Neither repository nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.

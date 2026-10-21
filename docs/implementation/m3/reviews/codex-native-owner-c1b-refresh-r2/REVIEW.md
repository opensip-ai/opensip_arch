# NATIVE-OWNER-C1B-REFRESH-r1 pre-run gate review — round 2

Verdict: **ACCEPT**. `runAuthorized: true` for the single run exactly described by `RUN-PLAN.md`, only after this exact gate is committed as an `ACCEPTED-UNIT` with substantive root assent and this review pinned. Preparation itself ran no blind mode and granted no qualification. No required findings or non-blocking observations.

Subject manifest SHA-256: `acf667fa445a3b4125587dbe3b7d5453bb013fa51b34c8045c87df6cc96367ea`.

## Correction and reproduction

**OWNPAT-CBR-R1-RF-1 is closed.** The 4,173-byte manifest and all 17 members match their recorded lengths and SHA-256 values. Relative to rejected round 1, the wrapper, postchecker, freeze, bindings, joined units, plans, source record and all runtime/input bytes are identical. Round 2 adds `CONTROL-REPAIR.md`, the pure checker, two complete vector files and its execution log, and replaces the result-only control summary with detailed expected and observed results.

The checker pins wrapper SHA-256 `6b71bdb38e4f372010e2136b7243e07bb04e537fa37f5f59933d0ab04a993eaf`, finds exactly one `receipt_ready` function, one blind loop, one ordinary loop and one eligibility assignment, and compiles only those AST nodes. Independent AST and file hashing reproduced all archived provenance:

- predicate AST: `77411a23bba8e5e1b93f38b154c00f48c200c3073eeba70f821f11a713d5afc1`;
- blind/ordinary/eligibility AST: `8c9a9b0493a3654388fddcb89d301ba5937e8a15a8385ee9e5f3f4259e1c6a61`;
- predicate vectors: `728dfc20fff4dd87f8cf81c604fc5a01fe2c1bad40d2a63241231f118244ddbd`;
- sequence vectors: `21d8b056a36e269e5de974cd01d956f92b0acbe83b14472a86cef473ee74e97c`;
- checker source: `a5fc51c37b248ec91a6fd5790659f5924ba2c3a6297ec3934891775402779cba`.

Using only the expressly permitted pinned-Python invocation, I wrote `receipt-decision-controls-reproduced.json` in this review directory. Its 12,909 bytes and SHA-256 `3780f5d6b6a6c5a69ca0878cdc43c7b059badf05719cbce33b191799375a8e24` are byte-identical to the frozen detailed result. All 15 receipt-predicate cases and all 15 actual-branch sequence cases pass; the recorded synthetic invocation order and stop points are exact; real blind invocations are zero. The controls cover the original nine cases plus integrity, population, standing, empty rows, state, failure-state handling, every ordinary stop point, the four-file gate, delta gate and discovery-equality eligibility gate.

## Exact inputs and accepted batch

- Product main is clean and exact at `66eed0289f40bfc24e3991d9788c3d94c31daab1`; architecture HEAD is the recorded `4420b4cc3db28648b77ed235ab446a69736f5af4`. Unrelated untracked architecture material is outside this frozen subject.
- Every live authority, accepted receipt-specific record, native inventory-v234 and description-182 subject pin, and the pinned Python 3.14.6 interpreter rehashes. The C1b plan, four C1b/C1c units, native materialization r2, inventory v234 with its binding carry, and description contract 182 retain their recorded acceptance and substantive assent.
- The five joined product commits are recorded in current state, are ancestors of exact main, and occur in the declared order: C1b-0, C1c-0, C1b-1, C1b-2, then native materialization.
- Both committed receipts remain byte-identical to the accepted `0772eb7f383cdbff1c3d0869486094a95ef7693a` refresh and retain `holds (blind census)` only as historical baseline evidence.
- The permitted public `freeze_c1b_refresh.py --bindings` recomputation equals both frozen bindings exactly. The discovery delta is the accepted two closure paths, generator-closure reference and tool pin. The companion delta is that nested discovery delta plus the accepted eight snapshot-source paths, three tool paths and `afterWalk`. Each equals the exact union of the five accepted joined-unit deltas.
- The generator closure differs from the historical baseline in exactly six rows: `schemas/source-map.json`, `schemas/sources/identity-v3.schema.json`, `schemas/sources/native-v2.schema.json`, `tools/contracts/options.json`, `tools/contracts/runtime/patterns.ts`, and `tools/contracts/runtime/schema.ts`. Python-package rows and all other top-level closure data are unchanged.

## Rulings

**Exact main: accepted.** Before any private access, the wrapper requires the committed gate's accepted status, substantive root assent, independently accepted review with authorization and no findings, exact manifest/self bytes, pinned interpreter, frozen record/helper/postchecker hashes, clean exact product main, a clean detached same-repository worktree at that HEAD, and exact recomputed public bindings. It holds the lane at nice 10 and uses a private 0700 temporary directory with the prescribed restricted environment.

**Combined batch: accepted.** The reviewed discovery and companion blind access, method, population and disclosure paths are unchanged. Discovery's tool movement is its accepted closure-pin change. The companion's model and recipe movements are exactly the accepted read-set, VCS and sealing terms. No unaccepted input is hidden in the current binding delta.

**Fallback: accepted.** C2b-0 and C1c-1 were unaccepted drafts when this exact-main package became ready. Excluding them satisfies native materialization's immediate post-metadata obligation while preserving C1b PLAN-r6 LD-C1B-7's one combined discovery/companion refresh. Later acceptance or integration of either draft opens a new interval and is outside this authorization.

**Expected row outcomes: accepted.** The actual loop invokes discovery once and reaches companion once only after exit zero, empty stderr, a written receipt, exact standing/bindings/IDs, measured-only discovery rows, true integrity/population, `holds`, and rows byte-equal by value to the historical receipt. Companion accepts only exact standing/bindings/IDs with true integrity/population and measured or over-item-5 rows; `holds` or `fails` preserves the reviewed under-2x return-to-law outcome as data. Any blind failure stops the sequence; any discovery receipt failure stops before companion. Ordinary discovery write/check, workspace check and companion write/check start only after both receipts pass and stop on the first nonzero result.

The run record is always written. `eligibleForPostRunReview` requires both blind and ordinary phases, exactly the two receipts and two census files changed, unchanged discovery rows, and exact IDs, frozen bindings and expected binding deltas for both receipts. The postchecker requires that explicit eligibility record and matching freeze, then independently requires detached exact main, clean main, recomputed bindings, all tool and architecture pins, and exactly those four changed files before the required census, blind-control and design checks. Neither script commits. Any error, unexpected difference or failed postcheck commits nothing; there is no tuning, peeking or retry. Independent post-run review and substantive root assent remain mandatory before any four-file product commit.

No build, Cargo command, lane, network operation, wrapper import, blind mode, post-run checker, private fixture, held-out store, cache, overlay, key, installation or other worktree was accessed. Only the permitted public binding recomputation and pure synthetic checker were executed. This review grants no product or project qualification.

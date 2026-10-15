# B2B4-PLAN-r6 review

Verdict: **ACCEPT**

Required findings: none. Non-blocking observations: none.

Independently verified subject.json: 658 bytes, SHA-256 `718a0e7103e52412d8b7a65f6b1839652f7d34122fd91e8fd810875ac5620212`. Both members match their pins:

- PLAN-r6.md: 35,483 bytes, SHA-256 `2b6dfd4d7263fdbcba974ada3af79c0f110d9cfbcf0fab4f33123959c5355565`.
- HELD-OUT-T2-MARGIN.md: 1,589 bytes, SHA-256 `375bbc6bbeccb9d1142f748c3416fe239516e385ca1b93fd73f2696ca6fe62d0`.

Product main is clean at `d33df45ac0a5422efbebb43eee9c652d17ee742a`; architecture matches `de2388edc19dec8c7ed2bffd0ceef2314d86cddc`. Compared the complete r5→r6 delta and the inherited sections against accepted r4, and checked the proposed lifecycle against the current generator, reference-loading path, margin test and owning law/plan requirements. This is plan acceptance, not implementation or run acceptance.

## Prior findings resolved

**B2B4PLAN-R5-RF-1 resolved.** The blind run writes a separate receipt. Its bindings cover the manifest, census tool bytes, whole cost closure, sizes, code caps and root lengths. Ordinary generation validates format, coverage and current bindings before composing results, without opening held-out stores. A current valid receipt survives ordinary --check and --write; drift produces stale outstanding rows and requires a new reviewed blind run. Invalid receipts refuse. Permitted top-level changes are limited to heldOutMargin, failingEntries and caps, with lead-readable/workspace evidence retained. Lifecycle controls cover regeneration, drift in each binding and spying on ordinary filesystem access. This addresses the current generator's unconditional outstanding rows and whole-file comparison without weakening ordinary held-out refusal.

**B2B4PLAN-R5-RF-2 resolved.** Measured rows have the exact declared fields, successful integrity/population checks, all three margins and a consistent passes2x value. Error rows contain only ID, error status and an allowed class, with no invented margins. Receipt IDs must equal the expected held-out IDs exactly. The defined states distinguish holds, measured margin failure, incomplete measurement and outstanding receipt; only holds closes the repository margin gate. Synthetic controls cover all four error classes, missing/duplicate/unknown IDs, forbidden or missing margin fields, inconsistent classification and output canaries. Failure returns the caps to the law; errors keep the gate open and require another reviewed run. No cap is raised by hand.

**B2B4PLAN-R5-NBO-1 addressed.** The chosen option is now quoted in full, including its opening authorization. Request base descriptions now agree with inventory v198 and shared r98.

## Owner choice and non-disclosure

The supplied owner record is byte-identical to the prior subject and explicitly records selection of option 1. The plan's quoted option now matches that record exactly. This assessment uses the user-supplied owner record as authority; the originating AskUserQuestion transcript is not separately included. No additional choice or assent is inferred. The selected mechanical run, review before opening stores, and review of the receipt and composed record afterwards are all retained. Neither review opens held-out stores, and the lead does not inspect contents.

The planned result contains only manifest IDs already known to the lead, pass/fail information, integer per-mille margins or an error class. Receipt bindings disclose public reviewed metadata, not held-out content. The one-line summary counts outcomes, not tree objects. Raw paths, names, object counts, sizes, exception messages and additional content-bearing values are excluded. Canary and closed-format allow-list checks cover receipt, stdout and stderr. Errors are mapped to INTEGRITY, POPULATION, MODEL or IO without retaining their messages. These are concrete implementation obligations for B2-b4c1, not a claim that unimplemented code has already demonstrated non-disclosure.

The separate mode-guarded digest join preserves the ordinary store_path refusal. The blind mode retains the lead-readable census's no-follow integrity verification, reference population comparison, cost model and actual code caps. The existing reference-loading path checks its accepted reference pins. The manifest contains ten held-out repositories and no held-out workspace; workspace rows remain unaffected and their full-ledger margin remains outstanding until B3-b's reviewed bound. Successful blind repository results grant no workspace or qualification claim.

## Classification and retained scope

For positive modeled cost c and cap L, floor(1000 L / c) >= 2000 exactly when L >= 2c. Thus requiring every measured per-mille margin to be at least 2,000 is equivalent to fitting twice in objects, edges and bytes at R=4,096. The format/coverage/binding checks are separate prerequisites, so that arithmetic alone cannot turn an error or incomplete receipt into success.

Measured insufficient margins return the caps to item 12. Incomplete/error, stale, absent or invalid results cannot complete B2-b. The before/after review sequence remains explicit; no weaker lead-readable-only gate or different runner is selected.

Sections 1 through 2.4 match accepted r4 byte for byte, apart from whitespace adjoining the added section. Existing lead decisions remain intact. The new receipt lifecycle and controls refine section 2.5 without reopening earlier accepted code, changing law or selecting new caps. No implementation, binding or qualification is claimed by this plan review.

## Boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, tests, builds, lane or network was run. No other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or held-out store/overlay was accessed. Optional cache counting was unnecessary. Neither repository, the stage nor control files was edited. Only REVIEW.md and review.json in the requested directory were written.

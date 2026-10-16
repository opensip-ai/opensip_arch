# B2-B4C1-r2 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none.

Independently verified the subject manifest: 11,813 bytes, SHA-256 `8fa38c44ac88720e0651faf76d884cc65512d820f49c3ec9bcc1872c69e358c1`. All 52 members match their pins. The three product-map rows match candidate worktree and archived bytes; parent pins match product base `d33df45ac0a5422efbebb43eee9c652d17ee742a`. Exactly the two mapped existing paths and the new synthetic blind-test path are changed. Main is clean at that base; architecture matches `a5b3fc88f7a84bbff40819679bd76172bcb60004`. All source-authority pins and the unchanged design-lock pin match.

## Prior findings

**B2B4C1-R1-RF-1 resolved.** The Rust margin test now binds the census manifest pin and ordered entry, workspace and held-out identity lists to reviewed SHA-256 constants. Independently recomputed all four constants from the manifest bytes, IDs and heldOut flags; each matches. The held-out-status identity digest and explicit workspace restriction prevent substituting a lead-readable/workspace row for a held-out measurement. Existing state-count checks then apply to the exact expected held-out identities. Four new census-record negatives reject duplicate IDs, a foreign ID, a lead-readable status substitution and an omitted lead-readable row; their logs fail at the new identity assertions.

**B2B4C1-R1-RF-2 resolved.** Argument abbreviations are disabled. After parsing, main selects the blind branch from the parsed arguments and encloses the complete run in an except BaseException boundary. SystemExit, KeyboardInterrupt and other failures emit only the fixed generic line and exit 1 without exception chaining. Parser help/usage exits precede store access and do not inspect content. Per-entry verification, measurement and margin handling also reduce SystemExit to the appropriate class. The new canaries cover message-bearing SystemExit, interrupts, ordinary exceptions and abbreviated options; the corresponding guard mutations are caught. The ordinary error-output path remains separate.

**B2B4C1-R1-RF-3 resolved.** Receipt bindings now include the imported discovery_walk_vectors helper, the generator-closure configuration selecting pinned Python packages, the bound reference, its SLM and rule, and the foundation canonicalizer. The reference-loading path checks that the selected reference/SLM/rule and canonicalizer origin match the declared binding paths. Package bytes remain verified through the generator closure. Synthetic drift controls alter each of the six newly bound reference inputs and make the old receipt stale; the reference-unbound mutation is caught. The population/model inputs relevant to the saved result are consequently bound or checked before reuse.

## Whole-unit assessment

The blind mode retains the ordinary census's integrity verifier, reference population check, cost model and code caps. The separate join requires the private mode token and a held-out entry; ordinary store_path still rejects held-outs. Ordinary generation composes receipt rows without joining or opening held-out stores. The synthetic filesystem spy exercises that separation.

The receipt generator writes only the declared receipt and one line of outcome counts. Its row output is restricted to known manifest IDs, verification/classification information and per-mille margins, or an allowed error class. It stores no held-out paths, names, raw counts, sizes or exception messages. Public source/input pins add no held-out content. The redaction boundary covers failures after parsing and before or during blind execution. No real blind run occurred in this review.

Python validation enforces closed measured/error row formats, nonnegative integer margins excluding booleans, true integrity/population on measured rows, exact passes2x consistency, unique IDs and a derived state. A current receipt must cover exactly the manifest's held-out IDs. An invalid receipt refuses; binding drift leaves stale outstanding rows. Ordinary --check/--write deterministically preserve a valid current result. Comparing coverage only after the manifest binding matches is a sound reading of the plan: a changed manifest invalidates the old claim without opening a store.

The Rust test independently classifies composed measured rows by the 2,000 threshold, checks their closed result shapes, verifies exact reviewed identities, and derives outstanding/incomplete/fails/holds state. For positive cost c, floor(1000 L/c) >= 2000 is equivalent to L >= 2c. Only all expected successful passing measurements meet the repository held-out gate. Known measured failures enter failingEntries and return caps to the law, including alongside error rows; errors keep the held-out state incomplete. The r7 full claim for lead-readable repositories remains enforced. Workspace full-ledger margins remain outstanding.

The cost model, walker and production admission behavior are unchanged. Both generated census records remain byte-identical to base because no real receipt exists. No law change, environment read, production caller, qualification or B2-b completion is claimed. Inventory v199 follows the code commit for the new synthetic-test path and the recorded description corrections; the real receipt and blind run remain B2-b4c2 work after the prescribed integration steps.

## Verification

Independently executed only the expressly permitted candidate checks:

- Operability source census: 114 rows, passed with no findings.
- Existing census controls: 18 tests passed.
- Blind census controls: 19 tests passed, using temporary synthetic stores and receipts only.
- Ordinary census --check over lead-readable stores/overlays: both generated records verified, with no real receipt present.

Rechecked the mapped candidate hashes after these checks; all remain exact. The actual receipt path remains absent.

Assessed supplied Rust/lane evidence without executing Rust or the lane. All 17 recorded check rows pass. Security preserves the same 14 baseline failures and 1,128 passes at base and candidate; this is matching failure sets, not a whole-suite pass. The recorded host/security all-targets Clippy command denies warnings and completes successfully. The edited Rust test file is base-clean and candidate-clean under the recorded formatting checks.

All 26 supplied control results match their logs: 11 guard mutations and 15 Rust census-record controls, comprising four valid records accepted and eleven invalid records rejected. The new negative cases exercise the prior coverage, redaction and reference-binding gaps. No control result was credited for a Rust compilation failure. The Python coverage-unchecked mutation is caught as an unexpected unittest error, which is still a nonzero test outcome.

## Boundaries

No Cargo, rustc, Rust tests, builds, lane or network was run. No other panes or delegation were used. No T2 held-out store or overlay was opened; --held-out-blind was never run against the T2 cache. No private fixture, installation directory, signing keys or held trees were accessed. No real receipt was written. Neither repository, the candidate worktree, the stage nor control files was edited. Only REVIEW.md and review.json in the requested directory were written. This is the owner's before-run code review; the real run and after-run review remain separate steps.

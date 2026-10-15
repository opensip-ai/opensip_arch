# B2-B4B3-r1 review

Verdict: **ACCEPT-UNIT**

Required findings: none. Non-blocking observations: none.

Independently verified the subject manifest: 8,583 bytes, SHA-256 `4cabcf584ed3664669556ed6864ccfbcaa407f4ba0edc130c2080109df77de0d`. Rehashed all 38 members. All seven product-map rows match the candidate worktree, staged archive and committed parent pins. The candidate changes exactly those seven existing paths and adds none. Product main is clean at `79c816096310711663104a5e9217717718f8f510`; architecture matches `8d2f4557cd8d28526b3564057fd68d045eded531`. All seven source-authority pins match committed architecture bytes; the candidate design lock matches its unchanged pin.

## Caps and margin claim

The only production Rust behavior change is `DISCOVERY_OBJECT_LIMIT`, from 2^20 to 2^22. The 2^21 edge and 2^30 byte caps and global caps remain unchanged. This exactly implements law r7 item 12 and B2-b4 plan r4 section 2.3. The two B2-b1 controls now use the recorded object cap. They retain exact-cap admission, one-beyond refusal, failure latching and the restriction that ordinary with_limits cannot raise global caps.

The census generator now includes bytes in passes2x at ROOT_LENGTHS[-1], which is 4,096 in the fixed `(134, 1024, 4096)` sequence. The native margin test independently takes the largest recorded root length and evaluates twice each row's objects, edges and affine byte cost against a fresh discovery ledger's own limits. It verifies each passes2x flag, byte values and byte classifications at every recorded root length, exact agreement with failingEntries, an empty failure set and recorded-margin-holds. The final boundary assertions establish that the record's limit values equal the code profile's actual limits.

Independently parsed the regenerated census: all 39 lead-readable repository rows and five walker-only workspace rows satisfy the three-dimensional numerical margin. The maximal values remain 1,476,438 objects, 1,007,224 edges and 358,480,897 bytes at R=4,096; twice each fits the recorded caps. Counts, costs and byte formulas are unchanged from the bound census. Changes to the record are the refreshed closure, object limit and derived margins/classifications, empty failingEntries, caps/capsRecordedBy and the explicit workspace limitation. Census vector values are unchanged apart from the closure pin. All whole-file closure pins match candidate bytes.

Every lead-readable workspace row explicitly records fullLedgerMargin as outstanding until B3-b's reviewed member-observation bound; its passes2x covers walker costs only. All ten held-out rows retain their exact outstanding status, and heldOutMargin stays outstanding. Those limitations are asserted by the test and stated in SCOPE. The recorded-margin-holds label therefore does not establish a workspace full-ledger or all-entry margin. B2-b remains incomplete.

The two stale inventory descriptions are accurately identified in SCOPE and expressly deferred to the next reviewed inventory successor using description corrections rather than an additive-only claim. No path or package ownership changes in this unit, so leaving inventory v198 unchanged is sound within this declared follow-up. The current lock still has 158 inventory successors and 164 contract successors. No inventory binding, law change, production caller, environment read or qualification is introduced.

## Verification

Independently executed only the expressly permitted candidate checks:

- Operability source census: 114 rows, no findings.
- Census controls: 18 tests passed.
- Walker storage structural checks: 5 tests passed.
- Full permitted census --check: both generated records verified, without opening held-out stores or overlays.

Candidate product-map hashes remain exact after those checks.

Assessed supplied Rust/lane evidence without executing Rust or the lane. All 17 current check rows pass. Security preserves the identical 14 baseline failures with 1,128 passes at both base and candidate. The platform suite records 295 passes, zero failures and seven result summaries at both base and candidate; its runner explicitly uses one test thread for both. SCOPE discloses the superseded parallel platform races and stale Python constant expectation from the earlier lane, and the current evidence covers their corrections. Matching security failure sets are not represented as a whole-suite pass.

The recorded all-targets Clippy command covers host, security and platform with warnings denied, and its log completes successfully. All three edited Rust files are base-clean and candidate-clean under rustfmt. The focused census suite passes six tests; all 56 supplied native soundness comparisons bound objects, edges and bytes, with 46 exact. Each of the six mutation logs contains precisely its listed runtime test failures and no compilation error. Reverting the cap makes the full-claim margin test fail; each of the five model mutations regenerates predictions and is caught by the native soundness controls.

## Boundaries

No Cargo, rustc, Rust tests, builds, lane or network was run. No other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or held-out store/overlay was accessed. Neither repository, the candidate worktree, the stage nor control files was edited. Only `REVIEW.md` and `review.json` in the requested directory were written. Lead assent, publication and the product code commit remain subsequent actions; nothing was pushed.

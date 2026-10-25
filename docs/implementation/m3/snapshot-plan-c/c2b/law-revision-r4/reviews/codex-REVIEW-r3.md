VERDICT: REQUIRED-CHANGES

Independent review of C2b snapshot edge-cap law-revision PLAN.md r3, 2026-10-25. The owner's census-validated revision decision is the review premise. None of the findings requests restoration of the open-ended LR-2 source/ABI programme.

Route: ROUTE-OK R3-FRONTIER codex gpt-6-astra/high against REQUEST-r3.md; counterpart and plan author Claude claude-opus-5-5/high. Product main e39cee850864df377d0a4d54287348b752257874; architecture HEAD c646734a594ee81d444720d5459f6aedc4371b7a. The live accepted plan remains the pinned r1 plan until a successor is accepted.

Required changes

R3-1 — Remove the circular M0 pass requirement without weakening the mandatory positive.
Locations: PLAN.md:70-81, 166-177.

M0 requires SP-1 to pass its own tests before measurement. The unchanged mandatory 4 MiB layout positive is one of those tests and still uses WorkLedger::new() (SP-1 node_modules_layout_tests.rs:1025-1027). Its current admission precharge cannot fit that profile: even the fixed plus 128-edge-per-row part alone is 64 + 128 * 21,026 = 2,691,392 edges, above the generic 131,072-edge cap, before the other admission work. checked_admission charges before evaluation. The retained necessary-condition review gives the fuller 28,806,258-edge admission figure and also establishes incompatibility with the old snapshot edge cap.

M5 reserves the production profile/test correction until after accepted cap law; M4 depends on M3 measurement; M3 depends on M0 passing. Thus the plan cannot reach the step that repairs this known failure without violating an earlier gate or weakening the positive.

Required change: separate pre-cap readiness from final production acceptance. M0 should require coherent compilation/Clippy and disposition of ordinary correctness failures, freeze the complete subject and test population, and retain the exact known cap-incompatibility failure as an explicit unresolved blocker to production acceptance. Define the separately reviewed M1/M3 measurement-only positive over the same unchanged case, under the isolated measurement profile, without relabeling the original failing test as passed or ignoring it in final validation. M5 must still make the unchanged size/digest/canonical-agreement positive and early one-byte-over Encoding refusal pass under the accepted production snapshot profile, with the complete final population. No early production cap increase, reduced fixture, cheap encoder substitute or changed positive expectation is authorized by this sequencing correction.

R3-2 — Tie Tsound to the post-audit charge model, not unchanged historical terms.
Locations: PLAN.md:32-37, 55-56, 85-100, 157-164.

The new rule uses Tsound + Lmax and defines L as C2 layout alone. M1a explicitly permits new charges outside layout: walk listing sort and scans, seal descriptor parse/schema/canonicalization, inventory/VCS/carrier hashing, VCS parse work and terminal copies. Those charges therefore cannot be justified by Lmax. Yet sections 1 and 5 call T r9's already-sound terms and keep r9's other terms unchanged, while M4 contains no explicit re-derivation gate for changed non-layout prices. Current SP-1 snapshot_seal.rs:514-520 illustrates the gap: the identity-admission call is preceded by the small identifier owned_record charge; adding the proposed covering charge changes the seal term.

A measured layout maximum cannot repair an understated non-layout subtotal. Model/anchor/vector coherence deferred to M5 is too late to justify the cap selected at M4.

Required change: make M1 produce a finite, complete assignment of the selected operation's charges to bounded non-layout T, empirical layout L, and the remaining non-row/refusal-margin work. For any M1 correction affecting T, require a conservative updated bound on the existing bounded domain, with current source/model/anchor/vector correspondence, before M4 cap selection (and current instrumentation/model pins before M3). Reuse existing terms only where their prices and premises remain valid. State that their owning semantics remain, while numerical terms may need revision; do not assert unchanged numbers if the charge audit changes them. If a non-layout family is intentionally made empirical instead, explicitly amend that additional guarantee rather than silently putting it under C2's Lmax. Conservative bounded calculations suffice; no exhaustive std-ABI proof is requested.

R3-3 — Make the normative fit guarantee match the retained margin and outcome domains.
Locations: PLAN.md:46-56, 125-148.

The first guarantee says every item-5 tree with L <= Lmax fits, merely adding "with r9's margin for non-row work." r9 section 5 instead makes fit conditional on non-row work staying within the remaining margin. A tree can have a small admitted descriptor and little/no layout yet arbitrarily more excluded/pruned/link/directory work; r9 explicitly places that work in the refusal domain. The empirical layout threshold does not remove that condition.

The next guarantee says "every measured case in M2 and every lead-readable census tree fits." M2 deliberately includes one-byte-over Encoding refusals, predicate refusals and non-row stress cases that may correctly exhaust a budget. Readability also does not establish census eligibility: r9 section 4 has 44 readable entries, five proven over item 5, and only 39 measured entries. The new text must not turn those refusals/exclusions into a success promise.

Required change: state the non-row margin condition explicitly using the revised partition and proposed caps, with each charge counted once. For example, a sufficient fit condition is bounded T <= Tsound, layout L <= Lmax, and remaining non-row work within cap - (Tsound + Lmax), componentwise. Limit the fit claim to the reviewed bounded positive cases and the eligible, successfully measured lead-readable census population. Require all other matrix rows to achieve their specified typed outcome; keep authorized-but-ineligible, failed and incomplete cases visible and distinct from cap-selection maxima. State whether "fit" means staying within the ledger or completing the operation; neither may erase a required non-budget refusal. Readability and the 44-entry authorization manifest are not themselves eligibility proofs.

Disposition of prior r2 findings

- RC-1: the empirical replacement is now explicit, and componentwise no-lowering is correct. The remaining T and fit-domain problems are R3-2/R3-3, not a demand for the discarded layout proof.
- RC-2: fixture identity, generic constructor, candidate-versus-main distinction and required provenance manifest are corrected. The prerequisite sequence remains blocked as R3-1.
- RC-3: resolved at plan level. M1c preserves B2's discovery ledger, walk -> layout -> read set -> seal on one snapshot ledger, one VCS observation through seal, retained captures/spent work and reconciliation of charged totals/reservations.
- RC-4: the prescribed pre-run matrix now covers the requested dimensions, physical versus predicate cases, joint feasibility, refusal outcomes, public population reconciliation and separate blind interval. R3-3 aligns the law's guarantee with that matrix.
- RC-5: resolved at plan level by the debug-assertion gate, explicit release-feature rejection, positive harness control and required shipped-artifact feature matrix. Their actual implementation and controls still need review.
- RC-6: the finite all-path audit, terminal-copy pricing, work-counter unit correction and discovery charging boundary are adequate plan requirements. R3-2 closes their connection to the cap formula.
- RC-7: resolved at plan level: reviewed memory/disk/time/fixture limits precede execution; external stops and measurement-cap hits remain failures; representative usage and near-cap exposure are distinguished.

Other observations and limits

SP-1 is presently an uncommitted candidate on e39cee8, with 22 tracked modifications and five new files. That is consistent with requiring a future exact manifest, not evidence of acceptance. The plan's "never compiled" narrative conflates the rejected P+D composition with its newer SP-1 replacement; identify those separately when updating M0 status. At inspection, lane/sp1-r1/report.json records only the base side, and no candidate-workspace-tests.log exists. I make no fresh candidate test-pass or runtime-failure claim.

The charge audit remains historical reconnaissance at e39cee8. Its stale "64 MiB SCHEMA_BUDGET" wording and omitted selected layout coverage are not current authority; r3 correctly requires source revalidation and identifies the work-counter unit. Carry that distinction into the finite audit.

M5's express retention of r1 LR-5 preserves the 17 controls, full30/full39, exact mutations/restorations, model/anchor/vector checks, fresh procedure assent, frozen-result review and receipt-specific baseline/delta/blind-refresh duties. None is waived here. cap_rule.py supplies arithmetic only; the selected numbers and their coverage remain separately reviewable evidence.

Review was read-only source/document/Git inspection and arithmetic. No test, compiler, fixture, measurement, census, held-out access or production edit was performed. Only the requested codex-review/REVIEW.md was written. No plan/runtime assent, cap selection, unit acceptance, integration or qualification follows.

SHA-256:
- PLAN.md r3: 514d93fee248d2a14092410a92423522aa9479c7cff2eb1cbdbf581426b79c13
- REQUEST-r3.md: 87fb44c334ead2a9bede0d2ce6293ce226b0511889355afa2451f267fc710d8d
- prior REVIEW-r2.md: 5a4a9fca128c080e61e5b1f77ff1e4f9f5595279e0081b0837414a01bc46e325
- CHARGE-SITE-AUDIT.md: 061ee60afaa127b79593099ca55600d18df554e94606e712885bf6ba40e7df63
- c1a-r9/RECORD-r9.md: f360d1aa9eb5b68c5ef36d1250548b60424f4c204673c73ff10ac51906d39b29
- c2b/PLAN-r3.md: 1392af25896e55c42034e1f390833039df395f23f7e6e97f982fd2d77bfaa709
- SP-1 node_modules_layout.rs: 1f8c823c3f7182a8cc7222e8919a2c8412f029d5d3e71dc142a598006e57b076
- SP-1 node_modules_layout_tests.rs: 32588776eca37ffb95dc43f021e06e82b4b5a799f1973c1212b934959fb131a5

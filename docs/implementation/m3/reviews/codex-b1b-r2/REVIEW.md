# B1-B-r2 review

Verdict: **REQUIRED-FINDINGS**

Two required findings remain, addressing portions of round-1 RF-03 and RF-04. Round-1 RF-01, RF-02 and NBO-01 are resolved. No non-blocking observations.

Verified the 11,591-byte subject manifest, SHA-256 `967257c8b5ef365993b82af7154f295ec3f1773193d9562778c3fe82ff71522f`, and all 51 members. All 26 product-map paths match their archived and candidate worktree bytes; parent pins match the product base, and new paths are absent there. The map equals the complete changed/untracked candidate path set. Authority pins match architecture `b98932720200253f671814d9cb728ba0615c1085`. Product and candidate HEADs remain `c0151bc6b7fdb6db9157124fa068c8be5061f5d4`, and the base product is clean. The product lock is byte-identical to base, selecting inventory 188 with 162 contract successors.

## Resolved findings

**RF-01:** `judge_project_object_sampled` returns the metadata sample on which the custody predicate passed; the legacy wrapper discards that result with the same native charges. Selection retains the descriptor and judged sample. Local judgment does the same. Capture requires equality to that sample before and after its bounded charged read, so it cannot establish a fresh baseline after a rewrite or custody change. New controls interpose both changes for both carriers; the re-baselining mutation is caught in its archived log.

**RF-02:** optional capture now shares the judged private walk and settlement with required capture. Every existing prefix receives private custody, exact-name and filesystem admission before its child is observed. An absent result retains parent paths and their original full samples. Full recheck reopens and re-judges those parents, checks exact names and sample equality, and then repeats the absence observation. Detachment is no longer accepted as vacuous absence. Wrong-custody, mode-change, replacement, detachment and appearance controls are present; the parent-sample mutation is caught. Failures retain the full-recheck and latching settlement.

**NBO-01:** the classification covers all 22 mapped Rust files. The rustfmt command covers all 13 new/base-clean files; all nine base-dirty exclusions are explicitly classified and recorded. No edited Rust file is omitted from both groups.

RF-03 is substantially improved: constants resolve to the three actual authorized names, test-module braces are matched on blanked code, allowance attachment is checked, and two negative controls pass. The inclusion-reachability defect below remains. RF-04 now includes five matched base/candidate ledger states, complete resolver output under cleared/hostile environments and a separate permitted-Git-refusal assertion. The remaining control gaps are identified below.

## B1B-R2-RF-01: Reject production inclusion of an allowed test file

Severity: medium. Prior finding: B1B-R1-RF-03. Location: tools/tests/test_environment_exceptions.py:110-121,136,154.

The revised scanner resolves constants and matches test-module braces correctly, but its included-file confinement rule tests whether the target has any test-gated include. included records all targets, test_included records targets with at least one test-gated include, and whole_file_test uses membership in both. A target included from both a test module and production is therefore classified wholly test-only. Moving or adding a production inclusion while retaining the test inclusion leaves its allowed call/allow sets unchanged and test_only true. Include discovery also scans the raw source, so include! text inside comments or literals can contribute edges. This does not establish the claimed included only from a test module property.

Required correction: Track each real include edge and its effective test scope; a production-reachable inclusion must prevent whole-file test classification. Ignore include-like text in comments and literals, and handle transitive inclusion conservatively. Add a negative control retaining the original test inclusion while introducing a production inclusion of an allowed helper, and require rejection independently of Clippy. Keep the existing constant-change and moved-helper controls.

Evidence:

- included.add(target) is unconditional; test_included.add(target) requires only one in-test occurrence
- whole_file_test = ... or (rel in included and rel in test_included)
- INCLUDE.finditer(texts[rel]) operates on the raw source
- M3-B r5 item 9 and plan r3 require every non-Git exception to remain confined to test targets

## B1B-R2-RF-02: Finish the zero-lookup and refused-pack controls

Severity: medium. Prior finding: B1B-R1-RF-04. Location: crates/security/src/custody/project_admission_carrier_tests.rs:561-627; SCOPE.md Round 2 controls.

The new CI test compares aggregate charges with local.json absent and present. A charged no-follow stat of local.json whose result is ignored has the same cost in both states, so this control still passes if CI always probes the local carrier. The interactive inequality does not establish a zero CI lookup count. The order control now checks registry-size-independent phase-1 costs and unchanged installation paths/file sizes, but still drops a successful CarrierAdmission in lieu of a refused project-layer pack. The existing host X12 test does exercise a refused project pack, yet neither test observes the combined carrier -> resolver/refusal -> no-registry/no-RESERVED/no-lease/no-journal path required by the accepted plan and the prior finding. Deferring that composition to J1 is a remaining control boundary, not completion of RF-04.

Required correction: Count accesses to the local carrier specifically and assert zero in CI, including a negative control that performs and ignores a charged local lookup. Add an observable test composition for a refused project-layer pack that establishes no registry capture and no RESERVED row, lease or journal, without adding a production facade or caller. Keep the host and security tests separate where appropriate, but provide the missing composition evidence or obtain a reviewed scope adjustment before claiming RF-04 and the accepted plan fully implemented.

Evidence:

- ci_makes_no_local_lookup_by_the_ledger_count asserts without == with and interactive != with
- the_first_phase_reads_no_registry_and_has_no_effect drops carriers without resolving a project-layer pack
- configuration_resolver_tests.rs:x12_order_admits_the_resolved_pack_selection_once_after_resolution is a pure host control
- plan r3 section 2 CI and Order controls; prior B1B-R1-RF-04

## Whole-unit assessment

The current implementation reads project/local bytes from the descriptor whose custody was judged, within 4 MiB, with charged samples/read attempts and held-fence carrier/absence rechecks. Source inspection shows the non-interactive branch performs no local lookup; the false rf04ControlsComplete field concerns the regression control's ability to prove that property, not an observed production local lookup.

The separate carrier phase precedes registry capture. The legacy branch remains non-capturing and skips the optional carrier recheck. Five archived matched probe states corroborate equal core admission charges and classification against a git-archive copy of the base. The existing legacy session/gate wrapper bodies retain their checks and latching; the new methods are separate. The probe itself measures core admission, rather than invoking both wrapper paths, so that distinction is retained.

Optional global capture is sound for this unit after the parent fix. It performs installation-private judgments, positively records absence and rechecks it under the same original parent samples, and creates nothing. InvocationModeV1 is unified; its pure rule is the conjunction of stdin/stderr terminal observations, with no environment input or production caller. The operability table adds only the one invocation_mode.rs stdio row, count one, owned by output and terminal.

The 13 current item-level allowances cover r5's 17 existing call sites; their actual names and current test confinement match the accepted law. The per-crate configurations name all four prohibited methods identically. The narrower implementation list without an unused child-marker read is sound (LD-B1B-5). Splitting hostile-environment controls by crate avoids a public facade and now compares complete stable resolution/provenance output and capture facts (LD-B1B-4). Those two decisions are sound; the unrelated remaining order/zero-lookup controls still prevent full-plan acceptance.

New refusal variants map to existing public rows. There is no new public API, CLI wiring, discovery, inventory successor, production caller or qualification.

## Evidence and review execution

Independently ran exactly the two permitted offline commands:

- `python3 -I -B tools/tests/test_environment_exceptions.py`: seven tests passed, including the two copy-based negative controls.
- `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-b1b`: passed, no findings, 114 rows.

Validated all eight archived control logs against controls.json: six mutations have the named test failures, and both planted production reads trigger disallowed_methods with compilation failure. The new judgment-binding and parent-sample controls were caught. Checked the five legacy probe lines against both raw archived probe logs; base and candidate match exactly for no config, small config, large config, .opensip present and local present.

The full-suite comparison record has equal failure-name sets and suite counts: security retains 14 failures with passes increasing from 1,046 to 1,061; host retains eight failures with passes increasing from 330 to 335. Full-suite raw transcripts are not subject members, so these full-run claims are supported by the submitted comparison record and runner, not independently rerun or reconstructed from raw suite transcripts. Archived Clippy evidence supports the all-targets warning-denied invocation. The format classification, tools/census logs and design-verification log agree with checks.json. Design verification reports inventory 188 and 162 contract successors. This review uses the supplied fresh checks-r4 evidence; failed earlier attempts are not acceptance evidence. SCOPE.md's older checks-r1 wording does not override the fresh pinned evidence.

No Cargo, rustc, builds, other tests, lane or network was run by this review. No private fixture, installation directory, signing keys, held trees, other panes or delegation were used. Neither repository, the candidate worktree, stage, controls nor prior review was edited. Persistent review writes are limited to this directory's REVIEW.md and review.json; the expressly permitted checker creates and cleans its own temporary copies.

# B1-B-r1 review

Verdict: **REQUIRED-FINDINGS**

Four required findings and one non-blocking observation. The candidate has the planned structure, but the custody gaps and incomplete structural/behavioral controls prevent acceptance.

Verified the 9,764-byte subject manifest, SHA-256 `d85805074572976992cebd1e13b75c95df3bcbc4c1b8dd4eb82541ccbcf617a5`, and all 43 members. All 24 product-map files match their candidate worktree and archived bytes: 18 changed and six new. Parent pins match product base `c0151bc6b7fdb6db9157124fa068c8be5061f5d4`; new paths are absent there. The candidate's changed/untracked path set equals the map exactly. Source authority pins match architecture base `b98932720200253f671814d9cb728ba0615c1085`. The unchanged lock retains inventory 188 and 162 contract successors.

## B1B-R1-RF-01: Bind capture to the custody judgment instead of taking a new baseline

Severity: high. Location: crates/security/src/custody/project_admission.rs:245-255,1091-1126,1205-1221.

Selection retains only File after judge_project_object returns (), discarding the sample that passed custody. capture_carrier later takes an entirely new metadata baseline; carrier_sample extracts metadata without applying the custody predicate. If the selected opensip.json is rewritten or made others-writable after selection but before this new baseline, both capture samples and the later same_carrier recheck can equal the changed state. The admission therefore accepts bytes or custody that differ from the selection judgment. Local capture has the same judgment-to-new-baseline gap. Retaining the same descriptor prevents replacement from redirecting that descriptor, but does not prevent mutation of its object.

Required correction: Retain the full sample associated with the successful custody judgment alongside the descriptor on the analysis path. Require the capture samples to match that judged sample, with appropriate custody/name checks, and keep the legacy path's charges unchanged. Add deterministic controls interposing a rewrite and a custody change between selection/judgment and the read; require refusal rather than accepting the new baseline. Retain the post-capture replacement controls.

Evidence:

- examine returns Examined::Config(Option<File>) without a judgment sample
- capture_carrier compares only samples acquired after the original judgment
- same_carrier compares against that later metadata baseline
- X2 r9 item 3a; MB item 2 swapped-file/race control; plan r3 section 1.1

## B1B-R1-RF-02: Judge and retain parents of optional absence observations

Severity: high. Location: crates/security/src/custody/installation_read.rs:628-642,939-1026.

first_absent opens each existing prefix but never calls judge_directory, named, or the installation filesystem admission. If I/host exists with wrong private custody and settings.json is absent, capture_optional returns Ok(None). Only the string host/settings.json is retained. recheck_absent opens those prefixes again without custody, exact-name, filesystem or original-identity checks, so replacement or a custody change of the parent also passes while the leaf remains absent. Neither the session's required files nor its captured-file list receives that optional parent. Native open_child_directory explicitly proves none of those custody facts. This is not a positive absence under a judged parent as LD-B1B-2 requires.

Required correction: Observe optional absence through the same charged private-directory, exact-name, filesystem and attachment judgments used by capture. Retain the judged existing parent chain and the first absent component, then recheck those original owners and the absence under the held fence. Preserve full-recheck/latching semantics on refusals. Add controls for a wrong-custody existing host directory with an absent leaf, custody changes, parent replacement/detachment, absent host appearing, and leaf appearance.

Evidence:

- first_absent retains Vec<RetainedDirectory> only locally and drops it on return
- State.absent is Vec<String>; recheck_absent reopens names and accepts vanished prefixes
- read_capture at installation_read.rs:1050-1088 performs the omitted parent judgments
- crates/platform/src/filesystem/directory_open.rs:127-134 documents the limited open guarantee
- MB item 2; plan r3 LD-B1B-2

## B1B-R1-RF-03: Make the exception pin enforce actual variable names and test confinement

Severity: medium. Location: tools/tests/test_environment_exceptions.py:16-38,51-70,90-101.

The permitted checker passes on the current bytes, but it does not enforce two claimed invariants. EXPECTED pins tokens HELPER_INPUT, x8c::HELPER and MARKER rather than their constant values; changing the corresponding definitions to a different environment name leaves the scan unchanged, while the enclosing Clippy allow still permits the new read. Test confinement is computed as any line after the first cfg(test) module opener (or merely a _tests.rs filename), without tracking the module's closing brace or whether an included file is actually test-gated. Moving an already-allowed function into production after such a module would still be classified test-only. These defeat the promised exact law list and sole production exception.

Required correction: Resolve or explicitly pin the three constant-backed environment names, and verify actual enclosing cfg/test-target scope rather than a first-line threshold or filename suffix. Check item-level allowance attachment within that scope. Add focused negative controls that change a constant's value and move an allowed test helper outside its test module; both must be rejected without relying on Clippy to detect an already-allowed method.

Evidence:

- CALL records call.group(2) unchanged; EXPECTED contains constant identifiers
- test_from is a single line index and test_only uses index > test_from
- M3-B r5 item 9 requires a concrete exact exception list confined to test targets
- plan r3 section 1.5 promises checks by file, enclosing item and variable name

## B1B-R1-RF-04: Complete the accepted plan's behavioral controls

Severity: medium. Location: crates/security/src/custody/project_admission_carrier_tests.rs:235-257,299-318,461-496; crates/host/src/configuration_resolver_tests.rs:1314-1372.

The order test drops a successful CarrierAdmission and calls that a refused pack; it neither exercises a refused project-layer pack nor asserts absence of registry capture, RESERVED rows, leases and journals. The legacy ledger test compares two executions of the candidate (small versus large carrier and absent versus present local), not the base-computed expectation required by plan r3, and does not cover both wrapper paths. The CI tests check outcomes rather than the promised counting observer, so an ignored local lookup need not fail. Finally the split hostile-environment controls compare carrier hashes and only resolvedConfigDigest plus provenance layer names; they do not compare the complete resolved record/provenance (operational values are excluded from that digest). The clean children inherit the parent environment instead of using the planned cleared baseline, and no new separate permitted-Git-refusal assertion is present. LD-B1B-4 avoids a public facade appropriately but does not retain the same control coverage as claimed.

Required correction: Supply an observable refused-project-pack composition control with the required no-registry/no-effect assertions, matched base ledger expectations for the legacy read-session and write-gate wrappers, and a local-lookup counting control. Keep the crate split, but compare complete stable resolution/provenance output including operational fields, use a controlled clean child environment, and separately assert the permitted Git environment refusal. Add the judgment-to-read and optional-parent controls required by RF-01/RF-02. Update evidence and SCOPE.md to describe what the controls actually establish.

Evidence:

- plan r3 sections 1.5 and 2 explicitly require these controls
- the_first_phase_reads_no_registry_and_the_second_does contains drop(carriers.unwrap()) without pack resolution or lookup/effect counters
- legacy_spend runs only the candidate implementation
- host child prints digest and leaf=layer, not complete resolved values/provenance
- security and host parents call env(...) only for the hostile variant and never env_clear()

## Non-blocking observation

B1B-R1-NBO-01: The rustfmt command checks eight Rust files and declares three base-dirty exclusions, leaving nine other edited Rust files outside both groups (the allowance-only changes in host integration tests, git_tracking, fence/root/routing/writer/read-premise tests and journal_store). Narrow the format claim or include those files in a later check with any additional base exclusions documented.

## Verified behavior and evidence limits

The analysis selection does retain and read the descriptor originally judged; RF-01 concerns the missing link to that judgment's sample, not reopening by name for the byte read. The project/local absence states have charged lookups and held-fence rechecks. CI's non-interactive branch performs no local lookup. The separate carrier and registry phases establish the structural order, while resolution/pack composition remains with J1. Legacy branches retain their reads and charges by source comparison, and skip carrier rechecks when carriers is None; the missing matched-base ledger control is recorded separately in RF-04.

InvocationModeV1 is unified with invocation.rs. The mode rule is stdin-terminal AND stderr-terminal, the observation uses IsTerminal without environment input, and production has no caller. Its operability addition is one stdio row owned by output and terminal. The only product exception-table change is that row.

The two crate-local Clippy files name the four disallowed methods identically. The 13 current item-level allows cover the 17 existing call sites authorized by r5, including the correctly scoped HOME uses; no new environment read was introduced. LD-B1B-5 is sound: an authorized child marker need not be read when ignored children are invoked by exact test name. The active implementation list may omit that unused allowance without admitting another exception. RF-03 concerns the checker failing to preserve the actual names and confinement under changes. LD-B1B-4's crate split avoids a public facade, but its claimed equivalent coverage is incomplete, so its overall soundness field is false pending RF-04.

The new refusal variant maps to existing CONFIG.CUSTODY_REFUSED; Changed and host-I/O rows remain existing rows. No public API, CLI caller, discovery implementation, inventory binding or qualification was added.

Independently ran only the two explicitly permitted offline commands in the candidate worktree:

- `python3 -I -B tools/tests/test_environment_exceptions.py`: five tests passed.
- `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-b1b`: passed, no findings, 114 rows.

The pinned test-comparison JSON records equal exact failure-name sets and suite counts: security 14 failures, 1,046 to 1,057 passes; host eight failures, 330 to 335 passes. The base/candidate suite transcripts are not members of this subject, so those full-run results are supported by the submitted comparison record and runner, not independently replayed or reconstructed from raw suite logs. The corresponding JSON field reflects the equal recorded sets.

Checked the archived raw control logs against controls.json: all four mutations have the named failing tests; both planted reads trigger disallowed_methods and compilation failure. All six controls were caught. The archived Clippy log and recorded command support the warning-denied all-targets run on host and security. The tools logs report five environment-pin tests and nine configuration-table tests; the source census and design verification logs pass, with selected inventory 188 and 162 contract successors. These checks do not remove the findings above or establish qualification.

No Cargo, rustc, builds, other tests or lane were run by this review. No network, private fixture, installation directory, signing keys, held trees, other panes or delegation were used. Neither repository, the worktree, stage nor control files was edited. Only this review directory's REVIEW.md and review.json were written.

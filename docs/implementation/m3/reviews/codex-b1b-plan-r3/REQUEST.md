# Review request: B1B-PLAN-r3 with M3-B r5 (round 3)

## Round 3

Round 2 (`/tmp/opensip-implementation/reviews/codex-b1b-plan-r2/`, your REQUIRED-FINDINGS) raised two findings and one observation. Do not modify it. The stage holds plan r3 (r1 and r2 kept as history) and the corrected M3-B r5.
- **RF-01.** r5's item 9 bullet and the plan now state the real-`HOME` exceptions by their actual use:
  - one comparison, `installation_root.rs:787` in `installation_root_native_source_ignores_environment_child`;
  - three named installation-absence probes, each with its enclosing test.

  r5's change table states the counts: 17 call sites, 1 production and 16 test-only, across 13 test variable names (NBO-01).
- **RF-02, the CI appearance control.** It is narrowed to a custody-valid `.opensip` with no marker, with a contrasting marker/custody refusal.
- **RF-02, the environment-equivalence control.** It now stops before X2's tracking step, and the permitted Git refusal is asserted separately.

Check r5 against the live `PROPOSAL.md` again: only the title, banner, change table and the item 9 Enforcement bullet may differ. Then check that the exception list is exact against every call site at the product base, and judge the whole plan again.


Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1b-plan-r3/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b1b-plan-r3-stage`
- **Subject file.** `subject.json`: 1036 bytes, SHA-256 `dd375c13ee384d9251bab9e07ca2e77d6cf16c1f2946f20a97921ef9ad4b84c2`, 4 member(s). Rehash every member.
- **Bases.** Product `c0151bc6b7fdb6db9157124fa068c8be5061f5d4` (clean: B1-a code and inventory v188 bound), architecture `93960ed5327615ead9af08845a4bc27ce3409e76`.
- **Authority.**
  - M3-B r4 (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`): items 2, 3, 9, 10 and 15, and the units table row B1-b.
  - X2 r9 (`docs/implementation/m2/project-root-x2/PROPOSAL-r9.md`): items 3, 3a with its order decision, 9 and 10.
  - AQ section 1.1 and HFC section 3.
  - The product sources section 0 cites: `crates/security/src/custody/project_admission.rs`, `installation_read.rs`, `installation_admission.rs` and `git_tracking.rs`; `crates/host/src/invocation.rs` and `configuration.rs`; `crates/platform/src/work_reader.rs`.

## What to review

The plan fixes how B1-b is built before any code exists. Judge:
0. **Rounds 1 and 2.** Are round 2's RF-01 and RF-02 resolved, and do round 1's resolutions still hold? Is r5 sound, exact and complete?
1. **Scope.** Does it match MB:876 and its gate cells (FW-01, SL:3, flag `--project`)?
2. **Facts.** Are section 0's facts accurate at the product base?
3. **Capture (section 1.1).** Does it meet X2 item 3a and MB item 2? Check retention by descriptor with no reopen by name; the 4 MiB bound; ledger charging; and the samples joining the held-fence recheck, including absence.
4. **LD-B1B-1.** Is the two-phase admission split sound, and does it enforce X2 r9's order without changing the existing callers' behavior?
5. **LD-B1B-2.** Is the optional global capture sound: positive absence rechecked, never created?
6. **Invocation mode.** Is it unified (B1-a's duplicate type removed), with no environment input and no caller wired before J1?
7. **LD-B1B-3.** Is the per-crate `clippy.toml` scope right? Is the exception list right, including the test-only fixture reads that the law's wording ("crash-matrix seams") does not name? Is the planted control adequate?
8. **Section 2's controls.** Are they sufficient, including the MB item 10 refused-pack control and FW-01?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "dd375c13ee384d9251bab9e07ca2e77d6cf16c1f2946f20a97921ef9ad4b84c2",
  "r2Rf01Resolved": true,
  "r2Rf02Resolved": true,
  "r1FindingsStayResolved": true,
  "mbR5OnlyItem9EnforcementChanged": true,
  "mbR5ExceptionListComplete": true,
  "scopeMatchesMB876": true,
  "factsSection0Accurate": true,
  "captureFollowsX2Item3a": true,
  "twoPhaseOrderLDB1B1Sound": true,
  "optionalGlobalCaptureLDB1B2Sound": true,
  "invocationModeUnified": true,
  "environmentCheckLDB1B3Sound": true,
  "controlsSufficient": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChangeOtherThanR5Item9": false,
  "productQualification": false
}
```

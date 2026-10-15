# Review request: B1B-PLAN-r2 with M3-B r5 (round 2)

## Round 2

Round 1 (`/tmp/opensip-implementation/reviews/codex-b1b-plan-r1/`, your REQUIRED-FINDINGS) raised three findings. Do not modify it. This round has two subjects in one stage:

- **`b1-b/PLAN-r2.md`.** It answers RF-01 (explicit, charged negative observations, rechecked; corrected inherited-recheck facts), RF-02 (the exception list now obeys law) and RF-03 (a separate analysis path; the legacy path untouched, with compatibility controls). `PLAN-r1.md` is kept beside it as history.
- **`PROPOSAL-r5.md`, M3-B r5.** RF-02 offered two ways out: remove the fixture dependencies, or correct the law. The lead chose a law correction. r5 changes only item 9's Enforcement bullet, to an enumerated exception list: one production read (`git_tracking::process_environment`) and the existing test-only reads, each confined to test targets and named concretely. Diff it against the live `PROPOSAL.md`. Everything except the title, banner, the new "r5 changes" table and that bullet must be byte-identical.

Check that r5's list is complete and exact against the product: every `std::env::var`, `var_os`, `vars` and `vars_os` call in `crates/host` and `crates/security` at the product base. Then judge the whole plan again.


Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1b-plan-r2/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b1b-plan-r2-stage`
- **Subject file.** `subject.json`: 843 bytes, SHA-256 `0becb1c863b7f808548f61173222aa59fe71af0806fc95a8482a6438e4b419dc`, 3 member(s). Rehash every member.
- **Bases.** Product `c0151bc6b7fdb6db9157124fa068c8be5061f5d4` (clean: B1-a code and inventory v188 bound), architecture `93960ed5327615ead9af08845a4bc27ce3409e76`.
- **Authority.**
  - M3-B r4 (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`): items 2, 3, 9, 10 and 15, and the units table row B1-b.
  - X2 r9 (`docs/implementation/m2/project-root-x2/PROPOSAL-r9.md`): items 3, 3a with its order decision, 9 and 10.
  - AQ section 1.1 and HFC section 3.
  - The product sources section 0 cites: `crates/security/src/custody/project_admission.rs`, `installation_read.rs`, `installation_admission.rs` and `git_tracking.rs`; `crates/host/src/invocation.rs` and `configuration.rs`; `crates/platform/src/work_reader.rs`.

## What to review

The plan fixes how B1-b is built before any code exists. Judge:
0. **Round 1.** Is each of RF-01, RF-02 and RF-03 resolved? Is r5 sound and complete?
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
  "subjectManifestSha256": "0becb1c863b7f808548f61173222aa59fe71af0806fc95a8482a6438e4b419dc",
  "rf01Resolved": true,
  "rf02Resolved": true,
  "rf03Resolved": true,
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

# Review request: B2B3-PLAN-r3 (the lead's implementation plan for B2-b3, the S3 downward walker)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b3-plan-r3/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b3-plan-r3-stage`
- **Subject file.** `subject.json`: 452 bytes, SHA-256 `bdf28579b863d79cc451e784e9ab559c6b6ef8e0c12f1524093972fc280fffe5`, 1 member(s). Rehash every member.
- **Earlier rounds.** Your `codex-b2b3-plan-r1` (REQUIRED-FINDINGS) is at `/tmp/opensip-implementation/reviews/codex-b2b3-plan-r1`, and your `codex-b2b3-plan-r2` (ACCEPT, published at architecture `363303dc`) is at `/tmp/opensip-implementation/reviews/codex-b2b3-plan-r2`. PLAN-r3 is plan r2 with one lead amendment, of LD-B2B3-12 (and the facts and split row it touches), stated in its "r3 changes" section. B2-b3a is bound; B2-b3b is in your review; no B2-b3c code exists.
- **Bases.** Product `aa037d09995f7710bda5f8993ff9133f829e3df3`, clean: B2-b1 and B2-b2 are bound. Architecture `c568f47930163bc3c8a85457c060a09eff0a4e34`.

## Authority

- The accepted B2-b plan r4 (`docs/implementation/m3/config-discovery-b/b2-b/PLAN-r4.md`): section 1.3, LD-B2B-2 and LD-B2B-5 to LD-B2B-9.
- M3-B r5 items 12, 13 and 15, and the test owners.
- **(r3)** Law X8 r3 item 4b and unit X9-1's site-list pin (`crates/security/src/crash_matrix_sites.rs`); the shared installation fixture (`custody/installation_read_fixture.rs`, `InstallationAt::writer` and `operation`); `crates/security/src/scenario.rs`; the host's resolver (`crates/host/src/configuration.rs`) and B1-b's cross-crate control (`crates/host/src/configuration_resolver_tests.rs`); COV:5268-5407.
- The bound B2-b0 reference's `walker_population` (contract successor 164).
- SL S3.
- X2 r9: items 1, 3a and 7a (the handoff).
- M3-C item 2's walk rules (`docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` lines 268-296).
- COV:5288 and COV:5388.
- The product's `operation_handoff.rs`, `installation_read.rs`, `installation_session.rs`, `project_admission.rs`, `project_chain.rs`, `read_premise.rs`, `trust/initial_platform.rs`, platform `directory_entries.rs` and `directory_open.rs`, `custody/discovery_scan.rs`, `scenario.rs`, `configuration.rs`, and `tools/tests/test_environment_exceptions.py`.

## What to review

Judge only the amendment, against the accepted plan r2:
1. **The facts.** Does X8 r3 item 4b, as unit X9-1's source pin (`crates/security/src/crash_matrix_sites.rs`) holds it, keep the shared installation fixture's read-session helpers `cfg(test)`, so that the `scenario-fixtures` seam cannot open a read session without a law change? Is the host's resolver `pub(crate)`, so that an integration test cannot use it?
2. **The write-path chain.** Is `ScenarioHome::discover`'s order sound: phase 1 with the explicit path and waiver; resolution and pack admission with the CLI layer; phase 2; tracking, first registration and `begin_operation` as the shared composition makes them; `discovery_root`; the walk and the core; `end`? Does it reach only fixture gates that X8 names? Does it keep r2's control that a resolution or admission failure never reaches phase 2 or any downward observation?
3. **The flag rows.** Are the `--project` and `--workspace-root` controls sufficient for COV:5288's and COV:5388's method ("exact applicability, provenance and precedence from the source join; selection never grants execution/custody and configuration never impersonates explicit consent")? Is leaving the foreign-owner case to the B2-b3a and B2-b3b vectors sound?
4. **The owner path.** Is running the rows as host unit tests, and leaving `crates/host/tests/discovery_tests.rs` planned for J1 (plan r4 LD-B2B-7), sound? Or must B2-b do something else?
5. **The rejected alternatives,** and whether every other decision of plan r2 stands unchanged.

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "bdf28579b863d79cc451e784e9ab559c6b6ef8e0c12f1524093972fc280fffe5",
  "r3FactsAccurate": true,
  "readSessionSeamNeedsLawChange": true,
  "writePathChainWithinX8Gates": true,
  "ldB2B3_12R3Sound": true,
  "flagRowControlsSufficient": true,
  "covOwnerPathHandlingSound": true,
  "otherDecisionsUnchanged": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```

# Review request: B2B-PLAN-r4 (the lead's implementation plan for M3-B unit B2-b, the S3 downward instrument)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b-plan-r4/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted. You may import architecture Python models read-only to check a claim; write nothing.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b-plan-r4-stage`
- **Subject file.** `subject.json`: 449 bytes, SHA-256 `7cfa2155256296156b5f4bb0b54ed8d46edf43042f49e30558c9dd9efb9dcecf`, 1 member(s). Rehash every member.
- **Earlier rounds.** Your `codex-b2b-plan-r1` (`/tmp/opensip-implementation/reviews/codex-b2b-plan-r1`) raised B2BPLAN-1 to B2BPLAN-5. Your `codex-b2b-plan-r2` (`/tmp/opensip-implementation/reviews/codex-b2b-plan-r2`) found B2BPLAN-2 to B2BPLAN-5 resolved and B2BPLAN-1 partially resolved, because SLM's `finish` over-observes below the anchors. PLAN-r3 added the observation adapter. Your `codex-b2b-plan-r3` (`/tmp/opensip-implementation/reviews/codex-b2b-plan-r3`) found two adapter defects: pruned anchors kept children (B2BPLAN-1), and the explicit chain lost ancestor `Cargo.toml` (B2BPLAN-2, reopened). PLAN-r4's "r4 changes" table states the resolution.
- **Bases.** Product `94e5fdebd63a174694dadbb5e647063855614b77` (clean: B1-a, B1-b, B3-a and B2-a are bound; inventory v191; 163 contract successors), architecture `424f64a3f331261d0f1e8fb323948492cda5a06d`.
- **Authority.**
  - M3-B r5 (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`): items 12, 13 and 15 (FW-01); the B2-b row; the order; the test owners.
  - B-S1: SX-1, LD-4, LD-10, LD-15, the V3 schema additions and the owed controls.
  - The B2-a plan's LD-B2A-2 and LD-B2A-5.
  - SL S3; SLM `discovery` and `boundary_inventory`; `security/discovery-cases.v1.json`.
  - X2 r9 (`docs/implementation/m2/project-root-x2/PROPOSAL.md`) and the T2 fetch spec.
  - The product's `work_ledger.rs`, `descriptor_acl_capture.rs`, `directory_entries.rs`, `directory_open.rs`, `project_admission.rs`, `project_chain.rs`, `custody.rs`, `operation_handoff.rs`, `outcomes.rs` and `installation_termination.rs`.

## What to review

The plan fixes how B2-b is built before any code exists. Judge:
0. **Earlier rounds.**
   - **B2BPLAN-1.** Is it fully resolved? A pruned anchor of any reason must contribute only its own entry, with no child (`.git` and `opensip.json` included), and the boundary-evidence exception must apply only to ordinary, non-pruned directories. Do the direct population assertions cover all four reasons?
   - **B2BPLAN-2.** Is it resolved again? The parent-first chain must observe each level's `Cargo.toml`, `.git` and `opensip.json`, stop unopened at the first pruned prefix, and refuse an earlier crossing first. Does that match SLM's crossing-first order on the restricted population? Do the Cargo `target` join controls through both sources, the ordinary-`target` control, the crossing-above-prune control and the repository-below-prune control suffice?
   - **Pass two's difference rule.** Every outcome difference must have a listed cause. Is that sound?
   - Do B2BPLAN-3 to B2BPLAN-5 stay resolved?
1. **Scope.** Does it match MB items 12 and 13 and the B2-b row? Does it leave B2-c, B3-b, C1 and J1 their own?
2. **Facts.** Are section 0's facts accurate? That includes the ledger caps and ACL cost, the missing by-name observation, the absent upward provenance, the existing host rows, and the T2 store.
3. **The split (LD-B2B-1)** and each sub-unit's content and tests.
4. **The lead decisions:**
   - LD-B2B-2: custody for unit chains and markers only;
   - LD-B2B-3: V3 records with D15 content pending B3-b, and a schema-valid inventory now;
   - LD-B2B-4: the census over the materialized store, with held-out entries excluded;
   - LD-B2B-5: case replay and its supersessions;
   - LD-B2B-6: rows through the host's existing observations;
   - LD-B2B-7: flag rows through the scenario seam;
   - LD-B2B-8: per-source observation strategies;
   - LD-B2B-9: the typed waiver;
   - B2-b0: the current reference projection (contract successor 164).
5. **Controls.** Are they sufficient? That includes the CI trace, the `lstat`/`open` refusal, exhaustion, FW-01 and the margin stop.

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "7cfa2155256296156b5f4bb0b54ed8d46edf43042f49e30558c9dd9efb9dcecf",
  "b2bplan1Resolved": true,
  "b2bplan2Resolved": true,
  "b2bplan3To5StayResolved": true,
  "observationAdapterSound": true,
  "pruningPrecedenceSound": true,
  "parentFirstChainSound": true,
  "scopeMatchesMBItems12And13AndB2bRow": true,
  "factsSection0Accurate": true,
  "splitSound": true,
  "ldB2B1Sound": true,
  "ldB2B2Sound": true,
  "ldB2B3Sound": true,
  "ldB2B4Sound": true,
  "ldB2B5Sound": true,
  "ldB2B6Sound": true,
  "ldB2B7Sound": true,
  "ldB2B8Sound": true,
  "ldB2B9Sound": true,
  "b2b0ReferenceSound": true,
  "controlsSufficient": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```

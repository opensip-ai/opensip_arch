# Review request: B3-A-r1 (`grants.rs`; M3-B unit B3-a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3a-r1/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing, Git queries, and these read-only offline checks are permitted:
- `python3 -I -B tools/tests/test_environment_exceptions.py` in the candidate worktree;
- `python3 -I -B tools/check_operability.py source --repository <tree>`;
- `python3 -I -B tools/security/storage_choice_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, run in the candidate worktree. It writes nothing in `--check` mode.

## Subject

- **Stage.** `/tmp/opensip-implementation/b3a-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b3-a-r1-subject.json`: 8188 bytes, SHA-256 `057c982301bf98043b6287fb32de502a70ca2c5a2b5e6b1fdbf167a4e44b9d12`, 37 members. Rehash every member.
- **Bases.**
  - Product `ec70009de1490449a6173c238a7eaf0a03e106c4`, clean: B1-b and v189 are bound.
  - Architecture `70950d53ce1ab79c99c51c5340b5d101b397801b`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b3a` holds the exact bytes of `product-map.json`.
- **Counts.** Inventory 189 and contract successors 162 are unchanged. v190 follows acceptance: `grants.rs` turns present, and the new paths are added.

## Authority

- The accepted plan `config-discovery-b/b3-a/PLAN-r1.md` (you accepted it in `codex-b3a-plan-r1`, with no findings).
- M3-B r5 (`PROPOSAL-r5.md`): item 23, item 8's shared-flags row, and the B3-a row.
- SL: S3 (SL:120-130), S3.1 (SL:317-331) and SL:1110.
- SLM `storage_write_admission` (SLM:3104-3128).
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit and two new lead decisions:
- **LD-B3A-4:** the compile check is an in-crate trait probe, not a rustc snippet in the accepted X8 harness.
- **LD-B3A-5:** the policy-record grammar refuses the trailing newline that Python's `$` admits.

Judge:
1. **The records against item 23 and plan section 1.1.**
   - Constructors from parsed invocation values only.
   - Duplicate collapse, provenance, and the 64 bound with no truncation and no public row (LD-B3A-2 and LD-B3A-3).
   - The waiver's refusal on the existing `PROJECT.EXPLICIT_PATH_INVALID` row.
   - The acknowledgement.
   - `PolicyRecordId` and `ConsentSource`, with SL:1110's mapping.
   - Private fields; not `Clone`; no conversion, default, serde or configuration path.
2. **S3.1.**
   - Does `storage_write_choice` reproduce `storage_write_admission`'s order and spellings exactly?
   - Is `Refuse` mapped to the existing `BackupChoiceRequired` row, whose host projection is `REQUEST.PRECONDITION_FAILED` / `storage.backup-choice-required`?
   - Are the 144 vectors sound and generated at the pinned bytes, with the tool following B1-a's pattern?
   - Is excluding the newline spelling (LD-B3A-5) right?
3. **`from_grants`.** Is it the typed source of the existing set, delegating to the unchanged `new`, with no consumer?
4. **The no-configuration and purity controls.**
   - Does the trait probe actually fail on a forbidden impl? The compile controls in `controls.json` should show it.
   - Are the source pins sound?
   - Is LD-B3A-4's replacement of the plan's rustc-snippet wording sound?
5. **The evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - Equal failure sets for security and host.
   - Clippy.
   - rustfmt, with its declared base-dirty exclusions.
   - The environment-exception pin, with an unchanged list; `grants.rs` sits under the lint.
   - The census, verify_design, the vector check, and the mutations, compile controls and planted read, each caught.
6. **Scope.** The paths are exactly the product map's. There is no host change, public API, caller or qualification. `initial_installation::storage_choice` is unchanged.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "057c982301bf98043b6287fb32de502a70ca2c5a2b5e6b1fdbf167a4e44b9d12",
  "implementsPlanR1": true,
  "recordsMatchItem23": true,
  "noConfigurationConstructor": true,
  "recordsNotClone": true,
  "s31ChoiceMirrorsSlm": true,
  "vectorsReproduceSlmAtAcceptedBytes": true,
  "existingRowsReusedNoNewCode": true,
  "fromGrantsDelegatesUnchanged": true,
  "modulePure": true,
  "ldB3A4Sound": true,
  "ldB3A5Sound": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 15,
  "inventoryUnchanged": 189,
  "contractSuccessorsUnchanged": 162,
  "publicApiAdded": false,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then v190, reviewed and bound separately. Nothing is pushed.

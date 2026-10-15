# Review request: B2-B2-r2 (the pure discovery core; M3-B unit B2-b, sub-unit B2-b2)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b2-r2/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing, Git queries, and these read-only offline checks are permitted:
- `python3 -I -B tools/check_operability.py source --repository <tree>`;
- `python3 -I -B tools/tests/test_environment_exceptions.py` in the candidate worktree;
- `python3 -I -B tools/security/discovery_scan_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, run in the candidate worktree. It writes nothing in `--check` mode.

You may also import the bound reference read-only to try your own synthetic scopes.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b2-r2-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b2-r2-subject.json`: 6944 bytes, SHA-256 `5b2f87759dc0993b6563ca05bdba12574bbdba7a55eac0ce10c516c90bab02a5`, 31 members. Rehash every member.
- **Round 1.** Your `codex-b2b2-r1` (REQUIRED-FINDINGS: B2B2-1) is at `/tmp/opensip-implementation/reviews/codex-b2b2-r1`. SCOPE.md's "r2 changes" section states the resolution.
- **Bases.**
  - Product `f51769f885dc786168e487033645ad1a4e0ae699`, clean: B2-b1 is bound, B2-b0 is contract successor 164, and inventory is v191.
  - Architecture `588e3e847379e871d9b86d73c4b86a27f08f9998`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b2` holds the exact bytes of `product-map.json`.
- **Counts.** Inventory 191 and contract successors 164 are unchanged. Inventory v192 follows acceptance and adds the four new paths.

## Authority

- The accepted B2-b plan r4, section 1.2, LD-B2B-3, LD-B2B-5 and LD-B2B-9 (`codex-b2b-plan-r4`).
- The bound current reference B2-b0 (contract successor 164), and through it SLM `discovery` / `finish`.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit. Judge:
0. **Round 1, B2B2-1.**
   - Is it resolved? `reference_order` must judge kind, owner, mode and the real ACL first, then links and size, exactly as SLM `_file_custody` does.
   - Is the legacy `check_project_object` order kept?
   - Do the eight new vectors (combined ACL and link or size failures, and waived chains with a foreign-owned marker) and the side-by-side test suffice?
   - Is the new mutation caught?
1. **The core against the bound reference.**
   - Does `discover` mirror SLM `finish`, as the current reference runs it, exactly?
   - In particular: nested repositories and projects; the exclusive source; `_explicit_units`, with every `JOIN_*` detail and the custody rows; automatic enumeration, with observed directories, the basis and unreadable anchors; the exclusions in their order; the cap after exclusions; the D9 rows.
2. **Custody through the product judge.**
   - Is the product's `check_project_object_waived` equivalent to SLM `_dir_custody` and `_file_custody` on these observations?
   - Is the normalized `ObservedAcl` (readable entries, or unreadable) a sound interface for the walker's premise-applied capture?
3. **The waiver (LD-B2B-9).**
   - Does it reach only root-to-unit chains, never markers?
   - Does it skip only the owner comparison?
   - Is the legacy `check_project_object` the same judgment?
4. **The records (LD-B2B-3).**
   - The pending provenance has no serializer, `impl` or completion, and no declaration type exists.
   - The boundary inventory is complete, with `to_json` as the closed V3 record.
   - The refusal codes and their D9.
5. **The vectors.**
   - Are the 79 vectors sound and generated at the bound bytes, with the tool following the established pattern?
   - Does the test's `fs`-to-observation conversion (modes, absent uid or gid, links, ACL grants, VCS) faithfully represent SLM's synthetic entries?
   - Are the 19 upward-only cases rightly B2-b3's?
6. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - Equal failure sets for security and host.
   - Clippy.
   - rustfmt, with its classification.
   - The environment pin.
   - The vector check, the census and verify_design.
   - The nine mutations and the planted read, each caught.
7. **Scope.** There is no walker, ledger, caller, public row, environment read or export, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "5b2f87759dc0993b6563ca05bdba12574bbdba7a55eac0ce10c516c90bab02a5",
  "b2b2_1Resolved": true,
  "implementsPlanR4Section12": true,
  "mirrorsCurrentReferenceSuccessor164": true,
  "vectorsReproduceReference": true,
  "upwardOnlyCasesRightlyLeftToB2b3": true,
  "custodyThroughProductJudgeEquivalent": true,
  "waiverNarrowAndTyped": true,
  "legacyJudgeUnchanged": true,
  "pendingProvenanceUnserializable": true,
  "boundaryInventoryCompleteAndSerializable": true,
  "corePure": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 10,
  "inventoryUnchanged": 191,
  "contractSuccessorsUnchanged": 164,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then inventory v192, reviewed and bound separately. Nothing is pushed.

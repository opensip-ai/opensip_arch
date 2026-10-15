# Review request: B2-A-r1 (the shared discovery rule; M3-B unit B2-a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2a-r1/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing, Git queries, and these read-only offline checks are permitted:
- `python3 -I -B tools/tests/test_environment_exceptions.py` in the candidate worktree;
- `python3 -I -B tools/check_operability.py source --repository <tree>`;
- `python3 -I -B tools/security/discovery_rule_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch`, run in the candidate worktree. It writes nothing in `--check` mode.

You may also import the bound reference copy read-only to spot-check a vector.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2a-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-a-r1-subject.json`: 6657 bytes, SHA-256 `9f029737e9028748a30b99694e60e8a9c24e4311320fce6ffbecbf94d0e449e3`, 30 members. Rehash every member.
- **Bases.**
  - Product `6d425bcd685b5b73f4c5474695d73964cc769af2`, clean: the reference refresh is bound as contract successor 163, and inventory is v190.
  - Architecture `a0a2e47d471030d2251465eb61d5de1c48f6111a`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2a` holds the exact bytes of `product-map.json`.
- **Counts.** Inventory 190 and contract successors 163 are unchanged. v191 follows acceptance and adds the new paths.

## Authority

- The accepted plan `config-discovery-b/b2-a/PLAN-r1.md`, section 1.2 and section 3 (`codex-b2a-plan-r1`).
- The bound reference `b2-a-reference/reference/discovery-defaults.sx1-r1.py` (`codex-b2a-reference-r2`).
- M3-B r5 items 13 and 14.
- B-S1's SX-1, its passages and its B2-a controls.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit. Judge:
1. **The rule against plan 1.2 and the bound reference.**
   - Does each function mirror its reference entry point exactly? That covers outermost-across-four-reasons, parent-first Cargo roots, the SX-1 anchor at `""` and member roots only, exact bytes, sorting, enumeration bases and unreadable anchors, the cap without truncation, locator grammar, boundary order, custody exclusion and both prefix functions.
   - Is `classify_entry` sound, with `NeverEnter` for every kind and `recorded` only for the anchor directory itself (LD-B2A-4, LD-B2A-5)?
2. **The vectors.**
   - Are the 2,516 vectors generated at the bound bytes, and is the tool sound?
   - Does the Rust dispatch faithfully reproduce each function's reference shape?
   - Is the sweep sufficient?
3. **The SX-1 controls B-S1 owes B2-a.** Is the disposition half here, with the trace left to B2-b as the plan states?
4. **Scope.**
   - `pub(crate)` with no export, under `allow(dead_code)` (LD-B2A-3).
   - No records, rows or membership (LD-B2A-2).
   - The paths are exactly the product map's, and no host file changed.
5. **The evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - Equal failure sets for security and host.
   - Clippy.
   - rustfmt, with its declared base-dirty exclusions.
   - The environment-exception pin, with an unchanged list.
   - The census, verify_design and the vector check.
   - The nine mutations and the planted read, each caught.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "9f029737e9028748a30b99694e60e8a9c24e4311320fce6ffbecbf94d0e449e3",
  "implementsPlanR1Section12": true,
  "mirrorsBoundReferenceSuccessor163": true,
  "vectorsReproduceReference": true,
  "sx1AnchorExactAndOutermost": true,
  "classifyEntrySound": true,
  "capNoTruncation": true,
  "recordsAndRowsLeftToB2b": true,
  "noExport": true,
  "modulePure": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 10,
  "inventoryUnchanged": 190,
  "contractSuccessorsUnchanged": 163,
  "publicApiAdded": false,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then v191, reviewed and bound separately. Nothing is pushed.

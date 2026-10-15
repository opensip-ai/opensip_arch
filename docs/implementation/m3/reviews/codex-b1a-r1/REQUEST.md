# Review request: B1-A-r1 (the configuration resolver; M3-B r4 unit B1-a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1a-r1/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds, generators or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only reading, hashing, JSON parsing and Git queries. Also, read-only and offline:
- `python3 -I -B tools/host/generate_configuration_tables.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --rustfmt /opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt`, run in the candidate worktree;
- `python3 -I -B tools/host/configuration_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, run in the candidate worktree.

Both only read their inputs. Each compares its output with the checked-in file.

## Subject

- **Stage.** `/tmp/opensip-implementation/b1a-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b1-a-r1-subject.json`: 7545 bytes, SHA-256 `a8037278b4849d2d888325eeebd54054bab0a5f15091fe88331c2cc944b64532`, 34 members. Rehash every member.
- **Bases.**
  - Product `08527ebf732b432d7bfe8fce9c749cbfab51d9c1`, clean: B-S10 is bound there.
  - Architecture `6450467bfc5345cb0727dda571a3de27409b16b2`.
  - Candidate worktree `/Users/sb/code/opensip-ai/opensip-b1a`, holding the exact bytes of `product-map.json`.
- **Counts.** Inventory 187 and contract successors 162 are unchanged. No inventory successor exists yet: v188 follows acceptance.

## Authority

- The accepted plan `config-discovery-b/b1-a/PLAN-r2.md` (your `codex-b1a-plan-r2`).
- M3-B r4 (`config-discovery-b/PROPOSAL.md`): items 1 to 8, 10 and 11, the B1-a row of "Units after the law", and the forbidden substitutes.
- AQ section 1.
- PCS, PCM and its checker.
- B-S9 (the remedy) and B-S10 (the bound admission sources).
- `source.json` pins every authority.

## What to review

`SCOPE.md` states the unit, the pipeline, the refusal rows and seven lead decisions (LD-B1A-1 to 7) taken within the plan. Judge each on its basis.

**1. Implementation against plan r2 and M3-B items 1 to 8, 10 and 11:**
- **Order and purity.** Is the eleven-step order exact, with every layer admitted before any merge? Is it pure: no I/O, environment, lock or ledger? Is the local carrier unread in CI?
- **Internal layers (RF-02).** Do the defaults and flags layers run the same steps, with the host-invariant row?
- **Merge.** Does a higher layer replace the whole leaf, and is absence preserving?
- **Logical paths.** Are they as PCM:23-27, with `.` admitted only for `workspaceRoots` and `ignorePaths`?
- **Registries.** Are the profile, capabilities (LD-B1A-1), waivers and components (LD-B1A-2) right?
- **Defaults completeness.** Is a missing compiled value the host invariant?
- **Partition.** Is it by the generated table only?
- **Normalization.** Is it PCM:42-48, with `allowedScopes` kept?
- **Semantic shape and digest.** Is the shape identity-v3 `semantic-configuration`, and the digest the raw SHA-256 of canonical bytes, not an H-identity?
- **Provenance.** Does it never enter the digest?
- **Schema-one.** Do schema-one files go through the exact preview carrier `$defs/<layer>`, with a 1:1 in-memory projection and no rewrite?
- **X12 order.** Does `resolve_analysis_configuration` resolve, then admit once, with nothing between?

**2. The refusal rows.**
- Is the row chosen by the layer's kind, not the step (plan r2 section 4)?
- Are the subjects as LD-B1A-4 states them?
- Are there no new codes?
- Does the termination match have no wildcard arm?
- Does B-S9's remedy reach external refusals byte for byte (706 bytes, `7ba6e8e5…`)?

**3. The generated registries and the mapping (item 8).**
- Is `configuration_classes.json` right:
  - each PCS leaf's DRC class;
  - the per-layer allowlist as item 2's table (LD-B1A-3);
  - the semantic leaves equal to identity-v3?
- Is the generator correct and drift-checked, and do the arch input pins match the accepted v45 manifest?
- Do the CINV flag classes and `configuration_leaf` keep the other six flags out of configuration?

**4. The PCM vectors (item 4 controls).**
- Is `configuration_vectors.py` sound: PCM at its accepted bytes, and `jsonschema` imported only after the pin check?
- Is LD-B1A-6's re-expression of `check-product-configuration.py` faithful?
- Are all 52 cases reproduced by the Rust test (digest, semantic record, provenance layers or refusal class)?

**5. The tests and the evidence.**
- The plan r2 section 6 controls.
- `evidence/checks.json`:
  - host tests base versus candidate, with equal failure sets (the pre-existing base failures);
  - Clippy;
  - rustfmt on the edited files;
  - the operability source census;
  - verify_design;
  - the generator and vector drift checks;
  - the tools controls.
- `evidence/mutations.json`: the eight mutations, each caught.

**6. Scope.**
- There is no caller, carrier capture, discovery, environment check, S-OP-5 field or release-registry content.
- The changed paths are exactly the eleven in the product map. One is the audited operability census row: `crates/host/src/configuration.rs` gains six lexical `from(` calls (five `BTreeMap::from`, one `i128::from`), none a mint. Is that row exact and justified?

## Output

`review.json` must carry:
- `verdict` (`ACCEPT-UNIT` or `REQUIRED-FINDINGS`);
- `requiredFindings`;
- `nonBlockingObservations`;
- these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "a8037278b4849d2d888325eeebd54054bab0a5f15091fe88331c2cc944b64532",
  "implementsPlanR2": true,
  "pipelineOrderAsItem4": true,
  "layerKindChoosesRow": true,
  "digestRecipeAsItem6": true,
  "pcmVectorsReproduced": true,
  "perLayerAllowlistAsItem2": true,
  "ciLocalNeverParsed": true,
  "x12OrderAsItem10": true,
  "s9RemedyRepinned": true,
  "generatedRegistriesDriftChecked": true,
  "hostTestFailureSetEqualsBase": true,
  "allTargetsClippyWarningsDenied": true,
  "mutationsCaught": 8,
  "pure": true,
  "inventoryUnchanged": 187,
  "contractSuccessorsUnchanged": 162,
  "productionCallerAdded": false,
  "newPublicCode": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead gives its own assent, then publishes the package (architecture), then makes the product code commit. The inventory successor v188 is prepared and reviewed separately. Nothing is pushed.

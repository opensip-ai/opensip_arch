All work is complete and both inputs still verify. Here is the delivery.

---

# Author remint on the merged native reference bytes

**Standing:** author-assisted reference construction. Not independent reconstruction, not blind acceptance, not application acceptance, not product qualification. **Do not supply these examples or oracles to a blind consumer.** The original 123/8/3 charter remains independent and pending.

**Bound to exactly these bytes.** `source-manifest.json` sha256 `29ea3a6ee8c5bfce710816c4f6a818ef9e18a7dc6bf9b8efd944eb3e6b4e4493` (12880 files), `package-manifest.json` sha256 `54af1f7bc1fb211e3da9331261f9364b77d24a07df5a0cba31803410243a625e` (118 files). **Registered native schema digest: `673a9bf8b3d1d0d3643d0fdd75813a6fa14d362d792e90d0ddd5f63e16a6bbe2`.** Both manifests verified before work and again after: **12880/12880** and **118/118**, zero mismatched, zero missing, zero extra on disk. The merged source is an intermediate integration input, not candidate26; nothing here carries to future changed bytes.

**Delivery:** `scratch/artifact-manifest.json` sha256 `b4f90d217d30085c77bacbe57429d3acc9ff60144216dce73101f372ac235cfc`, 189 artifacts, plus `scratch/COMMANDS.md`.

## 1. Portable construction path

The four construction entry points now take declared arguments — `--source`, `--package`, `--out`, optional `--helpers` and `--kit` — and resolve the three historical dependencies: the `ROOT/output` helpers path becomes the **bundled** `author-helpers/` loaded under the name `helpers`; the sibling `candidate-subject.v25` foundation becomes `--source`; and the missing `check-blind13-exported-graphs.v4.py` becomes the **bundled** `check-export.v4.py`, whose `decode_store(raw, M, notes)` is the same transport entry. `build-semantic-controls.py` additionally takes a required `--positive`, so the negatives are provably derived from a freshly reminted positive rather than a stale one.

The generator asserts the transform is minimal: **123, 137, 6 and 25 construction lines carried, zero dropped** — the only removed line is the one deliberately replaced (`src=ROOT/'checkpoint3'`).

**A fourth blocker existed that the package README did not name**, and it is the one that actually prevented reminting. Ten hardcoded historical constants live in the *helpers themselves*, read at import time:

| constant | modules |
|---|---|
| `KIT = /tmp/.../consumer-b.v13/subject` | builder, cap_admit, kit_schemas, law_admit, protocol3, runs, schema_admit |
| `OUT = /tmp/.../codex-author-followup.v1/output` | runs (dead), status |
| `REQS = /tmp/.../consumer-b.v13/requirements.json` | status |

`builder.py:20` derives `NAT_DIGEST` from `KIT/...native-evidence.schemas.v2.json`, so construction silently bound to the **old** schema. Minimal correction, one line per constant: each becomes environment-resolvable with its historical value as the default, so unset behaviour is byte-identical. Of the 12 kit documents the helpers read, all 12 exist under `--source` and **exactly one differs** — the native schema, precisely the document that moved. 15 helper modules are left byte-identical.

Recorded, reproducible intermediate failure:

```
--kit <historical>   -> PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT:native/native-evidence.schemas.v2.json,  0 of 4 built
--kit <merged source>-> 4 of 4 built
```

I also merged the `_default_unit_binding` naming fix from completed root-binding v1 (`987bade0…` → `7801111a…`), which touches only `ts_pilot.py` and therefore does not overwrite root's `runs.py` F-11 change — I verified that change is intact (`compare_proof(proof, proof)` replaced by `constructionProofSource`). Root's four portable probes and strengthened F-08 are preserved and exercised, not re-authored.

## 2. All seven positives + three negatives reminted, freshly derived

Every identity is derived from the changed bytes; no serialized id was search/replaced. The TS runId moved `541765b2…` → `b43717f0…`, confirming the remint took.

| group | run | owner | semantic | new digest | old digest |
|---|---|---|---|---|---|
| checkpoint3 | `author-ts` `b43717f0…` | ADMIT | **ADMIT** | ✅ | ✗ |
| normalized-examples6 | `rust` `4508ff27…`, `rust-partial` `aeb12002…`, `syntax-code` `5578a270…`, `syntax-data` `63f200c2…` | ADMIT | **ADMIT** | ✅ | ✗ |
| rust-selection-examples1 | `rust-bin` `d348e03b…`, `rust-lib-only` `7255bcc0…` | ADMIT | **ADMIT** | ✅ | ✗ |
| semantic-controls1 | `severity` `5a96f88c…`, `unrelated-scope` `6b9966e3…`, `collapsed-deficiencies` `092012e9…` | **ADMIT** | **REFUSE** | ✅ | ✗ |

Every store carries the new digest and none carries the old one. The three negatives start from the freshly reminted positive and reach the intended boundary after structural ADMIT — and I checked they refuse for the *intended* reason, not merely the same code:

- `severity` → differs only at `proof.findingIds` / `proof.ruleResults[0].findingIds`
- `unrelated-scope` → differs only at `proof.predicateProofs[0].scopeIds` (claimed 2, recomputed 1)
- `collapsed-deficiencies` → differs only at `proof.executionDeficiencies` (claimed 1 bundled, recomputed 2 separate)

Old exports and reports in the input package are untouched; all new output is under `scratch/`.

## 3. Probes re-run over the new exports

All four pass against a package-layout view of the fresh exports: **properties** (lib≠bin body identity, lib==lib-only, partial indeterminate with 0 clone facts — now carrying root's F-08 fields `sourceUnitOwnershipId`, `selectedUnitIds`, `selectedUnits`, `measuredBodyOwner`), **query 7/7**, **query assessment**, and **mixed-universe** (unmerged ADMIT; merged REFUSE `EXECUTION_INPUTS_COVERAGE_DERIVE`) — the §5 boundary holds on the merged source. Per-Run full replay reports are retained under `evidence/replay-a/owner-<group>/report.json`.

**Evidence weighting preserved and re-stated:** checkpoint3 is author-helper composition *independently compared* with the frozen owner (two-implementation agreement); the other six have the frozen owner derive *and* replay the proof — self-consistency and determinism, **not** two-implementation agreement; the three negatives derive from checkpoint3.

**Limitations re-measured on the new exports, not asserted:** operations across the seven positives are `exists` ×6 and `none` ×1. **No `and`/`or`/`not` anywhere** — the combinator limitation holds. `count-at-most` and `all-covered` are routed to the atom evaluator but remain unimplemented (`NotImplementedError`). I did not build or validate them; not requested.

## 4. F-05 / F-06 reminted, and the two-binding question answered honestly

| control | runId | structural | semantic |
|---|---|---|---|
| `ts-lawful-default` | `b43717f0…` (reproduces checkpoint3 exactly) | ADMIT | **ADMIT** |
| **F-05** `ts-invalid-default-entry` | `eb375144…` | **ADMIT** | **REFUSE — `EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY`** |
| **F-06** `ts-lawful-explicit-selection` | `1731a7b5…` | ADMIT | **ADMIT** |

**The two-binding cell: I could not build it, and I did not manufacture agreement.** I injected a genuine second binding at construction time (not a serialized edit) and recorded the exact ordered obligations the owner raised:

1. `ENUMERATION_BINDING_DUPLICATE_UNIVERSE` + `ENUMERATION_INVENTORY_MISSING_RECORD` — two available bindings in one cell must name **distinct** universes, and subject inventories are keyed by `(cellOrdinal, programOrdinal)`; the pilot mints them only at ordinal 0. (structural ADMIT, run `382ccea6…`)
2. Giving the second binding a distinct universe by editing a synthetic field then refused earlier, at `open_run_closure`: `NATIVE_UNIVERSE_BINDING:native.universe-path-not-inventoried:src/util.ts` — a distinct universe's `programRootFiles` must be **inventoried snapshot paths**, and the TS pilot inventories exactly one TypeScript source. (run `6fca6c0a…`)

Not reached because blocked earlier: the per-`(cell, program)` cellOutcome, and — under the §5 per-universe rule — coverage accounts whose `coverageIds` equal the complete matching returned partitions at the second universe, carried by views minted at that universe.

So the blocker is **constructive, not contradictory**: a second binding is a second *program* needing its own inventoried config/source bytes, its own inventories, and its own per-universe cell-bound coverage. **No owner defect is demonstrated** — every refusal is the owner correctly enforcing a published obligation against an incomplete construction, and nothing was normalized away in the constructor to make it pass. The shipped F-06 control is a single binding of non-default provenance and is never described as two.

## 5. Portability proved from a different arbitrary path

Re-ran the whole pipeline into `scratch/portability-proof/run-from-an-arbitrary-other-path/deep/nested`: **21 artifacts byte-identical**, identical runIds for all ten Runs plus the three binding controls, and full replay reproduced group-for-group. `construction-provenance.json` beside every output records source, package, helpers, kit, out and both schema digests.

## Findings and limitations

- The README's "four construction entry points remain historical, nonportable" understated the problem: the **helpers** carried the historical kit, and that — not the entry-point headers — is what bound construction to the old schema. Construction is now reproducible from declared inputs; that README limitation can be retired **only** if the helper overlay is merged with the entry points.
- The helper overlay is **required** for the remint, not optional. Without it the historical kit default silently rebinds to old schema bytes.
- No new semantic owner defect was found. The one suspicious observation — checkpoint3 initially reproducing its old runId — resolved to the kit binding, not an owner issue, and is recorded with its reproduction.
- `runs.OUT` is a dead constant and `status.py` is not on the construction path; I made both declarable for uniformity rather than leaving a hidden historical write target.

## Not claimed

No candidate26 acceptance, no application acceptance, no product qualification, no implementation, no commit or push. These are author oracles and must not reach a blind consumer. Fresh new-byte independent review remains required, and the original 123 requirements + 8 standing constraints + 3 future items remain independent and pending.

# Current-source reconciliation — proposed application map

This map becomes effective only with reviewed D-372 application. It preserves
historical source bytes and their actual acceptance standing. The product
contract index is the intended single current account; this is an audit map,
not another product design or readiness checklist.

| Historical/current source | Potentially misleading selector | Prospective current account |
|---|---|---|
| `docs/coop/architecture/01-product-boundary.md` | SEALED Windows support and Rust V1 spine | D-371 bounded product scope; product native/security contracts select macOS/Linux ARM/x64, common Rust host/pure evaluator and native TS/JS/Rust roles. Windows is not selected. |
| `docs/coop/architecture/08-surfaces-and-topology.md` | Historical command surface | Product workflow command inventory and output schemas, including invocation composition. |
| `docs/MAP-VS-CONTROL.md` | Older Map/Control command grammar | Product workflow advisory boundary and command inventory. Model output remains advisory; no bundled model/full Map application is required. |
| `docs/coop/completion/reference-architecture.v2.md` | Preview analyze/doctor/help-only command set | Frozen D-369 historical preview; no restriction on the prospectively selected full-product commands. |
| `docs/coop/IMPLEMENTATION-FREEZE.md` §7.1 | Claim that Run/Evidence bottom out only in unproduced capabilityManifestId | Applied DELIVERY v4 already supplies CAP-MANIFEST-ID-V1. Product identity contract supplies Plan/source/fact/view/proof/evidence/seal/Run and all producing/custody joins; no merely conceptual Run is elevated by a vector. |
| `docs/coop/IMPLEMENTER-BLUEPRINT.md` §5.1 correction | Applied capability and policy derivation recipes vs stale paragraphs | Preserve actual applied standing. Current evaluator outputs use explicit major-three domains; unchanged native and input identities retain major two; the retained capability manifest recipe remains its existing typed bare-hex recipe and committed CVE1 bytes. |
| `docs/coop/architecture/06-evidence-and-persistence.md` | Defaultless/ephemeral retention prose | Binding CD-RT-5 durable-unbounded default, DEFAULTED provenance and explicit first-use writes; identity/evidence contract joins actual custody, D9 and purge. |
| `docs/coop/artifacts/evidence.v15.json` and retention v28 | Applied head but missing Phase-1A/checker standing | Product identity/evidence is the prospective owning successor; old checker acceptance is not inferred. New schemas/reference checks and independent review must be named in D-372. |
| `docs/coop/artifacts/evaluation-proof.v8.json` and v13 | Distinct unapplied claim/provenance lineages and old observed-window checker escapes | Product identity/evidence proof and authenticated trusted evaluator boundary; every historical residual/observation/escape receives its own proposed disposition. Neither old candidate is retroactively applied. |
| `docs/coop/artifacts/fact-plane.v1.json` | Examined-set completeness mistaken for resolution completeness | Native Coverage3 and explicit unresolved-edge/closed-world sufficiency, with product FactRecord2 binding source2 and registered payload schemas. |
| `docs/coop/artifacts/versioning-policy.v8.json` | Prior-detector pivot supplied by fact dual emission | Workflow retained/bundled runnable executable closure, portable baseline custody and typed comparison axes. |
| `docs/coop/completion/architecture-application.v1.json` | `observedSha256` authoring annotations vs actual pins | Frozen application remains governed by its actual acceptance pins. Current source inventories are separate; no annotation rewrite is used to fabricate old custody. |
| `docs/coop/completion/security-completion.v8.md` | Duplicate numbered headings 10–12 | Review selectors use exact paths/heading text/content hashes, never ambiguous section number alone. Product security successor uses its own unambiguous contract sections. |
| `docs/v2/architecture/08-decision-and-readiness-register.md` | Historical scoped grades and current broader in-progress target | Central register remains sole readiness checklist. D-372 may update grades only with per-obligation accepted evidence and exact current applicability; reference counts alone do not satisfy conditions. |

Delivery-stage profiles are subsets of one intended-product contract set. A
stage lacking a capability must report typed absence and preserve state/trust
continuity under the designed bridge. Future implementation work has to satisfy
these contracts, even when scheduled after the first delivery. Product release
qualification remains separate from design acceptance and implementation
authorization.

## Current evaluator profile selection

Product identity §4 incorporates the enumeration, atom, execution-input,
composition and fault contracts as one intended design. The selected owner is
`foundation/identity-schemas.v3.json` / `identity-model.v3.py`. Full public Run
admission is complete replay. The historical profile2 owner and its original
checks remain evidence of their narrower native/identity joins.

The workflow owner is `workflows/schemas/evaluator3/` with
`workflows/command-inventory.v3.json`, JSON/CommandEnvelope major3, and the
explicit SARIF adapter profile. Schema filenames and output record majors are
separate axes; unchanged policy2, import2 and finding-key2 inputs keep their
recipes. Profile2 outputs cannot be relabelled as profile3 authority.

## Fallow constraint applicability in the full product

The historical borrow register's FUTURE/preview wording records D-370's original
application scope. D-371/D-372 select these contracts for the full intended product;
it is no longer a reason to omit their design. No upstream code is adopted.

| Constraint | Current contract and preserved boundary |
|---|---|
| FW-01 zero-config/recommend | Security project custody + native automatic units + Config2 resolver + workflow recommend; no implicit effects/config write. |
| FW-02 clones | Native exact/normalized/structural facts and near/cross-TSJS candidates; workflow external semantic-similarity observations are advisory, with no bundled model or semantic-equivalence/repair authority. |
| FW-03 native semantics | Native TS/JS/Rust capability matrix, sufficiency, unknown-edge and versioned wire contracts. |
| FW-04 richer evidence | Shared import2 registry, exact correspondence and observation scope; runtime/test/history do not become static Coverage or universal non-use. |
| FW-05 delta gate | Portable baseline, executable detector pivot, multiple comparison axes and separate audit gate participation. |
| FW-06 determinism | Exact canonical input/identity/proof/evidence/seal/Run, independent replay, immutable assurance and stable typed projections. |
| FW-07 coherent workflow | Host invocation, bounded step DAG, fresh attempts, derivation DAG and common failure/storage/output behavior. |
| FW-08 omissions | Native Coverage3 examined versus resolution completeness; output required/optional omissions and unavailable/operational-fault distinction. |
| FW-09 candidate→inspect→review | Workflow closed advisory artifacts and exact Control citations, stale/unknown-reference refusal. |
| FW-10 repair evidence | Recipe-specific closed-world/proof/current-trust requirements, separate apply consent, guarded journals/recovery and fresh verification. |
| FW-11 weakened safeguards/metric redistribution | Architecture13 §6 restrictions remain binding; workflow comparison separates policy/waiver/scope/evidence changes and advisory observations. Counts require equal metric definition, scope and comparison base; redistribution is not behavioral improvement. |
| FW-12 bounded review | Workflow brief schema, explicit truncation and membership, no claim of complete review or prose verification. |
| FW-13 common registry | Workflow command inventory plus authenticated capability/schema/closure declarations; generated or drift-checked projections and typed refusal of unknown records. |
| FW-14 real configuration corpus | DR-G13/G16 implementation harnesses must add consented or public pinned repository shapes, reproducible workarounds, manual-correction counts and positive/negative fixtures. No private-repository telemetry or implicit collection. Synthetic design cases are not that corpus. |
| FW-15 policy authoring/test | Closed declarative DSL, effective-policy preview, deterministic positive/negative test suites; direct-call evidence is not a transitive effect proof. |

The foundation `g13-result-schema.v5.json` remains the explicitly named `harness.DR-G13.typescript-quality.preview` historical qualification adapter. Its platform display aliases are labels within that old corpus, not machine platform IDs accepted by product grants/profiles. The product native matrix and security S8 use the four canonical machine IDs. Historical preview evidence never qualifies native product cells.


Explicit full-product re-entry selectors: admission-and-qualification §5 dispositions every one of file02's seven P-1/P-2/G3 boundary items; security S16 dispositions file05's prototype migration preservation5/distinctions5/prohibitions6; D372's output re-entry act supersedes the scoped D077 SARIF drop/D086 inapplicability and reactivates G17 for exactly the inventory's four SARIF commands. Historical grades and measurements are not extended. The final applied readiness/gate maps must name these selectors and exact independent review rather than using delivery-stage deferral or an old SATISFIED label.

## Graph-query clarification from the HydraDB proposals

The proposal documents in `docs/coop/hydradb-review/` remain research input;
their older source hashes do not select current contracts. The current graph
query owner is `workflows/query-projection-contract.v3.md` and the major-three
`workflows/schemas/evaluator3/graph-query.schema.json`, incorporated by product
workflows §8. Endpoint/result identity, deterministic traversal, exact retained
pagination and separate traversal/evidence disclosures are design requirements.
The existing GX-01/GX-02 accelerator and index lifecycle boundaries remain in
force. No HydraDB dependency, alternative evidence authority or performance
claim is introduced. `hydradb-dispositions.proposed.md` accounts for all eight
proposals. Fresh successor review and application still precede effectiveness.

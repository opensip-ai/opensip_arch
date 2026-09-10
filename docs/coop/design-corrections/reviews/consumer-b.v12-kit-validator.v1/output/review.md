# Pilot review: syntax-code Run export and closure/replay

**Outcome: `PILOT_REFUSED`**

This is a fresh kit-only reconstruction validator. It is not the root admission oracle, not product qualification, and not implementation authorization. The outcome is scoped to the first claimed syntax-code complete Run export and its closure/replay implementation. Other TypeScript/Rust snapshot files were not graded. This is not a whole-design verdict and not whole-consumer acceptance.

`newMustIssues` and `newShouldIssues` are empty because every reconstructed refusal cites an **existing published law** the consumer graph or replay helper did not implement or satisfy. A missing existing-law implementation is a consumer correction, not a design gap. No absent or contradictory normative selector blocked reconstruction of the joins this pilot required.

## Standing and custody

- Validator origin: `consumer-b.v12-kit-validator.v1` (fresh session, no subagents, no web, no author oracle).
- Design inputs: `/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject` only.
- Consumer bytes: read-only interim snapshot at `consumer-snapshot/` (not an acceptance claim).
- Output confined to this validator’s `output/` directory.

### Manifest verification

| Object | SHA-256 | Bytes | Result |
|---|---|---|---|
| `subject/consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | 16469 | matches expected |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | — | matches expected |
| 80 subject files | as listed in the manifest | — | **PASS** 80/80, 0 missing, 0 extra |
| `snapshot-manifest.json` | `824aea890b86ae9d71b914646f1e91bf07e73f590938cf29d8089f65426f27be` | 5962 | 37/37 **PASS**, 0 extra |
| `runs/syntax-code.store.json` | `8b0f6d826ed04f604ce8614e63b55e9666a9abdd48702f6b155c92c4ce54e654` | 862544 | hashed independently |
| `runs/syntax-code.meta.json` | `524c82004b6df9141305ab3c9f483a7e84144266d6b54d0cbb25d8722b4c4d5d` | 3917 | hashed independently |
| `runs/syntax-code.closure.json` | `c042cd7f3b7a890059b7dbc297722727b73fa0c94b41f29a10804af03ced1edf` | 2166 | hashed independently |
| `runs/syntax-code.replay.json` | `adb4010d79336ff4a05da19bae42893241b58d83e6a12d1603b8c377161b2abd` | 527 | hashed independently |

Claimed Run: `run3:aa19beddb09888f33cc29eb127574259331922655122840e74293ff0c1704835`. Claimed closure `ok: true`. Claimed replay `proofCompareEqual: true`, tamper `refused: true`. Those claims are not admission.

## First actual refusal

After H-frame parse (pass) and identity-record stock plus `x-opensip-order` schema (pass), identity-and-evidence §3 requires Run closure to **re-run native context admission over retained bytes**. native-evidence §1.2 requires every grammar definition, the bundle manifest, and the normalizer specification to be present in the retained `kind=grammar` closure tree.

**Observed:** the grammar closure tree contains two paths (`bin/grammar` stub and `grammars/rust.bin`). `grammarBundle.bundleDigest` and `normalizer.specificationDigest` are present as store blobs and rehash, but they are **not members of `closure.tree`**.

- Selector: `docs/v2/contracts/product-v1/native-evidence.md` §1.2; `docs/v2/contracts/product-v1/identity-and-evidence.md` §3 (native context admission, `admit_native_context`); `identity-schemas.v3.json` `x-opensip-digest-domains.domainSets` `native.context.syntax.v2` `closureJoins`.
- Probe: `grammar-artifacts-in-closure-tree`.
- Missing tree members: `04e13aeb0de3a28599d7085eab8988a84d70322c39988db1274e7bf0ce1a7a93`, `8fe22043ebe7e18a9c27b7a288f71b1010b024f040284d0eafab8659f8dd9d91`.

This is the first actual refusal in reconstructed close-run order. Later independent static omissions on the same export are listed below; they are not hypothesized.

The original probe run recorded `installed-bundle-seven-languages` as script-order first failure. That ordering was a **validator diagnostic defect** (see corrections). native-evidence §1.2 states that the product **host** bundles seven languages; `SyntaxGrammarBundleV1.grammars` is `minItems` 1 with a closed seven-member `languageId` enum. No reconstructed admission selector refuses a non-empty subset grammar component. That probe is preserved as originally failed and reclassified as a further static observation, not the first actual refusal.

## Further independent static omissions

These were executed on the same export after the first refusal. They are consumer corrections against existing laws.

### 1. Declares payload is not SubjectIdV1

`relation-payload-schemas.v2.json#/$defs/DeclaresPayloadV1` requires `container` and `declared` to be `SubjectIdV1`: lowercase ASCII namespace, colon, opaque identity (`^[a-z][a-z0-9-]*:[^…]`). Observed payload is `{"path-like": "hello.rs", "declared": "add"}` — actually `container="hello.rs"`, `declared="add"`. Stock JSON Schema refuses both fields.

The consumer’s `schemaChecks` validated `FilePayloadV1` and `ClonesPayloadV1` and never validated `DeclaresPayloadV1`. A stock pass on the enclosing `fact2` envelope is not payload-registry admission.

### 2. Clones body-identity frames are not retained

identity-and-evidence §3: the framed preimage is retained under the 64-hex suffix so closure can fetch, re-hash, parse, and join components. L1–L3 additionally require exact retained preimage custody even when the host cannot recompute tokenisation.

| Level | Claimed `bodyIdentity` | Frame retained under suffix |
|---|---|---|
| L0-verbatim | `sha256:72a35a8b39ca25929a4b2f0be6ef1288ebca9192fd04ad7cce37acd372390b36` | **no** |
| L1-lexical | `sha256:874cf4bd66165db89dd7b65b2c8d5caf6bf53edaa3ca5868a9b2d1da55190426` | **no** |

Independently, the L0 **recipe** was rebuilt from the retained syntax context (`parserName`, `parserVersion`, `bundleDigest`) and dialect `grammarVariant=rs` selected from the `.rs` suffix, using the published double length-prefix (`payload_len == raw_byte_len + 4`). That recomputed identity **equals** the claimed L0 identity. Recipe match is not frame retention. The consumer’s own `clones-L0-recomputed-from-anchor-bytes` join remints from builder memory and does not fetch a retained frame.

### 3. Invented syntax-only unit

native-evidence §1.2: a file on the compiler-free path is `syntax-only` membership with `unitOrdinal: null` under U-4, **not a member of an invented unit**. Observed `UnitMembershipV1`: one unit `{unitKind: syntax-only, unitOrdinal: 0, markerPath: hello.rs}` and a membership row with `unitOrdinal: 0`.

### 4. Missing enumeration inventories

enumeration-contract.v1.md §4: exactly one `SubjectInventoryV1` per `(cellOrdinal, programOrdinal, kind)` in `cell.kinds`. execution-inputs-contract.v1.md §4: inventory digests are exactly one per kind.

| Expected | Present |
|---|---|
| `(0,0,file)` clones-fact | missing |
| `(1,0,file)` inventory | present |
| `(1,0,package)` inventory | missing (empty package extent would still require a complete-empty record) |
| `(2,0,symbol)` syntax | missing (zero declaration rows are lawful only as a retained complete symbol inventory) |

Cell outcome `[1]` has one digest for kinds `{file, package}`. Cell outcome `[2]` has zero digests for kinds `{symbol}`.

### 5. Complete proof is not recomputed from the export

identity-and-evidence §4 and evaluator-composition-contract.v3.md §7: after admission, independently reconstruct every subject, enumeration, predicate, witness, finding, waiver, rule result and verdict from retained selected inputs; compare **C of the complete proof** and referenced preimages. Equal verdicts are insufficient. No caller-authored pass/fail substitutes.

Observed:

- `scripts/replay_from_export.py` reloads the run/seal/proof frames, recomputes `run` H, and **prints the saved `proof["verdict"]`**. It does not walk the predicate, derive findings, or compare C of a recomputed complete proof.
- `scripts/pilot_syntax_run.py` calls `walk_predicate` on **in-memory builder objects**, then sets `proofCompareEqual` to `C(parsed frame) == C(builder proof)` (reminted self-equality).
- `derivedVerdict` is the caller mapping `"pass" if tree2["value"] == "false" else "fail"`, not composition over findings/gates/deficiencies.
- `join("proof-canonical-retained", … or True)` is unconditionally true.

This validator independently evaluated the retained `none`/`file`/`hello.rs` atom (false on known match with complete Coverage) and derived composition core fields `{findingIds:[], verdict: pass, …}` equal to the retained subset. That is **not** complete-bundle admission. Byte-identical remint of `predicateProofs` / witnesses / `program-predicate.nodeDigest` from the export was **not reached**, because the consumer provided no fresh-process reconstruction of those nodes and saved proof fields were not used as an oracle.

### 6. Claimed tamper is not the comparison path

R-REPLAY-TAMPER: preserve identities and citation membership, change claimed logical result, replay refuses.

The consumer mutates `proof.verdict` `pass→fail`, keeps `predicateProofs`, and treats `C(tampered) != C(proof)` as `refused: true`. Independently, composition still derives `pass` from retained inputs, so a real comparison of recomputed complete proof versus the tampered claim **would** refuse. The consumer did not execute that path from the export. C inequality of a mutated verdict field is a stale-hash control, not semantic replay.

## Admitted boundaries (this export only)

These passed independent probes. They do not overcome the refusals above.

- All store blobs rehash. All H frames parse. `run3` and `proof3` identities recompute.
- `file@enumerated` inventoried-file joins: path, digest, length, retained bytes.
- Anchor cardinalities: file 0, clones 1, declares ≥1.
- File coverage totality over inventoried `hello.rs`; per-view subject-scope partition disjointness.
- `capabilityManifestId` derived from retained CVE1 bytes under `opensip.capability-manifest.v1`.
- Syntax universe binds the Plan-selected syntax context; `resolutionAttempted=false`; no compiler universe/context frames; snapshot has no `tsconfig.json` / `Cargo.toml` / `package.json`.
- `parserVersion` equals the grammar closure `semanticVersion`.
- RuleProgramV2 is the published projection of the Plan policy.
- Graph is acyclic: proof names neither evidence nor Run.
- Output majors are profile 3; native/input records remain major 2.
- PolicyDocumentV2 stock-validates once the workflow `$id` registry is attached (see diagnostic correction D-CORR-1).

## Diagnostic corrections (validator’s own)

Original failed probes are preserved in `diagnostics/syntax_code_pilot_probes.json` (132 probes, 119 pass, 13 fail).

| ID | Original | Correction |
|---|---|---|
| D-CORR-1 | `schema-policy` FAIL unresolvable `CanonicalIdentifier` | Validator omitted the workflow common/imported-evidence `$id` registry. Re-ran with those documents registered: **PASS**. Not a consumer-graph repair. |
| D-CORR-2 | `installed-bundle-seven-languages` recorded as firstRefusal | Reclassified to further static observation. Schema `minItems` 1; no reconstructed MUST that a synthetic grammar component contain all seven host languages. |
| D-CORR-3 | L0 recompute skipped in the original script when the frame was absent | Independently rebuilt L0 identity from derived `languageVersionBinding`; equals claimed `sha256:72a35a8b…`. Frame still unretained. |

## Four boundaries kept distinct

| Boundary | This pilot |
|---|---|
| Stock schema | Several identity records pass Draft 2020-12 plus independently implemented `x-opensip-order`. Declares payload fails its registered selector. Consumer `stockOk` checks are not closure. |
| Helper | Consumer C/H/lexical were audited against identity-and-evidence §3 and not used as an expected-output oracle. `eval_atom` occupancy `pass` is a helper defect hidden by this single-file filter. |
| Closure | Native context tree join, body-identity frame retention, U-4 membership, enumeration inventories, and relation payload selector were executed from published registries. They refuse. |
| Host enforcement | Not claimed. Synthetic trusted observations only. |

## Counterfactual boundaries

- If the grammar closure tree listed the retained bundle and level-specification blobs, later independently observed faults (DeclaresPayloadV1, unretained body frames, invented unit, missing inventories, incomplete replay) would still refuse this export. Those are not hypothesized.
- Real compiler, OS, crypto, SQLite, and host authentication were not demanded and their absence is not a design gap (`F-OS-COMPILER-CRYPTO-SQLITE`). Tamper control is evaluator replay, not host authentication (`F-AUTH-HOST`).

## Reproduction

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_probes.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_corrections.py
```

C/H/lexical in the probe script are taken from identity-and-evidence §3. Store transport is exact base64 plus SHA-256 rehash. Consumer builders and evaluator are not expected-output oracles.

## Read scope

Five contract owners, plus the current-source map as a scope/audit map (not a recipe): identity-and-evidence, security-and-lifecycle, native-evidence, workflows-and-surfaces, admission-and-qualification.

Incorporated for this exact pilot: `identity-schemas.v3.json`, `native-evidence.schemas.v2.json`, `relation-payload-schemas.v2.json`, atom/composition/enumeration/execution-input contracts and schemas, `fact-identity-policy.v2.json` (named body recipe), `capability-manifest-domains.v2.json`, `native-capability-matrix.v2.json`, PolicyDocumentV2 plus workflow common/imported-evidence `$id` registry, CVE1 from `resolved-inputs.v2.json#planIdContract.canonicalValueEncoding`.

Consumer snapshot inspected: syntax-code meta/store/closure/replay, `pilot_syntax_run.py`, `replay_from_export.py`, and helper modules named in `review.json`.

Not read: the repository; author models/code/cases/fixtures/goldens/reports; prior reviews; root admission reports; other `/tmp/opensip-design-corrections` directories; the original active consumer output; other sessions.

A later same-origin continuation may review newly frozen consumer bytes.

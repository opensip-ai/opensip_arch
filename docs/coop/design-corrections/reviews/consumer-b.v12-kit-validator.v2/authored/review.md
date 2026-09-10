# Pilot recheck: corrected syntax-code Run

**Outcome: `PILOT_ADMITS`**

Same-session continuation of the v1 kit-only validator. Not a new origin, not the root admission oracle, not product qualification, and **not whole-consumer ACCEPT**. Historical `blind-review` / `requirement-status` in this snapshot are not reaffirmed. All **123** accept-blocking requirements remain for later completion.

The selected work is the **corrected** first syntax-code complete Run (new identities). Other TypeScript/Rust/syntax-data exports were not graded.

`newMustIssues` and `newShouldIssues` are empty: no new missing or contradictory design law was found. Previous v1 refusals were consumer missing-law implementations and are preserved below; they are not design gaps.

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | 80/80 PASS (unchanged kit) |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| v2 `snapshot-manifest.json` | `f0339fa8345a5c7ce929a6a7ccd54239469d9862ce7d7e76700ded7a4ba65511` | **147/147 PASS**, 0 extra |
| new `syntax-code.store.json` | `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` | 867956 bytes, 79 blobs |
| preserved original store | `8b0f6d826ed04f604ce8614e63b55e9666a9abdd48702f6b155c92c4ce54e654` | still present under `preserved-failures/` |

NEW Run `run3:f2542b3afb9c5042438370893f9932830b4b6b1ac17f16299d35ed55d49db918`, proof `proof3:59d3b68084ae4c16c0b09956f24f3923801a82d361d9de8b362659129987e785`. Snapshot source inventory / `hello.rs` bytes are unchanged; plan/context/universe/run/proof identities changed because closure tree, membership, inventories, declares payload, and body frames changed.

## Independent measurement (not the consumer oracle)

125 independent probes, **125 pass**, firstRefusal `null`. Complete expected proof C SHA-256 `e9492b0456f58e11a9edebaf43d8c37ce6d2386f9c560cbb9a426eb45f342863` equals the retained claim.

C/H/lexical came from this validator’s v1 diagnostics (identity-and-evidence §3). Consumer `compose_proof` / `evaluator` were **not** used as expected-output oracles. An isolated copy of the consumer replay script was run under `output/isolated/` (KIT → this validator’s v1 subject; OUT → isolated) as a **claim measurement only**; it agreed with the independent C compare (exit 0, same proof C, tamper refused). Agreement with a consumer helper is not admission; the independent reconstruction is.

Reproduction:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v2/output/diagnostics/v2_syntax_code_recheck.py
```

## Previous seven (and related) complaints — not the whole chain

v1 first actual refusal on the **old** export remains `grammar-artifacts-in-closure-tree`. Original failed probes are preserved at `diagnostics/preserved-v1/` (probe JSON SHA `2e238db56c4814c3710d128e2c128765685b5a3422251ca9efa14b022dcfd2fe`).

| v1 refused boundary | On the NEW export |
|---|---|
| grammar tree missing bundle/spec | **admitted** — tree contains `70b27c78…` (grammarDigest), `04e13aeb…` (bundleDigest), `8fe22043…` (specificationDigest), plus stub `37361351…`; members rehash |
| DeclaresPayloadV1 not SubjectIdV1 | **admitted** — `file:hello.rs` / `function:add` |
| L0/L1 body-identity frames unretained | **admitted** — frames retained; L0 preimage equals independently rebuilt languageVersionBinding bytes; L1 is custody without a tokenisation claim |
| invented syntax-only unit / unitOrdinal 0 | **admitted** — `units=[]`, `unitOrdinal=null`, `reason=grammar-only` |
| missing SubjectInventoryV1 locators | **admitted** — `(0,0,file)`, `(1,0,file)`, `(1,0,package)`, `(2,0,symbol)`; cell outcomes one digest per kind |
| replay printed saved verdict / reminted C self-equality | **admitted** — independent reconstruction from retained selected inputs equals complete claimed proof C |
| tamper was stale-hash only | **admitted** — logical-result mutation compared against independently reconstructed expected proof (`pass` vs claimed `fail`); citations preserved; stale-hash labelled separately |

D-CORR-1 (policy `$id` registry) and D-CORR-2 (seven-language host bundle) remain validator diagnostics, not consumer-graph repairs. D-CORR-3 L0 recipe still matches `sha256:72a35a8b…`; the frame is now retained.

## Complete applicable chain (beyond those complaints)

Stock schema plus independently implemented `x-opensip-order` passed on the checked records. **That is not admission.** Also independently executed:

- File inventoried-file snapshotJoins (path, digest, length, retained bytes); anchor cardinalities; file coverage totality; per-view partition disjointness; `subjectScopeCommitment` = `sha256:` + H(`scope2`).
- Only syntax native context/universe; universe binds Plan-selected context; `resolutionAttempted=false`; no compiler markers in the snapshot.
- `capabilityManifestId` derived from retained CVE1; RuleProgramV2 is the published projection of Plan policy.
- Recursive retention of `selectedRefs` (4 inventories, 3 Coverage, 1 view) plus execution-inputs / rule-program / policy on `evaluationInputRefs`. evidence Coverage set equals the view; imports empty on both Plan and evidence.
- Plan `semanticClosures` are retained `provider` + `grammar`; evaluator closure kind is `evaluator`. Grant `projectId` joins the Run.
- File subjects were derived from complete file inventories, **not** from claimed `selectedSubjectIds`. Atom occupancy is payload `path`. `none` of `file` `hello.rs` is **false** on a known match with complete Coverage (not vacuous true). emitWhen false → no finding → gating pass.
- Seal cites evidence and this proof; proof names neither evidence nor Run.

## Tamper vs structural refusal

The input graph was left identity-valid. Claimed `verdict` / first predicate `value` / rule `outcome` were mutated; `witnessDigest` and `evaluationInputRefs` were kept. Independently reconstructed expected proof remains `verdict=pass`. `C(expected) ≠ C(tampered)`. Tampered identity `proof3:b32c360da612191a007b98e0b332101afb36d7cae172ce3a3bf9e9b2d01c9e80`. `C(tampered) ≠ C(claimed)` is recorded as a stale-hash control and is **not** the admission control.

## Not reached

- Generic `x-opensip-digest` keyword engine over every 64-hex field.
- Full delivery.v4 / component-manifest-schemas.v11 security metadata profile of `closure.manifestDigest` (bytes retained and rehash only).
- Real compiler/OS/crypto/SQLite/host authentication.
- The rest of the 123-requirement charter (other language Runs, envelopes, traces, query vectors).

## Four boundaries

| Boundary | This recheck |
|---|---|
| Stock schema | Checked records pass Draft 2020-12 plus `x-opensip-order`. Not admission. |
| Helper | Consumer occupancy now skips non-matching file paths. Isolated consumer replay agreed with independent C; it was not the oracle. |
| Closure + replay | Grammar tree, body frames, U-4, inventories, DeclaresPayloadV1, file/Coverage/universe/program/execution/proof/seal joins, and complete proof C compare executed from published selectors. |
| Host enforcement | Not claimed. |

A later same-origin continuation may review remaining charter items or newly frozen bytes.

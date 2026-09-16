# consumer24 findings — native, identity, enumeration, execution-input and zero-configuration owners

**Standing: nonblind bounded assessment by a coauthor.** Origin `823bf66b-e92a-4789-ab81-63a1a9dc371d`.

This is **not** independent design acceptance, a blind continuation, a patch, product qualification or a readiness claim. Nothing was edited in source, live, pins, planning, suites or review grades. The consumer's exports and code were read only as diagnostics, never as an oracle.

**Records.**
- `review.json` (SHA-256 `aab1b8c6ff71ea94214230c3799cd4033586303db9541f85d19e28ff2c8f6b78`) is built from the retained receipts under `receipts/`.
- Probes: `probes/probe_items.py` (attempt 1) and `probes/probe_items_v2.py` (attempt 2, which corrects two probe defects). Both attempts are kept.
- Interpreter: `/tmp/opensip-architecture-review-env/bin/python -I -B`.

## Custody

| Input | SHA-256 | Verified |
|---|---|---|
| source37 manifest | `245ef613…6680` | matches; snapshot exact (12,900 files, 736,891,310 bytes) |
| source38 manifest | `2ddfa0db…e5c5` | matches; snapshot exact (12,904 files, 737,100,757 bytes); parent = source37 |
| consumer kit manifest | `e57ef3a7…c3c` | matches; 102 members hash-exact, none unlisted, all equal to source37 |

- **source37 → source38:** 41 files changed, 4 added, none removed.
- **Owner files my items use that changed in 38:** `native-evidence.md` (the host-finalizer pointer only), `security-and-lifecycle.md`, `identity-model.v3.py`, `evaluator_composition_model.v3.py`, the semantic fixture and `check-semantic-replay.v3.py`.
- **Unchanged in 38:** the native payload schema, identity schemas, enumeration/execution-input schemas and models, the native model and `discovery-defaults.py`.
- **Every probe section gives identical results on 37 and 38.** No assigned item was corrected between the two.
- **Where the hashes are:** per-file hashes for every owner file and every consumer file read are in `review.json#/custody`.

**Probe standings are kept separate:**
- **helper** — a direct call of an owner function;
- **schema** — validation against an owner selector;
- **closure** — actual `identity-model.v3.close_run`;
- **static** — exact source presence in a hashed file.

Only M2 and S1 use actual `close_run`.

## Dispositions

| Item | Consumer severity | Disposition | Confirmed severity |
|---|---|---|---|
| M1 | MUST | Real design gap (cross-owner composition) | MUST |
| M2 | MUST | Real design gap (wrong record in an identity annotation) plus a reference validator gap that hid it | MUST for a conforming literal reader |
| M3 | MUST | Real design gap plus an excluded normative input | MUST |
| S1 | SHOULD | Real design gap (unnamed registry) plus a missing validator | SHOULD |
| S2 | SHOULD | Real design gap (unnamed join), validator only partial | SHOULD |
| S3 | SHOULD | Real design gap (owners contradict) | SHOULD (possible MUST, see below) |
| S4 | SHOULD | Real design gap (identity-bearing field with no value law) | SHOULD |
| A1 | advisory | Confirmed | advisory (S4 is its identity-bearing case) |
| A2 | advisory | Confirmed, no semantic effect | advisory |
| A4 | advisory | Confirmed undecided | recommend SHOULD |
| A5 | advisory | Confirmed; consumer's choice diverges from the reference | recommend SHOULD |

**No item is a consumer helper error.** None is an intended semantic choice that the kit states.

## M1 — required clones census makes default TS/JS/syntax Runs permanently indeterminate

**How the owners compose** (probed at helper level with the actual owners):
1. **Default selection requests clones-fact.** It is requested, `required=true`, for every unit in all six modes (`required_default_capabilities`; native §1.4).
2. **The census is every file.** clones-fact's enumeration kind is `[file]`. The enumeration owner's own `host_file_extent` for a tsjs cell returns `LICENSE`, `README.md`, `assets/logo.svg`, `package.json`, `src/a.ts`, `src/b.ts` and `tsconfig.json`, per the file-kind law "not grammar-gated".
3. **Every expected subject must be covered.** execution-inputs §5 requires each expected source-path subject to belong to a returned partition, and a mix of complete and unknown is not complete. The owner's `expected_source_census` over a tsjs file inventory includes `package.json`, `tsconfig.json` and `README.md`.
4. **TS and syntax must disclose unreadable paths.** `scopeCapabilityLaw` applies to closed-suffix-table dialects and judges source-path scopes on **all** subjects. For TypeScript and syntax, any scope containing `package.json`, `tsconfig.json`, `README.md` or `data.json` must disclose `language-tier-unsupported`/`capability-missing`.
5. **Rust never gates.** The Rust dialect form has no table, so the same law answers "supported" for `Cargo.toml`, `README.md` and even `src/a.ts`.

**Consequence.** A tsjs unit always holds `tsconfig.json` or `package.json`, so its required clones account can never be complete and the Run can never seal pass. The same holds for a syntax scope containing any data document. Native §1.2's "no syntax Run is made blanket-indeterminate" is contradicted for mixed scopes. The Rust/TS asymmetry the consumer measured is the owner law, not a consumer error, and Rust clones scopes over non-Rust files claim `complete` with no gate.

**Remedy for root** (cross-owner):
- Either define a body-readable clones census per universe — TS dialect-table suffixes among program members, selected code grammars for syntax, owned `.rs` for Rust — or state that an honestly disclosed unsupported non-body partition answers a required clones account the way `unsupported-typed` does.
- Make the Rust branch symmetric with whichever rule is chosen.
- **Affected:** native-evidence.md §1.2/§1.4/§10; `enumeration-plan.schema.v1.json` (a registered payload schema document whose bytes reach PlanId, so a byte change is a successor); execution-inputs-contract §5; `scopeCapabilityLaw` prose; the enumeration, execution-inputs and native models and their cases.

**Limit.** No maintained reference Run seals a default-selected TS unit; the consumer's closed Runs corroborate but were not rerun.

## M2 — `program-predicate.nodeDigest` names the policy-1 `Predicate`

**What the annotation says.** The record is `workflows/schemas/policy-document.schema.json#/$defs/Predicate` (policy major 1), but the digested node lives in `RuleProgramV2`.

**Schema probe** (workflows owner's pinned local-registry validator):
- `endpoint:"source"` and `endpoint:"target"` atoms are **refused** by the v1 selector and **admitted** by the v2 selector.
- The same atom without `endpoint` is admitted by both.

**Why the reference hides it.**
- Actual `close_run` admits a Run whose program carries `endpoint:"source"` (run3 `cab50311…`; the admitted atom is exactly the probed one).
- `identity-model.v3.py` `digest_field` returns early for `retention: fragment` and never applies the named record.
- The node is validated only indirectly, through the retained `RuleProgramV2`, and its digest is recomputed by `PROGRAM_PREDICATE_NODE_DIGEST`.

Identity §3 defines `canonical-record` as a digest of a **named** registered record. A reader who honours the annotation therefore cannot close any Run using a v2-only atom field, which includes every incoming target atom.

**Remedy.**
- Change the record to `policy-document.v2.schema.json#/$defs/Predicate`.
- State in identity §3 that a fragment is validated under its named record, and make the reference do so.
- `identity-schemas.v3.json` is not itself a registered payload schema document (the v1 policy document is), so the annotation edit does not re-mint payload schema digests. Root should still confirm that no other identity hashes the bundle's bytes.

## M3 — `UnitMembershipV1` order and `unitOrdinal` assignment are unpublished

**What admits any order.**
- `units` and `rows` carry `x-opensip-order: sequence`, so any order is schema-valid, and `membershipDigest` reaches PlanId.
- Reversed rows, and reversed units with ordinals remapped, are both schema-valid with digests different from the reference (`35957105…` vs `848e8e3a…` / `46b955ff…`).

**Where the order actually lives.**
- No normative prose states it. Native U-1…U-4 define which units and rows exist, never their order.
- The reference native model sorts units by `(rootPath UTF-8 bytes, languageFamily)`, assigns `unitOrdinal` = position, and orders rows by path UTF-8 bytes.
- The consumer's cb24 choice is **byte-identical** to that, so the consumer's pick matches the reference; the gap is that nothing publishes it.

**Why the reference Run closure admits other orders.**
- The optional operational derivation lane of `admit_enumeration` would refuse a reorder.
- Run closure (`evaluator_input_model.v3.py`) calls `admit_enumeration` without `membership_derivation`, so closure never recomputes membership.

**The excluded input.** U-4a delegates the rules to `docs/coop/design-corrections/discovery-defaults.py`. That file is present in source37 but outside the kit, and it does **not** contain this order: the order is only in `native_evidence_model.v2.py`.
- **Decision:** including either Python file would make an executable reference the law and would still not publish the order.
- **A normative prose extraction is required:** unit order, `unitOrdinal`, row / `unsupportedFiles` / `outsideBoundaryFiles` / `memberPackageRoots` order, and the pruning and unit-enumeration rules U-4a now points to in Python.

**Remedy.**
- Add an ordering law to native §1.4 and replace U-4a's delegation with prose.
- Enforce the order where closure sees it: an order and contiguity check in enumeration admission at closure, with no schema-byte change. `native-evidence.schemas.v2.json` is a registered payload schema document, so an `x-opensip-order` change there belongs in a successor.
- **Affected:** native-evidence.md, enumeration-contract.v1.md, `enumeration_model.v1.py` / `evaluator_input_model.v3.py`, native cases.

## S1 — no registry of stage output schema documents

- **Identity law.** Identity §3 and `stage-spec.outputSchemaDigest` require "registered stage output schema document bytes". No such registry exists, and the annotation lacks `artifactClass` (which `view.schemaDigests` does carry).
- **Closure probe.** The reference's own maintained fixture seals a Run whose stage output schema is `$id urn:opensip:fixture:evaluator3-semantic-view` (digest `4f203895…`). That document is not in `registered_schema_documents()`, yet `close_run` admits it.
- **Consequence.** exec-plan2, seal3 and run3 can diverge for one Plan.
- **Remedy.** Publish a closed stage-output registry plus an `artifactClass` closure check, or reword "registered" to name the producer-interface document. Migrate the fixtures.

## S2 — clone level-specification join is unnamed

**What closure checks.** `body_identity_join` checks only that `normalisationVersion` is a retained blob equal to the frame's raw `levelVersion`. It never joins that value to `SyntaxGrammarBundleV1.normalizer.specificationDigest`.

**Why the partial check doesn't close the gap.**
- Native context admission does require the syntax normalizer specification to be in the grammar closure tree.
- That digest is singular, while fact-identity policy versions each level.
- TypeScript and Rust contexts have no normalizer record.
- So "the retained specification" is unnamed for every universe.

**Consequence.** A clones fact can name any retained blob as its level specification.

**Remedy.** Name a per-level specification record per universe and add the closure join. This touches `native-evidence.schemas.v2.json`, so it is a successor.

**Limit.** Static evidence only; no clones Run was built.

## S3 — zero-config syntax-only unit and scope

**What the owners say.**
- enumeration-contract §1 promises a default syntax-only unit per directory.
- The native mode table says syntax-only serves repositories with no TS or Rust unit.
- `WorkspaceUnitV2` can represent `unitKind: syntax-only` with `languageFamily: none`. A hand-built one validates, and default selection over it requests 10 capability rows.

**What discovery and selection actually do.**
- `discover_units` never emits a syntax-only unit.
- With no markers there are no units, and default selection requests **0** capabilities.
- The scope descriptor gets no workspace roots.
- An explicit `.` without a marker refuses with `native.explicit-root-without-marker` (CONFIG.INVALID).

**Severity note.** If an empty default request can seal a successful analysis, that is a silent narrowing and should be MUST. That depends on host and workflow owners outside this assignment.

**Remedy.** Mint a syntax-only unit when no TS/Rust unit exists, or correct enumeration-contract §1 and the mode table to say syntax-only is explicit-only.

## S4 — `NativeCoverageAccountV1.targetUniverse`

**The law.** The field is required, §5 deliberately does not join it, and no value law exists.

**Owner admission probe** (a fixture graph with two universes):
- Setting every account's `targetUniverse` to another admitted universe, to `null`, or to an unbound hex **admits**, and each changes `executionInputsDigest`.
- The same mutation of `sourceUniverse` refuses with `EXECUTION_INPUTS_COVERAGE_DERIVE`.

**Consequence.** executionInputsDigest, proof3, seal3 and run3 can diverge across hosts with no semantic difference.

**Remedy.** State the carried value and join it, or drop the field in a schema successor. `execution-inputs.schema.v1.json` is not in the payload registry.

## A1, A2, A4, A5

- **A1 — confirmed.**
  - `execution-inputs.schema.v1.json` has 16 unannotated bare-hex positions and `incoming-search.schema.v1.json` has 3. Neither declares a document digest law.
  - The closing law explicitly governs `identity-schemas.v3` (plus the native and relation extensions), and the reference walk passes these fields silently.
  - Advisory; S4 is its identity-bearing case.
- **A2 — confirmed, no semantic effect.**
  - `enumeration-plan.schema.v1.json` (including the `scopeDigest` record `document`) and `subject-inventory.schema.v1.json` name `identity-schemas.v2.json`.
  - The referenced defs `scope-descriptor`, `LogicalPath` and `Text`, and the language-mode keys, are canonically equal in v2 and v3.
  - `enumeration-plan.schema.v1.json` is a registered payload schema document, so retargeting belongs in a successor.
- **A4 — confirmed undecided; recommend SHOULD.**
  - Identity §3 defines snapshot2 over the sorted source inventory and says nothing about pruned trees.
  - Native U-4 admits pruned-tree files as `host-ignore-convention` rows when supplied, and an inventory without them is equally admissible.
  - U-4a and security S3 A-5 decide only that bytes actually *read* from a pruned tree enter the read set. Whether unread `node_modules` or `target` bytes enter the inventory is decided nowhere, and snapshot2 identity depends on it.
- **A5 — confirmed; recommend SHOULD.**
  - native-evidence.md defines what `allowJs` and `checkJs` mean, but not how `jsAdmittedToProgram` and `jsDiagnosticsEnabled` are derived.
  - The reference derives `jsAdmittedToProgram` = `allowJs` ∧ (at least one JS root) and `jsDiagnosticsEnabled` = `checkJs`.
  - The consumer's rule (`allowJs`; `allowJs` ∧ `checkJs`) diverges in **4 of 8** probed configurations. Whether their Runs reach those configurations was not checked.
  - The checkJs-without-allowJs case should be decided against pinned compiler semantics, not the model.

## Cross-owner notes for root

- **Identity-bearing bytes.** M1, M3, S2 and A2 remedies touch documents whose raw bytes carry identity (`enumeration-plan.schema.v1.json`, `native-evidence.schemas.v2.json`). Prose and admission corrections can land without byte changes; schema-byte changes are successors that re-mint identities.
- **M2 needs a validator change too.** The one-selector fix must come with a reference change that validates fragments under their named record, or the annotation stays unchecked.
- **S1 and S4 need no new vocabulary.** Each needs a named registry or value law plus the closure or admission check the reference lacks today.

## Failed probe attempts (kept)

- **M2, attempt 1.** Bare-document validation could not resolve `urn:opensip:product-v1:workflows:common`. That was a probe error; attempt 2 used the owner's registry validator.
- **S3, attempt 1.** The registry rows were not in canonical-set order, and the hand-built unit used `languageFamily: syntax`, which is outside the enum. Both were probe errors, corrected in attempt 2.

## Limits

- **Finite corpus.** Probes use small constructed inputs and the maintained semantic fixture; they make no claim over all repositories, universes or relation combinations.
- **Standings stay separate.** Helper, schema, closure and static results are not conflated. Closed Runs were used only for M2 and S1, and nothing was built end to end for M1, S2 or A4.
- **Consumer evidence.** The consumer's exported Runs were read as diagnostics for M1 and M2 only and not rerun; root validates them separately.
- **Separation.** The independent source38 review runtime was neither read nor influenced.
- **Standing.** No patch, no acceptance and no readiness claim.

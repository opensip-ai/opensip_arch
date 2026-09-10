# bv3-corrections-author.v2 — second correction pass handoff

**Standing.** Design/schema/reference correction only. Not product implementation,
commit, push, publication, readiness or product qualification. I am the
correction author, not the independent reviewer and not the blind consumer; I
confer no acceptance. Root's probes and the earlier independent/blind judgments
are literal evidence, not new acceptance. Codex has **not** assented to these
bytes; that assessment is still owed.

- `sourceRoot`: `/tmp/opensip-design-corrections/bv3-corrections-author.v2/work`
- `work` began byte-identical to released v1 (2981 files, 0 differences).
- **Aggregate delta vs frozen v12: 20 files changed, 0 added, 0 deleted** — root
  can integrate directly from v12 using `delta.changedFiles`.
- **This turn vs v1: 13 files.** Both lists, with hashes, are in `handoff.json`
  and `output/delta.json`.
- All pins and generated reports in the released work **equal frozen v12**
  (144 such files checked against the manifest file; 0 divergent).

## 0. The manifest — resolved

`fc124cc7…` is the **raw SHA-256 of the manifest file**
`root-input/candidate-subject.v12.json` (668000 bytes). Verified: computed hash
equals the declared value. The frozen subject then verifies against its 2981
rows with **0 missing, 0 hash mismatches, 0 byte-length mismatches, 0 extra
files**. My v1 treated it as an unreproducible aggregation and tried seven
variants; that was my error of assumption — it identified a file, not a tree.

## 1. CB3-MUST-3 — bundled grammars. **Was incomplete. Now complete.**

Root was right and I reproduced it on my own released bytes: `BUNDLED_GRAMMARS`
(`native_evidence_model.v2.py:2732-2734`) has **14 suffixes over seven
languages**, `assign_membership` routes them all to `membership: syntax-only,
reason: grammar-only`, and my v1 descriptor enum admitted only three — refusing
`json`, `toml`, `markdown`, `yaml`. My v1 handoff called the three-member
equality a positive drift check; as a *coverage* claim that was wrong, and I
withdraw it.

**The distinction root asked me to identify exists in the original contracts.**
§6.3 defines body spans as *function, method, closure/lambda, `impl` item and
block bodies*, publishes L2/L3 normalisation tables **only** for TS/JS and Rust,
and puts `languageId ∈ {typescript, javascript, rust}` in the clone preimage.
U-4 gives grammar-only files exactly one published role: membership. And the kit
publishes **no** tokenisation, `literalKind` mapping or normalisation law for
the four data/document formats anywhere.

**Correction.**
- A **closed, published per-language capability registry**
  (`native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry`)
  maps all seven languages to a `syntaxClass` and their capability set. It is
  **not caller-selected**: grammar-bundle admission reads the class from the
  registry and refuses a row declaring any other
  (`native.syntax-grammar-class-not-the-registered-one`), in both directions.
- `code` (ts/js/rust): clone body identity + code-construct syntax relations;
  `languageId` **must** be in the `body-language-version` enum.
- `data-document` (json/toml/markdown/yaml): grammar-only **members**, never
  `unsupported-file`, bearing `file`/`package`/`vcs-change` inventory evidence;
  they mint no body identity, no suffix of theirs is in the dialect table, and
  their `languageId` **must not** be in the body-language enum. A clone or
  code-construct request against them is explicitly unavailable — never a
  complete empty clone result, which would read as a finding of no clones.
- The drift check changed from "all bundled grammars == body-language enum" to
  "**the `code` subset** == body-language enum", plus registry/suffix/dialect
  coverage — so all seven are accounted instead of four being ignored.
- Suffix claims are checked against the host table
  (`native.syntax-grammar-suffix-not-bundled-for-language`). This caught a real
  fixture bug: my v1 bundle claimed `languageId: typescript` for the
  `.js/.jsx/.mjs/.cjs` suffixes the host routes to `javascript`.
- Explained for a fresh blind consumer in the matrix cells, matrix limitations,
  §1.2, the §6.3-based rationale and the normative registry — reconstructible
  without author code.

**Vectors.** Root's `probe-grammar-domain.py` on final bytes: all seven bundled
languages admit, `python` still refuses.

**The compiler-free positive, corrected for root's precision point.** Root was
right that pointing the ordinary builder at `README.md` does not make a
repository without compiler units — `build()` unions `TS_SOURCES` and
`RUST_SOURCES` into the snapshot and puts all three contexts in the Plan. A
bounded `pure_syntax=True` construction mode now builds a **grammar-only
repository**, and the Run asserts it: the Plan names **only**
`native.context.syntax.v2`, the snapshot has **no** `Cargo.toml`/`tsconfig.json`/
`package.json`/lockfile, every inventory member is a bundled-grammar file, and
the members are exactly the four data/document languages. The mixed-repository
inventory Runs are kept, separately labelled as the differently-scoped evidence
they are. A **code grammar without a compiler** separately produces real
`declares@syntactic` and `clones@normalized-body-hash` facts in that same
compiler-free shape. Unknown-grammar (`.py`) negatives are present.

**Flagged, not invented:** data-format syntax facts would need a published
tokenisation and `literalKind` law. I did not write one; it is recorded in the
registry and the matrix as a bounded future capability so nothing over-promises.

## 2. CB3-MUST-5 — clone ownership disclosure. **Was not closed. Now enforced.**

Reproduced exactly on my released bytes with root's probe. The concrete bypass
is `identity-model.py:816-820`: the prerequisite asked only
`coverage == 'complete'` and `deficiency is None`. It never asked *which*
deficiency and never read `nativeCause`, so `budget-exhausted`/null admitted
under partial ownership. **My v1 `NativeCause` additions were necessary but not
sufficient**, and calling M5 "corrected" was wrong.

**Correction.** `clone_ownership_disclosure` in the owning native unit derives
the owed `(deficiency, nativeCause)` from the **committed ownership record** and
**this scope's subjects**, in the selection law's order — absent ownership; then
`enumeration: partial`, decided before any row is read; then a subject whose
*selected* owners disagree on effective edition. Run closure re-derives it
independently and refuses a mismatch, so the claim cannot define its own
correctness. Four distinct refusals: `COVERAGE_DIALECT_PREREQUISITE`,
`…_UNDISCLOSED`, `COVERAGE_DIALECT_DEFICIENCY_MISMATCH`,
`COVERAGE_DIALECT_CAUSE_MISMATCH`.

Root's counterexample on final bytes: producer-control **admits** with the
derived pair; `input-closure-incomplete`/null → `CAUSE_MISMATCH`;
`budget-exhausted`/null → `DEFICIENCY_MISMATCH`; false-complete →
`PREREQUISITE`. Covered for **absent, partial and ambiguous selected**
ownership, each with legal-pair/null/wrong-cause/wrong-deficiency/false-complete
controls, plus **healthy** and **deliberately excluded** selections owing no
disclosure — that distinction is preserved explicitly, since a committed
exclusion is visible in the universe identity while unfinished enumeration is
not. `examinedExhaustive` versus `resolutionCompleteness.state` is asserted as
two different claims. Empty-view indeterminacy holds and no body identity is
fabricated.

**Stale prose corrected** as root asked: `sourceUnitOwnershipId.description` said
null was admissible *"only while the edition map has a single distinct value"* —
the withdrawn package-default fast path, contradicted by the retained
`selectionLaw` and by `body_language_version`. The **nullable form is retained**;
only the explanation changed.

## 3. Import cardinality — **root was right; my v1 reasoning was wrong. Adopted 0..4096.**

This is the point where I made a substantive error of inference, so I state it
plainly rather than as a refinement.

My v1 justified `minItems: 1` from "`adapterClosure` asserts an adapter ran over
the bytes `sourcePath` names". Checking the definitions:

- `common#/$defs/UserInputPath` — the type of `ImportedEvidenceRecordV1.sourcePath`
  — says *"never enters any content identity; recorded in operational records
  only"*. My argument rested on a field the contract excludes from identity.
- **No join** binds `sourcePath` to `wrapper.blobs`; the only `sourcePath` joins
  (`workflows_model.v1.py:765,775`) belong to `SourceMappingV1` and bind to the
  **snapshot inventory**.
- Payload custody is independent of `blobs`: the canonical payload bytes and the
  exact registered schema **document** bytes are retained and re-hashed either
  way, so "cannot be re-derived" does not follow.
- The archive-member rule restricts **reading** and is vacuously satisfied by an
  empty list. My citation said §6; it is **§3 PO-4** (lines 916-935). Both
  corrected.

I also accept the methodological point: in v1 I treated **mirror agreement** as
if it justified the minimum. It does not — agreement is a property of the two
documents and says nothing about which admitted set is correct.

**Adopted `0..4096`** on both mirror sides. The maximum keeps its authority (the
`imported-evidence` description publishes 4096 blobs and a 256 MiB artifact
bound); narrowing foundation's 100000 is stated as a compatibility change.
Controls: a **zero-asset import closes a complete Run** with its payload and
schema still retained, both documents admit the same zero-asset instance, and
4097 refuses on both. Root's mirror probe on final bytes: 13 cases, 0
mismatches, `zero-blobs` admitted by both, `4097-blobs` refused by both. Same-
instance mirror tests and the logical-path/byte bounds are preserved.

## 4. CB3-MUST-4 — producing boundary. **Accounted honestly.**

Verified: `adopt_baseline` (`workflows_model.v1.py:643-657`) sets
`ctx['scopeDigest'] = doc_digest(scope)` from the **passed** document and uses
`plan` only as `'planId': plan`, a PlanId string. It cannot prove selection.
The same is true of `policyDigest`.

**Correction — both halves root offered.** The precondition is *named*:
`adopt_baseline` is a pure projection over documents the caller must already
have admitted, and with no analysis spec the scope binding is a **caller
assertion**, said so in the docstring and the contract. And a **bounded
composition** is added: `verify_scope_parameter_binding(analysis_spec, scope)`
requires the scope document's canonical digest to be the `payloadDigest` of a
selected parameter row citing the registered `ScopeDocumentV1` **document**
digest. Controls: verified-admits, non-selected document
(`BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`), no scope parameter selected and a
row cited under another schema (`BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER`), plus
end-to-end adopt-verifies and adopt-refuses. The baseline descriptor and its
identity are unchanged, and no product host is implied. The registry half is
preserved and root's `scope.json` still passes unchanged. Repository
`scope-descriptor` versus operator glob `ScopeDocumentV1` stays distinct.

## 5. Codex M2 follow-up — evidenceUse declaration. **Confirmed and closed.**

Reproduced independently on released v1: a policy whose evidence atom carried no
matching rule-level `evidenceUse` was refused by `resolve_policy`
(`IMPORT.ABSENT_FOR_PREDICATE`) and **admitted** by `close_run`. My v1 closure
loop called `admit_atom` alone and omitted the rule-level obligation.

**Correction.** The complete per-rule admission is factored into
`admit_policy_rule` and **reused** at the Run closure for policy rules;
`resolve_policy` is unchanged in behaviour and not weakened. The compiled
program carries no `evidenceUse` of its own, so its atoms are admitted directly
and the existing compilation join still forces it to be the exact projection of
the same admitted policy rules — both retained. Controls assert the two
boundaries give **one answer** for declared, undeclared, wrong-kind and
native-atom cases. On final bytes all boundaries agree; on released v1 they did
not. The 16 pure-helper policy cases are preserved and still pass — their
recorded scope explicitly did not claim host admission, so this does not rewrite
them.

## 6. Evidence and timing clarification (additive)

My v1 `inputsConsumed` recorded `CODEX-PUBLIC-NOTE.md` as read "before the
substantial edit batches and before handoff". The accurate scope is narrower: my
only full public Read was at **06:02**; my later tool call on that path computed
its **hash only**, and a hash is not substantive reading. Material root added
after 06:02 — the cardinality reasoning, the retained-Run M5 counterexamples and
the M3/`BUNDLED_GRAMMARS` contradiction — was **not** reflected in my v1
handoff. The v1 handoff and custody are untouched and byte-identical; this is
the additive correction. In this pass I read `current-codex-note.md`, every
`codex-rechecks` report, and the new `CODEX-PUBLIC-NOTE.md` in full before the
batches they govern.

## 7. Checks run

Whole-suite runs use a **further disposable copy** with an **explicit measured
pin refresh** (`probes/devtest.sh`). Those refreshed pins exist only in that copy,
are not candidate bytes, and are **not** accepted-candidate pin proof.

| Checker | v12 | v1 released | v2 final |
|---|---|---|---|
| `check-foundation.py` | 231/231 | 231/231 | **231/231** |
| `check-identity.py` | 767/767 | 823/823 | **903/903** |
| `check-product-quality.py` | 24/24 | 24/24 | **24/24** |
| `check-product-configuration.py` | 28/28 | 28/28 | **28/28** |
| `check-array-orders.py` | 65/65 | 65/65 | **65/65** |
| `check_workflows.v1.py` | 1290/1290 | 1590/1590 | **1598/1598** |
| `check_native_evidence.v2.py` | 151 cases/60 cells | 346/66 | **346/66** |

All exit 0. Root's own probes on final bytes: ownership 4/4 as required,
mirrors 13 cases/0 mismatches, scope 5/5, policy 16/16, grammar 8/8,
M2 boundaries agree.

## 8. Root's fixture-extraction interface — preserved and verified

`adapt-integration-builder-v13.py` extracts **54 named module-level
declarations** and asserts completeness. A correction that made one of them
depend on a new module-level name would compile and then fail at import. That
happened twice during this pass and both were fixed by keeping the declarations
self-contained (`GRAMMAR_FILES` derives its languages inline; the clone
disclosure derivation moved *inside* `coverage_result`). `probes/verify_root_interface.py`
reproduces root's extraction with **only** root's name set, imports the result
and exercises `build`, the syntax inventory Run and `graph_with_import`:
**54/54, imports cleanly, all three Runs close.**

## 9. Limits and open items

1. **No acceptance is conferred.** Codex must substantively assess these bytes;
   fresh independent review, a NEW blind consumer and complete application
   review all remain required.
2. **Pins are intentionally stale in the released delta and untouched**; all pin
   and report files equal frozen v12. Root refreshes pins **after** all recording
   edits, then runs the six commands and seals.
3. **Root's grammar probe tests descriptor vocabulary, not admission.** It calls
   `validate_native` only, so it exercises the schema enum; the `syntaxClass`
   registry law is enforced at `admit_native_context` and is covered by my own
   controls. I state this rather than letting an 8/8 vocabulary result read as
   proof of the class law.
4. **Integration dependency (unchanged from v1):** the native unit consumes
   `foundation/relation-payload-schemas.v2.json`; that row is in
   `CONSUMED_SOURCES` and **the native pin manifest will need it** at refresh. I
   did not edit the manifest.
5. **`integration-fixtures.py` is NOT in my delta.** Root owns fixture
   adaptation. I regenerated it only inside disposable copies.
6. **`bind_syntax_universe`** still accepts `retained`/`snapshot_inventory` for
   signature parity without consulting them; stated in its docstring.
7. **Not attempted:** no product host, no compiler/provider execution, no
   security or admission-contract changes, no JSON/YAML tokenisation, no Python
   support, no report re-derivation.

## 10. Development attempts that failed (retained)

- **First M2/F4 exploit probe (v1)** — non-discriminating; retained at
  `v1/logs/p2-FAILED-ATTEMPT-nondiscriminating.json`. Not rewritten.
- **Root-interface breakage, twice** — `GRAMMAR_FILES` depending on
  `GRAMMAR_LANGUAGES`, then `build` depending on `retained_clone_ownership`.
  Caught by `verify_root_interface.py`; fixed by keeping declarations
  self-contained.
- **`.d.ts` dialect drift check** — a naive set-equality between bundled code
  suffixes and the dialect table failed on the longest-match sub-variant
  `.d.ts`; replaced with a coverage + resolution check.
- **Suffix control masked by the order guard** — `['.rs','.py']` refused for
  array order before reaching the bundling check; reordered to `['.py','.rs']`.
- **Tautological assertion and wrong exception type** in my first zero-asset
  mirror control; both replaced with a real `mirror_admits` helper.
- **`tsconfig.json` as a data-grammar Run path** — collided with the TypeScript
  config graph (`native.universe-source-mismatch`); replaced with neutral paths.

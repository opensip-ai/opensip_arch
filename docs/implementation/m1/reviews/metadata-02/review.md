# Review 02 (nonblind correction review): RF-01 metadata-v2

**Verdict: ACCEPT-DESIGN-UNIT**

- Subject manifest: `/tmp/opensip-implementation/m1-metadata-subject-02.json`
- Subject manifest SHA-256: `1b456017cc5a1359b37fe2f663fd9c8b220363a843dafaf1924181ead72344c2`
- Candidate folder: `docs/implementation/m1/metadata-v2/`
- Prior review: `/tmp/opensip-implementation/m1-metadata-review-01` (subject-01, CHANGES-REQUIRED: RF-A, RF-B, RF-C)
- Environment: `/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B` (jsonschema 4.25.1, referencing 0.37.0)

**Scope of acceptance.** Only this scoped RF-01 design/reference correction is accepted. The following remain required:

- product implementation;
- binding this successor into the design-lock;
- startup, renderer and producer tests;
- the M1 gates;
- runtime and release qualification, including the M6 release producer.

Nothing here is product execution.

## Integrity

- **subject-02 before and after review:** the manifest SHA-256 matched, all 10 files matched on SHA-256 and byte length, and there were no unlisted files.
- **subject-01 after review:** still intact (manifest `bccfda51…`, all files match).
- **Architecture checkout:** its `docs/implementation/m1/metadata-v2` copies are byte-identical to the frozen subject.
- **Carried over unchanged from v1:** `command-envelope.schema.json`, `command-inventory.schema.json`, `command-inventory.v4.json` and `metadata.schema.json` are byte-identical to metadata-v1.
- **Changed:** README, checker, fixtures, coverage, sources (only the candidate paths moved from v1 to v2) and successor.

## Checker

Run from the frozen folder with `--architecture /Users/sb/code/opensip-ai/opensip_arch`: exit 0, `passed: true`, 28 schemas, 43 cases, 5 lexical negatives, `productQualification: false`. The output is saved in `checker-output.json`.

The v2 checker adds five things:

- `verify_successor`;
- loading candidate schemas from HERE by pin;
- `admit_build`, with a channel-disagreement negative;
- schema-only external-root assertions;
- refusal of unregistered references with no retrieval.

## Prior findings

### RF-A (coverage routing) — closed

- **Method text updated.** The coverage v2 help and version methods now state:
  - CommandEnvelope major 4, `metadata:1` and the fixed `metaDispatch` selectors;
  - human/JSON equality of the payload fields;
  - no project, store, component, helper, network or asset effects;
  - the corrected wording;
  - exact tests for the parser-refusal empty-errors rule.
- **Version adds the build-side obligations:** M1 is development-only, environment or caller release selection and invented closures are refused, and there is a single channel whose disagreement is refused.
- **Owners.** The version row gains the owner `crates/reporting/src/assets.rs`. The method names `crates/reporting/tests/projection_tests.rs` and `apps/cli/tests/startup_tests.rs`.
- **No new product files.** All three files already exist in the design-locked M1 `repository-file-inventory.v3.json`.
- **Clean diff.** A normalized diff against the v1 subject shows only those method texts, the owner addition and the inventory4 path.
- **Milestone map.** `moduleFirstMilestone` has no entry for `assets.rs`, but that map is partial by design: 45 of 85 row owners are absent, M1 owners included. This is not a routing defect.

### RF-B (successor binding) — closed

- **Member completeness.** `successor.json` pins all 9 other folder members; the checker enforces that the pinned set equals the folder contents minus successor.json.
- **Parents.** It pins 9 parents. I checked each against the v46 overlay `files` list, or against the design-lock `inventorySuccessor` for M1 inventory v3. All match and are live.
- **Passage overrides.** It carries 4 exact `passageOverrides`, each with a parent pin, a line number or JSON pointer, and full before and after text:
  - build plan L885;
  - ch14 L325;
  - repository-file-inventory v1 `/files/7/description`;
  - M1 inventory v3 `/files/7/description`.
- **Full check.** The checker verifies every pin, every before-text selection, and that each after-text is exactly the specified wording substitution.
- **No other occurrence.** Outside review folders and candidate folders, the old wording remains only in the superseded M1 `repository-file-inventory.v2.json` (the `previousCandidate` of the design-locked v3). The `delivery.v2` and `implementer-litmus.v4` hits use "signed release descriptors" for runtime version selection, a different concept.
- **Negatives on temporary copies under the review folder** (removed afterwards): all of the following are refused:
  - an unlisted member;
  - a tampered member;
  - a tampered parent;
  - changed override after-text;
  - a wrong override pointer;
  - a dropped override;
  - a dropped candidate.

  Unmodified copies pass.

### RF-C (single build channel) — closed at design/reference level

- **Design.** The README makes `crates/reporting/src/assets.rs`, the accepted HostAssetPinV1 owner (report-asset-binding.v1.json `owningModule`), the one compiled channel owner. BuildMetadataV1 and any fixture HostAssetPinV1 take their channel from one constant; there is no environment or configuration channel.
- **hostRelease source.** It comes only from the CLI's `env!("CARGO_PKG_VERSION")`.
- **M1 constructor.** It is development-only and produces no closures. The M6 release producer is deferred to a separately reviewed assembly.
- **Probes.** `admit_build` accepts development/development. It refuses development record with release asset, release record with development asset, a differently cased channel, a `None` channel, and an invalid record.

## New root finding: validator dialect switch through external-root references

**Reproduced independently. The adapter is correct and complete for the 28 pinned documents.**

- **Mechanism.** In `jsonschema/validators.py` L340–348, `evolve` calls `validator_for(schema, default=self.__class__)`. When a `$ref` resolves to a whole resource whose contents contain `$schema`, the 2020-12 meta-schema selects the standard `Draft202012Validator`. The extended `ExactValidator` is not registered, so the custom `const`, `enum`, `x-opensip-order` and integer type checks are lost. A `$ref` to a `#/$defs/...` pointer resolves to a sub-schema without `$schema` and keeps the custom validator. That is why direct-`$defs` probes, including mine in review-01, did not see the loss.
- **Instrumented reproduction.** I extended the validator with counting keywords. Validating `help-top-level` through envelope4:
  - with the metadata-v1-style registry (`Resource.from_contents`), `x-opensip-order` was never called;
  - with `$schema` kept in the contents and the dialect set explicitly (`Resource(contents, DRAFT202012)`), it was still never called, so the explicit dialect alone does not fix it;
  - with the v2 adapter, it was called.

  Checked directly: a `$ref` to the root drops the custom validator, and a `$ref` to a `$defs` pointer keeps it.
- **Behaviour.** With the old registry, `unsorted-help` and `duplicate-help-name` are accepted by schema-only validation through the envelope; with the adapter they are refused. My own new case, reversed release `closureIds` in a version envelope, shows the same difference. Duplicate closure IDs are refused either way, because `uniqueItems` is a standard keyword.
- **Differential.** Over all 43 fixture cases, validating the envelope schema only with the old registry and with the adapter differs on exactly `{duplicate-help-name, unsorted-help}`. Every accepted case is still accepted. This matches the reported two TS/Python disagreements. I did not rerun the TypeScript trial.
- **Adapter fidelity:**
  - every registry resource equals its original document minus top-level `$schema`;
  - every resource has the DRAFT202012 dialect;
  - all 28 documents declare the 2020-12 `$schema` (checker-asserted);
  - no nested `$schema`, no embedded `$id` resources, and no `$dynamicRef`, `$recursiveRef` or corresponding anchors.

  So removing only the top-level `$schema` is sufficient, and dialect semantics are otherwise unchanged. The original bytes and pins are unchanged.
- **Detection.** The new checker assertion (schema-only external-root refusal of `unsorted-help`, `duplicate-help-name` and `invented-development-closure`) catches:
  - reverting the adapter;
  - reverting to an explicit dialect with `$schema` kept;
  - dropping the help `x-opensip-order`;
  - dropping the development empty-closure rule.

  See advisory N-01 for the gap.
- **Exact const/enum.** jsonschema's standard `equal` already separates bool from int (`const:1` rejects `true`; `enum:[0]` rejects `false`). So through these edges the practical loss was the ordering annotations, not the bool/int distinction.
- **Scope.** There are 6 external-root `$ref` edges in the pinned set (listed in `root-refs.json`):
  - envelope4 to `metadata:1`, `baseline:2` and `invocation:3`;
  - envelope3 to `baseline:2` and `invocation:3`;
  - `fact-batch:3` to `occupancy-companion:1`.

  As requested, this review does not requalify historical evidence that validated through the last three edges with an unadapted registry. That is recorded as advisory N-02 and as a limitation.

### Correction to my review-01 conclusions (nonblind)

- **Ordering and uniqueness.** Review-01 listed "help rows strictly unique in UTF-8 order" and closure ordering as established. That evidence came from direct `$defs` validation plus semantic catalogue/build comparison. It did **not** establish that ordering is enforced when validation crosses into another document through the envelope; under the v1 checker it was not.
- **A-05.** Review-01's A-05 said semantic admission "masks" the help-order schema law. The more accurate cause is that the envelope path never enforced the law at all. The v1 mutation probe could not tell the two apart.
- **Unaffected conclusions.** Review-01's exclusivity, parser-refusal, SemVer, closure grammar, `maxItems` and development-rule conclusions use standard keywords or root-level `ExactValidator` keywords, so they are unaffected. The corresponding v2 probes agree.

## Topic spot-checks carried forward

- **Schemas, inventory and selectors.** They are unchanged bytes, so review-01's schema-behaviour results still apply, with the ordering correction above.
- **Selector equivalents.** The README now defines pointer/projection equivalents: `/meta/commands` followed by a per-row `name` projection in array order, plus three direct pointers. Arbitrary selector evaluation is forbidden.
- **Release with no closures.** Whether this is eligible is explicitly deferred to the admitted M6 component inventory; shape alone does not authorize a release.

## Required findings

None.

## Advisories (nonblocking)

- **N-01 — closure-order mutation gap.** Dropping `VersionMetadataV1.closureIds` `x-opensip-order` is not caught by the checker. The only closure-order check uses direct `$defs/BuildMetadataV1`, whose separate annotation is unaffected. Add a schema-only envelope case with reversed release closure IDs; my probe `repro-release-closure-order-envelope-*` shows it separates the two registries. Also, the `invented-development-closure` assertion guards the schema rule, not the adapter: it refuses under both registries.
- **N-02 — historical external-root edges.** Envelope3 to `baseline:2` and `invocation:3`, and `fact-batch:3` to `occupancy-companion:1`, may have lost custom keywords in earlier Python reference evidence that used `Resource.from_contents`. Record a separately scoped root item to decide whether any accepted evidence relied on ordering or exact keywords across those edges. This unit neither requalifies nor invalidates it.
- **N-03 — assets.rs inventory description.** The M1 `repository-file-inventory.v3.json` description of `assets.rs` still covers only asset-manifest validation. Its new compiled channel/metadata constant role is bound by the successor README and coverage, not by a passage override. Consider an override when binding.
- **N-04 — single verification owner.** The coverage version row's `verification.owner` is `apps/cli/tests/startup_tests.rs`. `projection_tests.rs` ownership of the producer and channel negatives is stated only in the method text.
- **N-05 — empty diagnostic text.** The coverage test obligation requires "nonempty diagnostic text", but the schema still admits `diagnostics:[""]`. Review-01 A-01's control-character and `projectId` hardening remains open.
- **N-06 — previousCandidate unchecked.** The checker does not verify the `previousCandidate` pin. It matches subject-01 today.
- **N-07 — superseded wording.** The superseded M1 `repository-file-inventory.v2.json` L279 keeps the old wording. It is not design-locked; no action needed unless it is revived.
- **Still open from review-01.** A-03, A-06 and A-07 (standing text replaced by an acceptance record) remain nonblocking.

## Executed checks

1. Pre- and post-review manifest and file hashes for subject-02; post-review integrity of subject-01; architecture copy identity.
2. Frozen checker run (exit 0; 28 schemas; 43 cases).
3. Byte comparison and normalized diffs, v1 to v2, for README, sources, fixtures and coverage; identity of the four schema/inventory files.
4. Parent pins checked against the v46 overlay and the design-lock `inventorySuccessor`; wording search across accepted docs.
5. M1 inventory v3 presence and descriptions for `assets.rs`, `projection_tests.rs`, `startup_tests.rs`, `bootstrap.rs` and `outcomes.rs`; coverage owner, milestone and `moduleFirstMilestone` analysis.
6. jsonschema `evolve` source inspection.
7. 47 independent probes (`probes.py`, results in `probe-results.json`), all as expected. They cover:
   - validator-class mechanism counts across three registry variants;
   - behavioural reproduction and a 43-case differential;
   - adapter fidelity, dialect, and nested/embedded/dynamic scans;
   - the external-root edge inventory;
   - six adapter/schema mutations;
   - six `admit_build` cases;
   - nine `verify_successor` baselines and negatives on temporary copies (removed).

## Limitations

- The separate TypeScript schema trial was not rerun. Its 43-case agreement is accepted only as consistent with my Python differential.
- Only jsonschema 4.25.1 and referencing 0.37.0 were used. Other versions may select validators differently.
- No product code exists or ran. Channel single-sourcing, `CARGO_PKG_VERSION` sourcing, no-effects bootstrap and renderer parity are design/reference obligations only.
- Historical evidence across the three pre-existing external-root edges was not re-examined (N-02). Entry-point closure of the whole corpus, including the known unrelated RF-03 dangling policy Atom, was not evaluated and is not counted as metadata success.
- The review covers the frozen subject and the parents cited here, not the full accepted set.

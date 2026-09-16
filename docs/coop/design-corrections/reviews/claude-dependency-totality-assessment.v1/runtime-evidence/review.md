# Bounded assessment — dependency totality, plus two text-consistency corrections

Reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`, actual Claude, after my completed **source35
ACCEPT**. This is a bounded assessment before the successor freeze. It is **not** source36 acceptance
and not application review, and it grants no acceptance, readiness, qualification or application
outcome.

All writes stayed in this runtime. Frozen35, the author runtime, the mutable successor tree and my
prior reviews were read-only; the successor's `atom_model` digest `2c5fdabb…` matches the author's
report and was unchanged across my probes. No consumer material, root-blind record or consumer-specific
input was read. Each owner file cited below equals its frozen35 manifest row.

---

## 1. Dependency totality — decision

**Totality over every current source subject is required by current law.** The source35 answer is a
**reference defect**. The one atom sentence that states the rule is under-specified, but no owner allows
the loose reading.

I wrote the expected law (`law-derivation-dependency.json`) **before** writing or running any probe; the
recorded timestamps prove the order. It rests on four owners:

- **Native RC-4** (`native-evidence.md:2002-2003`): "`reachability` counts `calls` edges **over the same
  examined set**."
- **Atom §4** (`atom-evaluation-contract.v1.md:269`): "No fictional complete entries."
- **Native sufficiency step 1** (`native-evidence.md:2085`): a relation absent from the view →
  `required-relation-missing`.
- **Identity §3** (`identity-and-evidence.md:1365-1366`): `complete` "remains a claim about the examined
  partition."

Suppose a reachability partition covers {f, g} but its folded `calls` dependency comes only from a scope
over {f}. The fold then claims complete calls evidence for g, which nobody examined. The atom sentence
"pair dep Coverage to current-source scopes **containing those native ids**" does not say *every*. That
is the textual under-specification. Outgoing already evaluates per subject.

## 2. Measured (atom-api, synthetic inputs; remedies applied in-process only)

Incoming reachability `all-covered`, primary scope over {f, g}:

| Dependency calls partitions | Expected law | frozen35 | successor | remedy A |
|---|---|---|---|---|
| one scope {f, g} | true | true | true | true |
| disjoint {f} + {g} (lawful) | true | true | true | true |
| **{f} only** | unknown | **true** | **true** | unknown |
| **{f} + {g} at the wrong universe** | unknown | **true** | **true** | unknown |
| **{f} + a {g} scope with no Coverage** | unknown | **true** | **true** | unknown |
| {f} + {g} with unknown Coverage | unknown | unknown | unknown | unknown |
| none | unknown | unknown | unknown | unknown |
| {f} + {f, g} (overlap; unlawful at `close_run`) | no law | true | true | true |

- **Author observation reproduced independently.** The author's §8 finding, `all-covered` true on
  frozen35 and on the successor, reproduces with my own fixture. It is not fixed by the author's
  successor bytes.
- **Remedy's answer on the partial cases** equals the **no-dependency answer exactly**: value, causes,
  `nativeDeficiencies` and `coverageIds`.
- **Order independence:** every map insertion order gives one result, on the successor and the remedy.
- **Outgoing:** from f it is true and from g unknown, on every model; the remedy changes nothing
  outgoing.
- **Known-match and count dominance.** A known incoming fact under the partial census keeps `exists`
  true, `none` false and `count≤0` false on every model. Only `count≤1` and `all-covered` move from true
  to unknown under the remedy.
- **Attestation whole-source view: same defect class.** A qualifying reachability attestation naming
  {f, g}, with calls for f only, gives true on frozen35, on the successor, **and under remedy A**.
  Variant **B** applies the same totality over the attested scopes' subjects, keeping whole-source when
  that set is empty. Under B it gives unknown, while total and disjoint calls stay true.
- **Empty source program: conservative, under-specified.**
  - With an empty primary scope closed by complete Coverage, reachability stays unknown on every model,
    even with an explicit empty calls partition, because containment pairs nothing.
  - The attestation route with an explicit empty calls partition does close.
  - Neither route is unsound, but they disagree for empty programs.
- **Different kind, whole-source (clones → declares): genuinely under-specified.** A declares partition
  for f alone satisfies a clones claim on a file that also declares g, on every model. No owner states a
  population rule for different-kind dependencies, and RC-4 names only reachability/calls. **Not
  claimed as a defect.**
- **Regression:**
  - The successor's check-atoms passes **95/95** under A and under A+B, so no existing expectation relies
    on a partial census.
  - All 8 atom-model consumer checkers (check-atoms, replay, semantic-replay, candidate-replay,
    execution-replay, execution-inputs, provider-attribution-return, composition) exit 0 on disposable
    kits with and without remedy A. Seven give byte-identical stdout.
  - `check-execution-inputs` differs only in five `ownedHashes[*].path` values, which embed the absolute
    kit directory. The hash values are equal, and each kit is identical run to run.

## 3. Reachability, by standing

| Standing | Finding |
|---|---|
| atom-api | **Demonstrated** (p01, p04) |
| native producer | **Not excluded.** `admit_coverage_result_v3` admits one scope and one entry and cannot see another relation (`relation-payload-schemas.v2.json` `coveragePartitionLaw.producerCannotDecideThis`). RC-4 is a stated producer obligation, not a between-relation admission check |
| `close_run` | **Not excluded.** Disjointness is per partition key, so different relations never overlap. The omission half is owed only by `file@enumerated` (`identity-model.v3.py:1027-1055`; `coverageTotalityLaw.whichRelationsHaveOne`) |
| execution-inputs census | **Partially neutralized.** g is uncovered in the calls cell's symbol census, so that account is incomplete (`execution-inputs-contract.v1.md:188-201`). A **required** calls cell, as in the default profile, drives the Run to `indeterminate` via `required-cell-unsatisfied`, but the atom value inside proof stays wrong. An **optional** calls cell carries no required deficiency |
| closed enumeration / retained Run | **Not constructed.** No full-Run counterexample is claimed |

## 4. Smallest remedy

**Required, remedy A.** In `_select_dep_coverages`, same-kind branch, applied on top of the successor
(which already removed the mapped fallback): after pairing exact scopes that contain a current subject,
if the **paired** scopes' subjects do not jointly contain every current subject, return no partitions.
The dependency then occupies no position. This is about ten lines and needs no new cause, field, schema
or registry change.

**Recommended for coherence, variant B.** The attestation view applies the same rule over the subjects
of the scopes the attestation names, when that set is non-empty.

**Contract §4 dependency paragraph, proposed wording:**

> Same sourceSubjectKind: pair dependency Coverage only to exact (relation, rung, S) scopes that contain
> a current source subject, and those paired scopes must jointly contain **every** current source
> subject — the atom subject (outgoing), the evaluated source scope's subjects (incoming), or the subjects
> of the scopes a qualifying attestation names (attestation view, when non-empty). Otherwise the
> dependency contributes no position and `sufficiency_v2` answers `required-relation-missing`
> (native RC-4).

Also add the §9 cases, and check-atoms controls for: partial census unknown and equal to no-dependency;
lawful disjoint true; attestation partial unknown; dominance under partial; outgoing unchanged.

**Cross-owner effects if adopted:**

- Changed owners: the contract, `atom_model`, check-atoms, and re-digested pins in five ledgers.
- No change to schema, registry, identity, native or execution-inputs owners.
- Consumer checkers unchanged.
- Package12 retained Runs hold no reachability dependency view.

**Optional follow-ups, not required for soundness:**

- an empty-examined-set rule so the Coverage and attestation routes agree;
- a population rule for different-kind whole-source dependencies.

## 5. Root's two text corrections

### `historySubjectOrder`: the proposal aligns every owner; one precision is owed

- The registry row "strict unique path UTF-8 / uniqueKey path" (`registry:823-826`) is the **only** owner
  asserting uniqueness. It contradicts the same registry's `HISTORY_SUBJECT_SEQUENCE_ORDINALS`
  (`:1133-1134`), atom §6 (`:352`), and the payload schema (`subjects`: `x-opensip-order: sequence`, no
  `uniqueItems`). It also contradicts the reference loop and `test_history_duplicate_path_retains_all_ordinals`.
- **Measured:** the stock schema admits duplicate paths in non-sorted producer order. The atom retains
  both ordinals [1, 2]: `exists` true, `count≤1` false, `count≤2` true.
- **Correction:** order is the existing sequence (producer order); there is no unique key; duplicate
  paths are allowed; every matching row is retained at its original ordinal.
- **Precision:** duplicates remain lawful payload for atom evaluation, but the repair
  `targetSubjectProjection` **refuses** when more than one subject matches one target
  (`imported-evidence.schema.json:970`, step 5). The row should confer no merge or pick rule. The phrase
  "HistorySubject keyed by {path}" names a match key, not uniqueness. Native `normalize_history`'s unique
  UTF-8 order is one lawful producer order.

### Runtime `importQuantifiers` prose: the proposal aligns existing owners; one precision is owed

**Measured on the atom API** (all 8 checks pass):

- unfiltered `exists` is true on `observed-hit` **and** on `observable-unhit`;
- filters `eq observed-hit` and `eq observable-unhit` restrict polarity;
- `unobservable` and `unmapped` never enter R and never make `exists` or `none` true;
- a filter naming `unobservable` is **admitted but matches nothing**;
- unobservable rows are disclosed as uncertain whether or not a filter is present.

**Proposed atom §6 sentence:**

> Unfiltered runtime `exists` is true on a consumable mapped row of either polarity — it asserts that an
> observed row exists, not that the subject executed; an `observability` filter restricts polarity;
> `unobservable`/`unmapped` rows never enter R and never make `exists` true.

**Precision:** registry `observabilityFilter` "may select disclosure" overstates what a filter does. A
filter cannot select those rows into R, and their disclosure is unconditional.

## 6. Probe errors kept

- My first p01 launch used shell redirection that the permission mode refused, so nothing ran. All
  probes then went through `probes/run.py`, which retains the command, stdout, stderr, exit and digests.
- p02 had a syntax slip and an assumed registry key path; both were fixed before p02 ran.
- p05 framed the execution-inputs stdout difference as remedy effect versus nondeterminism. It was
  neither: an embedded kit path. The JSON-path diff is the evidence relied on.

## 7. Remaining constraints

- **Remedy A is owed** before a frozen successor can claim the incoming dependency law is sound; B is
  recommended.
- Empty-source agreement and the different-kind population rule are open owner decisions.
- All evidence is atom-api, stock schema or read-level owner law. No native producer run, closed
  enumeration or retained Run was constructed.
- The full 107-row scope and integrated suites remain for the final frozen successor review.

# Independent design review — consolidated product **source31**

Substantive exact-source successor review. Same reviewer origin
(`ce3dec3b-0620-44ec-86e6-129b0e25cb1b`) that produced the source26 `CHANGES_REQUIRED` and source27
`ACCEPT` reviews. The source27 report (sha `4cb03aa8…`) is historical and unchanged; nothing here
alters it. This is not automatic promotion of 27 and not author assistance.

**Verdict: ACCEPT.** No unresolved required issue: **0 new MUST, 0 new SHOULD**, two advisories, each
stating why it is not a SHOULD.

Design review only. **No application grade, no activation, no blind acceptance, no implementation
authorization, no commit or push.**

---

## 1. Inputs, verified before anything was read

| Binding | Expected | Measured |
|---|---|---|
| `candidate-subject.v31.json` | `ca713db5…95bb5` | ✅ matches |
| `candidate-source.v31.tar.gz` | `0a980be4…83e0` | ✅ matches |
| Snapshot | 12,895 files / 736,536,507 B | ✅ every row's hash **and** size; 0 missing, 0 mismatched, **0 extras** |
| Ancestry | 31→30→29→28→27 | ✅ each child declares its parent's manifest digest; the v27 link resolves to `a1ae88ef…`, **the exact subject I graded** |
| Package `artifact-manifest.json` | `c9f63282…f258` | ✅ **270/270** members hash-match, 0 missing |
| Package `source-manifest.json` | binds 31 | ✅ byte-equal to the frozen31 manifest (12,895 rows) |
| Native schema | `3e37c7b7…b0b0` | ✅ matches |

Frozen snapshot re-measured **unchanged** after every run (0 deviations). Report-writing checkers ran
only inside disposable copies whose every byte I verified against the manifest first. No pin gate was
bypassed.

## 2. The delta, derived independently

Per-step and cumulative set differences over the five frozen manifests: **2 added, 0 removed, 14
changed — 16 touched**, +241,349 bytes. That is exactly the 16 paths root's listing names, with no
removals. Six of the fourteen changes are same-byte-count digest/pin refreshes.

Per step: 27→28 nine files (the ordering work plus pins), 28→29 nine (native schema, checker, report,
pins), 29→30 seven (the `native-cases` fixture plus pins), 30→31 nine (`check-enumeration` plus pins)
and the two added artifacts.

## 3. The five source-delta items, assessed on actual source

### 3.1 source28 — `ruleResults` ordering · **correct and complete**

Three owners now agree: `identity-model.v3.ordered:156` keys `ruleResults` by
`v['ruleId'].encode('utf8')`; `identity-schemas.v3` declares `x-opensip-order {"by":["ruleId"]}`;
composition contract line 194 says "`ruleResults` has one item per policy rule, ordered by `ruleId`
UTF-8."

I did not stop at the reported fix. **I enumerated all 57 `x-opensip-order` annotations**: exactly two
carry an explicit `{"by":[…]}` key order — `owner-source-set` and `ruleResults` — and **both** now
have a named branch. **Zero** explicit key orders are left falling through to the generic
canonical-member order. This is a complete fix, not a spot fix.

The fixture genuinely discriminates rather than assuming it does: line 115 asserts
`rr != sorted(rr, key=C.canonical)` with the comment *"Control must distinguish both ordering
recipes"*. Executed on frozen31: correct-order wholeRun **ADMIT** (`run3:ae87a362…`),
canonical-member order **REFUSE**, duplicate `ruleId` **REFUSE** — the refusal coming from the schema
validator itself (`array order {'by': ['ruleId']}: strict unique order required`), so two independent
enforcement points agree.

**I reproduced the regression.** In a disposable copy of 1,350 manifest-verified files I deleted the
single branch so the array falls back to the generic order. The same checker then fails with
`AdmissionError: ORDER_OR_DUPLICATE` *while minting the proof bundle* — the pre-28 reference could not
even construct a lawfully ordered proof. The branch is load-bearing.

### 3.2 source29 — native retention catalog · **correct and measured**

Most of the 37 KB growth is indentation, so I compared structured content, not a diff.

- **76 annotation sites** — my syntactic count, my structural walk, and the checker's own frozen
  report all agree. The stale 68 is gone, and `siteCountLaw` leaves no second hand-maintained total.
- **Exactly 3 `derived` uses**, all under `SourceUnitOwnershipV1` at `units[].unitId`,
  `selectedUnitIds[]` and `ownership[].unitId` — precisely the positions the catalog names.
- `derived` **reuses the existing recipe**: `UnitIdentityV1` and `native.compilation-unit.v1` were
  already in the bundle, and it retains no separate preimage frame, so no unused fragment retention
  was added.
- **0 sites** carry an undeclared representation or retention.

I checked that `derived` is *enforced*, not aspirational prose. `source_unit_ownership_faults`
re-derives every `unitId` and enforces both membership positions. My own end-to-end recompute: the
identity is stable, injective over its four fields, admits a `#` in `markerPath` (confirming the
published rationale that H needs no path restriction, unlike the earlier delimiter recipe), yields no
faults on a correct record, and names tampering at the right selector.

One honest note on method: the schema **and** the checker are source-pinned, so mutating the schema
answers `PIN-MISMATCH` before the digest-law check runs. I did not bypass that gate — I exercised the
checker's exact predicate in memory instead, where an undeclared retention names its site, an
undeclared representation names its site, and removing `derived` names exactly the three positions.

### 3.3 source30 — `native-cases` coverageView digest · **consistent, partially unverifiable by me**

The 29→30 edit has an identical byte count with a different digest — the signature of a fixed-width
64-hex swap, consistent with one refreshed schema digest. Every foundation drift guard and reference
suite passes on 31 (1,242 pins valid, 16/16 children, 11 group checkers), so the current state is
consistent and no semantic law moved.

I could **not** diff the 29→30 bytes (those snapshots are not inputs) and could not locate the
preserved source29 failed receipt anywhere in my inputs. I therefore assess the current state and do
**not** certify which field moved or that the failed receipt was preserved unaccepted. See **A-8**.

### 3.4 source31 / A-4 — enumeration root controls · **resolved, and they meet my gap**

My v27 advisory was that the internal-root guard was exercised by **0 of 27** checkers. Now
`check-enumeration.v1.py` runs five controls on an otherwise-valid fixture, **rebinding
`membershipDigest`** so a digest mismatch cannot mask the root-specific refusal and root admission is
genuinely reached. All five pass:

| case | expected | native | enumeration | refusals |
|---|---|---|---|---|
| `project-empty` | ADMIT | ADMIT | ADMIT | — |
| `project-dot` | REFUSE | REFUSE | REFUSE | `ENUMERATION_MEMBERSHIP_UNIT_ROOT` |
| `project-dot-slash` | REFUSE | REFUSE | REFUSE | `ENUMERATION_MEMBERSHIP_UNIT_ROOT` |
| `member-dot` | REFUSE | REFUSE | REFUSE | `ENUMERATION_MEMBERSHIP_UNIT_ROOT` |
| `member-empty` | REFUSE | REFUSE | REFUSE | `ENUMERATION_MEMBERSHIP_UNIT_ROOT` |

Each negative also asserts the exact native prefix, e.g.
`NATIVE_UNIT_ROOT_REPRESENTATION:units[0].rootPath:#/$defs/InternalUnitRootV1:'.'`.

**My own guard-omission mutation** shows they are load-bearing, and reproduces the *original* F-04
defect: with the guard disabled the two project-root cases refuse with
`ENUMERATION_BINDING_PROGRAM_ENTRY` — the exact misattribution — and the two member-root cases
**silently ADMIT**. The positive still passes, so the mutation is not just breaking the fixture.

On shape: these are **JOIN controls**, and the source says so. I do **not** insist on the
structural-ADMIT-then-refuse shape my v27 advisory suggested — `admit_unit_roots` runs at the
enumeration join, which *precedes* structural custody, so a structural-ADMIT claim here would be
misleading. My suggestion presumed a shape that does not apply at this boundary. That is the second
time a shape I proposed has been correctly declined, and both declinations were right.

### 3.5 source31 / A-5 — the two historical artifacts · **resolved; evidence restored, nothing repaired**

`evaluation-proof.v13.json` and `ep13.review-independent.json` are now frozen31 members with matching
digests, so the proposal's `source` fields resolve where they previously had **zero** occurrences. I
read the AX6/AX9/MD5/RX2c statements. The original declares `escapedEveryGuard` and
`declaredBlindSpotVariants` to be **exactly those four**, out of 29 variants built with 25 caught by
at least one guard, and sets `escapeSetIsAMeasurementNotACoverageClaim` and `aNarrowingIsNotAClosure`
true. Each residual account is a faithful restatement of its own original.

This restores available evidence. It does not repair, regrade, rerun or authenticate the original
measurements, and no historical file was edited.

## 4. Corrections to my own source27 record

The source27 report is left exactly as issued. All five of root's notes are correct and I accept them.

**RR27-01 — F-09 evidence claim was wrong.** v27 said the fault is raised only inside `load_coverage`
and `partitions_in_cell`. By AST enclosure: of the 7 sites, **1** is in `load_coverage`, **6** are
directly in the coverage-account loop of `admit_execution_inputs`, and `partitions_in_cell` contains
**none**. My v27 sentence was wrong in both directions — it named a function with zero sites and
missed the loop holding six. The **§5 conclusion stands**: every site is coverage-account derivation
and §5 is "Native Coverage accounts (derived)". (An intermediate indentation-based pass of my own also
mislabelled six sites as module level; it is preserved.)

**RR27-02 — stale current fields.** Correct: several v27 rows still presented resolved source26 issues
as current. Every row in this report carries a `currentScopeOn31` describing source31 only; historical
issues live in a separate field and never in current scope.

**RR27-03 — owner change accounting.** Correct: the v27 template matched prose labels, not paths.
Every row here lists actual file paths with `ownerFilesChangedIn27to31` computed by set-membership
against my derived delta. Across all 63 carried rows exactly two have changed owner files — **AR-12**
(native schema) and **FW-06** (`identity-model.v3.py`) — and those are the owners I read this session.

**RR27-04 — stale measurement.** Correct. Measured now: **12,895 files, 736,536,507 bytes**; the
current layer is `implementation-normative-inputs.v2.json` with **28 pins, all resolving against
frozen31**, and the original v1 layer is preserved and named as `previousArchitectureInputLayer`.
Root's read-coverage is also right that v27 never received layer 2 through the Read tool — I traversed
it programmatically then. **I have now read all 145 lines of it.**

**RR27-05 — environment claim.** Correct. Measured in this session: `rg` resolves on PATH and reports
ripgrep 15.2.0. My v27 statement that the binary "is not on this host" was unmeasured and wrong; it is
withdrawn. What stands: I did not execute the two historical checkers and their bytes are not members
of the snapshot.

## 5. Author package 7 — evidence, not results

All 270 members verified; the source binding is byte-equal to the frozen31 manifest. The provenance is
truthful: `source-rebuild.v1.json` pins **v30's** manifest as the construction receipt while
`source-binding.v31.json` separately binds 31 with `constructionSourceVersion: 30`. The checkpoint3
runId genuinely moved (`b43717f0…` → `0ef285d5…`) when the native schema changed at 29 — real
construction, not a label-only rebind — and the README says plainly that the source30 commands are
*not* claimed to have run against 31.

**I replayed all 13 exact stored cases through both boundaries** with my own decoder and the
snapshot31 owner: 7 positives ADMIT/ADMIT; 3 false-result controls structurally ADMIT then REFUSE
`EVALUATOR_COMPLETE_PROOF_REPLAY`; `ts-invalid-default-entry` ADMIT then REFUSE
`ENUMERATION_BINDING_PROGRAM_ENTRY`; both lawful binding controls ADMIT.

**I rebuilt everything from scratch against frozen source31** in a fresh arbitrary directory with only
`--source/--package/--out`, no helper overlay. **All 13 stores came out byte-identical** to the
preserved exports with identical runIds. The v27 "one differing unreferenced blob per store"
limitation is gone — measured, not assumed.

**A-6:** `verify-package.py` now runs the query reproduction after the 13 Run outcomes and asserts all
seven checks. Executed against frozen source31: rc=0, 12,895 source and 270 package files verified, 13
outcomes plus 7 query checks, and my regenerated query outputs are byte-identical to the retained
copies. The seven checks assert real semantics *and their limits* — empty traversal is never a proof
of absence, a work-bound limit with owed work is indeterminate, a wrong Run is refused, purged evidence
refuses rather than returning an empty graph. The property and mixed-universe probes remain separate,
as the README states; I ran both: properties pass with both effective-edition assertions, and the
merged view refuses `EXECUTION_INPUTS_COVERAGE_DERIVE` while the unmerged view admits.

**Weighting, unchanged and still accurate:** only TS checkpoint3 is helper-versus-owner agreement; the
other six are owner-derived and owner-replayed self-consistency. `exists`/`none` only; `and`/`or`/`not`
unexercised; `count-at-most`/`all-covered` unimplemented in the partial helper; the two-binding
construction incomplete and single-explicit only. **F-06's remainder stays an evidence limit, not a
demonstrated owner defect. F-14 is informational — I demand no forced uniform-verdict fix.** None of
this grants provider, compiler, OS or process-isolation qualification.

## 6. The thirty residuals and TCB-SCOPE-01

All 30 rows are individually disposed in `review.json`, keyed by the exact source31 ids. Binding
checks: **30/30 ids**, 0 selector mismatches, 0 evidence paths unresolved, 0 sha mismatches, all
`PENDING`, none `applied`. One row (`RES-EP13-13`) reports `sourceBytesChanged: false` for a file my
27→31 delta shows changing at 27→28; its `previousSha256` equals its current sha, so the claim is
scoped to the package's own predecessor baseline and is **correct in that frame** — not an error.

**TCB-SCOPE-01 is assessed once, as one shared assumption**, with **13** dependent rows. I re-decided
the set on current bytes by reading each row rather than adopting the list: `RES-EP13-13` belongs in it
("fixture isolation only, no process isolation against hostile Python" is the TCB move restated);
`IR-EP13-NB-02` and `IR-EP13-NB-06` do not, because their dispositions hold wherever the boundary is
drawn; no non-declared row rests on the move. **The declared 13 is exactly right.**

As design the assumption is coherent, disclosed and consistently applied. I do not grade it.
**Rejecting or changing this one assumption reopens all thirteen accounts together — never thirteen
independent successes — and would neither repair the historical attacks nor establish containment.**

## 7. Advisories (no MUST, no SHOULD)

- **A-7** — one native annotation record pointer still names `identity-schemas.v2.json` as the owning
  document. Not a SHOULD: all three record pointers resolve on frozen31, and I compared the
  definitions — `owner-source-set` and `import` are **byte-identical** between v2 and v3, so the legacy
  name binds the same record. Cosmetic, and the file is not in this delta.
- **A-8** — the preserved source29 failed receipt is not locatable among the inputs supplied to me
  (searched frozen31, all four root directories, the final31 verification set and every package
  historical directory: zero matches). Not a SHOULD: this is a limit on *my* evidence, not a defect in
  source31. It bounds §3.3 to "current state consistent" rather than a certification of the refresh.

## 8. What this review does not do

Every evaluation, AR, FW, inherited and scoped-owner row carries `appliedByThisReview=false` and
`finalApplicationOutcomeGranted=false`. **All 28** condition-2 obligations retained; **all 32**
qualification gates unperformed and **condition 5 NOT MET**; **all 54** commit-recovery cases
unexecuted. **DR-007 / DR-011-R08**: the successor D9 artifact carrying host-invariant remains a
disclosed, attributed implementation obligation, carried forward and not closed. The original fresh
blind **123/8/3** charter remains a separate requirement — I did not read or touch any blind runtime,
report or output, and I claim no blind acceptance. The final application review is separate.

---

*Machine-readable dispositions — 14 F, 30 evaluation residual, 16 AR, 15 FW, 27 inherited residual and
5 scoped owner rows, each with current owner selectors, current status and limits — are in
`review.json`. Every probe is under `receipts/`, including the six that failed on my own errors: two
incomplete disposable copies, one false load-bearing positive, two runs that misread `PIN-MISMATCH` as
enforcement, an indentation pass that mislabelled six code sites, a checker invoked without
`--stdout`, and a fixture using a TypeScript target kind against a Rust enum.*

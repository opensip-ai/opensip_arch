# Final independent application review — D-372 application-stage.v45.2

**Verdict: CHANGES_REQUIRED**

- **Subject manifest:** `/private/tmp/opensip-design-corrections/application-stage.v45.2/application-subject.v45.json`, SHA-256 `948d9bdd50169ad54871b6816d7f970a2f203fd9b1e84b7bea87dcc5c9ca6757`. It is verified, and byte-equal to the retained copy at `docs/coop/design-corrections/reviews/application-subject.v45.json`.
- **Reviewer:** actual Claude (`claude-opus-5`), acting as a new, fresh final-application origin. I authored none of the subject bytes. I resumed no author, design, blind or coauthor session, used no agents and read no private logs. Everything I wrote is in this runtime: `probes/`, `review.md` and `review.json`.
- **New MUST issues:** none.
- **New SHOULD issues:** one, **APP45-S1**.
- **New advisories:** six (APP45-ADV-01..06).

This review grants no grade, activation, readiness, implementation authorization or product qualification. The reviewed finalizer refuses a non-ACCEPT review, so nothing is applied. The substantive assessments below are evidence for a successor package. They do not extend as acceptance to changed bytes.

## 1. Why CHANGES_REQUIRED

Almost everything verifies on substance:

- custody and normative byte identity;
- the prerequisite reviews;
- the source-pin delta and the reference rerun;
- the finalizer and the three tooling corrections;
- links, the catalog generator and inventory scope;
- D9 carriage and TCB-SCOPE-01;
- the design substance of every condition-2 row.

One application-record accuracy defect remains. It is the same class the prior application review graded M-5.

### APP45-S1 (SHOULD): per-row release-gate routing omits gates the rows' own sources name

Register 08 says the per-row map records each row's "required release gates". For six rows, `readiness-row-map.v1.json` drops gates named by the row's own current successor section, retained inherited account, or retained historical routing. None of these omissions has a per-row disposition.

| Row | Selector | Routed | Omitted | Source naming the omitted gate |
|---|---|---|---|---|
| DR-103 | `/rows/2/releaseGates` | G06, G07, G15, G24, G31 | **G08** | Snapshot register line 291: "admission execution remains G07/G08/G15". The compatible inherited account `/rows/1` is retained. |
| DR-114 | `/rows/12/releaseGates` | G06, G09, G20, G32 | **G12** | G12 is the doctor gate ("Doctor and purge are safe, stable, and honest"). Register line 302: "G12/G32 execution remains". |
| DR-117 | `/rows/14/releaseGates` | G21, G29, G30 | **G09**; also G14, G16, G23 | The row's own successor, admission §5 item 4 (line 344): "G09/G21/G29/G30 must exercise these refusal and authority boundaries". Register line 305 routes the EE classes to G09/G14/G16/G21/G23/G29/G30. |
| DR-119 | `/rows/16/releaseGates` | G07, G13, G22, G30 | **G14** | The retained D-008 fragment: "closure evidence per role at DR-G14 qualification". G14's acceptance restates DR-119's rule. |
| DR-123 | `/rows/20/releaseGates` | G03, G04, G06, G17, G20, G28 | **G01, G02, G05, G12** | The retained D-009 fragment: "DR-G01..G05/G12/G17 carry the evidence". The source evidence includes footprint evidence. |
| DR-124 | `/rows/21/releaseGates` | G11, G12, G18, G19, G20 | **G09** | Register line 312: "G09/G18/G19 execution remains". The inherited account `/rows/11` is retained. |

**How this was found.** Probe `p24_row_gates.py` checks every row against three sources: the gates named in its exact cited sections, in its historical register cell, and in its source cells. The other 22 rows' hits are incidental; for example, workflows §8 names G17/G20 generally, identity §3 names G13, and S11 names G08. DR-131 dropping preview-only G26 is explained, because G26 is historical and routed on DR-122.

**Why SHOULD, not MUST.** No false qualification exists today: all 32 gates are mandatory, unperformed and `qualified:false`. However, a row-level release check would miss a gate, and ACCEPT requires no unresolved SHOULD.

**Remedy (application-only).**
1. Add the omitted gates, or record an explicit reasoned per-row disposition for any gate deliberately not routed (for example, a preview-only EE class).
2. Regenerate the dependent records and the manifest, and rerun the scoped checks.
3. Obtain a fresh final application review.

No contract, schema or model byte changes, so this finding needs no new design review and no new blind consumer.

## 2. Custody and byte identity

- **Package.** The manifest hash matches. All 519 entries (197 files, 76 before-images, 246 support) verify by path convention, with 0 mismatches. The only unlisted file is the manifest itself.
  - All 76 before-image hashes equal `files[].beforeSha256`, and 121 files are new.
  - All 197 live repository paths currently equal their before-state, so preexisting working-tree changes are preserved in `before/`.
  - `application-activation.v1.json` does not exist.
- **Snapshot.** The accepted snapshot has 12,920 entries: 0 mismatches, 0 unlisted files. The design manifest (`8b4efbb0…`) and the archive (`9536ebe3…`) verify.
- **Prerequisite hashes.** These all verify in the repository: design review `427ae73e…`, Codex assent `36830f6e…`, blind review `7ee66bb5…`, Codex blind assessment `d71b8942…`, blind kit `70771536…`, blind custody `490788cb…`, identity counts `e25de4bd…` and reference checks `5dc0de60…`.
- **Semantic sources.** 160 staged files are byte-identical to the accepted snapshot. That covers all product contracts, foundation/workflow contracts, schemas, models, cases and reports.
  - 22 files differ from the snapshot: navigation, decision and register documentation, plus the five pin ledgers.
  - 15 files are absent from the snapshot: application records, the finalizer, the inventories, the generator, and the root and catalog READMEs.
  - No semantic change requires new design or blind review.

## 3. Prerequisites (substantive evidence)

**Independent design review (`427ae73e…`).** Verdict ACCEPT, with 0 MUST and 0 SHOULD.
- Its scope is a nonblind successor review by origin 85a08aec, continuing that origin's own source40–44 reviews; it does not claim fresh-origin independence.
- It carries all 27 inherited rows, the 30 evaluation residuals, the AR and FW items and DR-201..205 as literal dispositions:
  - CONDITION-1-OBLIGATION-RETAINED-ASSESSED;
  - ASSESSED-CONSISTENT-GRADE-PENDING (30 author grades still PENDING);
  - NO-NEW-ISSUE;
  - OWNER-ROUTING-ASSESSED-NOT-EXECUTED;
  - ROUTING-ASSESSED-ONLY-NOT-APPLIED.
- Every row sets `appliedByThisReview:false` and `finalApplicationOutcomeGranted:false`, and TCB-SCOPE-01 is assessed as "NOT REJECTED … final application adjudication not granted".
- I confirmed that all preserved literal dispositions in the application records are byte-for-byte equal to the review rows. I did not turn any of them into a grade by inference; the grades below are my own assessments.

**Codex coauthor assent (`36830f6e…`).**
- `rootDesignAssent:true`, with 0 unresolved MUST/SHOULD, `finalApplicationGranted:false` and `implementationAuthorized:false`.
- The limitation is stated correctly: this is source design acceptance, not application.

**Blind consumer B (`7ee66bb5…`).** A separate actual session (9d3dfb70), continuing its own blind origin. Verdict ACCEPT-RECONSTRUCTABLE, 0 MUST / 0 SHOULD.
- Its kit is normative-only: 107 files, byte-equal to the snapshot, with no Python.
- It uses independently authored `ref/` code and vectors.
- 27 claimed positives were closed from scratch and replayed fresh on source45.
- Unaffected phases reuse exact prior measurements, with custody.
- It records 13 limitations and 16 advisories.

**Root blind assessments.**
- Exact replay: 27/27 ADMIT for transport, structural and semantic admission.
- Query assessment: PASS on 63 capture cases and 66 carrier/parity rows. Token portability is explicitly out of scope.
- Negative query: both declared loss/corruption cases are refused.
- The measurement records correctly carry `rootBlindAssent:false`, and the Codex blind assessment carries `rootBlindAssent:true`.

Normative-kit consumer assertions are not reference replay or product qualification.

## 4. Prior application-review findings (application-review.v1)

| ID | Disposition | What I checked |
|---|---|---|
| M-1 | RESOLVED | `application.v1.json` and `readiness-row-map.v1.json` are staged and applied. 518 links resolve; the 3 activation links are the reviewed output the finalizer writes last. |
| M-2 | RESOLVED IN FORM | All 28 proposed grades are activation-bound, so the register and map no longer contradict. This verdict prevents activation. |
| M-3 | RESOLVED | Condition 3 cites exact review records. DR-201..205 historical cells are kept behind a current prefix, and the literal routing-only disposition is preserved. |
| M-4 | RESOLVED | The 32-gate map is applied and linked from condition 4 and the gate preface. |
| M-5 | RESOLVED for G06/G11 (DR-106 G06+G11; DR-109, DR-113, DR-124 G11) | **The same class recurs for other gates: APP45-S1.** |
| M-6 | RESOLVED on substance | DR-106 adds admission §2/§3, S9.1 and G06/G11. DR-109 adds G11. DR-117's admission §5 maps one-to-one onto file02's seven items. DR-122 has an explicit re-entry act and G17. DR-130's S16 matches 5/5/6. DR-117 gate routing is in S1. |
| M-7 | RESOLVED | The D-372 applying body is staged in COORDINATOR-DECISIONS and bound by activation. |
| S-1 | RESOLVED | Six additional inherited accounts are pinned: the control-protocol v2 whole-file hash; D-012, D-006, D-008 and D-009 verbatim fragments with verified hashes; and the preview boundary v10. |
| S-2 | RESOLVED | `native-evidence.md` cites only `permission-truth-tables.v9.json`. |
| S-3 | RESOLVED | The generator's `--check` returns PASS against the staged classification. |
| S-4 | RESOLVED | The gate table has historical column labels plus a D-372 preface for G06/G10/G11/G17. |
| S-5 | RESOLVED | A forward pointer precedes the dated snapshot. |
| S-6 | RESOLVED | START-HERE has a topic walkthrough through chapters 01/02/03/04/13. |
| A-1 | CORRECTED (inherited defect) | The register anchor now resolves. The row map's JSON `sourceObligation` keeps the old anchor as a verbatim quotation. |
| A-2 | RETAINED LIMITATION | Working-tree-only delivery; commit, push and publication are excluded, and A-2 is not closed by committing. I could not measure git tracking state (the harness denied the call). |

The old external prerequisites P-1..P-6 are superseded by the actual v45 design review, the actual source45 blind consumer B, the recorded D-372 body, the applied records and this review.

## 5. Condition-2 rows (28), individually

Every row's successor section selectors resolve: 193 selectors against real snapshot headings. All 17 compatible inherited selectors resolve to the matching row IDs, and every one of DR-G01..G32 is routed somewhere.

| Row | My assessment | Basis (abridged; full text in JSON) |
|---|---|---|
| DR-101 | ACCEPT-DESIGN supported | S2/S8/S9, native §1/§3/§5, admission §2/§3; `/rows/0`; G01–G05/G07/G22 |
| DR-102 | ACCEPT-DESIGN supported | Native §9 (TS2/Rust3, §9.7 closedWorld), workflows §1/§8; control-protocol v2 retained |
| DR-103 | Substance supports; **row CHANGES_REQUIRED (S1: G08)** | Admission §1/§1.1, S2/S3/S9.1, workflows §8/§9 |
| DR-104 | ACCEPT-DESIGN supported | Identity §2/§3; 45-command closed inventory; D-012; G06/G31 |
| DR-105 | ACCEPT-DESIGN supported | S3/S6/S7/S8/S10–S10.2; workflows §6/§7/§12; truth tables v9 |
| DR-106 | ACCEPT-DESIGN supported | Admission §2/§3, S9.1/S11, identity §3–§5, native §3/§5, workflows §2; G06/G07/G11/G12/G19 |
| DR-107 | ACCEPT-DESIGN supported | S6/S7/S9/S9.2/S15; identity §5; G18/G19/G21 |
| DR-109 | ACCEPT-DESIGN supported | Identity §4/§5, S3.1/S7, workflows §1/§9; G11/G19/G20 |
| DR-110 | ACCEPT-DESIGN supported | S4–S7/S9/S9.2/S11/S14/S15; G07/G08/G18/G22 |
| DR-111 | ACCEPT-DESIGN supported | Identity §3/§5, native §9, S9, workflows §2–§4 |
| DR-112 | ACCEPT-DESIGN supported | S4/S4.5/S5/S6/S9.1/S11; G08/G09/G32 |
| DR-113 | ACCEPT-DESIGN supported | Identity §4/§5, workflows §2/§4/§8/§9; G11/G12/G19 |
| DR-114 | Substance supports; **row CHANGES_REQUIRED (S1: G12)** | S3/S11/S14, workflows §8/§9 |
| DR-115 | ACCEPT-DESIGN supported | Admission §2–§4 (3 warm-ups + 7 runs, 1.20×/1.25×), native §1/§12; D-006 |
| DR-117 | Substance supports; **row CHANGES_REQUIRED (S1: G09; G14/G16/G23 undispositioned)** | Admission §5 items 1–7 ↔ file02 lines 287–293; `boundaryItems=7` |
| DR-118 | ACCEPT-DESIGN supported | Native §1–§4/§6–§9, 66 cells (0 qualified); G10/G13/G14/G23/G25 |
| DR-119 | Substance supports; **row CHANGES_REQUIRED (S1: G14)** | Native §1/§2/§3/§5/§9, S8/S9.1; D-008 |
| DR-120 | ACCEPT-DESIGN supported | Admission §2/§3, native §1/§3/§5/§9, S8/S9.1 |
| DR-121 | ACCEPT-DESIGN supported | Admission §2/§3, native §1/§9, S8 |
| DR-122 | ACCEPT-DESIGN supported | D-372 re-entry act; workflows §8 SARIF parity; inventory v3 SARIF on exactly default/analyze/audit/repair-verify; G17 reactivated |
| DR-123 | Substance supports; **row CHANGES_REQUIRED (S1: G01/G02/G05/G12)** | Workflows §1/§8/§9, S14; D-009 |
| DR-124 | Substance supports; **row CHANGES_REQUIRED (S1: G09)** | Identity §2–§5, S3.1/S7/S9, workflows §1/§6 |
| DR-125 | ACCEPT-DESIGN supported | Workflows §1/§8/§9, S6/S7/S10, native §9 |
| DR-126 | ACCEPT-DESIGN supported | S8/S9.1 four platform IDs = gate `platformFamilies`; native §1/§2/§5 |
| DR-127 | ACCEPT-DESIGN supported | Native §9, S6/S7/S9, workflows §1/§3 |
| DR-130 | ACCEPT-DESIGN supported | S16 (lines 1510–1532): 5 preservations, 5 distinctions, 6 prohibitions matching file05 lines 67–81; S16's gates = the routed set |
| DR-131 | ACCEPT-DESIGN supported | Identity §3–§5, native §4, workflows §1/§5/§8/§9 |
| DR-133 | ACCEPT-DESIGN supported | Native §4/§9, identity §4, workflows §1/§8 |

The excluded rows (DR-108/116/128/129) are D-371's bounded selection, not scope cuts made to obtain completion.

## 6. Inherited rows (27) and evaluation subresiduals (30)

All 11 parent rows (DR-001..011) and all 16 residuals (R01..R16) are individually supported as ACCEPT-DESIGN at design level; the bases are in the JSON. Three need notes:

- **DR-003:** the explicit scoped D-372 timing disposition. Demonstration stays mandatory at G09/G18/G19/G21/G22 and DR-012, with no V10/enforcement claim.
- **DR-007 and DR-011-R08:** these carry the D9 obligation (§8 below).
- **DR-011-R10:** closed by the actual blind result.
  - The requirement is an implementer litmus after final integration.
  - It is met by the normative-only 107-file kit, independent vectors, fresh from-scratch replay of 27 positives, 16 identified inventions or naming freedoms, and root replay 27/27.
  - Limits: the blind origin is a continuation, not fresh on source45, and unaffected phases reuse measurements.
  - The design review's literal "OPEN" remains correct for that nonblind review.

All 30 evaluation subresiduals (19 RES, 7 NB, 4 measured escapes) are individually supported as prospective-product-replacement dispositions, and every historical limitation is preserved. Thirteen are jointly contingent on TCB-SCOPE-01. The author grades remain PENDING as literal history.

## 7. Shared trusted-code assumption: TCB-SCOPE-01, assessed once

**Position: ACCEPTED as an explicit product scope assumption (not rejected, not changed).**

**The assumption:** authenticated selected in-process host/evaluator code is trusted; providers and inert inputs are untrusted; adversarial same-process code is outside the threat model.

**Dependents (13):** RES-EP13-02/04/12/13/16/18, IR-EP13-NB-01/03/04, AX6, AX9, MD5 and RX2c. This list is identical in the accepted design account, the root/Codex account and the design review's `sharedDependency` field. DR-011-R12 reopens with it as well.

**Why it is coherent:**
- Admission §5 items 3–5: providers produce only facts/Coverage; no untrusted native/WASM; no imperative hooks.
- Security S10: repository code is a separately authorized trusted principal.
- Native §9/§9.7: provider process and wire boundaries, and a host-minted closedWorld.
- DR-G21 "does not claim security confinement".
- The measured in-process law mutability is explicitly out of scope.

**What it does not claim:** repaired historical attacks, in-process containment, or native/host/platform qualification (G02/G07/G09/G21/G22 are unperformed).

**Consequence:** if the assumption is rejected or changed, all dependents reopen **jointly**. It is one assumption, not thirteen independent successes. The source reviewer did not grade it; this is my assessment, and it is not effective under this verdict.

## 8. D9-APP-1

- **The historical assessment** was by an actual Claude bounded assessor (session 9a209c44, claude-opus-5, source20). It was **not a Grok session**. It raised a SHOULD for row-specific visibility, executed no integration checks and did not conduct final application review.
- **Codex's qualified assessment** corrected the broad absence premise: CB-ADV-4 was copied by the source20 assembler. Codex also classified the implementation-phase label as a planning classification.
- **Current generated records.** A `carriedCrossUnitObligation` exists on exactly DR-007 (`/parents/6`) and DR-011-R08 (`/residuals/7`).
  - It names the owner (the D9 exit-contract unit) and the exact mapping (host-invariant → existing SYSTEM.OUTCOME.ILLEGAL_STATE).
  - The inherited artifact hash `8dd33038` is verified.
  - `notDischargedBy` names condition 1, ACCEPT-DESIGN, the application, activation and the final review.
- **Selectors verified.**
  - The route registry obligation resolves, and says "Nothing in the product source" is owed.
  - `D9FaultCause` has 12 members: the inherited 11 plus host-invariant.
  - The v1.14 enum has 11 members, and ILLEGAL_STATE has no cause preimage.
  - `check-integration.py` lines 381–394 enforce all three halves.
  - Workflows §9 and the native route table map host-invariant.
- **Completeness.** The selected current composition is **complete**. Future owning-unit artifact publication, integration and qualification are **not** complete; they remain mandatory, live and undischarged, and this review does not discharge them.
- **Classification.** The phase label is a planning classification. D9 is not a design-level blocker. D9-APP-1 is **RESOLVED** in the current records.
- **Precision note:** CB-ADV-4 is absent from the current `accepted-review-advisories.v1.json`. Its current equivalents are blind advisory A-c2 and the row records (APP45-ADV-06).

## 9. Scoped owners DR-201..205, AR-01..16, FW-01..15, 32 gates, F-01..F-14

**DR-201..205.** Each keeps its literal ROUTING-ASSESSED-ONLY-NOT-APPLIED disposition; no historical grade is extended. My subject-specific assessment supports ACCEPT-DESIGN for each:
- DR-201 (semantic correctness): closedWorld law, blind and root replay, D9 carried.
- DR-202 (delivery/operations): S9/S9.2/S10.2/S15 and commit-recovery v3; 54 recovery cases unexecuted.
- DR-203 (prototype lessons): S16 and 24 report-inventory dispositions; G13 unperformed.
- DR-204 (V1/coop invariant coverage): all application pins resolve, the ledger deltas are exact, and 79 review selectors resolve. APP45-S1 is recorded against the rows.
- DR-205 (small core/components): admission §5 and TCB-SCOPE-01.

**AR-01..16.** Each is supported against its contract selector, and the AR tags appear in the headings (S3 AR-03, S4 AR-04, S5/S6 AR-05, S8 AR-06, native §3/§5 AR-07, workflows §1/§6/§7 AR-08, workflows §2 AR-10, §3/§4 AR-11, native §4 AR-12, native §1/§6 and workflows §8 AR-13, S7/S9 AR-14, workflows §8/§9 and S11 AR-16). AR-02 and AR-09 use numeric identity and admission sections. The literal NO-NEW-ISSUE disposition is preserved, and ADV42-01 and ADV44-01 are carried.

**FW-01..15.** Each has a row in the current source map with a concrete contract, plus an owner module and milestone (for example, analysis.rs M3 for FW-03 must mint the published closedWorld). Each is supported at design and routing level; none is executed.

**Gates.** All 32 have an acceptable design-contract mapping, with required product qualification unperformed (`qualified`/`demonstrated`/`harnessAuthored` all false).
- G06/G11 historical "BLOCKED/HARD-BLOCKED" cells are reconciled by the preface and current contracts.
- G10 now reads TS major 2 / Rust major 3, with the inherited claim kept.
- G17 is reactivated, with the historical drop text kept.
- G26 is preview-only history.

**F-01..F-14.** The provenance chain is intact: the v36 review record (v31 → 33 → 36), then root-independent36 verification (11 RE-VERIFIED-ON-PACKAGE13; F-04, F-07 and F-09 INHERITED; baseline fields exact, authority flags false), then the source45 design review (CARRIED-NOT-REGRADED). The source45 checks do not retroactively rerun the original F evidence, and no application record grades or re-verifies them.

## 10. Advisories and accounts

**New advisories:**
- **APP45-ADV-01.** The preserved `workflows-report.v1.json` embeds the old workflows ledger hash (`6e75029f`).
  - The rerun regenerated a report that differs only in that field (b607db8a vs accepted bc84b7dc).
  - The only disclosure is the rerun hash; the recording delta covers only the native report.
  - The report itself is lawfully preserved.
- **APP45-ADV-02.** The design-corrections README chronology keeps level-1 headings, "Current:" lines and a historical commit/push sentence (line 33) inside the historical section.
- **APP45-ADV-03.** The "fresh" wording for blind consumer B disagrees with the disclosed continuation origin.
- **APP45-ADV-04.** The finalizer's resume path does not handle a torn write. It fails closed; recovery is manual from `before/`.
- **APP45-ADV-05.** The applying D-372 body makes precision corrections to the wording of the pinned proposed act: identity profile 3 vs 2, and §8/§9. Both are consistent with accepted sources.
- **APP45-ADV-06.** The CB-ADV-4 provenance described above applies to the historical account, not the current records.

**Existing accounts:**
- **Design review advisories:** ADV42-01 (analysis.rs verification obligation) and ADV44-01 (optional planning binding), both carried. Historical CLAUDE-V13-ADV-1 (60 → 66 cells, equality verified) and CLAUDE-V13-ADV-2 (crate-size illustration) are preserved.
- **Design review observations:** OBS45-02, 04, 08 and 10 remain material limitations.
- **All 16 blind advisories** (A-c1 … A-s45-1) are carried non-blocking. The application accounts equal Codex's `newAdvisoryApplicationAccount`, and I assessed each (JSON).

## 11. Documentation, links, inventory

- **Current account.** The root README, START-HERE, architecture README, register unified section, current source map, design-corrections header, file 12 and the eleven chapter banners agree on the same account:
  - one complete intended product design, implemented in stages;
  - D-369 is historical;
  - conditions 1–4 hold at design level only after activation;
  - condition 5 is NOT MET.
- **Links.** 518 local links and anchors resolve, with 0 failures. The three activation-target links point at the reviewed output that the finalizer creates last. None is represented as existing evidence.
- **Catalog.** The generated catalog reproduces from the classification.
- **Inventory.**
  - 135,218 rows, of which 126,015 scoped D-372 content paths are all present with after-image hashes.
  - Exclusions: the activation, NEXT-REVIEW, and the two inventories. The late-evidence prefix is `application-review.v45/`.
  - Historical `referencedBy` samples are preserved, separate from `currentNavigationReferences`.
  - This is hash accounting, not exhaustive inbound counting.
- **Design artifacts.** Layout, naming, build planning and the 54 planned recovery cases are design artifacts. The 32 product gates and 54 recovery cases are unperformed.

## 12. Source pins, reruns, reproduction, tooling, finalizer

**Five-ledger delta.** The foundation, security, native and workflows ledgers each change 3 entries (the documentation applicability pointers for files 03/10/13). The evaluator3 ledger changes 7: the 3 pointers plus the 4 ledger hashes. This exactly matches `native-recording-delta.v1.json`. Every staged ledger entry matches the post-application tree, files 03/10/13 differ from the snapshot only by the recorded paragraph, and nothing historical is repinned.

**Rerun.** All 7 commands exit 0 with their sources unchanged.
- Native: 477/477.
- Foundation, identity, security and integration reports are byte-equal to the accepted execution.
- Evaluator3 differs only in paths. Workflows: see ADV-01.
- The integration checker (`6102bfdf`) is authenticated by its whole-subject manifest entry; report `e6988c6a` is byte-equal.

**v12-A1 (count account).**
- Selected measurement: 1596 passing calls, 1584 distinct IDs, 12 duplicate extra instances.
- My independent recount of the identity report gives the same numbers: closed-closure ×7 and exact-version-closure ×7.
- `application.v1.json#/referenceEvidenceSummary` matches. The v12 figures 767/757/10 are historical only.

**v12-A2 (reproduction).** For all 7 commands:
- the source hash matches the snapshot and the original record;
- normalizing the historical absolute source path plus `recordedOutput` → `reproductionOutput` reproduces the argv exactly;
- outputs are relative and distinct.

**Tooling corrections.**
- **Review shape (22 controls).** The strict map/array adapter refuses duplicates, conflicts, pointer injection and missing collections. It resolves to original array pointers, and the kit parent alias is explicit. I independently confirmed 79 selectors resolve to the matching IDs and all literal dispositions are equal.
- **Summary source.** It now reads the snapshot summary `43f3eb80`, not the divergent live file `e36dcfe4`.
- **Reproduction.** Only output flags are rewritten; there are 3 refusal controls.
- **Current helpers** are byte-equal to the corrected versions.

**Final-records corrections.** All four before/after hashes verify, and each change is application-only.

**Root preflight.** It distinguishes the 77 individual pointers, the 15-row FW collection and the separate R10 blind `/verdict` pointer.

**Finalizer.** The procedure is sound.
- It checks the review hash, `verdict == ACCEPT`, `newMustIssues`/`newShouldIssues` as empty lists, and a matching `subjectManifestSha256`.
- It checks safe paths, staged hashes, live before-images or exact after-images, and retained custody before any write.
- It writes activation last and never overwrites an existing activation.
- The self-test passes 20/20, including CHANGES_REQUIRED refusal.
- The hash-cycle design is coherent, because no review hash is embedded in its own subject.
- **Under this verdict the finalizer refuses to apply.**

## 13. Limitations

- **Reading scope.** I read every staged Markdown edit, the D-372 body, the named contract sections and all application records (through structured dumps). I did not read the full contracts or the 94/88 MB inventories line by line; I verified them byte-identical or probed them structurally.
- **Reference suites.** I did not re-execute them. I compared the retained rerun byte-for-byte against the accepted execution, and I did run the catalog generator check.
- **Git tracking (A-2)** was not measured.
- **Historical archives and chronology** were sampled, not re-reviewed.
- **No acceptance** from this review extends to a successor package, which needs its own fresh final application review.

## 14. Final re-verification

After all probes and before writing, I re-ran `p22_reverify.py --snapshot`:
- manifest `948d9bdd…` matches;
- 519/519 entries match, with 0 unlisted;
- 0 live paths differ from their before-state;
- activation is absent;
- 0 snapshot mismatches;
- the prerequisite hashes match.

A post-write re-verification is recorded in `review.json#/finalReverification`.

**Verdict: CHANGES_REQUIRED** — `subjectManifestSha256 = 948d9bdd50169ad54871b6816d7f970a2f203fd9b1e84b7bea87dcc5c9ca6757`.

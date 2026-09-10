# Independent design/reference review — corrected candidate v5

**Verdict: ACCEPT** (design layer only)

Reviewer: actual Claude (Opus 5), fresh independent reviewer session. I authored none of
the subject bytes. This is not blind consumer B, not application acceptance, and not
product qualification. Condition 5 remains NOT MET.

This review supersedes nothing in the retained v4 review; it binds the whole v5 subject.

---

## 1. Custody

| Item | Value |
|---|---|
| Manifest | `docs/coop/design-corrections/reviews/candidate-subject.v5.json` |
| Manifest SHA256 | `ccb2311ddbcaea7e8bd540030621c982fa6757792721095a505e4e47652c74cf` |
| Required SHA256 | `ccb2311ddbcaea7e8bd540030621c982fa6757792721095a505e4e47652c74cf` — **match** |
| Declared predecessor | `2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2` (v4) — **verified present and matching** |
| Snapshot | `/tmp/opensip-design-corrections/candidate-subject.v5` |
| Files | 1419 declared / 1419 verified / 1419 on disk |
| Bytes | 14,259,899 declared / 14,259,899 verified |
| Mismatched / missing / undeclared-on-disk | 0 / 0 / 0 |
| Verified | **before and after** review (`probes/verify_custody.py`; `scratch/custody-before.v2.txt`, `scratch/custody-after.v2.txt`) |

The subject is closed in both directions: every declared file exists with the declared
digest, and no file exists in the snapshot that the manifest does not declare. The v4
snapshot was independently re-verified (1378/1378) so that the v4→v5 diff is trustworthy.
The v4 review retained in the subject is byte-identical to the repository copy, and its
digest matches the one the v5 dispositions cite
(`2b703388c4c2ba24f5bbc557167803d4698d60d921bac097fc1fa13cf50b3851`).

I wrote only under `/tmp/opensip-design-corrections/post-reset-review.v5`. The snapshot,
its manifest and the repository were not edited or repinned. The scratch copy of the
subject was re-verified against the manifest after all five suites ran: 0 mismatches.

## 2. Complete v4 → v5 changed-file inventory

41 added, 0 removed, 20 modified, 1358 unchanged.

**Added (41)** — none normative. 39 are the retained v4 review artifacts
(`reviews/post-reset-review.v4/**` plus `reviews/candidate-subject.v4.json`); 2 are the new
`post-reset-dispositions.v5.proposed.json` and `historical-preservation-report.v5.json`.
No added file is a product contract, unit model, schema or case file (F7, F7b).

**Modified (20)**, all of which I inspected:

| File | Nature |
|---|---|
| `workflows/workflows_model.v1.py` | renderer: SARIF sourcing (1 line) |
| `workflows/command-inventory.v1.json` | parityFields for audit/repair-verify; ordering for default/analyze; sarif `parityRule` prose |
| `workflows/schemas/command-inventory.schema.json` | new `if formats contains sarif → then parityFields contains …` conditional |
| `workflows/workflow-cases.v1.json` | +3 render cases (default, audit, repair-verify) |
| `workflows/check_workflows.v1.py` | SARIF content assertions, 28 omission negatives, coverage check |
| `security/security_lifecycle_model_v1.py` | +20 lines, one contiguous additive hunk in `discovery()` |
| `check-integration.py` | lane-suffixed retention ids, operational 1024/1025 path, 5 discovery negatives, uniqueness assertion |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | §8 SARIF parity paragraph; new FW-11 section |
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` | S3 closed host-observation vocabulary |
| `docs/v2/contracts/product-v1/native-evidence.md` | §10 boundary-code row (1 line) |
| 4 × `source-pins*.json` | re-pinned to current bytes |
| 4 × report/summary files | regenerated; `README.md` v5 section |

Confinement verified: foundation and native units are unchanged except their pin files
(F2, F3); the security unit changed only in its model and pins (F4); the workflows unit
changed only in the eight expected files (F6); identity model, identity schemas and the
identity contract are byte-identical to v4 (C2f); the public detail registry is
byte-identical to v4 (F5); all seven governance artifacts are byte-identical (D3); of the
six product contracts only three changed (D2).

## 3. Reference suites and report reproduction

All five suites re-run in scratch from the verified copy, all exit 0:

| Suite | Count | Declared | Reports byte-identical |
|---|---|---|---|
| foundation | 397 checks, 1091 pins | 397 / 1091 | 5/5 |
| security | 444 cases + 9 sweeps | 444 + 9 | 1/1 |
| native | 101 cases, 60 matrix cells, 0 qualified | 101 / 60 / 0 | 1/1 |
| workflows | 1253 checks, 45 commands, 43 goldens | 1253 | 2/2 |
| integration | 319 checks, 319 distinct ids | 319 | 1/1 |

**All ten reports reproduced byte-identically** (`probes/report-comparison-final.json`).
Seven are also identical to the v4 rerun; the three that differ (workflows ×2,
integration) differ exactly where the delta touched.

The count movement is exactly reconstructible, with no unexplained checks (G1, G2):
workflows 1206 → 1253 = 28 schema negatives (4 commands × 7 fields) + 1 coverage check +
15 checks from the 3 new render cases + 3 SARIF checks retrofitted to the pre-existing
`analyze` case = 47. Integration 311 → 319 = 10 added ids − 2 replaced duplicates = 8.

These are reference tests, not qualification. No OS, compiler, crypto, SQLite or
end-to-end product measurement was performed or is implied. Synthetic signatures, host/OS
observations, evaluator callbacks and locks are stated TCB assumptions throughout.

## 4. Prior issue dispositions

### MUST-A(v4) — SARIF parity — **CORRECTED**

v4's defect was a *sourcing asymmetry*: `results` read `envelope['parity'].get('findings', [])`
(unfiltered, defaulting to `[]`) while `runProperties` read `parity.get('verdict')`
(filtered, defaulting to `None`). Two sources, two silent defaults; audit and repair-verify
emitted a null verdict and an unowned result, and three of four commands had no case.

v5 collapses both to strict indexing on the one filtered declared projection:

```python
return {'format': 'sarif', 'parity': parity, 'results': parity['findings'],
        'runProperties': {'verdict': parity['verdict'], 'deficiency': parity['deficiency']}}
```

I verified the corrected join with my own probes rather than by cross-renderer equality,
which v4 correctly identified as self-consistent but insufficient (19 probes, group A):

- **A1/A2** — SARIF is advertised by exactly `default`, `analyze`, `audit`, `repair-verify`,
  and all four declare all seven common fields (`run-id`, `verdict`, `required-coverage`,
  `deficiency`, `findings`, `termination-class`, `retention-disclosure`).
- **A3** — I built the schema registry independently (plain `Draft202012Validator` +
  `referencing`, not the subject's `ExactValidator`) and ran **28 negatives**: every single
  omission of every common field from every SARIF command is rejected; all four unmodified
  rows are valid. **A3b** — the rule is correctly scoped: removing `run-id` from a
  non-SARIF command is not rejected by it.
- **A4 — the discriminating probe.** I injected undeclared keys (`SECRET-undeclared`,
  `findings-shadow`) into `envelope['parity']`. None reaches `results`, `runProperties`,
  `parity`, or anywhere in the serialized rendering, for any of the four commands. This
  distinguishes filtered from unfiltered sourcing; the reference render cases cannot,
  because they construct `parity` exactly from `parityFields` (A14, raised as ADV-4).
- **A5/A5b** — **12 fabrication negatives**: dropping `findings`, `verdict` or `deficiency`
  from the host projection raises `KeyError` for every command; nothing renders. The exact
  v4 counterexample — a SARIF row lacking findings/verdict/deficiency — is rejected by the
  schema *and* refuses to render.
- **A6/A6b** — audit declares the analysis findings and deficiency alongside
  `baseline-id`/`comparison-id`/`comparison-counts`, and emits a real verdict and real
  findings where v4 observed `x-verdict` / `null` / an unowned single result.
- **A7/A7b** — repair-verify declares the common fields plus `applied-snapshot-id`,
  `verified-snapshot-id`, `snapshot-matched`, `targets-remaining`, `net-new-findings`, and
  emits a real fresh-Run verdict where v4 observed `null`.
- **A8** — one declared projection is shared by every advertised renderer of all four.
- **A9** — render cases exercise every advertised SARIF command.
- **A10** — an empty findings array renders `[]` and is distinguishable from an absent
  field, so an empty result is never inferred from a missing projection field.
- **A11** — an ephemeral `run-id` projects `null` without minting Run authority.
- **A12** — the same seven field names appear in prose, schema, inventory rows and checker.
- **A13/A13b** — no advisory command advertises SARIF; a non-applicable request refuses
  `OUTPUT.FORMAT_NOT_APPLICABLE`.

The renderer, inventory, schema, prose and all four command cases agree. D-372's unchanged
claims remain true against the corrected inventory (D3b, D3c), and DR-G17's threshold
"omission only by not advertising applicability, never by silent semantic loss" now holds
in the inventory rather than being contradicted by it (D4b).

### ADV-a(v4) — unique integration identifiers — **CORRECTED**
319 checks, 319 distinct ids, no duplicates. Both retention-loss lanes are separately
identifiable (`…-blobs`, `…-objects`), the lane name matches the map actually left empty,
and the checker now asserts its own identifier uniqueness (B1–B1d).

### ADV-b(v4) — 1024/1025 roots through the composed path — **CORRECTED**
The new `operational-scope-1024` / `operational-scope-1025` checks drive real security
discovery → admitted boundary inventory → native scope over one coherent host-observed
marker/filesystem inventory, not the standalone `unit_scope_descriptor` instrument. 1024
asserts a positive admitted size of exactly 1024; 1025 asserts exit 2 and the exact typed
subject `workspaceRoots:1025>1024`. The standalone unit evidence is retained alongside
(B2–B2e).

### ADV-c(v4) — canonical boundary-code prose — **CORRECTED**
The native §10 row now reads `native.explicit-root-without-marker` (missing marker);
`PROJECT.EXPLICIT_PATH_INVALID` (grammar or boundary crossing) — one canonical code stated
once for the two conditions that share it, instead of the A/B/B positional reading (B3).

### ADV-d(v4) — numeric metric comparability — **CORRECTED**
The owning workflow contract now restates the restriction: same metric definition, supplied
diff scope and comparison base; incompatible inputs reported incompatible, never presented
as an improvement; typed scope/policy/waiver/evidence deltas distinct from code changes;
redistribution is not behavioral improvement. It names architecture 13 §6 as the inherited
owner rather than forking it, and the source-map FW-11 row is unchanged (B4, B4b, D5).

### ADV-e(v4) — discovery host-observation seam — **CORRECTED**
`discovery()` now admits a closed key set before reading anything. I ran **25 negatives**
(unknown key, misspelled key, each of four missing required keys, bool-as-uid, string-as-uid,
negative uid, non-dict `fs`, non-string `accountHome`/`cwd`, string/int `ci`, int/string
`trustProjectOwner`, non-list `authorizedGroupIds`/`explicitJoins`/`configWorkspaceRoots`,
bool/string/negative group members, non-string `explicitProject`/`explicitResolved`,
non-dict input) — every one refuses `DISCOVERY_OBSERVATION_SHAPE`. I ran **8 positives**
covering every optional key with a correct type — all still admit, and the minimal
older-shape observation still succeeds with no regression (B5, B5b, B5c).

The seam is correctly bounded: `_int` rejects bools explicitly (B5f); the token is absent
from the public detail registry, the command inventory and the native contract, so it mints
no public request carrier or D9 code (B5d, E7d); the contract states it is an instrument
error and that the lstat/ACL map remains a synthetic trusted observation, not proof of
native custody (B5e); and the gate reads no environment variable, `PATH` or `HOME` (C3d).
The security-model change is a single contiguous additive hunk with zero lines removed or
altered, touching no execution/authorization function (E7–E7d).

## 5. Cross-unit regression account

- **Default discovery** — still admits with no explicit root, no `ci`, no groups; still
  deterministic over identical observations; CI discovery still admits (C3–C3c).
- **Nested boundaries / explicit Cargo** — 9 boundary/nested checks present and passing;
  the native unit is byte-unchanged apart from pins, so v4's evidence carries with proof
  (C4, F2).
- **Public detail vocabulary and required-output failure** — the registry is byte-identical
  to v4; the v5 prose adds no new public D9 code to the workflow contract; post-commit
  required failure keeps the committed `runId` and exits 4; every renderer still declares
  `operational-failed` (C5–C5d, F5, F5b).
- **Source-pinned source closure** — all four pin sets resolve to current bytes
  (1091 + 64 + 66 + 57), with no cross-suite disagreement on a shared path, and every
  changed normative/model/schema/case file is pinned (B6, B6c, B6d).
- **No silent execution authority** — no command changed `repositoryExecution`,
  `writesTrackedIntent`, `authority`, `authorizationClass` or `advisory`; audit and
  repair-verify remain non-executing despite gaining analysis fields; no command, step,
  flag, format or requestClass was added or removed; 45 commands before and after
  (C6–C7, C8d).
- **Semantic identities unaffected by output/operational fields** — the identity domain
  registry is closed (an output-shaped domain refuses `IDENTITY_DOMAIN`); none of its 18
  domains is an output/operational domain; no domain schema admits an output-projection or
  operational field; the `run` domain carries no exit code, renderer or delivery field; the
  derivation reads no output field name. The `verdict` present in `proof-bundle`,
  `evaluation-seal` and `policy-derivation` is the sealed **semantic** verdict — a closed
  `pass`/`fail`/`indeterminate` enum, legitimately identity-bearing — not the output
  projection, and those schemas are byte-identical to v4, so nothing moved in the delta
  (C2a–C2f, C2c–C2c5). The `verdict` mention in the identity model is solely the
  `VERDICT_JOIN` consistency guard.
- **Inventory delta bounds** — with `parityFields` and the SARIF `parityRule` text removed,
  the command inventory is *exactly* equal to v4; `sarif` is the only renderer row changed;
  no parity field was removed from any command anywhere; `default`/`analyze` changed by
  ordering only (C1–C1c, C8–C8d).

**Prior v4 probe errors and supersessions** were not treated as product failures; I used
v4's final substantive findings only, and independently re-derived every one I relied on
where the bytes changed.

## 6. New findings

**No new MUST. No new SHOULD.** Five advisories, none of which is a required design gap:

- **ADV-1(v5)** — `D-372-corrections.proposed.md` line 80 cites "Workflow §9's declared
  parity fields … and post-commit required-output failure law". Declared parity fields are
  owned by §8 ("Command inventory, outputs and parity"); §9 is "D9 goldens and typed
  detail" and carries only the golden table row for the delivery failure. The bytes are
  unchanged from v4 and the law itself is determinate and correctly owned; only the section
  number misdirects a reader of the very document MUST-A named as an owning selector.
  Selector: `docs/coop/design-corrections/D-372-corrections.proposed.md` §"Explicit product
  and output re-entry acts".
- **ADV-2(v5)** — `reviews/NEXT-REVIEW.md` ships inside the v5 subject still describing the
  **v4** review as active, citing manifest `2a2168c3…` and counts `workflows1206`,
  `integration311`. It is non-normative, not source-pinned, and the authoritative
  `validation-summary.v1.json` is correct and current (1253 / 319 /
  `PENDING-FROZEN-V5`), so there is no normative contradiction — but it is the designated
  resume pointer, and a reader who trusts it gets stale counts and a stale manifest.
  (Probe D.D7; D7b confirms the authoritative file is current.)
- **ADV-3(v5)** — `check-integration.py` is covered by no source-pin set, while all its
  model inputs are pinned. Pre-existing: it is equally unpinned in v4, and the four
  source-pinned suites are the pinned units by design. Flagged so the choice is explicit
  rather than incidental. (Probe B2.B6c.)
- **ADV-4(v5)** — the reference render cases construct `parity` exactly from
  `parityFields`, so filtered and unfiltered sourcing produce identical values in the case
  data. The reference suite therefore could not have caught the v4 defect and would not
  catch a regression back to unfiltered sourcing; my A4 probe supplies the discriminating
  input. Test strength, not a design gap: the model is now single-sourced and the schema
  enforces declaration at admission. Consider adding one case with an undeclared key in the
  envelope projection. (Probe A2.A14.)
- **ADV-5(v5)** — a declared parity field absent from the host projection raises an untyped
  `KeyError`. This satisfies the MUST — the failure is loud and nothing is fabricated — but
  §8 states that results and run properties are taken from the declared projection without
  stating that the projection must be *total* over `parityFields`, or which internal fault
  class a violation takes. One sentence would close it.

## 7. AR-01..16 account

Where the owning bytes are unchanged from v4, I verified that fact by digest and carry v4's
independent evidence; where the delta touched them I re-derived the disposition myself.

| AR | Disposition | Basis |
|---|---|---|
| AR-01 | ACCEPT | foundation unit byte-unchanged except pins (F3); 397 reproduced; identity model/schemas identical to v4 (C2f); ADV-e now closed (B5*) |
| AR-02 | ACCEPT | product-configuration model byte-unchanged (F1); reports reproduced; 0 qualified cells |
| AR-03 | **ACCEPT** (was ACCEPT-with-advisory) | ADV-b closed by the composed 1024/1025 path (B2–B2e); ADV-e closed (B5–B5f); security delta purely additive (E7–E7d) |
| AR-04 | ACCEPT | 9/9 sweeps reproduced byte-identically; security report identical to v4 |
| AR-05 | ACCEPT | sweeps reproduced; revocation/root-chain bytes unchanged |
| AR-06 | ACCEPT | security model unchanged apart from the additive gate (E7) |
| AR-07 | ACCEPT | native unit byte-unchanged except pins (F2); 101 cases reproduced |
| AR-08 | ACCEPT | workflow steps/flags/formats/requestClass unchanged (C7); repair/test surfaces untouched |
| AR-09 | ACCEPT | identity model, schemas and contract byte-identical to v4 (C2f); identity report reproduced |
| AR-10 | ACCEPT | baseline/pivot bytes unchanged; comparison cases reproduced |
| AR-11 | **ACCEPT** (was ACCEPT-with-advisory) | ADV-d closed: FW-11 restated in the owning contract without forking architecture 13 §6 (B4, B4b, D5) |
| AR-12 | ACCEPT | native 101 reproduced; §10 row now unambiguous (B3) |
| AR-13 | **ACCEPT** (was CHANGES_REQUIRED) | MUST-A closed: A1–A14, 28 schema negatives, 12 fabrication negatives, 4/4 commands cased |
| AR-14 | ACCEPT | host foundation model byte-unchanged (F1); required-output failure law intact (C5–C5c) |
| AR-15 | ACCEPT | policy/review bytes unchanged; workflows report reproduced |
| AR-16 | **ACCEPT** (was CHANGES_REQUIRED) | MUST-A closed; ADV-a closed (319 distinct ids, B1–B1d); ADV-c closed (B3); registry byte-identical, no new public code (C5d, F5) |

## 8. FW-01..15 account

FW-01 zero-config/recommend, FW-02 clones, FW-03 native semantics, FW-04 richer evidence,
FW-05 delta gate, FW-06 determinism, FW-07 coherent workflow, FW-08 omissions,
FW-09 candidate→inspect→review, FW-10 repair evidence, FW-12 bounded review,
FW-14 real configuration corpus and FW-15 policy authoring/test are **ACCEPT**: their
owning bytes are unchanged from v4 (verified by digest — foundation and native units whole,
identity model/schemas/contract, admission and identity contracts, public detail registry,
all seven governance artifacts), their suites reproduced byte-identically, and the delta is
confined to the SARIF surface, the discovery admission gate and the integration harness.
FW-14 in particular remains honest: synthetic design cases are still not the required
corpus, and no gate was flipped (D4c).

- **FW-11 weakened safeguards / metric redistribution — ACCEPT.** ADV-d closed; the owning
  workflow contract now restates equal metric definition / diff scope / comparison base and
  the redistribution distinction, citing architecture 13 §6 as the binding inherited owner.
  Architecture 13 is byte-unchanged (D1, D1b), so the restatement is a restatement and not
  a fork.
- **FW-13 common registry — ACCEPT.** The command inventory now declares a complete,
  schema-enforced SARIF parity field set; unknown records still refuse; the inventory
  outside `parityFields` and the SARIF `parityRule` is exactly equal to v4; 45 commands,
  43 goldens, 270-code registry byte-identical with internal aliases still distinct.

## 9. Inherited residual account

- **DR-011-R01..R16** — all sixteen carry an individual written disposition (E1). I confirm
  v4's grades for R01–R07, R09, R11, R12, R14–R16 on unchanged bytes.
  **R08 → ACCEPT** (was CHANGES_REQUIRED): the required-output failure law was already
  registered, and the SARIF projection's field set is now determined for all four commands
  (E6). **R13 → ACCEPT** (was CHANGES_REQUIRED): audit determines its SARIF content and
  keeps its comparison account (E6b).
  **R10 remains OPEN BY DESIGN** — the blind consumer-B litmus is a later distinct act that
  this review does not perform and does not prejudge (E1b).
- **DR-001..DR-011 parent rows** — all eleven appear individually; none is contradicted by
  the frozen bytes (E1c).
- **30 evaluation subresiduals** — individually written, all `PENDING`, no containment
  claim (E2). **ACCEPT as prospective.**
- **Six previously unpinned compatibility rows** (DR-102, DR-104, DR-115, DR-117, DR-119,
  DR-123) — every source pin resolves to its declared digest, and each row states a
  retained meaning, a selector and a custody rule rather than a bare pin (E3–E3c). **ACCEPT.**
- **DR-003 timing disposition** — **AFFIRMED AS PROPOSED** on unchanged bytes; still not a
  SATISFIED or DEMONSTRATED claim, still leaves DR-G09/G18/G19/G21/G22 and DR-012 mandatory.
- **Historical preservation** — all 31 historical files verify byte-unchanged in the
  repository, `changed` is empty, and none appears in the v4→v5 delta. The 10 also carried
  in the snapshot agree with both the report and the repository (D1, D1b, D1f).
- **Condition 5** — NOT MET and unchanged. No correction artifact asserts implementation
  authorization, qualification or readiness change anywhere in the subject (E4);
  `readinessChanged` is false; the dispositions file declares
  `independentAcceptance: false` and `implementationAuthorized: false` (D6, D6c, E4b).

## 10. Scoped DR-201..205 dispositions (new, this review owner)

These are **new full-product-scope dispositions by this reviewer**. The historical
2026-08-13 acceptances are untouched, retain their original subjects and digests, and are
**not extended** by anything here.

| Row | Disposition | Reason |
|---|---|---|
| **DR-201** semantic correctness | **ACCEPT** | The identity layer is byte-identical to v4, so v4's independent evidence carries with proof (C2f), and I re-derived the part the delta could have disturbed: the identity domain registry is closed and refuses an output-shaped domain; no domain schema admits an output-projection or operational field; the `run` domain carries no exit code, renderer or delivery field; the sealed `verdict` is a closed semantic enum, not the rendered projection; the derivation reads no output field name. Adding output fields to audit/repair-verify changed no semantic identity. (C2a–C2f, C2c–C2c5, C1–C1c) |
| **DR-202** delivery/operations | **ACCEPT** (was CHANGES_REQUIRED) | The sole condition v4 set — MUST-A — is met. All four advertised SARIF commands declare the same seven common analysis fields; the schema refuses any omission (28 negatives); results and run properties come from one filtered declared projection with no undeclared read and no null fallback (A4); a missing declared field cannot become fabricated valid output (12 negatives); audit preserves the current analysis findings and deficiency; repair-verify preserves the fresh Run's verdict and findings and adds its verification counts; all four commands are cased. The post-commit required-renderer failure law (`DELIVERY.REQUIRED_FAILED` (4) / `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, runId retained, every renderer `operational-failed`) is intact and re-verified. Advisories ADV-4 and ADV-5 attach here and are non-blocking. |
| **DR-203** prototype lessons | **ACCEPT** | Owning bytes unchanged from v4 (security S16, `prototype-evidence-reference.md` and architecture 05 are all byte-identical and outside the delta — D1, D1b, F4). v4's item-for-item check of five preserve obligations, five distinctions and six prohibitions, the pinned prototype commit, and the routing of the corpus to G06/G07/G11/G12/G18/G19/G21 as required future measurement therefore carries unchanged. Nothing in v5 executed the prototype and nothing claims to have. |
| **DR-204** inherited invariants | **ACCEPT** | Every inherited row carries an individual written disposition rather than an aggregate grade (§9), verified myself: 16 R-rows, 11 parent rows, 30 PENDING subresiduals, 6 resolving compatibility pins, 31 historical files byte-unchanged, all four pin sets resolving with no cross-suite disagreement. R08 and R13 move to ACCEPT on the MUST-A correction; R10 stays open by design. The DR-204 precedent is honoured: nothing in the subject accepts its own bytes, and this review supplies the independent oracle for the design layer only. |
| **DR-205** core/components | **ACCEPT** | Owning bytes unchanged from v4: `admission-and-qualification.md` (§5's seven-item P-1/P-2/G3 account), `identity-and-evidence.md` and the native/security sections outside the two-line and one-hunk deltas are byte-identical (D2, D3, F1–F4). The delta added no command, step, flag, format or authority, and audit/repair-verify remain non-executing despite gaining analysis fields (C6–C7), so no component gained host-reserved authority. |

## 11. Probe account

129 probe records across 8 groups, all reviewer-authored and retained with sources and
results. **9 records are superseded corrections of defects in my own probe construction**
(line-wrapped prose not whitespace-normalised; pin paths repository-root relative rather
than suite-relative; a crude substring search over the model source; a normalisation that
compared fields that legitimately changed; conflating the sealed semantic verdict with the
output projection; the preservation report concerning repository rather than snapshot
bytes; a wrong JSON key; an over-strict added-line classifier). **None is a product
failure**; each was corrected in a later file, and prior files are preserved.

**120 live probes: 118 PASS, 2 FAIL.** Both failures are raised as advisories
(ADV-2(v5) coordination-document currency; ADV-3(v5) unpinned integration harness), not as
required design gaps.

Sources and results: `probes/claude-probes-{A2,B,B2,C,C3,C4,D,D2,E,E2,F,G}.{py,json}`,
`probes/probe-index.json`, `probes/delta.json`, `probes/report-comparison-final.json`,
`probes/verify_custody.py`, `probes/verify_v4_snapshot.py`, `run-suites.v5.sh`,
`reports/`.

## 12. Limitations and what this verdict does not grant

- Not blind consumer B. That is a required distinct act and has never run.
- Not application acceptance. The central/navigation application is deliberately still
  pending; I did not treat that pendency as a false acceptance, and I did not accept it.
- Not product qualification. Every synthetic signature, host/OS observation, evaluator
  callback and lock in the subject is a stated TCB assumption. No OS, compiler, crypto,
  SQLite or end-to-end measurement was performed; those remain mandatory release gates,
  and no gate is qualified or demonstrated (D4, D4c).
- Condition 5 remains **NOT MET**. No implementation is authorized.
- Historical 2026-08-13 grades are not extended.
- The reference suites are reference evidence, not qualification.

## 13. Verdict

**ACCEPT** for the design layer, binding the whole v5 subject at manifest
`ccb2311ddbcaea7e8bd540030621c982fa6757792721095a505e4e47652c74cf`.

MUST-A(v4) is closed by an actual correction to the sourcing rule, enforced at inventory
admission and exercised for all four advertised commands; all five v4 advisories are
corrected; the delta is tightly confined, purely additive in the security model, and
introduces no new public code, authority, command or identity input; all ten reports
reproduce byte-identically and every count movement is exactly reconstructible. I found no
required design gap. The five advisories are recorded for the owning selectors and none
blocks acceptance.

Remaining required distinct acts, in order: fresh blind consumer B; a complete final
application package with its own actual independent application review; then application of
accepted documentation/readiness records. Condition 5 stays NOT MET until its own evidence
exists.

## 14. Output paths

- `/tmp/opensip-design-corrections/post-reset-review.v5/review.md` (this document)
- `/tmp/opensip-design-corrections/post-reset-review.v5/review.json`
- `/tmp/opensip-design-corrections/post-reset-review.v5/probes/` (sources, results, index)
- `/tmp/opensip-design-corrections/post-reset-review.v5/reports/` (10 reproduced reports, exit codes, stdout)
- `/tmp/opensip-design-corrections/post-reset-review.v5/run-suites.v5.sh`
- `/tmp/opensip-design-corrections/post-reset-review.v5/scratch/custody-before.v2.txt`, `custody-after.v2.txt`
- Interrupted predecessor preserved at `docs/coop/design-corrections/reviews/post-reset-review.v5-interrupted` (no verdict; no agreement inferred)

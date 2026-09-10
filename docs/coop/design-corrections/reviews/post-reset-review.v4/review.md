# Independent review — candidate-subject.v4 (post-reset, corrected mixed subject)

Reviewer: fresh actual Claude session (`claude-opus-5`). I authored **none** of the subject
bytes; actual-Claude author sessions and Codex did. No agents were spawned. No repository,
snapshot or staged byte was modified; nothing was committed, pushed or repinned.

Standing: substantive independent design/reference review of a FROZEN mixed-author subject.
This is **not** implementation qualification, **not** the blind consumer-B litmus
(DR-011-R10), and **not** an application review. Signatures, OS/custody observations,
evaluator callbacks, fence/lease observations, trust instants and pivot presences are
expressly synthetic TCB inputs and were treated as such throughout; no product qualification
is claimed for any platform.

## Verdict: CHANGES_REQUIRED

Everything the v3 design review and the v1 application review asked for in the design layer
is independently verified as corrected in these bytes: **MUST-A, SHOULD-A and ADV-i..ADV-vi**
are corrected; **N-1..N-5, A-1..A-5, CX-01..CX-07** and every original MUST-1..3 /
SHOULD-1..10 remain corrected; application-review **S-1** and **S-2** are corrected; and the
three substantive new acts I was asked to review — admission §5, security S16 and D-372's
SARIF/G17 re-entry — are real, complete and honest as written, with one exception.

One issue blocks acceptance:

- **MUST-A(v4)** — D-372's explicit SARIF/G17 re-entry act names four commands, but the owning
  inventory and the §8 renderer law do not jointly determine what the SARIF document contains
  for two of them. `repair-verify` is non-advisory, is advertised with SARIF, seals an
  authoritative Run, and yet declares no `verdict`, `deficiency` or `findings` parity field —
  so the reference renderer emits an authoritative SARIF with `verdict: null`. Three of the
  four re-entered commands have no SARIF reference case at all, so no unit or integration
  check can expose it.

One advisory is recorded. All counterexamples are executable and retained under `probes/`.

## Subject and verification

| Item | Value |
|---|---|
| Manifest | `docs/coop/design-corrections/reviews/candidate-subject.v4.json`, sha256 `2a2168c3006174ab5d130054144374698f2026686a0daab7ed1eca38c365c2e2` (**required value matched**) |
| Predecessor manifest | `e3365d6e64cb5b0260ec7261af5c3e554504c9ab9515456f680aeb01b31b76fd` (v3, as declared) |
| Snapshot | `/tmp/opensip-design-corrections/candidate-subject.v4` |
| Pinned files verified | **1378 of 1378** (0 mismatched, 0 missing, **0 files on disk outside the manifest**; 13 384 583 bytes as declared) before review (`evidence/00-manifest-verify.txt`) and again after every suite run and all 114 probes (probe **P82**) |
| Environment | `/tmp/opensip-architecture-review-env/bin/python -I -B`, Python 3.12.13, jsonschema 4.25.1 |
| Scratch copy | `scratch/docs/**` — the four unit checkers and the integration checker write beside their sources and ran there; neither the snapshot nor the repository was written |
| Delta reviewed | 61 added, 33 changed, 0 removed files against v3; every changed model, schema, checker and contract read line-by-line |

## Executed checks

| Check | Result | Where |
|---|---|---|
| Foundation launcher (check-foundation 231, check-identity 124, product-quality 24, product-configuration 18) | **397/397**, source pins valid (1091 files) | `reports/foundation-launcher.json`, `reports/foundation-reports/` |
| Security lifecycle checker | **444/444** cases, **9/9** invariant sweeps, pins valid, 38 output schemas validated | `reports/security-lifecycle-report.rerun.json` |
| Native evidence checker | **101/101** (35 positive, 66 negative), 60 matrix cells, **0 qualified**, 86 closed defs, 0 open objects | `reports/native-evidence-report.rerun.json` |
| Workflows launcher | **1206/1206** checks, 13 schemas, 57 pins valid | `reports/workflows-launcher.json`, `reports/workflows-report.rerun.json` |
| Integration checker | **311/311** | `reports/integration-report.rerun.json` |
| Report reproducibility | all **ten** regenerated reports byte-identical to the retained ones | `reports/report-diff.txt` |
| Counts versus `validation-summary.v1.json` | every claimed count equals the count I reproduced | probe **P44** |
| Source pins across all four units | every pinned path resolves at its pinned digest | probe **P58** |
| Independent probes | 114 probes: **73 OK, 4 counterexamples, 1 advisory, 36 superseded by my own corrected probes** | `probes/probe-index.json` |

Exit codes for all five suites are 0 (`reports/exit-codes.txt`). Counts are evidence that cases
ran; they are not acceptance, and none of them qualifies a platform.

**Honest note on my own probes.** 36 probes are marked `SUPERSEDED`: they failed on *my*
selector or fixture shape, not on the subject (wrong schema file, a `config` key the discovery
input does not have, a regex truncated at 180 characters, a bullet ending in "and"). Each is
superseded by a named probe that re-asks the same question against the correct frozen selector,
and every one of those successors passes. I have retained the failures rather than deleting
them, and `probes/probe-index.json` carries the supersession map. No finding below rests on a
superseded probe.

**Read in full:** the design-corrections README, D-372, the current source map, inherited
residuals, evaluation-residual dispositions, qualification gates, the correction crosswalk,
all three post-reset disposition files, `inherited-row-sources.proposed.json`,
JOINT-INTERFACES, integration issues, all five product contracts and their index, the v1/v2/v3
independent reviews and the v1 application review with their probes, the author v2 handoff and
both Codex technical reviews plus `codex-findings.v2.json` and `permission-head-delta.v1.json`,
the public detail registry, `discovery-defaults.py`, the integration host model, fixture builder
and integration checker, and the relevant definitions in all four units. Architecture files 02,
05, 13 and `prototype-evidence-reference.md` and `COORDINATOR-DECISIONS.md` were read where the
new acts cite them.

## Dispositions of the prior independent design review (post-reset-review.v3)

| Finding | Disposition | Independent basis |
|---|---|---|
| **MUST-A** consent enum disagreement; no `test run` admissible in CI | **CORRECTED** | P1–P5, P8d. `integration-host-model.py:108` now compares `policy-record`; workflows §12 prose now reads `policy-record -> pre-existing-policy`. I built lawful grants myself and composed the real security admission: all **8** (4 platforms × CI/non-CI) policy-record lanes **ADMIT** with `consentSource: pre-existing-policy`; all 4 interactive non-CI lanes admit; all 4 interactive-in-CI grants are refused **at security admission**. The projection's image over real admissions is exactly the closed schema enum `{pre-existing-policy, interactive-consent}` — the v3 constant-value regression is gone. Relabelling refuses in every direction (12 negatives), and the legacy `interactive` spelling refuses. |
| **SHOULD-A** untyped 1025..4096 scope band | **CORRECTED** | P9–P13, P10b. `ScopeRefusal` carries detail `PROJECT.SCOPE_LIMIT`, D9 `request-rejected`/`REQUEST.UNSATISFIABLE`/exit 2, and subject `{field,count,limit}`; the code is registered and in the schema enum; the host projects a valid closed `StepTermination` with subject `workspaceRoots:1025>1024`. 1024 roots admit, 1025 refuse, **nothing is truncated**. The 4096 discovery cap stays distinct (`native.too-many-units` → `PROJECT.WORKSPACE_UNIT_LIMIT`), and 4096 admitted units still hit the scope bound. Both other array bounds (65536) are typed the same way, and all three fields the model reads carry `maxItems`. Native §10 and §14 and security S12 state the outcome and the exact subject spelling. **P10b** additionally drives 1025 roots through the *operational* composition (real security discovery → admitted boundaries → native) and reaches the same typed refusal — the unit and integration cases use the standalone instrument. |
| **ADV-i** three consent spellings, unasserted join | **CORRECTED** | P6e, P7b, P8d. One explicit mapping table in workflows §12 matches all three real closed enums exactly (`Consent.mode`, `TestExecutionStepParams.consentSource`, `RepairApplyParams.consentSource` — the last in `invocation-record.schema.json`). The repair projection now carries both `consentSource` and the admitted `ci`, and `repair_apply` compares both; exhaustively, only 3 of 16 (mode, admittedCi, claimedConsent, claimedCi) tuples pass, and they are the right three. The residue I raised in P8 (the *test* projection carries no `ci`) is **not** a hole: **P8d** shows security itself refuses all 16 grant-ci/invocation-ci disagreements across all four platforms, and `ci` is a real boolean (`1`, `'true'`, `None`, `'False'` all refuse). |
| **ADV-ii** two public codes for conditions the product reports under another | **CORRECTED** | P14, P15b, P16e. `native.boundary-inventory-mismatch` and `native.explicit-root-crosses-boundary` are removed from the public registry and the `DomainDetailCode` enum, are refused as public codes, and are now internal aliases of `PROJECT.DISCOVERY_INVENTORY_MISMATCH` and `PROJECT.EXPLICIT_PATH_INVALID`. Each alias target's class/code/exit agrees with the native internal row, so `public_termination` translates without disagreement. The new public code has a **real host emitter**: three independent inventory-disagreement variants all raise the typed `DiscoveryInventoryMismatch` (`REQUEST.PRECONDITION_FAILED`, exit 2) before native is invoked. The four frozen boundary-crossing discovery cases all refuse first, under `PROJECT.EXPLICIT_PATH_INVALID`. Security S12 and native §14 state both rules. |
| **ADV-iii** dead `reselectsStore` | **CORRECTED** | P18, P17e/P17f. The security model no longer reads it; the closed 11-field intent is `additionalProperties: false` with `fromStoreGeneration`/`toStoreGeneration` required, so it could never have been carried. `core_transition_affected_namespaces` is total over all 20 operation × schema-change × store-change combinations and derives re-selection from the intent alone. The three surviving mentions are the **negative law** ("The caller cannot supply `reselectsStore` or a smaller namespace set"), its integration negative case, and the ADV-iii disposition text — all correct. |
| **ADV-iv** bare `KeyError` on a missing retained blob | **CORRECTED** | P19, P20b. Removing **every** retained object and **every** retained blob one at a time yields exactly one outcome class, `EvidenceUnavailable`, carrying a valid closed `StepTermination`: `operational-failed` / `HOST.IO_FAILURE` / `host-io` / `evidence.missing` / exit **4**. It stays distinct from admission rejection: a corrupt (present but wrong) blob is `BLOB_DIGEST` and a wrong domain is `REFERENCE_IDENTITY`, neither carrying a termination. Identity §4/§5 state the distinction. |
| **ADV-v** recovery-written revisions had no lawful holder | **CORRECTED** | P21b–P25. Over all **36** operation × closed-state combinations, a fresh recovery Attempt binds `installationRecoveryStartRef` to the observed durable revision and `installationJournalRefs[0]` equals it; the last written state always equals the decision's `journalStateAfter`. A PREPARED **store** recovery resumes `PREPARED → COMMITTED → DONE` in one lawful segment (3 refs) while a PREPARED **core** operation aborts (`PREPARED → ABORTED`), which is the S9.2 table. The original abandoned attempt is unchanged and its LEASED revision never appears in the recovery attempt; a foreign start ref, an immutable-field change and an illegal transition all refuse; a non-recovery history must still start LEASED. The `Attempt` schema adds the property with a conditional `required`, admits the recovery pair, refuses an orphan start ref and still admits an initial attempt; the order constraint the schema cannot express is enforced in the workflow observation join. Workflows §12 states the whole rule, including that callers cannot nominate a start ref. |
| **ADV-vi** crosswalk still names a superseded review | **CORRECTED AS PROSPECTIVE** | P46, P59. The crosswalk carries no `ACCEPT` grade; its standing and all rows remain author-corrected/pending. That is the correct pre-application posture, exactly as ADV-vi said. |

Prior-prior findings were re-verified rather than assumed: **N-1** (P15b, P16e, the shared
boundary inventory), **N-2** (P14, P36: registry closed, unique, owner-attributed, at exact
parity with the schema enum, sorted, aliases non-public and pointing at public targets, both
D9 maps covered), **N-3/CX-07** (P27, P28: exact and vcs-mapped imports close; foreign
snapshot, bad mapping, missing mapping, dirty worktree, undeclared build and out-of-set build
all refuse; a duplicate analysis-spec parameter row refuses, so an importer cannot nominate its
own labels), **N-4/CX-01** (P34, and the frozen recovery negatives), **N-5/CX-06** (P21b–P23b,
P55e), **A-1** (P26b: `prepare-code` iff a trusted-repository-code principal, `read-import` iff
the Plan selects imports — all four lanes), **A-2** (P1–P5), **A-3** (P35: an explicitly named
Cargo workspace root reproduces the automatic rows, keeps `memberPackageRoots`, keeps member
`target` pruned; a member alone is its own `cargo-package`), **A-4** (P44, P49: no duplicate
headings, no `/tmp` citation, no dangling relative link in any contract), **A-5** (P15b),
**CX-02** (P33b, P72), **CX-03** (P49), **CX-04** (P69: 1 018 closed patterns scanned across the
schema documents, **zero** `$`-anchored), **CX-05** (P68), **MUST-2** (P37: the same four
machine ids across security `PLATFORM_IDS`, the truth table, the test-execution schema and the
gates file; a display alias refuses; G13 v5 stays a scoped historical harness label),
**MUST-3** (P11).

## Dispositions of the separate application-content review (application-review.v1)

This review does **not** accept the application; that is a later distinct act. Two of its
findings were assigned to the design layer and are dispositioned here.

| Finding | Disposition | Independent basis |
|---|---|---|
| **S-1** six "retain" rows carry no inherited pin | **CORRECTED** | P40b: `inherited-row-sources.proposed.json` carries records for exactly DR-102, DR-104, DR-115, DR-117, DR-119 and DR-123, and every path/digest pin in it resolves against the frozen snapshot at the named digest. |
| **S-2** superseded permission truth table cited | **CORRECTED** | P29, P30: `native/source-pins.v2.json` pins `permission-truth-tables.v9.json` at its real digest, the file is in the snapshot, the native contract cites v9 and no longer cites v7, and Codex's retained `permission-head-delta.v1.json` is present. The contract adds an explicit sentence that the v7→v9 changes concern metadata/recording and the host-under-instruction network recital while the four copied rows are unchanged. The security truth table gives one identical row per machine id and is labelled a design selection, not a measurement. |
| **M-5/M-6** (the DR-117 and DR-130 halves) | **DESIGN CONTENT SUPPLIED** | Admission §5 and security S16; see below. The remaining per-row map work is application scope and is correctly left unassembled. |
| **M-1..M-4, M-7, S-3..S-6, A-1** | **CORRECTLY OUT OF SCOPE HERE** | These concern the final application package. The prior 14-file staged proposal was rejected and will not be applied; P50 confirms the register and navigation documents remain pre-application by design, and `validation-summary.v1.json` still reads `claudeFinalReview: PENDING-FROZEN-V4`, `readinessChanged: false`. I do not treat their absence as a false claim. |

## Substantive review of the three new acts

**Admission §5 — the seven P-1/P-2/G3 boundary dispositions (DR-117).** Complete and
substantive (P38, P52). Seven numbered items, each with a real disposition and **no deferral
phrase**: (1) one signed first-party registry, no marketplace/publisher admission/ecosystem
governance promise; (2) first-party lifecycle parity only, discovery cannot install or execute;
(3) contribution roles bounded to typed facts/Coverage/prepared imports and host-owned steps,
with findings, policy, verdict, persistence, finalization, rendering and termination reserved
to the host; (4) neither untrusted native nor WASM admitted, no sandbox claim, with G09/G21/
G29/G30 required to exercise the refusals and an explicit statement that a synthetic fixture is
not enforcement evidence; (5) no imperative contributions/hooks/root-parser extensions, closed
host inventory, consent to one step never becoming general authority; (6) offline analysis with
no implicit index refresh/download/telemetry/required egress; (7) the G3 substrate named
concretely, including that a management-only installation is not an authoritative closure. The
closing sentence — "this section introduces no new scope cut … a complete boundary selection
now, not a promise" — is the right disposal, and it matches D-371's exclusion set. This answers
the application review's DR-117 gap, which found items 1, 2, 6 and 7 uncovered.

**Security S16 — prototype-user coexistence and transition (DR-130).** Complete and
substantive (P39e, P39f, P53). Measured item-for-item against architecture file 05's
*Migration constraints*: file 05's **five** preserve obligations map one-to-one onto S16's five
numbered items; its **five** distinguish bullets map onto S16's five parenthesised
distinctions; its **six** "No migration silently…" prohibitions map onto S16's six bolded terms
(download, index refresh, lock mutation, replacement historical identity, evidence-meaning
rewrite, telemetry/network requirement). The prototype commit `a62509d6…` is pinned in both
S16 and `prototype-evidence-reference.md`. The two joins the instruction singles out both hold:

- *No-write pre-initialization versus explicit default authoritative invocation.* S16 item 2
  resolves these without contradiction: the prototype's no-write value is preserved through
  `--ephemeral` and metadata-only surfaces, while the product's default authoritative analysis
  remains "the explicitly invoked, disclosed first-write operation of identity §5" that
  distribution migration never invokes implicitly. Both surfaces are real (P51e): `--ephemeral`
  is a declared flag with its own closed `AnalysisResult` member in workflows §2, and the
  command inventory carries `writesTrackedIntent: false` on every analysis-class command, with
  tracked-intent writes confined to exactly the five commands §8 names (`policy-init`, `waive`,
  `baseline-adopt|export|upgrade`). The default command is `firstSourceWrite: true`,
  `writesTrackedIntent: false` — an explicit first write, not an implicit policy-file write.
- *Immutable coexistence and foreign-state refusal.* Stated as the complete transition policy,
  with an occupied root carrying a foreign/prototype marker or schema "refused by the existing
  root/schema admission **before a write**", no prototype Run/baseline/state importer, and
  removal that does not uninstall the prototype or purge by implication. The registered
  `MIGRATION.*` / root-custody codes back it (P53).

The closing paragraph routes the corpus to G06/G07/G11/G12/G18/G19/G21 as required
implementation/release tests and explicitly disclaims having executed the prototype. That is
honest.

**D-372 SARIF/G17 re-entry (DR-122/DR-131).** The act is properly recorded (P42, P65): it
expressly re-enters authoritative SARIF, reactivates DR-G17, supersedes D-077's drop and
D-086's inapplicability *only in this scope*, leaves the historical preview reductions
unchanged, and states that G17 is "an unperformed required product qualification gate after
this application, never an already-passed measurement". The G17 gate row carries a named owner,
harness and current contract with `qualified: false`, `demonstrated: false`,
`implementationHarnessAuthored: false`, as do all 32 rows. The inventory does advertise SARIF
for exactly `default`, `analyze`, `audit` and `repair-verify`, and no advisory command has
SARIF or a verdict parity field. **The act's content is right; what it does not deliver is the
determinate output for two of its own four commands — MUST-A(v4) below.**

## MUST issues

### MUST-A(v4) — the re-entered SARIF surface is not determinate for `repair-verify` or `audit`, and three of its four commands have no reference case (AR-13, AR-16, FW-13, DR-122, DR-131, DR-011-R08, DR-G17)

Evidence (P61, P62, P63, P64; report-shape caveat on P81 recorded below).

D-372 re-enters SARIF for exactly four commands and reactivates G17. Workflows §8 states the
renderer law: `sarif` v1 carries "results equal envelope findings one-to-one, **verdict/
deficiency in run properties**". §8 also states "Each command names its `parityFields`; every
applicable renderer must carry semantically equal values for them." The closed inventory then
declares, for the four SARIF commands:

| command | advisory | declares `findings` | declares `verdict` | declares `deficiency` |
|---|---|---|---|---|
| `default` | no | yes | yes | yes |
| `analyze` | no | yes | yes | yes |
| `audit` | no | **no** | yes | **no** |
| `repair-verify` | no | **no** | **no** | **no** |

Driving the real renderer exactly as `check_workflows.v1.py` drives it (P62) yields:

```
audit          runProperties = {'verdict': 'x-verdict', 'deficiency': None}   results = 1
repair-verify  runProperties = {'verdict': None,        'deficiency': None}   results = 1
```

Three concrete consequences:

1. **`repair-verify` produces an authoritative SARIF with a null verdict.** §6 says
   `repair verify` "seals a new authoritative Run and reports `VerificationOutcome` (applied/
   verified snapshot, targets remaining, **net-new findings**)". A sealed Run has a verdict.
   D-372's own sentence — "advisory-only commands do not gain SARIF or a verdict" — implies the
   converse for non-advisory SARIF commands; `repair-verify` is the single non-advisory SARIF
   command with no verdict parity field (P64). Either the inventory row or the act's sentence is
   wrong, and nothing in the contracts decides which.
2. **SARIF carries data outside the command's own declared parity set, for two commands.** The
   renderer is one expression with two sourcing rules (P63):
   `'results': envelope['parity'].get('findings', [])` reads the **unfiltered** envelope, while
   `'runProperties': {'verdict': parity.get('verdict'), ...}` reads the **parity-filtered**
   projection. So for `audit` and `repair-verify` the SARIF document emits findings that the
   same command's `json`, `human`, `html` and `agent` renderings do not carry, while dropping a
   verdict the Run does have. Cross-renderer parity still "holds" because parity is computed
   over the declared fields only — the checker's `parity_holds` cannot see the asymmetry.
3. **The re-entered surface is almost entirely unexercised.** `workflow-cases.v1.json` has
   three `renderCases`: `analyze` across five formats, `query`-sarif-refused, and `doctor`
   without SARIF. `default`, `audit` and `repair-verify` — the three commands this act newly
   brings back — have **no SARIF case at all** (P61). The workflow checker's only SARIF-named
   check is the negative `inventory.advisory-never-sarif`. No unit or integration check can
   therefore expose 1 or 2.

Why it blocks: this is the "self-consistent but wrong" join the instruction asks for. Each
piece is internally consistent — the inventory rows are well-formed, the renderer law is
stated, parity holds, advisory commands are correctly excluded — but the composition yields an
authoritative output whose contents a blind implementer cannot reconstruct for half the
commands the act names, and G17's qualification harness would be written against exactly this.
It is also the class of defect the corpus has repeatedly rejected: a contract asserting
something about its own subject ("verdict/deficiency in run properties"; "advisory-only
commands do not gain … a verdict") that its own bytes do not deliver.

Owning selectors:
`workflows-and-surfaces.md` §8 "**Renderers.**" paragraph, the `sarif` v1 clause;
`workflows-and-surfaces.md` §8 "Advisory projections never offer SARIF or manufacture a Control
verdict" sentence;
`workflows/command-inventory.v1.json` `/commands` rows `audit` and `repair-verify`
(`parityFields`);
`workflows/workflows_model.v1.py` `render` (the `fmt == 'sarif'` return expression);
`workflows/workflow-cases.v1.json` `/renderCases`;
`D-372-corrections.proposed.md` "Explicit product and output re-entry acts" paragraph, the
sentence beginning "The closed inventory advertises SARIF exactly for default, analyze, audit
and repair-verify";
`qualification-gates.proposed.json` the DR-G17 row.

Return: decide and state what SARIF carries for a command that declares neither `findings` nor
`verdict` — either add `verdict` (and, if net-new findings are in scope, `findings`) to
`repair-verify`'s and `audit`'s `parityFields`, or state in §8 that SARIF `results` and
`runProperties` are sourced from the envelope independently of `parityFields` and that
`runProperties.verdict` is absent (not null) for commands without one. Make the renderer's two
sourcing rules one rule either way. Then add a SARIF render case for `default`, `audit` and
`repair-verify` so the re-entered surface is exercised for every command the act names.

## SHOULD issues

None. Nothing else I probed leaves a design choice unmade for an implementer.

## Advisory

- **ADV-a(v4) (AR-16, FW-13)** The integration report contains **311 checks but 310 distinct
  ids**: `missing-retained-closure-is-typed-operational-loss` is emitted twice by the
  two-iteration loop at `check-integration.py:473` (missing objects, then missing blobs), so the
  two lanes are not separately identifiable in the report and the claimed count is not a count
  of distinct checks (P75). Both lanes do pass — I verified them separately and exhaustively in
  P19 — so this is bookkeeping, not behaviour. Suffix the id with the lane.
- **ADV-b(v4) (AR-03, SHOULD-A residue)** The new 1025-root evidence — the native case
  `scope-1025-first-party-roots-refuses-typed-without-truncation` and the integration checks
  `scope-1024-roots-admitted` / `scope-1025-roots-typed-refusal` — all call
  `unit_scope_descriptor` with `boundaries=None`, which is the standalone instrument that native
  §1.4 U-8 says "an operational host composition must not use". I confirmed in **P10b** that the
  operational join (`admit_repository_discovery` over a real security discovery of 1025 marker
  directories) reaches the same typed `ScopeRefusal`, so the design is determinate; but the
  retained evidence for the newly typed bound never exercises the composed path. Add the
  operational case, as MUST-3 and SHOULD-A both taught.
- **ADV-c(v4) (AR-16)** Native §10's boundary row now lists three conditions and three details
  where two of the three are the same code, so the cell reads
  `native.explicit-root-without-marker / PROJECT.EXPLICIT_PATH_INVALID /
  PROJECT.EXPLICIT_PATH_INVALID` (P83). The mapping is *correct* — that is precisely what ADV-ii
  asked for — but the positional A/B/B reading is easy to misread as a typo. Split the row or
  say once that grammar and boundary crossing share the canonical code.
- **ADV-d(v4) (AR-11, FW-11)** FW-11's numeric-comparability rule ("supplied diff scope and
  comparison base must agree or be reported incompatible") is owned by architecture file 13 §6,
  which the source map keeps binding; the product workflow contract classifies scope deltas but
  does not restate the comparability rule (P72, P79). That is lawful under the source map's
  "existing compatible constraints remain binding through the named source inventory", and the
  34 comparison cases exercise the behaviour. Consider restating it once in the owning workflow
  contract so the current account is self-contained.
- **ADV-e(v4)** `security_lifecycle_model_v1.discovery(inp)` reads its host-observation input
  with `inp.get(...)` and no closed-input admission, so an unrecognised key is silently ignored
  (this cost me two probes). Every field is a host observation rather than request input, and
  the caller-influenced ones are admitted upstream, so no authority follows; but the entry point
  is the one place in the four models where "exact input" is not enforced at the boundary.

## AR obligation dispositions

| AR | Disposition | Basis |
|---|---|---|
| AR-01 exact admission | ACCEPT | P69 (1 018 closed patterns, zero `$`-anchored), P68, P36, P58; foundation 397 reproduced. ADV-e noted. |
| AR-02 authenticated qualification | ACCEPT | P37, P42, P48; product-quality 24 reproduced; 0 qualified cells |
| AR-03 discovery/custody | ACCEPT with advisory | P9–P13, P10b, P11, P15b, P16e, P70, P35; ADV-b |
| AR-04 trust clock/recovery | ACCEPT | 9/9 sweeps reproduced; P34 |
| AR-05 expired root/live revocation | ACCEPT | sweeps reproduced; frozen revocation/root-chain cases |
| AR-06 platform population | ACCEPT | P37 |
| AR-07 sealed inputs/execution boundary | ACCEPT | P1–P5, P8d, P26b, P66; ADV-i corrected |
| AR-08 invocation/repair lifecycle | ACCEPT | P7b, P21b–P25, P34, P55e; ADV-v corrected |
| AR-09 identity/retention closure | ACCEPT | P19, P20b, P27, P28, P67, P71d; identity 124 reproduced; ADV-iv corrected |
| AR-10 runnable prior detector/baseline | ACCEPT | P33b, P72 |
| AR-11 typed comparison/imports | ACCEPT with advisory | P27, P28, P33b, P72, P79; ADV-d |
| AR-12 resolution completeness | ACCEPT | P73; native 101 reproduced, 66 negatives |
| AR-13 cells/discovery/parity | **CHANGES_REQUIRED** | MUST-A(v4) (SARIF parity/surface); otherwise P1–P5, P37, P51e |
| AR-14 stage transition/concurrency | ACCEPT | P17e/P17f, P18, P21b–P23b, P55e; ADV-iii corrected |
| AR-15 current narrative | ACCEPT | P46, P49, P50, P59, P77d |
| AR-16 provenance-specific remedies | **CHANGES_REQUIRED** | MUST-A(v4) (the SARIF/G17 output act); ADV-a, ADV-c; otherwise P14, P15b, P16e, P32e, P36 |

## Fallow constraint dispositions

FW-01 **ACCEPT** (P51e, P70; SHOULD-A corrected). FW-02 ACCEPT. FW-03 ACCEPT (P73).
FW-04 ACCEPT (P27, P28). FW-05 ACCEPT (P33b, P72). FW-06 ACCEPT (P67, P69). FW-07 ACCEPT
(P21b–P25). FW-08 ACCEPT (P73). FW-09 ACCEPT. FW-10 ACCEPT (P7b, P34). FW-11 ACCEPT with
ADV-d (P79). FW-12 ACCEPT. FW-13 **CHANGES_REQUIRED** (MUST-A(v4): the closed registry
advertises a SARIF projection it does not determine for two commands; P36 and P14 otherwise
clean). FW-14 ACCEPT as a stated harness obligation (P57f: "must add … Synthetic design cases
are not that corpus"). FW-15 ACCEPT (P68).

All fifteen rows are present in the source map with substantive current-contract text (P77d).

## Inherited residuals, D-372 and readiness obligations

The sixteen DR-011-R01..R16 rows and the eleven parent DR-001..011 rows each carry a written
disposition of real length (P78), and R10 correctly still says it "cannot be closed by this
proposed table". None is contradicted by the frozen bytes. MUST-A(v4) touches **R08** (the D9
branch/optional-field/selected-output behaviour: the required-output failure law is stated and
registered — P32e — but the SARIF projection's own field set is not) and **R13** (typed
multi-axis comparison, whose `audit` output is one of the two affected commands). R01, R04,
R09, R11, R15 and R16 are unaffected by this review's finding and were re-verified by P71d,
P73, P21b–P23b and P51e.

The thirty evaluation-proof residual dispositions are individually written, carry
`reviewStatus: PENDING`, and make no containment claim (P47). All 32 qualification-gate rows
record `qualified=false`, `demonstrated=false`, `implementationHarnessAuthored=false` (P42,
P56, P65). `historical-preservation-report.v4.json` verifies against the real repository files
(P45b). No subject byte authorizes implementation and no file reads condition 5 as MET (P43);
`post-reset-dispositions.v4.proposed.json` carries `implementationAuthorized: false`.

**DR-003 timing disposition:** independently affirmed as proposed (P56). It is explicitly a
scoped condition-1 disposition, explicitly "not a SATISFIED or DEMONSTRATED claim", keeps
demonstration mandatory at DR-G09/G18/G19/G21/G22 and DR-012 (all five gate rows present and
honest), states that a failed measurement cannot be waived by the synthetic reference result,
leaves the historical requirement intact for its original scope, and grants **no condition-5
implementation authorization**, which remains **NOT MET**.

The current source map's rows are consistent with the contracts, and its G13 sentence is
confirmed: the `g13-result-schema.v5.json` platform labels are a scoped historical corpus
adapter, not product machine ids (P37). The central register and navigation documents remain
pre-application by design, and `validation-summary.v1.json` still reads
`claudeFinalReview: PENDING-FROZEN-V4`, `readinessChanged: false` (P50).

## Scoped review-owner dispositions (DR-201..DR-205)

These are **new full-product-scope dispositions by this review owner**. The historical
2026-08-13 acceptances are untouched and retain their original subjects and digests; I inherit
none of them.

| Row | Disposition | Substantive basis and exact selectors |
|---|---|---|
| **DR-201 semantic correctness** | **ACCEPT** | The full-product semantic account is correct and determinate on the evidence I exercised: acyclic proof/evidence/seal closure with a cyclic proof refused (P67); exact retained-input closure with typed import source/build correspondence and six refusal lanes (P27, P28); semantic identity domains carrying no operational identifier (P71d, `foundation/identity-model.py` `PREFIX`); resolution completeness distinguished from examined-set completeness (P73, `native-evidence.md` §3/§4, `CoverageResultV3`); typed retention loss separated from admission rejection and from a false predicate (P19, P20b, `identity-and-evidence.md` §4/§5); integer-only confidence typing (P68). Selectors: `identity-and-evidence.md` §2–§5; `foundation/identity-schemas.v2.json`; `foundation/identity-model.py` `close_run`; `native-evidence.md` §3/§4/§14. |
| **DR-202 delivery/operations** | **CHANGES_REQUIRED** | The delivery/output half of the product owns MUST-A(v4). The post-commit required-renderer failure law itself is correct and registered (`DELIVERY.REQUIRED_FAILED` (4) / `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, optional sinks leaving `success`, every renderer's required-failure class operational — P32e), and the D9 branch contract is closed; but the newly re-entered SARIF projection is undetermined for `audit` and `repair-verify` and unexercised for three of four commands. Selectors: `workflows-and-surfaces.md` §8 **Renderers.** and §9; `workflows/command-inventory.v1.json` `audit`/`repair-verify` `parityFields`; `workflows_model.v1.py` `render`; `workflows/workflow-cases.v1.json` `/renderCases`. |
| **DR-203 prototype lessons** | **ACCEPT** | The gap this row was implicated in by the application review (DR-130) is closed by security **S16**, which I checked item-for-item against architecture file 05 rather than by term counting: five preserve obligations, five distinctions and six prohibitions all map one-to-one (P39e, P39f); the prototype commit `a62509d6…` is pinned in S16 and in `prototype-evidence-reference.md`; the two hardest joins (no-write pre-initialization versus the explicit default authoritative first write; immutable coexistence with foreign-state refusal before any write) are both stated and are backed by the real inventory rows (P51e) and registered refusal codes (P53). The corpus is routed to G06/G07/G11/G12/G18/G19/G21 as a required future measurement with an explicit disclaimer that nothing here executed the prototype. Selectors: `security-and-lifecycle.md` §S16; `docs/v2/architecture/05-v1-to-v2-relationship.md` §Migration constraints; `docs/v2/architecture/prototype-evidence-reference.md`; `workflows/command-inventory.v1.json` `writesTrackedIntent`/`firstSourceWrite`. |
| **DR-204 inherited invariants** | **ACCEPT** | Every inherited invariant I could exercise holds and every inherited row carries an individual written disposition rather than an aggregate grade: DR-011-R01..R16 (16) and DR-001..011 (11) with R10 correctly left open (P78); 30 evaluation subresiduals individually written and PENDING (P47); the six previously unpinned compatibility rows now pinned and resolving (P40b); historical files byte-unchanged (P45b); the truth-table pin moved to the accepted v9 head with a retained delta (P29, P30); source pins across all four units resolving (P58). The DR-204 precedent — that a coordinator-composed discharge cannot satisfy a grade requiring independent review — is honoured: nothing in the subject claims acceptance of its own bytes (P59, P80), and this review supplies the independent oracle for the design layer only. Selectors: `inherited-residuals.proposed.md`; `evaluation-residual-dispositions.proposed.json`; `inherited-row-sources.proposed.json`; `historical-preservation-report.v4.json`. |
| **DR-205 core/components** | **ACCEPT** | The component/boundary account is now complete rather than deferred: admission **§5** dispositions all seven P-1/P-2/G3 items with no deferral phrase, including the four (marketplace/catalog, external lifecycle parity, network/egress defaults, G3 substrate) the application review found uncovered (P38, P52); components are held to typed facts/Coverage/prepared imports with findings, policy, verdict, persistence, finalization, rendering and termination reserved to the host, and an operational test-runner grant cannot become a Plan semantic principal (P66); the core transition scope is derived from the closed intent and the fenced registry, never caller-supplied, and is all-or-nothing (P18, P55e, P17f). Selectors: `admission-and-qualification.md` §5; `security-and-lifecycle.md` §S9.2/§S10; `native-evidence.md` §5.5; `workflows-and-surfaces.md` §7/§8/§12. |

DR-202's grade follows MUST-A(v4) and would move to ACCEPT on its correction; the other four
do not depend on it.

## Limitations

Reference code ran only over synthetic fixtures. No OS custody, cryptography, SQLite
durability, fsync, process death, compiler, Cargo, provider, renderer or repository code was
executed and none is claimed; every signature, OS observation, evaluator callback, fence/lease
observation, trust instant and pivot presence is a declared TCB assumption. Host functions are
the admitted entry points and model TCB projections are not caller authorization: the workflow
and native models accept host projections as trusted inputs by design, so `repair_recover` and
`admit_test_execution` cannot themselves prove a well-formed projection came from a real
admission. I re-composed the real admissions myself in P1–P5, P7b, P8d, P10b, P15b and
P21b–P23b rather than trusting the fixtures, but a forged projection at that seam is outside
what any of these models can detect and is correctly declared as such.

Because each unit loads `foundation/canonical.py` under its own module name, `AdmissionError`
is three distinct classes at runtime; this is a loader artifact of the reference harness, not a
contract defect, and my probes catch all three. The workflows report records counts only, not
per-check ids, so probe P81's "no SARIF-named checks" reading is a report-shape artifact — the
substantive fact is P61, taken directly from `workflow-cases.v1.json`.

Unit expectations are same-author. This review is the independent oracle for the mixed final
bytes; it is **not** the blind implementer litmus (DR-011-R10), which remains a later distinct
act that I have not performed and do not prejudge, and it is **not** an application review or
acceptance. Severity is my judgement against the contracts' own statements; the single MUST
names a claim the subject makes that its bytes do not deliver.

## What the authors should do

1. Fix MUST-A(v4) in new bytes, consider ADV-a..ADV-e, re-pin, regenerate all five reports and
   freeze a new exact subject with a **new** manifest. Do not overwrite `candidate-subject.v4.json`.
2. Do not reuse this review for changed bytes; request a fresh independent re-review of the
   newly frozen subject. This review is CHANGES_REQUIRED and accepts nothing.
3. Only after an ACCEPT, run the separate blind consumer-B review; then assemble the complete
   application package with real design and consumer evidence; then the per-row application
   review; then apply D-372, the current source map and the central register.

**Paths.** This file; `review.json`; `probes/independent-probes.py` (+`-b`,`-c`,`-d`,`-e`) and
their `.json` outputs; `probes/probe-index.json`; `probes/independent-probes-f.json`;
`evidence/00-manifest-verify.txt`; `reports/` (launchers, reruns, `report-diff.txt`,
`exit-codes.txt`, per-suite stdout); `scratch/` (run-in-place copy); `run-suites.sh`.

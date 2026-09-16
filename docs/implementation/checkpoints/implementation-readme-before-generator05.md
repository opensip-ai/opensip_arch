# OpenSIP implementation

The [active work record](ACTIVE-WORK.md) is the current implementation/review status.
The user has authorized actual Grok as reviewer with Codex remaining lead; historical
Claude-only queue and checkpoint statements below do not block that authorization.


Product code belongs in the sibling `opensip` repository. Approved design,
reference contracts, review evidence and implementation acceptance records stay
in `opensip_arch`. The user authorized the entire implementation with actual
Claude verifying the work and asked us to continue until complete. This session
has no new implementation commit, push or publication authorization.

The [accepted design baseline](../coop/design-corrections/reviews/root-application46-delivery.v1/README.md)
and [build plan](../v2/architecture/implementation-boundaries-and-build-plan.md)
remain authoritative. Scoped corrections preserve source45/application46 and
historical evidence. A passing isolated trial does not complete its milestone.

| Milestone | Current status |
|---|---|
| M0 design baseline | Accepted; implementation-discovered corrections reviewed separately |
| M1 isolated builds/contracts | In progress; accepted units mostly staged; final source closure and integration incomplete |
| M2 admission/publication | Not started |
| M3 TS/JS/Rust analysis | Not started |
| M4 report/historical queries | Staged reader/navigation/overview/evidence/catalog views with browser checks; full report and host delivery incomplete; owner/source review pending |
| M5 workflows/lifecycle | Not started |
| M6 release qualification | Not started; all 32 gates and 54 recovery cases remain unperformed |

## Accepted and integrated foundations

The product currently has 13 foundation files plus initial [contextual help](m1/report-help-start/receipt.json) and [report styling](m1/report-style-start/receipt.json) at the already inventoried apps/report/src/report.css path. Contextual help passes strict TypeScript compilation and six checks in a fresh headless Chrome, with an inspected screenshot. Full report, supported-browser and accessibility qualification remain undone. [Canonical identity](m1/canonical-unit.v1.json)
implements exact JSON and SHA-256. The [binding correction](m1/design-binding4-correction-unit.v1.json)
provides explicit inventory/contract succession and generation-source checks.
The [common-control source bridge](m1/control-source-unit.v1.json) is
[integrated in the product design lock](m1/control-source-integration.v1.json):
46 static inputs, two contract successors, 29 source schemas and 56 binding tests.
Byte provenance does not itself establish semantic selection or product behavior.

## Accepted staged units

These units have substantive actual-Claude review and root assent. Their linked
records define the exact accepted scope and remaining integration duties.

| Unit | Acceptance record | Remaining use |
|---|---|---|
| Metadata design | [metadata](m1/metadata-unit.v1.json) | Rebase the final envelope and inventory closure |
| CLI help/version/completion | [CLI metadata](m1/cli-metadata-unit.v1.json) | Integrate and rebind final metadata/envelope and compiled asset metadata |
| Exact TypeScript runtime | [TS runtime](m1/ts-runtime-unit.v1.json) | Add the selected report profile and final generated closure |
| Eight generated-output algorithms | [eight outputs](m1/eight-output-unit.v1.json) | Apply only to the final accepted source selection |
| Confined generation adapter | [adapter](m1/generator-adapter-unit.v1.json) | Final inventory/bootstrap/source binding and integration acceptance |
| Common-control generation02 | [control generation](m1/control-generation-unit.v2.json) | Final integration; semantic admission remains separate |
| Native wire renderer05 | [native renderer](m1/native-wire-renderer-unit.v1.json) | Rebase to accepted native owner; complete closed-IDL integration |
| Rust package boundary checker | [package boundaries](m1/package-boundaries-unit.v1.json) | Inventory and actual build lanes |
| Report asset verifier02 | [asset verifier](m1/report-assets-unit.v1.json) | Actual bundle, compiled pin/channel, renderer join, D9 and platforms |
| Report asset assembly02 | [asset assembly](m1/report-asset-assembly-unit.v1.json) | Actual bundle, private compiled pin, immutable publication, source/tool closure and host integration |
| Interruption correction07 | [conditional owner acceptance](m1/interruption-envelope-unit.v1.json) | Final accepted parent/joint source, report/CLI rebase, host custody and output capacity L02 |

No generated outputs or staged CLI have been installed in the product repository.
The Rust provider isolation trial qualifies only the shared-source export build,
not Rust analysis. Platform trials here are not Linux or release qualification.

## Current correction and review work

| Workstream | Evidence and current disposition |
|---|---|
| Native owner | Root [subject06](m1/trials/native-wire-owner-06/subject-manifest.json) completes partial actual-Claude author06 after quota. It passes 596 checks, 149/149 mutation controls and an isolated 41-input reproduction of both. Payload/sequence binding and prepared-read authority corrections are proposed; actual independent review remains required. [Root receipt](m1/trials/native-wire-owner-06/root-validation/receipt.json) explicitly distinguishes root runs from Claude authorship and preserves historical attribution. |
| Report projection | [Subject08](m1/trials/report-projection-08/subject-manifest.json) passes strict root reproduction: 194 report cases, 47 envelope cases, 22 aggregates, 68 goldens/17 scenarios, 323 coverage rows and 96 external pins. It integrates interruption07 and report07 fixes. Actual review08 was prevented by quota; inherited envelope5 and correction6 need joint acceptance. The new [Q-FIT-1 audit](m1/audits/fit-interruption-parity-01/issue.md) proves interrupted fit with a completed query crashes the static parity function because advisoryReport is absent; the 144 declared-format count is not renderer execution. Q-FIT-1 and L02 are required M1 corrections; P01/X01 remain M5 duties. |
| Interruption envelope | [Review05](m1/reviews/interruption-envelope-05/review.md) accepts the behavioral delta conditionally but identifies an availability owner conflict. Root [subject07](m1/trials/interruption-envelope-07/subject-manifest.json) preserves invocation-scoped selections without a committed Run and adds a mandatory composite delivery join. It passes 42 shape, 59 component join, 36 availability delivery, 43 metadata, 102 owner-model and 12 wrong-result-kind cases. [Actual review06](m1/reviews/interruption-envelope-06/review.md) accepted the direction but required source-prose alignment and a started-attempt prerequisite. [Review07](m1/reviews/interruption-envelope-07/review.md) and root accept the correction at conditional owner/reference scope. Final accepted parent, joint source selection and L02 capacity remain required. |
| Report evidence feature owners | [Subject02](m1/trials/report-evidence-design-02/subject-manifest.json) passes root CHECK OK with 89 pins and actual evaluator3 reference Run compatibility/identity admission. It corrects historical recognition compatibility, cross-universe tests, partial globs, Cargo member roots, patch composition, coupling bounds and counting. S1–S4 remain unaccepted; final actual review is pending quota reset. |
| Presentation catalogue | Root [correction02](m1/trials/presentation-catalog-02/subject-manifest.json) passes 16 groups and 9 behavioral mutants; a redundant canonical-cap guard survives and needs independent confirmation. It proposes singular authenticated release capability-description authority, Run/declaration selection joins, distinct absence/retention states, full receipt fields and hostile-text restrictions. Actual release/Run custody, report integration and independent review remain required. |
| Configuration disclosure | [Subject01](m1/trials/config-disclosure-01/subject-manifest.json) proposes a closed 13-field resolved-configuration projection (DO04), disclosing only budget and allowed scopes. Ten root groups pass, including sensitive-value noninterference and exact digest checks. [Fresh review01](m1/reviews/report-presentation-owners-01/review.md) requires Plan binding, provenance and source-failure mappings. Root [correction02](m1/trials/config-disclosure-02/subject-manifest.json) passes 13 groups; review, host custody and final HTML leakage checks remain required. |
| Workflow timing | [Subject01](m1/trials/workflow-timing-01/subject-manifest.json) proposes invocation4 attempt duration observations (DO11), with unavailable states and legacy disclosure. Eight root groups pass. [Fresh review01](m1/reviews/report-presentation-owners-01/review.md) requires schema outcome joins, typed sums and legacy states. Root [correction02](m1/trials/workflow-timing-02/subject-manifest.json) passes 11 groups; actual timing capture, review and report integration remain required. |
| Explicit report history | Root [correction02](m1/trials/history-selection-02/subject-manifest.json) is frozen after a complete passing reproduction: 18 selection groups, 14 actual unchanged close_run reference checks, 12 mutation controls, seven byte-identical generated outputs and 71 pins. It proposes typed run.show admission, exact request/receipt joins, existing routes, snapshot timing and explicit bounded panels. [Root receipt](m1/trials/history-selection-02/subject/root-receipt.json) distinguishes synthetic custody from product behavior. Independent review, query versioning and final source/store/report integration remain required. |
| Interrupted fit | [Audit01](m1/audits/fit-interruption-parity-01/issue.md) proves a static parity crash and inadequate completed-query fixture evidence. Root [proposal01](m1/trials/fit-interruption-01/subject/contract.md) adds explicit analysis-step query binding, private completed-response retention and total unavailable-query parity. Thirteen groups, 36 actual static parity calls and 11 targeted mutation controls pass; three schema fragments reproduce. Full owner schema/report integration, actual host custody and independent review remain required. Q-FIT-1 is still open. |
| Required output capacity | [Audit01](m1/audits/envelope-capacity-01/issue.json) remains open. Root [proposal01](m1/trials/required-output-01/subject/contract.md) makes the existing D9 output-failure operation explicit after an interruption or renderer failure, with whole-envelope pre-emission bounds and honest partial-stream behavior. Thirteen groups and nine mutants pass against the unchanged D9 authority. It proposes explicit operational capacity failure after useful commits; whether that policy satisfies L02 requires independent review, source succession and product integration. It does not prove full oversized Run admission or reserve representability before selection. |
| Coverage prerequisite | [Accepted unit](m1/coverage-prerequisite-unit.v1.json) adds exactly the missing assets.rs M1 prerequisite key. The unchanged owned validator passes all 322 base and 323 pending-report rows without a workaround. Report07 binds it; final product closure integration remains pending. |
| TypeScript package boundaries | Root [correction04](m1/trials/typescript-boundary-04/subject-manifest.json) completes the actual review03 counterexamples and is frozen. The full offline reproduction passes 200 tests, 32 inherited and 11 new mutation controls, 164 comparison cases/29 Node oracles, 24 CLI invocation checks and 8 manifest controls. [Root receipt](m1/trials/typescript-boundary-04/root-validation/receipt.json) records exact bytes and the synthetic inventory/tooling limits. Actual independent review, final runtime/tooling policy, inventory, browser resolver and package-manager selection remain pending. |
| Report asset assembly | [Subject02](m1/trials/report-asset-assembly-02/subject-manifest.json) incorporates the required regression strengthening from [review01](m1/reviews/report-asset-assembly-01/review.md). Eleven unit groups, seven adopted reviewer groups, two Rust groups/19 projection pairs, Clippy and formatting pass. Typed OS failures, aggregate pre-read bounds and Windows reserved-name rejection are added. [Review02](m1/reviews/report-asset-assembly-02/review.md) and root accept the unit with no required fixes; its bundle is synthetic and final integration remains pending. |

The latest reviews and frozen subjects are retained under `m1/reviews` and
`m1/trials`. The TS02 subject is retained as a hash-bound tar archive preserving
1,207 entries and symlinks. Tool closure evidence does not itself select a
package manager or establish reproducible contributor bootstrap.

The supplemental [coverage source correction](m1/trials/report-coverage-binding-01-checkpoint-02/README.md)
identifies an inherited report binding error: a coverage2 ID names one result,
not a collection. Its32 passing reference checks bind the panel to the exact Run's
evidence collection and each row to its own descriptor/payload. Actual review,
report source succession, byte-budget recomputation and product integration
remain pending; current generated/report checkpoints are preserved.
The [evidence view](m1/trials/report-evidence-view-01-checkpoint-01/README.md)
passes strict compilation and17 browser groups with inspected desktop/narrow
layouts. It uses an internal presentation input for that proposal; the final
generated report adapter and host source admission are still pending.
The [catalog view](m1/trials/report-catalog-view-01-checkpoint-01/README.md)
renders rules, release capability declarations and exact-key descriptions with
source availability, search and local paging.31 current staged reports decode
and render, and18 browser groups pass. Final composition, real source custody
and independent review remain pending.

The native03 reviewer temporarily wrote two Python cache files inside its frozen
subject. The reviewer disclosed and removed them; root reverified the exact
64-file closure and all listed bytes afterward. This was a custody incident,
not an unchanged-throughout claim. Report06's first root attempt failed because
of cwd-sensitive audit behavior; its corrected-cwd run passed, and report07
subsequently corrects that audit defect. Historical reviews and failed controls
remain unchanged.


## Actual Claude availability

New actual-Claude review calls now report the weekly limit, resetting September
18 at 5 p.m. America/Los_Angeles. [Presentation review02](m1/reviews/report-presentation-owners-02/root-disposition.json)
and [report review08](m1/reviews/report-projection-08/root-disposition.json)
returned quota messages, not substantive reviews. Root continues authorized
implementation and verification; new candidates stay unapproved pending actual
review. TypeScript review03 and native author06 also ended with quota messages. Their partial work needs inspection and completion; no substantive final verdict was produced.

Frozen candidates needing review include native06, report08, evidence-feature02,
TS-boundary04, catalogue02, history02, output-policy01, configuration02, timing02 and help01.
The [eleven-unit review queue](m1/review-queue-01/queue.json) pins exact subjects and supplies separate review prompts. History correction02 is authored and frozen; L02 policy selection and complete owner succession remain open. No GPT reviewer substitutes for
Claude. The latest product addition is the small contextual-help control;
most implementation remains unfinished.

## Joint report integration before the coverage source correction

Root is combining eight report-related candidates at `/tmp/opensip-implementation/m1-report-joint-candidate-09`; [checkpoint06](m1/trials/report-joint-09-checkpoint-06/checkpoint.json) preserves unfinished work and failure evidence. Its full verification passes:215 frozen input members and182 external sources verified,29 outputs reproduced byte-identically,18 check processes passed, and194 predecessor cases reconciled as186 unchanged outcomes plus8 replacement witnesses. All19 predecessor positive scenarios and12 planning variants admit.14 composed schemas resolve2,728 references across66 documents.

New-Plan admission now binds the native helper to the composed v3 parameter registry and appends the recognition duty after existing checks. Six groups cover missing/duplicate parameters, native fault precedence, complete external/host error envelopes and25 unchanged prior native route branches. Historical Run closure remains unchanged. Current carriers select common4; the original common3 remains exact and refuses the two new public detail codes. The [candidate source map](m1/trials/report-joint-09-checkpoint-06/working-copy/candidate-source-map.json) prepares current Rust/TS generation without selecting product sources.

Complete report cases cover retained configuration/history, source-bound fit, feature evidence, shared budgets, catalogue descriptions and recipe previews. Catalogue checks reject visible registry/key contradictions and competing capability authorities. Required-output01 has a full proposed D9v1.15 view and complete-envelope integration tests;45 exit goldens,4 core-completion cases and6 reductions remain unchanged. Its capacity-failure alternative is unaccepted and does not satisfy L02's original stronger criterion. Report bounds remain27,829,365 bytes, a shared4 MiB exploration allowance and conservative depth39; these do not qualify product codecs or performance.

Final owner/source/package selection, accepted generated-source integration, actual Plan construction and custody, runtime/browser/release integration and actual independent review remain pending. The [review guide](m1/trials/report-joint-09-checkpoint-06/working-copy/REVIEW-GUIDE.md) and [obligation dispositions](m1/trials/report-joint-09-checkpoint-06/working-copy/joint-obligations.json) preserve scope and original criteria. This checkpoint is not a frozen review target or acceptance, and most product implementation remains unfinished.

## Contract generation preceding the coverage source correction

Root [joint-generation checkpoint02](m1/trials/joint-generation-01-checkpoint-02/README.md)
stages40 schemas and857 explicit entry points while retaining all587 prior names.
Eight generated outputs reproduce byte-for-byte. Rust compilation and65,491
value round-trips pass, including1,338 retained legacy Claude witnesses and62
current report/envelope cases; those62 also pass strict TS assignments and runtime
shape validation. Tuple/pattern comparisons and naming/constant-lowering controls
pass. This is unaccepted local generation evidence, not product integration or
confinement qualification. This checkpoint preserves the default4MiB/depth32 codec; the distinct report
profile is tracked below. Actual Claude review, final owner/source/bootstrap
selection and most product implementation remain pending.

## Distinct report codecs

Root [report-codec checkpoint02](m1/trials/report-codec-01-checkpoint-02/README.md)
implements the proposed 27,829,365-byte/depth39 profile in staged Rust and TS
code, preserving the default 4MiB/depth32 codec and identity hash limits.
102 TS boundary checks, 13 Rust test groups and Clippy remain valid for unchanged
codec algorithms. The source rebase passes 68 generated-consumer checks and
3,014 Rust/TS comparisons. A 4,202,744-byte synthetic report admitted by
the joint reference round-trips exactly in both languages and passes generated
shape validation. This remains unaccepted: source/API selection, embedded owner
admission, host/browser/delivery integration and release qualification are pending.
L01 and L02 remain open. The stale inventory5 provenance is corrected to inventory6
in joint checkpoint06, generated contracts and codec inputs. Both full reference
and generated consumers refuse the old marker. Normal and source-only clean
staging verification pass; the clean run starts without generated schemas,
models or report fixtures. Historical checkpoints and failed runner controls remain preserved.

## Invocation record capacity investigation

[Investigation01](m1/trials/invocation-capacity-01-checkpoint-01/README.md)
records a concrete L01 counterexample: a2,954-byte synthetic workflow plan
replays16 steps, each complete result fits the default codec, but the complete
invocation is4,421,772 bytes and refuses the4MiB codec. Shape/replay evidence does
not establish an admitted profile contribution, authentic doctor output or
retention. The proposed direction separates the logical invocation, retention
records and bounded public materializations; no storage or codec policy is
selected. A conditional aggregate estimate exceeds516MiB, so it must not become
an assumed whole-memory allocation. L01 and current conservative report bounds
remain unchanged pending an explicit owner decision and actual review.

## Staged report reader and navigation

The [report reader](m1/trials/report-data-01-checkpoint-01/README.md) implements
exact parsing, generated shape validation, explicit version/profile/limit errors
and deeply frozen presentation data.32 valid and56 refusal cases pass; six fresh
Chrome groups cover the same compiled boundary, including the dense report.
It does not authenticate evidence or duplicate host semantic admission.

[Local navigation](m1/trials/report-navigation-01-checkpoint-01/README.md)
implements mounted view routes, keyboard tabs, focus transfer, browser history,
explicit unknown-view states and cleanup.14 checks pass in a fresh Chrome over a
local file, and the fixture screenshot was inspected. Editor links and exact
symbol/candidate/Run routes remain unfinished. Both implementations stay staged
pending actual review and final generated-source integration; full report views,
loader/CSP/bundle, host delivery and supported-browser qualification remain open.

The [overview candidate](m1/trials/report-overview-01-checkpoint-01/README.md)
displays recorded outcomes, exact identifiers, attempts, timing and missing
observations without deriving verdicts.12 browser groups pass across31 current
report fixtures plus explicitly separate display-only controls. Desktop/narrow
screenshots were inspected; keyboard users can scroll the step table. The staged
stylesheet preserves the existing bytes and appends only overview layout rules.
Navigation/entrypoint integration, remaining views and actual review are pending.

## Historical resume order (current order is in ACTIVE-WORK.md)

1. Actual Claude is quota-blocked. Do not repeat calls until availability changes. Root native06 is now frozen and awaiting independent review (596 checks, 149 mutations, isolated reproduction all passed). Root catalogue02 is also frozen (16 groups, 9 caught controls plus one classified redundant guard). TS correction04 is frozen (2,032 entries; fullcheck exit0 with 200 tests and all mutation controls caught). History correction02 is now frozen with a complete passing reproduction, including panel/snapshot/budget and 12 mutation controls. Required-output proposal01 is frozen, with 13 groups and nine controls passing; it is an unaccepted policy proposal, not an L02 closure. All eleven frozen subjects were byte-verified when the review queue was prepared. Preserve original Claude partial work, synthetic-fixture disclosures and old failed controls.
2. Frozen report08, evidence-feature02, configuration02, timing02 and help01 need actual independent review. Prepared prompts in `/tmp/opensip-implementation` describe exact subjects and limits; quota-only requests must remain preserved. History02 and catalogue02 now await review. L02 has a concrete unaccepted output-failure policy; decide its adequacy and bind the required source successor before closing the obligation. Q-FIT-1 now has a frozen narrow proposal; its sourceStep/custody law, final full schemas and parent report integration still require completion and review. The history [owner audit](m1/audits/history-query-owner-01/result.json) shows run.show has no typed item in the selected generic query schema; do not pretend an existing typed adapter was invoked. Corrected candidates require newly frozen bytes and actual review before acceptance.
3. Integrate accepted interruption and feature owners into the report, close all
   required report obligations, bind scoped successors and integrate generation,
   the build tools and CLI against the final inventory/source lock. Complete the
   actual offline report bundle and its private compiled asset binding.
4. Implement M2–M6 with actual-Claude review, meaningful integration tests and
   every required release qualification. The M5 import/export selectors and
   remaining codec statement must be resolved in their owned scope. No reference
   fixture, individual acceptance record or test count completes the product.

The [prior checkpoint](m1/progress-checkpoint-before-owner04.md) preserves the
longer chronology, exact earlier trial paths, failed controls and limitations.
Historical acceptance records and lock-bound files must not be edited to make
new candidates appear accepted.

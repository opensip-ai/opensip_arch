# SD-5 — the public route of a manifest-class excluded form at R10a (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and adds no product file, code, class, exit code, error code or public detail code. It needs Grok's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** The accepted supervisor law **M3-D r3** (`docs/implementation/m3/supervisor-d/PROPOSAL-r3.md`, GROK2 ACCEPT, `9679dbc4…`) refuses DR-117's manifest-class excluded forms at a new pre-draw row, **R10a**, as the internal `ExcludedForm {class, subject}` (item 24, MD:708-746). It leaves the public projection to successor **SD-5**: "**Public projection** is J1's, with existing codes (SD-5). The lead's recommendation is `request-rejected` 2 with `EXTENSION.ADMISSION_REJECTED`, SL S12's admission family (SL:1306). No new code." (MD:733; the SD-5 row, MD:1091; SD-6, MD:1092).

The accepted host-pipeline law **M3-J1 r4** (`host-pipeline-j/PROPOSAL-r4.md`, GROK2 ACCEPT, `c18c0d3c…`) placed R10a and its ephemeral counterpart ER10a (MJ:325, MJ:337-349, MJ:426) and recorded the gap as successor **S20**: "Until S20 lands, item 10 has no row for them, and J2a's projection of them is incomplete" (MJ:774). Its drafter added: "SD-5 must also keep that refusal distinct from matrix row 27 (indeterminate, exit 3)" (row 27, MJ:673).

This unit is **SD-5 for R10a's route**: the class, exit, code, subject, detail and remedy of a manifest-class `ExcludedForm`, as one row of the route table it extends, NE §10's admission and event routes. It closes the outcome matrix's totality for `ExcludedForm` as J1 r4 places it (R10a and ER10a). Its owners are the NE and WS public-route owners (LD-S1).

**Product.** Main at `cd5958b` (I1-P's binding, 82 contract successors), read only. The record is built and checked against it. No bound successor overrides the line SD-5 uses.

## Short names

Each sha256 prefix is the first 8 hex of the exact bytes pinned in the review request (`reviews/grok-sd-5-r1/hashes.txt`).

| Name | Document | sha256 |
|---|---|---|
| **MD** | `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md`, M3-D r3, the accepted snapshot (`reviews/grok2-supervisor-d-r3`) | `9679dbc4…` |
| **MJ** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md`, M3-J1 r4, the accepted snapshot (`reviews/grok2-host-pipeline-j-r4`) | `c18c0d3c…` |
| **NE** | `docs/v2/contracts/product-v1/native-evidence.md`, the parent (329,013 bytes) | `83b99783…` |
| **WS** | `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `1ee203e3…` |
| **WSE** | `docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md`, WS's selected effective copy | `4478ce1a…` |
| **SL** | `docs/v2/contracts/product-v1/security-and-lifecycle.md` | `a319da39…` |
| **D9** | `docs/coop/artifacts/d9-exit-contract.v1.14.json` | `8dd33038…` |
| **REG** | `docs/coop/design-corrections/public-detail-registry.v1.json`, the closed public detail registry | `2702e6ca…` |
| **PPBS** | `docs/coop/artifacts/preview-product-boundary-successor.v10.json`, DR-117's EE classes | `8f34c92e…` |
| **X4T** | `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` (r11, accepted) | `8116f487…` |
| **C4** | the product's `schemas/sources/common-v4.schema.json` at `cd5958b` (`DomainDetailCode`) | `661b9fda…` |

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: the override with its exact `before` and candidate `after`, the effective table rows, and the new row cell by cell |
| `successor.json` | the contract successor record: one parent (NE), one line override, no supersession |
| `evidence/build_sd5.py` | builds `PASSAGES.md`, the record, the subject manifest and the draft unit record deterministically; `--check` compares instead of writing |
| `evidence/check_sd5.py` | read-only content checks |
| `evidence/verify_scratch.py` | runs the real `verify_design` with a synthetic review and assent, the binding-order probes and one conflict probe |
| `../sd-5-subject.json` | the subject manifest (generated) |
| `../sd-5-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`; not part of the subject |

## What changes: the one passage

| Parent | Line | Form | Change |
|---|---|---|---|
| NE | 3540 | insert-only | After §10's "**invalid authenticated RELEASE DECLARATION**" row, one new row of the same five-column table (NE:3523): "**component manifest that is an excluded form**". NE:3540 keeps every byte; its `after` is the line, a newline and the row. NE:3541 follows unchanged. |

Nothing else changes: no WS, WSE, SL, schema, registry, D9 or product byte (LD-S1). The exact row is in `PASSAGES.md` and `successor.json`.

## The route, field by field

| Field | Value | Basis |
|---|---|---|
| Condition | an authenticated component manifest (SL S1: its signature envelope and signed catalog association) that current trust admits and that the analysis step can select, refused at component admission before any analysis attempt's `ExecutionId` is drawn or reserved, on the durable and the ephemeral path, as `ExcludedForm {class, subject}` | MD item 24 (MD:717-733); MJ R10a and ER10a |
| Classes | `EE-1` publisher neither first-party nor explicitly trusted; `EE-3b` a claim of policy, persistence, rendering, termination or host-lifecycle authority (a `commands` entry for role `analyzer`, or a capability outside the native capability matrix's provider capabilities); `EE-4` untrusted native or WASM code; `EE-5a` a project hook, root command or contribution-granted probe | MD:728-731; PPBS:667-725 |
| Class / exit | `request-rejected` / 2 | D9 golden `extension-admission-rejected`; D9 `nonAnalysisDerivation` rule 2 ("incompatible contributions … are request-rejected") |
| Error code | `EXTENSION.ADMISSION_REJECTED`; no `faultCause` (request-rejected carries none) | D9 `rejectionCauseToErrorCode["extension-admission-rejected"]`; SL:1306; MD:733 |
| `domainDetail.code` | `PAYLOAD-NOT-ADMISSIBLE`, security S12's admission row for a signed document that is not admissible | SL:1306; SL S12.1 rule 3; REG; C4 (LD-S3) |
| `domainDetail.subject` | `excluded-form:<class>:<manifestDigest>`, the manifest's identity `closure.manifestDigest` (64 hex); at most 84 characters | LD-S4 |
| Which refusal | the refused manifest least by `manifestDigest`, with its first class in the order EE-1, EE-3b, EE-4, EE-5a; every `ExcludedForm` R10a returned goes to the operational record | LD-S4 |
| `domainDetail.remedy` | "This installed component is a form OpenSIP never admits. Only first-party or explicitly trusted components are admitted, and none may claim policy, persistence, rendering, termination or host-lifecycle authority, run untrusted native or WASM code, or declare a project hook, root command or probe. Remove the component, or install its first-party release." (355 ASCII characters) | LD-S5 |
| Envelope `errors` | exactly that one detail | WS:1340-1344; NE:3630-3639 |
| `runId` / `executionId` | none. On first use the creation prelude's id names the creation act only and is never bound to the analysis attempt | MD:722; MJ:341 |
| Creation disclosure | unchanged: J1's item 9 rule for every refusal after R3 | MJ:340 |

The three paths of J1's control J-C10b all take this one row: steady-state durable (3a), first use (3b: `Published`, `LostRace`, `NotPristine`), and ephemeral (ER10a). With no trust view (J1's E-3, E-4), ER10a admits nothing and refuses nothing, so this row cannot arise there.

## Distinct from row 27

J1 r4's row 27 is "Required provider closure not installed, or not admissible (including ephemeral with no trust, E-3) | indeterminate / 3 | — | `COVERAGE.PROVIDER_UNAVAILABLE`; `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` | runId if committed | WS:1374; NE:3370" (MJ:673). Its golden is WS:1374 (and WSE:1447).

| | SD-5's row | Row 27 |
|---|---|---|
| When | R10a or ER10a, before R11, R12 and any Plan | after the Plan, when closure selection finds no admitted closure for a required capability |
| Input | a manifest that current trust **does** admit, whose content is an excluded form | a required closure that is **absent**: not installed, or not admitted by current trust |
| Class / exit | request-rejected / 2 | indeterminate / 3 |
| Code | `EXTENSION.ADMISSION_REJECTED` | reason `COVERAGE.PROVIDER_UNAVAILABLE` |
| Detail | `PAYLOAD-NOT-ADMISSIBLE`, `excluded-form:…` | `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` |
| Run, Coverage | none | a Coverage-bearing Run (`provider-unavailable`, NE:3370) when one commits |

**The boundary, stated in the row.** An excluded form is never a `provider-unavailable` deficiency and never the not-installed golden. A required closure that is not installed, or that current trust does not admit (an ephemeral request with no trust view included), is never an excluded form and keeps that golden. So J1's "not admissible" in row 27 means "not admitted by current trust", and never "admitted by trust but refused as an excluded form".

**No request takes both.** R10a ends the request on its first refusal ("Step 0 ends on the refusal", MJ:340), so a request carrying an excluded-form manifest and also lacking a required closure ends on this row, and row 27 is never reached. A request whose manifests R10a all admits can still reach row 27. The two inputs are disjoint (admitted by trust versus absent), so each event has exactly one route.

**Why not indeterminate.** An excluded form is a hostile but well-formed contribution that the product refuses at admission (PPBS: "Refused at admission. No ExecutionId."; QG DR-G29: "no waiver for silent admission"). Routing it as unavailability would let it degrade to an `unknown` Coverage answer, the silent outcome DR-G29 forbids.

## Totality for `ExcludedForm`

- **J2a's match** (MJ:703, "an exhaustive match with no wildcard arm"). For an `ExcludedForm` whose origin is R10a or ER10a, the arm is this row. `class` ranges over the four values above, and each maps to the same class, code and detail. The subject is a total function of `(class, manifestDigest)`, and the choice among several refusals is fixed (LD-S4). No value is left without a row.
- **The matrix row J1 records under S20.** For J1's next revision, word for word:

  ```text
  | 56 | Component manifest that is a DR-117 excluded form at R10a or ER10a (EE-1, EE-3b, EE-4's manifest part, EE-5a), before any analysis-attempt ExecutionId | request-rejected / 2 | `EXTENSION.ADMISSION_REJECTED` | `PAYLOAD-NOT-ADMISSIBLE`, subject `excluded-form:<class>:<manifestDigest>`; every `ExcludedForm` in the operational record | none | NE §10 (SD-5); SL:1306; MD item 24 |
  ```

  Control J-C20 gains one test for row 56.
- **Not in this unit: M3-D item 25's request class.** `ExcludedForm` also arises at R1 for EE-2, EE-4's request part and EE-6a (MD:748-763). J1 r4 does not place it, and S20 is "for R10a's route". It is cross-law item X-SD5-1 below.

## Lead decisions

Each decision is made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each names the alternatives it rejects. The owner may reverse any of them.

**LD-S1. Form: a contract passage successor to NE §10's admission and event route table, owned by the NE and WS public-route owners.**
- J1's outcome matrix takes its native admission routes from this table (rows 24-26 and 52-55 cite NE:3525-3541), and its totality rule is NE:3543's "an unmapped detail is a model error". A row here gives J1's S20 a contract basis, as the rows beside it have.
- The new row sits after the authenticated release declaration row (NE:3540), the other refusal of an authenticated install-time input before any Plan.
- **The WS owner's surface needs no WS byte.** WS:1340-1344 already composes the failure envelope from "the composition in native §10", and WS §9's table is "Selected goldens", not the totality authority. WS:1374's golden keeps its meaning; the new row bounds it from the other side.
- MD's SD-5 row calls the content "J1 law content". The public route is a contract fact; J1's next revision still records the matrix row (above).
- **Rejected:**
  - **A J1-law row alone.** No contract table would route an `ExcludedForm`. The laws behind J1's other admission rows map their refusals onto existing contract rows (for example X4T item 10 onto SL S12), and this one would map onto none.
  - **A WS §9 golden row** (with WSE, as I1-L's LD-L5 did). A selection, two copies, and no totality.
  - **SL S12.** That table is security's own refusal vocabulary; `ExcludedForm` is the components owner's refusal (D4).
  - **Both NE and WS.** Two statements of one route can drift.

**LD-S2. Class and code: `request-rejected` 2, `EXTENSION.ADMISSION_REJECTED`.**
- D9's own rejection cause fits exactly: golden `extension-admission-rejected`, "extension signature, compatibility, or requested capability is rejected", with `rejectionCauseToErrorCode` mapping it to `EXTENSION.ADMISSION_REJECTED`. D9 rule 2 makes "incompatible contributions" request-rejected. It is SL S12's admission family and MD's recommendation.
- **Rejected:**
  - **`REQUEST.UNSATISFIABLE`** (MD item 25's request-class recommendation). The manifest is an installed contribution, not the request.
  - **`REQUEST.PRECONDITION_FAILED`** (the release-declaration row's code). That row is a malformed host-supplied registry; an excluded form is well-formed.
  - **indeterminate 3** (row 27's route). See "Why not indeterminate".

**LD-S3. Detail: `PAYLOAD-NOT-ADMISSIBLE`, the existing admission detail for a signed document that is not admissible.**
- A `kind=failure` envelope needs a nonempty `errors` array (WS:1340-1344; product `command-envelope-v7`), so a registered detail is owed whatever the termination carries. MD item 24 forbids "a new public code" and J1 item 10 adds none.
- No registered code names an excluded form. `PAYLOAD-NOT-ADMISSIBLE` is the closest true one. SL S12 routes it to request-rejected 2 `EXTENSION.ADMISSION_REJECTED`, the same class and code. The security model reads it as a signed document "that is not admissible" (`SECURITY_DOCUMENT_ADMISSION_FAMILIES`). X4T uses it at R10's fenced first read for "a signature or quorum failure, or a future payload" of the trust documents (X4T item 10; MJ row 17), and the product names the document in the subject (`catalog`, `revocation`, `inventory`, `root`; `crates/security/src/trust/current_trust_admission.rs`). A component manifest is a signed document of the same trust family (SL S1: `opensip-signature-envelope.2`, subject `kind=manifest`, associated through the signed catalog). Under SL S12.1 rule 3, the refusal supplies the code and the rest is subject text, so the subject names the document and why.
- It is carried as `domainDetail`, so the termination and `errors` say the same thing.
- **Rejected:**
  - **`COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`.** Row 27's detail: it collapses the distinction, and its remedy, "install", is false.
  - **`CONTINUE-CORE-NOT-TRUSTED`.** X4T's interim detail for continuation refusals names the core, and a trust-freshness state, not a content claim. X4T-c will move component cases to `CONTINUE-COMPONENT-NOT-TRUSTED`.
  - **`native.release-declaration-invalid`.** Its remedy is keyed by code, "the installed release declaration is malformed; repair or reinstall the release", and that is false for a well-formed excluded form (NE's `remedyKeyingConstraint`).
  - **`CONFIG.INVALID`.** Nothing configured is wrong, and its code-keyed remedy (B-S9) is false here.
  - **`domainDetail` absent.** The envelope would still need a detail, and the two surfaces would differ.
  - **A dedicated new code.** Forbidden by MD item 24 ("a new public code") and MJ item 10 ("No public code is added"), and new public codes are the owner's (X4T item 10, citing 468 item 6; 468a README:3). It is reviewer point R2: a dedicated code would need MD's revision and an X4T-c-style registry successor.

**LD-S4. One detail, chosen deterministically, with a fixed-length subject.**
- WS:1340-1344 makes `errors` exactly the termination's one detail. So with several refusals the projection names one: the least `manifestDigest`, then the first class in table order. The operational record keeps every `ExcludedForm`.
- `manifestDigest` is the closure's own identity coordinate (IE §3 `closure2`) and is 64 hex, so the subject is at most 84 characters, inside `BoundedText`'s 1024 with no elision.
- **Rejected:** a component display name (unbounded, and not an identity); several details (the termination carries one).

**LD-S5. One remedy, true for all four classes, selected by the subject.**
- Security-family details take the refusal's own remedy: SL S12.1's reference projection is `public_detail(refusal, detail, remedy)` (`security_lifecycle_model_v1.py:342`), and the product already selects `CONFIG.CUSTODY_REFUSED`'s remedy by its subject (`crates/host/src/doctor_ingress.rs:202-207`). J2a selects this remedy by the `excluded-form:` subject prefix.
- NE's `remedyKeyingConstraint` governs native `PUBLIC_ROUTE_REMEDIES` keys, and `PAYLOAD-NOT-ADMISSIBLE` is not one. The remedy states one next step that is true for each class: remove the component, or install its first-party release.
- **Rejected:** a remedy per class (four strings behind one code and one subject family).

**LD-S6. Scope: `ExcludedForm` at R10a and ER10a only.**
- That is S20's title ("for R10a's route") and the lead's assignment. It is what D4's integration and J3d's and J2c's R10a wiring wait on (MJ:774).
- **Rejected:**
  - **SD-5's whole set.** `MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound` and `confinement-refused` land with D1 to D5 and have their own owners' boundaries (MD:676-677). They stay owed as the rest of SD-5.
  - **Item 25's request class.** It needs its own class and code (MD:758) and raises an origin question (X-SD5-1).

## Points for the reviewer

- **R1 (LD-S1).** Is NE §10's admission table the right route table to extend, with the NE and WS public-route owners as owners and no WS byte changed?
- **R2 (LD-S3, LD-S5).** Is reusing `PAYLOAD-NOT-ADMISSIBLE`, with an `excluded-form:` subject and a subject-selected remedy, an honest existing detail? Or does the "two remedies behind one code" concern (D9 `codeVocabulary.rule`; SL S12's `MIGRATION.CORRUPT` note) require a dedicated code, which MD item 24 forbids without an owner decision?
- **R3 (distinctness).** Is the boundary with row 27 ("admitted by current trust" versus "absent") complete, including the ephemeral path with no trust view?
- **R4 (totality).** Is the proposed J1 row 56 total for R10a's and ER10a's `ExcludedForm`? Is leaving item 25's request class to X-SD5-1 right?

## Cross-law items

| ID | For | Item |
|---|---|---|
| **X-SD5-J1** | M3-J1's next revision (S20) | Add row 56 (above) to item 10, citing NE §10's SD-5 row. J-C20 tests it. Row 27's "not admissible" reads "not admitted by current trust". |
| **X-SD5-D** | M3-D's next revision | Item 24 cites SD-5's row. The SD-5 row splits: this unit for R10a's `ExcludedForm`; the rest (`MemoryBudgetBelowCeiling`, `ToolOutputBound`, `ToolScratchBound`, `confinement-refused`) stays owed. D4-T1 gains the public-route assertion (class, code, detail and subject). |
| **X-SD5-1** | M3-D's next revision, with J1 | **Item 25's request class has no placed route.** `ExcludedForm` also arises at R1 for EE-2, EE-4's request part and EE-6a. MD:758 recommends request-rejected 2 `REQUEST.UNSATISFIABLE`. J1 r4 places no row for it, and its R1 row says only that "A malformed library request is a host-generated layer: `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`" (MJ:315; NE:3573, "a host *bug* minting its own invalid spec"). At M3 every request is a library request (J1 item 1), so the two must be reconciled in words. **Lead recommendation, not decided here:** a well-formed request that asks for an excluded form is not malformed and is not a host bug, so it takes MD:758's route, request-rejected 2 `REQUEST.UNSATISFIABLE`, with a detail chosen under LD-S3's existing-code test; J1's malformed-request sentence keeps its own scope. D's next revision and J1's S20 record state the row. |
| **X-SD5-SL** | the security owner | Record only. `PAYLOAD-NOT-ADMISSIBLE` gains one more emitter, component admission, under S12's existing row. S12's row text, S12.1 and the registry are unchanged. A later S12 refresh may name component manifests in that row. |
| **FA-1** | — | Disjoint. FA-1 overrides NE:3529, NE:3849 and NE:3850. |

No owner question is raised. R2 is flagged so the owner can see it.

## Binding

SD-5 has one passage override, so it binds on the `verify_design` at main `cd5958b` with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
- copy the review to `docs/implementation/m3/reviews/grok-sd-5-r1/review.json`;
- complete `sd-5-unit.json` (`ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`);
- append to the product lock `{record, subjectManifest, review, assent}` pinning `sd-5/successor.json`, `sd-5-subject.json`, the review and `sd-5-unit.json`, in a binding-only product commit;
- run plain `verify_design`.

Selecting SD-5 changes no product byte and no generation source. J2a projects the row; D4 and J3d's and J2c's R10a wiring cite it. Nothing is staged tonight: the product is read-only for this run.

**The other drafts on NE.** FA-1 (NE 3529, 3849, 3850), FA-2 r2 (NE 93 to 4195, thirteen lines), `rust3-lim` (six lines) and SYN-1 (NE 288, 306, 3366, 3530, 3541) are all disjoint from NE:3540. SYN-1 inserts a row after NE:3541, so with both bound the table reads: release declaration, SD-5's row, the producer cause and carrier row, SYN-1's row. B-S1's eleven bound NE lines are disjoint. `build_sd5.py` asserts all of this.

**Evidence runs** (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read-only):
- `build_sd5.py`, then `build_sd5.py --check`: identical bytes.
- `check_sd5.py`: pass.
- `verify_scratch.py --rev cd5958b` and on the main checkout at `cd5958b`: SD-5 binds, 82 to 83, with one override and no supersession. The selected inventory and inheritance are unchanged. FA-1, FA-2 and SYN-1 each bind with it in both orders. A later override of NE:3540 refuses with "conflicting contract passage overrides". On the checkout, 40 generation sources are verified.

## Controls owed by the implementing units

- **D4-T1** (D4, with J-C10b): for each of EE-1, EE-3b, EE-4's manifest part and EE-5a, on paths 3a, 3b and ER10a, the envelope is request-rejected 2, `EXTENSION.ADMISSION_REJECTED`, with `domainDetail` `PAYLOAD-NOT-ADMISSIBLE`, subject `excluded-form:<class>:<manifestDigest>` and this remedy. `errors` equals it, and there is no runId or executionId.
- **Two refusals:** two excluded manifests, or one manifest with two classes, give the subject of the least `manifestDigest` and the first class, and the operational record holds both.
- **Distinctness:** a request with an excluded-form manifest and a missing required closure ends request-rejected 2 at R10a, with no Coverage. The same request without the excluded manifest reaches row 27. An ephemeral request with no trust view reaches row 27, never this row.
- **J-C20:** row 56.

## Not claimed

- No product code, test, build or checker run was made. Only the three evidence scripts ran, read-only.
- No law is amended. No class, exit, error code, fault cause or public detail code is added, and no registry, schema, WS, WSE or SL byte changes.
- The request-class route (X-SD5-1) and the rest of SD-5 are not decided here.
- No Linux claim.

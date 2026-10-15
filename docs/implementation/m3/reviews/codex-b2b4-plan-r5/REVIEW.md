# B2B4-PLAN-r5 review

Verdict: **REQUIRED-FINDINGS**

Independently verified subject.json: 658 bytes, SHA-256 `21dd1bd26b46d0c2284e09997b0ade007db63326351b409e7632573662a30e83`. Both members match:

- PLAN-r5.md: 31,004 bytes, SHA-256 `d2b440ba240e80358db0ad43b4e9282d04a2ab47715c74a462569f4e3e3845fa`.
- HELD-OUT-T2-MARGIN.md: 1,589 bytes, SHA-256 `375bbc6bbeccb9d1142f748c3416fe239516e385ca1b93fd73f2696ca6fe62d0`.

Product main is clean at `d33df45ac0a5422efbebb43eee9c652d17ee742a`; architecture is at `de2388edc19dec8c7ed2bffd0ceef2314d86cddc`. Reviewed the entire r4→r5 diff, the supplied owner record, the owning B2-b plan and current law limitations, and the current census generator/checker and margin-test integration. No held-out store or overlay was opened.

## Required findings

### B2B4PLAN-R5-RF-1: Define how blind results survive ordinary regeneration and remain bound to the reviewed inputs

Location: `docs/implementation/m3/config-discovery-b/b2-b4/PLAN-r5.md:229-242 (section 2.5)`.

The plan replaces outstanding held-out rows in the shared generated census, but gives no ordinary-mode preservation/checking rule. At the pinned product base, census_output always emits outstanding rows for held-outs and heldOutMargin=outstanding; main --check compares the entire regenerated file byte for byte, while --write replaces it. Thus the specified blind run makes the retained ordinary census --check fail, and an ordinary regeneration erases its result. Blind rows also omit raw costs, so they cannot simply be carried across a changed manifest, model/closure or cap profile and still establish the current margin. The plan does not state the binding/invalidation rule or how the top-level state and failure list are reconciled with its instruction to write only held-out rows.

Required change: Specify a reviewed blind-result lifecycle: how the ordinary mode validates/preserves or separately composes the authorized result without opening held-out stores; which exact reviewed manifest, model/tool, cost-closure, caps and root-length inputs the receipt binds; and when drift invalidates the result or requires a newly reviewed run. Define the permitted top-level updates (heldOutMargin and failure/cap state) and keep all lead-readable/workspace evidence unchanged except such explicit updates. Add synthetic controls for blind run followed by ordinary --check/regeneration, input drift, and forbidden ordinary held-out access. Metadata binding can use existing public pins and must not add content-bearing output.

### B2B4PLAN-R5-RF-2: Define error rows and require complete successful coverage before declaring the margin held

Location: `docs/implementation/m3/config-discovery-b/b2-b4/PLAN-r5.md:216-245 (section 2.5)`.

The allowed row fields and classification describe computed margins, but INTEGRITY, POPULATION, MODEL and IO failures can occur before any margins exist. The plan nevertheless says every failure becomes a class and a failing row has its margins only. It does not define where the class goes, whether unavailable margins are absent/null, or the exact success rule for integrity/population failure versus a genuine low margin. Its margin-only passes2x equivalence applies to successful measurements, not errored or missing rows. Without explicit row variants and exact held-out-ID coverage, the after-run test could accept high/stale margin values despite a failed verification, or overlook an omitted/duplicated entry. Existing listed controls do not cover MODEL/IO failures or these aggregate-state cases.

Required change: Define a closed success-row and error-row format. Successful measurements require passed integrity/population checks and three valid margins; error rows emit only the manifest ID, false/error status and an allowed class, with no fabricated margins or exception text. Define passes2x from the margins only for successful measurements, and require exactly one successful passing row for every expected held-out ID before heldOutMargin can become holds. Define failure versus incomplete/error top-level states and keep the completion gate open for either. Extend synthetic canary/output allow-list controls to MODEL and IO errors, absent/duplicate/unknown IDs, and failure rows carrying misleading margin values; capture stdout and stderr as well as saved output.

## Findings on the requested design

The supplied owner record explicitly selects option 1 and preserves the offered options rather than inferring assent from silence. It authorizes the lead's mechanical blind run, with a Codex review of code before the run and of the result afterwards. The assessment treats that user-supplied record as the decision authority; an independent transcript of the originating AskUserQuestion is not included in this subject. The record does not select either a weaker gate or another runner. The plan follows the selected workflow in intent, subject to RF-1 and RF-2. It does not authorize a reviewer to inspect held-out contents.

The intended disclosure surface is appropriately narrow: manifest IDs already known to the lead, pass/fail information and integer margins. Integrity/population booleans are pass/fail information. The pass/fail summary counts outcomes, not tree objects. No actual tree counts, paths, sizes, names, exception messages or additional digests are needed. RF-2 must turn that intention into an unambiguous closed format, including error classes and unavailable measurements.

A separate mode-guarded join is sound in principle. The ordinary store_path refusal must remain intact; the blind function must enforce the held-out manifest row and expected store root, retain no-follow integrity behavior and never become a route usable by the ordinary mode. This review approves the proposed separation, not an implementation that has yet to be written.

Reusing the integrity checks, reference population, model and actual code caps is correct. The manifest contains ten held-out repositories and no held-out workspace, so leaving workspace rows unaffected is factually accurate. Workspace full-ledger margins nevertheless remain outstanding under r6/r7 until the B3-b member-observation bound. A successful blind repository census must not close that separate obligation or imply qualification.

For a positive modeled cost c and positive cap L, floor(1000 L / c) >= 2000 if and only if L >= 2c. Thus the proposed integer-margin classification is exactly equivalent to fitting twice in each dimension for successfully computed measurements. No rounding approximation is required. That equivalence does not validate the provenance, completeness or verification status of a blind row; RF-1/RF-2 cover those requirements.

The two-review sequence and synthetic-only pre-run controls are appropriate. Returning a genuine insufficient-margin result to item 12, with no hand-raised caps and B2-b still open, is also appropriate. Integrity/model/I/O failures require their own incomplete/error treatment rather than invented costs or a margin pass.

Sections 1 through 2.4 are unchanged from accepted r4, byte for byte apart from adjacent new-section whitespace. Existing LD-B2B4-1 through 9 remain unchanged; only LD-B2B4-10 is added. Earlier accepted implementation remains closed. The new workflow must coexist with the retained ordinary census generation/checks, as RF-1 requires.

## Non-blocking observation

**B2B4PLAN-R5-NBO-1** (`PLAN-r5.md r5 changes quotation; REQUEST.md Bases`): The plan labels its selected-option quotation verbatim but omits the owner-record option text's opening Authorize and capitalizes the following article. Preserve the full option text or label this an excerpt. The request also describes the exact bases as inventory v195/shared r95, while those hashes are inventory v198/shared r98. The subject manifest pins and the staged plan's historical-base labels are consistent; these are presentation corrections.

## Boundaries and interpretation

The positive JSON fields describe sound proposed mechanisms or the supplied decision record, not completed code. The false fields identify unresolved output/error/lifecycle requirements. No code, binding, law change or qualification is approved as already performed.

Used only read-only reading, hashing, JSON parsing and Git queries. No tests, Cargo, builds, lane or network was run. No other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or held-out store/overlay was accessed; no optional cache counting was needed. Neither repository, the stage nor control files was edited. Only REVIEW.md and review.json in the requested directory were written.

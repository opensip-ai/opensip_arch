# X4T-c continuation diagnostics r1

ACCEPT-DESIGN-UNIT. implementationVerdict ACCEPT-UNIT. requiredFindings empty.

Subject manifest `docs/implementation/m2/continuation-diagnostics-x4tc-r1-subject.json` is 12508 bytes, sha256 `ac2efcd404777786886821317815201536f2e9f7b525ccd7b4bef8810551661e`. All 55 members match. Their paths are sorted and unique, and `successor.json` appears once. Successor `docs/implementation/m2/continuation-diagnostics-x4tc-r1/successor.json` is 13176 bytes, sha256 `2e7aa09e1b7231fef86eec66b3c4a0f4e91f72544a729393f0f2b0820e990930`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED X4T-c exact role continuation diagnostics, current common4 append and complete materialization; public no-bypass drift required before integration".

`candidates` is the other 54 subject members. The record path is absent. Each candidate pin equals its subject pin, and the candidate paths are sorted and unique.

Product HEAD `e4356d591f9d48392310939eec2e561b2dd8d24d` and architecture HEAD `d43e1b0143d44e1e53e2291a76bbdf64995768c9` are the pinned bases. Product is tracked-clean. Architecture is tracked-clean. Its untracked drafts stay outside this unit. `~/Library/Application Support/OpenSIP` is absent. Against the pinned product tree of 967 tracked files, the candidate differs in exactly the seventeen existing product files below. Stage copies match the candidate bytes, and those bytes match `productAfter`. The same paths at the product base match `productBefore`. `design-lock.json` does not yet contain this successor. The current lock has 126 contract successors and selects inventory v166.

## Law and parents

Law X4T r12 is `docs/implementation/m2/trust-admission-x4t/PROPOSAL-r12.md`, 79182 bytes, sha256 `cf566db721c0dd3b24aabdbf4613062c59ecbf52d7f64ebed507016f9f9643fb`. The accepted law review `docs/implementation/m2/reviews/grok2-x4t-f2-r1/review.json` is ACCEPT with that subject hash. The law is pinned authority and is not a contract parent.

The Lead decision "two continuation codes" adds exactly `CONTINUE-INDEX-NOT-TRUSTED` and `CONTINUE-COMPONENT-NOT-TRUSTED` on the continuation row: request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`, by common4 append, public-detail rows, D9 routes, generation, and drift. Until this unit, item 10 publishes stored index and component refusals as `CONTINUE-CORE-NOT-TRUSTED`. Item 10's clocked core row stays `CONTINUE-CORE-NOT-TRUSTED` with subject `core:expired` or `core:stale-revocation`. A revoked closure component stays that same core detail.

The three parents match the architecture bytes and the pins already accepted by bound successors. There is no passage override and no inventory successor.

- Admitted 468a public registry `docs/implementation/m2/existing-root-diagnostics-468a/reference/public-detail-registry.json` is 62827 / `2832bf1f3e7c76bb91fd1ee99fce29e00cd472b9ea3a554d7751be165cc3d1f0`, first accepted by `existing-root-diagnostics-468a/successor.json`.
- Admitted current common4 `docs/implementation/m2/existing-root-diagnostics-468a/schemas/common.v4.schema.json` is 65062 / `661b9fdae1b15238160cd4812456c5bc91cadfd5202ea3201a3ac8aabe4708d4`, the same successor. It equals the product common4 before this unit.
- Current J-BS admission registry `docs/implementation/m3/host-pipeline-j/j-bs-admission-r1/schemas/admission-registry.json` is 17170 / `a4a02c4271245c7a0c3a401fea95dc93f1849004bee41c4c7b1a433e5ed19c30`, first accepted by `j-bs-admission-r1/successor.json`. It equals the product admission registry before this unit.

Inventory v166 remains 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, 1067 rows. All seventeen product paths already exist. None of those rows pins content. No product path is added.

## Preservation

`DomainDetailCode` in common4 keeps its 322 values in order and appends `CONTINUE-INDEX-NOT-TRUSTED` then `CONTINUE-COMPONENT-NOT-TRUSTED`. Every other JSON value in that schema is unchanged. The unit schema copy equals the product schema. Common1 and common3 files are outside the delta, and their generated `DomainDetailCode` types are unchanged.

The public registry keeps all 322 records and all 9 aliases by value. It inserts two security rows in code order: `CONTINUE-COMPONENT-NOT-TRUSTED` between `CONFIG.INVALID` and `CONTINUE-CORE-NOT-TRUSTED`, and `CONTINUE-INDEX-NOT-TRUSTED` between `CONTINUE-CORE-NOT-TRUSTED` and `CORE.NO_EMBEDDED_RELEASE`. Each new selector cites r12 and the request-rejected exit-2 route. The only new object is `trustContinuationCorrection`. Standing and the earlier correction metadata stay as inherited.

The product admission registry changes one source, common4, from 65062 / `661b9fda…` to 65142 / `2dd7964b6aca3b843e195b6d3fef0f91f5601d588523011fd5eb9da26314182b`. `SOURCE_PINS` in `schema_registry.rs` updates that same length and digest. `from_sources` still refuses a set whose length or raw digest misses the pin. `schema_sources.rs` already includes `common-v4.schema.json`; the include list is unchanged.

`generator-closure.json` changes two file pins: `schemas/source-map.json` and `schemas/sources/common-v4.schema.json`. Its other pins match the candidate files. The contracts-v1 recipe keeps its options pin and its eight output declarations. Its 40 `sourceSha256s` stay sorted and unique, equal the 40 `schemas/sources` closure pins, and differ from the previous list by replacing the old common4 digest with `2dd7964b…`. `generatorClosureSha256` is the after closure file, `d1f540bab5fa2133aedac906bace256ac755a3226abcc125d219d83778a08c9c`.

`schemas/source-map.json` retargets only the common4 architecture source to this unit's schema copy. `schemas/admission-source-map.json` retargets the registry architecture source to this unit's admission registry and the common4 architecture source to this unit's schema. `schemas/registry.json` updates the common4 `sourceSha256` and the recipe join above.

Prospective generation reports 40 sources and eight outputs, passed, with `productModified` false and `sourceApproved` false. The six outputs other than `evidence.rs` and `report.ts` match the product base bytes, including the hashes in `generation-result.json`. `evidence.rs` gains only the two `Common4DomainDetailCode` variants, their Display arms, and their parse arms, appended after `WORK.BUDGET_EXHAUSTED`. `report.ts` updates the registry and closure provenance lines to the after digests, appends the same two codes to `Common4DomainDetailCode`, and refreshes the embedded schema bytes. Common1 and common3 type lines stay put.

The explicit implementation preflight log is `Design verification failed: generation source is not selected by accepted design`, exit 1, `correctlyRefused` true. `publicDriftVerified` is false. This acceptance can authorize the later strict public-drift run on the real lock after root assent, through the genuine generator entry, with no monkeypatch, scratch pin, or source-policy bypass. A failure of that run holds integration. This record grants no X9 set and no qualification.

## Projection

Stored standing uses the role machine. `standing_of` publishes `RefuseCore` as `TrustRow::Continuation` (`CONTINUE-CORE-NOT-TRUSTED`), `RefuseIndex` as `IndexContinuation` (`CONTINUE-INDEX-NOT-TRUSTED`), and `RefuseComponent` as `ComponentContinuation` (`CONTINUE-COMPONENT-NOT-TRUSTED`). The subject stays `core:`, `index:`, or `component:` plus the existing state token. The variant is chosen from `Standing`, so the runtime detail is not chosen by parsing the subject.

`admit_bound` still runs that stored join before authentication. Revoked closure components still return `TrustRow::Continuation` with the `{kind}:{subject}` text and cause `revoked-component`. `live_observation::classify` still treats a `release:`, `keyId:`, `namespace:`, or `catalogSnapshot:` continuation as revoke, and treats both new variants as `ObservationFailure::Standing`.

`clocked_standing_of` runs `standing_of` and maps only `IndexContinuation` and `ComponentContinuation` back to `Continuation`, keeping the subject and the refusal cause. The fenced read at tEval and the reread both join through `clocked_standing_of`. Clocked core expiry and staleness stay `CONTINUE-CORE-NOT-TRUSTED`. An expired or stale index alone stays `ExistingOnly`. Authentication, I/O, floor publication, write-ahead, role-state storage, and identity checks are the previous functions; the extra diff in those regions is formatting.

`operation_guard` maps the two new rows to `TrustIndexContinuation` and `TrustComponentContinuation`, copying the subject. The host termination match is exhaustive and sends both through the existing `admission` helper: request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`, fault none, and the matching `Common4DomainDetailCode`, with the original subject. No new class, exit, error code, or fault is added. No capacity, HSR, or E2s materialization and no new schema reader are in the delta.

## Controls

`evidence/checks.py` was not run. The supplied logs were read. They match its locked offline nice-10 commands: security library, `schema_sources::tests`, `installation_termination::tests`, and clippy `-D warnings` on security and host with `scenario-fixtures,crash-matrix`.

- `security-library.log`: `test result: ok. 1037 passed; 0 failed; 2 ignored`. The ignored tests are the existing host-observation pilot and the existing real-host clock composition. `clocked_join_preserves_core_detail_and_exact_subject` passed. Stored index and component controls now expect the role-specific row and code. Clocked `core:expired` and `core:stale-revocation`, and revoked-closure continuations, still expect `Continuation`.
- `host-source-controls.log`: 7 passed, 0 failed. `initialization_details_are_current_only_and_unknown_codes_still_refuse` admits both new codes on current common4 and on `Common4DomainDetailCode`, and refuses them on common1, common3, and the generated common1 and common3 enums.
- `host-route-controls.log`: 5 passed, 0 failed, including `role_specific_continuation_details_preserve_the_d9_route`.
- `feature-clippy.log`: Finished, with no `warning:` and no `error:`. The eight format logs are empty.

After root assent, `verify_design` runs on the current main lock. The seventeen product files land in one code commit and this bind in a separate lock commit. The strict public-drift check is required before that integration. Nothing is pushed.

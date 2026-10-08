# J3a-o whole code unit r1

Verdict: **ACCEPT-UNIT**. Required findings: none. This accepts the eleven-file wiring leg only. It authors no inventory, qualifies no product, and does not close O1-b, J3d, or M3.

Subject `subject.json` is 2344 bytes, sha256 `b716ad14ef9699910803a4fce67b2241c31036913f99e6d4ae34214018833913`, with 11 sorted members. Every pin matches the frozen candidate. Against product `14e989de220db1d271bb63c716748df5527593f0` the tree differs in those eleven files: eight modifications and three new refusal cases. `design-lock.json` is unchanged, so the current lock remains inventory v168, 128 inventory successors, and 140 contracts. The evidence logs name the authoring tree; its eleven files are byte-identical to the candidate.

## Wiring

O1 item 8 gives RequestId the form `From<&RequestIdentity>` and ExecutionId the form `From` the reserved platform value. SOP2 item 8(a) is that owning-type conversion. Item 9 still gives attempt and Run scopes only to their later admission and publish transitions.

`RequestScope` implements `From<&opensip_platform::RequestIdentity>` by copying `identity.bytes()` into the existing `RequestId` wrapper. `ExecutionId` implements `From<&opensip_platform::ReservedExecutionId>` by copying `identity.bytes()` into the existing `ExecutionId` wrapper. Both wrappers keep `minted` and `text` as `pub(crate)`. The new impls add no marker trait, no attempt scope, and no Run scope. `ExecutionId` is re-exported by its existing name. The crate-local byte test checks the request bytes and checks `ExecutionId` text against `ReservedExecutionId::as_str()`.

`RequestAuthority::logging_scope` calls the existing pointer lookup `identity` and converts only that lent `&RequestIdentity`. A foreign context, a forced reservation with no stored identity, and a repeated lend do not change the reservation or identity maps. `MetadataHost::logging_scope` returns `None` unless `capabilities` is present, then delegates. The host method draws nothing and does not allocate a request. The production diffs emit no event. `host.repair.completed` appears only in the external identity helper.

## Refusals and census

The three new paired cases convert `&RequestIdentity` and `&ReservedExecutionId` on the lawful side. Raw request bytes, raw execution bytes, and `ReservedExecutionId` into `AttemptScope` are annotated `E0277` on the `into` line. The case table is 28 files. The driver still has four self-test files. The structural function is unchanged: 10 non-field refusals and 13 bound mutations. `cargo test --test refusal_tests` reports 3 passed.

Ordinary exception rows, termination files, and the support-module list are unchanged: 113 rows. The checker adds lexical `from` and `into` names and still does no receiver inference. Recomputing `mint_inventory` on the candidate equals the audited `mintAudit` rows: 425. `scope.rs` now records two `from` definitions and 18 `minted` calls. The new checker test refuses both an added `into` call and a removed `from` call. Source control reports 113 rows and no findings. Checker tests report 18 passed. There is no separate mint-list file.

## Controls

Default operability reports 83 passed. Development operability reports 86 passed. Host request tests report 7 passed in each configuration, including `logging_scopes_require_the_owned_platform_reservation`. The logging test reports 1 passed in each configuration, including the owned, foreign, and no-start scope assertions. Warning-denied Clippy for operability, host, and CLI finishes in both the default and `operability-dev-sinks` configurations, and the logs contain no warning line.

Six fresh-process runs use distinct `req1_` values. Each stdout envelope carries that value. Each development stderr repair line and loss line carry the same value. All three default stderr streams are empty. The featureless release binary is 6357808 bytes, sha256 `812a98900d905d80d99f984ba84a236bca8f1234d00ed470f8b52698bac60eaf`, and contains neither sink marker. Saved help, version, and rejection envelopes match the accepted O1-a release binary after replacing `requestId`; both stderr streams are empty.

`inventoryAuthored` is false. `productQualification` is false. `entirePlanComplete` is false. Integration still needs lead assent, the code commit, and the architecture receipt, then a separate additive inventory v169. J3d still owns project, attempt, and Run wiring.

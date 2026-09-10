"""BV6-V3-RECEIPT: publish the deterministic idempotency key and lookup/delivery meaning for the
required import and native-preparation receipts, and correct the receipt-domain claim."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work')
P = W / 'docs/coop/design-corrections/workflows/schemas/repair.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = d['x-opensip-mutation-operation-map']

law['receiptOperationIsRequiredNotOptional'] = (
    "MutationReceiptV1 REQUIRES both `operation` and `idempotencyKey`. invocation-record "
    "ImportResult and NativePreparationResult BOTH require `receiptId`, and ReceiptId is "
    "`receipt2:`. `workflow.mutation-receipt` is the OWNING MUTATION receipt domain for those "
    "result branches; it is not the only `receipt2:` domain - workflows section 10 also lists "
    "`workflow.verification-link`, which is a different record with a different purpose, and an "
    "earlier revision of this map wrongly said exactly one receipt domain exists. So an import step "
    "and a native-preparation step each already owe a receipt carrying BOTH required fields, and "
    "what was missing was the binding for each. An earlier revision inferred from the reference "
    "model that no emitter existed and disclosed them as operations with no published emitter; that "
    "inference was wrong, because the absence of a Python emitter is a QUALIFICATION limit and not "
    "evidence that a required receipt field has no law. Both fields are bound below."
)
law['receiptIdempotencyKeyByStepKind'] = collections.OrderedDict([
    ('standing',
     "Normative and CLOSED. The deterministic idempotency key of the REQUIRED receipt, per step "
     "kind. It introduces NO new H domain, no new record and no new authority: every recipe below "
     "is an existing published one. An earlier revision said the three non-generic step kinds mint "
     "no H(workflow.mutation-intent) key at all; that is corrected here, and the correction is "
     "possible precisely because MutationReplayScopeV1.operation already admits `import` and "
     "`native-preparation` - two of the 23 tokens of the generic field domain. Narrowing that "
     "domain to the current generic emitters would have removed the very values this law needs."),
    ('sharingARecipeIsNotSharingReplayAuthority',
     "Two different things were conflated by the earlier wording. The KEY RECIPE is a deterministic "
     "function of immutable admitted inputs and grants nothing. The LOOKUP/DELIVERY MEANING is what "
     "a host may do when it finds a completed receipt under that key, and it differs per step kind "
     "and is stated separately below. Import and native-preparation remain excluded from GENERIC "
     "MUTATION step handling: they carry their own params (ImportParams, NativePreparationParams), "
     "not MutationParams, they are not generic `mutation` steps, and their retryPolicy is `none` by "
     "schema (workflows section 1)."),
    ('recipes', collections.OrderedDict([
        ('mutation', collections.OrderedDict([
            ('key', 'H("workflow.mutation-intent", MutationReplayScopeV1)'),
            ('preimage', '{schemaVersion: 1, requestId, stepId, projectId, operation}'),
            ('owner', 'workflows-and-surfaces.md section 1, unchanged'),
            ('lookupMeaning', "an equal COMPLETED receipt permits delivery replay with no second "
                              "effect; different fresh requests never deduplicate each other."),
        ])),
        ('repair-apply', collections.OrderedDict([
            ('key', 'raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId})'),
            ('preimage', 'content-derived, not request-scoped'),
            ('owner', 'workflows-and-surfaces.md section 1, unchanged'),
            ('lookupMeaning', "an equal completed key performs no second effect; the original "
                              "receipt is immutable and a replay delivery is separately identified."),
        ])),
        ('import', collections.OrderedDict([
            ('key', 'H("workflow.mutation-intent", MutationReplayScopeV1) with operation "import"'),
            ('preimage', '{schemaVersion: 1, requestId, stepId, projectId, operation: "import"} - '
                         'exactly the closed scope record, whose operation domain already admits '
                         'this token. The UserInputPath of ImportParams is deliberately NOT in the '
                         'preimage: workflows section 4 keeps it out of identity entirely.'),
            ('boundTo', 'the host-minted RequestId of the admitted invocation, the StepId which is '
                        'the step position, and the ProjectId - all immutable once the invocation '
                        'is admitted.'),
            ('lookupMeaning', "DELIVERY ONLY, and only within that same retained invocation. A "
                              "completed receipt under this key permits re-delivering the SAME "
                              "already-admitted import result; it never performs a second staging "
                              "or a second effect, and because requestId is host-minted and fresh "
                              "per invocation it never deduplicates across requests. Custody "
                              "(nofollow open of the user path), mandatory SourceCorrespondence and "
                              "the StalenessRule disposition are unchanged and are re-checked; a "
                              "receipt is never a substitute for any of them."),
        ])),
        ('native-preparation', collections.OrderedDict([
            ('key', 'H("workflow.mutation-intent", MutationReplayScopeV1) with operation '
                    '"native-preparation"'),
            ('preimage', '{schemaVersion: 1, requestId, stepId, projectId, operation: '
                         '"native-preparation"}'),
            ('boundTo', 'the same immutable admitted invocation/step/project inputs. The attempt is '
                        'separately identified by its ExecutionId, which stays OUT of the key '
                        'because operational identities are excluded from content identity.'),
            ('lookupMeaning', "NOT REPLAY. The key identifies that step's receipt so a result can "
                              "cite it; it authorizes nothing. A completed receipt NEVER suppresses "
                              "or substitutes for a new preparation: a fresh preparation is a NEW "
                              "EXPLICIT AUTHORIZED EXECUTION requiring its own AuthorizedExecutionV2 "
                              "and security grant set per native section 5 and security S15, there "
                              "is NO automatic retry (native section 5.4), and nothing here grants a "
                              "permission the security unit does not already admit."),
        ])),
    ])),
    ('whatIsNotClaimed',
     "The reference model in this kit emits a MutationReceiptV1 only for repair-apply and does not "
     "exercise a production import or native-preparation emitter. That is a stated QUALIFICATION "
     "limit of the reference evidence and is deliberately distinct from the design law above, which "
     "is normative and complete: both required fields now have a published binding."),
])
law['enforcedAt'] = (
    "check_workflows.v1.py: every step-kind binding names a real step kind and a registered "
    "operation; both results that require a receiptId are checked to require it; MutationReceiptV1 "
    "is checked to require BOTH operation and idempotencyKey; the two non-generic key recipes are "
    "computed by the reference and checked to be the published H over the closed scope record, and "
    "to differ from each other and from the generic rows only in the operation token; the generic "
    "rows are exactly the commands with a `mutation` step; the admissible field domain is verified "
    "by ADMITTING every one of its operations at the actual field schema and REFUSING the excluded "
    "one; and the one operation no step kind binds is recomputed rather than restated."
)
d['x-opensip-mutation-operation-map'] = law

# the step-kind rows point at their key recipe and drop the now-corrected 'mints no key' claim
bysk = law['byStepKindReceiptOperation']
bysk['import']['notGenericReplay'] = (
    "An import step is NOT a generic mutation step: it carries ImportParams, not MutationParams, so "
    "it is not admitted through the generic MutationParams branch and its retryPolicy is `none` by "
    "schema (section 1). It DOES have a required receipt with a required idempotency key, whose "
    "recipe and DELIVERY-ONLY lookup meaning are published at "
    "#/x-opensip-mutation-operation-map/receiptIdempotencyKeyByStepKind/recipes/import. Its custody "
    "and source-correspondence joins are unchanged and are not replay machinery."
)
bysk['native-preparation']['notGenericReplay'] = (
    "A native-preparation step carries NativePreparationParams, not MutationParams, and there is NO "
    "automatic retry (native section 5.4). It DOES have a required receipt with a required "
    "idempotency key, published at "
    "#/x-opensip-mutation-operation-map/receiptIdempotencyKeyByStepKind/recipes/native-preparation, "
    "whose lookup meaning is explicitly NOT replay: a fresh preparation is a new explicit authorized "
    "execution under its own AuthorizedExecutionV2 and grant set, and no completed receipt ever "
    "suppresses one."
)
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok')

"""CX-BV6-04 rework after the Codex note: publish the deterministic step-kind -> receipt-operation
law. ImportResult and NativePreparationResult BOTH require receiptId, ReceiptId resolves to the one
`workflow.mutation-receipt` domain, and MutationReceiptV1.operation is a required MutationOperation.
So `import` and `native-preparation` are REQUIRED receipt operations with no published binding, not
operations with no emitter. That is a missing design law and is corrected here."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work')
DC = W / 'docs/coop/design-corrections'
P = DC / 'workflows/schemas/repair.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = d['x-opensip-mutation-operation-map']
ops = d['$defs']['MutationOperation']['enum']
inv = json.loads((DC / 'workflows/command-inventory.v1.json').read_text(encoding='utf-8'))['commands']
generic = law['byCommandGenericMutationStep']

law['standing'] = (
    "Normative and CLOSED. It publishes FOUR different things that an earlier revision conflated or "
    "left undefined, and keeps them apart by name: (1) which MutationOperation each step KIND writes "
    "to its required receipt, (2) which operation each current command's generic `mutation` step "
    "emits, (3) the one operation excluded from the generic fields, and (4) the ACTUAL admissible "
    "domain of the generic operation field, which is a property of the schema and is NOT the set of "
    "tokens today's commands emit. It adds no command, no operation, no request class, no step kind "
    "and no receipt, and it narrows no field."
)
law['receiptOperationIsRequiredNotOptional'] = (
    "There is exactly ONE receipt domain, `workflow.mutation-receipt` (workflows section 10), "
    "ReceiptId is `receipt2:`, and MutationReceiptV1 REQUIRES `operation` typed as MutationOperation. "
    "invocation-record ImportResult and NativePreparationResult BOTH require `receiptId`. So an "
    "import step and a native-preparation step each already owe a receipt carrying an operation, and "
    "what was missing was the binding that says WHICH one. An earlier revision of this map inferred "
    "the opposite from the reference model - that no emitter existed - and disclosed `import` and "
    "`native-preparation` as operations with no published emitter. That inference was wrong: the "
    "absence of a Python emitter in a reference model is a QUALIFICATION limit, not evidence that a "
    "required receipt has no operation. The binding is published below."
)
law['byStepKindReceiptOperation'] = collections.OrderedDict([
    ('mutation', collections.OrderedDict([
        ('operation', 'the command row in byCommandGenericMutationStep'),
        ('carriedBy', ['invocation-record MutationParams.mutationClass',
                       'invocation-record MutationReplayScopeV1.operation (equal to it)',
                       'repair MutationReceiptV1.operation']),
        ('citations', ['workflows-and-surfaces.md section 1 - generic mutation idempotence and the '
                       'H(workflow.mutation-intent, MutationReplayScopeV1) key']),
    ])),
    ('repair-apply', collections.OrderedDict([
        ('operation', 'repair-apply'),
        ('carriedBy', ['repair MutationReceiptV1.operation']),
        ('citations', ['invocation-record RepairApplyParams - its own step params',
                       'workflows-and-surfaces.md section 1 - the dedicated content-derived '
                       'idempotency recipe, explicitly excluded from generic MutationParams']),
        ('excludedFromGenericFields', True),
    ])),
    ('import', collections.OrderedDict([
        ('operation', 'import'),
        ('carriedBy', ['repair MutationReceiptV1.operation, named by ImportResult.receiptId']),
        ('citations', ['invocation-record ImportResult - `receiptId` is REQUIRED',
                       'workflows-and-surfaces.md section 4 - `opensip import KIND PATH` is a '
                       'mutation step with an import receipt',
                       'workflows-and-surfaces.md section 10 - workflow.mutation-receipt is the one '
                       'receipt domain']),
        ('appliesToEveryImportStep',
         "The binding is by STEP KIND, not by command request class, so the import step of the "
         "`analyze` command (requestClass analysis) carries the same operation as the import step of "
         "the `import` command. `analyze` therefore needs no exception and none is made: it was never "
         "a defect in the map, it was a missing step-kind law, and an earlier revision subtracted it "
         "in the checker instead."),
        ('notGenericReplay',
         "An import step is NOT a generic mutation step: it carries ImportParams, not MutationParams, "
         "so it mints no MutationReplayScopeV1 and no H(workflow.mutation-intent) key, and its "
         "retryPolicy is `none` by schema (section 1). Its custody and source-correspondence joins "
         "(nofollow open of the UserInputPath, mandatory SourceCorrespondence, StalenessRule) are "
         "unchanged and are not replay machinery."),
    ])),
    ('native-preparation', collections.OrderedDict([
        ('operation', 'native-preparation'),
        ('carriedBy', ['repair MutationReceiptV1.operation, named by NativePreparationResult.receiptId']),
        ('citations', ['invocation-record NativePreparationResult - `receiptId` is REQUIRED',
                       'native-evidence.md section 14 - a completed preparation returns an execution '
                       'receipt and one admitted prepared import, never a Run',
                       'workflows-and-surfaces.md section 12 - per-owner native preparation, '
                       'delegated to native section 14 and security S15']),
        ('notGenericReplay',
         "A native-preparation step carries NativePreparationParams, not MutationParams. It mints no "
         "generic replay scope, its retryPolicy is `none` by schema and there is NO automatic retry "
         "(native section 5.4). A fresh preparation is a NEW authorized execution under its own "
         "AuthorizedExecutionV2 and security grant set - never a delivery replay of a prior receipt, "
         "and this binding grants no permission that the security unit does not already admit."),
    ])),
])
law['emissionRule'] = (
    "Which operation a receipt carries is a deterministic function of the STEP KIND, per "
    "byStepKindReceiptOperation. Only the generic `mutation` step additionally carries the operation "
    "in a request field (MutationParams.mutationClass) and in a replay scope; the other three step "
    "kinds carry it on the receipt alone, under their own params and their own idempotency law. A "
    "command with none of these four step kinds mints no operation at all."
)
law['byCommandGenericMutationStep'] = generic
law['operationsWithNoCommandInThisInventory'] = collections.OrderedDict([
    ('operations', ['config-write']),
    ('disclosure',
     "`config-write` is the one MutationOperation member no step kind binds and no command in this "
     "inventory emits: nothing here writes product configuration. It is disclosed rather than "
     "removed - a vocabulary change this correction does not own - and it remains admissible in the "
     "generic field, because narrowing a generic domain to today's emitters would remove a value no "
     "finding asked to remove."),
    ('scopeOfTheSearch',
     "The current command inventory, the four step-kind bindings above, and the non-review source "
     "tree of this subject snapshot. It is not a claim about every historical file or revision."),
])
law.pop('operationsWithNoPublishedEmitter', None)
law['injectivityIsNotAssumed'] = (
    "This map is NOT an inverse map and must not be read backwards. The `import` operation is bound "
    "by STEP KIND, so BOTH the `import` command and the `analyze` command emit it - a worked case of "
    "two commands sharing one operation, which is exactly why injectivity is not assumed. The twenty "
    "generic `mutation` rows happen to carry twenty distinct operations, and that is recorded as an "
    "observation about the current inventory, not as a law: an operation is an effect class and a "
    "command is a surface."
)
law['whatIsNotClaimed'] = (
    "The reference model in this kit emits a MutationReceiptV1 only for repair-apply. It does not "
    "exercise a production import or native-preparation receipt emitter, and this map does not claim "
    "it does. That is a stated QUALIFICATION limit of the reference evidence, and it is deliberately "
    "distinguished from the design law above, which is normative and complete: the receipt is "
    "required, its operation is required, and the value each step kind writes is now published."
)
law['enforcedAt'] = (
    "check_workflows.v1.py: every step-kind binding names a real step kind and a registered "
    "operation; the generic rows are exactly the commands with a `mutation` step; each row names a "
    "real step and request class of that command; both results that require a receiptId are checked "
    "to require it; the admissible field domain is verified by ADMITTING every one of its operations "
    "at the actual field schema and REFUSING the excluded one; and the one operation with no command "
    "is recomputed rather than restated."
)
d['$defs']['MutationOperation']['description'] = (
    "The closed effect-class vocabulary of a mutating step. Which operation each STEP KIND writes to "
    "its required receipt is published beside this enum at "
    "#/x-opensip-mutation-operation-map/byStepKindReceiptOperation, and which operation each current "
    "command's generic `mutation` step emits is at "
    "#/x-opensip-mutation-operation-map/byCommandGenericMutationStep; four commands do NOT share "
    "their operation's name, so name matching is not the derivation, and `import` is emitted by two "
    "commands, so the map is not invertible. Neither map is the admissible domain of the generic "
    "operation field: #/x-opensip-mutation-operation-map/admissibleGenericFieldDomain is, and it is "
    "every member here except `repair-apply`. `config-write` is the one member no step kind binds."
)
d['x-opensip-mutation-operation-map'] = law
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok; step kinds', list(law['byStepKindReceiptOperation']))

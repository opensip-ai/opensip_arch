"""CX-BV6-04: separate command names, emitted operations and the admissible generic field domain."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work')
DC = W / 'docs/coop/design-corrections'

P = DC / 'workflows/schemas/repair.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = d['x-opensip-mutation-operation-map']
ops = d['$defs']['MutationOperation']['enum']
inv = json.loads((DC / 'workflows/command-inventory.v1.json').read_text(encoding='utf-8'))['commands']
cmds = {c['name']: c for c in inv}

old_by_command = law['byCommand']
generic = collections.OrderedDict(
    (n, r) for n, r in old_by_command.items() if r['mintedByStepKind'] == 'mutation')
assert len(generic) == 20, len(generic)

new = collections.OrderedDict()
new['standing'] = (
    "Normative and CLOSED. It publishes THREE DIFFERENT things that an earlier revision of this map "
    "conflated, and keeps them apart by name: (1) which MutationOperation each current command's "
    "generic `mutation` step EMITS, (2) the one DEDICATED step operation, and (3) the ACTUAL "
    "admissible domain of the generic operation field, which is a property of the schema and is "
    "NOT the set of tokens today's commands happen to emit. It adds no command, no operation, no "
    "request class and no step kind, and it narrows no field."
)
new['theConflationThisReplaces'] = (
    "The earlier `genericMutationClasses` listed twenty COMMAND NAMES while the annotations on "
    "MutationParams.mutationClass and MutationReplayScopeV1.operation called that list the exact "
    "admissible operation set. Those are different vocabularies and they differ in nine places: "
    "three listed names (baseline-upgrade, policy-init, waive) are refused by the operation enum, "
    "and six admitted operation tokens (baseline-upgrade-apply, config-write, import, "
    "native-preparation, policy-write, waiver-change) were absent from the list. The lists below are "
    "named for what they actually are."
)
new['emissionRule'] = (
    "A command carries a MutationOperation only through a step whose params carry one. In this kit "
    "exactly two step kinds do: the generic `mutation` step, whose MutationParams.mutationClass "
    "carries it and whose MutationReplayScopeV1.operation must equal it, and the dedicated "
    "`repair-apply` step. `ImportParams` and `NativePreparationParams` carry NO operation field, so "
    "no import step and no native-preparation step is shown to emit an operation anywhere here - "
    "which is why the `analyze` command, whose steps include `import`, has no row and needs no "
    "exception: the rule already excludes it, and an earlier revision subtracted `analyze` in the "
    "checker instead of deriving it."
)
new['byCommandGenericMutationStep'] = generic
new['dedicatedStepOperations'] = collections.OrderedDict([
    ('repair-apply', collections.OrderedDict([
        ('command', 'repair-apply'),
        ('stepKind', 'repair-apply'),
        ('citations', [
            'invocation-record.schema.json#/$defs/RepairApplyParams - its own step params',
            'repair.schema.json#/$defs/MutationReceiptV1.operation - the receipt field it is written to',
            'workflows-and-surfaces.md section 1 - the dedicated content-derived idempotency recipe',
        ]),
        ('excludedFromGeneric', True),
        ('note', "Refused as MutationParams.mutationClass and as MutationReplayScopeV1.operation by "
                 "an explicit `not` beside each $ref. Listing it here does NOT make it admissible "
                 "there, and a control holds both refusals."),
    ])),
])
new['operationsWithNoPublishedEmitter'] = collections.OrderedDict([
    ('operations', sorted(set(ops) - {r['operation'] for r in generic.values()} - {'repair-apply'})),
    ('disclosure',
     "Members of the operation vocabulary that NO command in this inventory is SHOWN to emit here. "
     "`config-write` has no command at all: no command in the inventory writes product "
     "configuration. `import` and `native-preparation` name real step kinds, but those steps' params "
     "(ImportParams, NativePreparationParams) carry no operation field and no retained record in "
     "this kit binds an operation to them, so an earlier revision's claim that they carry their "
     "operation `on the receipt only` was an INFERENCE WITH NO CITATION and is withdrawn. This is a "
     "disclosure of what this kit does not establish, not a removal from the vocabulary and not an "
     "authorization to mint one."),
    ('scopeOfTheSearch',
     "The current command inventory and the non-review source tree of this subject snapshot. It is "
     "not a claim about every historical file or every past revision."),
])
new['admissibleGenericFieldDomain'] = collections.OrderedDict([
    ('fields', ['invocation-record.schema.json#/$defs/MutationParams/properties/mutationClass',
                'invocation-record.schema.json#/$defs/MutationReplayScopeV1/properties/operation']),
    ('operations', sorted(set(ops) - {'repair-apply'})),
    ('rule',
     "Every MutationOperation member EXCEPT repair-apply, which both fields refuse by an explicit "
     "`not`. This is the SCHEMA's domain and is deliberately WIDER than the set of tokens today's "
     "commands emit: narrowing a generic field to the current emitters would silently remove "
     "admissible values that no finding asked to remove, and would have to change again whenever a "
     "command is added. Complete MutationParams additionally require operation-specific fields for "
     "the core-* / store-* / repair-recover operations; those are per-operation requirements, not "
     "enum exclusions."),
])
new['renamedRows'] = law['renamedRows']
new['renamedRowsNote'] = law['renamedRowsNote']
new['injectivityIsNotAssumed'] = (
    "The twenty generic rows above happen to carry twenty distinct operations, and that is recorded "
    "as an OBSERVATION about the current inventory, not as a law. Nothing in the design forbids two "
    "commands from emitting one operation - an operation is an effect class and a command is a "
    "surface - so this map is not an inverse map and must not be read backwards to identify a "
    "command from an operation."
)
new['notARequestGrammar'] = law['notARequestGrammar']
new['enforcedAt'] = (
    "check_workflows.v1.py: the generic rows are exactly the commands with a `mutation` step, each "
    "row names a real step and request class of that command, every emitted value is a "
    "MutationOperation member, the admissible field domain is verified by ADMITTING every one of its "
    "operations at the actual field schema and REFUSING repair-apply there, the orphan set is "
    "recomputed rather than restated, and no command outside the inventory appears."
)
d['x-opensip-mutation-operation-map'] = new
d['$defs']['MutationOperation']['description'] = (
    "The closed effect-class vocabulary of a mutating step. Which command's generic `mutation` step "
    "emits which member is published beside this enum at "
    "#/x-opensip-mutation-operation-map/byCommandGenericMutationStep; four commands do NOT share "
    "their operation's name, so name matching is not the derivation. That map is NOT the admissible "
    "domain of the generic operation field: #/x-opensip-mutation-operation-map/"
    "admissibleGenericFieldDomain is, and it is every member here except `repair-apply`, which both "
    "generic fields refuse. `config-write`, `import` and `native-preparation` are members that no "
    "command in the current inventory is shown to emit."
)
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# ---------------------------------------------- annotations name the FIELD DOMAIN, not the commands
Q = DC / 'workflows/schemas/invocation-record.schema.json'
e = json.loads(Q.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ann = collections.OrderedDict([
    ('fieldDomainAuthority',
     'workflows/schemas/repair.schema.json#/x-opensip-mutation-operation-map/admissibleGenericFieldDomain'),
    ('commandEmissionMap',
     'workflows/schemas/repair.schema.json#/x-opensip-mutation-operation-map/byCommandGenericMutationStep'),
    ('scope',
     "GENERIC mutation steps. The ADMISSIBLE domain of this field is every MutationOperation member "
     "except repair-apply, which the `not` beside the $ref refuses; it is deliberately WIDER than "
     "the set of operations today's commands emit, and the command map is NOT this field's domain. "
     "An earlier annotation named the command list here, which was a different vocabulary."),
])
for path in (('MutationParams', 'mutationClass'), ('MutationReplayScopeV1', 'operation')):
    e['$defs'][path[0]]['properties'][path[1]]['x-opensip-vocabulary'] = ann
Q.write_text(json.dumps(e, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok; generic', len(generic), 'orphans', new['operationsWithNoPublishedEmitter']['operations'],
      'domain', len(new['admissibleGenericFieldDomain']['operations']))

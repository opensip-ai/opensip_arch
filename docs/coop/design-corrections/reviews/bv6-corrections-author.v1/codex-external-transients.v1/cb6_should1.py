import json, pathlib, collections

R = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections')
P = R / 'workflows/schemas/repair.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
assert 'x-opensip-mutation-operation-map' not in d

inv = json.loads((R / 'workflows/command-inventory.v1.json').read_text(encoding='utf-8'))
commands = {c['name']: c for c in inv['commands']}
ops = d['$defs']['MutationOperation']['enum']

# The map, written out explicitly rather than derived by name matching: three rows are renames and
# a rule that guessed would get them wrong.
BY_COMMAND = [
    # (command, step kind that mints it, operation, note)
    ('baseline-adopt', 'mutation', 'baseline-adopt', None),
    ('baseline-export', 'mutation', 'baseline-export', None),
    ('baseline-upgrade', 'mutation', 'baseline-upgrade-apply',
     "RENAME. The command runs `analysis` then `mutation`; the operation names the APPLY half, "
     "because the analysis half mints a Run and no mutation."),
    ('core-repair', 'mutation', 'core-repair', None),
    ('core-rollback', 'mutation', 'core-rollback', None),
    ('core-update', 'mutation', 'core-update', None),
    ('import', 'import', 'import',
     "The `import` command's mutating step is an `import` step, not a generic `mutation` step, so "
     "its operation appears on the receipt and never as MutationParams.mutationClass."),
    ('install', 'mutation', 'install', None),
    ('policy-init', 'mutation', 'policy-write',
     "RENAME. `policy-init` is the command that writes a policy document for the first time; the "
     "operation is the effect class `policy-write`, which is why one operation covers it. It is "
     "NOT `config-write`: product configuration is a different document with no command here."),
    ('purge', 'mutation', 'purge', None),
    ('repair-apply', 'repair-apply', 'repair-apply',
     "DEDICATED, and EXCLUDED from the generic path: repair apply is its own `repair-apply` step "
     "with its own content-derived idempotency key, and `repair-apply` is refused as "
     "MutationParams.mutationClass and as MutationReplayScopeV1.operation. It is in this map "
     "because it is a real command/operation pair, not to enable it there."),
    ('repair-recover', 'mutation', 'repair-recover', None),
    ('review-join', 'mutation', 'review-join', None),
    ('store-gc', 'mutation', 'store-gc', None),
    ('store-migrate', 'mutation', 'store-migrate', None),
    ('store-rollback', 'mutation', 'store-rollback', None),
    ('trust-import', 'mutation', 'trust-import', None),
    ('trust-recovery-challenge', 'mutation', 'trust-recovery-challenge', None),
    ('trust-recovery-import', 'mutation', 'trust-recovery-import', None),
    ('trust-refresh', 'mutation', 'trust-refresh', None),
    ('update', 'mutation', 'update', None),
    ('waive', 'mutation', 'waiver-change',
     "RENAME. `waive` adds a waiver; the operation is the effect class `waiver-change`, which also "
     "covers the amendment and revocation this same command performs."),
    ('native-prepare', 'native-preparation', 'native-preparation',
     "The command's mutating step is a `native-preparation` step, not a generic `mutation` step; "
     "its operation appears on the receipt and never as MutationParams.mutationClass."),
]
by_command = collections.OrderedDict()
for name, step, op, note in sorted(BY_COMMAND):
    assert name in commands, name
    assert op in ops, op
    assert step in commands[name]['steps'], (name, step)
    row = collections.OrderedDict([('operation', op), ('mintedByStepKind', step),
                                   ('requestClass', commands[name]['requestClass'])])
    if note:
        row['note'] = note
    by_command[name] = row

mapped = {r['operation'] for r in by_command.values()}
generic = sorted(n for n, r in by_command.items() if r['mintedByStepKind'] == 'mutation')

law = collections.OrderedDict()
law['standing'] = (
    "Normative and CLOSED. THE map from the closed command-name vocabulary "
    "(workflows/command-inventory.v1.json#/commands[].name, the declared SOLE command list) to "
    "#/$defs/MutationOperation. It adds no command, no operation, no request class and no step "
    "kind, and it widens no accepted request: it publishes a derivation a consumer previously had "
    "to guess. It is written out rather than computed by name matching because three rows are "
    "renames that any name-matching rule would get wrong."
)
law['whyItIsOwed'] = (
    "`mutationClass` is a PUBLIC envelope field (MutationReceiptProjection.operation), workflows "
    "section 1 makes MutationReplayScopeV1.operation equal to MutationParams.mutationClass, and "
    "that scope is the whole preimage of the published idempotencyKey "
    "H(workflow.mutation-intent, scope). The Command record carries no mutationClass field, so "
    "nothing in the contracts derived the expected value for a command. The impact is BOUNDED and "
    "that is why this is a SHOULD, not a MUST: requestId is host-minted and unique per invocation, "
    "so the key is scoped to one request, a spelling difference cannot cause a false or missed "
    "dedupe ACROSS hosts, and the key grants no authority. What was lost is a consumer's ability to "
    "derive the expected value from the contracts alone."
)
law['rule'] = (
    "A command mints an operation only through a mutating STEP, and the step kind decides which "
    "surface carries it. `mutation` steps carry it as MutationParams.mutationClass and as "
    "MutationReplayScopeV1.operation; the `repair-apply`, `import` and `native-preparation` steps "
    "are their own step kinds with their own params and carry their operation on the receipt only. "
    "A command with no mutating step mints no operation and is absent from byCommand - it is not "
    "mapped to a null."
)
law['renamedRows'] = collections.OrderedDict([
    ('baseline-upgrade', 'baseline-upgrade-apply'),
    ('policy-init', 'policy-write'),
    ('waive', 'waiver-change'),
])
law['byCommand'] = by_command
law['genericMutationClasses'] = generic
law['excludedFromGenericMutation'] = collections.OrderedDict([
    ('operations', ['repair-apply']),
    ('rule', "repair-apply is refused by MutationParams.mutationClass and by "
             "MutationReplayScopeV1.operation, both of which carry an explicit `not: {const: "
             "repair-apply}` beside the $ref. Repair apply is a dedicated step whose idempotency "
             "key is the raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId}) - "
             "content-derived, not request-scoped. Publishing this map DOES NOT make it available "
             "there, and a control holds that."),
])
law['operationsWithNoCommand'] = collections.OrderedDict([
    ('operations', sorted(set(ops) - mapped)),
    ('disclosure', "`config-write` is a member of the MutationOperation vocabulary that NO command "
                   "in the closed inventory mints. It is stated rather than removed or invented a "
                   "command for: removing an operation member is a vocabulary change this "
                   "correction does not own, and no command writes product configuration today. A "
                   "receipt carrying it would come from a surface outside this inventory. This is a "
                   "disclosure, not an authorization to mint one."),
])
law['notARequestGrammar'] = (
    "Nothing here decides which commands a host accepts, which request class a command has, or "
    "which authorizations it needs. Those stay with command-inventory.v1.json and the security "
    "unit. This map answers exactly one question: given a command name, which MutationOperation "
    "does its mutating step carry."
)
law['enforcedAt'] = (
    "check_workflows.v1.py: the map is total over every inventory command with a mutating step, "
    "carries no command outside the inventory, every value is a MutationOperation member, the step "
    "kind it names is actually one of that command's steps, the operations with no command are "
    "exactly the disclosed set, and repair-apply stays schema-refused in both generic positions."
)

out = collections.OrderedDict()
for k, v in d.items():
    out[k] = v
    if k == 'description':
        out['x-opensip-mutation-operation-map'] = law
d = out

# annotate the enum and both generic positions
enum_def = d['$defs']['MutationOperation']
enum_def['description'] = (
    "The closed effect-class vocabulary of a mutating step. Which command mints which member is "
    "published beside this enum at #/x-opensip-mutation-operation-map; three commands do NOT share "
    "their operation's name (baseline-upgrade -> baseline-upgrade-apply, policy-init -> "
    "policy-write, waive -> waiver-change), so name matching is not the derivation. `repair-apply` "
    "is a dedicated operation refused in the generic MutationParams and MutationReplayScopeV1 "
    "positions; `config-write` is currently minted by no command in the inventory."
)
enum_def['x-opensip-vocabulary'] = collections.OrderedDict([
    ("commandAuthority", "workflows/command-inventory.v1.json#/commands[].name"),
    ("map", "workflows/schemas/repair.schema.json#/x-opensip-mutation-operation-map/byCommand"),
    ("admittedBy", "check_workflows.v1.py mutation-operation-map controls"),
])

P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# --- the two generic positions point at the map -------------------------------------------------
P2 = R / 'workflows/schemas/invocation-record.schema.json'
d2 = json.loads(P2.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
ann = collections.OrderedDict([
    ("commandAuthority", "workflows/command-inventory.v1.json#/commands[].name"),
    ("map", "workflows/schemas/repair.schema.json#/x-opensip-mutation-operation-map/byCommand"),
    ("scope", "GENERIC mutation steps only. The map's genericMutationClasses list is exactly the "
              "set admissible here; repair-apply is excluded by the `not` beside the $ref, and the "
              "import and native-preparation operations are minted by their own step kinds and "
              "never appear in this position."),
])
mp = d2['$defs']['MutationParams']['properties']['mutationClass']
assert 'x-opensip-vocabulary' not in mp
mp['x-opensip-vocabulary'] = ann
mrs = d2['$defs']['MutationReplayScopeV1']['properties']['operation']
assert 'x-opensip-vocabulary' not in mrs
mrs['x-opensip-vocabulary'] = ann
P2.write_text(json.dumps(d2, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
print('ok; generic classes', len(generic), 'mapped', len(by_command), 'unmapped ops', sorted(set(ops) - mapped))

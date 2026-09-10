import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work')

# ---------------------------------------------------------------- check_workflows.v1.py controls
P = W / 'docs/coop/design-corrections/workflows/check_workflows.v1.py'
s = P.read_text(encoding='utf-8')
ANCHOR = """check('policy.every-relation-has-a-nonempty-ladder', all(M.RELATION_LADDERS.values()))
"""
CONTROLS = '''check('policy.every-relation-has-a-nonempty-ladder', all(M.RELATION_LADDERS.values()))
# CB6-SHOULD-1. The command name -> MutationOperation map. `mutationClass` is a public envelope
# field and equals MutationReplayScopeV1.operation, which is the whole preimage of the published
# idempotencyKey, yet the Command record carries no such field and three commands do not share
# their operation's name. These controls hold the published map total, closed and honest, and hold
# repair-apply OUT of the two generic positions.
_MAP = SCHEMAS[U + 'repair']['x-opensip-mutation-operation-map']
_BY_COMMAND = _MAP['byCommand']
_OPS = SCHEMAS[U + 'repair']['$defs']['MutationOperation']['enum']
_INV = canonical.parse((HERE / 'command-inventory.v1.json').read_bytes())['commands']
_CMD = {c['name']: c for c in _INV}
_MUTATING_STEPS = {'mutation', 'repair-apply', 'import', 'native-preparation'}
_COMMANDS_WITH_A_MUTATING_STEP = {c['name'] for c in _INV
                                  if _MUTATING_STEPS & set(c['steps'])} - {'analyze'}
check('workflow.mutation-operation-map-covers-every-command-that-mints-one',
      set(_BY_COMMAND) == _COMMANDS_WITH_A_MUTATING_STEP,
      str(sorted(set(_BY_COMMAND) ^ _COMMANDS_WITH_A_MUTATING_STEP)))
check('workflow.mutation-operation-map-names-no-command-outside-the-inventory',
      set(_BY_COMMAND) <= set(_CMD))
check('workflow.mutation-operation-map-values-are-all-registered-operations',
      all(r['operation'] in _OPS for r in _BY_COMMAND.values()))
check('workflow.mutation-operation-map-rows-name-a-real-step-of-that-command',
      all(r['mintedByStepKind'] in _CMD[n]['steps'] and r['requestClass'] == _CMD[n]['requestClass']
          for n, r in _BY_COMMAND.items()))
check('workflow.mutation-operation-map-is-injective',
      len({r['operation'] for r in _BY_COMMAND.values()}) == len(_BY_COMMAND))
# The three rows a name-matching rule would get wrong, named individually.
check('workflow.mutation-operation-renames-are-published',
      _MAP['renamedRows'] == {'baseline-upgrade': 'baseline-upgrade-apply',
                              'policy-init': 'policy-write', 'waive': 'waiver-change'}
      and all(_BY_COMMAND[c]['operation'] == o for c, o in _MAP['renamedRows'].items()))
check('workflow.the-renamed-rows-are-exactly-the-commands-with-no-same-named-operation',
      set(_MAP['renamedRows']) == {n for n in _BY_COMMAND if n not in _OPS})
# Honest disclosure rather than an invented command.
check('workflow.operations-with-no-command-are-exactly-the-disclosed-set',
      _MAP['operationsWithNoCommand']['operations']
      == sorted(set(_OPS) - {r['operation'] for r in _BY_COMMAND.values()})
      and _MAP['operationsWithNoCommand']['operations'] == ['config-write'])
# The generic set and the dedicated exclusion, held apart at the schema, not only in prose.
check('workflow.generic-mutation-classes-are-exactly-the-mutation-step-rows',
      _MAP['genericMutationClasses']
      == sorted(n for n, r in _BY_COMMAND.items() if r['mintedByStepKind'] == 'mutation'))
check('workflow.repair-apply-is-mapped-but-not-a-generic-mutation-class',
      _BY_COMMAND['repair-apply']['operation'] == 'repair-apply'
      and 'repair-apply' not in _MAP['genericMutationClasses']
      and _MAP['excludedFromGenericMutation']['operations'] == ['repair-apply'])
_SCOPE = {'schemaVersion': 1, 'requestId': C['REQ'], 'stepId': 2, 'projectId': C['PRJ']}
for _n in _MAP['genericMutationClasses']:
    _op = _BY_COMMAND[_n]['operation']
    must_valid('workflow.generic-mutation-scope-admits.' + _op,
               U + 'invocation-record#/$defs/MutationReplayScopeV1', dict(_SCOPE, operation=_op))
for _op in ('repair-apply',):
    must_invalid('workflow.generic-mutation-scope-refuses.' + _op,
                 U + 'invocation-record#/$defs/MutationReplayScopeV1', dict(_SCOPE, operation=_op))
    must_invalid('workflow.generic-mutation-params-refuses.' + _op,
                 U + 'invocation-record#/$defs/MutationParams',
                 {'kind': 'mutation', 'mutationClass': _op, 'idempotencyKey': 'a' * 64})
# Publishing the map did not widen what a generic mutation may claim.
check('workflow.publishing-the-map-added-no-operation-and-no-command',
      len(_OPS) == 24 and len(_INV) == 45)
'''
assert s.count(ANCHOR) == 1
P.write_text(s.replace(ANCHOR, CONTROLS), encoding='utf-8')

# ---------------------------------------------------- workflows-and-surfaces.md section 1 prose
P2 = W / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
s2 = P2.read_text(encoding='utf-8')
ANCHOR2 = """Repair apply is the explicit content-derived exception: it is a dedicated
`repair-apply` step, excluded from generic MutationParams."""
NEW2 = """**Which operation a command mints is published, not inferred.** The map from the
closed command-name vocabulary to `MutationOperation` is
`repair.schema.json#/x-opensip-mutation-operation-map`, beside the enum. A command
mints an operation only through a **mutating step**, and the step kind decides the
surface: a generic `mutation` step carries it as `MutationParams.mutationClass`
and as `MutationReplayScopeV1.operation`; the `repair-apply`, `import` and
`native-preparation` steps are their own kinds and carry their operation on the
receipt only. A command with no mutating step mints none and has no row.

Three commands do **not** share their operation's name, so name matching is not
the derivation and an implementer had to guess: `baseline-upgrade` →
`baseline-upgrade-apply` (the operation names the apply half; the analysis half
mints a Run, not a mutation), `policy-init` → `policy-write` and `waive` →
`waiver-change` (both are effect classes covering more than the one command
spelling). Two further facts are disclosed rather than tidied away:
`repair-apply` is in the map because it is a real command/operation pair, and
being in the map does **not** make it admissible in either generic position —
both still refuse it by schema; and `config-write` is a `MutationOperation`
member that **no command in this inventory mints**, which is stated rather than
removed or given an invented command. Publishing the map adds no command, no
operation and no accepted request.

Repair apply is the explicit content-derived exception: it is a dedicated
`repair-apply` step, excluded from generic MutationParams."""
assert s2.count(ANCHOR2) == 1
P2.write_text(s2.replace(ANCHOR2, NEW2), encoding='utf-8')
print('ok')

import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work')
P = W / 'docs/coop/design-corrections/workflows/schemas/repair.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
law = d['x-opensip-mutation-operation-map']

law['renamedRows'] = collections.OrderedDict([
    ('baseline-upgrade', 'baseline-upgrade-apply'),
    ('native-prepare', 'native-preparation'),
    ('policy-init', 'policy-write'),
    ('waive', 'waiver-change'),
])
law['renamedRowsNote'] = (
    "FOUR commands, not three. The three mutation-CLASS renames are baseline-upgrade, policy-init "
    "and waive; `native-prepare` is a fourth, in request class `execution`, whose "
    "`native-preparation` step carries the operation of the same name. Counting only the "
    "mutation-class commands would leave one command's operation still underivable, which is the "
    "defect this map exists to close, so the row is published with the other three. This set is "
    "held EQUAL to the commands whose name is not itself a MutationOperation member, so a future "
    "rename cannot be added to the vocabulary without appearing here."
)
d['$defs']['MutationOperation']['description'] = (
    "The closed effect-class vocabulary of a mutating step. Which command mints which member is "
    "published beside this enum at #/x-opensip-mutation-operation-map; four commands do NOT share "
    "their operation's name (baseline-upgrade -> baseline-upgrade-apply, policy-init -> "
    "policy-write, waive -> waiver-change, and the execution-class native-prepare -> "
    "native-preparation), so name matching is not the derivation. `repair-apply` is a dedicated "
    "operation refused in the generic MutationParams and MutationReplayScopeV1 positions; "
    "`config-write` is currently minted by no command in the inventory."
)
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# checker: assert the published set equals the derived set AND name the mutation-class three
P2 = W / 'docs/coop/design-corrections/workflows/check_workflows.v1.py'
s = P2.read_text(encoding='utf-8')
OLD = """check('workflow.mutation-operation-renames-are-published',
      _MAP['renamedRows'] == {'baseline-upgrade': 'baseline-upgrade-apply',
                              'policy-init': 'policy-write', 'waive': 'waiver-change'}
      and all(_BY_COMMAND[c]['operation'] == o for c, o in _MAP['renamedRows'].items()))
"""
NEW = """check('workflow.mutation-operation-renames-are-published',
      _MAP['renamedRows'] == {'baseline-upgrade': 'baseline-upgrade-apply',
                              'native-prepare': 'native-preparation',
                              'policy-init': 'policy-write', 'waive': 'waiver-change'}
      and all(_BY_COMMAND[c]['operation'] == o for c, o in _MAP['renamedRows'].items()))
check('workflow.the-three-mutation-class-renames-are-the-mutation-class-subset',
      {c for c in _MAP['renamedRows'] if _CMD[c]['requestClass'] == 'mutation'}
      == {'baseline-upgrade', 'policy-init', 'waive'}
      and _CMD['native-prepare']['requestClass'] == 'execution')
"""
assert s.count(OLD) == 1
P2.write_text(s.replace(OLD, NEW), encoding='utf-8')

# prose: four, with the mutation-class three named
P3 = W / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
s3 = P3.read_text(encoding='utf-8')
OLD3 = """Three commands do **not** share their operation's name, so name matching is not
the derivation and an implementer had to guess: `baseline-upgrade` →
`baseline-upgrade-apply` (the operation names the apply half; the analysis half
mints a Run, not a mutation), `policy-init` → `policy-write` and `waive` →
`waiver-change` (both are effect classes covering more than the one command
spelling). Two further facts are disclosed"""
NEW3 = """**Four** commands do not share their operation's name, so name matching is not
the derivation and an implementer had to guess. Three are mutation-class:
`baseline-upgrade` → `baseline-upgrade-apply` (the operation names the apply
half; the analysis half mints a Run, not a mutation), `policy-init` →
`policy-write` and `waive` → `waiver-change` (both are effect classes covering
more than the one command spelling). The fourth is the execution-class
`native-prepare` → `native-preparation`, whose operation is carried by its own
step kind; it is published with the other three because counting only the
mutation-class commands would leave one command's operation still underivable.
The published set is held **equal** to the commands whose name is not itself a
`MutationOperation` member, so a later rename cannot be added to the vocabulary
without appearing here. Two further facts are disclosed"""
assert s3.count(OLD3) == 1
P3.write_text(s3.replace(OLD3, NEW3), encoding='utf-8')
print('ok')

"""CX-BV6-04. Root's probe-bv6-mutation-map-draft-v2.py reads m['genericMutationClasses'], which
this correction REMOVED because that key was the conflation itself (it held command names while the
annotations called it the operation domain). Its unmodified failure is retained in
evidence/root-probe-mutation-map-unmodified-fails-on-removed-key.txt.

This probe asks root's question against the corrected structure: which operations does the ACTUAL
field schema admit, and does each published list say what it is named for."""
import importlib.util, json, hashlib, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve(); dc = root / 'docs/coop/design-corrections'
p = dc / 'workflows/workflows_model.v1.py'
sp = importlib.util.spec_from_file_location('m', p); W = importlib.util.module_from_spec(sp); sp.loader.exec_module(W)
schema = json.loads((dc / 'workflows/schemas/repair.schema.json').read_text())
m = schema['x-opensip-mutation-operation-map']; ops = schema['$defs']['MutationOperation']['enum']
emitted = {r['operation'] for r in m['byCommandGenericMutationStep'].values()}
domain = m['admissibleGenericFieldDomain']['operations']
rows = []
for operation in sorted(set(ops) | set(domain) | emitted):
    try:
        W.validate_import_record('workflows/schemas/invocation-record.schema.json',
                                 '#/$defs/MutationParams/properties/mutationClass', operation)
        actual = 'ADMIT'
    except Exception as e:
        actual = 'REFUSE:' + str(e)
    rows.append({'operation': operation, 'inPublishedFieldDomain': operation in domain,
                 'emittedByACurrentCommand': operation in emitted, 'actualSchema': actual,
                 'agrees': (operation in domain) == (actual == 'ADMIT')})
inv = json.loads((dc / 'workflows/command-inventory.v1.json').read_text())['commands']
mutating = {'mutation', 'repair-apply', 'import', 'native-preparation'}
print(json.dumps({
 'standing': 'Coauthor probe against corrected bytes; property-schema admission only, no replay '
             'authority and no host effect. Complete MutationParams additionally require '
             'per-operation fields, which this property check does not exercise.',
 'sourceRoot': str(root),
 'schemaSha256': hashlib.sha256((dc / 'workflows/schemas/repair.schema.json').read_bytes()).hexdigest(),
 'publishedFieldDomainSize': len(domain),
 'publishedEmittedSize': len(emitted),
 'orphans': m['operationsWithNoPublishedEmitter']['operations'],
 'fieldDomainMatchesSchemaExactly': all(r['agrees'] for r in rows),
 'commandsWithAMutatingStepNotInTheGenericMap':
   [{'name': c['name'], 'steps': c['steps'], 'requestClass': c['requestClass']}
    for c in inv if set(c['steps']) & mutating and c['name'] not in m['byCommandGenericMutationStep']],
 'checks': rows}, indent=1))

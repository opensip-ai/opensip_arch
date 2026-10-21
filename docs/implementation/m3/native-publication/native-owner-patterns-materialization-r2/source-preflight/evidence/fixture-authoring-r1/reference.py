"""Isolated current-shape synthetic replay graph authoring; never edits historical input."""
from pathlib import Path
import json, hashlib, ast, copy
P = Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover')
W = Path(__file__).resolve().parent / 'replay-candidate'
A = P.parent / 'opensip_arch'
B = Path(__file__).resolve().parent
OLD = '81d57d6d68bd1c310d632148fe3c4c3b9b23e224603465e1a9f43062cc8f0712'
current = (P / 'schemas/sources/native-v2.schema.json').read_bytes()
NEW = hashlib.sha256(current).hexdigest()
assert NEW == '7179d52e3b7ce7400a3ab24badcae5b4242acab7c1cb4523032adf4c706d3132'
source = A / 'docs/coop/design-corrections/foundation/identity-model.v3.py'
tree = ast.parse(source.read_text())
PREFIX = next((ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any((isinstance(t, ast.Name) and t.id == 'PREFIX' for t in n.targets))))

def can(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def hid(domain, v):
    raw = can(v)
    h = hashlib.sha256(b'opensip.product.v1\x00' + domain.encode() + b'\x00' + len(raw).to_bytes(8, 'big') + raw).hexdigest()
    return PREFIX[domain] + ':' + h

def order_identity(v, path=()):
    if isinstance(v, dict):
        return {k: order_identity(x, path + (k,)) for k, x in v.items()}
    if not isinstance(v, list):
        return v
    out = [order_identity(x, path + (str(i),)) for i, x in enumerate(v)]
    name = path[-1] if path else ''
    if name == 'allowedScopes':
        return out
    if name in ('sourceInventory', 'tree', 'blobs'):
        key = lambda x: x['path'].encode()
    elif name == 'requires':
        key = lambda x: x
    elif name == 'owner-source-set':
        key = lambda x: x['ownerKey'].encode()
    elif name == 'stages':
        key = lambda x: x['ordinal']
    elif name == 'predicateProofs':
        key = lambda x: (x['ruleId'], x['subjectId'], x['predicateId'])
    elif name == 'ruleResults':
        key = lambda x: x['ruleId'].encode()
    else:
        key = can
    return sorted(out, key=key)
SET_FIELDS = {'findingIds', 'waivedFindingIds', 'evidenceRefs', 'inputRefs', 'evaluationInputRefs', 'scopeIds', 'coverageIds', 'matchingFactIds', 'uncertainFactIds', 'matchingImportRows', 'uncertainImportRows', 'deficiencies', 'selectedRefs'}
EXECUTION_SCHEMA = json.loads((P / 'schemas/sources/execution-inputs-v1.schema.json').read_bytes())

def order_selected_execution(v, node):
    while '$ref' in node:
        reference = node['$ref']
        assert reference.startswith('#/'), reference
        node = EXECUTION_SCHEMA
        for part in reference[2:].split('/'):
            node = node[part.replace('~1', '/').replace('~0', '~')]
    if isinstance(v, dict):
        return {k: order_selected_execution(x, node['properties'][k]) if k in node.get('properties', {}) else x for k, x in v.items()}
    if isinstance(v, list):
        out = [order_selected_execution(x, node['items']) if isinstance(node.get('items'), dict) else x for x in v]
        return sorted(out, key=can) if node.get('x-opensip-order') == 'canonical-set' else out
    return v

def order_blob(v):
    if isinstance(v, dict):
        out = {k: order_blob(x) for k, x in v.items()}
        for k, x in out.items():
            if isinstance(x, list) and k in SET_FIELDS:
                out[k] = sorted(x, key=can)
            elif isinstance(x, list) and k == 'predicateProofs':
                out[k] = sorted(x, key=lambda y: (y['ruleId'], y['subjectId'], y['predicateId']))
        if set(EXECUTION_SCHEMA['required']).issubset(out):
            out = order_selected_execution(out, EXECUTION_SCHEMA)
        return out
    if isinstance(v, list):
        return [order_blob(x) for x in v]
    return v

def sub(v):
    if isinstance(v, str):
        return mapping.get(v, v)
    if isinstance(v, list):
        return [sub(x) for x in v]
    if isinstance(v, dict):
        return {mapping.get(k, k): sub(x) for k, x in v.items()}
    return v

def rebuild_blob(row):
    raw = bytes.fromhex(row['hex'])
    if row['digest'] == OLD:
        return current
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeError):
        return raw
    if can(value) != raw:
        return raw
    return can(order_blob(sub(value)))

INITIAL_MAPPING={OLD:NEW,'53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a':'3add72f2cecd755be5e21795cfee545cdc68ff80ed8c43fedd417093917ade62'}
replacement_blobs={OLD:current,'53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a':(P/'schemas/sources/relation-payload-v2.schema.json').read_bytes()}
assert all(hashlib.sha256(raw).hexdigest()==INITIAL_MAPPING[old] for old,raw in replacement_blobs.items())
original_rebuild_blob=rebuild_blob
def rebuild_blob(row):
 return replacement_blobs.get(row['digest']) if row['digest'] in replacement_blobs else original_rebuild_blob(row)

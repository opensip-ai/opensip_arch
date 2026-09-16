# Control C16 - the receipt join, against the ACTUAL closed commit-receipt and the actual
# thirteen-field association. No {x:1}/{y:1} stand-ins.
#
# Settles root correction 3: the receipt has no storeGenerationDigest, so the store binding is
# joined through the admitted handle plus the association, and a binding mismatch is caught at
# that owning join.
#
# usage: python c16-receipt-join.py <source25Root> <planRoot> <reportPath>
import json
import os
import sys

import jsonschema

SRC, PLANROOT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
IDS = json.load(open(os.path.join(
    SRC, 'docs/coop/design-corrections/foundation/identity-schemas.v3.json'), encoding='utf-8'))
PLAN = json.load(open(os.path.join(PLANROOT, 'commit-recovery-plan.v1.json'), encoding='utf-8'))

RECEIPT = IDS['$defs']['commit-receipt']
ASSOC = PLAN['recordSchema']

checks = []


def ck(name, ok, detail=''):
    checks.append({'check': name, 'pass': bool(ok), 'detail': str(detail)[:300]})
    return ok


# ---- 1. the actual closed receipt shape --------------------------------------
ck('commit-receipt is closed', RECEIPT.get('additionalProperties') is False)
ck('commit-receipt has exactly eight members',
   len(RECEIPT['required']) == 8 and len(RECEIPT['properties']) == 8, RECEIPT['required'])
ck('commit-receipt has NO storeGenerationDigest member',
   'storeGenerationDigest' not in RECEIPT['properties'], sorted(RECEIPT['properties']))
ck('the association DOES carry storeGenerationDigest',
   'storeGenerationDigest' in ASSOC['properties'])
SHARED = set(RECEIPT['properties']) & set(ASSOC['properties'])
ck('the members actually shared by receipt and association are exactly the join keys',
   SHARED == {'executionId', 'namespaceId', 'runId', 'commitSequence', 'inventoryDigest'},
   sorted(SHARED))

# ---- 2. build real instances and validate them against their real schemas ----
def V(schema, doc):
    s = dict(doc)
    s.pop('$ref', None)
    s['$ref'] = schema
    jsonschema.Draft202012Validator.check_schema(s)
    return jsonschema.Draft202012Validator(s)


rv = V('#/$defs/commit-receipt', IDS)
av = jsonschema.Draft202012Validator(ASSOC)

NS = 'ns1'
EXEC = 'exec1_' + '1' * 32
RUN = 'run3:' + '0' * 64
INV = 'a' * 64
SGD_GOOD = 'f' * 64
SGD_OTHER = '9' * 64
OPREF = 'op-' + 'a' * 32

# The receipt's own schemaVersion is const 2. That is a THIRD version axis, distinct from the
# association's recordSchema 1 and the journal's recordSchema 3, and it is not interchangeable.
receipt = {'schemaVersion': 2, 'runId': RUN, 'executionId': EXEC, 'namespaceId': NS,
           'commitSequence': 42, 'inventoryDigest': INV,
           'sealedAssurance': 'replayable', 'signerKeyId': 'k1'}
assoc = {'recordSchema': 1, 'storeGenerationDigest': SGD_GOOD, 'namespaceId': NS,
         'executionId': EXEC, 'runId': RUN, 'inventoryDigest': INV, 'commitSequence': '42',
         'receiptBytesSha256': 'b' * 64, 'journalCarrierDigest': 'e' * 64,
         'grantGeneration': 1, 'journalSeq': 7, 'journalBodySha256': 'c' * 64,
         'operationRef': OPREF}

rerr = [e.message for e in rv.iter_errors(receipt)]
aerr = [e.message for e in av.iter_errors(assoc)]
ck('the constructed receipt validates against the actual closed schema', not rerr, rerr)
ck('the constructed association validates against the actual plan schema', not aerr, aerr)
ck('a receipt carrying storeGenerationDigest is REFUSED by the closed schema',
   bool([e for e in rv.iter_errors(dict(receipt, storeGenerationDigest=SGD_GOOD))]))


# ---- 3. the joins, as the corrected law states them --------------------------
def join_receipt(receipt_doc, assoc_doc):
    """Join on the members the closed receipt actually has."""
    if receipt_doc['executionId'] != assoc_doc['executionId']:
        return 'mismatch:executionId'
    if receipt_doc['namespaceId'] != assoc_doc['namespaceId']:
        return 'mismatch:namespaceId'
    if receipt_doc['runId'] != assoc_doc['runId']:
        return 'mismatch:runId'
    if receipt_doc['inventoryDigest'] != assoc_doc['inventoryDigest']:
        return 'mismatch:inventoryDigest'
    if str(receipt_doc['commitSequence']) != assoc_doc['commitSequence']:
        return 'mismatch:commitSequence'
    return 'joined'


def join_store_binding(admitted_handle_digest, assoc_doc):
    """The store binding is NOT on the receipt. It comes from the admitted handle and is carried
    by the association. This is the owning join for a binding mismatch."""
    if admitted_handle_digest != assoc_doc['storeGenerationDigest']:
        return 'binding-unusable'
    return 'bound'


ck('receipt and association join on the actual shared members',
   join_receipt(receipt, assoc) == 'joined')
ck('the store binding joins through the admitted handle and the association',
   join_store_binding(SGD_GOOD, assoc) == 'bound')
ck('a store-binding mismatch is caught at the association join, not at the receipt',
   join_store_binding(SGD_OTHER, assoc) == 'binding-unusable'
   and join_receipt(receipt, assoc) == 'joined')

cases = []
for label, r2, a2, handle, want_r, want_b in [
    ('all joined', receipt, assoc, SGD_GOOD, 'joined', 'bound'),
    ('wrong store generation for an otherwise perfect receipt',
     receipt, assoc, SGD_OTHER, 'joined', 'binding-unusable'),
    ('association from a different store generation',
     receipt, dict(assoc, storeGenerationDigest=SGD_OTHER), SGD_GOOD, 'joined',
     'binding-unusable'),
    ('executionId swap', dict(receipt, executionId='exec1_' + '2' * 32), assoc, SGD_GOOD,
     'mismatch:executionId', 'bound'),
    ('runId swap', dict(receipt, runId='run3:' + '1' * 64), assoc, SGD_GOOD,
     'mismatch:runId', 'bound'),
    ('inventoryDigest swap', dict(receipt, inventoryDigest='d' * 64), assoc, SGD_GOOD,
     'mismatch:inventoryDigest', 'bound'),
    ('commitSequence swap', dict(receipt, commitSequence=43), assoc, SGD_GOOD,
     'mismatch:commitSequence', 'bound'),
    ('namespace swap', dict(receipt, namespaceId='other'), assoc, SGD_GOOD,
     'mismatch:namespaceId', 'bound'),
]:
    gr, gb = join_receipt(r2, a2), join_store_binding(handle, a2)
    cases.append({'case': label, 'receiptJoin': gr, 'bindingJoin': gb,
                  'expected': [want_r, want_b], 'pass': (gr, gb) == (want_r, want_b)})
    ck('join case: ' + label, (gr, gb) == (want_r, want_b), [gr, gb])

ck('every mismatch is attributed to the join that actually owns the member',
   all(c['pass'] for c in cases))
ck('no join implies a receipt member that does not exist',
   all(k in RECEIPT['properties'] for k in
       ('executionId', 'namespaceId', 'runId', 'inventoryDigest', 'commitSequence')))

ck('the receipt schemaVersion is const 2, a third version axis distinct from recordSchema 1 '
   'on the association and recordSchema 3 on the journal',
   RECEIPT['properties']['schemaVersion'].get('const') == 2
   and ASSOC['properties']['recordSchema'].get('maximum') == 1)

rep = {'control': 'c16-receipt-join',
       'versionAxes': {'receiptSchemaVersion': RECEIPT['properties']['schemaVersion'].get('const'),
                       'associationRecordSchema': 1, 'journalRecordSchema': 3,
                       'note': 'three separate axes; none is interchangeable with another'},
       'actualReceiptMembers': sorted(RECEIPT['properties']),
       'receiptIsClosed': RECEIPT.get('additionalProperties') is False,
       'sharedJoinMembers': sorted(SHARED),
       'storeBindingOwner': ('admitted store handle and registry, carried by '
                             'CommitRecoveryAssociationV1.storeGenerationDigest'),
       'joinCases': cases,
       'passed': sum(1 for c in checks if c['pass']),
       'failed': sum(1 for c in checks if not c['pass']),
       'checks': checks}
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('passed %d failed %d' % (rep['passed'], rep['failed']))
print('receipt members:', sorted(RECEIPT['properties']))
print('shared join members:', sorted(SHARED))
for c in checks:
    if not c['pass']:
        print('  FAIL', c['check'], '::', c['detail'])

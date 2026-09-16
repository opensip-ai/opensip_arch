# Control C15 - replay root's own ddl-atomicity helper shape against the CORRECTED act_B.
#
# Root's ddl-atomicity.py AST-extracted the v5 act_B unchanged, injected one SQL error before the
# first trigger, and recorded tablesSurvivingFailure ["carrier_format"] with the transaction
# closed. That proved the v5 helper never ran one transaction. This control does the same thing to
# the v6 act_B, so the correction is demonstrated by root's own method rather than by my assertion.
#
# Root's original file and its recorded failure are NOT modified. In-memory transaction evidence
# only: nothing here establishes OS durability, fsync behaviour or real crash behaviour.
#
# usage: python c15-root-atomicity-replay.py <v6ControlsDir> <v3sqlPath> <rootResultJson> <out>
import ast
import json
import sqlite3
import sys

CTRL, V3SQL, ROOTJSON, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

src = open(CTRL + '/c13-migration-prefixes.py', encoding='utf-8').read()
tree = ast.parse(src)
wanted = {'act_B', 'split_sql'}
fns = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name in wanted]
assert {f.name for f in fns} == wanted, sorted(f.name for f in fns)

ddl = open(V3SQL, encoding='utf-8').read()
assert 'CREATE TRIGGER' in ddl
faulted = ddl.replace('CREATE TRIGGER', 'SELECT root_injected_failure();\nCREATE TRIGGER', 1)

ns = {'DDL3': faulted, 're': __import__('re')}
exec(compile(ast.Module(body=fns, type_ignores=[]), '<actual-c13-act-B-v6>', 'exec'), ns)

c = sqlite3.connect(':memory:')
try:
    ns['act_B'](c)
    error = None
except sqlite3.Error as e:
    error = str(e)
tables = [x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
triggers = [x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='trigger'")]
open_txn = c.in_transaction
c.close()

# the success path through the same extracted function, unfaulted
ns2 = {'DDL3': ddl, 're': __import__('re')}
exec(compile(ast.Module(body=fns, type_ignores=[]), '<actual-c13-act-B-v6>', 'exec'), ns2)
c2 = sqlite3.connect(':memory:')
ns2['act_B'](c2)
created = sorted(x[0] for x in c2.execute('SELECT name FROM sqlite_master'))
open_txn2 = c2.in_transaction
c2.close()

root_prior = json.load(open(ROOTJSON, encoding='utf-8'))

rep = {
    'control': 'c15-root-atomicity-replay',
    'method': ("root's own AST extraction and single injected SQL failure, applied unchanged to "
               'the v6 act_B; split_sql is extracted with it because act_B now calls it'),
    'standing': ('In-memory transaction evidence only. Not OS durability, not fsync, not a real '
                 'crash, and not a qualification of the migration.'),
    'rootPriorFinding': {
        'source': ROOTJSON,
        'tablesSurvivingFailure': root_prior.get('tablesSurvivingFailure'),
        'atomicActBEstablishedByThisHelper': root_prior.get('atomicActBEstablishedByThisHelper'),
        'preserved': True,
        'note': ('Root observed carrier_format surviving because executescript issues an '
                 'implicit COMMIT and then runs statements one at a time. The finding stands '
                 'against the v5 helper and is not overwritten.'),
    },
    'v6FaultedRun': {'error': error, 'tablesSurvivingFailure': tables,
                     'triggersSurvivingFailure': triggers, 'transactionStillOpen': open_txn},
    'v6SuccessRun': {'objectsCreated': created, 'transactionStillOpen': open_txn2},
}
checks = [
    ('the injected failure still raises', error is not None),
    ('no table survives the injected failure', tables == []),
    ('no trigger survives the injected failure', triggers == []),
    ('no transaction is left open after the rollback', open_txn is False),
    # 9 on a bare connection: the 7 carrierFormat 3 objects plus the two inherited side tables,
    # which the script creates with IF NOT EXISTS and which are absent here because this
    # connection was not seeded with the inherited DDL first.
    ('the same extracted function succeeds unfaulted and creates every object',
     len(created) == 9),
    ('no transaction is left open after success', open_txn2 is False),
    ("root's prior finding is carried forward unchanged",
     root_prior.get('tablesSurvivingFailure') == ['carrier_format']),
]
rep['checks'] = [{'check': n, 'pass': bool(v)} for n, v in checks]
rep['passed'] = sum(1 for _, v in checks if v)
rep['failed'] = sum(1 for _, v in checks if not v)
with open(OUT, 'w', encoding='utf-8') as fh:
    fh.write(json.dumps(rep, indent=1) + '\n')
print('WROTE', OUT)
print('passed %d failed %d' % (rep['passed'], rep['failed']))
print('v5 (root):', root_prior.get('tablesSurvivingFailure'), '-> v6:', tables)
for ch in rep['checks']:
    if not ch['pass']:
        print('  FAIL', ch['check'])

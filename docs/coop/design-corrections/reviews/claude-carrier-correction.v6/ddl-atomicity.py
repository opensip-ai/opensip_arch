import ast,json,sqlite3
from pathlib import Path
r=Path('/tmp/opensip-design-corrections/claude-carrier-correction.v5/scratch')
s=(r/'controls/c13-migration-prefixes.py').read_text();tree=ast.parse(s);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='act_B')
ddl=(r/'proposal/docs/coop/design-corrections/security/grant-journal.carrier.v3.sql').read_text()
assert 'CREATE TRIGGER' in ddl
faulted=ddl.replace('CREATE TRIGGER','SELECT root_injected_failure();\nCREATE TRIGGER',1)
ns={'DDL3':faulted};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<actual-c13-act-B>','exec'),ns)
c=sqlite3.connect(':memory:')
try:ns['act_B'](c);error=None
except sqlite3.Error as e:error=str(e)
tables=[x[0] for x in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print(json.dumps({'standing':'Root executes unchanged actual C13 act_B with one injected SQL failure before first trigger. In-memory transaction control only, not OS durability.','error':error,'transactionStillOpen':c.in_transaction,'tablesSurvivingFailure':tables,'atomicActBEstablishedByThisHelper':not tables},indent=2))
assert error and tables and not c.in_transaction

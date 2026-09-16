from pathlib import Path
import json,runpy,sys,sqlite3,re,hashlib
T=Path('/tmp/opensip-design-corrections/claude-return-successor.v1')
O=Path(__file__).parent
P=Path('/tmp/opensip-design-corrections/claude-carrier-correction.v7/scratch/controls/c18-selected-dispatch.py')
S=T/'docs/coop/design-corrections/security'
sys.argv=[str(P),str(T),str(S/'grant-journal.carrier.v3.sql'),str(S/'carrier-dispatch.v3.json'),str(O/'base-c18.json')]
v=runpy.run_path(str(P));c=sqlite3.connect(':memory:');trace=[];c.set_trace_callback(trace.append)
v['act_B'](c)
before=v['dispatch'](c);assert before==('incomplete-footprint-resume-at-C',1)
assert 'grant_journal' not in {r[0] for r in c.execute('SELECT name FROM sqlite_master')}
c.execute('INSERT INTO carrier_format VALUES (1,3,?,1,1,NULL,NULL)',('e'*64,));c.commit()
after=v['dispatch'](c);assert after==(3,1)
assert not any(re.search(r'(?i)from\s+grant_journal(?:\s|$)',q) for q in trace)
d=json.loads((S/'carrier-dispatch.v3.json').read_bytes());assert 'interruptedAfterB' in d['openDispatch']['freshInstallPath']
(O/'probe.json').write_text(json.dumps({'standing':'Root in-memory interrupted-fresh-install reference control, not OS/crash qualification','beforePublication':before,'afterFreshPublication':after,'absentInheritedTableRead':False,'passed':True,'controlSha256':hashlib.sha256(P.read_bytes()).hexdigest()},indent=2)+'\n')
print('PASS interrupted fresh install B->C without reading inherited table')

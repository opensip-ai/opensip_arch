#!/usr/bin/env python3
"""Execute lifecycle design DDL against SQLite and injected local process death.

Uses real SQLite constraints/transactions and local fsync/rename operations on
synthetic fixture bytes. Verification/lease/GC callbacks model observations from
host security/OS services; no signatures or four-platform qualification claimed.
"""
import argparse
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

B = Path(__file__).resolve().parent
ROOT = B.parents[2]
G1='11111111-1111-4111-8111-111111111111'
G2='22222222-2222-4222-8222-222222222222'
G3='33333333-3333-4333-8333-333333333333'
P1='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'
P2='bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb'
T1='44444444-4444-4444-8444-444444444444'
T2='55555555-5555-4555-8555-555555555555'
T3='66666666-6666-4666-8666-666666666666'
L1='77777777-7777-4777-8777-777777777777'
BOOT='88888888-8888-4888-8888-888888888888'
N1='99999999-9999-4999-8999-999999999999'
N2='cccccccc-cccc-4ccc-8ccc-cccccccccccc'
SHA=lambda b:hashlib.sha256(b).hexdigest()


class Store:
    def __init__(self, directory, initialize=True):
        self.root=Path(directory)
        self.root.mkdir(exist_ok=True)
        self.db=self.root/'lifecycle.sqlite'
        self.lockfile=(self.root/'lifecycle.lock').open('a+b')
        self.held=False
        self.epoch=[1,2,3,'a'*64]
        self.tickets={}
        self.root_tickets={}
        self.fixture_locks={}
        self.bound_projects={P1}
        self.durable=set()
        self.gc=set()
        self.prunable=set()
        self.lease_acquired=set()
        self.lease_released=set()
        self.connection=sqlite3.connect(self.db,isolation_level=None)
        self.connection.execute('PRAGMA foreign_keys=ON')
        self.connection.execute('PRAGMA synchronous=FULL')
        self.register()
        if initialize:
            self.connection.executescript((B/'lifecycle-carrier.schema.v1.sql').read_text())
            with self.writer():
                self.register_project()
                self.register_project(P2,N2,'/fixtures/root2','102')
        assert self.connection.execute('PRAGMA encoding').fetchone()[0]=='UTF-8'
        assert self.connection.execute('PRAGMA foreign_keys').fetchone()[0]==1
        assert self.connection.execute('PRAGMA synchronous').fetchone()[0]==2
        assert self.connection.execute('PRAGMA journal_mode').fetchone()[0]=='wal'

    def register(self):
        def verified(*args):
            return int(self.held and list(args[4:])==self.epoch and self.tickets.get(args[0])==list(args))
        def scope_match(key,gid,digest):
            raw=self.fixture_locks.get(gid)
            if not self.held or raw is None or SHA(raw)!=digest:return 0
            context=json.loads(raw)['scopeContext']
            return int((context['projectKey'] is None and context['allowedScopes']==['global']) or (context['projectKey']==key and context['allowedScopes']==['project','global']))
        funcs=[('lifecycle_generation_project_scope',3,scope_match),
               ('lifecycle_project_root_verified',8,lambda *args:int(self.held and self.root_tickets.get(args[0])==list(args))),
               ('lifecycle_project_binding',1,lambda key:int(self.held and key in self.bound_projects)),
               ('lifecycle_writer_authorized',0,lambda:int(self.held)),
               ('lifecycle_verified_generation',8,verified),
               ('lifecycle_durable_ready',2,lambda gid,path:int(self.held and gid in self.durable and path=='generations/'+gid)),
               ('lifecycle_gc_authorized',1,lambda gid:int(self.held and gid in self.gc)),
               ('lifecycle_transition_prune_authorized',1,lambda tid:int(self.held and tid in self.prunable)),
               ('lifecycle_lease_acquired',3,lambda lid,boot,token:int(self.held and (lid,boot,token) in self.lease_acquired)),
               ('lifecycle_lease_release_authorized',1,lambda lid:int(self.held and lid in self.lease_released))]
        for name,arity,fn in funcs:self.connection.create_function(name,arity,fn)

    @contextlib.contextmanager
    def writer(self):
        fcntl.flock(self.lockfile,fcntl.LOCK_EX)
        self.held=True
        try:yield
        finally:
            self.held=False
            fcntl.flock(self.lockfile,fcntl.LOCK_UN)

    def execute(self,sql,values=()):
        return self.connection.execute(sql,values)

    def register_project(self,key=P1,namespace=N1,path='/fixtures/root1',inode='101',verified=True,**overrides):
        args=[key,namespace,'macos',path.encode('utf-8').hex(),'1',inode,100,0]
        positions={'key':0,'namespace':1,'platform':2,'pathHex':3,'device':4,'inode':5,'birthSeconds':6,'birthNanoseconds':7}
        for k,v in overrides.items():args[positions[k]]=v
        if verified:self.root_tickets[args[0]]=args[:]
        self.execute('INSERT INTO project_registry VALUES(?,?,?,?,?,?,?,?,?)',args+['ACTIVE'])

    def insert_generation(self,gid=G1,lockProjectKey=None,**overrides):
        context={'projectKey':lockProjectKey,'allowedScopes':['global'] if lockProjectKey is None else ['project','global']}
        self.fixture_locks[gid]=json.dumps({'fixtureGeneration':gid,'scopeContext':context},sort_keys=True,separators=(',',':')).encode()
        values={'id':gid,'manifestDigest':SHA(('fixture manifest '+gid).encode()),'lockDigest':SHA(self.fixture_locks[gid]),
                'platform':'macos-arm64','immutablePath':'generations/'+gid,'state':'PREPARING'}
        values.update(overrides)
        keys=list(values)
        self.execute('INSERT INTO generation ('+','.join(keys)+') VALUES ('+','.join('?' for _ in keys)+')',[values[k] for k in keys])

    def ticket(self,gid):
        row=self.execute('SELECT id,manifestDigest,lockDigest,platform FROM generation WHERE id=?',(gid,)).fetchone()
        # Model verifier checks explicit independent synthetic input bytes. This
        # is not a signature verifier or an admission of a production manifest.
        assert row[1]==SHA(('fixture manifest '+gid).encode())
        assert row[2]==SHA(self.fixture_locks[gid])
        self.tickets[gid]=list(row)+self.epoch[:]

    def verify(self,gid=G1):
        self.ticket(gid)
        self.execute("UPDATE generation SET state='VERIFIED',rootVersion=?,indexSnapshotVersion=?,revocationVersion=?,permissionPolicyDigest=? WHERE id=?",self.epoch+[gid])

    def make_durable(self,gid=G1):
        staging=self.root/'staging'/gid
        staging.mkdir(parents=True)
        for name,body in [('manifest',('fixture manifest '+gid).encode()),('lock',self.fixture_locks[gid])]:
            with (staging/name).open('wb') as f:
                f.write(body);f.flush();os.fsync(f.fileno())
        fd=os.open(staging,os.O_RDONLY);os.fsync(fd);os.close(fd)
        final=self.root/'generations'/gid
        final.parent.mkdir(exist_ok=True)
        os.rename(staging,final)
        fd=os.open(final.parent,os.O_RDONLY);os.fsync(fd);os.close(fd)
        self.durable.add(gid)

    def ready(self,gid=G1):
        self.make_durable(gid)
        self.execute("UPDATE generation SET state='READY' WHERE id=?",(gid,))

    def transition(self,tid=T1,project=P1,old=None,new=G1):
        self.execute('INSERT INTO transition VALUES(?,?,?,?,?)',(tid,project,old,new,'PREPARING'))

    def advance(self,tid=T1):
        self.execute("UPDATE transition SET phase='VERIFIED' WHERE txId=?",(tid,))
        self.execute("UPDATE transition SET phase='READY' WHERE txId=?",(tid,))

    def publish(self,project=P1,gid=G1):
        if self.execute('SELECT 1 FROM project_selection WHERE projectKey=?',(project,)).fetchone():
            self.execute('UPDATE project_selection SET generationId=? WHERE projectKey=?',(gid,project))
        else:self.execute('INSERT INTO project_selection VALUES(?,?)',(project,gid))

    def setup(self,level='preparing'):
        with self.writer():
            self.insert_generation()
            if level=='preparing':return
            self.verify()
            if level=='verified':return
            self.ready()
            if level=='ready':return
            self.transition();self.advance();self.publish()
            if level=='selected':return
            self.insert_generation(G2);self.verify(G2);self.ready(G2)
            self.transition(T2,P1,G1,G2);self.advance(T2)

    def lease(self,lid=L1,project=P1,gid=G1,token='fixture-process-start:1',acquire=True):
        if acquire:self.lease_acquired.add((lid,BOOT,token))
        self.execute('INSERT INTO operation_lease VALUES(?,?,?,?,?)',(lid,project,gid,BOOT,token))

    def close(self):
        self.connection.close();self.lockfile.close()


def act(store,action):
    op=action['op']
    if op=='sql':return store.execute(action['sql'],action.get('params',[])).fetchall()
    if op=='register-project':return store.register_project(**action.get('values',{}))
    if op=='bind-project':
        store.bound_projects.add(action['key']);return
    if op=='unbind-project':
        store.bound_projects.discard(action['key']);return
    if op=='root-ticket':
        row=store.execute('SELECT projectKey,namespaceId,platform,rootPathBytesHex,deviceId,inodeId,birthSeconds,birthNanoseconds FROM project_registry WHERE projectKey=?',(action['key'],)).fetchone()
        values=list(row)
        if 'newPath' in action:values[3]=action['newPath'].encode().hex()
        store.root_tickets[action['key']]=values;return
    if op=='insert':return store.insert_generation(**action.get('values',{}))
    if op=='verify':return store.verify(action.get('generation',G1))
    if op=='ready':return store.ready(action.get('generation',G1))
    if op=='ticket':return store.ticket(action.get('generation',G1))
    if op=='transition':return store.transition(**action.get('values',{}))
    if op=='advance':return store.advance(action.get('transition',T1))
    if op=='publish':return store.publish(action.get('project',P1),action.get('generation',G1))
    if op=='lease':return store.lease(**action.get('values',{}))
    if op=='epoch':
        store.epoch=action['value'];return
    if op=='permit':
        getattr(store,action['set']).add(action['value']);return
    if op=='missing-callback':
        other=sqlite3.connect(store.db)
        try:
            other.execute('PRAGMA foreign_keys=ON')
            other.execute("DELETE FROM generation WHERE id=?",(G1,))
        finally:other.close()
        return
    raise ValueError(op)


def run_case(case):
    with tempfile.TemporaryDirectory(prefix='opensip-lifecycle-carrier-') as td:
        store=Store(td)
        if case['setup']!='empty':store.setup(case['setup'])
        observed='ACCEPT';error=None
        try:
            lock=store.writer() if case.get('writer',True) else contextlib.nullcontext()
            with lock:
                store.execute('BEGIN IMMEDIATE')
                try:
                    for action in case['actions']:act(store,action)
                    store.execute('COMMIT')
                except BaseException:
                    store.execute('ROLLBACK');raise
        except (sqlite3.Error,OverflowError) as e:
            observed='REFUSE';error=str(e)
        assertions=[]
        for assertion in case.get('postconditions',[]):
            actual=[list(row) for row in store.execute(assertion['sql'],assertion.get('params',[])).fetchall()]
            assertions.append({'expected':assertion['expected'],'observed':actual,'passed':actual==assertion['expected']})
        store.close()
        return {'id':case['id'],'expected':case['expected'],'observed':observed,'passed':observed==case['expected'] and all(x['passed'] for x in assertions),'sqliteRefusal':error,'postconditions':assertions}


def crash_worker(directory,phase):
    store=Store(directory,initialize=False)
    config=json.loads((store.root/'worker-observations.json').read_text())
    store.tickets=config['tickets'];store.durable=set(config['durable']);store.epoch=config['epoch'];store.root_tickets=config['rootTickets'];store.fixture_locks={key:bytes.fromhex(value) for key,value in config['fixtureLocks'].items()}
    with store.writer():
        store.execute('BEGIN IMMEDIATE')
        store.publish(P1,G2)
        if phase=='after-commit':store.execute('COMMIT')
        os._exit(71)


def crash_checks():
    results=[]
    for phase,generation,txphase in [('before-commit',G1,'READY'),('after-commit',G2,'COMMITTED')]:
        with tempfile.TemporaryDirectory(prefix='opensip-lifecycle-crash-') as td:
            store=Store(td);store.setup('pending')
            with store.writer():store.lease()
            (store.root/'worker-observations.json').write_text(json.dumps({'tickets':store.tickets,'durable':list(store.durable),'epoch':store.epoch,'rootTickets':store.root_tickets,'fixtureLocks':{key:value.hex() for key,value in store.fixture_locks.items()}}))
            child=subprocess.run([sys.executable,str(Path(__file__)), '--crash-worker',td,'--phase',phase],check=False)
            observed={'exitCode':child.returncode,'selection':store.execute('SELECT generationId FROM project_selection WHERE projectKey=?',(P1,)).fetchone()[0],
                      'transition':store.execute('SELECT phase FROM transition WHERE txId=?',(T2,)).fetchone()[0],
                      'liveOperation':store.execute('SELECT generationId FROM operation_lease WHERE leaseId=?',(L1,)).fetchone()[0],
                      'integrity':store.execute('PRAGMA integrity_check').fetchone()[0],
                      'foreignKeyViolations':store.execute('PRAGMA foreign_key_check').fetchall()}
            expected={'exitCode':71,'selection':generation,'transition':txphase,'liveOperation':G1,'integrity':'ok','foreignKeyViolations':[]}
            results.append({'id':'process-death/'+phase,'observed':observed,'expected':expected,'passed':observed==expected})
            store.close()
    return results


def nonblocking_gc_probe_check():
    """Exercise the actual local flock primitive under the install writer lock."""
    with tempfile.TemporaryDirectory(prefix='opensip-lifecycle-lease-probe-') as td:
        store=Store(td)
        lease_path=store.root/'operation-fixture.lease'
        child_code="import fcntl,sys; f=open(sys.argv[1],'a+b'); fcntl.flock(f,fcntl.LOCK_EX); print('HELD',flush=True); sys.stdin.readline(); fcntl.flock(f,fcntl.LOCK_UN)"
        child=subprocess.Popen([sys.executable,'-c',child_code,str(lease_path)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
        try:
            assert child.stdout.readline().strip()=='HELD'
            with store.writer(),lease_path.open('a+b') as candidate:
                try:
                    fcntl.flock(candidate,fcntl.LOCK_EX|fcntl.LOCK_NB)
                    busy='ACQUIRED'
                except BlockingIOError:
                    busy='BUSY'
            # Release the lifecycle fence before waiting for holder termination.
            child.communicate('release\n',timeout=5)
            with store.writer(),lease_path.open('a+b') as candidate:
                fcntl.flock(candidate,fcntl.LOCK_EX|fcntl.LOCK_NB)
                released='ACQUIRED'
                fcntl.flock(candidate,fcntl.LOCK_UN)
            observed={'busyProbe':busy,'afterRelease':released,'holderExit':child.returncode}
            expected={'busyProbe':'BUSY','afterRelease':'ACQUIRED','holderExit':0}
            return {'id':'nonblocking-gc-lease-census','observed':observed,'expected':expected,'passed':observed==expected}
        finally:
            if child.poll() is None:
                child.kill();child.wait()
            store.close()


def run(args):
    corpus_path=B/'lifecycle-carrier.cases.v1.json';contract_path=B/'lifecycle-carrier.contract.v1.json'
    corpus=json.loads(corpus_path.read_text());contract=json.loads(contract_path.read_text());results=[]
    for pin in contract['sourcePins']:
        observed=SHA((ROOT/pin['path']).read_bytes());results.append({'id':'source/'+pin['path'],'passed':observed==pin['sha256']})
    for case in corpus['cases']:results.append(run_case(case))
    results+=crash_checks()
    results.append(nonblocking_gc_probe_check())
    report={'status':'DESIGN-DDL-RESULT-NOT-PRODUCT-QUALIFICATION','sqliteVersion':sqlite3.sqlite_version,'passed':sum(r['passed'] for r in results),'total':len(results),
            'sourcePins':[{'path':str(p.relative_to(ROOT)),'sha256':SHA(p.read_bytes())} for p in [Path(__file__),corpus_path,contract_path,B/'lifecycle-carrier.schema.v1.sql']],
            'limitations':contract['reviewLimits'],'results':results}
    Path(args.report).write_text(json.dumps(report,indent=2)+'\n')
    print(f"Lifecycle carrier DDL: {report['passed']}/{report['total']} passed (SQLite {sqlite3.sqlite_version})")
    for item in results:
        if not item['passed']:print(json.dumps(item))
    return 0 if report['passed']==report['total'] else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',default=str(B/'lifecycle-carrier.report.v1.json'))
    parser.add_argument('--crash-worker')
    parser.add_argument('--phase',choices=['before-commit','after-commit'])
    args=parser.parse_args()
    if args.crash_worker:crash_worker(args.crash_worker,args.phase)
    else:raise SystemExit(run(args))

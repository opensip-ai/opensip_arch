# Control C2 - proposed carrierFormat 3 DDL, migration and open dispatch, by execution.
import hashlib,importlib.util,json,os,re,sqlite3,sys
S=sys.argv[1]; V3=sys.argv[2]; O=sys.argv[3]
Q=9007199254740991
F2=os.path.join(S,'docs/coop/completion/security-schemas.v2/grant-journal.sql')
ddl2=open(F2,encoding='utf-8').read()
ddl3=open(V3,encoding='utf-8').read()
sp=importlib.util.spec_from_file_location('sul8',os.path.join(S,'docs/coop/completion/security_unit_lib_v8.py'))
L=importlib.util.module_from_spec(sp); sp.loader.exec_module(L)
R={'control':'c2-carrier-v3','frozenV2Sha256':hashlib.sha256(open(F2,'rb').read()).hexdigest(),
   'proposedV3Sha256':hashlib.sha256(open(V3,'rb').read()).hexdigest()}
PKD='e'*64
C3=('grantGeneration','seq','record_schema','record_type','operation_ref','request_ref','token',
 'install_generation_id','manifest_digest','platform','run_id','body','body_sha256','prev_sha256')
OP='op-'+'a'*32; H='b'*64; RUN='run3:'+'0'*64

def r3(gg,seq,rs,rt,pf=None,tk=None,ig=None,md=None,rid=None,rq=None,op=OP):
    return (gg,seq,rs,rt,op,rq,tk,ig,md,pf,rid,'{}',H,H)
def new3(first=1,cl=1,mf=None,mop=None):
    c=sqlite3.connect(':memory:'); c.executescript(ddl3)
    c.execute('INSERT INTO carrier_format VALUES (1,3,?,?,?,?,?)',(PKD,first,cl,mf,mop)); c.commit()
    return c
def ins3(c,row):
    q='INSERT INTO grant_journal_v3 ('+','.join(C3)+') VALUES ('+','.join(['?']*len(C3))+')'
    try:
        c.execute(q,row); c.commit(); return {'admitted':True,'error':None}
    except sqlite3.Error as e:
        return {'admitted':False,'error':str(e)}
P={}
G3=dict(pf='macos-aarch64',tk='PT-FS-READ-PROJECT',ig='ig1',md='c'*64)
c=new3(); P['V01_schema3_SEAL_with_run3']=ins3(c,r3(1,1,3,'SEAL',rid=RUN)); c.close()
c=new3(); P['V02_schema3_SEAL_without_run_id']=ins3(c,r3(1,1,3,'SEAL')); c.close()
for pf in ('macos-aarch64','macos-x86_64','linux-x86_64-gnu','linux-aarch64-gnu'):
    c=new3(); P['V03_GRANT_machineId_'+pf]=ins3(c,r3(1,1,3,'GRANT',pf=pf,tk='PT-FS-READ-PROJECT',ig='ig1',md='c'*64)); c.close()
for pf in ('macos-arm64','linux-x86_64','linux-arm64'):
    c=new3(); P['V04_GRANT_displayAliasOnly_'+pf]=ins3(c,r3(1,1,3,'GRANT',pf=pf,tk='PT-FS-READ-PROJECT',ig='ig1',md='c'*64)); c.close()

c=new3(); P['V05a_TERMINAL_as_schema3']=ins3(c,r3(1,1,3,'TERMINAL')); c.close()
c=new3(); P['V05b_TERMINAL_as_frozen_schema1']=ins3(c,r3(1,1,1,'TERMINAL')); c.close()
c=new3(); P['V06_operational_row_as_schema1']=ins3(c,r3(1,1,1,'SEAL',rid=RUN)); c.close()
c=new3()
P['V07a_REV_seq1']=ins3(c,r3(1,1,3,'REV'))
P['V07b_TERMINAL_seq2']=ins3(c,r3(1,2,1,'TERMINAL'))
P['V07c_append_after_TERMINAL']=ins3(c,r3(1,3,3,'REV'))
c.close()
c=new3(); P['V08a_non_contiguous']=ins3(c,r3(1,2,3,'REV')); c.close()
c=new3(); P['V08b_first_REV']=ins3(c,r3(1,1,3,'REV'))
for nm,st in (('V08c_UPDATE','UPDATE grant_journal_v3 SET request_ref=?'),('V08d_DELETE','DELETE FROM grant_journal_v3')):
    try:
        c.execute(st,('x',)) if '?' in st else c.execute(st)
        c.commit(); P[nm]={'admitted':True,'error':None}
    except sqlite3.Error as e:
        P[nm]={'admitted':False,'error':str(e)}
c.close()
for nm,rt in (('V14_NARROW','NARROW'),('V14_EXPIRY','EXPIRY'),('V14_AUD','AUD'),('V14_CHECKPOINT','CHECKPOINT'),('V14_MIGRATION','MIGRATION')):
    c=new3(); P[nm]=ins3(c,r3(1,1,3,rt)); c.close()

c=new3(first=5); P['V10_generation_below_first_generation']=ins3(c,r3(4,1,3,'REV')); c.close()
c=new3()
P['V11a_gen1']=ins3(c,r3(1,1,3,'REV'))
P['V11b_gen2']=ins3(c,r3(2,1,3,'REV'))
P['V11c_back_to_superseded_gen1']=ins3(c,r3(1,2,3,'REV'))
c.close()
c=new3(); P['V12_TERMINAL_carrying_platform']=ins3(c,r3(1,1,1,'TERMINAL',pf='macos-aarch64')); c.close()
c=new3()
for nm,st,pr in (('V13a_carrier_format_UPDATE','UPDATE carrier_format SET first_generation=9',()),
                 ('V13b_carrier_format_DELETE','DELETE FROM carrier_format',()),
                 ('V13c_second_carrier_format_row','INSERT INTO carrier_format VALUES (2,3,?,1,1,NULL,NULL)',(PKD,))):
    try:
        c.execute(st,pr); c.commit(); P[nm]={'admitted':True,'error':None}
    except sqlite3.Error as e:
        P[nm]={'admitted':False,'error':str(e)}
c.close()
c=new3()
tg=c.execute('SELECT sql FROM sqlite_master WHERE type=? AND name=?',('trigger','gj3_append_laws')).fetchone()[0]
c.execute('DROP TRIGGER gj3_append_laws'); c.commit()
P['V09a_harness_seed_tail_at_cap_minus_1']=ins3(c,r3(1,Q-1,3,'REV'))
c.executescript(tg)
P['V09b_reserved_slot_operational']=ins3(c,r3(1,Q,3,'SEAL',rid=RUN))
P['V09c_reserved_slot_TERMINAL']=ins3(c,r3(1,Q,1,'TERMINAL'))
c.close()
R['ddlProbes']=P
R['v09HarnessDisclosure']='V09 only: gj3_append_laws lifted in an in-memory scratch database to seed tail=cap-1, then reinstalled verbatim from sqlite_master. No file modified.'

C2C=('grantGeneration','seq','record_type','operation_ref','request_ref','token',
 'install_generation_id','manifest_digest','platform','body','body_sha256','prev_sha256')
def r2(seq,rt,pf=None,tk=None,ig=None,md=None,op=OP):
    return (1,seq,rt,op,None,tk,ig,md,pf,'{}',H,H)
def ins2(c,row):
    q='INSERT INTO grant_journal ('+','.join(C2C)+') VALUES ('+','.join(['?']*len(C2C))+')'
    try:
        c.execute(q,row); c.commit(); return {'admitted':True,'error':None}
    except sqlite3.Error as e:
        return {'admitted':False,'error':str(e)}
M={}
c=sqlite3.connect(':memory:'); c.executescript(ddl2)
M['m1_legacy_GRANT_alias_platform']=ins2(c,r2(1,'GRANT',pf='macos-arm64',tk='PT-FS-READ-PROJECT',ig='ig1',md='c'*64))
M['m2_legacy_RCO']=ins2(c,r2(2,'RCO'))
before=c.execute('SELECT * FROM grant_journal ORDER BY grantGeneration,seq').fetchall()
beforeSql=sorted(c.execute('SELECT type,name,sql FROM sqlite_master').fetchall())
M['m3_TERMINAL_closes_legacy_generation_under_frozen_constraints']=ins2(c,r2(3,'TERMINAL'))
M['m4_legacy_append_after_TERMINAL']=ins2(c,r2(4,'RCO'))

c.executescript(ddl3)
c.execute('INSERT INTO carrier_format VALUES (1,3,?,2,1,2,?)',(PKD,OP)); c.commit()
M['m5_v3_gen2_schema3_SEAL']=ins3(c,r3(2,1,3,'SEAL',rid=RUN))
M['m6_v3_gen1_precedes_first_generation']=ins3(c,r3(1,1,3,'REV'))
after=c.execute('SELECT * FROM grant_journal ORDER BY grantGeneration,seq').fetchall()
afterSql=sorted(c.execute('SELECT type,name,sql FROM sqlite_master').fetchall())
M['m7_legacy_rows_unchanged_excluding_new_TERMINAL']=(after[:len(before)]==before)
M['m8_legacy_row_count_before_after']=[len(before),len(after)]
oldnames={x[1] for x in beforeSql}
M['m9_legacy_schema_objects_unchanged']=sorted([x for x in afterSql if x[1] in oldnames])==beforeSql
M['m10_new_schema_objects']=sorted(x[1] for x in afterSql if x[1] not in oldnames)
try:
    c.executescript(ddl3); M['m11_second_migration']={'admitted':True,'error':None}
except sqlite3.Error as e:
    M['m11_second_migration']={'admitted':False,'error':str(e)}
M['m12_legacy_platform_value_retained_verbatim']=c.execute('SELECT platform FROM grant_journal WHERE record_type=?',('GRANT',)).fetchone()[0]
R['migration']=M
c.close()

DDL1=open(os.path.join(S,'docs/coop/completion/security-completion.v1.md'),encoding='utf-8').read()
DDL1=DDL1.split(chr(96)*3+'sql')[1].split(chr(96)*3)[0]
def detect(c):
    n={x[0] for x in c.execute('SELECT name FROM sqlite_master').fetchall()}
    if 'grant_journal_v3' in n and 'carrier_format' in n: return 3
    if 'grant_journal' in n and 'gj_seq_contiguous' in n: return 2
    if 'grant_journal' in n: return 1
    return 0
DT={}
c=sqlite3.connect(':memory:'); c.executescript(DDL1); DT['format1_db']=detect(c); c.close()
c=sqlite3.connect(':memory:'); c.executescript(ddl2); DT['format2_db']=detect(c); c.close()
c=new3(); DT['format3_fresh']=detect(c); c.close()
c=sqlite3.connect(':memory:'); DT['empty_db']=detect(c); c.close()

c=sqlite3.connect(':memory:'); c.executescript(ddl2); c.executescript(ddl3)
DT['migrated_2_to_3']=detect(c)
q1=c.execute('SELECT sql FROM sqlite_master WHERE name=?',('carrier_quarantine',)).fetchone()[0]
p1=c.execute('SELECT sql FROM sqlite_master WHERE name=?',('carrier_capacity_pause',)).fetchone()[0]
c.close()
c=sqlite3.connect(':memory:'); c.executescript(ddl2)
DT['frozen_side_table_text_preserved']=[
 q1==c.execute('SELECT sql FROM sqlite_master WHERE name=?',('carrier_quarantine',)).fetchone()[0],
 p1==c.execute('SELECT sql FROM sqlite_master WHERE name=?',('carrier_capacity_pause',)).fetchone()[0]]
c.close()
DT['expected']={'format1_db':1,'format2_db':2,'format3_fresh':3,'migrated_2_to_3':3,'empty_db':0}
DT['allCorrect']=all(DT[k]==v for k,v in DT['expected'].items())
R['openDispatch']=DT

def bsha(o): return L.record_body_sha(o)
def prev1(prev_body_sha,prev_seq): return hashlib.sha256((prev_body_sha+str(prev_seq)).encode('ascii')).hexdigest()
def prev2(prev_prev,prev_body_sha,prev_seq): return hashlib.sha256((prev_prev+prev_body_sha+str(prev_seq)).encode('ascii')).hexdigest()
def mkbody(seq,rt,extra=None):
    b={'recordSchema':3,'grantGeneration':2,'seq':seq,'operationRef':OP,'recordType':rt}
    if extra: b.update(extra)
    return b
def build(bodies,law,pk='proj-key-example',gg=2):
    rows=[]; g=L.genesis_prev(pk,gg)
    for i,b in enumerate(bodies):
        s=i+1; bs=bsha(b)
        if s==1: pv=g
        elif law==1: pv=prev1(rows[-1]['body_sha256'],s-1)
        else: pv=prev2(rows[-1]['prev_sha256'],rows[-1]['body_sha256'],s-1)
        rows.append({'seq':s,'body':b,'body_sha256':bs,'prev_sha256':pv})
    return rows

def verify(rows,law,pk='proj-key-example',gg=2):
    g=L.genesis_prev(pk,gg); ok=True; bad=[]
    for i,r in enumerate(rows):
        if bsha(r['body'])!=r['body_sha256']: ok=False; bad.append(('body',r['seq']))
        if r['seq']==1:
            if r['prev_sha256']!=g: ok=False; bad.append(('genesis',1))
        elif law==1:
            if r['prev_sha256']!=prev1(rows[i-1]['body_sha256'],r['seq']-1): ok=False; bad.append(('chain',r['seq']))
        else:
            if r['prev_sha256']!=prev2(rows[i-1]['prev_sha256'],rows[i-1]['body_sha256'],r['seq']-1): ok=False; bad.append(('chain',r['seq']))
    return {'consistent':ok,'violations':bad}
BODIES=[mkbody(1,'GRANT'),mkbody(2,'RA',{'requestRef':'rq1'}),mkbody(3,'SEAL',{'runId':RUN})]
A={}
for law in (1,2):
    rows=build(BODIES,law)
    A['law%d_clean'%law]=verify(rows,law)
    A['law%d_tail_body_sha256'%law]=rows[-1]['body_sha256']
    A['law%d_tail_prev_sha256'%law]=rows[-1]['prev_sha256']

SUB=[mkbody(1,'GRANT'),mkbody(2,'RA',{'requestRef':'SUBSTITUTED'}),mkbody(3,'SEAL',{'runId':RUN})]
for law in (1,2):
    orig=build(BODIES,law); tamp=build(SUB,law)
    A['law%d_substituted_interior_body_selfconsistent'%law]=verify(tamp,law)
    A['law%d_tail_body_sha256_changed'%law]=orig[-1]['body_sha256']!=tamp[-1]['body_sha256']
    A['law%d_tail_prev_sha256_changed'%law]=orig[-1]['prev_sha256']!=tamp[-1]['prev_sha256']
    A['law%d_witnessed_tail_detects_interior_substitution'%law]=(
        orig[-1]['body_sha256']!=tamp[-1]['body_sha256'] or orig[-1]['prev_sha256']!=tamp[-1]['prev_sha256'])
A['note']=('A witness names {seq, bodySha256}. Detection from a witnessed tail alone therefore '
 'depends on whether the tail body_sha256 changes. law1 binds only the immediately previous body '
 'digest and index, so an interior substitution with a recomputed successor prev_sha256 leaves the '
 'tail body_sha256 unchanged and the whole chain self-consistent.')
A['law1_witness_field_detects_substitution']=A['law1_tail_body_sha256_changed']
A['law2_witness_field_detects_substitution']=A['law2_tail_body_sha256_changed']
R['chainLaw']=A
open(O,'w').write(json.dumps(R,indent=1,sort_keys=True)+chr(10))
print('WROTE',O)
print(json.dumps(R['openDispatch'],indent=1,sort_keys=True))
print(json.dumps(R['chainLaw'],indent=1,sort_keys=True))

SUB1=[mkbody(1,'GRANT',{'grant':'SUBSTITUTED'}),mkbody(2,'RA',{'requestRef':'rq1'}),mkbody(3,'SEAL',{'runId':RUN})]
B={}
for law in (1,2):
    orig=build(BODIES,law)
    for nm,alt in (('sub_at_seq1',SUB1),('sub_at_seq2',SUB)):
        t=build(alt,law)
        B['law%d_%s_selfconsistent'%(law,nm)]=verify(t,law)['consistent']
        B['law%d_%s_seen_by_witness_bodySha256'%(law,nm)]=orig[-1]['body_sha256']!=t[-1]['body_sha256']
        B['law%d_%s_seen_by_chainhead_prev'%(law,nm)]=orig[-1]['prev_sha256']!=t[-1]['prev_sha256']

B['v1_stated_intent']='Hash chain. Tamper-evidence for audit, not tamper-proof; the chain head is in the witness.'
B['v8_witness_members']=['witnessSchema','projectKeyDigest','grantGeneration','seq','state','bodySha256']
B['witness_carries_chain_head']=('prev_sha256' in B['v8_witness_members']) or ('chainHead' in B['v8_witness_members'])
R['anchorFieldDiscrimination']=B
open(O,'w').write(json.dumps(R,indent=1,sort_keys=True)+chr(10))
print(json.dumps(B,indent=1,sort_keys=True))

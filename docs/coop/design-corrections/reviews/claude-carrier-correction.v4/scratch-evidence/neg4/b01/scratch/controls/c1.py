# Control C1 - inherited grant-journal carrier laws, by execution. Read-only vs Source25.
import hashlib,importlib.util,inspect,json,os,re,sqlite3,sys
S=sys.argv[1]; O=sys.argv[2]
Q=9007199254740991
R={'control':'c1-inherited-carrier-laws','sourceRoot':S}
M=['docs/coop/completion/security-schemas.v2/grant-journal.sql',
'docs/coop/completion/security-schemas.v2/journal-record.schema.json',
'docs/coop/completion/security-schemas.v8/journal-record.schema.json',
'docs/coop/completion/security_unit_lib_v8.py',
'docs/coop/completion/security-completion.v1.md',
'docs/coop/completion/security-completion.v8.md',
'docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json',
'docs/v2/contracts/product-v1/security-and-lifecycle.md']
R['members']={}
for m in M:
    b=open(os.path.join(S,m),'rb').read()
    R['members'][m]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}

ddl=open(os.path.join(S,M[0]),encoding='utf-8').read()
pt=set(re.findall(r'[A-Z]+',re.search(r'record_type\s+TEXT\s+NOT NULL CHECK \(record_type IN\s*\(([^)]*)\)',ddl).group(1)))
b1=json.load(open(os.path.join(S,M[1]),encoding='utf-8'))
t1=set(v['properties']['recordType']['const'] for v in b1['oneOf'])
sl=json.load(open(os.path.join(S,M[6]),encoding='utf-8'))
t3=set(sl['$defs']['JournalRecord']['properties']['recordType']['enum'])
t2=set(sl['$defs']['JournalRecordV2']['properties']['recordType']['enum'])
tl=set(sl['schemas']['LinearizationV1']['properties']['journalTypes']['items']['enum'])
R['recordTypeAlgebra']={
 'physicalCheckDDL':sorted(pt),
 'logicalBodySchema1':sorted(t1),
 'logicalBodySchema1_recordSchemaConst':sorted(set(v['properties']['recordSchema']['const'] for v in b1['oneOf'])),
 'logicalJournalRecordV2_schema2':sorted(t2),
 'logicalJournalRecord_schema3':sorted(t3),
 'linearizationV1JournalTypes':sorted(tl),
 'schema3_types_not_admitted_by_physical_DDL':sorted(t3-pt),
 'physical_types_absent_from_schema3':sorted(pt-t3),
 'schema3_equals_linearizationTypes':sorted(t3)==sorted(tl),
 'schema1_equals_physicalDDL':sorted(t1)==sorted(pt),
 'schema3_additionalProperties':sl['$defs']['JournalRecord'].get('additionalProperties')}

pp=set(re.findall(r'[a-z0-9_-]+',re.search(r'platform\s+TEXT CHECK \(platform IS NULL OR platform IN \(([^)]*)\)',ddl).group(1)))
sec=open(os.path.join(S,M[7]),encoding='utf-8').read()
tbl=re.findall(r'^\| .([a-z0-9x_-]+). \| ([a-z0-9x_-]+) \| ',sec,re.M)
mid=set(x[0] for x in tbl); al=set(x[1] for x in tbl)
R['platformVocabulary']={'physicalCheckDDL':sorted(pp),
 's8_machineId_to_displayAlias':tbl,'machineIds':sorted(mid),'displayAliases':sorted(al),
 'machineIds_not_admitted_by_physical_DDL':sorted(mid-pp),
 'physical_values_that_are_display_aliases_only':sorted((pp&al)-mid),
 'lawfully_shared_values':sorted(pp&mid)}

sp=importlib.util.spec_from_file_location('sul8',os.path.join(S,M[3]))
L=importlib.util.module_from_spec(sp); sp.loader.exec_module(L)
bd={'recordSchema':1,'grantGeneration':1,'seq':1,'operationRef':'op-'+'0'*32,
 'wallClockData':'2026-01-01T00:00:00Z','recordType':'REV','reason':'operator'}
cb=L.canon(bd).encode('utf-8'); dm=L.DOMAIN_TAGS['journal']
D={'domainTag':dm,'canonicalBodyText':L.canon(bd),'record_body_sha':L.record_body_sha(bd),
 'raw_sha256_of_canonical_body':hashlib.sha256(cb).hexdigest(),
 'domain_framed_sha256':hashlib.sha256(dm.encode('utf-8')+b'\x00'+cb).hexdigest()}
D['body_sha256_is_raw_sha256_of_body']=D['record_body_sha']==D['raw_sha256_of_canonical_body']
D['body_sha256_is_domain_framed']=D['record_body_sha']==D['domain_framed_sha256']
R['digestSemantics']=D

D['genesis_prev_example']=L.genesis_prev('proj-key-example',1)
s8=open(os.path.join(S,M[3]),encoding='utf-8').read()
D['prev_sha256_only_specification']=[l.strip() for l in open(os.path.join(S,M[4]),encoding='utf-8').read().split(chr(10)) if 'prev_sha256' in l and 'chain' in l]
D['reference_lib_defines_a_prev_sha_function']=bool(re.search(r'def [a-z_]*prev[a-z_]*\(',s8))
D['genesis_prev_call_sites_in_lib']=len(re.findall(r'genesis_prev',s8))-1
D['v8_defers_ddl_to_v2']=[l.strip() for l in open(os.path.join(S,M[5]),encoding='utf-8').read().split(chr(10)) if 'uint53 cap' in l]

OP='op-'+'a'*32; H='b'*64
C=('grantGeneration','seq','record_type','operation_ref','request_ref','token',
 'install_generation_id','manifest_digest','platform','body','body_sha256','prev_sha256')
def rw(seq,rt,pf=None,tk=None,ig=None,md=None,op=OP):
    return (1,seq,rt,op,None,tk,ig,md,pf,'{}',H,H)
def fresh():
    c=sqlite3.connect(':memory:'); c.executescript(ddl); return c
def ins(c,r):
    q='INSERT INTO grant_journal ('+','.join(C)+') VALUES ('+','.join(['?']*len(C))+')'
    try:
        c.execute(q,r); c.commit(); return {'admitted':True,'error':None}
    except sqlite3.Error as e:
        return {'admitted':False,'error':str(e)}
P={}

G=dict(pf='macos-arm64',tk='PT-FS-READ-PROJECT',ig='ig1',md='c'*64)
c=fresh(); P['L1_SEAL_append_schema3_recordType']=ins(c,rw(1,'SEAL')); c.close()
c=fresh(); P['L2a_GRANT_machineId_macos_aarch64']=ins(c,rw(1,'GRANT',pf='macos-aarch64',tk='PT-FS-READ-PROJECT',ig='ig1',md='c'*64)); c.close()
c=fresh(); P['L2b_GRANT_machineId_linux_x86_64_gnu']=ins(c,rw(1,'GRANT',pf='linux-x86_64-gnu',tk='PT-FS-READ-PROJECT',ig='ig1',md='c'*64)); c.close()
c=fresh(); P['L3_GRANT_displayAlias_macos_arm64']=ins(c,rw(1,'GRANT',**G)); c.close()
c=fresh(); P['L4_non_contiguous_seq2_on_empty']=ins(c,rw(2,'REV')); c.close()
c=fresh(); P['L7_seq_above_uint53_cap']=ins(c,rw(Q+1,'REV')); c.close()
c=fresh(); P['L9_malformed_operation_ref']=ins(c,rw(1,'REV',op='op-XYZ')); c.close()

c=fresh()
P['L5a_first_REV']=ins(c,rw(1,'REV'))
for nm,st in (('L5b_UPDATE','UPDATE grant_journal SET request_ref=?'),('L5c_DELETE','DELETE FROM grant_journal')):
    try:
        c.execute(st,('x',)) if '?' in st else c.execute(st)
        c.commit(); P[nm]={'admitted':True,'error':None}
    except sqlite3.Error as e:
        P[nm]={'admitted':False,'error':str(e)}
c.close()
c=fresh()
P['L6a_REV_seq1']=ins(c,rw(1,'REV'))
P['L6b_TERMINAL_seq2']=ins(c,rw(2,'TERMINAL'))
P['L6c_append_after_TERMINAL']=ins(c,rw(3,'REV'))
c.close()

c=fresh()
tg=c.execute('SELECT sql FROM sqlite_master WHERE type=? AND name=?',('trigger','gj_seq_contiguous')).fetchone()[0]
c.execute('DROP TRIGGER gj_seq_contiguous'); c.commit()
P['L8a_harness_seed_tail_at_cap_minus_1']=ins(c,rw(Q-1,'REV'))
c.executescript(tg)
P['L8b_reserved_slot_non_TERMINAL']=ins(c,rw(Q,'REV'))
P['L8c_reserved_slot_TERMINAL']=ins(c,rw(Q,'TERMINAL'))
c.close()
R['ddlProbes']=P
R['ddlProbeHarnessDisclosure']=('L8 only: the frozen gj_seq_contiguous trigger was lifted in an in-memory scratch database to seed tail=cap-1, then reinstalled verbatim from sqlite_master before the reserved-slot probes. The reserved slot is unreachable by contiguous append in bounded time. No frozen file was modified.')
R['reinstalledTriggerTextIsFrozenText']=tg.strip() in ddl

PK='proj-key-example'; GG=1; pkd=L.project_key_digest(PK)
def W(sq,st,sh=None):
    return {'witnessSchema':1,'projectKeyDigest':pkd,'grantGeneration':GG,'seq':sq,'state':st,'bodySha256':sh}
A='a'*64; B='d'*64
CS=[('empty carrier, no witness',None,None),
 ('COMMITTED n = tail n, same body hash',(5,A),W(5,'COMMITTED',A)),
 ('COMMITTED 0 on empty carrier',None,W(0,'COMMITTED',None)),
 ('PENDING n+1 with tail n',(5,A),W(6,'PENDING',B)),
 ('PENDING n = tail n, same hash',(5,A),W(5,'PENDING',A)),
 ('COMMITTED n > tail',(5,A),W(7,'COMMITTED',B)),
 ('COMMITTED n = tail n, different hash',(5,A),W(5,'COMMITTED',B)),
 ('PENDING n = tail n, different hash',(5,A),W(5,'PENDING',B)),
 ('tail > witness seq (COMMITTED)',(9,A),W(5,'COMMITTED',B)),
 ('PENDING not adjacent to the tail',(5,A),W(9,'PENDING',B)),
 ('witness absent with a non-empty journal',(5,A),None),
 ('malformed shape: PENDING 0',(5,A),W(0,'PENDING',None)),
 ('malformed shape: bool seq',(5,A),W(True,'COMMITTED',A))]

CS.append(('witness names another carrier (generation)',(5,A),
 {'witnessSchema':1,'projectKeyDigest':pkd,'grantGeneration':2,'seq':5,'state':'COMMITTED','bodySha256':A}))
R['reconcileWitness']=[]
for lb,tl2,wt in CS:
    a,d=L.reconcile_witness(tl2,wt,PK,GG)
    R['reconcileWitness'].append({'case':lb,'tail':tl2,'action':a,'detail':d})
sw=inspect.getsource(L._reconcile_witness_checked)
R['reconcileWitnessSignature']=str(inspect.signature(L.reconcile_witness))
R['reconcileWitnessConsultsScTrustHighWater']=('high_water' in sw) or ('highWater' in sw)
R['reconcileWitnessIgnoresTerminalArg']='terminal' not in sw.split('def ')[1].split(chr(10),1)[1]
open(O,'w').write(json.dumps(R,indent=1,sort_keys=True)+chr(10))
print('WROTE',O)
for k in ('recordTypeAlgebra','platformVocabulary','digestSemantics'):
    print(k,json.dumps(R[k],indent=1,sort_keys=True))

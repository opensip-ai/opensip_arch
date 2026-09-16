# Control C3 - bounded read-only recovery algorithm and commit-admission gate models.
import itertools,json,sys
O=sys.argv[1]
R={'control':'c3-recovery-and-gate'}
class Mutation(Exception): pass
class Env:
    def __init__(s,ledger,journal,witness,floor,active,reopen=None,carrierFormat=3):
        s.ledger=ledger; s.journal=journal; s.witness=witness; s.floor=floor
        s.active=active; s.reopen=reopen; s.carrierFormat=carrierFormat
        s.ledgerOpens=0; s.journalOpens=0; s.mutations=[]
    def snapLedger(s):
        s.ledgerOpens+=1
        if s.ledger is None: raise IOError('ledger unreadable')
        return dict(s.ledger)
    def snapJournal(s,second=False):
        s.journalOpens+=1
        j=s.reopen if (second and s.reopen is not None) else s.journal
        return dict(j) if j is not None else None
    def mutate(s,what): s.mutations.append(what); raise Mutation(what)

WMEM={'witnessSchema','projectKeyDigest','grantGeneration','seq','state','bodySha256'}
def wshape(w):
    if w is None or w=='MALFORMED': return False
    if set(w.keys())!=WMEM: return False
    if w['witnessSchema']!=1: return False
    if type(w['seq']) is bool or not isinstance(w['seq'],int): return False
    if not (0<=w['seq']<=9007199254740991): return False
    if w['state'] not in ('PENDING','COMMITTED'): return False
    if w['state']=='PENDING' and w['seq']<1: return False
    if w['seq']>=1 and not (isinstance(w['bodySha256'],str) and len(w['bodySha256'])==64): return False
    if w['seq']==0 and w['bodySha256'] is not None: return False
    return True
def out(c,anchor=None,diag=None,notInvalidated=False,env=None):
    return {'conclusion':c,'anchor':anchor,'diagnosis':diag or [],'notInvalidated':notInvalidated,
            'mutations':list(env.mutations) if env else [],'ledgerOpens':env.ledgerOpens if env else 0,
            'journalOpens':env.journalOpens if env else 0}

def recover(req,env):
    try: Lg=env.snapLedger()
    except IOError: return out('unavailable',diag=['ledger-unreadable','F24'],env=env)
    if req['executionId'] in env.active:
        return out('in-progress',diag=['active-attempt','F29'],env=env)
    rc=Lg.get('receipt'); asc=Lg.get('association')
    if rc is None and asc is None:
        return out('not-committed-verified-absent',diag=['verified-empty-exact-lookup','F36'],env=env)
    if (rc is None) != (asc is None):
        return out('unknown-custody',diag=['receipt-association-contradiction','F23'],env=env)
    if asc['storeGenerationDigest']!=req['storeGenerationDigest'] or asc['namespaceId']!=req['namespaceId']:
        return out('unknown-custody',diag=['binding-swap','F27'],env=env)
    k=asc['journalSeq']
    J=env.snapJournal()
    if J is None: return out('unavailable',diag=['carrier-unreadable'],env=env)
    d=[]
    if env.carrierFormat<3:
        return out('unknown-carrier-incompatible',diag=['no-SEAL-representable','F31','F46'],env=env)
    if k>J['tail']:
        d.append('journal-view-behind-ledger-snapshot')
        J=env.snapJournal(second=True)
        if J is None: return out('unavailable',diag=d+['carrier-unreadable'],env=env)
        if k>J['tail']:
            if env.floor and env.floor.get('lastSeq',0)>=k:
                return out('unknown-quarantine-condition',diag=d+['uncertainTailLoss','F22'],notInvalidated=True,env=env)
            return out('unavailable-busy',diag=d+['reopen-did-not-reconcile','owner=security-carrier','F43'],env=env)
        d.append('reconciled-after-single-reopen')
    W=env.witness; H=env.floor; t=J['tail']
    if W is None:
        return out('unknown-custody',diag=d+['witnesslessRestore','F21'],notInvalidated=True,env=env)
    if not wshape(W):
        return out('unknown-custody',diag=d+['witnessMalformed','F20'],notInvalidated=True,env=env)
    if W['projectKeyDigest']!=asc['journalCarrierDigest'] or W['grantGeneration']!=asc['grantGeneration']:
        return out('unknown-custody',diag=d+['witness-names-another-carrier','F20'],notInvalidated=True,env=env)
    if not J.get('contiguous',True):
        return out('unknown-custody',diag=d+['non-contiguous-sequence'],notInvalidated=True,env=env)
    if H is None:
        return out('unknown-custody',diag=d+['no-sc-trust-floor-for-carrier'],notInvalidated=True,env=env)
    if t<H['lastSeq']:
        return out('unknown-quarantine-condition',diag=d+['tail-below-observed-floor','F22'],notInvalidated=True,env=env)
    row=J['rows'].get(k)
    if row is None:
        return out('unknown-custody',diag=d+['seal-row-absent-at-journalSeq','F33'],notInvalidated=True,env=env)
    if not (row['record_type']=='SEAL' and row['record_schema']==3
            and row['body_sha256']==asc['journalBodySha256']
            and row['operation_ref']==asc['operationRef'] and row['run_id']==asc['runId']):
        return out('unknown-custody',diag=d+['join-differs','F33'],notInvalidated=True,env=env)
    floorOk = (H['lastSeq']==0) or (J['rows'].get(H['lastSeq']) is not None
        and J['rows'][H['lastSeq']]['body_sha256']==H['tailSha256'])
    anchor=None
    if W['state']=='COMMITTED' and W['seq']==t and (t==0 or W['bodySha256']==J['rows'][t]['body_sha256']):
        anchor='witness-committed-tail'
    elif W['state']=='PENDING' and W['seq']==t and W['bodySha256']==J['rows'][t]['body_sha256']:
        anchor='witness-pending-at-tail'; d.append('witnessWouldAdvance')
    elif W['state']=='PENDING' and W['seq']==t+1:
        d.append('witnessWouldRevert'); d.append('no-live-witnessed-anchor-for-durable-prefix')
        if not floorOk:
            return out('unknown-quarantine-condition',diag=d+['floor-hash-contradicts-tail','F22'],notInvalidated=True,env=env)
        if k<=H['lastSeq']: anchor='sc-trust-floor'
        else:
            return out('unknown-custody',diag=d+['above-floor-under-pending-next-slot','F44'],notInvalidated=True,env=env)
    else:
        return out('unknown-quarantine-condition',diag=d+['witness-state-unreconciled','F20'],notInvalidated=True,env=env)
    if not floorOk:
        return out('unknown-quarantine-condition',diag=d+['floor-hash-contradicts-tail','F22'],notInvalidated=True,env=env)
    av=Lg.get('availability','retained')
    c='committed-historically' if av=='retained' else 'committed-availability-degraded'
    if av!='retained': d.append('availability='+av); d.append('F25')
    d.append('confirmed-under-retained-custody')
    d.append('interior-bodies-not-authenticated')
    return out(c,anchor=anchor,diag=d,env=env)

PKD='e'*64; OP='op-'+'a'*32; RUN='run3:'+'0'*64; SGD='f'*64; NS='ns1'; EX='exec1_'+'1'*32
def mkrows(n,sealat):
    return {i:{'record_type':('SEAL' if i==sealat else 'RCO'),'record_schema':3,
        'body_sha256':('%064x'%i),'operation_ref':OP,'run_id':(RUN if i==sealat else None)} for i in range(1,n+1)}
def asc(k):
    return {'storeGenerationDigest':SGD,'namespaceId':NS,'executionId':EX,'runId':RUN,
        'journalCarrierDigest':PKD,'grantGeneration':1,'journalSeq':k,
        'journalBodySha256':('%064x'%k),'operationRef':OP}
def W(sq,st,sh):
    return {'witnessSchema':1,'projectKeyDigest':PKD,'grantGeneration':1,'seq':sq,'state':st,'bodySha256':sh}
def Fl(ls): return {'projectKeyDigest':PKD,'grantGeneration':1,'lastSeq':ls,'tailSha256':('%064x'%ls) if ls else None}
def LG(av='retained',rc=True,ass=True,k=3):
    return {'receipt':{'x':1} if rc else None,'association':asc(k) if ass else None,'availability':av}
REQ={'storeGenerationDigest':SGD,'namespaceId':NS,'executionId':EX}
def J(t,n=None,sealat=3,contig=True):
    return {'tail':t,'rows':mkrows(n if n else t,sealat),'contiguous':contig}

CASES=[]
def add(nm,env,exp,expAnchor=None):
    r=recover(REQ,env)
    CASES.append({'case':nm,'expected':exp,'expectedAnchor':expAnchor,'got':r['conclusion'],
        'gotAnchor':r['anchor'],'pass':r['conclusion']==exp and r['anchor']==expAnchor,
        'diagnosis':r['diagnosis'],'mutations':r['mutations'],
        'ledgerOpens':r['ledgerOpens'],'journalOpens':r['journalOpens'],'notInvalidated':r['notInvalidated']})
add('A1 COMMITTED at tail, k<=t',Env(LG(),J(3),W(3,'COMMITTED','%064x'%3),Fl(3),set()),'committed-historically','witness-committed-tail')
add('A2 PENDING at tail same hash',Env(LG(),J(3),W(3,'PENDING','%064x'%3),Fl(3),set()),'committed-historically','witness-pending-at-tail')
add('A3 PENDING next slot, k<=floor',Env(LG(k=3),J(3),W(4,'PENDING','%064x'%4),Fl(3),set()),'committed-historically','sc-trust-floor')
add('A4 PENDING next slot, k>floor',Env(LG(k=3),J(3),W(4,'PENDING','%064x'%4),Fl(2),set()),'unknown-custody',None)
add('A5 PENDING next slot, floor hash mismatch',Env(LG(k=3),J(3),{'witnessSchema':1,'projectKeyDigest':PKD,'grantGeneration':1,'seq':4,'state':'PENDING','bodySha256':'%064x'%4},{'projectKeyDigest':PKD,'grantGeneration':1,'lastSeq':3,'tailSha256':'9'*64},set()),'unknown-quarantine-condition',None)
add('A6 tail below observed floor',Env(LG(k=3),J(3),W(3,'COMMITTED','%064x'%3),Fl(5),set()),'unknown-quarantine-condition',None)
add('A7 COMMITTED beyond tail',Env(LG(k=3),J(3),W(7,'COMMITTED','%064x'%7),Fl(3),set()),'unknown-quarantine-condition',None)
add('A8 witnessless restore',Env(LG(k=3),J(3),None,Fl(3),set()),'unknown-custody',None)
add('A9 witness malformed (PENDING 0)',Env(LG(k=3),J(3),W(0,'PENDING',None),Fl(3),set()),'unknown-custody',None)
add('A10 witness foreign carrier',Env(LG(k=3),J(3),{'witnessSchema':1,'projectKeyDigest':'1'*64,'grantGeneration':1,'seq':3,'state':'COMMITTED','bodySha256':'%064x'%3},Fl(3),set()),'unknown-custody',None)

add('B1 ordering hazard, single reopen reconciles',Env(LG(k=3),J(2,2,99),W(3,'COMMITTED','%064x'%3),Fl(3),set(),reopen=J(3)),'committed-historically','witness-committed-tail')
add('B2 hazard unreconciled, floor at/above k',Env(LG(k=3),J(2,2,99),W(2,'COMMITTED','%064x'%2),Fl(3),set(),reopen=J(2,2,99)),'unknown-quarantine-condition',None)
add('B3 hazard unreconciled, floor below k',Env(LG(k=3),J(2,2,99),W(2,'COMMITTED','%064x'%2),Fl(1),set(),reopen=J(2,2,99)),'unavailable-busy',None)
add('C1 ledger unreadable',Env(None,J(3),W(3,'COMMITTED','%064x'%3),Fl(3),set()),'unavailable',None)
add('C2 verified absent receipt and association',Env(LG(rc=False,ass=False),J(3),W(3,'COMMITTED','%064x'%3),Fl(3),set()),'not-committed-verified-absent',None)
add('C3 receipt present, association absent',Env(LG(ass=False),J(3),W(3,'COMMITTED','%064x'%3),Fl(3),set()),'unknown-custody',None)
add('C4 requested attempt actively running',Env(LG(k=3),J(3),W(3,'COMMITTED','%064x'%3),Fl(3),{EX}),'in-progress',None)
add('D1 carrierFormat 2 generation',Env(LG(k=3),J(3),W(3,'COMMITTED','%064x'%3),Fl(3),set(),carrierFormat=2),'unknown-carrier-incompatible',None)
add('D2 committed but availability purged',Env(LG(av='purged'),J(3),W(3,'COMMITTED','%064x'%3),Fl(3),set()),'committed-availability-degraded','witness-committed-tail')
add('D3 join differs at journalSeq',Env({'receipt':{'x':1},'association':dict(asc(3),journalBodySha256='7'*64),'availability':'retained'},J(3),W(3,'COMMITTED','%064x'%3),Fl(3),set()),'unknown-custody',None)
add('D4 binding swap',Env({'receipt':{'x':1},'association':dict(asc(3),namespaceId='other'),'availability':'retained'},J(3),W(3,'COMMITTED','%064x'%3),Fl(3),set()),'unknown-custody',None)
R['recoveryCases']=CASES
R['recoveryAllPass']=all(c['pass'] for c in CASES)
R['recoveryNoMutations']=all(c['mutations']==[] for c in CASES)
R['recoveryLedgerOpensAlwaysOne']=all(c['ledgerOpens']==1 for c in CASES)
R['recoveryJournalOpensAtMostTwo']=all(c['journalOpens']<=2 for c in CASES)

def attempt(schedule,commitResult):
    st='preparing'; seal=False; staged=False; issued=False; latched=False; ev2=[]
    for ev in schedule:
        if ev=='seal': seal=True; ev2.append('seal-durable')
        elif ev=='stage':
            if st=='preparing': staged=True; ev2.append('sql-staged-after-seal-witness')
        elif ev=='latch':
            latched=True
            if st=='preparing': st='latched'; ev2.append('latch-won-preparing')
            else: ev2.append('latch-post-admission-blocks-subsequent-effects-only')
        elif ev=='gate':
            if st=='preparing' and staged: st='commit-admitted'; ev2.append('commit-admitted')
            elif st=='latched': ev2.append('gate-refused-latch-won')
        elif ev=='commit':
            if st=='commit-admitted': issued=True; ev2.append('commit-issued:'+commitResult)
    return st,seal,staged,issued,latched,ev2

def conclude(st,seal,issued,commitResult):
    if st=='latched':
        return {'conclusion':'uncommitted','d9':None,'runIdObservable':False,
                'orphanSeal':seal,'note':'no evidence commit issued; SEAL stays an uncommitted attempt (F36)'}
    if st=='commit-admitted' and issued and commitResult=='confirmed':
        return {'conclusion':'committed','d9':None,'runIdObservable':True,'orphanSeal':False,'note':'latch can only refuse subsequent effects'}
    if st=='commit-admitted' and issued and commitResult=='delivery-failed':
        return {'conclusion':'committed-delivery-failed','d9':'DELIVERY.REQUIRED_FAILED/operational-failed/4',
                'runIdObservable':True,'orphanSeal':False,'note':'commit durable; required delivery failed after it'}
    if st=='commit-admitted' and issued and commitResult in ('error','barrier-unconfirmed'):
        return {'conclusion':'durability-undetermined','d9':'DURABILITY.COMMIT_FAILED/operational-failed/4',
                'runIdObservable':False,'orphanSeal':False,
                'note':'ExecutionId retained and terminal; runId omitted; no automatic write retry'}
    return {'conclusion':'uncommitted','d9':None,'runIdObservable':False,'orphanSeal':seal,'note':'gate never admitted'}

G=[]
def gadd(nm,sched,res,exp):
    st,seal,staged,issued,latched,ev2=attempt(sched,res)
    c=conclude(st,seal,issued,res)
    G.append({'case':nm,'schedule':sched,'commitResult':res,'state':st,'events':ev2,
              'expected':exp,'got':c['conclusion'],'pass':c['conclusion']==exp,
              'd9':c['d9'],'runIdObservable':c['runIdObservable'],'orphanSeal':c['orphanSeal'],'note':c['note']})
gadd('F38 latch wins while preparing',['seal','stage','latch','gate','commit'],'confirmed','uncommitted')
gadd('F39 latch after admission, commit confirmed',['seal','stage','gate','latch','commit'],'confirmed','committed')
gadd('F39b latch after admission, delivery fails',['seal','stage','gate','latch','commit'],'delivery-failed','committed-delivery-failed')
gadd('F40 latch during commit syscall, error',['seal','stage','gate','commit','latch'],'error','durability-undetermined')
gadd('F40b barrier unconfirmed',['seal','stage','gate','commit','latch'],'barrier-unconfirmed','durability-undetermined')
gadd('F18 latch before SEAL',['latch','seal','stage','gate','commit'],'confirmed','uncommitted')
gadd('F19 latch after SEAL before staging',['seal','latch','stage','gate','commit'],'confirmed','uncommitted')

base=['seal','stage','gate','commit']
viol=[]; total=0
for pos in range(len(base)+1):
    sched=base[:pos]+['latch']+base[pos:]
    for res in ('confirmed','error','delivery-failed'):
        total+=1
        st,seal,staged,issued,latched,ev2=attempt(sched,res)
        c=conclude(st,seal,issued,res)
        if (c['conclusion'] in ('committed','committed-delivery-failed')) and st=='latched':
            viol.append({'schedule':sched,'res':res,'bug':'committed-while-latch-won'})
        if c['conclusion']=='uncommitted' and issued:
            viol.append({'schedule':sched,'res':res,'bug':'uncommitted-after-commit-issued'})
R['gateCases']=G
R['gateAllPass']=all(g['pass'] for g in G)
R['gateExhaustive']={'interleavings':total,'violations':viol,'singleWinner':viol==[]}
R['cleanupOrder']=['release level-4 append mutex',
 'abort/release the open evidence level-3 transaction and the journal level-3 transaction',
 'with the stopped operation lease still held, fresh lawful level-3 journal transaction then level-4 to append REV/CLN',
 'release the operation lease',
 'ordinary S7 end handoff: fence, non-blocking re-lease, SC-TRUST high-water copy, release']
R['cleanupLaws']={'no_level3_under_level4':True,'no_fence_while_holding_lease':True,
 'drop_not_guaranteed_on':['mem::forget','process abort','stalled syscall'],
 'capacity_route':'security typed CarrierCapacityExhausted -> storage -> host/finalization.rs -> lifecycle rollover under the fence AFTER lease release; storage never calls lifecycle'}
open(O,'w').write(json.dumps(R,indent=1,sort_keys=True)+chr(10))
print('WROTE',O)
print('recoveryAllPass',R['recoveryAllPass'],'noMutations',R['recoveryNoMutations'])
print('ledgerOpens==1',R['recoveryLedgerOpensAlwaysOne'],'journalOpens<=2',R['recoveryJournalOpensAtMostTwo'])
print('gateAllPass',R['gateAllPass'],'gateExhaustive',R['gateExhaustive'])
for c in R['recoveryCases']:
    print((' PASS ' if c['pass'] else ' FAIL '),c['case'],'->',c['got'],c['gotAnchor'])

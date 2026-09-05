"""Systematic malformed-record challenges, design evidence; no qualification.
Every mutation is applied independently to a valid control. Type-changing
mutations are rejected, never exceptions. Unknown keys are tested in closed
records (not arbitrary namespace maps). Optional members have separate controls.
"""
from copy import deepcopy
import json
from pathlib import Path


def run(L, rec, rb):
    p=Path(__file__).parent
    bh=json.loads(rb('security-fixtures.v7/broker-handles.example.json'))
    root=json.loads(rb('security-fixtures.v7/root.example.json'))
    gj=json.loads(rb('security-fixtures.v7/grant-journal.example.json'))
    first=bh['cases'][0]
    request={'body':first['body'], 'ctx':{'connectionMap':bh['connectionMaps']['example'], 'currentBinding':first['currentBinding'], 'journalState':bh['journalStates']['example'], 'snapshotMembers':bh['snapshotMembersDefault']}}
    courier=deepcopy(next(c for c in bh['resultCourier']['cases'] if c['id']=='M4-adjudicator-courier-valid-control'))
    uid=courier['ctx']['selfUid']
    witness={'witnessSchema':1,'projectKeyDigest':L.project_key_digest(gj['projectKey']), 'grantGeneration':1,'seq':0,'state':'COMMITTED','bodySha256':None}
    policy=json.loads(rb('security-fixtures.v7/permission-policy.effective.example.json'))
    env=json.loads(rb('security-fixtures.v7/typescript-analyzer.envelope.json'))
    stored=rb('security-fixtures.v7/typescript-analyzer.manifest.json')
    admitted,errs=L.admit_root_document(root)
    assert admitted is not None and not errs
    inputs={
        'policy':{'global':policy['global'],'project':policy['project']},
        'envelope':env,
        'root':root,
        'witness':{'witness':witness,'generation':1,'terminal':False,'projectKey':gj['projectKey']},
        'request':request,
        'result':{'ref':courier['resultRef'],'ctx':courier['ctx']},
        'stage':{'stat':{'type':'regular','nlink':1,'uid':uid,'size':5},'uid':uid,'cap':16},
        'recovery':{'class':'REVERSIBLE','records':['RA','RCI'],'footprint':'absent'},
    }
    calls={
        'policy':lambda x:not L.merge_policy(x['global'],x['project'])[1],
        'envelope':lambda x:L.verify_envelope(stored,x,admitted,'manifest','opensip')[0]=='VERIFIED',
        'root':lambda x:L.admit_root_document(x)[0] is not None,
        'witness':lambda x:L.reconcile_witness(None,x['witness'],x['projectKey'],x['generation'],x['terminal'])[0]=='OK',
        'request':lambda x:L.verify_effect_request(x['body'],x['ctx']) is None,
        'result':lambda x:L.resolve_result(x['ref'],lambda _:b'probe',x['ctx'])[0]=='OK',
        'stage':lambda x:L.stage_file_admission(x['stat'],x['uid'],x['cap']) is None,
        'recovery':lambda x:L.he1_recover(x['class'],x['records'],x['footprint'])[0]!='QUARANTINE',
    }
    def check(name,fn,want):
        try:got=fn();rec('boundary.'+name,got is want,repr(got))
        except Exception as e:rec('boundary.'+name,False,'UNCAUGHT '+type(e).__name__)
    def paths(v, path=()):
        yield path,v
        if isinstance(v,dict):
            for k,x in v.items():yield from paths(x,path+(k,))
        elif isinstance(v,list):
            for k,x in enumerate(v):yield from paths(x,path+(k,))
    def replace(base,path,value):
        v=deepcopy(base)
        if not path:return value
        at=v
        for k in path[:-1]:at=at[k]
        at[path[-1]]=deepcopy(value)
        return v
    for kind,base in inputs.items():
        call=calls[kind];check(kind+'.positive-control',lambda:call(deepcopy(base)),True)
        for path,value in paths(base):
            # Synthetic argument wrappers are not actual consumed records.
            if not path and kind not in ('root','envelope'):continue
            # Opaque projectKey bytes are allowed non-NFC; wrong type still refuses.
            label=kind+'.'+'.'.join(map(str,path))
            mutant = 1.0 if isinstance(value,(int,bool)) else ('not-an-array' if isinstance(value,list) else (['wrong-type'] if isinstance(value,str) else ('not-an-object' if isinstance(value,dict) else {})))
            changed=replace(base,path,mutant)
            check(label+'.wrong-type',lambda v=changed:call(v),False)
            if type(value) is int:
                changed=replace(base,path,True)
                check(label+'.bool-for-int',lambda v=changed:call(v),False)
            if isinstance(value,dict):
                # root namespace grants are dynamic dictionaries; insert an
                # invalid value there via wrong-type rather than assert closed.
                dynamic = kind=='root' and path==('namespaces',)
                if not dynamic:
                    changed=replace(base,path,dict(value,unexpectedMember=True))
                    check(label+'.unknown-key',lambda v=changed:call(v),False)
    # Exact second failed-confirmation probes, original IDs retained.
    bad=deepcopy(root);bad['keys'][0]['label']='e\u0301'
    check('M1-noncanonical-label-admission',lambda:L.admit_root_document(bad)[0] is not None,False)
    w=deepcopy(witness);w['witnessSchema']=1.0
    check('M3-float-witness-version',lambda:L.reconcile_witness(None,w,gj['projectKey'],1)[0]=='OK',False)
    q=deepcopy(request);q['ctx']['snapshotMembers']=['s/file.ts']
    for e in q['ctx']['connectionMap'].values():
        if e['effectClass']=='HE-2':e['target']['memberPath']='s/file.ts'
    for g in q['ctx']['journalState'].values():
        if 'pathPrefixes'in g['scope']:g['scope']['pathPrefixes']='src'
    check('M4-string-path-prefixes-grants-characters',lambda:L.verify_effect_request(q['body'],q['ctx']) is None,False)
    q=deepcopy(courier['ctx']);q['effectResult']['unexpectedMember']=True
    reads=[]
    result=L.resolve_result(courier['resultRef'],lambda rid:reads.append(rid) or b'probe',q)
    rec('boundary.M4-result-unknown-member',result[0]!='OK' and result[1] is None and not reads,repr(result))
    for cid,cc,fp in [('M5-invalid-class','BROKEN','absent'),('M5-invalid-footprint','REVERSIBLE','BROKEN')]:
        check(cid,lambda cc=cc,fp=fp:L.he1_recover(cc,['RA','RCI'],fp)[0]!='QUARANTINE',False)
    # Required-field deletion is checked at actual closed boundaries. Optional
    # fields remain optional, with positive absence controls, never made required.
    for kind,path,required in [
        ('root',(),['rootSchema','rootVersion','issuedAt','expiresAt','keys','roles','recoveryAuthority','namespaces','kernelAttestationKeys','previousRootVersion']),
        ('witness',('witness',),list(witness)),
        ('request',('body',),list(first['body'])),
        ('request',('ctx',),list(request['ctx'])),
        ('request',('ctx','currentBinding'),list(first['currentBinding'])),
        ('result',('ctx',),list(courier['ctx'])),
        ('result',('ctx','effectResult'),['requestSeq','decisionSeq','outcomeSeq','commitClass','effectOutcome']),
        ('stage',('stat',),['type','nlink','uid','size'])]:
        at=inputs[kind]
        for k in path:at=at[k]
        for key in required:
            if key not in at:continue
            mutated=deepcopy(at);del mutated[key]
            changed=replace(inputs[kind],path,mutated)
            check(kind+'.missing.'+'.'.join(map(str,path+(key,))),lambda v=changed,k=kind:calls[k](v),False)
    # Required five-member wire body, optional resultRef independently permitted.
    er=deepcopy(courier['ctx']['effectResult']);er.pop('resultRef')
    check('effect-result-optional-ref-absent',lambda:L.valid_effect_result(er),True)
    # Every actual body is also checked through the frozen control schema.
    wire=json.loads(rb('control-completion.schema.v3.json'))['oneOf'][13]['properties']['body']
    L.validate(courier['ctx']['effectResult'],wire)
    rec('boundary.effect-result-full-wire-control',True,'actual frozen wire shape')
    # Recovery composition: RA without intent cannot append an outcome lacking
    # that intent. Revoke the dead operation first, then close CLN not-begun.
    for cc in ('REVERSIBLE','IRREVERSIBLE'):
        a,r,o=L.he1_recover(cc,['RA'],'absent')
        a2,r2,o2=L.he1_recover(cc,['RA','REV'],'absent')
        rec('boundary.recovery.no-intent-composition.'+cc,(a,r,o)==('REVOKE-FIRST',('REV','process-death'),'PENDING') and (a2,r2,o2)==('APPEND',('CLN','not-begun'),'FAILED'))
    doc=rb('security-completion.v7.md').decode()
    rec('boundary.M5-no-retired-outcome-prose','or `REVERTED` for a reverted' not in doc)
    rec('boundary.M5-no-carried-receipt-prose','commit id carried on the RCO' not in doc)

    # Exact LEAD-CORRECTION-REVIEW 1 findings, with independently scoped controls.
    ef=deepcopy(env);ef['envelopeSchema']=2.0
    check('SEC6-LR1-M1-envelope-float',lambda:L.verify_envelope(stored,ef,admitted,'manifest','opensip')[0]=='VERIFIED',False)
    sid=first['currentBinding']['stableId']
    def pol(layer,scope):
        return {'policySchema':1,'policyScope':layer,'grants':[{'stableId':sid,'token':'PT-FS-WRITE-HOST-STATE','scope':scope}], 'denies':[], 'consents':[]}
    global_empty,project_class=pol('global',{}),pol('project',{'stateClass':'SC-OPS'})
    eff,err=L.merge_policy(global_empty,project_class)
    rec('boundary.SEC6-LR1-M2-state-class-creation',bool(err) and eff['grants']==[],str(err))
    # The downstream grant projection cannot be populated from refused merge output.
    rec('boundary.SEC6-LR1-M2-no-derived-grant',not any(g['token']=='PT-FS-WRITE-HOST-STATE' for g in eff['grants']))
    eff,err=L.merge_policy(pol('global',{'stateClass':'SC-OPS'}),project_class)
    rec('boundary.policy-equal-state-class-control',not err and eff['grants'][0]['scope']=={'stateClass':'SC-OPS'})
    eff,err=L.merge_policy(pol('global',{'stateClass':'SC-OPS'}),pol('project',{}))
    rec('boundary.policy-project-omission-inherits-control',not err and eff['grants'][0]['scope']=={'stateClass':'SC-OPS'})
    # Named peer-review probes: string prefixes, unknown grant/deny/scope,
    # float IDs/version, and nonobject source all refuse without exceptions.
    pg=deepcopy(policy['global']);pp=deepcopy(policy['project'])
    pg['grants'][0]['scope']['pathPrefixes']='src';pp['grants'][0]['scope']['pathPrefixes']=['s/file.ts']
    check('peer.policy-string-prefix-characters',lambda:not L.merge_policy(pg,pp)[1],False)
    for field in ('policySchema','stableId'):
        pg=deepcopy(policy['global'])
        if field=='policySchema':pg[field]=1.0
        else:pg['grants'][0][field]=1.0
        check('peer.policy-float-'+field,lambda pg=pg:not L.merge_policy(pg,policy['project'])[1],False)
    for bad in (None,[],True,1,'bad'):
        check('peer.policy-nonobject-'+repr(bad),lambda b=bad:not L.merge_policy(b,None)[1],False)
    eff,err=L.effective_policy_for_operation(None,None,True)
    rec('boundary.policy-both-files-absent-denies',not err and eff['grants']==[] and eff['sources']['global'] is not None and eff['sources']['project'] is not None)
    eff,err=L.effective_policy_for_operation(None,None,False)
    rec('boundary.policy-global-file-absent-core-denies',not err and eff['grants']==[] and eff['sources']['project'] is None)
    doc=rb('security-completion.v7.md').decode()
    rec('boundary.SEC6-LR1-S1-exact-context-spelling','scratchDirStat' not in doc and 'fileStat' not in doc and '{effectResult, expectedRequestSeq, scratchDirSt, selfUid, fileSt,' in doc)
    # Required raw-policy and envelope fields; unknown members already swept above.
    for kind,base,required in [('envelope',env,['envelopeSchema','subject','role','namespace','signatures']),('policy-global',policy['global'],['policySchema','policyScope','grants','denies','consents'])]:
        for key in required:
            bad=deepcopy(base);bad.pop(key,None)
            if kind=='envelope':fn=lambda b=bad:L.verify_envelope(stored,b,admitted,'manifest','opensip')[0]=='VERIFIED'
            else:fn=lambda b=bad:not L.merge_policy(b,policy['project'])[1]
            check(kind+'.missing-'+key,fn,False)

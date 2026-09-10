"""Reference design evidence; never a product runtime or OS qualification harness."""
import copy, hashlib, itertools, json, re
TOKENS = ('PT-FS-READ-PROJECT','PT-FS-READ-COMPONENT','PT-FS-WRITE-HOST-STATE','PT-PROC-EXEC-DECLARED','PT-NET-EGRESS','PT-ENV-READ','PT-HOST-EFFECT-BROKERED')
STATUSES=('PASS','FAIL','UNDETERMINED','NOT-APPLICABLE','CONSENT-REQUIRED')
STATES=('ST-UNBOOTSTRAPPED','ST-TRUSTED','ST-EXPIRED','ST-STALE-REVOCATION','ST-QUORUM-LOST','ST-RECOVERY','ST-REVOKED')
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def permission(x):
 t=x['token']; pr=None
 if t not in TOKENS: pr='PR-3'
 elif t not in x['declared']: pr='PR-1'
 elif t in x['denied']: pr='PR-2'
 elif x.get('revoked'): pr='PR-5'
 elif x.get('requiresConfinement') and t!='PT-ENV-READ': pr='PR-6'
 elif not x.get('scopeMatches',True): pr='PR-4'
 elif x.get('consentRequired') and not x.get('consent'): pr='PR-7'
 elif x.get('exclusiveHeld'): pr='PR-9'
 return {'decision':pr or 'GRANTED','wire':None if x.get('admission') or not pr else 'RF-6','promptAttempts':0,'hostIntentCount':0 if pr else 1,'enforcement':'ENFORCED-BY-CONSTRUCTION' if t=='PT-ENV-READ' else 'ENFORCED-AT-HOST-BROKER' if t=='PT-HOST-EFFECT-BROKERED' else 'DISCLOSURE-ONLY'}
def journal(x):
 # A supplied writer schedule, not incoming message times, defines this reference order.
 durable=[]; volatile=None; initiated=[]; inverse=[]; inverseAttempts=[]; outcomes={}; refusals=[]; revoked=False; revoked_at=None; cln=False; duplicate=0
 def append(typ,req=None,value=None):
  r={'seq':len(durable)+1,'type':typ}
  if req is not None:r['request']=req
  if value is not None:r['value']=value
  durable.append(r)
 def invert(req):
  inverseAttempts.append(req)
  if req not in inverse:inverse.append(req)
 def apply(r):
  nonlocal revoked,revoked_at,cln,duplicate
  typ=r['type']; req=r.get('request')
  if typ in ('REV','EXPIRY'):
   if revoked: duplicate+=1
   else: revoked=True;revoked_at=r['seq']
  if typ=='CLN':cln=True
  if typ in ('RCO','ICO'):outcomes[req]=r.get('value')
 for a in x['schedule']:
  op=a['op']
  if op=='WRITE':
   typ=a['type'];req=a.get('request')
   if revoked and typ in ('RA','RCI','ICI'):
    refusals.append({'request':req,'decision':'PR-8' if typ=='ICI' else 'PR-5'});continue
   if typ=='CLN' and cln:continue
   if typ=='CLN':
    for prior in durable:
     if prior['type']=='RCI':invert(prior['request'])
   volatile={k:v for k,v in a.items() if k in ('type','request','value')}
  elif op=='SYNC':
   if volatile:
    append(**{'typ':volatile['type'],'req':volatile.get('request'),'value':volatile.get('value')});apply(durable[-1]);volatile=None
  elif op=='EFFECT':
   req=a['request']
   if any(r.get('request')==req and r['type'] in ('RCI','ICI') for r in durable): initiated.append(req)
   else: refusals.append({'request':req,'decision':'NO-DURABLE-INTENT'})
  elif op=='CRASH':
   volatile=None; recovered_inverse=set()
   # Recovery uses durable bytes only; no retry of external effects.
   for r in list(durable):
    req=r.get('request')
    if r['type']=='ICI' and req not in outcomes:
     append('ICO',req,'INDETERMINATE');outcomes[req]='INDETERMINATE'
     if not revoked:append('REV');apply(durable[-1])
    elif r['type']=='RCI' and req not in outcomes:
     invert(req);recovered_inverse.add(req);append('RCO',req,'CLEANED');outcomes[req]='CLEANED'
    elif r['type']=='RA' and not any(z.get('request')==req and z['type'] in ('RCI','ICI') for z in durable):outcomes[req]='CANCELED-BY-RECOVERY'
   if revoked and not cln:
    for r in durable:
     if r['type']=='RCI' and r.get('request') not in recovered_inverse:invert(r['request'])
    append('CLN',value='BOUND-EXHAUSTED' if x.get('cleanupFails') else 'CLOSED');apply(durable[-1])
  elif op=='CLEANUP':
   if revoked and not cln:
    for r in durable:
     if r['type']=='RCI':invert(r['request'])
    append('CLN',value='BOUND-EXHAUSTED' if x.get('cleanupFails') else 'CLOSED');apply(durable[-1])
  else: raise ValueError(op)
 return {'journal':durable,'initiated':initiated,'inverse':inverse,'inverseAttempts':inverseAttempts,'outcomes':outcomes,'refusals':refusals,'revoked':revoked,'revokedAt':revoked_at,'cleanupClosed':cln,'duplicateRevocations':duplicate,'retryCount':0}
def wording(x):
 v=x['outcome']+'-BEFORE-REVOCATION'
 return {'machine':{'effectOutcome':x['outcome'],'ordering':v},'human':v+'\n','audit':{'ordering':v,'effectOutcome':x['outcome']}}
def environment(x): return {k:v for k,v in x['host'].items() if k in x['granted'] or k in x['structural']}
def actor(x):
 if x['actor']=='component':return {'authority':'DR-105','token':x.get('token'),'hostConsentGrant':False}
 if x['actor']=='customer-tool':return {'authority':'CUSTOMER-TOOL-TAIL','admitted':False,'ridesOn':'DR-119 + later D-000 product admission'}
 if x.get('permissionRef') is not None:return {'authority':'HOST','decision':'DENIED','reason':'RESERVED-FIELD'}
 a=x['action'];s=x.get('subtype'); reason=None
 if a in ('DEFAULT-READ','OPMETA-WRITE'):
  return {'authority':'HOST-DEFAULT','decision':'DENIED' if x.get('hostClassDenied') else 'GRANTED','grantJournalWritten':False}
 if a not in ('CA-1','CA-2','CA-3','CA-4'):reason='UNNAMED-ACT'
 elif not x.get('contract'):reason='CONTRACT-NOT-RECORDED'
 elif a=='CA-2':reason='CA2-PREVIEW-EXCLUDED'
 elif a=='CA-1' and s!='SPAWN':reason='INPROCESS-PREVIEW-EXCLUDED'
 elif a=='CA-3' and s!='OUT_OF_ROOT_READ':reason='SUBTYPE-NOT-ADMITTED'
 elif a=='CA-4' and s!='PATH-TRUST-STATE-REFRESH':reason='SUBTYPE-NOT-ADMITTED'
 elif not x.get('admission'):reason='PRODUCT-NOT-ADMITTED'
 elif not x.get('consent'):reason='CONSENT-REQUIRED'
 elif x.get('actual')!=x.get('bound'):reason='BINDING-MISMATCH'
 elif any(c in json.dumps(x.get('bound')) for c in ('*','?')):reason='WILDCARD-SCOPE'
 return {'authority':'HOST','decision':'DENIED' if reason else 'GRANTED','reason':reason,'grantJournalWritten':False,'promptAttempts':0}
def host_outcome(x):
 if not x['survivingWriter']:return {'standing':'UNEMITTED-CRASH'}
 if x['boundary']=='before':v='DEFINITELY_NOT_PERFORMED'
 elif x['knownCompleted']:v='COMPLETED'
 else:v='INDETERMINATE'
 return {'effectOutcome':v}
def outcome(x):
 if x.get('fault'):return 'OC-5'
 if x.get('refused'):return 'OC-4'
 if any(s not in STATUSES for s in x['statuses']):return 'REFUSE-SCHEMA'
 if 'FAIL' in x['statuses']:return 'OC-2'
 if any(s in ('UNDETERMINED','CONSENT-REQUIRED') for s in x['statuses']):return 'OC-3'
 return 'OC-1'
def mode(x):
 m='project' if x.get('explicit')=='project' or x.get('explicit') is None and x['present'] else 'core'
 return {'mode':m,'projectStatus':'NOT-APPLICABLE' if m=='core' else 'PASS' if x['resolvable'] else 'UNDETERMINED'}
def redact(x):
 # Tier 1 ignores classified values completely, including hashes/previews.
 text=x['diagnostic'];text=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text);text=''.join(c for c in text if ord(c)>=32)
 text=re.sub(r'(https?://)[^/@\s]+:[^/@\s]+@',r'\1[REDACTED]@',text)
 text=re.sub(r'(?i)Bearer\s+[A-Za-z0-9._~+/-]+','Bearer [REDACTED]',text)
 text=re.sub(r'(?i)\b(password|token|secret|api_key)=[^\s]+',r'\1=[REDACTED]',text)
 if len(text.encode())>1024:
  text=text.encode()[:1008].decode('utf-8','ignore')+'[TRUNCATED]'
 return {'secret':'[REDACTED]','credentialPresent':x['credentialPresent'],'project':'<PROJECT>','diagnostic':text,'tier2Limitation':'Known-shape scrubbing only; unknown credentials can remain visible.'}
def continuation(x):
 c,i,p=x['states']
 if c!='ST-TRUSTED':return {'alreadyRunning':False,'newProcess':False,'reason':'CONTINUE-CORE-NOT-TRUSTED'}
 if i not in ('ST-TRUSTED','ST-EXPIRED','ST-STALE-REVOCATION'):return {'alreadyRunning':False,'newProcess':False,'reason':'CONTINUE-INDEX-NOT-TRUSTED'}
 if p!='ST-TRUSTED':return {'alreadyRunning':False,'newProcess':False,'reason':'CONTINUE-COMPONENT-NOT-TRUSTED'}
 return {'alreadyRunning':True,'newProcess':i=='ST-TRUSTED','reason':None}
def trust(x):
 state=x['state'];event=x['event'];to=state;reason=None;extra={};accepted=True
 if event=='CLOCK':
  if state in ('ST-TRUSTED','ST-STALE-REVOCATION') and x['eval']>=x['expires']:to='ST-EXPIRED'
  elif state=='ST-TRUSTED' and x['eval']-x['revocationIssued']>90*86400:to='ST-STALE-REVOCATION'
 elif event=='REVOKE':
  if state!='ST-UNBOOTSTRAPPED' and x['newCounter']>x['oldCounter'] and x['valid']:to='ST-REVOKED'
  else:reason='REVOKE-NOT-NEWER-OR-INVALID'
 elif event=='INSTALL':
  if state!='ST-TRUSTED':reason='INSTALL-NOT-TRUSTED'
  elif not x['active']:reason='ENVELOPE-INACTIVE'
  elif not x['valid']:reason='INSTALL-NOT-TRUSTED'
 elif event=='PRESENT':
  if x['kind']=='recovery':
   if state not in ('ST-EXPIRED','ST-STALE-REVOCATION','ST-QUORUM-LOST','ST-REVOKED','ST-UNBOOTSTRAPPED','ST-RECOVERY') or not x['complete']:reason='PAYLOAD-NOT-ADMISSIBLE'
  elif state in ('ST-RECOVERY','ST-REVOKED'):reason='PAYLOAD-NOT-ADMISSIBLE'
  elif not x['active']:reason='ENVELOPE-INACTIVE'
  elif not x['valid'] or not x['complete']:reason='PAYLOAD-NOT-ADMISSIBLE'
  else:to='ST-TRUSTED'
 elif event=='RECOVER-BEGIN':
  if state not in ('ST-EXPIRED','ST-STALE-REVOCATION','ST-QUORUM-LOST','ST-REVOKED','ST-UNBOOTSTRAPPED') or not x['complete']:reason='RECOVERY-BEGIN-REFUSED'
  else:to='ST-RECOVERY'
 elif event=='RECOVER-COMMIT':
  if state!='ST-RECOVERY':reason='RECOVERY-COMMIT-REFUSED'
  elif not x['active']:reason='ENVELOPE-INACTIVE'
  elif not (x['valid'] and len(set(x['authorizedSigners']))>=3 and x['rootBinding'] and x['oldRootNamed']):reason='RECOVERY-COMMIT-REFUSED'
  else:to='ST-TRUSTED';extra['countersAdvance']=True
 elif event=='RECOVER-ABORT':
  if state!='ST-RECOVERY':reason='RECOVERY-ABORT-NOT-IN-CEREMONY'
  else:
   to=next((s for s in ('ST-REVOKED','ST-QUORUM-LOST','ST-EXPIRED','ST-STALE-REVOCATION') if s in x['stillTrue']),'ST-UNBOOTSTRAPPED');extra['ceremonyTermination']='RECOVERY-ABORTED'
 elif event=='QUORUM':
  if state not in ('ST-REVOKED','ST-UNBOOTSTRAPPED') and x['signers']<2:to='ST-QUORUM-LOST'
 else:reason='NO-MATCHING-GUARD'
 out={'from':state,'to':to,'outcome':'refused' if reason else 'accepted',**extra}
 if reason:out['refusalReason']=reason
 return out

def policy_numbers(x):
 if x['kind']=='time':
  high=x['highwater']; decisions=[]
  for now in x['observations']:
   high=max(now,high);decisions.append('EXPIRED' if high>=x['expires'] else 'FUTURE' if x['issued']>high+86400 else 'FRESH')
  return {'highwater':high,'decisions':decisions}
 if x['kind']=='restore':return {'admission':'REFUSED' if x['restoreDetected'] or not x['anchorMatches'] else 'ALLOWED','networkFallback':False}
 if x['kind']=='waiver':return {'allowed':x['days']<=30 and x['renewals']<=1 and x['product'] and x['release'] and not x['semanticOrTrustBlocker']}
 if x['kind']=='threshold':return {'accepted':len(set(x['validAuthorizedSigners']))>=(3 if x['role']=='RECOVERY' else 2)}
 raise ValueError(x)
MODELS={'permission':permission,'journal':journal,'wording':wording,'environment':environment,'actor':actor,'host-outcome':host_outcome,'doctor-outcome':outcome,'mode':mode,'redact':redact,'continuation':continuation,'trust':trust,'policy-numbers':policy_numbers}
def run(case): return MODELS[case['model']](case['input'])

AR_KEYS={'id','actor','actionClass','actionSubtype','componentGenerationIdentity','admittedManifestDigest','designContractRef','invocationId','checkIds','resourceScope','toolIdentity','endpointSet','platform','consentCarrier','policyProvenance','productAdmissionRefs','resolution','owners','auditIdentity'}
SCOPE_KEYS={'actor','actionSubtype','invocation','checks','resources','targetIdentity','observationDeadline','byteCap','endpointSet','platform','policyProvenance','designContractRef','productAdmissionRefs','owners','auditIdentity'}
SUBTYPES={'CA-1':['SPAWN','IN_PROCESS'],'CA-2':[None],'CA-3':['OUT_OF_ROOT_READ','LOCAL_SOCKET_OR_PIPE','KEYCHAIN','PRIVILEGED_PLATFORM_FACILITY'],'CA-4':['PATH-TRUST-STATE-REFRESH','PATH-INDEX-REACH','PATH-DECLARED-EXTERNAL-SERVICE']}
def uint(n):return type(n) is int and 0<=n<=2**53-1
def hex64(s):return isinstance(s,str) and re.fullmatch('[0-9a-f]{64}',s) is not None
def source_ref(s):return isinstance(s,dict) and set(s)=={'authority','artifactPath','selector','digest'} and hex64(s['digest']) and all(isinstance(v,str) and 0<len(v.encode())<=512 for v in s.values())
def _host_projection_validate(x):
 ar=x['authorization'];cr=x['consent'];sc=cr.get('scope',{});action=cr.get('actionClass');errors=[]
 def need(test,label):
  if not test:errors.append(label)
 need(set(ar)==AR_KEYS,'authorization-closed-19');need(set(sc)==SCOPE_KEYS,'scope-closed-15')
 if errors:return {'accepted':False,'errors':errors}
 translation={'CA-1-HOST-HEAD':'CA-1','CA-2':'CA-2','CA-3':'CA-3','CA-4-HOST':'CA-4'}
 need(action in SUBTYPES and sc['actionSubtype'] in SUBTYPES.get(action,[]),'subtype-class')
 need(translation.get(ar['actionClass'])==action,'class-projection')
 need(ar['actor']=='HOST-UNDER-INSTRUCTION','actor')
 need(all(isinstance(ar[k],str) and 0<len(ar[k].encode())<=4096 for k in ('id','invocationId','auditIdentity')),'local-identifiers')
 need(ar['owners']==['Operability+security','Security+platform'],'joint-owners')
 need(all(isinstance(ar[k],list) and all(isinstance(v,str) and 0<len(v.encode())<=4096 for v in ar[k]) for k in ('checkIds','resourceScope')),'enumeration-shape')
 need(ar['admittedManifestDigest'] is None or hex64(ar['admittedManifestDigest']),'manifest-digest')
 need(ar['resolution'] in ('GRANTED','DENIED'),'resolution')
 need(ar['designContractRef']==x['recordedContext']['contract'],'recorded-contract-ref')
 need(ar['productAdmissionRefs']==x['recordedContext']['admissions'],'recorded-admission-refs')
 need(ar['platform'] in ('macos-arm64','macos-x86_64','linux-arm64','linux-x86_64'),'platform')
 for af,sf in [('actor','actor'),('actionSubtype','actionSubtype'),('invocationId','invocation'),('checkIds','checks'),('resourceScope','resources'),('endpointSet','endpointSet'),('platform','platform'),('policyProvenance','policyProvenance'),('designContractRef','designContractRef'),('productAdmissionRefs','productAdmissionRefs'),('owners','owners'),('auditIdentity','auditIdentity')]:need(ar[af]==sc[sf],'projection-'+af)
 need(cr.get('id')==ar['id'],'record-id');need(cr.get('authorization')==ar['resolution'].lower(),'resolution-projection')
 pol=ar['policyProvenance'];carrier=ar['consentCarrier']
 need((carrier=='invocation-time-naming' and pol is None) or (carrier=='pre-existing-policy' and source_ref(pol)),'policy-carrier')
 dc=ar['designContractRef'];need(isinstance(dc,dict) and set(dc)=={'path','version','sha256'} and hex64(dc['sha256']),'contract-ref')
 refs=ar['productAdmissionRefs'];need(isinstance(refs,list) and all(isinstance(r,dict) and set(r)=={'authority','artifactPath','selector','digest','standing','scope'} and hex64(r['digest']) for r in refs),'admission-refs')
 if ar['resolution']=='GRANTED':need(bool(refs),'admission-required')
 for key in ('resourceScope','endpointSet','toolIdentity','checkIds'):
  need(not any(k in json.dumps(ar[key]) for k in ('*','?')),'wildcard-'+key)
 deadline=sc['observationDeadline'];need(isinstance(deadline,dict) and set(deadline)=={'kind','value','unit','clockRule'} and deadline.get('kind')=='DURATION-FROM-INVOCATION-START' and uint(deadline.get('value')) and deadline.get('unit')=='milliseconds' and deadline.get('clockRule')=='OBSERVATION-ONLY','deadline')
 cap=sc['byteCap'];target=sc['targetIdentity']
 if action in ('CA-1','CA-2'):
  need(isinstance(cap,dict) and set(cap)=={'acceptFromTarget'} and uint(cap['acceptFromTarget']),'byte-cap')
  want={'generation':ar['componentGenerationIdentity'],'admittedManifestDigest':ar['admittedManifestDigest']} if action=='CA-1' else {'toolIdentity':ar['toolIdentity']}
  need(target==want and all(v is not None for v in want.values()),'target')
 elif action=='CA-3':need(cap is None and target is None,'ca3-null-bounds')
 elif action=='CA-4':need(target is None and isinstance(cap,dict) and set(cap)=={'send','receive'} and all(uint(v) for v in cap.values()) and bool(sc['endpointSet']),'ca4-bounds')
 need(cr.get('effectOutcome') in ('COMPLETED','DEFINITELY_NOT_PERFORMED','INDETERMINATE'),'effect-outcome')
 need(cr.get('permissionRef')=={'reserved':True,'ridesOn':['DR-105']},'permission-ref-reserved')
 need(cr.get('execution') in ('enforced','disclosed-trusted-code','refused'),'execution')
 if cr.get('effectOutcome')=='INDETERMINATE':need(cr.get('execution')!='refused','unknown-not-refused')
 need(isinstance(cr.get('residualLimitation'),dict),'residual')
 obs=x.get('observation',{})
 if action=='CA-4' and 'sendHex' in obs:
  need(cr.get('bytes')=={'send':len(bytes.fromhex(obs['sendHex'])),'receive':len(bytes.fromhex(obs['receiveHex']))},'observed-byte-counts')
  need(cr.get('endpoint')==obs['endpoints'],'observed-endpoint')
 elif action=='CA-1' and 'acceptHex' in obs:need(cr.get('bytes')=={'acceptFromTarget':len(bytes.fromhex(obs['acceptHex']))},'observed-byte-counts')
 return {'accepted':not errors,'errors':errors}

def doctor_observe(x):
 # Synthetic source images are retained bytes, read without locks/leases or mutation.
 source=x['source'];after=x.get('sourceAfter',source);status='PASS';cause=None;observed={}
 if after!=source:status='UNDETERMINED';cause='source-changed-under-observation'
 elif x.get('timeUnestablished'):status='UNDETERMINED';cause='observation-bounded';observed={'issuedAt':x['issuedAt'],'expiresAt':x['expiresAt']}
 elif x['kind']=='lock':
  try:
   pairs=[]
   def pairs_hook(ps):
    out={}
    for k,v in ps:
     if k in out:raise ValueError('duplicate-key:'+k)
     out[k]=v
    return out
   obj=json.loads(source,object_pairs_hook=pairs_hook)
   observed={'selectionCount':len(obj.get('components',[]))}
   if x.get('missingComponent'):status='FAIL';cause='dependency-absent'
  except (ValueError,TypeError) as e:status='UNDETERMINED';cause=str(e).split(':')[0];observed={'diagnostic':'duplicate-key:components' if 'duplicate-key' in str(e) else 'document-unreadable'}
 elif x['kind']=='inventory':
  observed={'expected':x['expectedDigest'],'actual':hashlib.sha256(source.encode()).hexdigest()}
  if observed['expected']!=observed['actual']:status='FAIL'
 elif x['kind']=='revocation':
  observed={'revoked':x['revoked']};status='FAIL' if x['revoked'] else 'PASS'
 elif x['kind']=='migration':
  observed={'phase':source};status='UNDETERMINED' if source=='AMBIGUOUS' else 'PASS';cause='observation-bounded' if status=='UNDETERMINED' else None
 return {'status':status,'cause':cause,'observed':observed,'sourceAfter':after,'writes':[],'locks':[],'network':[],'exec':[]}

def remediation(x):
 if not x['active']:return {'decision':'RESERVED_FIELD_POPULATED'}
 closed=x['daysElapsed']>=90 and x['minorCycles']>=1
 cls='WINDOW-CLOSED-ACTION-REQUIRED' if closed and x['referenced'] else 'UPDATE-PIN' if x['referenced'] else 'WINDOW-OPEN-NO-ACTION-REQUIRED'
 return {'remediationClass':cls,'appliedBy':'operator','windowState':x['recordedWindow'],'mutations':[]}
MODELS.update({'doctor-observe':doctor_observe,'remediation':remediation})

def airgap(x):
 payload=x['payload'];required={'rootChain','index','revocation','expiry','manifests','payloads','permissions','repairMaterial'}
 missing=sorted(required-payload.keys())
 absence=payload.get('repairMaterial')=={'absent':True,'ridesOn':'DR-110','stage':'REENTRY-REQUIRED'}
 valid=not missing and absence and x['authenticated'] and x['roleBinding'] and x['namespaceAuthorized'] and x['antiRollback'] and x['envelopeMatches']
 return {'accepted':valid,'missing':missing,'network':[],'refresh':[],'lockMutation':False,'repairExecutable':False}
def grant_binding(x):
 required={'requestAttempt','component','installGenerationId','manifestDigest','processInstance','operation','grantGeneration','grant','project','scope','expiry'}
 records=x['records'];ok=bool(records)
 for r in records:
  if set(r.get('binding',{}))!=required or r['binding']!=x['binding']:ok=False
 if [r['type'] for r in records]!=['REQUESTED','GRANT','RA','RCI','RCO','AUD']:ok=False
 return {'accepted':ok,'authoritativeIdentityMinted':False}
def typed_absence(x):return {'standing':'REENTRY-REQUIRED','ridesOn':x['ridesOn'],'executionAllowed':False}
MODELS.update({'airgap':airgap,'grant-binding':grant_binding,'typed-absence':typed_absence})

# V2 composed validation: schemas are source-independent structural validators, followed
# by semantic rules. All malformed values produce refusal instead of escaping as exceptions.
from pathlib import Path
import jsonschema
_SCHEMA=json.loads(Path(__file__).with_name('security-behavior-doctor-schema.v3.json').read_text())
def max_utf8_bytes(validator,limit,instance,schema):
 if isinstance(instance,str):
  try:valid=len(instance.encode('utf-8'))<=limit
  except UnicodeError:valid=False
  if not valid:yield jsonschema.ValidationError('string exceeds declared UTF-8 byte cap')
_TypedValidator=jsonschema.validators.extend(jsonschema.Draft202012Validator,{'maxUtf8Bytes':max_utf8_bytes})
def bounded(value,key='',depth=0):
 if isinstance(value,(dict,list)):
  if depth>=32:return False
  if len(value)>4096:return False
  vals=value.items() if isinstance(value,dict) else enumerate(value)
  return all((not isinstance(k,str) or len(k.encode())<=128) and bounded(v,str(k),depth+1) for k,v in vals)
 if isinstance(value,str):
  cap=1024 if key in ('diagnostic','detail') else 128 if key in ('id','class','status','kind','cause','actor','actionClass','actionSubtype','invocationId','invocation','auditIdentity','installedGenerationRef') else 4096
  return len(value.encode('utf-8'))<=cap
 return value is None or type(value) in (bool,int,float)
def schema_ok(value,schema):
 try:return bounded(value) and not list(_TypedValidator(schema).iter_errors(value))
 except (ValueError,TypeError,UnicodeError,RecursionError):return False
_host_old=_host_projection_validate
def preview_excluded(action,subtype):
 return action=='CA-2' or (action=='CA-1' and subtype=='IN_PROCESS') or (action=='CA-3' and subtype!='OUT_OF_ROOT_READ') or (action=='CA-4' and subtype!='PATH-TRUST-STATE-REFRESH')
def host_record_valid(x):
 try:
  ar=x['authorization'];cr=x['consent']
  if not schema_ok(ar,_SCHEMA['$defs']['authorization']) or not schema_ok(cr,_SCHEMA['$defs']['consent']):return {'accepted':False,'errors':['record-schema']}
  action=cr['actionClass'];sub=cr['scope']['actionSubtype']
  # An authenticated context cannot grant an excluded preview act.
  context=x['recordedContext']; consent=x['invocationConsent']; actual=x['actualAttempt']; bound=x['boundAttempt']
  permitted=context.get('contractRecorded') is True and context.get('admissionActive') is True and bool(context.get('admissions')) and consent is True and actual==bound
  record_binding={'actor':ar['actor'],'class':action,'subtype':sub,'platform':ar['platform'],'generation':ar['componentGenerationIdentity'],'manifestDigest':ar['admittedManifestDigest'],'checks':ar['checkIds'],'resources':ar['resourceScope'],'toolIdentity':ar['toolIdentity'],'endpointSet':ar['endpointSet']}
  permitted=permitted and bound==record_binding
  permitted=permitted and action in context['admittedClasses'] and sub in context['admittedClasses'][action]
  permitted=permitted and not preview_excluded(action,sub)
  if ar['resolution']!=('GRANTED' if permitted else 'DENIED'):return {'accepted':False,'errors':['resolution-not-derived']}
  if action!='CA-1' and (ar['componentGenerationIdentity'] is not None or ar['admittedManifestDigest'] is not None):return {'accepted':False,'errors':['class-nullability']}
  if action!='CA-2' and ar['toolIdentity'] is not None:return {'accepted':False,'errors':['class-nullability']}
  if action!='CA-4' and ar['endpointSet'] is not None:return {'accepted':False,'errors':['class-nullability']}
  # A distinct doctor record id is legal only with an explicit AR-id cross-reference.
  yy=copy.deepcopy(x)
  if cr['id']!=ar['id']:
   if cr['residualLimitation'].get('authorizationRecordId')!=ar['id']:return {'accepted':False,'errors':['record-id-unbound']}
   yy['consent']['id']=ar['id']
  return _host_old(yy)
 except (ValueError,TypeError,KeyError,AttributeError,UnicodeError):return {'accepted':False,'errors':['malformed-record']}
def doctor_reader(x):
 try:
  r=x['report']; encoded=json.dumps(r,ensure_ascii=False,separators=(',',':')).encode('utf-8')
  if len(encoded)>16*1024*1024 or not schema_ok(r,_SCHEMA):return {'accepted':False,'outcome':None,'errors':['report-schema-or-bounds']}
  env=r['environment'];checks=r['checks'];statuses=[c['status'] for c in checks];events=x.get('events');errors=[]
  if env['mode']!=r['mode']:errors.append('mode-mismatch')
  for c in checks:
   if c['status'] in ('PASS','FAIL') and not c['evidence']:errors.append('verdict-without-evidence')
   if c['status'] in ('UNDETERMINED','CONSENT-REQUIRED') and c['residualLimitation'] is None:errors.append('limitation-required')
  for cr in r['consentRecords']:
   if cr['authorization']=='granted' and preview_excluded(cr['actionClass'],cr['scope']['actionSubtype']):errors.append('preview-excluded-grant')
   if cr['effectOutcome']=='INDETERMINATE' and cr['execution']=='refused':errors.append('unknown-not-refused')
  if r['outcome']=='OC-4' and checks:errors.append('refusal-has-check-results')
  if not checks and r['outcome'] not in ('OC-4','OC-5'):errors.append('empty-normal-report')
  if events is not None:
   if events.get('outputSinkFailed'):errors.append('no-emitted-report-after-output-failure')
   fault=events.get('constructionFailed',False) or events.get('requiredConsentWriteFailed',False)
   refused=events.get('invocationRefusedBeforeChecks',False)
   if refused and events['checksExecuted']!=0:errors.append('refusal-after-execution')
   derived=outcome({'statuses':statuses,'fault':fault,'refused':refused})
   if r['outcome']!=derived:errors.append('independent-outcome-mismatch')
   if fault and any(s in ('PASS','FAIL') for s in statuses):errors.append('fault-presented-environment-verdict')
  else:
   derived=r['outcome'] if r['outcome'] in ('OC-4','OC-5') else outcome({'statuses':statuses})
   if derived!=r['outcome']:errors.append('check-outcome-mismatch')
  if 'FAIL' in statuses and any(s in ('UNDETERMINED','CONSENT-REQUIRED') for s in statuses) and not r['residualLimitations']:errors.append('incomplete-fail-residual')
  return {'accepted':not errors,'outcome':derived if not errors else None,'errors':errors,'verification':'EXECUTION-EVENTS-AND-STRUCTURE' if events is not None else 'STRUCTURE-ONLY-OC4-OC5-EVENTS-UNVERIFIED'}
 except (TypeError,ValueError,KeyError,AttributeError,UnicodeError,RecursionError):return {'accepted':False,'outcome':None,'errors':['malformed-report']}
def doctor_execution(x):
 events=x['events']
 if events.get('outputSinkFailed') or events.get('constructionFailed'):return {'outcome':'OC-5','reportEmitted':False,'environmentVerdict':False}
 if events.get('invocationRefusedBeforeChecks') and events.get('checksExecuted')!=0:return {'accepted':False,'reason':'refusal-after-checks'}
 return {'outcome':outcome({'statuses':x['statuses'],'fault':events.get('requiredConsentWriteFailed',False),'refused':events.get('invocationRefusedBeforeChecks',False)}),'reportEmitted':True}
def bound_probe(x):
 v=x['value'];encoded=json.dumps(v,ensure_ascii=False,separators=(',',':')).encode()
 return {'accepted':len(encoded)<=16*1024*1024 and bounded(v),'encodedBytes':len(encoded)}
MODELS.update({'host-record':host_record_valid,'doctor-reader':doctor_reader,'doctor-execution':doctor_execution,'bound-probe':bound_probe})

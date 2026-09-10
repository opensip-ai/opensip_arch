"""Checkpoint-2: the COMPLETE public composition, instantiated and validated.
guard refusal -> normalization -> origin-aware termination -> schema-admitted failure envelope,
and the bounded availability collection on the original invocation. Schema admission only."""
import importlib.util,json,pathlib,sys
DC=pathlib.Path(sys.argv[1])
s=importlib.util.spec_from_file_location('f',DC/'integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
N,W=f.N,f.W
CM='workflows/schemas/common.schema.json';ENV='workflows/schemas/command-envelope.schema.json'
out={}
def adm(doc,sel,v):
    try:W.validate_import_record(doc,sel,v);return 'ADMIT'
    except Exception as e:
        c=e.__cause__;return 'REFUSE:'+(str(c).split('\n')[0] if c else str(e))[:90]
# --- REPRESENTATIVE guard-output STRINGS, colon-suffixed, driven through the whole chain.
# These are hand-written strings shaped like guard output; they are NOT produced by invoking a guard,
# so this file is a composition test only. p3_actual_guards.py invokes the actual guards.
raws=[('native.requested-capability-unregistered:made-up-capability','external-configuration'),
      ('native.requested-capability-unregistered:made-up-capability','externally-supplied-spec'),
      ('native.requested-capability-unregistered:made-up-capability','host-generated-internal-layer'),
      ('native.requested-capability-mode-unregistered:syntax:cobol-classic','external-configuration'),
      ('native.requested-capability-mode-not-selected:clones-cross-tsjs:rust-cargo',None),
      ('native.release-capability-unregistered:made-up',None),
      ('native.release-capability-duplicate:syntax',None),
      ('native.coverage-cause-not-for-deficiency:input-closure-incomplete:capability-missing',None),
      ('native.coverage-cause-required:input-closure-incomplete',None)]
rows=[]
for raw,origin in raws:
    key,subject=N.normalize_internal_key(raw)
    t=N.public_termination_for(raw,origin)
    errors=N.failure_envelope_errors(raw,origin)
    env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure',
         'requestId':'req1_'+'a'*32,'termination':t,'exitCode':W.EXIT[t['class']],'errors':errors}
    rows.append({'raw':raw,'origin':origin,'key':key,'subject':subject,
                 'class':t['class'],'errorCode':t['errorCode'],
                 'errorCodes':[e['code'] for e in errors],'errorSubjects':[e.get('subject') for e in errors],
                 'terminationAdmission':adm(CM,'#/$defs/StepTermination',t),
                 'envelopeAdmission':adm(ENV,'',env)})
out['failureChain']=rows
# --- the bounded availability collection over TWO units
units=[{'rootPath':p,'languageMode':'ts-tsconfig','languageFamily':'tsjs'} for p in ('apps/a','apps/b')]
sel=N.default_capability_selection(units,[])
avail=N.release_absence_notices(sel['undeclaredCapabilities'])
tuples={(n['capabilityId'],n['languageMode'],n['workspaceRoot']) for n in avail['notices']}
env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'run',
     'requestId':'req1_'+'b'*32,'projectId':'prj1-'+'a'*64,'termination':{'class':'success'},'exitCode':0,
     'run':{'kind':'analysis','authority':'authoritative','runId':'run2:'+'a'*64,'planId':'plan2:'+'b'*64,
            'verdict':'pass','requiredCoverage':'satisfied','durability':'committed','deficiency':'none',
            'secondaryDeficiencies':[]},
     'availability':avail}
out['availability']={'units':2,'inputRows':len(sel['undeclaredCapabilities']),
  'noticeCount':avail['noticeCount'],'notices':len(avail['notices']),
  'distinctOwnershipTuples':len(tuples),
  'countEqualsLength':avail['noticeCount']==len(avail['notices']),
  'orderIsSelectionOrder':[(n['capabilityId'],n['languageMode'],n['workspaceRoot']) for n in avail['notices']]==
    [(r['capabilityId'],r['languageMode'],r['workspaceRoot']) for r in sel['undeclaredCapabilities']],
  'noticeAdmission':sorted({adm(CM,'#/$defs/CapabilityAvailabilityNoticeV1',n) for n in avail['notices']}),
  'collectionAdmission':adm(CM,'#/$defs/CapabilityAvailabilityV1',avail),
  'envelopeWithAvailabilityAdmission':adm(ENV,'',env),
  'candidateOnlySample':[n for n in avail['notices'] if n['capabilityId']=='clones-near'],
  'boundEqualsRequestBound':json.loads((DC/'workflows/schemas/common.schema.json').read_text())
     ['$defs']['CapabilityAvailabilityV1']['properties']['notices']['maxItems']==1024}
# --- negatives
def neg(label,fn):
    try:fn();out.setdefault('negatives',[]).append({'case':label,'outcome':'ADMIT'})
    except Exception as e:out.setdefault('negatives',[]).append({'case':label,'outcome':'REFUSE','error':str(e)[:110]})
neg('an unregistered raw key normalizes to nothing',lambda:N.normalize_internal_key('native.made-up:x'))
neg('an unregistered raw key refuses through the whole chain',
    lambda:N.failure_envelope_errors('native.made-up:x','external-configuration'))
neg('a release key claimed as user configuration',
    lambda:N.failure_envelope_errors('native.release-capability-unregistered:x','external-configuration'))
neg('the advisory absence key is not a failure',
    lambda:N.failure_envelope_errors('native.release-capability-undeclared'))
print(json.dumps(out,indent=1))

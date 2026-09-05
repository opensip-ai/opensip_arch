#!/usr/bin/env python3
"""Design-only parser and property model. Never imports or executes OpenSIP runtime."""
import argparse, hashlib, io, json, struct, sys, unicodedata
from pathlib import Path
import cbor2
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
WIRE = json.loads((ROOT/'docs/coop/artifacts/delivery.v2.json').read_text())['typescriptSemanticSubstrate']['providerProtocol']['wireSchema']
FACT = json.loads((ROOT/'docs/coop/artifacts/fact-plane.v1.json').read_text())
VOCAB = ['hello','helloAck','select','selectAck','refusal','ping','pong','cancel','health','healthReport','resourceReport','fault','effectRequest','effectResult','shutdown','shutdownAck']
STATES = ['AWAIT-HELLO','AWAIT-HELLO-ACK','AWAIT-SELECT','AWAIT-SELECT-ACK','STEADY','TEARDOWN','CLOSED','FAULTED']
SID='00000000-0000-4000-8000-000000000001'
DIG='1'*64
TUPLE={'role':'semantic-provider','roleSubprotocol':'typescript','subprotocolVersion':1}

def sha(b): return hashlib.sha256(b).hexdigest()
def reject(x): raise ValueError(x)
def pairs(items):
    out={}
    for k,v in items:
        if k in out: reject('RF-2')
        out[k]=v
    return out

def control_parse(raw, ctx):
    if len(raw)<4: reject('RF-2')
    n=int.from_bytes(raw[:4],'big')
    if n==0 or n>ctx.get('bound',65536): reject('RF-2')
    if len(raw)!=n+4: reject('RF-2')
    try:
        v=json.loads(raw[4:].decode('utf-8'),object_pairs_hook=pairs,parse_float=lambda _:reject('RF-2'),parse_constant=lambda _:reject('RF-2'))
    except (UnicodeError,json.JSONDecodeError): reject('RF-2')
    if not isinstance(v,dict) or set(v)!={'type','seq','controlMajor','body'}: reject('RF-2')
    if not isinstance(v['type'],str) or type(v['controlMajor']) is not int or v['controlMajor']<1: reject('RF-2')
    if type(v['seq']) is not int or v['seq']<0: reject('RF-2')
    # Accepted framing specifically assigns sequence overflow RF-7.
    if v['seq']>9007199254740991: reject('RF-7')
    if v['type']=='hello' and v['controlMajor']!=1: reject('RF-1')
    def nums(x):
        if type(x) is int and not 0<=x<=9007199254740991: reject('RF-2')
        if isinstance(x,dict):
            for y in x.values(): nums(y)
        if isinstance(x,list):
            for y in x: nums(y)
    nums(v)
    if not isinstance(v['body'],dict): reject('RF-2')
    if v['type'] not in VOCAB: reject('RF-2')
    t=v['type'];b=v['body'];state=ctx.get('state','STEADY');direction=ctx.get('direction','host-to-component')
    # This model validates only the closed body projections exercised by its corpus.
    bodies={'hello':{'controlMajor','expectedStableId','admittedManifestDigest','platform','maxControlFrameBytesOffer','subprotocolOffers'},'helloAck':{'controlMajor','stableId','admittedManifestDigest','maxControlFrameBytes','subprotocolConfirms'},'select':set(TUPLE),'selectAck':set(TUPLE),'ping':{'nonce'},'pong':{'nonce'},'health':{'nonce'},'healthReport':{'nonce','status'},'cancel':{'reason'},'shutdown':{'reason'},'shutdownAck':set(),'fault':{'detail'},'resourceReport':{'residentBytes','cpuNanoseconds','openHandles'},'effectRequest':{'effectClass','authorizationRef'}}
    if t in bodies and set(b)!=bodies[t]: reject('RF-2')
    if t=='hello' and ctx.get('helloSeen',state!='AWAIT-HELLO'): reject('RF-8')
    if t=='helloAck' and (v['controlMajor']!=1 or b.get('controlMajor')!=1): reject('RF-8')
    if t in ['select','selectAck'] and state=='STEADY': reject('RF-8')
    if v['seq']!=ctx.get('nextSeq',1): reject('RF-7')
    if v['controlMajor']!=1: reject('RF-7')
    h2c={'hello','select','ping','cancel','health','shutdown','effectResult','refusal'}
    c2h={'helloAck','selectAck','pong','healthReport','resourceReport','fault','effectRequest','shutdownAck','refusal'}
    if t not in (h2c if direction=='host-to-component' else c2h): reject('RF-7')
    lawful={'AWAIT-HELLO':{'hello','refusal'},'AWAIT-HELLO-ACK':{'helloAck','refusal'},'AWAIT-SELECT':{'select','shutdown','refusal'},'AWAIT-SELECT-ACK':{'selectAck','refusal'},'STEADY':set(VOCAB)-{'hello','helloAck','select','selectAck','shutdownAck'},'TEARDOWN':{'shutdownAck','refusal'},'CLOSED':set(),'FAULTED':{'refusal'}}
    if t not in lawful[state]: reject('RF-7')
    if t in ['hello','helloAck']:
        identity=b.get('expectedStableId',b.get('stableId'))
        if identity!=SID or b.get('admittedManifestDigest')!=DIG: reject('RF-3')
        tuples=b.get('subprotocolOffers',b.get('subprotocolConfirms'))
        if not isinstance(tuples,list) or any(q!=TUPLE for q in tuples) or ctx.get('manifestStableId',SID)!=SID: reject('RF-4')
    if t in ['select','selectAck'] and b!=TUPLE: reject('RF-4')
    if t=='effectRequest':
        if b['effectClass'] in ['retry-analysis','discard-last-result']: reject('RF-5')
        if b['effectClass']!='read-project-file' or b['authorizationRef']!='grant:fixture-valid': reject('RF-6')
    if t=='cancel' and b['reason'] not in ['user','deadline','supervisor-fault']: reject('RF-5')
    return {'verdict':'ACCEPT','type':t,'state':{'hello':'AWAIT-HELLO-ACK','helloAck':'AWAIT-SELECT','select':'AWAIT-SELECT-ACK','selectAck':'STEADY','cancel':'TEARDOWN','shutdown':'TEARDOWN','shutdownAck':'CLOSED','refusal':'FAULTED','fault':'FAULTED'}.get(t,state)}

def decode_cbor(raw):
    stream=io.BytesIO(raw)
    try: v=cbor2.CBORDecoder(stream).decode()
    except (ValueError,EOFError): reject('provider-protocol')
    if stream.tell()!=len(raw) or cbor2.dumps(v,canonical=True)!=raw: reject('provider-protocol')
    def model(x):
        if x is None or type(x) is bool: return
        if type(x) is int:
            if not -2**63<=x<2**64: reject('provider-protocol')
        elif type(x) is str:
            if unicodedata.normalize('NFC',x)!=x: reject('provider-protocol')
        elif type(x) is bytes: pass
        elif type(x) is list:
            for y in x:model(y)
        elif type(x) is dict:
            for k,y in x.items():
                if type(k) is not str: reject('provider-protocol')
                model(k);model(y)
        else: reject('provider-protocol')
    model(v);return v

def closed(v, keys):
    if not isinstance(v,dict) or set(v)!=set(keys):reject('provider-protocol')

def provider_parse(raw,ctx):
    if len(raw)<40: reject('provider-protocol')
    n=int.from_bytes(raw[:8],'big')
    if n>67108864 or len(raw)!=40+n or hashlib.sha256(raw[40:]).digest()!=raw[8:40]:reject('provider-protocol')
    v=decode_cbor(raw[40:]);closed(v,WIRE['frameEnvelope']['required'])
    if type(v['protocolMajor']) is not int or v['protocolMajor']!=1 or type(v['sequence']) is not int or v['sequence']!=ctx.get('nextSeq',0):reject('provider-protocol')
    t=v['frameType']
    if t not in WIRE['frameSchemas'] or WIRE['frameSchemas'][t]['direction']!='worker-to-host':reject('provider-protocol')
    p=v['payload'];schema=WIRE['payloadSchemas'][WIRE['frameSchemas'][t]['payloadType']];closed(p,schema['required'])
    if ctx.get('terminal',False):reject('provider-protocol')
    if t=='FactBatch':
        if not isinstance(p['facts'],list) or not p['facts']: reject('provider-protocol')
        for fact in p['facts']:
            closed(fact,WIRE['definitions']['FactCandidateV1']['required'])
            registry=FACT['factRecordContractV1']['relationPayloadSchemaRegistryV1']['schemas']
            relation=fact['relation']
            if relation not in registry or fact['relationSchemaId']!=registry[relation]['schemaId']:reject('provider-protocol')
            payload=decode_cbor(fact['canonicalRelationPayload'])
            # This package uses an accepted declares conformance vector as positive source.
            if fact['canonicalRelationPayload'].hex()!=ctx['admittedRelationPayloadHex']:reject('provider-protocol')
    if t=='Coverage':
        if not isinstance(p['entries'],list) or not p['entries']:reject('provider-protocol')
        keys=[]
        for entry in p['entries']:
            closed(entry,WIRE['definitions']['CoverageResultV1']['required']);closed(entry['key'],WIRE['definitions']['CoverageKeyV1']['required']);keys.append(entry['key'])
            if entry['coverageState'] not in ['complete','unknown']: reject('provider-protocol')
            if (entry['coverageState']=='complete')!=(entry['deficiency'] is None):reject('provider-protocol')
            if ctx.get('hostKnownUnknown',False) and entry['coverageState']=='complete':reject('provider-protocol')
        if keys!=ctx['requestedKeys']:reject('provider-protocol')
    return {'verdict':'ACCEPT','type':t}

def boundary(x):
    a=x['action']
    if a=='admit-pack':
        p=x['pack'];ok=p['name']=='opensip.preview.typescript.pack' and p['version']==1 and p['origin']=='bundled-first-party' and p['kind']=='declarative'
        return {'admitted':ok,'evaluationStarted':ok}
    if a=='coverage':return {'coverage':'unknown' if not x['rungAvailable'] or not x['universeConstructible'] else 'complete','syntaxFallback':False,'authoritativeSuccess':False}
    if a=='output-mode':return {'offered':['human','json'],'accepted':x['requested'] in ['human','json'],'G17Required':False}
    if a=='publish-preview':
        return {'kind':'preview-result','sealedRun':False,'durableWrites':[],'promotionAccepted':False}
    if a=='host-projection':
        valid=x['origin']=='core-completion' and x['destination']=='policyOutcome'
        return {'accepted':valid,'policyOutcome':x['value'] if valid else None,'mintedD9':False,'mintedExit':False,'mintedHostTermination':False}
    reject('unknown boundary action')

def run_case(c):
    kind=c['kind']
    if kind=='control-length-recipe':
        base=bytes.fromhex(c['bodyBaseHex']);body=base+b' '*(c['bodyLength']-len(base))
        return control_parse(c['bodyLength'].to_bytes(4,'big')+body,c['context'])
    if kind in ['control','provider']:
        raw=bytes.fromhex(c['bytesHex'])
        try:out=(control_parse if kind=='control' else provider_parse)(raw,c['context'])
        except ValueError as e:out={'verdict':str(e),'discardCandidates':True,'teardown':True}
        return out
    if kind=='opaque-fault':
        snapshot=c['semanticSnapshotAfterOrdinaryFault']
        required={'facts','findings','coverage','policyOutcome','d9','hostTermination','exitCode','planAdmission','runFinalization','coreCompletion'}
        if set(snapshot)!=required:reject('incomplete semantic snapshot')
        paired=[]
        for key in ['benignControlHex','controlHex']:
            out=control_parse(bytes.fromhex(c[key]),{'state':'STEADY','direction':'component-to-host'})
            # Ordinary fault supervision has already determined the semantic snapshot
            # using the owning provider boundary event; detail is never an input.
            paired.append({'controlState':out['state'],'providerHex':c['providerHex'],'semanticSnapshot':snapshot})
        return {'benignFault':paired[0],'smugglingFault':paired[1],'semanticSnapshotsEqual':paired[0]['semanticSnapshot']==paired[1]['semanticSnapshot'],'detailInterpretation':'opaque-diagnostic-only'}
    if kind=='provider-transaction':
        facts=[];entries=[];batches=0;terminal=False;phase='facts'
        def commit(domain,v):return 'sha256:'+sha(domain.encode()+b'\0'+cbor2.dumps(v,canonical=True))
        domains=WIRE['commitments']['domains']
        try:
            for index,h in enumerate(c['framesHex']):
                raw=bytes.fromhex(h);ctx={**c['context'],'nextSeq':index,'terminal':terminal}
                provider_parse(raw,ctx);v=decode_cbor(raw[40:]);p=v['payload'];t=v['frameType']
                if t=='FactBatch':
                    if phase!='facts' or p['batchIndex']!=batches or p['stageId']!='ts-declares':reject('provider-protocol')
                    if p['batchCommitment']!=commit(domains['factBatch'],p['facts']):reject('provider-protocol')
                    facts+=p['facts'];batches+=1
                elif t=='Coverage':
                    if phase!='facts' or p['stageId']!='ts-declares':reject('provider-protocol')
                    entries=p['entries'];phase='complete'
                    if p['coverageCommitment']!=commit(domains['stageCoverage'],entries):reject('provider-protocol')
                elif t=='Complete':
                    if phase!='complete':reject('provider-protocol')
                    expected={'stageId':'ts-declares','stageOrdinal':0,'factBatchCount':batches,'factCount':len(facts),'coverageEntryCount':len(entries),'factCommitment':commit(domains['stageFacts'],facts),'coverageCommitment':commit(domains['stageCoverage'],entries)}
                    if p['stageResults']!=[expected] or p['factStreamCommitment']!=commit(domains['factStream'],facts) or p['coverageStreamCommitment']!=commit(domains['coverageStream'],entries):reject('provider-protocol')
                    terminal=True
                else:reject('provider-protocol')
            if not terminal or c['processTail']!=['exit:0','EOF']:reject('provider-protocol')
            return {'verdict':'ADMIT','candidateCount':len(facts),'coverageCount':len(entries)}
        except ValueError:return {'verdict':'DISCARD','candidateCount':0,'coverageCount':0}
    if kind=='boundary':return boundary(c['input'])
    if kind=='event-order':
        priority={'provider-final-octet':0,'control-fault':1,'provider-fault-report':2,'provider-EOF':2,'cancel-issued':3,'teardown-initiated':4,'drain-deadline-expired':5,'process-death':6}
        indexed=list(enumerate(c['events']))
        # J3 death is a deferred append until drain EOF or explicit drain expiry.
        ordered=sorted(indexed,key=lambda z:(z[1]['kind']=='process-death',z[1]['instant'],priority[z[1]['kind']],z[0]))
        return {'order':[e['kind'] for _,e in ordered],'providerHex':c['providerHex']}
    if kind=='transport':
        chunks=[bytes.fromhex(h) for h in c['chunksHex']]
        # Reference carrier deliberately concatenates bytes, never provider-decodes.
        return {'providerHex':b''.join(chunks).hex(),'controlTypes':[control_parse(bytes.fromhex(h),{'state':'STEADY','nextSeq':i+1})['type'] for i,h in enumerate(c['controlHex'])]}
    if kind=='process-trace':
        delivered=bytearray();steps=[];death=False
        initial=c['initialState'];early=False
        for e in c['events']:
            if e['kind']=='provider-bytes':
                if death: reject('bytes-after-reap')
                delivered.extend(bytes.fromhex(e['bytesHex']))
                early |= initial in STATES[:4]
            elif e['kind']=='begin-teardown':steps+=['T-1','T-2']
            elif e['kind']=='wait-expired':steps+=['wait-expired','T-3']
            elif e['kind']=='drain-deadline-expired':steps.append('drain-deadline-expired')
            elif e['kind']=='kill-tree':steps.append('T-4')
            elif e['kind']=='process-death':steps.append('T-5');death=True
        return {'discardCandidates':death,'terminalSuccess':False,'dataEarly':early,'teardown':steps,'lastEvent':c['events'][-1]['kind'],'providerHex':bytes(delivered).hex()}
    if kind=='containment':
        x=c['input'];core=x['coreSnapshots'];desc=set(x['descendantsAtInjection']);after=set(x['pidsAfter'])
        diagnostics=bytes.fromhex(x['diagnosticHex'])
        return {'coreSurvived':len({r['pid'] for r in core})==1 and all(r['alive'] for r in core) and x['subsequentSession']=='completed',
                'treeReaped':not (desc & after) and desc<=set(x['reapedPids']),
                'candidatesDiscarded':not x['candidateBufferAfter'] and not x['subsequentCandidateView'],
                'sealedBytesPreserved':x['sealedBeforeHex']==x['sealedAfterHex'],
                'diagnosticsBoundedRedacted':len(diagnostics)<=x['diagnosticBound'] and b'\x1b' not in diagnostics and x['secretSentinel'].encode() not in diagnostics,
                'projectionPreserved':x['actualProjection']==x['expectedProjection']}
    if kind=='atomicity':
        e=c['events'];ok=e==['FactBatch','Coverage','Complete','exit:0','EOF']
        return {'admittedCandidates':c['candidateCount'] if ok else 0,'discardedCandidates':0 if ok else c['candidateCount']}
    raise ValueError('Unknown case kind '+kind)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report',type=Path,default=HERE/'protocol-model-report.v2.json');args=parser.parse_args()
    manifest=json.loads((HERE/'protocol-fixtures.v2.json').read_text())
    blobfile=HERE/'protocol-fixture-blobs.v2.json'
    blobs=json.loads(blobfile.read_text())
    def expand(v):
        if isinstance(v,dict):
            if set(v)=={'$bytes'}:
                h=v['$bytes'];raw=bytes.fromhex(blobs[h]);assert sha(raw)==h;return raw.hex()
            return {k:expand(x) for k,x in v.items()}
        if isinstance(v,list):return [expand(x) for x in v]
        return v
    manifest=expand(manifest)
    checks=[]
    coverage=json.loads((HERE/'protocol-coverage.v2.json').read_text())
    ids=[c['id'] for c in manifest['cases']]
    checks.append({'id':'coverage:case-ids','pass':len(ids)==len(set(ids))==coverage['caseCount'] and sha('\n'.join(sorted(ids)).encode())==coverage['caseIdSetSha256']})
    for prefix,count in coverage['matrixCounts'].items():checks.append({'id':'coverage:matrix:'+prefix,'pass':sum(i.startswith(prefix) for i in ids)==count})
    for req,spec in coverage['requirements'].items():
        checks.append({'id':'coverage:obligation:'+req,'pass':all(any(i.startswith(p) for i in ids) for p in spec['casePrefixes'])})
    for p,h in manifest['sourcePins'].items():
        checks.append({'id':'source:'+p,'pass':sha((ROOT/p).read_bytes())==h})
    for c in manifest['cases']:
        try: got=run_case(c);ok=got==c['expected']
        except Exception as e:got={'checkerError':repr(e)};ok=False
        checks.append({'id':c['id'],'pass':ok,**({} if ok else {'expected':c['expected'],'actual':got})})
    required={f'DR131-NT{i}' for i in range(1,9)}|{f'DR133-NT{i}' for i in range(1,8)}|{f'CC-{i}' for i in range(1,12)}
    actual={t for c in manifest['cases'] for t in c['covers']}
    checks.append({'id':'coverage:all-retained-NT-and-CC','pass':required<=actual,'missing':sorted(required-actual)})
    report={'status':'DESIGN-MODEL-EVIDENCE-ONLY','productQualified':False,'platformExecutions':[],'sourceSha256':sha(Path(__file__).read_bytes()),'fixtureSha256':sha((HERE/'protocol-fixtures.v2.json').read_bytes()),'blobSha256':sha(blobfile.read_bytes()),'coverageSha256':sha((HERE/'protocol-coverage.v2.json').read_bytes()),'total':len(checks),'passed':sum(x['pass'] for x in checks),'checks':checks,'limits':manifest['limits']}
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='checks'},indent=2))
    if report['passed']!=report['total']:
        print(json.dumps([x for x in checks if not x['pass']],indent=2));sys.exit(1)
if __name__=='__main__':main()

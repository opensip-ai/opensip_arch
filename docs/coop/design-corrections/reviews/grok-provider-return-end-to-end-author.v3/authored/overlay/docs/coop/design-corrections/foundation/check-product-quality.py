"""Synthetic multi-language report custody/admission mutations, not native measurements."""
import argparse,copy,hashlib,importlib.util,json,subprocess,tempfile,sys
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('pq',H/'product-quality-validator.py');Q=importlib.util.module_from_spec(s);s.loader.exec_module(Q)
C=Q.C
rows=[]
def check(name,condition):rows.append({'id':name,'passed':bool(condition)})
with tempfile.TemporaryDirectory(prefix='opensip-product-quality-') as td:
    p=Path(td)
    subprocess.run(['openssl','genpkey','-algorithm','ED25519','-out',str(p/'key')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    public=subprocess.check_output(['openssl','pkey','-in',str(p/'key'),'-pubout']).decode()
    ctx={k:hashlib.sha256(k.encode()).hexdigest() for k in ['hostDigest','providerClosureDigest','harnessDigest']}
    ctx.update({'producerPublicKeyPem':public,'runnerId':'reference-runner','profileId':'reference-profile','expectedCells':{},'qualificationRequestId':'req1_'+'1'*32})
    for k in ['matrix','corpus','environment']:
        ctx[k+'Bytes']=C.canonical({'kind':k,'referenceOnly':True});ctx[k+'Digest']=hashlib.sha256(ctx[k+'Bytes']).hexdigest()
    cells=[]
    for mode,observation in [('ts-tsconfig','resolved'),('js-synthesized','resolution-incomplete'),('rust-cargo','input-closure-incomplete')]:
        cid='references/'+mode+'/macos-aarch64/reference-profile/fixture'
        atom={'kind':'coverage','subject':'fixture','value':observation}
        ctx['expectedCells'][cid]={'observations':[atom],'exitStatus':0,'absoluteNanos':1000,'absoluteRssBytes':1000,'baselineMedianNanos':100,'baselinePeakRssBytes':100}
        cells.append({'cellId':cid,'warmupRuns':3,'elapsedNanos':[100]*7,'peakRssBytes':[100]*7,'observations':[atom],'exitStatus':0})
    report={k:ctx[k] for k in ['hostDigest','providerClosureDigest','harnessDigest','matrixDigest','corpusDigest','runnerId','profileId','environmentDigest','qualificationRequestId']}
    report.update({'schemaMajor':3,'cells':cells})
    def sign(raw):
        (p/'message').write_bytes(Q.G.signature_message(raw,ctx))
        return subprocess.check_output(['openssl','pkeyutl','-sign','-inkey',str(p/'key'),'-rawin','-in',str(p/'message')])
    def evaluate(value,context=None):
        raw=C.canonical(value);return Q.admit(raw,sign(raw),context or ctx)
    result=evaluate(report);check('valid-three-language-reference',result['admitted'] and result['passed'])
    for field in ['hostDigest','providerClosureDigest','harnessDigest','matrixDigest','corpusDigest','environmentDigest','runnerId','profileId','qualificationRequestId']:
        bad=copy.deepcopy(report);bad[field]='e'*64 if field.endswith('Digest') else 'other'
        check('forged-'+field,not evaluate(bad)['admitted'])
    bad=copy.deepcopy(report);bad['cells'][0]['observations']=[]
    result=evaluate(bad);check('zero-actual-cannot-zero-oracle',result['admitted'] and not result['passed'] and result['cells'][1 if result['cells'][0]['cellId']!=cells[0]['cellId'] else 0]['expectedCount']>=1)
    bad=copy.deepcopy(report);bad['cells'][1]['observations'][0]['value']='complete'
    result=evaluate(bad);check('false-js-completeness-fails',result['admitted'] and not result['passed'])
    bad=copy.deepcopy(report);bad['cells'].pop();check('missing-rust-cell-rejected',not evaluate(bad)['admitted'])
    bad=copy.deepcopy(report);bad['cells'].append(copy.deepcopy(bad['cells'][0]));check('duplicate-cell-rejected',not evaluate(bad)['admitted'])
    bad=copy.deepcopy(report);bad['cells'][0]['observations']*=2;check('duplicate-observation-rejected',not evaluate(bad)['admitted'])
    for field in ['elapsedNanos','peakRssBytes']:
        bad=copy.deepcopy(report);bad['cells'][0][field]=[200]*7
        result=evaluate(bad);check('false-performance-'+field,result['admitted'] and not result['passed'])
    bad=copy.deepcopy(report);bad['cells'][0]['elapsedNanos']=[0]*7;check('zero-duration-rejected',not evaluate(bad)['admitted'])
    bad=copy.deepcopy(report);bad['passed']=True;check('submitted-pass-flag-rejected',not evaluate(bad)['admitted'])
    bad=copy.deepcopy(ctx);bad['corpusBytes']=b'changed';check('changed-trusted-corpus-bytes-rejected',not evaluate(report,bad)['admitted'])
    raw=C.canonical(report);signature=sign(raw);check('invalid-signature-rejected',not Q.admit(raw,b'0'*64,ctx)['admitted'])
    raw=raw.replace(b'"schemaMajor":3',b'"schemaMajor":3.0');check('signed-rounded-major-rejected',not Q.admit(raw,sign(raw),ctx)['admitted'])
    for fields in [('baselineMedianNanos',),('baselineMedianNanos','baselinePeakRssBytes')]:
        bad=copy.deepcopy(ctx)
        for field in fields:bad['expectedCells'][cells[0]['cellId']][field]=None
        result=evaluate(report,bad);check('missing-initial-baseline-not-qualified-'+str(fields),not result.get('passed',False))
out={'standing':'design-reference-only','productQualification':False,'checks':rows,'passed':sum(v['passed'] for v in rows),'failed':sum(not v['passed'] for v in rows)}
p=argparse.ArgumentParser();p.add_argument('--report');a=p.parse_args()
if a.report:Path(a.report).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['passed','failed','productQualification']}));sys.exit(bool(out['failed']))

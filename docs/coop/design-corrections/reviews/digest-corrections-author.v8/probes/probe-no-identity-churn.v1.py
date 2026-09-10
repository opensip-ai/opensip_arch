"""PROBE: does the v7 validator fix move any identity?

My interface note asserted it should not, and v6 taught me to measure that rather than assume it.
This is a validator-consistency fix: it adds a refusal for a condition the shipped document does
not contain, and touches no encoder, no join, no registry and no schema document. So every Run
identity should be byte-identical between the frozen v9 subject and the corrected tree.

Method: run the SAME builders in two namespaces - the frozen v9 candidate copy and the working tree
- and compare RunId, PlanId, the clone bodyIdentity and the language-version component across the
shapes this correction could plausibly disturb. Only the two owned files differ between them; that
is asserted here rather than assumed, by hashing all nine previously-owned files in both.
"""
import ast,hashlib,json,sys
from pathlib import Path

FROZEN=Path('/tmp/opensip-design-corrections/candidate-subject.v9')
WORKING=Path('/Users/sb/code/opensip-ai/opensip_arch')
NINE=['docs/coop/design-corrections/foundation/identity-model.py',
      'docs/coop/design-corrections/foundation/check-identity.py',
      'docs/coop/design-corrections/foundation/identity-schemas.v2.json',
      'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json',
      'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
      'docs/coop/design-corrections/native/native_evidence_model.v2.py',
      'docs/coop/design-corrections/native/native-cases.v2.json',
      'docs/v2/contracts/product-v1/identity-and-evidence.md',
      'docs/v2/contracts/product-v1/native-evidence.md']

def load(root,label):
    path=root/'docs/coop/design-corrections/foundation/check-identity.py'
    source=path.read_text();tree=ast.parse(source)
    last=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import').end_lineno
    ns={'__file__':str(path),'__name__':'churn_'+label};sys.argv=[sys.argv[0]]
    exec(compile('\n'.join(source.split('\n')[:last]),str(path),'exec'),ns)
    return ns

def measure(root,label):
    ns=load(root,label);M,C=ns['M'],ns['C']
    out={}
    for shape,kwargs in (('references',{}),
                         ('file',{'relation':'file'}),
                         ('clones-typescript',{'relation':'clones'}),
                         ('clones-rust',{'relation':'clones','universe_language':'rust'})):
        run,objects,blobs=ns['build'](resolved=True,has_match=True,**kwargs)
        row={'runId':M.close_run(run,objects,blobs),'planId':run['planId']}
        fact=next(v for k,(d,v) in objects.items() if d=='fact')
        payload=C.parse(blobs[fact['payloadDigest']])
        row['factPayloadDigest']=fact['payloadDigest']
        if 'bodyIdentity' in payload:
            row['bodyIdentity']=payload['bodyIdentity']
            row['languageVersionHex']=M.parse_body_frame(
                blobs[payload['bodyIdentity'].removeprefix('sha256:')])[4].hex()
        out[shape]=row
    return out

images={p:{'frozen':hashlib.sha256((FROZEN/p).read_bytes()).hexdigest(),
           'working':hashlib.sha256((WORKING/p).read_bytes()).hexdigest()} for p in NINE}
differ=sorted(p for p,v in images.items() if v['frozen']!=v['working'])
frozen=measure(FROZEN,'frozen');working=measure(WORKING,'working')
identical={shape:frozen[shape]==working[shape] for shape in frozen}

print(json.dumps({
 'standing':'actual Claude coauthor measurement across the frozen v9 subject and the corrected tree; '
            'design/reference evidence only, no product qualification',
 'ownedFilesThatDiffer':differ,
 'ownedFilesUnchanged':sorted(set(NINE)-set(differ)),
 'frozen':frozen,'working':working,
 'identicalByShape':identical,
 'verdict':('NO CHURN: every RunId, PlanId, fact payload digest, bodyIdentity and language-version '
            'component is identical across the two images'
            if all(identical.values()) else 'CHURN: see identicalByShape')},indent=1))

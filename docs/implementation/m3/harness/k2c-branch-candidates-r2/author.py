"""Independent finite recipes. No parser, compiler or producer import/execution."""
import hashlib, json
from pathlib import Path
arch=Path('/Users/sb/code/opensip-ai/opensip_arch')
root=Path('/tmp/opensip-implementation/k2c-branch-stage-r2')
rel='docs/implementation/m3/harness/k2c-branch-candidates-r2'
dest=root/rel
dest.mkdir(parents=True,exist_ok=False)
source_prefix='docs/implementation/m3/harness/k2c-finite-source-r1'
normalizer='docs/implementation/m3/syntax-e/syn-ns/closure/opensip-interface/grammar/normalizer.v1.json'
def pin(p,label):
    raw=p.read_bytes(); return {'path':label,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def span(start,end): return {'startByte':start,'endByte':end}
files=[]
for grammar,suffix in [('javascript','js'),('rust','rs'),('tsx','tsx'),('typescript','ts')]:
    path=f'{source_prefix}/fixtures/{grammar}/syntax-control.{suffix}'
    raw=(arch/path).read_bytes()
    leaf=f'syntax-control.{suffix}'
    file_subject='syntax:'+leaf+'#'
    owner=file_subject+'function:branch@0'
    function_span=span(0,len(raw.rstrip(b'\n')))
    body_span=span(raw.index(b'{'),len(raw.rstrip(b'\n')))
    declares=[{'declared':owner,'container':file_subject,'declarationKind':'function','anchor':function_span}]
    if grammar!='rust':
        start=raw.index(b'value')
        declares.append({'declared':owner+'/parameter:value@0','container':owner,'declarationKind':'parameter','anchor':span(start,start+5)})
    literals=[]
    # Exact independently authored numeric tokens in these four owned source controls.
    for token,needle in [(b'0',b'0'),(b'7',b'7'),(b'1',b'1')]:
        start=raw.index(needle)
        assert raw[start:start+len(token)]==token
        literals.append({'owner':owner,'literalKind':'number','valueText':token.decode(),'anchor':span(start,start+len(token))})
    if_start=raw.index(b'if ')
    if grammar=='rust':
        if_end=raw.index(b'\n',if_start)
        if_subject=owner+'/stmt:if_expression@0'
        true_subject=if_subject+'/stmt:integer_literal@0'
        false_subject=if_subject+'/stmt:binary_expression@0'
        true_start=raw.index(b'7')
        false_start=raw.index(b'value + 1')
        statements=[{'subject':if_subject,'kind':'if_expression','anchor':span(if_start,if_end)}, {'subject':true_subject,'kind':'integer_literal','anchor':span(true_start,true_start+1)}, {'subject':false_subject,'kind':'binary_expression','anchor':span(false_start,false_start+9)}]
        true_kind=false_kind='fallthrough'
    else:
        if_end=raw.index(b'}',if_start)+1
        if_subject=owner+'/stmt:if_statement@0'
        true_subject=if_subject+'/stmt:return_statement@0'
        false_subject=owner+'/stmt:return_statement@0'
        true_start=raw.index(b'return 7;')
        false_start=raw.index(b'return value + 1;')
        statements=[{'subject':if_subject,'kind':'if_statement','anchor':span(if_start,if_end)}, {'subject':true_subject,'kind':'return_statement','anchor':span(true_start,true_start+9)}, {'subject':false_subject,'kind':'return_statement','anchor':span(false_start,false_start+17)}]
        true_kind=false_kind='return'
    entry=owner+'/entry:@0'; exit_=owner+'/exit:@0'
    anchors={r['subject']:r['anchor'] for r in statements}
    anchors[entry]=body_span
    edges=[]
    for from_,to,kind in [(entry,if_subject,'fallthrough'),(if_subject,true_subject,'branch-true'),(if_subject,false_subject,'branch-false'),(true_subject,exit_,true_kind),(false_subject,exit_,false_kind)]:
        edges.append({'fromSubject':from_,'toSubject':to,'edgeKind':kind,'anchor':anchors[from_]})
    row={'grammarVariant':grammar,'bodyLanguage':'typescript' if grammar=='tsx' else grammar,'sourceInput':pin(arch/path,path),'snapshotPath':leaf,'caseExtent':'This single accepted source control at its grammar-specific isolated snapshot root.','fileSubject':file_subject,'declares':declares,'literals':literals,'controlFlowGraphs':[{'owner':owner,'bodySpan':body_span,'entry':entry,'exit':exit_,'statements':statements,'edges':edges}], 'notes':['Independent declarative candidate recipe under accepted SYN-NS; no AST or producer output was consulted.', 'Rust tail if_expression branches each complete normally; JavaScript-family return statements go directly to exit.', 'Rust plain parameter pattern binds nothing; JavaScript-family value parameter binds once.', 'Body is below the 64 raw-byte clone candidate floor; no clone group or near pair is expected.', 'No Fact2/Body2/Coverage/context/universe identity, normalized cell atom, whole-case exit or lane freeze is minted here.']}
    # Mechanical worksheet assertions inspect only exact already-owned source bytes.
    assert raw[body_span['startByte']:body_span['endByte']].startswith(b'{')
    assert raw[body_span['startByte']:body_span['endByte']].endswith(b'}')
    assert body_span['endByte']-body_span['startByte'] < 64
    for statement in statements:
        anchor=statement['anchor']; assert 0 <= anchor['startByte'] < anchor['endByte'] <= len(raw)
        text=raw[anchor['startByte']:anchor['endByte']]
        if statement['kind'] in ('if_statement','if_expression'): assert text.startswith(b'if ')
        elif statement['kind']=='return_statement': assert text.startswith(b'return') and text.endswith(b';')
        elif statement['kind']=='integer_literal': assert text==b'7'
        elif statement['kind']=='binary_expression': assert text==b'value + 1'
    assert len({(r['fromSubject'],r['toSubject'],r['edgeKind']) for r in edges})==5
    assert row['bodyLanguage'] == {'javascript':'javascript','rust':'rust','tsx':'typescript','typescript':'typescript'}[grammar]
    files.append(row)
worksheet={'schemaVersion':1,'standing':'INDEPENDENT-FINITE-BRANCH-CANDIDATE-EXPECTATIONS-NOT-FULL-ORACLE','normalizer':pin(arch/normalizer,normalizer),'files':files,'parserRuns':0,'compilerRuns':0,'producerRuns':0,'laneFrozen':False,'fullCaseSet':False,'productQualification':False}
(dest/'branch-candidate-worksheet.json').write_text(json.dumps(worksheet,indent=2)+'\n')
checks={'sourceFiles':len(files),'declares':sum(len(r['declares']) for r in files),'literals':sum(len(r['literals']) for r in files),'controlFlowGraphs':len(files),'statements':sum(len(r['controlFlowGraphs'][0]['statements']) for r in files),'edges':sum(len(r['controlFlowGraphs'][0]['edges']) for r in files),'mechanicalSpanAndEdgeAssertionsPassed':True,'parserRuns':0,'compilerRuns':0,'producerRuns':0,'laneFrozen':False,'fullCaseSet':False,'productQualification':False}
(dest/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(dest/'author.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(checks))

from pathlib import Path
import ast,json,copy,hashlib
base=Path('/tmp/opensip-design-corrections/payload-closure-probe.v8');fixture=base/'work/docs/coop/design-corrections/foundation/check-identity.py';tree=ast.parse(fixture.read_text());last=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import').end_lineno
ns={'__file__':str(fixture),'__name__':'captured_fixture'};exec(compile('\n'.join(fixture.read_text().split('\n')[:last]),str(fixture),'exec'),ns)
M,C,N=ns['M'],ns['C'],ns['N'];build,rekey,put=ns['build'],ns['rekey'],ns['put_blob']
def outcome(run,objects,blobs):
 try:return {'admitted':True,'runId':M.close_run(run,objects,blobs)}
 except Exception as e:return {'admitted':False,'exception':type(e).__name__,'cause':str(e)}
r,o,b=build(has_match=True);control=outcome(r,o,b);vid=o[r['evidenceId']][1]['viewIds'][0];view=copy.deepcopy(o[vid][1]);fid=view['facts'][0];bad=copy.deepcopy(o[fid][1]);bad['payloadSchemaDigest']=put(b,{'type':'object'})
# Change one harmless anchor bound to make the invalid fact sort AFTER its valid sibling.
for end in range(len(b[bad['anchors'][0]['blobDigest']])+1):
 bad['anchors'][0]['endByte']=end;bid=M.identifier('fact',bad)
 if bid>fid:break
else:raise AssertionError('no ordered fixture candidate')
o[bid]=('fact',bad);view['facts']=sorted([fid,bid]);view['schemaDigests']=sorted(set(view['schemaDigests'])|{bad['payloadSchemaDigest']});rekey(o,vid,view,r)
pid=o[r['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(o[pid][1]);view=o[o[r['evidenceId']][1]['viewIds'][0]][1]
for pred in proof['predicateProofs']:
 witness=C.parse(b[pred['witnessDigest']]);witness['matchingFactIds']=view['facts'];witness['coverageIds']=view['coverageIds'];pred['witnessDigest']=put(b,witness)
rekey(o,pid,proof,r)
result={'standing':'Codex coauthor context-sensitive payload memo probe; exact SAME captured source as coverage counterexamples','control':control,'validFactId':fid,'invalidFactId':bid,'invalidFactSortsAfterValid':bid>fid,'sharedPayloadDigest':bad['payloadDigest'],'wrongSchemaDigest':bad['payloadSchemaDigest'],'twoFactGraph':outcome(r,o,b)}
if result['twoFactGraph']['admitted']:
 try:store=M.EvidenceStore();store.prepare(r,o,b,'exec1_'+'f'*32,ns['replay']);result['twoFactGraph']['storeCommit']=store.commit('exec1_'+'f'*32)
 except Exception as e:result['twoFactGraph']['storeRefusal']=str(e)
# Invalid schema without the valid memo-priming sibling must be refused for exactly the registration.
r2,o2,b2=build(has_match=True);v2=o2[o2[r2['evidenceId']][1]['viewIds'][0]][1];f2=v2['facts'][0];bad2=copy.deepcopy(o2[f2][1]);bad2['payloadSchemaDigest']=put(b2,{'type':'object'});rekey(o2,f2,bad2,r2)
result['sameInvalidSchemaAlone']=outcome(r2,o2,b2)
(base/'memo-result.json').write_text(json.dumps(result,indent=2)+'\n');(base/'memo-probe.py').write_bytes(Path(__file__).read_bytes());print(json.dumps(result))

fixture=work/'docs/coop/design-corrections/foundation/check-identity.py';tree=ast.parse(fixture.read_text());last=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import').end_lineno
ns={'__file__':str(fixture),'__name__':'captured_fixture'};exec(compile('\n'.join(fixture.read_text().split('\n')[:last]),str(fixture),'exec'),ns)
M,C,N=ns['M'],ns['C'],ns['N'];build,rekey,put=ns['build'],ns['rekey'],ns['put_blob'];result={'standing':'Codex coauthor counterexample over captured in-progress bytes, not independent review','vectors':[]}
def fix_witness(run,objects,blobs):
 pid=objects[run['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(objects[pid][1]);view=objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
 for pred in proof['predicateProofs']:
  witness=C.parse(blobs[pred['witnessDigest']]);witness['coverageIds']=view['coverageIds'];witness['matchingFactIds']=view['facts'];pred['witnessDigest']=put(blobs,witness)
 rekey(objects,pid,proof,run)
def closure(run,objects,blobs):
 try:return {'admitted':True,'runId':M.close_run(run,objects,blobs)}
 except Exception as e:return {'admitted':False,'exception':type(e).__name__,'cause':str(e)}
r,o,b=build();control=closure(r,o,b);result['positive']=control
if control['admitted']:
 for name,mutate in [('wrong-subject-count',lambda p:p['entry']['examinedUniverse'].update(subjectCount=999)),('complete-without-attempt',lambda p:p['entry']['resolutionCompleteness'].update(attempted=False))]:
  r,o,b=build();cid=o[r['evidenceId']][1]['coverageIds'][0];cov=copy.deepcopy(o[cid][1]);scope=o[cov['scopeId']][1];payload=C.parse(b[cov['payloadDigest']]);mutate(payload)
  native=N.admit_coverage_result_v3(payload,scope,[],cov['payloadSchemaDigest']);cov['payloadDigest']=put(b,payload);rekey(o,cid,cov,r);fix_witness(r,o,b)
  outcome=closure(r,o,b)
  if outcome['admitted']:
   try:store=M.EvidenceStore();rid=store.prepare(r,o,b,'exec1_'+'e'*32,ns['replay']);outcome['storeCommit']=store.commit('exec1_'+'e'*32);outcome['storedRunId']=rid
   except Exception as e:outcome['storeRefusal']=str(e)
  result['vectors'].append({'id':name,'nativeAdmission':native,'completeRunClosure':outcome})
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(out/'probe.py').write_bytes(Path(__file__).read_bytes());print(json.dumps(result))

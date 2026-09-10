from pathlib import Path
import json,base64,hashlib
P=Path(__file__).parent
t=json.loads((P/'object-table.json').read_text());bb=json.loads((P/'blobs.b64.json').read_text())['blobs']
raw={h:base64.b64decode(s,validate=True) for h,s in bb.items()};assert all(hashlib.sha256(b).hexdigest()==h for h,b in raw.items())
results=[]
for r in t['runs']:
 objects={o['typedIdentity']:o['descriptor'] for o in r['objects'] if o['kind']=='h-identity'}
 run=objects[r['runId']];seal=objects[run['evaluationSealId']];proof=objects[seal['proofBundleId']];ev=objects[seal['evidenceId']]
 prog=json.loads(raw[proof['ruleProgramDigest']]);policy=json.loads(raw[seal['policyDigest']]);assert len(prog['rules'])==len(policy['rules'])==1
 node=prog['rules'][0]['emitWhen']
 if node!={'op':'exists','relation':'unresolved-edge','minResolution':'observed','filters':[]}:
  results.append({'runId':r['runId'],'label':r['label'],'result':'DIFFERENT_POLICY_NOT_AUDITED','node':node,'basis':'No generic semantic replay is claimed by this focused audit.'});continue
 facts=[objects[f] for v in ev['viewIds'] for f in objects[v]['facts']]
 coverage=[json.loads(raw[objects[c]['payloadDigest']]) for c in ev['coverageIds']]
 relfacts=[f for f in facts if f['relation']=='unresolved-edge'];relcov=[c for c in coverage if c['entry']['relation']=='unresolved-edge']
 assert not relfacts
 row={'runId':r['runId'],'label':r['label'],'selectedUnresolvedEdgeFacts':len(relfacts),'selectedUnresolvedEdgeCoverage':len(relcov),'claimedPredicateValue':proof['predicateProofs'][0]['value'],'claimedVerdict':proof['verdict']}
 if not relcov:
  row.update(result='FALSE_ABSENCE_NOT_JUSTIFIED',requiredValue='indeterminate',basis='Identity-and-evidence section4: exists with no known match and without complete absence is indeterminate; no Coverage for this relation is retained. This audits this atom only, not a general replay implementation.')
 else:row.update(result='HAS_RELATION_COVERAGE_NOT_FULL_REPLAYED',basis='Relevant Coverage exists. This focused audit does not establish complete subject enumeration, scope membership, witness exactness or aggregate proof validity.')
 results.append(row)
out={'standing':'Root focused audit of exact independently exported atoms. No author or independent source edits. Missing matching Coverage is an own-reconstruction issue with published normative law, not an inferred design gap.','runs':results}
(P/'predicate-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

from pathlib import Path
import json,hashlib,shutil,collections
B=Path('/tmp/opensip-implementation/sm-stage-volume-2026-10-09/compiler-definition-join-observations');v=json.loads((B/'results-all32.json').read_text());assert v['successfulUnits']==32 and v['incompleteUnits']==0 and len(v['excludedUnits'])==33;rows=[]
for r in v['rows']:
 events=[json.loads(s) for s in Path(r['stdout']).read_text().splitlines()];headers={};exports={};spans={};lexed={};definitions={};hj=None;dj=None
 for e in events:
  typ=e['event']
  if typ=='expanded_function_definition_join':hj=e
  if typ=='local_definition_join':dj=e;assert e['definitionId'] not in definitions;definitions[e['definitionId']]=e
  if typ in ['expanded_ast_function_header_observation','compiler_function_header_lexer_observation']:
   assert hj and hj['defPath']==e['defPath'] and hj['headerProjection']==e['headerProjection'];dest=headers if typ=='expanded_ast_function_header_observation' else lexed;assert hj['definitionId'] not in dest;dest[hj['definitionId']]=e|dict(defPathHash=hj['defPathHash'])
  if typ in ['effective_export_observation','function_signature_span_observation']:
   assert dj and dj['defPath']==e['defPath'];dest=exports if typ=='effective_export_observation' else spans;assert dj['definitionId'] not in dest;dest[dj['definitionId']]=e
 assert set(headers)==set(spans)==set(lexed);assert set(exports)==set(definitions);assert len({e['defPathHash'] for e in definitions.values()})==len(definitions)
 for key,h in headers.items():
  assert exports[key]['exported']==h['exported'] and exports[key]['defKind']==h['defKind'];assert definitions[key]['defPathHash']==h['defPathHash'];l=lexed[key];assert ''.join(t['text'] for t in l['tokens'])==l['headerProjection']==h['headerProjection']
 counts=collections.Counter(e['defPath'] for e in definitions.values());rows.append(dict(index=r['index'],headers=len(headers),expandedHeaders=sum(e['fromExpansion'] for e in headers.values()),definitions=len(definitions),repeatedDisplayedPathRows=sum(n-1 for n in counts.values()),compilerHeaderSpanIdSetsEqual=True,effectiveExportIdJoinsEqual=True,stableDefPathHashesUnique=True,exactLexerHeaderReconstruction=True))
audit=dict(standing='UNREVIEWED ACTUAL COMPILER DEFINITION-ID JOINS AND FUNCTION-ONLY AST/LEXER CROSS-QUERY OBSERVATIONS',successfulUnits=32,excludedUnits=33,functionHeaders=sum(r['headers'] for r in rows),expandedHeaders=sum(r['expandedHeaders'] for r in rows),definitions=sum(r['definitions'] for r in rows),repeatedDisplayedPathRows=sum(r['repeatedDisplayedPathRows'] for r in rows),compilerHeaderSpanIdSetsEqual=True,effectiveExportIdJoinsEqual=True,stableDefPathHashesUniqueWithinEachUnit=True,allLexerTokensRetained=True,exactHeaderReconstruction=True,rows=rows,originalCompilerASTUnchanged=True,completeSymbolCensus=False,actualFactCandidates=False,signatureTokensQualified=False,sourceAdmission=False,actualC2PlanOrKeys=False,fullSM=False)
(B/'cross-query-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({k:v for k,v in audit.items() if k!='rows'},indent=2));C=Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06');p=C/'CURRENT-STATE.json';j=json.loads(p.read_text());j['SMCompilerDefinitionJoinObservations']=audit|dict(directory=str(B),resultsSha256=hashlib.sha256((B/'results-all32.json').read_bytes()).hexdigest());j['currentReviewStatus']='working seq413';p.write_text(json.dumps(j,indent=2)+'\n');shutil.copytree(B,C/'continuation-preserved/sm-compiler-definition-join-observations')

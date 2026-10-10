from pathlib import Path
import json,hashlib
B=Path('/tmp/opensip-implementation/sm-stage-volume-2026-10-09');D=B/'compiler-expanded-ast-signature-observations';L=B/'compiler-header-lexer-observations';v=json.loads((D/'results-all32.json').read_text());assert v['successfulUnits']==32 and v['incompleteUnits']==0 and len(v['excludedUnits'])==33
rows=[]
for r in v['rows']:
 events=[json.loads(s) for s in Path(r['stdout']).read_text().splitlines()];headers={};exports={};spans={}
 for e in events:
  if e['event']=='expanded_ast_function_header_observation':assert e['defPath'] not in headers;headers[e['defPath']]=e
  if e['event']=='effective_export_observation':assert e['defPath'] not in exports;exports[e['defPath']]=e
  if e['event']=='function_signature_span_observation':assert e['defPath'] not in spans;spans[e['defPath']]=e
 assert set(headers)==set(spans)
 assert all(exports[k]['exported']==h['exported'] and exports[k]['defKind']==h['defKind'] for k,h in headers.items())
 rows.append(dict(index=r['index'],headers=len(headers),expanded=sum(h['fromExpansion'] for h in headers.values()),exported=sum(h['exported'] for h in headers.values()),compilerHeaderSpanSetsEqual=True,effectiveExportJoinEqual=True))
events=[json.loads(s) for s in (L/'axum-core.stdout').read_text().splitlines()];lexed=[e for e in events if e['event']=='compiler_function_header_lexer_observation'];headers={e['defPath']:e for e in events if e['event']=='expanded_ast_function_header_observation'};assert len(lexed)==len(headers)==338
for e in lexed:assert ''.join(t['text'] for t in e['tokens'])==e['headerProjection']==headers[e['defPath']]['headerProjection']
audit=dict(standing='UNREVIEWED FUNCTION-ONLY CROSS-QUERY OBSERVATIONS',successfulUnits=32,excludedUnits=33,functionHeaders=sum(r['headers'] for r in rows),expandedHeaders=sum(r['expanded'] for r in rows),compilerHeaderSpanSetsEqual=True,effectiveExportJoinsEqual=True,lexerHeaderRows=338,allLexerTokensRetained=True,exactHeaderReconstruction=True,rows=rows,originalCompilerASTUnchanged=True,completeSymbolCensus=False,actualFactCandidates=False,signatureTokensQualified=False,sourceAdmission=False,actualC2PlanOrKeys=False,fullSM=False)
(D/'cross-query-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({k:v for k,v in audit.items() if k!='rows'},indent=2))

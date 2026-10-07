from pathlib import Path
import json,hashlib
p=Path('/tmp/opensip-implementation/k2c-literal-shapes-authoring');w=json.loads((p/'literal-shapes-worksheet.json').read_text());spec=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/syntax-e/syn-ns/closure/opensip-interface/grammar/normalizer.v1.json');normalizer=json.loads(spec.read_text());rows={r['grammarId']:r for r in normalizer['rows']};count=nested=0
for entry in w['entries']:
 raw=(p/entry['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==entry['sourceSha256'];assert len(entry['literals'])==entry['expectedLiteralCount'];labels={v['label']:v for v in entry['literals']};rule={v['kind']:v['literalKind'] for v in rows[entry['grammarId']]['literals']}
 grammar=entry['grammarId'];name='tree-sitter-rust' if grammar=='rust' else 'tree-sitter-javascript' if grammar=='javascript' else 'tree-sitter-typescript';rel='src-node-types.json' if grammar in ['rust','javascript'] else grammar+'-src-node-types.json';nodes=json.loads((p/'upstream'/(name+'-'+rel)).read_text());kinds={v['type'] for v in nodes if v['named']}
 for literal in entry['literals']:
  assert raw[literal['startByte']:literal['endByte']].decode()==literal['rawText']==literal['valueText'];assert literal['rawText'].isascii();assert not any(ord(c)<32 or 127<=ord(c)<=159 for c in literal['rawText']);assert rule[literal['nodeKind']]==literal['literalKind'];assert literal['nodeKind'] in kinds;count+=1
  if 'nestedUnder' in literal:
   parent=labels[literal['nestedUnder']];assert parent['startByte']<literal['startByte']<literal['endByte']<parent['endByte'];nested+=1
 assert labels['escaped']['rawText']=='"a\\nb"'
 if grammar!='rust':assert labels['expression']['rawText']=='/ab+/gi' and labels['missing']['literalKind']=='null';assert entry['expectedLiteralCount']==8
 else:assert labels['raw']['nodeKind']=='raw_string_literal' and labels['character']['nodeKind']=='char_literal';assert entry['expectedLiteralCount']==5
assert count==29 and nested==6 and w['parserRuns']==w['producerRuns']==0 and not w['laneFrozen']
report={'standing':'CONDITIONAL LOCAL CANDIDATE RECIPE CHECKS; NOT FINAL ORACLE/FREEZE','ownedSourceFiles':4,'literalRecipes':29,'nestedOverlapRecipes':6,'selectedKindsChecked':True,'asciiTextPreserved':True,'parserRuns':0,'producerRuns':0,'laneFrozen':False,'fullK2cComplete':False,'productQualification':False};(p/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

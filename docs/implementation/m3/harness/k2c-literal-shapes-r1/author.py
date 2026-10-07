from pathlib import Path
import json,hashlib
p=Path('/tmp/opensip-implementation/k2c-literal-shapes-authoring');(p/'fixtures').mkdir(exist_ok=True);rows=[]
for grammar,suffix in [('javascript','js'),('typescript','ts'),('tsx','tsx'),('rust','rs')]:
 rust=grammar=='rust';source='fn literal_shapes() {\n' if rust else 'function literal_shapes() {\n';literals=[]
 values=[('escaped','"a\\nb"','string_literal' if rust else 'string','string')]
 if rust:values.extend([('raw','r#"raw"#','raw_string_literal','string'),('character',"'a'",'char_literal','string'),('yes','true','boolean_literal','boolean'),('no','false','boolean_literal','boolean')])
 else:values.extend([('expression','/ab+/gi','regex','regex'),('yes','true','true','boolean'),('no','false','false','boolean'),('missing','null','null','null'),('templated','`x ${"inner"} ${1}`','template_string','template')])
 for label,raw,kind,literal_kind in values:
  prefix=('    let ' if rust else '  const ')+label+' = ';start=len((source+prefix).encode());source+=prefix+raw+';\n';literals.append({'label':label,'nodeKind':kind,'literalKind':literal_kind,'startByte':start,'endByte':start+len(raw.encode()),'rawText':raw,'valueText':raw})
  if label=='templated':
   for child,child_raw,child_kind,child_literal_kind,offset in [('nested-string','"inner"','string','string',raw.index('"inner"')),('nested-number','1','number','number',raw.index('${1}')+2)]:
    child_start=start+offset;literals.append({'label':child,'nodeKind':child_kind,'literalKind':child_literal_kind,'startByte':child_start,'endByte':child_start+len(child_raw),'rawText':child_raw,'valueText':child_raw,'nestedUnder':'templated'})
 source+='}\n';rel=f'fixtures/literal-shapes.{suffix}';(p/rel).write_text(source);rows.append({'grammarId':grammar,'languageId':'typescript' if grammar=='tsx' else grammar,'path':rel,'sourceSha256':hashlib.sha256(source.encode()).hexdigest(),'expectedLiteralCount':len(literals),'literals':literals,'scope':'conditional local recipes over exact source spans, not parsed facts or admitted atoms'})
w={'standing':'INDEPENDENT LITERAL SHAPE/NESTING RECIPES; NOT FINAL ORACLE OR FREEZE','entries':rows,'rule':'Every literal rule node contributes, including a literal nested within another literal. Exact raw source text is represented; escape syntax and regex flags are not decoded or stripped.','parserRuns':0,'producerRuns':0,'laneFrozen':False,'fullK2cComplete':False,'productQualification':False};(p/'literal-shapes-worksheet.json').write_text(json.dumps(w,indent=2)+'\n');print(json.dumps({'ownedSources':4,'literalRecipes':sum(r['expectedLiteralCount'] for r in rows),'overlappingChildRecipes':sum('nestedUnder' in v for r in rows for v in r['literals']),'parserRuns':0,'producerRuns':0}))

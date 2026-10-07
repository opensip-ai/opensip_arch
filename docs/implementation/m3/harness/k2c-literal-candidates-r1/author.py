from pathlib import Path
import hashlib,json
root=Path('/tmp/opensip-implementation/k2c-literal-candidates-authoring');fixtures=root/'fixtures';fixtures.mkdir(exist_ok=True)
rows=[]
# Hand-selected literal spellings and expected node kinds; no parser-derived label.
for grammar,suffix in [('javascript','js'),('typescript','ts'),('tsx','tsx'),('rust','rs')]:
 rust=grammar=='rust';source='fn literal_spellings() -> i64 {\n' if rust else 'function literal_spellings() {\n';expected=[]
 values=[('plain','1','integer_literal' if rust else 'number'),('fraction','1.0','float_literal' if rust else 'number'),('exponent','1e0','float_literal' if rust else 'number'),('radix','0x1','integer_literal' if rust else 'number'),('grouped','1_000','integer_literal' if rust else 'number')]
 if rust:values.append(('suffixed','1u64','integer_literal'))
 for label,text,kind in values:
  prefix=('    let ' if rust else '  const ')+label+' = ';start=len((source+prefix).encode());source+=prefix+text+';\n';expected.append({'label':label,'nodeKind':kind,'literalKind':'number','startByte':start,'endByte':start+len(text),'rawText':text,'valueText':text})
 # Unary minus is outside the numeric literal node span.
 prefix='    -' if rust else '  return -';start=len((source+prefix).encode());source+=prefix+'1'+('\n' if rust else ';\n')+'}\n';expected.append({'label':'negative-operand','nodeKind':'integer_literal' if rust else 'number','literalKind':'number','startByte':start,'endByte':start+1,'rawText':'1','valueText':'1','unaryMinusIncluded':False})
 rel=f'fixtures/numeric-spellings.{suffix}';(root/rel).write_text(source);raw=source.encode();rows.append({'grammarId':grammar,'languageId':'typescript' if grammar=='tsx' else grammar,'path':rel,'sourceSha256':hashlib.sha256(raw).hexdigest(),'expectedLiteralCount':len(expected),'literals':expected,'scope':'conditional local literal candidate recipes, no facts/anchors/identity/parse outcome admitted'})
# Only already-NFC ASCII and two explicitly hand-owned normalization controls.
representations=[]
for label,raw,step1,step2 in [
 ('c1-control','"a\u0085b"','"a\\u0085b"','"a\\u0085b"'),
 ('literal-escape-text','"a\\u0085b"','"a\\u0085b"','"a\\u0085b"'),
 ('decomposed-accent','"e\u0301"','"e\u0301"','"é"'),
 ('control-before-nfc','"e\u0301\u0001"','"e\u0301\\u0001"','"é\\u0001"'),
 ('4096-char-boundary','"'+'a'*4094+'"','"'+'a'*4094+'"','"'+'a'*4094+'"'),
 ('4097-char-truncation','"'+'a'*4095+'"','"'+'a'*4095+'"','"'+'a'*4095+'"'),
 ('scalar-not-byte-boundary','"'+'é'*4094+'"','"'+'é'*4094+'"','"'+'é'*4094+'"'),
 ('scalar-truncation','"'+'é'*4095+'"','"'+'é'*4095+'"','"'+'é'*4095+'"'),
 ]:
  value=step2 if len(step2)<=4096 else step2[:3996]+'…sha256:'+hashlib.sha256(step2.encode()).hexdigest()
  representations.append({'label':label,'rawUtf8Hex':raw.encode().hex(),'step1Text':step1,'step2NfcText':step2,'step2Characters':len(step2),'step2Utf8Bytes':len(step2.encode()),'valueText':value,'valueCharacters':len(value),'claim':'hand-owned representation vector only; not a parsed file or minted fact'})
# The first pair deliberately has equal valueText and unequal raw source bytes.
assert representations[0]['valueText']==representations[1]['valueText'] and representations[0]['rawUtf8Hex']!=representations[1]['rawUtf8Hex']
worksheet={'standing':'INDEPENDENT LITERAL CANDIDATE/REPRESENTATION RECIPES; NOT FINAL ORACLE OR FREEZE','numericSources':rows,'representationVectors':representations,'representationRule':'escape C0/C1 to uppercase six-character backslash-u; NFC; >4096scalars -> first3996scalars + ellipsis + sha256: + full step2 UTF8 rawSHA256','producerRuns':0,'parserRuns':0,'fullCaseSet':False,'frozen':False,'productQualification':False}
(root/'literal-candidate-worksheet.json').write_text(json.dumps(worksheet,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'ownedSources':len(rows),'numericLiteralRecipes':sum(r['expectedLiteralCount'] for r in rows),'representationVectors':len(representations),'producerRuns':0,'parserRuns':0}))

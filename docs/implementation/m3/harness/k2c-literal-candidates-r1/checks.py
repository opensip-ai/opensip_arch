from pathlib import Path
import json,hashlib,unicodedata
p=Path('/tmp/opensip-implementation/k2c-literal-candidates-authoring');w=json.loads((p/'literal-candidate-worksheet.json').read_text());count=0
for row in w['numericSources']:
 raw=(p/row['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sourceSha256'];assert len(row['literals'])==row['expectedLiteralCount'];count+=len(row['literals'])
 for v in row['literals']:
  assert raw[v['startByte']:v['endByte']].decode()==v['rawText']==v['valueText'];assert v['literalKind']=='number'
  if v['label']=='negative-operand':assert raw[v['startByte']-1:v['startByte']]==b'-' and v['unaryMinusIncluded'] is False
 assert len({v['valueText'] for v in row['literals'] if v['label']!='negative-operand'})==row['expectedLiteralCount']-1
for v in w['representationVectors']:
 raw=bytes.fromhex(v['rawUtf8Hex']).decode();step1=''.join(f"\\u{ord(c):04X}" if ord(c)<=31 or 127<=ord(c)<=159 else c for c in raw);assert step1==v['step1Text'];step2=unicodedata.normalize('NFC',step1);assert step2==v['step2NfcText'];assert len(step2)==v['step2Characters'] and len(step2.encode())==v['step2Utf8Bytes'];value=step2 if len(step2)<=4096 else step2[:3996]+'…sha256:'+hashlib.sha256(step2.encode()).hexdigest();assert value==v['valueText'];assert len(value)==v['valueCharacters'] and len(value)<=4096
 if len(step2)>4096:assert len(value)==4068
assert count==25 and len(w['representationVectors'])==8 and w['parserRuns']==0 and w['producerRuns']==0 and not w['frozen']
report={'standing':'INDEPENDENT CANDIDATE RECIPE CHECKS; NOT FINAL ORACLE OR FREEZE','ownedSourceFiles':4,'numericLiteralRecipes':25,'representationVectors':8,'unicodeOracleVersion':unicodedata.unidata_version,'unicodeOracleScope':'Only explicitly hand-owned ASCII/C0/C1/Latin accent vectors; not a selected product normalization engine','parserRuns':0,'producerRuns':0,'productQualification':False};(p/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

from pathlib import Path
import json,hashlib,datetime
F=Path(__file__).parent;W=Path('/Users/sb/code/opensip-ai/opensip-d4factory-takeover');old=json.loads((F/'constructor-pin-r2/report.json').read_text());deltas=[]
for row in old['allIdentifierOccurrences']:
 source=(W/row['path']).read_text();actual=len(source[:row['byteOffset']].encode('utf-8'))
 if actual!=row['byteOffset']:deltas.append(dict(path=row['path'],line=row['line'],recordedCharacterIndex=row['byteOffset'],actualUtf8ByteOffset=actual))
assert len(deltas)==12
finding=dict(id='LEAD-D4F-R1-OFFSET-1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),standing='ROOT REQUIRED PACKAGING CORRECTION; do not integrate R1 even if independently accepted. Complete current independent review before fresh metadata-only successor.',subjectManifestSha256='5d129b0f2ad4b6563b7f6f15a7403b24c54a699135a3ff135be4cd8ed2f886e4',finding='constructor-pin-r2/report.json labels Python character indices byteOffset. Twelve occurrences follow non-ASCII source text and differ from actual UTF-8 byte offsets.',affected=deltas,sourceCodeChanged=False,sourceLocationsAndCountsChanged=False,typedBehaviorChanged=False,inventoryChanged=False,correction='Preserve characterOffset explicitly and compute byteOffset from original UTF-8 source prefix; assert original raw bytes at the resulting offset start with from_recheck. Correct current constructor report/driver only and retain R1 history. Fresh exact subject/verdict required; no repeated code test/build lane justified by metadata-only change.',rootAssent=False,productQualification=False)
(F/'root-offset-finding-r1.json').write_text(json.dumps(finding,indent=2)+'\n')
s=(F/'check_constructor_pin_r2.py').read_text().replace("B=F/'constructor-pin-r2'","B=F/'constructor-pin-r3'").replace('byteOffset=match.start()','characterOffset=match.start(),byteOffset=len(source[:match.start()].encode(\'utf-8\'))')
s=s.replace("actual={p:sum", "for row in rows:\n assert (W/row['path']).read_bytes()[row['byteOffset']:].startswith(b'from_recheck')\n assert (W/row['path']).read_text()[row['characterOffset']:].startswith('from_recheck')\nactual={p:sum")
s=s.replace('scannedRustFiles=len(rust),',"offsetUnits=dict(characterOffset='Unicode code point index in original source',byteOffset='UTF-8 byte index in original source'),allRawByteOffsetsValidated=True,scannedRustFiles=len(rust),")
(F/'check_constructor_pin_r3.py').write_text(s)
print('Recorded root packaging finding:12offset labels; prepared exact UTF-8 byte/character distinction and raw-byte validation; R1 remains frozen and unassented.')

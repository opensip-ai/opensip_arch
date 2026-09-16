from pathlib import Path
import subprocess,unicodedata,hashlib,json
B=Path(__file__).resolve().parent;P=B/'NormalizationTest-16.0.0.txt';assert unicodedata.unidata_version=='16.0.0';assert P.read_text().startswith('# NormalizationTest-16.0.0.txt')
rows=[];listed=set();part=None;corpus_rows=0
for line in P.read_text().splitlines():
 content=line.split('#')[0].strip()
 if content.startswith('@'):part=content;continue
 if not content:continue
 cols=[''.join(chr(int(x,16))for x in col.split())for col in content.split(';')[:5]];assert len(cols)==5;corpus_rows+=1
 if part=='@Part1':listed.update(map(ord,cols[0]))
 for i,s in enumerate(cols):
  want=cols[1]if i<3 else cols[3];assert unicodedata.normalize('NFC',s)==want
  rows.append((s,want))
remaining=0
for i in range(0x110000):
 if i in listed or 0xd800<=i<=0xdfff:continue
 s=chr(i)
 if unicodedata.category(s)=='Cn':continue
 assert unicodedata.normalize('NFC',s)==s
 rows.append((s,s));remaining+=1
# Allocation/buffer spill checks do not qualify M6 resource envelopes.
rows.extend([('a'*(4*1024*1024),'a'*(4*1024*1024)),('a'+'\u0315\u0300'*1000,unicodedata.normalize('NFC','a'+'\u0315\u0300'*1000))])
with(B/'requests.txt').open('w')as out,(B/'expected.txt').open('w')as expected:
 for s,want in rows:
  out.write(' '.join(format(ord(ch),'x')for ch in s)+'\n');expected.write(str(s==want).lower()+';'+''.join(format(ord(ch),'x')+' 'for ch in want)+'\n')
with(B/'requests.txt').open('rb')as inp,(B/'actual.txt').open('wb')as out,(B/'probe.stderr').open('wb')as err:r=subprocess.run([str(B/'target/debug/unicode-conformance-probe')],stdin=inp,stdout=out,stderr=err,timeout=120)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  while x:=f.read(1024*1024):h.update(x)
 return h.hexdigest()
result={'unicodeVersion':'16.0.0','testDataUrl':'https://www.unicode.org/Public/16.0.0/ucd/NormalizationTest.txt','testDataSha256':sha(P),'normalizationRows':corpus_rows,'nfcColumnCases':corpus_rows*5,'otherAssignedScalars':remaining,'allocationCases':2,'cases':len(rows),'exitCode':r.returncode,'expectedSha256':sha(B/'expected.txt'),'actualSha256':sha(B/'actual.txt'),'standing':'Full official Unicode16 NFC column laws and other-assigned-scalar NFC identity, with is_nfc==iterator==Python. Not other normalization forms or M6 qualification.'}
result['matched']=result['actualSha256']==result['expectedSha256'];(B/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert r.returncode==0 and result['matched']

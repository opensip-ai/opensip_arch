from pathlib import Path
import json, re, hashlib, subprocess
B=Path('/tmp/opensip-implementation/o1-definition-r1-authoring');D=Path('/tmp/opensip-implementation/o1-definition-r1-stage/docs/implementation/m3/operability/o1-definitions-r1')
patterns=json.loads((D/'evidence/credential-pattern-profile.json').read_text())['patterns']
cases=[
 ('inline-p2',{'path':'password=CANARY','count':1},['password=CANARY'],0,1),
 ('url-p2',{'path':'https://user:CANARY@host/x','count':1},['https://user:CANARY@host/x'],0,1),
 ('auth-p2',{'path':'Bearer ABCD','count':1},['Bearer ABCD'],0,1),
 ('mixed',{'path':'password=CANARY','other':'Bearer ABCD'},['password=CANARY'],1,1),
 ('outside-inline',{'other':'password=CANARY'},[],1,0),
 ('outside-url',{'other':'https://user:CANARY@host/x'},[],1,0),
 ('outside-auth',{'other':'Basic abcd'},[],1,0),
 ('quoted-name',{'path':'password="CANARY"','count':1},['password="CANARY"'],0,1),
 ('escaped-controls',{'path':'password=CANARY\nname\u001b[31m'},['password=CANARY\nname\u001b[31m'],0,1),
 ('elided-tail',{'path':{'elided':True,'tail':'password=CANARY'},'count':1},['password=CANARY'],0,1),
 ('two-p2',{'a':'password=CANARY','b':'Bearer ABCD'},['password=CANARY','Bearer ABCD'],0,2),
 ('no-cross-token',{'password':'CANARY','Bearer':'ABCD'},[],0,0),
 ('short-auth',{'other':'Bearer ABC'},[],0,0),
 ('long-s',{'path':'ſecret=CANARY'},['ſecret=CANARY'],0,1),
 ('kelvin',{'path':'APIKEY=CANARY'},['APIKEY=CANARY'],0,1),
 ('feff',{'other':'Bearer\ufeffABCD'},[],1,0),
 ('0085-not-space',{'other':'Bearer\u0085ABCD'},[],0,0),
 ('overlap',{'path':'https://user:password=CANARY@host'},['https://user:password=CANARY@host'],0,2)]
js='var patterns='+json.dumps(patterns,ensure_ascii=False)+';\nvar cases='+json.dumps(cases,ensure_ascii=False)+';\n'+r'''
function tokens(wire) {
 var rows=[];for(var i=0;i<wire.length;i++) {
  if(wire[i]!==String.fromCharCode(34))continue;
  var begin=i; i++;
  while(i<wire.length) {if(wire[i]==='\\'){i+=2;continue;}if(wire[i]===String.fromCharCode(34))break;i++;}
  if(i===wire.length)throw new Error('unclosed');
  rows.push({begin:begin+1,end:i,decoded:JSON.parse(wire.slice(begin,i+1))});
 }return rows;
}
function classify(wire,p2) {
 JSON.parse(wire);var ts=tokens(wire),defects=0,disclosures=0;
 // This synthetic model selects whole token interiors by their declared decoded values.
 // Actual implementation must instead carry sealed byte-coordinate encoder maps.
 var segments=[],last=0;
 ts.forEach(function(t){if(last<t.begin-1)segments.push({decoded:wire.slice(last,t.begin-1),p2:false});segments.push({decoded:t.decoded,p2:p2.indexOf(t.decoded)>=0});last=t.end+1;});
 if(last<wire.length)segments.push({decoded:wire.slice(last),p2:false});
 segments.forEach(function(t){patterns.forEach(function(p){var r=new RegExp(p.expression,p.flags),m;while((m=r.exec(t.decoded))!==null){if(t.p2)disclosures++;else defects++;if(m[0].length===0)throw new Error('zero');}});});
 return {defects:defects,disclosures:disclosures,original:wire};
}
function run() {
 var rows=cases.map(function(c){var wire=JSON.stringify(c[1]),v=classify(wire,c[2]);if(v.defects!==c[3]||v.disclosures!==c[4])throw new Error(c[0]+' '+JSON.stringify(v));JSON.parse(v.original);return {id:c[0],defects:v.defects,disclosures:v.disclosures,lawfulBytesUnchanged:true};});
 return JSON.stringify({standing:'Synthetic token-bounded finite specification vectors, not Rust sealed maps, admitted records or actual sink/corpus controls',rows:rows,productQualification:false},null,2);
}'''
(B/'token-controls.js').write_text(js)
r=subprocess.run(['/usr/bin/osascript','-l','JavaScript',str(B/'token-controls.js')],capture_output=True,check=True)
report=json.loads(r.stdout);(D/'evidence/token-controls.js').write_text(js);(D/'evidence/token-controls.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
guard=json.loads((D/'guard-definition.json').read_text()); marker=guard['lengthMarker'].encode();assert len(marker)==3
def bound(body):
 raw=body.encode()
 if len(raw)+1<=4096:return raw+b'\n',False
 prefix=raw[:4092]
 while True:
  try:prefix.decode();break
  except UnicodeDecodeError:prefix=prefix[:-1]
 return prefix+marker+b'\n',True
rows=[]
for name,body,cut in [('below','x'*4094,False),('exact','x'*4095,False),('above','x'*4096,True),('multibyte','€'*2000,True),('four-byte','😀'*2000,True)]:
 output,did=bound(body);assert did==cut and len(output)<=4096 and output.endswith(b'\n');output.decode();assert not cut or output.endswith(marker+b'\n');rows.append({'id':name,'bytes':len(output),'cut':did,'utf8':True})
original='\x1b[31mhello\t\r\nworld';ansi=re.sub(r'\x1b\[[0-9;]*[A-Za-z]','',original);scrub=''.join(c for c in ansi if ord(c)>31);assert scrub=='helloworld' and ansi=='hello\t\r\nworld'
catalog=json.loads((D/'catalog-definition.json').read_text());members=catalog['members'];assert hashlib.sha256(bytes.fromhex(catalog['preimageHex'])).hexdigest()==catalog['memberDigestRawSha256']
accepted=0
for value in members:assert re.fullmatch(r'[A-Za-z0-9_.:@/+-]{1,128}',value) and len(json.dumps(value).encode())<=130;accepted+=1
negative=['','calls\n','calls\r','calls ','calls\t','x'*129,'callſ','unknown','macOS','linux-x86_64-musl']
for value in negative:assert not(re.fullmatch(r'[A-Za-z0-9_.:@/+-]{1,128}',value) and value in members)
def admit_catalog(entries,verified):
 if not verified or not entries or len(entries)!=len(set(entries)):return 'prerequisite-unavailable'
 if entries!=members:return 'prerequisite-unavailable'
 return 'admitted'
assert admit_catalog([],True)=='prerequisite-unavailable' and admit_catalog(members,False)=='prerequisite-unavailable' and admit_catalog(members+['calls'],True)=='prerequisite-unavailable' and admit_catalog(members,True)=='admitted'
(D/'evidence/definition-controls.json').write_text(json.dumps({'standing':'Design-level finite bound/catalog specification controls only; no actual Rust reader, typed constructor, gate/snapshot, corpus or product execution','boundControls':rows,'ansiBeforeC0':True,'catalogMembersChecked':accepted,'catalogNegativeControls':len(negative),'catalogPrerequisiteCases':4,'tokenCases':len(report['rows']),'productQualification':False},indent=2)+'\n')
print(json.dumps({'tokenVectors':len(report['rows']),'boundControls':len(rows),'catalogMembers':accepted,'catalogNegatives':len(negative),'productQualification':False}))

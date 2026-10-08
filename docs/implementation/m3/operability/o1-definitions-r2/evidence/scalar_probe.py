from pathlib import Path
import json, subprocess
B=Path('/tmp/opensip-implementation/o1-definition-r1-authoring')
D=Path('/tmp/opensip-implementation/o1-definition-r1-stage/docs/implementation/m3/operability/o1-definitions-r1/evidence')
js=r'''function run() {
 var a=[],w=[],s=[],count=0;
 var az=/^[a-z]$/iu, word=/^\w$/iu, space=/^\s$/u;
 for(var cp=0;cp<=0x10ffff;cp++) {
  if(cp>=0xd800 && cp<=0xdfff) continue;
  count++;var ch=String.fromCodePoint(cp);
  if(az.test(ch))a.push(cp);if(word.test(ch))w.push(cp);if(space.test(ch))s.push(cp);
 }
 return JSON.stringify({standing:'Actual pure ECMAScript regular-expression observation across every Unicode scalar; prospective finite profile, no OpenSIP execution',scalars:count,asciiLetterInsensitive:a,wordInsensitive:w,whiteSpace:s,productQualification:false},null,2);
}'''
(B/'scalar-probe.js').write_text(js)
r=subprocess.run(['/usr/bin/osascript','-l','JavaScript',str(B/'scalar-probe.js')],capture_output=True,check=True)
v=json.loads(r.stdout);assert v['scalars']==1112064
assert v['asciiLetterInsensitive']==list(range(65,91))+list(range(97,123))+[383,8490]
assert v['wordInsensitive']==list(range(48,58))+list(range(65,91))+[95]+list(range(97,123))+[383,8490]
assert v['whiteSpace']==[9,10,11,12,13,32,160,5760,*range(8192,8203),8232,8233,8239,8287,12288,65279]
(D/'scalar-probe.js').write_text(js);(D/'scalar-probe.json').write_text(json.dumps(v,indent=2)+'\n')
print(json.dumps({'allScalarControls':v['scalars'],'asciiFoldExtras':[383,8490],'whitespaceMembers':len(v['whiteSpace'])}))

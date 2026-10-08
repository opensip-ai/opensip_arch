function run() {
 var a=[],w=[],s=[],count=0;
 var az=/^[a-z]$/iu, word=/^\w$/iu, space=/^\s$/u;
 for(var cp=0;cp<=0x10ffff;cp++) {
  if(cp>=0xd800 && cp<=0xdfff) continue;
  count++;var ch=String.fromCodePoint(cp);
  if(az.test(ch))a.push(cp);if(word.test(ch))w.push(cp);if(space.test(ch))s.push(cp);
 }
 return JSON.stringify({standing:'Actual pure ECMAScript regular-expression observation across every Unicode scalar; prospective finite profile, no OpenSIP execution',scalars:count,asciiLetterInsensitive:a,wordInsensitive:w,whiteSpace:s,productQualification:false},null,2);
}
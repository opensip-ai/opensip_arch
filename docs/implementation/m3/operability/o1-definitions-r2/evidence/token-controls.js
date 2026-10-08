var patterns=[{"sourceConstant": "URL_USERINFO_RE", "family": "url-userinfo", "expression": "(\\b[a-z][a-z0-9+.-]*:\\/\\/)([^@/\\s:]+):([^@/\\s]+)@", "flags": "giu"}, {"sourceConstant": "AUTH_SCHEME_RE", "family": "auth-scheme", "expression": "\\b(bearer|basic)\\s+([\\w.~+/=-]{4,})", "flags": "giu"}, {"sourceConstant": "INLINE_SECRET_RE", "family": "inline-credential-assignment", "expression": "\\b(password|passwd|pwd|token|api[_-]?key|secret)\\b([\"']?\\s*[:=]\\s*[\"']?)(\\S+)", "flags": "giu"}];
var cases=[["inline-p2", {"path": "password=CANARY", "count": 1}, ["password=CANARY"], 0, 1], ["url-p2", {"path": "https://user:CANARY@host/x", "count": 1}, ["https://user:CANARY@host/x"], 0, 1], ["auth-p2", {"path": "Bearer ABCD", "count": 1}, ["Bearer ABCD"], 0, 1], ["mixed", {"path": "password=CANARY", "other": "Bearer ABCD"}, ["password=CANARY"], 1, 1], ["outside-inline", {"other": "password=CANARY"}, [], 1, 0], ["outside-url", {"other": "https://user:CANARY@host/x"}, [], 1, 0], ["outside-auth", {"other": "Basic abcd"}, [], 1, 0], ["quoted-name", {"path": "password=\"CANARY\"", "count": 1}, ["password=\"CANARY\""], 0, 1], ["escaped-controls", {"path": "password=CANARY\nname\u001b[31m"}, ["password=CANARY\nname\u001b[31m"], 0, 1], ["elided-tail", {"path": {"elided": true, "tail": "password=CANARY"}, "count": 1}, ["password=CANARY"], 0, 1], ["two-p2", {"a": "password=CANARY", "b": "Bearer ABCD"}, ["password=CANARY", "Bearer ABCD"], 0, 2], ["no-cross-token", {"password": "CANARY", "Bearer": "ABCD"}, [], 0, 0], ["short-auth", {"other": "Bearer ABC"}, [], 0, 0], ["long-s", {"path": "ſecret=CANARY"}, ["ſecret=CANARY"], 0, 1], ["kelvin", {"path": "APIKEY=CANARY"}, ["APIKEY=CANARY"], 0, 1], ["feff", {"other": "Bearer﻿ABCD"}, [], 1, 0], ["0085-not-space", {"other": "BearerABCD"}, [], 0, 0], ["overlap", {"path": "https://user:password=CANARY@host"}, ["https://user:password=CANARY@host"], 0, 2]];

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
}
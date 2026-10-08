var patterns = [{"sourceConstant": "URL_USERINFO_RE", "family": "url-userinfo", "expression": "(\\b[a-z][a-z0-9+.-]*:\\/\\/)([^@/\\s:]+):([^@/\\s]+)@", "flags": "giu"}, {"sourceConstant": "AUTH_SCHEME_RE", "family": "auth-scheme", "expression": "\\b(bearer|basic)\\s+([\\w.~+/=-]{4,})", "flags": "giu"}, {"sourceConstant": "INLINE_SECRET_RE", "family": "inline-credential-assignment", "expression": "\\b(password|passwd|pwd|token|api[_-]?key|secret)\\b([\"']?\\s*[:=]\\s*[\"']?)(\\S+)", "flags": "giu"}];
var cases = [["url", "https://user:CANARY@host/x", "https://user:***@host/x"], ["bearer", "Bearer ABCD", "Bearer ***"], ["basic", "Basic a+b_==", "Basic ***"], ["inline", "password=CANARY", "password=***"], ["quoted-inline", "password=\"CANARY\"", "password=\"***"], ["api-key", "api-key: CANARY", "api-key: ***"], ["ordinary", "highentropyCANARYnotaclassifiedshape", "highentropyCANARYnotaclassifiedshape"], ["short-auth", "Bearer ABC", "Bearer ABC"], ["no-word-boundary", "notpassword=CANARY", "notpassword=CANARY"], ["long-s-casefold", "ſecret=CANARY", "ſecret=***"], ["kelvin-casefold", "APIKEY=CANARY", "APIKEY=***"], ["unicode-space", "Bearer ABCD", "Bearer ***"]];
function redact(s) {
 return s.replace(new RegExp(patterns[0].expression, patterns[0].flags), function(match, scheme, user) {return scheme + user + ':***@';})
 .replace(new RegExp(patterns[1].expression, patterns[1].flags), function(match, scheme) {return scheme + ' ***';})
 .replace(new RegExp(patterns[2].expression, patterns[2].flags), function(match, key, sep) {return key + sep + '***';});
}
function run() {
 var rows = cases.map(function(c) {var actual=redact(c[1]); if(actual!==c[2]) throw new Error('case '+c[0]+' mismatch'); return {id:c[0],expected:c[2],actual:actual};});
 var wire = JSON.stringify({fields:{path:'password=CANARY',count:1}});
 var masked=redact(wire);var invalid=false;try {JSON.parse(masked);}catch(e){invalid=true;}
 if(!invalid) throw new Error('Expected naive line-wide pattern boundary defect');
 return JSON.stringify({standing:'ISOLATED PURE ECMASCRIPT REGEX OBSERVATION ONLY; no prototype functions or product code executed',rows:rows,naiveJsonLine:wire,naivelyMasked:masked,naiveLineNoLongerValidJson:invalid,p2TokenContent:'password=CANARY',tokenOnlyMatch: redactedToken(),productCodeChanged:false,productQualification:false},null,2);
}
function redactedToken(){return redact('password=CANARY');}

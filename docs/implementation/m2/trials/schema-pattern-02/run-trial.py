from pathlib import Path
import json,re,shutil,subprocess,hashlib
B=Path('/tmp/opensip-implementation/m2-schema-pattern-trial-02'); O=B.with_name('m2-schema-pattern-trial-01'); assert not B.exists(); B.mkdir();shutil.copytree(O/'probe',B/'probe',ignore=shutil.ignore_patterns('target'));shutil.copy2(O/'pattern-census.json',B/'pattern-census.json')
# Exploratory profile adapter, not a product or general Python-regex translator.
# Only these exact census inputs are being assessed. Dollar and wildcard have
# different line-terminator semantics in Python and ECMAScript.
def adapt(pattern):
 out=[]; in_class=False; escaped=False
 for char in pattern:
  if escaped:out.append(char);escaped=False;continue
  if char=='\\':out.append(char);escaped=True;continue
  if char=='[':in_class=True
  elif char==']':in_class=False
  if not in_class and char=='$':out.append(r'(?=\n?(?![\s\S]))')
  elif not in_class and char=='.':out.append(r'[^\n]')
  else:out.append(char)
 assert not escaped and not in_class
 return ''.join(out)
patterns=[r['pattern'] for r in json.loads((O/'pattern-census.json').read_bytes())['patterns']];mapping={p:adapt(p) for p in patterns};(B/'adaptations.json').write_text(json.dumps(mapping,indent=2)+'\n')
cases=[json.loads(line) for line in (O/'cases.jsonl').read_bytes().splitlines()]
# Target each permissive wildcard in the selected unescaped security domains;
# include each line terminator and ordinary scalar rather than testing only IDs.
extra=set()
for stem in ['security.repo-execution-grant.v2','security.repo-execution-grants.v2']:
 for i,c in enumerate(stem):
  if c=='.':
   for x in ['\n','\r','\r\n','\u2028','\u2029','\u0085','\v','\f','.', 'x', '😀']:
    extra.add(stem[:i]+x+stem[i+1:]+':'+'a'*64)
for prefix in ['', 'a/', 'a\r/', 'a\u2028/', 'a\u2029/', 'a\n/']:
 for part in ['.', '..', '...']:
  for end in ['', '\n','\r','\r\n','\u2028','\u2029','\n\n']:
   extra.add(prefix+part+end)
cases += [{'pattern':p,'text':s} for p in patterns for s in sorted(extra)]
raw=''.join(json.dumps({'pattern':mapping[c['pattern']],'text':c['text']},ensure_ascii=True,separators=(',',':'))+'\n' for c in cases).encode();(B/'cases-adapted.jsonl').write_bytes(raw)
expected=[bool(re.search(c['pattern'],c['text'])) for c in cases]
cargo='/opt/homebrew/Cellar/rust/1.95.0/bin/cargo';r=subprocess.run([cargo,'build','--locked','--offline','--manifest-path',str(B/'probe/Cargo.toml')],capture_output=True,timeout=300);(B/'build.stdout').write_bytes(r.stdout);(B/'build.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr.decode()
r=subprocess.run([str(B/'probe/target/debug/opensip-schema-pattern-trial')],input=raw,capture_output=True,timeout=180);(B/'probe.stdout').write_bytes(r.stdout);(B/'probe.stderr').write_bytes(r.stderr);assert r.returncode==0;actual=r.stdout.splitlines();assert len(actual)==len(cases)
mis=[{**c,'adaptedPattern':mapping[c['pattern']],'pythonReference':e,'regressUnicode':a.decode()} for c,e,a in zip(cases,expected,actual) if a==b'E' or (a==b'1')!=e]
(B/'mismatches.json').write_text(json.dumps(mis,indent=2)+'\n');result={'standing':'Exploratory exact-selected-pattern adapter trial. Not general regex compatibility, runtime schema selection, product implementation or resource-bound proof.','patterns':len(patterns),'adaptedPatterns':sum(k!=v for k,v in mapping.items()),'cases':len(cases),'mismatches':len(mis),'compileErrorCases':sum(a==b'E' for a in actual),'adaptation':'Outside character classes and escapes, Python dollar becomes optional-one-final-LF assertion; wildcard dot becomes non-LF scalar class. No other syntax adaptation claimed.','productChanged':False};(B/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

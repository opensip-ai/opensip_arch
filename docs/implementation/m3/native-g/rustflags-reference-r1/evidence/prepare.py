from pathlib import Path
import json,hashlib,ast,re
b=Path('/tmp/opensip-implementation/rustflags-reference-authoring');a=Path('/Users/sb/code/opensip-ai/opensip_arch');rel='docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py';s=(a/rel).read_text();old=s
for before,after in [('_CFG_RE = re.compile(r\'^[A-Za-z_][A-Za-z0-9_]*(="[^"\\\\]*")?$\')','_CFG_RE = re.compile(r\'^[A-Za-z_][A-Za-z0-9_]*(="[^"\\\\]*")?\\Z\')'),("_LINT_RE = re.compile(r'^[a-z0-9_:]+$')","_LINT_RE = re.compile(r'^[a-z0-9_:]+\\Z')"),("_ALLOWED_C_VALUES = re.compile(r'^[A-Za-z0-9_+,\\-.=]+$')","_ALLOWED_C_VALUES = re.compile(r'^[A-Za-z0-9_+,\\-.=]+\\Z')")]:
 assert s.count(before)==1,before;s=s.replace(before,after)
before='''        elif f.startswith("--cap-lints=") or f.startswith(("-A", "-W", "-D", "-F")) and len(f) > 2 and _LINT_RE.match(f[2:]):
            honored.append(f); i += 1'''
after='''        elif f.startswith("--cap-lints="):
            value = f[len("--cap-lints="):]
            (honored.append(f) if value in ("allow", "warn", "deny", "forbid") else stripped.append({"flag": f, "reason": "cap-lints-value"})); i += 1
        elif f.startswith(("-A", "-W", "-D", "-F")) and len(f) > 2 and _LINT_RE.match(f[2:]):
            honored.append(f); i += 1'''
assert s.count(before)==1;s=s.replace(before,after);assert s.replace(after,before).replace("?\\Z')","?$')").replace("_:]+\\Z')","_:]+$')").replace("\\-.=]+\\Z')","\\-.=]+$')")==old
ast.parse(s);(b/'native_evidence_model.v2.py').write_text(s)
(b/'preparation.json').write_text(json.dumps(dict(parent=dict(path=rel,bytes=len(old.encode()),sha256=hashlib.sha256(old.encode()).hexdigest()),patches=4,productUnchanged=True,scope='inline cap-lints named value validation and exact end anchors only; not full rustflags conformance'),indent=2)+'\n')
print('Four exact source changes prepared; original model untouched.')

from pathlib import Path
import hashlib,json
b=Path('/tmp/opensip-implementation/rustflags-long-lint-authoring');a=Path('/Users/sb/code/opensip-ai/opensip_arch');rel='docs/implementation/m3/native-g/rustflags-reference-r1/reference/native_evidence_model.v2.py';raw=(a/rel).read_bytes();assert hashlib.sha256(raw).hexdigest()=='4c3f78a9c43102ed391430a9ec8fd84f0d31535a2e0beb366035c14887a8907e'
s=raw.decode();needle='''        elif f.startswith("--cap-lints="):
''';branch='''        elif f.startswith(("--allow=", "--warn=", "--deny=", "--forbid=")):
            value = f.split("=", 1)[1]
            (honored.append(f) if _LINT_RE.match(value) else stripped.append({"flag": f, "reason": "lint-syntax"})); i += 1
''';assert s.count(needle)==1;s=s.replace(needle,branch+needle);assert s.replace(branch,'').encode()==raw
(b/'native_evidence_model.v2.py').write_text(s)
(b/'authority.json').write_text(json.dumps(dict(parent=dict(path=rel,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),sitesChanged=1,productEdited=False,qualification=False),indent=2)+'\n');print('Prospective long-lint reference copy authored; accepted r1 unchanged.')

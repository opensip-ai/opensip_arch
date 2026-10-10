from pathlib import Path
import re,hashlib,json
W=Path('/Users/sb/code/opensip-ai/opensip-native-public');p=W/'crates/identity/src/schema_registry.rs';text=p.read_text();changed=[]
for source in [f'schemas/sources/common-v{v}.schema.json' for v in (1,3,4)]+['schemas/sources/native-v2.schema.json']:
    raw=(W/source).read_bytes();digest=hashlib.sha256(raw).digest()
    pattern=r'(SourcePin \{\s*id: "[^"]+",\s*path: "'+re.escape(source)+r'",\s*bytes: )\d+(,\s*sha256: \[)[\d,\s]+(\],\s*\})'
    text,count=re.subn(pattern,lambda m:m[1]+str(len(raw))+m[2]+', '.join(str(v) for v in digest)+',\n        '+m[3],text)
    assert count==1,source;changed.append(dict(path=source,bytes=len(raw),sha256=digest.hex()))
p.write_text(text)
closure=json.loads((W/'tools/contracts/generator-closure.json').read_bytes());assert p.relative_to(W).as_posix() not in [r['path'] for r in closure['files']]
(Path('/tmp/opensip-implementation/native-publication-r1')/'compiled-registry-repin.json').write_text(json.dumps(dict(changedSources=changed,unchangedClosedSourceSet=True),indent=2)+'\n')
print('Updated four existing compiled full-document source pins; no source-set or alias expansion.')

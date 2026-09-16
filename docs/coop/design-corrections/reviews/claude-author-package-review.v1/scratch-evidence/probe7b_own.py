
import importlib.util,json,base64
from pathlib import Path
PKG=Path('/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2')
F=Path('/tmp/opensip-design-corrections/candidate-subject.v25/docs/coop/design-corrections/foundation')
s=importlib.util.spec_from_file_location('mi',F/'identity-model.v3.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
d=json.loads((PKG/'normalized-examples6/rust.store.json').read_text())
b={k:base64.b64decode(v) for k,v in d['blobs'].items()}
hexd='6c50818b7f6d971ae875c229a987b6f667c893b1f87a3573eaf59d1415d8136d'
raw=b[hexd]
print('len',len(raw))
print('first 160 bytes repr:',repr(raw[:160]))
print()
print('domainSets keys:',list(M.DIGESTS['domainSets'].keys())[:20])
for k,v in M.DIGESTS['domainSets'].items():
    if any('ownership' in str(x) for x in v): print('OWNERSHIP SET',k,v)

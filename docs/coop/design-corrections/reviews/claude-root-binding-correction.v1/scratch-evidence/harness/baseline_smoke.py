import importlib.util,json,sys
from pathlib import Path
BASE=Path(sys.argv[1])
N=BASE/'docs/coop/design-corrections/native/native_evidence_model.v2.py'
s=importlib.util.spec_from_file_location('nev',N);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
markers={'tsconfig.json':{'sha256':'a'*64},'crates/alpha/Cargo.toml':{'sha256':'b'*64}}
disc=M.discover_units(markers)
print('discover refused:',disc['refused'])
for u in disc['units']: print('  unit rootPath=',repr(u['rootPath']),u['languageFamily'],u['languageMode'],'members',u['memberPackageRoots'])
files=['index.ts','src/a.ts','crates/alpha/src/lib.rs']
mem=M.assign_membership(disc['units'],files)
for r in mem['rows']: print('  row',r['path'],r['membership'],r['reason'],r['unitOrdinal'])

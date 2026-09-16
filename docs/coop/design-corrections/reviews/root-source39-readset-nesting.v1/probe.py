"""Check VCS exclusions inside an otherwise admitted dependency read set."""
from pathlib import Path
import argparse, hashlib, importlib.util, json
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
S=a.source.resolve();O=a.out.resolve();O.mkdir(parents=True,exist_ok=False)
F=S/'docs/coop/design-corrections/foundation'
s=importlib.util.spec_from_file_location('root_nested_readset',F/'check-native-consumer24-corrections.v1.py');K=importlib.util.module_from_spec(s);s.loader.exec_module(K)
rows=[]
for path in ['node_modules/left-pad/index.js','node_modules/left-pad/.git/HEAD','node_modules/left-pad/.hg/store/data','node_modules/left-pad/.git-like/index.js']:
    graph=K.SR.S.build_ts_semantic_graph(atom=K.SR.REFS_EXISTS_SRC,has_declares=False,has_references_fact=True,extra_sources={path:b'export const x=1;\n'})
    try:
        result=K.SR.close_positive(graph)
        rows.append({'path':path,'outcome':'RETURNED','result':result})
    except Exception as exc:rows.append({'path':path,'outcome':'REFUSE','exceptionType':type(exc).__name__,'reason':str(exc)})
report={'standing':'Root full-Run read-set nesting probes. Capture only; no aggregate acceptance or product qualification.','source':str(S),'modelSha256':hashlib.sha256((F/'identity-model.v3.py').read_bytes()).hexdigest(),'cases':rows}
(O/'report.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
for r in rows:print(r['path'],r['outcome'],r.get('reason',''))

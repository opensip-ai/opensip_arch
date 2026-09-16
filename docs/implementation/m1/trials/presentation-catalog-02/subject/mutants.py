"""Root02 behavioral controls; no independent review, product or custody proof."""
from pathlib import Path
import json,shutil,subprocess,tempfile
ROOT=Path(__file__).resolve().parent
FILES=['catalog.py','build_schema.py','check.py','input-pins.json','presentation-catalog.schema.json']
sites=[
 ('release-closure','catalog.py',"        require(authority['closureId'] == admitted['closureId'], 'CATALOG.RELEASE-CLOSURE')\n",'',False),
 ('release-registry','catalog.py',"    require(digest == selection['registrySha256'], 'CATALOG.RELEASE-REGISTRY')\n",'',False),
 ('release-plan-closure','catalog.py',"    require(selection['catalogClosureId'] in selection['semanticClosureIds'], 'CATALOG.RELEASE-PLAN-CLOSURE')\n",'',False),
 ('run-selection','catalog.py',"        require(set(selected[group]) <= set(run_selection[group]), 'CATALOG.RUN-SELECTION')\n",'',False),
 ('selected-declaration','catalog.py',"        require(set(selected[group]) <= receipt['declared'][group], 'CATALOG.SELECTED-UNDECLARED')\n",'        pass\n',False),
 ('delivery-tree-absence','catalog.py',"        require(not blobs, 'CATALOG.CLOSURE-TREE')\n",'',False),
 ('platform','catalog.py',"    require(closure['platform'] == admitted['selectedPlatform'], 'CATALOG.PLATFORM')\n",'',False),
 ('missing-descriptor-label','catalog.py',"'reason': 'descriptor-not-declared'","'reason': 'descriptor-not-retained'",False),
 ('CAT-M6-undeclared-capabilities','catalog.py',"        require(set(keys) <= declared[group], 'CATALOG.UNDECLARED-KEY')\n","        if group != 'capabilities': require(set(keys) <= declared[group], 'CATALOG.UNDECLARED-KEY')\n",False),
 ('CAT-M3-canonical-cap','catalog.py',"    reference.canonical(data)\n",'',True),
]
PYTHON='/tmp/opensip-implementation/metadata-reference-env/bin/python'
work=Path(tempfile.mkdtemp(prefix='opensip-catalog02-controls-'))
rows=[]
for name,file,before,after,redundant in sites:
 dst=work/name;dst.mkdir()
 for item in FILES:shutil.copy2(ROOT/item,dst/item)
 p=dst/file;s=p.read_text();assert s.count(before)==1,(name,s.count(before));p.write_text(s.replace(before,after))
 run=subprocess.run([PYTHON,'-I','-B','check.py'],cwd=dst,capture_output=True,text=True)
 caught=run.returncode==1 and 'FAIL:' in run.stderr and 'ERROR:' not in run.stderr
 rows.append({'id':name,'exit':run.returncode,'caught':caught,'expectedRedundant':redundant,'classification':'raw-cap subsumes canonical-cap; requires independent confirmation' if redundant else 'behavioral guard','stdout':run.stdout,'stderr':run.stderr})
 print(name,run.returncode,'caught' if caught else 'survived')
result={'standing':'root02 controls, no independent acceptance','work':str(work),'rows':rows,'expectedResults':all(r['caught'] if not r['expectedRedundant'] else r['exit']==0 for r in rows)}
(ROOT/'mutant-results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['expectedResults'] else 1)

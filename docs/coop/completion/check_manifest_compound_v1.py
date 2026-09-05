"""Retained compound optional-tree cases resolving MCR-S1; design only."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
B=Path(__file__).resolve().parent

def main(output):
    path=B/'check_manifest_completed_v1.py'
    spec=importlib.util.spec_from_file_location('manifest_compound_subject',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    bases=json.loads((B/'manifest-bases.completed.v1.json').read_text())
    blobs=json.loads((B/'manifest-artifact-blobs.completed.v1.json').read_text())
    manifest=copy.deepcopy(bases['security-full']);root=manifest['name']
    manifest['commands'].extend([
        {'name':'left','description':'Left branch','parent':root},
        {'name':'right','description':'Right branch','parent':root},
        {'name':'child','description':'Child under left','parent':'left'},
        {'name':'child','description':'Child under right','parent':'right'}])
    cases=[('same-child-name-in-distinct-parents',copy.deepcopy(manifest),'ACCEPT')]
    manifest['commands'].append({'name':'leaf','description':'Ambiguous parent','parent':'child'})
    cases.append(('ambiguous-unqualified-parent',manifest,'RJ-2'))
    results=[]
    for name,value,expected in cases:
        raw=json.dumps(value,separators=(',',':'),ensure_ascii=True).encode()
        try: actual=module.validate(raw,{},bases,blobs)['verdict']
        except module.Refuse as error:actual=error.code
        assert actual==expected,(name,expected,actual)
        results.append({'case':name,'input':value,'inputSha256':hashlib.sha256(raw).hexdigest(),'expected':expected,'actual':actual})
    inputs=[Path(__file__),path,B/'manifest-bases.completed.v1.json',B/'manifest-artifact-blobs.completed.v1.json',B/'manifest-completed.independent-review.v1.json']
    report={'kind':'MANIFEST-COMPOUND-DESIGN-CASES','finding':'MCR-S1','qualification':False,'count':len(results),'passed':len(results),'results':results,'inputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
    Path(output).write_text(json.dumps(report,indent=2)+'\n');print({'passed':len(results),'count':len(results)})
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--report',required=True);main(p.parse_args().report)

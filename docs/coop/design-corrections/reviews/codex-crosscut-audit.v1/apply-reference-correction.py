"""Apply an author proposal ONLY to a separate copy of candidate25."""
import argparse, hashlib, json, difflib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--copy',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
assert a.source.resolve()!=a.copy.resolve();a.out.mkdir(exist_ok=True)
D='docs/coop/design-corrections/'
changes={
D+'discovery-defaults.py':[
 ('def enumerate_units(marker_relpaths: Iterable[str]) -> dict:', 'def enumerate_units(marker_relpaths: Iterable[str], *, enforce_limit: bool = True) -> dict:'),
 ('    if len(unit_dirs) > MAX_WORKSPACE_UNITS:', '    if enforce_limit and len(unit_dirs) > MAX_WORKSPACE_UNITS:'),
 ('    Zero-config', '    Zero-config')],
D+'security/security_lifecycle_model_v1.py':[
 ('enum = DD.enumerate_units(_relative_marker_paths(root))','enum = DD.enumerate_units(_relative_marker_paths(root), enforce_limit=False)'),
 ("            if enum['refusal'] is not None:\n                return refuse('PROJECT.WORKSPACE_UNIT_LIMIT', root,\n                              'WORKSPACE_UNIT_LIMIT:%d>%d' % (enum['refusal']['unitCount'], enum['refusal']['limit']))\n",''),
 ("                prov['units'].append({'path': d, 'kind': 'workspace-auto', 'markers': markers})\n        return {'status': 'ACCEPT', 'provenance': prov}", "                prov['units'].append({'path': d, 'kind': 'workspace-auto', 'markers': markers})\n            # Count admitted project units after authority/custody exclusions.\n            unit_count = len(prov['units'])\n            if unit_count > DD.MAX_WORKSPACE_UNITS:\n                prov['units'] = []\n                return refuse('PROJECT.WORKSPACE_UNIT_LIMIT', root,\n                              'WORKSPACE_UNIT_LIMIT:%d>%d' % (unit_count, DD.MAX_WORKSPACE_UNITS))\n        return {'status': 'ACCEPT', 'provenance': prov}")],
D+'native/native_evidence_model.v2.py':[
 ('enum = DD.enumerate_units(markers)', 'enum = DD.enumerate_units(markers, enforce_limit=False)'),
 ('    if enum["refusal"] is not None:\n        return refused("native.too-many-units", [], unitCount=enum["refusal"]["unitCount"], limit=enum["refusal"]["limit"])\n',''),
 ('    provenance = "EXPLICIT" if explicit_workspace_roots is not None else "DISCOVERED"', '    # Apply the directory cap only after boundary and explicit-root selection.\n    if len(by_dir) > MAX_WORKSPACE_UNITS:\n        return refused("native.too-many-units", [], unitCount=len(by_dir), limit=MAX_WORKSPACE_UNITS)\n    provenance = "EXPLICIT" if explicit_workspace_roots is not None else "DISCOVERED"'),
 ('# unreachable after enumerate_units; kept as the stated bound', '# defensive guard after selected-directory admission')]
}
# No-op prose sentinel is intentionally omitted; every actual replacement must be unique.
changes[D+'discovery-defaults.py']=changes[D+'discovery-defaults.py'][:2]
rows=[]
for rel,replacements in changes.items():
 original=(a.source/rel).read_text(); target=a.copy/rel
 assert target.read_text()==original,rel
 updated=original
 for before,after in replacements:
  assert updated.count(before)==1,(rel,before[:80],updated.count(before));updated=updated.replace(before,after)
 target.chmod(target.stat().st_mode|0o200);target.write_text(updated)
 patch=''.join(difflib.unified_diff(original.splitlines(True),updated.splitlines(True),fromfile=rel,tofile=rel))
 (a.out/(target.name+'.patch')).write_text(patch)
 (a.out/target.name).write_text(updated)
 rows.append({'path':rel,'beforeSha256':hashlib.sha256(original.encode()).hexdigest(),'afterSha256':hashlib.sha256(updated.encode()).hexdigest()})
(a.out/'changed-source.json').write_text(json.dumps({'standing':'AUTHOR PROPOSAL; no accepted source changed','files':rows},indent=2)+'\n')
print('Prepared three-file isolated reference correction.')

"""Product configuration resolution reference, after trusted carrier/discovery admission.
Does not implement filesystem custody, framework discovery or component installation.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('config_canonical',H/'canonical.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
SCHEMA=json.loads((H/'product-configuration.schema.v2.json').read_text())
def resolve(layers,registry,ci=False):
    # registry is the authenticated selected release declaration registry.
    allowed=['defaults','global','project','local','flags']
    if set(layers)-set(allowed):raise C.AdmissionError('CONFIG_LAYER')
    resolved={};provenance={}
    for name in allowed:
        if name=='local' and ci:continue  # carrier must not even probe local input in CI
        raw=layers.get(name)
        if raw is None:continue
        value=C.parse(raw);C.validate(SCHEMA,value)
        for group,record in value.items():
            if group=='schemaVersion':continue
            for field,item in record.items():
                resolved.setdefault(group,{})[field]=copy.deepcopy(item);provenance[group+'.'+field]=name
    for name in ['entryPoints','workspaceRoots','ignorePaths']:
        for value in resolved.get('discovery',{}).get(name,[]):
            if value == '.' and name in ('workspaceRoots', 'ignorePaths'):
                continue
            if value.startswith('/') or '\\' in value or '\x00' in value or any(p in ['', '.', '..'] for p in value.split('/')):raise C.AdmissionError('CONFIG_LOGICAL_PATH')
    analysis=resolved.get('analysis',{})
    if 'profileId' not in analysis:raise C.AdmissionError('CONFIG_PROFILE_MISSING')
    if analysis.get('profileId') not in registry['profiles']:raise C.AdmissionError('CONFIG_PROFILE_UNREGISTERED')
    if any(v not in registry['capabilities'] for v in analysis.get('capabilities',[])):raise C.AdmissionError('CONFIG_CAPABILITY_UNREGISTERED')
    if any(v not in registry['packs'] for v in resolved.get('policy',{}).get('packIds',[])):raise C.AdmissionError('CONFIG_PACK_UNREGISTERED')
    if any(v not in registry.get('waivers',[]) for v in resolved.get('policy',{}).get('waiverIds',[])):raise C.AdmissionError('CONFIG_WAIVER_UNREGISTERED')
    for field in ['request','pins','holds']:
        values=resolved.get('components',{}).get(field,[]);keys=[v['stableId'] for v in values]
        if len(set(keys))!=len(keys):raise C.AdmissionError('CONFIG_DUPLICATE_COMPONENT')
    if not {'profileId','capabilities','budget'} <= set(analysis):raise C.AdmissionError('CONFIG_DEFAULTS_INCOMPLETE')
    semantics={k:copy.deepcopy(resolved.get(k,{})) for k in ['analysis','components','discovery','policy','evidence']}
    # Presentation and custody choices have their own operational admission and
    # never silently become analyzer inputs. All meaningful array sets sort here;
    # source winning arrays/provenance stay available unchanged for explanation.
    def normalize(v,key=''):
        if type(v) is dict:return {k:normalize(x,k) for k,x in v.items()}
        if type(v) is list:
            if key=='allowedScopes':return copy.deepcopy(v) # declared priority sequence
            return sorted([normalize(x) for x in v],key=C.canonical)
        return v
    semantics=normalize(semantics)
    schema=json.loads((H/'identity-schemas.v2.json').read_text());schema['$ref']='#/$defs/semantic-configuration'
    C.validate(schema,semantics)
    return {'resolved':resolved,'provenance':provenance,'semantic':semantics,'resolvedConfigDigest':hashlib.sha256(C.canonical(semantics)).hexdigest()}

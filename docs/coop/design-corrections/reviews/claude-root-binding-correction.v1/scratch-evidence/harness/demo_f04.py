import importlib.util,json,sys,copy
from pathlib import Path
BASE=Path(sys.argv[1]); OUT=sys.argv[2]
def load(n,pp):
    s=importlib.util.spec_from_file_location(n,pp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
NVP=BASE/'docs/coop/design-corrections/native/native_evidence_model.v2.py'
ENP=BASE/'docs/coop/design-corrections/foundation/enumeration_model.v1.py'
NV=load('nv',NVP); EN=load('en',ENP)
res={'tree':str(BASE),'cases':[]}
def rec(name,**kw):
    row={'case':name}; row.update(kw); res['cases'].append(row); return row
def unit(root,fam='tsjs',mode='ts-tsconfig',kind='ts-program',marker='tsconfig.json',ordinal=0,members=None):
    return {'unitOrdinal':ordinal,'rootPath':root,'languageFamily':fam,'languageMode':mode,'unitKind':kind,
            'markerPath':marker,'markerSha256':'0'*64,'recognizerId':'typescript-config','recognizerVersion':1,
            'provenance':'DISCOVERED','memberPackageRoots':members or []}
FILES=['index.ts','src/a.ts','src/b.ts']
def try_membership(units,files=None):
    try:
        m=NV.assign_membership(copy.deepcopy(units), list(files or FILES))
        return {'outcome':'RETURNED','rows':[{'path':r['path'],'membership':r['membership'],'reason':r['reason']} for r in m['rows']]}
    except Exception as e:
        return {'outcome':'REFUSED','error':type(e).__name__,'message':str(e)[:220]}
def try_scope(units):
    try:
        d=NV.unit_scope_descriptor(copy.deepcopy(units),[])
        return {'outcome':'RETURNED','workspaceRoots':d['scopeDescriptor']['workspaceRoots'],'scopeDigest':d['scopeDigest']}
    except Exception as e:
        return {'outcome':'REFUSED','error':type(e).__name__,'message':str(e)[:220]}
def try_caps(units):
    reg=[]
    try:
        NV.default_capability_selection(copy.deepcopy(units),reg)
        return {'outcome':'RETURNED'}
    except Exception as e:
        return {'outcome':'REFUSED','error':type(e).__name__,'message':str(e)[:220]}
def schema_ok(defname,value):
    try:
        NV.validate_native(defname,value); return True
    except Exception as e:
        return False

# C1 lawful project root
u_ok=[unit('')]
rec('C1-lawful-project-root', schemaValid=schema_ok('WorkspaceUnitV2',u_ok[0]), membership=try_membership(u_ok), scope=try_scope(u_ok))
# C2 external sentinel as internal root
u_dot=[unit('.')]
rec('C2-sentinel-dot-root', schemaValid=schema_ok('WorkspaceUnitV2',u_dot[0]), membership=try_membership(u_dot), scope=try_scope(u_dot), caps=try_caps(u_dot))
# C3 trailing slash
u_ts=[unit('src/')]
rec('C3-trailing-slash-root', schemaValid=schema_ok('WorkspaceUnitV2',u_ts[0]), membership=try_membership(u_ts))
# C4 empty interior segment
u_es=[unit('src//deep')]
rec('C4-empty-segment-root', schemaValid=schema_ok('WorkspaceUnitV2',u_es[0]), membership=try_membership(u_es))
# C5 member package root with sentinel
u_m=[unit('', fam='rust', mode='rust-cargo', kind='cargo-workspace', marker='Cargo.toml', members=['.'])]
rec('C5-sentinel-member-root', schemaValid=schema_ok('WorkspaceUnitV2',u_m[0]), membership=try_membership(u_m,['crates/alpha/src/lib.rs']))
# C6 nested + co-located TS/Rust, all lawful
u_co=[unit('',ordinal=0), unit('',fam='rust',mode='rust-cargo',kind='cargo-workspace',marker='Cargo.toml',ordinal=1,members=['crates/alpha']), unit('src/inner',ordinal=2)]
rec('C6-colocated-and-nested', schemaValid=all(schema_ok('WorkspaceUnitV2',x) for x in u_co),
    membership=try_membership(u_co,['index.ts','src/inner/x.ts','crates/alpha/src/lib.rs']), scope=try_scope(u_co))
# C7 enumeration binding misattribution
def enum_probe(root):
    mem={'units':[unit(root)],'rows':[]}
    faults=[]
    guarded=None
    if hasattr(EN,'_admit_membership_unit_roots'):
        guarded=EN._admit_membership_unit_roots(mem,faults)
    found=EN._unit_for_cell(mem,'.','ts-tsconfig')
    derived=EN._u1_entry(found,'ts-tsconfig')
    retained='tsconfig.json'
    return {'rootGuardPresent':hasattr(EN,'_admit_membership_unit_roots'),'rootGuardPassed':guarded,
            'rootGuardFaults':faults,'unitForCell':('FOUND' if found else None),'derivedU1Entry':derived,
            'retainedEntryConfigPath':retained,
            'bindingFaultWithoutGuard':(None if derived==retained else 'ENUMERATION_BINDING_PROGRAM_ENTRY')}
rec('C7-enum-binding-attribution-empty-root', probe=enum_probe(''))
rec('C7-enum-binding-attribution-dot-root', probe=enum_probe('.'))
# C8 ownership round trip on lawful units
own_units=[{'unitId':None,'crateName':'alpha','markerPath':'crates/alpha/Cargo.toml','targetKind':'lib','targetName':'alpha','targetEdition':None},
           {'unitId':None,'crateName':'alpha','markerPath':'crates/alpha/Cargo.toml','targetKind':'bin','targetName':'alpha-bin','targetEdition':2021}]
try:
    for x in own_units: x['unitId']=NV.source_unit_id(x)
    rec2={'schemaVersion':1,'enumeration':'complete',
          'units':own_units,
          'ownership':[{'path':'crates/alpha/src/shared.rs','unitId':own_units[0]['unitId']},
                       {'path':'crates/alpha/src/shared.rs','unitId':own_units[1]['unitId']}],
          'selectedUnitIds':[own_units[0]['unitId']]}
    valid=schema_ok('SourceUnitOwnershipV1',rec2)
    reid=[NV.source_unit_id(x)==x['unitId'] for x in own_units]
    rec('C8-ownership-roundtrip', outcome='RETURNED', schemaValid=valid, unitIdsReDerive=reid,
        projections=[NV.unit_identity_projection(x) for x in own_units],
        ownershipIdentity=NV.source_unit_ownership_identity(rec2))
except Exception as e:
    rec('C8-ownership-roundtrip', outcome='ERROR', error=type(e).__name__, message=str(e)[:220])
# C9 no new public D9 code is possible
try:
    NV.d9_map('native.unit-root-representation')
    rec('C9-invented-public-d9', outcome='ACCEPTED-UNEXPECTED')
except Exception as e:
    rec('C9-invented-public-d9', outcome='REFUSED', error=type(e).__name__, message=str(e)[:220])
# C10 external boundary unchanged
try:
    norm=NV.DD.normalize_explicit_root('.')
    rec('C10-external-root-normalizes-inward', outcome='RETURNED', normalized=repr(norm), spelledBack=repr(NV.DD.spell_root(norm)))
except Exception as e:
    rec('C10-external-root-normalizes-inward', outcome='ERROR', message=str(e)[:220])
try:
    NV.DD.normalize_explicit_root('a/../b')
    rec('C11-external-malformed-root', outcome='ACCEPTED-UNEXPECTED')
except Exception as e:
    rec('C11-external-malformed-root', outcome='REFUSED', error=type(e).__name__, message=str(e)[:160])
# C12 discovery still produces lawful internal roots
d=NV.discover_units({'tsconfig.json':{'sha256':'a'*64},'crates/alpha/Cargo.toml':{'sha256':'b'*64}})
rec('C12-discovery-internal-roots', refused=d['refused'], roots=[u['rootPath'] for u in d['units']],
    membership=try_membership(d['units'],['index.ts','crates/alpha/src/lib.rs']))
json.dump(res,open(OUT,'w'),indent=1)
print(json.dumps(res,indent=1))

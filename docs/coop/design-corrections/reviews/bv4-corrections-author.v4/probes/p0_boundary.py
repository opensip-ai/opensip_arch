"""Pre-edit reproduction of root's default-cardinality probe, plus the questions root left open:
is the overflow reachable only through the default helper, and does any existing law own it?"""
import importlib.util,json,pathlib,sys
DC=pathlib.Path(sys.argv[1])
s=importlib.util.spec_from_file_location('n',DC/'native/native_evidence_model.v2.py');N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
IM=N.IM
out={}
CAPS=len(N.required_default_capabilities('ts-tsconfig'))
BOUND=IM.SCHEMA['$defs']['analysis-spec']['properties']['requestedCapabilities']['maxItems']
SCOPE=IM.SCHEMA['$defs']['scope-descriptor']['properties']['workspaceRoots']['maxItems']
out['bounds']={'requestedCapabilitiesMaxItems':BOUND,'workspaceRootsMaxItems':SCOPE,
  'defaultCapabilitiesPerTsUnit':CAPS,'defaultCapabilitiesPerRustUnit':len(N.required_default_capabilities('rust-cargo')),
  'largestTsUnitCountThatFits':BOUND//CAPS,
  'unitsScopeAdmitsButDefaultCannot':[BOUND//CAPS+1,SCOPE]}
rows=[]
for count in (93,94):
    units=[{'rootPath':'apps/u%03d'%i,'languageMode':'ts-tsconfig','languageFamily':'tsjs'} for i in range(count)]
    try:
        r=N.default_capability_selection(units,[])
        rows.append({'units':count,'outcome':'ADMIT','requests':len(r['analysisSpec']['requestedCapabilities'])})
    except Exception as e:
        rows.append({'units':count,'outcome':'REFUSE','exception':type(e).__name__,
                     'rawScalars':len(str(e)),'isTypedRefusal':isinstance(e,N.ScopeRefusal),
                     'hasSubject':hasattr(e,'subject'),'prefix':str(e)[:90]})
out['defaultSelection']=rows
# Is the ScopeRefusal machinery field-generic already?
try:
    r=N.ScopeRefusal('requestedCapabilities',1034,1024)
    out['scopeRefusalIsFieldGeneric']={'detail':r.detail,'subject':r.subject,'d9':r.d9,'message':str(r)}
except Exception as e:
    out['scopeRefusalIsFieldGeneric']='ERROR:'+str(e)
# Does the scope descriptor itself refuse at 94 units? (i.e. is there an earlier owning refusal?)
units94=[{'rootPath':'apps/u%03d'%i,'languageMode':'ts-tsconfig','languageFamily':'tsjs'} for i in range(94)]
try:
    d=N.unit_scope_descriptor(units94,[])
    out['scopeDescriptorAt94Units']={'outcome':'ADMIT','workspaceRoots':len(d['scopeDescriptor']['workspaceRoots'])}
except Exception as e:
    out['scopeDescriptorAt94Units']={'outcome':'REFUSE','error':str(e)[:120]}
# Can an EXPLICIT (non-default) spec overflow the same bound, i.e. is the default the only path?
explicit=[{'capabilityId':'inventory','languageMode':'ts-tsconfig','workspaceRoot':'apps/u%04d'%i,'required':True}
          for i in range(1025)]
try:
    N.validate_foundation('analysis-spec',{'schemaVersion':2,'requestedCapabilities':explicit,
                                           'policyPackIds':[],'parameters':[]})
    out['explicitOverflow']={'outcome':'ADMIT'}
except Exception as e:
    out['explicitOverflow']={'outcome':'REFUSE','exception':type(e).__name__,'rawScalars':len(str(e)),
                             'isTypedRefusal':isinstance(e,N.ScopeRefusal)}
# Does any published contract text already own the analysis-spec bound as a refusal?
md=(DC.parents[1]/'v2/contracts/product-v1/native-evidence.md').read_text()
out['existingLawSearch']={
 'scopeArrayParagraphNamesOnlyScopeFields':'workspaceRoots has limit1024' in md and 'requestedCapabilities' not in
   md.split('A scope array that exceeds')[1][:900],
 'anyRequestedCapabilitiesRefusalRow':'requestedCapabilities' in md and
   any('requestedCapabilities' in l and 'UNSATISFIABLE' in l for l in md.splitlines())}
print(json.dumps(out,indent=1))

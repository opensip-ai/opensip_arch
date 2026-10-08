"""Synthetic design controls only; this function cannot admit actual owners."""
from pathlib import Path
import argparse, copy, hashlib, importlib.util, json, sys
p=argparse.ArgumentParser();p.add_argument('--architecture',type=Path,required=True);p.add_argument('--deps',type=Path,required=True);p.add_argument('--write',action='store_true');args=p.parse_args()
sys.path.insert(0,str(args.deps));here=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('canonical',args.architecture/'docs/coop/design-corrections/foundation/canonical.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
schema=json.loads((here/'native-key-codecs.schema.json').read_text());native=json.loads((args.architecture/'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text());identity=json.loads((args.architecture/'docs/coop/design-corrections/foundation/identity-schemas.v3.json').read_text())
assert schema['$defs']['LogicalPath']==identity['$defs']['LogicalPath']
for k in ['name','version','sourceId']:assert schema['$defs']['NativePackageWitnessV1']['properties'][k]==native['$defs']['DependencyPackageSourceV1']['properties'][k]
assert schema['$defs']['NativeOwnerWitnessV2']['properties']['sourceKind']==native['$defs']['DependencyPackageSourceV1']['properties']['sourceKind']
def digest(prefix,preimage):return prefix+hashlib.sha256(c.canonical(preimage)).hexdigest()
def package(name,version,source):return {'name':name,'version':version,'sourceId':source,'packageKey':digest('pkg1-',[name,version,source])}
def owner(package,source,kind,path):return {'source':source,'sourceKind':kind,'package':copy.deepcopy(package),'snapshotManifestPath':path,'ownerKey':digest('own2-',[source,package['packageKey'],path])}
def shape_and_rederive(w):
 c.validate(dict(schema,**{'$ref':'#/$defs/NativeOwnerWitnessV2'}),w);c.canonical(w)
 q=w['package'];assert q['packageKey']==digest('pkg1-',[q['name'],q['version'],q['sourceId']]),'PACKAGE_KEY_MISMATCH'
 if w['snapshotManifestPath'] is not None:assert w['snapshotManifestPath'].rsplit('/',1)[-1]=='Cargo.toml','MANIFEST_BASENAME'
 assert w['ownerKey']==digest('own2-',[w['source'],q['packageKey'],w['snapshotManifestPath']]),'OWNER_KEY_MISMATCH'
 # NO source/producer/activation/custody/snapshot admission is performed here.
cases=[]
pathpkg=package('same-name','0.1.0','');regpkg=package('same-name','0.1.0','registry+https://example.invalid/one');other=package('same-name','0.1.0','registry+https://example.invalid/two')
positives=[('workspace-a',owner(pathpkg,'snapshot-member','path','workspace-a/Cargo.toml')),('workspace-b',owner(pathpkg,'snapshot-member','path','workspace-b/Cargo.toml')),('nonworkspace-path',owner(pathpkg,'dependency-closure-member','path','libs/Cargo.toml')),('registry',owner(regpkg,'dependency-closure-member','registry',None)),('different-source',owner(other,'dependency-closure-member','registry',None)),('git',owner(package('g','0.2.0','git+https://example.invalid/g#abc'),'dependency-closure-member','git',None)),('vendored',owner(regpkg,'dependency-closure-member','vendored',None)),('unicode-preserved',owner(package('é'*256,'0.1.0',''),'snapshot-member','path','é/Cargo.toml'))]
for label,w in positives:
 shape_and_rederive(w);q=w['package'];pa=[q['name'],q['version'],q['sourceId']];oa=[w['source'],q['packageKey'],w['snapshotManifestPath']]
 cases.append({'id':label,'expected':'shape-and-recipe-valid-only','witness':w,'packageCanonicalUtf8':c.canonical(pa).decode(),'ownerCanonicalUtf8':c.canonical(oa).decode()})
assert positives[0][1]['package']['packageKey']==positives[1][1]['package']['packageKey']
assert positives[0][1]['ownerKey']!=positives[1][1]['ownerKey']
assert regpkg['packageKey']!=other['packageKey']
assert positives[3][1]['ownerKey']==positives[6][1]['ownerKey'] # same actual source tuple/path selector, acquisition mode is not identity
assert package('é','0.1.0','')['packageKey']!=package('e\u0301','0.1.0','')['packageKey']
base=positives[0][1]
def altered(**kw):return dict(copy.deepcopy(base),**kw)
bad=[('missing-path',altered(snapshotManifestPath=None)),('absolute-path',altered(snapshotManifestPath='/tmp/Cargo.toml')),('dot-dot-path',altered(snapshotManifestPath='../Cargo.toml')),('backslash-path',altered(snapshotManifestPath='a\\Cargo.toml')),('wrong-basename',altered(snapshotManifestPath='workspace-a/Other.toml')),('snapshot-nonpath',altered(sourceKind='registry')),('unknown-source',altered(source='caller-source')),('unknown-kind',altered(sourceKind='external')),('extra-field',altered(extra=True)),('legacy-owner-key',altered(ownerKey='own1-'+base['ownerKey'][5:])),('wrong-owner-key',altered(ownerKey='own2-'+'0'*64)),('path-moved-key-unchanged',altered(snapshotManifestPath='moved/Cargo.toml')),('field-type',altered(snapshotManifestPath=1)),('unicode-surrogate',altered(snapshotManifestPath='\ud800/Cargo.toml'))]
w=owner(pathpkg,'dependency-closure-member','path','libs/Cargo.toml');w['package']['sourceId']='registry+https://example.invalid/one';bad.append(('path-source-id-not-empty',w))
w=copy.deepcopy(positives[3][1]);w['snapshotManifestPath']='registry/Cargo.toml';bad.append(('nonpath-locator-inserted',w))
w=copy.deepcopy(base);w['package']['packageKey']='pkg1-'+'0'*64;bad.append(('wrong-package-key',w))
w=copy.deepcopy(base);w['package']['name']='x'*257;bad.append(('name-scalar-overflow',w))
w=copy.deepcopy(base);del w['package']['version'];bad.append(('missing-version',w))
w=copy.deepcopy(base);w['package']['sourceId']=None;bad.append(('source-null-normalized',w))
w=copy.deepcopy(base);w['ownerKey']=digest('own2-',list(reversed([w['source'],pathpkg['packageKey'],w['snapshotManifestPath']])));bad.append(('reversed-owner-preimage',w))
w=copy.deepcopy(base);w['ownerKey']='own2-'+c.identity('native.owner.v2',[w['source'],pathpkg['packageKey'],w['snapshotManifestPath']]);bad.append(('domain-digest-substitution',w))
for label,w in bad:
 try:shape_and_rederive(w)
 except (c.AdmissionError,c.ValidationError,AssertionError) as e:cases.append({'id':label,'expected':'refuse-shape-or-recipe','observedType':type(e).__name__})
 else:raise AssertionError(label)
for case in cases:
 if 'witness' in case:shape_and_rederive(case['witness'])
report={'standing':'Synthetic closed shape/hash reference controls, NOT actual producer/snapshot/source/activation/custody/owner admission','schemaCopiesEqualByValue':5,'positiveControls':len(positives),'negativeControls':len(bad),'cases':cases,'sameTupleDifferentManifestOwnersDistinct':True,'UnicodeScalarBoundsPreserved':True,'NoUnicodeNormalization':True,'productExecuted':False,'ownerMappingPublished':False,'R3Resolved':False,'productQualification':False}
t=here/'evidence/codec-controls.json'
if args.write:t.write_text(json.dumps(report,indent=2,ensure_ascii=True)+'\n')
else:assert json.loads(t.read_text())==report
print(f'{len(positives)} synthetic positive / {len(bad)} negative codec controls pass; no actual admission.')

"""Read-only staged J-BS schema checks; no emitter/publication/generator execution."""
import argparse,copy,hashlib,importlib.util,itertools,json,pathlib,sys

def pin(root,row):
 b=(root/row['path']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
def main():
 p=argparse.ArgumentParser();p.add_argument('--architecture',type=pathlib.Path,required=True);p.add_argument('--product',type=pathlib.Path,required=True);args=p.parse_args();local=pathlib.Path(__file__).parent;authority=json.loads((local/'authority.json').read_text())
 for row in authority['architecture']:pin(args.architecture,row)
 for row in authority['product']:pin(args.product,row)
 parent_rel='docs/implementation/m1/source-selection-v2/schemas/sources/invocation.v5.schema.json';original=json.loads((args.architecture/parent_rel).read_text());candidate=json.loads((local.parent/'schemas/invocation-v5.schema.json').read_text());d=candidate['$defs']['RetentionDisclosure'];after=copy.deepcopy(candidate);after['$defs']['RetentionDisclosure']['properties'].pop('backupStatus');after['$defs']['RetentionDisclosure'].pop('allOf');assert after==original
 assert d['properties']['backupStatus']=={'type':'string','enum':['backed-up','not-backed-up','unknown']};assert candidate['$id']==original['$id'];assert d['required']==original['$defs']['RetentionDisclosure']['required']
 quality=args.product/'tools/quality';sys.path.insert(0,str(quality));spec=importlib.util.spec_from_file_location('jbs_dependencies',quality/'envelope_shape.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);library=module._dependencies(args.product/'tools/contracts/python-packages',(args.product/'tools/contracts/python-packages.json').read_bytes())
 from referencing import Registry,Resource
 common=json.loads((args.product/'schemas/sources/common-v4.schema.json').read_text());envelope=json.loads((args.product/'schemas/sources/command-envelope-v7.schema.json').read_text());registry=Registry().with_resources([(schema['$id'],Resource.from_contents(schema)) for schema in [candidate,common,envelope]])
 library.Draft202012Validator.check_schema(candidate);retention=library.Draft202012Validator({'$ref':candidate['$id']+'#/$defs/RetentionDisclosure'},registry=registry);env=library.Draft202012Validator(envelope,registry=registry)
 rows=[];omitted=object()
 for policy,provenance,first,status in itertools.product(['durable-unbounded','durable-bounded','ephemeral'],['DEFAULTED','CONFIGURED','EXPLICIT-FLAG'],[False,True],[omitted,'backed-up','not-backed-up','unknown']):
  value={'policy':policy,'provenance':provenance,'firstUse':first,'storageRoot':'/tmp/jbs-synthetic-path-only'}
  if status is not omitted:value['backupStatus']=status
  expected=(first and status is not omitted) or (not first and status is omitted);assert retention.is_valid(value)==expected
  rows.append({'policy':policy,'provenance':provenance,'firstUse':first,'backupStatus':None if status is omitted else status,'statusOmitted':status is omitted,'expectedValid':expected})
 base={'policy':'durable-unbounded','provenance':'DEFAULTED','firstUse':True,'storageRoot':'/tmp/jbs-synthetic-path-only','backupStatus':'unknown'};bad=0
 for value in [None,True,False,1,0,{},[], 'UNKNOWN','unknown\n','not backed up','']:
  row=copy.deepcopy(base);row['backupStatus']=value;assert not retention.is_valid(row);bad+=1
 for value in [None,1,0,'true',{},[]]:
  row=copy.deepcopy(base);row['firstUse']=value;assert not retention.is_valid(row);bad+=1
 for key in ['policy','provenance','firstUse','storageRoot']:
  row=copy.deepcopy(base);row.pop(key);assert not retention.is_valid(row);bad+=1
 row=copy.deepcopy(base);row['extra']=True;assert not retention.is_valid(row);bad+=1
 interrupted=[]
 for signal in ['SIGINT','SIGTERM','SIGHUP']:
  row={'schemaFamily':'opensip.product.envelope','schemaMajor':7,'kind':'failure','requestId':'req1_'+'0'*32,'termination':{'class':'interrupted','signal':signal},'exitCode':130,'errors':[]};assert env.is_valid(row)
  for first in [False,True]:
   with_disclosure=copy.deepcopy(row);disclosure=copy.deepcopy(base);disclosure['firstUse']=first
   if not first:disclosure.pop('backupStatus')
   assert retention.is_valid(disclosure);with_disclosure['retentionDisclosure']=disclosure;assert not env.is_valid(with_disclosure);interrupted.append({'signal':signal,'firstUse':first,'expectedValidWithoutDisclosure':True,'expectedValidWithDisclosure':False})
 classification=(args.product/'crates/security/src/initial_installation.rs').read_text();assert 'Self::BackedUp => "backed-up"' in classification and 'Self::NotBackedUp => "not-backed-up"' in classification and 'Self::Unknown => "unknown"' in classification;assert 'fn classify_backup(_target: &std::path::Path) -> BackupClassification {\n    BackupClassification::Unknown\n}' in classification
 law=(args.architecture/'docs/implementation/m3/host-pipeline-j/PROPOSAL-r6.md').read_text();assert 'It is present exactly when `firstUse` is true.' in law and 'publication rename' in law and 'The first emitter' in law and 'never** carries it' in law
 assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 print(json.dumps({'passed':True,'standing':'J-BS DESIGN SCHEMA CONTROLS ONLY; NO EMITTER OR PUBLICATION','schemaRestorationEqualsParent':True,'presenceCaseCount':len(rows),'presenceCases':rows,'malformedCaseCount':bad,'interruptedCases':interrupted,'emptyInterruptedBaselineCount':3,'interruptedDisclosureRefusals':len(interrupted),'dependencyManifestSha256':module.PACKAGES_SHA256,'dependencyFileCount':len(json.loads((args.product/'tools/contracts/python-packages.json').read_text())['files']),'noticeExecuted':False,'emitterRan':False,'generatorRan':False,'installationAbsent':True,'productQualification':False},indent=2))
if __name__=='__main__':main()

"""Complete description reports and internal cross-catalogue joins.

Release/closure selection dictionaries are synthetic host preconditions. This
checks contradictions inside a report, not signatures or actual Run membership.
"""
from pathlib import Path
import copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
Q=load('check_catalogue_joins');V=Q.V;O=Q.O;J=Q.J;M=load('models/report_model');A=load('report_admission');FJ=load('fit_join');META=load('metadata_owner')


def refresh(doc):
 doc['disclosures']=J.disclosures(doc['panels'],None,M,V.H,doc['envelope'].get('run',{}).get('runId'),lambda v:V.validate(V.history_schema['$id'],v))
 row=next(c for c in META.read('inventory')['commands'] if c['name']==doc['command'])
 raw=M.static_parity_text(doc['envelope'],row,doc['disclosures']).encode()
 doc['staticParity']={'format':M.STATIC_FORMAT,'textSha256':hashlib.sha256(raw).hexdigest(),'textBytes':len(raw)}
 return doc


def complete():
 doc=json.loads((HERE/'parent-bases.fixture.json').read_bytes())['audit-full'];data=O.fixture()
 display={k:copy.deepcopy(data['rules'][0][k]) for k in ['name','description','tags']}
 data['rules']=[{'ruleProgramRef':copy.deepcopy(r['ruleProgramRef']),**copy.deepcopy(display)} for r in doc['panels']['catalog']['data']['rules']['data']['rules']]
 data['recipes']=[]
 ctx,raw,declared=O.bound(data);receipt=O.admit(ctx,raw,declared)
 selection={g:sorted([list(k) for k in declared[g]],key=V.C.canonical) for g in O.catalog.GROUPS}
 projected=O.select(receipt,{g:[tuple(k) for k in v] for g,v in selection.items()},ctx['closureId'])
 selected={'closureId':ctx['closureId'],**selection};run=doc['envelope']['run']
 declarations=[{'capabilityId':'reachability','languageModes':['syntax-only']}]
 caps=doc['panels']['catalog']['data']['capabilities']['data'];caps['declarations']=declarations;caps['source']['registrySha256']=hashlib.sha256(V.C.canonical(declarations)).hexdigest()
 doc['panels']['descriptions']={'state':'present','data':{'run':{'state':'present','data':{'runId':run['runId'],'planId':run['planId'],'selection':[selected],'receipts':[projected]}},'recipe':{'state':'omitted','reason':'not-selected'},'provenance':copy.deepcopy(V.report['$defs']['DescriptionsPanelV1']['properties']['provenance']['const'])}}
 return refresh(doc)


def admit(doc):return A.admit(M.canonical(doc),V,M,J,O.catalog,FJ.owner_summary(V.C))

class CatalogueSourceTests(unittest.TestCase):
 def test_complete_owner_receipt_and_visible_catalogue_agree(self):
  doc=complete();admit(doc)
  (HERE/'complete-catalogue.fixture.json').write_text(json.dumps(doc,indent=2)+'\n')
 def test_valid_carriers_with_conflicting_source_keys_refuse(self):
  for change,code in [('registry','DESCRIPTION-CATALOGUE-REGISTRY'),('capability','DESCRIPTION-CATALOGUE-CAPABILITY'),('rule','DESCRIPTION-CATALOGUE-RULE')]:
   doc=complete();row=doc['panels']['descriptions']['data']['run']['data'];selected=row['selection'][0];receipt=row['receipts'][0]
   if change=='registry':receipt['capabilityAuthority']['registrySha256']='f'*64
   elif change=='capability':
    selected['capabilities'][0][0]='other-capability';receipt['capabilities'][0]['descriptor']['capabilityId']='other-capability'
   else:
    selected['rules'][0][3]='f'*64;receipt['rules'][0]['descriptor']['ruleProgramRef']['programDigest']='f'*64
   refresh(doc);V.validate(V.report['$id'],doc)
   with self.subTest(change=change),self.assertRaisesRegex(ValueError,code):admit(doc)
 def test_second_capability_authority_refuses_even_without_selected_keys(self):
  doc=complete();row=doc['panels']['descriptions']['data']['run']['data'];second=copy.deepcopy(row['receipts'][0]);other='closure2:'+'a'*64
  second['closureId']=other;second['capabilityAuthority']['closureId']=other
  for group in O.catalog.GROUPS:second[group]=[]
  row['selection'].append({'closureId':other,**{g:[] for g in O.catalog.GROUPS}});row['receipts'].append(second)
  V.validate(V.report['$id'],doc)
  with self.assertRaisesRegex(ValueError,'DESCRIPTION-MULTIPLE-CAPABILITY-AUTHORITIES'):admit(doc)
 def test_complete_recipe_description_matches_actual_preview_carrier(self):
  doc=json.loads((HERE/'parent-bases.fixture.json').read_bytes())['repair-preview']
  preview=doc['envelope']['queryRecord']['plan'];recipe=preview['descriptor']['recipe'];data=O.fixture()
  data['recipes'][0]['recipeKey']={k:recipe[k] for k in ['contributionId','recipeId','recipeVersion']}
  ctx,raw,declared=O.bound(data);ctx['closureId']=recipe['closureId'];receipt=O.admit(ctx,raw,declared)
  key=next(iter(declared['recipes']));selected={'capabilities':[],'rules':[],'recipes':[key]}
  projected=O.select(receipt,selected,ctx['closureId'])
  selection={'closureId':ctx['closureId'],'capabilities':[],'rules':[],'recipes':[list(key)]}
  doc['panels']['descriptions']={'state':'present','data':{'run':{'state':'omitted','reason':'not-selected'},
   'recipe':{'state':'present','data':{'repairPlanId':preview['repairPlanId'],'recipe':copy.deepcopy(recipe),'selection':selection,'receipt':projected}},
   'provenance':copy.deepcopy(V.report['$defs']['DescriptionsPanelV1']['properties']['provenance']['const'])}}
  refresh(doc);admit(doc)
  (HERE/'complete-recipe-catalogue.fixture.json').write_text(json.dumps(doc,indent=2)+'\n')
  doc['panels']['descriptions']['data']['recipe']['data']['recipe']['recipeVersion']='9.9.9'
  with self.assertRaisesRegex(ValueError,'DESCRIPTION-PREVIEW-RECIPE'):admit(doc)
 def test_duplicate_selected_rule_across_closures_refuses(self):
  doc=complete();row=doc['panels']['descriptions']['data']['run']['data'];second=copy.deepcopy(row['receipts'][0]);other='closure2:'+'a'*64
  second['closureId']=other;second['capabilityAuthority']=None;second['capabilities']=[]
  selected={'closureId':other,'capabilities':[],'rules':copy.deepcopy(row['selection'][0]['rules']),'recipes':[]}
  row['selection'].append(selected);row['receipts'].append(second)
  V.validate(V.report['$id'],doc)
  with self.assertRaisesRegex(ValueError,'DESCRIPTION-DUPLICATE-RULE'):admit(doc)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CatalogueSourceTests))
 out={'standing':'Root complete catalogue report and visible source contradiction checks; source contexts remain synthetic, no authenticated release/Run custody','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'catalogue-source-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(not result.wasSuccessful())

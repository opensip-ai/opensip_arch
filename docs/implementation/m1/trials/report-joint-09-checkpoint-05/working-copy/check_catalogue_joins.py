"""Closed document receipt joins; admitted release/Run selection is a host premise."""
from pathlib import Path
import copy,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');J=load(HERE/'document_joins.py','j')
for name in ['check.py','catalog.py','build_schema.py','input-pins.json','presentation-catalog.schema.json']:V.read_unit('presentation-catalog',name)
O=load(V.subjects['presentation-catalog']/'check.py','catalogue_owner_helpers')
anchor={'runId':'run3:'+'1'*64,'planId':'plan2:'+'2'*64}


def receipt():
 data=O.fixture();ctx,raw,declared=O.bound(data);admitted=O.admit(ctx,raw,declared)
 selected={g:sorted([list(k) for k in declared[g]],key=V.C.canonical) for g in O.catalog.GROUPS}
 selected['recipes']=[]
 source={g:[tuple(k) for k in values] for g,values in selected.items()}
 projected=O.select(admitted,source,ctx['closureId'])
 return {'closureId':ctx['closureId'],**selected},projected


def admit(selected,value):
 V.validate(V.report['$id']+'#/$defs/DescriptionReceiptV1',value)
 J.receipt(selected,value,O.catalog,V.C.equal_typed)

class CatalogueTests(unittest.TestCase):
 def test_unchanged_owner_selected_receipt_passes_document_joins(self):
  selected,value=receipt();admit(selected,value)
  panel={'state':'present','data':{'run':{'state':'present','data':{**anchor,'selection':[selected],'receipts':[value]}},
    'recipe':{'state':'omitted','reason':'not-selected'},'provenance':copy.deepcopy(V.report['$defs']['DescriptionsPanelV1']['properties']['provenance']['const'])}}
  V.validate(V.report['$id']+'#/$defs/DescriptionsPanelStateV1',panel)
  J.descriptions(panel,anchor,None,O.catalog,V.C.equal_typed)
  wrong=copy.deepcopy(panel);wrong['data']['run']['data']['planId']='plan2:'+'f'*64
  with self.assertRaisesRegex(ValueError,'RUN-PLAN'):J.descriptions(wrong,anchor,None,O.catalog,V.C.equal_typed)
  wrong=copy.deepcopy(panel);wrong['data']['run']['data']['receipts']=[]
  with self.assertRaisesRegex(ValueError,'RECEIPT-COUNT'):J.descriptions(wrong,anchor,None,O.catalog,V.C.equal_typed)
 def test_receipt_mutations_cannot_forge_selection_or_embedded_association(self):
  selected,value=receipt();admit(selected,value)
  for change in ['closure','listing','authority-platform','authority-closure','missing-authority','selected-key','duplicate-tree']:
   bad=copy.deepcopy(value);sel=copy.deepcopy(selected)
   if change=='closure':bad['closureId']='closure2:'+'f'*64
   elif change=='listing':bad['listing']['sha256']='0'*64
   elif change=='authority-platform':bad['capabilityAuthority']['platform']='other-platform'
   elif change=='authority-closure':bad['capabilityAuthority']['closureId']='closure2:'+'f'*64
   elif change=='missing-authority':bad['capabilityAuthority']=None
   elif change=='selected-key':sel['capabilities']=[]
   else:bad['tree'].append(copy.deepcopy(bad['tree'][0]))
   with self.subTest(change=change),self.assertRaises((ValueError,V.C.ValidationError)):admit(sel,bad)
 def test_run_receipt_cannot_select_recipes_and_preview_requires_exact_one(self):
  selected,value=receipt();run={**anchor,'selection':[selected],'receipts':[value]}
  V.validate(V.report['$id']+'#/$defs/RunDescriptionsV1',run)
  bad=copy.deepcopy(run);bad['selection'][0]['recipes']=[['a','b','1.0.0']]
  with self.assertRaises(V.C.ValidationError):V.validate(V.report['$id']+'#/$defs/RunDescriptionsV1',bad)
  # Use the unchanged selected recipe descriptor as a separate preview premise.
  data=O.fixture();ctx,raw,declared=O.bound(data);admitted=O.admit(ctx,raw,declared)
  key=next(iter(declared['recipes']));recipe={'closureId':ctx['closureId'],**dict(zip(['contributionId','recipeId','recipeVersion'],key))}
  source={'capabilities':[],'rules':[],'recipes':[key]};projected=O.select(admitted,source,ctx['closureId'])
  selection={'closureId':ctx['closureId'],'capabilities':[],'rules':[],'recipes':[list(key)]}
  preview={'repairPlanId':'repairplan2:'+'3'*64,'descriptor':{'recipe':recipe}}
  row={'repairPlanId':preview['repairPlanId'],'recipe':recipe,'selection':selection,'receipt':projected}
  V.validate(V.report['$id']+'#/$defs/RecipeDescriptionsV1',row)
  panel={'state':'present','data':{'run':{'state':'omitted','reason':'not-selected'},'recipe':{'state':'present','data':row},
        'provenance':copy.deepcopy(V.report['$defs']['DescriptionsPanelV1']['properties']['provenance']['const'])}}
  J.descriptions(panel,None,preview,O.catalog,V.C.equal_typed)
  for keys in [[],[list(key),list(key)]]:
   bad=copy.deepcopy(row);bad['selection']['recipes']=keys
   with self.assertRaises(V.C.ValidationError):V.validate(V.report['$id']+'#/$defs/RecipeDescriptionsV1',bad)
  wrong=copy.deepcopy(preview);wrong['descriptor']['recipe']['recipeVersion']='9.9.9'
  with self.assertRaisesRegex(ValueError,'PREVIEW-RECIPE'):J.descriptions(panel,None,wrong,O.catalog,V.C.equal_typed)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CatalogueTests))
 out={'standing':'Root document-only catalogue association checks with unchanged owner fixtures; no authenticated Run/release custody','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'catalogue-join-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(not result.wasSuccessful())

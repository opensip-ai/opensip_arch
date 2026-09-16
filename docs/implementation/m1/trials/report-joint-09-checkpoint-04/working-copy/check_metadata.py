"""Composed inventory/history detail admission and scoped succession controls."""
from pathlib import Path
import copy,json,types,unittest
HERE=Path(__file__).resolve().parent

def load(name):
 p=HERE/(name+'.py');m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
V=load('check_model_carriers');O=load('metadata_owner');P=load('planning_owner')
INV='urn:opensip:product-v1:workflows:evaluator3:command-inventory:6'
value=O.read('inventory');parent=json.loads(V.read_unit('report-projection','owner/command-inventory.v5.json'))
flags=json.loads(V.read_unit('history-selection','history-command-flags.json'))['rows']

class MetadataTests(unittest.TestCase):
 def test_inventory_and_all_history_flag_applicability(self):
  V.validate(INV,value)
  flagged={c['name'] for c in value['commands'] if any(f['flag']=='--history-run' for f in c['flags'])}
  self.assertEqual(flagged,{r['command'] for r in flags})
  self.assertEqual(flagged,{c['name'] for c in value['commands'] if 'html' in c['formats']})
  for row in flags:
   command=next(c for c in value['commands'] if c['name']==row['command'])
   self.assertEqual([f for f in command['flags'] if f['flag']=='--history-run'],[row['appendFlag']])
 def test_scope_preserves_existing_commands_authorization_and_parity(self):
  restored=copy.deepcopy(value);restored['schemaMajor']=parent['schemaMajor'];restored['standing']=parent['standing']
  for command in restored['commands']:
   command['flags']=[f for f in command['flags'] if f['flag']!='--history-run']
   if command['name']=='fit':command['advisoryDispatch'].pop('sourceBinding')
  next(r for r in restored['renderers'] if r['format']=='json').update(copy.deepcopy(next(r for r in parent['renderers'] if r['format']=='json')))
  self.assertEqual(restored,parent)
 def test_fit_binding_and_new_envelope_reference_are_explicit(self):
  fit=next(c for c in value['commands'] if c['name']=='fit');binding=fit['advisoryDispatch']['sourceBinding']
  self.assertEqual(binding['plannedParams'],P.read()['commands']['fit'][0]['steps'][1]['representativeParams'])
  self.assertEqual(binding['requestSchemaMajor'],V.query_schema['$defs']['GraphQueryRequestV1']['properties']['schemaMajor']['const'])
  renderer=next(r for r in value['renderers'] if r['format']=='json');self.assertEqual(renderer['version'],7)
  for alter in ['remove-source','wrong-step','wrong-query-major']:
   bad=copy.deepcopy(value);dispatch=next(c for c in bad['commands'] if c['name']=='fit')['advisoryDispatch']
   if alter=='remove-source':dispatch.pop('sourceBinding')
   elif alter=='wrong-step':dispatch['sourceBinding']['plannedParams']['sourceStep']=1
   else:dispatch['sourceBinding']['requestSchemaMajor']=3
   with self.subTest(alter=alter),self.assertRaises(V.C.ValidationError):V.validate(INV,bad)
 def test_detail_registry_matches_the_composed_public_enum(self):
  registry=O.read('details');codes=[r['code'] for r in registry['records']]
  common=V.schemas['urn:opensip:product-v1:workflows:evaluator3:common:3']
  self.assertEqual(len(codes),len(set(codes)));self.assertEqual(set(codes),set(common['$defs']['DomainDetailCode']['enum']))
  self.assertIn('REPORT.HISTORY_SELECTION_INVALID',codes)
  self.assertEqual(registry,json.loads(V.read_unit('history-selection','public-detail-registry.history-candidate.json')))

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MetadataTests))
 out={'standing':'Root inventory6/public-detail composition checks; no selected CLI parser, help or generator integration','groups':result.testsRun,'commands':len(value['commands']),'historyCommands':len(flags),'passed':result.wasSuccessful()}
 (HERE/'metadata-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(not result.wasSuccessful())

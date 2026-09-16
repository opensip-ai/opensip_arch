"""Common4 vocabulary is selected explicitly; historical common3 stays exact."""
from pathlib import Path
import copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent
p=HERE/'check_model_carriers.py';V=types.ModuleType('v');V.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),V.__dict__)
OLD='urn:opensip:product-v1:workflows:evaluator3:common:3';NEW=OLD[:-1]+'4'
CODES=['REPORT.HISTORY_SELECTION_INVALID','native.framework-recognition-parameter-required']
pins=json.loads(V.read_unit('report-projection','source-pins.json'))['files']
pin=next(r for r in pins if r['path'].endswith('/workflows/schemas/evaluator3/common.schema.json'))
raw=Path(pin['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==pin['sha256'];parent=json.loads(raw)

class CommonTests(unittest.TestCase):
 def test_old_namespace_keeps_exact_pinned_schema(self):
  self.assertEqual(V.schemas[OLD],parent)
  for code in CODES:
   value={'code':code,'remedy':'supply the required input'}
   with self.subTest(code=code),self.assertRaises(V.C.ValidationError):V.validate(OLD+'#/$defs/DomainDetail',value)
   V.validate(NEW+'#/$defs/DomainDetail',value)
 def test_new_namespace_changes_only_two_codes_and_descriptive_identity(self):
  restored=copy.deepcopy(V.schemas[NEW])
  for k in ['$id','title','description']:
   if k in parent:restored[k]=copy.deepcopy(parent[k])
   else:restored.pop(k,None)
  for code in CODES:restored['$defs']['DomainDetailCode']['enum'].remove(code)
  self.assertEqual(restored,parent)
 def test_every_current_schema_ref_selects_new_common(self):
  refs=[]
  def walk(v):
   if isinstance(v,dict):
    if isinstance(v.get('$ref'),str):refs.append(v['$ref'])
    for x in v.values():walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  for row in json.loads((HERE/'composition-result.json').read_bytes())['outputs']:
   walk(json.loads((HERE/row['path']).read_bytes()))
  self.assertTrue(any(r.startswith(NEW+'#') for r in refs))
  self.assertFalse(any(r==OLD or r.startswith(OLD+'#') for r in refs))

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CommonTests))
 out={'standing':'Root common3 preservation and explicit common4 source succession; not product compatibility or source acceptance','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'common-succession-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(not result.wasSuccessful())

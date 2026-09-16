"""All19 parent positive scenarios reconstructed under the joint consumer."""
from pathlib import Path
import json,types,unittest
HERE=Path(__file__).resolve().parent

def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
V=load(HERE/'check_model_carriers.py','v');A=load(HERE/'report_admission.py','a');M=load(HERE/'models/report_model.py','m')
J=load(HERE/'document_joins.py','j');K=load(HERE/'models/catalog.py','k');Q=load(HERE/'fit_join.py','q')
S=load(HERE/'parent_fixture_source.py','s');F=load(HERE/'check_fit_documents.py','f');B=load(HERE/'parent_bases.py','b')
rows=[]

class BaseTests(unittest.TestCase):
 def test_all_parent_positive_scenarios(self):
  bases,material=B.build(V,M,S,F)
  self.assertEqual(len(bases),19)
  for name,doc in bases.items():
   with self.subTest(name=name):
    try:A.admit(M.canonical(doc),V,M,J,K,Q.owner_summary(V.C));observed='accept'
    except Exception as error:observed=getattr(error,'code',type(error).__name__)
    rows.append({'id':name,'observed':observed,'passed':observed=='accept'})
    self.assertEqual(observed,'accept')
  (HERE/'parent-bases.fixture.json').write_text(json.dumps(bases,indent=2)+'\n')

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(BaseTests))
 out={'standing':'Root all19 reconstructed parent positive scenarios; synthetic domain observations with fresh mock graph queries, not product/stored-envelope migration qualification','passed':result.wasSuccessful(),'rows':rows}
 (HERE/'parent-bases-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(not result.wasSuccessful())

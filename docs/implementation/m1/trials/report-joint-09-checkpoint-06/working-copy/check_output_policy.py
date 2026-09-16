"""Explicit successor equality and unchanged D9 golden derivation, not acceptance."""
from pathlib import Path
import copy,hashlib,json,types,unittest
HERE=Path(__file__).resolve().parent
p=HERE/'check_output_integration.py';O=types.ModuleType('integration');O.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),O.__dict__)
row=json.loads((HERE/'output-policy-composition-result.json').read_bytes());pin=row['output'];raw=(HERE/pin['path']).read_bytes()
assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
value=json.loads(raw);parent=O.O.CONTRACT

class PolicyTests(unittest.TestCase):
 def test_exact_scope_of_the_proposed_full_view(self):
  restored=copy.deepcopy(value)
  for key in ['version','status','supersedes','purpose']:restored[key]=copy.deepcopy(parent[key])
  restored.pop('jointOutputSuccession')
  invariant=next(r for r in restored['invariants'] if r['id']=='invariant-envelope-parity')
  self.assertEqual(invariant['text'],row['invariantChange']['after']);invariant['text']=row['invariantChange']['before']
  self.assertEqual(restored,parent)
  self.assertEqual(value['jointOutputSuccession']['parentSha256'],row['parentSha256'])
 def test_every_existing_golden_derives_unchanged_from_actual_owner(self):
  results=O.O.D._derived_rows(value)
  self.assertEqual(results,O.O.D._declared_rows(value))
  self.assertEqual(results,O.O.D._derived_rows(parent))
  self.assertEqual(sum(r[0]=='golden' for r in results),45)
  self.assertEqual(sum(r[0]=='matrix' for r in results),4)
  self.assertEqual(sum(r[0]=='reduction' for r in results),6)
  (HERE/'output-policy-golden-results.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PolicyTests))
 out={'standing':'Root exact successor scope and45 unchanged D9 golden derivations; inherited checker not asserted to accept v1.15, policy and L02 unresolved pending actual review','groups':result.testsRun,'passed':result.wasSuccessful()}
 (HERE/'output-policy-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));raise SystemExit(not result.wasSuccessful())

"""Stage public synthetic companion authoring from accepted construction recipes.
No repository/worktree writes, generator execution, private inputs or runtime tests.
"""
from pathlib import Path
import ast,json,hashlib,subprocess
F=Path(__file__).parent;B=F/'fixture-authoring-r1';assert not B.exists();B.mkdir()
P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-native-owner-patterns-takeover';A=P.parent/'opensip_arch'
R=A/'docs/implementation/m3/native-publication/host-current-replay-r1/evidence'
N=A/'docs/implementation/m3/native-publication/host-native-current-r1/evidence/authoring'
source=(R/'rebuild_replay.py').read_text()
tree=ast.parse(source);nodes=[]
for n in tree.body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='original' for t in n.targets):break
 nodes.append(n)
nodes.extend(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('sub','rebuild_blob'))
common=ast.unparse(ast.Module(body=nodes,type_ignores=[]))+'\n'
common=common.replace("P = Path('/Users/sb/code/opensip-ai/opensip')", "P = Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover')")
common=common.replace("W = P.parent / 'opensip-host-current-corpus'", "W = Path(__file__).resolve().parent / 'replay-candidate'")
common=common.replace('e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773','81d57d6d68bd1c310d632148fe3c4c3b9b23e224603465e1a9f43062cc8f0712')
common=common.replace("assert NEW == '81d57d6d68bd1c310d632148fe3c4c3b9b23e224603465e1a9f43062cc8f0712'", "assert NEW == '7179d52e3b7ce7400a3ab24badcae5b4242acab7c1cb4523032adf4c706d3132'")
common+='''
INITIAL_MAPPING={OLD:NEW,'53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a':'3add72f2cecd755be5e21795cfee545cdc68ff80ed8c43fedd417093917ade62'}
replacement_blobs={OLD:current,'53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a':(P/'schemas/sources/relation-payload-v2.schema.json').read_bytes()}
assert all(hashlib.sha256(raw).hexdigest()==INITIAL_MAPPING[old] for old,raw in replacement_blobs.items())
original_rebuild_blob=rebuild_blob
def rebuild_blob(row):
 return replacement_blobs.get(row['digest']) if row['digest'] in replacement_blobs else original_rebuild_blob(row)
'''
(B/'reference.py').write_text(common)
bootstrap="""from pathlib import Path
import importlib.util
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('accepted_current_recipe',B/'reference.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
"""
for name,filename,outname in [('pooled','rebuild_pooled_r2.py','pooled-candidates-r1'),('native-context','rebuild_native_context.py','native-context-candidate')]:
 s=(N/filename).read_text();start=s.index('P=g.P;out=');s='from pathlib import Path\nimport ast,types,json,hashlib,copy\n'+bootstrap+s[start:]
 s=s.replace("B/'pooled-candidates-r2'","B/'pooled-candidates-r1'")
 s=s.replace("+name+'-fixtures.json'","+name+'-fixtures.current.json'")
 s=s.replace("g.mapping={g.OLD:g.NEW}","g.mapping=dict(g.INITIAL_MAPPING)")
 s=s.replace("+'-fixtures.current.json'","+'-fixtures.native-owner-r1.json'")
 # The preceding output rename also affects the source expression: restore it.
 s=s.replace("'crates/host/tests/fixtures/'+name+'-fixtures.native-owner-r1.json'","'crates/host/tests/fixtures/'+name+'-fixtures.current.json'")
 (B/(name+'.py')).write_text(s)
# Use the accepted replay reconstruction body on the already accepted current
# inputs; all expected verdicts and deliberate graph faults stay input data.
replay=source[source.index('original=(P/') :]
replay=replay.replace("'crates/host/tests/fixtures/replay-fixtures.json'","'crates/host/tests/fixtures/replay-fixtures.current.json'")
replay=replay.replace("mapping={OLD:NEW}","mapping=dict(INITIAL_MAPPING)")
replay=replay.replace("out=W/'crates/host/tests/fixtures/replay-fixtures.current.json';assert not out.exists();out.write_bytes(raw)","out=B/'replay-fixtures.native-owner-r1.json';assert not out.exists();out.write_bytes(raw)")
replay=replay.replace(" and (W/'crates/host/tests/fixtures/replay-fixtures.current.json').read_bytes()==original",'')
replay_tree=ast.parse(replay)
replay_tree.body=[n for n in replay_tree.body if not(isinstance(n,ast.FunctionDef) and n.name in ('sub','rebuild_blob'))]
(B/'replay.py').write_text(common+'\n'+ast.unparse(replay_tree)+'\n')
cycle=(R/'rebuild_cycle.py').read_text();start=cycle.index('P=g.P;W=g.W;');cycle='from pathlib import Path\nimport ast,json,hashlib,copy,types\n'+bootstrap+cycle[start:]
cycle=cycle.replace("'crates/evaluator/tests/fixtures/cycle-representative.v1.json'","'crates/evaluator/tests/fixtures/cycle-representative.current.v1.json'")
cycle=cycle.replace('g.mapping={g.OLD:g.NEW}','g.mapping=dict(g.INITIAL_MAPPING)')
cycle=cycle.replace("out=W/'crates/evaluator/tests/fixtures/cycle-representative.current.v1.json'","out=B/'cycle-representative.native-owner-r1.v1.json'")
cycle=cycle.replace(" and(W/rel).read_bytes()==raw",'')
# No runtime include is changed by this authoring stage.
cut=cycle.index("p=W/'crates/evaluator/src/atoms.rs'");resume=cycle.index('report=dict(',cut);cycle=cycle[:cut]+cycle[resume:]
(B/'cycle.py').write_text(cycle)
pins=[]
for p in [R/'rebuild_replay.py',R/'rebuild_cycle.py',N/'rebuild_pooled_r2.py',N/'rebuild_native_context.py',A/'docs/coop/design-corrections/foundation/identity-model.v3.py']:
 raw=p.read_bytes();pins.append(dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
(B/'accepted-recipe-inputs.json').write_text(json.dumps(dict(standing='UNREVIEWED PUBLIC SYNTHETIC COMPANION AUTHORING; NO PRODUCT WRITES',recipeInputs=pins,schemaReplacements=2,expectedVerdictsNotRewritten=True),indent=2)+'\n')
print('Prepared explicit recipe adaptations under',B)

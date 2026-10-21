"""Prepare retained native-owner predecessor descriptions after accepted code and inventory integration.
Preserve the immutable selected inventory; use the existing contract profile.
"""
from pathlib import Path
import json, hashlib, subprocess, os

F = Path(__file__).parent
B = F / 'descriptions'
S = B / 'architecture'
P = Path('/Users/sb/code/opensip-ai/opensip')
A = P.parent / 'opensip_arch'
Q = Path('/tmp/opensip-implementation/reviews/codex-native-owner-descriptions-r1')
PRE = 'docs/implementation/m3/native-publication/native-owner-descriptions-r1'
UNIT = 'NATIVE-OWNER-DESCRIPTIONS-r1'
ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_CONFIG_COUNT']:
    ENV.pop(k, None)

def git(root, *args):
    return subprocess.check_output(['/usr/bin/git', *args], cwd=root, env=ENV, text=True).strip()

def pin(root, path):
    raw = (root / path).read_bytes()
    return dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

assert not B.exists() and not Q.exists()
integration = json.loads((F / 'integration.json').read_text())
assert integration['unit'] == 'NATIVE-OWNER-MATERIALIZATION-r2'
inventory_integration=json.loads((F/'inventory/integration.json').read_text())
assert git(P,'rev-parse','HEAD')==inventory_integration['productLock']
assert git(A,'rev-parse','HEAD')==inventory_integration['architecture']
assert subprocess.run(['/usr/bin/git','merge-base','--is-ancestor',integration['productCode'],'HEAD'],cwd=P,env=ENV).returncode==0
assert not git(P, 'status', '--porcelain') and not git(A, 'diff', '--name-only', 'HEAD')
lock = json.loads((P / 'design-lock.json').read_text())
parent = lock['inventorySuccessors'][-1]['candidate']
assert pin(A, parent['path']) == parent
doc = json.loads((A / parent['path']).read_text())
indices = {r['path']: i for i, r in enumerate(doc['files'])}
after={}
readiness=json.loads((F/'inventory-readiness.json').read_text())
for row in readiness['newPaths']:
 path=row['retainedPredecessor'];current=row['path'];assert path in indices and current in indices
 assert (P/path).exists() and (P/current).exists()
 if row['role']=='registry':
  after[path]='Retained pre-native-owner current-schema runtime metadata predecessor, preserved byte-exact with its original schema digest bindings. The owning runtime include now selects '+current+'. This predecessor adds no producer, owner, selector, semantic source registration or current admission authority; no qualification follows.'
 else:
  after[path]='Retained pre-native-owner current-schema SYNTHETIC fixture predecessor, preserved byte-exact with its original objects, blobs, faults and expectations. Current owning controls select '+current+' with the separately accepted current schema and dependent identity bindings. Retaining this predecessor grants no raw-source guard exception, successful admission, live compiler/provider/custody/source re-registration, durable publication or product qualification.'
assert len(after)==15

overrides = []
for path in sorted(after, key=lambda p: indices[p]):
    row = doc['files'][indices[path]]
    overrides.append(dict(parent=parent, selector=dict(jsonPointer=f'/files/{indices[path]}/description'), before=row['description'], after=after[path]))
# A direct first override must not restate an inherited or existing direct meaning.
for e in lock['inventoryPassageInheritance']:
    p = json.loads((A / e['parent']['path']).read_text())
    assert p['files'][int(e['selector']['jsonPointer'].split('/')[2])]['path'] not in after
for binding in lock['contractSuccessors']:
    record = json.loads((A / binding['record']['path']).read_text())
    for e in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
        parts = e['selector'].get('jsonPointer', '').split('/')
        if len(parts) == 4 and parts[1] == 'files' and parts[3] == 'description':
            p = json.loads((A / e['parent']['path']).read_text())
            assert p['files'][int(parts[2])]['path'] not in after
code_pre = 'docs/implementation/m3/native-publication/native-owner-patterns-materialization-r2'
authorities = [pin(A, p) for p in [code_pre+'-unit.json', code_pre+'-subject.json', code_pre+'/product-map.json', 'docs/implementation/m3/reviews/codex-native-owner-materialization-r2/review.json', inventory_integration['subjectManifest']['path'], inventory_integration['review']['path']]]
for r in json.loads((A / (code_pre+'/product-map.json')).read_text())['rows']:
    assert pin(P, r['path']) == r['candidate']
readme = PRE+'/README.md'
(S/readme).parent.mkdir(parents=True)
(S/readme).write_text(f'''# Retained native-owner predecessor description qualification

Fifteen first direct description overrides qualify physically retained .current fixture/metadata predecessors after exact accepted materialization and additive inventory binding. Their original bytes remain intact; active owning includes/readers now select the distinct .native-owner-r1 companions. No predecessor is erased or treated as a current selected raw-source guard exception. New companion descriptions remain in the preceding additive inventory.

The existing additive inventory profile preserves inherited rows by value; this existing contract passage-override profile qualifies their selected meaning without rewriting the raw inventory or113inherited passage bindings. Packages, edges, pending decisions, planned absences and inventory successor count remain unchanged. No code, profile, receipt, semantic source registration, successful admission population, production caller or qualification changes.

The blind receipt stays STALE/PENDING until the mandatory separate exact-main pre-run gate, one authorized blind refresh and independent post-run acceptance/root assent. No census-dependent continuation occurs before that gate. Whole-project duties remain open.
''')
source_rel = PRE+'/source.json'
write(S/source_rel, dict(productHead=git(P,'rev-parse','HEAD'), architectureHead=git(A,'rev-parse','HEAD'), productLock=pin(P,'design-lock.json'), authorities=authorities, selectedInventory=parent, changedDescriptionPaths=sorted(after), contractSuccessorsBefore=len(lock['contractSuccessors']), contractSuccessorsAfter=len(lock['contractSuccessors'])+1, inventorySuccessorsUnchanged=len(lock['inventorySuccessors']), inheritanceRowsUnchanged=len(lock['inventoryPassageInheritance']), noEarlierMeaningRestated=True, productCodeChanged=False, productQualification=False))
candidates = sorted([pin(S,readme),pin(S,source_rel)], key=lambda r:r['path'])
record_rel = PRE+'/successor.json'
write(S/record_rel,dict(schemaVersion=1,standing='PROPOSED description-only native-owner predecessor successor; exact independent design-unit review and root assent required',parents=[parent],candidates=candidates,passageOverrides=overrides))
record = pin(S,record_rel)
manifest_rel=PRE+'-subject.json'
write(S/manifest_rel,dict(schemaVersion=1,unit=UNIT,files=sorted(candidates+[record],key=lambda r:r['path'])))
prepared=dict(unit=UNIT,stage=str(S),parent=parent,record=record,subjectManifest=pin(S,manifest_rel),reviewDirectory=str(Q),productHead=git(P,'rev-parse','HEAD'),architectureHead=git(A,'rev-parse','HEAD'),contractSuccessorAfter=len(lock['contractSuccessors'])+1,overrides=15)
write(B/'prepared.json',prepared);Q.mkdir(parents=True);write(Q/'subject.json',prepared)
expected=dict(verdict='ACCEPT-DESIGN-UNIT',subjectManifestSha256=prepared['subjectManifest']['sha256'],requiredFindings=[],nonBlockingObservations=[],passageOverrides=15,beforeTextsExact=True,afterTextsAccurate=True,noEarlierMeaningRestated=True,productCodeChanged=False,productQualification=False)
(Q/'REQUEST.md').write_text(f'''# Native-owner retained predecessor description qualification

Read subject.json and frozen stage {S}. Rehash every manifest member, selected inventory and exact integrated accepted code/map plus inventory binding authorities. Judge all15exact before/after descriptions as retained pre-native-owner .current predecessors and verify owning source includes/readers select their named .native-owner-r1 siblings. Original predecessor files remain byte-exact, never erased. This discharges the explicit retained-description obligation carried by accepted complete materialization and its additive inventory. Check whether any other description requires qualification; do not silently omit one.

Verify15first direct passage overrides with no prior direct/inherited override or supersession for these rows. Raw selected inventory remains byte-exact, inherited rows/packages/pending/planned state and113inheritance bindings unchanged; inventory successor count unchanged. Append existing contract successor{prepared['contractSuccessorAfter']}only; no code, source/alias/entrypoint, owner/semantic registration, receipt or successful admission change. Current blind receipt remains STALE/PENDING; immediate separately reviewed exact-main one-run refresh before dependent consumption is still mandatory. No product/project qualification.

Read-only hashes/JSON/Git/source only. No repo/worktree/stage/control/evidence edits, tests/builds/Cargo/lanes/network/panes/delegation/private413/keys/installations/heldout/T2/census modes. Write ONLY REVIEW.md and review.json in {Q}. Independently check JSON fields below plus any OWNPAT-DESC-R1-RF-n/NBO-n:

{json.dumps(expected,indent=2)}
''')
print(json.dumps(prepared,indent=2))

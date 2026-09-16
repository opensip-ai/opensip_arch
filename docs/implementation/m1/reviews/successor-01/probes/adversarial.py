"""Independent adversarial probes for design-lock v2 (reviewer-authored)."""
import copy, hashlib, importlib.util, json, shutil, sys, tempfile
from pathlib import Path
S=Path('/tmp/opensip-implementation/m1-successor-subject-01'); A=Path('/Users/sb/code/opensip-ai/opensip_arch')
spec=importlib.util.spec_from_file_location('vd',S/'tools/verify_design.py'); M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
LOCK=M.decode((S/'design-lock.json').read_bytes())
results=[]
def run(name, fn, expect):
    try:
        out=fn(); got='ACCEPT'
    except M.DesignError as e: got='REFUSE'; out=str(e)
    except Exception as e: got='CRASH'; out=f'{type(e).__name__}: {e}'
    ok = got==expect
    results.append((ok,name,expect,got,str(out)[:160])); print(('PASS ' if ok else 'UNEXPECTED ')+f'{name}: expect={expect} got={got} :: {str(out)[:160]}')
def lockv(mut):
    l=copy.deepcopy(LOCK); mut(l); return lambda: M.verify(A,l)
def pin(path):
    raw=(A/path).read_bytes(); return {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
IS=lambda l:l['inventorySuccessor']
# --- lock-level, real architecture checkout
run('baseline real v2', lockv(lambda l:None), 'ACCEPT')
run('v1 lock carrying inventorySuccessor', lockv(lambda l:l.update(schemaVersion=1)), 'REFUSE')
run('v2 lock without inventorySuccessor', lockv(lambda l:l.pop('inventorySuccessor')), 'REFUSE')
for v in (2.0,'2',3,True,None): run(f'schemaVersion={v!r}', lockv(lambda l,v=v:l.update(schemaVersion=v)), 'REFUSE')
for v in (None,[],'x',{}): run(f'inventorySuccessor={v!r}', lockv(lambda l,v=v:l.update(inventorySuccessor=v)), 'REFUSE')
run('successor pin extra field', lockv(lambda l:IS(l)['candidate'].update(note='x')), 'REFUSE')
run('successor pin uppercase sha', lockv(lambda l:IS(l)['record'].update(sha256=IS(l)['record']['sha256'].upper())), 'REFUSE')
run('successor pin bytes True', lockv(lambda l:IS(l)['assent'].update(bytes=True)), 'REFUSE')
run('successor pin bytes float', lockv(lambda l:IS(l)['assent'].update(bytes=2464.0)), 'REFUSE')
run('successor pin traversal', lockv(lambda l:IS(l)['review'].update(path='docs/../docs/implementation/m1/reviews/canonical-03/review.json')), 'REFUSE')
run('successor pin missing file', lockv(lambda l:IS(l)['review'].update(path='docs/implementation/m1/reviews/canonical-99/review.json')), 'REFUSE')
run('select superseded unaccepted inventory v2 (honest repin)', lockv(lambda l:IS(l).update(candidate=pin('docs/implementation/m1/repository-file-inventory.v2.json'))), 'REFUSE')
run('select superseded record v1 (honest repin)', lockv(lambda l:IS(l).update(record=pin('docs/implementation/m1/inventory-successor.json'))), 'REFUSE')
if (A/'docs/implementation/m1/reviews/canonical-02/review.json').exists():
    run('select older canonical-02 review (honest repin)', lockv(lambda l:IS(l).update(review=pin('docs/implementation/m1/reviews/canonical-02/review.json'))), 'REFUSE')
run('swap record and review pins', lockv(lambda l:IS(l).update(record=IS(l)['review'],review=IS(l)['record'])), 'REFUSE')
run('candidate path equals parent (parent as candidate)', lockv(lambda l:IS(l).update(candidate=dict(IS(l)['parent']))), 'REFUSE')
run('parent = different selected input', lockv(lambda l:IS(l).update(parent=pin('docs/coop/design-corrections/workflows/command-inventory.v3.json'))), 'REFUSE')
run('parent removed from inputs', lockv(lambda l:l.update(inputs=[r for r in l['inputs'] if r['path']!=IS(l)['parent']['path']])), 'REFUSE')
run('parent pin key order permuted (same values)', lockv(lambda l:IS(l).update(parent={'bytes':IS(l)['parent']['bytes'],'sha256':IS(l)['parent']['sha256'],'path':IS(l)['parent']['path']})), 'ACCEPT')
run('assent pin -> review file (role confusion)', lockv(lambda l:IS(l).update(assent=IS(l)['review'])), 'REFUSE')
# --- document-level: mutated copies of real evidence in a scratch root, rebound honestly
KEYS=('parent','candidate','record','review','assent')
def scratch(mutators):
    d=Path(tempfile.mkdtemp(prefix='succ-',dir='/tmp/opensip-implementation/m1-successor-review-01/probes'))
    try:
        b=copy.deepcopy(LOCK['inventorySuccessor']); docs={}
        for k in KEYS:
            (d/b[k]['path']).parent.mkdir(parents=True,exist_ok=True); docs[k]=json.loads((A/b[k]['path']).read_bytes())
        for k,f in mutators:
            if k in KEYS: f(docs[k])
        def put(k):
            raw=(json.dumps(docs[k],indent=2)+'\n').encode(); (d/b[k]['path']).write_bytes(raw)
            b[k].update(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
        # rebind chain in dependency order: parent,candidate -> record -> review -> assent
        put('parent'); put('candidate')
        docs['record']['parent']=dict(b['parent']); docs['record']['candidate']=dict(b['candidate']); put('record')
        a=docs['review']['inventoryCandidateAssessment']; a.update(path=b['candidate']['path'],sha256=b['candidate']['sha256'],bytes=b['candidate']['bytes'])
        a['parent'].update(sha256=b['parent']['sha256'],bytes=b['parent']['bytes']); a['successorRecord'].update(sha256=b['record']['sha256'])
        for k,f in mutators:
            if k=='review!': f(docs['review'])
        put('review')
        docs['assent']['actualClaudeReview']['sha256']=b['review']['sha256']; docs['assent']['acceptedInventory']['sha256']=b['candidate']['sha256']
        for k,f in mutators:
            if k=='assent!': f(docs['assent'])
        put('assent')
        return M.inventory_successor(d,b,[b['parent']])
    finally: shutil.rmtree(d)
def sc(*m): return lambda: scratch([x for x in m if x[0] in KEYS]+[x for x in m if x[0] not in KEYS]) 
def noop(d): pass
run('scratch baseline (reserialized, rebound)', sc(), 'ACCEPT')
def inh(f): return ('candidate', lambda d: f(next(r for r in d['files'] if r['path']=='README.md' or True)))
run('inherited row generated false->0 (JSON type change)', sc(('candidate',lambda d:d['files'][0].update(generated=0))), 'REFUSE')
run('inherited row generated false->0.0', sc(('candidate',lambda d:d['files'][0].update(generated=0.0))), 'REFUSE')
run('inherited row field reorder only', sc(('candidate',lambda d:d['files'].__setitem__(0,dict(reversed(list(d['files'][0].items())))))), 'ACCEPT')
run('inherited row description edited', sc(('candidate',lambda d:d['files'][0].update(description='x'))), 'REFUSE')
run('inherited row extra key', sc(('candidate',lambda d:d['files'][0].update(extra=None))), 'REFUSE')
run('package dependency added', sc(('candidate',lambda d:d['packages'][0].setdefault('dependencies',[]).append('zz') if isinstance(d['packages'][0],dict) else None)), 'REFUSE')
run('pendingDecisions changed', sc(('candidate',lambda d:d['pendingDecisions'].append('x'))), 'REFUSE')
run('added row with undeclared package', sc(('candidate',lambda d:(d['files'].append({'path':'zzz/new.rs','package':'no-such-package','role':'test','description':'','generated':False,'standing':''}),d['files'].sort(key=lambda r:r['path'])))), 'ACCEPT')
run('added row with noncanonical path ../escape', sc(('candidate',lambda d:(d['files'].append({'path':'../escape','package':'tooling','role':'test'}),d['files'].sort(key=lambda r:r['path'])))), 'ACCEPT')
run('added row missing required row fields', sc(('candidate',lambda d:(d['files'].append({'path':'zzz'}),d['files'].sort(key=lambda r:r['path'])))), 'ACCEPT')
run('candidate rows unsorted', sc(('candidate',lambda d:d['files'].reverse())), 'REFUSE')
run('candidate removes inherited row, adds one', sc(('candidate',lambda d:(d['files'].pop(0),d['files'].append({'path':'zzzz'})))), 'REFUSE')
run('candidate identical rows (no addition)', sc(('candidate',lambda d:d.update(files=json.loads((A/LOCK['inventorySuccessor']['parent']['path']).read_bytes())['files']))), 'REFUSE')
run('candidate top-level extra key', sc(('candidate',lambda d:d.update(extra=1))), 'REFUSE')
run('candidate standing non-string', sc(('candidate',lambda d:d.update(standing=None))), 'ACCEPT')
run('candidate schemaVersion 1->True', sc(('candidate',lambda d:d.update(schemaVersion=True))), 'REFUSE')
run('record parentArtifactBytesUnchanged "true"', sc(('record',lambda d:d.update(parentArtifactBytesUnchanged='true'))), 'REFUSE')
run('record independentAcceptancePending true (historical, ignored)', sc(), 'ACCEPT')
run('review verdict ACCEPT (not -UNIT)', sc(('review!',lambda d:d.update(verdict='ACCEPT'))), 'REFUSE')
run('review requiredFindings missing', sc(('review!',lambda d:d.pop('requiredFindings'))), 'REFUSE')
run('review assessment verdict CHANGES-REQUIRED', sc(('review!',lambda d:d['inventoryCandidateAssessment'].update(verdict='CHANGES-REQUIRED'))), 'REFUSE')
run('review assessment bytes wrong', sc(('review!',lambda d:d['inventoryCandidateAssessment'].update(bytes=1))), 'REFUSE')
run('review assessment bytes float-equal', sc(('review!',lambda d:d['inventoryCandidateAssessment'].update(bytes=float(d['inventoryCandidateAssessment']['bytes'])))), 'REFUSE')
run('review assessment parent path different', sc(('review!',lambda d:d['inventoryCandidateAssessment']['parent'].update(path='x.json'))), 'REFUSE')
run('review subject digest changed', sc(('review!',lambda d:d.update(subjectManifestSha256='0'*64))), 'REFUSE')
run('review subject digest missing both sides', sc(('review!',lambda d:d.pop('subjectManifestSha256')),('assent!',lambda d:d['subjectManifest'].pop('sha256'))), 'REFUSE')
run('assent status ACCEPTED', sc(('assent!',lambda d:d.update(status='ACCEPTED'))), 'REFUSE')
run('assent requiredUnitFindings missing', sc(('assent!',lambda d:d.pop('requiredUnitFindings'))), 'REFUSE')
run('assent rootSubstantiveAssent 1', sc(('assent!',lambda d:d.update(rootSubstantiveAssent=1))), 'REFUSE')
run('assent acceptedInventory path differs', sc(('assent!',lambda d:d['acceptedInventory'].update(path='other.json'))), 'REFUSE')
run('assent actualClaudeReview missing', sc(('assent!',lambda d:d.pop('actualClaudeReview'))), 'REFUSE')
unexpected=[r for r in results if not r[0]]
print(f'\nTOTAL {len(results)} probes; unexpected {len(unexpected)}')
for r in unexpected: print('UNEXPECTED',r)

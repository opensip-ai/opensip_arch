from pathlib import Path
import argparse,copy,hashlib,importlib.util,json

# The one hundred and three rows inventory138 (unit E2a) projects from its
# parent, inventory137 (unit J2a): the one hundred and three inheritance rows
# a lock selecting inventory137 binds to it, as inventory137 projected them
# (inventory136's one hundred and the three direct overrides of
# read-endpoint-x3a2-descriptions on inventory136). No bound contract
# successor has a passage override or supersession on inventory137. The one
# projected row sorted after the twenty-two inserted paths moves. inventory137
# is not yet integrated: when the given lock selects inventory136, J2a's
# staged entry (its evidence/verify_scratch.py) is applied in memory first, as
# J2a stages it. Checked at product d2c00a9.
ROWS=103

def pinned(root,row):
    p=root/row['path'];b=p.read_bytes()
    assert len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
    return json.loads(b)

def expected(root,record,lock):
    assert lock['inventorySuccessors'][-1]['candidate']==record['parent']
    parent=pinned(root,record['parent']);candidate=pinned(root,record['candidate'])
    rows={r['path']:(i,r)for i,r in enumerate(candidate['files'])}
    assert len(rows)==len(candidate['files'])
    overrides={}
    def add(o):
        assert o['parent']==record['parent']
        parts=o['selector']['jsonPointer'].split('/')
        assert len(parts)==4 and parts[1]=='files'and parts[2].isdigit()and parts[3]=='description'
        row=parent['files'][int(parts[2])];assert row['description']==o['before']
        if row['path']in overrides:assert overrides[row['path']]==o
        overrides[row['path']]=o
    for o in lock['inventoryPassageInheritance']:add(o)
    folds={}
    for binding in lock['contractSuccessors']:
        successor=pinned(root,binding['record'])
        for o in successor['passageOverrides']:
            if o['parent']==record['parent']:add(o)
        for s in successor.get('passageSupersessions',[]):
            if s['parent']!=record['parent']:continue
            path=parent['files'][int(s['selector']['jsonPointer'].split('/')[2])]['path']
            assert path not in folds;folds[path]=s
    out=[]
    for path,o in sorted(overrides.items()):
        source=parent['files'][int(o['selector']['jsonPointer'].split('/')[2])]
        index,target=rows[path];assert source==target
        effective=o['after']
        if path in folds:
            s=folds.pop(path);assert s['before']==effective and s['selector']==o['selector'];effective=s['after']
        out.append({'filePath':path,'parentSelector':o['selector'],'candidateSelector':{'jsonPointer':f'/files/{index}/description'},'before':o['before'],'effectiveDescription':effective})
    assert not folds,sorted(folds)
    assert len(out)==ROWS
    return out

def with_parent(root,record,lock):
    if lock['inventorySuccessors'][-1]['candidate']==record['parent']:return lock
    spec=importlib.util.spec_from_file_location('j2a_scratch',root/'docs/implementation/m2/host-invocation-j2a-inventory-v137/evidence/verify_scratch.py')
    j2a=importlib.util.module_from_spec(spec);spec.loader.exec_module(j2a);return j2a.staged(lock)

def verify(rows,wanted):assert rows==wanted

def main():
    p=argparse.ArgumentParser();p.add_argument('--architecture',type=Path,required=True);p.add_argument('--lock',type=Path,required=True);a=p.parse_args()
    record=json.loads((Path(__file__).parent/'successor.json').read_bytes());lock=with_parent(a.architecture,record,json.loads(a.lock.read_bytes()));wanted=expected(a.architecture,record,lock);verify(record['descriptionOverrideProjection'],wanted)
    refused=0
    for i in range(ROWS):
        for key,value in [('filePath','wrong'),('parentSelector',{'jsonPointer':'/files/0/description'}),('candidateSelector',{'jsonPointer':'/files/0/description'}),('before','wrong'),('effectiveDescription','wrong')]:
            bad=copy.deepcopy(wanted);bad[i][key]=value
            try:verify(bad,wanted)
            except AssertionError:refused+=1
            else:raise AssertionError('corruption accepted')
    for bad in (wanted[:-1],wanted+[wanted[0]], [r for r in wanted if r['filePath']!='crates/host/src/installation_lineage.rs']):
        try:verify(bad,wanted)
        except AssertionError:refused+=1
        else:raise AssertionError('changed rowset accepted')
    print(json.dumps({'readOnly':True,'projectionRows':ROWS,'positive':'PASS','corruptionsRefused':refused,'directParentOverrideIncluded':True}))
if __name__=='__main__':main()

from pathlib import Path
import argparse,copy,hashlib,json

# The fifty-five rows the lock binds to inventory131 (inventory133's parent,
# unit X9-5): the sixteen carried unchanged from inventory81 onward (eight
# inherited through inventory80 and 461b's eight overrides on inventory80)
# and D1's thirty-nine overrides, joined at inventory122, with D2's four
# passage supersessions already folded into their effective descriptions
# when inventory123 was integrated, and carried through inventory118,
# inventory129, inventory130 and inventory131. No contract successor binds
# an override to inventory131 itself. A contract successor the lock binds
# may supersede an inherited row on inventory131 (law VD1): each
# supersession names that row's current meaning as its before, and is folded
# into the row's effective description. None does at product eb0d503. The
# row count stays fifty-five.
ROWS=55

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

def verify(rows,wanted):assert rows==wanted

def main():
    p=argparse.ArgumentParser();p.add_argument('--architecture',type=Path,required=True);p.add_argument('--lock',type=Path,required=True);a=p.parse_args()
    record=json.loads((Path(__file__).parent/'successor.json').read_bytes());lock=json.loads(a.lock.read_bytes());wanted=expected(a.architecture,record,lock);verify(record['descriptionOverrideProjection'],wanted)
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

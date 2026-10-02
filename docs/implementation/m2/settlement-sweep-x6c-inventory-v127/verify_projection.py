from pathlib import Path
import argparse,copy,hashlib,json

# The fifty-five rows the lock binds to the parent: the sixteen carried
# unchanged from inventory81 onward (eight inherited through inventory80 and
# 461b's eight overrides on inventory80) and D1's thirty-nine overrides,
# joined at inventory122. D2's four passage supersessions are on
# inventory122; X5a's inventory123 folded them, and the lock binds them to
# inventory126 (unit X6b) as plain inheritance rows, so none is left to fold
# on that parent.
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
    for binding in lock['contractSuccessors']:
        for o in pinned(root,binding['record'])['passageOverrides']:
            if o['parent']==record['parent']:add(o)
    # Contract successor D2's passage supersessions on the parent (law VD1
    # item 3): each ends its row's current meaning, and its after becomes the
    # effective description. The row count does not change.
    folded=0
    for binding in lock['contractSuccessors']:
        for s in pinned(root,binding['record']).get('passageSupersessions',[]):
            if s['parent']!=record['parent']:continue
            hits=[path for path,o in overrides.items()if o['selector']==s['selector']]
            assert len(hits)==1 and overrides[hits[0]]['after']==s['before'],s['selector']
            overrides[hits[0]]=dict(overrides[hits[0]],after=s['after']);folded+=1
    d2=json.loads((root/'docs/implementation/m2/description-batch-d2/successor.json').read_bytes())['passageSupersessions']
    assert folded==(4 if record['parent']==d2[0]['parent'] else 0)
    out=[]
    for path,o in sorted(overrides.items()):
        source=parent['files'][int(o['selector']['jsonPointer'].split('/')[2])]
        index,target=rows[path];assert source==target
        out.append({'filePath':path,'parentSelector':o['selector'],'candidateSelector':{'jsonPointer':f'/files/{index}/description'},'before':o['before'],'effectiveDescription':o['after']})
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

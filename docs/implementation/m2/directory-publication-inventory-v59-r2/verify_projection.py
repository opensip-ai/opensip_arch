from pathlib import Path
import json,copy,argparse

def verify(record,parent,candidate,lock):
 rows=record['descriptionOverrideProjection'];expected=[];by={r['path']:(i,r)for i,r in enumerate(candidate['files'])}
 assert len(by)==len(candidate['files'])
 for old in lock['inventoryPassageInheritance']:
  assert old['parent']==record['parent']
  bits=old['selector']['jsonPointer'].split('/');assert len(bits)==4 and bits[1]=='files'and bits[3]=='description'
  source=parent['files'][int(bits[2])];index,target=by[source['path']];assert target==source and source['description']==old['before']
  expected.append({'filePath':source['path'],'parentSelector':old['selector'],'candidateSelector':{'jsonPointer':f'/files/{index}/description'},'before':old['before'],'effectiveDescription':old['after']})
 assert rows==sorted(expected,key=lambda r:r['filePath'])and len(rows)==4
 return rows

def main():
 a=argparse.ArgumentParser();a.add_argument('--architecture',type=Path,required=True);a.add_argument('--lock',type=Path,required=True);q=a.parse_args();u=Path(__file__).resolve().parent;r=json.loads((u/'successor.json').read_bytes());p=json.loads((q.architecture/r['parent']['path']).read_bytes());c=json.loads((q.architecture/r['candidate']['path']).read_bytes());l=json.loads(q.lock.read_bytes());verify(r,p,c,l);count=0
 for i in range(4):
  for key,value in [('filePath','wrong'),('candidateSelector',{'jsonPointer':'/files/0/description'}),('before','wrong'),('effectiveDescription','wrong')]:
   bad=copy.deepcopy(r);bad['descriptionOverrideProjection'][i][key]=value
   try:verify(bad,p,c,l)
   except (AssertionError,KeyError,ValueError):count+=1
   else:raise AssertionError('corruption accepted')
 for rows in (r['descriptionOverrideProjection'][:-1],r['descriptionOverrideProjection']+[r['descriptionOverrideProjection'][0]]):
  bad=copy.deepcopy(r);bad['descriptionOverrideProjection']=rows
  try:verify(bad,p,c,l)
  except AssertionError:count+=1
  else:raise AssertionError('changed rowset accepted')
 print(json.dumps({'projectionRows':4,'positive':'PASS','corruptionsRefused':count,'readOnly':True}))
if __name__=='__main__':main()

from pathlib import Path
import json,re
B=Path(__file__).resolve().parent;lines=(B/'checks-r3/native-owner.log').read_text().splitlines();decoder=json.JSONDecoder()
def parse(s,pos=0):
 while pos<len(s)and s[pos].isspace():pos+=1
 for word in ['Object','Array','String','Integer','Bool']:
  if s.startswith(word+'(',pos):
   v,end=parse(s,pos+len(word)+1);assert s[end]==')',(s[end:end+25],word);return v,end+1
 if s.startswith('Null',pos):return None,pos+4
 if s[pos]=='{':
  out={};pos+=1
  while s[pos]!='}':
   if s[pos]in ' ,':pos+=1;continue
   key,end=parse(s,pos);pos=end
   while s[pos]in ' :':pos+=1
   value,pos=parse(s,pos);out[key]=value
  return out,pos+1
 if s[pos]=='[':
  out=[];pos+=1
  while s[pos]!=']':
   if s[pos]in ' ,':pos+=1;continue
   value,pos=parse(s,pos);out.append(value)
  return out,pos+1
 return decoder.raw_decode(s,pos)
def diffs(a,b,path=''):
 if type(a)!=type(b):return [dict(path=path,left=a,right=b)]
 if isinstance(a,dict):
  out=[]
  for k in sorted(a.keys()|b.keys()):
   if k not in a or k not in b:out.append(dict(path=path+'/'+k,left=a.get(k),right=b.get(k)))
   else:out+=diffs(a[k],b[k],path+'/'+k)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [dict(path=path,leftLength=len(a),rightLength=len(b))]
  return sum((diffs(x,y,path+'/'+str(i))for i,(x,y)in enumerate(zip(a,b))),[])
 return []if a==b else [dict(path=path,left=a,right=b)]
rows=[];label=''
for i,line in enumerate(lines):
 if line.startswith('assertion '):label=line
 if line.startswith('  left: '):
  left=line[8:];right=lines[i+1].split('right: ',1)[1];a,end=parse(left);assert end==len(left);b,end=parse(right);assert end==len(right);rows.append(dict(assertion=label,differences=diffs(a,b)))
(B/'debug-differences-r3.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))

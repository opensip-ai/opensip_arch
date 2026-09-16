import json,re
pats=json.load(open('reviewer-patterns.json'))
bases=['a','..','a/..','../x','a/../b','x/y','1.2.3','sha256:'+'0'*64,'A_B','ab','/a','run3:'+'a'*64,'2026-01-01','0'*40,'--ab','a.b-c','a:b','ab12','DEPTH','DISCLOSURE-ONLY','#/$defs/Ab','/a-b/c','a/b/../../../etc']
ins=[chr(10),chr(13),chr(0x2028),chr(0x2029),chr(0x85),chr(0xa0),chr(9),chr(0x663),chr(0xe9)]
strs=set(bases)
for b in bases:
    for c in ins:
        strs.update([b+c,c+b,b[:1]+c+b[1:],'a'+c+'/'+b,b+c+'x'])
rows=[[p,s,bool(re.search(p,s))] for p in pats for s in sorted(strs)]
json.dump({'rows':rows},open('regex-py.json','w'))
print(len(rows))

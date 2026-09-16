import json,re,itertools
prof=json.load(open('/tmp/opensip-implementation/m1-ts-runtime-subject-02/pattern-profile.json'))['patterns']
alpha=['a','.','/','\\',chr(0),chr(10),chr(13),chr(0x2028),chr(0x85),'0','-','Z',':']
strs=['']
for n in range(1,6): strs+= [''.join(t) for t in itertools.product(alpha,repeat=n)]
# structured: identity-style prefixes with terminator insertion at every position
struct=set()
for r in prof:
    src=r['source']
    for pre in ['exec1_'+'a'*32,'req1_'+'a'*32,'sha256:'+'a'*64,'security.repo-execution-grant.v2:'+'a'*64,'securityXrepo-execution-grantsXv2:'+'a'*64,'1.2.3-a.b+c','2026-01-01T00:00:00Z','ENFORCED-PLATFORM:a.b','MARKER_CUSTODY:Cargo.toml:A_B','#/$defs/Ab','/a-b','ab','a/b/c','--ab']:
        for i in range(len(pre)+1):
            for t in [chr(10),chr(13),chr(0x2028),'\r\n','.','/','/..','\n/..']:
                struct.add(pre[:i]+t+pre[i:])
strs+=sorted(struct)
exp=[[1 if re.search(r['source'],s) else 0 for s in strs] for r in prof]
json.dump({'values':strs,'expected':[''.join(map(str,e)) for e in exp]},open('exhaust-cases.json','w'),ensure_ascii=True)
print(len(strs),'strings',len(strs)*len(prof),'comparisons')

# Independent residue hunt: EVERY schema location that can hold a 64-hex string,
# including $ref-to-Hash and $ref-to-Ref, with or without a prefix. Determines
# whether the "no residue" claim holds and whether prose scope matches enforcement.
import json,re,sys
B='/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections/foundation/'
sch=json.load(open(B+'identity-schemas.v2.json'))
D=sch['$defs']
HEXDEF=set()
# which $defs are, transitively, bare-64-hex string types
def isbarehex(n):
    p=n.get('pattern') if isinstance(n,dict) else None
    return isinstance(p,str) and re.match(r'^\^\[0-9a-f\]\{64\}(\(\?!\[\\s\\S\]\)|\$)$',p)
for k,v in D.items():
    if isbarehex(v): HEXDEF.add('#/$defs/'+k)
print('bare-hex $defs:',sorted(HEXDEF))

sites=[]
def walk(n,path,inprops):
    if isinstance(n,dict):
        ref=n.get('$ref')
        pat=n.get('pattern')
        hit=None
        if ref in HEXDEF: hit='ref:'+ref
        elif isinstance(pat,str) and re.match(r'^\^\[0-9a-f\]\{64\}(\(\?!\[\\s\\S\]\)|\$)$',pat): hit='inline-bare'
        elif isinstance(pat,str) and '[0-9a-f]{64}' in pat: hit='inline-prefixed:'+pat
        if hit: sites.append({'path':path,'kind':hit,'ann':n.get('x-opensip-digest')})
        for k,v in n.items(): walk(v,path+'/'+k,k=='properties')
    elif isinstance(n,list):
        for i,v in enumerate(n): walk(v,path+'/'+str(i),False)
walk(sch,'',False)
bare=[s for s in sites if s['kind'].startswith(('ref:','inline-bare'))]
pref=[s for s in sites if s['kind'].startswith('inline-prefixed')]
# exclude the $defs/Hash definition itself and other $def roots
def isdefroot(p): return re.fullmatch(r'/\$defs/[^/]+',p)
bare_fields=[s for s in bare if not isdefroot(s['path'])]
bare_unann=[s['path'] for s in bare_fields if not s['ann']]
pref_fields=[s for s in pref if not isdefroot(s['path'])]
pref_unann=[s['path'] for s in pref_fields if not s['ann']]
out={'bareHexSites':len(bare_fields),'bareUnannotated':bare_unann,
     'prefixedHexSites':len(pref_fields),'prefixedUnannotatedCount':len(pref_unann),
     'prefixedAnnotated':[s['path'] for s in pref_fields if s['ann']]}
reps={}
for s in bare_fields+pref_fields:
    if s['ann']: reps.setdefault(s['ann'].get('representation'),[]).append(s['path'])
out['representationCounts']={k:len(v) for k,v in reps.items()}
out['byDomainFields']=reps.get('by-domain',[])
out['hIdentityFields']=reps.get('h-identity',[])
print(json.dumps(out,indent=1))
json.dump({'sites':sites},open(sys.argv[1],'w'),indent=1)

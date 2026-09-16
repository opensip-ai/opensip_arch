import json
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
def load(t):
    return json.load(open(S+'/'+t+'/docs/coop/design-corrections/foundation/identity-report.json'))
a=load('baseline25'); b=load('src25')
for tag,d in [('baseline',a),('src25',b)]:
    print(tag,'passed=',d.get('passed'),'failed=',json.dumps(d.get('failed'))[:400],'checks type=',type(d['checks']).__name__,'len=',len(d['checks']))
ca,cb=a['checks'],b['checks']
if isinstance(ca,dict):
    ks=sorted(set(ca)|set(cb))
    diff=[k for k in ks if ca.get(k)!=cb.get(k)]
    print('differing checks:',len(diff))
    for k in diff[:30]: print('   ',k,'baseline=',ca.get(k),'src25=',cb.get(k))
else:
    print('list form; first item:',json.dumps(ca[0])[:300])

import json,glob,os
P='/tmp/opensip-design-corrections/post-reset-review.v5/probes/'
files=['claude-probes-A2.json','claude-probes-B.json','claude-probes-B2.json','claude-probes-C.json',
       'claude-probes-C3.json','claude-probes-C4.json','claude-probes-D.json','claude-probes-D2.json',
       'claude-probes-E.json','claude-probes-E2.json','claude-probes-F.json']
SUPERSEDED={
 'B.B4':'superseded by B2.B4 (probe defect: line-wrapped prose not whitespace-normalised)',
 'B.B6':'superseded by B2.B6 (probe defect: pin paths are repository-root relative)',
 'C.C2':'superseded by C3.C2/C2a-C2e and C4 (probe defect: crude substring search)',
 'C.C8':'superseded by C3.C8 (probe defect: normalisation compared fields that legitimately changed)',
 'C3.C2c':'superseded by C4.C2c (probe defect: conflated the semantic seal verdict with the output projection)',
 'D.D1':'superseded by D2.D1 (probe defect: preservation report concerns repository bytes)',
 'D.D7':'RETAINED AS FINDING (advisory ADV-2(v5)); not a probe defect',
 'D2.D1e':'superseded (probe defect: wrong assumption that no preserved file is carried in the snapshot)',
 'E.E3':'superseded by E2.E3 (probe defect: wrong JSON key, records not items)',
 'E.E7':'superseded by E2.E7/E7b/E7c/E7d (probe defect: over-strict added-line classifier)',
}
idx=[];tot=0;fails=[]
for f in files:
    grp=f.replace('claude-probes-','').replace('.json','')
    for r in json.load(open(P+f)):
        pid=grp+'.'+r['id']; tot+=1
        e={'probe':pid,'title':r['title'],'result':r['result'],'detail':r['detail'][:300]}
        if pid in SUPERSEDED: e['supersession']=SUPERSEDED[pid]
        idx.append(e)
        if r['result']=='FAIL' and pid not in SUPERSEDED: fails.append(pid)
live=[e for e in idx if 'supersession' not in e]
print('total probe records',tot)
print('superseded (probe defects, not product failures)',len([e for e in idx if 'supersession' in e and 'RETAINED' not in e['supersession']]))
print('live probes',len(live),'live PASS',sum(1 for e in live if e['result']=='PASS'),'live FAIL',sum(1 for e in live if e['result']=='FAIL'))
print('unresolved failures:',fails)
json.dump({'totalRecords':tot,'liveProbes':len(live),
           'livePass':sum(1 for e in live if e['result']=='PASS'),
           'liveFail':sum(1 for e in live if e['result']=='FAIL'),
           'supersessions':SUPERSEDED,'probes':idx},
          open(P+'probe-index.json','w'),indent=1)

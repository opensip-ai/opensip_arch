import json
P='/tmp/opensip-design-corrections/post-reset-review.v5/probes/'
files=['claude-probes-A2.json','claude-probes-B.json','claude-probes-B2.json','claude-probes-C.json',
       'claude-probes-C3.json','claude-probes-C4.json','claude-probes-D.json','claude-probes-D2.json',
       'claude-probes-E.json','claude-probes-E2.json','claude-probes-F.json','claude-probes-G.json']
SUPERSEDED={
 'B.B4':'superseded by B2.B4 - probe defect: line-wrapped prose was not whitespace-normalised',
 'B.B6':'superseded by B2.B6 - probe defect: pin paths are repository-root relative, not suite relative',
 'C.C2':'superseded by C3.C2/C2a-C2e and C4 - probe defect: crude substring search over the model source',
 'C.C8':'superseded by C3.C8 - probe defect: normalisation compared fields that legitimately changed',
 'C3.C2c':'superseded by C4.C2c - probe defect: conflated the sealed semantic verdict with the output projection',
 'D.D1':'superseded by D2.D1 - probe defect: the preservation report concerns repository bytes, not snapshot bytes',
 'D2.D1e':'superseded - probe defect: wrongly assumed no preserved file is carried in the snapshot',
 'E.E3':'superseded by E2.E3 - probe defect: wrong JSON key (records, not items)',
 'E.E7':'superseded by E2.E7/E7b/E7c/E7d - probe defect: over-strict added-line classifier',
}
FINDING={'D.D7':'ADV-2(v5)','B2.B6c':'ADV-3(v5)'}
idx=[];tot=0
for f in files:
    grp=f.replace('claude-probes-','').replace('.json','')
    for r in json.load(open(P+f)):
        pid=grp+'.'+r['id']; tot+=1
        e={'probe':pid,'title':r['title'],'result':r['result'],'detail':r['detail'][:320]}
        if pid in SUPERSEDED: e['supersededBy']=SUPERSEDED[pid]
        if pid in FINDING: e['raisedAs']=FINDING[pid]
        idx.append(e)
live=[e for e in idx if 'supersededBy' not in e]
lp=sum(1 for e in live if e['result']=='PASS'); lf=[e['probe'] for e in live if e['result']=='FAIL']
print('total records',tot,'| superseded probe defects',tot-len(live))
print('live probes',len(live),'PASS',lp,'FAIL',len(lf),lf)
json.dump({'reviewer':'actual Claude (Opus 5), fresh independent v5 design reviewer; authored none of the subject',
           'totalRecords':tot,'supersededProbeDefects':tot-len(live),
           'liveProbes':len(live),'livePass':lp,'liveFail':len(lf),'liveFailures':lf,
           'note':'Superseded entries are defects in my own probe construction, corrected in a later file, and are not product failures. The two live failures are raised as advisories, not required gaps.',
           'supersessions':SUPERSEDED,'findings':FINDING,'probes':idx},
          open(P+'probe-index.json','w'),indent=1)

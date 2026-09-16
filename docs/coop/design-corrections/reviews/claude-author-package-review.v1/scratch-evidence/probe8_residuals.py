import json,hashlib,os
PKG='/tmp/opensip-design-corrections/claude-return-review.v1/inputs/docs/coop/design-corrections/reviews/codex-author-followup.v2'
CAND='/tmp/opensip-design-corrections/candidate-subject.v25'
d=json.loads(open(PKG+'/evaluation-residual-author-assessment.json').read())
src=json.loads(open(CAND+'/docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json').read())
items=d['items']
srcitems=src['items'] if isinstance(src,dict) and 'items' in src else src
print('items',len(items),'uniqueIds',len(set(i['id'] for i in items)),'sourceItems',len(srcitems))
bad=[];ev_ok=0;ev_bad=0;ev_missing=0
grades={};applied={};hist={};assess={}
for i in items:
    sel=i['sourceSelector'];idx=int(sel.rsplit('/',1)[1])
    if idx>=len(srcitems):
        bad.append([i['id'],'selector-out-of-range',sel])
    else:
        txt=json.dumps(srcitems[idx])
        if i['sourceCorrection'] not in txt: bad.append([i['id'],'sourceCorrection-not-verbatim',sel])
    for e in i.get('evidence',[]):
        fp=os.path.join(CAND,e['path'])
        if not os.path.isfile(fp):
            ev_missing=ev_missing+1;bad.append([i['id'],'evidence-missing',e['path']])
        else:
            h=hashlib.sha256(open(fp,'rb').read()).hexdigest()
            if h==e['sha256']: ev_ok=ev_ok+1
            else:
                ev_bad=ev_bad+1;bad.append([i['id'],'evidence-sha-mismatch',e['path']])
        if e.get('resolveAgainst')!='frozen candidate25': bad.append([i['id'],'resolveAgainst',str(e.get('resolveAgainst'))])
    grades[i['independentGrade']]=grades.get(i['independentGrade'],0)+1
    applied[i['applied']]=applied.get(i['applied'],0)+1
    hist[i['historicalLimitationReclassified']]=hist.get(i['historicalLimitationReclassified'],0)+1
    assess[i['authorAssessment']]=assess.get(i['authorAssessment'],0)+1
print('evidenceRefs ok',ev_ok,'mismatch',ev_bad,'missing',ev_missing)
print('independentGrade',grades)
print('applied',applied)
print('historicalLimitationReclassified',hist)
print('authorAssessment',json.dumps(assess,indent=1))
print('problems',len(bad))
for b in bad[:25]: print('  ',b)

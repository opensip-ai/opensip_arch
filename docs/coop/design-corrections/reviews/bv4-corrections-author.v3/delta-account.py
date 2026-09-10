"""Aggregate delta vs frozen v13 and this-turn delta vs released v2."""
import hashlib,json,pathlib
FROZEN=pathlib.Path('/tmp/opensip-design-corrections/candidate-subject.v13')
V2=pathlib.Path('/tmp/opensip-design-corrections/bv4-corrections-author.v2/work')
V3=pathlib.Path('/tmp/opensip-design-corrections/bv4-corrections-author.v3/work')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tree=lambda r:{str(p.relative_to(r)):p for p in r.rglob('*') if p.is_file()}
fz,v2,v3=tree(FROZEN),tree(V2),tree(V3)
agg=[{'path':k,'beforeSha256':sha(fz[k]),'afterSha256':sha(v3[k])} for k in sorted(fz) if k in v3 and sha(fz[k])!=sha(v3[k])]
turn=[{'path':k,'v2Sha256':sha(v2[k]),'finalSha256':sha(v3[k])} for k in sorted(v2) if k in v3 and sha(v2[k])!=sha(v3[k])]
FORBIDDEN=('source-pins','-report.','validation-summary','readiness','crosswalk','/reviews/')
print(json.dumps({
 'fileCounts':{'frozenV13':len(fz),'v2':len(v2),'final':len(v3)},
 'aggregateVsFrozenV13':{'changedFiles':agg,'changedCount':len(agg),
   'additions':sorted(set(v3)-set(fz)),'deletions':sorted(set(fz)-set(v3))},
 'thisTurnVsV2':{'changedFiles':turn,'changedCount':len(turn),
   'additions':sorted(set(v3)-set(v2)),'deletions':sorted(set(v2)-set(v3))},
 'forbiddenPathsTouched':[c['path'] for c in agg if any(t in c['path'] for t in FORBIDDEN)],
 'historicalD9Sha256':sha(V3/'docs/coop/artifacts/d9-exit-contract.v1.14.json'),
 'historicalD9Unchanged':sha(V3/'docs/coop/artifacts/d9-exit-contract.v1.14.json')==sha(FROZEN/'docs/coop/artifacts/d9-exit-contract.v1.14.json'),
},indent=1))

"""Complete delta account: aggregate vs frozen v13 (for direct integration) and this turn vs v1."""
import hashlib,json,pathlib
FROZEN=pathlib.Path('/tmp/opensip-design-corrections/candidate-subject.v13')
V1=pathlib.Path('/tmp/opensip-design-corrections/bv4-corrections-author.v1/work')
V2=pathlib.Path('/tmp/opensip-design-corrections/bv4-corrections-author.v2/work')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tree=lambda r:{str(p.relative_to(r)):p for p in r.rglob('*') if p.is_file()}
fz,v1,v2=tree(FROZEN),tree(V1),tree(V2)
agg=[{'path':k,'beforeSha256':sha(fz[k]),'afterSha256':sha(v2[k]),
      'beforeBytes':fz[k].stat().st_size,'afterBytes':v2[k].stat().st_size}
     for k in sorted(fz) if k in v2 and sha(fz[k])!=sha(v2[k])]
turn=[{'path':k,'v1Sha256':sha(v1[k]),'finalSha256':sha(v2[k]),
       'v1Bytes':v1[k].stat().st_size,'finalBytes':v2[k].stat().st_size}
      for k in sorted(v1) if k in v2 and sha(v1[k])!=sha(v2[k])]
FORBIDDEN=('source-pins','-report.','validation-summary','/reviews/')
print(json.dumps({
 'frozenFileCount':len(fz),'v1FileCount':len(v1),'finalFileCount':len(v2),
 'aggregateVsFrozenV13':{'changedFiles':agg,'changedCount':len(agg),
   'added':sorted(set(v2)-set(fz)),'deleted':sorted(set(fz)-set(v2))},
 'thisTurnVsV1':{'changedFiles':turn,'changedCount':len(turn),
   'added':sorted(set(v2)-set(v1)),'deleted':sorted(set(v1)-set(v2))},
 'forbiddenPathsTouched':[c['path'] for c in agg if any(t in c['path'] for t in FORBIDDEN)],
},indent=1))

"""Root bounded differential check of provider transition reference behavior.
This exercises pure state transitions, not provider wire-schema validation, OS execution,
real compiler behavior or host qualification. Publication must preserve these old outcomes.
"""
from pathlib import Path
import argparse,importlib.util,hashlib,json,collections
p=argparse.ArgumentParser();p.add_argument('--before',type=Path,required=True);p.add_argument('--after',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out;out.mkdir(exist_ok=False)
rel='docs/coop/design-corrections/native/native_evidence_model.v2.py';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=load(a.before/rel,'root_protocol_before');new=load(a.after/rel,'root_protocol_after')
# Keep predecessor names and include successor additions: neither removal nor addition evades comparison.
frames=sorted({r['frame'] for module in [old,new] for r in module.PROTOCOL3_RULES if not r['frame'].startswith('*')}|set(old._PROCESS_FAULTS)|set(new._PROCESS_FAULTS)|{'unexpected-frame'})
events=[]
for f in frames:
 if f=='HelloAck':
  events.extend([{'frame':f,'capabilities':list(old.IDENTITY_TOKENS)},{'frame':f,'capabilities':[]},{'frame':f,'capabilities':list(old.IDENTITY_TOKENS)[:-1]}])
 elif f=='OpenUniverse':
  events.extend({'frame':f,'dependencyMode':d,'preparedMode':r} for d in [False,True] for r in [False,True])
 else:events.append({'frame':f})
def modes(trace):
 for x in reversed(trace):
  if x['frame']=='OpenUniverse':return bool(x.get('dependencyMode',False)),bool(x.get('preparedMode',False))
 return False,False
rows=[];mismatches=[];state_counts={}
for count in [1,2]:
 queue=collections.deque([[]]);seen=set()
 while queue:
  prefix=queue.popleft();state=old.protocol3_run(prefix,count)
  # The predecessor's full hidden state is represented by this key for the selected stage count:
  # modes guard transitions; phase/terminal/stages/identity/source-disclosure cover remaining state.
  key=(state['finalPhase'],state['terminalKind'],state['sourceBytesSent'],state['stagesCompleted'],state['identityNegotiated'],*modes(prefix))
  if key in seen:continue
  seen.add(key)
  for ev in events:
   trace=prefix+[ev];expected=old.protocol3_run(trace,count);actual=new.protocol3_run(trace,count)
   row={'stageCount':count,'events':trace,'before':expected,'after':actual,'equal':expected==actual};rows.append(row)
   if expected!=actual:mismatches.append(len(rows)-1)
   if len(trace)<30 and expected['finalPhase'] not in ['FAULT','DONE']:queue.append(trace)
  # Exercise absorbing states themselves, not only their entry.
  if state['finalPhase'] in ['FAULT','DONE']:continue
 state_counts[str(count)]=len(seen)
# Explicit post-terminal and FAULT absorption extensions are compared above when fault is reached,
# but queued terminal states are excluded from BFS expansion. Cover them directly now.
terminal_seeds={}
for row in rows:
 st=row['before'];k=(row['stageCount'],st['finalPhase'],st['terminalKind'])
 if st['finalPhase'] in ['FAULT','DONE'] and k not in terminal_seeds:terminal_seeds[k]=row
for seed in terminal_seeds.values():
 for ev in events:
  trace=seed['events']+[ev];n=seed['stageCount'];x=old.protocol3_run(trace,n);y=new.protocol3_run(trace,n);rows.append({'stageCount':n,'events':trace,'before':x,'after':y,'equal':x==y})
  if x!=y:mismatches.append(len(rows)-1)
assert len(rows)>100
raw=out/'comparisons.json';raw.write_text(json.dumps(rows,indent=1)+'\n')
summary={'standing':__doc__,'sourceHashes':{'before':sha(a.before/rel),'after':sha(a.after/rel)},'predecessorRuleCount':len(old.PROTOCOL3_RULES),'eventAlternatives':len(events),'stageCounts':[1,2],'maxExplorationPrefix':30,'distinctObservableStates':state_counts,'comparisonCalls':len(rows),'mismatchIndices':mismatches,'allEqual':not mismatches,'casesArtifact':{'path':raw.name,'sha256':sha(raw)},'limits':['Finite predecessor-reachable transition exploration for stage counts1 and2 with selected event-field variants. Not exhaustive over arbitrary input objects or stage counts.','Pure transition helper only; payload schemas, confinement, process observation and stage execution are not exercised.','Tuple equivalence is specific to this helper state and selected stageCount; no general model-checker completeness claim.']}
(out/'result.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2));raise SystemExit(bool(mismatches))

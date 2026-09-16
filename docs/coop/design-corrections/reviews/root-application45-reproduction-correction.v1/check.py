from pathlib import Path
import copy,hashlib,json,shutil
B=Path('/tmp/opensip-design-corrections');R=Path('/Users/sb/code/opensip-ai/opensip_arch');H=B/'application-successor-root.v2';O=Path(__file__).parent
p=H/'assemble-records.successor.v1.py';text=p.read_text();compile(text,str(p),'exec')
code=text[text.index("commands_rel = dc + f'reviews/codex-post-reset.v1/final-reference.{dv}/reference-checks.json'"):text.index('# Preserve ONLY versioned operational-guide variants')]
mf=R/'docs/coop/design-corrections/reviews/candidate-subject.v45.json';manifest=json.loads(mf.read_text());original=json.loads((R/'docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v45/reference-checks.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def render(commands):
 ns={'dc':'docs/coop/design-corrections/','dv':'v45','accepted_files':{r['path']:r for r in manifest['files']},'load':lambda _:copy.deepcopy(commands),'ref':lambda path:{'path':path,'sha256':sha(R/path)},'app':{},'manifest_ref':{'path':str(mf.relative_to(R)),'sha256':sha(mf)}}
 exec(compile(code,str(p)+':reproduction-extract','exec'),ns)
 return ns['app']['acceptedDesignReproduction']
actual=render(original);assert len(actual['commands'])==7
for row,old in zip(actual['commands'],original['commands']):
 assert row['source']==old['source'] and row['sourceSha256']==old['sourceSha256']
 assert row['argv'][3]==row['source']
 for binding in row['outputBindings']:
  assert not Path(binding['reproductionOutput']).is_absolute() and '/' not in binding['reproductionOutput']
  assert binding['recordedOutput'] in old['command'] and binding['reproductionOutput'] not in old['command']
cases=[]
for name,mutate in [('unsupported-output-flag',lambda j:j['commands'][0]['command'].__setitem__(4,'--unknown')),('missing-output-value',lambda j:j['commands'][0]['command'].pop()),('source-hash-drift',lambda j:j['commands'][0].__setitem__('sourceSha256','0'*64))]:
 j=copy.deepcopy(original);mutate(j)
 try:render(j);raise RuntimeError('Expected refusal: '+name)
 except AssertionError:cases.append({'case':name,'refused':True})
(O/'corrected-reproduction.json').write_text(json.dumps(actual,indent=2)+'\n')
(O/'checks.json').write_text(json.dumps({'standing':'Actual seven recorded commands transformed by the exact assembler reproduction block. Only explicit report/output paths changed to fresh relative targets; original output bindings and original execution record preserved. No reference suite re-execution claimed by this path test.','sevenCommandsVerified':True,'negativeCases':cases,'result':'PASS'},indent=2)+'\n')
shutil.copyfile(p,O/p.name)
shutil.copytree(O,R/'docs/coop/design-corrections/reviews'/O.name)
print('PASS seven commands; three refusal controls; original evidence unchanged')

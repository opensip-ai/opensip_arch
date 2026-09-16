import subprocess,json,time,hashlib,sys
from pathlib import Path
root=Path(__file__).parent
cmd=['/Users/sb/.local/bin/claude', '--safe-mode', '--strict-mcp-config', '--model', 'opus', '--resume', '85a08aec-9d22-4ac6-8ec2-c10170e727d7', '--permission-mode', 'dontAsk', '--tools', 'Read,Glob,Grep,Bash,Write,Edit', '--allowedTools', 'Read', 'Glob', 'Grep', 'Write', 'Edit', 'Bash(python3 *)', 'Bash(/tmp/opensip-architecture-review-env/bin/python *)', '--output-format', 'stream-json', '--verbose', '-p', '--add-dir', '/tmp/opensip-design-corrections/candidate-subject.v43', '--add-dir', '/tmp/opensip-design-corrections/candidate-subject.v42', '--add-dir', '/tmp/opensip-design-corrections/candidate-subject.v40', '--add-dir', '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews', '--add-dir', '/tmp/opensip-architecture-review-env', '--add-dir', '/tmp/opensip-design-corrections/claude-independent-design.v42', '--add-dir', '/tmp/opensip-design-corrections/claude-independent-design.v40', '--add-dir', '/tmp/opensip-design-corrections/claude-author-package-successor.v20', '--add-dir', '/tmp/opensip-design-corrections/author-package-final43-verification.v1', '--add-dir', '/tmp/opensip-design-corrections/root-author-package-final43-rebuild.v1', '--add-dir', '/tmp/opensip-design-corrections/root-author-package-formal43-binding.v1', '--add-dir', '/tmp/opensip-design-corrections/root-query43-independent-note.v1', '--add-dir', '/tmp/opensip-design-corrections/root-source43-planning-verification.v1', '--add-dir', '/tmp/opensip-design-corrections/root-source43-final-reference.v1']
start=time.time()
p=subprocess.Popen(cmd,cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
(root/'process.json').write_text(json.dumps({'pid':p.pid,'startedAt':start,'command':cmd,'promptSha256':hashlib.sha256((root/'prompt.md').read_bytes()).hexdigest(),'standing':'running'},indent=2)+'\n')
p.stdin.write((root/'prompt.md').read_text());p.stdin.close()
with (root/'public-events.jsonl').open('x') as out:
 for line in p.stdout:
  try: obj=json.loads(line)
  except ValueError: continue
  typ=obj.get('type')
  if typ in ('assistant','user'):
   msg=obj.get('message',{});blocks=[b for b in msg.get('content',[]) if b.get('type') in ('text','tool_use','tool_result')]
   clean={'type':typ,'session_id':obj.get('session_id'),'message':{'role':msg.get('role'),'model':msg.get('model'),'content':blocks}}
  elif typ=='result':
   clean={k:v for k,v in obj.items() if k in ('type','subtype','is_error','duration_ms','num_turns','result','session_id','total_cost_usd','usage','modelUsage','permission_denials','errors')}
   (root/'result.json').write_text(json.dumps(clean,indent=2)+'\n')
   (root/'final-response.md').write_text(clean.get('result','')+'\n')
  elif typ=='system' and obj.get('subtype')=='init':
   clean={k:obj.get(k) for k in ('type','subtype','session_id','model','claude_code_version','permissionMode')}
  else: continue
  out.write(json.dumps(clean)+'\n');out.flush()
  if typ=='system' or typ=='result': print(json.dumps(clean)[:1200],flush=True)
code=p.wait();err=p.stderr.read()
(root/'process-completion.json').write_text(json.dumps({'pid':p.pid,'exitCode':code,'finishedAt':time.time(),'stderr':err,'standing':'process ended; substantive review requires root assessment'},indent=2)+'\n')
print('exit',code,flush=True)

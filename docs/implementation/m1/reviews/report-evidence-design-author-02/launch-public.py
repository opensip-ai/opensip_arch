import subprocess,json,time,hashlib,sys,os
from pathlib import Path
root=Path(__file__).parent
cmd=['/Users/sb/.local/bin/claude', '--safe-mode', '--strict-mcp-config', '--model', 'opus', '--effort', 'high', '--permission-mode', 'dontAsk', '--tools', 'Read,Glob,Grep,Bash,Write,Edit', '--allowedTools', 'Read', 'Glob', 'Grep', 'Bash', 'Write', 'Edit', '--add-dir', '/tmp/opensip-implementation', '--add-dir', '/Users/sb/code/opensip-ai/opensip_arch', '--add-dir', '/Users/sb/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/sha2-const-stable-0.1.0', '--resume', '5081bb38-d208-4f07-8659-9deeea9daefc', '--output-format', 'stream-json', '--verbose', '-p']
start=time.time()
p=subprocess.Popen(cmd,cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env={**os.environ,'CARGO_TARGET_DIR':str(root/'target')})
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

if (root/'result.json').is_file():
 (root/'response.json').write_bytes((root/'result.json').read_bytes())

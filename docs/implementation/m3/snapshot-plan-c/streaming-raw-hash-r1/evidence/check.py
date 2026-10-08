from pathlib import Path
import subprocess,os,sys,tempfile,json
base=Path('/tmp/opensip-implementation/streaming-raw-hash-r1-authoring');work=Path('/Users/sb/code/opensip-ai/opensip-stream-hash');temp=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=temp/'opensip-lanes.lock';assert str(lock)=='/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-lanes.lock';assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists();created=False
try:
 result=subprocess.run(['/bin/mkdir',str(lock)],capture_output=True)
 if result.returncode:
  print('Shared lane held; no build or formatter started.');sys.exit(75)
 created=True
 mode=sys.argv[1];env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',CARGO_HOME='/Users/sb/.cargo');env['SDKROOT']=subprocess.check_output(['/usr/bin/xcrun','--sdk','macosx','--show-sdk-path']).decode().strip();env['RUSTFLAGS']='-C linker=/usr/bin/cc';env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
 for key in ['GIT_CONFIG_COUNT','GIT_DIR','GIT_WORK_TREE']:env.pop(key,None)
 if mode=='format':cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024','src/streaming_digest.rs'];cwd=work/'crates/identity'
 else:
  private=Path(tempfile.mkdtemp(prefix='opensip-stream-hash-',dir=temp));private.chmod(0o700);env['TMPDIR']=str(private);(base/(mode+'-tmpdir.txt')).write_text(str(private)+'\n');cwd=work
  if mode=='test':args=['test','-p','opensip-identity','--lib']
  elif mode=='clippy':args=['clippy','-p','opensip-identity','--all-targets','--','-D','warnings']
  elif mode=='release':args=['check','-p','opensip-identity','--release']
  else:raise ValueError(mode)
  cmd=['/usr/bin/nice','-n','10','/opt/homebrew/Cellar/rust/1.95.0/bin/cargo',*args[:1],'--locked','--offline',*args[1:]]
 result=subprocess.run(cmd,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(base/(mode+'.log')).write_bytes(result.stdout);print(result.stdout.decode()[-6000:]);assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists();sys.exit(result.returncode)
finally:
 if created:subprocess.run(['/bin/rmdir',str(lock)],check=True)

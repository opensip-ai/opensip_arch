from pathlib import Path
import os,subprocess,json,hashlib,time
# Generate labelled synthetic replay packets with the CLOSED accepted generator (prepare_packet.py) and re-mint
# (remint_selected_schema.py), both byte-identical to the accepted 2026-10-09 native spike, for each workload size.
# Sizing (lead decision, labelled lower bound): one synthetic fact and one finding per analysed source:
# TS distinct configured files (express: 141 synthesized-program roots), Rust RUST3-LIM subjects S.
os.setpriority(os.PRIO_PROCESS,0,10)
H=Path(__file__).resolve().parent;PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
N=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes/s-m-full-replay-partial-2026-10-09/native')
for n in ['prepare_packet.py','remint_selected_schema.py']:assert (H/n).read_bytes()==(N/n).read_bytes()
assert hashlib.sha256(Path('/tmp/opensip-implementation/sm-replay-2026-10-09/probe.py').read_bytes()).hexdigest()=='b28f92b90907bb22b9719fb3cc14628c5bcab3fbc9f0e6773447b92058f0ef3b'
SIZES={'js-medium-express':141,'poly-medium-napi-rs (TS)':193,'ts-medium-powertools-lambda':936,'ts-medium-smithy-typescript':1159,'ts-medium-umami':1381,'ts-medium-vite':678,
       'poly-medium-napi-rs (Rust)':239,'rs-medium-aws-lambda-rust-runtime':192,'rs-medium-axum':301,'rs-medium-hyper':98,'rs-medium-serde':208,'rs-medium-serde-json':71,'rs-medium-tokio':808,'mr-rs-medium-serde-json':279}
out={}
for count in sorted(set(SIZES.values())):
 sel=H/f'packet-{count}-selected.json'
 if not sel.exists():
  t=time.monotonic_ns();subprocess.run([PY,'-I','-B',str(H/'prepare_packet.py'),str(count)],cwd=H,check=True);subprocess.run([PY,'-I','-B',str(H/'remint_selected_schema.py'),str(count)],cwd=H,check=True);print(count,'generated',(time.monotonic_ns()-t)/1e9,'s',flush=True)
 raw=sel.read_bytes();out[count]=dict(path=str(sel),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),raw=dict(path=str(H/f'packet-{count}.json'),sha256=hashlib.sha256((H/f'packet-{count}.json').read_bytes()).hexdigest()))
assert out[193]['sha256']=='f33da67037c8bf6d67b2694ce7f4833f70f78549ace1bcf6ca4cded88d593e32'
(H/'sized-packets-r1.json').write_text(json.dumps(dict(standing='LABELLED SYNTHETIC LOWER-BOUND REPLAY PACKETS; ONE FACT AND ONE FINDING PER ANALYSED SOURCE; NOT COMPILER FACT VOLUMES',sizes=SIZES,packets={str(k):v for k,v in out.items()},generator=dict(prepare=str(H/'prepare_packet.py'),remint=str(H/'remint_selected_schema.py'),selectedSchemaDifferences=str(H/'selected-schema-differences.json')),closedGeneratorBytesUnchanged=True,acceptedPacket193Reproduced=True),indent=2)+'\n')
print('done')

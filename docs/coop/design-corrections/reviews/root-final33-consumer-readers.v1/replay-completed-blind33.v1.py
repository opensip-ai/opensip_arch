"""Root captures completed consumer exports and replays exact bytes. No consumer imports."""
from pathlib import Path
import argparse,json,hashlib,subprocess,concurrent.futures
B=Path('/tmp/opensip-design-corrections')
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--runtime',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 assert (a.runtime/'process-completion.json').is_file(),'Wait for process completion before final capture'
 assert not a.out.exists();assert not a.out.resolve().is_relative_to(a.runtime.resolve());a.out.mkdir();inputs=a.out/'captured';inputs.mkdir();rows=[]
 for name in ['syntax-code','typescript','rust','rust-partial','syntax-data']:
  src=a.runtime/'output/runs'/(name+'.store.json');raw=src.read_bytes();d=json.loads(raw);rid=d['claim']['runId'];dst=inputs/(name+'.store.json');dst.write_bytes(raw);rows.append({'name':name,'original':str(src),'input':str(dst),'runId':rid,'sha256':sha(raw)})
 meta={}
 for rel in ['process-completion.json','result.json','output/blind-review.json','output/blind-review.md','output/requirement-status.json','output/verify-all.json']:
  src=a.runtime/rel
  if src.is_file():
   raw=src.read_bytes();dst=a.out/'captured-process-and-claims'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw);meta[rel]=sha(raw)
 (a.out/'capture.json').write_text(json.dumps({'standing':'Process ended; no substantive consumer acceptance inferred. Exact exported bytes only.','files':rows,'processAndClaimHashes':meta},indent=2)+'\n')
 def run(r):
  cmd=['/tmp/opensip-architecture-review-env/bin/python','-I','-B',str(B/'check-blind-successor33-export.v1.py'),'--input',r['input'],'--run-id',r['runId'],'--source',str(B/'candidate-subject.v33'),'--manifest',str(L/'candidate-subject.v33.json'),'--out',str(a.out/r['name'])]
  q=subprocess.run(cmd,capture_output=True,text=True);(a.out/(r['name']+'.process.json')).write_text(json.dumps({'command':cmd,'exitCode':q.returncode,'stdout':q.stdout,'stderr':q.stderr},indent=2)+'\n');rp=a.out/r['name']/'report.json';v=json.loads(rp.read_text()) if rp.exists() else {'passed':False,'reason':'No report; inspect process evidence'};row={'name':r['name'],**{k:v.get(k) for k in ['runId','exportSha256','transportAdmission','structuralAdmission','semanticAdmission','reason','passed']}};print(json.dumps(row),flush=True);return row
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:results=list(ex.map(run,rows))
 (a.out/'summary.json').write_text(json.dumps({'standing':'Root exact transport and both frozen structural/semantic owner admission. Not complete charter assessment or blind acceptance.','sourceManifestSha256':'1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299','allPassed':all(r['passed'] for r in results),'results':results},indent=2)+'\n')
if __name__=='__main__':main()

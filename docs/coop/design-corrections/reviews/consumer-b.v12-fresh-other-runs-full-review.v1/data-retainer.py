"""Strictly retain one of three declared fresh data-only Grok reviews; custody is not acceptance."""
from pathlib import Path
from urllib.parse import quote
import hashlib,json,shutil,subprocess,sys
B=Path('/tmp/opensip-design-corrections')
R=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
ALLOWED={
 'consumer-b.v12-fresh-other-runs-full-review.v1':('export-manifest.json','b515c415da8c0a496e0078b48dfb8b3eabb9364e3522d48929343492d116023b','exports'),
 'consumer-b.v12-fresh-export-admission.v1':('export-manifest.json','4101367795f1a30280601a3a01a8ea36a489f4891f9d0256e92481a8e6369129','exports'),
 'consumer-b.v12-fresh-foundation-data-review.v1':('data-manifest.json','2751637973eeb7c113c630b9666424015b4717127b73efc01979f4134b8acfd4','data'),
}
name=sys.argv[1];assert name in ALLOWED
manifest_name,manifest_hash,data_dir=ALLOWED[name]
s=B/name;d=R/name;assert not d.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(s/manifest_name)==manifest_hash
for row in json.loads((s/manifest_name).read_text())['files']:
 p=(s/row['path']);assert p.resolve().is_relative_to(s.resolve())
 assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
assert sha(s/'original-consumer-charter.txt')=='57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec'
assert sha(s/'requirements.json')=='855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495'
kit=s/'subject/consumer-input-manifest.json'
assert sha(kit)=='ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8'
for row in json.loads(kit.read_text())['files']:
 p=kit.parent/row['path'];assert p.resolve().is_relative_to(kit.parent.resolve());assert sha(p)==row['sha256']
proc=json.loads((s/'process.json').read_text());assert proc['freshSession'] is True and '--resume' not in proc['command']
raw=json.loads((s/'response.raw.json').read_text());assert raw['stopReason']=='end_turn'
assert (s/'stderr.log').stat().st_size==0
cwd=Path(proc['command'][proc['command'].index('--cwd')+1]).resolve()
updates=Path('/Users/sb/.grok/sessions')/quote(str(cwd),safe='')/raw['sessionId']/'updates.jsonl'
sys.path.insert(0,str(B/'application-successor-root.v1'))
import retain_public as P
public,account=P.public_grok_update_blocks(updates.read_text(),raw['sessionId'],(s/'prompt.txt').read_text().strip())
subprocess.run([sys.executable,str(B/'retain-grok-fresh-review-public.v2.py'),name,'blind-consumer'],check=True)
retained=[json.loads(x)for x in(d/'public-tools-and-responses.jsonl').read_text().splitlines()if x]
assert retained==public
(d/'strict-public-precheck.json').write_text(json.dumps({'selectorSha256':sha(Path(P.__file__)),'account':account,'matchesFreshV2PublicExactly':True,'standing':'Public custody only; no substantive acceptance.'},indent=2)+'\n')
for key in ['subject',data_dir]:shutil.copytree(s/key,d/key)
shutil.copytree(s/'output',d/'authored')
for key in ['requirements.json','original-consumer-charter.txt',manifest_name]:shutil.copy2(s/key,d/key)
shutil.copy2(Path(__file__),d/'data-retainer.py')
(d/'retained-files.json').write_text(json.dumps({'files':[{'path':str(p.relative_to(d)),'bytes':p.stat().st_size,'sha256':sha(p)}for p in sorted(d.rglob('*'))if p.is_file()and p.name!='retained-files.json']},indent=2)+'\n')
print(json.dumps({'out':str(d),'sessionId':raw['sessionId'],'numTurns':raw['num_turns'],'publicBlocks':len(public),'files':sum(p.is_file()for p in d.rglob('*')),'substantiveAcceptance':False}))

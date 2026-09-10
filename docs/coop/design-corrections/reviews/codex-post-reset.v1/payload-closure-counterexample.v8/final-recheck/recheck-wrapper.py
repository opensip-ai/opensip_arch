"""Run ONLY after actual author completion/source capture; never replace original bypass evidence."""
from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';author=dc/'reviews/digest-corrections-author.v3';assert (author/'custody.json').exists(),'retain completed author before final-source recheck'
original=dc/'reviews/codex-post-reset.v1/payload-closure-counterexample.v8';out=Path('/tmp/opensip-design-corrections/payload-closure-final-recheck.v8');out.mkdir(exist_ok=False)
manifest=json.loads((dc/'reviews/candidate-subject.v7.json').read_text());base=Path(manifest['snapshotRoot']);work=out/'work';shutil.copytree(base,work)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();paths=[]
for folder in ['foundation','native','workflows','security']:
 paths += [p for p in (dc/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths += list((root/'docs/v2/contracts/product-v1').glob('*.md'));rows=[]
for p in paths:
 rel=p.relative_to(root);q=work/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 if not (base/rel).exists() or sha(base/rel)!=sha(q):rows.append({'path':str(rel),'sha256':sha(q),'bytes':q.stat().st_size})
(out/'captured-source-delta.json').write_text(json.dumps({'standing':'Final coauthor source recheck, not independent review','baseManifestSha256':'b5cfb5d316eb0101950476a37a2095ed0d9c5d51263408d3462f105d63165f7b','files':rows},indent=2)+'\n')
# Execute the original retained attack suffix on a new exact source capture. The scripts name
# their original observations as in-progress; wrapper provenance explicitly distinguishes this run.
src=(original/'probe.py').read_text();suffix=src[src.index("fixture=work/"):]
ns={'__file__':str(original/'probe.py'),'__name__':'final_coverage_probe','Path':Path,'json':json,'hashlib':hashlib,'shutil':shutil,'out':out,'work':work}
import ast,copy
(out/'executed-coverage-suffix.py').write_text(suffix);(out/'recheck-wrapper.py').write_bytes(Path(__file__).read_bytes())
ns.update(ast=ast,copy=copy);exec(compile(suffix,str(original/'probe.py'),'exec'),ns)
coverage=json.loads((out/'result.json').read_text());assert coverage['positive']['admitted'];assert len(coverage['vectors'])==2
for row in coverage['vectors']:assert row['nativeAdmission']['result']=='REFUSE' and not row['completeRunClosure']['admitted'],row
memo=(original/'memo-probe.py').read_text().replace("base=Path('/tmp/opensip-design-corrections/payload-closure-probe.v8')",'base=Path('+repr(str(out))+')')
(out/'memo-adaptation.py').write_text(memo);exec(compile(memo,str(out/'memo-adaptation.py'),'exec'),{'__file__':str(out/'memo-adaptation.py'),'__name__':'final_memo_probe'})
m=json.loads((out/'memo-result.json').read_text());assert m['control']['admitted'] and not m['twoFactGraph']['admitted'] and not m['sameInvalidSchemaAlone']['admitted'],m
retained=original/'final-recheck';retained.mkdir(exist_ok=False)
for p in out.iterdir():
 if p.is_file():shutil.copyfile(p,retained/p.name)
for row in rows:
 p=work/row['path'];q=retained/'source-delta'/row['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
(retained/'custody.json').write_text(json.dumps({'standing':'Codex final-source re-execution/adaptation of its own original counterexamples; no independent acceptance','originalEvidencePreserved':True,'actualFinalSource':rows,'allControlsAdmitted':True,'allThreeBypassesRefused':True,'productQualification':False},indent=2)+'\n')
print('final source valid controls pass and all three original bypasses refuse; exact source deltas retained')

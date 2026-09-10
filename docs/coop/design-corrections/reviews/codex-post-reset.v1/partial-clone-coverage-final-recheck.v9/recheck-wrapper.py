from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--cause',required=True);args=p.parse_args()
root=Path.cwd();dc=root/'docs/coop/design-corrections'
assert (dc/'reviews/digest-corrections-author.v6/custody.json').is_file()
original=dc/'reviews/codex-post-reset.v1/partial-clone-coverage-counterexample.v9/probe.py';source=original.read_text()
old="owned=json.loads((dc/'reviews/digest-corrections-author.v5/handoff.json').read_text())['ownedFilesChanged'];rows=[]"
new="owned=list({r['path']:r for v in ('v5','v6') for r in json.loads((dc/('reviews/digest-corrections-author.'+v+'/handoff.json')).read_text())['ownedFilesChanged']}.values());rows=[]"
assert old in source;source=source.replace(old,new)
source=source.replace('partial-clone-coverage-counterexample.v9','partial-clone-coverage-final-recheck.v9')
source=source.replace('captured in-progress v6 source','captured released final v9 source')
launch=Path('/tmp/opensip-design-corrections/partial-clone-coverage-final-launch.v9');launch.mkdir(exist_ok=False)
adapted=launch/'adapted-probe.py';adapted.write_text(source)
exec(compile(source,str(adapted),'exec'),{'__file__':str(adapted),'__name__':'codex_partial_clone_final_recheck'})
out=dc/'reviews/codex-post-reset.v1/partial-clone-coverage-final-recheck.v9';result=json.loads((out/'result.json').read_text());vectors={v['id']:v for v in result['vectors']}
control=vectors['honest-unknown-control'];bad=vectors['contradictory-complete-claim']
assert control['store'].get('commit')=='committed' and control['sealVerdict']=='indeterminate'
assert not bad['closure']['admitted'] and args.cause in bad['closure']['cause'],bad
(out/'recheck-wrapper.py').write_bytes(Path(__file__).read_bytes())
(out/'recheck-assessment.json').write_text(json.dumps({'standing':'Codex rerun of its own original complete-Run vectors on captured final source; not independent acceptance or product qualification.','originalPreserved':True,'honestControlCommittedIndeterminate':True,'contradictoryCompleteClaimRefused':True,'requiredCauseSubstring':args.cause,'observedCause':bad['closure']['cause']},indent=2)+'\n')
print('Final source preserves honest partial Run and rejects contradictory complete Coverage at intended join')

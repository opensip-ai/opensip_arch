from pathlib import Path
import hashlib,json,shutil,subprocess,sys
B=Path('/tmp/opensip-design-corrections'); L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
old=B/'consumer-b.v20'; out=B/'consumer-b.v22'; mf=L/'candidate-subject.v34.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (old/'process-completion.json').is_file() and not out.exists()
manifest=json.loads(mf.read_bytes()); subject=out/'subject'
cmd=[sys.executable,'-I','-B',str(B/'final-claude-source-preparation.v5/prepare-blind-kit.py'),'--snapshot',manifest['snapshotRoot'],'--origin-standing','continuation','--manifest',str(mf),'--manifest-sha256',sha(mf),'--previous-kit-manifest',str(old/'subject/consumer-input-manifest.json'),'--out',str(subject)]
p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0,(p.stdout,p.stderr)
kit=subject/'consumer-input-manifest.json';kd=json.loads(kit.read_bytes())
shutil.copytree(old/'output',out/'output',ignore=shutil.ignore_patterns('__pycache__'))
for n in ['requirements.json','original-charter-prompt.source26.md']:
 shutil.copy2(old/n,out/n)
shutil.copy2(old/'requirements.json',out/'requirements.before22.json')
shutil.copy2(old/'final-response.md',out/'previous-turn-response.md')
r=json.loads((out/'requirements.json').read_bytes());r['inputKit']={'manifestSha256':sha(kit),'parentSubjectSha256':sha(mf)}
(out/'requirements.json').write_text(json.dumps(r,indent=2)+'\n')
prev={x['path']:x for x in json.loads((old/'subject/consumer-input-manifest.json').read_bytes())['files']}
delta=[{'path':r['path'],'previousSha256':prev.get(r['path'],{}).get('sha256'),'currentSha256':r['sha256']} for r in kd['files'] if prev.get(r['path'],{}).get('sha256')!=r['sha256']]
(out/'normative-delta.json').write_text(json.dumps({'standing':'Kit byte inventory only, no semantic expected result or root outcome.','files':delta},indent=2)+'\n')
prompt=f'''Continue SAME originally fresh blind actual-Claude origin79569ae1-10f4-4181-972b-334f7ed2f07a,14→15→16→17→18→19→20→22. Generation21 was only prepared and never launched; no21 result exists. Not a source author. Original123requirements+8standing+3future unchanged; no scope dropped or added by this continuation. Reconstruct the newly frozen normative successor independently.

Inputs ONLY inside THIS runtime: subject/ exact {len(kd['files'])}-file normative kit, manifest SHA {sha(kit)}, parentSource34 SHA {sha(mf)}; original-charter-prompt.source26.md; requirements.json; your OWN20 output copied exactly to output/ and previous-turn-response.md. requirements.before22.json preserves20 input metadata; only inputKit was updated, original historical example paths remain provenance, not write authority. normative-delta.json is a hash inventory; verify and derive your own delta. No author implementation, controls, expected outputs, root replay/refusal reports or source-author diagnosis is supplied. Never read live repo or any other review/runtime except your supplied own copies. All older generations read-only.

FIRST use direct /tmp/opensip-architecture-review-env/bin/python -I -B -c 'import jsonschema; print("REFERENCE_INTERPRETER_AVAILABLE")'. This absolute interpreter and standard-library python3 are both permitted. If denied, stop with exact external error. Never work around missing jsonschema with a reduced validator.

Before executing copied code, audit ALL literal consumer-b.vN paths and write destinations. Rebind current read/write paths to22local copies. Preserve originals in a22local beforeimages directory. Do NOT globally rewrite historical generation labels in report content. Current consumerId/inputKit/receipts become22, historical V17/V18/V19/V20 findings retain true provenance. Keep actual past overwrite disclosures; do not invent pristine history. All writes under22, no scratchnotes in earlier generation.

Read all changed normative owner regions and cross-owner references, independently reconcile your existing atom/completeness/cause/dependency interpretation with the new published clauses, rebuild the complete affected retained Runs and replay exports. Diagnose from law and your own artifacts only. No root outcome is known to you; do not infer acceptance from earlier reports. Distinguish actual native support, execution completion, enumeration completeness and proof verdict. State measured results with full admitted retained joins and typed original causes.

Recheck the ENTIRE original charter, especially all standalone workflow/query/mutation/surface vectors and their owner clauses, not just the changed execution laws. Independently build a clause-to-code-and-measured-artifact map for all published query-operation/projection/ordering/disclosure/bounds/cursor/summary/renderer/envelope laws and mutation schema/identity/replay-scope/key laws. Compare actual final response records and fields to owning schemas and normative semantics. Preserve raw response records with actual requests/host controls and current admitted Run references. A helper that validates only its own subset is insufficient. This is the original charter's complete reconstruction, not a new product engine or a demand for real host qualification. Determine corrections yourself from the kit; no answer oracle is supplied.

Retain all original complete Run properties, standalone config/clone/repair vectors, protocol/capability/CVE1/raw canonical vectors, zero-config selection chain, baseline/pivots, failure/termination/purge/availability/invocation envelopes and semantic replay. Five exported positives can cover six overlapping Run requirements. Do not demand an extra sixth Run by count. Do not upgrade standalone vectors into complete Runs. Repair controls use actual schema-valid identities and evidence-bound descriptors when claimed; synthetic helper-only observations must be labeled. Preserved S1/S2/Area1/2/3 work remains part of the original scope, with final current law applied.

Execute fresh-process verify_all.py AFTER final edits and export exactframes/objecttables/blobs plus replayed complete proofs. Negative controls retain first actual refusal and masking. Current positive admission means owning-schema+closed registry+retained joins then complete semantic proof comparison, never caller truth or a literal PASS. Reconcile all final review.md/json, checkpoints, requirementstatus, commands/stages, artifact hashes and source lineage to those exact final bytes. Inherit a prior execution only with exact input equality and explicit historical standing; never relabel old commands as22. Retain failures/corrections and use fresh receipt names rather than overwriting earlier attempts.

Final output/blind-review.md/json and complete substantive reconstruction required. ACCEPT-RECONSTRUCTABLE only when all blocking original work is executed with no open MUST/SHOULD/helper failure; otherwise honest CHANGES_REQUIRED/BLOCKED and exact remaining issues. Root separately checks final exported bytes; no root verdict is supplied to you. Complete the work, not a progress-only handoff, unless actually externally blocked.

No product implementation, source/kit edits, commit/push, other agents, acceptance on root's behalf or product qualification. OS/compiler/crypto/SQLite/host enforcement remains future qualification, synthetic TCB observations explicitly assumptions.
'''
(out/'prompt.md').write_text(prompt)
launch=(old/'launch.py').read_text().replace("'--add-dir', '/tmp/opensip-design-corrections/consumer-b.v20'","'--add-dir', '/tmp/opensip-design-corrections/consumer-b.v22'")
(out/'launch.py').write_text(launch)
(out/'dispatch.json').write_text(json.dumps({'standing':'Prepared only; no execution or acceptance. Exact normative successor plus disclosed same-origin20 outputs, no root outcomes.','sessionId':'79569ae1-10f4-4181-972b-334f7ed2f07a','sourceManifestSha256':sha(mf),'kitManifestSha256':sha(kit),'promptSha256':sha(out/'prompt.md'),'requirementsSemanticsUnchanged':r['requirements']==json.loads((old/'requirements.json').read_bytes())['requirements'],'kitPreparationCommand':cmd,'kitPreparationStdout':p.stdout},indent=2)+'\n')
print('Prepared consumer22',len(kd['files']),'kit files',len(delta),'changed/new')

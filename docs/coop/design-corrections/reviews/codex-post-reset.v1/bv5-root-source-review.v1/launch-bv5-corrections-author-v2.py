"""Resume the actual completed Claude coauthor with exact root counterexamples; not independent."""
from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
root=Path('/Users/sb/code/opensip-ai/opensip_arch');ev=root/'docs/coop/design-corrections/reviews'
base=Path('/tmp/opensip-design-corrections');old=base/'bv5-corrections-author.v1';out=base/'bv5-corrections-author.v2'
sid='f6955666-0878-461a-a4e1-2ca2c4f5e824';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
response=json.loads((old/'response.json').read_text());assert response.get('is_error') is False and response['session_id']==sid
retained=ev/'bv5-corrections-author.v1';assert (retained/'custody.json').is_file() or (retained/'codex-retention-custody.json').is_file()
assert sha(old/'handoff.json')==sha(retained/'handoff.json') and sha(old/'handoff.md')==sha(retained/'handoff.md')
assessment=ev/'codex-post-reset.v1/coauthor-assessment-bv5-v1.json';a=json.loads(assessment.read_text())
assert a['finalSourceAssent'] is False and a['handoffReadInFull'] is True
assert not out.exists();out.mkdir();shutil.copytree(old/'work',out/'work');inputs=out/'root-input';inputs.mkdir()
for name in ['handoff.json','handoff.md']:shutil.copyfile(retained/name,inputs/('prior-'+name))
shutil.copyfile(assessment,inputs/'root-assessment.json')
helpers=Path(__file__).parent
for name in ['bv5-draft-root-feedback.v1.md','probe-bv5-draft-rc1.py','probe-bv5-draft-rc1.first-attempt.py','bv5-draft-rc1-result.v1.json','bv5-draft-rc1-result.v2.json','probe-bv5-draft-cross-rung.py','bv5-draft-cross-rung-result.v1.json','probe-bv5-rc1-full-run.py','bv5-rc1-full-run-result.v1.json']:
 shutil.copyfile(helpers/name,inputs/name)
mp=ev/'candidate-subject.v15.json';assert sha(mp)=='5ec7928426c7a91e323240337dc382c4de32bd4e5f2626eba92c8991067b365f'
shutil.copyfile(mp,inputs/mp.name)
(inputs/'custody.json').write_text(json.dumps({'sessionId':sid,'standing':'Root feedback and counterexamples for actual coauthor follow-up; no independent assent.','files':[{'path':str(p.relative_to(inputs)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(inputs.iterdir()) if p.is_file()]},indent=2)+'\n')
prompt=f'''Continue as actual Claude COAUTHOR. Your first correction pass and its substantive review are preserved verbatim. Codex read your final handoff and source but does NOT assent yet. No source integrated or successor frozen. Your only editable scope for this follow-up is {out}; work source {out/'work'} is an exact copy of your FINAL v1 proposal. This scope supersedes the previous v1-only editing location. Do not edit v1, live repo, frozen subjects, historical reports or evidence. No product implementation, commits, pushes, publication or subagents.

FIRST fully read {inputs/'root-assessment.json'}, {inputs/'bv5-draft-root-feedback.v1.md'}, and the actual full-Run diagnostic {inputs/'bv5-rc1-full-run-result.v1.json'} plus its source. Substantively assess all eight root points and all your own final v1 new findings. Correct every material mismatch in minimal consistent current prose/schema/reference/corpus bytes; do not merely list a required issue as future work. Keep original severities/history and report disagreement where evidence supports it.

The root full-Run evidence is concrete: proper unresolved-edge request added, complete retained graph re-keyed, valid observed control ADMITs; wrong unresolved-edge@enumerated ADMITs; observed attempted=true ADMITs; observed nonempty registered unresolved classes ADMITs. This is more than the pure helper/single producer probe. Your cross-rung negative on resolved-binding only exercised resolved-rung NA rejection; it cannot establish relation-specific membership for other non-resolved rungs. Fix the actual producer and retained admission, including fact-free coverage. Preserve all valid registered pairs, the five resolved rungs and RC2, unknown vocabulary refusal, stageTerminal (NA may retain complete/budget-exhausted), examined partition and honest incomplete resolution. Add meaningful final reference regression controls on full graphs using the shared integration fixture or appropriately scoped native admission; no full-suite AST extraction is necessary to run the supplied root probe.

The Unicode mismatch is exact: existing str.lower() is full/context-sensitive default lowercase, not simple code-point lowercase or casefold. Measured reference UCD15.0.0: U+0130->U+0069 U+0307, ΟΣ->ος, sharp-s stays sharp-s (casefold would be ss). Publish a deterministic adequately version-bound operation matching the intended existing comparison; do not silently narrow inputs to ASCII or delegate to locale/default future runtime data. This is a design/reference task, not implementing TypeScript. Reconcile source and discriminating controls; if an explicit UCD version law requires a minimal reference-version check, account its real portability consequence honestly rather than claim unchanged behavior on every runtime.

Other points: cardinality conditional stage includes missing/wrong-shape values and schema errors retain origin-dependent host fault exit4 vs external exit2; fix prose AND docstring. Repair guard remains all delete/replace actions, with original full native evidence/target-relative affected-edge checks; projection alone grants no authority and dynamicDispatch alone must not globally veto unrelated targets. Path descriptions must distinguish direct two $refs, anchor snapshot joins and fingerprint imperative grammar, without claiming a nonexistent fingerprint snapshot join or uniform per-segment enforcement. Correct Windows citation and same-observation overstatement. Individually address your v1 new findings proportionately: synthetic reference fixture limits are not automatic product host failures, but a contradictory normative/reference admission must be fixed rather than hidden by a limitation.

Efficiency: do not repeat six whole-suite checks after each small edit. Root runs six final pinned commands only after final source and records/pins. Keep published pins/generated reports/readiness/crosswalk untouched in RELEASED work. Any temporary repins/checks stay in a separately accounted disposable copy under {out}; preserve every original failed attempt. Write concise assessment.md/json answering feedback before edits, then final handoff.md/json: technicalAssent to exact final source, each original four required/four advisory/V15ADV1 disposition, each eight root points and own new finding; aggregate source delta vs frozenv15 AND this turn delta vs released v1 with before/after SHA256; exact commands/results/limitations and full disposable-copy roots. Do not claim product qualification, independence, blind acceptance or readiness.

Before final handoff reread this prompt and {out/'CODEX-PUBLIC-NOTE.md'} if present. Finish the bounded corrections now; all source must be reviewable and mutually consistent. Root will independently check final bytes and then request fresh independent Claude and a NEW blind consumer.'''
(out/'prompt.txt').write_text(prompt)
args=['/Users/sb/.local/bin/claude','--resume',sid,'-p','--model','opus','--effort','high','--permission-mode','dontAsk','--tools','Read,Grep,Glob,Edit,Write,Bash','--allowedTools','Read','Grep','Glob','Edit','Write','Bash','--strict-mcp-config','--output-format','json']
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
proc=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=(out/'response.json').open('wb'),stderr=(out/'stderr.log').open('wb'),cwd=old/'work',start_new_session=True)
proc.stdin.write(prompt.encode());proc.stdin.close()
(out/'process.json').write_text(json.dumps({'pid':proc.pid,'sessionId':sid,'startedAt':start,'command':args,'parentSubjectSha256':sha(mp),'priorHandoffSha256':sha(old/'handoff.json'),'sourceRoot':str(out/'work'),'workingDirectory':str(old/'work')},indent=2)+'\n')
shutil.copyfile(old/'session-discovery.json',out/'session-discovery.json')
print(json.dumps({'pid':proc.pid,'sessionId':sid,'out':str(out),'standing':'Actual coauthor follow-up active; no source assent.'}))

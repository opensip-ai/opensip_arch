from pathlib import Path
import hashlib,json
B=Path('/tmp/opensip-design-corrections')
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O=B/'claude-independent-design.v34'
assert not O.exists()
mf=L/'candidate-subject.v34.json'; raw=mf.read_bytes(); m=json.loads(raw)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parent=json.loads((L/'candidate-subject.v33.json').read_bytes())
before={r['path']:r for r in parent['files']}; after={r['path']:r for r in m['files']}
delta=[{'path':p,'beforeSha256':before.get(p,{}).get('sha256'),'afterSha256':r['sha256'],'bytes':r['bytes']} for p,r in after.items() if before.get(p,{}).get('sha256')!=r['sha256']]
O.mkdir()
(O/'root-delta33-to34.json').write_text(json.dumps({'standing':'Inventory only, independently verify. No acceptance.','files':delta,'removed':sorted(set(before)-set(after))},indent=2)+'\n')
prompt=f'''Continue SAME independent reviewer ce3dec3b-0620-44ec-86e6-129b0e25cb1b. You have authored no source. Review exact newly frozen source34. Your source33 ACCEPT and reconciliations are historical unchanged; they do not accept these new bytes. Write only THIS runtime; source, prior evidence and live repository read-only. No product implementation, activation, commit, push or other agents.

SUBJECT: {mf}, SHA {sha(mf)}; archive {L/'candidate-source.v34.tar.gz'} SHA {sha(L/'candidate-source.v34.tar.gz')}; snapshot {m['snapshotRoot']}, {m['fileCount']} files/{m['totalBytes']} bytes. Verify full custody, archive equality and parent33 ancestry. Independently derive delta; root-delta33-to34.json is only inventory.

BASELINE: your COMPLETE corrected107-row review is claude-independent33-reconciliation.v2/review.json (SHA {sha(B/'claude-independent33-reconciliation.v2/review.json')}) and accompanying review.md. Preserve original33, reconciliation1/2 and read-history corrections. Root already accepted those record corrections; do not repeat old metadata errors or rerun unchanged probes without reason. Inherit source reads only with exact-byte verification and explicit inherited standing. Reassess every changed owner and its cross-owner consequences; maintain the full whole-design obligations, not merely a focused approval.

The changed atom completeness law requires substantive scrutiny: no owed binding versus no binding at the subject universe; outgoing early returns stop completeness, never known matches; incoming shared prelude and whole-source/provider accumulation; all three cause channels, typed source-universe attribution, dependency traversal and partition fold ordering. Examine the actual final prose/reference/control diffs and both endpoint branches, including same-kind dependency pairing across multiple scopes and ties in whole-record folds. Test order independence at actual affected boundaries. Distinguish synthetic helper evidence from schema-admitted retained Runs; do not upgrade a stable unrelated real fixture into a demonstrated full-Run counterexample or qualification. Source author evidence is not independent acceptance. Root will retain the complete final author handoff separately; derive your own conclusions from exact frozen owners and probes.

Root's prior corrected33 review acceptance was bounded to record reconciliation: complete baseline corrected JSON has currentStatusOn33 and actual manifest-owner arrays, but eight legacy readingStanding strings are stale. Preserve history while giving every current34 row an accurate current inherited/changed-source account; do not copy a stale unversioned sentence as current byte equality. Prior application outcomes remain false. No source author is eligible acceptor: eaa8276c-dc65-4d26-8ca2-703b345698f9,36a89be8-3442-4edb-90d8-a6fd959a437c,0aa529b3-0da1-44b1-b2b9-dbcd9f1bd206,329a5132-ee66-4303-97a9-b9ebd1b7ffc0,919c766d-f2d0-4cfa-abaa-9d7425d9395f,823bf66b-e92a-4789-ab81-63a1a9dc371d. You are none of these.

Planning: assess current input layer4 (retain it if all29 input bytes are unchanged; a new source version alone does not require a new planning layer), coverage/build plan and unchanged populations198paths/20packages/320mappings/54unexecuted recoverycases. Preserve layer3/2/original25 history. Report/module layout and M0–M6 remain in your whole review. Root integrated-suite receipts are evidence, not authority; independently run meaningful changed suites/planning checks and justified regressions, retaining exact commands/results and source hashes.

Author reference package: use ONLY a current source34-bound package with a verified artifact manifest and actual current replay; historical source30 construction cannot become a new execution by rebinding. Package11 binds the exact mixed-provenance package10 exports to source34; inspect its construction/current binding receipts. Verify all13 exact Run/control cases through BOTH open_run_closure and close_run, then7queries. If it fails new law, record the actual failure honestly; never remint as independent reviewer. Root will arrange a corrected author package if required. Retain A10 limits: TS helper-v-owner only, six self-consistency; exists/none, other operator limitations; incomplete two-binding construction/single explicit binding; no compiler/provider/OS qualification. A9 repair controls retain their exact admitted-v-unit limitations. All30 author proposals remain PENDING independent grading until substantively assessed.

OUTPUT complete review.md and review.json: verifiedManifest/current SHA/verdict/newMustIssues/newShouldIssues/advisories, measured probes with exact evidence, and ALL107 individually reasoned rows in14F,30evaluationResidualDispositions,16arDispositions,15fwDispositions,27inheritedResidualDispositions,5scopedReviewOwnerDispositions. Preserve complete baseline rows with justified exact-byte inherited reading; add current34 deltas/status and actual current owner paths/selectors. Do not relabel old commands as34 or drop scopes. Derive changed-file arrays from manifests, not guessed prose. No need to regenerate unchanged reasoning cosmetically.

TCB-SCOPE-01 remains one joint consequence with13dependent rows; all28condition2 obligations,32product gates and54recoverycases remain. Product condition5 NOT MET. D9 implementation obligation DR007/DR011R08 persists. This design review grants NO final application outcomes: appliedByThisReview=false/finalApplicationOutcomeGranted=false on each row. Blind consumer and final application review/activation are separate. DO NOT read ANY consumer outputs/runtime/reports or root blind replay files; no blind result or oracle is an input to this review.

Use actual /tmp/opensip-architecture-review-env/bin/python -I -B. Finish substantive review with honest remaining issues; no progress-only handoff unless externally blocked. Scope remains design/reference, no product qualification.
'''
(O/'prompt.md').write_text(prompt)
template=(B/'claude-execution-account-author.v1/launch.py').read_text()
start=template.index('cmd='); end=template.index('\nstart=time.time()',start)
cmd=['/Users/sb/.local/bin/claude','--safe-mode','--strict-mcp-config','--model','opus','--resume','ce3dec3b-0620-44ec-86e6-129b0e25cb1b','--permission-mode','dontAsk','--tools','Read,Glob,Grep,Bash,Write,Edit','--allowedTools','Read','Glob','Grep','Write','Edit','Bash(python3 *)','Bash(/tmp/opensip-architecture-review-env/bin/python *)']
for p in [Path(m['snapshotRoot']), B/'claude-independent-design.v33', B/'claude-independent33-reconciliation.v1', B/'claude-independent33-reconciliation.v2', B/'claude-author-package-successor.v11', B/'root-final34-reference.v1', B/'root-final34-planning-checks.v1', L, Path('/tmp/opensip-architecture-review-env')]:cmd+=['--add-dir',str(p)]
cmd+=['--output-format','stream-json','--verbose','-p']
(O/'launch.py').write_text(template[:start]+'cmd='+repr(cmd)+template[end:])
(O/'dispatch.json').write_text(json.dumps({'standing':'Prepared only; no review execution or acceptance','sessionId':'ce3dec3b-0620-44ec-86e6-129b0e25cb1b','manifestSha256':sha(mf),'promptSha256':sha(O/'prompt.md'),'deltaFiles':len(delta)},indent=2)+'\n')
print('Prepared independent34',len(delta))

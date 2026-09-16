from pathlib import Path
import hashlib,json
B=Path('/tmp/opensip-design-corrections')
L=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews')
O=B/'claude-independent-design.v33'
assert not O.exists()
mf=L/'candidate-subject.v33.json'; raw=mf.read_bytes(); m=json.loads(raw)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parent=json.loads((L/'candidate-subject.v32.json').read_bytes())
before={r['path']:r for r in parent['files']}; after={r['path']:r for r in m['files']}
delta=[{'path':p,'beforeSha256':before.get(p,{}).get('sha256'),'afterSha256':r['sha256'],'bytes':r['bytes']} for p,r in after.items() if before.get(p,{}).get('sha256')!=r['sha256']]
O.mkdir()
(O/'root-delta32-to33.json').write_text(json.dumps({'standing':'Inventory only, independently verify. No acceptance.','files':delta,'removed':sorted(set(before)-set(after))},indent=2)+'\n')
prompt=f'''Continue SAME independent reviewer ce3dec3b-0620-44ec-86e6-129b0e25cb1b. You have authored no source. Review exact newly frozen source33. Your source32 ACCEPT and reconciliations are historical unchanged; they do not accept these new bytes. Write only THIS runtime; source, prior evidence and live repository read-only. No product implementation, activation, commit, push or other agents.

SUBJECT: {mf}, SHA {sha(mf)}; archive {L/'candidate-source.v33.tar.gz'} SHA {sha(L/'candidate-source.v33.tar.gz')}; snapshot {m['snapshotRoot']}, {m['fileCount']} files/{m['totalBytes']} bytes. Verify full custody, archive equality and parent32 ancestry. Independently derive delta; root-delta32-to33.json is only inventory.

BASELINE: your COMPLETE corrected107-row review is claude-independent32-reconciliation.v2/review.json (SHA {sha(B/'claude-independent32-reconciliation.v2/review.json')}) and accompanying review.md. Preserve original32, reconciliation1/2 and read-history corrections. Root already accepted those record corrections; do not repeat old metadata errors or rerun unchanged probes without reason. Inherit source reads only with exact-byte verification and explicit inherited standing. Reassess every changed owner and its cross-owner consequences; maintain the full whole-design obligations, not merely a focused approval.

Changed execution law needs substantive scrutiny: external sourceUniverse-to-binding join for every applicability; explicit FIRST-MATCH VCS-none/matrixunsupported/unselected/null-U/supportedavailable; distinguish capability request from enumerator selection and optional retained disclosure; selected-U unsupported native Coverage retained outside empty account coverageIds; required unsupported proof remains indeterminate. Missing partitions or expected subjects carry null/null when no actual source pair exists, with required-cell-unsatisfied proof bridge and originating refs. Mixed typed and untyped sources require deterministic whole-pair selection and retention of all evidence. Parent composition explicitly specified provider fallback in conflict with execution no-invention law: assess corrected owners together. Examine final source, not these descriptions as truth. Independently test real admitted/full Run boundaries where available and label unit/synthetic limits.

The author and root correction records in claude-execution-account-author.v1/v2 and root-execution-account-draft-review.v1/v2 explain proposed issues and scope; author evidence is not independent acceptance. Read relevant final handoff, exact code/contracts/schema/checker/fixture diffs, independent cross-source source ordering and report standing. No source author is eligible acceptor: eaa8276c-dc65-4d26-8ca2-703b345698f9,36a89be8-3442-4edb-90d8-a6fd959a437c,0aa529b3-0da1-44b1-b2b9-dbcd9f1bd206,329a5132-ee66-4303-97a9-b9ebd1b7ffc0,919c766d-f2d0-4cfa-abaa-9d7425d9395f,823bf66b-e92a-4789-ab81-63a1a9dc371d. You are none of these.

Planning: assess current new input layer4 (29 inputs), regenerated coverage/build plan and unchanged populations198paths/20packages/320mappings/54unexecuted recoverycases. Preserve layer3/2/original25 history. Report/module layout and M0–M6 remain in your whole review. Root integrated-suite receipts are evidence, not authority; independently run meaningful changed suites/planning checks and justified regressions, retaining exact commands/results and source hashes.

Author reference package: use ONLY a current source33-bound package with a verified artifact manifest and actual current replay; historical source30 construction cannot become a new execution by rebinding. Package9 is provisionally rebound from8; verify all13 exact Run/control cases through BOTH open_run_closure and close_run, then7queries. If it fails new law, record actual failure honestly; never remint as independent reviewer. Root will provide a corrected author package if required. Retain A10 limits: TS helper-v-owner only, six self-consistency; exists/none, other operator limitations; incomplete two-binding construction/single explicit binding; no compiler/provider/OS qualification. A9 repair controls retain their exact admitted-v-unit limitations. All30 author proposals remain PENDING independent grading until substantively assessed.

OUTPUT complete review.md and review.json: verifiedManifest/current SHA/verdict/newMustIssues/newShouldIssues/advisories, measured probes with exact evidence, and ALL107 individually reasoned rows in14F,30evaluationResidualDispositions,16arDispositions,15fwDispositions,27inheritedResidualDispositions,5scopedReviewOwnerDispositions. Preserve complete baseline rows with justified exact-byte inherited reading; add current33 deltas/status and actual current owner paths/selectors. Do not relabel old commands as33 or drop scopes. Derive changed-file arrays from manifests, not guessed prose. No need to regenerate unchanged reasoning cosmetically.

TCB-SCOPE-01 remains one joint consequence with13dependent rows; all28condition2 obligations,32product gates and54recoverycases remain. Product condition5 NOT MET. D9 implementation obligation DR007/DR011R08 persists. This design review grants NO final application outcomes: appliedByThisReview=false/finalApplicationOutcomeGranted=false on each row. Blind consumer and final application review/activation are separate. DO NOT read ANY consumer outputs/runtime/reports or root blind replay files; no blind result or oracle is an input to this review.

Use actual /tmp/opensip-architecture-review-env/bin/python -I -B. Finish substantive review with honest remaining issues; no progress-only handoff unless externally blocked. Scope remains design/reference, no product qualification.
'''
(O/'prompt.md').write_text(prompt)
template=(B/'claude-execution-account-author.v1/launch.py').read_text()
start=template.index('cmd='); end=template.index('\nstart=time.time()',start)
cmd=['/Users/sb/.local/bin/claude','--safe-mode','--strict-mcp-config','--model','opus','--resume','ce3dec3b-0620-44ec-86e6-129b0e25cb1b','--permission-mode','dontAsk','--tools','Read,Glob,Grep,Bash,Write,Edit','--allowedTools','Read','Glob','Grep','Write','Edit','Bash(python3 *)','Bash(/tmp/opensip-architecture-review-env/bin/python *)']
for p in [Path(m['snapshotRoot']), B/'claude-independent-design.v32', B/'claude-independent32-reconciliation.v1',B/'claude-independent32-reconciliation.v2',B/'claude-author-package-successor.v9',B/'claude-execution-account-author.v1',B/'claude-execution-account-author.v2',B/'root-execution-account-draft-review.v1',B/'root-execution-account-draft-review.v2',L,Path('/tmp/opensip-architecture-review-env')]:cmd+=['--add-dir',str(p)]
cmd+=['--output-format','stream-json','--verbose','-p']
(O/'launch.py').write_text(template[:start]+'cmd='+repr(cmd)+template[end:])
(O/'dispatch.json').write_text(json.dumps({'standing':'Prepared only; no review execution or acceptance','sessionId':'ce3dec3b-0620-44ec-86e6-129b0e25cb1b','manifestSha256':sha(mf),'promptSha256':sha(O/'prompt.md'),'deltaFiles':len(delta)},indent=2)+'\n')
print('Prepared independent33',len(delta))

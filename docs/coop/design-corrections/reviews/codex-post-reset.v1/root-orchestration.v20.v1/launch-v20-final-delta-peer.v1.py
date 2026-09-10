from pathlib import Path
import subprocess,json,hashlib,datetime
B=Path('/tmp/opensip-design-corrections');P=B/'v20-final-delta-peer.v1';assert not P.exists();P.mkdir()
F=B/'v20-final-source.v1';h=hashlib.sha256((F/'proposal.json').read_bytes()).hexdigest();assert h=='cec32147433b2879721a1597206e03035b5c213cd75ead9a19ca0a725972163d'
prompt=f'''You are actual Claude, a bounded SOURCE PEER collaborating with Codex. This is NOT fresh independent source20 acceptance, not a blind consumer and not readiness. Work only under {P}; all other source/history/live trees READ ONLY. No agents/implementation/commits/push.

Assess the final SMALL ROOT DELTA on top of the completed route coauthor's nine-file overlay. Parent preliminary source was already assessed by actual Claude8edfd51b-fba3-45cd-85ae-25d3505ee3cc; route coauthor132a831b-3202-4120-94b1-41292d025f21 separately owns the route overlay. Do not repeat their whole tasks or the six suites: root will run all six after final pins.

Exact proposed final source: {F}/work. Manifest {F}/proposal.json SHA256 {h}. Four nonempty root-diffs contain EVERY additional root change over routeoverlay/preliminary. Verify manifest/all12 final hashes and exact completeness of the root diffs against route overlay at {B}/v20-route-coauthor.v1/overlay (fallback preliminarywork for paths route did not change). Read all nonempty rootdiffs and underlying relevant owning code. Changes are:
1 refine native route why opening (previously only described rows differingrequired despite now handling identical default rows too);
2 narrow false 'one refusal default path can reach' to THIS duplicate-selection refusal in native contract/checkercomment;
3 strengthen selected-scope baseline positive from excluding only2scopeRefusals to rejecting ANY Refusal (helper projection over caller-admitted inputs; not valid closedRun/outputschema claim);
4 refresh coverageView fragment from stale b1fff schema document to exact FINALnativeSchema (your check digest arithmetic);
5 durable fragment-declared-schema membership guard against registered_schema_documents. It is fixture drift prevention, not fullRun qualification.

Root will concurrently run identity1592expected checks in finalsource. You need not repeat all tests: run focused independent arithmetic/positive helper/mutation guard reasoning or a bounded executable probe where useful, disclose exact scope. Do not mutate finalsource. You may copy only needed inputs to your own work. Determine whether these EXACT four changed final files and unchanged carry-forward12file composition are technically sound within this scope. Report actual objections rather than ceremonial approval. Scope extra observations carefully; do not infer current semantic defects from missing speculative future controls.
Return assessment.json and assessment.md naming fullRead scope, exactmanifest, perfilehashassent, substantive reasoning, actual commands/exits, limitations, requiredChanges. No edits to parent. If a required correction is necessary, provide tiny exact patch and reasoning; no silentchanges. Preserve all public evidence. Proceed now.'''
(P/'prompt.txt').write_text(prompt)
args=['/Users/sb/.local/bin/claude','-p','--model','opus','--effort','high','--permission-mode','dontAsk','--tools','Read,Grep,Glob,Write,Bash','--allowedTools','Read','Grep','Glob','Write','Bash','--strict-mcp-config','--output-format','json']
p=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=(P/'response.json').open('wb'),stderr=(P/'stderr.log').open('wb'),cwd=P,start_new_session=True);p.stdin.write(prompt.encode());p.stdin.close();(P/'process.json').write_text(json.dumps({'pid':p.pid,'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':args},indent=2)+'\n');print(p.pid)

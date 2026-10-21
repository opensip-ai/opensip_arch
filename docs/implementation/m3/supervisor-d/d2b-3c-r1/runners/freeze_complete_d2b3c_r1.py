"""Freeze the exact complete D2b-3c review subject only after terminal owning/mutants."""
from pathlib import Path
import json,hashlib,subprocess,shutil
F=Path(__file__).parent;B=F/'native-resume-r1';W=Path('/Users/sb/code/opensip-ai/opensip-d2b3c-native-resume');P=W.parent/'opensip';A=W.parent/'opensip_arch'
S=B/'unit-r1/architecture';PRE='docs/implementation/m3/supervisor-d/d2b-3c-r1';D=S/PRE;Q=Path('/tmp/opensip-implementation/reviews/codex-d2b-3c-r1')
def pin(root,p):
 raw=(root/p).read_bytes();return dict(path=p,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def git(root,*args):return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True).strip()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def copy(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
own=json.loads((B/'owning-r3-retry/report.json').read_text());mut=json.loads((B/'mutations-r2/report.json').read_text());prep=json.loads((B/'prepared.json').read_text())
assert own['allPassed'] and own['publicReceiptBindingsUnchanged'] and mut['allCaught'] and mut['allRestored'] and mut['compiledRuntimeMutants']==9
assert own['sourcePins']==mut['baselineSourcePins']
assert git(W,'rev-parse','HEAD')==git(P,'rev-parse','HEAD')==own['productBase']
assert not git(P,'status','--porcelain') and not git(A,'diff','--name-only','HEAD')
paths=sorted(git(W,'diff','--name-only').splitlines()+git(W,'ls-files','--others','--exclude-standard').splitlines());assert len(paths)==13 and set(paths)=={r['path'] for r in own['sourcePins']}
for row in own['sourcePins']:assert pin(W,row['path'])==row
for row in own['receiptAndCensusPinsUnchanged']:assert pin(W,row['path'])==row
note=json.loads((B/'OWNER-PREFLIGHT-R1-LEAD-NOTE.json').read_text());assert note['limitedSourceRootAssent'] and not note['unitAccepted']
for row in note['sourcePaths']:assert pin(W,row['path'])==row
assert not S.exists() and not Q.exists();D.mkdir(parents=True)
rows=[]
for p in paths:
 copy(W/p,D/'product'/p);r=subprocess.run(['/usr/bin/git','-C',str(P),'show','HEAD:'+p],capture_output=True);parent=None
 if r.returncode==0:
  pp=D/'parents'/p;pp.parent.mkdir(parents=True,exist_ok=True);pp.write_bytes(r.stdout);parent=pin(D/'parents',p)
 rows.append(dict(path=p,parent=parent,candidate=pin(W,p),archived=pin(S,PRE+'/product/'+p)))
assert sum(r['parent'] is None for r in rows)==5
write(D/'product-map.json',dict(rows=rows));(D/'tracked-product.diff').write_bytes(subprocess.check_output(['/usr/bin/git','-C',str(W),'diff','--binary']))
# Include historical failures and current positives. Executables remain pinned external evidence, not product files.
folders=['owning-r1','owner-profile-r1','owning-r2','wide-row-red-r3','wide-row-green-r1','owning-r3-retry','mutations-r1','mutations-r2']
for folder in folders:
 for p in sorted((B/folder).rglob('*')):
  if p.is_file() and p.suffix in ['.json','.jsonl','.log']:copy(p,D/'evidence'/folder/p.relative_to(B/folder))
for n in ['prepared.json','OWNER-PREFLIGHT-R1-LEAD-NOTE.json']:copy(B/n,D/'evidence'/n)
for n in ['trial07-selection.json','recovery-corrections.json','RESTORATION.json']:copy(F/n,D/'evidence'/n)
for n in ['wide-row-red-lane.log','wide-row-green-r1-lane.log','owning-r3-lane.log','owning-r3-retry-lane.log','mutations-r2-lane.log']:
 if (B/n).exists():copy(B/n,D/'evidence'/n)
for p in sorted(F.glob('*.py')):copy(p,D/'runners'/p.name)
pre=B/'owner-preflight-r1/architecture';shutil.copytree(pre,D/'history/owner-preflight-r1/stage')
for n in ['REQUEST.md','subject.json','REVIEW.md','review.json']:copy(Path('/tmp/opensip-implementation/reviews/codex-d2b3c-owner-preflight-r1')/n,D/'history/owner-preflight-r1/review'/n)
auths=[r['path'] for r in json.loads((pre/'docs/implementation/m3/supervisor-d/d2b3c-owner-preflight-r1-subject.json').read_text())['authorities']]
auths+=['docs/implementation/m3/supervisor-d/d2b/PLAN-r3-A1.md','docs/implementation/m3/supervisor-d/d2b-0b-r1-unit.json','docs/implementation/m3/supervisor-d/d2b-2-r2-unit.json','docs/implementation/m3/native-successors-fa/fa-2-unit.json','docs/implementation/m3/native-successors-fa/fa-2/evidence/vectors.json']
# Accepted unit records bind the exact predecessor review and manifest, which remain authorities.
for p in list(auths):
 if p.endswith('-unit.json'):
  unit=json.loads((A/p).read_text())
  for key in ['subjectManifest','independentReview']:
   if isinstance(unit.get(key),dict) and 'path' in unit[key]:auths.append(unit[key]['path'])
auths=sorted(set(auths));authorities=[]
for p in auths:copy(A/p,D/'authorities'/p);authorities.append(pin(A,p))
# Keep source patterns, schemas, compiler and all public census inputs pinned to accepted main.
invariant_paths=['design-lock.json','crates/identity/src/schema_patterns.rs','schemas/sources/symbol-census-v1.schema.json']+[r['path'] for r in own['receiptAndCensusPinsUnchanged']]
invariants=[]
for p in invariant_paths:
 assert (W/p).read_bytes()==(P/p).read_bytes();copy(P/p,D/'accepted-invariants'/p);invariants.append(pin(P,p))
write(D/'source.json',dict(productBase=git(P,'rev-parse','HEAD'),architectureBase=git(A,'rev-parse','HEAD'),worktree=str(W),authorities=authorities,unchangedAcceptedPins=invariants,existingPaths=8,newPaths=[r['path'] for r in rows if r['parent'] is None],sourcePreflightOnly=False,unitAccepted=False,productQualification=False,entireProjectComplete=False))
write(D/'checks-summary.json',dict(finalOwning=own,finalCompiledMutations=mut,earlierOwningAndMutationEvidenceHistoricalOnly=True,signatureBoundaryRed=json.loads((B/'wide-row-red-r3/report.json').read_text()),signatureBoundaryGreen=json.loads((B/'wide-row-green-r1/report.json').read_text()),realBlindInvocations=0,unitAccepted=False,productQualification=False))
(D/'SCOPE.md').write_text('''# D2b-3c complete TS2 successor and replay unit r1

This is the complete unit assigned by accepted D2b PLAN-r3, A1 and A2, following accepted D2b-3a and 3b. Thirteen product paths: eight existing and five new. The recovered archive and old recovered worktree are retained untouched; a fresh checkout at current accepted product main carries the recovered work plus the accepted native startup test appended exactly. The recovered draft was never accepted. No Rust3 codec, production caller, C4 Plan producer, H record admission or qualification is claimed.

## Lead implementation decisions

LD-D2B3C-1: the participant spools the admitted raw FactBatch, Coverage, Complete, Unavailable and BudgetExhausted payloads in admission order, under its existing aggregate bound, then moves them to H at clean settlement. They remain candidates. This makes the received census and entries available without reconstructing them or admitting facts here.

LD-D2B3C-2/3: the successor schema owns Analyze/Complete when the census token is negotiated; the historical branch remains when both exact arrays omit it. CompleteV2 is admitted piecewise under its original schema and represented by the inherited generated Complete carrier plus a parallel typed census event. The original received payload is retained for H. The builder and receive halves enforce both mismatch directions. Token omission/addition fails at HelloAck before source bytes.

LD-D2B3C-4: complete census admission decomposes only the declared large arrays, preserving original schema checks on actual metadata and representative items, then checks every actual element, count, canonical ordering and uniqueness. Each row path must belong to examinedPaths. Count caps and deterministic received CBOR bytes remain distinct; no partial census is admitted. The source-derived closure recomputes frame and embedded relation depth separately, with deepest-valid and one-over tests.

Nested signatureTokens requires another decomposition: a lawful <=4MiB CBOR row may exceed the separate 4MiB canonical JSON limit solely through escaping NULs. The archived red-r3 proves this at runtime; earlier setup/compile failures do not count. The correction retains all row metadata and its first token for the original row schema, enforces the original token maxItems, and checks every later token's type and Unicode scalar maxLength directly. CensusLaw first requires the pinned item schema to have exactly type:string, minLength:0 and maxLength; any extra item constraint fails closed. This checks each token once rather than repeatedly serializing large row metadata. NFC/Unicode CBOR admission stays prior. Repeats and token order are retained. Actual original rows pass into ordering, received-byte accounting, generated typing and H. No new schema entrypoint, generic matcher policy, copied pattern or arbitrary validation waiver is introduced. Wide ASCII, NUL and non-BMP positives and late length/type/count negatives cover this boundary. Mutations distinguish early schema refusal from later generated conversion refusal.

LD-D2B3C-5: over-bound is a typed admitted event only when a declared count or possible byte bound is exceeded, with no rows. No provider fault is manufactured. H owns the scope-limit route and projected record cap.

LD-D2B3C-6/7: only symbol-kind keys under a census defer their census-dependent returned commitment check to H. Non-symbol keys retain exact echoes. The Plan supplies owed census/enumeratorClosure and Dempty commitments; the builder verifies the supplied request values. D2b decides neither Plan admission nor returned subject settlement. Clean Complete/over-bound/Unavailable/BudgetExhausted entries and received handoff are covered.

The two identity files implement the already published FA2 LogicalPath dot keyword under its resolved registered owner only. The independent owner source preflight ruled existing FA2/D2b authorities sufficient. Its two source files stay exact here. Generic72 forms, three native owners/26 forms, foreign resolved documents, other six census patterns, patternProperties, 52-source raw guard, 15 aliases and shared matcher remain unchanged. This preflight alone did not accept this unit.

## Replay and evidence boundaries

Original trial07 is 353 vectors/31 rules, pinned byte-exact. The integer selection retains 352 by value and preserves one intentional Rust3 float-zero vector as exact raw metadata, explicitly deferred to D2b-4c. This unit does not claim to execute 352 TS2 vectors. Fifteen rule families have TS2-owned replay paths; mixed protocol/site families are filtered to their owned inputs. Sixteen families have explicit Rust3/C4/H ownership reasons, and the classification is checked complete. FA2 vectors are separately hash-pinned. D2b-T4 covers every echo mismatch before disclosure; T5 checks the complete commitmentMap set and swapped domain/class/order refusals. The 1.6GB Plan metadata case is not materialized; the actual 64MiB wire-accounting case runs and passes in the complete suite.

Final owning-r3-retry covers exact final13pins: identity81, components270, docs3, operability96, Clippy three packages/all targets/-Dwarnings, workspace alltargets and design verification; focused accepted-native/path-replay/wide-row checks pass. The initial owning-r3 precheck stopped before tests because a previous executable had been rebuilt by the focused green run; retry archives the already preserved exact R2 owning binary. No source or test expectation changed for that precheck. Final nine mutants compile and fail their intended runtime assertions, then restore all13sourcepins and pass a fresh positive each time. Compile failures never count. Previous owning/mutation rounds are historical where source changed. Both public receipt binding objects recompute equal to current; all four receipt/census files stay exact. No blind mode or private fixture was used.

## Remaining project obligations

Full independent ACCEPT-UNIT and substantive root assent precede exact code integration. Then the five new paths require an additive inventory successor (anticipated235), preserving raw234 parent rows and all inherited meanings plus projecting current direct description meanings (117+15 expected132 absent another accepted change). Existing retained predecessors remain qualified through the descriptions mechanism. Current source39 registration, production wiring, C4/H implementation, Rust3-4a/4b/4c, signing/installation, all platform/owner/privacy/clock gates and complete project qualification remain separate. No unit acceptance proves the entire project complete.
''')
manifest=PRE+'-subject.json';write(S/manifest,dict(schemaVersion=1,unit='D2B-3c-r1',authorities=authorities,files=[pin(S,str(p.relative_to(S))) for p in sorted(S.rglob('*')) if p.is_file()]))
Q.mkdir(parents=True);subject=dict(unit='D2B-3c-r1',architectureStage=str(S),subjectManifest=pin(S,manifest),productBase=git(P,'rev-parse','HEAD'),architectureBase=git(A,'rev-parse','HEAD'),worktree=str(W));write(Q/'subject.json',subject)
(Q/'REQUEST.md').write_text(f'''# Complete D2b-3c r1 independent unit review

Read subject.json and the frozen stage {S}; rehash every manifest member/authority and the exact13path product map (8existing/5new), parent bytes against pinned accepted main and live candidate bytes. Manifest SHA256 {subject['subjectManifest']['sha256']}. This requests full ACCEPT-UNIT for accepted D2b PLAN-r3+A1+A2 D2b-3c, not another source preflight. Read SCOPE.md and final checks-summary.json, complete implementation and tests. Judge all LD-D2B3C decisions against LD-D2B2/3/14/16/18, RF3 and D2bT4/T5, actual accepted FA2 vectors and predecessor3a/3b. Audit receive/send token variants, old refusals, exact before-source echoes, Plan Dempty join, separate wire/relation depth closure, census bytes/count/order/path/null, typed overbound without providerfault, clean terminals, raw received census+entries handoff and H settlement boundary. Judge nested signatureTokens decomposition: lawful CBOR vs escapedJSON cap, exact closed item shape guard, all actual metadata/count/type/scalars, linear work, repeat/order retention, no extra schema policy. Check archived actual runtime red and green plus new mutants; setup/compile failures are not evidence of a kill. Two identity files remain exact to source preflight; its ruling supplies no acceptance of the rest. Shared matcher/native profile/registry sources/aliases must remain unchanged.

Validate final exact-source owning-r3-retry and9fresh compiled runtime mutants/restorations. R2 checks/mutations are historical because runtime changed afterward. Each mutant has intended runtime witness, all13bytes restored and positive recompiled. The late-token mutant may fail at later generated Admission instead of required Schema; that still proves the early guard's necessity. Check meaningful tests rather than totals. Trial07 353raw/352selected-by-value does NOT mean352TS2executions: inspect actual filters/31rule classification/15mixed TS2families/16otherowner families; preserve the exact raw Rust3 float0.0 deferral to4c. No 1.6GB materialization claim. Public receipt bindings stay current and four data pins exact, zero real blind runs. Protected unrelated drafts untouched. Judge five-path additive inventory and current direct meaning projection as mandatory carried obligations, with no production/qualification waiver.

Read-only source/JSON/hash/Git queries only. No builds/tests/Cargo/generation/lanes/network/panes/delegation. No repository/worktree/stage/control/evidence edits. Write ONLY REVIEW.md and review.json in {Q}. JSON: verdict ACCEPT-UNIT or REQUIRED-FINDINGS; subjectManifestSha256; requiredFindings; nonBlockingObservations; productQualification:false. Finding IDs D2B3C-R1-RF-n/NBO-n. Unit review grants no integration, inventory, source39 registration or whole-project qualification.
''')
print(json.dumps(subject,indent=2))

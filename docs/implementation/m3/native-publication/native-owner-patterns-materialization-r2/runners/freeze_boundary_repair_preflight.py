from pathlib import Path
import json,hashlib,shutil,subprocess
F=Path(__file__).parent;B=F/'boundary-repair-preflight-r1';Q=Path('/tmp/opensip-implementation/reviews/codex-native-owner-boundary-repair-preflight-r1');assert not B.exists() and not Q.exists()
W=Path('/Users/sb/code/opensip-ai/opensip-native-owner-patterns-takeover');P=W.parent/'opensip';A=W.parent/'opensip_arch'
def pin(root,p):
 raw=(root/p).read_bytes();return dict(path=p,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def copy(src,dst):dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
oldq=Path('/tmp/opensip-implementation/reviews/codex-native-owner-materialization-r1');oldsub=json.loads((oldq/'subject.json').read_text());olds=Path(oldsub['architectureStage']);pre='docs/implementation/m3/native-publication/native-owner-patterns-materialization-r1';oldmap=json.loads((olds/pre/'product-map.json').read_text())['rows']
repaired=['crates/identity/src/schema_patterns.rs','crates/identity/src/schema_tests.rs'];source=[]
full=json.loads((F/'full-r5/report.json').read_text());assert len(full['sourcePins'])==42
for row in oldmap:
 p=row['path'];now=pin(W,p);assert now['sha256']==full['sourcePins'][p]
 if p in repaired:
  assert now!=row['candidate'];copy(W/p,B/'proposed'/p);copy(olds/pre/'product'/p,B/'rejected-r1'/p)
 else:assert now==row['candidate']
 source.append(dict(path=p,rejectedR1=row['candidate'],candidate=now,changed=p in repaired))
for folder,names in [('inherited-boundary-fix-r1',['report.json']),('inherited-boundary-focused-r1',['report.json','identity.log','registered-host.log','provider-paths.log']),('ecma-full-differential-r4',['report.json','main.rs','reference.cjs','rust.log']),('mutations-r2',['report.json']),('companion-mutations-r2',['report.json'])]:
 for n in names:copy(F/folder/n,B/'evidence'/folder/n)
for n in ['fix_inherited_profile_boundary.py','native_mutations_r2.py']:copy(F/n,B/'runners'/n)
for n in ['REVIEW.md','review.json','subject.json']:copy(oldq/n,B/'history/rejected-unit-r1'/n)
write(B/'source.json',dict(productBase=subprocess.check_output(['/usr/bin/git','-C',str(P),'rev-parse','HEAD'],text=True).strip(),architectureBase=subprocess.check_output(['/usr/bin/git','-C',str(A),'rev-parse','HEAD'],text=True).strip(),rejectedR1Subject=oldsub,changedPaths=repaired,rows=source,currentFullOwningStillPending=True,unitAccepted=False,blindModesRun=False))
write(B/'subject-manifest.json',dict(schemaVersion=1,unit='NATIVE-OWNER-BOUNDARY-REPAIR-PREFLIGHT-r1',files=[pin(B,str(p.relative_to(B))) for p in sorted(B.rglob('*')) if p.is_file()]))
Q.mkdir();subject=dict(stage=str(B),subjectManifest=pin(B,'subject-manifest.json'),sourcePreflightOnly=True,unitAccepted=False);write(Q/'subject.json',subject)
(Q/'REQUEST.md').write_text(f'''# Required finding OWNPAT-UNIT-R1-RF-1 source repair preflight

Read subject.json and frozen stage {B}, manifest SHA256 {subject['subjectManifest']['sha256']}. Rehash all members and source.json joins to rejected complete R1 manifest/map and current pinned Git bases. Only two of42product paths changed; the other40remain exact. This asks source PREFLIGHT-CLEAR only while the fresh full owningR5 runs, never ACCEPT-UNIT/integration/qualification.

Judge whether OWNPAT-UNIT-R1-RF-1 is repaired without an inherited-profile expansion. Both corrected complete-relative-path literals and Kind::CompleteRelativePath are removed from the shared TABLE and generic dispatcher; the table is byte-exact to accepted main's72-form predecessor. Only matches_native_owner evaluates the two new forms, after its closed26form gate. Native owner/profile/reference boundaries and patternProperties routing remain selected; no source/map/generator/fixture/provenance file changes. Test both native literals under selected native pattern owners, generic/foreign admission refusal including native-to-foreign refs, and native/foreign patternProperties refusal. New test compares the ENTIRE shared form set with exact72predecessor literals, not merely old-pattern outputs.

Focused identity78/registeredhost2/provider1 controls pass. Strengthened full differential compares exact inherited sets, refuses both new literals for all119250inputs through the inherited evaluator, and compares3.1Mnative/8.586Minherited results with zero mismatches. Fresh13core plus4companion compiled mutants are caught/restored; new mutants reinsert EACH corrected literal in sharedTABLE and route patternProperties through nativeprofile, all compiling then failing runtime controls. Complete owningR5 is separate and pending; no final check/acceptance claim. Prior complete R1 remains REQUIRED-FINDINGS and preserved. All prior companion/selected source bytes remain exact. No blindmode/privatecontent used.

Read-only hashes/JSON/Git/source queries only; no builds/tests/Cargo/generation/lanes/network/panes/delegation or repo/worktree/stage/control/evidence edits. No private413/keys/installations/heldout/T2/census modes. Write ONLY REVIEW.md and review.json in {Q}. JSON: verdict PREFLIGHT-CLEAR or REQUIRED-FINDINGS; subjectManifestSha256; requiredFindings;nonBlockingObservations;sourcePreflightOnly:true;unitAccepted:false;blindRefreshComplete:false;productQualification:false. IDs OWNPAT-BOUND-PRE-R1-RF-n/NBO-n. Complete repaired code-unit acceptance must follow full owning evidence and separate review.
''');print(json.dumps(subject,indent=2))

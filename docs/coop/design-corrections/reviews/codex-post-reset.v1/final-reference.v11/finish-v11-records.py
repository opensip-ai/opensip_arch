from pathlib import Path
import json,shutil,hashlib
r=Path.cwd();dc=r/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1';tmp=Path('/tmp/opensip-design-corrections/codex-post-reset.v1');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert (dc/'historical-preservation-report.v11.json').is_file()
checks=Path('/tmp/opensip-design-corrections/final-reference-v11');report=json.loads((checks/'reference-checks.json').read_text());assert report['passed']
dest=out/'final-reference.v11';assert not dest.exists();shutil.copytree(checks,dest)
for name in ['run-final-v11.py','adapt-integration-builder-v11.py','refresh-pins-v6.py','record-v11.py','finish-v11-records.py','prepare-v11-dispositions.py']:
 shutil.copyfile(tmp/name,dest/name)
for stem in ['annotation-traversal-final-v11','annotation-alias-final-v11','annotation-inherited-limbs-final-v11']:
 shutil.copyfile(Path('/tmp/opensip-design-corrections')/(stem+'.log'),dest/(stem+'.log'))
rows=[{'path':str(p.relative_to(dest)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(dest.rglob('*')) if p.is_file()];(dest/'custody.json').write_text(json.dumps({'standing':'Codex executed final-source commands and integration/recording scripts, not independent acceptance.','files':rows},indent=2)+'\n')
rp=dc/'reviews/post-reset-review.v10/review.json';rev=json.loads(rp.read_text());assert not rev['newMustIssues'] and [x['id'] for x in rev['newShouldIssues']]==['v10-S1'];ref={'path':str(rp.relative_to(r)),'sha256':sha(rp),'subjectManifestSha256':'82c1be11d3b61908b2a45ebb6e59e71bb5cb31d8450a96a61857ced430e786fd','overallVerdict':'CHANGES_REQUIRED','unresolvedShouldIds':['v10-S1']}
p=dc/'correction-crosswalk.proposed.json';d=json.loads(p.read_text())
for row in d['items']:
 row.setdefault('historicalReviews',[]).append(row['latestCompletedReview']);row['latestCompletedReview']=dict(ref,selector='/arDispositions/'+row['id'],standing='Completed v10 predecessor review resolves previous annotation findings but requires same-path order independence. Corrected successor requires new independent review; fresh blind and complete application remain separate gates.')
p.write_text(json.dumps(d,indent=2)+'\n')
p=dc/'post-reset-dispositions.v11.proposed.json';d=json.loads(p.read_text());d['actualCoauthorHistory']=[{'path':f'docs/coop/design-corrections/reviews/digest-corrections-author.{v}/handoff.json','sha256':sha(dc/f'reviews/digest-corrections-author.{v}/handoff.json'),'sessionId':'5dec928a-6357-4726-9ea8-49a3079fb726','role':'Actual Claude coauthor, not independent acceptance'} for v in ('v7','v8','v9')]
for row in d['advisoryCorrections']:row['status']='CORRECTED-PENDING-INDEPENDENT-REVIEW'
d['advisoryCorrections'][0]['evidence']='reviews/codex-post-reset.v1/normative-annotation-clarification.v11/custody.json';d['advisoryCorrections'][1]['evidence']=d['advisoryCorrections'][0]['evidence'];d['advisoryCorrections'][2]['evidence']='reviews/codex-post-reset.v1/annotation-aggregation-final-recheck.v11/result.json';d['advisoryAccount']['standing']='28 carried actual advisories; current A1/A2/A3 corrections and limits explicitly accounted, pending independent successor assessment.';p.write_text(json.dumps(d,indent=2)+'\n')
p=out/'advisory-application-account.v11.proposed.json';a=json.loads(p.read_text());a['standing']='28 carried actual v5-v10 advisories; A1/A2 normative clarification and A3 discriminating merge regressions applied to proposed v11 with exact custody, pending fresh independent acceptance. No actual v11 assent yet.'
for row in a['items']:
 if row['id']=='v10-A1':row['disposition']='Corrected in proposed v11: the existing normative identity contract explicitly names conflicting effective annotations and unaddressable claimed joins as refusals. The exact insertion was substantively assessed by actual Claude and applied by Codex with before/after custody. Registered schema bytes and payload types are unchanged. Fresh independent acceptance remains required; historical advisory severity unchanged.'
 if row['id']=='v10-A2':row['disposition']='Corrected in proposed v11: the normative identity contract supplied to the blind kit states effective annotation inheritance, intermediate aliases, terminal exclusion, per-occurrence coverage and order independence, with top-level non-governed property and join-addressing boundaries. Exemption reasons remain an authoring disclosure expectation; reference admission checks declared retention, not reason prose presence/content. Actual Claude assessed the exact final insertion; fresh independent and new blind assessment remain required.'
 if row['id']=='v10-A3':row['disposition']='Corrected in proposed v11 with cases that actually reach same-path aggregation: both original orders and all-lawful controls, plus a later annotation after missingness. Actual coauthor pre/post source measurements discriminate four negative cases; all five Codex final-source rechecks pass. Count growth is not claimed as exhaustive coverage. Original independent zero-collision instrumentation is preserved.'
p.write_text(json.dumps(a,indent=2)+'\n')
tech='''# Codex technical review of proposed v11 corrections

Standing: coauthor/integration assessment, **not independent acceptance or implementation readiness**. The actual completed v10 independent review is CHANGES_REQUIRED: zero MUST, one SHOULD v10-S1 and three advisories. Its exact JSON SHA is `64e15aff50d77f0f84b53c145acc6a46d208afe0a1e090272d5deaf25ca3e8f9`. The original reviewer custody.json is preserved verbatim; Codex's additional receipt is codex-retention-custody.json. All 2,502 frozen files verified before/after/final, and all six commands, logs and deterministic reports were reproduced byte-identically.

## Correction and actual collaboration

The independent review resolves v9-S1 and confirms the effective-annotation cases from v10, but finds a remaining same-path aggregation defect. `record()` merged incoming annotations before testing their absence. An annotated sighting followed by an unannotated sighting admitted, while the opposite order refused. The reviewer proved this both with referenced-container/local-property occurrences and with a pure JSON key-order swap between items and additionalProperties. Every hypothetical schema passed the metaschema, and positive controls discriminated. The full 661-check authored suite reached the merge zero times: the earlier oneOf fix separated branch paths, so passing those tests did not exercise this merge.

Actual Claude coauthor session `5dec928a-6357-4726-9ea8-49a3079fb726` corrected an isolated frozen-v10 copy while the independent reviewer completed its review. Neither live nor frozen candidate files changed during those passes. Codex retained the successful final coauthor response, exact released sources and public tool evidence, then applied only its two-file delta after both passes completed. Full before-images and source hashes are in `released-coauthor-delta.v11/`.

The corrected reference keeps missingness as an explicit monotonic fact alongside the accumulated annotations. Once an occurrence at a location lacks an annotation, no later annotation can erase that absence. The merge uses typed equality for annotation deduplication, matching conflict checks. All earlier missing-annotation, retention, join, alias, branch, terminal exclusion and join-addressing controls remain in force. New actual pre/post measurements discriminate four negative cases, and all-lawful controls remain admitted. This remains schema/reference consistency for reviewed future registry edits, not a current payload or Run attack: shipped closed selectors have no unannotated governed fields or same-path collisions.

## Normative wording, settled before the blind pass

Codex chose to address the independent v10-A1/A2 advisories now, preserving their original nonblocking severity. The supported inheritance and conflict rules must be discoverable from the normative subset supplied to the next blind consumer, without reading author Python. Codex proposed a paragraph in the existing identity-and-evidence contract. Claude substantively checked it, identifying that exemption reasons are an authoring disclosure expectation while reference admission validates retention rather than prose presence or content. No `reason` key was invented. Codex accepted that distinction and explicitly limited the non-governed-property clause to top-level selector properties, matching the direct second pass; Claude measured and acknowledged that correction too.

Claude then read the exact final 2,825-byte insertion, SHA `32db349536ffc74081b5081aa698f9966d100485268fc24822fde2a1a94cd13f`, and confirmed that it accurately states the corrected reference. Codex applied those exact bytes with full contract before/after custody in `normative-annotation-clarification.v11/`. Earlier draft notes and handoffs remain distinct evidence; no agreement is inferred from an earlier unread version. The coauthor did not read the full completed independent v10 review and does not claim to have done so; its substantive p02/p03 and exact wording assessments have their own retained scope.

The insertion states governed forms, supported local-reference/container/branch traversal, annotation inheritance with terminal-type exclusion, per-occurrence coverage, monotonic missingness, conflict refusal, declared retentions, top-level join addressing, and the distinction between schema coherence and owning-fact truth. The raw registered schema documents and registry bytes are unchanged, so this normative prose does not change their identity preimages. The prospective application tooling is separate and still requires independent application review.

## Final-source verification

Five Codex rechecks pass on the exact released source:

- `annotation-aggregation-final-recheck.v11/`: eight metaschema-valid cases cover both original order arrangements, all-annotated positive controls and single-occurrence controls; missing occurrences refuse with the intended cause.
- `annotation-coverage-final-recheck.v11/`: all 13 actual selectors admit; 39 injected governed fields and a removed existing annotation refuse; the two earlier residue rules retain their intended causes.
- `annotation-traversal-final-recheck.v11/`: referenced containers and both original branch orders refuse missing annotations while the actual document admits.
- `annotation-alias-final-recheck.v11/`: missing alias annotation refuses; field-local and intermediate-alias annotations admit.
- `annotation-inherited-limbs-final-recheck.v11/`: all nine field/alias/branch retention and join cases match their expected refusals and lawful exemptions.

The integration fixture is extracted from the released checker with its exact source hash and explicit declaration list; synthetic composition remains distinct from an independent oracle. All four consuming pin sets are refreshed against their current inputs. The six final executed commands pass, with logs, source hashes and scripts retained in `final-reference.v11/`; the validation summary records their measured counts. These are authored/reference results, not independent acceptance.

## Limits and remaining acts

The coauthor's failed insertion and incorrect first three-occurrence fixture remain disclosed. A duplicated comment already in frozen v10 was restored exactly rather than silently tidied. The corrected three-occurrence construction uses a two-level reference chain; an allOf branch would have a different location. Earlier failed neutralisation and reviewer harness attempts remain literal historical evidence. The reviewer initially checked 31 protected files against a scoped snapshot, then correctly checked them against the repository; all 31 are unchanged. Its p01 removal tally includes non-governed UInt64 byteLength, whose annotation removal is not a third-limb missing-governed-field refusal.

The 28 carried v5-v10 advisory dispositions are explicit. L1-L3 normalization and level-specification fixture assets remain unqualified. No clone facts alone exempts Coverage prerequisites. Complete-ledger comparison and actual host/renderer failure wiring remain implementation obligations. All AR/FW, inherited residual and scoped-review routing obligations remain accounted; all 32 qualification gates remain undemonstrated. D-371 already selects the complete intended-product scope; the remaining unapplied correction/readiness act is D-372. The v10 review's shorthand D371/D372-unapplied statement does not undo that existing selection.

A fresh independent review of frozen v11 at zero unresolved MUST/SHOULD, actual Codex assent, a NEW fresh blind consumer on those accepted normative bytes, and complete independently reviewed application/readiness reconciliation remain required. This technical assessment authorizes no product implementation, commit or push.
'''
p=out/'technical-review.v11.md';assert not p.exists();p.write_text(tech)
p=dc/'README.md';old=p.read_text();p.write_text('''# Architecture corrections — v11 ready for independent review

**Not ready for implementation.** Actual Claude and Codex corrected the remaining schema key-order dependence and added mutually assessed normative wording for annotation inheritance and conflict handling. [The technical assessment](reviews/codex-post-reset.v1/technical-review.v11.md) records the exact source custody, five final rechecks, six passing commands and their limits.

The newly frozen successor must receive fresh independent acceptance with zero unresolved MUST/SHOULD, a new blind consumer on the accepted normative bytes, and complete independently reviewed application/readiness reconciliation. No product implementation, commit or push is authorized. [The resume guide](reviews/NEXT-REVIEW.md) owns current status.

## Earlier progress — historical

'''+old)
print('V11 final evidence,28-advisory account, crosswalk, normative assessment and technical review recorded; no independent acceptance.')

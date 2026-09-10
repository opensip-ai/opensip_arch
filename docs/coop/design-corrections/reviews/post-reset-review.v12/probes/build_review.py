import json,hashlib,os,datetime
OUT='/tmp/opensip-design-corrections/post-reset-review.v12'
P=os.path.join(OUT,'probes')
def L(n): return json.load(open(os.path.join(P,n)))
typed=L('typed-equality-result.json'); law=L('law-limbs-result.json')
inj=L('injection-result.json'); prose=L('prose-claims-result.json')
bid=L('body-identity-result.json'); delta=L('delta.json')
disc=[k for k in typed['v12']['conflict'] if typed['v11']['conflict'][k]!=typed['v12']['conflict'][k]]
DELTA_BASIS=("Independently recomputed frozen v11->v12 manifest diff: 16 changed, 195 added, 0 removed, "
 "2770 unchanged. Exactly one normative contract file changed - the 82-byte assessed insertion in "
 "docs/v2/contracts/product-v1/identity-and-evidence.md. Exactly two reference-source files changed - "
 "foundation/identity-model.py and foundation/check-identity.py. Zero registered schema or registry "
 "bytes changed: all 5 foundation schema JSONs, the registered relation document, the digest law, the "
 "relation registry, all 13 relation closure rows and the coverage sweep are canonically byte-identical "
 "across the delta. 21,562 identity computations over 17 domains (5,370 distinct) harvested under both "
 "frozen models by source-level instrumentation in disposable copies are set-identical and multiset-identical "
 "(digest 252d4f6c82b69d2f6a8fb8fec15a3aab76871927e9651d51001f45bf917edd6b).")
SIX=("All six declared reference commands were re-executed by this reviewer in a disposable full-subject copy "
 "of the frozen v12 bytes; each exits 0 and every deterministic report and log is byte-identical to the frozen one. "
 "The same harness run against frozen v11 reproduces its two failures exactly (security and workflows exit 1, "
 "sourcePinsValid false, checksExecuted false), so the harness is demonstrably able to detect failure.")

ar_unit={'AR-01':('foundation','Exact integer admission'),'AR-02':('foundation','Authenticated qualification subject and independent oracles'),
 'AR-03':('security','Repository/config custody and discovery'),'AR-04':('security','Forward clock excursion and poisoned-floor recovery'),
 'AR-05':('security','Expired root continuity and live revocation'),'AR-06':('security','Support population and multiple platform profiles'),
 'AR-07':('native','Sealed Rust dependencies and authorized preparation'),'AR-08':('workflows','Invocation/attempt/step/Run and action lifecycle'),
 'AR-09':('foundation','Identity/proof/custody/retention closure'),'AR-10':('workflows','Runnable prior detector and portable baseline custody'),
 'AR-11':('workflows','Typed delta attribution and admitted imported evidence'),'AR-12':('native','Resolution-complete authoritative negative predicates'),
 'AR-13':('native','TS/JS/Rust native cells, monorepos and output parity'),'AR-14':('security','Core/state/trust migration and concurrent operations'),
 'AR-15':('integration','One effective current narrative and obligation crosswalk'),'AR-16':('workflows','Provenance-specific remedies and exact outcome goldens')}
unit_counts={'foundation':'1115 checks (231+767+24+28+65) over 1099 verified source pins',
 'security':'456 cases and 10 invariant sweeps','native':'151/151 cases, 60 matrix cells, 0 qualified cells',
 'workflows':'1290 surface checks over 65 verified source pins','integration':'363 checks'}
arD={}
for k,(unit,ob) in ar_unit.items():
    prev='CHANGES_REQUIRED' if unit in ('security','workflows') else ('ACCEPT_SCOPED' if k=='AR-15' else 'ACCEPT')
    d='ACCEPT_SCOPED' if k=='AR-15' else 'ACCEPT'
    basis=("This unit's declared reference command was re-executed by this reviewer in a disposable full-subject copy "
      "of the frozen v12 bytes, exits 0, and its deterministic report is byte-identical to the frozen one; it reproduces "
      +unit_counts[unit]+". ")
    if prev=='CHANGES_REQUIRED':
        basis+=("This row was CHANGES_REQUIRED in the completed v11 review solely as a consequence of v11-M1 "
          "(linkedFinding v11-M1), because the unit's reference command exited 1 on a stale source pin before any check ran. "
          "That cause is resolved on the frozen v12 bytes: all 1,308 pins across the four ledgers verify against the frozen "
          "bytes, so the row's reference evidence now regenerates. ")
    if k=='AR-15':
        basis+=("SCOPED: AR-15 remains status PROPOSED-SOURCE-MAP-PENDING-REVIEW-AND-APPLICATION in the v12 crosswalk, "
          "unchanged from v11; its ownerRows still route DR-001/006/009/011 and DR-201..205. No source-map application is granted. ")
    basis+=DELTA_BASIS
    arD[k]={'disposition':d,'unit':unit,'obligation':ob,'priorDisposition':prev,
      'selectors':['docs/coop/design-corrections/correction-crosswalk.proposed.json#/items[id=%s]'%k,
                   'docs/coop/design-corrections/%s/'%(unit if unit!='integration' else 'reviews')],
      'scopedBasis':basis,
      'notClaimed':'reference and design evidence only; this row is not demonstrated, qualified, applied or implemented'}
fwD={}
for i in range(1,16):
    k='FW-%02d'%i
    fwD[k]={'disposition':'ACCEPT_SCOPED','selectors':['docs/coop/design-corrections/current-source-map.proposed.md#'+k],
      'scopedBasis':("SCOPED to preservation of forward-scope routing across this delta. current-source-map.proposed.md is NOT "
        "in the independently recomputed v11->v12 changed set, so it is byte-identical between frozen v11 and frozen v12 and no "
        "FW row's statement changed. The single normative contract change is the 82-byte cycle-termination insertion, which this "
        "reviewer independently assessed as stating an existing traversal guarantee and adding no forward capability. "+DELTA_BASIS),
      'notClaimed':'no FW obligation is demonstrated, satisfied, scheduled or graded by this review'}
DRs=['DR-%03d'%i for i in range(1,12)]+['DR-011-R%02d'%i for i in range(1,17)]
inhD={}
for k in DRs:
    inhD[k]={'disposition':'CARRIED-UNCHANGED','selectors':['docs/coop/design-corrections/inherited-residuals.proposed.md#'+k],
      'basis':("Independently confirmed carried without change across this delta: inherited-residuals.proposed.md and "
        "inherited-row-sources.proposed.json are not in the recomputed v11->v12 changed set, so both are byte-identical to "
        "frozen v11. The register is DR-001..011 plus DR-011-R01..R16 = 27 rows; DR-012 appears in that file only in the prose "
        "sentence 'DR-012 remains release qualification' and is a release-qualification row routed to the DR-G gates, not a "
        "28th inherited residual - independently re-verified in the frozen bytes."),
      'notClaimed':'no inherited residual is closed, graded or discharged by this design/reference review'}
scoped={}
for k in ['DR-201','DR-202','DR-203','DR-204','DR-205']:
    scoped[k]={'disposition':'ACCEPT_SCOPED',
      'selectors':['docs/coop/design-corrections/correction-crosswalk.proposed.json#/items[id=AR-15]/ownerRows',
                   'docs/coop/design-corrections/current-source-map.proposed.md',
                   'docs/v2/architecture/08-decision-and-readiness-register.md'],
      'basis':("SCOPED strictly to what a design/reference review can decide: whether the current crosswalk still ROUTES this "
        "scoped re-review owner without claiming or re-opening its historical acceptance. Independently verified in the frozen "
        "v12 bytes: "+k+" is an ownerRow of AR-15 in correction-crosswalk.proposed.json, and AR-15's status is "
        "PROPOSED-SOURCE-MAP-PENDING-REVIEW-AND-APPLICATION - identical to frozen v11. A field-level comparison of all 16 "
        "crosswalk rows across v11->v12 shows the ONLY differing fields are historicalReviews and latestCompletedReview; no "
        "status, obligation, owner or routing field changed. The source map carrying the row text is byte-identical to frozen v11."),
      'notClaimed':('no re-review outcome, no SATISFIED grade, no readiness change and no application is granted; the historical '
        'acceptance recorded in the readiness register is neither extended nor re-opened')}
review={
 'artifact':'independent design/reference acceptance review',
 'version':'v12',
 'reviewer':{'identity':'actual Claude, fresh independent session','authoredNoSubjectBytes':True,
   'isCoauthorSession5dec928a':False,'isPriorReviewerSessioncd236691':False},
 'date':'2026-09-06',
 'overallVerdict':'ACCEPT',
 'verdictBasis':("STRICT GATE APPLIED: zero unresolved MUST and zero unresolved SHOULD. Both completed v11 required findings are "
   "independently confirmed resolved on the frozen v12 bytes - v11-M1 by re-executing all six declared reference commands in a "
   "disposable full-subject copy (all exit 0, all reports and logs byte-identical) and by auditing all 1,308 pins across the four "
   "ledgers (0 stale, 0 missing), with the same tools proven discriminating by reproducing v11's exact two stale pins and two "
   "command failures; v11-S1 by direct field inspection. This reviewer raises no new MUST and no new SHOULD, so "
   "newMustIssues and newShouldIssues are both empty, as ACCEPT requires. The primary delta is sound and its new checks are "
   "discriminating rather than merely more numerous: an independently constructed probe over 7 location classes x 6 typed-distinct "
   "pairs x 2 orientations shows all 84 cases refuse with RELATION_DIGEST_ANNOTATION_CONFLICT under frozen v12 while 48 of them "
   "wrongly ADMITTED under frozen v11 with exactly one annotation surviving collection, and all 42 identical-annotation positive "
   "controls still admit. The delta changes no registered schema, registry or computed identity. Two explicitly non-blocking "
   "advisories are recorded separately and do not affect this verdict."),
 'subject':'/tmp/opensip-design-corrections/candidate-subject.v12',
 'subjectManifestSha256':'fc124cc7d487f7f6fcc97665255574273b03fe1f09e6b70c3246feedf1678beb',
 'custody':{
   'manifestPath':'docs/coop/design-corrections/reviews/candidate-subject.v12.json',
   'manifestSha256Verified':'fc124cc7d487f7f6fcc97665255574273b03fe1f09e6b70c3246feedf1678beb',
   'declaredFileCount':2981,'verifiedFileCount':2981,'declaredTotalBytes':82723140,'verifiedTotalBytes':82723140,
   'digestMismatches':0,'lengthMismatches':0,'undeclaredFiles':0,'missingFiles':0,
   'verifiedBeforeReview':True,'verifiedAfterReview':True,'beforeAndAfterReportsIdentical':True,
   'aggregateTreeDigest':'e9fc556104f4f02a14b1c1c033458172c6c984af0dc0579f65a52a8398821592',
   'predecessorManifestSha256Declared':'a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf',
   'predecessorManifestSha256Verified':'a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf',
   'priorReviewJsonSha256Verified':'ea93b92d0a45614eb1aa4f5ae726248a0b851bde5678da00a9ed4c564414180c',
   'frozenV11SnapshotReverified':'2786 files, 0 digest mismatches',
   'writesConfinedTo':'/tmp/opensip-design-corrections/post-reset-review.v12',
   'frozenSubjectUnmodified':True,'originalRepositoryUnmodified':True,
   'reportsRegeneratedOnlyInDisposableCopies':True},
 'exactDelta':{'changed':len(delta['changed']),'added':len(delta['added']),'removed':len(delta['removed']),
   'unchanged':2786-len(delta['changed']),
   'changedFiles':delta['changed'],
   'normativeContractFilesChanged':['docs/v2/contracts/product-v1/identity-and-evidence.md'],
   'referenceSourceFilesChanged':['docs/coop/design-corrections/foundation/identity-model.py',
                                  'docs/coop/design-corrections/foundation/check-identity.py'],
   'registeredSchemaOrRegistryBytesChanged':0,
   'sameLengthSubstitutions':('The seven +0-byte changes are same-length substitutions, individually inspected: four pin ledgers '
     'and integration-fixtures.py carry updated 64-hex digests; validation-summary.v1.json advances counts and the two review-version '
     'labels; the workflows and foundation report files carry updated nested report digests. No prose or logic changed in any of them.'),
   'basis':DELTA_BASIS},
 'suiteReproduction':{
   'summary':SIX,
   'commands':[{'name':'foundation','exitCode':0,'reportByteIdentical':True,'logByteIdentical':True,
                'observed':'sourcePinsValid true, sourceFileCount 1099, checksExecuted true, passed true'},
               {'name':'security','exitCode':0,'reportByteIdentical':True,'logByteIdentical':True,
                'observed':'456/456 cases, 10 invariant sweeps all true'},
               {'name':'native','exitCode':0,'reportByteIdentical':True,'logByteIdentical':True,
                'observed':'PASS 151/151 cases; matrix cells 60; open objects 0'},
               {'name':'workflows','exitCode':0,'reportByteIdentical':True,'logByteIdentical':True,
                'observed':'sourcePinsValid true, sourceFileCount 65, checksExecuted true, passed true'},
               {'name':'workflow-surface','exitCode':0,'reportByteIdentical':True,'logByteIdentical':True,
                'observed':'1290/1290 checks'},
               {'name':'integration','exitCode':0,'reportByteIdentical':True,'logByteIdentical':True,
                'observed':'363 passed, 0 failed, syntheticTcbInputs true'}],
   'negativeControl':('The identical harness run against frozen v11 yields security exit 1 and workflows exit 1 with '
     '{"sourcePinsValid": false, "changedOrMissing": ["docs/coop/design-corrections/correction-crosswalk.proposed.json"]} '
     'and checksExecuted false, reproducing the completed v11 finding exactly.'),
   'declaredSummaryAgreement':('validation-summary.v1.json records foundation 1115 = 231+767+24+28+65, security 456 + 10 sweeps, '
     'native 151, workflows 1290, integration 363. Every one of these matches the values this reviewer measured from the '
     're-executed commands.'),
   'pinAudit':{'ledgers':4,'pinsChecked':1308,'perLedger':{'foundation':1099,'security':73,'workflows':65,'native':71},
     'stale':0,'missing':0,
     'positiveControl':('The same auditor run against frozen v11 reports exactly 2 stale pins - security and workflows both '
       'pinning correction-crosswalk.proposed.json at 9560a51e (its frozen v10 digest) against an observed ae78c7e6 - '
       'which is precisely the completed v11 finding, so the zero-stale result on v12 is not vacuous.')},
   'fixtureProvenance':('integration-fixtures.py declares Source: foundation/check-identity.py SHA256 f9b427a8..., which equals the '
     'actual applied checker digest. The fixture is itself transitively pinned at cfd85e86... identically in all four ledgers. '
     'It self-declares as synthetic shared construction from which no verdict is derived; this reviewer treats it as corroboration '
     'of declared provenance only and NOT as an independent oracle.')},
 'priorFindingDispositions':{
  'v11-M1':{'severity':'MUST','disposition':'RESOLVED','independentlyVerified':True,
    'finding':('Two of the six declared reference commands did not pass on the frozen v11 bytes: the security and workflows pin '
      'ledgers still carried the v10 digest of correction-crosswalk.proposed.json, which the final recording step rewrote after '
      'the pins were refreshed and after the commands were run.'),
    'howVerified':("Reproduced from the frozen bytes rather than accepted from the root's sequencing assertion, as required. "
      "(1) Full audit of all 1,308 pins across the four ledgers against the frozen v12 bytes: 0 stale, 0 missing; the two "
      "previously stale entries now read 556879f7... which equals the actual frozen digest of correction-crosswalk.proposed.json. "
      "(2) All six declared commands re-executed in a disposable full-subject copy: all exit 0 and every report and log is "
      "byte-identical to the frozen one. (3) Both tools proven discriminating against frozen v11, where they reproduce exactly "
      "the two stale pins and the two exit-1 failures. The frozen bytes are therefore self-reproducing regardless of the order "
      "in which they were produced, which is the stronger and order-independent test."),
    'sequencingAssertionNotReliedOn':("The root asserts that in v12 all pinned record edits precede pin refresh and command "
      "execution. This reviewer did not accept that assertion as evidence. The outcome test - every pin valid on the FINAL frozen "
      "bytes and every report regenerating byte-identically FROM those bytes - is what was verified, and it holds irrespective of "
      "the pipeline order. Independently, a field-level comparison of the updated crosswalk shows the only fields that changed "
      "across v11->v12 are historicalReviews and latestCompletedReview."),
    'historicalEvidencePreserved':("The earlier PASS reports remain in the frozen tree as historical records of an earlier working "
      "state, and the root's own error account is disclosed separately in "
      "reviews/codex-post-reset.v1/post-freeze-pin-drift.v11/account.json with a read-only recheck showing 2 mismatches of 1,308. "
      "This reviewer independently reproduced that recheck.")},
  'v11-S1':{'severity':'SHOULD','disposition':'RESOLVED','independentlyVerified':True,
    'finding':('validation-summary.v1.json still recorded claudeFinalReview "PENDING-FROZEN-V10" in the frozen v11 candidate, '
      'misstating which frozen candidate awaits final independent review.'),
    'howVerified':("Direct inspection of the frozen v12 bytes: claudeFinalReview now reads PENDING-FROZEN-V12 and the sibling "
      "claudePriorReview reads reviews/post-reset-review.v11/review.json, with priorReviewLimitation rewritten to the v11 outcome. "
      "The field correctly names the candidate this very review is against, and the label advances V10->V12 rather than to a stale "
      "V11, which is right because the v11 review is complete. The change is a same-length substitution, independently confirmed "
      "as one of the seven +0-byte changes in the recomputed delta.")}},
 'priorAdvisoryDispositions':{
  'v11-A1':{'severity':'ADVISORY','severityPreserved':True,'disposition':'CORRECTED-AND-INDEPENDENTLY-CONFIRMED',
    'finding':("The two annotation-deduplication sites used different equality notions: record() used typed equality while walk()'s "
      "inherited/chain filter used Python ==, so ordinal=1 and ordinal=true were collapsed before typed conflict checking."),
    'howVerified':("Independently constructed probe - this reviewer's own document shapes, own typed-distinct pair table and own "
      "oracle - run against BOTH the frozen v11 and frozen v12 models. 7 location classes (direct property + alias, two-step alias "
      "chain, nullable oneOf branch, enclosing object container, container $ref overlay, same-path double arrival, and array-items "
      "container) x 6 typed-distinct pairs (1/true, 0/false, object, array, deep nested, depth-3 mixed) x 2 orientations = 84 cases. "
      "Under frozen v12 ALL 84 refuse with RELATION_DIGEST_ANNOTATION_CONFLICT in BOTH orientations and BOTH annotations survive "
      "collection (2 survivors in all 84). Under frozen v11, 48 of the 84 wrongly ADMITTED with exactly 1 surviving annotation - "
      "the collapse - across 4 location classes. 42 identical-annotation positive controls ADMIT under v12, so typed-equal controls "
      "remain usable and the fix does not over-reject. The array-items-container class is one this reviewer invented and is NOT in "
      "the authored matrix, so the correction generalises beyond the cases its author tested."),
    'sourceCompleteness':("All four annotation comparison/dedup sites in identity-model.py now route through the single helper "
      "annotation_already_collected, which is C.equal_typed: the same-path merge (line 364), the inherited collection (376), the "
      "$ref-chain contribution filter (381) and the conflict limb's distinct list (486). governed_form only concatenates "
      "annotations and performs no equality comparison, so it cannot collapse a pair. No residual Python-equality annotation "
      "comparison remains."),
    'implementsAgreedRule':("This implements the already-agreed v11 normative typed-equality rule. It introduces no new annotation "
      "schema restriction and no new normative feature: the registered relation document, digest law and registry are canonically "
      "byte-identical across the delta, and all 13 relation closure rows and the coverage sweep are unchanged."),
    'boundedScope':("Confirmed to be a hypothetical registered-schema/reference consistency probe, not an attack on current closed "
      "Run payloads: no annotation value in the registered relation document is numeric or boolean, so no such pair can be written "
      "today.")},
  'v11-A2':{'severity':'ADVISORY','severityPreserved':True,'disposition':'EXPLICITLY-ACCOUNTED-NOT-SUBSTANTIVELY-CORRECTED',
    'finding':"The identity suite's reported check count includes duplicate check ids.",
    'howVerified':("Independently recounted from the frozen identity-report.json of both candidates. Frozen v12: 767 passing calls, "
      "757 distinct ids, 10 extra instances from exactly two parameterised ids - closed-closure (6) and exact-version-closure (6). "
      "Frozen v11: 673 calls, 663 distinct, the same 2 ids and same 10 extra instances. All instances of each duplicated id agree, "
      "so no failure can be masked. Set comparison of check ids confirms ZERO historic ids were renamed or dropped: v12's id set is "
      "a strict superset of v11's, adding 94 new ids. These figures match the subject's own identity-check-counts.v12.json exactly."),
    'standing':("The duplication itself is NOT corrected - the advisory's suggestion to parameterise the ids was not adopted. It is "
      "instead measured and disclosed honestly in a dedicated artifact. That is a legitimate response to a non-blocking advisory and "
      "this reviewer does not escalate it; it remains a carried open advisory, and a related new non-blocking advisory (v12-A1) is "
      "raised about where that disclosure lives.")},
  'v11-A3':{'severity':'ADVISORY','severityPreserved':True,'disposition':'CORRECTED-AND-INDEPENDENTLY-CONFIRMED',
    'finding':("The inserted prose told a blind implementer to follow local references but did not state that the traversal must "
      "terminate on a cyclic $defs reference."),
    'howVerified':("Inspected the ACTUAL final insertion and the actual custody chain rather than substring similarity with earlier "
      "draft notes. The single added sentence is 'Following local references must terminate even when a local definition is cyclic.' "
      "- exactly 81 bytes, sha256 7375c21035ed4c3f0aba9c229a702249422d73dd76365ad8bcc1f5099cef10da, matching the declared value. "
      "This reviewer recomputed the replaced and replacement blocks from the frozen bytes: v11 lines 582-586 are 409 bytes hashing "
      "to c6c61d289308a079a1ccdab4e22f68552a3ba5b13f288f47aa8840fe9163c9da and the v12 replacement is 491 bytes hashing to "
      "79c9484979ddd1534bd26a1d77b374c5e91b5eb12e9f2751d07feab6532ed315 - both byte-exactly the blocks recorded in the actual "
      "bounded Claude assessment (assessment.json, sha256 2ed0b757...) and in the root custody "
      "(cycle-normative-clarification.v12/custody.json). Whitespace-normalised comparison of the whole 83KB contract proves the rest "
      "of the document is identical after removing that one sentence, so the only other effect is the explicitly assessed local "
      "rewrap including the pre-existing 105-column line. Net +82 bytes."),
    'provenance':("The bounded coauthor read Codex's 52-byte proposed insert ('Local-reference traversal must terminate on cycles.') "
      "and proposed a clearer alternative; the applied text is byte-identical to that assessed refinement block, not a paraphrase "
      "of it. The assessment explicitly records agrees=true, refinementIsBlocking=false, sourcesEdited=[] and suitesRun=[], and "
      "states it did not claim to read a completed independent verdict."),
    'statesExistingRobustnessNotNewFeature':("Independently confirmed behavioural: this reviewer's own cycle controls show a "
      "self-referential container terminates and refuses when unannotated, admits when annotated, and that mutually recursive defs "
      "and an alias-only cycle both terminate. Both chain guards ('target not in chain') are per-reference-path. No new schema "
      "feature, admission verdict, algorithm or complexity bound is introduced, and no admission outcome changes.")}},
 'newMustIssues':[],
 'newShouldIssues':[],
 'newAdvisories':[
  {'id':'v12-A1','severity':'ADVISORY',
   'title':("validation-summary.v1.json reports the identity component as 767 without cross-referencing the distinct-id "
     "measurement (757) that the subject records in a sibling artifact"),
   'observed':("validation-summary.v1.json is the designated reference-evidence summary and records foundation.components.identity "
     "= 767 and checksPassed = 1115. 767 is the honest count of passing CHECK CALLS; the count of distinct check ids is 757, "
     "measured by the subject itself in reviews/codex-post-reset.v1/identity-check-counts.v12.json and independently reconfirmed "
     "here. The summary does not name or link that artifact, so a downstream reader of the summary alone sees only the call count."),
   'whyNonBlocking':("Nothing is misstated: the field counts passing checks and every instance genuinely passed, and the subject "
     "does disclose the distinction explicitly in a dedicated file whose standing sentence says neither number is a coverage or "
     "acceptance claim. No verdict, count or behaviour depends on it, and the duplicate ids are pre-existing and agreeing."),
   'relationTo':'continues the standing caution restated in v10-A3 and v11-A2 that a check-count is not a coverage measure',
   'suggestion':("when the summary is next edited, carry the distinct-id figure or a link to identity-check-counts.v12.json "
     "alongside the call count, so the reference summary is self-contained for a reader who does not open the sibling artifact"),
   'noPatchProposed':True},
  {'id':'v12-A2','severity':'ADVISORY',
   'title':("the recorded reference commands embed absolute live-repository paths, so reproducing them from the frozen snapshot "
     "alone requires rewriting the command, even though the checkers themselves are relocatable"),
   'observed':("reference-checks.json records each of the six commands with an absolute interpreter path and an absolute script "
     "path under /Users/sb/code/opensip-ai/opensip_arch/..., while the --report argument is snapshot-relative. The frozen snapshot "
     "root is /tmp/opensip-design-corrections/candidate-subject.v12, so the recorded command as literally written would execute the "
     "LIVE repository's checker, not the frozen one. This reviewer had to substitute the copy's own script paths to reproduce "
     "against the frozen bytes."),
   'whyNonBlocking':("It did not impede reproduction and indicates no defect in the evidence. The checkers resolve their root from "
     "Path(__file__).resolve().parents[3] rather than from the working directory, so running the copy's own scripts is fully "
     "self-contained; all six commands then reproduce byte-identically. The recorded sourceSha256 for each command also pins the "
     "checker independently of its path, so the intended script is unambiguous."),
   'suggestion':("record the script path snapshot-relative alongside the pinned sourceSha256, so the declared command is executable "
     "against a frozen snapshot without editing - relevant to the later blind and application gates, which consume frozen kits"),
   'noPatchProposed':True}],
 'carriedAdvisoryAccount':{
   'declaredCount':31,'verifiedCount':31,
   'path':'reviews/codex-post-reset.v1/advisory-application-account.v12.proposed.json',
   'ids':['ADV-1(v5)','ADV-2(v5)','ADV-3(v5)','ADV-4(v5)','ADV-5(v5)','NEW-ADV-1(v6)','NEW-ADV-2(v6)','NEW-ADV-3(v6)',
     'V7-ADV-1','V7-ADV-2','V7-ADV-3','v8-A1','v8-A2','v8-A3','v9-A1','v9-A2','v9-A3','v9-A4','v9-A5','v9-A6','v9-A7',
     'v9-A8','v9-A9','v9-A10','v9-A11','v10-A1','v10-A2','v10-A3','v11-A1','v11-A2','v11-A3'],
   'preservation':("All 31 carried v5..v11 advisories are explicitly present with their ORIGINAL ids and original severities; none "
     "was silently upgraded, downgraded, merged or dropped. Independently enumerated from the frozen account file. v11-A1 in "
     "particular retains ADVISORY severity despite being substantively corrected."),
   'stillOpenInSubstance':['v11-A2'],
   'newlyAdded':['v12-A1','v12-A2']},
 'arDispositions':arD,
 'fwDispositions':fwD,
 'inheritedResidualDispositions':inhD,
 'scopedReviewOwnerDispositions':scoped,
 'productQualificationGates':{'count':32,'demonstrated':0,'qualified':0,'implementationHarnessAuthored':0,
   'platformFamilies':['linux-x86_64-gnu','linux-aarch64-gnu','macos-aarch64','macos-x86_64'],
   'basis':("Independently enumerated from qualification-gates.proposed.json in the frozen v12 bytes: all 32 items carry "
     "demonstrated=false, qualified=false and implementationHarnessAuthored=false. Zero gates are true on any of the three boolean "
     "fields. This review demonstrates and qualifies none of them and does not extend any historical preview grade."),
   'disposition':'ALL-32-REMAIN-UNDEMONSTRATED'},
 'evaluationSubresiduals':{'count':30,'disposition':'CARRIED-UNCHANGED',
   'ids':json.load(open(os.path.join(P,'eval-ids.json'))),
   'basis':("evaluation-residual-dispositions.proposed.json is not in the recomputed v11->v12 changed set and is therefore "
     "byte-identical to frozen v11; independently recounted as 30 items. None is closed or graded by this review.")},
 'normativeProseAssessment':{
   'verdict':'ACCURATE-AND-SUFFICIENT-FOR-A-BLIND-IMPLEMENTER',
   'method':("Each normative sentence was treated as a falsifiable claim and tested against the reference implementation with this "
     "reviewer's own constructed documents - 14 targeted cases - rather than assessed by reading. All 14 hold."),
   'refusalConditionsNamed':("All six refusal causes the implementation can raise are derivable from the prose: missing annotations "
     "(RELATION_DIGEST_UNANNOTATED), conflicting annotations (RELATION_DIGEST_ANNOTATION_CONFLICT), undeclared retention values "
     "(RELATION_DIGEST_RETENTION), unaddressable claimed joins (RELATION_DIGEST_UNJOINABLE_LOCATION), missing joins "
     "(RELATION_DIGEST_LAW_RESIDUE) and joins naming absent fields (RELATION_JOIN_FIELD_UNKNOWN). The closing sentence enumerates "
     "all six explicitly."),
   'propertiesNamedAndIndependentlyConfirmed':{
     'annotationInheritance':'stated and confirmed: occurrence, enclosing schema path or intermediate alias applies',
     'terminalScalarExclusion':("stated and confirmed behaviourally: annotating the shared terminal DigestHex $def does NOT "
       "blanket-exempt an unannotated governed occurrence, which still refuses"),
     'branchOccurrenceIsolation':("stated and confirmed in BOTH branch orders: an annotated alternative does not cover an "
       "unannotated alternative, while a parent annotation does cover each alternative it encloses"),
     'monotonicMissingness':("stated and confirmed in both visit orders, including a third ANNOTATED sighting arriving after a "
       "missing one, which still refuses - the previous v11 same-path missingness fix is intact"),
     'orderIndependence':("stated and confirmed: all 6 permutations of the object keys of a probe node yield a single identical "
       "outcome"),
     'conflictRefusalAndTypedEquality':("stated and confirmed: distinct annotations conflict, and annotations equal under typed "
       "canonical equality do not"),
     'topLevelJoinAddressing':("stated and confirmed: a nested object member cannot be joined and must declare not-joined; a scalar "
       "alternative of a top-level property preserves the join address and admits"),
     'cycleTermination':'newly stated and confirmed across self, mutual and alias-only cycles',
     'directNonGovernedAnnotations':("the prose refers explicitly to top-level SELECTOR PROPERTIES, and this is exactly what the "
       "implementation does: file.byteLength refs UInt64 and is non-governed, yet being a directly annotated top-level property it "
       "is still subject to retention and join checks - an invalid retention on it refuses with RELATION_DIGEST_RETENTION and a "
       "joined retention without its join refuses with RELATION_DIGEST_LAW_RESIDUE - while an annotated NON-top-level non-governed "
       "member is correctly not dragged in and admits")},
   'exemptionReasonsAreAuthoringDisclosure':("Confirmed exactly as the prose states: admission validates the DECLARED RETENTION, "
     "not the presence or content of the reason prose. An annotation declaring retention not-joined with the reason key absent, and "
     "one with an empty reason string, both ADMIT. No new reason key is invented: the law's retention vocabulary is exactly "
     "{not-joined, preimage, provider-output-retained, snapshot-inventoried}."),
   'blindInputCompleteness':("A blind implementer can derive the traversal surface, the effective-annotation rule, the three limbs, "
     "the typed-equality notion, order independence, monotonic missingness, join addressability and every refusal condition from "
     "the prose WITHOUT reading the author's Python. This reviewer found no silent gap in the claimed language."),
   'noArbitraryFutureFeatureDemanded':("This review demands no schema-language feature beyond declared support. The prose accurately "
     "states existing boundaries; it does not promise capability the reference lacks.")},
 'deltaProvenance':{
   'coauthorTwoFileDelta':("The two changed reference-source files are byte-identical to the retained released coauthor images: "
     "digest-corrections-author.v10/author-source/.../identity-model.py == the applied file at "
     "ed38f172291a30c590e6a424794f345802892c27e455ff682df7e8f5599a0fcd, and .../check-identity.py == the applied file at "
     "f9b427a8671da7dcf761ad0de7037334c30cac1128bc457661de13b6648f21f5. The retained BEFORE images are byte-identical to the frozen "
     "v11 files (de3ae06b... and 90a3b590...). Handoff sha256 74de34c5... and assessment sha256 2ed0b757... both verified. "
     "The exact released two-file delta was therefore applied, and nothing else in those two paths."),
   'orderingOfApplication':("The subject states the released delta was applied only after BOTH the completed independent v11 review "
     "and the coauthor pass finished. This reviewer verified the checkable part - that the applied bytes equal the released images "
     "and that the before-images equal frozen v11 - and does not rely on the ordering narrative for its verdict."),
   'cycleWordingCustody':'exact 409-byte before block and 491-byte after block recomputed from the frozen bytes and matched',
   'failedAttemptsPreserved':("The completed v11 review's failed p12 whole-suite sys.settrace reachability attempt is preserved "
     "literally in the frozen v12 tree: logs/p12-reachability.json is a ZERO-BYTE file, exactly as 'no result' should look, with "
     "the driver and probe retained. The v11 review itself records that it exceeded the 600-second foreground wait, was moved to "
     "the background and was terminated by its reviewer with exit 144 and no result. The subsequent explicit disposable "
     "instrumentation p12b independently produced completed reachability evidence (v11 mergeBranch executions 16 vs v10 zero, "
     "1355 record calls) with both suites exiting 0. The technical review restates this distinction and does not present the "
     "incomplete trace as passing evidence. This reviewer confirms the literal failed attempt and its actual limits are preserved, "
     "and reproduced none of it as success."),
   'priorHarnessSelfCorrectionsPreserved':("The v11 review's four honest self-corrections (p08 null-branch, p17 synthetic identity "
     "inputs, p12 timeout, p16 DR-012 regex) are retained verbatim. This reviewer independently re-checked the p16 one: "
     "inherited-residuals.proposed.md contains DR-012 only in the sentence 'DR-012 remains release qualification', confirming the "
     "27-row register and the correctness of that self-correction.")},
 'preservationOfPreviouslyConfirmedBehaviour':{
   'method':("Preservation rests on three independent measurements rather than re-derivation of each behaviour: (1) the exact "
     "recomputed delta shows only 2 reference-source files and 1 normative prose file changed, with ZERO registered schema or "
     "registry bytes changed; (2) every check id present in frozen v11 is still present in frozen v12 and still passes - the id set "
     "is a strict superset, adding 94 and renaming or dropping none, with failed=0 in both; (3) 21,562 identity computations over "
     "17 domains (5,370 distinct) harvested under both frozen models are multiset-identical."),
   'registeredArtifactsCanonicallyIdentical':['all 5 foundation schema JSON files','the registered relation document',
     'x-opensip-digest-law','x-opensip-relation-registry','all 13 relation closure rows','the coverage sweep'],
   'targetedProbesWhereUncertaintyWarranted':{
     '39 injections across 13 selectors':("independently re-run: 13 relations x 3 governed forms = 39, ALL refuse with "
       "RELATION_DIGEST_UNANNOTATED and none admits; the positive control shows all 39 ADMIT once annotated, so the refusal is "
       "caused by the missing annotation and by nothing else about injecting a field"),
     'exact inline patterns, referenced containers, nested/array and cyclic shapes':("all 8 shapes - ref, inline, nullable, aliased, "
       "nested, array, container-ref and cyclic-container-ref - refuse when unannotated and admit when annotated, preserving the "
       "earlier Codex traversal/alias/inherited-limb counterexamples"),
     'three law limbs on the same effective annotations':("independently confirmed for field, alias-definition AND nullable-branch "
       "placements: unannotated governed field -> RELATION_DIGEST_UNANNOTATED; annotated field without join -> "
       "RELATION_DIGEST_LAW_RESIDUE; join naming a missing field -> RELATION_JOIN_FIELD_UNKNOWN; invalid retention refuses with "
       "RELATION_DIGEST_RETENTION"),
     'RELATION_DIGEST_UNANNOTATED intended cause':("verified as the intended cause with the exact selector text "
       "'RELATION_DIGEST_UNANNOTATED:file:file.strayGoverned:DigestHex' naming relation, field and form"),
     'third annotated sighting after missing':'refuses; monotonic missingness holds and the v11 same-path fix is intact',
     'all-lawful annotations still admitted':'identical annotations on both arrivals admit; all 13 registered relations admit',
     'byteLength distinction':("independently distinguished as required: file.byteLength is annotated but refs UInt64 and is "
       "NON-governed, appearing as an ungoverned sighting with form None. REMOVING its annotation ADMITS - it does not require "
       "third-limb refusal - whereas removing the annotation from any of the 7 governed digest/path fields "
       "(clones.bodyIdentity, clones.normalisationVersion, file.path, file.contentSha256, package.manifestPath, vcs-change.path, "
       "vcs-change.previousPath) refuses with RELATION_DIGEST_UNANNOTATED. The coverage sweep counts exactly 7 governed fields "
       "(file 2, package 1, vcs-change 2, clones 2) and does not count byteLength."),
     'previousPath not-joined exemption':("preserved verbatim with representation snapshot-path, retention not-joined, authority "
       "vcs-observation and its stated reason about the pre-rename path naming a state before the analysed snapshot"),
     '13 closed selectors remain coherent':'all 13 registered relations admit and their closure rows are canonically unchanged'},
   'carriedBehavioursNotIndividuallyReDerived':("The full carried list - owning-snapshot file hash/length/path joins and memo owner "
     "context, file@enumerated coverage without an invented resolved rung, 13 registered full-schema-document relations and typed "
     "arrays, CVE1 all four gates, nativeCoverage producer admission, Plan enumerator membership, complete TypeScript+Rust Run "
     "closure, TS node_modules/config/layout/ordered repeats/extends/custom config/jsconfig, raw32 compiler/dialect clone body "
     "version, actual JS body language via the TS engine, retained L0 grammar/source recomputation versus L1-L3 custody/framing "
     "only, Rust target edition/shared physical source explicit selection/# markers/max bounds/derived unit identity, stable body "
     "IDs under unrelated ownership, partial/absent ownership cannot claim complete empty clone Coverage, honest partial and "
     "healthy empty controls, cache lookup versus validated hit, generic mutation versus repair replay, public purge disclosure, "
     "required output failure/committed Run preservation, and complete leased pin ledger comparison versus pure projection - is "
     "asserted by named check ids in the identity and unit suites. Every one of those ids is present and passing in frozen v12, "
     "the suites reproduce byte-identically, and the computed identity multiset is unchanged. This reviewer did not re-derive each "
     "behaviour from first principles and says so plainly."),
   'canonicalRecordsPreserved':("The 723-byte example remains the canonical wrapped edition record with the bare map at 711; suffix "
     "choices remain conservative; the fixture-level spec is not a qualified FACT-IDENTITY asset; absence of clone facts does not "
     "exempt Coverage prerequisites; multiple contexts per language remain allowed with owning-universe joins. These are carried on "
     "the byte-identity of their governing files across the delta, not re-litigated here."),
   'syntheticTcbUnchanged':("All native, OS, compiler, crypto and storage observations remain synthetic TCB assumptions. The "
     "integration report itself declares syntheticTcbInputs true. Nothing was measured on a real toolchain and no platform is "
     "qualified.")},
 'independentProbes':[
  {'id':'cx-p01','name':'subject custody before/after','script':'probes/verify_subject.py',
   'result':'2981/2981 verified, 0 mismatches, 0 undeclared, 0 missing; before and after reports identical'},
  {'id':'cx-p02','name':'exact v11->v12 delta','script':'probes/diff_v11_v12.py',
   'result':'16 changed, 195 added, 0 removed; v11 snapshot itself re-verified at 2786 files, 0 mismatches'},
  {'id':'cx-p03','name':'all-ledger pin audit','script':'probes/pin_audit.py',
   'result':'1308 pins (1099/73/65/71), 0 stale, 0 missing on frozen v12'},
  {'id':'cx-p03c','name':'pin audit positive control on frozen v11','script':'probes/pin_audit_v11_control.py',
   'result':'exactly 2 stale pins reproduced with exact hashes, proving the auditor discriminates'},
  {'id':'cx-p04','name':'six reference commands in a disposable full-subject copy','script':'probes/sixrun/',
   'result':'all six exit 0; all reports and logs byte-identical to frozen'},
  {'id':'cx-p04c','name':'six-command negative control on frozen v11','script':'probes/sixrun-v11-control/',
   'result':'security and workflows exit 1 with sourcePinsValid false, reproducing the v11 finding'},
  {'id':'cx-p05','name':'typed-equality probe, own shapes, both models','script':'probes/typed_equality_probe.py',
   'result':('84 conflict cases: v12 refuses all 84 with 2 survivors each; v11 wrongly admits 48 with 1 survivor across 4 location '
     'classes; 42 identical-annotation positive controls admit under v12')},
  {'id':'cx-p06','name':'law limbs, missingness, exemptions, cycles','script':'probes/law_limbs_probe.py',
   'result':'18/18 cases as expected, after two self-corrections recorded below'},
  {'id':'cx-p07','name':'39-injection sweep and byteLength distinction','script':'probes/injection_probe.py',
   'result':'39/39 refuse unannotated and 39/39 admit annotated; 8/8 shapes; byteLength strip admits; 7 governed strips refuse'},
  {'id':'cx-p08','name':'normative prose claims as falsifiable tests','script':'probes/prose_claims_probe.py',
   'result':'14/14 prose claims hold'},
  {'id':'cx-p09','name':'registered-artifact and closure stability','script':'probes/identity_stability.py',
   'result':'schemas, relation document, law, registry, 13 closure rows and coverage all canonically identical across the delta'},
  {'id':'cx-p10','name':'identity harvest under both models','script':'probes/body_identity_probe2.py',
   'result':'21,562 calls, 5,370 distinct, 17 domains, multiset digests identical; both suites exit 0 (673 and 767, failed 0)'},
  {'id':'cx-p11','name':'duplicate check-id recount','script':'inline',
   'result':'v12 767/757/10 and v11 673/663/10, same 2 ids, all agreeing, zero historic ids renamed or dropped'},
  {'id':'cx-p12','name':'cycle-wording block custody','script':'inline',
   'result':'409-byte before and 491-byte after blocks recomputed and matched byte-exactly; 81-byte sentence sha matched'},
  {'id':'cx-p13','name':'crosswalk row comparison','script':'inline',
   'result':'16 rows both sides, ids identical, ONLY historicalReviews and latestCompletedReview differ; AR-15 status unchanged'}],
 'harnessErrorsCorrectedNotCountedAsDefects':[
  {'probe':'cx-p06','error':("my first law-limb run caught C.AdmissionError from a canonical module I had injected as 'canonical', "
     "but identity-model.py binds its OWN canonical module instance, so the exception class did not match and the probe crashed "
     "instead of classifying the refusal"),
   'correction':("re-bound the probe to the model's own C (M.C) so exception identity matches. Not a subject defect - the model "
     "raised exactly the right error, my catch was wrong.")},
  {'probe':'cx-p06','error':("four of my cases used retention='retained-blob', a value I invented. They refused with "
     "RELATION_DIGEST_RETENTION before reaching the limb I was testing, which was the model behaving correctly"),
   'correction':("re-ran with the lawful vocabulary value 'preimage'; all 18 cases then behaved as expected. My invented value was "
     "the error, not the subject's handling of it.")},
  {'probe':'cx-p10 (first attempt)','error':("my first identity harvest monkeypatched identifier() on a model object I had loaded, "
     "but check-identity.py loads its own model instance, so nothing was captured. It reported 0 identities with the sha256 of the "
     "empty string for both candidates - a vacuously 'identical' result"),
   'correction':("discarded that result rather than reporting it as stability evidence, and replaced it with source-level "
     "instrumentation of identifier() inside disposable copies of each frozen tree, which captured 21,562 real computations per "
     "candidate. The vacuous first result is disclosed here and is not used as evidence anywhere in this review.")}],
 'limitations':[
  ("This is independent DESIGN and REFERENCE acceptance only. It is not reconstructability, not readiness, not application "
   "acceptance and not product qualification."),
  ("No product implementation, commit, push, source edit, reset or clean was performed. Every write was confined to "
   "/tmp/opensip-design-corrections/post-reset-review.v12, including all disposable copies and probes."),
  ("Reports were regenerated only inside disposable copies, never inside the frozen subject and never inside the original "
   "repository; both were re-verified unmodified afterwards."),
  ("All native, OS, compiler, crypto and storage observations remain synthetic TCB assumptions. Nothing was measured on real "
   "toolchains and no platform is qualified."),
  ("The integration fixture's synthetic shared construction is NOT an independent oracle. I verified only that its declared source "
   "hash equals the applied checker and that it is transitively pinned; agreement between it and the checker is shared "
   "construction, not corroboration."),
  ("I did not re-derive every previously confirmed behaviour from first principles. Their preservation rests on the exact delta, "
   "the byte-identical suite reproduction, the superset-and-passing check-id set and the identical identity multiset, as stated."),
  ("I verified that the applied bytes equal the released coauthor images and the before-images equal frozen v11. I did not and "
   "cannot verify from bytes alone the wall-clock ORDER in which the root performed its steps, and my verdict does not depend on "
   "that ordering narrative."),
  ("The root's prospective /tmp application and finalizer tooling is outside this frozen design and was not reviewed; the final "
   "application review is a later separate gate."),
  ("Termination of local-reference traversal is confirmed; no work-complexity bound is claimed."),
  ("No subagents were used. No Codex assent, no blind consumer pass and no application review is performed or implied."),
  ("I authored none of the subject bytes and am neither the coauthor session 5dec928a nor the prior reviewer session cd236691.")],
 'claimsExplicitlyNotMade':[
  'no readiness change','no implementation authorization','no product qualification','no application acceptance',
  'no blind consumer acceptance','no Codex assent','no reconstructability claim',
  'no historical preview grade is extended and no self-hash review cycle is invented',
  'no qualification gate is demonstrated','no AR or FW obligation is demonstrated or satisfied',
  'no inherited residual or scoped review owner is closed, and no historical acceptance is re-opened',
  'no current payload or Run exploit is asserted - the annotation work is hypothetical registered-schema/reference consistency'],
 'requiredNextActs':[
  'actual Codex assent to these exact frozen bytes, carrying all 31 prior advisories plus v12-A1 and v12-A2',
  'a NEW fresh blind consumer B v3 on the accepted normative subset',
  'a complete, independently reviewed application, then readiness verification'],
 'readinessChanged':False,'implementationAuthorized':False,'productQualification':False,
 'applicationAccepted':False,'blindAccepted':False}
os.makedirs(OUT,exist_ok=True)
open(os.path.join(OUT,'review.json'),'w').write(json.dumps(review,indent=1)+'\n')
print('wrote review.json',os.path.getsize(os.path.join(OUT,'review.json')),'bytes')
print('verdict',review['overallVerdict'],'| newMust',len(review['newMustIssues']),'| newShould',len(review['newShouldIssues']),
      '| newAdvisories',len(review['newAdvisories']))
print('ar',len(review['arDispositions']),'fw',len(review['fwDispositions']),
      'inherited',len(review['inheritedResidualDispositions']),'scoped',len(review['scopedReviewOwnerDispositions']))

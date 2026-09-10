import hashlib, json
from pathlib import Path

S = Path('/tmp/opensip-design-corrections/v14-advisory-clarification.v1')
REPO = Path('/Users/sb/code/opensip-ai/opensip_arch')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
insp = json.loads((S / 'inspection.json').read_text())
prop = json.loads((S / 'proposal.json').read_text())
ch = {c['id']: c for c in prop['changes']}

doc = {
 'artifact': 'v14-advisory-clarification-assessment',
 'version': 'v1',
 'assessor': ('actual Claude COAUTHOR of the integrated v4 source, not an independent reviewer. '
   'I authored the bytes that V14-ADV-1 before-file contains; V14-ADV-2 file is not mine. This is a '
   'technical assessment of two root-proposed wording corrections, not a review verdict.'),
 'date': '2026-09-07',
 'proposalSha256': sha(S / 'proposal.json'),
 'reviewSha256': sha('/tmp/opensip-design-corrections/post-reset-review.v14/review.json'),
 'reviewVerdictRead': {'overallVerdict': 'ACCEPT', 'newMustIssues': 0, 'newShouldIssues': 0,
   'newAdvisories': 2, 'severityPreserved': 'both remain ADVISORY; nothing here raises or lowers them'},

 'technicalAssent': False,
 'assentSummary': ('Assent to V14-ADV-2 exactly as proposed. NO assent to V14-ADV-1 as written: its '
   'substance is right and its cross-reference is wrong. Both statements it reconciles are in '
   'SECTION 10; section 13 is "Joins (closed; current spellings, no future owner choices)" and '
   'mentions no DomainDetailCode at all. Integrating the proposed string would put a false '
   'cross-reference into normative prose - the same staleness class both advisories exist to remove. '
   'A precise alternative differing in four words is supplied with its exact hash.'),
 'perChangeAssent': {'V14-ADV-1': False, 'V14-ADV-2': True},

 'hashVerification': {
   'method': ('Every declared hash recomputed from the actual bytes; each old string counted in the '
     'before file; each change applied mechanically and compared to the proposed bytes.'),
   'rows': insp['hashVerification'],
   'allDeclaredHashesCorrect': True,
   'liveRepositoryMatchesBeforeForBoth': True,
   'eachChangeIsExactlyOneHunkAndOneOccurrence': True},

 'changes': [
  {'id': 'V14-ADV-1',
   'path': ch['V14-ADV-1']['path'],
   'beforeSha256': ch['V14-ADV-1']['beforeSha256'],
   'proposedSha256': ch['V14-ADV-1']['proposedSha256'],
   'assent': False,
   'advisorySubstanceAgreed': True,
   'substantiveRationale': {
     'theAdvisoryIsReal': ('Verified in the owning law, not accepted from the review. The section-10 '
       'paragraph is entirely about how a LAWFUL entry deficiency and cause reach the public surface '
       '- deficiency projects as an existing closed DomainDetailCode, cause travels as typed detail '
       'in the coverage2 record - and for that route no code is added. The sentence "No new public '
       'code is added and none is needed" carries no scope in its own text, while four members are '
       'added ~109 lines later for REFUSAL branches, one of them named for the Coverage-cause route '
       'the same paragraph discusses. Scoping the sentence is correct and adds no behaviour.'),
     'whyTheProposedTextIsWrong': ('It says "The refusal branches in section 13". Measured in BOTH '
       'the live integrated file and the frozen v14 file: the unqualified sentence is at line 2267 '
       'and the four-codes paragraph at line 2376, and BOTH are inside "## 10. Deficiencies, '
       'precedence and D9 mapping" (lines 2140-2537). "## 13. Joins (closed; current spellings, no '
       'future owner choices)" begins at line 2750 and contains no occurrence of DomainDetailCode. '
       'The public detail registry corroborates independently: the selector on all four added '
       'records names "native-evidence.md section 10", never section 13. A reader following the new '
       'cross-reference would be sent to the joins section and find nothing.'),
     'whereTheErrorOriginated': ('Not root invention: the independent review V14-ADV-1 text itself '
       'says "section 13 of the same document adds four DomainDetailCode members" while its own '
       'selector cites lines 2376-2385, which are section 10. The proposal faithfully carried the '
       'review wording forward. The review verdict, its severity and its measured evidence '
       '(registry 283 -> 287, 0 removed) are unaffected; only the section label is wrong.'),
     'whatIsNotDisputed': ('The first proposed sentence - "No new public code is added for this '
       'projection of a lawful entry deficiency and cause" - is accurate and I assent to it. The '
       'closing clause "those additions do not change this projection" is also accurate: the four '
       'added codes serve refusal branches and none of them is the projection route for a lawful '
       'entry deficiency or cause.')},
   'preciseAlternative': {
     'old': ch['V14-ADV-1']['old'],
     'new': ("`nativeCause`-carried rows. No new public code is added for this projection of a "
       "lawful entry's deficiency and cause. The refusal branches later in this section separately "
       "add four public detail codes; those additions do not change this projection."),
     'differsFromRootProposalBy': '"in section 13" becomes "later in this section"; nothing else changes',
     'exactProposedFile': 'claude-alternative/docs/v2/contracts/product-v1/native-evidence.md',
     'alternativeSha256': insp['claudeAlternative']['sha256'],
     'whyThisWording': ('It is true of the current bytes, it stays true under renumbering, and it '
       'still gives a reader a direction. Naming the intervening sub-heading "Admission and event '
       'routes" would be more precise but that heading reads "(existing; unchanged rows)", which '
       'would import a second inaccuracy into the fix.'),
     'appliesCleanly': True,
     'addsNoFieldCodeOrTest': True,
     'altersNoAdmissionSemantics': True},
   'evidence': insp['adv1']},

  {'id': 'V14-ADV-2',
   'path': ch['V14-ADV-2']['path'],
   'beforeSha256': ch['V14-ADV-2']['beforeSha256'],
   'proposedSha256': ch['V14-ADV-2']['proposedSha256'],
   'assent': True,
   'substantiveRationale': {
     'everyFactualClaimVerifiedAtTheCallSites': {
       'anchorLawHasExactlyOneCallSite': ('identity-model.py: defined at 840, called at 939, and the '
         'only other occurrence (1081) is a comment. That call is inside relation_payload_rules '
         '(923), whose only call site is 755 - inside open_run_closure (566). close_run (561) '
         'delegates to open_run_closure, and admit_cache_entry (1484) reaches it too. So the '
         'reference model exhibits this law at retained Run closure, and nowhere else.'),
       'noProducerBoundaryCallSiteExists': ('Confirmed, and confirmed to be unavoidable: the native '
         'model defines no fact-anchor cardinality guard at all. This matters for the choice of '
         'repair - the review offered "narrow enforcedAt OR name the producer-boundary call site the '
         'way the cause registry names admit_coverage_result_v3", and the second option is not '
         'available, because there is no such function to name.'),
       'theOrderingClauseIsTrue': ('anchor_law runs at 939, before relation_source_joins - "the '
         'per-relation snapshot-join registry, enforced on EVERY owning fact" - is defined at 1003 '
         'and called at 957. Re-scoping that clause to "At retained Run closure" is accurate.'),
       'theAsymmetryTheReviewCitedIsReal': ('the deficiency-cause registry enforcedAt names '
         'native_evidence_model admit_coverage_result_v3 - the producer boundary - AND foundation '
         'close_run, and admit_coverage_result_v3 does exist.')},
     'itDoesNotWeakenProducerObligation': ('It strengthens the statement of it. The before text '
       'asserted as FACT that the law "is checked ... at the producer boundary", which the reference '
       'model does not exhibit. The proposed text makes it an explicit obligation - "The producer '
       'MUST enforce this law on every owning fact" - and keeps "on every owning fact" attached to '
       'that obligation rather than to the model exhibit. An obligation that is stated and unmet by '
       'a producer is now a conformance failure with a sentence to cite; before, a reader could '
       'believe the reference model already discharged it.'),
     'itDoesNotInventAProducerImplementation': ('It names no producer function, no call site and no '
       'new boundary; it says producer enforcement remains an implementation conformance obligation, '
       'which matches the review own whyNotAMustOrShould - the native producer is outside this '
       'reference model scope and its conformance is future qualification work.'),
     'itAddsNoFieldCodeOrTestAndAltersNoAdmissionSemantics': ('enforcedAt is a prose value inside '
       'x-opensip-relation-registry. No checker asserts on its text - the only live occurrences of '
       'the old sentence outside retained review archives are the file itself. The cardinality law, '
       'its three classes, the refusal FACT_ANCHOR_CARDINALITY and every admission path are '
       'untouched.')},
   'evidence': insp['adv2']}],

 'consequenceRootMustHandle': {
   'finding': ('relation-payload-schemas.v2.json is not merely prose-bearing: identity-model joins '
     'this document BY DIGEST at admission and refuses '
     'PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT on a mismatch. Changing the enforcedAt string moves '
     'the document digest from 629c2868c3c9e7961e009bc7352d2ca44fab5f75c22c08def3691e48aa92656e to '
     'ef0c244e7817e8bda6039ec66fc3180114f8e9997b3eacee4fe313c7f3d737b8.'),
   'whatThisDoesNotBreak': ('Nothing in the fixtures. check-identity computes '
     'RELATION_DOCUMENT_DIGEST from the file bytes rather than hardcoding it, so the reference cases '
     'follow the new bytes automatically. No retained fixture, no generated report and no checker '
     'carries the old digest as a literal.'),
   'whatItRequires': ('Four live pin manifests carry the old digest as a literal and must be '
     're-sealed at the successor freeze: foundation/source-pins.v1.json, '
     'workflows/source-pins.v1.json, native/source-pins.v2.json and security/source-pins.v1.json. '
     'That is ordinary freeze work and is root own; I changed nothing and re-pinned nothing.'),
   'sameConsiderationForAdv1': ('native-evidence.md is contract prose and is pinned the same way, '
     'but is not digest-joined at admission.')},

 'requiredFollowup': [
  {'id': 'FU-1', 'owner': 'root', 'blocking': True,
   'action': ('Do not integrate the V14-ADV-1 proposed bytes '
     '(f36942b53c6401bb35574071ba028d98110cf4a703453319455484708f6fade4). Use the supplied '
     'alternative instead, or any wording that does not send the reader to section 13. Exact '
     'alternative bytes and hash are in this directory; the change applies cleanly to the same '
     'before-file and is one hunk.'),
   'alternativeSha256': insp['claudeAlternative']['sha256']},
  {'id': 'FU-2', 'owner': 'root', 'blocking': False,
   'action': ('Record - without editing the frozen review artifact - that post-reset-review.v14 '
     'V14-ADV-1 mislabels the four-codes paragraph as section 13 when its own selector cites lines '
     '2376-2385 in section 10. The advisory stands; only its section label is wrong. A successor '
     'independent reviewer should not inherit the mislabel.')},
  {'id': 'FU-3', 'owner': 'root', 'blocking': True,
   'action': ('Re-seal the four pin manifests that carry the relation-payload-schemas.v2.json digest '
     'as a literal, and re-run the reference commands and regenerated reports at the successor '
     'freeze. The digest change is a consequence of V14-ADV-2 and is expected, not a defect.')},
  {'id': 'FU-4', 'owner': 'root', 'blocking': False,
   'action': ('Optional and NOT proposed here: the four-codes paragraph sits under the section-10 '
     'sub-heading "Admission and event routes (existing; unchanged rows)", which reads oddly over '
     'text that adds four members. I raise this as an observation only. It is not a finding, I '
     'assign it no severity, and changing it is outside this proposal scope.')}],

 'limitations': [
  'This is a coauthor technical assessment. It is NOT design acceptance, NOT independent review, NOT '
  'blind reconstruction and NOT application acceptance, and it does not change the v14 verdict.',
  'Both advisories keep the severity the independent review gave them. Nothing here is raised to a '
  'MUST or a SHOULD, and nothing is lowered or closed.',
  'I am the coauthor of the integrated v4 bytes that the V14-ADV-1 before-file contains, so I am not '
  'independent on that file. The defect I identify in the proposed wording is checkable from the '
  'bytes alone: section headings and line numbers, in both the live and the frozen file.',
  'Read-only. No source, pin, report, repository or frozen input was edited. Everything written is '
  'under /tmp/opensip-design-corrections/v14-advisory-clarification.v1.',
  'No suite was rerun and none is needed for two non-executable strings: enforcedAt is prose in a '
  'registry object and the section-10 sentence is contract prose; no checker asserts on either text. '
  'The successor reference commands and the NEW independent review assess the frozen bytes.',
  'No host, renderer, CLI, D9 interpreter or Run was executed. The call-site evidence is read-only '
  'static reading of identity-model.py, not an executed Run.',
  'V14-ADV-1 before-file is the INTEGRATED v4 byte (55dec8bf...), not the v14 reviewed byte '
  '(20b4cc04...). I verified the advisory transfers cleanly: both statements sit at the same lines '
  'and in the same section 10 in both files.'],

 'standingOfThisDocument': ('Coauthor technical assessment for root. Root owns integration, the '
   'successor freeze and pin seal, the reference commands and the NEW independent review.'),
 'implementationAuthorized': False,
}
(S / 'assessment.json').write_text(json.dumps(doc, indent=2) + '\n')
print(json.dumps({'technicalAssent': doc['technicalAssent'],
                  'perChange': doc['perChangeAssent'],
                  'proposalSha256': doc['proposalSha256'],
                  'alternativeSha256': insp['claudeAlternative']['sha256'],
                  'assessmentSha256': sha(S / 'assessment.json')}, indent=1))

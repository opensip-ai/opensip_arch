"""Read-only inspection behind the assessment. Reads the live repository and the frozen v14 snapshot;
writes ONLY under /tmp/opensip-design-corrections/v14-advisory-clarification.v1."""
import hashlib, json, re
from pathlib import Path

REPO = Path('/Users/sb/code/opensip-ai/opensip_arch')
FROZEN = Path('/tmp/opensip-design-corrections/candidate-subject.v14')
S = Path('/tmp/opensip-design-corrections/v14-advisory-clarification.v1')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
prop = json.loads((S / 'proposal.json').read_text())

def sections(path):
    lines = Path(path).read_text().split('\n')
    heads = [(i, l) for i, l in enumerate(lines, 1) if re.match(r'^## ', l)]
    def owning(n):
        return max((h for h in heads if h[0] < n), key=lambda h: h[0])[1]
    def line_of(frag):
        return next(i for i, l in enumerate(lines, 1) if frag in l)
    return owning, line_of, heads

out = {'inputs': {
    'review': {'path': '/tmp/opensip-design-corrections/post-reset-review.v14/review.json',
               'sha256': sha('/tmp/opensip-design-corrections/post-reset-review.v14/review.json')},
    'proposal': {'path': str(S / 'proposal.json'), 'sha256': sha(S / 'proposal.json')}}}

# 1. every proposal hash, and whether old->new reproduces the proposed bytes exactly
rows = []
for c in prop['changes']:
    b, p, live = S / 'before' / c['path'], S / 'proposed' / c['path'], REPO / c['path']
    bt, pt = b.read_text(), p.read_text()
    rows.append({'id': c['id'], 'path': c['path'],
                 'beforeFileMatchesDeclared': sha(b) == c['beforeSha256'],
                 'proposedFileMatchesDeclared': sha(p) == c['proposedSha256'],
                 'liveRepositoryEqualsBefore': live.exists() and sha(live) == c['beforeSha256'],
                 'oldOccurrencesInBefore': bt.count(c['old']),
                 'applyingOldToNewReproducesProposedBytes': bt.replace(c['old'], c['new'], 1) == pt,
                 'byteDelta': len(pt.encode()) - len(bt.encode())})
out['hashVerification'] = rows

# 2. V14-ADV-1: which SECTION owns each of the two statements, in the live and the frozen bytes
adv1 = {}
for label, root in [('liveIntegrated', REPO), ('frozenV14', FROZEN)]:
    f = root / 'docs/v2/contracts/product-v1/native-evidence.md'
    owning, line_of, heads = sections(f)
    s = line_of('No new public code is added and none is needed.')
    q = line_of('Four `DomainDetailCode` members are **added**')
    adv1[label] = {'fileSha256': sha(f), 'unqualifiedSentenceLine': s,
                   'unqualifiedSentenceSection': owning(s),
                   'fourCodesLine': q, 'fourCodesSection': owning(q),
                   'sectionThirteenHeading': next(l for _, l in heads if l.startswith('## 13')),
                   'bothStatementsInTheSameSection': owning(s) == owning(q)}
lines = (REPO / 'docs/v2/contracts/product-v1/native-evidence.md').read_text().split('\n')
adv1['sectionThirteenMentionsDomainDetailCode'] = any(
    'DomainDetailCode' in l for i, l in enumerate(lines, 1) if 2750 <= i < 2831)
adv1['registrySelectorsForTheFourAddedCodes'] = [
    r for r in json.loads((REPO / 'docs/coop/design-corrections/public-detail-registry.v1.json').read_text())['records']
    if r['code'] in {'native.capability-spec-invalid', 'native.release-declaration-invalid',
                     'native.coverage-cause-unsupported', 'HOST.INVARIANT_VIOLATED'}]
out['adv1'] = adv1

# 3. V14-ADV-2: the actual call sites, and the ordering claim
idm = (REPO / 'docs/coop/design-corrections/foundation/identity-model.py').read_text().split('\n')
where = lambda pat: [i for i, l in enumerate(idm, 1) if re.search(pat, l)]
anchor_lines = where(r'anchor_law')
out['adv2'] = {
  'identityModelSha256': sha(REPO / 'docs/coop/design-corrections/foundation/identity-model.py'),
  'anchorLawOccurrences': anchor_lines,
  'anchorLawDefinition': where(r'def anchor_law'),
  'anchorLawCallSites': [i for i in anchor_lines
                         if not idm[i-1].lstrip().startswith('#') and 'def ' not in idm[i-1]],
  'relationPayloadRulesDefinition': where(r'def relation_payload_rules'),
  'relationPayloadRulesCallSites': [i for i in where(r'relation_payload_rules\(')
                                    if 'def ' not in idm[i-1]],
  'openRunClosureDefinition': where(r'def open_run_closure'),
  'closeRunDelegatesToOpenRunClosure': 'return open_run_closure(run,objects,blobs)[0]' in
                                       ''.join(l.strip() for l in idm[560:564]),
  'admitCacheEntryReachesOpenRunClosure': bool([i for i in where(r'open_run_closure\(') if i > 1484]),
  'relationSourceJoinsDefinition': where(r'def relation_source_joins'),
  'anchorLawRunsBeforeSnapshotJoins': min(i for i in anchor_lines if idm[i-1].strip() == 'anchor_law(row,fact)')
                                      < where(r'def relation_source_joins')[0],
  'nativeModelDefinesNoAnchorCardinalityGuard':
      not [l for l in (REPO / 'docs/coop/design-corrections/native/native_evidence_model.v2.py').read_text().split('\n')
           if l.startswith('def ') and 'anchor' in l.lower()],
  'causeRegistryEnforcedAt': json.loads(
      (REPO / 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json').read_text()
      )['x-opensip-deficiency-cause-registry']['enforcedAt'],
  'admitCoverageResultV3Exists': 'def admit_coverage_result_v3' in
      (REPO / 'docs/coop/design-corrections/native/native_evidence_model.v2.py').read_text(),
}

# 4. is enforcedAt machine-consumed, and what does changing this file's bytes touch?
live_pins = []
for m, k in [('foundation/source-pins.v1.json', 'files'), ('workflows/source-pins.v1.json', 'files'),
             ('native/source-pins.v2.json', 'pins'), ('security/source-pins.v1.json', 'pins')]:
    d = json.loads((REPO / 'docs/coop/design-corrections' / m).read_text())
    for r in d[k]:
        if r['path'] == 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json':
            live_pins.append({'manifest': m, 'pinnedSha256': r['sha256']})
chk = (REPO / 'docs/coop/design-corrections/foundation/check-identity.py').read_text()
out['consumption'] = {
  'anyCheckerAssertsOnAnchorLawEnforcedAtText': "anchorLaw'][ 'enforcedAt" in chk or "enforcedAt" in chk,
  'relationDocumentDigestIsComputedFromBytesNotHardcoded':
      'RELATION_DOCUMENT_DIGEST=hashlib.sha256(RELATION_DOCUMENT_BYTES).hexdigest()' in chk,
  'documentDigestIsJoinedAtAdmission':
      'PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT' in '\n'.join(idm),
  'livePinManifestsCarryingTheCurrentDigest': live_pins,
  'currentDigest': sha(REPO / 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'),
  'proposedDigest': sha(S / 'proposed/docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json'),
}

# 5. the alternative I supply for V14-ADV-1
alt = S / 'claude-alternative/docs/v2/contracts/product-v1/native-evidence.md'
out['claudeAlternative'] = {'path': str(alt.relative_to(S)), 'sha256': sha(alt),
  'differsFromRootProposalOnlyBy': 'in section 13 -> later in this section'}

(S / 'inspection.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'adv1BothInSameSection': adv1['liveIntegrated']['bothStatementsInTheSameSection'],
                  'adv1SectionOfEach': [adv1['liveIntegrated']['unqualifiedSentenceSection'],
                                        adv1['liveIntegrated']['fourCodesSection']],
                  'adv2CallSites': out['adv2']['anchorLawCallSites'],
                  'adv2OrderingHolds': out['adv2']['anchorLawRunsBeforeSnapshotJoins'],
                  'allHashesVerify': all(r['beforeFileMatchesDeclared'] and r['proposedFileMatchesDeclared']
                                         and r['liveRepositoryEqualsBefore']
                                         and r['applyingOldToNewReproducesProposedBytes'] for r in rows)},
                 indent=1))

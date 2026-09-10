"""p24: independent governance verification on the v18 snapshot.
Re-verify owner-document byte identity, the five DR-201..205 owner-row flags, the 32
qualification gates, D-372 and its condition 5 -- against actual bytes, not headline claims."""
import json, os, re

F = '/tmp/opensip-design-corrections/candidate-subject.v18'
R = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
v17 = {e['path']: e['sha256'] for e in json.load(open(R + 'candidate-subject.v17.json'))['files']}
v18 = {e['path']: e['sha256'] for e in json.load(open(R + 'candidate-subject.v18.json'))['files']}
rev = json.load(open(F + '/docs/coop/design-corrections/reviews/post-reset-review.v17-clarification.v1/review.json'))

# --- owner-row flags
print('--- scopedReviewOwnerDispositions (DR-201..205) ---')
bad = []
for i, d in rev['scopedReviewOwnerDispositions'].items():
    ap, fg = d.get('appliedByThisReview'), d.get('finalApplicationOutcomeGranted')
    has = all(d.get(k) for k in ('basis', 'scope', 'authority'))
    if ap is not False or fg is not False or not has:
        bad.append(i)
    print(' %-8s applied=%-5s granted=%-5s basis/scope/authority=%s disposition=%s'
          % (i, ap, fg, has, d.get('disposition')))
print('ownerRowsViolatingRequiredFalseFlags=%d' % len(bad))

# --- every cited owner document: still byte-identical in v18?
print('\n--- owner documents cited across all four registers ---')
cited = set()
for key in ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions', 'scopedReviewOwnerDispositions'):
    for d in rev[key].values():
        for m in re.finditer(r'docs/[\w./\-]+\.(?:md|json)', json.dumps(d)):
            cited.add(m.group(0))
inv17 = [p for p in sorted(cited) if p in v17 and p in v18]
changed = [p for p in inv17 if v17[p] != v18[p]]
notin = [p for p in sorted(cited) if p not in v18]
print('citedOwnerDocs=%d inBothManifests=%d changedV17toV18=%d notInV18Manifest=%d'
      % (len(cited), len(inv17), len(changed), len(notin)))
for p in changed:
    print('   CHANGED', p)
for p in notin[:10]:
    print('   NOT-IN-SNAPSHOT', p)

# --- the 32 qualification gates
print('\n--- qualification gates ---')
reg = rev.get('registers', {})
print('declared: gates=%s demonstrated=%s qualified=%s allUnperformed=%s performedByThisReview=%s'
      % (reg.get('qualificationGates'), reg.get('gatesDemonstrated'), reg.get('gatesQualified'),
         reg.get('allGatesRemainUnperformed'), reg.get('gatesPerformedByThisReview')))

gate_doc = 'docs/v2/architecture/12-architecture-completion-goal.md'
for cand in (gate_doc, 'docs/v2/architecture/08-decision-and-readiness-register.md'):
    p = os.path.join(F, cand)
    if os.path.isfile(p):
        t = open(p).read()
        flags = {k: len(re.findall(k + r'\s*[:=]\s*(?:true|false)', t, re.I)) for k in
                 ('demonstrated', 'qualified', 'implementationHarnessAuthored')}
        tr = len(re.findall(r'(?:demonstrated|qualified|implementationHarnessAuthored)\s*[:=]\s*true', t, re.I))
        print(' %-58s flagMentions=%s trueFlags=%d bytesIdenticalV17=%s'
              % (cand.split('/')[-1], flags, tr, v17.get(cand) == v18.get(cand)))

# --- D-372 and condition 5
print('\n--- D-372 ---')
for cand in ('docs/v2/architecture/08-decision-and-readiness-register.md',
             'docs/v2/architecture/12-architecture-completion-goal.md'):
    p = os.path.join(F, cand)
    if not os.path.isfile(p):
        continue
    t = open(p).read()
    for m in re.finditer(r'D-372', t):
        s = max(0, m.start() - 200)
        seg = t[s:m.start() + 500].replace('\n', ' ')
        print(' %s ... %s' % (cand.split('/')[-1], seg[:430]))
        break

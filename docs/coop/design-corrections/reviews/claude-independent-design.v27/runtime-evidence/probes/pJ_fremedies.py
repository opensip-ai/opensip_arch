"""PROBE J (v27) — assess the F-01..F-14 remedies against frozen bytes.

Findings come from claude-author-package-review.v1/review.md (the named review.json is absent;
the rows are spelled F-01..F-14 in an embedded JSON block). They were raised against
candidate-subject.v25 and the 97-file package. This probe measures whether each requested
correction now holds in the 213-file successor package v4 and in snapshot27.

Nothing here grades a row from author self-assessment: every check reads bytes.
"""
import hashlib, io, json, os, re, subprocess, tarfile

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
PY = '/tmp/opensip-architecture-review-env/bin/python'
os.makedirs(OUT, exist_ok=True)
R = {}


def sha_file(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def txt(p):
    return open(p, encoding='utf-8').read()


def jl(p):
    return json.load(open(p, encoding='utf-8'))


def hdr(k, title):
    print('\n' + '=' * 96)
    print('%s  %s' % (k, title))
    print('=' * 96)


# ---------------- F-01 charter custody ----------------
hdr('F-01', 'charter bytes must resolve inside the frozen package')
PIN = '08dffd7f73d2e8d31830fae66818920488ab5c17d0eb82f6a60576f3bec5196e'
ho = jl(os.path.join(PKG, 'original-requirement-handoff.json'))
orig = os.path.join(PKG, 'historical-consumer-custody/original-requirements.json')
f01 = {'pinFromF01': PIN,
       'handoffTopKeys': sorted(ho)[:30],
       'originalRequirementsPresent': os.path.isfile(orig)}
if os.path.isfile(orig):
    f01['originalRequirementsSha256'] = sha_file(orig)
    f01['shaMatchesF01Pin'] = f01['originalRequirementsSha256'] == PIN
    o = jl(orig)
    f01['originalRequirementsTopKeys'] = sorted(o) if isinstance(o, dict) else ['<list>']
    # count 123 / 8 / 3
    counts = {}
    def count(o, path=''):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, list):
                    counts[path + '/' + k] = len(v)
                count(v, path + '/' + k)
    count(o)
    f01['listLengths'] = {k: v for k, v in counts.items() if v in (123, 8, 3)}
    f01['allListLengths'] = counts
# where does the handoff now point?
hs = json.dumps(ho)
f01['handoffMentionsPin'] = PIN in hs
f01['handoffShaFields'] = sorted(set(re.findall(r'"([A-Za-z0-9_]*[Ss]ha256[A-Za-z0-9_]*)"\s*:', hs)))
for k in ('originalRequirementsSha256', 'originalRequirementsPath', 'originalRequirements'):
    if k in ho:
        f01['handoff.' + k] = str(ho[k])[:200]
R['F-01'] = f01
for k, v in f01.items():
    print('  %-32s %s' % (k, json.dumps(v)[:400]))

# ---------------- F-02 consumer-b custody ----------------
hdr('F-02', 'consumer-b v13 v6/v7 assessments frozen and hash-pinned in-package')
hc = os.path.join(PKG, 'historical-consumer-custody')
f02 = {'dirPresent': os.path.isdir(hc)}
am = os.path.join(hc, 'attachment-manifest.json')
if os.path.isfile(am):
    a = jl(am)
    f02['attachmentManifestTopKeys'] = sorted(a) if isinstance(a, dict) else ['<list>']
    files = a.get('files') if isinstance(a, dict) else a
    if isinstance(files, list):
        ok = bad = miss = 0
        badrows = []
        for rec in files:
            rel = rec.get('path') or rec.get('name')
            p = os.path.join(hc, rel)
            if not os.path.isfile(p):
                p = os.path.join(PKG, rel)
            if not os.path.isfile(p):
                miss += 1
                badrows.append(('MISSING', rel))
                continue
            h = sha_file(p)
            if rec.get('sha256') == h:
                ok += 1
            else:
                bad += 1
                badrows.append(('MISMATCH', rel))
        f02.update(attachmentRows=len(files), hashMatch=ok, mismatch=bad, missing=miss,
                   badRows=badrows[:8])
f02['v6RootOwnerAssessmentPresent'] = os.path.isdir(
    os.path.join(hc, 'consumer-b.v13-pilot-admission.v6/root-owner-assessment.v1'))
f02['v7RootPartialAssessmentPresent'] = os.path.isdir(
    os.path.join(hc, 'consumer-b.v13-pilot-admission.v7/root-partial-assessment.v1'))
# does anything still point at a live /tmp working path as the authority?
live = []
for dp, dn, fn in os.walk(hc):
    for n in fn:
        if n.endswith(('.json', '.md')):
            t = open(os.path.join(dp, n), encoding='utf-8', errors='replace').read()
            for m in re.findall(r'/tmp/opensip-design-corrections/[A-Za-z0-9._/-]+', t):
                live.append((os.path.relpath(os.path.join(dp, n), hc), m))
f02['liveWorkingPathMentions'] = len(live)
f02['liveWorkingPathSample'] = sorted(set(x[1] for x in live))[:6]
R['F-02'] = f02
for k, v in f02.items():
    print('  %-32s %s' % (k, json.dumps(v)[:400]))

# ---------------- F-03 query regenerability ----------------
hdr('F-03', 'seven query checks regenerable; blind13 helper resolvable; wired into verify')
caq = txt(os.path.join(PKG, 'check-author-query.py'))
f03 = {'importsBlind13': 'blind13' in caq,
       'blind13FileInPackage': any('blind13' in n for dp, dn, fn in os.walk(PKG) for n in fn),
       'queryFiles': sorted(os.listdir(os.path.join(PKG, 'query-checks1'))),
       'queryAssessmentAtTop': os.path.isfile(os.path.join(PKG, 'query-assessment.json'))}
f03['checkAuthorQueryHead'] = caq[:1400]
vp = txt(os.path.join(PKG, 'verify-package.py'))
f03['verifyPackageMentionsQuery'] = 'query' in vp.lower()
f03['verifyPackageHead'] = vp[:900]
# did the query outputs actually change vs the source25-era copies?
changed = []
for n in f03['queryFiles']:
    new = os.path.join(PKG, 'query-checks1', n)
    old = os.path.join(PKG, 'historical-source25-preparation/query-checks1', n)
    if os.path.isfile(old):
        changed.append({'file': n, 'sameBytes': sha_file(new) == sha_file(old),
                        'newBytes': os.path.getsize(new), 'oldBytes': os.path.getsize(old)})
f03['vsSource25Era'] = changed
R['F-03'] = f03
for k, v in f03.items():
    if k.endswith('Head'):
        continue
    print('  %-32s %s' % (k, json.dumps(v)[:400]))

# ---------------- F-04 root spelling, on snapshot27 ----------------
hdr('F-04', 'WorkspaceUnitV2.rootPath internal-root spelling normative on snapshot27')
NS = os.path.join(SRC, 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json')
sch = jl(NS)
f04 = {'schemaSha256': sha_file(NS)}


def find_def(o, name):
    if isinstance(o, dict):
        if name in o.get('$defs', {}):
            return o['$defs'][name]
        for v in o.values():
            r = find_def(v, name)
            if r:
                return r
    return None


wu = find_def(sch, 'WorkspaceUnitV2')
f04['workspaceUnitV2Found'] = wu is not None
if wu:
    props = wu.get('properties', {})
    f04['rootPath'] = props.get('rootPath')
    f04['memberPackageRoots'] = props.get('memberPackageRoots')
    f04['workspaceUnitV2Keys'] = sorted(props)
NM = os.path.join(SRC, 'docs/v2/contracts/product-v1/native-evidence.md')
nmd = txt(NM)
f04['nativeEvidenceMdSha256'] = sha_file(NM)
f04['mdMentionsInternalRoot'] = len(re.findall(r'internal[- ]root', nmd, re.I))
f04['mdRootPathHits'] = len(re.findall(r'rootPath', nmd))
# any root-specific fault code anywhere on 27?
grep = subprocess.run(['grep', '-rl', 'ROOT_SPELLING\|WORKSPACE_ROOT\|UNIT_ROOT',
                       os.path.join(SRC, 'docs/coop/design-corrections')],
                      capture_output=True, text=True)
f04['rootFaultCodeFiles'] = [os.path.relpath(x, SRC) for x in grep.stdout.split() if x][:12]
R['F-04'] = f04
for k, v in f04.items():
    print('  %-32s %s' % (k, json.dumps(v)[:500]))

# ---------------- F-05/F-06 binding controls ----------------
hdr('F-05/F-06', 'default-unit negative control + explicit-selection binding')
bc = os.path.join(PKG, 'binding-controls')
f56 = {'claims': jl(os.path.join(bc, 'claims.json')),
       'variants': jl(os.path.join(bc, 'variants.json')),
       'constructionProvenance': jl(os.path.join(bc, 'construction-provenance.json'))}
bb = txt(os.path.join(PKG, 'build-binding-controls.py'))
f56['buildScript'] = bb[:2200]
tp = txt(os.path.join(PKG, 'ts_pilot.py.patch'))
f56['tsPilotPatch'] = tp
ts = txt(os.path.join(PKG, 'author-helpers/ts_pilot.py'))
f56['tsPilotHasProgramEntryParam'] = 'program_entry' in ts
f56['tsPilotProgramEntryLines'] = [l.strip()[:140] for l in ts.splitlines() if 'program_entry' in l][:12]
f56['tsPilotProvenanceLines'] = [l.strip()[:140] for l in ts.splitlines() if 'provenance' in l][:14]
R['F-05/F-06'] = {k: v for k, v in f56.items() if k not in ('buildScript', 'tsPilotPatch')}
for k, v in f56.items():
    if k in ('buildScript', 'tsPilotPatch'):
        continue
    print('  %-32s %s' % (k, json.dumps(v)[:600]))
print('\n--- ts_pilot.py.patch ---\n' + tp[:2000])

# ---------------- F-07 combinators ----------------
hdr('F-07', 'and/or/not combinators and count-at-most/all-covered')
ev = txt(os.path.join(PKG, 'author-helpers/evaluator.py'))
f07 = {'notImplementedLines': [l.strip()[:160] for l in ev.splitlines() if 'NotImplementedError' in l],
       'opTokens': sorted(set(re.findall(r"'(exists|none|all-covered|count-at-most|and|or|not)'", ev)))}
rd = txt(os.path.join(PKG, 'README.md'))
f07['readmeCombinatorSentences'] = [s.strip()[:300] for s in re.split(r'(?<=[.\n])', rd)
                                    if re.search(r'and/or/not|combinator|unexercised|two-binding', s, re.I)]
R['F-07'] = f07
for k, v in f07.items():
    print('  %-32s %s' % (k, json.dumps(v)[:700]))

# ---------------- F-08 effective edition ----------------
hdr('F-08', 'selectedUnitIds + effective targetEdition published and asserted')
ap = jl(os.path.join(PKG, 'author-properties.json'))
before = jl(os.path.join(PKG, 'historical-source25-preparation/author-properties.before-f8.json'))
aps, bfs = json.dumps(ap), json.dumps(before)
f08 = {'nowHasSelectedUnitIds': 'selectedUnitIds' in aps,
       'beforeHadSelectedUnitIds': 'selectedUnitIds' in bfs,
       'nowHasEffectiveEdition': bool(re.search(r'effective\w*[Ee]dition', aps)),
       'beforeHadEffectiveEdition': bool(re.search(r'effective\w*[Ee]dition', bfs)),
       'topKeys': sorted(ap)}
cap = txt(os.path.join(PKG, 'check-author-properties.py'))
f08['checkerAssertsEffectiveEdition'] = bool(re.search(r'effective\w*[Ee]dition', cap))
f08['checkerAssertsSelectedUnitIds'] = 'selectedUnitIds' in cap
f08['checkerAssertLines'] = [l.strip()[:150] for l in cap.splitlines()
                             if re.search(r'edition|selectedUnitIds', l)][:14]
if 'rustComparisons' in ap:
    f08['rustComparisonKeys'] = sorted(ap['rustComparisons'])
    k0 = sorted(ap['rustComparisons'])[0]
    f08['sampleComparison'] = json.dumps(ap['rustComparisons'][k0])[:900]
R['F-08'] = f08
for k, v in f08.items():
    print('  %-32s %s' % (k, json.dumps(v)[:700]))

# ---------------- F-09 citation ----------------
hdr('F-09', 'mixed-universe refusal cited to the operative clause with its code')
f09 = {}
for name in ('README.md', 'probe-mixed-universe-view.py', 'mixed-universe-view.probe.json',
             'claude-author-remint-review.md'):
    p = os.path.join(PKG, name)
    if os.path.isfile(p):
        t = txt(p)
        f09[name] = {'mentionsSection5': bool(re.search(r'§\s*5|section 5', t, re.I)),
                     'mentionsSection3': bool(re.search(r'§\s*3|section 3', t, re.I)),
                     'namesRefusalCode': 'EXECUTION_INPUTS_COVERAGE_DERIVE' in t,
                     'sentences': [s.strip()[:260] for s in re.split(r'(?<=\.)\s', t)
                                   if re.search(r'mixed[- ]universe|COVERAGE_DERIVE', s, re.I)][:6]}
R['F-09'] = f09
print(json.dumps(f09, indent=1)[:2600])

# ---------------- F-10 portability ----------------
hdr('F-10', 'portable path-parameterised entry point')
apo = txt(os.path.join(PKG, 'author_portable.py'))
f10 = {'authorPortablePresent': True, 'bytes': len(apo),
       'sha256': sha_file(os.path.join(PKG, 'author_portable.py')),
       'head': apo[:1800]}
adc = txt(os.path.join(PKG, 'author-delivery-commands.md'))
f10['deliveryMentionsPortable'] = 'author_portable' in adc
R['F-10'] = {k: v for k, v in f10.items() if k != 'head'}
print(apo[:1800])

# ---------------- F-11 self-comparison ----------------
hdr('F-11', 'vacuous self-comparison removed')
runs = txt(os.path.join(PKG, 'author-helpers/runs.py'))
f11 = {'derivedProofToken': runs.count('derivedProof'),
       'claimedProofToken': runs.count('claimedProof'),
       'compareProofSelf': len(re.findall(r'compare_proof\(\s*proof\s*,\s*proof\s*\)', runs)),
       'patch': txt(os.path.join(PKG, 'runs.py.patch'))[:2200]}
R['F-11'] = {k: v for k, v in f11.items() if k != 'patch'}
for k, v in f11.items():
    if k == 'patch':
        continue
    print('  %-32s %s' % (k, v))
print('\n--- runs.py.patch ---\n' + f11['patch'][:1800])

# ---------------- F-12/F-13/F-14 weighting + shared TCB ----------------
hdr('F-12/F-13/F-14', 'per-group derivation weighting; shared TCB dependency disclosed')
era = jl(os.path.join(PKG, 'evaluation-residual-author-assessment.json'))
s = json.dumps(era)
f12 = {'readmeWeightingSentences': [x.strip()[:300] for x in re.split(r'(?<=\.)\s', rd)
                                   if re.search(r'self-deriv|two-implementation|frozen owner|frozen-owner|weight', x, re.I)][:8]}
tcb = {'topKeys': sorted(era) if isinstance(era, dict) else ['<list>'],
       'mentionsTcbScope01': 'TCB-SCOPE-01' in s,
       'sharedDependencyTokens': sorted(set(re.findall(r'TCB[-_A-Z0-9]*', s)))[:12]}
items = era.get('items') if isinstance(era, dict) else era
if isinstance(items, list):
    tcb['itemCount'] = len(items)
    tcb['itemIds'] = [i.get('id') for i in items]
    verdicts = {}
    for i in items:
        for k, v in i.items():
            if 'ssessment' in k and isinstance(v, str):
                verdicts.setdefault(v, 0)
                verdicts[v] += 1
    tcb['authorAssessmentVerdictCounts'] = verdicts
for k in era if isinstance(era, dict) else []:
    if 'tcb' in k.lower() or 'shared' in k.lower() or 'depend' in k.lower():
        tcb['block.' + k] = json.dumps(era[k])[:1500]
R['F-12'] = f12
R['F-13/F-14'] = tcb
print(json.dumps(f12, indent=1)[:1500])
print(json.dumps(tcb, indent=1)[:3000])

json.dump(R, open(os.path.join(OUT, 'pJ-fremedies.json'), 'w'), indent=1, default=str)
print('\nwrote', os.path.join(OUT, 'pJ-fremedies.json'))

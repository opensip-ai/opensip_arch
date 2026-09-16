"""PROBE 10 (v31) — source30 item: the native-cases.v2 coverageView schema digest refresh.

The claim is that a foundation drift guard correctly FAILED at source29 and that source30 refreshed
exactly one coverageView schema digest, with no semantic law changed and the failed source29 receipt
preserved. I check the refreshed digest actually equals the current schema digest it guards (so the
guard is satisfied by truth, not by loosening), and look for the preserved failed receipt.
"""
import hashlib, json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v31.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {}

NC = os.path.join(SRC, 'docs/coop/design-corrections/native/native-cases.v2.json')
d = json.load(open(NC))
R['nativeCasesTopKeys'] = sorted(d) if isinstance(d, dict) else '<list>'
R['nativeCasesSha256'] = hashlib.sha256(open(NC, 'rb').read()).hexdigest()
print('native-cases.v2.json top keys:', R['nativeCasesTopKeys'])

# every 64-hex under a path mentioning coverage/view/schema
found = []
def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            np = path + '/' + k
            if isinstance(v, str) and re.fullmatch(r'[0-9a-f]{64}', v):
                found.append((np, v))
            walk(v, np)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + '/%d' % i)
walk(d)
R['total64HexFields'] = len(found)
cov = [(p, v) for p, v in found if re.search(r'coverage|view', p, re.I)]
R['coverageViewDigestFields'] = [{'path': p, 'digest': v} for p, v in cov]
print('64-hex fields: %d | coverage/view-named: %d' % (len(found), len(cov)))
for p, v in cov[:12]:
    print('   %-72s %s' % (p[:72], v[:24]))

# distinct schema-digest values and which frozen document each equals
docs = {}
for rel, f in man.items():
    docs.setdefault(f['sha256'], []).append(rel)
resolved = []
for p, v in cov:
    resolved.append({'path': p, 'digest': v, 'matchesFrozenDocument': docs.get(v, [])})
R['coverageDigestsResolvedToFrozenDocuments'] = resolved
print('\ncoverage/view digests resolved against frozen31 documents:')
for x in resolved[:12]:
    print('   %-60s -> %s' % (x['path'][-60:], x['matchesFrozenDocument'] or 'NO RAW-FILE MATCH'))

# the same exercise for ALL schema-digest-looking fields, to find the guarded pairs
sd = [(p, v) for p, v in found if re.search(r'schemaDigest|schemaSha|documentSha', p)]
R['schemaDigestFields'] = [{'path': p, 'digest': v, 'matchesFrozenDocument': docs.get(v, [])} for p, v in sd]
print('\nschemaDigest-style fields: %d' % len(sd))
unresolved = [x for x in R['schemaDigestFields'] if not x['matchesFrozenDocument']]
R['schemaDigestFieldsNotMatchingAnyFrozenFile'] = unresolved[:8]
R['schemaDigestFieldsResolvedCount'] = len(sd) - len(unresolved)
for x in R['schemaDigestFields'][:10]:
    print('   %-58s -> %s' % (x['path'][-58:], x['matchesFrozenDocument'] or 'canonical/derived, not a raw file'))

# preserved failed source29 receipt?
cands = [rel for rel in man if re.search(r'29', rel) and re.search(r'receipt|report|verif', rel, re.I)]
R['source29ReceiptCandidatesInFrozen31'] = cands[:20]
print('\nfrozen31 paths that look like a source29 receipt:', cands[:10])
for base in ('/tmp/opensip-design-corrections/final31-independent-review-inputs.v1',
             '/tmp/opensip-design-corrections/root-native-digest-catalog-correction.v1'):
    if os.path.isdir(base):
        listing = []
        for dp, dn, fn in os.walk(base):
            for n in fn:
                listing.append(os.path.relpath(os.path.join(dp, n), base))
        R['rootDir_' + os.path.basename(base)] = sorted(listing)[:40]
        print('\n%s:' % base)
        for x in sorted(listing)[:25]:
            print('   ', x)

json.dump(R, open(os.path.join(OUT, 'p10-coverageview.json'), 'w'), indent=1, default=str)
print('\nwrote p10-coverageview.json')

"""S05 — same bounded section-level comparison for the OTHER changed owner the seven rows cite:
docs/v2/contracts/product-v1/native-evidence.md. Read-only, one file, headings only."""
import difflib, hashlib, json, os, re

A = '/tmp/opensip-design-corrections/candidate-subject.v32/docs/v2/contracts/product-v1/native-evidence.md'
B = '/tmp/opensip-design-corrections/candidate-subject.v33/docs/v2/contracts/product-v1/native-evidence.md'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/receipts'
R = {}
R['sha32'] = hashlib.sha256(open(A, 'rb').read()).hexdigest()
R['sha33'] = hashlib.sha256(open(B, 'rb').read()).hexdigest()
R['matchesMyDeltaRecord'] = (
    R['sha32'] == '6bffdeef81ce0699d8005914613526fe52dea1648cc6793578992f7b61bc7cb2' and
    R['sha33'] == '1cfc8fccf0ac2e79c41671da524a5c4c5b4e91447a144d65a3e293e59b34ae0c')
print('both digests match my recorded delta row:', R['matchesMyDeltaRecord'])


def sections(p):
    out, cur, buf = {}, '(preamble)', []
    for line in open(p, encoding='utf-8'):
        if re.match(r'^#{1,4} ', line):
            out[cur] = ''.join(buf)
            cur, buf = line.strip(), []
        else:
            buf.append(line)
    out[cur] = ''.join(buf)
    return out


sa, sb = sections(A), sections(B)
R['sections32'], R['sections33'] = len(sa), len(sb)
R['addedSections'] = [k for k in sb if k not in sa]
R['removedSections'] = [k for k in sa if k not in sb]
changed = [k for k in sb if k in sa and sa[k] != sb[k]]
R['changedSections'] = changed
print('sections 32/33: %d/%d | added: %s | removed: %s' % (len(sa), len(sb), R['addedSections'], R['removedSections']))
print('changed sections (%d):' % len(changed))
for k in changed:
    print('   ', k[:120])
R['changedSectionDiffs'] = {}
added = []
for k in changed:
    d = list(difflib.unified_diff(sa[k].splitlines(), sb[k].splitlines(), lineterm='', n=1))
    R['changedSectionDiffs'][k] = d
    print('\n===== %s' % k[:120])
    for line in d:
        if line.startswith(('+', '-')) and not line.startswith(('+++', '---')):
            print('   %s' % line[:240])
            if line.startswith('+'):
                added.append(line[1:])
R['addedText'] = '\n'.join(added)

SUBJ = {'AR-13': ['monorepo', 'output handling', 'TS', 'Rust', 'language cell'],
        'FW-01': ['zero-config', 'recommend'],
        'FW-02': ['clone'],
        'FW-04': ['richer evidence', 'evidence richness'],
        'DR-011-R05': ['protocol', 'PC-7', 'phase', 'negotiation', 'reject-before-disclosure'],
        'DR-011-R08': ['D9', 'termination', 'faultCause', 'host-owned']}
R['rowSubjectHitsInChangedText'] = {}
low = R['addedText'].lower()
for rid, toks in SUBJ.items():
    R['rowSubjectHitsInChangedText'][rid] = {t: low.count(t.lower()) for t in toks}
    print('\n%s subject tokens in ADDED text: %s' % (rid, R['rowSubjectHitsInChangedText'][rid]))
json.dump(R, open(os.path.join(OUT, 's05-nativediff.json'), 'w'), indent=1, default=str)
print('\nwrote s05-nativediff.json')

"""S04 — bounded, read-only section-level comparison of the ONE changed composition contract between
frozen32 and frozen33, so the three residual statements rest on measurement rather than inference.
Not a suite, not a rerun: one file, section headings only, both sides read-only."""
import difflib, hashlib, json, os, re

A = '/tmp/opensip-design-corrections/candidate-subject.v32/docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md'
B = '/tmp/opensip-design-corrections/candidate-subject.v33/docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/receipts'
R = {}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


R['sha32'] = sha(A)
R['sha33'] = sha(B)
R['matchesMyDeltaRecord'] = (
    R['sha32'] == 'c5b8fd2f1de1c5c1e77c5c074b35f3581004318c1c1e0983aa34cb09a83ecf8e' and
    R['sha33'] == '1640740f71ab501818cf8498153354228f6fb84e920a03f7c5c96f1b3ced4bda')
print('both digests match my recorded delta row:', R['matchesMyDeltaRecord'])


def sections(p):
    out, cur, buf = {}, '(preamble)', []
    for line in open(p, encoding='utf-8'):
        if re.match(r'^#{1,3} ', line):
            out[cur] = ''.join(buf)
            cur, buf = line.strip(), []
        else:
            buf.append(line)
    out[cur] = ''.join(buf)
    return out


sa, sb = sections(A), sections(B)
R['sections32'] = len(sa)
R['sections33'] = len(sb)
R['addedSections'] = [k for k in sb if k not in sa]
R['removedSections'] = [k for k in sa if k not in sb]
changed = [k for k in sb if k in sa and sa[k] != sb[k]]
R['changedSections'] = changed
print('sections 32/33: %d/%d | added: %s | removed: %s' % (len(sa), len(sb), R['addedSections'], R['removedSections']))
print('changed sections (%d): %s' % (len(changed), changed))

R['changedSectionDiffs'] = {}
for k in changed:
    d = list(difflib.unified_diff(sa[k].splitlines(), sb[k].splitlines(), lineterm='', n=1))
    R['changedSectionDiffs'][k] = d
    print('\n===== %s  (%d diff lines)' % (k, len(d)))
    for line in d[:60]:
        if line.startswith(('+', '-')) and not line.startswith(('+++', '---')):
            print('   %s' % line[:230])

# which residual subjects appear in the changed regions?
SUBJ = {'RES-EP13-01': ['derivation DAG', 'plan2', 'exec-plan2', 'transitive', 'C-2'],
        'RES-EP13-07': ['seal', 'verdict', 'policy', 'proof'],
        'RES-EP13-15': ['self-census', 'check-c2-v5', 'v4', 'adjudication']}
R['residualSubjectHitsInChangedText'] = {}
addedtext = '\n'.join(l[1:] for k in changed for l in R['changedSectionDiffs'][k]
                      if l.startswith('+') and not l.startswith('+++'))
R['addedTextChars'] = len(addedtext)
for rid, toks in SUBJ.items():
    hits = {t: addedtext.lower().count(t.lower()) for t in toks}
    R['residualSubjectHitsInChangedText'][rid] = hits
    print('\n%s subject tokens in the ADDED text: %s' % (rid, hits))
json.dump(R, open(os.path.join(OUT, 's04-compdiff.json'), 'w'), indent=1, default=str)
print('\nwrote s04-compdiff.json')

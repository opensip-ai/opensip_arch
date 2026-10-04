"""Check SD-8 without writing anything.

Usage: check_sd8.py [--product PATH] [--rev REV]
(default /Users/sb/code/opensip-ai/opensip and 1799d3d; both read only, through `git show`).

It re-derives, independently of build_sd8.py:
1. the parent pin against the arch bytes and as accepted in the product lock, with no complete NE copy;
2. the supersession: it names SD-7's bound record by exact pin, the same parent and selector; its
   `before` equals SD-7's `after`; SD-7's entry is still the current meaning of NE:3540; and the chain
   below it is SD-5's override of the raw line, which SD-7 superseded;
3. what changed: the release-declaration row is untouched; every word of SD-7's text survives, in
   order; the only removed character is the sentence-ending period the new clause follows; and the
   new text says exactly the durable detail, the ephemeral form without detail, and RTC section 7.4;
4. the sources: RTC section 7.4 (the selected text, which no bound record overrides) admits no
   detail on an ephemeral attempt; the lead ruling, M3-C r8's item 7 and J1 r6 (accepted; row 27,
   the item 10 bullet and "Routed to the lead") say the same;
5. that the README names the passage and carries the exact supersededPassages list.
Run with python3 -I -B at nice -n 19.
"""
import difflib, hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
B = A / 'docs/implementation/m3/supervisor-d'
D = B / 'sd-8'
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', '1799d3d')
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
RTC = 'docs/coop/design-corrections/foundation/run-termination-contract.v1.md'
SD5 = 'docs/implementation/m3/supervisor-d/sd-5/successor.json'
SD7 = 'docs/implementation/m3/supervisor-d/sd-7/successor.json'
SOURCES = {
    'ruling': ('docs/implementation/m3/reviews/grok-j2a-r1/REQUEST.md',
               'c2fbbe412ae581cebb3b5043adf5b866b6f838f29dae7547bdb71a26e88b02ea'),
    'mc8': ('docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md',
            '578c186ec9fc239f42d88713b8c31ec7085ab507251691f6cbba01e49b6607e1'),
    'mj6': ('docs/implementation/m3/host-pipeline-j/PROPOSAL-r6.md',
            '086e804a41bb924325e320f317cb023fa9a2212c56e95c5bdcc806cca2794ea9'),
}


def show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def pinned(row):
    raw = (A / row['path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == row['sha256'] and len(raw) == row['bytes'], row['path']
    return raw


def keyof(entry):
    return (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))


def flat(text):
    return re.sub(r'\s+', ' ', text)


record = json.loads((D / 'successor.json').read_bytes())
lock = json.loads(show('design-lock.json'))
accepted, current, pins, entries, names = {}, {}, {}, {}, set()
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = {k: row[k] for k in ('path', 'bytes', 'sha256')}
for b in lock['contractSuccessors']:
    rec = json.loads(pinned(b['record']))
    pins[b['record']['path']] = b['record']
    for row in rec['candidates']:
        accepted[row['path']] = row
        names.add(row['path'].rsplit('/', 1)[-1])
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        current[keyof(e)] = (b['record'], e)
        entries[(b['record']['path'],) + keyof(e)] = e
report = {'rev': REV, 'contractSuccessors': len(lock['contractSuccessors'])}

# 1. Parent.
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'passageSupersessions', 'candidates'}
assert record['passageOverrides'] == []
assert [p['path'] for p in record['parents']] == [NE]
ne_pin = record['parents'][0]
ne_raw = pinned(ne_pin)
assert accepted[NE] == ne_pin and NE.rsplit('/', 1)[-1] not in names

# 2. The supersession and the chain under it.
[s] = record['passageSupersessions']
assert set(s) == {'parent', 'selector', 'before', 'after', 'supersedes'}
assert s['parent'] == ne_pin and s['selector'] == {'line': 3540}
assert s['supersedes'] == {'record': pins[SD7], 'parent': ne_pin, 'selector': {'line': 3540}}
owner, sd7_entry = current[keyof(s)]
assert owner == pins[SD7], 'SD-7 is no longer the current meaning of NE:3540'
assert 'supersedes' in sd7_entry and sd7_entry['after'] == s['before']
assert sd7_entry['supersedes']['record'] == pins[SD5]
sd5_entry = entries[(SD5,) + keyof(s)]
assert 'supersedes' not in sd5_entry and sd5_entry['after'] == sd7_entry['before']
assert ne_raw.decode('utf-8').splitlines()[3539] == sd5_entry['before']
report['chain'] = ['raw NE:3540', 'SD-5 override', 'SD-7 supersession', 'SD-8 supersession (this unit)']

# 3. What changed.
b_rows, a_rows = s['before'].split('\n'), s['after'].split('\n')
assert len(b_rows) == len(a_rows) == 2 and b_rows[0] == a_rows[0], 'the release-declaration row changed'
bw, aw = re.findall(r'\S+', s['before']), re.findall(r'\S+', s['after'])
it = iter(aw)
removed = []
for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, s['before'], s['after'], autojunk=False).get_opcodes():
    if tag in ('replace', 'delete'):
        removed.append(s['before'][i1:i2])
assert removed == ['.'] or removed == [], removed
words_kept = sum(1 for w in bw if w.rstrip('.') in (x.rstrip('.') for x in it))
assert words_kept == len(bw), 'a word of SD-7\'s text is lost'
OLD_TAIL = ('keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`,'
            ' `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`.')
assert s['before'].count(OLD_TAIL) == 1 and OLD_TAIL not in s['after']
for phrase in ('with `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` on a durable request.',
               'On an ephemeral request, the no-trust form included, it is `indeterminate` (3),'
               ' `COVERAGE.PROVIDER_UNAVAILABLE`, `authority: ephemeral`, with no runId and no detail',
               'the run-termination contract\'s §7.4 admits no detail on an ephemeral attempt',
               '(contract successor SD-8)'):
    assert phrase in s['after'], phrase
assert s['after'].count('COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED') == 1
assert s['after'].count('—') == s['before'].count('—')
report['wordsKept'] = words_kept

# 4. Sources.
assert not any(k[0] == RTC for k in current), 'RTC carries a bound override'
rtc = flat(pinned(accepted[RTC]).decode('utf-8'))
assert ('No §7.5 detail is admitted for an ephemeral attempt either (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`)' in rtc)
assert 'Every verdict class carries `authority=ephemeral`' in rtc and 'never carries `runId`' in rtc
for name, (path, sha) in SOURCES.items():
    raw = (A / path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == sha, path
    text = flat(raw.decode('utf-8'))
    if name == 'ruling':
        assert '**The run-termination contract\'s §7.4 governs.** An ephemeral attempt carries no detail' in text
    elif name == 'mj6':
        lines = raw.decode('utf-8').splitlines()
        assert lines[782].startswith('| 27 |') and 'Ephemeral (E-3): no detail (RTC §7.4)' in lines[782]
        assert '**Lead ruling:** an NE passage supersession, **SD-8**, of SD-7\'s NE:3540 override' in lines[971]
        assert 'Routed to the lead' in lines[970] and 'Recorded, not resolved' in lines[821]
    else:
        assert 'The durable not-installed case keeps that detail' in text and 'no `domainDetail`' in text

# 5. README.
readme = (D / 'README.md').read_text(encoding='utf-8')
assert NE in readme and 'line 3540' in readme
assert json.dumps([s['supersedes']]) in readme
report['supersededPassages'] = [s['supersedes']]
report['check'] = 'pass'
print(json.dumps(report, indent=1))

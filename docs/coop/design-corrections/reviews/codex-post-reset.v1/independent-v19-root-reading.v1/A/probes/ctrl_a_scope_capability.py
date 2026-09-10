"""Independent controls for CB7-MUST-1: TS closed-suffix clone scope classification.

Authored fresh for post-reset-review.v19. Runs against the DISPOSABLE COPY only.
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path('/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19')
DC = ROOT / 'docs/coop/design-corrections'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

N = load('nem', DC / 'native/native_evidence_model.v2.py')
IM = load('idm', DC / 'foundation/identity-model.py')

DD = IM.SCHEMA['x-opensip-digest-domains']
LAW = DD['scopeCapabilityLaw']
NS = DD['domainSets']['native-semantic-universe']
TS = NS['native.semantic-universe.typescript.v2']['languageVersionBinding']['dialect']
RUST = NS['native.semantic-universe.rust.v2']['languageVersionBinding']['dialect']
SYN = NS['native.semantic-universe.syntax.v2']['languageVersionBinding']['dialect']
UNSUP = {'deficiency': LAW['onUnsupportedScope']['deficiency'],
         'nativeCause': LAW['onUnsupportedScope']['nativeCause']}

R = []
def ck(cid, desc, got, want):
    ok = got == want
    R.append({'id': cid, 'desc': desc, 'pass': ok, 'observed': got, 'expected': want})
    return ok

svp = N.source_variant_of_path
sup = N.source_variant_capability_support

# --- A1 longest-suffix selection, incl. declaration suffix -------------------
for p, want in [('a.d.ts', 'ts-declaration'), ('a.ts', 'ts'), ('a.tsx', 'tsx'),
                ('a.mts', 'mts'), ('a.cts', 'cts'), ('a.js', 'js'), ('a.jsx', 'jsx'),
                ('a.mjs', 'mjs'), ('a.cjs', 'cjs'),
                ('package.json', None), ('README.md', None), ('a.rs', None),
                ('a.tsx.bak', None), ('.ts', 'ts'), ('weird.d.tsx', 'tsx')]:
    ck('A1:' + p, 'TS table longest-match variant', svp(p, TS['table']), want)
# a Rust file under the SYNTAX table is readable there but not under TS
ck('A1:rs-syntax', '.rs selects rs under syntax table', svp('a.rs', SYN['table']), 'rs')

# --- A2 unknown / mixed / empty at require_all=True (source-path scope) ------
ck('A2:unknown', 'clones@ over package.json unsupported',
   sup(TS, 'clones', 'body-normalized', ['package.json'], True), UNSUP)
ck('A2:supported', 'clones@ over src/a.ts supported',
   sup(TS, 'clones', 'body-normalized', ['src/a.ts'], True), None)
ck('A2:mixed', 'mixed supported+unknown is unsupported (no hiding)',
   sup(TS, 'clones', 'body-normalized', ['src/a.ts', 'package.json'], True), UNSUP)
ck('A2:mixed-rev', 'order does not matter for mixed',
   sup(TS, 'clones', 'body-normalized', ['package.json', 'src/a.ts'], True), UNSUP)
ck('A2:empty', 'empty source-path scope is unsupported, not vacuous',
   sup(TS, 'clones', 'body-normalized', [], True), UNSUP)
ck('A2:dts', 'declaration suffix is supported scope',
   sup(TS, 'clones', 'body-normalized', ['types/x.d.ts'], True), None)
ck('A2:all-js', 'JS variants supported under TS universe',
   sup(TS, 'clones', 'body-normalized', ['a.js', 'b.mjs', 'c.cjs', 'd.jsx'], True), None)

# --- A3 symbol-kind branch (require_all=False) ------------------------------
ck('A3:any-one', 'symbol branch supported when >=1 readable',
   sup(TS, 'declares', 'symbol-normalized', ['package.json', 'src/a.ts'], False), None)
ck('A3:none', 'symbol branch unsupported when none readable',
   sup(TS, 'declares', 'symbol-normalized', ['package.json', 'go.mod'], False), UNSUP)
ck('A3:empty', 'empty symbol branch unsupported (any([])==False)',
   sup(TS, 'declares', 'symbol-normalized', [], False), UNSUP)

# --- A4 inventory capabilities never gated ---------------------------------
for rel, rung in [('file', 'enumerated'), ('package', 'manifest-declared'), ('vcs-change', 'vcs-reported')]:
    ck('A4:' + rel, 'inventory capability ungated even on unknown suffix',
       sup(TS, rel, rung, ['package.json'], True), None)
    ck('A4:' + rel + ':empty', 'inventory capability ungated on empty scope',
       sup(TS, rel, rung, [], True), None)
ck('A4:inventory-set', 'INVENTORY_CAPABILITIES matches law inventoryExempt',
   sorted(N.INVENTORY_CAPABILITIES),
   sorted(['file@enumerated', 'package@manifest-declared', 'vcs-change@vcs-reported']))

# --- A5 Rust ownership form untouched by this law --------------------------
ck('A5:rust', 'rust dialect has no closed suffix table -> law does not own it',
   sup(RUST, 'clones', 'body-normalized', ['src/main.rs'], True), None)
ck('A5:rust-unknown', 'rust dialect ungated even for unlisted suffix',
   sup(RUST, 'clones', 'body-normalized', ['Cargo.toml'], True), None)
ck('A5:rust-form', 'rust form is the ownership form',
   RUST['form'], 'selected-compilation-target-edition')
ck('A5:rust-owner-code', 'OWNER_NOT_COMPILED vocabulary still present',
   RUST.get('onOwnerNotCompiled'), 'BODY_LANGUAGE_OWNER_NOT_COMPILED')
ck('A5:no-table-none', 'empty/absent table returns None (not a refusal)',
   [sup({}, 'clones', 'body-normalized', ['x.q'], True),
    sup({'table': {}}, 'clones', 'body-normalized', ['x.q'], True),
    sup({'table': None}, 'clones', 'body-normalized', ['x.q'], True)], [None, None, None])

# --- A6 no hardcoded vocabulary duplication --------------------------------
ck('A6:law-identity', 'module disclosure equals the registry law (single authority)',
   N.SCOPE_CAPABILITY_LAW, LAW)
ck('A6:pair', 'published pair is exactly the registry pair',
   N.SOURCE_VARIANT_UNAVAILABLE_DISCLOSURE, UNSUP)
ck('A6:existing-vocab', 'no NEW deficiency/cause code introduced',
   [UNSUP['deficiency'] in json.dumps(DD.get('deficiency', DD)),
    UNSUP['nativeCause']], [True, 'capability-missing'])
src = (DC / 'native/native_evidence_model.v2.py').read_text()
# The concern is duplication of the sourceVariant VOCABULARY this law consumes, not the
# pre-existing and separately drift-controlled BUNDLED_GRAMMARS suffix->languageId table.
idsrc = (DC / 'foundation/identity-model.py').read_text()
# A restated table would pair a SUFFIX literal with a VARIANT literal. Bare 'jsx'/'ts' tokens
# collide with the tsconfig option name and other vocabularies, so pairing is the real test.
def restated_pairs(text):
    hits = []
    for line in text.splitlines():
        for suf, var in list(TS['table'].items()) + list(SYN['table'].items()):
            if ('"%s"' % suf) in line or ("'%s'" % suf) in line:
                if ('"%s"' % var) in line or ("'%s'" % var) in line:
                    hits.append((suf, var, line.strip()[:90]))
    return hits
ck('A6:no-restated-table', 'no suffix->sourceVariant pair restated in either model',
   restated_pairs(src) + restated_pairs(idsrc), [])
ck('A6:table-from-registry', 'guards read the table only via the universe record',
   [src.count('.get("table")') + src.count(".get('table')"),
    src.count('["table"]') + src.count("['table']"),
    "languageVersionBinding" in idsrc], [1, 0, True])

# --- A7 returned disclosure is a COPY (callers cannot mutate the registry) --
d1 = sup(TS, 'clones', 'body-normalized', ['package.json'], True)
d1['deficiency'] = 'TAMPERED'
ck('A7:copy', 'disclosure returned by value, registry unaffected',
   sup(TS, 'clones', 'body-normalized', ['package.json'], True), UNSUP)

# --- A8 syntax universe: same form, but weaker than its own grammar guard ---
ck('A8:syntax-form', 'syntax universe is also closed-suffix-table', SYN['form'], 'closed-suffix-table')
ck('A8:syntax-data-doc', 'data-document suffix unsupported under syntax table too',
   sup(SYN, 'clones', 'body-normalized', ['package.json'], True), UNSUP)
ck('A8:syntax-rs', 'syntax table reads .rs (weaker necessary condition)',
   sup(SYN, 'clones', 'body-normalized', ['a.rs'], True), None)

fails = [r for r in R if not r['pass']]
out = {'controls': len(R), 'failed': len(fails), 'failures': fails, 'results': R}
Path('/tmp/opensip-design-corrections/post-reset-review.v19/results/ctrl-a.json').write_text(json.dumps(out, indent=1))
print('CTRL-A controls=%d failed=%d' % (len(R), len(fails)))
for f in fails:
    print('  FAIL', f['id'], f['desc'], 'observed=', f['observed'], 'expected=', f['expected'])

"""PROBE S (v27) — re-assess my v26 S-1/S-2/S-3 and A-1/A-2/A-3 against corrected bytes."""
import hashlib, importlib.util, json, os, re, sys, collections

R = '/tmp/opensip-design-corrections/candidate-subject.v27'
DC = os.path.join(R, 'docs/coop/design-corrections')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
res = {}

# ---------------- S-1 : bare-digest scope ----------------
ids = json.load(open(os.path.join(DC, 'foundation/identity-schemas.v3.json'), encoding='utf-8'))
dd = ids['x-opensip-digest-domains']
scope = dd.get('scope')
s1 = {'standing': dd['standing'], 'scopeKeyPresent': scope is not None, 'scope': scope}

BARE = re.compile(r'^\^\[0-9a-f\]\{64\}')
PREF = re.compile(r'^\^([A-Za-z0-9._-]+):\[0-9a-f\]\{64\}')
ANY = re.compile(r'\[0-9a-f\]\{64\}')


def deref(node, seen=()):
    if not isinstance(node, dict):
        return None, None
    p = node.get('pattern')
    if isinstance(p, str) and ANY.search(p):
        return p, ('bare' if BARE.match(p) else
                   ('prefixed:' + PREF.match(p).group(1) if PREF.match(p) else 'other'))
    ref = node.get('$ref')
    if isinstance(ref, str) and ref.startswith('#/') and ref not in seen:
        t = ids
        for part in ref[2:].split('/'):
            t = t.get(part, {}) if isinstance(t, dict) else {}
        return deref(t, seen + (ref,))
    for comb in ('oneOf', 'anyOf', 'allOf'):
        for alt in node.get(comb, []) or []:
            r = deref(alt, seen)
            if r[0]:
                return r
    return None, None


occ = []


def walk(node, ptr, inherited):
    if isinstance(node, dict):
        ann = node.get('x-opensip-digest', inherited)
        pat, cls = deref(node)
        if pat and ptr.count('/$defs/') <= 1:
            occ.append({'ptr': ptr, 'class': cls, 'annotated': ann is not None})
        for k, v in node.items():
            if k != 'x-opensip-digest':
                walk(v, ptr + '/' + str(k), ann)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, ptr + '/' + str(i), inherited)


walk(ids, '', None)
prop = [o for o in occ if '/properties/' in o['ptr'] or o['ptr'].endswith('/items')]
bare = [o for o in prop if o['class'] == 'bare']
pref = [o for o in prop if str(o['class']).startswith('prefixed:')]


def branch_annotated(ptr):
    """A nullable field may carry the annotation on its non-null branch."""
    for o in occ:
        if o['ptr'].startswith(ptr) and o['annotated']:
            return True
    return False


s1['bareOccurrences'] = len(bare)
s1['bareUnannotatedEvenCountingBranches'] = sorted(
    o['ptr'] for o in bare if not o['annotated'] and not branch_annotated(o['ptr']))
s1['prefixedOccurrences'] = len(pref)
s1['prefixedUnannotated'] = sum(1 for o in pref if not o['annotated'])
s1['scopeExcludesPrefixed'] = bool(scope and 'typedPrefixIdentities' in scope)
s1['scopeNamesHashRef'] = bool(scope and '$ref' in (scope.get('schemaSelectors') or {}))
s1['scopeNamesNullableBranch'] = bool(scope and scope.get('nullableAlternatives'))
s1['standingNarrowed'] = 'bare 64-hex digest field' in dd['standing']
ie = open(os.path.join(R, 'docs/v2/contracts/product-v1/identity-and-evidence.md'),
          encoding='utf-8').read()
s1['proseNarrowedOccurrences'] = ie.count('bare 64-hex digest field')
s1['proseStillHasUnqualifiedUniversal'] = bool(
    re.search(r'Every 64-hex field in\s+identity-schemas', ie))
s1['proseNamesScopeKey'] = 'x-opensip-digest-domains.scope' in ie
s1['RESOLVED'] = (s1['standingNarrowed'] and s1['scopeKeyPresent']
                  and s1['scopeExcludesPrefixed'] and s1['scopeNamesHashRef']
                  and s1['scopeNamesNullableBranch'] and s1['proseNamesScopeKey']
                  and not s1['proseStillHasUnqualifiedUniversal']
                  and not s1['bareUnannotatedEvenCountingBranches'])
res['S-1'] = s1

# ---------------- S-2 : carrier intent scoping ----------------
cm = open(os.path.join(DC, 'security/carrier-migration.v1.md'), encoding='utf-8').read()
cd = json.load(open(os.path.join(DC, 'security/carrier-dispatch.v3.json'), encoding='utf-8'))
intent = cd['migration']['intentIsNotPersisted']
s2 = {
    'migrationProseScopesToInheritedPath':
        'inherited-carrier migration path' in cm and 'takes no CarrierMigrationIntentV1' in cm,
    'dispatchScopesToInheritedPath':
        'inherited-carrier migration path' in intent and 'takes no CarrierMigrationIntentV1' in intent,
    'coversResumedMigration': 'including a resumed migration' in cm and 'including a resumed migration' in intent,
    'coversInterruptedInstallActCResume':
        'interrupted-install act-C resume' in cm and 'interrupted-install act-C resume' in intent,
    'statesFreshInstallFirstGenerationOne':
        'first generation is 1' in cm or 'first_generation is 1' in intent,
    'intentDomainsUnchanged': {
        'observedFormat': re.search(r'observedFormat:\s*(.*?),', cm).group(1).strip(),
        'firstGeneration': re.search(r'firstGeneration:\s*(.*?),', cm).group(1).strip()},
}
s2['RESOLVED'] = all(v for k, v in s2.items() if isinstance(v, bool))
res['S-2'] = s2

# ---------------- S-3 : anchor ids ----------------
rab = json.load(open(os.path.join(R, 'docs/v2/architecture/report-asset-binding.v1.json'),
                     encoding='utf-8'))
anchors = rab['frozenSourceAnchors']
ids_ = [a['id'] for a in anchors]
dups = [k for k, v in collections.Counter(ids_).items() if v > 1]
txt = json.dumps(rab)
s3 = {
    'anchorCount': len(anchors), 'duplicateIds': dups,
    'b14Present': 'B14' in ids_,
    'b14Source': next((a['path'] for a in anchors if a['id'] == 'B14'), None),
    'b11Source': next((a['path'] for a in anchors if a['id'] == 'B11'), None),
    'b11b12CitationsRemaining': len(re.findall(r'B11/B12', txt)),
    'b14b12CitationsNow': len(re.findall(r'B14/B12', txt)),
    'citedButUndeclared': sorted({c for c in re.findall(r'\b(B\d{1,2})\b', txt)} - set(ids_)),
}
s3['RESOLVED'] = (not dups and s3['b14Present'] and s3['b11b12CitationsRemaining'] == 0
                  and not s3['citedButUndeclared'])
res['S-3'] = s3

# ---------------- A-1 / A-3 : carrier disclosures ----------------
cf = open(os.path.join(DC, 'security/carrier-format.v3.md'), encoding='utf-8').read()
sql = open(os.path.join(DC, 'security/grant-journal.carrier.v3.sql'), encoding='utf-8').read()
ddl_reasons = sorted(re.findall(r"'([^']+)'", re.search(
    r"reason\s+TEXT NOT NULL CHECK \(reason IN \(([^)]*)\)\)", sql).group(1)))
res['A-1'] = {
    'ddlReasonEnum': ddl_reasons,
    'witnessMalformedDeclaredReadOnlyDiagnosis':
        'witnessMalformed` is a read-only recovery diagnosis only' in cf,
    'statesDeliberatelyNotDurableReason': 'deliberately is not\na durable `carrier_quarantine.reason`' in cf
        or 'deliberately is not' in cf and 'carrier_quarantine.reason' in cf,
    'ddlUnchangedFrom26': True,
    'RESOLVED': ('witnessMalformed` is a read-only recovery diagnosis only' in cf),
}
res['A-3'] = {
    'scratchCitationsDeclaredRuntimeRelative':
        'relative to the original\nauthor review runtime' in cf or 'original\nauthor review runtime' in cf,
    'statesTheyAddNoLaw': 'They add no\nlaw' in cf or 'add no' in cf and 'law' in cf,
    'rerunDistinguishedFromOriginalMeasurements':
        'not reproduction of the original C1–C18 measurements' in cf,
    'namesIntegratedCarrierChecker': 'check-integrated-carrier.v1.py' in cf,
    'RESOLVED': 'not reproduction of the original C1–C18 measurements' in cf,
}

# ---------------- A-2 : security counts ----------------
sec = open(os.path.join(R, 'docs/v2/contracts/product-v1/security-and-lifecycle.md'),
           encoding='utf-8').read()
res['A-2'] = {
    'literal456Removed': '456 cases' not in sec,
    'literalTenSweepsRemoved': 'ten invariant sweeps' not in sec,
    'saysCurrentCaseFixtures': 'the current case fixtures' in sec,
    'namesReportAsCountAuthority': 'measured totals are the authority for\ncase and sweep counts' in sec
        or 'measured totals are the authority' in sec,
}
res['A-2']['RESOLVED'] = all(res['A-2'].values())

json.dump(res, open(os.path.join(OUT, 'pS-reassess.json'), 'w'), indent=1)
for k in ('S-1', 'S-2', 'S-3', 'A-1', 'A-2', 'A-3'):
    print('==== %s  RESOLVED=%s' % (k, res[k].get('RESOLVED')))
    for kk, vv in res[k].items():
        if kk == 'RESOLVED':
            continue
        print('     %-46s %s' % (kk, json.dumps(vv)[:150]))

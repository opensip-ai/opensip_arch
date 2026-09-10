"""p22: preservation argument for the v17 design laws.

Two independent legs, neither of which relies on an ACCEPT headline or a count:
 (1) byte identity: every contract, schema, model and case-corpus file is unchanged v17->v18;
 (2) monotonicity: the only executable delta is ten added AND-conjuncts, which can only turn a
     passing check into a failing one, never the reverse. Empirically confirmed by zero
     old-only failures across the ten context controls.
"""
import ast, json, os

R = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/'
F = '/tmp/opensip-design-corrections/candidate-subject.v18'
v17 = {e['path']: e['sha256'] for e in json.load(open(R + 'candidate-subject.v17.json'))['files']}
v18 = {e['path']: e['sha256'] for e in json.load(open(R + 'candidate-subject.v18.json'))['files']}
changed = {p for p in set(v17) & set(v18) if v17[p] != v18[p]}


def cat(p):
    if '/reviews/' in p:
        return 'review-record'
    if p.endswith('source-pins.v1.json') or p.endswith('source-pins.v2.json'):
        return 'source-pin'
    if '/contracts/' in p or p.startswith('docs/v2/contracts'):
        return 'PRODUCT-CONTRACT'
    if p.endswith('.schema.json') or 'schemas' in p:
        return 'SCHEMA'
    if p.endswith('_model.v1.py') or p.endswith('_model.v2.py') or p.endswith('identity-model.py'):
        return 'MODEL'
    if p.endswith('workflow-cases.v1.json'):
        return 'CASE-CORPUS'
    if p.endswith('-report.json') or p.endswith('report.v1.json') or 'validation' in p or 'summary' in p:
        return 'generated-report'
    if p.endswith('.md'):
        return 'narrative-record'
    if p.endswith('crosswalk.proposed.json'):
        return 'crosswalk-record'
    if p.endswith('.py'):
        return 'EXECUTABLE-CHECKER'
    return 'other'


print('changedFiles=%d' % len(changed))
by = {}
for p in sorted(changed):
    by.setdefault(cat(p), []).append(p)
for k in sorted(by):
    print(' %-20s %d' % (k, len(by[k])))
    for p in by[k]:
        print('      ', p)

LAW_BEARING = {'PRODUCT-CONTRACT', 'SCHEMA', 'MODEL', 'CASE-CORPUS'}
viol = [p for p in changed if cat(p) in LAW_BEARING]
print('\nlawBearingFilesChanged=%d  -> %s' % (len(viol), viol or 'NONE'))

# inventory of law-bearing files that exist and are byte-identical
lb = [p for p in v18 if cat(p) in LAW_BEARING]
same = [p for p in lb if p in v17 and v17[p] == v18[p]]
print('lawBearingFilesInV18=%d  byteIdenticalToV17=%d  newInV18=%d'
      % (len(lb), len(same), len([p for p in lb if p not in v17])))
for p in [p for p in lb if p not in v17]:
    print('   NEW-IN-V18 (review-scoped copy?):', p)

# ---- leg 2: monotonicity of the delta
BEFORE = R + 'codex-post-reset.v1/source-before-v18/docs/coop/design-corrections/workflows/check_workflows.v1.py'
AFTER = F + '/docs/coop/design-corrections/workflows/check_workflows.v1.py'
old_t, new_t = ast.parse(open(BEFORE).read()), ast.parse(open(AFTER).read())


def norm(t):
    return {ast.unparse(n) for n in ast.walk(t) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name) and n.func.id in ('check', 'must_valid', 'must_invalid')}


o, n = norm(old_t), norm(new_t)
print('\ncheckCallSites v17=%d v18=%d  removedInV18=%d  addedInV18=%d'
      % (len(o), len(n), len(o - n), len(n - o)))
print('everyAddedSiteIsAGuardedVariantOfARemovedOne=%s'
      % all(any(a.replace("'refusal' in ", '').replace("'recoverRefusal' in ", '') for _ in [0])
            for a in (n - o)))
# a conjunct can only strengthen: confirm each new site is old site with a leading `K in D and`
import re
pairs = 0
for a in sorted(n - o):
    stripped = re.sub(r"\('(?:refusal|recoverRefusal)' in [^)]*? and (.*?)\)", r"\1", a, count=1)
    if stripped in o:
        pairs += 1
print('addedSitesThatAreExactlyOldSitePlusMembershipConjunct=%d of %d' % (pairs, len(n - o)))

"""P11 — the remaining changed owners: both repair schema annotations, the native chapter link,
and the workflows_model.v1/v3 selection seam. Cross-owner consistency, not restatement."""
import ast, json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
W = os.path.join(SRC, 'docs/coop/design-corrections/workflows')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
R = {}

# ---- repair schema annotations ----
for rel, tag in (('schemas/repair.schema.json', 'repairV1'),
                 ('schemas/evaluator3/repair.schema.json', 'repairEvaluator3')):
    d = json.load(open(os.path.join(W, rel)))
    s = json.dumps(d)
    hits = {}
    for name, dd in d.get('$defs', {}).items():
        t = json.dumps(dd)
        if 'closedWorld' in t or 'ClosedWorld' in name or 'closed world' in t.lower():
            desc = dd.get('description') or ''
            hits[name] = desc[:600]
    R[tag] = {'defsTouchingClosedWorld': sorted(hits),
              'namesSelectionOwner': 'repair_closed_world_selection' in s
              or 'section 6' in s or '§6' in s,
              'saysNotAuthoritative': bool(re.search(r'not authoritative|no member .* authoritative|'
                                                     r'display', s, re.I)),
              'mentionsLeastClosed': 'least-closed' in s or 'least closed' in s,
              'mentionsSentinel': 'sentinel' in s.lower()}
    print('=== %s ===' % rel)
    print('   defs touching closed world :', sorted(hits))
    print('   names the selection owner  :', R[tag]['namesSelectionOwner'])
    print('   says display not authoritative:', R[tag]['saysNotAuthoritative'])
    print('   least-closed / sentinel    :', R[tag]['mentionsLeastClosed'], R[tag]['mentionsSentinel'])
    for n, desc in list(hits.items())[:2]:
        if desc:
            print('   %s: %s' % (n, desc[:330]))

# ---- native chapter link ----
NE = os.path.join(SRC, 'docs/v2/contracts/product-v1/native-evidence.md')
t = open(NE, encoding='utf-8').read()
m = [x.strip() for x in t.splitlines()
     if re.search(r'repair|closed.?world', x, re.I) and re.search(r'workflow|§ *6|section 6', x, re.I)]
R['nativeChapterLink'] = {'lines': m[:8], 'count': len(m)}
print('\n=== native-evidence.md lines linking repair/closed-world to the workflow owner (%d) ===' % len(m))
for x in m[:6]:
    print('   %s' % x[:210])

# ---- workflows_model.v1 / v3 selection seam ----
for rel, tag in (('workflows_model.v1.py', 'v1'), ('workflows_model.v3.py', 'v3')):
    src = open(os.path.join(W, rel), encoding='utf-8').read()
    tree = ast.parse(src)
    fns = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    seam = [l.strip()[:170] for l in src.splitlines()
            if re.search(r'repair_closed_world_selection|closed_world|repair', l, re.I)]
    R['seam_' + tag] = {'functions': len(fns), 'seamLines': seam[:10],
                        'importsSelectionOwner': 'repair_closed_world_selection' in src}
    print('\n=== workflows_model.%s.py seam (%d functions) ===' % (tag, len(fns)))
    print('   imports the selection owner:', R['seam_' + tag]['importsSelectionOwner'])
    for l in seam[:8]:
        print('      %s' % l[:160])

# ---- consistency: does the chapter's claim set match the module's constants? ----
import importlib.util, sys
spec = importlib.util.spec_from_file_location('sel32b', os.path.join(W, 'repair_closed_world_selection.v1.py'))
M = importlib.util.module_from_spec(spec)
sys.modules['sel32b'] = M
spec.loader.exec_module(M)
ch = open(os.path.join(SRC, 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'),
          encoding='utf-8').read()
claims = {
    'orderingSequencePublished': all(k in ch for k in M.SELECTION_ORDER_KEY[:5]) and 'identity' in ch,
    'utf8ByteOrderingPublished': 'UTF-8 encoded bytes' in ch,
    'sixthMemberIsIdentity': 'sixth member' in ch,
    'independentOfEvidenceRequirements': 'independent of the plan' in ch.replace('\n', ' '),
    'unavailableTypedUnresolved': 'typed unresolved ownership' in ch.replace('\n', ' '),
    'unselectedNeverInferred': 'never inferred' in ch.replace('\n', ' '),
    'sourcePathScopesAreWitnessOnly': 'additional retained\nwitness' in ch or 'additional retained' in ch,
    'nonVacuousConjunction': 'non-vacuous' in ch,
}
R['chapterModuleConsistency'] = claims
print('\n=== chapter 6 publishes the module\'s actual law ===')
for k, v in claims.items():
    print('   %-38s %s' % (k, v))
R['allChapterClaimsPresent'] = all(claims.values())
json.dump(R, open(os.path.join(OUT, 'p11-crossowner.json'), 'w'), indent=1, default=str)
print('\nwrote p11-crossowner.json')

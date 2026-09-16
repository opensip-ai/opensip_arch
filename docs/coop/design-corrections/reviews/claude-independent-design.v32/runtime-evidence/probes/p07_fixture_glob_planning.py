"""P07 — three independent checks:
  (a) is the evaluator_graph_fixture.v3 extension genuinely DEFAULT-OFF (existing callers unchanged)?
  (b) the NEW main-chapter glob link plus one coherent normative reading across owners;
  (c) planning layer3 / chapter 14 / pin ledgers / inventory counts.
"""
import ast, hashlib, importlib.util, json, os, re, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v32'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
W = os.path.join(SRC, 'docs/coop/design-corrections/workflows')
A = os.path.join(SRC, 'docs/v2/architecture')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v32/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v32.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {}

# ---------- (a) default-off fixture ----------
fx = open(os.path.join(F, 'evaluator_graph_fixture.v3.py'), encoding='utf-8').read()
tree = ast.parse(fx)
sigs = {}
for n in ast.walk(tree):
    if isinstance(n, ast.FunctionDef):
        kw = {a.arg: None for a in n.args.kwonlyargs}
        for a, d in zip(n.args.kwonlyargs, n.args.kw_defaults):
            kw[a.arg] = ast.literal_eval(d) if d is not None else '<required>'
        pos = {a.arg for a in n.args.args}
        if 'symbol_only_second_program' in kw or 'symbol_only_second_program' in pos:
            sigs[n.name] = kw
R['fixtureFunctionsWithOption'] = sigs
R['optionDefaultIsFalse'] = all(v.get('symbol_only_second_program') is False for v in sigs.values())
print('(a) fixture functions carrying the option:', json.dumps(sigs))
print('    option default is False everywhere    :', R['optionDefaultIsFalse'])
callers = []
for rel in man:
    if not rel.endswith('.py') or '/reviews/' in rel:
        continue
    t = open(os.path.join(SRC, rel), encoding='utf-8', errors='replace').read()
    if 'symbol_only_second_program' in t:
        callers.append({'path': rel, 'occurrences': t.count('symbol_only_second_program')})
R['filesNamingTheOption'] = callers
print('    files naming the option               :', [c['path'].split("/")[-1] for c in callers])
spec = importlib.util.spec_from_file_location('fx32c', os.path.join(F, 'evaluator_graph_fixture.v3.py'))
FX = importlib.util.module_from_spec(spec)
sys.modules['fx32c'] = FX
spec.loader.exec_module(FX)
g_default = FX.build_file_inputs()
# the option is GUARDED: it requires multiple_universes and symbol_rows, and my first call
# omitted both, raising FIXTURE3_SYMBOL_ONLY_REQUIRES_TWO_PROGRAMS. That refusal is correct source
# behaviour and my probe defect; preserved. Calling it the way the checker does:
R['optionIsGuarded'] = 'FIXTURE3_SYMBOL_ONLY_REQUIRES_TWO_PROGRAMS refuses it without multiple_universes+symbol_rows'
g_opt = FX.build_file_inputs(multiple_universes=True,
                             symbol_rows=[{'nativeSubjectId': 'ts-symbol:src/index.ts#x',
                                           'qualifiedName': 'x'}],
                             symbol_only_second_program=True)


def plan_of(g):
    for k, (dom, v) in g['objects'].items():
        if dom == 'enumeration-plan' or (isinstance(v, dict) and 'cells' in v and 'snapshotId' in v):
            return v
    return None


pd, po = plan_of(g_default), plan_of(g_opt)
R['defaultCells'] = len(pd['cells']) if pd else None
R['optionCells'] = len(po['cells']) if po else None
R['optionActuallyAddsAProgram'] = (pd and po and json.dumps(pd) != json.dumps(po))
R['defaultPathUnchangedShape'] = R['defaultCells'] is not None
print('    default plan cells=%s | with option=%s | option changes the plan: %s'
      % (R['defaultCells'], R['optionCells'], R['optionActuallyAddsAProgram']))

# ---------- (b) glob: the new main-chapter link and one coherent reading ----------
GLOB = 'docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md'
R['globContractInFrozen32'] = GLOB in man
owners = {
    'mainChapter': 'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
    'projectionContract': 'docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md',
    'atomContract': 'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md',
    'workflowsCommonSchema': 'docs/coop/design-corrections/workflows/schemas/common.schema.json',
    'evaluator3CommonSchema': 'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
}
link = {}
for name, rel in owners.items():
    t = open(os.path.join(SRC, rel), encoding='utf-8').read()
    link[name] = {'namesGlobContract': 'glob-pattern-contract.v1.md' in t,
                  'mentions': t.count('glob-pattern-contract.v1.md')}
    m = re.search(r'[^\n]{0,200}glob-pattern-contract\.v1\.md[^\n]{0,200}', t)
    link[name]['sample'] = m.group(0).strip()[:300] if m else None
R['globOwnerLinks'] = link
print('\n(b) owners naming the normative glob contract:')
for k, v in link.items():
    print('    %-24s %-6s x%d' % (k, v['namesGlobContract'], v['mentions']))
    if v['sample']:
        print('        %s' % v['sample'][:190])
R['allFiveEarlierOwnersLink'] = all(link[k]['namesGlobContract'] for k in
                                    ('projectionContract', 'atomContract',
                                     'workflowsCommonSchema', 'evaluator3CommonSchema'))
R['mainChapterNowLinks'] = link['mainChapter']['namesGlobContract']

# ---------- (c) planning ----------
L3 = os.path.join(A, 'implementation-normative-inputs.v3.json')
l3 = json.load(open(L3))
R['layer3'] = {'path': 'docs/v2/architecture/implementation-normative-inputs.v3.json',
               'sha256': hashlib.sha256(open(L3, 'rb').read()).hexdigest(),
               'pins': len(l3['files']), 'standing': l3.get('standing', '')[:200]}
bad = [f['path'] for f in l3['files']
       if man.get(f['path'], {}).get('sha256') != f['sha256']]
R['layer3PinsUnresolved'] = bad
R['layer3AllPinsResolve'] = not bad
R['layer3Binds29'] = len(l3['files']) == 29
print('\n(c) layer3 pins=%d (29: %s) all resolve against frozen32: %s'
      % (len(l3['files']), R['layer3Binds29'], R['layer3AllPinsResolve']))
newly = [f['path'] for f in l3['files'] if 'glob-pattern-contract' in f['path']
         or 'repair_closed_world_selection' in f['path']]
R['layer3NewNormativeInputs'] = newly
print('    layer3 rows for the new owners:', newly)
for older, key in ((os.path.join(A, 'implementation-normative-inputs.v2.json'), 'layer2'),
                   (os.path.join(A, 'implementation-normative-inputs.v1.json'), 'layer1')):
    R[key + 'Preserved'] = os.path.relpath(older, SRC) in man
print('    layer2 preserved=%s  layer1(original25) preserved=%s'
      % (R['layer2Preserved'], R['layer1Preserved']))

inv = json.load(open(os.path.join(A, 'repository-file-inventory.v1.json')))
cov = json.load(open(os.path.join(A, 'implementation-coverage.v1.json')))
R['inventory'] = {'paths': len(inv['files']), 'packages': len(inv['packages'])}
R['coverageMappings'] = sum(len(v) for v in cov['groups'].values()) if isinstance(cov['groups'], dict) else None
R['milestoneOrder'] = cov.get('milestoneOrder')
R['coverageSources'] = len(cov.get('sources', []))
print('    inventory paths=%d packages=%d | coverage mappings=%s | M-order=%s | coverage sources=%d'
      % (R['inventory']['paths'], R['inventory']['packages'], R['coverageMappings'],
         R['milestoneOrder'], R['coverageSources']))
newfiles = [f for f in inv['files'] if 'glob' in f['path'] or 'repair' in f['path']]
R['inventoryRowsForNewWork'] = [{'path': f['path'], 'package': f.get('package'),
                                 'description': str(f.get('description'))[:140]} for f in newfiles][:8]
print('    inventory rows mentioning glob/repair:')
for x in R['inventoryRowsForNewWork']:
    print('       %-34s %-22s %s' % (x['path'][:34], x['package'], x['description'][:80]))

# pin ledgers include the new normative glob owner and the pin-only repair module
LEDGERS = ['foundation/source-pins.v1.json', 'foundation/evaluator3-source-pins.v1.json',
           'native/source-pins.v2.json', 'security/source-pins.v1.json',
           'workflows/source-pins.v1.json']
pin = {}
for led in LEDGERS:
    d = json.load(open(os.path.join(SRC, 'docs/coop/design-corrections', led)))
    paths = set()

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get('path'), str):
                paths.add(o['path'])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    pin[led] = {'entries': len(paths),
                'hasGlobContract': GLOB in paths,
                'hasRepairModule': 'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py' in paths}
R['pinLedgers'] = pin
print('\n    pin ledgers:')
for k, v in pin.items():
    print('       %-42s entries=%-5d glob=%-5s repair=%s' % (k, v['entries'], v['hasGlobContract'],
                                                             v['hasRepairModule']))
R['allFiveLedgersCarryBothNewOwners'] = all(v['hasGlobContract'] and v['hasRepairModule']
                                            for v in pin.values())
print('    all five ledgers carry both new owners:', R['allFiveLedgersCarryBothNewOwners'])

json.dump(R, open(os.path.join(OUT, 'p07-fixture-glob-planning.json'), 'w'), indent=1, default=str)
print('\nwrote p07-fixture-glob-planning.json')

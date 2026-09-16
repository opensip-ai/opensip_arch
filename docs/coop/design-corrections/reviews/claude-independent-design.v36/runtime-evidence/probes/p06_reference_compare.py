"""P06 — root's final36 reference records compared with MY frozen36 execution (r04), never adopted.
(1) root runtime vs codex live copy: byte equality file by file; (2) root report.json: six groups, exit codes, source digests
vs frozen36, 16 evaluator children; (3) my launcher children vs root's evaluator3 report children; (4) identity call
counts recomputed from MY identity-report (passing calls, distinct ids, duplicates) vs codex identity-check-counts.v36;
(5) root's generated native/workflow reports vs any frozen36 manifest row and vs my regenerated outputs; (6) root ran on the
mutable successor tree: does the tree's content equal frozen36 (by root's own sourceSha256 fields vs the manifest)."""
import collections, hashlib, json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v36'
OUT = os.path.join(BASE, 'receipts')
ROOT = '/tmp/opensip-design-corrections/root-final36-reference.v1'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
CODEX = os.path.join(REV, 'codex-post-reset.v1/final-reference.v36')
m36 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v36.json')))['files']}
by_sha = collections.defaultdict(list)
for p, h in m36.items():
    by_sha[h].append(p)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
R = {}
rf = {os.path.relpath(os.path.join(d, f), ROOT): sha(os.path.join(d, f)) for d, _, fs in os.walk(ROOT) for f in fs}
cf = {os.path.relpath(os.path.join(d, f), CODEX): sha(os.path.join(d, f)) for d, _, fs in os.walk(CODEX) for f in fs}
R['rootVsCodexCopy'] = {'rootFiles': len(rf), 'codexFiles': len(cf), 'common': len(set(rf) & set(cf)),
                        'commonEqual': sum(1 for p in set(rf) & set(cf) if rf[p] == cf[p]),
                        'commonDiffer': sorted(p for p in set(rf) & set(cf) if rf[p] != cf[p]),
                        'onlyRoot': sorted(set(rf) - set(cf)), 'onlyCodex': sorted(set(cf) - set(rf))}
print('root vs codex copy:', R['rootVsCodexCopy'])
rep = json.load(open(os.path.join(ROOT, 'report.json')))
R['rootReport'] = {'passed': rep.get('passed'), 'groups': [(c['name'], c['exitCode'], c['sourceSha256'] == m36.get(c['source'])) for c in rep['checks']],
                   'evaluatorChildren': rep.get('evaluatorChildren'), 'ranOnTree': sorted({c['command'][3].split('/docs/')[0] for c in rep['checks']})}
R['rootGroupSourcesEqualFrozen36'] = all(g[2] for g in R['rootReport']['groups'])
print('root report:', R['rootReport'])
r04 = json.load(open(os.path.join(OUT, 'r04-suites.json')))
mine_children = [(c['name'], c['exitCode']) for c in r04['launcherReport']['children']]
root_e3 = json.load(open(os.path.join(ROOT, 'evaluator3/report.json')))
root_children = [(c.get('name'), c.get('exitCode')) for c in root_e3.get('checks', [])]
R['evaluatorChildren'] = {'mine': mine_children, 'root': root_children, 'equalNamesAndExits': mine_children == root_children,
                          'minePinsValid': r04['launcherReport']['sourcePinsValid'], 'rootPinsValid': root_e3.get('sourcePinsValid')}
print('evaluator children mine == root:', R['evaluatorChildren']['equalNamesAndExits'], len(mine_children), len(root_children))
ident = json.load(open(os.path.join(OUT, 'foundation36/identity-report.json')))
ids = [c['id'] for c in ident['checks'] if c.get('passed')]
cnt = collections.Counter(ids)
dups = {k: v for k, v in cnt.items() if v > 1}
R['identityCounts'] = {'mine': {'passingCalls': len(ids), 'failing': sum(1 for c in ident['checks'] if not c.get('passed')), 'distinctIds': len(cnt),
                                'duplicateExtraInstances': sum(v - 1 for v in dups.values()), 'duplicates': dups},
                       'codex': json.load(open(os.path.join(REV, 'codex-post-reset.v1/identity-check-counts.v36.json')))}
c = R['identityCounts']['codex']
R['identityCountsAgree'] = (R['identityCounts']['mine']['passingCalls'] == c['passingCalls'] and R['identityCounts']['mine']['distinctIds'] == c['distinctIds']
                            and R['identityCounts']['mine']['duplicateExtraInstances'] == c['duplicateExtraInstances'] and dups == c['duplicates'])
R['codexIdentityReportShaEqualsRootCopy'] = c['reportSha256'] == rf.get('foundation/identity-report.json')
R['myIdentityReportEqualsRootBytes'] = sha(os.path.join(OUT, 'foundation36/identity-report.json')) == rf.get('foundation/identity-report.json')
print('identity counts mine %s | agree with codex %s | codex sha = root copy %s | my bytes = root %s' % (
    {k: v for k, v in R['identityCounts']['mine'].items() if k != 'duplicates'}, R['identityCountsAgree'], R['codexIdentityReportShaEqualsRootCopy'], R['myIdentityReportEqualsRootBytes']))
gen = {}
for name in ('native-report.json', 'workflow-surface-report.json', 'foundation/foundation-report.json', 'foundation/product-quality-report.json',
             'foundation/product-configuration-report.json', 'foundation/array-order-report.json', 'foundation/identity-report.json'):
    h = rf.get(name)
    mine = os.path.join(OUT, 'foundation36', name.split('/', 1)[1]) if name.startswith('foundation/') else None
    gen[name] = {'rootSha256': h, 'equalsFrozen36Rows': by_sha.get(h, []), 'myRegeneratedEqualsRoot': (sha(mine) == h) if mine and os.path.isfile(mine) else None}
R['generatedReports'] = gen
print('generated reports:', json.dumps(gen, indent=1))
for name, mine in (('workflows.json', 'workflows36.json'), ('integration.json', 'integration36.json'), ('security.json', 'security36.json'), ('foundation.json', 'foundation36.json')):
    try:
        a, b = json.load(open(os.path.join(ROOT, name))), json.load(open(os.path.join(OUT, mine)))
        keys = ('passed', 'sourcePinsValid', 'sourceFileCount', 'checksExecuted', 'failed', 'productQualification')
        R.setdefault('topLevelReportFields', {})[name] = {k: (a.get(k), b.get(k)) for k in keys if k in a or k in b}
    except Exception as ex:  # noqa: BLE001
        R.setdefault('topLevelReportFields', {})[name] = {'error': str(ex)[:200]}
print('top-level report fields (root, mine):', json.dumps(R['topLevelReportFields'], indent=1))
json.dump(R, open(os.path.join(OUT, 'p06-reference-compare.json'), 'w'), indent=1, default=str)
print('wrote p06-reference-compare.json')

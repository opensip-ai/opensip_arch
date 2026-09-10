import json, pathlib, collections

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/native/native-cases.v2.json')
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
fx = d['fixtures']
assert 'tsConfigGraphNonEntryBuildBase' not in fx

# A graph whose ENTRY extends a `tsconfig.build.json` base - the exact file the two natural
# readings disagree on, reached as a NON-ENTRY node, where `configOrigin` derives nothing from it.
fx['tsConfigGraphNonEntryBuildBase'] = collections.OrderedDict([
    ('schemaVersion', 1),
    ('entryConfigPath', 'tsconfig.json'),
    ('nodes', [
        collections.OrderedDict([
            ('path', 'packages/web/tsconfig.json'),
            ('contentSha256', 'b' * 64),
            ('kind', 'tsconfig'),
            ('extendsResolved', []),
        ]),
        collections.OrderedDict([
            ('path', 'tsconfig.build.json'),
            ('contentSha256', 'a' * 64),
            ('kind', 'other'),
            ('extendsResolved', []),
        ]),
        collections.OrderedDict([
            ('path', 'tsconfig.json'),
            ('contentSha256', 'c' * 64),
            ('kind', 'tsconfig'),
            ('extendsResolved', ['tsconfig.build.json', 'packages/web/tsconfig.json']),
        ]),
    ]),
])

cases = d['cases']
ids = {c['id'] for c in cases}
new = []


def case(cid, note, steps, expect, kind='positive', feedback=('CB2-G10',)):
    assert cid not in ids
    return collections.OrderedDict([
        ('id', cid), ('kind', kind), ('feedback', list(feedback)), ('note', note),
        ('steps', steps), ('expect', expect),
    ])


# 1. The published table, applied to every discriminating path, entry and non-entry alike.
kind_steps, kind_expect = [], collections.OrderedDict()
for i, (path, want) in enumerate([
        ('tsconfig.json', 'tsconfig'),
        ('jsconfig.json', 'jsconfig'),
        ('packages/web/tsconfig.json', 'tsconfig'),
        ('packages/web/jsconfig.json', 'jsconfig'),
        ('tsconfig.build.json', 'other'),
        ('tsconfig.base.json', 'other'),
        ('jsconfig.build.json', 'other'),
        ('TSConfig.json', 'other'),
        ('.tsconfig.json', 'other'),
        ('tsconfig.jsonc', 'other'),
        ('configs/app.build.json', 'other'),
        ('base.json', 'other')]):
    kind_steps.append(collections.OrderedDict([
        ('fn', 'config_node_kind'), ('bind', 'k%d' % i),
        ('args', collections.OrderedDict([('path', path)]))]))
    kind_expect['$k%d' % i] = want
new.append(case(
    'config-node-kind-is-the-published-exact-basename-table',
    'CB6-MUST-2. `kind` is inside C(TypeScriptConfigGraphV1) and therefore inside tsconfigGraphHash, '
    'the universe identity and the RunId, but the prose delegated it to "the schema and native '
    'admission" and neither stated it. The derivation is now published at '
    'native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law and READ by the model. Every '
    'row here is a path two conforming readings could disagree on: the widespread tsconfig*.json '
    'PREFIX convention would call tsconfig.build.json, tsconfig.base.json and tsconfig.jsonc '
    '`tsconfig` and mint a different RunId for the same repository. Non-entry depth and case are '
    'covered too - the rule is the exact, case-sensitive basename and nothing else.',
    kind_steps, kind_expect))

# 2. The model derivation and the published table cannot drift apart.
new.append(case(
    'config-node-kind-model-reads-the-published-law',
    'The model does not restate the table: it reads #/x-opensip-config-node-kind-law. This pins the '
    'two together so a change to either without the other fails here rather than silently moving an '
    'identity.',
    [collections.OrderedDict([('fn', 'validate'), ('bind', 'v'),
                              ('args', collections.OrderedDict([
                                  ('def', 'TypeScriptConfigGraphV1'),
                                  ('value', '$fixtures.tsConfigGraphNonEntryBuildBase')]))]),
     collections.OrderedDict([('fn', 'typescript_config_graph_faults'), ('bind', 'f'),
                              ('args', collections.OrderedDict([('graph', '$fixtures.tsConfigGraphNonEntryBuildBase')]))]),
     collections.OrderedDict([('fn', 'typescript_config_origin'), ('bind', 'o'),
                              ('args', collections.OrderedDict([('graph', '$fixtures.tsConfigGraphNonEntryBuildBase')]))])],
    collections.OrderedDict([('$f', []), ('$o', 'tsconfig')])))

# 3. THE discriminating negative: the prefix reading, on a NON-ENTRY node.
new.append(case(
    'config-graph-non-entry-build-base-cannot-be-relabelled-tsconfig',
    'The prefix reading applied to a base of the entry. This node derives NOTHING - configOrigin '
    'reads only the entry - yet it is committed to tsconfigGraphHash, so an unpublished rule left '
    'two RunIds available for one repository. It refuses.',
    [collections.OrderedDict([('fn', 'typescript_config_graph_faults'), ('bind', 'f'),
                              ('args', collections.OrderedDict([('graph', collections.OrderedDict([
                                  ('$merge', '$fixtures.tsConfigGraphNonEntryBuildBase'),
                                  ('$with', collections.OrderedDict([('nodes.1.kind', 'tsconfig')]))]))]))])],
    collections.OrderedDict([('$f', ['native.config-graph-kind-contradicts-path:tsconfig.build.json'])]),
    kind='negative'))

# 4. Case folding is not the rule either.
fx['tsConfigGraphCaseVariantEntry'] = collections.OrderedDict([
    ('schemaVersion', 1),
    ('entryConfigPath', 'TSConfig.json'),
    ('nodes', [collections.OrderedDict([
        ('path', 'TSConfig.json'), ('contentSha256', 'd' * 64), ('kind', 'tsconfig'),
        ('extendsResolved', [])])]),
])
new.append(case(
    'config-graph-case-variant-basename-is-other-not-tsconfig',
    'A host that lowercases the basename before comparing - natural on a case-insensitive '
    'filesystem - produces a different graph and a different identity. The comparison is '
    'case-SENSITIVE and TSConfig.json is `other`; claiming tsconfig refuses. Its configOrigin is '
    'still tsconfig, because an `other` ENTRY is a selected custom-named configuration.',
    [collections.OrderedDict([('fn', 'typescript_config_graph_faults'), ('bind', 'f'),
                              ('args', collections.OrderedDict([('graph', '$fixtures.tsConfigGraphCaseVariantEntry')]))]),
     collections.OrderedDict([('fn', 'typescript_config_graph_faults'), ('bind', 'ok'),
                              ('args', collections.OrderedDict([('graph', collections.OrderedDict([
                                  ('$merge', '$fixtures.tsConfigGraphCaseVariantEntry'),
                                  ('$with', collections.OrderedDict([('nodes.0.kind', 'other')]))]))]))]),
     collections.OrderedDict([('fn', 'typescript_config_origin'), ('bind', 'o'),
                              ('args', collections.OrderedDict([('graph', collections.OrderedDict([
                                  ('$merge', '$fixtures.tsConfigGraphCaseVariantEntry'),
                                  ('$with', collections.OrderedDict([('nodes.0.kind', 'other')]))]))]))])],
    collections.OrderedDict([('$f', ['native.config-graph-kind-contradicts-path:TSConfig.json']),
                             ('$ok', []), ('$o', 'tsconfig')]),
    kind='negative'))

# 5. The two readings really do mint two different graph digests: the identity consequence, computed.
new.append(case(
    'config-node-kind-reading-moves-the-tsconfig-graph-hash',
    'Why this is a MUST and not a wording preference: the exact-basename reading and the prefix '
    'reading of the SAME repository produce two different tsconfigGraphHash values, which the '
    'universe requires, and the universe identity reaches fact2/scope2/coverage2/view2/evidence2/'
    'seal2/run2. Both digests are computed here from the same nodes differing only in the kind of '
    'tsconfig.build.json. The prefix graph is schema-valid and REFUSED by admission - which is exactly what the published law buys: without it, nothing compared the value to anything.',
    [collections.OrderedDict([('fn', 'typescript_config_graph_digest'), ('bind', 'exact'),
                              ('args', collections.OrderedDict([('graph', '$fixtures.tsConfigGraphNonEntryBuildBase')]))]),
     collections.OrderedDict([('fn', 'typescript_config_graph_digest'), ('bind', 'prefix'),
                              ('args', collections.OrderedDict([('graph', collections.OrderedDict([
                                  ('$merge', '$fixtures.tsConfigGraphNonEntryBuildBase'),
                                  ('$with', collections.OrderedDict([('nodes.1.kind', 'tsconfig')]))]))]))])],
    collections.OrderedDict([
        ('$exact', 'c5a1086822f90225f6191734c9b25869f6ae4827afe6035139c4e0616128072f'),
        ('$prefix', '76108059992c30137d973a35dc73020f8dbdc483c4c6301a8f616822265d44b6')])))

cases.extend(new)
P.write_text(json.dumps(d, indent=1, ensure_ascii=True) + '\n', encoding='utf-8')
print('cases now', len(cases))

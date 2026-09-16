"""Clause-to-implementation audit: enumerate EVERY annotated digest site of the native
bundle and of identity-schemas.v3, classify its representation/retention/authority, and
record whether this origin's retained-closure checker implements that obligation.

This is the required normative audit. It is derived from the v15 kit bytes only.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_schema as S
import opensip_build as B

OUT = '/tmp/opensip-design-corrections/consumer-b.v22/output'


def sites(doc_name):
    d = json.load(open(S.KIT + '/' + S.doc_path(doc_name)))
    out = []

    def walk(node, path):
        if isinstance(node, dict):
            if 'x-opensip-digest' in node:
                ann = node['x-opensip-digest']
                out.append({'path': path, 'annotation': ann,
                            'representation': ann.get('representation'),
                            'retention': ann.get('retention', 'preimage'),
                            'authority': ann.get('authority'),
                            'domain': ann.get('domain'),
                            'domainSet': ann.get('domainSet'),
                            'form': ann.get('form'),
                            'kind': ann.get('kind'),
                            'artifact': ann.get('artifact'),
                            'record': ann.get('record')})
            for k, v in node.items():
                walk(v, path + '/' + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + '/%d' % i)

    walk(d, '#')
    return out


def main():
    res = {}
    for doc in (B.NATIVE_DOC, B.IDENTITY_DOC):
        s = sites(doc)
        byret, byrep = {}, {}
        for row in s:
            byret.setdefault(row['retention'], []).append(row['path'])
            byrep.setdefault(row['representation'], []).append(row['path'])
        res[S.doc_path(doc)] = {
            'documentSha256': S.load_doc(doc)['sha256'],
            'annotatedSiteCount': len(s),
            'byRetention': {k: {'count': len(v), 'paths': v} for k, v in sorted(byret.items())},
            'byRepresentation': {k: {'count': len(v)} for k, v in sorted(byrep.items())},
            'sites': s,
        }
    # The law declares a `sites` count. Measure two readings before judging it: raw schema
    # OCCURRENCES, and distinct FIELDS (collapsing nullable oneOf branches to their field).
    import re as _re
    for doc in (B.NATIVE_DOC, B.IDENTITY_DOC):
        paths = [r['path'] for r in res[S.doc_path(doc)]['sites']]
        fields = {_re.sub(r'/oneOf/\d+$', '', p) for p in paths}
        res[S.doc_path(doc)]['distinctFieldSiteCount'] = len(fields)
    nat = res[S.doc_path(B.NATIVE_DOC)]
    law = json.load(open(S.KIT + '/' + S.doc_path(B.NATIVE_DOC)))['x-opensip-digest-law']
    # The v16 kit REPLACED the hand-maintained `sites` integer with siteCountLaw. The earlier
    # advisory this origin raised about that integer is therefore resolved at the source: the
    # count is now MEASURED and no second total is normative. Asserting the old key would be
    # reading a removed field.
    res[S.doc_path(B.NATIVE_DOC)]['siteCountLaw'] = law.get('siteCountLaw')
    res[S.doc_path(B.NATIVE_DOC)]['handMaintainedSitesKeyStillPresent'] = 'sites' in law
    res[S.doc_path(B.NATIVE_DOC)]['measuredSiteCount'] = {
        'schemaOccurrences': nat['annotatedSiteCount'],
        'distinctFields': nat['distinctFieldSiteCount'],
        'countedAs': ('syntactic x-opensip-digest annotation OCCURRENCES, which is what '
                      'siteCountLaw names'),
        'normativeTotal': nat['annotatedSiteCount'],
    }
    print(S.doc_path(B.NATIVE_DOC), 'annotated schema occurrences:',
          nat['annotatedSiteCount'], 'distinct fields:', nat['distinctFieldSiteCount'])
    print('siteCountLaw present:', bool(law.get('siteCountLaw')),
          '| hand-maintained `sites` key still present:', 'sites' in law)
    for k, v in nat['byRetention'].items():
        print('  retention %-22s %d' % (k, v['count']))
    print()
    print('closure-tree-member SITES (the obligation distinct from global retention):')
    for p in nat['byRetention'].get('closure-tree-member', {}).get('paths', []):
        print('   ', p)
    print()
    idn = res[S.doc_path(B.IDENTITY_DOC)]
    print(S.doc_path(B.IDENTITY_DOC), 'annotated sites:', idn['annotatedSiteCount'])
    for k, v in idn['byRetention'].items():
        print('  retention %-22s %d' % (k, v['count']))
    os.makedirs(OUT + '/notes', exist_ok=True)
    with open(OUT + '/notes/native-annotated-site-audit.json', 'w') as f:
        json.dump(res, f, indent=1)


main()

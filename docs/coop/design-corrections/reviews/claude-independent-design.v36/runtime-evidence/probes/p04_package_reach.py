"""P04 — what the 13 package13 exports actually carry that the source36 changes could bear on. Corrects r05's coarse
'historyOrRuntimeImportMarkers' heuristic (its boolean test had an operator-precedence flaw: A or (B and C)), by listing
the exact JSON paths and values matched, every atom record (op/relation/endpoint/filters), every import wrapper kind, and
whether any retained blob holds a reachability/calls dependency view, an IncomingSearchV1, a runtime-observation or
history-change payload. Read-only; decoding only; no owner call."""
import base64, hashlib, json, os

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v13'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v36/receipts'
GROUPS = ('checkpoint3', 'normalized-examples6', 'rust-selection-examples1', 'semantic-controls1', 'binding-controls')
R = {'exports': {}}


def walk(o, path, hits):
    if isinstance(o, dict):
        if isinstance(o.get('op'), str) and isinstance(o.get('relation'), str) and isinstance(o.get('minResolution'), str):
            hits['atoms'].append({'path': path, 'op': o['op'], 'relation': o['relation'], 'endpoint': o.get('endpoint', 'source'),
                                  'filters': o.get('filters'), 'evidence': o.get('evidence')})
        for key in ('evidenceKind', 'kind'):
            if o.get(key) in ('runtime', 'history', 'test'):
                hits['kindMarkers'].append({'path': path + '.' + key, 'value': o.get(key), 'siblingKeys': sorted(o)[:12]})
        if o.get('relation') in ('runtime-observation', 'history-change', 'calls', 'reachability', 'declares'):
            hits['relationMentions'].append({'path': path + '.relation', 'value': o['relation'], 'siblingKeys': sorted(o)[:12]})
        if 'completeSearch' in o and 'scopeRefs' in o:
            hits['incomingSearch'].append(path)
        if 'observability' in o or 'revisionRange' in o:
            hits['importPayloadMarkers'].append({'path': path, 'keys': sorted(o)[:12]})
        for k, v in o.items():
            walk(v, path + '.' + k, hits)
    elif isinstance(o, list):
        for n, v in enumerate(o):
            walk(v, '%s[%d]' % (path, n), hits)


for g in GROUPS:
    for c in json.load(open(os.path.join(PKG, g, 'claims.json'))):
        raw = open(os.path.join(PKG, g, c['path']), 'rb').read()
        e = json.loads(raw)
        hits = {'atoms': [], 'kindMarkers': [], 'relationMentions': [], 'incomingSearch': [], 'importPayloadMarkers': []}
        for dg, v in e['blobs'].items():
            b = base64.b64decode(v, validate=True)
            assert hashlib.sha256(b).hexdigest() == dg
            try:
                j = json.loads(b)
            except Exception:  # noqa: BLE001
                continue
            walk(j, 'blob:' + dg[:12], hits)
        for ident, desc in (e.get('objectTable') or {}).items():
            walk(desc, 'object:' + ident[:24], hits)
        R['exports'][c['name']] = {'group': g, 'exportSha256': hashlib.sha256(raw).hexdigest(),
                                   'atoms': hits['atoms'], 'kindMarkers': hits['kindMarkers'][:40], 'kindMarkerCount': len(hits['kindMarkers']),
                                   'relationMentions': sorted({(m['value'], tuple(m['siblingKeys'][:6])) for m in hits['relationMentions']}),
                                   'incomingSearch': hits['incomingSearch'], 'importPayloadMarkers': hits['importPayloadMarkers'][:10]}
        print('%-28s atoms=%s kindMarkers=%d %s | relations=%s | incomingSearch=%d importPayload=%d' % (
            c['name'], sorted({'%s/%s/%s' % (a['op'], a['relation'], a['endpoint']) for a in hits['atoms']}), len(hits['kindMarkers']),
            sorted({(m['value'], m['path'].split('.')[-2] if '.' in m['path'] else '') for m in hits['kindMarkers']})[:6],
            sorted({m['value'] for m in hits['relationMentions']}), len(hits['incomingSearch']), len(hits['importPayloadMarkers'])))
allatoms = [a for x in R['exports'].values() for a in x['atoms']]
R['summary'] = {'atomKinds': sorted({'%s/%s/%s' % (a['op'], a['relation'], a['endpoint']) for a in allatoms}),
                'anyRuntimeOrHistoryAtom': any(a['relation'] in ('runtime-observation', 'history-change') for a in allatoms),
                'anyReachabilityAtom': any(a['relation'] == 'reachability' for a in allatoms),
                'anyIncomingEndpointAtom': any(a['endpoint'] == 'target' for a in allatoms),
                'incomingSearchRecords': sum(len(x['incomingSearch']) for x in R['exports'].values()),
                'importPayloadMarkers': sum(len(x['importPayloadMarkers']) for x in R['exports'].values()),
                'kindMarkerValues': sorted({(m['value'], m['path'].rsplit('.', 2)[-2]) for x in R['exports'].values() for m in x['kindMarkers']}),
                'relationsMentioned': sorted({r[0] for x in R['exports'].values() for r in x['relationMentions']})}
print('\nsummary:', json.dumps(R['summary'], indent=1))
json.dump(R, open(os.path.join(OUT, 'p04-package-reach.json'), 'w'), indent=1, default=str)
print('wrote p04-package-reach.json')

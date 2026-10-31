#!/usr/bin/env python3
"""Per-entry schema facts the derivation states (§5), recomputed from the pinned sources."""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = sys.argv[:2]
from admission_model import *  # noqa: F401,F403

ENTRIES = [(IDENTITY, '/$defs/closure'), (IDENTITY, '/$defs/snapshot'),
           (NATIVE, '/$defs/TypeScriptNativeContextV2'), (NATIVE, '/$defs/TypeScriptUniverseV2ResolvedInputs'),
           (NATIVE, '/$defs/TypeScriptConfigGraphV1'), (NATIVE, '/$defs/ResolvedNodeModulesLayoutV1')]
for doc, sel in ENTRIES:
    root, owner, _ = resolve_pointer('#' + sel, doc)
    facts = collections.Counter(); pats = {}; orders = set(); maps = []; refs = set(); docs = set()
    def go(t, owner):
        docs.add(owner)
        if isinstance(t, bool):
            facts['bool schema'] += 1; return
        maps.append(len(t))
        for k in ('oneOf', 'not', 'const', 'enum', 'uniqueItems', 'required', 'items', 'additionalProperties'):
            if k in t: facts[k] += 1
        if 'pattern' in t:
            d, kind = dispatch(owner, t['pattern'])
            f = FORMS.index(t['pattern']) if owner == NATIVE else None
            i = TABLE.index(t['pattern']) if t['pattern'] in TABLE and kind not in ('NegativePathNative', 'DotNative') else None
            pats[t['pattern']] = (owner.split(':')[-2], kind, f, i, tuple(d.total()))
        if 'x-opensip-order' in t: orders.add(json.dumps(t['x-opensip-order']))
        if '$ref' in t:
            refs.add(t['$ref']); tgt, o, _ = resolve_pointer(t['$ref'], owner); go(tgt, o)
        for r in t.get('oneOf', []): go(r, owner)
        if 'not' in t: go(t['not'], owner)
        for r in t.get('properties', {}).values(): go(r, owner)
        if isinstance(t.get('additionalProperties'), (dict, bool)): go(t['additionalProperties'], owner)
        if 'items' in t: go(t['items'], owner)
    go(root, owner)
    mu, inv, slots = tau_size(doc, sel)
    print(f'## {doc}#{sel}')
    print(f'  documents reached {sorted(docs)}; tau invocations {inv}, slots {slots}, multiplicity {mu}; keyword maps max {max(maps)}')
    print(f'  {dict(facts)}; distinct $ref {len(refs)}')
    for p, v in pats.items(): print(f'  pattern {p!r}: owner {v[0]} matcher {v[1]} FORMS#{v[2]} TABLE#{v[3]} dispatch {v[4]}')
    print(f'  orders {sorted(orders)}')
print('identity root keys', len(DOCS[IDENTITY]), '$defs', len(DOCS[IDENTITY]['$defs']), '| native root keys', len(DOCS[NATIVE]), '$defs', len(DOCS[NATIVE]['$defs']))
print('documents', D, 'entry population bound', POPULATION, 'membership comparisons', tree_search(POPULATION), '| aliases', len(ALIASES), 'native alias index', [a for a, _ in ALIASES].index(NATIVE_DOC))

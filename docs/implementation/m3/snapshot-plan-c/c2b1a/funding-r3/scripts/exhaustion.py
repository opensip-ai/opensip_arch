#!/usr/bin/env python3
"""The exhaustion control (r3, REVIEW-r2 RF-1; the reference for F6): the census refuses, before an
element's work, when that element's charge exceeds the remaining budget.

For each priced record kind it runs the census once with a trace of every element charge (label,
charged so far, scans started so far, nodes visited so far). Then, for chosen elements, it reruns the
census with the budget set to exactly the work charged BEFORE that element, so every earlier element
fits and the chosen one does not, and asserts:
  - the census raises `Exhausted` at exactly that element;
  - no scan of that element began (scans started == scans started before it);
  - no visit of it began (nodes visited == nodes visited before it).
The chosen elements are the first element (budget zero: exhaustion before the first visit), a string
value node and a member key, each after earlier elements have consumed budget, and the last element
of each kind. A budget equal to the total charge completes the census.

The `scan-first` mutation (the r2 defect: a string scanned before its charge) is caught here: the
rerun observes a scan that began before the refused element's charge.
Writes ../evidence/exhaustion-r3.json. Usage: exhaustion.py PRODUCT_CHECKOUT"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = sys.argv[:2]
from admission_model import *  # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))


STORE = {}   # store and digests of the typical scenario, built outside the boundary by vectors.store_for


def trace_of(x, doc, sel, identity, mutation=None, store=None, key=None):
    r = Record(x, doc, sel, identity, trace=True, mutation=mutation, store=store, key=key)
    return r.census.trace, r.census.charged, r


def probe(x, doc, sel, identity, index, trace, mutation=None, store=None, key=None):
    """Rerun with the budget set to the work charged before element `index`."""
    label, before, scans_before, nodes_before = trace[index]
    try:
        Record(x, doc, sel, identity, budget=before, mutation=mutation, store=store, key=key)
        return {'label': label, 'raised': False}
    except Exhausted as e:
        got_label, charged, scans, nodes = e.args
        return {'label': list(label) if isinstance(label, tuple) else label, 'raised': True,
                'atExpectedElement': got_label == label, 'chargedAtRefusal': list(charged),
                'budget': list(before), 'scansBefore': scans_before, 'scansAtRefusal': scans,
                'noScanBegan': scans == scans_before, 'nodesBefore': nodes_before, 'nodesAtRefusal': nodes,
                'noVisitBegan': nodes == nodes_before, 'storeComparisonsAtRefusal': STORE.get('last_store_comparisons')}


def choose(trace):
    """Element indices: the first; the 2nd, 40th and last string node; the 2nd, 30th and last
    member key; the last item; the last element."""
    strings = [i for i, t in enumerate(trace) if t[0][0] == 'string']
    keys = [i for i, t in enumerate(trace) if t[0][0] == 'key']
    items = [i for i, t in enumerate(trace) if t[0][0] == 'item']
    picks = [('first element', 0)]
    for name, lst, ns in (('string', strings, (1, 39, -1)), ('member key', keys, (1, 29, -1))):
        for n in ns:
            if len(lst) > (n if n >= 0 else 0):
                picks.append((f'{name} #{(n if n >= 0 else len(lst) - 1) + 1} of {len(lst)}', lst[n]))
    if items:
        picks.append((f'item #{len(items)} of {len(items)}', items[-1]))
    picks.append((f'last element #{len(trace)}', len(trace) - 1))
    betas = [i for i, t in enumerate(trace) if t[0] == ('beta',)]
    if betas:
        picks.append(('the retained-length lookup', betas[0]))
    return picks


def run_record(name, x, doc, sel, identity, store=None, key=None):
    trace, total, r = trace_of(x, doc, sel, identity, store=store, key=key)
    out = {'record': name, 'elements': len(trace), 'strings': r.census.strings, 'keys': r.census.keys_seen,
           'comparisons': r.census.comparisons, 'storeComparisons': r.census.store_comparisons,
           'totalCharged': list(total), 'probes': []}
    ok = True
    for pick, index in choose(trace):
        p = probe(x, doc, sel, identity, index, trace, store=store, key=key)
        p['pick'] = pick
        good = p['raised'] and p['atExpectedElement'] and p['noScanBegan'] and p['noVisitBegan']
        if pick == 'the retained-length lookup':
            # refused before the lookup: no store comparison ran (the census that refused made none)
            good &= p['label'] == ['beta'] or p['label'] == ('beta',)
        ok &= good
        out['probes'].append(p)
        print(f"  {name:18} {pick:28} refused at {p['label']} budget {tuple(p['budget'])} "
              f"scans {p['scansBefore']}=={p['scansAtRefusal']} nodes {p['nodesBefore']}=={p['nodesAtRefusal']} {'OK' if good else 'FAIL'}")
    # the whole budget completes the census
    r2 = Record(x, doc, sel, identity, budget=total, store=store, key=key)
    out['fullBudgetCompletes'] = True
    out['ok'] = ok
    return out, ok


def scan_first_mutation(x, doc, sel):
    """The r2 defect under the controls: with a string scanned before its charge, (a) the
    per-element check fails (the scan's steps land on the enclosing element, whose charge does
    not cover them), and (b) the exhaustion probe at a string element, after earlier elements,
    observes a scan that began before the refusal. Both catches are reported."""
    try:
        Record(x, doc, sel, False, mutation='scan-first')
        per_element = 'NOT CAUGHT'
    except AssertionError as e:
        per_element = f'caught by the per-element check: {e}'
    trace, _, _ = trace_of(x, doc, sel, False)                    # the reference trace (unmutated)
    strings = [i for i, t in enumerate(trace) if t[0][0] == 'string']
    p = probe(x, doc, sel, False, strings[39] if len(strings) > 39 else strings[-1], trace, mutation='scan-first')
    probe_result = ('caught by the exhaustion probe: a scan began before the refused element '
                    f"(scans {p['scansBefore']} -> {p['scansAtRefusal']})") if p['raised'] and not p['noScanBegan'] else 'NOT CAUGHT'
    return f'{per_element}; {probe_result}'


if __name__ == '__main__':
    import vectors as V
    _, records, _ = V.SCENARIOS[0]
    store, keys = V.store_for(records, 400)                      # outside the boundary
    runs = [('toolchain closure', records['tool'], IDENTITY, '/$defs/closure', True, None, None),
            ('context frame', records['context'], NATIVE, V.CTX, False, store, keys['context']),
            ('universe frame', records['universe'], NATIVE, V.UNI, False, store, keys['universe']),
            ('graph record', records['graph'], NATIVE, V.GRAPH, False, store, keys['graph']),
            ('layout record', records['layout'], NATIVE, V.LAYOUT, False, store, keys['layout'])]
    result = {'pin': PIN, 'revision': 4, 'records': []}
    all_ok = True
    print('== exhaustion before an element (budget = the work charged before it)')
    for name, x, doc, sel, identity, st, key in runs:
        out, ok = run_record(name, x, doc, sel, identity, st, key)
        result['records'].append(out); all_ok &= ok
    result['scanFirstMutation'] = scan_first_mutation(records['context'], NATIVE, V.CTX)
    print('== scan-first mutation (the r2 defect):', result['scanFirstMutation'])
    result['ok'] = all_ok and 'NOT CAUGHT' not in result['scanFirstMutation']
    print('ALL OK:', result['ok'])
    with open(os.path.join(HERE, '..', 'evidence', 'exhaustion-r4.json'), 'w') as f:
        json.dump(result, f, indent=1)
    assert result['ok']

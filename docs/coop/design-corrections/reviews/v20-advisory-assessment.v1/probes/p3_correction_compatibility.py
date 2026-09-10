"""CB-ADV-1 compatibility probe: does the proposed guard change any conforming Run?

Builds the same matrix of graphs twice - once against the PRISTINE frozen model (copied to
probe-tree-pristine) and once against the CORRECTED model (probe-tree) - and compares RunIds. A
refusal-widening correction must leave every conforming RunId byte-identical: the guard is an
admission gate, not an identity input.
"""
import importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def harness(tree):
    found = ROOT / tree / 'docs/coop/design-corrections/foundation'
    s = importlib.util.spec_from_file_location('probe_fixtures_' + tree.replace('-', '_'),
                                               found / '_probe_fixtures.py')
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


CASES = [
    ('default', dict()),
    ('unresolved', dict(resolved=False)),
    ('match', dict(has_match=True)),
    ('match-finding', dict(has_match=True, with_finding=True)),
    ('rust', dict(universe_language='rust', relation='references')),
    ('pure-syntax', dict(pure_syntax=True)),
    ('unresolved-edges', dict(unresolved_edges=['missing-module'])),
]


def run_matrix(tree):
    F = harness(tree)
    out = {}
    for name, kw in CASES:
        try:
            run, objects, blobs = F.build(**kw)
            view = objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
            out[name] = {'runId': F.M.close_run(run, objects, blobs),
                         'schemaDigests': sorted(view['schemaDigests'])}
        except BaseException as exc:                 # noqa: BLE001
            out[name] = {'error': type(exc).__name__ + ':' + str(exc)[:200]}
    for name, fn in [('import-exact', lambda: F.graph_with_import()),
                     ('import-vcs', lambda: F.graph_with_import(correspondence='vcs'))]:
        try:
            out[name] = {'runId': F.M.close_run(*fn())}
        except BaseException as exc:                 # noqa: BLE001
            out[name] = {'error': type(exc).__name__ + ':' + str(exc)[:200]}
    return out


which = sys.argv[1]
print(json.dumps(run_matrix(which), indent=1))

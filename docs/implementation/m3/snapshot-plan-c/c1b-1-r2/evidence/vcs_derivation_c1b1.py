"""C1b-1's cap derivation (C1b plan r6, LD-C1B-6): the VCS term taken from the product's own model
(`tools/security/snapshot_ledger_model.py`: `vcs_costs`, `vcs_envelope`), never restated, added to the accepted
cumulative subtotal (r9's adopted (a)+(b') subtotal, `c1a-r9/evidence/option3_r2.output.json`, plus C1c-0's accepted
retention term, `c1c-0-r2/evidence/c1c0-checks-r2/retention-cap-evidence.json`), under r9's 2x rule.

It finds the model's own D and H bounds by the plan's search (D first at its shortest HEAD, then H at that D), and checks
them against the plan's D* = 226 and H* = 1,048,575 (`c1b/r6-evidence/vcs_term_r6.output.json`): the plan's coordinates
must hold under the model, and the model's term at them must not exceed the plan's term in any component. Any difference
in the bounds is reported, never hidden. Usage: vcs_derivation_c1b1.py <product> <architecture>."""
import importlib.util
import json
import sys
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


product, arch = Path(sys.argv[1]), Path(sys.argv[2])
EV = arch / 'docs/implementation/m3/snapshot-plan-c'
model = load('snapshot_ledger_model', product / 'tools/security/snapshot_ledger_model.py')
dc = load('discovery_census', product / 'tools/security/discovery_census.py')
c = model.vcs_costs(product, model.snapshot_costs(product, dc)[0])
caps = model.snapshot_caps(product)
KEYS = ('objects', 'edges', 'bytes')
option3 = json.loads((EV / 'c1a-r9/evidence/option3_r2.output.json').read_bytes())['combinations']["a+b'"]
r9 = tuple(max(option3[v]['subtotal'][k] for v in option3) for k in KEYS)
retention = json.loads((EV / 'c1c-0-r2/evidence/c1c0-checks-r2/retention-cap-evidence.json').read_bytes())
assert tuple(retention['r9Subtotal'][k] for k in KEYS) == r9 and retention['allPass']
subtotal = tuple(retention['total'][k] for k in KEYS)
plan = json.loads((EV / 'c1b/r6-evidence/vcs_term_r6.output.json').read_bytes())
assert tuple(plan['subtotal'][k] for k in KEYS) == subtotal
PLAN_D, PLAN_H = plan['derived']['refDirectories'], plan['derived']['headBytes']
plan_term = tuple(plan['atDerived']['term'][k] for k in KEYS)


def total(head, dirs):
    term = model.vcs_envelope(c, head, dirs)
    grand = tuple(subtotal[i] + term[i] for i in range(3))
    return dict(term=dict(zip(KEYS, term)), total=dict(zip(KEYS, grand)), twice=dict(zip(KEYS, (2 * g for g in grand))),
                holds=dict(zip(KEYS, (2 * grand[i] <= caps[i] for i in range(3)))))


def holds(head, dirs):
    return all(total(head, dirs)['holds'].values())


def shortest(dirs):
    return len('ref: refs') + 2 * dirs + 1


low, high = 0, c['INDEX_CAP']
while low < high:
    mid = (low + high + 1) // 2
    low, high = (mid, high) if holds(shortest(mid), mid) else (low, mid - 1)
dirs = low
low, high = shortest(dirs), c['INDEX_CAP']
while low < high:
    mid = (low + high + 1) // 2
    low, high = (mid, high) if holds(mid, dirs) else (low, mid - 1)
head = low
at_plan = total(PLAN_H, PLAN_D)
model_term_at_plan = tuple(at_plan['term'][k] for k in KEYS)
out = dict(
    standing=__doc__.splitlines()[0],
    caps=dict(zip(KEYS, caps)), subtotal=dict(zip(KEYS, subtotal)), recordMax=model.vcs_record_max(c),
    plan=dict(refDirectories=PLAN_D, headBytes=PLAN_H, term=dict(zip(KEYS, plan_term))),
    atPlan=at_plan,
    modelTermWithinPlanTerm=all(model_term_at_plan[i] <= plan_term[i] for i in range(3)),
    model=dict(refDirectories=dirs, headBytes=head),
    atModel=total(head, dirs), onePastModelDirectories=total(shortest(dirs + 1), dirs + 1), onePastModelHead=total(head + 1, dirs),
    reproduces=dict(refDirectories=dirs == PLAN_D, headBytes=head == PLAN_H),
)
assert all(at_plan['holds'].values()), 'the plan coordinates do not hold under the model'
assert out['modelTermWithinPlanTerm'], 'the model charges more than the plan priced'
assert all(out['atModel']['holds'].values())
assert not all(out['onePastModelDirectories']['holds'].values()) and not all(out['onePastModelHead']['holds'].values())
json.dump(out, sys.stdout, indent=1)
print()

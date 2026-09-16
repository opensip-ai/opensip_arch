"""PROBE B2 — drive the ACTUAL host boundary, not the schema alone: does the
provider-return capture / atom admission refuse a kind=unknown companion carrying a
non-null logicalPath, and does the host projection carry that value into the
retained TargetAttributionV2 whose digest enters selectedRefs?"""
import importlib.util, json, os, sys, inspect

DC = '/tmp/opensip-design-corrections/candidate-subject.v26/docs/coop/design-corrections'


def load(name, rel):
    p = os.path.join(DC, rel)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


R = {}
P = load('par2', 'foundation/provider_attribution_return_model.v2.py')
A = load('atom1', 'foundation/atom_model.v1.py')
R['provider_return_public_defs'] = [n for n, o in vars(P).items()
                                    if inspect.isfunction(o) and not n.startswith('_')]
R['atom_admission_defs'] = [n for n, o in vars(A).items()
                            if inspect.isfunction(o) and n.startswith('admit')]

# what does the projection copy?
src = open(os.path.join(DC, 'foundation/provider_attribution_return_model.v2.py'), encoding='utf-8').read()
i = src.find('logicalPath')
R['projection_excerpt'] = src[max(0, i - 700):i + 700] if i >= 0 else 'logicalPath not referenced'

# the atom sidecar guard, verbatim
asrc = open(os.path.join(DC, 'foundation/atom_model.v1.py'), encoding='utf-8').read()
j = asrc.find('TARGET_ATTRIBUTION_LOGICAL_PATH_ON_FIRST_PARTY')
R['atom_guard_excerpt'] = asrc[max(0, j - 800):j + 500]

print(json.dumps({k: v for k, v in R.items() if 'excerpt' not in k}, indent=1))
print('\n--- provider-return projection around logicalPath ---')
print(R['projection_excerpt'][:1600])
print('\n--- atom sidecar logicalPath guard ---')
print(R['atom_guard_excerpt'][:1400])
json.dump(R, open('/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/probeB2.json', 'w'), indent=1)

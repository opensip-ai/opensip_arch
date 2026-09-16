"""Fix 1 after failed run oc-1 (oc2-owner-string-expression-case-is-policy-imperative-key-refused returned CONFIG.INVALID).

Diagnosis (receipts/checks/oc-1 plus the recorded diagnostic): Atom's allOf carries two if/then CONSTRAINT members. The
grammar flattener pushed every allOf member as a positional ALTERNATIVE, so each conditional member looked like an
unconstrained alternative that admits a string, and a string expression at a predicate position was not recognised.
An allOf member constrains the same instance; only oneOf/anyOf branches are alternatives. Follow a structural allOf member
(a $ref, a type, members, items or its own branches) and never treat a conditional member as an alternative.
"""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-workflow-owner-completion.v1/tools')
from textedit import apply  # noqa: E402

V3 = 'docs/coop/design-corrections/workflows/workflows_model.v3.py'
row = apply('Q2 fix1 grammar alternatives follow only structural allOf members', V3, [
    ('''    """Leaf alternatives admitted at one position: local $refs resolved, oneOf/anyOf/allOf flattened; a non-local $ref is opaque."""''',
     '''    """Leaf alternatives admitted at one position: local $refs resolved and oneOf/anyOf branches flattened. An allOf member
    constrains the SAME instance, so only a structural member ($ref, type, members, items or its own branches) is followed and
    a conditional if/then member is never an alternative. A non-local $ref is opaque."""'''),
    ('''        combined=[c for k in ('oneOf','anyOf','allOf') for c in n.get(k,[])]
        stack.extend(combined)
        if not combined or any(k in n for k in ('type','properties','items','const','enum')):out.append(n)''',
     '''        branches=[c for k in ('oneOf','anyOf') for c in n.get(k,[])]
        structural=[c for c in n.get('allOf',[]) if isinstance(c,dict) and any(k in c for k in ('$ref','type','properties','items','oneOf','anyOf'))]
        stack.extend(branches+structural)
        if not (branches or structural) or any(k in n for k in ('type','properties','items','const','enum')):out.append(n)'''),
])
print(json.dumps(row, indent=1))

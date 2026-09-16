"""Fix 2 after reviewing diffs/capture-to-work.diff (all checks had passed at final-1/final-others).

The new workflows-and-surfaces section 5 sentence said "a string where the grammar admits only a predicate object", but the
owner classifier (workflows_model.v3.policy_grammar_violation, and its docstring) flags a string at ANY position whose every
closed alternative is an object. The normative sentence is aligned to the implemented and controlled law; no code changes.
"""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-workflow-owner-completion.v1/tools')
from textedit import apply  # noqa: E402

WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
row = apply('Q2 fix2 section 5 string-expression wording equals the classifier law', WS, [
    ('''grammar declares at that position, or a string where the grammar admits only a predicate object,
is `POLICY.IMPERATIVE_KEY_REFUSED`.''',
     '''grammar declares at that position, or a string where every closed alternative at that position is
an object (a string expression), is `POLICY.IMPERATIVE_KEY_REFUSED`.'''),
])
print(json.dumps(row, indent=1))

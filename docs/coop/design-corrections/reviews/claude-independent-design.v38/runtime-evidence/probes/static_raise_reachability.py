"""Independent reviewer probe (static, reads source only; writes only this runtime's receipts).

Question: identity-model.v3 open_run_closure calls owning-unit functions (native, workflow) WITHOUT a local
try/except at several call sites. close_run then normalizes only the replay stack's declared class objects.
Which exceptions can statically ESCAPE those unwrapped entry points, and are they AdmissionError-family owner
refusals (which would escape close_run normalization) or other exceptions?

Attempt 2 (attempt 1 ignored try blocks around CALL sites and over-reported, e.g. admit_capability_manifest wraps
cve1_decode; its receipt is preserved as static-raise-reachability.attempt1-call-site-try-ignored.json).
Escape is a fixpoint: escaping(f) = raises in f not caught by an enclosing handler in f, plus escaping(g) for every
call of g in f that is not inside a try whose handler catches that exception.

Approximation limits: intra-module calls by bare Name only; getattr/dynamic dispatch, methods, callbacks and
cross-module calls are not followed; handler matching is by name (the raised class, its module-local bases,
AdmissionError family, Exception/BaseException or bare except). Syntactic escape, not a retained-bytes demonstration.
"""
import ast
import json
import sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v38')
SRC = RT / 'work/source38-pkg/docs/coop/design-corrections'
OUT = RT / 'receipts/static-raise-reachability.json'

TARGETS = {
    'native/native_evidence_model.v2.py': {
        'unwrappedEntries': ['syntax_capability_support', 'source_variant_capability_support', 'clone_ownership_disclosure',
                             'admit_native_context', 'admit_capability_manifest', '_rung_index', 'admit_coverage_result_v3',
                             'bind_typescript_universe', 'bind_rust_universe', 'bind_syntax_universe'],
        'wrappedEntries': ['admit_requested_capabilities'],
        'admissionFamily': {'AdmissionError', 'C.AdmissionError'},
    },
    'workflows/workflows_model.v3.py': {
        'unwrappedEntries': ['rule_program_digest'],
        'wrappedEntries': [],
        'admissionFamily': {'Refusal', 'AdmissionError', 'C.AdmissionError'},
    },
}


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        return base + '.' + node.attr if base else node.attr
    if isinstance(node, ast.Call):
        return dotted(node.func)
    return None


class FunctionFacts(ast.NodeVisitor):
    def __init__(self):
        self.calls, self.raises, self.try_stack = [], [], []

    def handlers(self):
        return set().union(*self.try_stack) if self.try_stack else set()

    def visit_Try(self, node):
        caught = set()
        for h in node.handlers:
            if h.type is None:
                caught.add('*')
            elif isinstance(h.type, ast.Tuple):
                caught.update(filter(None, (dotted(e) for e in h.type.elts)))
            else:
                caught.add(dotted(h.type))
        self.try_stack.append(caught)
        for stmt in node.body:
            self.visit(stmt)
        self.try_stack.pop()
        for part in node.handlers + node.orelse + node.finalbody:
            self.visit(part)

    visit_TryStar = visit_Try

    def visit_Call(self, node):
        name = dotted(node.func)
        if name and '.' not in name:
            self.calls.append((name, node.lineno, self.handlers()))
        self.generic_visit(node)

    def visit_Raise(self, node):
        name = dotted(node.exc) if node.exc is not None else '<reraise>'
        self.raises.append((name, node.lineno, self.handlers()))
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        for stmt in node.body:
            self.visit(stmt)

    visit_AsyncFunctionDef = visit_FunctionDef


def analyse(rel, spec):
    tree = ast.parse((SRC / rel).read_text(encoding='utf-8'))
    functions = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            facts = FunctionFacts()
            for stmt in node.body:
                facts.visit(stmt)
            functions[node.name] = facts
    classes = {n.name: [dotted(b) for b in n.bases] for n in tree.body if isinstance(n, ast.ClassDef)}

    def lineage(exc):
        seen, todo = [], [exc]
        while todo:
            c = todo.pop()
            if c in seen:
                continue
            seen.append(c)
            todo.extend(b for b in classes.get(c, []) if b)
        return seen

    def family(exc):
        return any(c in spec['admissionFamily'] for c in lineage(exc))

    def caught(exc, handlers):
        if handlers & {'*', 'Exception', 'BaseException'}:
            return True
        if exc == '<reraise>':
            return False
        return bool(handlers & set(lineage(exc))) or (family(exc) and bool(handlers & spec['admissionFamily']))

    # escaping[f] = {(exc, origin_function, origin_line)}
    escaping = {f: set() for f in functions}
    changed = True
    while changed:
        changed = False
        for f, facts in functions.items():
            new = {(exc, f, line) for exc, line, h in facts.raises if not caught(exc, h)}
            for callee, _line, h in facts.calls:
                if callee in escaping:
                    new |= {row for row in escaping[callee] if not caught(row[0], h)}
            if not new <= escaping[f]:
                escaping[f] |= new
                changed = True

    result = {}
    for entry in spec['unwrappedEntries'] + spec['wrappedEntries']:
        if entry not in functions:
            result[entry] = {'error': 'not a top-level function'}
            continue
        rows = sorted(escaping[entry], key=lambda r: (r[1], r[2]))
        result[entry] = {
            'wrappedAtIdentityCallSite': entry in spec['wrappedEntries'],
            'escapingRaiseSites': len(rows),
            'escapingAdmissionFamily': [{'exception': e, 'function': f, 'line': l} for e, f, l in rows if family(e)],
            'escapingOther': [{'exception': e, 'function': f, 'line': l} for e, f, l in rows if not family(e)],
        }
    return result


out = {'standing': 'independent reviewer static probe attempt 2; syntactic escape only, not a retained-bytes demonstration',
       'python': sys.version.split()[0], 'results': {rel: analyse(rel, spec) for rel, spec in TARGETS.items()}}
OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + '\n')
for rel, rows in out['results'].items():
    for entry, row in rows.items():
        print(rel, entry, json.dumps(row))

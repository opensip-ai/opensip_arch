"""PROBE 18b (v31) — finish the RR27-01 correction with the exact enclosure, using the AST so the
answer does not depend on my own indentation heuristics (which mislabelled six sites '<module
level>' in p18)."""
import ast, json, os

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
P = os.path.join(SRC, 'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
src = open(P, encoding='utf-8').read()
tree = ast.parse(src)
TOK = 'EXECUTION_INPUTS_COVERAGE_DERIVE'
R = {'corrects': 'p18 used indentation extents and mislabelled six sites as module level'}

# map each line to the chain of enclosing function defs, via AST
chain = {}
def visit(node, stack):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            ns = stack + [child.name]
            for ln in range(child.lineno, (child.end_lineno or child.lineno) + 1):
                chain[ln] = ns
            visit(child, ns)
        else:
            visit(child, stack)
visit(tree, [])

lines = src.splitlines()
rows = []
for i, l in enumerate(lines, 1):
    if TOK in l:
        c = chain.get(i, [])
        rows.append({'line': i, 'enclosingChain': c,
                     'innermost': c[-1] if c else '<module level>',
                     'isRaise': '_add(faults' in l,
                     'text': l.strip()[:110]})
R['sites'] = rows
print('%-6s %-9s %-46s %s' % ('line', 'is-raise', 'enclosing function chain', 'innermost'))
for x in rows:
    print('%-6d %-9s %-46s %s' % (x['line'], x['isRaise'], ' > '.join(x['enclosingChain'])[:46],
                                  x['innermost']))

raises = [x for x in rows if x['isRaise']]
R['raiseCount'] = len(raises)
R['innermostCounts'] = {}
for x in raises:
    R['innermostCounts'][x['innermost']] = R['innermostCounts'].get(x['innermost'], 0) + 1
print('\nraise sites: %d' % len(raises))
print('innermost function counts:', json.dumps(R['innermostCounts']))
R['insideHelperCount'] = sum(v for k, v in R['innermostCounts'].items()
                             if k in ('load_coverage', 'partitions_in_cell'))
R['inEnclosingLoopCount'] = len(raises) - R['insideHelperCount']
R['enclosingFunction'] = raises[-1]['enclosingChain'][0] if raises and raises[-1]['enclosingChain'] else None
print('inside load_coverage/partitions_in_cell : %d' % R['insideHelperCount'])
print('directly in the enclosing function body : %d' % R['inEnclosingLoopCount'])
print('enclosing function                      : %s' % R['enclosingFunction'])
R['v27ExclusivityClaimFalse'] = R['inEnclosingLoopCount'] > 0
R['correctedStatement'] = (
    'Of the %d raise sites, %d is inside the nested helper load_coverage and %d are directly in the '
    'coverage-account loop of %s (the `for ... in owed:` loop), where load_coverage and '
    'partitions_in_cell are nested helpers rather than the enclosing scope. The v27 report\'s '
    '"only inside load_coverage and partitions_in_cell" was therefore wrong. Every site is still '
    'coverage-account derivation, so the section 5 attribution is unaffected.'
    % (len(raises), R['insideHelperCount'], R['inEnclosingLoopCount'], R['enclosingFunction']))
print('\n' + R['correctedStatement'])
json.dump(R, open(os.path.join(OUT, 'p18b-f09enclosure.json'), 'w'), indent=1, default=str)
print('\nwrote p18b-f09enclosure.json')

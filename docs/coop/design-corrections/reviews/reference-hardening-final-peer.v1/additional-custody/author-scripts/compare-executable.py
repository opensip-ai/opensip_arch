"""Compare two Python sources three ways, keeping DOCSTRING differences separate from EXECUTABLE
behaviour, which a naive `co_consts` comparison conflates (a docstring IS a code-object constant).

  1. AST modulo docstrings  - every docstring node replaced by a fixed sentinel, then ast.dump
                              compared. Comments never enter the AST, so this ignores both.
  2. Compiled code objects  - co_code / co_names / co_varnames / co_consts compared recursively,
                              with docstring constants normalised the same way. Proves the
                              interpreter executes the same instructions.
  3. Docstring inventory    - the docstrings that DO differ, enumerated by qualified name, so an
                              intended documentation change is visible rather than hidden.
"""
import ast, sys
from pathlib import Path

SENTINEL = '<<DOCSTRING>>'


def _docstring_nodes(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                yield node, body[0].value


def qualnames(tree):
    """{qualified name: docstring} for every docstring-bearing node."""
    out, stack = {}, []

    def walk(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + child.name
                doc = ast.get_docstring(child, clean=False)
                if doc is not None:
                    out[name] = doc
                walk(child, name + '.')
            else:
                walk(child, prefix)

    doc = ast.get_docstring(tree, clean=False)
    if doc is not None:
        out['<module>'] = doc
    walk(tree, '')
    return out


def stripped_ast(src):
    tree = ast.parse(src)
    for _, const in _docstring_nodes(tree):
        const.value = SENTINEL
    return tree


def norm_consts(code):
    out = []
    for c in code.co_consts:
        if hasattr(c, 'co_code'):
            out.append(('CODE', c.co_name, code_tuple(c)))
        else:
            out.append(c)
    # the leading docstring constant, if any, is normalised
    if out and isinstance(out[0], str):
        out[0] = SENTINEL
    return tuple(out)


def code_tuple(code):
    return (code.co_code, code.co_names, code.co_varnames, code.co_argcount,
            code.co_flags & ~0, norm_consts(code))


def main(pa, pb):
    a, b = Path(pa).read_text(), Path(pb).read_text()
    print('A', pa)
    print('B', pb)
    print('identical bytes:', a == b)

    da, db = ast.dump(stripped_ast(a)), ast.dump(stripped_ast(b))
    print('1. AST modulo docstrings IDENTICAL:', da == db)

    ca = compile(stripped_ast(a), '<a>', 'exec')
    cb = compile(stripped_ast(b), '<b>', 'exec')
    print('2. compiled code objects IDENTICAL:', code_tuple(ca) == code_tuple(cb))

    qa, qb = qualnames(ast.parse(a)), qualnames(ast.parse(b))
    diff = sorted(k for k in set(qa) | set(qb) if qa.get(k) != qb.get(k))
    print('3. docstrings differing:', len(diff), diff)
    ok = (da == db) and code_tuple(ca) == code_tuple(cb)
    print('EXECUTABLE EQUIVALENCE:', 'YES' if ok else 'NO')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))

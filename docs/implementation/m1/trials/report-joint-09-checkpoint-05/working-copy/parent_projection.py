"""Proposed shared-budget successor around the verified parent projector.

Retains the parent's projection algorithms, includes later panel reservations
from the outset, and stops after an earlier whole panel exhausts the budget.
Owner callbacks remain synthetic/reference inputs until host integration.
"""
import ast,copy,types

def bind(read_unit,model,reserved,placement):
    raw=read_unit('report-projection','report_model.py')
    fn=next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=='project_exploration')
    initialization=next(n for n in fn.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='panels' for t in n.targets))
    assert ast.unparse(initialization.value)=='{name: dict(omitted) for name in applicable}'
    offset=fn.body.index(initialization)+1
    fn.body[offset:offset]=ast.parse("if set(panels) & set(RESERVED): raise ValueError('reserved and parent panels overlap')\npanels.update(copy.deepcopy(RESERVED))\nif len(canonical(panels)) > budget_bytes: raise ValueError('reserved panel states exceed shared allowance')").body
    loop=next(n for n in fn.body if isinstance(n,ast.For) and ast.unparse(n.iter)=='PROJECTION_PRIORITY')
    # Only earlier names can stop this loop: later initial omitted states do not.
    loop.body[:0]=ast.parse("if any(BUDGET_OMITTED(k,panels[k]) for k in PROJECTION_PRIORITY[:PROJECTION_PRIORITY.index(name)] if k in panels): break").body
    # The predecessor settles a rejected graph slot before checking whether
    # even the zero-slot panel fits. Refuse that whole panel first.
    guards=0
    for node in ast.walk(loop):
        if isinstance(node,ast.If) and ast.unparse(node.test)=='stopped':
            call=next(n for n in node.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='settle')
            idx=node.body.index(call)
            node.body[idx:idx]=ast.parse("panels[name] = panel(slots, PLACEHOLDER_DELTA)\nif size() > cap:\n    panels[name] = dict(omitted)\n    continue").body
            guards+=1
    assert guards==1
    ns=dict(vars(model));ns.update(RESERVED=copy.deepcopy(reserved),BUDGET_OMITTED=placement.budget_omitted)
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),'pinned-report08-projector#joint-reservation-and-stop','exec'),ns)
    facade=types.SimpleNamespace(**{k:v for k,v in vars(model).items() if not k.startswith('__')})
    facade.project_exploration=ns['project_exploration']
    return facade

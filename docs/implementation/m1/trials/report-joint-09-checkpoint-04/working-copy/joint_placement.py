"""Append owner-built panels under one shared report allowance and priority.

Inputs before these panels must already be projected/admitted with the reserved
new panel states included in their byte accounting. Builders receive only the
remaining data bytes; None means the complete minimum projection cannot fit.
"""
import copy
OMITTED={'state':'omitted','reason':'exploration-budget-exceeded'}


def budget_omitted(name,value):
    if value.get('reason')=='exploration-budget-exceeded':return True
    return name=='catalog' and value.get('state')=='present' and any(v.get('reason')=='exploration-budget-exceeded' for v in value['data'].values())


def append(existing,builders,terminal,priority,cap,model):
    if set(builders)&set(terminal):raise ValueError('one panel source state required')
    if (set(builders)|set(terminal))-set(priority):raise ValueError('unknown panel priority')
    panels=copy.deepcopy(existing)
    for name in builders:panels[name]=copy.deepcopy(OMITTED)
    panels.update(copy.deepcopy(terminal))
    measure=lambda v:len(model.canonical(v))
    if measure(panels)>cap:raise ValueError('reserved panel states exceed shared allowance')
    stopped=False;budgets={}
    for name in priority:
        if name not in panels:continue
        if name not in builders:
            if stopped and panels[name].get('state')=='present':raise ValueError('later existing panel violates priority')
            stopped=stopped or budget_omitted(name,panels[name]);continue
        if stopped:continue
        remaining=cap-measure(panels)+measure(panels[name])-measure({'state':'present','data':None})+measure(None)
        budgets[name]=remaining
        value=builders[name](remaining) if remaining>0 else None
        if value is None:stopped=True;continue
        if measure(value)>remaining:raise ValueError('owner exceeded its panel allowance')
        panels[name]={'state':'present','data':value}
        if measure(panels)>cap:raise ValueError('shared panel allowance exceeded')
    return panels,budgets


def allocation(panels,name,priority,cap,model):
    """Reconstruct this panel's data allowance before later present panels ran."""
    if name not in priority or panels.get(name,{}).get('state')!='present':raise ValueError('present prioritized panel required')
    staged=copy.deepcopy(panels);at=priority.index(name)
    for later in priority[at+1:]:
        if staged.get(later,{}).get('state')=='present':staged[later]=copy.deepcopy(OMITTED)
    staged[name]=copy.deepcopy(OMITTED)
    measure=lambda v:len(model.canonical(v))
    return cap-measure(staged)+measure(OMITTED)-measure({'state':'present','data':None})+measure(None)


def check_feature_deltas(data,allowed,model):
    """Necessary arithmetic only; omitted contents/delta measurement remain host assertions."""
    size=len(model.canonical(data));pending=[data]
    while pending:
        value=pending.pop()
        if isinstance(value,dict):
            if value.get('omissionCause')=='byte-budget':
                delta=value.get('rejectedByteDelta')
                if type(delta) is not int or delta<=0 or size+delta<=allowed:
                    raise ValueError('FEATURE-BYTE-OMISSION-CAUSE')
            pending.extend(value.values())
        elif isinstance(value,list):pending.extend(value)

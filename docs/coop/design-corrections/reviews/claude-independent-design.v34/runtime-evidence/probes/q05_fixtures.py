import copy
def e2_inputs(Kmod, AMmod, hash_order=False):
    """3 same-kind calls scopes, 4 calls Coverage: one paired by TWO scopes via commitment, one unrelated.
    The lowest id carries NO deficiency, so the carrier must be the first WITH one."""
    i = Kmod.base_inputs(enumerationPlan=Kmod.plan_one(cap='reachability'))
    Kmod.install_pair(i, *Kmod.paired('reachability', 'from-resolved-calls', Kmod.U1, Kmod.U1, [Kmod.F_SYM], tag='1'))
    s5, sc5 = Kmod.scope('calls', 'resolved-callee', Kmod.U1, Kmod.U1, [Kmod.F_SYM], sid='5')
    s6, sc6 = Kmod.scope('calls', 'resolved-callee', Kmod.U1, Kmod.U1, [Kmod.F_SYM], sid='6')
    s7, sc7 = Kmod.scope('calls', 'resolved-callee', Kmod.U1, Kmod.U1, [Kmod.G_SYM], sid='7')
    derived = AMmod._derive_scope_commitment(sc5)
    covs = {}
    for cid, dfc, nc in (('2', None, None), ('3', 'input-closure-incomplete', 'lockfile-missing'),
                         ('4', 'input-closure-incomplete', 'no-program-unit'), ('9', 'input-closure-incomplete', 'no-program-unit')):
        c, cv = Kmod.coverage('calls', 'resolved-callee', Kmod.U1, Kmod.U1, cov='unknown', cid=cid)
        cv['entry']['deficiency'], cv['entry']['nativeCause'] = dfc, nc
        covs[cid] = (c, cv)
    if derived:
        covs['4'][1]['key']['subjectScopeCommitment'] = derived
    i['scopes'].update({s5: sc5, s6: sc6, s7: sc7})
    items = [covs[k] for k in ('9', '4', '3', '2')]
    for c, cv in items:
        i['coverages'][c] = cv
    i['coverageScopes'].update({covs['2'][0]: s6, covs['3'][0]: s5, covs['9'][0]: s7})
    if not derived:
        i['coverageScopes'][covs['4'][0]] = s5
    if hash_order:
        order = list(set(i['coverages']))
        i['coverages'] = {c: i['coverages'][c] for c in order}
        sorder = list(set(i['scopes']))
        i['scopes'] = {s: i['scopes'][s] for s in sorder}
    return i

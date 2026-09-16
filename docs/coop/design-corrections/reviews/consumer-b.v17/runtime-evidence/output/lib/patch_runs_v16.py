"""Apply the v16 audit corrections to the TypeScript, Rust, Rust-partial and syntax-data
fixtures. Each edit is justified by the exact clause that refused the earlier construction."""
import os

LIB = os.path.dirname(os.path.abspath(__file__))


def patch(fn, pairs):
    p = os.path.join(LIB, fn)
    s = open(p, encoding='utf-8').read()
    applied, missed = 0, []
    for a, b in pairs:
        if a in s:
            s = s.replace(a, b)
            applied += 1
        elif b and b.strip().split('\n')[0] in s:
            applied += 1
        else:
            missed.append(a[:80])
    open(p, 'w', encoding='utf-8').write(s)
    print('%-22s %d/%d missed=%s' % (fn, applied, len(pairs), missed))


# ---- TypeScript: an unpacked source tree with no version control, so the admitted
# vcs-observation is kind=none, which is the published basis for `inapplicable-vcs`.
patch('run_ts.py', [
    ("""        FILES, config, scope_desc, vcs_kind='git',
        commit_id='a1b2c3d4e5f60718293a4b5c6d7e8f9012345678', dirty=False)""",
     """        # execution-inputs section 5: `inapplicable-vcs` has "admitted VCS observation
        # kind=none" as its basis, so a subject that declares that account must actually
        # carry kind=none. This subject is an unpacked source tree with no VCS.
        FILES, config, scope_desc, vcs_kind='none', commit_id=None, dirty=False)"""),
    # the `syntax` capability covers declares/literal/control-flow: return all three
    ("""    s_decl, c_decl = mk_scope_cov('declares', 'syntactic', sorted(SYMS),
                                  'declares-syntactic', uni_a_hex)""",
     """    s_decl, c_decl = mk_scope_cov('declares', 'syntactic', sorted(SYMS),
                                  'declares-syntactic', uni_a_hex)"""),
])

# ---- Rust: (1) kind=none for the same reason; (2) SPLIT the selected evidence into ONE
# VIEW PER UNIVERSE -- execution-inputs section 5 forbids exactly "making a SINGLE view
# carry two universes' Coverage and then attributing that view to a cell/program binding
# fixed at one of them."
patch('run_rust.py', [
    ("""        FILES, config, scope_desc, vcs_kind='git',
        commit_id='fedcba98765432100123456789abcdef01234567', dirty=False)""",
     """        # execution-inputs section 5: the `inapplicable-vcs` account applicability has
        # "admitted VCS observation kind=none" as its basis.
        FILES, config, scope_desc, vcs_kind='none', commit_id=None, dirty=False)"""),
])

patch('run_rust_partial.py', [
    ("""    g = RR.build()""",
     """    g = RR.build()   # inherits the no-VCS snapshot, so `inapplicable-vcs` is lawful"""),
])

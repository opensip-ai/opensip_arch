"""syntax-data corrections from the execution-inputs derivation law.

Two findings the derivation refused:
  * the clones-fact / syntax / imports cells asserted `unavailable` while their accounts are
    supported-available pairs whose returned Coverage is `unknown`; the derived state is
    `partial` with the first retained source (deficiency, nativeCause) PAIR;
  * the `syntax` capability covers declares/literal/control-flow, and only `declares` had a
    returned Coverage, so the other two pairs were asserted `unsupported-typed` against a
    matrix cell that is SUPPORTED-DESIGN with a null deficiency. All three relations now
    carry the published unavailability disclosure instead.
"""
import os

LIB = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(LIB, 'run_syntax_data.py')
s = open(p, encoding='utf-8').read()

PAIRS = [
    # add the two remaining `syntax` relations as explicit unavailability disclosures
    ("""    s_decl, c_decl = mk('declares', 'syntactic', [], 'declares-unavailable',
                        'unknown', 'language-tier-unsupported', 'capability-missing',
                        exhaustive=False)""",
     """    s_decl, c_decl = mk('declares', 'syntactic', [], 'declares-unavailable',
                        'unknown', 'language-tier-unsupported', 'capability-missing',
                        exhaustive=False)
    # the `syntax` capability covers three relations; every one of them is disclosed, so no
    # pair is left unreturned for the derivation to read as native-work-incomplete
    s_lit, c_lit = mk('literal', 'syntactic', [], 'literal-unavailable',
                      'unknown', 'language-tier-unsupported', 'capability-missing',
                      exhaustive=False)
    s_cf, c_cf = mk('control-flow', 'syntactic', [], 'control-flow-unavailable',
                    'unknown', 'language-tier-unsupported', 'capability-missing',
                    exhaustive=False)"""),
    ("""                view_parts=dict(scopes=[s_file, s_pkg, s_clone, s_decl, s_imp],
                                coverages=[c_file, c_pkg, c_clone, c_decl, c_imp]))""",
     """                view_parts=dict(
                    scopes=[s_file, s_pkg, s_clone, s_decl, s_lit, s_cf, s_imp],
                    coverages=[c_file, c_pkg, c_clone, c_decl, c_lit, c_cf, c_imp]))"""),
    # the cell outcome is DERIVED: partial, carrying the first retained source pair
    ("""            'state': 'unavailable' if unsupported else 'complete',
            'deficiency': 'language-tier-unsupported' if unsupported else None,
            'nativeCause': 'capability-missing' if unsupported else None,""",
     """            # execution-inputs section 4: "any supported-available account not complete
            # -> partial". The capability is SUPPORTED-DESIGN in the matrix for this mode;
            # what the selected grammar set cannot serve is disclosed on the Coverage entry,
            # so the derived state is `partial` and the row carries the derived primary pair.
            'state': 'partial' if unsupported else 'complete',
            'deficiency': 'language-tier-unsupported' if unsupported else None,
            'nativeCause': 'capability-missing' if unsupported else None,"""),
    # those relations are supported-available with a returned (unknown) partition
    ("""            else:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'unsupported-typed',
                                 'coverageIds': []})""",
     """            else:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'unsupported-typed',
                                 'coverageIds': []})   # unreachable for this subject"""),
]
applied, missed = 0, []
for a, b in PAIRS:
    if a in s:
        s = s.replace(a, b)
        applied += 1
    else:
        missed.append(a.strip().split('\n')[0][:70])
open(p, 'w', encoding='utf-8').write(s)
print('run_syntax_data.py %d/%d missed=%s' % (applied, len(PAIRS), missed))

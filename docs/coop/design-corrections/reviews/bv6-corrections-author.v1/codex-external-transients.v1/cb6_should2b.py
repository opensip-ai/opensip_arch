import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/foundation/check-identity.py')
s = P.read_text(encoding='utf-8')

ANCHOR = """check('only-file-enumerated-declares-coverage-totality',
      [n for n,r in M.RELATIONS.items() if 'coverageTotality' in r]==['file'])
"""
NEW = """check('only-file-enumerated-declares-coverage-totality',
      [n for n,r in M.RELATIONS.items() if 'coverageTotality' in r]==['file'])
# CB6-SHOULD-2. identity section 3 said Coverage scopes partition the claimed universe `without
# overlaps or omissions`, while native section 1.2 said only relations with a `coverageTotality` row
# owe totality. The reconciliation now published in BOTH documents is that the two halves have
# different owners: DISJOINTNESS is general and is stated over the FULL owning tuple, while the
# OMISSION half is discharged only where the registry carries a row. These controls hold the
# reconciled reading to the registry it appeals to, extend the not-total evidence from the two
# inventory relations to a SYMBOL relation - the class the clause was undecidable for - and keep the
# symbol trust boundary stated rather than quietly re-derived.
_SYMBOL_RELATIONS=sorted(n for n,r in M.RELATIONS.items()
                         if r.get('anchorLaw',{}).get('class')=='source-text')
check('the-nine-symbol-kind-relations-owe-no-omission-obligation',
      len(_SYMBOL_RELATIONS)==9 and all('coverageTotality' not in M.RELATIONS[n] for n in _SYMBOL_RELATIONS))
check('the-disjointness-half-is-stated-over-the-full-owning-tuple',
      M.RELATIONS['file']['coverageTotality']['matchOn']
      ==['snapshotId','relation','resolution','sourceUniverse','targetUniverse'])
# An empty COMPLETE result for a symbol relation is an ordinary finding, exactly as for the two
# inventory relations above: a subject may lawfully bear no fact where no totality row exists, and
# an over-broad reading of `without omissions` would refuse this honest Run.
for _relation in ('references','declares'):
    check('an-empty-complete-'+_relation+'-result-is-an-ordinary-finding-not-an-omission',
          M.close_run(*build(resolved=True,has_match=False,relation=_relation)).startswith('run2:'))
# ...and `complete` is still not vacuous where no totality row exists: the SAME scope, claiming a
# fact it does not retain, is still refused by the totality law where the registry does own it.
check('completeness-is-still-decided-by-the-registry-not-by-the-clause',
      not_admitted(lambda:M.close_run(*build(resolved=True,has_match=False,relation='file')))
      and M.close_run(*build(resolved=True,has_match=False,relation='references')).startswith('run2:'))
# The two prose statements now name each other, so a reader arriving at either is not left to
# reconcile them, and the symbol-attribution limit is not restated as a re-derivation.
_IDENTITY_MD=(H.parents[2]/'v2/contracts/product-v1/identity-and-evidence.md').read_text(encoding='utf-8')
_NATIVE_MD=(H.parents[2]/'v2/contracts/product-v1/native-evidence.md').read_text(encoding='utf-8')
check('identity-section-3-defers-the-omission-half-to-the-coverage-totality-registry',
      'coverageTotality' in _IDENTITY_MD and 'Disjointness' in _IDENTITY_MD
      and 'not\\nre-derivable' in _IDENTITY_MD.replace('**',''))
check('native-section-1-2-names-the-identity-clause-it-is-the-successor-to',
      'without overlaps or omissions' in _NATIVE_MD and 'disjointness' in _NATIVE_MD)
"""
assert s.count(ANCHOR) == 1
P.write_text(s.replace(ANCHOR, NEW), encoding='utf-8')
print('ok')

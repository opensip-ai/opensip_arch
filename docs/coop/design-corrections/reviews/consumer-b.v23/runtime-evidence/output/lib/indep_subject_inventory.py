"""INDEPENDENT derivation #2 -- SubjectInventoryV1 deficiency / carrier, checked ON THE
INVENTORY ITSELF.

Built from the clauses first. It deliberately does NOT look at the binding's carrier or the
ExecutionInputs projection to decide whether an inventory's own pair is lawful: the instruction's
point, and the schema's, is that the inventory carries its own.

CLAUSE -> CODE MAP

 S1 subject-inventory.schema.v1.json #/properties/deficiency DESC: "null iff state=complete"
    + native x-opensip-deficiency-cause-registry.noDeficiencyNoCause: "A null deficiency
    requires a null nativeCause."
      -> state complete  <=> deficiency null, and deficiency null => nativeCause null
 S2 #/allOf[state=unavailable]: rows maxItems 0, examinedPaths maxItems 0, deficiency is an
    EnumerationDeficiencyV1 and NOT null
 S3 #/allOf[state=partial]: deficiency non-null
 S4 #/$defs/EnumerationDeficiencyV1: "copied native DeficiencyV2 OR the local member
    source-syntax-invalid ... nativeCause MUST be null for the local member ... Parse/
    classification failure of a first-party manifest is this local member, NEVER
    provider-unavailable."
 S5 #/properties/deficiency DESC: "Native DeficiencyV2 members keep OWNER CARRIER LAW."
      -> for a copied member, the native deficiency-cause registry row decides the nativeCause:
         must-be-null -> null; required -> non-null and a member of allowedCauses;
         optional -> null or a member of allowedCauses. A deficiency with NO row refuses
         ("There is no default row: a deficiency with no row here is a registry defect and
         refuses").
      -> a copied member whose carrier is an `entry.*` field that a SubjectInventoryV1 does not
         have can still be carried here only through its nativeCause verdict; the enumeration
         contract names exactly that case for a timeout ("Timeout: budget-exhausted,
         nativeCause null per owner carrier law").
 S6 #/properties/examinedPaths DESC: every examined path is a member of that kind's extent;
    "PARTIAL MAY equal the extent"; "COMPLETE FILE requires set equality with the file extent
    AND a row per path"
 S7 #/$defs/InventoryRowV1 + x-opensip-subject-language-table: file/package signatureTokens
    MUST be the canonical empty array; subjectLanguage is the LONGEST-suffix match of the path
    with `unspecified` for an unlisted suffix; package language is the manifest FORMAT
    (package.json -> json, Cargo.toml -> toml); file/symbol nativeSubjectId unique; package
    unique by (nativeSubjectId, path); file qualifiedName equals the path
 S8 enumeration-contract section 4: "Parse/classification failure CANNOT be `complete`
    (including complete-empty): it is `partial` with local deficiency `source-syntax-invalid`";
    "every known named record ... is retained as a row ... Dropping a known named row on that
    partial is ENUMERATION_PACKAGE_PARSE"
 S9 "Host membership does not make a missing/invalid carrier valid" -- so this module never
    consults UnitMembershipV1 to excuse a carrier; membership is used only to derive extents.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'
KIT = S.KIT
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


class F:
    def __init__(self):
        self.rows = []

    def need(self, cond, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check,
                          'result': 'PASS' if cond else 'REFUSE', 'detail': detail})
        return cond

    def ok(self, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check, 'result': 'PASS',
                          'detail': detail})

    def na(self, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check, 'result': 'NOT-APPLICABLE',
                          'detail': detail})

    @property
    def refusals(self):
        return [r for r in self.rows if r['result'] == 'REFUSE']


def language_of(path, table):
    best, lang = '', 'unspecified'
    for m in table['members']:
        for suf in m['suffixes']:
            if path.endswith(suf) and len(suf) > len(best):
                best, lang = suf, m['languageId']
    return lang


def check(label):
    f = F()
    st, _ = ST.Store.load(OUT + '/runs/%s.store.json' % label)
    inv_doc = kitdoc(B.SUBJ_INV_DOC)
    lang_table = inv_doc['x-opensip-subject-language-table']
    defs = inv_doc['$defs']
    native_v2 = set(defs['DeficiencyV2']['enum'])
    causes = set(defs['NativeCause']['enum'])
    registry = kitdoc(B.NATIVE_DOC)['x-opensip-deficiency-cause-registry']['deficiencies']

    enum_plan = json.loads(st.get_blob(st.labels['enumeration-plan']).decode())
    snap = None
    for t, r in st.objects.items():
        if t.startswith('snapshot2:'):
            snap = r
    inv_paths = {r['path']: r for r in snap['sourceInventory']}

    invs = []
    for lab, dig in sorted(st.labels.items()):
        if lab.startswith('subject-inventory:'):
            invs.append((lab, json.loads(st.get_blob(dig).decode())))

    for lab, inv in invs:
        cell = enum_plan['cells'][inv['cellOrdinal']]
        binding = cell['programBindings'][inv['programOrdinal']]
        ext = {e['kind']: set(e['paths']) for e in (binding.get('extents') or [])}
        kind, state = inv['kind'], inv['state']
        dfc, cause = inv['deficiency'], inv['nativeCause']
        where = {'inventory': lab, 'kind': kind, 'state': state,
                 'deficiency': dfc, 'nativeCause': cause}

        # ---- S1 / S2 / S3 state <-> carrier presence
        f.need((dfc is None) == (state == 'complete'),
               'S1 deficiency DESC "null iff state=complete"',
               'DEFICIENCY_NULL_IFF_COMPLETE', where)
        if dfc is None:
            f.need(cause is None,
                   'S1 registry.noDeficiencyNoCause',
                   'NULL_DEFICIENCY_REQUIRES_NULL_NATIVE_CAUSE', where)
        if state == 'unavailable':
            f.need(not inv['rows'] and not inv['examinedPaths'] and dfc is not None,
                   'S2 allOf[state=unavailable]',
                   'UNAVAILABLE_HAS_NO_ROWS_NO_EXAMINED_PATHS_AND_A_DEFICIENCY',
                   dict(where, rows=len(inv['rows']),
                        examinedPaths=len(inv['examinedPaths'])))
        if state == 'partial':
            f.need(dfc is not None, 'S3 allOf[state=partial]',
                   'PARTIAL_REQUIRES_A_DEFICIENCY', where)

        # ---- S4 / S5 the carrier pair, ON THIS RECORD
        if dfc is not None:
            local = dfc == 'source-syntax-invalid'
            f.need(local or dfc in native_v2,
                   'S4 EnumerationDeficiencyV1 oneOf',
                   'DEFICIENCY_IS_A_COPIED_NATIVE_MEMBER_OR_THE_LOCAL_MEMBER', where)
            if local:
                f.need(cause is None,
                       'S4 "nativeCause MUST be null for the local member"',
                       'LOCAL_SOURCE_SYNTAX_INVALID_HAS_A_NULL_NATIVE_CAUSE', where)
                f.need(dfc not in native_v2 and dfc not in causes,
                       'S4 "Do not add the local member to copied DeficiencyV2 or NativeCause"',
                       'LOCAL_MEMBER_IS_NOT_IN_THE_COPIED_VOCABULARIES', where)
            else:
                row = registry.get(dfc)
                if not f.need(row is not None,
                              'S5 registry standing "There is no default row: a deficiency '
                              'with no row here is a registry defect and refuses"',
                              'COPIED_DEFICIENCY_HAS_A_REGISTRY_ROW', where):
                    continue
                verdict = row.get('nativeCause')
                allowed = row.get('allowedCauses') or []
                if verdict == 'must-be-null':
                    f.need(cause is None,
                           'S5 owner carrier law (nativeCause must-be-null)',
                           'CARRIER_NATIVE_CAUSE_IS_NULL_FOR_THIS_DEFICIENCY',
                           dict(where, carrier=row.get('carrier')))
                elif verdict == 'required':
                    f.need(cause is not None and cause in allowed,
                           'S5 owner carrier law (nativeCause required)',
                           'CARRIER_NATIVE_CAUSE_IS_A_MEMBER_OF_ALLOWED_CAUSES',
                           dict(where, allowedCauses=allowed,
                                carrier=row.get('carrier')))
                elif verdict == 'optional':
                    f.need(cause is None or cause in allowed,
                           'S5 owner carrier law (nativeCause optional)',
                           'CARRIER_NATIVE_CAUSE_IS_NULL_OR_ALLOWED',
                           dict(where, allowedCauses=allowed))
                else:
                    f.need(False, 'S5 registry row nativeCause verdict',
                           'REGISTRY_ROW_NATIVE_CAUSE_VERDICT_IS_RECOGNISED',
                           dict(where, verdict=verdict))
                if row.get('carrier', '').startswith('entry.') \
                        and row['carrier'] != 'entry.nativeCause':
                    f.ok('S5 "Native DeficiencyV2 members keep owner carrier law"',
                         'CARRIER_FIELD_IS_NOT_A_SUBJECT_INVENTORY_FIELD_SO_ONLY_THE_'
                         'NATIVE_CAUSE_VERDICT_TRANSFERS',
                         dict(where, carrier=row['carrier'],
                              note=('a SubjectInventoryV1 has no Coverage entry, so the '
                                    'carrier FIELD cannot be checked here; the enumeration '
                                    'contract names this case for a timeout and the '
                                    'nativeCause verdict is what this record must honour')))

        # ---- S6 examinedPaths vs the extent of THIS kind
        kext = ext.get(kind, set())
        f.need(set(inv['examinedPaths']) <= kext,
               'S6 examinedPaths DESC "Each examined path MUST be a member of that extent"',
               'EXAMINED_PATHS_SUBSET_OF_THE_KIND_EXTENT',
               dict(where, outside=sorted(set(inv['examinedPaths']) - kext)))
        if state == 'complete' and kind == 'file':
            paths = {r['path'] for r in inv['rows']}
            f.need(set(inv['examinedPaths']) == kext and paths == kext,
                   'S6 "COMPLETE FILE requires set equality with the file extent AND a row '
                   'per path"',
                   'COMPLETE_FILE_TOTALITY', dict(where, rows=sorted(paths),
                                                  extent=sorted(kext)))

        # ---- S7 row shape and the language table
        seen_ids, seen_pkg = set(), set()
        for r in inv['rows']:
            f.need(r['kind'] == kind, 'S7 InventoryRowV1.kind',
                   'ROW_KIND_EQUALS_THE_INVENTORY_KIND',
                   dict(where, row=r['path'], rowKind=r['kind']))
            if kind in ('file', 'package'):
                f.need(r['signatureTokens'] == [],
                       'S7 signatureTokens DESC "File/package MUST be empty (canonical [] '
                       'discriminator)"',
                       'FILE_OR_PACKAGE_ROW_HAS_CANONICAL_EMPTY_TOKENS',
                       dict(where, row=r['path']))
            if kind == 'package':
                base = r['path'].rsplit('/', 1)[-1]
                want = {'package.json': 'json', 'Cargo.toml': 'toml'}.get(base)
                f.need(r['subjectLanguage'] == want,
                       'S7 x-opensip-subject-language-table.packageLanguage '
                       '("Manifest FORMAT language only")',
                       'PACKAGE_ROW_LANGUAGE_IS_THE_MANIFEST_FORMAT',
                       dict(where, row=r['path'], declared=r['subjectLanguage'],
                            derived=want))
                key = (r['nativeSubjectId'], r['path'])
                f.need(key not in seen_pkg, 'S7 rows DESC package uniqueness',
                       'PACKAGE_ROW_UNIQUE_BY_NATIVE_ID_AND_PATH', dict(where, key=key))
                seen_pkg.add(key)
            else:
                want = language_of(r['path'], lang_table)
                f.need(r['subjectLanguage'] == want,
                       'S7 x-opensip-subject-language-table (longest suffix wins; unlisted '
                       '=> unspecified)',
                       'ROW_SUBJECT_LANGUAGE_IS_THE_SUFFIX_TABLE_VALUE',
                       dict(where, row=r['path'], declared=r['subjectLanguage'],
                            derived=want))
                f.need(r['nativeSubjectId'] not in seen_ids,
                       'S7 rows DESC file/symbol uniqueness',
                       'FILE_OR_SYMBOL_ROW_NATIVE_ID_UNIQUE',
                       dict(where, id=r['nativeSubjectId']))
                seen_ids.add(r['nativeSubjectId'])
            if kind == 'file':
                f.need(r['qualifiedName'] == r['path'],
                       'S7 enumeration-contract section 8 "File qualifiedName equals path"',
                       'FILE_ROW_QUALIFIED_NAME_EQUALS_PATH', dict(where, row=r['path']))
            f.need(r['path'] in inv_paths,
                   'S7 "no fake external snapshot paths"',
                   'ROW_PATH_IS_A_SNAPSHOT_MEMBER', dict(where, row=r['path']))

        # ---- S8 parse/classification failure cannot be complete
        if kind == 'package':
            failed = []
            for p in sorted(kext):
                base = p.rsplit('/', 1)[-1]
                by = st.get_blob(inv_paths[p]['sha256']) if p in inv_paths else None
                if by is None:
                    failed.append(p)
                    continue
                try:
                    if base == 'package.json':
                        nm = json.loads(by.decode()).get('name')
                    else:
                        import tomllib
                        nm = (tomllib.loads(by.decode()).get('package') or {}).get('name')
                except Exception:
                    failed.append(p)
                    continue
                if not (isinstance(nm, str) and nm):
                    pass     # nameless manifest: not a subject, not a failure
            if failed:
                f.need(state == 'partial' and dfc == 'source-syntax-invalid',
                       'S8 enumeration-contract section 4 "Parse/classification failure '
                       'cannot be complete ... it is partial with local deficiency '
                       'source-syntax-invalid"',
                       'PARSE_FAILURE_IS_PARTIAL_WITH_THE_LOCAL_MEMBER',
                       dict(where, failedManifests=failed))
            else:
                f.ok('S8 no parse failure in this candidate extent',
                     'NO_MANIFEST_PARSE_FAILURE_TO_CLASSIFY', dict(where))
            f.need(dfc != 'provider-unavailable',
                   'S4 "Parse/classification failure ... NEVER provider-unavailable"',
                   'PACKAGE_INVENTORY_DOES_NOT_REWRITE_A_PARSE_FAILURE_AS_PROVIDER_'
                   'UNAVAILABLE', where)
    return f


def main():
    out, total = {}, 0
    for label in RUNS:
        f = check(label)
        out[label] = {'checks': f.rows,
                      'passed': sum(1 for r in f.rows if r['result'] == 'PASS'),
                      'notApplicable': sum(1 for r in f.rows
                                           if r['result'] == 'NOT-APPLICABLE'),
                      'refused': len(f.refusals), 'refusals': f.refusals}
        total += len(f.refusals)
        print('%-13s passed=%-4d refused=%d' % (label, out[label]['passed'],
                                                out[label]['refused']))
        for r in f.refusals:
            print('    REFUSE %-56s %s' % (r['check'][:56],
                                           json.dumps(r['detail'], default=str)[:140]))
    with open(OUT + '/vectors/indep-subject-inventory.json', 'w') as fh:
        json.dump({'standing': __doc__, 'runs': out, 'totalRefusals': total}, fh,
                  indent=1, default=str)
    print('total refusals:', total)


main()

"""CB7-MUST-1 (2/4): the retained-closure binding, beside coverage_dialect_prerequisite."""
import pathlib

W = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1/work')
P = W / 'docs/coop/design-corrections/foundation/identity-model.py'
s = P.read_text(encoding='utf-8')

ANCHOR = """    def relation_source_joins(value,row,fact):
"""
NEW = '''    def coverage_source_variant_prerequisite(scope,coverage_payload):
        """A Coverage claim about a body-dialect relation under a CLOSED SUFFIX TABLE universe must
        be consistent with whether that universe reads the subjects at all.

        THE SIBLING OF `coverage_dialect_prerequisite`, AND DISJOINT FROM IT. Each dialect `form`
        has exactly one owning scope prerequisite and they select on that form: the ownership form
        returns early here, this closed-suffix-table form has no `ownership` key and returns early
        there. Together with the syntax universe`s `syntax_capability_prerequisite` every published
        universe now has a TOTAL scope interpretation, so there is no third reading in which a
        request is neither served nor disclosed.

        WHAT WAS OPEN. `body_language_version` refuses an unlisted suffix with the registry`s own
        `onUnknown` - `BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN` - so the FACT boundary was already
        total. But that selector runs only while a body is being derived, and a scope with NO facts
        derives none: a `clones` scope over `package.json` under the TypeScript universe reached no
        classification at all and could claim `coverage: complete` with a null deficiency, a
        determinate `no clones here` about a file that universe cannot read as any TypeScript
        dialect. Coverage is a claim about the EXAMINATION, so it cannot be decided by whether the
        examination happened to produce output.

        WHAT IS CLAIMED AND WHAT IS NOT. Unsupported means UNKNOWN coverage with the published
        `language-tier-unsupported` / `capability-missing` pair - the same existing vocabulary the
        syntax universe uses, no new deficiency and no new cause. It is emphatically NOT a statement
        that no clone exists, and it qualifies no compiler: nothing here executes tsc, decides
        whether a listed suffix would actually parse, or ranks dialects. The only question asked is
        the registry`s own - does this path`s suffix select a variant in the closed table the
        universe published - and the answer is derived from the OWNING universe record and the
        scope`s subjects, never read from the claim being judged.

        SCOPE OF THE GATE. `bodyIdentityJoin`, exactly as the ownership sibling: the dialect axis is
        consulted where a body identity is joined, which under today`s relation registry is `clones`
        alone. Extending it to `declares` or `references` would assert that a suffix table decides
        symbol capability, which no published law says. Inventory relations never reach it both by
        that gate and by `INVENTORY_CAPABILITIES` inside the derivation, so `file`, `package` and
        `vcs-change` keep their promised meaning on every inventoried path.

        `clones` is a `source-path` relation, so the live branch judges THIS scope`s own subjects and
        requires ALL of them: a mixed `src/a.ts` + `package.json` scope discloses rather than hiding
        its unsupported half behind its supported half, and an empty subject list is unsupported
        rather than vacuously complete. The `symbol` branch mirrors `syntax_capability_prerequisite`
        for a future row that joins a body identity to a non-path subject kind; no relation reaches
        it today. Like its siblings it never inspects whether facts exist, so an EMPTY view is judged
        on the same evidence as a populated one."""
        row=RELATIONS.get(scope['relation'])
        if row is None or 'bodyIdentityJoin' not in row:return
        admit_frame(scope['sourceUniverse'],'native-semantic-universe')
        domain,universe,universe_row,universe_retained=native_universes[scope['sourceUniverse']]
        dialect=universe_row.get('languageVersionBinding',{}).get('dialect')
        if not isinstance(dialect,dict) or dialect.get('form')!='closed-suffix-table':return
        if row.get('subjectKind')=='source-path':
            paths,require_all=list(scope['subjects']),True
        else:
            paths,require_all=[item['path'] for item in get(scope['snapshotId'],'snapshot')['sourceInventory']],False
        owed=native_admission().source_variant_capability_support(
            dialect,scope['relation'],scope['resolution'],paths,require_all)
        if owed is None:return
        entry=coverage_payload['entry']
        label=scope['relation']+'@'+scope['resolution']
        # Three refusals for the three separable faults, the same shape the two sibling guards use:
        # a false COMPLETE, a right-shaped unknown carrying the wrong deficiency, and one carrying
        # the wrong cause. A single combined check would admit an entry that discloses SOMETHING.
        if entry['coverage']=='complete':
            raise C.AdmissionError('COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE:'+label+':'+owed['nativeCause'])
        if entry.get('deficiency')!=owed['deficiency']:
            raise C.AdmissionError('COVERAGE_SOURCE_VARIANT_DEFICIENCY_MISMATCH:'+label+':expected='
                                   +owed['deficiency']+':declared='+str(entry.get('deficiency')))
        if entry.get('nativeCause')!=owed['nativeCause']:
            raise C.AdmissionError('COVERAGE_SOURCE_VARIANT_CAUSE_MISMATCH:'+label+':expected='
                                   +owed['nativeCause']+':declared='+str(entry.get('nativeCause')))

    def relation_source_joins(value,row,fact):
'''
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, NEW)

CALL = """            coverage_dialect_prerequisite(scope,coverage_payload)
            syntax_capability_prerequisite(scope,coverage_payload)
"""
CALL_NEW = """            coverage_dialect_prerequisite(scope,coverage_payload)
            coverage_source_variant_prerequisite(scope,coverage_payload)
            syntax_capability_prerequisite(scope,coverage_payload)
"""
assert s.count(CALL) == 1
s = s.replace(CALL, CALL_NEW)
P.write_text(s, encoding='utf-8')
print('ok')

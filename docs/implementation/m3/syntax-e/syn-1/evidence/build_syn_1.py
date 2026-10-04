"""Build contract successor SYN-1 (law M3-E1 r3, item 19: the native contract successor) deterministically.

Writes, under docs/implementation/m3/syntax-e/:
  syn-1/design/native/native-evidence.schemas.v2.json       (NES successor copy)
  syn-1/product/schemas/sources/native-v2.schema.json       (product native source successor copy)
  syn-1/PASSAGES.md, syn-1/materialization-map.json, syn-1/evidence/copies-report.json,
  syn-1/successor.json and syn-1-subject.json.

The NE text passages are line overrides (NE is Markdown). The two JSON documents are complete successor
copies (I1-L's form, LD-L1): each copy is its parent's raw bytes with every passage override the product
lock binds to that parent applied in place (there are none today; asserted), then SYN-1's edits:
  - "source-parse-error" inserted at its code-point position (before "source-replacement-outside-snapshot")
    in #/$defs/NativeCause/enum and in
    #/x-opensip-deficiency-cause-registry/deficiencies/input-closure-incomplete/allowedCauses;
  - that registry row's `rule` text, whose "twelve" becomes false, restated for thirteen.
Nothing else changes.

The lock is read at BASE_REV with read-only `git show`; the output does not depend on any other revision.
The checks restate tools/verify_design.py's contract_successor and successor_chain rules for this record.

Usage: python3.14 -I -B evidence/build_syn_1.py [--product /path/to/opensip] [--check]
--check rebuilds in memory and compares with the files on disk instead of writing.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/syntax-e'
UNIT = f'{BASE}/syn-1'
BASE_REV = 'cd5958b'          # product main at drafting (82 contract successors); read-only
LAW = f'{BASE}/PROPOSAL-r3.md'
LAW_SHA256 = 'd71031ff1aee01ba20b471e9db1891f4a0e976751741ffa10a783585eedd7c46'

NE = 'docs/v2/contracts/product-v1/native-evidence.md'
NES = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
PNES = 'docs/implementation/m1/source-selection-v2/schemas/sources/native.v2.schema.json'
COPIES = {  # parent -> (copy path, product path or None)
    NES: (f'{UNIT}/design/native/native-evidence.schemas.v2.json', None),
    PNES: (f'{UNIT}/product/schemas/sources/native-v2.schema.json', 'schemas/sources/native-v2.schema.json'),
}
MEMBER = 'source-parse-error'
NEXT_MEMBER = 'source-replacement-outside-snapshot'
ENUMS = ['/$defs/NativeCause/enum',
         '/x-opensip-deficiency-cause-registry/deficiencies/input-closure-incomplete/allowedCauses']
RULE = '/x-opensip-deficiency-cause-registry/deficiencies/input-closure-incomplete/rule'
RULE_OLD = ('The one deficiency whose cause genuinely IS a single named missing input, which is why section 10 '
            'lists twelve of them and why the three body-language-* members were added here.')
RULE_NEW = ('The one deficiency whose cause genuinely IS a single named missing or unreadable input, which is why '
            'section 10 lists thirteen of them, why the three body-language-* members were added here, and why '
            'contract successor SYN-1 of law M3-E1 added source-parse-error: a code-grammar file under the syntax '
            'universe whose bytes are not valid UTF-8 or whose validated tree has an ERROR or MISSING node, so that '
            'no fact and no body of it is admitted (native-evidence section 1.2, per-file parse outcomes).')

# ---------------------------------------------------------------------------------------------------------
# NE passages. (line, anchor, text, kind, source). kind: 'append' (after the line), 'insert' (after the
# anchor, which occurs exactly once in the line), 'block' (after the line, separated by a blank line) or
# 'row' (a new table row after the line).
# ---------------------------------------------------------------------------------------------------------
NE288 = (' **A data-document row is a format definition, never a parser** (contract successor SYN-1 of law '
         'M3-E1, item 8): its `grammarDigest` names a definition record with `parse: "none"`, no parser for it '
         'is pinned, built, linked or run, and no data-document file reaches the syntax pass\'s parser or '
         'receives a parse outcome.')

# (key, emitted forms, subject, raised when, branch). Every emitted form is literal except <placeholders>.
KEY_FORMS = [
    ('native.syntax-grammar-version-not-from-manifest', ['native.syntax-grammar-version-not-from-manifest'],
     'none (bare)', 'the grammar closure\'s `semanticVersion` differs from `parserVersion` (§1.2)', 'both'),
    ('native.syntax-grammar-bundle-not-in-closure', ['native.syntax-grammar-bundle-not-in-closure'],
     'none (bare)', '`bundleDigest` is not a member of the closure tree (§1.2)', 'both'),
    ('native.syntax-grammar-not-in-closure', ['native.syntax-grammar-not-in-closure:<grammarId>'],
     'the row\'s `grammarId`', 'a row\'s `grammarDigest` is not a member of the closure tree (§1.2)', 'both'),
    ('native.syntax-normalizer-spec-not-in-closure', ['native.syntax-normalizer-spec-not-in-closure'],
     'none (bare)', '`normalizer.specificationDigest` is not a member of the closure tree (§1.2)', 'both'),
    ('native.syntax-grammar-suffix-ambiguous', ['native.syntax-grammar-suffix-ambiguous:<suffix>'],
     'the suffix', 'a suffix is owned by more than one row, once per suffix (§1.2)', 'both'),
    ('native.syntax-grammar-language-not-in-capability-registry',
     ['native.syntax-grammar-language-not-in-capability-registry:<languageId>'],
     'the row\'s `languageId`', 'the row\'s language has no registry row (§1.2)', 'both'),
    ('native.syntax-grammar-class-not-the-registered-one',
     ['native.syntax-grammar-class-not-the-registered-one:<languageId>:declared=<syntaxClass>:registered=<syntaxClass>'],
     'the row\'s `languageId`, then its declared and the registry\'s `syntaxClass`',
     'the row\'s `syntaxClass` is not the registry\'s (§1.2)', 'both'),
    ('native.syntax-grammar-code-language-not-body-identifiable',
     ['native.syntax-grammar-code-language-not-body-identifiable:<languageId>'],
     'the row\'s `languageId`', 'a `code` language is not in the `body-language-version` enum (§1.2)', 'both'),
    ('native.syntax-grammar-data-language-claims-body-identity',
     ['native.syntax-grammar-data-language-claims-body-identity:<languageId>'],
     'the row\'s `languageId`', 'a `data-document` language is in the `body-language-version` enum (§1.2)', 'both'),
    ('native.syntax-grammar-suffix-not-bundled-for-language',
     ['native.syntax-grammar-suffix-not-bundled-for-language:<suffix>:<languageId>'],
     'the suffix, then the row\'s `languageId`', 'a row claims a suffix the discovery table routes elsewhere (§1.2)',
     'both'),
    ('native.syntax-grammar-not-in-bundle', ['native.syntax-grammar-not-in-bundle:<grammarId>'],
     'the selected `grammarId`', 'universe binding selects a grammar the bundle lacks (§1.2)', 'both'),
    ('native.syntax-grammar-closure-absent', ['native.syntax-grammar-closure-absent'],
     'none (bare)', 'no `kind=grammar` closure is installed, so no syntax context can be minted (SYN-1)', 'both'),
    ('native.syntax-grammar-bundle-manifest-mismatch',
     ['native.syntax-grammar-bundle-manifest-mismatch:<member>:path|size|canonical|digest',
      'native.syntax-grammar-bundle-manifest-mismatch:descriptor:<field>',
      'native.syntax-grammar-bundle-manifest-mismatch:unlisted:<treePath>',
      'native.syntax-grammar-bundle-manifest-mismatch:runtime-pin'],
     '`<member>` is the fixed tree path of the manifest, the normalizer specification, the build receipt or a '
     'module; `<field>` a `SyntaxGrammarBundleV1` field; `<treePath>` a member no root reaches',
     'A3 (fixed path, size, canonical bytes, digest); A4 (descriptor against manifest); A6 (an unlisted member, or '
     'runtime pins that differ across definitions)', 'both'),
    ('native.syntax-grammar-definition-mismatch',
     ['native.syntax-grammar-definition-mismatch:<grammarId>:path|size|canonical|digest',
      'native.syntax-grammar-definition-mismatch:<grammarId>:grammarId|languageId|syntaxClass|suffixes|grammarVersion',
      'native.syntax-grammar-definition-mismatch:<grammarId>:member:<treePath>'],
     'the row\'s `grammarId`, then the check, the disagreeing field, or the missing member\'s tree path',
     'A3 (the definition record); A5 (definition against manifest row); A6 (a listed member missing or wrong)',
     'both'),
    ('native.syntax-grammar-normalization-map-mismatch',
     ['native.syntax-grammar-normalization-map-mismatch:missing|size|canonical',
      'native.syntax-grammar-normalization-map-mismatch:normalizerId|levels',
      'native.syntax-grammar-normalization-map-mismatch:<level>:missing|path|digest|bytes'],
     'the check, or the level and its check', 'A3 (the map); A6 (the map\'s normalizer, its levels, a level file)',
     'both'),
    ('native.syntax-grammar-execution-model-mismatch', ['native.syntax-grammar-execution-model-mismatch:<grammarId>'],
     'the row\'s `grammarId`', 'A7 (`executionModel` against module presence)', 'both'),
    ('native.syntax-grammar-engine-mismatch', ['native.syntax-grammar-engine-mismatch:<field>'],
     '`name`, `version` or `fuelModel` of the engine; a `limits` member\'s name; or `runtime` (the definitions\' '
     'runtime pin against the compiled-in runtime)', 'A8 (engine identity, limit ranges, runtime)', 'both'),
    ('native.syntax-grammar-bundle-not-the-registry', ['native.syntax-grammar-bundle-not-the-registry'],
     'none (bare)', 'A12 (the bundle\'s rows are not the whole registry, M3-E1 item 7)', 'both'),
    ('native.syntax-normalizer-kind-unknown', ['native.syntax-normalizer-kind-unknown:<grammarId>:<name>'],
     'the row\'s `grammarId`, then the node kind, anonymous token or field name',
     'A12 (a name that `normalizer.v1.json` or a mapped level specification uses for the row is not in its '
     '`SymbolTableV1`)', 'both'),
    ('native.syntax-grammar-build-mismatch',
     ['native.syntax-grammar-build-mismatch:<grammarId>:grammarDigest|languageAbi|symbolTableSha256|runtimeVersion',
      'native.syntax-grammar-build-mismatch:<grammarId>:linked-symbol-table'],
     'the row\'s `grammarId`, then the compiled-in table field the definition disagrees with, or '
     '`linked-symbol-table` when the table recomputed from the linked `Language` disagrees',
     'A9 to A11 bound to the linked code', '`native-linked-v1` (selected)'),
    ('native.syntax-grammar-module-invalid',
     ['native.syntax-grammar-module-invalid:<grammarId>:<reason>',
      'native.syntax-grammar-module-invalid:<grammarId>:admission-call'],
     'the row\'s `grammarId`, then the validator\'s reason, or `admission-call`', 'A9; A11\'s admission calls',
     '`wasm32-fuel-v1` (inactive)'),
    ('native.syntax-grammar-module-import-forbidden', ['native.syntax-grammar-module-import-forbidden:<grammarId>'],
     'the row\'s `grammarId`', 'A9 (any import)', '`wasm32-fuel-v1` (inactive)'),
    ('native.syntax-grammar-module-exports-mismatch',
     ['native.syntax-grammar-module-exports-mismatch:<grammarId>:<export>'],
     'the row\'s `grammarId`, then the export name', 'A10 (closed, typed exports)', '`wasm32-fuel-v1` (inactive)'),
    ('native.syntax-grammar-abi-mismatch', ['native.syntax-grammar-abi-mismatch:<grammarId>'],
     'the row\'s `grammarId`', 'A11 (shim ABI)', '`wasm32-fuel-v1` (inactive)'),
    ('native.syntax-grammar-symbol-table-mismatch',
     ['native.syntax-grammar-symbol-table-mismatch:<grammarId>:digest|languageAbi|bounds'],
     'the row\'s `grammarId`, then the check', 'A11 (`SymbolTableV1` from the module)', '`wasm32-fuel-v1` (inactive)'),
]


def key_row(row):
    key, forms, subject, when, branch = row
    # A pipe inside a table cell is written \\| (as law M3-E1's own tables do), so the row keeps five cells.
    cell = '; '.join('`' + f.replace('|', '\\|') + '`' for f in forms)
    return '| `{}` | {} | {} | {} | {} |'.format(key, cell, subject, when, branch)


NE306 = '\n'.join([
    '**Per-file parse outcomes under the syntax universe (contract successor SYN-1 of law M3-E1, items 10, 11 '
    'and 14a).** The host\'s syntax pass decides exactly one outcome for each file of an examined extent that a '
    'selected `code` grammar row reads. A `data-document` file has no outcome: it is never parsed, and its '
    'inventory evidence above is unaffected. The grammar bundle manifest\'s `executionModel` says how the '
    'grammars execute. `native-linked-v1`, the branch law M3-E1 item 3 selected through its probe E0 '
    '(`docs/implementation/m3/syntax-e/E0-REPORT.md`), links them into the host. `wasm32-fuel-v1` runs them as '
    'WebAssembly modules and is **inactive unless the lead\'s M4 re-decision (M3-E1 item 18) selects it**. '
    'Outcomes, bounds and routes are the same on both branches except where a branch is named.',
    '',
    '| Outcome | When | Facts and bodies from the file | Coverage of a code capability over a scope whose extent contains the file |',
    '|---|---|---|---|',
    '| `parsed` | the validated tree has no ERROR node and no MISSING node | admissible | `complete` is possible, under the capability law below |',
    '| `syntax-error` | the bytes are not valid UTF-8 (the parser is not run), or the validated tree has any ERROR or MISSING node | none: no fact and no body | `unknown`; deficiency `input-closure-incomplete`; `nativeCause` `source-parse-error`; `examinedExhaustive` true |',
    '| `truncated:<bound>` | a bound of the manifest\'s identity-bearing `limits` is reached: `size` (more than `maxFileBytes`; the parser is not run); `fuel`, the work bound (under `native-linked-v1` an operation budget counted in parse-progress callbacks; under `wasm32-fuel-v1` engine fuel); `nodes` (`maxNodes`, and also a `SubjectIdV1` text that would exceed its 4,096 characters, which is never shortened); `depth` (`maxDepth`); and, under `wasm32-fuel-v1` only, `memory` (`maxMemoryPages`) | none | `unknown`; `budget-exhausted`; `nativeCause` null; `resolutionCompleteness.stageTerminal` `budget-exhausted`; `examinedExhaustive` false |',
    '| `backend-fault` | a tree that fails validation (below); under `wasm32-fuel-v1` also a trap other than fuel or memory exhaustion, or a protocol violation by the module | none | **none: not a Coverage answer.** The syntax step fails on the `native.syntax-backend-fault` route (§10) and is never retried with another backend |',
    '',
    '- **The selected branch\'s residual risk.** Under `native-linked-v1` a crash, stack overflow or allocation '
    'failure inside the linked parser is **not an outcome**: it ends the host process. It is a declared residual '
    'risk of that branch (M3-E1 item 18), not a typed return, and no Coverage, candidate envelope or Run follows '
    'from it. Under `native-linked-v1` the `memory` bound does not exist; `maxFileBytes` and `maxNodes` bound the '
    'work instead.',
    '- **The whole file.** Any ERROR or MISSING node makes the whole file `syntax-error`. Error-free subtrees are '
    'never salvaged, because error recovery can re-attribute structure outside the ERROR subtree. No byte is '
    'rewritten before parsing: no BOM stripping, newline normalization or re-encoding.',
    '- **Several outcomes in one scope** declare one pair, chosen by §10\'s precedence: `input-closure-incomplete` '
    'outranks `budget-exhausted`. The retained `resolutionCompleteness.stageTerminal` may still record '
    '`budget-exhausted`. Inventory Coverage never depends on a parse outcome.',
    '- **Clones.** A body in a file that is not `parsed` is owed and unexamined: its required `clones` cell is '
    '`unknown` and the body is never filtered out of the obligation.',
    '- **Tree validation, on both branches.** The host validates every tree completely before any use. A tree is '
    'the preorder of the visible nodes of the parse, each decoded to a symbol, a field, the flags `named`, `extra`, '
    '`error` and `missing`, a start byte, an end byte and a child count. It is valid only if every range lies '
    'within the input bytes and within its parent\'s range; siblings are ordered and do not overlap; child counts '
    'agree with the preorder; the node count and depth are within `maxNodes` and `maxDepth`; every field id is 0 '
    '(no field) or an id of the grammar\'s `SymbolTableV1` field list; and every symbol is an id of that table\'s '
    'symbol list, **with one exception: the reserved ERROR symbol 65535 (0xFFFF)**. That symbol is lawful exactly '
    'on a node whose `error` flag is set, and the `error` flag is set exactly on nodes carrying it. '
    '`SymbolTableV1` lists ids 0 to n−1 contiguously and never lists 65535. The runtime\'s internal ERROR_REPEAT '
    'symbol 65534 never appears among visible nodes and is not lawful there. A node with symbol 65535 makes the '
    'file `syntax-error`. A tree that fails validation is `backend-fault`, never `syntax-error`: a malformed tree '
    'is a defect of a trusted component, not a property of the source.',
    '- **The tree\'s byte layout is not contract.** Under `native-linked-v1` the tree is the host\'s own projection '
    'of the linked runtime\'s tree. Under `wasm32-fuel-v1` it is the shim export ABI (`shimAbi` 1), bound by the '
    'module and shim digests. Unit E2a fixes the layout; the probe layout the E0 report documents is not '
    'normative.',
    '- **The `clones-near` candidate envelope.** `clones-near` has no Coverage. A syntax-only `clones-near` '
    'binding\'s executed result is exactly one retained `CandidateProducerResultV1` (execution-inputs §6), and the '
    'same outcomes decide its pair and its `examinedPaths`:',
    '  - every census path `parsed` and no group withheld: `complete`, with a null pair and `examinedPaths` equal '
    'to the census. An explicit `[]` census is `complete` with `examinedPaths: []`, `groupDigests: []` and '
    '`sourceBodies: []`. A successful result with no group is `complete` with `examinedPaths` equal to the census, '
    '`groupDigests: []` and `sourceBodies: []`;',
    '  - a census path `syntax-error`: `partial`, `input-closure-incomplete` / `source-parse-error`;',
    '  - a census path `truncated`, or a group withheld by the retention rule below: `partial`, '
    '`budget-exhausted` / null;',
    '  - a census path that no selected code row reads: `partial`, `language-tier-unsupported` / '
    '`capability-missing`;',
    '  - one pair per envelope, chosen by §10\'s precedence (`language-tier-unsupported`, then '
    '`input-closure-incomplete`, then `budget-exhausted`). `examinedPaths` lists exactly the `parsed` census '
    'paths, and groups and `sourceBodies` come from bodies of `parsed` paths only.',
    '- **Group retention.** A group with more than `maxCandidatesPerGroup` (4,096) members is withheld. The other '
    'groups are taken in ascending order of their group digest, the raw SHA-256 of the canonical '
    '`CloneCandidateGroupV2` bytes. The retained set is the longest prefix of that order with at most '
    '`maxGroupsPerUniverse` (1,000,000) groups and at most 100,000 distinct member ids, the `sourceBodies` bound; '
    'every later group is withheld whole. Groups are never cut, every member of a retained group has exactly one '
    '`sourceBodies` row, and no other row exists. An envelope that withheld anything is `partial`, never '
    '`complete`.',
    '- **No envelope** follows a `backend-fault` or a cancelled step. `unavailable` is never emitted for a selected '
    'syntax binding: a missing or inadmissible grammar closure refuses before PlanId (§10\'s syntax grammar '
    'context route).',
    '- **The trust limit.** Evaluator replay does not re-parse, so a host that misreports an outcome is not caught '
    'by replay. This is the same boundary as provider-produced Coverage. The determinism suite re-derives outcomes '
    'from the retained bytes and closure.',
    '',
    '**Syntax grammar context refusal keys and their emitted forms (contract successor SYN-1 of law M3-E1, item '
    '5).** Each key below takes §10\'s syntax grammar context route, and is emitted exactly in the form shown: a '
    'bare key, or the key, a colon and the subject shown. `<grammarId>`, `<languageId>`, `<suffix>` and '
    '`<syntaxClass>` are the offending row\'s own values; an alternative written `a|b` is one of the listed words. '
    'The first eleven are §1.2\'s existing checks, in exactly the forms the native reference model emits; that model '
    'is unchanged. A descriptor that names a grammar closure the host did not retain, or one that is malformed, '
    'recomputes to another identity or has the wrong kind, refuses as any native context does (§2.3\'s closure '
    'keys, subject `grammarBundle.closureId`); `native.syntax-grammar-closure-absent` is the different case in which '
    'no grammar closure is installed at all, so no descriptor can be built.',
    '',
    '| Key | Emitted form | Subject | Raised when | Branch |',
    '|---|---|---|---|---|',
] + [key_row(row) for row in KEY_FORMS])

NE3366_ANCHOR = '`body-language-owner-ambiguous`'
NE3366 = (', `source-parse-error` (a code-grammar file under the syntax universe whose bytes are not valid UTF-8 '
          'or whose validated tree has an ERROR or MISSING node; §1.2 per-file parse outcomes, contract successor '
          'SYN-1)')

NE3530 = ('| **syntax grammar context** (§1.2; contract successor SYN-1 of law M3-E1, item 5): no admissible '
          '`kind=grammar` closure is installed, so `native.context.syntax.v2` cannot be minted and no other parser '
          'is substituted (`native.syntax-grammar-closure-absent`); a §1.2 row check fails '
          '(`native.syntax-grammar-version-not-from-manifest`, `native.syntax-grammar-bundle-not-in-closure`, '
          '`native.syntax-grammar-not-in-closure`, `native.syntax-normalizer-spec-not-in-closure`, '
          '`native.syntax-grammar-suffix-ambiguous`, `native.syntax-grammar-language-not-in-capability-registry`, '
          '`native.syntax-grammar-class-not-the-registered-one`, '
          '`native.syntax-grammar-code-language-not-body-identifiable`, '
          '`native.syntax-grammar-data-language-claims-body-identity`, '
          '`native.syntax-grammar-suffix-not-bundled-for-language`, and at universe binding '
          '`native.syntax-grammar-not-in-bundle`); or the execution admission chain refuses the installed closure. '
          'On both branches: `native.syntax-grammar-bundle-manifest-mismatch`, '
          '`native.syntax-grammar-definition-mismatch`, `native.syntax-grammar-normalization-map-mismatch`, '
          '`native.syntax-grammar-execution-model-mismatch`, `native.syntax-grammar-engine-mismatch`, '
          '`native.syntax-grammar-bundle-not-the-registry`, and `native.syntax-normalizer-kind-unknown` (a node kind '
          'or field that `normalizer.v1.json` or a level specification of the closure\'s normalization map names '
          'for a row is absent from that row\'s `SymbolTableV1`). Under `native-linked-v1`, the selected branch: '
          '`native.syntax-grammar-build-mismatch`. Under `wasm32-fuel-v1` only, **inactive unless the M4 re-decision '
          'selects it**: `native.syntax-grammar-module-invalid`, `native.syntax-grammar-module-import-forbidden`, '
          '`native.syntax-grammar-module-exports-mismatch`, `native.syntax-grammar-abi-mismatch` and '
          '`native.syntax-grammar-symbol-table-mismatch`. Each key is emitted exactly in the form §1.2\'s table of '
          'syntax grammar context refusal keys gives, bare or with the subject it shows, and the refusals are one '
          'sorted set. A static incompatibility of the installed closure is never '
          '`operational-failed` and never Coverage | | `request-rejected` (2) | `REQUEST.PRECONDITION_FAILED` | '
          'request detail (before PlanId; no Plan is minted and no file is parsed) |')

NE3541 = ('| **syntax backend fault** while parsing a source file after admission (§1.2 per-file parse outcomes; '
          'contract successor SYN-1 of law M3-E1, item 10): a tree that fails validation, on either branch, or, '
          'under `wasm32-fuel-v1` only, a trap other than fuel or memory exhaustion or a protocol violation by the '
          'grammar module (`native.syntax-backend-fault:<grammarId>`). Never retried with another backend; no '
          'Coverage, no candidate envelope and no Run | | `operational-failed` (4) | `SYSTEM.OUTCOME.ILLEGAL_STATE` '
          '(`host-invariant`) | `HOST.INVARIANT_VIOLATED`, subject `native.syntax-backend-fault:<grammarId>` |')

TEXT = [
    (288, None, NE288, 'append', 'item 19 SYN-1 (c): the data-document "format definition, no parse" sentence (item 8)'),
    (306, None, NE306, 'block', 'item 19 SYN-1 (b): the per-file outcome law for Coverage (items 10 and 11) and for '
                                '`clones-near` envelopes (item 14a), with the E0 ERROR-symbol exception'),
    (3366, NE3366_ANCHOR, NE3366, 'insert', 'item 19 SYN-1 (a): the §10 table row gains the cause'),
    (3530, None, NE3530, 'row', 'item 19 SYN-1 (d): the pre-Plan route for every native.syntax-grammar-* and '
                                'native.syntax-normalizer-* key'),
    (3541, None, NE3541, 'row', 'item 19 SYN-1 (e): the backend-fault route (item 10)'),
]

STANDING = (
    'PROPOSED SYN-1 native contract successor (law M3-E1 r3, item 19, SYN-1 (a) to (f)), written for the branch '
    'E0 selected, native-linked-v1, with wasm32-fuel-v1 text kept only where M3-E1 keeps both branches and marked '
    'inactive unless the M4 re-decision selects it. Five insert-only line overrides of native-evidence.md: the '
    'data-document format-definition sentence; the per-file parse outcome law for Coverage and for clones-near '
    'candidate envelopes, with tree validation and the reserved ERROR symbol 65535; the section 10 row gaining '
    'source-parse-error; the pre-Plan syntax grammar context route row; the operational syntax backend fault row. '
    'Complete successor copies of native-evidence.schemas.v2.json and of its selected product source '
    'native.v2.schema.json: source-parse-error inserted at its code-point position in NativeCause and in '
    'input-closure-incomplete.allowedCauses, and that registry row\'s rule restated for thirteen causes; no other '
    'byte changes and no bound override is carried (none is bound). No startup-schema, UnavailableReasonV3, '
    'DeficiencyV2, D9 class, code or exit change; no native model change. The accepted law snapshot is a '
    'candidate so that later units may name it as a parent. Binds together with SYN-1F, immediately before it. '
    'Exact frozen candidate requires actual independent review and root assent.')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def read(path):
    return (ARCH / path).read_bytes()


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def git_show(product, rev, path):
    return subprocess.run(['git', '-C', str(product), 'show', f'{rev}:{path}'], check=True,
                          capture_output=True).stdout


def pointer_get(doc, pointer):
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        doc = doc[int(token)] if isinstance(doc, list) else doc[token]
    return doc


def lock_state(product):
    lock = json.loads(git_show(product, BASE_REV, 'design-lock.json'))
    accepted = {}
    for name in ('sourceManifest', 'applicationManifest'):
        for row in json.loads(read(lock['approvals'][name]['path']))['files']:
            accepted[row['path']] = row
    for binding in lock['inventorySuccessors']:
        accepted[binding['parent']['path']] = binding['parent']
        accepted[binding['candidate']['path']] = binding['candidate']
    bound = {}
    for binding in lock['contractSuccessors']:
        assert pin(binding['record']['path'], read(binding['record']['path'])) == binding['record']
        record = json.loads(read(binding['record']['path']))
        accepted[binding['record']['path']] = binding['record']
        for row in record['candidates']:
            accepted[row['path']] = row
        name = binding['record']['path'].split('/')[-2]
        for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
            bound.setdefault(entry['parent']['path'], []).append((name, entry))
    return lock, accepted, bound


def json_copy(parent, bound):
    raw = read(parent)
    if bound.get(parent):
        raise SystemExit(f'{parent} carries bound overrides; the reviewed form assumes none')
    text = raw.decode('utf-8')
    expected = json.loads(raw)
    lines = text.split('\n')
    edits = []
    for pointer in ENUMS:
        members = pointer_get(expected, pointer)
        if MEMBER in members or members != sorted(members) or NEXT_MEMBER not in members:
            raise SystemExit(f'{parent}{pointer}: unexpected member list')
        want = [json.dumps(m) for m in members]
        hits = [i for i, line in enumerate(lines) if line.rstrip().endswith('[')
                and [x.strip().rstrip(',') for x in lines[i + 1:i + 1 + len(members)]] == want
                and lines[i + 1 + len(members)].strip().startswith(']')]
        if len(hits) != 1:
            raise SystemExit(f'cannot place {pointer} in {parent}: {hits}')
        at = hits[0] + 1 + members.index(NEXT_MEMBER)
        indent = lines[at][:len(lines[at]) - len(lines[at].lstrip())]
        lines.insert(at, indent + json.dumps(MEMBER) + ',')
        members.insert(members.index(NEXT_MEMBER), MEMBER)
        edits.append({'jsonPointer': pointer, 'newMemberLine': at + 1})
    text = '\n'.join(lines)
    old = pointer_get(expected, RULE)
    if not old.startswith(RULE_OLD):
        raise SystemExit('the registry rule text differs from the reviewed one')
    new = RULE_NEW + old[len(RULE_OLD):]
    if text.count(json.dumps(old)) != 1:
        raise SystemExit('cannot place the rule text')
    text = text.replace(json.dumps(old), json.dumps(new))
    pointer_get(expected, '/x-opensip-deficiency-cause-registry/deficiencies/input-closure-incomplete')['rule'] = new
    edits.append({'jsonPointer': RULE,
                  'line': next(n for n, l in enumerate(text.split('\n'), 1) if json.dumps(new) in l)})
    out = text.encode('utf-8')
    if json.loads(out) != expected:
        raise SystemExit(f'{parent}: copy does not parse to the expected document')
    hunks = [{'parentLines': [i1 + 1, i2], 'copyLines': [j1 + 1, j2]} for tag, i1, i2, j1, j2 in
             difflib.SequenceMatcher(None, raw.decode().split('\n'), text.split('\n'), autojunk=False).get_opcodes()
             if tag != 'equal']
    return out, {'parent': pin(parent, raw), 'copy': pin(COPIES[parent][0], out), 'boundOverridesCarried': [],
                 'syn1Edits': edits, 'hunks': hunks}


def overrides():
    raw = read(NE)
    lines = raw.decode('utf-8').splitlines()
    out = []
    for line, anchor, insertion, kind, _why in TEXT:
        before = lines[line - 1]
        if kind == 'append':
            after = before + insertion
        elif kind == 'insert':
            if before.count(anchor) != 1:
                raise SystemExit(f'anchor not unique at NE:{line}')
            cut = before.index(anchor) + len(anchor)
            after = before[:cut] + insertion + before[cut:]
        elif kind == 'block':
            assert lines[line] == '', 'a block insertion needs the blank line after its anchor line'
            after = before + '\n\n' + insertion
        elif kind == 'row':
            assert before.startswith('| ') and before.endswith(' |'), f'NE:{line} is not a table row'
            after = before + '\n' + insertion
        else:
            raise SystemExit(kind)
        out.append({'parent': pin(NE, raw), 'selector': {'line': line}, 'before': before, 'after': after})
    return out


def passages_md(entries):
    parts = ['# SYN-1 passages (generated by evidence/build_syn_1.py; do not edit)', '',
             f'Parent: `{NE}` ({entries[0]["parent"]["bytes"]} bytes, `{entries[0]["parent"]["sha256"]}`). '
             'Each `after` keeps its `before` text word for word and only inserts.', '']
    for (line, _a, _i, kind, why), entry in zip(TEXT, entries):
        parts += [f'## NE:{line} ({kind})', '', f'Source: {why}.', '', '`before`:', '', '~~~~text', entry['before'],
                  '~~~~', '', '`after`:', '', '~~~~text', entry['after'], '~~~~', '']
    return ('\n'.join(parts)).encode('utf-8')


def check(record, subject, files, accepted, bound, lock):
    """verify_design's contract_successor / successor_chain rules for this one record."""
    members = subject['files']
    paths = [row['path'] for row in members]
    assert paths == sorted(set(paths)), 'subject paths must be sorted and unique'
    record_path = f'{UNIT}/successor.json'
    assert {r['path'] for r in record['candidates']} == set(paths) - {record_path}
    for row in members:
        assert pin(row['path'], files[row['path']]) == row
        assert row['path'] not in accepted, f'candidate reuses an accepted path: {row["path"]}'
    parents = record['parents']
    assert [p['path'] for p in parents] == sorted({p['path'] for p in parents}) and parents
    for row in parents:
        assert accepted.get(row['path'], {}).get('sha256') == row['sha256'], row['path']
        assert accepted[row['path']]['bytes'] == row['bytes']
        assert pin(row['path'], read(row['path'])) == row
        assert row['path'] not in paths
    parent_map = {p['path']: p for p in parents}
    seen = set()
    for entry in record['passageOverrides']:
        assert set(entry) == {'parent', 'selector', 'before', 'after'}
        assert parent_map.get(entry['parent']['path']) == entry['parent']
        key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
        assert key not in seen
        seen.add(key)
        assert isinstance(entry['after'], str) and entry['after'] and entry['before'] != entry['after']
        raw = read(entry['parent']['path'])
        assert set(entry['selector']) == {'line'}
        assert raw.decode('utf-8').splitlines()[entry['selector']['line'] - 1] == entry['before']
        try:
            json.loads(raw)
        except ValueError:
            pass
        else:
            raise AssertionError('v4 JSON parent passages require JSON Pointer selectors')
        for name, other in bound.get(entry['parent']['path'], []):
            assert json.dumps(other['selector'], sort_keys=True) != key[1], f'selector already bound by {name}'
    for binding in lock['contractSuccessors']:
        assert binding['record']['path'] != record_path


def build(product):
    lock, accepted, bound = lock_state(product)
    files, reports = {}, []
    for parent, (path, product_path) in COPIES.items():
        out, report = json_copy(parent, bound)
        files[path] = out
        if product_path:
            if git_show(product, BASE_REV, product_path) != read(parent):
                raise SystemExit(f'product {product_path} differs from its accepted parent')
            report['productPath'] = product_path
        reports.append(report)
    design, prod = (json.loads(files[COPIES[p][0]]) for p in (NES, PNES))
    for pointer in ENUMS:
        assert pointer_get(design, pointer) == pointer_get(prod, pointer), 'design and product copies disagree'
    passage_overrides = overrides()
    files[f'{UNIT}/PASSAGES.md'] = passages_md(passage_overrides)
    files[f'{UNIT}/materialization-map.json'] = dumps({
        'schemaVersion': 1,
        'standing': ('Exact schema source bytes for unit E2s: it copies the candidate to its product path and '
                     're-points the generation and admission source maps at it. E2s also applies SYN-1F, the '
                     'evaluator registries and the generated carriers, which this map does not fix. Independent '
                     'review and root assent are required before selection.'),
        'baseProductRev': BASE_REV,
        'files': [{'productPath': r['productPath'], 'candidatePath': r['copy']['path'],
                   'before': {'bytes': r['parent']['bytes'], 'sha256': r['parent']['sha256']},
                   'after': {'bytes': r['copy']['bytes'], 'sha256': r['copy']['sha256']}}
                  for r in reports if 'productPath' in r]})
    files[f'{UNIT}/evidence/copies-report.json'] = dumps({
        'schemaVersion': 1, 'baseProductRev': BASE_REV, 'member': MEMBER, 'copies': reports})
    static = [LAW, f'{UNIT}/README.md', f'{UNIT}/evidence/build_syn_1.py', f'{UNIT}/evidence/check_syn_1.py',
              f'{UNIT}/evidence/verify_scratch.py', f'{UNIT}/evidence/key-forms.json']
    for path in static:
        files[path] = read(path)
    assert sha(files[LAW]) == LAW_SHA256, 'law bytes changed'
    parents = sorted({NE} | set(COPIES))
    record = {'schemaVersion': 1, 'standing': STANDING, 'parents': [pin(p, read(p)) for p in parents],
              'passageOverrides': passage_overrides, 'candidates': [pin(p, files[p]) for p in sorted(files)]}
    files[f'{UNIT}/successor.json'] = dumps(record)
    subject = {'schemaVersion': 1, 'files': [pin(p, files[p]) for p in sorted(files)]}
    files[f'{BASE}/syn-1-subject.json'] = dumps(subject)
    check(record, subject, files, accepted, bound, lock)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = build(args.product.resolve())
    generated = [p for p in files if p.startswith(UNIT + '/') and not p.endswith(('README.md', '.py'))
                 and not p.endswith('key-forms.json')]
    generated.append(f'{BASE}/syn-1-subject.json')
    for path in sorted(set(generated)):
        target = ARCH / path
        if args.check:
            if target.read_bytes() != files[path]:
                raise SystemExit(f'differs: {path}')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[path])
    print(json.dumps({'subject': pin(f'{BASE}/syn-1-subject.json', files[f'{BASE}/syn-1-subject.json']),
                      'successor': pin(f'{UNIT}/successor.json', files[f'{UNIT}/successor.json']),
                      'overrides': len(json.loads(files[f'{UNIT}/successor.json'])['passageOverrides']),
                      'candidates': len(json.loads(files[f'{UNIT}/successor.json'])['candidates']),
                      'checked': args.check}))


if __name__ == '__main__':
    main()

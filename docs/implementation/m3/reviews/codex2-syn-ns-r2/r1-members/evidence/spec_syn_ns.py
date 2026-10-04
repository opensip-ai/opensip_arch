"""The SYN-NS specification documents, as data (contract successor SYN-NS of law M3-E1 r3, items 13 and 14).

build_syn_ns.py imports this module and writes each document's canonical bytes (foundation/canonical.py's rule:
sorted keys, no insignificant whitespace, UTF-8). Nothing here is executed against a repository.

Every node-kind and field name below is checked by check_syn_ns.py against the pinned grammars' symbol tables
and node-types.json (E0's pins).
"""

NORMALIZER_ID = 'opensip.syntax.normalizer'
NORMALIZER_VERSION = '1'
LEVELS = ['L0-verbatim', 'L1-lexical', 'L2-comment-insensitive', 'L3-identifier-insensitive']
CODE_ROWS = ['javascript', 'rust', 'tsx', 'typescript']
TS_LIKE = ['javascript', 'tsx', 'typescript']

CONVENTIONS = {
    'nodeKinds': ('A kind, kinds, child, descendant, firstChild, parentKinds, grandparentKinds, within, leaves or '
                  'other kind-list value names a visible, public, NAMED symbol of the row\'s grammar exactly as its '
                  'SymbolTableV1 lists it (named true, visible true). An anonymous '
                  'value names a visible ANONYMOUS symbol of the row\'s grammar by its exact name. A field or fields '
                  'value names a field of SymbolTableV1\'s field list, and, where the same object names a kind, a '
                  'field the grammar\'s node-types.json declares on that kind (on the child kind, where a rule names '
                  'a child and a field). Grammar admission refuses any other '
                  'name (native.syntax-normalizer-kind-unknown, step A12, as contract successor SYN-1 states it).'),
    'tree': ('Rules read the validated tree of a parsed file (native-evidence section 1.2): the preorder of visible '
             'nodes, with their symbols, fields, flags and byte ranges. A file that is not parsed yields no body, no '
             'token stream and no syntax fact.'),
    'order': 'Array order is part of these bytes. A rule list is applied in the order written; the first rule that '
             'matches a node decides.',
}

PARAMETERS = {
    'source': 'native-evidence.md section 6.2 (selected parameters), copied; a difference is a defect of these bytes',
    'minOccurrences': 2,
    'minBodyBytes': 64,
    'minTokensLevels': 20,
    'minTokensNear': 50,
    'nearThresholdMillionths': 800000,
    'maxCandidatesPerGroup': 4096,
    'maxGroupsPerUniverse': 1000000,
}

# ------------------------------------------------------------------------------------------------------------
# Bodies (normalizer.v1.json)
# ------------------------------------------------------------------------------------------------------------
TS_BODIES = [
    {'kind': 'function_declaration', 'bodyKind': 'function', 'field': 'body'},
    {'kind': 'generator_function_declaration', 'bodyKind': 'function', 'field': 'body'},
    {'kind': 'function_expression', 'bodyKind': 'function', 'field': 'body'},
    {'kind': 'generator_function', 'bodyKind': 'function', 'field': 'body'},
    {'kind': 'method_definition', 'bodyKind': 'method', 'field': 'body'},
    {'kind': 'arrow_function', 'bodyKind': 'lambda', 'field': 'body'},
    {'kind': 'class_static_block', 'bodyKind': 'block', 'field': 'body'},
]
RUST_BODIES = [
    {'kind': 'function_item', 'bodyKind': 'function', 'field': 'body',
     'methodWhen': {'parentKinds': ['declaration_list'], 'grandparentKinds': ['impl_item', 'trait_item']}},
    {'kind': 'closure_expression', 'bodyKind': 'lambda', 'field': 'body'},
    {'kind': 'impl_item', 'bodyKind': 'impl', 'field': 'body'},
    {'kind': 'unsafe_block', 'bodyKind': 'block', 'child': 'block'},
    {'kind': 'async_block', 'bodyKind': 'block', 'child': 'block'},
    {'kind': 'const_block', 'bodyKind': 'block', 'field': 'body'},
    {'kind': 'try_block', 'bodyKind': 'block', 'child': 'block'},
    {'kind': 'gen_block', 'bodyKind': 'block', 'child': 'block'},
]
IMPORT_ONLY = {
    'javascript': {'kinds': ['import_statement'], 'commentKinds': ['comment', 'html_comment']},
    'tsx': {'kinds': ['import_statement', 'import_alias', 'ambient_declaration'],
            'commentKinds': ['comment', 'html_comment']},
    'typescript': {'kinds': ['import_statement', 'import_alias', 'ambient_declaration'],
                   'commentKinds': ['comment', 'html_comment']},
    'rust': {'kinds': ['use_declaration', 'extern_crate_declaration', 'inner_attribute_item'],
             'commentKinds': ['line_comment', 'block_comment']},
}
STATEMENT_CONTAINERS = {'javascript': ['statement_block'], 'tsx': ['statement_block'],
                        'typescript': ['statement_block'], 'rust': ['block', 'declaration_list']}

BODIES_LAW = [
    'A body is the node a row\'s bodies rule selects: the node in the rule\'s field of a node of the rule\'s kind, or, '
    'for a child rule, that node\'s first named child of the child kind. Its span is that node\'s half-open byte '
    'range [start, end) in the snapshot file bytes. These are native-evidence section 6.3\'s function, method, '
    'closure or lambda, impl item and block bodies; a block body is one of the row\'s block-kind rules (a class '
    'static block; a Rust unsafe, async, const, try or gen block), never the block of an if, a loop or a function.',
    'Bodies nest: a body inside another body is a body of its own, and both are owed.',
    'bodyKind is function, method, lambda, impl or block. A Rust function_item is a method when the methodWhen '
    'clause holds. bodyKind is descriptive: it enters no identity.',
    'An import-only body is excluded as a clone candidate at every level (native-evidence section 6.3): a body whose '
    'span node is one of the row\'s statementContainers, has at least one named child, and whose named children are '
    'all of the row\'s importOnly kinds or importOnly commentKinds. A kept body is hashed over its exact bytes; no '
    'statement inside a kept body is stripped.',
    'Body identity and owed bodies follow native-evidence section 6 and identity-and-evidence section 3: languageId is '
    'the row\'s body language (typescript for both the typescript and tsx rows), dialect is {grammarVariant}, and the '
    'level\'s normalisationVersion is the digest of the level specification the closure\'s normalization map names. '
    'The parameters above decide which bodies become candidates.',
]

# ------------------------------------------------------------------------------------------------------------
# Subjects, declares, literals (normalizer.v1.json; law M3-E1 item 13)
# ------------------------------------------------------------------------------------------------------------
SUBJECTS_LAW = [
    'A syntax subject identity is the SubjectIdV1 text "syntax:" + esc(path) + "#" + chain, where path is the '
    'anchor\'s snapshot path and chain is the segments of the subject joined by "/". The file itself is the subject '
    'with the empty chain.',
    'A segment is tag + ":" + esc(name) + "@" + ordinal. tag is the declarationKind of a declares rule, or the tag '
    'of a containers rule (lambda, type, impl or block) for an anonymous container, or stmt, entry or exit for a '
    'control-flow node. name is the declared '
    'name\'s exact source text (empty for an anonymous container and for entry and exit; the node kind for stmt). '
    'For a Rust impl_item, name is the text of its trait field, " for ", and the text of its type field when it has a '
    'trait, else the text of its type field, with every run of ASCII whitespace replaced by one space and leading '
    'and trailing whitespace removed.',
    'esc(s) is s\'s UTF-8 bytes with every byte outside 0x21 to 0x7E, and each of the bytes % # / @ :, written as % '
    'and two uppercase hexadecimal digits. The text is therefore ASCII, NFC and free of controls, and esc is '
    'injective.',
    'ordinal is the decimal count of earlier segments, in preorder of the file, with the same tag and escaped name '
    'and the same parent chain. It is 0 for the first. No byte offset, line number or column enters a subject '
    'identity (identity-and-evidence finding-key2), so inserting a blank line changes no subject.',
    'A container is a node matched by a declares rule marked container, or by a containers rule. When a declares '
    'rule marked container holds for a node (a named function or class expression), its segment is that rule\'s; '
    'otherwise the containers rule\'s (an anonymous one, with the empty name). The chain of a node is the segments '
    'of its enclosing containers (its strict ancestors), outermost first. A declared subject is its container chain '
    'plus its own segment.',
    'A SubjectIdV1 text longer than 4,096 characters makes the file truncated:nodes (law M3-E1 item 11): no fact '
    'from the file, and the identity is never shortened.',
]
DECLARES_LAW = [
    'For each node of a parsed code file that a declares rule matches (in the whole file, not only in bodies), the '
    'host derives one inert declares candidate: declared is the rule\'s subject, container is the subject of the '
    'nearest enclosing container (the file subject when there is none), declarationKind is the rule\'s, and its one '
    'source-text anchor is the matched node\'s span (a binding\'s identifier span for a bindings rule).',
    'A name rule declares the text of the node in its field. A names rule declares each node in its field. A '
    'bindings rule declares each binding of the pattern in its field (or of each named child, for a rule without a '
    'field), by the row\'s patternLaw; bindings of one pattern with the same name are one declaration, anchored at '
    'the first.',
    'A rule with when holds only if the named condition holds; otherwise the next rule is tried.',
    'Data-document rows declare nothing (native-evidence section 1.2). No resolution is claimed: an identifier is not '
    'a reference and a call is not an edge.',
]
LITERALS_LAW = [
    'For each node of a literal rule\'s kind in a parsed code file, the host derives one inert literal candidate: '
    'owner is the subject of the nearest enclosing container (the file subject when there is none), literalKind is '
    'the rule\'s, and its one anchor is the node\'s span. A node of a literal kind inside another literal node (a '
    'string inside a template substitution) is a literal of its own.',
    'valueText is derived from the node\'s exact source text in three steps. (1) Each C0 or C1 control character '
    '(U+0000 to U+001F, U+007F to U+009F) becomes the six characters backslash, u and four uppercase hexadecimal '
    'digits of its code point. (2) The result is put in Unicode Normalization Form C. (3) If it is longer than 4,096 '
    'characters it becomes its first 3,996 characters, U+2026, "sha256:" and the 64 lowercase hexadecimal digits of '
    'the SHA-256 of step 2\'s UTF-8 bytes. valueText is a representation, not an injective encoding: the anchor '
    'locates the exact bytes.',
]
NEAR = {
    'algorithmId': 'near-v1',
    'law': [
        'Input: the L3-identifier-insensitive token stream of every owed, kept body (import-only bodies excluded) with '
        'at least minTokensNear tokens, under the level specification the closure\'s normalization map names for L3.',
        'A shingle is a run of 5 consecutive tokens, encoded as the concatenation of the 5 tokens\' framed encodings '
        '(u16be kind length, kind bytes, u32be value length, value bytes). A body\'s shingle set is the set of its '
        'shingles.',
        'Two bodies with the same body language (languageId) are similar when 1,000,000 times the size of the '
        'intersection of their shingle sets is at least nearThresholdMillionths times the size of their union. Their '
        'similarityMillionths is the floor of 1,000,000 times intersection over union. Bodies of different body '
        'languages are never compared, so a group is never typescript+javascript in this mode.',
        'A group is a connected component, with at least two members, of the graph whose vertices are the bodies and '
        'whose edges are the similar pairs. It is a CloneCandidateGroupV2 with mode near, evidenceLevel '
        'similar-candidate, authority candidate-only, language the body language, grouping connected-component and '
        'scoreMeaning minimum-member-best-neighbor. members are the bodies\' candidate body ids (law M3-E1 item 14a: '
        '"sb1:" and the hex SHA-256 of the canonical {grammarId, path, startByte, endByte}) in ascending byte order. '
        'matchedEdges are the group\'s similar pairs as {left, right, similarityMillionths} with left before right in '
        'byte order, sorted by left and then right. similarityMillionths is the minimum, over members, of each '
        'member\'s best edge.',
        'Group retention, the envelope and its pair follow native-evidence section 1.2 (contract successor SYN-1). A '
        'near group is a candidate, never a fact.',
    ],
}

# Declares rules. A rule is {kind, declarationKind, name|names|bindings: {field}|{} , container?, when?}
TS_DECLARES_COMMON = [
    {'kind': 'function_declaration', 'declarationKind': 'function', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'generator_function_declaration', 'declarationKind': 'function', 'name': {'field': 'name'},
     'container': True},
    {'kind': 'function_expression', 'declarationKind': 'function', 'name': {'field': 'name'}, 'container': True,
     'when': 'has-field'},
    {'kind': 'generator_function', 'declarationKind': 'function', 'name': {'field': 'name'}, 'container': True,
     'when': 'has-field'},
    {'kind': 'method_definition', 'declarationKind': 'method', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'class_declaration', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'class', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True, 'when': 'has-field'},
    {'kind': 'variable_declarator', 'declarationKind': 'variable', 'bindings': {'field': 'name'}},
    {'kind': 'catch_clause', 'declarationKind': 'parameter', 'bindings': {'field': 'parameter'}},
    {'kind': 'for_in_statement', 'declarationKind': 'variable', 'bindings': {'field': 'left'},
     'when': 'binding-kind'},
    {'kind': 'arrow_function', 'declarationKind': 'parameter', 'bindings': {'field': 'parameter'},
     'when': 'has-field'},
]
JS_DECLARES = TS_DECLARES_COMMON + [
    {'kind': 'field_definition', 'declarationKind': 'field', 'name': {'field': 'property'}},
    {'kind': 'formal_parameters', 'declarationKind': 'parameter', 'bindings': {}},
]
TS_DECLARES = TS_DECLARES_COMMON + [
    {'kind': 'abstract_class_declaration', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'interface_declaration', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'type_alias_declaration', 'declarationKind': 'type', 'name': {'field': 'name'}},
    {'kind': 'enum_declaration', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'enum_body', 'declarationKind': 'field', 'names': {'field': 'name'}},
    {'kind': 'enum_assignment', 'declarationKind': 'field', 'name': {'field': 'name'}},
    {'kind': 'internal_module', 'declarationKind': 'namespace', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'module', 'declarationKind': 'namespace', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'function_signature', 'declarationKind': 'function', 'name': {'field': 'name'}},
    {'kind': 'method_signature', 'declarationKind': 'method', 'name': {'field': 'name'}},
    {'kind': 'abstract_method_signature', 'declarationKind': 'method', 'name': {'field': 'name'}},
    {'kind': 'property_signature', 'declarationKind': 'field', 'name': {'field': 'name'}},
    {'kind': 'public_field_definition', 'declarationKind': 'field', 'name': {'field': 'name'}},
    {'kind': 'required_parameter', 'declarationKind': 'parameter', 'bindings': {'field': 'pattern'}},
    {'kind': 'optional_parameter', 'declarationKind': 'parameter', 'bindings': {'field': 'pattern'}},
]
TS_CONTAINERS = [
    {'kind': 'arrow_function', 'tag': 'lambda'},
    {'kind': 'function_expression', 'tag': 'lambda'},
    {'kind': 'generator_function', 'tag': 'lambda'},
    {'kind': 'class', 'tag': 'type'},
    {'kind': 'class_static_block', 'tag': 'block'},
]
RUST_DECLARES = [
    {'kind': 'function_item', 'declarationKind': 'method', 'name': {'field': 'name'}, 'container': True,
     'when': 'in-impl-or-trait'},
    {'kind': 'function_item', 'declarationKind': 'function', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'function_signature_item', 'declarationKind': 'method', 'name': {'field': 'name'},
     'when': 'in-impl-or-trait'},
    {'kind': 'function_signature_item', 'declarationKind': 'function', 'name': {'field': 'name'}},
    {'kind': 'struct_item', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'enum_item', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'union_item', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'trait_item', 'declarationKind': 'type', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'type_item', 'declarationKind': 'type', 'name': {'field': 'name'}},
    {'kind': 'associated_type', 'declarationKind': 'type', 'name': {'field': 'name'}},
    {'kind': 'mod_item', 'declarationKind': 'module', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'const_item', 'declarationKind': 'variable', 'name': {'field': 'name'}},
    {'kind': 'static_item', 'declarationKind': 'variable', 'name': {'field': 'name'}},
    {'kind': 'field_declaration', 'declarationKind': 'field', 'name': {'field': 'name'}},
    {'kind': 'enum_variant', 'declarationKind': 'field', 'name': {'field': 'name'}, 'container': True},
    {'kind': 'let_declaration', 'declarationKind': 'variable', 'bindings': {'field': 'pattern'}},
    {'kind': 'parameter', 'declarationKind': 'parameter', 'bindings': {'field': 'pattern'}},
    {'kind': 'closure_parameters', 'declarationKind': 'parameter', 'bindings': {}},
    {'kind': 'match_arm', 'declarationKind': 'variable', 'bindings': {'field': 'pattern'}},
    {'kind': 'let_condition', 'declarationKind': 'variable', 'bindings': {'field': 'pattern'}},
    {'kind': 'for_expression', 'declarationKind': 'variable', 'bindings': {'field': 'pattern'}},
]
RUST_CONTAINERS = [
    {'kind': 'closure_expression', 'tag': 'lambda'},
    {'kind': 'impl_item', 'tag': 'impl'},
    {'kind': 'unsafe_block', 'tag': 'block'},
    {'kind': 'async_block', 'tag': 'block'},
    {'kind': 'const_block', 'tag': 'block'},
    {'kind': 'try_block', 'tag': 'block'},
    {'kind': 'gen_block', 'tag': 'block'},
]
WHEN_LAW = {
    'has-field': 'the node has a child in the rule\'s field',
    'binding-kind': ('the for_in_statement has a kind field holding one of the anonymous tokens var, let, const or '
                     'using; without one, its left is an assignment target and declares nothing'),
    'in-impl-or-trait': 'the node\'s parent is a declaration_list whose parent is an impl_item or a trait_item',
}

# Pattern laws (shared by declares bindings and the L3 binding sites).
TS_PATTERN_LAW = {
    'leaves': ['identifier', 'shorthand_property_identifier_pattern'],
    'descend': [
        {'kind': 'object_pattern', 'into': 'named-children'},
        {'kind': 'array_pattern', 'into': 'named-children'},
        {'kind': 'pair_pattern', 'field': 'value'},
        {'kind': 'assignment_pattern', 'field': 'left'},
        {'kind': 'object_assignment_pattern', 'field': 'left'},
        {'kind': 'rest_pattern', 'into': 'named-children'},
    ],
    'law': ('The bindings of a pattern node P: if P is a leaf kind it binds its own text; if P matches a descend rule, '
            'the bindings of each node the rule reaches (its named children, or the node in its field), in order; '
            'any other node binds nothing (a member or subscript target, undefined, this, a default value, a '
            'computed key or a type annotation).'),
}
TS_PARAM_LAW = {
    'javascript': 'A formal_parameters bindings rule takes each named child of formal_parameters as a pattern.',
    'tsx': ('A formal_parameters child is a required_parameter or optional_parameter, whose own rule takes its '
            'pattern field.'),
    'typescript': ('A formal_parameters child is a required_parameter or optional_parameter, whose own rule takes '
                   'its pattern field.'),
}
RUST_PATTERN_LAW = {
    'leaves': ['identifier', 'shorthand_field_identifier'],
    'descend': [
        {'kind': 'mut_pattern', 'into': 'named-children'},
        {'kind': 'ref_pattern', 'into': 'named-children'},
        {'kind': 'reference_pattern', 'into': 'named-children'},
        {'kind': 'captured_pattern', 'into': 'named-children'},
        {'kind': 'tuple_pattern', 'into': 'named-children'},
        {'kind': 'slice_pattern', 'into': 'named-children'},
        {'kind': 'or_pattern', 'into': 'named-children'},
        {'kind': 'tuple_struct_pattern', 'into': 'named-children-except-field', 'field': 'type'},
        {'kind': 'struct_pattern', 'into': 'named-children-except-field', 'field': 'type'},
        {'kind': 'field_pattern', 'into': 'shorthand-or-field', 'field': 'pattern'},
        {'kind': 'match_pattern', 'into': 'named-children-except-field', 'field': 'condition'},
    ],
    'law': ('The bindings of a pattern node P: an identifier binds its text under the case rule; a '
            'shorthand_field_identifier binds its text; a descend rule reaches its named children (except the node '
            'in its field, for -except-field), or, for field_pattern, its shorthand_field_identifier name or else '
            'the node in its pattern field; any other node binds nothing (a path, a literal, a range, _, .., self). '
            'Case rule: an identifier that is the first named child of a captured_pattern, or a direct child of a '
            'mut_pattern or ref_pattern, always binds. A bare identifier binds in an irrefutable position (the '
            'pattern of a parameter, a closure parameter, a for_expression, or a let_declaration without an '
            'alternative field). In a refutable position (a match_arm, a let_condition, a let_declaration with an '
            'alternative) a bare identifier binds only when its first byte is not an ASCII capital letter A to Z; '
            'otherwise it is read as a path to a constant, unit struct or unit variant and binds nothing.'),
    'statedLimit': ('Rust resolves a bare identifier pattern by the items in scope, which a syntax-only reading '
                    'cannot see. A lowercase constant, unit struct or unit variant used as a pattern, and an '
                    'uppercase binding in a refutable position, are misread. Both are against Rust\'s naming lints '
                    '(non_upper_case_globals, non_camel_case_types, non_snake_case).'),
}
RUST_PARAM_LAW = ('A closure_parameters bindings rule takes each named child as a pattern, and a parameter child '
                  'by its own rule\'s pattern field; a self_parameter binds nothing.')

TS_LITERALS = [
    {'kind': 'string', 'literalKind': 'string'},
    {'kind': 'template_string', 'literalKind': 'template'},
    {'kind': 'number', 'literalKind': 'number'},
    {'kind': 'true', 'literalKind': 'boolean'},
    {'kind': 'false', 'literalKind': 'boolean'},
    {'kind': 'null', 'literalKind': 'null'},
    {'kind': 'regex', 'literalKind': 'regex'},
]
RUST_LITERALS = [
    {'kind': 'string_literal', 'literalKind': 'string'},
    {'kind': 'raw_string_literal', 'literalKind': 'string'},
    {'kind': 'char_literal', 'literalKind': 'string'},
    {'kind': 'integer_literal', 'literalKind': 'number'},
    {'kind': 'float_literal', 'literalKind': 'number'},
    {'kind': 'boolean_literal', 'literalKind': 'boolean'},
]

# ------------------------------------------------------------------------------------------------------------
# Control flow (normalizer.v1.json; law M3-E1 item 13)
# ------------------------------------------------------------------------------------------------------------
CONTROL_FLOW_LAW = [
    'Scope. One graph per body whose bodyKind is function, method, lambda or block; an impl body has none. Edges are '
    'intra-body: a nested body is its own graph and is opaque inside the enclosing one. Each edge is one inert '
    'control-flow candidate {from, to, edgeKind}; edges are a set, so a repeated edge is one candidate. Its one anchor '
    'is the from node\'s span, or the body span for entry.',
    'Nodes. entry and exit, and the flow nodes. A flow node is (a) each named child of a statementLists node, except '
    'the row\'s nonStatements kinds, and (b) the node in a singleStatement field of a role, when that node is not a '
    'statementLists node. A statementLists node that is a role\'s field child, or the body itself, is transparent: '
    'its flow nodes stand in its place. A flow node\'s subject is the body owner\'s chain, then a stmt segment for '
    'each enclosing flow node and itself (name the node kind; ordinal among flow nodes of that kind with the same '
    'enclosing flow node); entry and exit are the owner chain plus entry and exit segments.',
    'first(X): for a transparent list, its first flow node, or none when it has none; for a single-statement child, '
    'the child.',
    'next(S): the flow node after S in its list. When S is the last of its list, or a single-statement child, next '
    'is the list owner\'s continuation: exit for the body; next(B) for a block role B, for a branch, consequence or '
    'alternative of B, for a labeled body of B, for a match arm value of B, and for the finalizer of a try B; B '
    'itself, as a loop edge, for the body of a loop B; first of the next switch case with a flow node, else '
    'next(switch), for a switch case body; and first(finalizer) when the try has a finalizer with a flow node, else '
    'next(try), for a try body or a catch body.',
    'An edge to a target that is none goes to the target\'s continuation instead, by the same rules.',
    'Edges. (1) entry to first(body) as fallthrough, or entry to exit when the body has no flow node (an expression '
    'body has none). (2) A simple node S: S to next(S), fallthrough, or loop when next is reached as the end of a loop '
    'body. (3) block: S to first(list), fallthrough. (4) branch: S to first(consequence) as branch-true; S to '
    'first(alternative) as branch-false when there is an alternative, else S to next(S) as branch-false; an else '
    'holding another branch makes that branch the alternative\'s flow node. (5) pretest loop: S to first(body) as '
    'branch-true (S to S as loop when the body has no flow node); S to next(S) as branch-false, except a for_statement '
    'whose condition is absent or empty. (6) posttest loop: S to first(body) as fallthrough; the body\'s end to S as '
    'loop; S to next(S) as branch-false. (7) infinite loop: S to first(body) as fallthrough; the body\'s end to S as '
    'loop; no other exit but break. (8) switch: for each case in order, S to the first flow node of that case or a '
    'later one as branch-true (branch-false for the default case); with no default case, S to next(S) as branch-false. '
    '(9) match: for each arm, S to first(the arm value) as branch-true when the value is a block with a flow node, '
    'else S to next(S) as branch-true. (10) try: S to first(try body) as fallthrough; with a handler, S to first(handler '
    'body) as exception. (11) labeled: S to first(body) as fallthrough. (12) return: S to exit as return. (13) throw: S '
    'to first(handler body) of the innermost enclosing try in this body whose try body contains S and which has a '
    'handler, as throw; else S to exit as throw. (14) break: S to next(T) as fallthrough, where T is the innermost '
    'enclosing loop or switch (a JavaScript-family row) or loop (Rust), or the node carrying the named label. (15) '
    'continue: S to T as loop, where T is the innermost enclosing loop or the loop carrying the named label (for a '
    'labeled_statement, the loop in its body). (16) Rust early return: a flow node S with a try_expression in its own '
    'part (S\'s subtree minus its nested flow nodes and minus nested bodies and nested try_block nodes) also gets S to '
    'exit as return.',
    'Stated simplifications. A finally clause is entered only by normal completion and by the try\'s exception edge; '
    'a return, break, continue or throw that a finally would intercept goes to its stated target. Control flow inside '
    'an expression is not decomposed: an if, match, loop or block that is not a flow node (a let initializer, a call '
    'argument) belongs to its enclosing flow node, and a short-circuit operator, conditional expression, optional '
    'chain, await or yield adds no edge. Unreachable flow nodes keep their outgoing edges.',
]
TS_CONTROL = {
    'statementLists': [{'kind': 'statement_block'}, {'kind': 'switch_case', 'field': 'body'},
                       {'kind': 'switch_default', 'field': 'body'}],
    'nonStatements': ['comment', 'html_comment'],
    'roles': [
        {'kind': 'if_statement', 'role': 'branch', 'consequence': 'consequence', 'alternative': 'alternative',
         'alternativeChild': 'else_clause'},
        {'kind': 'while_statement', 'role': 'pretest-loop', 'body': 'body'},
        {'kind': 'for_statement', 'role': 'pretest-loop', 'body': 'body', 'condition': 'condition'},
        {'kind': 'for_in_statement', 'role': 'pretest-loop', 'body': 'body'},
        {'kind': 'do_statement', 'role': 'posttest-loop', 'body': 'body'},
        {'kind': 'switch_statement', 'role': 'switch', 'body': 'body', 'cases': ['switch_case', 'switch_default'],
         'default': 'switch_default'},
        {'kind': 'try_statement', 'role': 'try', 'body': 'body', 'handler': 'handler', 'finalizer': 'finalizer',
         'handlerBody': 'catch_clause', 'finalizerBody': 'finally_clause'},
        {'kind': 'labeled_statement', 'role': 'labeled', 'body': 'body', 'label': 'label'},
        {'kind': 'with_statement', 'role': 'labeled', 'body': 'body'},
        {'kind': 'return_statement', 'role': 'return'},
        {'kind': 'throw_statement', 'role': 'throw'},
        {'kind': 'break_statement', 'role': 'break', 'label': 'label'},
        {'kind': 'continue_statement', 'role': 'continue', 'label': 'label'},
        {'kind': 'statement_block', 'role': 'block'},
    ],
    'roleLaw': ('Every other flow node is simple. with_statement takes the labeled role (enter its body). The body of '
                'a catch_clause and a finally_clause is its body field. A switch_case or switch_default body is the '
                'list of its body field nodes.'),
}
RUST_CONTROL = {
    'statementLists': [{'kind': 'block'}],
    'nonStatements': ['line_comment', 'block_comment', 'attribute_item', 'inner_attribute_item', 'label'],
    'roles': [
        {'kind': 'if_expression', 'role': 'branch', 'consequence': 'consequence', 'alternative': 'alternative',
         'alternativeChild': 'else_clause'},
        {'kind': 'while_expression', 'role': 'pretest-loop', 'body': 'body'},
        {'kind': 'for_expression', 'role': 'pretest-loop', 'body': 'body'},
        {'kind': 'loop_expression', 'role': 'infinite-loop', 'body': 'body'},
        {'kind': 'match_expression', 'role': 'match', 'body': 'body', 'arms': 'match_arm', 'armValue': 'value'},
        {'kind': 'block', 'role': 'block'},
        {'kind': 'unsafe_block', 'role': 'block', 'child': 'block'},
        {'kind': 'return_expression', 'role': 'return'},
        {'kind': 'break_expression', 'role': 'break', 'labelChild': 'label'},
        {'kind': 'continue_expression', 'role': 'continue', 'labelChild': 'label'},
    ],
    'roleLaw': ('A flow node takes the role of its own kind, or, for an expression_statement, the role of its '
                'expression child. Every other flow node is simple: a let_declaration, an item, a macro_invocation, '
                'an async_block, const_block, try_block or gen_block, and any other expression. The last named child '
                'of a block that is an expression without a semicolon is a flow node like any other; its normal '
                'completion is the block\'s. A loop carries its label in a label child; break and continue name one '
                'in theirs.'),
    'earlyReturn': {'kind': 'try_expression', 'opaque': ['closure_expression', 'async_block', 'const_block',
                                                         'try_block', 'gen_block', 'function_item']},
}

# ------------------------------------------------------------------------------------------------------------
# Level specifications (identity-and-evidence section 3; fact-identity-policy.v2 canonicalisationSchema)
# ------------------------------------------------------------------------------------------------------------
BYTE_GRAMMAR = {
    'inheritedFrom': 'docs/coop/artifacts/fact-identity-policy.v2.json#/canonicalisationSchema/byteGrammar',
    'payload': 'u32be token_count || token*',
    'token': 'u16be kind_id_len || kind_id_bytes || u32be value_len || value_bytes',
    'law': ('This specification fixes the framedTokenStream payload of the inherited byteGrammar for this level: '
            'which tokens, with which kind ids and value bytes, in which order. The frame around the payload '
            '(domain tag, levelId, levelVersion, languageId, languageVersion) is identity-and-evidence section 3\'s, '
            'unchanged. levelVersion is the raw SHA-256 of these exact canonical bytes.'),
}
TOKEN_LAW = [
    'The token stream of a body is computed from the validated tree of a parsed file and the body span [start, end) '
    'that the native normalizer\'s bodies table selects.',
    'Token nodes. Walk the body node\'s subtree in preorder. A node of the row\'s atomicKinds is a token node and is '
    'not entered; any other node with no visible child is a token node. A token node with an empty range is not a '
    'token.',
    'Gaps. The bytes of [start, end) covered by no token node form maximal gap runs. A run made only of the bytes '
    '0x09, 0x0A, 0x0B, 0x0C, 0x0D and 0x20 is dropped: that is the whole of the whitespace and line-ending '
    'normalisation. Any other run is one gap token, with its exact bytes, including any whitespace inside it.',
    'Order and values. Tokens are in ascending order of their start byte. A token node\'s value is its exact source '
    'bytes; there is no Unicode normalisation, no re-encoding and no case change.',
    'Kind ids (the canonical token-kind registry). A token node\'s kind id is "n:" followed by its symbol name when '
    'the symbol is named, and "a:" followed by its symbol name when it is anonymous. A gap token\'s kind id is '
    '"opensip:gap". No numeric symbol id is used.',
]
TS_ATOMIC = ['string', 'regex', 'comment', 'html_comment']
RUST_ATOMIC = ['string_literal', 'raw_string_literal', 'char_literal', 'line_comment', 'block_comment']

L2_LAW = [
    'L2-comment-insensitive is L1-lexical\'s token stream with every comment token that is not a directive removed. A '
    'comment token is a token node of the row\'s commentKinds. Removal deletes the token; no other token changes.',
    'Directive classification. A JavaScript-family comment token is a directive when its value matches one of the '
    'row\'s directivePatterns (ECMAScript regular expressions over the token\'s text, anchored at its start): a '
    'triple-slash directive, a TypeScript @ts- pragma or a JSX pragma. A Rust comment token is a directive (a doc '
    'comment) when it has a child of the row\'s docMarkerKinds; rustc keeps doc comments as attributes. Every other '
    'comment is removed.',
    'Everything native-evidence section 6.3 keeps significant at every level stays: string, template and regex '
    'literal contents, JSX text, \'use strict\' and \'use client\' (which are statements, not comments), decorators, '
    'macro token trees, attributes including #[cfg], lifetimes.',
]
TS_DIRECTIVES = ['^///[ \\t]*<', '^//[ \\t]*@ts-', '^/\\*[\\s*]*@ts-', '^//[ \\t]*@jsx', '^/\\*[\\s*]*@jsx']
RUST_DOC_MARKERS = ['outer_doc_comment_marker', 'inner_doc_comment_marker']

L3_LAW = [
    'L3-identifier-insensitive is L2-comment-insensitive\'s token stream with each occurrence of a renamable local '
    'name replaced. Native-evidence section 6.3 fixes what is renamed: in the JavaScript family, local let, const and '
    'var bindings, parameters, local function names and destructured locals, never properties, imports, exports, '
    'globals or this members; in Rust, local let bindings, parameters, closure parameters and pattern bindings, '
    'never fields, paths, generics, trait names or macro-introduced names.',
    'Occurrences. An occurrence is a token node of the row\'s identifierKinds that is not inside a notOccurrence node. '
    'A binding site is the identifier that a bindingRules rule binds (by the row\'s pattern law), or the name a '
    'nonRenamable rule binds; its scope is the rule\'s.',
    'Boundary. The scopes considered are those whose node lies in the body, plus, for a function, method or lambda '
    'body, the scope of its owning node, which holds its parameters. A barrier kind is never crossed outward: an '
    'occurrence inside it resolves within it or not at all.',
    'Resolution. An occurrence resolves to the binding of its name in the innermost enclosing scope, inside the '
    'boundary, that binds the name. In the JavaScript family a scope binds a name anywhere in it (hoisting and the '
    'temporal dead zone both bind). In Rust a let_declaration binds its names for the following siblings of its '
    'block and their subtrees only, so a later let shadows an earlier one and a let\'s own value, type and '
    'alternative see the earlier binding; every other Rust scope binds throughout its region. An occurrence with no '
    'such binding is free.',
    'Renamable names. A name N is renamable in the body when all hold: (R1) N has a binding site of a bindingRules '
    'rule within the boundary; (R2) N has no binding site of a nonRenamable rule within the boundary; (R3) every '
    'occurrence of N in the body resolves to a bindingRules binding within the boundary; (R4) N has no '
    'disqualifying occurrence and no formatCapture match; and (R5) the body has no bodyDisqualifiers node. Any other '
    'name is kept verbatim at every occurrence.',
    'Replacement. Renamable names are numbered 1, 2, 3 in the order of their first occurrence in the L2 token stream. '
    'Every occurrence token of a renamable name becomes the token with kind id "opensip:local" and value the ASCII '
    'decimal of its number; no other token changes. A replaced token can never equal a source identifier token, '
    'because its kind id differs, so a source name such as $1 cannot collide with a replacement.',
    'Why this is sound. Two bodies with equal L3 streams differ only by a one-to-one renaming of names every '
    'occurrence of which is bound inside the body; free names, properties and kept names are identical. That is '
    'native-evidence\'s identifier-insensitive identity, and no semantic equivalence is claimed.',
]
TS_L3_COMMON_FUNCTION_SCOPES = ['function_declaration', 'generator_function_declaration', 'function_expression',
                                'generator_function', 'arrow_function', 'method_definition', 'class_static_block']
TS_L3_BLOCK_SCOPES = ['statement_block', 'switch_body', 'for_statement', 'for_in_statement', 'catch_clause']


def ts_l3(row):
    bindings = [
        {'kind': 'variable_declaration', 'child': 'variable_declarator', 'field': 'name', 'scope': 'function'},
        {'kind': 'lexical_declaration', 'child': 'variable_declarator', 'field': 'name', 'scope': 'block'},
        {'kind': 'arrow_function', 'field': 'parameter', 'scope': 'function'},
        {'kind': 'catch_clause', 'field': 'parameter', 'scope': 'catch_clause'},
        {'kind': 'for_in_statement', 'field': 'left', 'scope': 'by-kind',
         'anonymous': ['var', 'let', 'const'] + (['using'] if row == 'javascript' else [])},
        {'kind': 'function_declaration', 'field': 'name', 'scope': 'function', 'when': 'direct-in-function-list'},
        {'kind': 'generator_function_declaration', 'field': 'name', 'scope': 'function',
         'when': 'direct-in-function-list'},
    ]
    if row == 'javascript':
        bindings.insert(2, {'kind': 'using_declaration', 'child': 'variable_declarator', 'field': 'name',
                            'scope': 'block'})
        bindings.insert(3, {'kind': 'formal_parameters', 'scope': 'function'})
    else:
        bindings.insert(2, {'kind': 'required_parameter', 'field': 'pattern', 'scope': 'function'})
        bindings.insert(3, {'kind': 'optional_parameter', 'field': 'pattern', 'scope': 'function'})
    non_renamable = [
        {'kind': 'function_declaration', 'field': 'name', 'scope': 'block', 'when': 'not-direct-in-function-list'},
        {'kind': 'generator_function_declaration', 'field': 'name', 'scope': 'block',
         'when': 'not-direct-in-function-list'},
        {'kind': 'function_expression', 'field': 'name', 'scope': 'self'},
        {'kind': 'generator_function', 'field': 'name', 'scope': 'self'},
        {'kind': 'class_declaration', 'field': 'name', 'scope': 'block'},
        {'kind': 'class', 'field': 'name', 'scope': 'self'},
    ]
    if row != 'javascript':
        non_renamable += [
            {'kind': 'abstract_class_declaration', 'field': 'name', 'scope': 'block'},
            {'kind': 'enum_declaration', 'field': 'name', 'scope': 'block'},
            {'kind': 'internal_module', 'field': 'name', 'scope': 'block'},
            {'kind': 'module', 'field': 'name', 'scope': 'block'},
            {'kind': 'function_signature', 'field': 'name', 'scope': 'block'},
            {'kind': 'import_alias', 'scope': 'block', 'firstChild': 'identifier'},
        ]
    disqualifying = [{'kind': 'shorthand_property_identifier'}, {'kind': 'shorthand_property_identifier_pattern'}]
    if row in ('javascript', 'tsx'):
        disqualifying.append({'within': ['jsx_opening_element', 'jsx_closing_element', 'jsx_self_closing_element'],
                              'field': 'name'})
    out = {
        'grammarId': row,
        'identifierKinds': ['identifier'],
        'functionScopes': TS_L3_COMMON_FUNCTION_SCOPES,
        'blockScopes': TS_L3_BLOCK_SCOPES,
        'barriers': [],
        'bindingRules': bindings,
        'nonRenamable': non_renamable,
        'notOccurrences': [],
        'disqualifying': disqualifying,
        'bodyDisqualifiers': [{'kind': 'with_statement'},
                              {'kind': 'call_expression', 'field': 'function', 'identifierText': 'eval'}],
        'patternLaw': TS_PATTERN_LAW,
        'parameterLaw': TS_PARAM_LAW[row],
    }
    return out


SCOPE_LAW_TS = [
    'A function scope is a node of functionScopes; it binds the parameters of its node and every var binding and '
    'every direct-in-function-list function declaration of its region not inside a nested function scope. A block '
    'scope is a node of blockScopes; it binds its let, const and using bindings, its class declarations and its '
    'not-direct-in-function-list function declarations. The body statement_block of a function is part of the '
    'function scope. for_in_statement binds by its kind token: var in the enclosing function scope; let, const or '
    'using in the for_in_statement. A catch_clause binds its parameter. self binds a function or class expression\'s '
    'own name inside that expression only.',
    'direct-in-function-list: the declaration is a direct child of the statement_block that is the body of a '
    'function scope node (or of the body itself). A function declaration nested in any other block is nonRenamable, '
    'because its scope differs between strict and sloppy code.',
    'bodyDisqualifiers: a with_statement, or a call_expression whose function field is the identifier eval (a direct '
    'eval), anywhere in the body, makes every name non-renamable for the body.',
    'disqualifying: a name occurring as a shorthand property or shorthand pattern (where the name is also a property '
    'key), or as an identifier anywhere in the name field of a JSX element, is non-renamable.',
]
SCOPE_LAW_RUST = [
    'Scopes. function_item binds its parameters for its body; closure_expression binds its closure parameters for '
    'its body; block binds its let_declaration bindings sequentially and its item and use names throughout; '
    'match_arm binds its pattern for its guard and value; a let_condition binds for the consequence or body of the '
    'if_expression or while_expression whose condition holds it, and for later members of its let_chain; '
    'for_expression binds its pattern for its body.',
    'barriers: items do not see the locals around them, so an occurrence inside an item resolves inside it or not at '
    'all. Closures and async blocks capture, so they are not barriers.',
    'nonRenamable: item names declared in a block (fn, const, static, struct, enum, union, trait, type, mod, '
    'macro_rules), and the names a use_declaration in a block binds (the last segment, or the alias of a '
    'use_as_clause, of each path it imports), bind in their block but are never renamed.',
    'notOccurrences: an identifier inside a path (scoped_identifier, scoped_type_identifier, scoped_use_list, '
    'use_declaration), a label, a lifetime, an attribute, a visibility_modifier or the macro field of a '
    'macro_invocation never names a local and is kept verbatim.',
    'disqualifying: a name occurring in a macro token_tree or macro_definition (native-evidence section 6.3 keeps '
    'macro token trees verbatim), as a shorthand field pattern or as a shorthand field initializer (where the name is '
    'also the field name) is non-renamable. formatCapture: a name N is non-renamable when a string_literal or '
    'raw_string_literal token inside a token_tree contains "{" N "}" or "{" N ":" (format argument capture).',
    'bodyDisqualifiers: a use_declaration holding a use_wildcard anywhere in the body makes every name non-renamable '
    'for the body, because a glob import binds names this reading cannot see.',
    'Stated limit: a statement-position macro invocation that defines an item whose name does not occur in its own '
    'token tree is not seen.',
]
RUST_L3 = {
    'grammarId': 'rust',
    'identifierKinds': ['identifier'],
    'functionScopes': ['function_item', 'closure_expression'],
    'blockScopes': ['block', 'match_arm', 'if_expression', 'while_expression', 'for_expression'],
    'barriers': ['function_item', 'const_item', 'static_item', 'impl_item', 'trait_item', 'mod_item', 'struct_item',
                 'enum_item', 'union_item', 'type_item', 'macro_definition', 'foreign_mod_item'],
    'bindingRules': [
        {'kind': 'parameter', 'field': 'pattern', 'scope': 'function', 'position': 'irrefutable'},
        {'kind': 'closure_parameters', 'scope': 'function', 'position': 'irrefutable'},
        {'kind': 'let_declaration', 'field': 'pattern', 'scope': 'sequential', 'position': 'by-alternative',
         'alternativeField': 'alternative'},
        {'kind': 'match_arm', 'field': 'pattern', 'scope': 'match_arm', 'position': 'refutable'},
        {'kind': 'let_condition', 'field': 'pattern', 'scope': 'condition-holder', 'position': 'refutable'},
        {'kind': 'for_expression', 'field': 'pattern', 'scope': 'for_expression', 'position': 'irrefutable'},
    ],
    'nonRenamable': [
        {'kind': 'function_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'const_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'static_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'struct_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'enum_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'union_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'trait_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'type_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'mod_item', 'field': 'name', 'scope': 'block'},
        {'kind': 'macro_definition', 'field': 'name', 'scope': 'block'},
        {'kind': 'use_declaration', 'field': 'argument', 'scope': 'block', 'names': 'imported'},
    ],
    'notOccurrences': [{'within': ['scoped_identifier', 'scoped_type_identifier', 'scoped_use_list',
                                   'use_declaration', 'label', 'lifetime', 'attribute_item', 'inner_attribute_item',
                                   'visibility_modifier']},
                       {'within': ['macro_invocation'], 'field': 'macro'}],
    'disqualifying': [{'within': ['token_tree', 'macro_definition']}, {'kind': 'shorthand_field_identifier'},
                      {'within': ['shorthand_field_initializer']}],
    'formatCapture': {'kinds': ['string_literal', 'raw_string_literal'], 'within': ['token_tree']},
    'bodyDisqualifiers': [{'kind': 'use_declaration', 'descendant': 'use_wildcard'}],
    'patternLaw': RUST_PATTERN_LAW,
    'parameterLaw': RUST_PARAM_LAW,
}


def row_tokens(row):
    atomic = RUST_ATOMIC if row == 'rust' else TS_ATOMIC
    return {'grammarId': row, 'atomicKinds': atomic}


def row_comments(row):
    if row == 'rust':
        return {'grammarId': row, 'atomicKinds': RUST_ATOMIC, 'commentKinds': ['line_comment', 'block_comment'],
                'docMarkerKinds': RUST_DOC_MARKERS}
    return {'grammarId': row, 'atomicKinds': TS_ATOMIC, 'commentKinds': ['comment', 'html_comment'],
            'directivePatterns': TS_DIRECTIVES}


def level_doc(level):
    doc = {
        'schemaVersion': 1,
        'artifact': 'opensip.syntax.level-specification',
        'normalizerId': NORMALIZER_ID,
        'level': level,
        'standing': ('The canonical level specification of the syntax universe\'s normalizer for ' + level + ': the '
                     'exact retained bytes identity-and-evidence section 3 names through the grammar closure\'s '
                     'normalization map (opensip-interface/normalization/specification-map.v1.json). Contract '
                     'successor SYN-NS of law M3-E1 (items 13 and 14). It is complete for its level: it depends on no '
                     'other level\'s bytes.'),
        'conventions': CONVENTIONS,
    }
    if level == 'L0-verbatim':
        doc.update({
            'payload': 'u32be raw_byte_len || the exact body-span bytes',
            'tokenisation': 'forbidden',
            'law': ['The payload is the body span\'s exact snapshot bytes [start, end), length-prefixed, as '
                    'identity-and-evidence section 3 fixes for L0-verbatim (the payload is length-prefixed inside the '
                    'frame\'s own length). No byte is changed, removed or tokenised.',
                    'The span is the one the native normalizer\'s bodies table selects; this level adds nothing to it.'],
            'inheritedFrom': 'docs/coop/artifacts/fact-identity-policy.v2.json#/canonicalisationSchema/byteGrammar',
            'rows': [{'grammarId': r} for r in CODE_ROWS],
        })
        return doc
    doc['byteGrammar'] = BYTE_GRAMMAR
    doc['tokenLaw'] = TOKEN_LAW
    if level == 'L1-lexical':
        doc['transformOrder'] = ['tokens']
        doc['rows'] = [row_tokens(r) for r in CODE_ROWS]
    elif level == 'L2-comment-insensitive':
        doc['transformOrder'] = ['tokens', 'remove-non-directive-comments']
        doc['commentLaw'] = L2_LAW
        doc['rows'] = [row_comments(r) for r in CODE_ROWS]
    else:
        doc['transformOrder'] = ['tokens', 'remove-non-directive-comments', 'rename-locals']
        doc['commentLaw'] = L2_LAW
        doc['renameLaw'] = L3_LAW
        doc['scopeLaw'] = {'javascript-family': SCOPE_LAW_TS, 'rust': SCOPE_LAW_RUST}
        rows = []
        for r in CODE_ROWS:
            base = row_comments(r)
            base.update(RUST_L3 if r == 'rust' else ts_l3(r))
            rows.append(base)
        doc['rows'] = rows
    return doc


def normalizer_doc():
    rows = []
    for r in CODE_ROWS:
        if r == 'rust':
            rows.append({'grammarId': r, 'bodies': RUST_BODIES, 'statementContainers': STATEMENT_CONTAINERS[r],
                         'importOnly': IMPORT_ONLY[r], 'declares': RUST_DECLARES, 'containers': RUST_CONTAINERS,
                         'patternLaw': RUST_PATTERN_LAW, 'parameterLaw': RUST_PARAM_LAW,
                         'literals': RUST_LITERALS, 'controlFlow': RUST_CONTROL})
        else:
            rows.append({'grammarId': r, 'bodies': TS_BODIES, 'statementContainers': STATEMENT_CONTAINERS[r],
                         'importOnly': IMPORT_ONLY[r],
                         'declares': JS_DECLARES if r == 'javascript' else TS_DECLARES,
                         'containers': TS_CONTAINERS, 'patternLaw': TS_PATTERN_LAW,
                         'parameterLaw': TS_PARAM_LAW[r], 'literals': TS_LITERALS, 'controlFlow': TS_CONTROL})
    return {
        'schemaVersion': 1,
        'artifact': 'opensip.syntax.normalizer-specification',
        'normalizerId': NORMALIZER_ID,
        'normalizerVersion': NORMALIZER_VERSION,
        'standing': ('The native normalizer specification of the syntax universe (the grammar bundle\'s '
                     'normalizer.specificationDigest member, native-evidence section 1.2): which spans are bodies, '
                     'how syntax subjects are named, which nodes declare, which tokens are literals, the intra-body '
                     'control-flow edges and near-v1. Contract successor SYN-NS of law M3-E1 (items 13 and 14). It '
                     'does not select any level\'s specification: identity-and-evidence section 3\'s normalization '
                     'map does, and each level specification is complete for its level.'),
        'conventions': CONVENTIONS,
        'parameters': PARAMETERS,
        'bodies': {'law': BODIES_LAW},
        'subjects': {'law': SUBJECTS_LAW},
        'declares': {'law': DECLARES_LAW, 'when': WHEN_LAW},
        'literals': {'law': LITERALS_LAW},
        'controlFlow': {'law': CONTROL_FLOW_LAW},
        'near': NEAR,
        'rows': rows,
    }

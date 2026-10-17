//! M3-D r5 item 9 (unit D2a): the common control codec, CC v5 exactly.
//!
//! One received frame is decided by [`classify`] against an explicit
//! [`ControlContext`], as CC v5's retained reference decides it
//! (`control-completion.check.v5.py`): the 4-byte big-endian framing, a
//! bounded iterative JSON reader that keeps long integer lexemes, the
//! product schema `control-v3.schema.json` evaluated by a closed interpreter,
//! the UTF-8 byte bounds, RF precedence with its two repairs, the eight
//! states, and the identity, tuple, nonce and effect correlations. The two
//! directions' sequences and stopping are [`ControlSession`]'s. The host's own
//! frames are written by [`encode`]. Nothing here spawns, reads a descriptor
//! or translates a provider frame (item 11); serde never reads wire bytes.
use opensip_contracts::generated::evidence::FieldPresence;
/// The validated message type: the product schema's generated root.
pub use opensip_contracts::generated::protocol::Control3Root;
use opensip_contracts::generated::protocol::*;
use std::collections::BTreeSet;
use std::num::NonZeroU64;

/// The largest control integer (2^53 - 1).
const MAX_INTEGER: i64 = 9_007_199_254_740_991;
/// Item 9's host offer and session bound (lead decision).
pub const HOST_FRAME_BOUND: u32 = 65_536;
/// The product schema, embedded: the interpreter's only schema.
const SCHEMA: &str = include_str!("../../../schemas/sources/control-v3.schema.json");

// ------------------------------------------------------------------ the reader

/// A decoded JSON string: valid Unicode text, or UTF-16 code units holding
/// an unpaired surrogate escape, kept so the reference's later UTF-8 walk
/// decides it (LD-D2A-2).
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum JStr {
    Text(String),
    Units(Vec<u16>),
}
impl JStr {
    fn text(&self) -> Option<&str> {
        match self {
            Self::Text(t) => Some(t),
            Self::Units(_) => None,
        }
    }
    /// Code points, as the reference's `len(str)` counts them (an unpaired
    /// surrogate counts one).
    fn code_points(&self) -> usize {
        match self {
            Self::Text(t) => t.chars().count(),
            Self::Units(u) => char::decode_utf16(u.iter().copied()).count(),
        }
    }
}

/// One value of the reader's flat arena. Containers hold child indices, so
/// nothing about the tree recurses: building, dropping and comparing it are
/// all iterative.
#[derive(Debug, Clone)]
pub(crate) enum Node {
    Null,
    Bool(bool),
    /// An integer lexeme of at most sixteen digits.
    Int(i64),
    /// A longer integer lexeme, never converted (CC:189-191).
    Large {
        negative: bool,
    },
    /// A numeric token with a fraction or exponent.
    Float,
    Str(JStr),
    Array(Vec<usize>),
    Object(Vec<(JStr, usize)>),
}

/// A parsed document: the arena and its root.
#[derive(Debug, Clone)]
pub(crate) struct Doc {
    pub(crate) nodes: Vec<Node>,
    pub(crate) root: usize,
}

enum Phase {
    FirstKey,
    Key,
    Colon,
    Value,
    FirstValue,
    Separator,
}
struct Open {
    node: usize,
    object: bool,
    phase: Phase,
    key: Option<JStr>,
    keys: BTreeSet<JStr>,
}

/// The reference's `iterative_json`: RFC 8259 syntax with an explicit
/// container stack, strict strings, decoded-key duplicate refusal and exact
/// integer tokens. `Err(())` is RF2.
pub(crate) fn read_json(text: &str) -> Result<Doc, ()> {
    let b = text.as_bytes();
    let mut i = 0usize;
    let mut nodes: Vec<Node> = Vec::new();
    let mut stack: Vec<Open> = Vec::new();
    let mut root: Option<usize> = None;
    // Attach a finished value to its parent, or make it the root.
    fn put(
        nodes: &mut [Node],
        stack: &mut [Open],
        root: &mut Option<usize>,
        id: usize,
    ) -> Result<(), ()> {
        let Some(top) = stack.last_mut() else {
            if root.is_some() {
                return Err(());
            }
            *root = Some(id);
            return Ok(());
        };
        match &mut nodes[top.node] {
            Node::Object(members) => members.push((top.key.take().ok_or(())?, id)),
            Node::Array(items) => items.push(id),
            _ => return Err(()),
        }
        top.phase = Phase::Separator;
        Ok(())
    }
    loop {
        while i < b.len() && matches!(b[i], b' ' | b'\t' | b'\r' | b'\n') {
            i += 1;
        }
        if i == b.len() {
            if !stack.is_empty() {
                return Err(());
            }
            return root.map(|root| Doc { nodes, root }).ok_or(());
        }
        if stack.is_empty() && root.is_some() {
            return Err(());
        }
        let ch = b[i];
        if let Some(top) = stack.last_mut() {
            match top.phase {
                Phase::Separator => {
                    if ch == b',' {
                        top.phase = if top.object { Phase::Key } else { Phase::Value };
                        i += 1;
                        continue;
                    }
                    if ch == if top.object { b'}' } else { b']' } {
                        stack.pop();
                        i += 1;
                        continue;
                    }
                    return Err(());
                }
                Phase::FirstKey | Phase::Key => {
                    if matches!(top.phase, Phase::FirstKey) && ch == b'}' {
                        stack.pop();
                        i += 1;
                        continue;
                    }
                    if ch != b'"' {
                        return Err(());
                    }
                    let (key, next) = scan_string(text, i + 1)?;
                    if !top.keys.insert(key.clone()) {
                        return Err(());
                    }
                    top.key = Some(key);
                    top.phase = Phase::Colon;
                    i = next;
                    continue;
                }
                Phase::Colon => {
                    if ch != b':' {
                        return Err(());
                    }
                    top.phase = Phase::Value;
                    i += 1;
                    continue;
                }
                Phase::FirstValue if ch == b']' => {
                    stack.pop();
                    i += 1;
                    continue;
                }
                Phase::FirstValue | Phase::Value => {}
            }
        }
        match ch {
            b'{' | b'[' => {
                let object = ch == b'{';
                let id = nodes.len();
                nodes.push(if object {
                    Node::Object(Vec::new())
                } else {
                    Node::Array(Vec::new())
                });
                put(&mut nodes, &mut stack, &mut root, id)?;
                stack.push(Open {
                    node: id,
                    object,
                    phase: if object {
                        Phase::FirstKey
                    } else {
                        Phase::FirstValue
                    },
                    key: None,
                    keys: BTreeSet::new(),
                });
                i += 1;
            }
            b'"' => {
                let (value, next) = scan_string(text, i + 1)?;
                let id = nodes.len();
                nodes.push(Node::Str(value));
                put(&mut nodes, &mut stack, &mut root, id)?;
                i = next;
            }
            _ => {
                let (value, next) = if b[i..].starts_with(b"true") {
                    (Node::Bool(true), i + 4)
                } else if b[i..].starts_with(b"false") {
                    (Node::Bool(false), i + 5)
                } else if b[i..].starts_with(b"null") {
                    (Node::Null, i + 4)
                } else {
                    scan_number(b, i)?
                };
                let id = nodes.len();
                nodes.push(value);
                put(&mut nodes, &mut stack, &mut root, id)?;
                i = next;
            }
        }
    }
}

/// `json.decoder.scanstring(text, start, strict=True)`: from just after the
/// opening quote to just after the closing one.
fn scan_string(text: &str, start: usize) -> Result<(JStr, usize), ()> {
    let mut units: Vec<u16> = Vec::new();
    let mut chars = text[start..].char_indices();
    while let Some((offset, c)) = chars.next() {
        match c {
            '"' => {
                let end = start + offset + 1;
                return Ok((
                    match String::from_utf16(&units) {
                        Ok(s) => JStr::Text(s),
                        Err(_) => JStr::Units(units),
                    },
                    end,
                ));
            }
            '\\' => {
                let (_, e) = chars.next().ok_or(())?;
                let unit = match e {
                    '"' => 0x22,
                    '\\' => 0x5c,
                    '/' => 0x2f,
                    'b' => 0x08,
                    'f' => 0x0c,
                    'n' => 0x0a,
                    'r' => 0x0d,
                    't' => 0x09,
                    'u' => {
                        let mut v: u16 = 0;
                        for _ in 0..4 {
                            let (_, h) = chars.next().ok_or(())?;
                            v = v * 16 + h.to_digit(16).ok_or(())? as u16;
                        }
                        v
                    }
                    _ => return Err(()),
                };
                units.push(unit);
            }
            c if (c as u32) < 0x20 => return Err(()),
            c => {
                let mut buf = [0u16; 2];
                units.extend_from_slice(c.encode_utf16(&mut buf));
            }
        }
    }
    Err(())
}

/// The reference's number token, `-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?`,
/// matched greedily at `i`: a fraction or exponent makes a non-integer, more
/// than sixteen digits a kept lexeme, anything else an integer.
fn scan_number(b: &[u8], start: usize) -> Result<(Node, usize), ()> {
    let mut i = start;
    let negative = b.get(i) == Some(&b'-');
    if negative {
        i += 1;
    }
    let digits_start = i;
    match b.get(i) {
        Some(b'0') => i += 1,
        Some(b'1'..=b'9') => {
            while matches!(b.get(i), Some(b'0'..=b'9')) {
                i += 1;
            }
        }
        _ => return Err(()),
    }
    let digits_end = i;
    let mut non_integer = false;
    if b.get(i) == Some(&b'.') && matches!(b.get(i + 1), Some(b'0'..=b'9')) {
        i += 1;
        while matches!(b.get(i), Some(b'0'..=b'9')) {
            i += 1;
        }
        non_integer = true;
    }
    if matches!(b.get(i), Some(b'e' | b'E')) {
        let mut j = i + 1;
        if matches!(b.get(j), Some(b'+' | b'-')) {
            j += 1;
        }
        if matches!(b.get(j), Some(b'0'..=b'9')) {
            while matches!(b.get(j), Some(b'0'..=b'9')) {
                j += 1;
            }
            i = j;
            non_integer = true;
        }
    }
    if non_integer {
        return Ok((Node::Float, i));
    }
    let digits = &b[digits_start..digits_end];
    if digits.len() > 16 {
        return Ok((Node::Large { negative }, i));
    }
    let mut value: i64 = 0;
    for d in digits {
        value = value * 10 + (d - b'0') as i64;
    }
    Ok((Node::Int(if negative { -value } else { value }), i))
}

// ------------------------------------------------------------------ values

impl Doc {
    fn object(&self, id: usize) -> Option<&[(JStr, usize)]> {
        match &self.nodes[id] {
            Node::Object(m) => Some(m),
            _ => None,
        }
    }
    fn member(&self, id: usize, key: &str) -> Option<usize> {
        self.object(id)?
            .iter()
            .find(|(k, _)| k.text() == Some(key))
            .map(|(_, v)| *v)
    }
    fn text(&self, id: usize) -> Option<&str> {
        match &self.nodes[id] {
            Node::Str(s) => s.text(),
            _ => None,
        }
    }
    fn int(&self, id: usize) -> Option<i64> {
        match self.nodes[id] {
            Node::Int(v) => Some(v),
            _ => None,
        }
    }
    fn str_of(&self, id: usize, key: &str) -> Option<&str> {
        self.member(id, key).and_then(|v| self.text(v))
    }
    fn int_of(&self, id: usize, key: &str) -> Option<i64> {
        self.member(id, key).and_then(|v| self.int(v))
    }
}

/// Structural equality of two values (the reference's `==` after its integer
/// walk): objects unordered, booleans distinct from integers. Iterative.
fn equal(a: &Doc, x: usize, b: &Doc, y: usize) -> bool {
    let mut pending = vec![(x, y)];
    while let Some((x, y)) = pending.pop() {
        match (&a.nodes[x], &b.nodes[y]) {
            (Node::Null, Node::Null) => {}
            (Node::Bool(p), Node::Bool(q)) if p == q => {}
            (Node::Int(p), Node::Int(q)) if p == q => {}
            (Node::Str(p), Node::Str(q)) if p == q => {}
            (Node::Array(p), Node::Array(q)) if p.len() == q.len() => {
                pending.extend(p.iter().copied().zip(q.iter().copied()));
            }
            (Node::Object(p), Node::Object(q)) if p.len() == q.len() => {
                for (k, v) in p {
                    match q.iter().find(|(l, _)| l == k) {
                        Some((_, w)) => pending.push((*v, *w)),
                        None => return false,
                    }
                }
            }
            _ => return false,
        }
    }
    true
}

// ------------------------------------------------------------------ the schema interpreter

/// The keywords the closed interpreter evaluates; any other refuses the
/// schema at load (LD-D2A-3).
const KEYWORDS: &[&str] = &[
    "type",
    "const",
    "enum",
    "properties",
    "required",
    "additionalProperties",
    "minLength",
    "maxLength",
    "minimum",
    "maximum",
    "items",
    "minItems",
    "maxItems",
    "uniqueItems",
    "allOf",
    "if",
    "then",
    "else",
    "not",
    "pattern",
    "x-maxUtf8Bytes",
];
/// The schema's two patterns, each matched exactly (anchored at both ends).
const UUID_PATTERN: &str =
    "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![\\s\\S])";
const DIGEST_PATTERN: &str = "^[0-9a-f]{64}(?![\\s\\S])";

/// The loaded product schema: its arena and each message's `oneOf` member.
pub struct Schema {
    doc: Doc,
    members: Vec<(String, usize)>,
}
/// Why the embedded schema cannot be interpreted.
#[derive(Debug, PartialEq, Eq)]
pub enum SchemaRefusal {
    Unparsed,
    Shape(&'static str),
    UnknownKeyword(String),
    UnknownPattern(String),
}

impl Schema {
    /// Load and check `text`: every subschema uses only the interpreted
    /// keywords and the two known patterns.
    pub fn load(text: &str) -> Result<Self, SchemaRefusal> {
        let doc = read_json(text).map_err(|_| SchemaRefusal::Unparsed)?;
        // The document root is closed too (r2, Codex D2A-R1-NBO-1): its
        // inert metadata and `oneOf`, nothing else.
        let root = doc.object(doc.root).ok_or(SchemaRefusal::Shape("root"))?;
        for (key, _) in root {
            let key = key.text().unwrap_or("");
            if !matches!(key, "$schema" | "$id" | "title" | "oneOf") {
                return Err(SchemaRefusal::UnknownKeyword(key.to_owned()));
            }
        }
        let one_of = doc
            .member(doc.root, "oneOf")
            .ok_or(SchemaRefusal::Shape("oneOf"))?;
        let Node::Array(items) = &doc.nodes[one_of] else {
            return Err(SchemaRefusal::Shape("oneOf"));
        };
        let mut members = Vec::new();
        for &member in items {
            let ty = doc
                .member(member, "properties")
                .and_then(|p| doc.member(p, "type"))
                .and_then(|t| doc.str_of(t, "const"))
                .ok_or(SchemaRefusal::Shape("type const"))?;
            members.push((ty.to_owned(), member));
            check_subschema(&doc, member)?;
        }
        if members.len() != 16 {
            return Err(SchemaRefusal::Shape("sixteen messages"));
        }
        Ok(Self { doc, members })
    }
    fn member_for(&self, ty: &str) -> Option<usize> {
        self.members.iter().find(|(t, _)| t == ty).map(|(_, m)| *m)
    }
    /// The message types the schema defines, in its `oneOf` order.
    pub fn message_types(&self) -> impl Iterator<Item = &str> {
        self.members.iter().map(|(t, _)| t.as_str())
    }
}

/// Every keyword under `id` is interpreted, and every pattern known.
fn check_subschema(doc: &Doc, id: usize) -> Result<(), SchemaRefusal> {
    let mut pending = vec![id];
    while let Some(id) = pending.pop() {
        let Some(members) = doc.object(id) else {
            return Err(SchemaRefusal::Shape("subschema"));
        };
        for (key, value) in members {
            let key = key.text().unwrap_or("");
            if !KEYWORDS.contains(&key) {
                return Err(SchemaRefusal::UnknownKeyword(key.to_owned()));
            }
            match key {
                "properties" => {
                    for (_, sub) in doc
                        .object(*value)
                        .ok_or(SchemaRefusal::Shape("properties"))?
                    {
                        pending.push(*sub);
                    }
                }
                "items" | "if" | "then" | "else" | "not" => pending.push(*value),
                "allOf" => match &doc.nodes[*value] {
                    Node::Array(subs) => pending.extend(subs.iter().copied()),
                    _ => return Err(SchemaRefusal::Shape("allOf")),
                },
                "additionalProperties" if !matches!(doc.nodes[*value], Node::Bool(false)) => {
                    return Err(SchemaRefusal::Shape("additionalProperties"));
                }
                "pattern" => {
                    let p = doc.text(*value).unwrap_or("");
                    if p != UUID_PATTERN && p != DIGEST_PATTERN {
                        return Err(SchemaRefusal::UnknownPattern(p.to_owned()));
                    }
                }
                _ => {}
            }
        }
    }
    Ok(())
}

fn hex_run(s: &[u8]) -> bool {
    s.iter().all(|c| matches!(c, b'0'..=b'9' | b'a'..=b'f'))
}
fn matches_pattern(pattern: &str, value: &str) -> bool {
    let b = value.as_bytes();
    if pattern == DIGEST_PATTERN {
        return b.len() == 64 && hex_run(b);
    }
    b.len() == 36
        && [8, 13, 18, 23].iter().all(|&i| b[i] == b'-')
        && hex_run(&b[..8])
        && hex_run(&b[9..13])
        && hex_run(&b[14..18])
        && hex_run(&b[19..23])
        && hex_run(&b[24..])
}

/// Draft 2020-12 validity of instance `x` of `inst` against subschema `s`,
/// for the interpreted keywords. Recursion follows the schema, which is
/// shallow; instance depth is reached only through `equal`, which iterates.
fn valid(schema: &Doc, s: usize, inst: &Doc, x: usize) -> bool {
    let Some(keywords) = schema.object(s) else {
        return false;
    };
    let node = &inst.nodes[x];
    for (key, value) in keywords {
        let ok = match key.text().unwrap_or("") {
            "type" => match schema.text(*value) {
                Some("object") => matches!(node, Node::Object(_)),
                Some("array") => matches!(node, Node::Array(_)),
                Some("string") => matches!(node, Node::Str(_)),
                Some("integer") => matches!(node, Node::Int(_)),
                Some("boolean") => matches!(node, Node::Bool(_)),
                Some("null") => matches!(node, Node::Null),
                _ => false,
            },
            "const" => equal(inst, x, schema, *value),
            "enum" => match &schema.nodes[*value] {
                Node::Array(options) => options.iter().any(|o| equal(inst, x, schema, *o)),
                _ => false,
            },
            "properties" => match node {
                Node::Object(members) => members.iter().all(|(k, v)| {
                    match k.text().and_then(|k| schema.member(*value, k)) {
                        Some(sub) => valid(schema, sub, inst, *v),
                        None => true,
                    }
                }),
                _ => true,
            },
            "additionalProperties" => match node {
                Node::Object(members) => {
                    let props = schema.member(s, "properties");
                    members.iter().all(|(k, _)| {
                        k.text()
                            .zip(props)
                            .is_some_and(|(k, p)| schema.member(p, k).is_some())
                    })
                }
                _ => true,
            },
            "required" => match (node, &schema.nodes[*value]) {
                (Node::Object(_), Node::Array(names)) => names
                    .iter()
                    .all(|n| schema.text(*n).is_some_and(|n| inst.member(x, n).is_some())),
                _ => true,
            },
            "minLength" | "maxLength" => match node {
                Node::Str(text) => {
                    let n = text.code_points() as i64;
                    let bound = schema.int(*value).unwrap_or(0);
                    if key.text() == Some("minLength") {
                        n >= bound
                    } else {
                        n <= bound
                    }
                }
                _ => true,
            },
            "minimum" | "maximum" => match node {
                Node::Int(n) => {
                    let bound = schema.int(*value).unwrap_or(0);
                    if key.text() == Some("minimum") {
                        *n >= bound
                    } else {
                        *n <= bound
                    }
                }
                _ => true,
            },
            "items" => match node {
                Node::Array(items) => items.iter().all(|i| valid(schema, *value, inst, *i)),
                _ => true,
            },
            "minItems" | "maxItems" => match node {
                Node::Array(items) => {
                    let n = items.len() as i64;
                    let bound = schema.int(*value).unwrap_or(0);
                    if key.text() == Some("minItems") {
                        n >= bound
                    } else {
                        n <= bound
                    }
                }
                _ => true,
            },
            "uniqueItems" => match (node, &schema.nodes[*value]) {
                (Node::Array(items), Node::Bool(true)) => items
                    .iter()
                    .enumerate()
                    .all(|(i, a)| items[i + 1..].iter().all(|b| !equal(inst, *a, inst, *b))),
                _ => true,
            },
            "allOf" => match &schema.nodes[*value] {
                Node::Array(subs) => subs.iter().all(|sub| valid(schema, *sub, inst, x)),
                _ => false,
            },
            "if" => {
                if valid(schema, *value, inst, x) {
                    schema
                        .member(s, "then")
                        .is_none_or(|then| valid(schema, then, inst, x))
                } else {
                    schema
                        .member(s, "else")
                        .is_none_or(|other| valid(schema, other, inst, x))
                }
            }
            "then" | "else" | "x-maxUtf8Bytes" => true,
            "not" => !valid(schema, *value, inst, x),
            "pattern" => match node {
                Node::Str(text) => text
                    .text()
                    .zip(schema.text(*value))
                    .is_some_and(|(t, p)| matches_pattern(p, t)),
                _ => true,
            },
            _ => false,
        };
        if !ok {
            return false;
        }
    }
    true
}

/// The reference's `utf8_bounds`: every string's UTF-8 length within its
/// schema position's `x-maxUtf8Bytes` (1,024 by default); an unpaired
/// surrogate cannot be encoded. Walks the frame `x` as received, with only a
/// faulty seq replaced, along the schema.
fn utf8_bounds(schema: &Doc, s: Option<usize>, inst: &Doc, x: usize) -> bool {
    let mut pending = vec![(s, x)];
    while let Some((s, x)) = pending.pop() {
        match &inst.nodes[x] {
            Node::Str(JStr::Units(_)) => return false,
            Node::Str(JStr::Text(t)) => {
                let limit = s
                    .and_then(|s| schema.int_of(s, "x-maxUtf8Bytes"))
                    .unwrap_or(1024);
                if t.len() as i64 > limit {
                    return false;
                }
            }
            Node::Object(members) => {
                let props = s.and_then(|s| schema.member(s, "properties"));
                for (k, v) in members {
                    let sub = props.and_then(|p| k.text().and_then(|k| schema.member(p, k)));
                    pending.push((sub, *v));
                }
            }
            Node::Array(items) => {
                let sub = s.and_then(|s| schema.member(s, "items"));
                pending.extend(items.iter().map(|i| (sub, *i)));
            }
            _ => {}
        }
    }
    true
}

// ------------------------------------------------------------------ states, context and verdicts

/// CC's eight states (CC:126-135).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ControlState {
    AwaitHello,
    AwaitHelloAck,
    AwaitSelect,
    AwaitSelectAck,
    Steady,
    Teardown,
    Closed,
    Faulted,
}
impl ControlState {
    pub const ALL: [ControlState; 8] = [
        Self::AwaitHello,
        Self::AwaitHelloAck,
        Self::AwaitSelect,
        Self::AwaitSelectAck,
        Self::Steady,
        Self::Teardown,
        Self::Closed,
        Self::Faulted,
    ];
    pub fn as_str(self) -> &'static str {
        match self {
            Self::AwaitHello => "AWAIT-HELLO",
            Self::AwaitHelloAck => "AWAIT-HELLO-ACK",
            Self::AwaitSelect => "AWAIT-SELECT",
            Self::AwaitSelectAck => "AWAIT-SELECT-ACK",
            Self::Steady => "STEADY",
            Self::Teardown => "TEARDOWN",
            Self::Closed => "CLOSED",
            Self::Faulted => "FAULTED",
        }
    }
    pub fn parse(text: &str) -> Option<Self> {
        Self::ALL.into_iter().find(|s| s.as_str() == text)
    }
    /// The message types this state may receive (`LAWFUL`).
    fn lawful(self, ty: &str) -> bool {
        match self {
            Self::AwaitHello => matches!(ty, "hello" | "refusal"),
            Self::AwaitHelloAck => matches!(ty, "helloAck" | "refusal"),
            Self::AwaitSelect => matches!(ty, "select" | "shutdown" | "refusal"),
            Self::AwaitSelectAck => matches!(ty, "selectAck" | "refusal"),
            Self::Steady => matches!(
                ty,
                "ping"
                    | "pong"
                    | "health"
                    | "healthReport"
                    | "resourceReport"
                    | "fault"
                    | "cancel"
                    | "shutdown"
                    | "effectRequest"
                    | "effectResult"
                    | "refusal"
            ),
            Self::Teardown => matches!(ty, "shutdownAck" | "refusal"),
            Self::Closed => false,
            Self::Faulted => ty == "refusal",
        }
    }
    /// The state after accepting `ty` here (`NEXT`).
    fn after(self, ty: &str) -> Self {
        match ty {
            "hello" => Self::AwaitHelloAck,
            "helloAck" => Self::AwaitSelect,
            "select" => Self::AwaitSelectAck,
            "selectAck" => Self::Steady,
            "shutdown" | "cancel" => Self::Teardown,
            "shutdownAck" => Self::Closed,
            "fault" | "refusal" => Self::Faulted,
            _ => self,
        }
    }
}

/// A receive direction.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Direction {
    HostToComponent,
    ComponentToHost,
}
impl Direction {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::HostToComponent => "host-to-component",
            Self::ComponentToHost => "component-to-host",
        }
    }
    pub fn parse(text: &str) -> Option<Self> {
        [Self::HostToComponent, Self::ComponentToHost]
            .into_iter()
            .find(|d| d.as_str() == text)
    }
    /// The types this direction carries (`H2C`, `C2H`).
    fn carries(self, ty: &str) -> bool {
        match self {
            Self::HostToComponent => matches!(
                ty,
                "hello"
                    | "select"
                    | "ping"
                    | "health"
                    | "cancel"
                    | "shutdown"
                    | "effectResult"
                    | "refusal"
            ),
            Self::ComponentToHost => matches!(
                ty,
                "helloAck"
                    | "selectAck"
                    | "pong"
                    | "healthReport"
                    | "resourceReport"
                    | "fault"
                    | "shutdownAck"
                    | "effectRequest"
                    | "refusal"
            ),
        }
    }
}

/// CC's refusal families (CC:104-117).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RefusalFamily {
    Rf1,
    Rf2,
    Rf3,
    Rf4,
    Rf5,
    Rf6,
    Rf7,
    Rf8,
}
impl RefusalFamily {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Rf1 => "RF-1",
            Self::Rf2 => "RF-2",
            Self::Rf3 => "RF-3",
            Self::Rf4 => "RF-4",
            Self::Rf5 => "RF-5",
            Self::Rf6 => "RF-6",
            Self::Rf7 => "RF-7",
            Self::Rf8 => "RF-8",
        }
    }
}

/// A `{role, roleSubprotocol, subprotocolVersion}` tuple.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SubprotocolTuple {
    pub role: String,
    pub role_subprotocol: String,
    pub subprotocol_version: i64,
}
/// A `{os, arch}` platform.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Platform {
    pub os: String,
    pub arch: String,
}
/// The pending effect request's authorization, as the reference's
/// `authorizationEvidence` holds it.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AuthorizationEvidence {
    pub authorized: bool,
    pub effect_class: String,
    pub authorization_ref: String,
    pub operation_ref: String,
    pub decision_class: Option<String>,
    pub binding_mismatch_decision_class: Option<String>,
}
/// The pending effect outcome, as the reference's `effectOutcomeEvidence`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EffectOutcomeEvidence {
    pub request_seq: i64,
    pub decision_seq: i64,
    pub outcome_seq: i64,
    pub commit_class: String,
    pub effect_outcome: String,
    pub effect_class: String,
}

/// What one frame is decided against (LD-D2A-1): the reference's sixteen
/// context members, plus the refusal major it was offered, split (r2, Codex
/// D2A-R1-RF-3) into the session's fixed policy and what it has observed.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlContext {
    policy: ControlPolicy,
    /// The observations the supervisor advances as the session proceeds.
    pub observed: ControlObservations,
}

/// The session's fixed policy: the frame bound and the offer, the admitted
/// identities and platform, and the permitted tuples. Its fields are
/// private. Production makes it only through [`ControlContext::for_session`]
/// (the 65,536 bound and offer, and the admitted selection's one tuple), and
/// nothing changes it afterwards: a session cannot widen its bound or its
/// offer set.
///
/// Each of these fails to compile only because the policy is private: a
/// policy cannot be written whole, a copy of one cannot be widened, and a
/// context cannot be assembled around another policy.
///
/// ```compile_fail
/// use opensip_components::control_protocol::{ControlPolicy, Platform};
/// let widened = ControlPolicy {
///     frame_bound: 16_777_216,
///     frame_offer: 16_777_216,
///     stable_id: String::new(),
///     manifest_digest: String::new(),
///     platform: Platform { os: String::new(), arch: String::new() },
///     manifest_tuples: Vec::new(),
///     offered_tuples: Vec::new(),
///     offered_control_major: 1,
/// };
/// ```
///
/// ```compile_fail
/// use opensip_components::control_protocol::ControlContext;
/// fn widen(context: &ControlContext) {
///     let mut policy = context.policy().clone();
///     policy.frame_bound = 16_777_216;
/// }
/// ```
///
/// ```compile_fail
/// use opensip_components::control_protocol::ControlContext;
/// fn reassemble(context: &ControlContext) -> ControlContext {
///     ControlContext {
///         policy: context.policy().clone(),
///         observed: context.observed.clone(),
///     }
/// }
/// ```
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlPolicy {
    frame_bound: u32,
    frame_offer: i64,
    stable_id: String,
    manifest_digest: String,
    platform: Platform,
    manifest_tuples: Vec<SubprotocolTuple>,
    offered_tuples: Vec<SubprotocolTuple>,
    offered_control_major: i64,
}
impl ControlPolicy {
    pub fn frame_bound(&self) -> u32 {
        self.frame_bound
    }
    pub fn frame_offer(&self) -> i64 {
        self.frame_offer
    }
    pub fn stable_id(&self) -> &str {
        &self.stable_id
    }
    pub fn manifest_digest(&self) -> &str {
        &self.manifest_digest
    }
    pub fn platform(&self) -> &Platform {
        &self.platform
    }
    pub fn manifest_tuples(&self) -> &[SubprotocolTuple] {
        &self.manifest_tuples
    }
    pub fn offered_tuples(&self) -> &[SubprotocolTuple] {
        &self.offered_tuples
    }
    pub fn offered_control_major(&self) -> i64 {
        self.offered_control_major
    }
}

/// What the session has observed: its state, the direction and sequence
/// being decided, the confirms and selection, the pending nonces, and the
/// effect evidence. The supervisor advances these; none widens the policy.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ControlObservations {
    pub state: ControlState,
    pub direction: Direction,
    pub hello_seen: bool,
    pub next_seq: i64,
    pub confirmed_tuples: Vec<SubprotocolTuple>,
    pub selected_tuple: Option<SubprotocolTuple>,
    pub pending_pong: Option<String>,
    pub pending_health_report: Option<String>,
    pub authorization: AuthorizationEvidence,
    pub effect_outcome: EffectOutcomeEvidence,
}

/// An admitted selection's values (D4's, from the admitted manifest): the
/// only inputs to the host's hello and select (item 9).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AdmittedSelection {
    pub stable_id: String,
    pub manifest_digest: String,
    pub platform: Platform,
    /// Role `analyzer`, the provider id and the protocol major.
    pub tuple: SubprotocolTuple,
}

impl ControlContext {
    /// The production session's starting context (item 9's lead
    /// decisions): the 65,536 bound and offer, and the admitted selection's
    /// one tuple as the only offer. Confirms, the selection, nonces and
    /// effect evidence are the supervisor's to set as the session advances.
    pub fn for_session(selection: &AdmittedSelection) -> Self {
        Self {
            policy: ControlPolicy {
                frame_bound: HOST_FRAME_BOUND,
                frame_offer: HOST_FRAME_BOUND as i64,
                stable_id: selection.stable_id.clone(),
                manifest_digest: selection.manifest_digest.clone(),
                platform: selection.platform.clone(),
                manifest_tuples: vec![selection.tuple.clone()],
                offered_tuples: vec![selection.tuple.clone()],
                offered_control_major: 1,
            },
            observed: ControlObservations {
                state: ControlState::AwaitHello,
                direction: Direction::ComponentToHost,
                hello_seen: false,
                next_seq: 1,
                confirmed_tuples: Vec::new(),
                selected_tuple: None,
                pending_pong: None,
                pending_health_report: None,
                authorization: AuthorizationEvidence {
                    authorized: false,
                    effect_class: String::new(),
                    authorization_ref: String::new(),
                    operation_ref: String::new(),
                    decision_class: None,
                    binding_mismatch_decision_class: None,
                },
                effect_outcome: EffectOutcomeEvidence {
                    request_seq: 0,
                    decision_seq: 0,
                    outcome_seq: 0,
                    commit_class: String::new(),
                    effect_outcome: String::new(),
                    effect_class: String::new(),
                },
            },
        }
    }
    /// The fixed policy, read-only.
    pub fn policy(&self) -> &ControlPolicy {
        &self.policy
    }
    /// A reference corpus case's context, whatever its bound, offer and
    /// tuples. Test-only: the corpus replays contexts production never
    /// makes (frame bounds of 131,072 and 16,777,216).
    #[cfg(test)]
    #[allow(clippy::too_many_arguments)]
    pub(crate) fn reference(
        frame_bound: u32,
        frame_offer: i64,
        stable_id: String,
        manifest_digest: String,
        platform: Platform,
        manifest_tuples: Vec<SubprotocolTuple>,
        offered_tuples: Vec<SubprotocolTuple>,
        offered_control_major: i64,
        observed: ControlObservations,
    ) -> Self {
        Self {
            policy: ControlPolicy {
                frame_bound,
                frame_offer,
                stable_id,
                manifest_digest,
                platform,
                manifest_tuples,
                offered_tuples,
                offered_control_major,
            },
            observed,
        }
    }
}

/// An accepted frame: its type, the next state, a refusal's terminal family,
/// and the validated message as the generated `Control3Root`.
#[derive(Debug, Clone)]
pub struct AcceptedFrame {
    pub message_type: &'static str,
    pub next_state: ControlState,
    pub terminal_family: Option<String>,
    pub message: Control3Root,
}
/// A refused frame: its family, an RF6 decision class, and whether its body
/// was buffered before the refusal.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RefusedFrame {
    pub family: RefusalFamily,
    pub decision_class: Option<String>,
    pub body_buffered: bool,
}
/// One frame's decision.
#[derive(Debug, Clone)]
pub enum ControlVerdict {
    Accepted(AcceptedFrame),
    Refused(RefusedFrame),
}

fn refusal(family: RefusalFamily) -> RefusedFrame {
    RefusedFrame {
        family,
        decision_class: None,
        body_buffered: true,
    }
}
fn fail<T>(family: RefusalFamily) -> Result<T, RefusedFrame> {
    Err(refusal(family))
}

static SCHEMA_LOADED: std::sync::OnceLock<Result<Schema, SchemaRefusal>> =
    std::sync::OnceLock::new();
/// The embedded product schema, loaded once. A schema the interpreter cannot
/// take refuses every known-major frame (RF2), never validates loosely.
pub fn schema() -> Result<&'static Schema, &'static SchemaRefusal> {
    SCHEMA_LOADED.get_or_init(|| Schema::load(SCHEMA)).as_ref()
}

const MESSAGE_TYPES: [&str; 16] = [
    "hello",
    "helloAck",
    "select",
    "selectAck",
    "refusal",
    "ping",
    "pong",
    "cancel",
    "health",
    "healthReport",
    "resourceReport",
    "fault",
    "effectRequest",
    "effectResult",
    "shutdown",
    "shutdownAck",
];

/// Decide one received frame (the reference's `parse`), in its order.
pub fn classify(frame: &[u8], context: &ControlContext) -> ControlVerdict {
    match decide(frame, context) {
        Ok(accepted) => ControlVerdict::Accepted(accepted),
        Err(refused) => ControlVerdict::Refused(refused),
    }
}

fn tuple_is(doc: &Doc, id: usize, tuple: &SubprotocolTuple) -> bool {
    doc.object(id).is_some_and(|m| m.len() == 3)
        && doc.str_of(id, "role") == Some(tuple.role.as_str())
        && doc.str_of(id, "roleSubprotocol") == Some(tuple.role_subprotocol.as_str())
        && doc.int_of(id, "subprotocolVersion") == Some(tuple.subprotocol_version)
}
fn tuples(doc: &Doc, id: Option<usize>) -> &[usize] {
    match id.map(|id| &doc.nodes[id]) {
        Some(Node::Array(items)) => items,
        _ => &[],
    }
}

fn decide(frame: &[u8], context: &ControlContext) -> Result<AcceptedFrame, RefusedFrame> {
    use RefusalFamily as F;
    // Framing: decided from the four-byte prefix before any body is buffered.
    let unbuffered = RefusedFrame {
        family: F::Rf2,
        decision_class: None,
        body_buffered: false,
    };
    if frame.len() < 4 {
        return Err(unbuffered);
    }
    let n = u32::from_be_bytes([frame[0], frame[1], frame[2], frame[3]]);
    if n == 0 || n > context.policy.frame_bound {
        return Err(unbuffered);
    }
    if frame.len() != 4 + n as usize {
        return fail(F::Rf2);
    }
    let Ok(text) = std::str::from_utf8(&frame[4..]) else {
        return fail(F::Rf2);
    };
    let Ok(doc) = read_json(text) else {
        return fail(F::Rf2);
    };
    // The frozen envelope.
    let root = doc.root;
    let Some(members) = doc.object(root) else {
        return fail(F::Rf2);
    };
    let keys: BTreeSet<&str> = members.iter().filter_map(|(k, _)| k.text()).collect();
    if members.len() != 4 || keys != BTreeSet::from_iter(["type", "seq", "controlMajor", "body"]) {
        return fail(F::Rf2);
    }
    let field = |k: &str| doc.member(root, k).expect("an envelope member");
    let (ty_id, seq_id, major_id, body) = (
        field("type"),
        field("seq"),
        field("controlMajor"),
        field("body"),
    );
    let ty = match &doc.nodes[ty_id] {
        Node::Str(s) => s.clone(),
        _ => return fail(F::Rf2),
    };
    let major = match doc.nodes[major_id] {
        Node::Int(m) if (1..=MAX_INTEGER).contains(&m) => m,
        _ => return fail(F::Rf2),
    };
    let (seq, sequence_fault) = match doc.nodes[seq_id] {
        Node::Large { negative: true } => return fail(F::Rf2),
        Node::Large { negative: false } => (None, true),
        Node::Int(s) if s < 0 => return fail(F::Rf2),
        Node::Int(s) => (Some(s), s == 0 || s > MAX_INTEGER),
        _ => return fail(F::Rf2),
    };
    if doc.object(body).is_none() {
        return fail(F::Rf2);
    }
    // An unsupported-major hello: the body stays opaque (CC:204-213).
    if ty.text() == Some("hello") && major != 1 {
        if sequence_fault || context.observed.direction != Direction::HostToComponent {
            return fail(F::Rf7);
        }
        if context.observed.hello_seen {
            return fail(F::Rf8);
        }
        if context.observed.state != ControlState::AwaitHello
            || seq != Some(context.observed.next_seq)
        {
            return fail(F::Rf7);
        }
        return fail(F::Rf1);
    }
    let Some(t) = ty
        .text()
        .and_then(|t| MESSAGE_TYPES.iter().copied().find(|m| *m == t))
    else {
        return fail(F::Rf2);
    };
    let Ok(schema) = schema() else {
        return fail(F::Rf2);
    };
    let member = schema.member_for(t).ok_or(refusal(F::Rf2))?;
    // The validation copy: seq replaced by the sentinel 1 when faulty, and
    // for hello and helloAck the string identities replaced by the context's
    // (the specific RF3 exception). The received frame itself is untouched.
    let mut copy = doc.clone();
    if sequence_fault {
        copy.nodes[seq_id] = Node::Int(1);
    }
    if !integers_in_range(&copy, copy.root) {
        return fail(F::Rf2);
    }
    if matches!(t, "hello" | "helloAck") {
        let identity = if t == "hello" {
            "expectedStableId"
        } else {
            "stableId"
        };
        for (key, value) in [
            (identity, context.policy.stable_id.as_str()),
            (
                "admittedManifestDigest",
                context.policy.manifest_digest.as_str(),
            ),
        ] {
            if let Some(id) = copy.member(body, key)
                && matches!(copy.nodes[id], Node::Str(_))
            {
                copy.nodes[id] = Node::Str(JStr::Text(value.to_owned()));
            }
        }
    }
    if !valid(&schema.doc, member, &copy, copy.root) {
        return fail(F::Rf2);
    }
    // The UTF-8 walk sees every received string, with only seq replaced.
    let mut walked = doc.clone();
    if sequence_fault {
        walked.nodes[seq_id] = Node::Int(1);
    }
    if !utf8_bounds(&schema.doc, Some(member), &walked, walked.root) {
        return fail(F::Rf2);
    }
    if sequence_fault {
        return fail(F::Rf7);
    }
    let seq = seq.expect("a non-faulty seq");
    // State and semantics, in the reference's order.
    let state = context.observed.state;
    if !context.observed.direction.carries(t) {
        return fail(F::Rf7);
    }
    if t == "hello" && context.observed.hello_seen {
        return fail(F::Rf8);
    }
    if t == "helloAck" && (major != 1 || doc.int_of(body, "controlMajor") != Some(1)) {
        return fail(F::Rf8);
    }
    if matches!(t, "select" | "selectAck") && state == ControlState::Steady {
        return fail(F::Rf8);
    }
    if seq != context.observed.next_seq || !state.lawful(t) {
        return fail(F::Rf7);
    }
    let expected_major = if t == "refusal" {
        context.policy.offered_control_major
    } else {
        1
    };
    if major != expected_major {
        return fail(F::Rf7);
    }
    if t == "hello" && doc.int_of(body, "controlMajor") != Some(major) {
        return fail(F::Rf8);
    }
    if matches!(t, "hello" | "helloAck") {
        let sid = doc
            .str_of(body, "expectedStableId")
            .or_else(|| doc.str_of(body, "stableId"));
        if sid != Some(context.policy.stable_id.as_str())
            || doc.str_of(body, "admittedManifestDigest")
                != Some(context.policy.manifest_digest.as_str())
        {
            return fail(F::Rf3);
        }
        if t == "hello" {
            let platform = doc.member(body, "platform").expect("a validated platform");
            if doc.str_of(platform, "os") != Some(context.policy.platform.os.as_str())
                || doc.str_of(platform, "arch") != Some(context.policy.platform.arch.as_str())
            {
                return fail(F::Rf3);
            }
        }
        let list = doc
            .member(body, "subprotocolOffers")
            .or_else(|| doc.member(body, "subprotocolConfirms"));
        let items = tuples(&doc, list);
        if items.iter().any(|q| {
            !context
                .policy
                .manifest_tuples
                .iter()
                .any(|m| tuple_is(&doc, *q, m))
        }) {
            return fail(F::Rf4);
        }
        if t == "helloAck" {
            if items.iter().any(|q| {
                !context
                    .policy
                    .offered_tuples
                    .iter()
                    .any(|m| tuple_is(&doc, *q, m))
            }) {
                return fail(F::Rf4);
            }
            if doc.int_of(body, "maxControlFrameBytes").unwrap_or(0) > context.policy.frame_offer {
                return fail(F::Rf2);
            }
        }
    }
    if matches!(t, "select" | "selectAck") {
        if !context
            .observed
            .confirmed_tuples
            .iter()
            .any(|m| tuple_is(&doc, body, m))
        {
            return fail(F::Rf4);
        }
        if t == "selectAck"
            && !context
                .observed
                .selected_tuple
                .as_ref()
                .is_some_and(|m| tuple_is(&doc, body, m))
        {
            return fail(F::Rf4);
        }
    }
    if matches!(t, "pong" | "healthReport") {
        let pending = if t == "pong" {
            &context.observed.pending_pong
        } else {
            &context.observed.pending_health_report
        };
        if doc.str_of(body, "nonce") != pending.as_deref() {
            return fail(F::Rf7);
        }
    }
    if t == "effectRequest" {
        let auth = &context.observed.authorization;
        if !auth.authorized {
            return Err(RefusedFrame {
                family: F::Rf6,
                decision_class: auth.decision_class.clone().filter(|d| !d.is_empty()),
                body_buffered: true,
            });
        }
        if doc.str_of(body, "effectClass") != Some(auth.effect_class.as_str())
            || doc.str_of(body, "authorizationRef") != Some(auth.authorization_ref.as_str())
            || doc.str_of(body, "operationRef") != Some(auth.operation_ref.as_str())
        {
            return Err(RefusedFrame {
                family: F::Rf6,
                decision_class: auth
                    .binding_mismatch_decision_class
                    .clone()
                    .filter(|d| !d.is_empty()),
                body_buffered: true,
            });
        }
    }
    if t == "effectResult" {
        let pending = &context.observed.effect_outcome;
        let int = |k| doc.int_of(body, k).unwrap_or(0);
        if int("outcomeSeq") <= int("decisionSeq")
            || int("requestSeq") != pending.request_seq
            || int("decisionSeq") != pending.decision_seq
            || int("outcomeSeq") != pending.outcome_seq
            || doc.str_of(body, "commitClass") != Some(pending.commit_class.as_str())
            || doc.str_of(body, "effectOutcome") != Some(pending.effect_outcome.as_str())
        {
            return fail(F::Rf7);
        }
        if pending.effect_class == "HE-2" && doc.str_of(body, "commitClass") != Some("REVERSIBLE") {
            return fail(F::Rf7);
        }
    }
    let message = build(t, &doc, seq, major, body).ok_or(refusal(F::Rf2))?;
    Ok(AcceptedFrame {
        message_type: t,
        next_state: state.after(t),
        terminal_family: (t == "refusal")
            .then(|| doc.str_of(body, "family").map(str::to_owned))
            .flatten(),
        message,
    })
}

/// The reference's `numbers`: every integer reachable from `id` within
/// 0..=2^53-1, and no kept lexeme or non-integer anywhere. Iterative.
fn integers_in_range(doc: &Doc, id: usize) -> bool {
    let mut pending = vec![id];
    while let Some(id) = pending.pop() {
        match &doc.nodes[id] {
            Node::Large { .. } | Node::Float => return false,
            Node::Int(v) if !(0..=MAX_INTEGER).contains(v) => return false,
            Node::Array(items) => pending.extend(items.iter().copied()),
            Node::Object(members) => pending.extend(members.iter().map(|(_, v)| *v)),
            _ => {}
        }
    }
    true
}

// ------------------------------------------------------------------ the typed message

fn nz(v: i64) -> Option<NonZeroU64> {
    NonZeroU64::new(u64::try_from(v).ok()?)
}

/// Build the validated frame into `Control3Root` by hand, through the
/// generated types' own constructors (never serde on wire bytes).
fn build(t: &str, doc: &Doc, seq: i64, major: i64, body: usize) -> Option<Control3Root> {
    let s = |k: &str| doc.str_of(body, k);
    let i = |k: &str| doc.int_of(body, k);
    let (seq, control_major) = (nz(seq)?, nz(major)?);
    let tuple_list = |key: &str| -> Option<Vec<(String, String, NonZeroU64)>> {
        tuples(doc, doc.member(body, key))
            .iter()
            .map(|q| {
                Some((
                    doc.str_of(*q, "role")?.to_owned(),
                    doc.str_of(*q, "roleSubprotocol")?.to_owned(),
                    nz(doc.int_of(*q, "subprotocolVersion")?)?,
                ))
            })
            .collect()
    };
    Some(match t {
        "hello" => {
            let platform = doc.member(body, "platform")?;
            Control3Root::Hello {
                body: Control3RootVariant0Property0 {
                    admitted_manifest_digest: s("admittedManifestDigest")?.to_owned(),
                    control_major: nz(i("controlMajor")?)?,
                    expected_stable_id: s("expectedStableId")?.to_owned(),
                    max_control_frame_bytes_offer: i("maxControlFrameBytesOffer")?,
                    platform: Control3RootVariant0Property0Platform {
                        arch: match doc.str_of(platform, "arch")? {
                            "arm64" => Control3RootVariant0Property0PlatformArch::Arm64,
                            "x86_64" => Control3RootVariant0Property0PlatformArch::X8664,
                            _ => return None,
                        },
                        os: match doc.str_of(platform, "os")? {
                            "macos" => Control3RootVariant0Property0PlatformOs::Macos,
                            "linux" => Control3RootVariant0Property0PlatformOs::Linux,
                            _ => return None,
                        },
                    },
                    subprotocol_offers: tuple_list("subprotocolOffers")?
                        .into_iter()
                        .map(|(role, sub, version)| {
                            Some(Control3RootVariant0Property0SubprotocolOffersItem {
                                role: role.parse().ok()?,
                                role_subprotocol: sub.parse().ok()?,
                                subprotocol_version: version,
                            })
                        })
                        .collect::<Option<Vec<_>>>()?,
                },
                control_major,
                seq,
            }
        }
        "helloAck" => Control3Root::HelloAck {
            body: Control3RootVariant1Property0 {
                admitted_manifest_digest: s("admittedManifestDigest")?.to_owned(),
                control_major: nz(i("controlMajor")?)?,
                max_control_frame_bytes: i("maxControlFrameBytes")?,
                stable_id: s("stableId")?.to_owned(),
                subprotocol_confirms: tuple_list("subprotocolConfirms")?
                    .into_iter()
                    .map(|(role, sub, version)| {
                        Some(Control3RootVariant1Property0SubprotocolConfirmsItem {
                            role: role.parse().ok()?,
                            role_subprotocol: sub.parse().ok()?,
                            subprotocol_version: version,
                        })
                    })
                    .collect::<Option<Vec<_>>>()?,
            },
            control_major,
            seq,
        },
        "select" => Control3Root::Select {
            body: Control3RootVariant2Property0 {
                role: s("role")?.parse().ok()?,
                role_subprotocol: s("roleSubprotocol")?.parse().ok()?,
                subprotocol_version: nz(i("subprotocolVersion")?)?,
            },
            control_major,
            seq,
        },
        "selectAck" => Control3Root::SelectAck {
            body: Control3RootVariant3Property0 {
                role: s("role")?.parse().ok()?,
                role_subprotocol: s("roleSubprotocol")?.parse().ok()?,
                subprotocol_version: nz(i("subprotocolVersion")?)?,
            },
            control_major,
            seq,
        },
        "refusal" => Control3Root::Refusal {
            body: Control3RootVariant4Property0 {
                decision_class: match s("decisionClass") {
                    None => FieldPresence::Missing,
                    Some(d) => FieldPresence::Present(Some(match d {
                        "PR-1" => Control3RootVariant4Property0DecisionClass::Pr1,
                        "PR-2" => Control3RootVariant4Property0DecisionClass::Pr2,
                        "PR-3" => Control3RootVariant4Property0DecisionClass::Pr3,
                        "PR-4" => Control3RootVariant4Property0DecisionClass::Pr4,
                        "PR-5" => Control3RootVariant4Property0DecisionClass::Pr5,
                        "PR-6" => Control3RootVariant4Property0DecisionClass::Pr6,
                        "PR-7" => Control3RootVariant4Property0DecisionClass::Pr7,
                        "PR-8" => Control3RootVariant4Property0DecisionClass::Pr8,
                        "PR-9" => Control3RootVariant4Property0DecisionClass::Pr9,
                        _ => return None,
                    })),
                },
                detail: match s("detail") {
                    None => FieldPresence::Missing,
                    Some(d) => FieldPresence::Present(Some(d.parse().ok()?)),
                },
                family: match s("family")? {
                    "RF-1" => Control3RootVariant4Property0Family::Rf1,
                    "RF-2" => Control3RootVariant4Property0Family::Rf2,
                    "RF-3" => Control3RootVariant4Property0Family::Rf3,
                    "RF-4" => Control3RootVariant4Property0Family::Rf4,
                    "RF-5" => Control3RootVariant4Property0Family::Rf5,
                    "RF-6" => Control3RootVariant4Property0Family::Rf6,
                    "RF-7" => Control3RootVariant4Property0Family::Rf7,
                    "RF-8" => Control3RootVariant4Property0Family::Rf8,
                    _ => return None,
                },
                supported_control_majors: match doc.member(body, "supportedControlMajors") {
                    None => FieldPresence::Missing,
                    Some(list) => FieldPresence::Present(Some(
                        tuples(doc, Some(list))
                            .iter()
                            .map(|m| nz(doc.int(*m)?))
                            .collect::<Option<Vec<_>>>()?,
                    )),
                },
            },
            control_major,
            seq,
        },
        "ping" => Control3Root::Ping {
            body: Control3RootVariant5Property0 {
                nonce: s("nonce")?.parse().ok()?,
            },
            control_major,
            seq,
        },
        "pong" => Control3Root::Pong {
            body: Control3RootVariant6Property0 {
                nonce: s("nonce")?.parse().ok()?,
            },
            control_major,
            seq,
        },
        "cancel" => Control3Root::Cancel {
            body: Control3RootVariant7Property0 {
                reason: match s("reason")? {
                    "user" => Control3RootVariant7Property0Reason::User,
                    "deadline" => Control3RootVariant7Property0Reason::Deadline,
                    "supervisor-fault" => Control3RootVariant7Property0Reason::SupervisorFault,
                    _ => return None,
                },
            },
            control_major,
            seq,
        },
        "health" => Control3Root::Health {
            body: Control3RootVariant8Property0 {
                nonce: s("nonce")?.parse().ok()?,
            },
            control_major,
            seq,
        },
        "healthReport" => Control3Root::HealthReport {
            body: Control3RootVariant9Property0 {
                nonce: s("nonce")?.parse().ok()?,
                status: match s("status")? {
                    "ready" => Control3RootVariant9Property0Status::Ready,
                    "busy" => Control3RootVariant9Property0Status::Busy,
                    "stopping" => Control3RootVariant9Property0Status::Stopping,
                    _ => return None,
                },
            },
            control_major,
            seq,
        },
        "resourceReport" => Control3Root::ResourceReport {
            body: Control3RootVariant10Property0 {
                cpu_nanoseconds: i("cpuNanoseconds")?,
                open_handles: i("openHandles")?,
                resident_bytes: i("residentBytes")?,
            },
            control_major,
            seq,
        },
        "fault" => Control3Root::Fault {
            body: Control3RootVariant11Property0 {
                detail: s("detail")?.parse().ok()?,
            },
            control_major,
            seq,
        },
        "effectRequest" => Control3Root::EffectRequest {
            body: Control3RootVariant12Property0 {
                authorization_ref: s("authorizationRef")?.parse().ok()?,
                effect_class: match s("effectClass")? {
                    "HE-1" => Control3RootVariant12Property0EffectClass::He1,
                    "HE-2" => Control3RootVariant12Property0EffectClass::He2,
                    _ => return None,
                },
                operation_ref: s("operationRef")?.parse().ok()?,
            },
            control_major,
            seq,
        },
        "effectResult" => Control3Root::EffectResult {
            body: Control3RootVariant13Property0 {
                commit_class: match s("commitClass")? {
                    "REVERSIBLE" => Control3RootVariant13Property0CommitClass::Reversible,
                    "IRREVERSIBLE" => Control3RootVariant13Property0CommitClass::Irreversible,
                    _ => return None,
                },
                decision_seq: nz(i("decisionSeq")?)?,
                effect_outcome: match s("effectOutcome")? {
                    "COMPLETED" => Control3RootVariant13Property0EffectOutcome::Completed,
                    "FAILED" => Control3RootVariant13Property0EffectOutcome::Failed,
                    "INDETERMINATE" => Control3RootVariant13Property0EffectOutcome::Indeterminate,
                    _ => return None,
                },
                outcome_seq: nz(i("outcomeSeq")?)?,
                request_seq: nz(i("requestSeq")?)?,
                result_ref: match s("resultRef") {
                    None => FieldPresence::Missing,
                    Some(r) => FieldPresence::Present(Some(r.parse().ok()?)),
                },
            },
            control_major,
            seq,
        },
        "shutdown" => Control3Root::Shutdown {
            body: Control3RootVariant14Property0 {
                reason: match s("reason")? {
                    "normal" => Control3RootVariant14Property0Reason::Normal,
                    "cancelled" => Control3RootVariant14Property0Reason::Cancelled,
                    "refused" => Control3RootVariant14Property0Reason::Refused,
                    "fault" => Control3RootVariant14Property0Reason::Fault,
                    _ => return None,
                },
            },
            control_major,
            seq,
        },
        "shutdownAck" => Control3Root::ShutdownAck {
            body: Control3RootVariant15Property0 {},
            control_major,
            seq,
        },
        _ => return None,
    })
}

// ------------------------------------------------------------------ the session driver

/// One received frame's step in a session: its decision, and the session
/// after it.
#[derive(Debug, Clone)]
pub struct SessionStep {
    pub verdict: ControlVerdict,
    pub state: ControlState,
    pub stopped: Vec<Direction>,
    pub next_seq: [i64; 2],
}

/// The two directions' sequences and stopping (LD-D2A-5; CC:137-140; the
/// reference's `run_session`): a frame on a stopped direction is RF7, never
/// buffered or parsed; a refusal verdict stops its direction and faults the
/// session; an accepted refusal or shutdownAck stops its direction; with both
/// directions stopped the session is closed. A direction never reopens.
#[derive(Debug, Clone)]
pub struct ControlSession {
    context: ControlContext,
    stopped: BTreeSet<Direction>,
    next_seq: [i64; 2],
}
fn slot(direction: Direction) -> usize {
    match direction {
        Direction::HostToComponent => 0,
        Direction::ComponentToHost => 1,
    }
}
impl ControlSession {
    /// A session from `context`'s state; both directions start at seq 1.
    pub fn new(context: ControlContext) -> Self {
        Self {
            context,
            stopped: BTreeSet::new(),
            next_seq: [1, 1],
        }
    }
    pub fn state(&self) -> ControlState {
        self.context.observed.state
    }
    /// The observations the next frame is decided against, for the
    /// supervisor to advance (confirms, the selection, nonces, effect
    /// evidence). The policy is not reachable from here.
    pub fn observations_mut(&mut self) -> &mut ControlObservations {
        &mut self.context.observed
    }
    /// The session's fixed policy.
    pub fn policy(&self) -> &ControlPolicy {
        &self.context.policy
    }
    /// The verdict a frame on `direction` would get now, changing nothing.
    fn verdict(&self, direction: Direction, frame: &[u8]) -> ControlVerdict {
        if self.stopped.contains(&direction) {
            return ControlVerdict::Refused(RefusedFrame {
                family: RefusalFamily::Rf7,
                decision_class: None,
                body_buffered: false,
            });
        }
        let mut context = self.context.clone();
        context.observed.direction = direction;
        context.observed.next_seq = self.next_seq[slot(direction)];
        classify(frame, &context)
    }

    /// Encode and send the host's `message` (r2, Codex D2A-R1-RF-2): it must
    /// be a valid host frame (`encode`); a hello must carry exactly the
    /// policy's identities, platform, offer and offered tuples, and a select
    /// one of the offered tuples; and the session must accept it as the
    /// host's next frame. Only then is the session advanced and the frame
    /// returned. A refusal sends and advances nothing.
    pub fn send(&mut self, message: &Control3Root) -> Result<Vec<u8>, EncodeRefusal> {
        let frame = encode(message)?;
        let policy = &self.context.policy;
        let offered = |role: &str, sub: &str, version: NonZeroU64| {
            policy.offered_tuples.iter().any(|t| {
                t.role == role
                    && t.role_subprotocol == sub
                    && u64::try_from(t.subprotocol_version).ok() == Some(version.get())
            })
        };
        match message {
            Control3Root::Hello { body, .. } => {
                if *body.expected_stable_id != *policy.stable_id
                    || *body.admitted_manifest_digest != *policy.manifest_digest
                {
                    return Err(EncodeRefusal::Policy("identities"));
                }
                let platform = (
                    match body.platform.os {
                        Control3RootVariant0Property0PlatformOs::Macos => "macos",
                        Control3RootVariant0Property0PlatformOs::Linux => "linux",
                    },
                    match body.platform.arch {
                        Control3RootVariant0Property0PlatformArch::Arm64 => "arm64",
                        Control3RootVariant0Property0PlatformArch::X8664 => "x86_64",
                    },
                );
                if platform != (policy.platform.os.as_str(), policy.platform.arch.as_str()) {
                    return Err(EncodeRefusal::Policy("platform"));
                }
                if body.max_control_frame_bytes_offer != policy.frame_offer {
                    return Err(EncodeRefusal::Policy("frame offer"));
                }
                if body.subprotocol_offers.len() != policy.offered_tuples.len()
                    || !body
                        .subprotocol_offers
                        .iter()
                        .all(|q| offered(&q.role, &q.role_subprotocol, q.subprotocol_version))
                {
                    return Err(EncodeRefusal::Policy("offered tuples"));
                }
            }
            Control3Root::Select { body, .. }
                if !offered(&body.role, &body.role_subprotocol, body.subprotocol_version) =>
            {
                return Err(EncodeRefusal::Policy("selected tuple"));
            }
            _ => {}
        }
        match self.verdict(Direction::HostToComponent, &frame) {
            ControlVerdict::Accepted(accepted) => {
                self.apply(
                    Direction::HostToComponent,
                    &ControlVerdict::Accepted(accepted),
                );
                Ok(frame)
            }
            ControlVerdict::Refused(refused) => Err(EncodeRefusal::Session(refused.family)),
        }
    }

    /// Advance the session after `verdict` on `direction`.
    fn apply(&mut self, direction: Direction, verdict: &ControlVerdict) {
        if !self.stopped.contains(&direction) {
            match verdict {
                ControlVerdict::Accepted(accepted) => {
                    self.next_seq[slot(direction)] += 1;
                    self.context.observed.state = accepted.next_state;
                    if matches!(accepted.message_type, "refusal" | "shutdownAck") {
                        self.stopped.insert(direction);
                    }
                }
                ControlVerdict::Refused(_) => {
                    self.stopped.insert(direction);
                    self.context.observed.state = ControlState::Faulted;
                }
            }
        }
        if self.stopped.len() == 2 {
            self.context.observed.state = ControlState::Closed;
        }
    }

    /// Decide one frame received on `direction`.
    pub fn receive(&mut self, direction: Direction, frame: &[u8]) -> SessionStep {
        let verdict = self.verdict(direction, frame);
        self.apply(direction, &verdict);
        // Stopped directions in name order, as the reference sorts them.
        let mut stopped: Vec<Direction> = self.stopped.iter().copied().collect();
        stopped.sort_by_key(|d| d.as_str());
        SessionStep {
            verdict,
            state: self.context.observed.state,
            stopped,
            next_seq: self.next_seq,
        }
    }
}

// ------------------------------------------------------------------ the encoder

/// Why the host's own frame is not written.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EncodeRefusal {
    /// A component's message: the host never writes one (r2, Codex
    /// D2A-R1-RF-1).
    ComponentMessage(&'static str),
    /// A hello must offer exactly the one admitted tuple (LD-D2A-8).
    HelloOffers(usize),
    /// An optional member present as null, which no host message admits.
    NullMember(&'static str),
    /// The written frame breaks the closed message schema (the identity
    /// patterns and refusal conditionals included), the integer domain or a
    /// string's UTF-8 bound (r2, Codex D2A-R1-RF-2).
    Invalid(&'static str),
    /// The frame would exceed the host's bound.
    TooLarge(usize),
    /// The message breaks the session's fixed policy: its identities,
    /// platform, offer or tuples (r2, D2A-R1-RF-2).
    Policy(&'static str),
    /// The session would refuse the frame (its state, direction or
    /// sequence), with that family. Nothing is sent or advanced.
    Session(RefusalFamily),
}

struct Writer(String);
impl Writer {
    fn string(&mut self, s: &str) {
        self.0.push('"');
        for c in s.chars() {
            match c {
                '"' => self.0.push_str("\\\""),
                '\\' => self.0.push_str("\\\\"),
                c if (c as u32) < 0x20 => {
                    const HEX: &[u8; 16] = b"0123456789abcdef";
                    let v = c as u32;
                    self.0.push_str("\\u00");
                    self.0.push(HEX[(v >> 4) as usize] as char);
                    self.0.push(HEX[(v & 15) as usize] as char);
                }
                c => self.0.push(c),
            }
        }
        self.0.push('"');
    }
    fn key(&mut self, first: &mut bool, k: &str) {
        if !*first {
            self.0.push(',');
        }
        *first = false;
        self.string(k);
        self.0.push(':');
    }
    fn int(&mut self, v: u64) {
        self.0.push_str(&v.to_string());
    }
    fn signed(&mut self, v: i64) {
        self.0.push_str(&v.to_string());
    }
}

/// A tuple object's members, in schema order.
fn write_tuple(w: &mut Writer, role: &str, sub: &str, version: NonZeroU64) {
    w.0.push('{');
    let mut first = true;
    w.key(&mut first, "role");
    w.string(role);
    w.key(&mut first, "roleSubprotocol");
    w.string(sub);
    w.key(&mut first, "subprotocolVersion");
    w.int(version.get());
    w.0.push('}');
}

/// Serialize a generated value's closed enum or newtype through its own
/// serde name, without a serializer crate: each is matched here.
fn write_body(w: &mut Writer, message: &Control3Root) -> Result<(), EncodeRefusal> {
    let mut first = true;
    w.0.push('{');
    match message {
        Control3Root::Hello { body, .. } => {
            if body.subprotocol_offers.len() != 1 {
                return Err(EncodeRefusal::HelloOffers(body.subprotocol_offers.len()));
            }
            w.key(&mut first, "controlMajor");
            w.int(body.control_major.get());
            w.key(&mut first, "expectedStableId");
            w.string(&body.expected_stable_id);
            w.key(&mut first, "admittedManifestDigest");
            w.string(&body.admitted_manifest_digest);
            w.key(&mut first, "platform");
            w.0.push('{');
            let mut inner = true;
            w.key(&mut inner, "os");
            w.string(match body.platform.os {
                Control3RootVariant0Property0PlatformOs::Macos => "macos",
                Control3RootVariant0Property0PlatformOs::Linux => "linux",
            });
            w.key(&mut inner, "arch");
            w.string(match body.platform.arch {
                Control3RootVariant0Property0PlatformArch::Arm64 => "arm64",
                Control3RootVariant0Property0PlatformArch::X8664 => "x86_64",
            });
            w.0.push('}');
            w.key(&mut first, "maxControlFrameBytesOffer");
            w.signed(body.max_control_frame_bytes_offer);
            w.key(&mut first, "subprotocolOffers");
            w.0.push('[');
            for (n, q) in body.subprotocol_offers.iter().enumerate() {
                if n > 0 {
                    w.0.push(',');
                }
                write_tuple(w, &q.role, &q.role_subprotocol, q.subprotocol_version);
            }
            w.0.push(']');
        }
        Control3Root::Select { body, .. } => {
            // The tuple object is the body itself.
            w.0.pop();
            write_tuple(
                w,
                &body.role,
                &body.role_subprotocol,
                body.subprotocol_version,
            );
            return Ok(());
        }
        Control3Root::Ping { body, .. } => {
            w.key(&mut first, "nonce");
            w.string(&body.nonce);
        }
        Control3Root::Health { body, .. } => {
            w.key(&mut first, "nonce");
            w.string(&body.nonce);
        }
        Control3Root::Cancel { body, .. } => {
            w.key(&mut first, "reason");
            w.string(match body.reason {
                Control3RootVariant7Property0Reason::User => "user",
                Control3RootVariant7Property0Reason::Deadline => "deadline",
                Control3RootVariant7Property0Reason::SupervisorFault => "supervisor-fault",
            });
        }
        Control3Root::Shutdown { body, .. } => {
            w.key(&mut first, "reason");
            w.string(match body.reason {
                Control3RootVariant14Property0Reason::Normal => "normal",
                Control3RootVariant14Property0Reason::Cancelled => "cancelled",
                Control3RootVariant14Property0Reason::Refused => "refused",
                Control3RootVariant14Property0Reason::Fault => "fault",
            });
        }
        Control3Root::EffectResult { body, .. } => {
            w.key(&mut first, "requestSeq");
            w.int(body.request_seq.get());
            w.key(&mut first, "decisionSeq");
            w.int(body.decision_seq.get());
            w.key(&mut first, "outcomeSeq");
            w.int(body.outcome_seq.get());
            w.key(&mut first, "commitClass");
            w.string(match body.commit_class {
                Control3RootVariant13Property0CommitClass::Reversible => "REVERSIBLE",
                Control3RootVariant13Property0CommitClass::Irreversible => "IRREVERSIBLE",
            });
            w.key(&mut first, "effectOutcome");
            w.string(match body.effect_outcome {
                Control3RootVariant13Property0EffectOutcome::Completed => "COMPLETED",
                Control3RootVariant13Property0EffectOutcome::Failed => "FAILED",
                Control3RootVariant13Property0EffectOutcome::Indeterminate => "INDETERMINATE",
            });
            match &body.result_ref {
                FieldPresence::Missing => {}
                FieldPresence::Present(None) => return Err(EncodeRefusal::NullMember("resultRef")),
                FieldPresence::Present(Some(r)) => {
                    w.key(&mut first, "resultRef");
                    w.string(r);
                }
            }
        }
        Control3Root::Refusal { body, .. } => {
            w.key(&mut first, "family");
            w.string(match body.family {
                Control3RootVariant4Property0Family::Rf1 => "RF-1",
                Control3RootVariant4Property0Family::Rf2 => "RF-2",
                Control3RootVariant4Property0Family::Rf3 => "RF-3",
                Control3RootVariant4Property0Family::Rf4 => "RF-4",
                Control3RootVariant4Property0Family::Rf5 => "RF-5",
                Control3RootVariant4Property0Family::Rf6 => "RF-6",
                Control3RootVariant4Property0Family::Rf7 => "RF-7",
                Control3RootVariant4Property0Family::Rf8 => "RF-8",
            });
            if let FieldPresence::Present(None) = &body.supported_control_majors {
                return Err(EncodeRefusal::NullMember("supportedControlMajors"));
            }
            if let FieldPresence::Present(Some(majors)) = &body.supported_control_majors {
                w.key(&mut first, "supportedControlMajors");
                w.0.push('[');
                for (n, m) in majors.iter().enumerate() {
                    if n > 0 {
                        w.0.push(',');
                    }
                    w.int(m.get());
                }
                w.0.push(']');
            }
            if let FieldPresence::Present(None) = &body.decision_class {
                return Err(EncodeRefusal::NullMember("decisionClass"));
            }
            if let FieldPresence::Present(Some(d)) = &body.decision_class {
                w.key(&mut first, "decisionClass");
                w.string(match d {
                    Control3RootVariant4Property0DecisionClass::Pr1 => "PR-1",
                    Control3RootVariant4Property0DecisionClass::Pr2 => "PR-2",
                    Control3RootVariant4Property0DecisionClass::Pr3 => "PR-3",
                    Control3RootVariant4Property0DecisionClass::Pr4 => "PR-4",
                    Control3RootVariant4Property0DecisionClass::Pr5 => "PR-5",
                    Control3RootVariant4Property0DecisionClass::Pr6 => "PR-6",
                    Control3RootVariant4Property0DecisionClass::Pr7 => "PR-7",
                    Control3RootVariant4Property0DecisionClass::Pr8 => "PR-8",
                    Control3RootVariant4Property0DecisionClass::Pr9 => "PR-9",
                });
            }
            match &body.detail {
                FieldPresence::Missing => {}
                FieldPresence::Present(None) => return Err(EncodeRefusal::NullMember("detail")),
                FieldPresence::Present(Some(detail)) => {
                    w.key(&mut first, "detail");
                    w.string(detail);
                }
            }
        }
        // The component's messages: the host never writes them (r2,
        // D2A-R1-RF-1). `encode` refuses every one before it writes a byte.
        Control3Root::HelloAck { .. }
        | Control3Root::SelectAck { .. }
        | Control3Root::Pong { .. }
        | Control3Root::HealthReport { .. }
        | Control3Root::ResourceReport { .. }
        | Control3Root::Fault { .. }
        | Control3Root::EffectRequest { .. }
        | Control3Root::ShutdownAck { .. } => {
            unreachable!("encode refuses a component message first")
        }
    }
    w.0.push('}');
    Ok(())
}

/// The message's type name and envelope.
fn envelope(message: &Control3Root) -> (&'static str, NonZeroU64, NonZeroU64) {
    match message {
        Control3Root::Hello {
            seq, control_major, ..
        } => ("hello", *seq, *control_major),
        Control3Root::HelloAck {
            seq, control_major, ..
        } => ("helloAck", *seq, *control_major),
        Control3Root::Select {
            seq, control_major, ..
        } => ("select", *seq, *control_major),
        Control3Root::SelectAck {
            seq, control_major, ..
        } => ("selectAck", *seq, *control_major),
        Control3Root::Refusal {
            seq, control_major, ..
        } => ("refusal", *seq, *control_major),
        Control3Root::Ping {
            seq, control_major, ..
        } => ("ping", *seq, *control_major),
        Control3Root::Pong {
            seq, control_major, ..
        } => ("pong", *seq, *control_major),
        Control3Root::Cancel {
            seq, control_major, ..
        } => ("cancel", *seq, *control_major),
        Control3Root::Health {
            seq, control_major, ..
        } => ("health", *seq, *control_major),
        Control3Root::HealthReport {
            seq, control_major, ..
        } => ("healthReport", *seq, *control_major),
        Control3Root::ResourceReport {
            seq, control_major, ..
        } => ("resourceReport", *seq, *control_major),
        Control3Root::Fault {
            seq, control_major, ..
        } => ("fault", *seq, *control_major),
        Control3Root::EffectRequest {
            seq, control_major, ..
        } => ("effectRequest", *seq, *control_major),
        Control3Root::EffectResult {
            seq, control_major, ..
        } => ("effectResult", *seq, *control_major),
        Control3Root::Shutdown {
            seq, control_major, ..
        } => ("shutdown", *seq, *control_major),
        Control3Root::ShutdownAck {
            seq, control_major, ..
        } => ("shutdownAck", *seq, *control_major),
    }
}

/// Write one of the host's frames: the 4-byte big-endian length, then the
/// closed JSON object. Only the host's eight message types are written; a
/// hello must carry exactly one offer; no optional member is null; the
/// written frame must satisfy the closed message schema with no identity
/// substitution, the integer domain and every string's UTF-8 bound (r2,
/// D2A-R1-RF-2); and it must fit the host's bound.
pub fn encode(message: &Control3Root) -> Result<Vec<u8>, EncodeRefusal> {
    let (ty, seq, major) = envelope(message);
    if !Direction::HostToComponent.carries(ty) {
        return Err(EncodeRefusal::ComponentMessage(ty));
    }
    let mut w = Writer(String::new());
    w.0.push('{');
    let mut first = true;
    w.key(&mut first, "type");
    w.string(ty);
    w.key(&mut first, "seq");
    w.int(seq.get());
    w.key(&mut first, "controlMajor");
    w.int(major.get());
    w.key(&mut first, "body");
    write_body(&mut w, message)?;
    w.0.push('}');
    let body = bounded(w.0, HOST_FRAME_BOUND)?;
    validate_outgoing(&body, ty)?;
    let mut frame = (body.len() as u32).to_be_bytes().to_vec();
    frame.extend_from_slice(body.as_bytes());
    Ok(frame)
}

/// The written body within `bound` bytes: exactly the bound fits.
fn bounded(body: String, bound: u32) -> Result<String, EncodeRefusal> {
    if body.len() > bound as usize {
        return Err(EncodeRefusal::TooLarge(body.len()));
    }
    Ok(body)
}

/// The host's written body judged as its receiver would judge it, but with
/// no identity substitution: every outgoing identity must itself satisfy
/// the schema's patterns.
fn validate_outgoing(body: &str, ty: &str) -> Result<(), EncodeRefusal> {
    let doc = read_json(body).map_err(|_| EncodeRefusal::Invalid("not strict JSON"))?;
    if !integers_in_range(&doc, doc.root) {
        return Err(EncodeRefusal::Invalid("integer domain"));
    }
    let schema = schema().map_err(|_| EncodeRefusal::Invalid("schema unloadable"))?;
    let member = schema
        .member_for(ty)
        .ok_or(EncodeRefusal::Invalid("message type"))?;
    if !valid(&schema.doc, member, &doc, doc.root) {
        return Err(EncodeRefusal::Invalid("message schema"));
    }
    if !utf8_bounds(&schema.doc, Some(member), &doc, doc.root) {
        return Err(EncodeRefusal::Invalid("UTF-8 bound"));
    }
    Ok(())
}

/// The host's hello for an admitted selection (item 9): its identities and
/// platform, the 65,536 offer and exactly its one tuple.
pub fn host_hello(selection: &AdmittedSelection, seq: NonZeroU64) -> Option<Control3Root> {
    let tuple = &selection.tuple;
    Some(Control3Root::Hello {
        body: Control3RootVariant0Property0 {
            admitted_manifest_digest: selection.manifest_digest.clone(),
            control_major: NonZeroU64::MIN,
            expected_stable_id: selection.stable_id.clone(),
            max_control_frame_bytes_offer: HOST_FRAME_BOUND as i64,
            platform: Control3RootVariant0Property0Platform {
                arch: match selection.platform.arch.as_str() {
                    "arm64" => Control3RootVariant0Property0PlatformArch::Arm64,
                    "x86_64" => Control3RootVariant0Property0PlatformArch::X8664,
                    _ => return None,
                },
                os: match selection.platform.os.as_str() {
                    "macos" => Control3RootVariant0Property0PlatformOs::Macos,
                    "linux" => Control3RootVariant0Property0PlatformOs::Linux,
                    _ => return None,
                },
            },
            subprotocol_offers: vec![Control3RootVariant0Property0SubprotocolOffersItem {
                role: tuple.role.parse().ok()?,
                role_subprotocol: tuple.role_subprotocol.parse().ok()?,
                subprotocol_version: nz(tuple.subprotocol_version)?,
            }],
        },
        control_major: NonZeroU64::MIN,
        seq,
    })
}

/// The host's select: the admitted selection's one tuple (item 9).
pub fn host_select(selection: &AdmittedSelection, seq: NonZeroU64) -> Option<Control3Root> {
    let tuple = &selection.tuple;
    Some(Control3Root::Select {
        body: Control3RootVariant2Property0 {
            role: tuple.role.parse().ok()?,
            role_subprotocol: tuple.role_subprotocol.parse().ok()?,
            subprotocol_version: nz(tuple.subprotocol_version)?,
        },
        control_major: NonZeroU64::MIN,
        seq,
    })
}

#[cfg(test)]
#[path = "control_protocol_tests.rs"]
mod tests;

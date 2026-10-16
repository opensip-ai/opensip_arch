// M3-B r8 item 14a (unit B2-c2): the first-party JSONC reader shared by the
// pre-Plan TypeScript configuration graph (`typescript_config.rs`) and C2's
// `TypeScriptConfigProjectionV2`. Pure: it reads a byte slice and evaluates
// nothing (FW-01).
//
// The grammar is RFC 8259 JSON with `//` and `/* */` comments wherever
// whitespace may stand, and one trailing comma after the last member of an
// object or the last element of an array. A duplicate key keeps its last
// value at its first position, as a JavaScript object literal does. The
// input is UTF-8; a leading byte order mark is ignored (RFC 8259 §8.1). A
// document holding only whitespace and comments has no root value.
//
// The parser is iterative over an arena, so neither parsing nor dropping a
// deeply nested document recurses: the 64 KiB file bound is the only bound.
use std::collections::BTreeMap;

/// One parsed value. Containers hold arena indices, never owned children.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) enum Node {
    Null,
    Bool(bool),
    /// The number's exact lexeme; nothing here reads a number's value.
    Number(String),
    String(String),
    Array(Vec<usize>),
    /// Members in first-occurrence order, each key once (the last value).
    Object(Vec<(String, usize)>),
}

/// A parsed document: the arena and its root, `None` for a document that
/// holds only whitespace and comments.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct Document {
    nodes: Vec<Node>,
    root: Option<usize>,
}
impl Document {
    pub(crate) fn root(&self) -> Option<&Node> {
        self.root.map(|i| &self.nodes[i])
    }
    pub(crate) fn node(&self, index: usize) -> &Node {
        &self.nodes[index]
    }
    /// An object's member value, if `object` is an object holding `key`.
    pub(crate) fn member(&self, object: &Node, key: &str) -> Option<&Node> {
        match object {
            Node::Object(members) => members
                .iter()
                .find(|(k, _)| k == key)
                .map(|(_, i)| &self.nodes[*i]),
            _ => None,
        }
    }
}

/// Why a byte slice is not JSONC, and the byte offset where that was found.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct JsoncError {
    pub(crate) offset: usize,
    pub(crate) reason: &'static str,
}

const BOM: &[u8] = b"\xef\xbb\xbf";

/// Parse `bytes` as one JSONC document.
pub(crate) fn parse(bytes: &[u8]) -> Result<Document, JsoncError> {
    if let Err(e) = std::str::from_utf8(bytes) {
        return Err(JsoncError {
            offset: e.valid_up_to(),
            reason: "not UTF-8",
        });
    }
    let mut p = Parser {
        text: bytes,
        at: if bytes.starts_with(BOM) { BOM.len() } else { 0 },
        nodes: Vec::new(),
    };
    p.skip()?;
    if p.at == p.text.len() {
        return Ok(Document {
            nodes: p.nodes,
            root: None,
        });
    }
    let root = p.value()?;
    p.skip()?;
    if p.at != p.text.len() {
        return Err(p.error("content after the root value"));
    }
    Ok(Document {
        nodes: p.nodes,
        root: Some(root),
    })
}

/// An open container: its arena index, and for an object the pending key
/// and the position of each key already present.
enum Frame {
    Array(usize),
    Object {
        node: usize,
        key: String,
        positions: BTreeMap<String, usize>,
    },
}

struct Parser<'t> {
    text: &'t [u8],
    at: usize,
    nodes: Vec<Node>,
}
impl Parser<'_> {
    fn error(&self, reason: &'static str) -> JsoncError {
        JsoncError {
            offset: self.at,
            reason,
        }
    }
    fn peek(&self) -> Option<u8> {
        self.text.get(self.at).copied()
    }
    fn eat(&mut self, byte: u8) -> bool {
        let hit = self.peek() == Some(byte);
        if hit {
            self.at += 1;
        }
        hit
    }
    fn push(&mut self, node: Node) -> usize {
        self.nodes.push(node);
        self.nodes.len() - 1
    }
    /// Whitespace (space, tab, LF, CR) and comments. A line comment ends at
    /// LF or CR; a block comment must close.
    fn skip(&mut self) -> Result<(), JsoncError> {
        loop {
            match self.peek() {
                Some(b' ' | b'\t' | b'\n' | b'\r') => self.at += 1,
                Some(b'/') => match self.text.get(self.at + 1) {
                    Some(b'/') => {
                        self.at += 2;
                        while !matches!(self.peek(), None | Some(b'\n' | b'\r')) {
                            self.at += 1;
                        }
                    }
                    Some(b'*') => {
                        let start = self.at;
                        self.at += 2;
                        loop {
                            match self.peek() {
                                None => {
                                    self.at = start;
                                    return Err(self.error("unterminated block comment"));
                                }
                                Some(b'*') if self.text.get(self.at + 1) == Some(&b'/') => {
                                    self.at += 2;
                                    break;
                                }
                                Some(_) => self.at += 1,
                            }
                        }
                    }
                    _ => return Err(self.error("a lone '/'")),
                },
                _ => return Ok(()),
            }
        }
    }
    /// An object key, its colon, and the whitespace before its value.
    fn key(&mut self) -> Result<String, JsoncError> {
        if self.peek() != Some(b'"') {
            return Err(self.error("an object key must be a string"));
        }
        let key = self.string()?;
        self.skip()?;
        if !self.eat(b':') {
            return Err(self.error("expected ':'"));
        }
        self.skip()?;
        Ok(key)
    }
    /// One value at the cursor (whitespace already skipped), iteratively.
    fn value(&mut self) -> Result<usize, JsoncError> {
        let mut stack: Vec<Frame> = Vec::new();
        loop {
            let mut done = match self.peek() {
                Some(b'{') => {
                    self.at += 1;
                    let node = self.push(Node::Object(Vec::new()));
                    self.skip()?;
                    if self.eat(b'}') {
                        node
                    } else {
                        let key = self.key()?;
                        stack.push(Frame::Object {
                            node,
                            key,
                            positions: BTreeMap::new(),
                        });
                        continue;
                    }
                }
                Some(b'[') => {
                    self.at += 1;
                    let node = self.push(Node::Array(Vec::new()));
                    self.skip()?;
                    if self.eat(b']') {
                        node
                    } else {
                        stack.push(Frame::Array(node));
                        continue;
                    }
                }
                _ => self.scalar()?,
            };
            // Attach each completed value to its container, closing every
            // container that ends here.
            loop {
                let Some(frame) = stack.last_mut() else {
                    return Ok(done);
                };
                match frame {
                    Frame::Array(node) => {
                        let node = *node;
                        if let Node::Array(items) = &mut self.nodes[node] {
                            items.push(done);
                        }
                        self.skip()?;
                        if self.eat(b',') {
                            self.skip()?;
                            if !self.eat(b']') {
                                break;
                            }
                        } else if !self.eat(b']') {
                            return Err(self.error("expected ',' or ']'"));
                        }
                        stack.pop();
                        done = node;
                    }
                    Frame::Object {
                        node,
                        key,
                        positions,
                    } => {
                        let node = *node;
                        let key = std::mem::take(key);
                        if let Node::Object(members) = &mut self.nodes[node] {
                            match positions.get(&key) {
                                Some(&at) => members[at].1 = done,
                                None => {
                                    positions.insert(key.clone(), members.len());
                                    members.push((key, done));
                                }
                            }
                        }
                        self.skip()?;
                        if self.eat(b',') {
                            self.skip()?;
                            if !self.eat(b'}') {
                                let next = self.key()?;
                                if let Some(Frame::Object { key, .. }) = stack.last_mut() {
                                    *key = next;
                                }
                                break;
                            }
                        } else if !self.eat(b'}') {
                            return Err(self.error("expected ',' or '}'"));
                        }
                        stack.pop();
                        done = node;
                    }
                }
            }
        }
    }
    fn scalar(&mut self) -> Result<usize, JsoncError> {
        let node = match self.peek() {
            Some(b'"') => Node::String(self.string()?),
            Some(b'-' | b'0'..=b'9') => Node::Number(self.number()?),
            _ => {
                let rest = &self.text[self.at..];
                let (node, len) = if rest.starts_with(b"true") {
                    (Node::Bool(true), 4)
                } else if rest.starts_with(b"false") {
                    (Node::Bool(false), 5)
                } else if rest.starts_with(b"null") {
                    (Node::Null, 4)
                } else {
                    return Err(self.error("expected a value"));
                };
                self.at += len;
                node
            }
        };
        Ok(self.push(node))
    }
    fn digits(&mut self) -> usize {
        let start = self.at;
        while matches!(self.peek(), Some(b'0'..=b'9')) {
            self.at += 1;
        }
        self.at - start
    }
    /// `-? (0 | [1-9][0-9]*) (. [0-9]+)? ([eE] [+-]? [0-9]+)?`
    fn number(&mut self) -> Result<String, JsoncError> {
        let start = self.at;
        self.eat(b'-');
        match self.peek() {
            Some(b'0') => self.at += 1,
            Some(b'1'..=b'9') => {
                self.digits();
            }
            _ => return Err(self.error("malformed number")),
        }
        if self.eat(b'.') && self.digits() == 0 {
            return Err(self.error("malformed number"));
        }
        if matches!(self.peek(), Some(b'e' | b'E')) {
            self.at += 1;
            if !self.eat(b'+') {
                self.eat(b'-');
            }
            if self.digits() == 0 {
                return Err(self.error("malformed number"));
            }
        }
        // The slice is ASCII digits and signs.
        Ok(String::from_utf8_lossy(&self.text[start..self.at]).into_owned())
    }
    fn hex4(&mut self) -> Result<u32, JsoncError> {
        let mut value = 0u32;
        for _ in 0..4 {
            let digit = match self.peek().map(char::from).and_then(|c| c.to_digit(16)) {
                Some(digit) => digit,
                None => return Err(self.error("malformed \\u escape")),
            };
            value = value * 16 + digit;
            self.at += 1;
        }
        Ok(value)
    }
    /// A string at the cursor. No raw character below U+0020; the RFC's
    /// escapes; a `\u` surrogate must pair (a lone surrogate is no scalar).
    fn string(&mut self) -> Result<String, JsoncError> {
        self.at += 1;
        let mut out: Vec<u8> = Vec::new();
        loop {
            match self.peek() {
                None => return Err(self.error("unterminated string")),
                Some(b'"') => {
                    self.at += 1;
                    // Only whole UTF-8 sequences and encoded scalars entered.
                    return String::from_utf8(out).map_err(|_| self.error("not UTF-8"));
                }
                Some(b'\\') => {
                    self.at += 1;
                    let simple = match self.peek() {
                        Some(b'"') => Some(b'"'),
                        Some(b'\\') => Some(b'\\'),
                        Some(b'/') => Some(b'/'),
                        Some(b'b') => Some(0x08),
                        Some(b'f') => Some(0x0c),
                        Some(b'n') => Some(b'\n'),
                        Some(b'r') => Some(b'\r'),
                        Some(b't') => Some(b'\t'),
                        Some(b'u') => None,
                        _ => return Err(self.error("malformed escape")),
                    };
                    self.at += 1;
                    if let Some(byte) = simple {
                        out.push(byte);
                        continue;
                    }
                    let high = self.hex4()?;
                    let scalar = match high {
                        0xd800..=0xdbff => {
                            if !(self.eat(b'\\') && self.eat(b'u')) {
                                return Err(self.error("lone surrogate"));
                            }
                            let low = self.hex4()?;
                            if !(0xdc00..=0xdfff).contains(&low) {
                                return Err(self.error("lone surrogate"));
                            }
                            0x10000 + ((high - 0xd800) << 10) + (low - 0xdc00)
                        }
                        0xdc00..=0xdfff => return Err(self.error("lone surrogate")),
                        _ => high,
                    };
                    match char::from_u32(scalar) {
                        Some(c) => {
                            let mut buf = [0u8; 4];
                            out.extend_from_slice(c.encode_utf8(&mut buf).as_bytes());
                        }
                        None => return Err(self.error("lone surrogate")),
                    }
                }
                Some(c) if c < 0x20 => {
                    return Err(self.error("control character in string"));
                }
                Some(c) => {
                    out.push(c);
                    self.at += 1;
                }
            }
        }
    }
}

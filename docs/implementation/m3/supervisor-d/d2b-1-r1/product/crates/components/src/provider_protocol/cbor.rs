//! M3-D r5 item 10 (unit D2b-1): the strict deterministic-CBOR reader and
//! encoder for the two provider profiles (DLV:650-656; RPP:172-199).
//!
//! The closed data model is null, false, true, unsigned integers to 2^64 - 1,
//! (under `ts2-cbor` only) negative integers to -2^63, UTF-8 NFC text, byte
//! strings, definite arrays and definite maps keyed by text, each key strictly
//! greater, bytewise, than the one before (for text keys bytewise order and
//! length-first order agree). Shortest encodings only; no tag, float, other
//! simple value or indefinite length; nothing after the single item; and the
//! decoded value must re-encode to exactly the received bytes. Refusals carry
//! the reference decoder's codes (native wire owner trial 07,
//! `tools/wirecodec.py`). The reader is iterative, with an explicit stack
//! bounded by `max_depth` (LD-D2B-2), and never allocates from a claimed
//! length: containers grow one decoded item at a time.

/// The two closed profiles.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Profile {
    /// TypeScript protocol 2: negative integers to -2^63 decode.
    Ts2,
    /// Rust protocol 3: any negative integer refuses.
    Rust3,
}

/// One decoded value.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Value {
    Null,
    Bool(bool),
    Unsigned(u64),
    /// A negative integer, `ts2-cbor` only.
    Negative(i64),
    Bytes(Vec<u8>),
    Text(String),
    Array(Vec<Value>),
    /// Members in their (strictly ascending) received order.
    Map(Vec<(String, Value)>),
}

/// The reference decoder's refusal codes, plus the depth bound.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CborRefusal {
    NonShortest,
    IndefiniteOrReserved,
    Tag,
    FloatOrSimple,
    NegativeIntegerForbidden,
    IntRange,
    InvalidUtf8,
    NonNfc,
    NonTextKey,
    DuplicateKey,
    MapOrder,
    Truncated,
    TrailingBytes,
    ReencodeMismatch,
    /// Nesting beyond the bound (LD-D2B-2).
    Depth,
}
impl CborRefusal {
    /// The reference's code.
    pub fn code(self) -> &'static str {
        match self {
            Self::NonShortest => "NON_SHORTEST",
            Self::IndefiniteOrReserved => "INDEFINITE_OR_RESERVED",
            Self::Tag => "TAG",
            Self::FloatOrSimple => "FLOAT_OR_SIMPLE",
            Self::NegativeIntegerForbidden => "NEGATIVE_INTEGER_FORBIDDEN",
            Self::IntRange => "INT_RANGE",
            Self::InvalidUtf8 => "INVALID_UTF8",
            Self::NonNfc => "NON_NFC",
            Self::NonTextKey => "NON_TEXT_KEY",
            Self::DuplicateKey => "DUPLICATE_KEY",
            Self::MapOrder => "MAP_ORDER",
            Self::Truncated => "TRUNCATED",
            Self::TrailingBytes => "TRAILING_BYTES",
            Self::ReencodeMismatch => "REENCODE_MISMATCH",
            Self::Depth => "DEPTH",
        }
    }
}

/// One decoded value's received bytes, `data[start..end]`, and the node of
/// its container. Nodes are the values in pre-order; map keys are not nodes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Span {
    pub start: usize,
    pub end: usize,
    pub parent: Option<usize>,
}

/// An open container on the reader's stack, with its node (`None` for a
/// container read as a map key, which then refuses).
enum Open {
    Array {
        node: Option<usize>,
        items: Vec<Value>,
        remaining: u64,
    },
    Map {
        node: Option<usize>,
        members: Vec<(String, Value)>,
        remaining: u64,
        /// The previous key's encoded bytes, as a range of the input.
        previous: Option<(usize, usize)>,
        /// The key just read, waiting for its value.
        key: Option<String>,
        /// Where the key being read starts.
        key_start: usize,
    },
}

/// Decode one item under `profile`, refusing every non-canonical form, with
/// nesting at most `max_depth` (the top-level item is depth 1).
pub fn decode(data: &[u8], profile: Profile, max_depth: usize) -> Result<Value, CborRefusal> {
    decode_spanned(data, profile, max_depth).map(|(value, _)| value)
}

/// [`decode`], also returning every value's received byte range (LD-D2B-3):
/// node 0 is the root, then each value in pre-order.
pub fn decode_spanned(
    data: &[u8],
    profile: Profile,
    max_depth: usize,
) -> Result<(Value, Vec<Span>), CborRefusal> {
    let mut pos = 0usize;
    let mut stack: Vec<Open> = Vec::new();
    let mut spans: Vec<Span> = Vec::new();
    let root = loop {
        // A map waiting for a key records where that key's bytes begin; a
        // key is not a node. Every other item is the next node.
        let node = match stack.last_mut() {
            Some(Open::Map {
                key: None,
                key_start,
                ..
            }) => {
                *key_start = pos;
                None
            }
            top => {
                let parent = match top {
                    Some(Open::Array { node, .. } | Open::Map { node, .. }) => *node,
                    None => None,
                };
                spans.push(Span {
                    start: pos,
                    end: pos,
                    parent,
                });
                Some(spans.len() - 1)
            }
        };
        let ib = *data.get(pos).ok_or(CborRefusal::Truncated)?;
        pos += 1;
        let (major, ai) = (ib >> 5, ib & 31);
        let mut value = match major {
            7 => match ai {
                20 => Value::Bool(false),
                21 => Value::Bool(true),
                22 => Value::Null,
                _ => return Err(CborRefusal::FloatOrSimple),
            },
            6 => return Err(CborRefusal::Tag),
            _ => {
                let n = argument(data, &mut pos, ai)?;
                match major {
                    0 => Value::Unsigned(n),
                    1 => {
                        if profile == Profile::Rust3 {
                            return Err(CborRefusal::NegativeIntegerForbidden);
                        }
                        if n > i64::MAX as u64 {
                            return Err(CborRefusal::IntRange);
                        }
                        Value::Negative(-1 - n as i64)
                    }
                    2 | 3 => {
                        let len = usize::try_from(n).map_err(|_| CborRefusal::Truncated)?;
                        let end = pos.checked_add(len).ok_or(CborRefusal::Truncated)?;
                        let raw = data.get(pos..end).ok_or(CborRefusal::Truncated)?;
                        pos = end;
                        if major == 2 {
                            Value::Bytes(raw.to_vec())
                        } else {
                            let text =
                                std::str::from_utf8(raw).map_err(|_| CborRefusal::InvalidUtf8)?;
                            if !opensip_identity::is_nfc(text) {
                                return Err(CborRefusal::NonNfc);
                            }
                            Value::Text(text.to_owned())
                        }
                    }
                    4 | 5 => {
                        if stack.len() + 1 > max_depth {
                            return Err(CborRefusal::Depth);
                        }
                        if n == 0 {
                            if major == 4 {
                                Value::Array(Vec::new())
                            } else {
                                Value::Map(Vec::new())
                            }
                        } else {
                            stack.push(if major == 4 {
                                Open::Array {
                                    node,
                                    items: Vec::new(),
                                    remaining: n,
                                }
                            } else {
                                Open::Map {
                                    node,
                                    members: Vec::new(),
                                    remaining: n,
                                    previous: None,
                                    key: None,
                                    key_start: pos,
                                }
                            });
                            continue;
                        }
                    }
                    _ => unreachable!("major types are three bits"),
                }
            }
        };
        if let Some(node) = node {
            spans[node].end = pos;
        }
        // Deliver the finished value to its container, closing every
        // container it completes; the root is the value that empties the
        // stack.
        let finished = loop {
            let Some(top) = stack.last_mut() else {
                break Some(value);
            };
            match top {
                Open::Array {
                    items, remaining, ..
                } => {
                    items.push(value);
                    *remaining -= 1;
                    if *remaining > 0 {
                        break None;
                    }
                }
                Open::Map {
                    members,
                    remaining,
                    previous,
                    key,
                    key_start,
                    ..
                } => match key.take() {
                    None => {
                        let Value::Text(text) = value else {
                            return Err(CborRefusal::NonTextKey);
                        };
                        let raw = &data[*key_start..pos];
                        if let Some((start, end)) = *previous {
                            let prior = &data[start..end];
                            if raw <= prior {
                                return Err(if raw == prior {
                                    CborRefusal::DuplicateKey
                                } else {
                                    CborRefusal::MapOrder
                                });
                            }
                        }
                        *previous = Some((*key_start, pos));
                        *key = Some(text);
                        break None;
                    }
                    Some(name) => {
                        members.push((name, value));
                        *remaining -= 1;
                        if *remaining > 0 {
                            break None;
                        }
                    }
                },
            }
            let (closed, node) = match stack.pop().expect("a completed container") {
                Open::Array { items, node, .. } => (Value::Array(items), node),
                Open::Map { members, node, .. } => (Value::Map(members), node),
            };
            if let Some(node) = node {
                spans[node].end = pos;
            }
            value = closed;
        };
        if let Some(root) = finished {
            break root;
        }
    };
    if pos != data.len() {
        return Err(CborRefusal::TrailingBytes);
    }
    if encode(&root) != data {
        return Err(CborRefusal::ReencodeMismatch);
    }
    Ok((root, spans))
}

/// An integer or length argument, refusing non-shortest forms and the
/// reserved and indefinite additional-information values.
fn argument(data: &[u8], pos: &mut usize, ai: u8) -> Result<u64, CborRefusal> {
    if ai < 24 {
        return Ok(ai as u64);
    }
    if ai > 27 {
        return Err(CborRefusal::IndefiniteOrReserved);
    }
    let size = 1usize << (ai - 24);
    let end = pos.checked_add(size).ok_or(CborRefusal::Truncated)?;
    let raw = data.get(*pos..end).ok_or(CborRefusal::Truncated)?;
    *pos = end;
    let n = raw.iter().fold(0u64, |n, b| (n << 8) | *b as u64);
    let shortest = if ai == 24 {
        n >= 24
    } else {
        n >= 1u64 << (8 * (size / 2))
    };
    if !shortest {
        return Err(CborRefusal::NonShortest);
    }
    Ok(n)
}

pub(crate) fn head(out: &mut Vec<u8>, major: u8, n: u64) {
    let m = major << 5;
    if n < 24 {
        out.push(m | n as u8);
    } else if n < 1 << 8 {
        out.push(m | 24);
        out.push(n as u8);
    } else if n < 1 << 16 {
        out.push(m | 25);
        out.extend_from_slice(&(n as u16).to_be_bytes());
    } else if n < 1 << 32 {
        out.push(m | 26);
        out.extend_from_slice(&(n as u32).to_be_bytes());
    } else {
        out.push(m | 27);
        out.extend_from_slice(&n.to_be_bytes());
    }
}

/// The deterministic encoding: shortest heads, and map members sorted
/// bytewise by their encoded keys.
pub fn encode(value: &Value) -> Vec<u8> {
    let mut out = Vec::new();
    // Iterative: a stack of values still to write.
    enum Item<'a> {
        Value(&'a Value),
        Raw(Vec<u8>),
    }
    let mut pending = vec![Item::Value(value)];
    while let Some(item) = pending.pop() {
        let v = match item {
            Item::Raw(bytes) => {
                out.extend_from_slice(&bytes);
                continue;
            }
            Item::Value(v) => v,
        };
        match v {
            Value::Null => out.push(0xf6),
            Value::Bool(true) => out.push(0xf5),
            Value::Bool(false) => out.push(0xf4),
            Value::Unsigned(n) => head(&mut out, 0, *n),
            Value::Negative(n) => head(&mut out, 1, (-1 - *n) as u64),
            Value::Bytes(b) => {
                head(&mut out, 2, b.len() as u64);
                out.extend_from_slice(b);
            }
            Value::Text(t) => {
                head(&mut out, 3, t.len() as u64);
                out.extend_from_slice(t.as_bytes());
            }
            Value::Array(items) => {
                head(&mut out, 4, items.len() as u64);
                pending.extend(items.iter().rev().map(Item::Value));
            }
            Value::Map(members) => {
                head(&mut out, 5, members.len() as u64);
                let mut keyed: Vec<(Vec<u8>, &Value)> = members
                    .iter()
                    .map(|(k, v)| {
                        let mut key = Vec::new();
                        head(&mut key, 3, k.len() as u64);
                        key.extend_from_slice(k.as_bytes());
                        (key, v)
                    })
                    .collect();
                keyed.sort_by(|a, b| a.0.cmp(&b.0));
                for (key, v) in keyed.into_iter().rev() {
                    pending.push(Item::Value(v));
                    pending.push(Item::Raw(key));
                }
            }
        }
    }
    out
}

#[cfg(test)]
#[path = "cbor_tests.rs"]
mod tests;

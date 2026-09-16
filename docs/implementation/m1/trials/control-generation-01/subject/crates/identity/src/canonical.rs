//! Product JSON profile: exact integers, scalar Unicode and bounded containers.
use alloc::{collections::BTreeMap, string::String, vec::Vec};
use core::fmt::{self, Write};

pub const MAX_BYTES: usize = 4 * 1024 * 1024;
pub const MAX_DEPTH: usize = 32;
pub const MIN_INTEGER: i128 = -(1_i128 << 63);
pub const MAX_INTEGER: i128 = (1_i128 << 64) - 1;

/// An exact admitted profile integer. Schema-specific narrower bounds follow.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct Integer(i128);

impl Integer {
    pub fn new(value: i128) -> Result<Self, Error> {
        if (MIN_INTEGER..=MAX_INTEGER).contains(&value) {
            Ok(Self(value))
        } else {
            Err(Error::IntegerRange)
        }
    }

    pub fn get(self) -> i128 {
        self.0
    }
}

/// An inert exact JSON value. Constructing one is not schema or Run admission.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Value {
    Null,
    Bool(bool),
    Integer(Integer),
    String(String),
    Array(Vec<Value>),
    Object(BTreeMap<String, Value>),
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Error {
    ByteLimit,
    DepthLimit,
    InvalidUtf8,
    InvalidJson,
    InvalidUnicode,
    DuplicateKey,
    NegativeZero,
    IntegerRange,
    FloatForbidden,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{self:?}")
    }
}

impl core::error::Error for Error {}

/// Reject lexical violations before any lossy deserialization can occur.
pub fn parse(raw: &[u8]) -> Result<Value, Error> {
    if raw.len() > MAX_BYTES {
        return Err(Error::ByteLimit);
    }
    core::str::from_utf8(raw).map_err(|_| Error::InvalidUtf8)?;
    let mut parser = Parser { raw, pos: 0 };
    let value = parser.value(0)?;
    parser.whitespace();
    if parser.pos != raw.len() {
        return Err(Error::InvalidJson);
    }
    Ok(value)
}

struct Parser<'a> {
    raw: &'a [u8],
    pos: usize,
}

impl Parser<'_> {
    fn whitespace(&mut self) {
        while matches!(self.raw.get(self.pos), Some(b' ' | b'\n' | b'\r' | b'\t')) {
            self.pos += 1;
        }
    }

    fn consume(&mut self, byte: u8) -> bool {
        if self.raw.get(self.pos) == Some(&byte) {
            self.pos += 1;
            true
        } else {
            false
        }
    }

    fn value(&mut self, containers: usize) -> Result<Value, Error> {
        self.whitespace();
        match self.raw.get(self.pos).copied() {
            Some(b'n') => self.literal(b"null", Value::Null),
            Some(b't') => self.literal(b"true", Value::Bool(true)),
            Some(b'f') => self.literal(b"false", Value::Bool(false)),
            Some(b'"') => self.string().map(Value::String),
            Some(b'-' | b'0'..=b'9') => self.integer().map(Value::Integer),
            Some(b'[' | b'{') if containers == MAX_DEPTH => Err(Error::DepthLimit),
            Some(b'[') => self.array(containers + 1),
            Some(b'{') => self.object(containers + 1),
            _ => Err(Error::InvalidJson),
        }
    }

    fn literal(&mut self, text: &[u8], value: Value) -> Result<Value, Error> {
        if self.raw[self.pos..].starts_with(text) {
            self.pos += text.len();
            Ok(value)
        } else {
            Err(Error::InvalidJson)
        }
    }

    fn integer(&mut self) -> Result<Integer, Error> {
        let start = self.pos;
        let negative = self.consume(b'-');
        if self.consume(b'0') {
            if self.raw.get(self.pos).is_some_and(u8::is_ascii_digit) {
                return Err(Error::InvalidJson);
            }
        } else {
            if !matches!(self.raw.get(self.pos), Some(b'1'..=b'9')) {
                return Err(Error::InvalidJson);
            }
            while self.raw.get(self.pos).is_some_and(u8::is_ascii_digit) {
                self.pos += 1;
            }
        }
        if matches!(self.raw.get(self.pos), Some(b'.' | b'e' | b'E')) {
            return Err(Error::FloatForbidden);
        }
        if negative && &self.raw[start..self.pos] == b"-0" {
            return Err(Error::NegativeZero);
        }
        // UTF-8 was checked at entry, and this range contains only ASCII digits.
        let token =
            core::str::from_utf8(&self.raw[start..self.pos]).map_err(|_| Error::InvalidJson)?;
        Integer::new(token.parse::<i128>().map_err(|_| Error::IntegerRange)?)
    }

    fn string(&mut self) -> Result<String, Error> {
        if !self.consume(b'"') {
            return Err(Error::InvalidJson);
        }
        let mut result = String::new();
        let mut chunk = self.pos;
        loop {
            let byte = *self.raw.get(self.pos).ok_or(Error::InvalidJson)?;
            if byte == b'"' || byte == b'\\' {
                result.push_str(
                    core::str::from_utf8(&self.raw[chunk..self.pos])
                        .map_err(|_| Error::InvalidUtf8)?,
                );
                self.pos += 1;
                if byte == b'"' {
                    return Ok(result);
                }
                let escaped = *self.raw.get(self.pos).ok_or(Error::InvalidJson)?;
                self.pos += 1;
                match escaped {
                    b'"' => result.push('"'),
                    b'\\' => result.push('\\'),
                    b'/' => result.push('/'),
                    b'b' => result.push('\u{8}'),
                    b'f' => result.push('\u{c}'),
                    b'n' => result.push('\n'),
                    b'r' => result.push('\r'),
                    b't' => result.push('\t'),
                    b'u' => {
                        let high = self.hex4()?;
                        let scalar = if (0xd800..=0xdbff).contains(&high) {
                            if !self.consume(b'\\') || !self.consume(b'u') {
                                return Err(Error::InvalidUnicode);
                            }
                            let low = self.hex4()?;
                            if !(0xdc00..=0xdfff).contains(&low) {
                                return Err(Error::InvalidUnicode);
                            }
                            0x10000 + ((u32::from(high) - 0xd800) << 10) + u32::from(low) - 0xdc00
                        } else {
                            u32::from(high)
                        };
                        result.push(char::from_u32(scalar).ok_or(Error::InvalidUnicode)?);
                    }
                    _ => return Err(Error::InvalidJson),
                }
                chunk = self.pos;
            } else if byte < 0x20 {
                return Err(Error::InvalidJson);
            } else {
                self.pos += 1;
            }
        }
    }

    fn hex4(&mut self) -> Result<u16, Error> {
        let mut value = 0_u16;
        for _ in 0..4 {
            let byte = *self.raw.get(self.pos).ok_or(Error::InvalidJson)?;
            self.pos += 1;
            let digit = match byte {
                b'0'..=b'9' => byte - b'0',
                b'a'..=b'f' => byte - b'a' + 10,
                b'A'..=b'F' => byte - b'A' + 10,
                _ => return Err(Error::InvalidJson),
            };
            value = value * 16 + u16::from(digit);
        }
        Ok(value)
    }

    fn array(&mut self, containers: usize) -> Result<Value, Error> {
        self.pos += 1;
        self.whitespace();
        let mut items = Vec::new();
        if self.consume(b']') {
            return Ok(Value::Array(items));
        }
        loop {
            items.push(self.value(containers)?);
            self.whitespace();
            if self.consume(b']') {
                return Ok(Value::Array(items));
            }
            if !self.consume(b',') {
                return Err(Error::InvalidJson);
            }
        }
    }

    fn object(&mut self, containers: usize) -> Result<Value, Error> {
        self.pos += 1;
        self.whitespace();
        let mut items = BTreeMap::new();
        if self.consume(b'}') {
            return Ok(Value::Object(items));
        }
        loop {
            self.whitespace();
            let key = self.string()?;
            if items.contains_key(&key) {
                return Err(Error::DuplicateKey);
            }
            self.whitespace();
            if !self.consume(b':') {
                return Err(Error::InvalidJson);
            }
            items.insert(key, self.value(containers)?);
            self.whitespace();
            if self.consume(b'}') {
                return Ok(Value::Object(items));
            }
            if !self.consume(b',') {
                return Err(Error::InvalidJson);
            }
        }
    }
}

/// Encode C(X), preserving array order and validating programmatic inputs too.
pub fn encode(value: &Value) -> Result<Vec<u8>, Error> {
    let mut encoder = Encoder { bytes: Vec::new() };
    encoder.value(value, 0)?;
    Ok(encoder.bytes)
}

struct Encoder {
    bytes: Vec<u8>,
}

impl Encoder {
    fn append(&mut self, raw: &[u8]) -> Result<(), Error> {
        if raw.len() > MAX_BYTES - self.bytes.len() {
            return Err(Error::ByteLimit);
        }
        self.bytes.extend_from_slice(raw);
        Ok(())
    }

    fn string(&mut self, value: &str) -> Result<(), Error> {
        self.append(b"\"")?;
        for scalar in value.chars() {
            match scalar {
                '"' => self.append(b"\\\"")?,
                '\\' => self.append(b"\\\\")?,
                '\u{8}' => self.append(b"\\b")?,
                '\u{c}' => self.append(b"\\f")?,
                '\n' => self.append(b"\\n")?,
                '\r' => self.append(b"\\r")?,
                '\t' => self.append(b"\\t")?,
                '\0'..='\u{1f}' => {
                    const HEX: &[u8] = b"0123456789abcdef";
                    let byte = scalar as u8;
                    self.append(&[
                        b'\\',
                        b'u',
                        b'0',
                        b'0',
                        HEX[usize::from(byte >> 4)],
                        HEX[usize::from(byte & 15)],
                    ])?;
                }
                _ => self.append(scalar.encode_utf8(&mut [0; 4]).as_bytes())?,
            }
        }
        self.append(b"\"")
    }

    fn value(&mut self, value: &Value, containers: usize) -> Result<(), Error> {
        match value {
            Value::Null => self.append(b"null"),
            Value::Bool(true) => self.append(b"true"),
            Value::Bool(false) => self.append(b"false"),
            Value::Integer(number) => {
                let mut decimal = String::new();
                write!(decimal, "{}", number.get()).map_err(|_| Error::InvalidJson)?;
                self.append(decimal.as_bytes())
            }
            Value::String(value) => self.string(value),
            Value::Array(_) | Value::Object(_) if containers == MAX_DEPTH => Err(Error::DepthLimit),
            Value::Array(values) => {
                self.append(b"[")?;
                for (index, value) in values.iter().enumerate() {
                    if index != 0 {
                        self.append(b",")?;
                    }
                    self.value(value, containers + 1)?;
                }
                self.append(b"]")
            }
            Value::Object(values) => {
                self.append(b"{")?;
                // Rust String ordering is lexical UTF-8 byte ordering.
                for (index, (key, value)) in values.iter().enumerate() {
                    if index != 0 {
                        self.append(b",")?;
                    }
                    self.string(key)?;
                    self.append(b":")?;
                    self.value(value, containers + 1)?;
                }
                self.append(b"}")
            }
        }
    }
}

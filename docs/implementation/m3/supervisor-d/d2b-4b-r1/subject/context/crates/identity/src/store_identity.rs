//! Pure private store-instance spelling; no native existence or authority.
use alloc::string::String;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Error;
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct StoreInstance(String);
impl StoreInstance {
    pub fn parse(value: &str) -> Result<Self, Error> {
        if value.len() != 32
            || !value
                .bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
        {
            return Err(Error);
        }
        Ok(Self(value.into()))
    }
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

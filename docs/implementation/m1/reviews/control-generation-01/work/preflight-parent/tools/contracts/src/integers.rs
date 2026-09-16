/// Exact JSON integer domain [-2^63, 2^64-1], including mixed signed ranges.
/// Construction from the two wire primitives preserves one numeric value.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub struct ExactInteger(i128);
impl ExactInteger {
    pub fn as_i128(self) -> i128 { self.0 }
}
impl From<i64> for ExactInteger {
    fn from(value: i64) -> Self { Self(i128::from(value)) }
}
impl From<u64> for ExactInteger {
    fn from(value: u64) -> Self { Self(i128::from(value)) }
}
impl ::std::fmt::Display for ExactInteger {
    fn fmt(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
        self.0.fmt(f)
    }
}
impl ::serde::Serialize for ExactInteger {
    fn serialize<S: ::serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        if self.0 < 0 { serializer.serialize_i64(self.0 as i64) }
        else { serializer.serialize_u64(self.0 as u64) }
    }
}
impl<'de> ::serde::Deserialize<'de> for ExactInteger {
    fn deserialize<D: ::serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Visitor;
        impl<'de> ::serde::de::Visitor<'de> for Visitor {
            type Value = ExactInteger;
            fn expecting(&self, f: &mut ::std::fmt::Formatter<'_>) -> ::std::fmt::Result {
                f.write_str("an exact integer in [-2^63, 2^64-1]")
            }
            fn visit_i64<E: ::serde::de::Error>(self, value: i64) -> Result<Self::Value, E> {
                Ok(ExactInteger::from(value))
            }
            fn visit_u64<E: ::serde::de::Error>(self, value: u64) -> Result<Self::Value, E> {
                Ok(ExactInteger::from(value))
            }
        }
        deserializer.deserialize_any(Visitor)
    }
}

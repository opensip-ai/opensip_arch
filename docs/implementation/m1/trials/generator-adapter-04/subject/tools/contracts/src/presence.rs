/// Wire field presence is distinct from a present null, empty array or object.
/// This inert carrier helper does not admit a value under its schema.
#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub enum FieldPresence<T> {
    Missing,
    Present(T),
}
impl<T> Default for FieldPresence<T> {
    fn default() -> Self { Self::Missing }
}
impl<T> FieldPresence<T> {
    pub fn is_missing(&self) -> bool { matches!(self, Self::Missing) }
}
impl<T: ::serde::Serialize> ::serde::Serialize for FieldPresence<T> {
    fn serialize<S: ::serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        match self {
            Self::Present(value) => value.serialize(serializer),
            Self::Missing => Err(::serde::ser::Error::custom("missing field must be omitted by its containing object")),
        }
    }
}
impl<'de, T: ::serde::Deserialize<'de>> ::serde::Deserialize<'de> for FieldPresence<T> {
    fn deserialize<D: ::serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        T::deserialize(deserializer).map(Self::Present)
    }
}

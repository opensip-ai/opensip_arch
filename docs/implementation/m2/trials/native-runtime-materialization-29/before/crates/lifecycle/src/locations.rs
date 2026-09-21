//! Private syntactic location components for the proposed physical-layout owner201 (199 F-1 correction).
//! Parsing names neither admits a registry/store binding nor acquires custody or a
//! lease. Only future host admission may combine these with retained handles.
use std::path::PathBuf;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) enum NameError {
    Namespace,
    StoreInstance,
    Execution,
    GrantGeneration,
}
fn lower_hex(s: &str, n: usize) -> bool {
    s.len() == n
        && s.bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}
#[derive(Debug, Clone, PartialEq, Eq)]
struct NamespaceComponent(String);
impl NamespaceComponent {
    fn parse(s: &str) -> Result<Self, NameError> {
        let b = s.as_bytes();
        if b.len() != 36
            || b[14] != b'4'
            || !matches!(b[19], b'8' | b'9' | b'a' | b'b')
            || !b.iter().enumerate().all(|(i, b)| {
                if [8, 13, 18, 23].contains(&i) {
                    *b == b'-'
                } else {
                    b.is_ascii_digit() || (b'a'..=b'f').contains(b)
                }
            })
        {
            return Err(NameError::Namespace);
        }
        Ok(Self(s.into()))
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub(super) struct StoreComponent(String);
impl StoreComponent {
    pub(super) fn parse(s: &str) -> Result<Self, NameError> {
        if lower_hex(s, 32) {
            Ok(Self(s.into()))
        } else {
            Err(NameError::StoreInstance)
        }
    }
    pub(super) fn as_str(&self) -> &str {
        &self.0
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
struct ExecutionComponent(String);
impl ExecutionComponent {
    fn parse(s: &str) -> Result<Self, NameError> {
        if s.strip_prefix("exec1_").is_some_and(|s| lower_hex(s, 32)) {
            Ok(Self(s.into()))
        } else {
            Err(NameError::Execution)
        }
    }
    fn staging_relative(&self) -> PathBuf {
        PathBuf::from("stores").join(".staging").join(&self.0)
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct GrantGenerationComponent(i64);
impl GrantGenerationComponent {
    fn parse(s: &str) -> Result<Self, NameError> {
        if s.is_empty()
            || s.len() > 19
            || s.as_bytes()[0] == b'0'
            || !s.bytes().all(|b| b.is_ascii_digit())
        {
            return Err(NameError::GrantGeneration);
        }
        let value = s.parse::<i64>().map_err(|_| NameError::GrantGeneration)?;
        if value <= 0 {
            return Err(NameError::GrantGeneration);
        }
        Ok(Self(value))
    }
}
/// Namespace-relative names do not require any store selection. These are
/// syntactic components, not admitted registry/custody/lease capabilities.
struct NamespaceNames {
    namespace: NamespaceComponent,
}
impl NamespaceNames {
    fn new(namespace: NamespaceComponent) -> Self {
        Self { namespace }
    }
    fn in_store<'a>(&'a self, store: &'a StoreNames) -> LedgerNames<'a> {
        LedgerNames {
            namespace: self,
            store,
        }
    }
    fn namespace_relative(&self) -> PathBuf {
        PathBuf::from("host")
            .join("projects")
            .join(&self.namespace.0)
    }
    fn writer_lease_relative(&self) -> PathBuf {
        self.namespace_relative().join("writer.lease")
    }
    fn readers_lease_relative(&self) -> PathBuf {
        self.namespace_relative().join("readers.lease")
    }
    fn journal_relative(&self) -> PathBuf {
        self.namespace_relative().join("grant-journal.sqlite")
    }
    fn journal_wal_relative(&self) -> PathBuf {
        self.namespace_relative().join("grant-journal.sqlite-wal")
    }
    fn journal_shm_relative(&self) -> PathBuf {
        self.namespace_relative().join("grant-journal.sqlite-shm")
    }
    fn witness_relative(&self) -> PathBuf {
        self.namespace_relative().join("grant-journal.witness")
    }
    fn floor_relative(&self, generation: GrantGenerationComponent) -> PathBuf {
        PathBuf::from("trust")
            .join("journal-floors")
            .join(&self.namespace.0)
            .join(format!("{}.floor", generation.0))
    }
}
/// Store-relative names do not require a namespace or imply marker admission.
struct StoreNames {
    store: StoreComponent,
}
impl StoreNames {
    fn new(store: StoreComponent) -> Self {
        Self { store }
    }
    fn store_relative(&self) -> PathBuf {
        PathBuf::from("stores").join(&self.store.0)
    }
    fn marker_relative(&self) -> PathBuf {
        self.store_relative().join("store-instance.v1")
    }
}
/// Both legs are borrowed from one explicit syntactic pairing. No method accepts
/// an independent namespace override. The lifetime is ordinary Rust borrowing,
/// not an operation lease: a future sealed host context must establish admission
/// and retain the required custody and leases through the consuming operation.
struct LedgerNames<'a> {
    namespace: &'a NamespaceNames,
    store: &'a StoreNames,
}
impl LedgerNames<'_> {
    fn ledger_relative(&self) -> PathBuf {
        self.store
            .store_relative()
            .join("projects")
            .join(&self.namespace.namespace.0)
            .join("ledger.sqlite")
    }
    fn ledger_wal_relative(&self) -> PathBuf {
        self.store
            .store_relative()
            .join("projects")
            .join(&self.namespace.namespace.0)
            .join("ledger.sqlite-wal")
    }
    fn ledger_shm_relative(&self) -> PathBuf {
        self.store
            .store_relative()
            .join("projects")
            .join(&self.namespace.namespace.0)
            .join("ledger.sqlite-shm")
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Component;
    const N: &str = "12345678-1234-4abc-8def-123456789abc";
    fn namespace(n: &str) -> NamespaceNames {
        NamespaceNames::new(NamespaceComponent::parse(n).unwrap())
    }
    fn store(s: &str) -> StoreNames {
        StoreNames::new(StoreComponent::parse(s).unwrap())
    }
    #[test]
    fn component_grammars_refuse_aliases_separators_and_out_of_range_values() {
        for variant in ['8', '9', 'a', 'b'] {
            let mut s = N.to_owned();
            s.replace_range(19..20, &variant.to_string());
            assert!(NamespaceComponent::parse(&s).is_ok());
        }
        for s in [
            N.to_uppercase(),
            N.replace("-4abc-", "-5abc-"),
            N.replace("-8def-", "-cdef-"),
            N.replace('-', "/"),
            format!("{N}\n"),
            format!("/{N}"),
            format!("{N}/.."),
            format!("{N}\0"),
            "é".repeat(18),
        ] {
            assert_eq!(
                NamespaceComponent::parse(&s),
                Err(NameError::Namespace),
                "{s:?}"
            );
        }
        for s in [
            "".to_owned(),
            "a".repeat(31),
            "a".repeat(33),
            "A".repeat(32),
            "g".repeat(32),
            format!("{}\0", "a".repeat(31)),
            "../".repeat(10),
            "%2f".repeat(10),
            "é".repeat(16),
        ] {
            assert!(StoreComponent::parse(&s).is_err());
            assert!(ExecutionComponent::parse(&format!("exec1_{s}")).is_err());
        }
        assert!(StoreComponent::parse(&"0".repeat(32)).is_ok());
        for s in [
            "0",
            "00",
            "01",
            "+1",
            "-1",
            " 1",
            "1 ",
            "1\n",
            "1\0",
            "1/2",
            "1\\2",
            "9223372036854775808",
            "99999999999999999999",
            "١",
        ] {
            assert_eq!(
                GrantGenerationComponent::parse(s),
                Err(NameError::GrantGeneration),
                "{s:?}"
            );
        }
        for s in ["1", "9", "10", "9223372036854775807"] {
            assert_eq!(GrantGenerationComponent::parse(s).unwrap().0.to_string(), s);
        }
        for s in ["1_", "EXEC1_", "exec2_", ""] {
            assert!(ExecutionComponent::parse(&format!("{s}{}", "a".repeat(32))).is_err());
        }
    }
    #[test]
    fn all_roles_have_exact_bounded_relative_spellings() {
        let s = "a".repeat(32);
        let n = namespace(N);
        let selected = store(&s);
        let ledger = n.in_store(&selected);
        let g = GrantGenerationComponent::parse("9223372036854775807").unwrap();
        let namespace = format!("host/projects/{N}");
        let store = format!("stores/{s}");
        let rows = [
            (n.namespace_relative(), namespace.clone()),
            (
                n.writer_lease_relative(),
                format!("{namespace}/writer.lease"),
            ),
            (
                n.readers_lease_relative(),
                format!("{namespace}/readers.lease"),
            ),
            (
                n.journal_relative(),
                format!("{namespace}/grant-journal.sqlite"),
            ),
            (
                n.journal_wal_relative(),
                format!("{namespace}/grant-journal.sqlite-wal"),
            ),
            (
                n.journal_shm_relative(),
                format!("{namespace}/grant-journal.sqlite-shm"),
            ),
            (
                n.witness_relative(),
                format!("{namespace}/grant-journal.witness"),
            ),
            (
                n.floor_relative(g),
                format!("trust/journal-floors/{N}/9223372036854775807.floor"),
            ),
            (selected.store_relative(), store.clone()),
            (
                selected.marker_relative(),
                format!("{store}/store-instance.v1"),
            ),
            (
                ledger.ledger_relative(),
                format!("{store}/projects/{N}/ledger.sqlite"),
            ),
            (
                ledger.ledger_wal_relative(),
                format!("{store}/projects/{N}/ledger.sqlite-wal"),
            ),
            (
                ledger.ledger_shm_relative(),
                format!("{store}/projects/{N}/ledger.sqlite-shm"),
            ),
        ];
        for (path, want) in rows {
            assert_eq!(path.to_str(), Some(want.as_str()));
            assert!(!path.is_absolute());
            assert!(path.components().all(|c| matches!(c, Component::Normal(_))));
        }
        let e = ExecutionComponent::parse(&format!("exec1_{}", "b".repeat(32))).unwrap();
        assert_eq!(
            e.staging_relative(),
            PathBuf::from(format!("stores/.staging/exec1_{}", "b".repeat(32)))
        );
    }
    #[test]
    fn independent_scopes_and_borrowed_pair_preserve_namespace_and_store_isolation() {
        let n = namespace(N);
        let other = namespace("12345678-1234-4abc-8def-123456789abd");
        let a = store(&"a".repeat(32));
        let b = store(&"b".repeat(32));
        let g = GrantGenerationComponent::parse("1").unwrap();
        // No store is needed for namespace roles; no namespace is needed for
        // store roles. Pairing does not alter either independent owner.
        let before = [
            n.writer_lease_relative(),
            n.readers_lease_relative(),
            n.journal_relative(),
            n.witness_relative(),
            n.floor_relative(g),
        ];
        let markers = [a.marker_relative(), b.marker_relative()];
        let na = n.in_store(&a);
        let nb = n.in_store(&b);
        let other_a = other.in_store(&a);
        assert_ne!(na.ledger_relative(), nb.ledger_relative());
        assert_ne!(na.ledger_relative(), other_a.ledger_relative());
        assert_ne!(na.ledger_wal_relative(), nb.ledger_wal_relative());
        assert_ne!(na.ledger_shm_relative(), other_a.ledger_shm_relative());
        assert!(na.ledger_relative().starts_with(a.store_relative()));
        assert!(nb.ledger_relative().starts_with(b.store_relative()));
        assert_eq!(
            before,
            [
                n.writer_lease_relative(),
                n.readers_lease_relative(),
                n.journal_relative(),
                n.witness_relative(),
                n.floor_relative(g)
            ]
        );
        assert_eq!(markers, [a.marker_relative(), b.marker_relative()]);
        assert_ne!(n.namespace_relative(), other.namespace_relative());
        assert_ne!(n.journal_relative(), other.journal_relative());
        assert_ne!(n.floor_relative(g), other.floor_relative(g));
        assert_ne!(
            n.floor_relative(g),
            n.floor_relative(GrantGenerationComponent::parse("2").unwrap())
        );
        assert!(!n.floor_relative(g).starts_with(n.namespace_relative()));
        assert!(!n.floor_relative(g).starts_with(a.store_relative()));
        assert!(n.floor_relative(g).starts_with("trust/journal-floors"));
    }
}

//! The one registry (S-OP-2 items 1 to 3; M3-O1 item 16).
//!
//! `code_tables!` and `event!` are not exported. Tables here are the ones
//! whose members the accepted laws name in full. O1-D1 r2 supplies Platform,
//! BuildProfile and IoErrorKind. ComponentRole remains with its emitting owner.

use super::super::constants::{HEADER_RESERVE, Level, MAX_FIELDS, MAX_LINE};
use super::{
    Bytes, Code, Count, Counts, Elapsed, Errno, Flag, Form, PrivacyClass, ProcessId, Reduced,
    RegisteredCode, SafeField, Version,
};

mod code_seal {
    pub trait Sealed {}
}

/// A registration witness whose only constructor belongs to this module.
/// Public metadata can name the witness, but cannot construct or adapt it.
pub struct TableRegistration<E> {
    _registered: std::marker::PhantomData<fn() -> E>,
}
impl<E> TableRegistration<E> {
    fn new() -> Self {
        Self {
            _registered: std::marker::PhantomData,
        }
    }
}

pub trait CodeEnum: Copy + code_seal::Sealed {
    const TEXT: &'static [&'static str];
    const CAP: usize;
    fn index(self) -> u16;
    fn registration() -> TableRegistration<Self>;
}

const fn eq(left: &[u8], right: &[u8]) -> bool {
    if left.len() != right.len() {
        return false;
    }
    let mut index = 0;
    while index < left.len() {
        if left[index] != right[index] {
            return false;
        }
        index += 1;
    }
    true
}

/// K1 member grammar: `[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}`, and the table's own cap.
const fn member_ok(text: &str, cap: usize) -> bool {
    let bytes = text.as_bytes();
    if bytes.is_empty() || bytes.len() > cap || bytes.len() > 64 {
        return false;
    }
    let first = bytes[0];
    if !first.is_ascii_alphanumeric() {
        return false;
    }
    let mut index = 1;
    while index < bytes.len() {
        let byte = bytes[index];
        if !(byte.is_ascii_alphanumeric()
            || byte == b'_'
            || byte == b'.'
            || byte == b':'
            || byte == b'-')
        {
            return false;
        }
        index += 1;
    }
    true
}

const fn members_ok(text: &[&str], cap: usize) -> bool {
    if text.is_empty() {
        return false;
    }
    let mut index = 0;
    while index < text.len() {
        if !member_ok(text[index], cap) {
            return false;
        }
        let mut earlier = 0;
        while earlier < index {
            if eq(text[index].as_bytes(), text[earlier].as_bytes()) {
                return false;
            }
            earlier += 1;
        }
        index += 1;
    }
    true
}

const fn is_lower_alnum(byte: u8) -> bool {
    byte.is_ascii_lowercase() || byte.is_ascii_digit()
}

/// A name segment is `[a-z][a-z0-9]*(_[a-z0-9]+)*`, at most
/// 32 bytes. Range indexing is not stable const on this toolchain.
const fn segment_at(bytes: &[u8], start: usize, end: usize) -> bool {
    let len = end - start;
    if len == 0 || len > 32 || !bytes[start].is_ascii_lowercase() {
        return false;
    }
    let mut index = start + 1;
    while index < end {
        let byte = bytes[index];
        if byte == b'_' {
            index += 1;
            if index >= end || !is_lower_alnum(bytes[index]) {
                return false;
            }
            index += 1;
            while index < end && is_lower_alnum(bytes[index]) {
                index += 1;
            }
        } else if is_lower_alnum(byte) {
            index += 1;
        } else {
            return false;
        }
    }
    true
}

const fn eq_at(bytes: &[u8], start: usize, end: usize, right: &[u8]) -> bool {
    let len = end - start;
    if len != right.len() {
        return false;
    }
    let mut index = 0;
    while index < len {
        if bytes[start + index] != right[index] {
            return false;
        }
        index += 1;
    }
    true
}

const DOMAINS: [&str; 13] = [
    "host",
    "config",
    "discovery",
    "snapshot",
    "plan",
    "supervision",
    "provider",
    "evaluation",
    "storage",
    "delivery",
    "doctor",
    "log",
    // M3-D r5 item 21's tool class (:692); an ordinary registration
    // (SOP2 item 3, "a domain"), unit D3a-3.
    "tool",
];

/// Exactly three segments. The domain is the closed list in item 2.
pub(crate) const fn event_name_ok(name: &str) -> bool {
    let bytes = name.as_bytes();
    if bytes.is_empty() || bytes.len() > 96 {
        return false;
    }
    let mut dots = [0usize; 2];
    let mut found = 0;
    let mut cursor = 0;
    while cursor < bytes.len() {
        if bytes[cursor] == b'.' {
            if found == 2 {
                return false;
            }
            dots[found] = cursor;
            found += 1;
        }
        cursor += 1;
    }
    if found != 2 {
        return false;
    }
    let first = (0, dots[0]);
    let second = (dots[0] + 1, dots[1]);
    let third = (dots[1] + 1, bytes.len());
    if !segment_at(bytes, first.0, first.1)
        || !segment_at(bytes, second.0, second.1)
        || !segment_at(bytes, third.0, third.1)
    {
        return false;
    }
    let mut domain = 0;
    while domain < DOMAINS.len() {
        if eq_at(bytes, first.0, first.1, DOMAINS[domain].as_bytes()) {
            return true;
        }
        domain += 1;
    }
    false
}

const fn template_ok(text: &str) -> bool {
    let bytes = text.as_bytes();
    if bytes.is_empty() || bytes.len() > 160 {
        return false;
    }
    let mut index = 0;
    while index < bytes.len() {
        let byte = bytes[index];
        // Printable ASCII, and no placeholder braces.
        if byte < 0x20 || byte > 0x7E || byte == b'{' || byte == b'}' {
            return false;
        }
        index += 1;
    }
    true
}

const fn key_ok(text: &str) -> bool {
    let bytes = text.as_bytes();
    if bytes.is_empty() || bytes.len() > 32 || !bytes[0].is_ascii_lowercase() {
        return false;
    }
    let mut index = 1;
    while index < bytes.len() {
        let byte = bytes[index];
        if !(byte.is_ascii_lowercase() || byte.is_ascii_digit() || byte == b'_') {
            return false;
        }
        index += 1;
    }
    true
}

macro_rules! code_table {
    // An admitted empty open-code vocabulary is uninhabited. It can reduce
    // external text through K3 but cannot produce a K1 member. K8's distinct
    // counter_table! macro and Counts still require a nonempty frozen map.
    ($name:ident, cap $cap:literal, {}) => {
        #[derive(Clone, Copy, Debug, PartialEq, Eq)]
        pub enum $name {}
        impl code_seal::Sealed for $name {}
        impl CodeEnum for $name {
            const TEXT: &'static [&'static str] = &[];
            const CAP: usize = $cap;
            fn index(self) -> u16 { match self {} }
            fn registration() -> TableRegistration<Self> { TableRegistration::new() }
        }
        const _: () = assert!($cap > 0 && $cap <= 64);
    };

    ($name:ident, cap $cap:literal, { $($variant:ident => $text:literal),+ $(,)? }) => {
        #[derive(Clone, Copy, Debug, PartialEq, Eq)]
        #[repr(u16)]
        pub enum $name {
            $($variant),+
        }

        impl code_seal::Sealed for $name {}

        impl CodeEnum for $name {
            const TEXT: &'static [&'static str] = &[$($text),+];
            const CAP: usize = $cap;
            fn index(self) -> u16 {
                self as u16
            }
            fn registration() -> TableRegistration<Self> { TableRegistration::new() }
        }

        const _: () = {
            assert!(members_ok($name::TEXT, $cap));
            assert!($name::TEXT.len() == [$($text),+].len());
        };
    };
}

code_table!(Phase, cap 32, {
    Request => "request",
    Discovery => "discovery",
    Snapshot => "snapshot",
    Plan => "plan",
    Provider => "provider",
    ProviderStart => "provider.start",
    ProviderAnalysis => "provider.analysis",
    ProviderTeardown => "provider.teardown",
    Admission => "admission",
    Evaluation => "evaluation",
    Commit => "commit",
    Delivery => "delivery",
    Reuse => "reuse",
});

/// Parent of each `Phase` member, in table order. `request` is the root.
pub(crate) const PHASE_PARENT: [Option<Phase>; 13] = [
    None,
    Some(Phase::Request),
    Some(Phase::Request),
    Some(Phase::Request),
    Some(Phase::Request),
    Some(Phase::Provider),
    Some(Phase::Provider),
    Some(Phase::Provider),
    Some(Phase::Request),
    Some(Phase::Request),
    Some(Phase::Request),
    Some(Phase::Request),
    Some(Phase::Request),
];

const _: () = assert!(PHASE_PARENT.len() == Phase::TEXT.len());

impl Phase {
    pub const fn parent(self) -> Option<Self> {
        PHASE_PARENT[self as usize]
    }
}

// Exact M3-O1 item14 vocabulary; no free-form outcome is admitted.
code_table!(PhaseOutcome, cap 32, {
    Completed => "completed",
    Failed => "failed",
    Cancelled => "cancelled",
    NotApplicable => "not-applicable",
});

code_table!(PathAnchor, cap 16, {
    Installation => "installation",
    Store => "store",
    LogRoot => "log-root",
    Scratch => "scratch",
    Project => "project",
    SystemTemp => "system-temp",
    External => "external",
});

code_table!(Sink, cap 64, {
    File => "file",
    Stderr => "stderr",
    Harness => "harness",
});

code_table!(Platform, cap 32, {
    LinuxAarch64Gnu => "linux-aarch64-gnu",
    LinuxX86_64Gnu => "linux-x86_64-gnu",
    MacosAarch64 => "macos-aarch64",
    MacosX86_64 => "macos-x86_64",
});

impl Platform {
    /// Build target family only; this is never S8 security qualification.
    pub const fn compiled() -> Option<Self> {
        if cfg!(all(
            target_os = "linux",
            target_env = "gnu",
            target_arch = "aarch64"
        )) {
            Some(Self::LinuxAarch64Gnu)
        } else if cfg!(all(
            target_os = "linux",
            target_env = "gnu",
            target_arch = "x86_64"
        )) {
            Some(Self::LinuxX86_64Gnu)
        } else if cfg!(all(target_os = "macos", target_arch = "aarch64")) {
            Some(Self::MacosAarch64)
        } else if cfg!(all(target_os = "macos", target_arch = "x86_64")) {
            Some(Self::MacosX86_64)
        } else {
            None
        }
    }
}

code_table!(BuildProfile, cap 32, {
    DebugAssertionsOn => "debug-assertions-on",
    DebugAssertionsOff => "debug-assertions-off",
});

impl BuildProfile {
    /// One compiled assertion fact, not Cargo profile/inheritance/settings.
    pub const fn compiled() -> Self {
        if cfg!(debug_assertions) {
            Self::DebugAssertionsOn
        } else {
            Self::DebugAssertionsOff
        }
    }
}

code_table!(IoErrorKind, cap 32, {
    PermissionDenied => "permission-denied",
    NoSpace => "no-space",
    IoError => "io-error",
    Other => "other",
});

impl IoErrorKind {
    /// Only the writer calls this on an actual returned I/O error. No message
    /// or worker label is retained, and short-write success is not an error.
    pub fn capture(error: &std::io::Error) -> (Self, Option<super::Errno>) {
        let raw = error.raw_os_error();
        let kind = match error.kind() {
            std::io::ErrorKind::PermissionDenied => Self::PermissionDenied,
            std::io::ErrorKind::StorageFull => Self::NoSpace,
            _ if raw.is_some() => Self::IoError,
            _ => Self::Other,
        };
        (kind, raw.map(super::Errno::from_raw_os_error))
    }
}

code_table!(CommitNotPublished, cap 64, {
    Undetermined => "undetermined",
    Refused => "refused",
});

code_table!(RepairKind, cap 64, {
    Registration => "registration",
    StoreDirectory => "store-directory",
    LedgerFile => "ledger-file",
    LedgerSchema => "ledger-schema",
    CarrierFloors => "carrier-floors",
    TrustDirectory => "trust-directory",
    TrustDependency => "trust-dependency",
});

code_table!(RepairState, cap 64, {
    RwR1 => "RW-R1",
    RwR2 => "RW-R2",
    RwR3 => "RW-R3",
    RwR4 => "RW-R4",
    RwR5 => "RW-R5",
    RwR6 => "RW-R6",
    RwR7 => "RW-R7",
    RwP1 => "RW-P1",
    RwP2 => "RW-P2",
    RwP3 => "RW-P3",
    RwL1 => "RW-L1",
    RwT1 => "RW-T1",
    RwT2 => "RW-T2",
    RwT3 => "RW-T3",
});

mod event_seal {
    pub trait Sealed {}
}

mod counter_seal {
    pub trait Sealed {}
}

pub trait CounterTable: counter_seal::Sealed {
    const MAP: &'static [(&'static str, Level)];
}

macro_rules! counter_table {
    ($name:ident, [$(($reason:literal, $level:expr)),+ $(,)?]) => {
        #[derive(Clone, Copy, Debug, PartialEq, Eq)]
        pub enum $name {}
        impl counter_seal::Sealed for $name {}
        impl CounterTable for $name {
            const MAP: &'static [(&'static str, Level)] = &[$(($reason,$level)),+];
        }
    };
}

// K8 frozen loss map: reason-major then level, exactly the item 17 tuples.
// No delivered outcome belongs to this map. The registration is private.
counter_table!(
    LossCell,
    [
        ("refused", Level::Error),
        ("refused", Level::Warn),
        ("refused", Level::Info),
        ("refused", Level::Debug),
        ("refused", Level::Trace),
        ("budget", Level::Error),
        ("budget", Level::Warn),
        ("budget", Level::Info),
        ("budget", Level::Debug),
        ("budget", Level::Trace),
        ("queue-full", Level::Error),
        ("queue-full", Level::Warn),
        ("queue-full", Level::Info),
        ("queue-full", Level::Debug),
        ("queue-full", Level::Trace),
        ("prescope-full", Level::Error),
        ("prescope-full", Level::Warn),
        ("prescope-full", Level::Info),
        ("prescope-full", Level::Debug),
        ("prescope-full", Level::Trace),
        ("unpersisted", Level::Error),
        ("unpersisted", Level::Warn),
        ("unpersisted", Level::Info),
        ("unpersisted", Level::Debug),
        ("unpersisted", Level::Trace),
        ("sink-failed", Level::Error),
        ("sink-failed", Level::Warn),
        ("sink-failed", Level::Info),
        ("sink-failed", Level::Debug),
        ("sink-failed", Level::Trace),
        ("sink-stopped", Level::Error),
        ("sink-stopped", Level::Warn),
        ("sink-stopped", Level::Info),
        ("sink-stopped", Level::Debug),
        ("sink-stopped", Level::Trace),
        ("drain-abandoned", Level::Error),
        ("drain-abandoned", Level::Warn),
        ("drain-abandoned", Level::Info),
        ("drain-abandoned", Level::Debug),
        ("drain-abandoned", Level::Trace),
    ]
);

const _: () = {
    assert!(LossCell::MAP.len() == 40);
    let mut index = 0;
    while index < 40 {
        assert!(eq(
            LossCell::MAP[index].0.as_bytes(),
            crate::constants::LOSS_REASONS[index / 5].as_bytes()
        ));
        assert!(LossCell::MAP[index].1.index() == index % 5);
        index += 1;
    }
};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum IdentitySet {
    Request,
    /// M3-D r5 item 21's tool events (:692; finding F6), unit D3a-3.
    Project,
    ProjectPlanExecution,
    ProjectPlanExecutionRun,
}

pub trait Event: event_seal::Sealed {
    const NAME: &'static str;
    const LEVEL: Level;
    const TEMPLATE: &'static str;
    const EXPORT: bool;
    const REQUIRES: IdentitySet;
    const FIELD_COUNT: usize;
    const MAX_LINE: usize;
    const FIELD_CLASSES: &'static [PrivacyClass];
    const FIELD_KEYS: &'static [&'static str];
    const FIELD_KINDS: &'static [&'static str];
    const FIELD_BOUNDS: &'static [usize];
    const FIELD_PRIVACY: &'static [(&'static str, PrivacyClass)];
    const FIELD_OPTIONAL: &'static [bool] = &[];
    /// Provider-asserted fields (SOP2 item 4), labelled in the reference.
    const FIELD_ASSERTED: &'static [bool] = &[];
    const COUNTER_MAPS: &'static [(&'static str, &'static [(&'static str, Level)])] = &[];
}

/// Builds the two `owned(storage)` commit events. Issued only through [`CapabilitySet`].
pub struct StorageCommitOwner {
    _private: (),
}

macro_rules! event {
    (
        struct $type:ident;
        name: $name:literal;
        level: $level:expr;
        requires: $requires:expr;
        export: $export:literal;
        template: $template:literal;
        fields: { $($key:ident $class:ident : $fty:ty),+ $(,)? }
    ) => {
        pub struct $type {
            $($key: $fty,)+
        }

        impl event_seal::Sealed for $type {}

        impl Event for $type {
            const NAME: &'static str = $name;
            const LEVEL: Level = $level;
            const TEMPLATE: &'static str = $template;
            const EXPORT: bool = $export;
            const REQUIRES: IdentitySet = $requires;
            const FIELD_COUNT: usize = 0 $(+ { let _ = stringify!($key); 1 })+;
            const MAX_LINE: usize = HEADER_RESERVE
                $(+ stringify!($key).len() + 4 + <$fty as SafeField>::MAX_VALUE)+;
            const FIELD_CLASSES: &'static [PrivacyClass] = &[$(PrivacyClass::$class),+];
            const FIELD_KEYS: &'static [&'static str] = &[$(stringify!($key)),+];
            const FIELD_KINDS: &'static [&'static str] = &[$(stringify!($fty)),+];
            const FIELD_BOUNDS: &'static [usize] = &[$(<$fty as SafeField>::MAX_VALUE),+];
            const FIELD_PRIVACY: &'static [(&'static str, PrivacyClass)] = &[$((stringify!($key), PrivacyClass::$class)),+];
        }

        impl $type {
            pub fn new($($key: $fty),+) -> Self {
                Self { $($key,)+ }
            }

            pub(crate) fn projected_truncated(&self, ceiling: PrivacyClass) -> usize {
                0 $(+ usize::from(PrivacyClass::$class <= ceiling && self.$key.truncated()))+
            }

            /// JSON object of the fields at or below `ceiling`. The count is `omitted`.
            pub(crate) fn project_fields(&self, ceiling: PrivacyClass, out: &mut Vec<u8>) -> usize {
                out.push(b'{');
                let mut omitted = 0usize;
                let mut written = 0usize;
                $(
                    if PrivacyClass::$class <= ceiling {
                        if written > 0 {
                            out.push(b',');
                        }
                        written += 1;
                        out.push(b'"');
                        out.extend_from_slice(stringify!($key).as_bytes());
                        out.extend_from_slice(b"\":");
                        self.$key.encode(Form::Json, out);
                    } else {
                        omitted += 1;
                    }
                )+
                out.push(b'}');
                let visited = written + omitted;
                assert!(visited == Self::FIELD_COUNT);
                omitted
            }

            /// Human `key=value` pairs at or below `ceiling`. Each pair has a leading space.
            pub(crate) fn project_fields_human(
                &self,
                ceiling: PrivacyClass,
                out: &mut Vec<u8>,
            ) -> usize {
                let mut omitted = 0usize;
                let mut written = 0usize;
                $(
                    if PrivacyClass::$class <= ceiling {
                        written += 1;
                        out.push(b' ');
                        out.extend_from_slice(stringify!($key).as_bytes());
                        out.push(b'=');
                        self.$key.encode(Form::Human, out);
                    } else {
                        omitted += 1;
                    }
                )+
                let visited = written + omitted;
                assert!(visited == Self::FIELD_COUNT);
                omitted
            }
        }

        const _: () = {
            assert!(event_name_ok($name));
            assert!(template_ok($template));
            $(assert!(key_ok(stringify!($key)));)+
            $(assert!(PrivacyClass::$class as u8 == <$fty as SafeField>::CLASS as u8);
              assert!(<$fty as SafeField>::DEPTH <= 2);)+
            assert!($type::FIELD_COUNT <= MAX_FIELDS);
            assert!($type::FIELD_COUNT == $type::FIELD_CLASSES.len());
            assert!($type::FIELD_COUNT == $type::FIELD_KEYS.len());
            assert!($type::FIELD_COUNT == $type::FIELD_KINDS.len());
            assert!($type::FIELD_COUNT == $type::FIELD_BOUNDS.len());
            assert!($type::MAX_LINE <= MAX_LINE);
        };
    };
    (
        owned struct $type:ident;
        name: $name:literal;
        level: $level:expr;
        requires: $requires:expr;
        export: $export:literal;
        template: $template:literal;
        fields: { $($key:ident $class:ident : $fty:ty),+ $(,)? }
    ) => {
        pub struct $type {
            $($key: $fty,)+
        }

        impl event_seal::Sealed for $type {}

        impl Event for $type {
            const NAME: &'static str = $name;
            const LEVEL: Level = $level;
            const TEMPLATE: &'static str = $template;
            const EXPORT: bool = $export;
            const REQUIRES: IdentitySet = $requires;
            const FIELD_COUNT: usize = 0 $(+ { let _ = stringify!($key); 1 })+;
            const MAX_LINE: usize = HEADER_RESERVE
                $(+ stringify!($key).len() + 4 + <$fty as SafeField>::MAX_VALUE)+;
            const FIELD_CLASSES: &'static [PrivacyClass] = &[$(PrivacyClass::$class),+];
            const FIELD_KEYS: &'static [&'static str] = &[$(stringify!($key)),+];
            const FIELD_KINDS: &'static [&'static str] = &[$(stringify!($fty)),+];
            const FIELD_BOUNDS: &'static [usize] = &[$(<$fty as SafeField>::MAX_VALUE),+];
            const FIELD_PRIVACY: &'static [(&'static str, PrivacyClass)] = &[$((stringify!($key), PrivacyClass::$class)),+];
        }

        impl $type {
            pub fn new(_owner: &StorageCommitOwner, $($key: $fty),+) -> Self {
                Self { $($key,)+ }
            }

            pub(crate) fn projected_truncated(&self, ceiling: PrivacyClass) -> usize {
                0 $(+ usize::from(PrivacyClass::$class <= ceiling && self.$key.truncated()))+
            }

            /// JSON object of the fields at or below `ceiling`. The count is `omitted`.
            pub(crate) fn project_fields(&self, ceiling: PrivacyClass, out: &mut Vec<u8>) -> usize {
                out.push(b'{');
                let mut omitted = 0usize;
                let mut written = 0usize;
                $(
                    if PrivacyClass::$class <= ceiling {
                        if written > 0 {
                            out.push(b',');
                        }
                        written += 1;
                        out.push(b'"');
                        out.extend_from_slice(stringify!($key).as_bytes());
                        out.extend_from_slice(b"\":");
                        self.$key.encode(Form::Json, out);
                    } else {
                        omitted += 1;
                    }
                )+
                out.push(b'}');
                let visited = written + omitted;
                assert!(visited == Self::FIELD_COUNT);
                omitted
            }

            /// Human `key=value` pairs at or below `ceiling`. Each pair has a leading space.
            pub(crate) fn project_fields_human(
                &self,
                ceiling: PrivacyClass,
                out: &mut Vec<u8>,
            ) -> usize {
                let mut omitted = 0usize;
                let mut written = 0usize;
                $(
                    if PrivacyClass::$class <= ceiling {
                        written += 1;
                        out.push(b' ');
                        out.extend_from_slice(stringify!($key).as_bytes());
                        out.push(b'=');
                        self.$key.encode(Form::Human, out);
                    } else {
                        omitted += 1;
                    }
                )+
                let visited = written + omitted;
                assert!(visited == Self::FIELD_COUNT);
                omitted
            }
        }

        const _: () = {
            assert!(event_name_ok($name));
            assert!(template_ok($template));
            $(assert!(key_ok(stringify!($key)));)+
            $(assert!(PrivacyClass::$class as u8 == <$fty as SafeField>::CLASS as u8);
              assert!(<$fty as SafeField>::DEPTH <= 2);)+
            assert!($type::FIELD_COUNT <= MAX_FIELDS);
            assert!($type::FIELD_COUNT == $type::FIELD_CLASSES.len());
            assert!($type::FIELD_COUNT == $type::FIELD_KEYS.len());
            assert!($type::FIELD_COUNT == $type::FIELD_KINDS.len());
            assert!($type::FIELD_COUNT == $type::FIELD_BOUNDS.len());
            assert!($type::MAX_LINE <= MAX_LINE);
        };
    };
}

event! {
    struct LogStreamOpened;
    name: "log.stream.opened";
    level: Level::Info;
    requires: IdentitySet::Request;
    export: false;
    template: "log stream opened";
    fields: {
        version P0: Version,
        platform P0: Code<Platform>,
        build P0: Code<BuildProfile>,
        sink P0: Code<Sink>,
        pid P1: ProcessId,
    }
}

/// Loss records are internal writer-owned records. The optional code and
/// errno are derived together from the same captured actual I/O error.
macro_rules! loss_event {
    ($type:ident, $name:literal, $template:literal) => {
        pub struct $type {
            #[cfg(any(
                test,
                feature = "operability-dev-sinks",
                feature = "harness-instrumentation"
            ))]
            sink: Code<Sink>,
            #[cfg(any(
                test,
                feature = "operability-dev-sinks",
                feature = "harness-instrumentation"
            ))]
            counts: Counts<LossCell, 40>,
            #[cfg(any(
                test,
                feature = "operability-dev-sinks",
                feature = "harness-instrumentation"
            ))]
            error: Option<crate::writer::CapturedError>,
        }
        impl event_seal::Sealed for $type {}
        impl Event for $type {
            const NAME: &'static str = $name;
            const LEVEL: Level = Level::Warn;
            const TEMPLATE: &'static str = $template;
            const EXPORT: bool = false;
            const REQUIRES: IdentitySet = IdentitySet::Request;
            const FIELD_COUNT: usize = 4;
            const MAX_LINE: usize = HEADER_RESERVE
                + 4
                + 4
                + Code::<Sink>::MAX_VALUE
                + 6
                + 4
                + Counts::<LossCell, 40>::MAX_VALUE
                + 10
                + 4
                + Code::<IoErrorKind>::MAX_VALUE
                + 5
                + 4
                + Errno::MAX_VALUE;
            const FIELD_KEYS: &'static [&'static str] = &["sink", "counts", "sink_error", "errno"];
            const FIELD_CLASSES: &'static [PrivacyClass] = &[PrivacyClass::P0; 4];
            const FIELD_KINDS: &'static [&'static str] = &[
                "Code<Sink>",
                "Counts<LossCell,40>",
                "Code<IoErrorKind>",
                "Errno",
            ];
            const FIELD_BOUNDS: &'static [usize] = &[
                Code::<Sink>::MAX_VALUE,
                Counts::<LossCell, 40>::MAX_VALUE,
                Code::<IoErrorKind>::MAX_VALUE,
                Errno::MAX_VALUE,
            ];
            const FIELD_PRIVACY: &'static [(&'static str, PrivacyClass)] = &[
                ("sink", PrivacyClass::P0),
                ("counts", PrivacyClass::P0),
                ("sink_error", PrivacyClass::P0),
                ("errno", PrivacyClass::P0),
            ];
            const FIELD_OPTIONAL: &'static [bool] = &[false, false, true, true];
            const COUNTER_MAPS: &'static [(&'static str, &'static [(&'static str, Level)])] =
                &[("counts", LossCell::MAP)];
        }
        impl $type {
            #[cfg(any(
                test,
                feature = "operability-dev-sinks",
                feature = "harness-instrumentation"
            ))]
            pub(crate) fn from_snapshot(
                sink: Sink,
                counts: [u64; 40],
                error: Option<crate::writer::CapturedError>,
            ) -> Self {
                Self {
                    sink: Code::from_enum(sink),
                    counts: Counts::new(counts),
                    error,
                }
            }
            #[cfg(any(test, feature = "operability-dev-sinks"))]
            pub(crate) fn projected_truncated(&self, _ceiling: PrivacyClass) -> usize {
                0
            }
            #[cfg(any(test, feature = "harness-instrumentation"))]
            pub(crate) fn project_fields(
                &self,
                _ceiling: PrivacyClass,
                out: &mut Vec<u8>,
            ) -> usize {
                out.extend_from_slice(b"{\"sink\":");
                self.sink.encode(Form::Json, out);
                out.extend_from_slice(b",\"counts\":");
                self.counts.encode(Form::Json, out);
                if let Some(error) = self.error {
                    out.extend_from_slice(b",\"sink_error\":");
                    Code::from_enum(error.kind).encode(Form::Json, out);
                    if let Some(errno) = error.errno {
                        out.extend_from_slice(b",\"errno\":");
                        errno.encode(Form::Json, out);
                    }
                }
                out.push(b'}');
                0
            }
            #[cfg(any(test, feature = "operability-dev-sinks"))]
            pub(crate) fn project_fields_human(
                &self,
                _ceiling: PrivacyClass,
                out: &mut Vec<u8>,
            ) -> usize {
                out.extend_from_slice(b" sink=");
                self.sink.encode(Form::Human, out);
                out.extend_from_slice(b" counts=");
                self.counts.encode(Form::Human, out);
                if let Some(error) = self.error {
                    out.extend_from_slice(b" sink_error=");
                    Code::from_enum(error.kind).encode(Form::Human, out);
                    if let Some(errno) = error.errno {
                        out.extend_from_slice(b" errno=");
                        errno.encode(Form::Human, out);
                    }
                }
                0
            }
        }
        const _: () = {
            assert!(event_name_ok($name));
            assert!(template_ok($template));
            assert!($type::MAX_LINE <= MAX_LINE);
        };
    };
}

loss_event!(LogLossCounted, "log.loss.counted", "log loss counted");

event! {
    struct HostRepairCompleted;
    name: "host.repair.completed";
    level: Level::Info;
    requires: IdentitySet::Request;
    export: false;
    template: "repair completed";
    fields: {
        kind P0: Code<RepairKind>,
        state P0: Code<RepairState>,
    }
}

event! {
    owned struct StorageCommitPublished;
    name: "storage.commit.published";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecutionRun;
    export: true;
    template: "commit published";
    fields: { latched P0: Flag }
}

event! {
    owned struct StorageCommitNotPublished;
    name: "storage.commit.not_published";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: true;
    template: "commit not published";
    fields: { outcome P0: Code<CommitNotPublished> }
}

/// Returned once by `start`; the owning host lends only the named mint legs.
pub(crate) struct CapabilitySet {
    pub(crate) process_id: super::ProcessIdMint,
    pub(crate) position: super::PositionMint,
    pub(crate) rule_id: super::RuleIdMint,
    pub(crate) declared_name: super::DeclaredNameMint,
    pub(crate) project_path: super::ProjectPathMint,
    pub(crate) path_ref: super::PathRefMint,
    pub(crate) snapshot_digest: super::IdentityDigestMint<super::SnapshotDigest>,
    pub(crate) closure_digest: super::IdentityDigestMint<super::ClosureDigest>,
    pub(crate) universe_digest: super::IdentityDigestMint<super::UniverseDigest>,
    pub(crate) manifest_digest: super::IdentityDigestMint<super::ManifestDigest>,
    pub(crate) storage: StorageCommitOwner,
}

impl CapabilitySet {
    pub(crate) fn issue() -> Self {
        Self {
            process_id: super::ProcessIdMint::issue(),
            position: super::PositionMint::issue(),
            rule_id: super::RuleIdMint::issue(),
            declared_name: super::DeclaredNameMint::issue(),
            project_path: super::ProjectPathMint::issue(),
            path_ref: super::PathRefMint::issue(),
            snapshot_digest: super::IdentityDigestMint::issue(),
            closure_digest: super::IdentityDigestMint::issue(),
            universe_digest: super::IdentityDigestMint::issue(),
            manifest_digest: super::IdentityDigestMint::issue(),
            storage: StorageCommitOwner { _private: () },
        }
    }
}

#[cfg(test)]
#[path = "registry_tests.rs"]
mod tests;

// O1-b ordinary phase registrations. The parent is derived from the selected
// closed Phase table, so no constructor accepts an arbitrary parent.
pub struct HostPhaseStarted {
    phase: Code<Phase>,
    parent: Option<Code<Phase>>,
    at: Elapsed,
}
impl event_seal::Sealed for HostPhaseStarted {}
impl Event for HostPhaseStarted {
    const NAME: &'static str = "host.phase.started";
    const LEVEL: Level = Level::Info;
    const TEMPLATE: &'static str = "phase started";
    const EXPORT: bool = false;
    const REQUIRES: IdentitySet = IdentitySet::Request;
    const FIELD_COUNT: usize = 3;
    const MAX_LINE: usize = HEADER_RESERVE
        + 5
        + 4
        + <Code<Phase> as SafeField>::MAX_VALUE
        + 6
        + 4
        + <Code<Phase> as SafeField>::MAX_VALUE
        + 2
        + 4
        + <Elapsed as SafeField>::MAX_VALUE;
    const FIELD_CLASSES: &'static [PrivacyClass] = &[PrivacyClass::P0; 3];
    const FIELD_KEYS: &'static [&'static str] = &["phase", "parent", "at"];
    const FIELD_KINDS: &'static [&'static str] = &["Code<Phase>", "Code<Phase>", "Elapsed"];
    const FIELD_BOUNDS: &'static [usize] = &[
        <Code<Phase> as SafeField>::MAX_VALUE,
        <Code<Phase> as SafeField>::MAX_VALUE,
        <Elapsed as SafeField>::MAX_VALUE,
    ];
    const FIELD_PRIVACY: &'static [(&'static str, PrivacyClass)] = &[
        ("phase", PrivacyClass::P0),
        ("parent", PrivacyClass::P0),
        ("at", PrivacyClass::P0),
    ];
    const FIELD_OPTIONAL: &'static [bool] = &[false, true, false];
}
impl HostPhaseStarted {
    pub fn new(phase: Phase, at: Elapsed) -> Self {
        Self {
            phase: Code::from_enum(phase),
            parent: phase.parent().map(Code::from_enum),
            at,
        }
    }
    pub(crate) fn projected_truncated(&self, _ceiling: PrivacyClass) -> usize {
        0
    }
    pub(crate) fn project_fields(&self, _ceiling: PrivacyClass, out: &mut Vec<u8>) -> usize {
        out.extend_from_slice(b"{\"phase\":");
        self.phase.encode(Form::Json, out);
        if let Some(parent) = self.parent {
            out.extend_from_slice(b",\"parent\":");
            parent.encode(Form::Json, out);
        }
        out.extend_from_slice(b",\"at\":");
        self.at.encode(Form::Json, out);
        out.push(b'}');
        0
    }
    pub(crate) fn project_fields_human(&self, _ceiling: PrivacyClass, out: &mut Vec<u8>) -> usize {
        out.extend_from_slice(b" phase=");
        self.phase.encode(Form::Human, out);
        if let Some(parent) = self.parent {
            out.extend_from_slice(b" parent=");
            parent.encode(Form::Human, out);
        }
        out.extend_from_slice(b" at=");
        self.at.encode(Form::Human, out);
        0
    }
}
const _: () = {
    assert!(event_name_ok(HostPhaseStarted::NAME));
    assert!(template_ok(HostPhaseStarted::TEMPLATE));
    assert!(HostPhaseStarted::MAX_LINE <= MAX_LINE);
    assert!(HostPhaseStarted::FIELD_COUNT <= MAX_FIELDS);
};

event! {
    struct HostPhaseCompleted;
    name: "host.phase.completed";
    level: Level::Info;
    requires: IdentitySet::Request;
    export: true;
    template: "phase completed";
    fields: {
        phase P0: Code<Phase>,
        wall P0: Elapsed,
        cpu P0: Elapsed,
        outcome P0: Code<PhaseOutcome>,
        at P0: Elapsed,
    }
}

#[cfg(test)]
mod phase_registration_tests {
    use super::*;
    #[test]
    fn the_started_parent_is_absent_only_for_the_selected_root() {
        let mut root = Vec::new();
        let omitted = HostPhaseStarted::new(Phase::Request, Elapsed::new(0))
            .project_fields(PrivacyClass::P0, &mut root);
        assert_eq!(omitted, 0);
        assert_eq!(root, b"{\"phase\":\"request\",\"at\":0}");
        let mut delivery = Vec::new();
        let omitted = HostPhaseStarted::new(Phase::Delivery, Elapsed::new(42))
            .project_fields(PrivacyClass::P0, &mut delivery);
        assert_eq!(omitted, 0);
        assert_eq!(
            delivery,
            b"{\"phase\":\"delivery\",\"parent\":\"request\",\"at\":42}"
        );
        for phase in [
            Phase::ProviderStart,
            Phase::ProviderAnalysis,
            Phase::ProviderTeardown,
        ] {
            assert_eq!(phase.parent(), Some(Phase::Provider));
        }
        assert_eq!(
            PhaseOutcome::TEXT,
            &["completed", "failed", "cancelled", "not-applicable"]
        );
    }
}

// ------------------------------------------------------------------ M3-D unit D3a-3: supervision records
//
// M3-D r5 item 21 (`docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`:680-698)
// registers S-OP-2 item 23's provider and supervision events (SOP2:877-890)
// and D3's ordinary registrations (SOP2:226-230), under the D3a plan r4's
// LD-D3A-10. Every `provider.*` and `supervision.*` event carries `role` K1
// `ProviderRole` and `universe` K9 and requires Project, Plan and Execution
// (SOP2:856-859). Four S-OP-2 events are not registered: their required
// tables (`StageKind`, `ProviderState`, `Signal`, `ProviderReason`) resolve
// in no pinned contract, carrier or law, so each is an explicit blocker
// (LD-D3A-10): `provider.stage.changed`, `provider.stage.terminal`,
// `provider.process.reaped` and `supervision.progress.absent`.

// Registry-literal tables (SOP2 item 3).
// SOP2:340.
code_table!(ProviderRole, cap 64, {
    TypescriptSemantic => "typescript-semantic",
    RustSemantic => "rust-semantic",
});
// The two selectable protocols, TS2 and Rust3 (M3-D r5 :379; NE:2785).
code_table!(ProtocolMajor, cap 64, {
    TypescriptSemantic2 => "typescript-semantic-2",
    RustSemantic3 => "rust-semantic-3",
});
// SOP2:881.
code_table!(RssUnit, cap 64, {
    Kib => "kib",
    Bytes => "bytes",
});
// SOP2:883.
code_table!(FaultSource, cap 64, {
    ControlFault => "control-fault",
    ControlRefusal => "control-refusal",
    RustProviderFault => "rust-provider-fault",
});
// SOP2:889.
code_table!(ForceTrigger, cap 64, {
    SecondSignal => "second-signal",
    GraceExpired => "grace-expired",
});
// M3-D r5 item 12's causes (:446), as LD-D3A-19 reads `provider-protocol`.
// `control-refusal` and `byte-bound` carry their family and kind in their
// own records (`provider.fault.reduced`, `supervision.limit.breached`).
code_table!(TeardownCause, cap 64, {
    Clean => "clean",
    ClosureRecheckFailed => "closure-recheck-failed",
    SessionSpecInconsistent => "session-spec-inconsistent",
    SpawnFailed => "spawn-failed",
    HandshakeDeadline => "handshake-deadline",
    ControlRefusal => "control-refusal",
    ProviderProtocol => "provider-protocol",
    UnexpectedExit => "unexpected-exit",
    Deadline => "deadline",
    Liveness => "liveness",
    MemoryCeiling => "memory-ceiling",
    ProcessCount => "process-count",
    ByteBound => "byte-bound",
    ScratchBound => "scratch-bound",
    UserCancel => "user-cancel",
    Revoked => "revoked",
    ObserverFailStop => "observer-fail-stop",
    HostFault => "host-fault",
    Abandoned => "abandoned",
    ConfinementRefused => "confinement-refused",
});
// M3-D r5 item 14's bounded waits (:481-496).
code_table!(BoundedWait, cap 64, {
    Handshake => "handshake",
    LivenessWindow => "liveness-window",
    ProgressAbsent => "progress-absent",
    WallClock => "wall-clock",
    NormalExitGrace => "normal-exit-grace",
    Stage1CancelGrace => "stage1-cancel-grace",
    ShutdownAck => "shutdown-ack",
    TermToKill => "term-to-kill",
    ReapCeiling => "reap-ceiling",
    Drain => "drain",
});
// M3-D r5 item 16's bounds (:528-549) and their units.
code_table!(LimitKind, cap 64, {
    ResidentMemory => "resident-memory",
    ProcessCount => "process-count",
    Response => "response",
    Scratch => "scratch",
    ToolOutput => "tool-output",
});
code_table!(LimitUnit, cap 64, {
    Bytes => "bytes",
    Processes => "processes",
});
// M3-D r5 item 12's `exit` (:440).
code_table!(ExitClass, cap 64, {
    Exited => "exited",
    Signaled => "signaled",
    Unreaped => "unreaped",
});
// M3-D r5 item 20 and item 21 as LD-D3A-17 and LD-D3A-18 amend them.
code_table!(ScratchRetainedReason, cap 64, {
    IoFailure => "io-failure",
    WorkExhausted => "work-exhausted",
    RootUnreaped => "root-unreaped",
});
// D3a-3's ordinary field on `supervision.liveness.missed` (D3A1-R2-NBO-1):
// the window expired, or a report's nonce mismatched.
code_table!(LivenessMiss, cap 64, {
    WindowExpired => "window-expired",
    NonceMismatch => "nonce-mismatch",
});

// Protocol-enum tables (SOP2 item 3): members written here as literals, each
// equal to its pinned schema's enum; C-2's equality check is the components
// crate's, which holds the generated contracts.
// CC's refusal families RF-1 to RF-8 (CC:104-117).
code_table!(RefusalFamily, cap 64, {
    Rf1 => "RF-1",
    Rf2 => "RF-2",
    Rf3 => "RF-3",
    Rf4 => "RF-4",
    Rf5 => "RF-5",
    Rf6 => "RF-6",
    Rf7 => "RF-7",
    Rf8 => "RF-8",
});
// CC:37, the generated `Control3RootVariant7Property0Reason`.
code_table!(ControlCancelReason, cap 64, {
    User => "user",
    Deadline => "deadline",
    SupervisorFault => "supervisor-fault",
});
// RPP:445 `ProviderFaultV2.faultKind`, the generated
// `Rust3ProviderFaultV2Field3Value`.
code_table!(RustFaultKind, cap 64, {
    CompilerCrash => "compiler-crash",
    InputRejected => "input-rejected",
    InternalInvariant => "internal-invariant",
});
// SOP2:844: an empty K3 table at r2, so every value is `{unrecognized}`.
code_table!(RustDetailCode, cap 64, {});

/// A field's mode in [`supervision_event!`]: required, optional, or required
/// and provider-asserted (SOP2 item 4: labelled `asserted`, never progress).
macro_rules! field_ty {
    (req, $t:ty) => { $t };
    (asserted, $t:ty) => { $t };
    (opt, $t:ty) => { Option<$t> };
}
macro_rules! field_optional {
    (opt) => {
        true
    };
    ($mode:ident) => {
        false
    };
}
macro_rules! field_asserted {
    (asserted) => {
        true
    };
    ($mode:ident) => {
        false
    };
}
macro_rules! field_present {
    (opt, $value:expr) => {
        $value.as_ref()
    };
    ($mode:ident, $value:expr) => {
        Some(&$value)
    };
}

/// D3a-3's events: as `event!`, with optional and asserted fields, and an
/// optional private constructor where only typed builders may make a value.
macro_rules! supervision_event {
    (
        struct $type:ident;
        name: $name:literal;
        level: $level:expr;
        requires: $requires:expr;
        export: $export:literal;
        template: $template:literal;
        constructor: $vis:vis fields: { $($key:ident $class:ident $mode:ident : $fty:ty),+ $(,)? }
    ) => {
        pub struct $type {
            $($key: field_ty!($mode, $fty),)+
        }

        impl event_seal::Sealed for $type {}

        impl Event for $type {
            const NAME: &'static str = $name;
            const LEVEL: Level = $level;
            const TEMPLATE: &'static str = $template;
            const EXPORT: bool = $export;
            const REQUIRES: IdentitySet = $requires;
            const FIELD_COUNT: usize = [$(stringify!($key)),+].len();
            const MAX_LINE: usize = HEADER_RESERVE
                $(+ stringify!($key).len() + 4 + <$fty as SafeField>::MAX_VALUE)+;
            const FIELD_CLASSES: &'static [PrivacyClass] = &[$(PrivacyClass::$class),+];
            const FIELD_KEYS: &'static [&'static str] = &[$(stringify!($key)),+];
            const FIELD_KINDS: &'static [&'static str] = &[$(stringify!($fty)),+];
            const FIELD_BOUNDS: &'static [usize] = &[$(<$fty as SafeField>::MAX_VALUE),+];
            const FIELD_PRIVACY: &'static [(&'static str, PrivacyClass)] = &[$((stringify!($key), PrivacyClass::$class)),+];
            const FIELD_OPTIONAL: &'static [bool] = &[$(field_optional!($mode)),+];
            const FIELD_ASSERTED: &'static [bool] = &[$(field_asserted!($mode)),+];
        }

        impl $type {
            #[allow(clippy::too_many_arguments)]
            $vis fn new($($key: field_ty!($mode, $fty)),+) -> Self {
                Self { $($key,)+ }
            }

            pub(crate) fn projected_truncated(&self, ceiling: PrivacyClass) -> usize {
                0 $(+ usize::from(
                    PrivacyClass::$class <= ceiling
                        && field_present!($mode, self.$key).is_some_and(|value| value.truncated())
                ))+
            }

            /// JSON object of the present fields at or below `ceiling`; an
            /// absent optional field is not written. The count is `omitted`.
            pub(crate) fn project_fields(&self, ceiling: PrivacyClass, out: &mut Vec<u8>) -> usize {
                out.push(b'{');
                let mut omitted = 0usize;
                let mut written = 0usize;
                $(
                    if let Some(value) = field_present!($mode, self.$key) {
                        if PrivacyClass::$class <= ceiling {
                            if written > 0 {
                                out.push(b',');
                            }
                            written += 1;
                            out.push(b'"');
                            out.extend_from_slice(stringify!($key).as_bytes());
                            out.extend_from_slice(b"\":");
                            value.encode(Form::Json, out);
                        } else {
                            omitted += 1;
                        }
                    }
                )+
                out.push(b'}');
                debug_assert!(written + omitted <= Self::FIELD_COUNT);
                omitted
            }

            /// Human `key=value` pairs of the present fields at or below `ceiling`.
            pub(crate) fn project_fields_human(
                &self,
                ceiling: PrivacyClass,
                out: &mut Vec<u8>,
            ) -> usize {
                let mut omitted = 0usize;
                $(
                    if let Some(value) = field_present!($mode, self.$key) {
                        if PrivacyClass::$class <= ceiling {
                            out.push(b' ');
                            out.extend_from_slice(stringify!($key).as_bytes());
                            out.push(b'=');
                            value.encode(Form::Human, out);
                        } else {
                            omitted += 1;
                        }
                    }
                )+
                omitted
            }
        }

        const _: () = {
            assert!(event_name_ok($name));
            assert!(template_ok($template));
            $(assert!(key_ok(stringify!($key)));)+
            $(assert!(PrivacyClass::$class as u8 == <$fty as SafeField>::CLASS as u8);
              assert!(<$fty as SafeField>::DEPTH <= 2);)+
            assert!($type::FIELD_COUNT <= MAX_FIELDS);
            assert!($type::FIELD_COUNT == $type::FIELD_CLASSES.len());
            assert!($type::FIELD_COUNT == $type::FIELD_KEYS.len());
            assert!($type::FIELD_COUNT == $type::FIELD_KINDS.len());
            assert!($type::FIELD_COUNT == $type::FIELD_BOUNDS.len());
            assert!($type::FIELD_COUNT == $type::FIELD_OPTIONAL.len());
            assert!($type::FIELD_COUNT == $type::FIELD_ASSERTED.len());
            assert!($type::MAX_LINE <= MAX_LINE);
        };
    };
}

/// K9 `Universe` (SOP2:859; NE:3160-3164): the universe key's digest.
pub type Universe = super::IdentityDigest<super::UniverseDigest>;

supervision_event! {
    struct ProviderProcessSpawned;
    name: "provider.process.spawned";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "provider process spawned";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        protocol P0 req: Code<ProtocolMajor>,
        pid P1 req: ProcessId,
    }
}

supervision_event! {
    struct ProviderProcessReady;
    name: "provider.process.ready";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "provider process ready";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        start P0 req: Elapsed,
        transfer P0 req: Elapsed,
    }
}

supervision_event! {
    struct ProviderStderrReduced;
    name: "provider.stderr.reduced";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "provider stderr reduced";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        stderr P0 req: Reduced,
    }
}

supervision_event! {
    struct ProviderFaultReduced;
    name: "provider.fault.reduced";
    level: Level::Warn;
    requires: IdentitySet::ProjectPlanExecution;
    export: true;
    template: "provider fault reduced";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        source P0 req: Code<FaultSource>,
        fault_kind P0 opt: Code<RustFaultKind>,
        refusal_family P0 opt: Code<RefusalFamily>,
        detail P0 req: Reduced,
        detail_code P0 opt: RegisteredCode<RustDetailCode>,
    }
}

supervision_event! {
    struct ProviderResourcesReported;
    name: "provider.resources.reported";
    level: Level::Debug;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "provider resources reported";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        resident P0 asserted: Bytes,
        cpu P0 asserted: Elapsed,
        handles P0 asserted: Count,
    }
}

supervision_event! {
    struct SupervisionLivenessMissed;
    name: "supervision.liveness.missed";
    level: Level::Warn;
    requires: IdentitySet::ProjectPlanExecution;
    export: true;
    template: "liveness missed";
    constructor: pub(crate) fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        window P0 req: Elapsed,
        miss P0 req: Code<LivenessMiss>,
        refusal_family P0 opt: Code<RefusalFamily>,
    }
}

impl SupervisionLivenessMissed {
    /// The window expired with no report (item 15).
    pub fn window_expired(role: Code<ProviderRole>, universe: Universe, window: Elapsed) -> Self {
        Self::new(
            role,
            universe,
            window,
            Code::from_enum(LivenessMiss::WindowExpired),
            None,
        )
    }
    /// A report's nonce mismatched, refused by the control owner in
    /// `family` (D3A1-R2-NBO-1). No nonce or frame text is recorded.
    pub fn nonce_mismatch(
        role: Code<ProviderRole>,
        universe: Universe,
        window: Elapsed,
        family: Code<RefusalFamily>,
    ) -> Self {
        Self::new(
            role,
            universe,
            window,
            Code::from_enum(LivenessMiss::NonceMismatch),
            Some(family),
        )
    }
}

supervision_event! {
    struct SupervisionLimitBreached;
    name: "supervision.limit.breached";
    level: Level::Warn;
    requires: IdentitySet::ProjectPlanExecution;
    export: true;
    template: "limit breached";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        limit P0 req: Code<LimitKind>,
        observed P0 req: Count,
        unit P0 req: Code<LimitUnit>,
    }
}

supervision_event! {
    struct SupervisionSampleIncomplete;
    name: "supervision.sample.incomplete";
    level: Level::Warn;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "resource sample incomplete";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        listed P0 req: Count,
        unsampled P0 req: Count,
        listing_failed P0 req: Flag,
    }
}

supervision_event! {
    struct SupervisionCancelSent;
    name: "supervision.cancel.sent";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "cancel sent";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        inband P0 req: Flag,
        control_reason P0 req: Code<ControlCancelReason>,
    }
}

supervision_event! {
    struct SupervisionCancelForced;
    name: "supervision.cancel.forced";
    level: Level::Warn;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "cancel forced";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        trigger P0 req: Code<ForceTrigger>,
        grace P0 req: Elapsed,
    }
}

supervision_event! {
    struct SupervisionWaitExpired;
    name: "supervision.wait.expired";
    level: Level::Warn;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "wait expired";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        wait P0 req: Code<BoundedWait>,
        limit P0 req: Elapsed,
    }
}

supervision_event! {
    struct SupervisionTeardownStarted;
    name: "supervision.teardown.started";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "teardown started";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        cause P0 req: Code<TeardownCause>,
    }
}

supervision_event! {
    struct SupervisionTreeSwept;
    name: "supervision.tree.swept";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "tree swept";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        killed P0 req: Count,
        unattributed P0 req: Count,
        platform_limited P0 req: Flag,
    }
}

supervision_event! {
    struct SupervisionScratchRetained;
    name: "supervision.scratch.retained";
    level: Level::Warn;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "scratch retained";
    constructor: pub(crate) fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        reason P0 req: Code<ScratchRetainedReason>,
        errno P0 opt: Errno,
    }
}

impl SupervisionScratchRetained {
    /// `io-failure`, with the failing call's actual errno (LD-D3A-17).
    pub fn io_failure(role: Code<ProviderRole>, universe: Universe, errno: Errno) -> Self {
        Self::new(
            role,
            universe,
            Code::from_enum(ScratchRetainedReason::IoFailure),
            Some(errno),
        )
    }
    /// `work-exhausted`: the removal walk's budget ran out; no errno exists.
    pub fn work_exhausted(role: Code<ProviderRole>, universe: Universe) -> Self {
        Self::new(
            role,
            universe,
            Code::from_enum(ScratchRetainedReason::WorkExhausted),
            None,
        )
    }
    /// `root-unreaped`: the root was abandoned at the reap ceiling and may
    /// still run in its scratch; no errno exists (LD-D3A-18).
    pub fn root_unreaped(role: Code<ProviderRole>, universe: Universe) -> Self {
        Self::new(
            role,
            universe,
            Code::from_enum(ScratchRetainedReason::RootUnreaped),
            None,
        )
    }
}

// M3-D r5 item 21 names this event `supervision.settled`, two segments,
// which S-OP-2 item 2's grammar refuses (exactly three: domain, object,
// action). It is registered as `supervision.child.settled` (LD-D3A3-11).

supervision_event! {
    struct SupervisionSettled;
    name: "supervision.child.settled";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "supervision settled";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        cause P0 req: Code<TeardownCause>,
        admissible P0 req: Flag,
        user_interrupted P0 req: Flag,
    }
}

// The tool class (M3-D r5 item 21, :692): Project only, because a tool runs
// before PlanId. Item 21 names no fields; these are D3a-3's ordinary fields
// (SOP2 item 3), with no `signal` until a `Signal` table resolves.
supervision_event! {
    struct ToolProcessSpawned;
    name: "tool.process.spawned";
    level: Level::Info;
    requires: IdentitySet::Project;
    export: false;
    template: "tool process spawned";
    constructor: pub fields: {
        pid P1 req: ProcessId,
    }
}

supervision_event! {
    struct ToolProcessReaped;
    name: "tool.process.reaped";
    level: Level::Info;
    requires: IdentitySet::Project;
    export: false;
    template: "tool process reaped";
    constructor: pub(crate) fields: {
        pid P1 req: ProcessId,
        exit_class P0 req: Code<ExitClass>,
        // D3a-4: S-OP-2c's `ChildSignal` (LD-OPT-4 "also usable by").
        signal P0 opt: Code<ChildSignal>,
        max_rss_native P0 req: Count,
        rss_unit P0 req: Code<RssUnit>,
        max_rss_bytes P0 opt: Bytes,
        cpu P0 req: Elapsed,
    }
}

impl ToolProcessReaped {
    /// The one builder: `signal` follows from `exit` (S-OP-2c item 23a).
    pub fn of(pid: ProcessId, exit: ReapedExit, usage: ReapedUsage) -> Self {
        let (class, signal) = match exit {
            ReapedExit::Exited => (ExitClass::Exited, None),
            ReapedExit::Signaled(signal) => (ExitClass::Signaled, signal.map(Code::from_enum)),
        };
        Self::new(
            pid,
            Code::from_enum(class),
            signal,
            usage.max_rss_native,
            Code::from_enum(usage.rss_unit),
            usage.max_rss_bytes,
            usage.cpu,
        )
    }
}

// r2 (Codex D3A3-R1-RF-1): a tool's own supervision records. A tool runs
// before PlanId and has no provider role or universe (item 21, :692), so the
// supervision records it produces are D3a-3's ordinary Project-only
// registrations here, never the provider-identity `supervision.*` ones.
supervision_event! {
    struct ToolLimitBreached;
    name: "tool.limit.breached";
    level: Level::Warn;
    requires: IdentitySet::Project;
    export: false;
    template: "tool limit breached";
    constructor: pub fields: {
        limit P0 req: Code<LimitKind>,
        observed P0 req: Count,
        unit P0 req: Code<LimitUnit>,
    }
}

supervision_event! {
    struct ToolSampleIncomplete;
    name: "tool.sample.incomplete";
    level: Level::Warn;
    requires: IdentitySet::Project;
    export: false;
    template: "tool resource sample incomplete";
    constructor: pub fields: {
        listed P0 req: Count,
        unsampled P0 req: Count,
        listing_failed P0 req: Flag,
    }
}

supervision_event! {
    struct ToolWaitExpired;
    name: "tool.wait.expired";
    level: Level::Warn;
    requires: IdentitySet::Project;
    export: false;
    template: "tool wait expired";
    constructor: pub fields: {
        wait P0 req: Code<BoundedWait>,
        limit P0 req: Elapsed,
    }
}

supervision_event! {
    struct ToolTeardownStarted;
    name: "tool.teardown.started";
    level: Level::Info;
    requires: IdentitySet::Project;
    export: false;
    template: "tool teardown started";
    constructor: pub fields: {
        cause P0 req: Code<TeardownCause>,
    }
}

supervision_event! {
    struct ToolScratchRetained;
    name: "tool.scratch.retained";
    level: Level::Warn;
    requires: IdentitySet::Project;
    export: false;
    template: "tool scratch retained";
    constructor: pub(crate) fields: {
        reason P0 req: Code<ScratchRetainedReason>,
        errno P0 opt: Errno,
    }
}

impl ToolScratchRetained {
    /// `io-failure`, with the failing call's actual errno (LD-D3A-17).
    pub fn io_failure(errno: Errno) -> Self {
        Self::new(
            Code::from_enum(ScratchRetainedReason::IoFailure),
            Some(errno),
        )
    }
    /// `work-exhausted`: no errno exists.
    pub fn work_exhausted() -> Self {
        Self::new(Code::from_enum(ScratchRetainedReason::WorkExhausted), None)
    }
    /// `root-unreaped`: no errno exists (LD-D3A-18).
    pub fn root_unreaped() -> Self {
        Self::new(Code::from_enum(ScratchRetainedReason::RootUnreaped), None)
    }
}

supervision_event! {
    struct ToolChildSettled;
    name: "tool.child.settled";
    level: Level::Info;
    requires: IdentitySet::Project;
    export: false;
    template: "tool settled";
    constructor: pub fields: {
        cause P0 req: Code<TeardownCause>,
        user_interrupted P0 req: Flag,
    }
}

// ------------------------------------------------------------------ M3-D unit D3a-4: the four unblocked events
//
// S-OP-2c item 23a (contract successor 177) fixes the four tables S-OP-2 item
// 23 named without members, so D3a-3's four blocked events are registered
// here (LD-D3A-10). Only the tables D3's events use are registered
// (LD-D3A4-1): `Signal` (COMMON4 `D9Signal`) is `host.signal.received`'s,
// left to its owner.

// S-OP-2c LD-OPT-1, protocol-enum: the stage `operator` const of TS2
// `StageRequestV1` and Rust3 `PlanStageV3` (generated
// `Ts2StageRequestV1Field2Value`, `Rust3C2PlanStageV3Field5Value`).
code_table!(StageKind, cap 64, {
    SemanticProvider => "semantic-provider",
});
// S-OP-2c LD-OPT-2, protocol-enum: P3T's `phases`, in order (T2O's are a
// subset).
code_table!(ProviderState, cap 64, {
    Start => "START",
    WaitHelloAck => "WAIT_HELLO_ACK",
    ReadyOpenUniverse => "READY_OPEN_UNIVERSE",
    WaitUniverseAccepted => "WAIT_UNIVERSE_ACCEPTED",
    ReadySnapshotManifest => "READY_SNAPSHOT_MANIFEST",
    ReceivingSnapshot => "RECEIVING_SNAPSHOT",
    WaitSnapshotAccepted => "WAIT_SNAPSHOT_ACCEPTED",
    ReadyDependencyManifest => "READY_DEPENDENCY_MANIFEST",
    ReceivingDependency => "RECEIVING_DEPENDENCY",
    WaitDependencyAccepted => "WAIT_DEPENDENCY_ACCEPTED",
    ReadyPreparedManifest => "READY_PREPARED_MANIFEST",
    ReceivingPrepared => "RECEIVING_PREPARED",
    WaitPreparedAccepted => "WAIT_PREPARED_ACCEPTED",
    WaitNativeContextVerified => "WAIT_NATIVE_CONTEXT_VERIFIED",
    ReadyAnalyze => "READY_ANALYZE",
    Analyzing => "ANALYZING",
    ReadyComplete => "READY_COMPLETE",
    WaitCancelled => "WAIT_CANCELLED",
    WaitZeroExit => "WAIT_ZERO_EXIT",
    WaitEof => "WAIT_EOF",
    Done => "DONE",
    Fault => "FAULT",
});
// S-OP-2c LD-OPT-4, registry-literal: the chosen common subset of the POSIX
// terminating signals (default action T or A) that every supported platform
// defines, less `SIGPOLL` (SOP2C-R1-NBO-1). A raw number maps to a member
// only by the platform's pinned `libc` constant.
code_table!(ChildSignal, cap 64, {
    Sigabrt => "SIGABRT",
    Sigalrm => "SIGALRM",
    Sigbus => "SIGBUS",
    Sigfpe => "SIGFPE",
    Sighup => "SIGHUP",
    Sigill => "SIGILL",
    Sigint => "SIGINT",
    Sigkill => "SIGKILL",
    Sigpipe => "SIGPIPE",
    Sigprof => "SIGPROF",
    Sigquit => "SIGQUIT",
    Sigsegv => "SIGSEGV",
    Sigsys => "SIGSYS",
    Sigterm => "SIGTERM",
    Sigtrap => "SIGTRAP",
    Sigusr1 => "SIGUSR1",
    Sigusr2 => "SIGUSR2",
    Sigvtalrm => "SIGVTALRM",
    Sigxcpu => "SIGXCPU",
    Sigxfsz => "SIGXFSZ",
});
// S-OP-2c LD-OPT-5, protocol-enum: the union of the admitted `Unavailable`
// reasons (`PreAnalyzeUnavailableV1`, TS2 `TypeScriptUnavailableV2`, Rust3
// `UnavailableV3`).
code_table!(ProviderReason, cap 64, {
    CapabilityMissing => "capability-missing",
    DependencySourceIncomplete => "dependency-source-incomplete",
    GeneratedCfgUnavailable => "generated-cfg-unavailable",
    IdentityVersionMismatch => "identity-version-mismatch",
    NativeContextMismatch => "native-context-mismatch",
    NodeModulesOutsideReadSet => "node-modules-outside-read-set",
    PreparedOutputNotInert => "prepared-output-not-inert",
    PreparedOutputStale => "prepared-output-stale",
    SemanticUniverseIncomplete => "semantic-universe-incomplete",
    SnapshotResolutionInputMissing => "snapshot-resolution-input-missing",
    UnsupportedCompilerMode => "unsupported-compiler-mode",
});
// SOP2:880 (NE:2025), protocol-enum: the generated `Native2StageTerminal`.
code_table!(StageTerminal, cap 64, {
    Complete => "complete",
    Unavailable => "unavailable",
    BudgetExhausted => "budget-exhausted",
    ProviderFault => "provider-fault",
    Cancelled => "cancelled",
    Crash => "crash",
});

supervision_event! {
    struct ProviderStageChanged;
    name: "provider.stage.changed";
    level: Level::Debug;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "provider stage changed";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        stage P0 req: Code<StageKind>,
        state P0 req: Code<ProviderState>,
    }
}

supervision_event! {
    struct ProviderStageTerminal;
    name: "provider.stage.terminal";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: true;
    template: "provider stage terminal";
    constructor: pub(crate) fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        stage P0 req: Code<StageKind>,
        terminal P0 req: Code<StageTerminal>,
        reason P0 opt: Code<ProviderReason>,
        fact_frames P0 req: Count,
        coverage_frames P0 req: Count,
        analysis P0 req: Elapsed,
    }
}

/// `reason` is present exactly when `terminal` is `unavailable` (S-OP-2c item
/// 23a), so these are the only builders.
impl ProviderStageTerminal {
    /// An `unavailable` terminal, with its admitted reason.
    pub fn unavailable(
        role: Code<ProviderRole>,
        universe: Universe,
        reason: Code<ProviderReason>,
        frames: (Count, Count),
        analysis: Elapsed,
    ) -> Self {
        Self::new(
            role,
            universe,
            Code::from_enum(StageKind::SemanticProvider),
            Code::from_enum(StageTerminal::Unavailable),
            Some(reason),
            frames.0,
            frames.1,
            analysis,
        )
    }
    /// Any other terminal, which carries no reason; `None` for `unavailable`.
    pub fn other(
        role: Code<ProviderRole>,
        universe: Universe,
        terminal: StageTerminal,
        frames: (Count, Count),
        analysis: Elapsed,
    ) -> Option<Self> {
        (terminal != StageTerminal::Unavailable).then(|| {
            Self::new(
                role,
                universe,
                Code::from_enum(StageKind::SemanticProvider),
                Code::from_enum(terminal),
                None,
                frames.0,
                frames.1,
                analysis,
            )
        })
    }
}

supervision_event! {
    struct ProviderProcessReaped;
    name: "provider.process.reaped";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "provider process reaped";
    constructor: pub(crate) fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        pid P1 req: ProcessId,
        exit_class P0 req: Code<ExitClass>,
        signal P0 opt: Code<ChildSignal>,
        max_rss_native P0 req: Count,
        rss_unit P0 req: Code<RssUnit>,
        max_rss_bytes P0 opt: Bytes,
        cpu P0 req: Elapsed,
        teardown P0 req: Elapsed,
    }
}

/// What a reaped child's status says: an exit, or a signal (its member, or
/// none when the number is no member's, S-OP-2c item 23a). `signal` is
/// present only for `signaled`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ReapedExit {
    Exited,
    Signaled(Option<ChildSignal>),
}
/// The rusage part of a reap record: the raw `ru_maxrss` in its native unit,
/// its conversion to bytes when it exists, and the CPU.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ReapedUsage {
    pub max_rss_native: Count,
    pub rss_unit: RssUnit,
    pub max_rss_bytes: Option<Bytes>,
    pub cpu: Elapsed,
}

impl ProviderProcessReaped {
    /// The one builder: `signal` follows from `exit`.
    pub fn of(
        role: Code<ProviderRole>,
        universe: Universe,
        pid: ProcessId,
        exit: ReapedExit,
        usage: ReapedUsage,
        teardown: Elapsed,
    ) -> Self {
        let (class, signal) = match exit {
            ReapedExit::Exited => (ExitClass::Exited, None),
            ReapedExit::Signaled(signal) => (ExitClass::Signaled, signal.map(Code::from_enum)),
        };
        Self::new(
            role,
            universe,
            pid,
            Code::from_enum(class),
            signal,
            usage.max_rss_native,
            Code::from_enum(usage.rss_unit),
            usage.max_rss_bytes,
            usage.cpu,
            teardown,
        )
    }
}

supervision_event! {
    struct SupervisionProgressAbsent;
    name: "supervision.progress.absent";
    level: Level::Info;
    requires: IdentitySet::ProjectPlanExecution;
    export: false;
    template: "progress absent";
    constructor: pub fields: {
        role P0 req: Code<ProviderRole>,
        universe P1 req: Universe,
        stage P0 req: Code<StageKind>,
        since P0 req: Elapsed,
    }
}

// ------------------------------------------------------------------ M3-D unit D3b-1: a tool's tree sweep
//
// D3b plan r3, LD-D3B-9 (an ordinary registration, SOP2 item 3; D3a-3 r2's
// RF-1 rule): a tool has only a Project, so its sweep record is
// `supervision.tree.swept`'s fields without `role` and `universe`.

supervision_event! {
    struct ToolTreeSwept;
    name: "tool.tree.swept";
    level: Level::Info;
    requires: IdentitySet::Project;
    export: false;
    template: "tool tree swept";
    constructor: pub fields: {
        killed P0 req: Count,
        unattributed P0 req: Count,
        platform_limited P0 req: Flag,
    }
}

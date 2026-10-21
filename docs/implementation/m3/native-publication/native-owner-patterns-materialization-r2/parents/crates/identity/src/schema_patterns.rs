//! Exploratory closed-pattern predicates. Not selected product schema admission.
//! Pure over str, no allocation, regex engine, backtracking or ambient effects.
#[derive(Clone, Copy)]
enum Kind {
    NonLfFinal,
    CanonicalText(bool),
    SubjectId,
    Hex(&'static str, usize),
    HexPair,
    HexEven,
    Uuid,
    DotSegment,
    NegativePath(bool),
    CanonicalPath(bool),
    Segments255,
    NoBackslashNul,
    SafeText(bool),
    AsciiFilename,
    UpperTag,
    LowerLoose,
    LowerSeparated(bool),
    Camel,
    DefSelector,
    SlashTags,
    Semver(bool),
    Custody,
    Enforcement,
    LongFlag,
    ReportDisposition,
    Date(bool),
    RunOrClosure,
    SecurityWildcard(bool),
}
const TABLE: &[(&str, Kind)] = &[
    (r##"^.+$"##, Kind::NonLfFinal),
    (r##"(^|/)\.\.?(/|$)"##, Kind::DotSegment),
    (r##"^#/\$defs/[A-Za-z0-9]+(?![\s\S])"##, Kind::DefSelector),
    (r##"^(/[A-Za-z0-9-]+)+(?![\s\S])"##, Kind::SlashTags),
    (
        r##"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(\.(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(?![\s\S])"##,
        Kind::Semver(true),
    ),
    (
        r##"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(?:(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?![\s\S])"##,
        Kind::Semver(true),
    ),
    (
        r##"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?(?![\s\S])"##,
        Kind::Semver(false),
    ),
    (
        r##"^(?!/)(?!.*(^|/)\.\.?(/|$))[^\u0000\\]*(?![\s\S])"##,
        Kind::NegativePath(true),
    ),
    (
        r##"^(?!/)(?!.*(^|/)\.\.?(/|$))[^\u0000\\]+(?![\s\S])"##,
        Kind::NegativePath(false),
    ),
    (
        r##"^(?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+(/(?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+)*(?![\s\S])"##,
        Kind::CanonicalPath(false),
    ),
    (
        r##"^(?:|(?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+(/(?!\.\.?(?:/|(?![\s\S])))[^\u0000\\/]+)*)(?![\s\S])"##,
        Kind::CanonicalPath(true),
    ),
    (
        r##"^(DIRECTORY_CUSTODY:[A-Z_]+|MARKER_CUSTODY:(Cargo\.toml|package\.json|tsconfig\.json|jsconfig\.json):[A-Z_]+|DEPTH)(?![\s\S])"##,
        Kind::Custody,
    ),
    (
        r##"^(DISCLOSURE-ONLY|ENFORCED-BY-CONSTRUCTION|ENFORCED-AT-HOST-BROKER|ENFORCED-PLATFORM:[a-z0-9.-]{1,64})(?![\s\S])"##,
        Kind::Enforcement,
    ),
    (r##"^([0-9a-f]{2})+(?![\s\S])"##, Kind::HexEven),
    (r##"^([0-9a-f]{40}|[0-9a-f]{64})(?![\s\S])"##, Kind::HexPair),
    (
        r##"^(run3|closure2):[0-9a-f]{64}(?![\s\S])"##,
        Kind::RunOrClosure,
    ),
    (r##"^--[a-z][a-z0-9-]*(?![\s\S])"##, Kind::LongFlag),
    (r##"^RP-DO-[0-9]{2}(?![\s\S])"##, Kind::ReportDisposition),
    (
        r##"^[0-9]{4}-[0-9]{2}-[0-9]{2}(?![\s\S])"##,
        Kind::Date(false),
    ),
    (
        r##"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z(?![\s\S])"##,
        Kind::Date(true),
    ),
    (r##"^[0-9a-f]{128}(?![\s\S])"##, Kind::Hex("", 128)),
    (r##"^[0-9a-f]{40}(?![\s\S])"##, Kind::Hex("", 40)),
    (r##"^[0-9a-f]{64}(?![\s\S])"##, Kind::Hex("", 64)),
    (
        r##"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?![\s\S])"##,
        Kind::Uuid,
    ),
    (r##"^[A-Z_][A-Z0-9_]*(?![\s\S])"##, Kind::UpperTag),
    (r##"^[A-Za-z0-9_.-]+(?![\s\S])"##, Kind::AsciiFilename),
    (
        r##"^[^/\\\u0000]{1,255}(/[^/\\\u0000]{1,255})*(?![\s\S])"##,
        Kind::Segments255,
    ),
    (r##"^[^\\\u0000]+(?![\s\S])"##, Kind::NoBackslashNul),
    (
        r##"^[^\u0000-\u001f\u007f-\u009f\u061c\u200e\u200f\u2028-\u202e\u2066-\u2069]+(?![\s\S])"##,
        Kind::SafeText(true),
    ),
    (
        r##"^[^\u0000-\u001f\u0080-\u009f]+(?![\s\S])"##,
        Kind::SafeText(false),
    ),
    (r##"^[a-z][a-z0-9._:-]*(?![\s\S])"##, Kind::LowerLoose),
    (
        r##"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*(?![\s\S])"##,
        Kind::LowerSeparated(false),
    ),
    (
        r##"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*(?![\s\S])"##,
        Kind::LowerSeparated(true),
    ),
    (r##"^[a-z][a-zA-Z0-9]*(?![\s\S])"##, Kind::Camel),
    (
        r##"^baseline2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("baseline2:", 64),
    ),
    (
        r##"^candidate2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("candidate2:", 64),
    ),
    (
        r##"^closure2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("closure2:", 64),
    ),
    (
        r##"^comparison2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("comparison2:", 64),
    ),
    (
        r##"^coverage2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("coverage2:", 64),
    ),
    (
        r##"^evidence2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("evidence2:", 64),
    ),
    (
        r##"^evidence3:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("evidence3:", 64),
    ),
    (
        r##"^exec-plan2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("exec-plan2:", 64),
    ),
    (
        r##"^exec1_[0-9a-f]{32}(?![\s\S])"##,
        Kind::Hex("exec1_", 32),
    ),
    (
        r##"^fact2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("fact2:", 64),
    ),
    (
        r##"^finding-key2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("finding-key2:", 64),
    ),
    (
        r##"^finding3:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("finding3:", 64),
    ),
    (
        r##"^import2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("import2:", 64),
    ),
    (
        r##"^owner1:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("owner1:", 64),
    ),
    (
        r##"^plan2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("plan2:", 64),
    ),
    (
        r##"^policytest2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("policytest2:", 64),
    ),
    (r##"^prj1-[0-9a-f]{64}(?![\s\S])"##, Kind::Hex("prj1-", 64)),
    (
        r##"^proof3:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("proof3:", 64),
    ),
    (
        r##"^receipt2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("receipt2:", 64),
    ),
    (
        r##"^repairplan2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("repairplan2:", 64),
    ),
    (r##"^req1_[0-9a-f]{32}(?![\s\S])"##, Kind::Hex("req1_", 32)),
    (r##"^run2:[0-9a-f]{64}(?![\s\S])"##, Kind::Hex("run2:", 64)),
    (r##"^run3:[0-9a-f]{64}(?![\s\S])"##, Kind::Hex("run3:", 64)),
    (
        r##"^scope2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("scope2:", 64),
    ),
    (
        r##"^seal3:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("seal3:", 64),
    ),
    (
        r##"^security.repo-execution-grant.v2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::SecurityWildcard(false),
    ),
    (
        r##"^security.repo-execution-grants.v2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::SecurityWildcard(true),
    ),
    (
        r##"^security\.installation-transition-journal\.v1:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("security.installation-transition-journal.v1:", 64),
    ),
    (
        r##"^security\.repair-apply-authorization\.v1:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("security.repair-apply-authorization.v1:", 64),
    ),
    (
        r##"^security\.repair-apply-journal-identity\.v1:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("security.repair-apply-journal-identity.v1:", 64),
    ),
    (
        r##"^security\.repair-recovery-authorization\.v1:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("security.repair-recovery-authorization.v1:", 64),
    ),
    (
        r##"^sha256:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("sha256:", 64),
    ),
    (
        r##"^snapshot2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("snapshot2:", 64),
    ),
    (
        r##"^subject3:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("subject3:", 64),
    ),
    (
        r##"^view2:[0-9a-f]{64}(?![\s\S])"##,
        Kind::Hex("view2:", 64),
    ),
    (
        r#"^[^\u0000-\u001f\u007f-\u009f]*(?![\s\S])"#,
        Kind::CanonicalText(true),
    ),
    (
        r#"^[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])"#,
        Kind::CanonicalText(false),
    ),
    (
        r#"^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+(?![\s\S])"#,
        Kind::SubjectId,
    ),
];

pub fn matches(pattern: &str, value: &str) -> Result<bool, &'static str> {
    let kind = TABLE
        .iter()
        .find(|row| row.0 == pattern)
        .map(|row| row.1)
        .ok_or("unselected pattern")?;
    Ok(match kind {
        Kind::CanonicalText(empty) => (empty || !value.is_empty()) && canonical_text(value),
        Kind::SubjectId => value.split_once(':').is_some_and(|(prefix,body)| prefix.as_bytes().first().is_some_and(u8::is_ascii_lowercase) && prefix.bytes().all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b==b'-') && !body.is_empty() && canonical_text(body)),
        Kind::NonLfFinal => { let v=value.strip_suffix('\n').unwrap_or(value); !v.is_empty() && !v.contains('\n') },
        Kind::Hex(prefix, n) => value.strip_prefix(prefix).is_some_and(|s| hex(s, n)),
        Kind::HexPair => hex(value, 40) || hex(value, 64),
        Kind::HexEven => !value.is_empty() && value.len().is_multiple_of(2) && value.bytes().all(lower_hex),
        Kind::Uuid => value.len()==36 && value.bytes().enumerate().all(|(i,b)| if [8,13,18,23].contains(&i) { b==b'-' } else { lower_hex(b) }),
        Kind::DotSegment => dot_segment(value, false),
        Kind::NegativePath(empty) => (empty || !value.is_empty()) && !value.starts_with('/') && !value.contains(['\0','\\']) && !dot_segment(value, true),
        Kind::CanonicalPath(empty) => (empty && value.is_empty()) || (!value.is_empty() && !value.contains(['\0','\\']) && value.split('/').all(|s| !matches!(s,""|"."|".."))),
        Kind::Segments255 => !value.contains(['\0','\\']) && value.split('/').all(|s| !s.is_empty() && s.chars().take(256).count()<=255),
        Kind::NoBackslashNul => !value.is_empty() && !value.contains(['\0','\\']),
        Kind::SafeText(broad) => !value.is_empty() && value.chars().all(|c| {
            let n=u32::from(c);
            if broad { !matches!(n,0..=0x1f | 0x7f..=0x9f | 0x61c | 0x200e | 0x200f | 0x2028..=0x202e | 0x2066..=0x2069) }
            else { !matches!(n,0..=0x1f | 0x80..=0x9f) }
        }),
        Kind::AsciiFilename => ascii_nonempty(value, |b| b.is_ascii_alphanumeric() || matches!(b,b'_'|b'.'|b'-')),
        Kind::UpperTag => value.as_bytes().first().is_some_and(|b| b.is_ascii_uppercase() || *b==b'_') && value.bytes().all(|b| b.is_ascii_uppercase() || b.is_ascii_digit() || b==b'_'),
        Kind::LowerLoose => value.as_bytes().first().is_some_and(u8::is_ascii_lowercase) && value.bytes().all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || matches!(b,b'.'|b'_'|b':'|b'-')),
        Kind::LowerSeparated(colon) => lower_separated(value,colon),
        Kind::Camel => value.as_bytes().first().is_some_and(u8::is_ascii_lowercase) && value.bytes().all(|b| b.is_ascii_alphanumeric()),
        Kind::DefSelector => value.strip_prefix("#/$defs/").is_some_and(|s| ascii_nonempty(s, |b| b.is_ascii_alphanumeric())),
        Kind::SlashTags => value.strip_prefix('/').is_some_and(|s| s.split('/').all(|part| ascii_nonempty(part, |b| b.is_ascii_alphanumeric() || b==b'-'))),
        Kind::Semver(strict) => semver(value,strict),
        Kind::Custody => custody(value),
        Kind::Enforcement => matches!(value,"DISCLOSURE-ONLY"|"ENFORCED-BY-CONSTRUCTION"|"ENFORCED-AT-HOST-BROKER") || value.strip_prefix("ENFORCED-PLATFORM:").is_some_and(|s| s.len()<=64 && ascii_nonempty(s, |b| b.is_ascii_lowercase() || b.is_ascii_digit() || matches!(b,b'.'|b'-'))),
        Kind::LongFlag => value.strip_prefix("--").is_some_and(|s| s.as_bytes().first().is_some_and(u8::is_ascii_lowercase) && s.bytes().all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b==b'-')),
        Kind::ReportDisposition => value.strip_prefix("RP-DO-").is_some_and(|s| s.len()==2 && s.bytes().all(|b| b.is_ascii_digit())),
        Kind::Date(time) => date(value,time),
        Kind::RunOrClosure => ["run3:","closure2:"].iter().any(|p| value.strip_prefix(p).is_some_and(|s| hex(s,64))),
        Kind::SecurityWildcard(plural) => security_wildcard(value,plural),
    })
}
fn lower_hex(b: u8) -> bool {
    b.is_ascii_digit() || matches!(b, b'a'..=b'f')
}
fn hex(s: &str, n: usize) -> bool {
    s.len() == n && s.bytes().all(lower_hex)
}
fn ascii_nonempty(s: &str, f: impl Fn(u8) -> bool) -> bool {
    !s.is_empty() && s.bytes().all(f)
}
fn dot_segment(s: &str, prefix_only: bool) -> bool {
    let limit = if prefix_only {
        s.find('\n').unwrap_or(s.len())
    } else {
        s.len()
    };
    let mut offset = 0;
    for part in s.split('/') {
        if offset > limit {
            return false;
        }
        let last = offset + part.len() == s.len();
        if matches!(part, "." | "..")
            || (last
                && part
                    .strip_suffix('\n')
                    .is_some_and(|p| matches!(p, "." | "..")))
        {
            return true;
        }
        offset += part.len() + 1;
    }
    false
}
fn lower_separated(s: &str, colon: bool) -> bool {
    if !s.as_bytes().first().is_some_and(u8::is_ascii_lowercase) {
        return false;
    }
    let mut separator = false;
    for b in s.bytes() {
        if b.is_ascii_lowercase() || b.is_ascii_digit() {
            separator = false;
        } else if matches!(b, b'.' | b'_' | b'-') || (colon && b == b':') {
            if separator {
                return false;
            }
            separator = true;
        } else {
            return false;
        }
    }
    !separator
}
fn numeric(s: &str) -> bool {
    ascii_nonempty(s, |b| b.is_ascii_digit()) && (s == "0" || !s.starts_with('0'))
}
fn semver(s: &str, strict: bool) -> bool {
    let (version, build) = s.split_once('+').map_or((s, None), |(a, b)| (a, Some(b)));
    let identifiers = |text: &str, pre: bool| {
        text.split('.').all(|p| {
            ascii_nonempty(p, |b| b.is_ascii_alphanumeric() || b == b'-')
                && (!pre || !p.bytes().all(|b| b.is_ascii_digit()) || numeric(p))
        })
    };
    let loose = |text: &str| {
        ascii_nonempty(text, |b| {
            b.is_ascii_alphanumeric() || matches!(b, b'.' | b'-')
        })
    };
    if build.is_some_and(|b| {
        if strict {
            !identifiers(b, false)
        } else {
            !loose(b)
        }
    }) {
        return false;
    }
    let (core, pre) = version
        .split_once('-')
        .map_or((version, None), |(a, b)| (a, Some(b)));
    if pre.is_some_and(|p| {
        if strict {
            !identifiers(p, true)
        } else {
            !loose(p)
        }
    }) {
        return false;
    }
    let mut parts = core.split('.');
    (0..3).all(|_| parts.next().is_some_and(numeric)) && parts.next().is_none()
}
fn custody(s: &str) -> bool {
    let tag = |v: &str| ascii_nonempty(v, |b| b.is_ascii_uppercase() || b == b'_');
    s == "DEPTH"
        || s.strip_prefix("DIRECTORY_CUSTODY:").is_some_and(tag)
        || s.strip_prefix("MARKER_CUSTODY:").is_some_and(|v| {
            v.split_once(':').is_some_and(|(name, t)| {
                matches!(
                    name,
                    "Cargo.toml" | "package.json" | "tsconfig.json" | "jsconfig.json"
                ) && tag(t)
            })
        })
}
fn date(s: &str, time: bool) -> bool {
    if s.len() != if time { 20 } else { 10 } {
        return false;
    }
    s.bytes().enumerate().all(|(i, b)| match i {
        4 | 7 => b == b'-',
        10 => b == b'T',
        13 | 16 => b == b':',
        19 => b == b'Z',
        _ => b.is_ascii_digit(),
    })
}
fn wildcard(s: &str) -> Option<&str> {
    let c = s.chars().next()?;
    if c == '\n' {
        None
    } else {
        Some(&s[c.len_utf8()..])
    }
}
fn security_wildcard(s: &str, plural: bool) -> bool {
    let Some(s) = s.strip_prefix("security").and_then(wildcard) else {
        return false;
    };
    let Some(s) = s
        .strip_prefix(if plural {
            "repo-execution-grants"
        } else {
            "repo-execution-grant"
        })
        .and_then(wildcard)
    else {
        return false;
    };
    s.strip_prefix("v2:").is_some_and(|s| hex(s, 64))
}

fn canonical_text(s: &str) -> bool {
    s.chars()
        .all(|c| !matches!(u32::from(c),0..=0x1f | 0x7f..=0x9f))
}

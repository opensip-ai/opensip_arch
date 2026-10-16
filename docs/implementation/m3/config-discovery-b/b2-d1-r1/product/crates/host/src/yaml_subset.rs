// M3-B r9 item 16 (unit B2-d1, B2-d plan r3 section 2): the closed YAML
// subset reader for `pnpm-workspace.yaml`. Pure: it reads a byte slice and
// evaluates nothing (FW-01). There is no YAML dependency (item 16 rejects
// one for a single key, and M3-P0's policy has no YAML row).
//
// A document is inside the subset when it is UTF-8 of at most 64 KiB, with
// no byte order mark and no tab, whose only line breaks are LF or CRLF, and
// whose characters are YAML 1.2's c-printable set less DEL, the C1 block,
// NEL, U+2028, U+2029 and an inner byte order mark. Line by line it holds
// only blank lines, `#` comment lines, the single key `packages:` at column
// 0, and either the empty flow sequence (`packages: []`, separated by at
// least one space) or at least one block item: at least one space, `-`, at
// least one space, one scalar and an optional comment. A scalar is quoted
// (single, with `''`; double, with `\"` and `\\` only) or plain: no leading
// indicator, no `:`, and not a form a YAML parser would read as null, a
// boolean, a number or a date. Everything else is outside the subset, as
// one typed refusal and never a partial list: recognition then discloses
// `config-requires-evaluation` (FR-1). The bound B2-d0 reference
// (`parse_pnpm_packages`, contract successor 171) is the oracle.

/// The subset's own bound (B2-d plan r3 section 2).
pub(crate) const MAX_BYTES: usize = 64 * 1024;

/// Why a document is outside the subset. Every reason has the same effect.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum OutsideSubset {
    /// Over 64 KiB.
    Bound,
    /// Not UTF-8.
    NotUtf8,
    /// A byte order mark, a tab, a bare CR or another excluded character.
    Character,
    /// Not the `packages:` key with a sequence of scalars.
    Structure,
    /// A scalar outside the subset.
    Scalar,
}

const INDICATORS: &str = "-?:,[]{}#&*!|>'\"%@`";
/// Plain scalars a YAML 1.1 or 1.2 parser would not read as a string
/// (compared lowercase).
const RESERVED: [&str; 15] = [
    "", "~", "null", "true", "false", "yes", "no", "on", "off", "y", "n", ".inf", "-.inf", "+.inf",
    ".nan",
];

fn character_ok(ch: char) -> bool {
    let o = ch as u32;
    if ch == '\n' || (0x20..=0x7E).contains(&o) {
        return true;
    }
    if (0xA0..=0xD7FF).contains(&o) {
        return o != 0x2028 && o != 0x2029;
    }
    if (0xE000..=0xFFFD).contains(&o) {
        return o != 0xFEFF;
    }
    (0x10000..=0x10FFFF).contains(&o)
}

/// `( +#.*)?`: nothing, or at least one space then a comment.
fn comment_tail(after: &str) -> bool {
    let rest = after.trim_start_matches(' ');
    after.is_empty() || (rest.len() < after.len() && rest.starts_with('#'))
}

/// ` *( +#.*)?`: spaces only, or at least one space then a comment.
fn spaces_or_comment(after: &str) -> bool {
    let rest = after.trim_start_matches(' ');
    rest.is_empty() || (rest.len() < after.len() && rest.starts_with('#'))
}

/// `[-+]?([0-9][0-9a-fA-FxXoObB_.:eE+-]*|\.[0-9][0-9_eE+-]*)`.
fn numeric(value: &str) -> bool {
    let body = value
        .strip_prefix('-')
        .or_else(|| value.strip_prefix('+'))
        .unwrap_or(value);
    let mut chars = body.chars();
    match chars.next() {
        Some(c) if c.is_ascii_digit() => {
            chars.all(|c| c.is_ascii_hexdigit() || "xXoObB_.:eE+-".contains(c))
        }
        Some('.') => {
            matches!(chars.next(), Some(c) if c.is_ascii_digit())
                && chars.all(|c| c.is_ascii_digit() || "_eE+-".contains(c))
        }
        _ => false,
    }
}

/// `[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}([Tt ].*)?`.
fn date(value: &str) -> bool {
    let b = value.as_bytes();
    let digits = |from: usize, least: usize, most: usize| -> Option<usize> {
        let n = b[from..]
            .iter()
            .take(most)
            .take_while(|c| c.is_ascii_digit())
            .count();
        (n >= least).then_some(from + n)
    };
    let Some(i) = digits(0, 4, 4) else {
        return false;
    };
    if b.get(i) != Some(&b'-') {
        return false;
    }
    let Some(i) = digits(i + 1, 1, 2) else {
        return false;
    };
    if b.get(i) != Some(&b'-') {
        return false;
    }
    let Some(i) = digits(i + 1, 1, 2) else {
        return false;
    };
    i == b.len() || matches!(b[i], b'T' | b't' | b' ')
}

/// One scalar and an optional trailing comment.
fn scalar(rest: &str) -> Result<String, OutsideSubset> {
    if let Some(body) = rest.strip_prefix('\'') {
        let mut out = String::new();
        let mut i = 0;
        loop {
            let Some(j) = body[i..].find('\'') else {
                return Err(OutsideSubset::Scalar);
            };
            out.push_str(&body[i..i + j]);
            let after = &body[i + j + 1..];
            if let Some(next) = after.strip_prefix('\'') {
                out.push('\'');
                i = body.len() - next.len();
                continue;
            }
            return if comment_tail(after) {
                Ok(out)
            } else {
                Err(OutsideSubset::Scalar)
            };
        }
    }
    if let Some(body) = rest.strip_prefix('"') {
        let mut out = String::new();
        let mut chars = body.char_indices();
        while let Some((at, ch)) = chars.next() {
            match ch {
                '\\' => match chars.next() {
                    Some((_, escaped @ ('"' | '\\'))) => out.push(escaped),
                    _ => return Err(OutsideSubset::Scalar),
                },
                '"' => {
                    return if comment_tail(&body[at + 1..]) {
                        Ok(out)
                    } else {
                        Err(OutsideSubset::Scalar)
                    };
                }
                other => out.push(other),
            }
        }
        return Err(OutsideSubset::Scalar);
    }
    let value = match rest.find(" #") {
        Some(at) => &rest[..at],
        None => rest,
    }
    .trim_end_matches(' ');
    let first = value.chars().next();
    if first.is_none_or(|c| INDICATORS.contains(c))
        || value.contains(':')
        || RESERVED.contains(&value.to_lowercase().as_str())
        || numeric(value)
        || date(value)
    {
        return Err(OutsideSubset::Scalar);
    }
    Ok(value.to_owned())
}

#[derive(PartialEq, Eq)]
enum State {
    Before,
    Block,
    Closed,
}

/// The `packages:` globs of a `pnpm-workspace.yaml` inside the subset, in
/// order; `OutsideSubset` otherwise.
pub(crate) fn parse_pnpm_packages(raw: &[u8]) -> Result<Vec<String>, OutsideSubset> {
    if raw.len() > MAX_BYTES {
        return Err(OutsideSubset::Bound);
    }
    let text = std::str::from_utf8(raw).map_err(|_| OutsideSubset::NotUtf8)?;
    if text.starts_with('\u{feff}') || text.contains('\t') {
        return Err(OutsideSubset::Character);
    }
    // Only CRLF pairs are line breaks; any other CR is outside.
    let text = text.replace("\r\n", "\n");
    if text.contains('\r') || !text.chars().all(character_ok) {
        return Err(OutsideSubset::Character);
    }
    let mut state = State::Before;
    let mut indent = None;
    let mut out = Vec::new();
    for row in text.split('\n') {
        let stripped = row.trim_start_matches(' ');
        if stripped.is_empty() || stripped.starts_with('#') {
            continue;
        }
        match state {
            State::Before => {
                let Some(after) = row.strip_prefix("packages:") else {
                    return Err(OutsideSubset::Structure);
                };
                if comment_tail(after) {
                    state = State::Block;
                    continue;
                }
                let flow = after.trim_start_matches(' ');
                match flow.strip_prefix("[]") {
                    Some(tail) if flow.len() < after.len() && spaces_or_comment(tail) => {
                        state = State::Closed;
                    }
                    _ => return Err(OutsideSubset::Structure),
                }
            }
            State::Closed => return Err(OutsideSubset::Structure),
            State::Block => {
                let lead = row.len() - stripped.len();
                let Some(item) = stripped.strip_prefix('-') else {
                    return Err(OutsideSubset::Structure);
                };
                let rest = item.trim_start_matches(' ');
                if lead == 0 || rest.len() == item.len() {
                    return Err(OutsideSubset::Structure);
                }
                if *indent.get_or_insert(lead) != lead {
                    return Err(OutsideSubset::Structure);
                }
                out.push(scalar(rest)?);
            }
        }
    }
    match state {
        State::Before => Err(OutsideSubset::Structure),
        // A bare key, or one followed by comments only, is a null value.
        State::Block if out.is_empty() => Err(OutsideSubset::Structure),
        _ => Ok(out),
    }
}

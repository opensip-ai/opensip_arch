const KNOWN_CLI_MAIN_SOURCE: &str = r########"#![forbid(unsafe_code)]
mod arguments;
mod bootstrap;
mod terminal;
fn main() -> std::process::ExitCode {
    std::process::ExitCode::from(bootstrap::run(std::env::args_os().skip(1)))
}
"########;
const KNOWN_NONFEATURE_IMPORTS: &[&str] = &[
r########"use InstallationEntry::*;"########,
r########"use Observation as O;"########,
r########"use crate::arguments::{self, Request};"########,
r########"use crate::outcomes::{Format, MetadataError, RenderedResponse};"########,
r########"use crate::{DoctorOutcome, DoctorReportV1, InstallationTerminationV1};"########,
r########"use opensip_contracts::generated::evidence::{
    Common4D9Class as Class, Common4DomainDetailCode as Detail,
};"########,
r########"use opensip_contracts::generated::invocation::Inventory3CommandName as C;"########,
r########"use opensip_contracts::generated::output::Envelope7Root;"########,
r########"use opensip_host::{Format, MetadataRequest};"########,
r########"use opensip_host::{MetadataError, MetadataHost, finalize_invocation};"########,
r########"use serde_json::{Value, json};"########,
r########"use std::ffi::OsString;"########,
r########"use std::fmt::Write;"########,
r########"use std::io;"########,
r########"use std::os::fd::AsFd;"########,
r########"use std::{
    ffi::OsString,
    io::{self, Write},
};"########,
r########"use std::{collections::BTreeMap, sync::Arc};"########,
];
const KNOWN_EXPRESSION_MACROS: &[&str] = &["compile_error","format","json","matches","unreachable","vec","write","writeln"];

fn source_code_without_data(text: &str) -> Option<String> {
    let bytes = text.as_bytes();
    let mut code = bytes.to_vec();
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i..].starts_with(b"//") {
            let end = bytes[i..].iter().position(|b| *b == b'\n').map_or(bytes.len(), |n| i + n);
            code[i..end].fill(b' ');
            i = end;
            continue;
        }
        if bytes[i..].starts_with(b"/*") {
            let mut depth = 1;
            let mut end = i + 2;
            while end < bytes.len() && depth != 0 {
                if bytes[end..].starts_with(b"/*") { depth += 1; end += 2; }
                else if bytes[end..].starts_with(b"*/") { depth -= 1; end += 2; }
                else { end += 1; }
            }
            if depth != 0 { return None; }
            code[i..end].fill(b' ');
            i = end;
            continue;
        }
        // Only the already selected package-version query is allowed; an
        // env!("HOME") or CARGO_FEATURE query is not a logging permission.
        let version = b"env!(\"CARGO_PKG_VERSION\")";
        let mut before = i;
        while before > 0 && bytes[before-1].is_ascii_whitespace() { before -= 1; }
        if bytes[i..].starts_with(version) && (before == 0 || !matches!(bytes[before-1], b':' | b'#')) {
            code[i..i+version.len()].fill(b' ');
            i += version.len();
            continue;
        }
        let raw_prefix = if bytes[i..].starts_with(b"br") || bytes[i..].starts_with(b"cr") { 2 }
            else if bytes[i] == b'r' { 1 } else { 0 };
        if raw_prefix != 0 {
            let start = i + raw_prefix;
            let mut quote = start;
            while bytes.get(quote) == Some(&b'#') { quote += 1; }
            if bytes.get(quote) == Some(&b'"') {
                let hashes = &bytes[start..quote];
                let mut end = quote + 1;
                loop {
                    if end >= bytes.len() { return None; }
                    if bytes[end] == b'"' && bytes.get(end+1..end+1+hashes.len()) == Some(hashes) {
                        end += 1 + hashes.len();
                        break;
                    }
                    end += 1;
                }
                code[i..end].fill(b' ');
                i = end;
                continue;
            }
        }
        if bytes[i] == b'"' {
            let mut end = i + 1;
            loop {
                match bytes.get(end) {
                    None => return None,
                    Some(b'\\') => { if end + 1 >= bytes.len() { return None; } end += 2; }
                    Some(b'"') => { end += 1; break; }
                    Some(_) => end += 1,
                }
            }
            code[i..end].fill(b' ');
            i = end;
            continue;
        }
        if bytes[i] == b'\'' {
            let mut end = i + 1;
            if bytes.get(end) == Some(&b'\\') {
                end += 1;
                match bytes.get(end) {
                    Some(b'u') if bytes.get(end+1) == Some(&b'{') => {
                        end += 2;
                        while bytes.get(end).is_some_and(|b| b.is_ascii_hexdigit() || *b == b'_') { end += 1; }
                        if bytes.get(end) == Some(&b'}') { end += 1; }
                    }
                    Some(b'x') if bytes.get(end+1).is_some_and(u8::is_ascii_hexdigit)
                        && bytes.get(end+2).is_some_and(u8::is_ascii_hexdigit) => end += 3,
                    Some(_) => end += 1,
                    None => return None,
                }
            } else if let Some(c) = text.get(end..)?.chars().next() { end += c.len_utf8(); }
            if bytes.get(end) == Some(&b'\'') {
                end += 1;
                code[i..end].fill(b' ');
                i = end;
                continue;
            }
        }
        if bytes[i] == b'#' {
            let end = bytes[i..].iter().position(|b| *b == b'\n').map_or(bytes.len(), |n| i+n);
            let attribute = std::str::from_utf8(&bytes[i..end]).ok()?.trim_end();
            if [
                "#![forbid(unsafe_code)]", r#"#[cfg(target_os = "macos")]"#,
                r#"#[cfg(not(target_os = "macos"))]"#, "#[cfg(unix)]", "#[cfg(not(unix))]",
                "#[derive(Debug, Clone, Copy, PartialEq, Eq)]",
                "#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]",
                "#[derive(Debug, Clone, PartialEq, Eq)]",
                "#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]",
                "#[derive(Debug, PartialEq, Eq)]", "#[derive(Default)]",
            ].contains(&attribute) {
                code[i..end].fill(b' ');
                i = end;
                continue;
            }
        }
        if bytes[i].is_ascii_alphabetic() || bytes[i] == b'_' || bytes[i] >= 0x80 {
            i += 1;
            while i < bytes.len() && (bytes[i].is_ascii_alphanumeric() || bytes[i] == b'_' || bytes[i] >= 0x80) { i += 1; }
        } else { i += 1; }
    }
    String::from_utf8(code).ok()
}
fn expression_macros_are_closed(code: &str) -> bool {
    let bytes = code.as_bytes();
    for (i, b) in bytes.iter().enumerate() {
        if *b != b'!' { continue; }
        let mut next = i + 1;
        while bytes.get(next).is_some_and(u8::is_ascii_whitespace) { next += 1; }
        if !bytes.get(next).is_some_and(|b| matches!(b, b'(' | b'[' | b'{')) { continue; }
        let mut end = i;
        while end > 0 && bytes[end-1].is_ascii_whitespace() { end -= 1; }
        let mut start = end;
        while start > 0 && (bytes[start-1].is_ascii_alphanumeric() || bytes[start-1] == b'_' || bytes[start-1] >= 0x80) { start -= 1; }
        if start == end { continue; }
        let mut name = code[start..end].to_owned();
        loop {
            let mut before = start;
            while before > 0 && bytes[before-1].is_ascii_whitespace() { before -= 1; }
            if before < 2 || &bytes[before-2..before] != b"::" { break; }
            before -= 2;
            while before > 0 && bytes[before-1].is_ascii_whitespace() { before -= 1; }
            let previous_end = before;
            while before > 0 && (bytes[before-1].is_ascii_alphanumeric() || bytes[before-1] == b'_' || bytes[before-1] >= 0x80) { before -= 1; }
            if before == previous_end { name = format!("::{name}"); break; }
            name = format!("{}::{name}", &code[before..previous_end]);
            start = before;
        }
        if ["if", "while", "return", "break", "else", "match"].contains(&name.as_str()) { continue; }
        if !KNOWN_EXPRESSION_MACROS.contains(&name.as_str()) { return false; }
    }
    true
}

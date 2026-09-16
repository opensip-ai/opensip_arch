//! Private no_std NFC wrapper. Not product code.
#![no_std]
extern crate alloc;
use alloc::string::String;
use unicode_normalization::UnicodeNormalization;

pub fn nfc(s: &str) -> String {
    s.nfc().collect()
}

pub const UNICODE_VERSION: (u8, u8, u8) = unicode_normalization::UNICODE_VERSION;

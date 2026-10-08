//! RFC 1952 trailer arithmetic only; no source or read-completion authority.

const fn table() -> [u32; 256] {
    let mut values = [0; 256];
    let mut index = 0;
    while index < values.len() {
        let mut value = index as u32;
        let mut bit = 0;
        while bit < 8 {
            value = (value >> 1) ^ (0xedb8_8320 & 0_u32.wrapping_sub(value & 1));
            bit += 1;
        }
        values[index] = value;
        index += 1;
    }
    values
}

const CRC_TABLE: [u32; 256] = table();

pub(super) struct GzipChecksum {
    crc: u32,
    isize: u32,
}

impl GzipChecksum {
    pub(super) fn new() -> Self {
        Self {
            crc: u32::MAX,
            isize: 0,
        }
    }

    pub(super) fn update(&mut self, bytes: &[u8]) {
        for &byte in bytes {
            self.crc = CRC_TABLE[((self.crc ^ u32::from(byte)) & 0xff) as usize] ^ (self.crc >> 8);
        }
        // RFC 1952 ISIZE is the uncompressed length modulo 2^32.
        self.isize = self.isize.wrapping_add(bytes.len() as u32);
    }

    pub(super) fn trailer(&self) -> [u8; 8] {
        let mut trailer = [0; 8];
        trailer[..4].copy_from_slice(&(!self.crc).to_le_bytes());
        trailer[4..].copy_from_slice(&self.isize.to_le_bytes());
        trailer
    }
}

#[cfg(test)]
#[path = "gzip_checksum_tests.rs"]
mod tests;

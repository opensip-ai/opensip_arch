use super::GzipChecksum;

#[test]
fn independent_crc_vectors_and_chunk_boundaries_match() {
    let vectors: &[(usize, u32)] = &[
        (0, 0x00000000),
        (1, 0x4c667a2e),
        (7, 0x3e483922),
        (255, 0x50a22b05),
        (256, 0x0ce9d363),
        (257, 0x98d1a31f),
        (4095, 0x7b3f9134),
        (4096, 0x5d1c4ee3),
        (4097, 0x7538d5a2),
        (32767, 0x7d290604),
        (32768, 0x7bc368d8),
        (32769, 0xc415e3a0),
        (100000, 0x92858800),
    ];
    for &(length, expected) in vectors {
        let bytes: Vec<u8> = (0..length).map(|i| ((31 * i + 7) % 256) as u8).collect();
        for width in [1, 7, 255, 4096, 32768] {
            let mut checksum = GzipChecksum::new();
            checksum.update(&[]);
            for chunk in bytes.chunks(width) {
                checksum.update(chunk);
                checksum.update(&[]);
            }
            let mut trailer = [0; 8];
            trailer[..4].copy_from_slice(&expected.to_le_bytes());
            trailer[4..].copy_from_slice(&(length as u32).to_le_bytes());
            assert_eq!(checksum.trailer(), trailer, "{length}/{width}");
        }
    }
}

#[test]
fn standard_crc_check_value_and_empty_trailer_match() {
    let mut checksum = GzipChecksum::new();
    assert_eq!(checksum.trailer(), [0; 8]);
    checksum.update(b"123456789");
    assert_eq!(checksum.trailer(), [0x26, 0x39, 0xf4, 0xcb, 9, 0, 0, 0]);
}

#[test]
fn isize_wraps_as_a_trailer_field_without_claiming_a_giant_read() {
    let mut checksum = GzipChecksum::new();
    checksum.isize = u32::MAX - 1;
    checksum.update(b"abc");
    assert_eq!(&checksum.trailer()[4..], &1_u32.to_le_bytes());
    assert_eq!(&checksum.trailer()[..4], &0x3524_41c2_u32.to_le_bytes());
}

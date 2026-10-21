use super::{MAX_MESSAGE_BYTES, RawSha256, RawSha256LengthError};
use crate::{digest_hex, raw_sha256};
use alloc::vec::Vec;

// Independent Python hashlib oracles, fixed before running this implementation.
const VECTORS: &[(usize, &str)] = &[
    (
        0,
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ),
    (
        1,
        "ca358758f6d27e6cf45272937977a748fd88391db679ceda7dc7bf1f005ee879",
    ),
    (
        55,
        "8aa994584139d128848eeebc4e815639ba5ab6e6e39574195a63ac4f14f7c43b",
    ),
    (
        56,
        "ad574708f75c044c9b85de64cb568ee7711ff4f36448c6242f053ba8f6cc2b63",
    ),
    (
        63,
        "280ed3e8ff1df845b2e7dfe6ac6cee817bef20e783cc65abc41b818b4d2fe076",
    ),
    (
        64,
        "c6ab9724ade5b6a7a1edfffb12f3aa9181351355af8fd08c919952ad211339dd",
    ),
    (
        65,
        "788367c73c7ddf4c53f65e68cc0d943e6227ab55b0e78ba63ace822b1c6301c0",
    ),
    (
        127,
        "192409cd280e14b743642ad1343fbd3e82d9305de72c078117745a679210cc3d",
    ),
    (
        128,
        "cc548ca2dec1f6fe4f58b2e27aa9c7521607df1130d140b55a4dad0665302356",
    ),
    (
        129,
        "81e89a7b2911aaa7795f9e3d4910cb47d6cd2b00d83b8399481527261a1a7519",
    ),
    (
        4095,
        "e22f185103f5d75f22898e979206334d51aa47b9a01b6d835df0ec9000aac2e5",
    ),
    (
        4096,
        "d41d438c379110c7f7b2c561b1f04f26c1b4549110791f8e022f48974280c13e",
    ),
    (
        4097,
        "bb37fb3430fb3bc003f70512ee0189aec84b029b221885c8f16280d1b935483e",
    ),
    (
        32768,
        "611253a4531dea3d840789b4f11a1ad9c4329fbbf85ee1634f2ae601e6da6db0",
    ),
];

#[test]
fn independent_vectors_preserve_every_chunk_boundary_and_empty_updates() {
    for &(length, expected) in VECTORS {
        let input: Vec<u8> = (0..length).map(|i| ((i * 31 + 7) % 256) as u8).collect();
        assert_eq!(digest_hex(&raw_sha256(&input)), expected);
        for width in [1, 7, 55, 56, 63, 64, 65, 4096, 32768] {
            let mut stream = RawSha256::new().update(&[]).unwrap();
            for chunk in input.chunks(width) {
                stream = stream.update(chunk).unwrap().update(&[]).unwrap();
            }
            assert_eq!(stream.byte_length(), length as u64);
            assert_eq!(digest_hex(&stream.finish()), expected, "{length}/{width}");
        }
    }
}

#[test]
fn standard_short_and_million_byte_messages_need_no_whole_input_buffer() {
    assert_eq!(
        digest_hex(&RawSha256::default().finish()),
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    );
    let stream = RawSha256::new()
        .update(b"a")
        .unwrap()
        .update(b"b")
        .unwrap()
        .update(b"c")
        .unwrap();
    assert_eq!(
        digest_hex(&stream.finish()),
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    );
    let block = [b'a'; 1000];
    let mut stream = RawSha256::new();
    for _ in 0..1000 {
        stream = stream.update(&block).unwrap();
    }
    assert_eq!(stream.byte_length(), 1_000_000);
    assert_eq!(
        digest_hex(&stream.finish()),
        "cdc76e5c9914fb9281a1c7e284d73e67f1809a48a497200e046d39ccc7112cd0"
    );
}

#[test]
fn byte_count_is_exact_and_length_refusal_precedes_underlying_bit_overflow() {
    let mut stream = RawSha256::new();
    assert_eq!(stream.byte_length(), 0);
    for n in 0..129 {
        let bytes = alloc::vec![0; n];
        stream = stream.update(&bytes).unwrap();
        assert_eq!(stream.byte_length(), (n * (n + 1) / 2) as u64);
    }
    // Counter injection checks the guard only, not a physically read giant input.
    let stream = RawSha256 {
        byte_length: MAX_MESSAGE_BYTES - 1,
        ..RawSha256::new()
    };
    let stream = stream.update(b"a").unwrap();
    assert_eq!(stream.byte_length(), MAX_MESSAGE_BYTES);
    let stream = stream.update(&[]).unwrap();
    assert!(matches!(stream.update(b"b"), Err(RawSha256LengthError)));
    let stream = RawSha256 {
        byte_length: u64::MAX,
        ..RawSha256::new()
    };
    assert!(matches!(stream.update(b"x"), Err(RawSha256LengthError)));
}

#[test]
fn accumulator_storage_does_not_grow_with_message_length() {
    assert_eq!(
        core::mem::size_of::<RawSha256>(),
        core::mem::size_of::<sha2_const_stable::Sha256>() + core::mem::size_of::<u64>()
    );
}

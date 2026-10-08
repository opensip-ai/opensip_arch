use super::*;
use opensip_identity::raw_sha256;
use serde_json::Value;
use std::io::{self, Read};

#[derive(Default)]
struct Receiver {
    bytes: Vec<u8>,
    began: usize,
    ended: usize,
    checkpoints: usize,
    abort: bool,
}
impl ArchiveConsumer for Receiver {
    type Error = &'static str;
    fn checkpoint(&mut self) -> Result<(), Self::Error> {
        self.checkpoints += 1;
        if self.abort {
            Err("owning-abort")
        } else {
            Ok(())
        }
    }
    fn begin(&mut self, _: &LogicalPath, _: u128) -> Result<(), Self::Error> {
        self.began += 1;
        Ok(())
    }
    fn content(&mut self, bytes: &[u8]) -> Result<(), Self::Error> {
        self.bytes.extend_from_slice(bytes);
        Ok(())
    }
    fn end(&mut self, _: &FileRecord) -> Result<(), Self::Error> {
        self.ended += 1;
        Ok(())
    }
}
struct Short<'a> {
    bytes: &'a [u8],
    width: usize,
    largest: usize,
}
impl Read for Short<'_> {
    fn read(&mut self, out: &mut [u8]) -> io::Result<usize> {
        self.largest = self.largest.max(out.len());
        let n = self.bytes.len().min(out.len()).min(self.width);
        out[..n].copy_from_slice(&self.bytes[..n]);
        self.bytes = &self.bytes[n..];
        Ok(n)
    }
}
fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{b:02x}")).collect()
}

#[test]
fn independent_python_and_pinned_producer_fixtures_decode_completely_across_chunks() {
    let expected: Value = serde_json::from_str(include_str!("fixtures/expected.json")).unwrap();
    for (name, bytes) in [
        ("base", include_bytes!("fixtures/base.tar.gz").as_slice()),
        ("long", include_bytes!("fixtures/long.tar.gz").as_slice()),
        ("empty", include_bytes!("fixtures/empty.tar.gz").as_slice()),
        (
            "producer",
            include_bytes!("fixtures/producer.crate").as_slice(),
        ),
    ] {
        let wanted = &expected[name];
        for width in [1, 7, 511, 512, 4096, 32768] {
            let mut reader = Short {
                bytes,
                width,
                largest: 0,
            };
            let mut receiver = Receiver::default();
            let result = decode(
                &mut reader,
                wanted["packageName"].as_str().unwrap(),
                wanted["packageVersion"].as_str().unwrap(),
                &mut receiver,
            )
            .unwrap();
            assert!(reader.bytes.is_empty());
            assert!(reader.largest <= 4096);
            assert_eq!(
                hex(&result.compressed_sha256),
                wanted["compressedSha256"].as_str().unwrap()
            );
            assert_eq!(
                result.compressed_bytes,
                wanted["compressedBytes"].as_u64().unwrap()
            );
            assert_eq!(
                result.inflated_bytes,
                u128::from(wanted["inflatedBytes"].as_u64().unwrap())
            );
            assert_eq!(
                result.content_bytes,
                u128::from(wanted["contentBytes"].as_u64().unwrap())
            );
            let files = wanted["files"].as_array().unwrap();
            assert_eq!(result.files.len(), files.len());
            for (actual, expected) in result.files.iter().zip(files) {
                assert_eq!(actual.path.as_str(), expected["path"].as_str().unwrap());
                assert_eq!(actual.byte_length, expected["byteLength"].as_u64().unwrap());
                assert_eq!(
                    hex(&actual.content_sha256),
                    expected["contentSha256"].as_str().unwrap()
                );
            }
            assert_eq!(receiver.began, files.len());
            assert_eq!(receiver.ended, files.len());
            assert_eq!(receiver.bytes.len() as u128, result.content_bytes);
        }
    }
}
fn header(path: &[u8], kind: u8, length: u64) -> [u8; 512] {
    let mut h = [0; 512];
    let n = path.len().min(100);
    h[..n].copy_from_slice(&path[..n]);
    h[124..136].copy_from_slice(format!("{length:011o}\0").as_bytes());
    h[156] = kind;
    h[257..265].copy_from_slice(b"ustar  \0");
    fix_checksum(&mut h);
    h
}
fn fix_checksum(h: &mut [u8; 512]) {
    h[148..156].fill(b' ');
    let sum: u64 = h.iter().map(|b| u64::from(*b)).sum();
    h[148..156].copy_from_slice(format!("{sum:06o}\0 ").as_bytes());
}
fn append(tar: &mut Vec<u8>, h: [u8; 512], bytes: &[u8]) {
    tar.extend_from_slice(&h);
    tar.extend_from_slice(bytes);
    tar.extend(std::iter::repeat_n(0, (512 - bytes.len() % 512) % 512));
}
fn stored(tar: &[u8]) -> Vec<u8> {
    let mut gzip = vec![0x1f, 0x8b, 8, 0, 0, 0, 0, 0, 0, 255];
    let chunks = tar.chunks(65535);
    let count = chunks.len();
    for (index, chunk) in chunks.enumerate() {
        gzip.push(u8::from(index + 1 == count));
        let length = chunk.len() as u16;
        gzip.extend_from_slice(&length.to_le_bytes());
        gzip.extend_from_slice(&(!length).to_le_bytes());
        gzip.extend_from_slice(chunk);
    }
    if tar.is_empty() {
        gzip.extend_from_slice(&[1, 0, 0, 255, 255]);
    }
    // Independent slow recurrence in the fixture writer; positive CRC vectors
    // also come from Python zlib and complete gzip fixtures from Python gzip.
    let mut crc = u32::MAX;
    for &byte in tar {
        crc ^= u32::from(byte);
        for _ in 0..8 {
            crc = (crc >> 1) ^ if crc & 1 != 0 { 0xedb8_8320 } else { 0 };
        }
    }
    gzip.extend_from_slice(&(!crc).to_le_bytes());
    gzip.extend_from_slice(&(tar.len() as u32).to_le_bytes());
    gzip
}
fn profile(bytes: &[u8]) -> ProfileError {
    match decode(bytes, "unit", "1.0.0", &mut Receiver::default()) {
        Err(DecodeError::Profile(error)) => error,
        other => panic!("expected profile refusal: {other:?}"),
    }
}

#[test]
fn all_prefixes_trailers_flags_extra_members_and_tail_refuse() {
    let base = include_bytes!("fixtures/base.tar.gz");
    for n in 0..base.len() {
        assert!(
            decode(&base[..n], "unit", "1.0.0", &mut Receiver::default()).is_err(),
            "prefix{n}"
        );
    }
    for at in [base.len() - 8, base.len() - 4] {
        let mut b = base.to_vec();
        b[at] ^= 1;
        assert_eq!(profile(&b), ProfileError::GzipTrailer);
    }
    for flag in [2, 4, 16, 32, 64, 128] {
        let mut b = base.to_vec();
        b[3] = flag;
        assert_eq!(profile(&b), ProfileError::GzipHeader);
    }
    for tail in [vec![0], base.to_vec()] {
        let mut b = base.to_vec();
        b.extend(tail);
        assert_eq!(profile(&b), ProfileError::GzipTail);
    }
}

#[test]
fn selected_fname_boundary_includes_nul_and_chunk_boundaries_do_not_reset_it() {
    let base = include_bytes!("fixtures/empty.tar.gz");
    for length in [0, 4094, 4095, 4096] {
        let mut bytes = base.to_vec();
        bytes[3] = 9;
        bytes.splice(10..10, std::iter::repeat_n(b'x', length).chain([0]));
        for width in [1, 7, 4096] {
            let reader = Short {
                bytes: &bytes,
                width,
                largest: 0,
            };
            let result = decode(reader, "unit", "1.0.0", &mut Receiver::default());
            if length <= 4095 {
                assert!(result.is_ok());
            } else {
                assert!(matches!(
                    result,
                    Err(DecodeError::Profile(ProfileError::FnameBound))
                ));
            }
        }
    }
    let mut truncated = base[..10].to_vec();
    truncated[3] = 8;
    truncated.extend_from_slice(b"unterminated");
    assert_eq!(profile(&truncated), ProfileError::TruncatedGzip);
}

#[test]
fn tar_header_checksum_types_numeric_and_truncated_body_refuse_without_defaulting() {
    let normal = header(b"unit-1.0.0/a", b'0', 0);
    for kind in [
        0, b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'K', b'x', b'g', b'S', b'M', b'V', b'N', b'Z',
    ] {
        let mut h = normal;
        h[156] = kind;
        fix_checksum(&mut h);
        let mut t = h.to_vec();
        t.extend_from_slice(&[0; 1024]);
        assert_eq!(profile(&stored(&t)), ProfileError::TarType);
    }
    let mut bad = normal;
    bad[20] ^= 1;
    let mut t = bad.to_vec();
    t.extend_from_slice(&[0; 1024]);
    assert_eq!(profile(&stored(&t)), ProfileError::TarChecksum);
    for size in [b"00000000008\0".as_slice(), &[0; 12]] {
        let mut h = normal;
        h[124..136].copy_from_slice(size);
        fix_checksum(&mut h);
        let mut t = h.to_vec();
        t.extend_from_slice(&[0; 1024]);
        assert_eq!(profile(&stored(&t)), ProfileError::TarSize);
    }
    let mut h = normal;
    h[124..136].fill(0);
    h[124] = 128;
    h[127] = 64;
    fix_checksum(&mut h);
    let mut t = h.to_vec();
    t.extend_from_slice(&[0; 1024]);
    // This is a legal positive above-octal-range base256 size >u64, not
    // a profile-size error. The physically short body is actually truncated.
    assert_eq!(profile(&stored(&t)), ProfileError::TruncatedTar);
}

#[test]
fn effective_paths_duplicates_and_long_record_relationships_are_checked() {
    for path in [
        b"unit-1.0.0/../a".as_slice(),
        b"unit-1.0.0/a//b",
        b"unit-1.0.0/a\\b",
        b"other-1.0.0/a",
        b"unit-1.0.0/",
        b"unit-1.0.0/\xff",
    ] {
        let mut t = Vec::new();
        append(&mut t, header(path, b'0', 0), &[]);
        t.extend_from_slice(&[0; 1024]);
        assert_eq!(profile(&stored(&t)), ProfileError::Path);
    }
    let mut t = Vec::new();
    for _ in 0..2 {
        append(&mut t, header(b"unit-1.0.0/a", b'0', 0), &[]);
    }
    t.extend_from_slice(&[0; 1024]);
    assert_eq!(profile(&stored(&t)), ProfileError::DuplicatePath);
    let long = b"unit-1.0.0/a\0";
    let mut t = Vec::new();
    append(
        &mut t,
        header(b"././@LongLink", b'L', long.len() as u64),
        long,
    );
    let mut orphan = t.clone();
    orphan.extend_from_slice(&[0; 1024]);
    assert_eq!(profile(&stored(&orphan)), ProfileError::OrphanLong);
    let mut chain = t.clone();
    append(
        &mut chain,
        header(b"././@LongLink", b'L', long.len() as u64),
        long,
    );
    chain.extend_from_slice(&[0; 1024]);
    assert_eq!(profile(&stored(&chain)), ProfileError::LongChain);
    append(&mut t, header(b"unit-1.0.0/b", b'0', 0), &[]);
    t.extend_from_slice(&[0; 1024]);
    assert_eq!(profile(&stored(&t)), ProfileError::LongPrefix);
}

#[test]
fn zero_end_region_has_its_own_incremental_bound_and_block_alignment() {
    for length in [0, 512, 1023, 1024, 1536, 10240, 10241, 10752] {
        let bytes = stored(&vec![0; length]);
        let result = decode(bytes.as_slice(), "unit", "1.0.0", &mut Receiver::default());
        assert_eq!(
            result.is_ok(),
            (1024..=10240).contains(&length) && length % 512 == 0,
            "{length}"
        );
    }
    let mut t = vec![0; 1024];
    t[513] = 1;
    assert_eq!(profile(&stored(&t)), ProfileError::TarEnd);
}

#[test]
fn owning_abort_and_physical_io_are_preserved_and_no_success_report_is_returned() {
    let mut receiver = Receiver {
        abort: true,
        ..Receiver::default()
    };
    assert!(matches!(
        decode(
            include_bytes!("fixtures/base.tar.gz").as_slice(),
            "unit",
            "1.0.0",
            &mut receiver
        ),
        Err(DecodeError::Consumer("owning-abort"))
    ));
    assert_eq!(receiver.began, 0);
    struct Broken;
    impl Read for Broken {
        fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
            Err(io::Error::from(io::ErrorKind::PermissionDenied))
        }
    }
    match decode(Broken, "unit", "1.0.0", &mut Receiver::default()) {
        Err(DecodeError::Io(error)) => assert_eq!(error.kind(), io::ErrorKind::PermissionDenied),
        other => panic!("unexpected result: {other:?}"),
    }
    let result = decode(
        include_bytes!("fixtures/base.tar.gz").as_slice(),
        "unit",
        "1.0.0",
        &mut Receiver::default(),
    )
    .unwrap();
    assert_eq!(
        result.compressed_sha256,
        raw_sha256(include_bytes!("fixtures/base.tar.gz"))
    );
}

#[test]
fn compressed_work_guard_refuses_empty_blocks_before_their_end() {
    let tar = vec![0; 1024];
    for count in [200_000, 210_000] {
        let ordinary = stored(&tar);
        let mut bytes = ordinary[..10].to_vec();
        for _ in 0..count {
            bytes.extend_from_slice(&[0, 0, 0, 255, 255]);
        }
        bytes.extend_from_slice(&ordinary[10..]);
        let result = decode(bytes.as_slice(), "unit", "1.0.0", &mut Receiver::default());
        if count == 200_000 {
            assert!(result.is_ok());
        } else {
            assert!(matches!(
                result,
                Err(DecodeError::Profile(ProfileError::CompressedBound))
            ));
        }
    }
}

#[test]
fn late_trailer_refusal_never_returns_a_complete_archive_and_content_stays_provisional() {
    let mut bytes = include_bytes!("fixtures/base.tar.gz").to_vec();
    let at = bytes.len() - 8;
    bytes[at] ^= 1;
    let mut consumer = Receiver::default();
    assert!(matches!(
        decode(bytes.as_slice(), "unit", "1.0.0", &mut consumer),
        Err(DecodeError::Profile(ProfileError::GzipTrailer))
    ));
    assert_eq!(consumer.began, 3);
    assert_eq!(consumer.ended, 3);
    assert_eq!(consumer.bytes, b"hello\nfn main(){}");
    // The callbacks deliberately have no source/import/owner capability. Their
    // caller must quarantine these provisional bytes; no decoder result exists.
}

#[test]
fn interrupted_reads_recheck_the_owning_checkpoint_and_preserve_its_abort() {
    struct Interrupted;
    impl Read for Interrupted {
        fn read(&mut self, _: &mut [u8]) -> io::Result<usize> {
            Err(io::Error::from(io::ErrorKind::Interrupted))
        }
    }
    struct Stop {
        checks: usize,
    }
    impl ArchiveConsumer for Stop {
        type Error = &'static str;
        fn checkpoint(&mut self) -> Result<(), Self::Error> {
            self.checks += 1;
            if self.checks == 3 {
                Err("cancelled")
            } else {
                Ok(())
            }
        }
        fn begin(&mut self, _: &LogicalPath, _: u128) -> Result<(), Self::Error> {
            panic!("no header")
        }
        fn content(&mut self, _: &[u8]) -> Result<(), Self::Error> {
            panic!("no content")
        }
        fn end(&mut self, _: &FileRecord) -> Result<(), Self::Error> {
            panic!("no file")
        }
    }
    let mut consumer = Stop { checks: 0 };
    assert!(matches!(
        decode(Interrupted, "unit", "1.0.0", &mut consumer),
        Err(DecodeError::Consumer("cancelled"))
    ));
    assert_eq!(consumer.checks, 3);
}

#[test]
fn long_control_payload_bound_is_distinct_from_malformed_shape() {
    for (length, wanted) in [
        (1, ProfileError::LongName),
        (16386, ProfileError::ControlBound),
    ] {
        let mut tar = header(b"././@LongLink", b'L', length).to_vec();
        tar.extend_from_slice(&[0; 1024]);
        assert_eq!(profile(&stored(&tar)), wanted);
    }
}

#[test]
fn long_paths_count_unicode_scalars_and_keep_raw_distinct_names() {
    for full_scalars in [4096, 4097] {
        let mut path = String::from("unit-1.0.0/");
        while full_scalars - path.chars().count() > 255 {
            path.extend(std::iter::repeat_n('\u{1f600}', 255));
            path.push('/');
        }
        path.extend(std::iter::repeat_n(
            '\u{1f600}',
            full_scalars - path.chars().count(),
        ));
        let mut payload = path.as_bytes().to_vec();
        payload.push(0);
        assert!(payload.len() <= 16385);
        let mut tar = Vec::new();
        append(
            &mut tar,
            header(b"././@LongLink", b'L', payload.len() as u64),
            &payload,
        );
        let mut prefix_length = 100;
        while !path.is_char_boundary(prefix_length) {
            prefix_length -= 1;
        }
        append(
            &mut tar,
            header(&path.as_bytes()[..prefix_length], b'0', 0),
            &[],
        );
        tar.extend_from_slice(&[0; 1024]);
        let gzip = stored(&tar);
        let result = decode(gzip.as_slice(), "unit", "1.0.0", &mut Receiver::default());
        assert_eq!(result.is_ok(), full_scalars == 4096);
    }
    let mut tar = Vec::new();
    for name in ["unit-1.0.0/\u{e9}", "unit-1.0.0/e\u{301}"] {
        append(&mut tar, header(name.as_bytes(), b'0', 0), &[]);
    }
    tar.extend_from_slice(&[0; 1024]);
    let gzip = stored(&tar);
    let result = decode(gzip.as_slice(), "unit", "1.0.0", &mut Receiver::default()).unwrap();
    assert_eq!(result.files.len(), 2);
    assert_ne!(result.files[0].path, result.files[1].path);
}

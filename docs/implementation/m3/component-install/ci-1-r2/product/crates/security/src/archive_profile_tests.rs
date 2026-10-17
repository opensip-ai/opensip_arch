// CI-1's controls (component installation plan r3, section 4: CI-T1, CI-T2,
// CI-T5 and CI-T13). CI-T1 is PKG-AP's exact 15 `goldenAndNegativeCases`,
// one test each, named after the case. AT-ARCHIVE-MODE-MAX and
// AT-ARCHIVE-SIZE-MAX are codec-capacity cases, metadata-only (PKG-AP permits
// a synthetic, metadata-only fixture): they are never installable signed
// positives, since the manifest admits modes up to 0777 only. These are pure
// codec checks, not signed installations.
use super::*;
use opensip_identity::raw_sha256;

/// The streamed events, owned, with each file's bytes concatenated.
#[derive(Debug, Clone, PartialEq, Eq)]
enum Seen {
    Header(usize),
    Bytes(usize, Vec<u8>),
    End(usize),
    Done([u8; 32]),
}

fn file<'a>(path: &'a str, mode: u32, body: &[u8]) -> TreeRow<'a> {
    TreeRow {
        path,
        mode,
        kind: RowKind::File {
            length: body.len() as u64,
            sha256: raw_sha256(body),
        },
    }
}
fn dir(path: &str, mode: u32) -> TreeRow<'_> {
    TreeRow {
        path,
        mode,
        kind: RowKind::Dir,
    }
}
fn symlink<'a>(path: &'a str, mode: u32, target: &'a str) -> TreeRow<'a> {
    TreeRow {
        path,
        mode,
        kind: RowKind::Symlink { target },
    }
}
fn payload(n: u32, a: u32, c: u32) -> Vec<u8> {
    (0..n).map(|i| ((i * a + c) % 256) as u8).collect()
}

/// Streams `archive` through a verifier for `rows` in chunks of `chunk` bytes,
/// then finishes it at the input's end.
fn stream(rows: &[TreeRow<'_>], archive: &[u8], chunk: usize) -> Result<Vec<Seen>, ArchiveRefusal> {
    let plan = ArchivePlan::new(rows)?;
    let mut v = plan.verifier();
    let mut seen: Vec<Seen> = Vec::new();
    for piece in archive.chunks(chunk) {
        let mut input = piece;
        loop {
            let (next, event) = v.step(&mut input)?;
            v = next;
            match event {
                None => break,
                Some(ArchiveEvent::Header { position }) => seen.push(Seen::Header(position)),
                Some(ArchiveEvent::FileBytes { position, bytes }) => match seen.last_mut() {
                    Some(Seen::Bytes(p, b)) if *p == position => b.extend_from_slice(bytes),
                    _ => seen.push(Seen::Bytes(position, bytes.to_vec())),
                },
                Some(ArchiveEvent::MemberEnd { position }) => seen.push(Seen::End(position)),
                Some(ArchiveEvent::End { sha256 }) => seen.push(Seen::Done(sha256)),
            }
        }
    }
    v.finish()?;
    Ok(seen)
}

/// Recomputes a tampered header's checksum exactly as PKG-AP stores it.
fn rehash(archive: &mut [u8], at: usize) {
    let h = &mut archive[at..at + 512];
    h[148..156].fill(b' ');
    let sum: u32 = h.iter().map(|&b| b as u32).sum();
    h[148..156].copy_from_slice(format!("{sum:06o}\0 ").as_bytes());
}

struct Vector {
    readme: Vec<u8>,
    accent: Vec<u8>,
}
impl Vector {
    fn new() -> Self {
        Self {
            readme: payload(700, 7, 3),
            accent: payload(512, 13, 5),
        }
    }
    /// The fixed vector's tree, in member order.
    fn rows(&self) -> Vec<TreeRow<'_>> {
        vec![
            file("README", 0o644, &self.readme),
            dir("a", 0o755),
            file("a-x", 0o600, b""),
            dir("a/b", 0o700),
            file("a/b/c.txt", 0o444, b"c\n"),
            dir("bin", 0o755),
            file("bin/tool", 0o755, b"#!/bin/sh\nexit 0\n"),
            dir("donn\u{e9}es", 0o755),
            file("donn\u{e9}es/\u{e9}.txt", 0o644, &self.accent),
            symlink("latest", 0o777, "bin/tool"),
        ]
    }
    fn payloads(&self) -> Vec<(&str, &[u8])> {
        vec![
            ("README", &self.readme[..]),
            ("a-x", &b""[..]),
            ("a/b/c.txt", &b"c\n"[..]),
            ("bin/tool", &b"#!/bin/sh\nexit 0\n"[..]),
            ("donn\u{e9}es/\u{e9}.txt", &self.accent[..]),
        ]
    }
    fn archive(&self) -> Vec<u8> {
        emit(&self.rows(), &self.payloads()).unwrap()
    }
}

/// The offset of member `position`'s header in `rows`' archive.
fn header_at(rows: &[TreeRow<'_>], position: usize) -> usize {
    rows[..position]
        .iter()
        .map(|r| match r.kind {
            RowKind::File { length, .. } => 512 + padded(length) as usize,
            _ => 512,
        })
        .sum()
}

// ---- CI-T1: PKG-AP's 15 golden and negative cases ----

#[test]
fn at_archive_identity() {
    let v = Vector::new();
    let first = v.archive();
    let second = v.archive();
    assert_eq!(first, second);
    assert_eq!(raw_sha256(&first), raw_sha256(&second));
    // The input order of the rows enters no byte.
    let mut shuffled = v.rows();
    shuffled.reverse();
    shuffled.swap(2, 7);
    assert_eq!(emit(&shuffled, &v.payloads()).unwrap(), first);
    let seen = stream(&v.rows(), &first, 65536).unwrap();
    assert_eq!(seen.last(), Some(&Seen::Done(raw_sha256(&first))));
}

#[test]
fn at_archive_body_mismatch() {
    let v = Vector::new();
    let rows = v.rows();
    let archive = v.archive();
    // A body byte changed: the digest refuses at that member's end.
    let mut changed = archive.clone();
    changed[header_at(&rows, 4) + 512] ^= 1;
    assert_eq!(
        stream(&rows, &changed, 64),
        Err(ArchiveRefusal::FileDigest { position: 4 })
    );
    // A row whose length differs: the length refuses first, and the header's size field differs.
    let mut longer = rows.clone();
    longer[4] = file("a/b/c.txt", 0o444, b"c\n\n");
    let plan = ArchivePlan::new(&longer[..]).unwrap();
    assert_eq!(plan.length(), archive.len() as u64, "same padded length");
    assert_eq!(
        stream(&longer, &archive, 4096),
        Err(ArchiveRefusal::Header {
            position: 4,
            field: HeaderField::Size
        })
    );
    // The emitter refuses a payload whose length or digest is not the row's, or a missing one.
    let mut wrong = v.payloads();
    wrong[2].1 = b"c\r";
    assert_eq!(
        emit(&rows, &wrong),
        Err(EmitRefusal::SizeOrDigestMismatch {
            path: "a/b/c.txt".to_string()
        })
    );
    wrong[2].1 = b"c";
    assert!(matches!(
        emit(&rows, &wrong),
        Err(EmitRefusal::SizeOrDigestMismatch { .. })
    ));
    let all = v.payloads();
    let missing = &all[1..];
    assert_eq!(
        emit(&rows, missing),
        Err(EmitRefusal::SizeOrDigestMismatch {
            path: "README".to_string()
        })
    );
}

#[test]
fn at_archive_target_mismatch() {
    let v = Vector::new();
    let mut rows = v.rows();
    rows[9] = symlink("latest", 0o777, "bin/tooL");
    assert_eq!(
        stream(&rows, &v.archive(), 512),
        Err(ArchiveRefusal::Header {
            position: 9,
            field: HeaderField::Linkname
        })
    );
}

#[test]
fn at_archive_extra_member() {
    let v = Vector::new();
    let rows = v.rows();
    // An extra member at the end, where the trailer belongs.
    let mut more = rows.clone();
    more.push(dir("zz", 0o755));
    let extra = emit(&more, &v.payloads()).unwrap();
    let plan = ArchivePlan::new(&rows[..]).unwrap();
    assert_eq!(
        plan.check_length(extra.len() as u64),
        Err(ArchiveRefusal::Length {
            expected: plan.length(),
            observed: extra.len() as u64
        })
    );
    assert_eq!(stream(&rows, &extra, 1000), Err(ArchiveRefusal::Trailer));
    // An extra member in the middle.
    let mut middle = rows.clone();
    middle.insert(1, dir("Z", 0o755));
    let extra = emit(&middle, &v.payloads()).unwrap();
    assert_eq!(
        stream(&rows, &extra, 1000),
        Err(ArchiveRefusal::Header {
            position: 1,
            field: HeaderField::Name
        })
    );
}

#[test]
fn at_archive_missing_member() {
    let v = Vector::new();
    let rows = v.rows();
    let mut fewer = rows.clone();
    fewer.remove(1);
    let missing = emit(&fewer, &v.payloads()).unwrap();
    let plan = ArchivePlan::new(&rows[..]).unwrap();
    assert!(matches!(
        plan.check_length(missing.len() as u64),
        Err(ArchiveRefusal::Length { .. })
    ));
    assert_eq!(
        stream(&rows, &missing, 333),
        Err(ArchiveRefusal::Header {
            position: 1,
            field: HeaderField::Name
        })
    );
    // The last member missing: the trailer arrives where a header belongs.
    fewer = rows.clone();
    fewer.pop();
    let missing = emit(&fewer, &v.payloads()).unwrap();
    assert_eq!(
        stream(&rows, &missing, 333),
        Err(ArchiveRefusal::Header {
            position: 9,
            field: HeaderField::Name
        })
    );
}

#[test]
fn at_archive_name_100() {
    let path = format!("{}/{}", "n".repeat(49), "m".repeat(50));
    assert_eq!(path.len(), 100);
    let parent = "n".repeat(49);
    let rows = [dir(&parent, 0o755), file(&path, 0o644, b"x")];
    let archive = emit(&rows, &[(path.as_str(), &b"x"[..])]).unwrap();
    // The name field is full and has no terminator.
    assert_eq!(&archive[512..612], path.as_bytes());
    assert_eq!(archive[612], b'0', "the mode field follows directly");
    stream(&rows, &archive, 7).unwrap();
}

#[test]
fn at_archive_name_101() {
    let path = "p".repeat(101);
    let rows = [file(&path, 0o644, b"")];
    let refusal = ArchivePlan::new(&rows[..]).err();
    assert_eq!(
        refusal,
        Some(ArchiveRefusal::Capacity {
            position: 0,
            capacity: Capacity::PathExceedsUstarName
        })
    );
    assert_eq!(
        Capacity::PathExceedsUstarName.token(),
        "PATH-EXCEEDS-USTAR-NAME"
    );
    // A 101-byte UTF-8 path of fewer code points refuses too: bytes count.
    let accented = format!("{}\u{e9}", "p".repeat(99));
    assert_eq!((accented.len(), accented.chars().count()), (101, 100));
    let rows = [file(&accented, 0o644, b"")];
    assert!(matches!(
        ArchivePlan::new(&rows[..]),
        Err(ArchiveRefusal::Capacity {
            capacity: Capacity::PathExceedsUstarName,
            ..
        })
    ));
}

#[test]
fn at_archive_link_100() {
    let target = "t".repeat(100);
    let rows = [symlink("link", 0o777, &target)];
    let archive = emit(&rows, &[]).unwrap();
    assert_eq!(&archive[157..257], target.as_bytes());
    assert_eq!(&archive[257..263], b"ustar\0");
    let seen = stream(&rows, &archive, 1).unwrap();
    assert_eq!(seen[..2], [Seen::Header(0), Seen::End(0)]);
}

#[test]
fn at_archive_link_101() {
    let target = "t".repeat(101);
    let rows = [symlink("link", 0o777, &target)];
    assert_eq!(
        ArchivePlan::new(&rows[..]).err(),
        Some(ArchiveRefusal::Capacity {
            position: 0,
            capacity: Capacity::LinkTargetExceedsUstarLinkname
        })
    );
    assert_eq!(
        Capacity::LinkTargetExceedsUstarLinkname.token(),
        "LINKTARGET-EXCEEDS-USTAR-LINKNAME"
    );
}

#[test]
fn at_archive_typeflag_nul() {
    let v = Vector::new();
    let rows = v.rows();
    let mut archive = v.archive();
    let at = header_at(&rows, 0);
    assert_eq!(archive[at + 156], b'0');
    archive[at + 156] = 0;
    rehash(&mut archive, at);
    assert_eq!(
        stream(&rows, &archive, 4096),
        Err(ArchiveRefusal::Header {
            position: 0,
            field: HeaderField::Typeflag
        })
    );
}

#[test]
fn at_archive_chksum_spaces() {
    let v = Vector::new();
    let rows = v.rows();
    let mut archive = v.archive();
    // The emitted header's checksum: computed under the all-spaces mask, stored six digits, NUL, space.
    let h = &archive[..512];
    let mut masked = h.to_vec();
    masked[148..156].fill(b' ');
    let sum: u32 = masked.iter().map(|&b| b as u32).sum();
    assert_eq!(&h[148..156], format!("{sum:06o}\0 ").as_bytes());
    // Any NUL in the computation mask gives another stored value, which fails.
    for nuls in [8usize, 1, 7] {
        let mut m = masked.clone();
        m[148..148 + nuls].fill(0);
        let wrong: u32 = m.iter().map(|&b| b as u32).sum();
        archive[148..156].copy_from_slice(format!("{wrong:06o}\0 ").as_bytes());
        assert_eq!(
            stream(&rows, &archive, 512),
            Err(ArchiveRefusal::Header {
                position: 0,
                field: HeaderField::Chksum
            })
        );
    }
    // The stored layout's alternatives fail too: NUL NUL, or space space.
    for tail in [b"\0\0", b"  "] {
        let mut stored = format!("{sum:06o}").into_bytes();
        stored.extend_from_slice(tail);
        archive[148..156].copy_from_slice(&stored);
        assert!(matches!(
            stream(&rows, &archive, 512),
            Err(ArchiveRefusal::Header {
                field: HeaderField::Chksum,
                ..
            })
        ));
    }
}

/// The fixed vector's expected bytes come from a second encoder written from
/// PKG-AP's text alone and cross-read by Python's `tarfile` and the system
/// `tar` (the CI-1 package's `fixed_vector.py`), not from this codec.
const FIXED_VECTOR_LENGTH: usize = 8704;
const FIXED_VECTOR_SHA256: &str =
    "47fd5fd72177201dbe3aaff23ea649ead391e98d77dae6eb3391ac0ac16f6795";

#[test]
fn at_archive_fixed_vector() {
    let v = Vector::new();
    let rows = v.rows();
    let archive = v.archive();
    assert_eq!(archive.len(), FIXED_VECTOR_LENGTH);
    assert_eq!(
        ArchivePlan::new(&rows[..]).unwrap().length(),
        FIXED_VECTOR_LENGTH as u64
    );
    assert_eq!(
        opensip_identity::digest_hex(&raw_sha256(&archive)),
        FIXED_VECTOR_SHA256
    );
    let seen = stream(&rows, &archive, 65536).unwrap();
    assert_eq!(seen.last(), Some(&Seen::Done(raw_sha256(&archive))));
}

#[test]
fn at_archive_mode_max() {
    // Metadata-only: a codec-capacity case, never an installable signed positive.
    let rows = [dir("d", MAX_MODE)];
    assert_eq!(MAX_MODE, 2_097_151);
    let archive = emit(&rows, &[]).unwrap();
    assert_eq!(&archive[100..108], b"7777777\0");
    stream(&rows, &archive, 512).unwrap();
    let over = [dir("d", MAX_MODE + 1)];
    assert_eq!(
        ArchivePlan::new(&over[..]).err(),
        Some(ArchiveRefusal::Capacity {
            position: 0,
            capacity: Capacity::ModeExceedsUstarField
        })
    );
    assert_eq!(
        Capacity::ModeExceedsUstarField.token(),
        "MODE-EXCEEDS-USTAR-FIELD"
    );
}

#[test]
fn at_archive_size_max() {
    // Metadata-only: the field maximum is admitted and encoded with no payload.
    assert_eq!(MAX_SIZE, 8_589_934_591);
    let max = [TreeRow {
        path: "big",
        mode: 0o644,
        kind: RowKind::File {
            length: MAX_SIZE,
            sha256: [0; 32],
        },
    }];
    let plan = ArchivePlan::new(&max[..]).unwrap();
    assert_eq!(plan.length(), 512 + 8_589_934_592 + 1024);
    assert_eq!(&header(&max[0])[124..136], b"77777777777\0");
    let over = [TreeRow {
        path: "big",
        mode: 0o644,
        kind: RowKind::File {
            length: MAX_SIZE + 1,
            sha256: [0; 32],
        },
    }];
    assert_eq!(
        ArchivePlan::new(&over[..]).err(),
        Some(ArchiveRefusal::Capacity {
            position: 0,
            capacity: Capacity::SizeExceedsUstarField
        })
    );
    assert_eq!(
        Capacity::SizeExceedsUstarField.token(),
        "SIZE-EXCEEDS-USTAR-FIELD"
    );
}

#[test]
fn at_archive_noncanon_uid() {
    let v = Vector::new();
    let rows = v.rows();
    let mut archive = v.archive();
    let at = header_at(&rows, 3);
    archive[at + 108..at + 116].copy_from_slice(b"0000001\0");
    rehash(&mut archive, at);
    assert_eq!(
        stream(&rows, &archive, 4096),
        Err(ArchiveRefusal::Header {
            position: 3,
            field: HeaderField::Uid
        })
    );
}

// ---- CI-T2: the length, before any read ----

#[test]
fn ci_t2_length_mismatch_refuses_before_any_member() {
    let v = Vector::new();
    let rows = v.rows();
    let archive = v.archive();
    let plan = ArchivePlan::new(&rows[..]).unwrap();
    assert_eq!(plan.check_length(archive.len() as u64), Ok(()));
    for observed in [
        0,
        archive.len() as u64 - 1,
        archive.len() as u64 + 1,
        archive.len() as u64 + 512,
    ] {
        assert_eq!(
            plan.check_length(observed),
            Err(ArchiveRefusal::Length {
                expected: archive.len() as u64,
                observed
            })
        );
    }
    assert_eq!(plan.read_limit(), archive.len() as u64 + 1);
    // Streamed, a longer archive refuses at its first extra byte: at most the length plus one is read.
    let mut longer = archive.clone();
    longer.extend_from_slice(&[0; 512]);
    let mut verifier = plan.verifier();
    let mut fed = 0u64;
    let refusal = 'feed: loop {
        let mut input = &longer[fed as usize..fed as usize + 1];
        fed += 1;
        loop {
            match verifier.step(&mut input) {
                Err(e) => break 'feed e,
                Ok((next, Some(_))) => verifier = next,
                Ok((next, None)) => {
                    verifier = next;
                    break;
                }
            }
        }
    };
    assert_eq!(refusal, ArchiveRefusal::TrailingBytes);
    assert_eq!(fed, plan.read_limit());
}

#[test]
fn ci_t2_every_truncation_refuses_at_the_end_of_input() {
    let v = Vector::new();
    let rows = v.rows();
    let archive = v.archive();
    for cut in (0..archive.len())
        .step_by(37)
        .chain([511, 512, 8191, 8192, 8703])
    {
        assert_eq!(
            stream(&rows, &archive[..cut], 4096),
            Err(ArchiveRefusal::Truncated {
                consumed: cut as u64
            }),
            "{cut}"
        );
    }
}

// ---- CI-T5: capacities, before any read ----

#[test]
fn ci_t5_capacity_refuses_before_any_read() {
    let long = "q".repeat(101);
    for rows in [
        vec![dir("a", 0o755), file(&long, 0o644, b"")],
        vec![dir("a", 0o755), symlink("b", 0o777, &long)],
    ] {
        // No verifier exists without a plan, so nothing can be read.
        assert!(matches!(
            ArchivePlan::new(&rows[..]),
            Err(ArchiveRefusal::Capacity { position: 1, .. })
        ));
    }
}

// ---- The stream, the structure and the extensions ----

#[test]
fn events_are_exact_at_every_chunk_size() {
    let v = Vector::new();
    let rows = v.rows();
    let archive = v.archive();
    let reference = stream(&rows, &archive, archive.len()).unwrap();
    let mut expected = Vec::new();
    for (position, row) in rows.iter().enumerate() {
        expected.push(Seen::Header(position));
        if let RowKind::File { length, .. } = row.kind
            && length > 0
        {
            let (_, body) = v
                .payloads()
                .into_iter()
                .find(|(p, _)| *p == row.path)
                .unwrap();
            expected.push(Seen::Bytes(position, body.to_vec()));
        }
        expected.push(Seen::End(position));
    }
    expected.push(Seen::Done(raw_sha256(&archive)));
    assert_eq!(reference, expected);
    for chunk in [1, 2, 7, 100, 511, 512, 513, 1023, 4096, 65536] {
        assert_eq!(stream(&rows, &archive, chunk).unwrap(), expected, "{chunk}");
    }
}

#[test]
fn pad_and_trailer_bytes_must_be_nul() {
    let v = Vector::new();
    let rows = v.rows();
    let archive = v.archive();
    // README is 700 bytes: its pad is 324 bytes, from 512 + 700.
    let mut padded = archive.clone();
    padded[512 + 700 + 323] = b' ';
    assert_eq!(
        stream(&rows, &padded, 4096),
        Err(ArchiveRefusal::Pad { position: 0 })
    );
    let mut trailer = archive.clone();
    let last = trailer.len() - 1;
    trailer[last] = 1;
    assert_eq!(stream(&rows, &trailer, 4096), Err(ArchiveRefusal::Trailer));
    let mut trailer = archive.clone();
    trailer[archive.len() - 1024] = 1;
    assert_eq!(stream(&rows, &trailer, 4096), Err(ArchiveRefusal::Trailer));
}

#[test]
fn pax_and_gnu_extensions_refuse() {
    let v = Vector::new();
    let rows = v.rows();
    for flag in [b'x', b'g', b'L', b'K', b'1', b'7', b'5'] {
        let mut archive = v.archive();
        archive[156] = flag;
        rehash(&mut archive, 0);
        assert_eq!(
            stream(&rows, &archive, 4096),
            Err(ArchiveRefusal::Header {
                position: 0,
                field: HeaderField::Typeflag
            }),
            "{}",
            flag as char
        );
    }
    // A PAX extended header member before the first member.
    let pax_rows = [file("PaxHeaders/README", 0o644, b"20 path=README\n")];
    let mut pax = emit(
        &pax_rows,
        &[("PaxHeaders/README", &b"20 path=README\n"[..])],
    )
    .unwrap();
    pax[156] = b'x';
    rehash(&mut pax, 0);
    pax.truncate(1024);
    pax.extend_from_slice(&v.archive());
    assert_eq!(
        stream(&rows, &pax, 4096),
        Err(ArchiveRefusal::Header {
            position: 0,
            field: HeaderField::Name
        })
    );
    // GNU's magic, and a name split into the prefix field.
    let mut gnu = v.archive();
    gnu[257..265].copy_from_slice(b"ustar  \0");
    rehash(&mut gnu, 0);
    assert_eq!(
        stream(&rows, &gnu, 4096),
        Err(ArchiveRefusal::Header {
            position: 0,
            field: HeaderField::Magic
        })
    );
    let mut split = v.archive();
    let at = header_at(&rows, 4);
    split[at..at + 100].fill(0);
    split[at..at + 5].copy_from_slice(b"c.txt");
    split[at + 345..at + 348].copy_from_slice(b"a/b");
    rehash(&mut split, at);
    assert_eq!(
        stream(&rows, &split, 4096),
        Err(ArchiveRefusal::Header {
            position: 4,
            field: HeaderField::Name
        })
    );
}

#[test]
fn bytes_after_a_field_terminator_are_compared() {
    // A decoder would read these fields as equal; the octets are not.
    let v = Vector::new();
    let rows = v.rows();
    for (offset, field) in [
        (10, HeaderField::Name),
        (157 + 20, HeaderField::Linkname),
        (265 + 5, HeaderField::Uname),
        (345 + 154, HeaderField::Prefix),
        (500, HeaderField::Pad),
        (511, HeaderField::Pad),
    ] {
        let mut archive = v.archive();
        let at = header_at(&rows, 1);
        assert_eq!(archive[at + offset], 0);
        archive[at + offset] = b'J';
        rehash(&mut archive, at);
        assert_eq!(
            stream(&rows, &archive, 4096),
            Err(ArchiveRefusal::Header { position: 1, field }),
            "{offset}"
        );
    }
    // Numeric alternatives a decoder would accept: a space terminator, a shorter field.
    for (range, bytes, field) in [
        (100..108, &b"0000755 "[..], HeaderField::Mode),
        (100..108, &b"755\0\0\0\0\0"[..], HeaderField::Mode),
        (329..337, &b"\0\0\0\0\0\0\0\0"[..], HeaderField::Devmajor),
        (136..148, &b"00000000000 "[..], HeaderField::Mtime),
    ] {
        let mut archive = v.archive();
        let at = header_at(&rows, 1);
        archive[at + range.start..at + range.end].copy_from_slice(bytes);
        rehash(&mut archive, at);
        assert_eq!(
            stream(&rows, &archive, 4096),
            Err(ArchiveRefusal::Header { position: 1, field }),
            "{field:?}"
        );
    }
}

#[test]
fn rows_must_hold_the_admitted_manifest_invariants() {
    let empty: [TreeRow<'_>; 0] = [];
    assert_eq!(
        ArchivePlan::new(&empty[..]).err(),
        Some(ArchiveRefusal::Rows {
            position: 0,
            invariant: RowsInvariant::Count
        })
    );
    struct Many;
    impl ArchiveRows for Many {
        fn count(&self) -> usize {
            MAX_ENTRIES + 1
        }
        fn row(&self, _: usize) -> TreeRow<'_> {
            unreachable!("the count refuses first")
        }
    }
    assert!(matches!(
        ArchivePlan::new(&Many),
        Err(ArchiveRefusal::Rows {
            invariant: RowsInvariant::Count,
            ..
        })
    ));
    fn order(rows: &[TreeRow<'_>]) -> Option<ArchiveRefusal> {
        ArchivePlan::new(rows).err()
    }
    let unsorted = [dir("b", 0o755), dir("a", 0o755)];
    let duplicate = [dir("a", 0o755), dir("a", 0o755)];
    // Byte order, which is code-point order: "a-x" precedes "a/b", "Z" precedes "a".
    let component_order = [dir("a", 0o755), dir("a/b", 0o755), dir("a-x", 0o755)];
    for rows in [&unsorted[..], &duplicate[..], &component_order[..]] {
        assert!(matches!(
            order(rows),
            Some(ArchiveRefusal::Rows {
                invariant: RowsInvariant::Order,
                ..
            })
        ));
    }
    assert!(
        order(&[
            dir("Z", 0o755),
            dir("a", 0o755),
            dir("a-x", 0o755),
            dir("a/b", 0o755)
        ])
        .is_none()
    );
    for rows in [
        vec![dir("", 0o755)],
        vec![dir("a\0b", 0o755)],
        vec![symlink("l", 0o777, "")],
        vec![symlink("l", 0o777, "t\0")],
    ] {
        assert!(matches!(
            order(&rows),
            Some(ArchiveRefusal::Rows {
                invariant: RowsInvariant::Text,
                ..
            })
        ));
    }
}

#[test]
fn archive_length_is_the_profile_formula() {
    let v = Vector::new();
    let rows = v.rows();
    let files: u64 = [700u64, 0, 2, 17, 512]
        .iter()
        .map(|l| l.div_ceil(512) * 512)
        .sum();
    assert_eq!(
        ArchivePlan::new(&rows[..]).unwrap().length(),
        512 * 10 + files + 1024
    );
    let one = [dir("d", 0o755)];
    assert_eq!(ArchivePlan::new(&one[..]).unwrap().length(), 512 + 1024);
}

#[test]
fn emitter_refuses_payloads_without_a_file_row() {
    let v = Vector::new();
    let rows = v.rows();
    for extra in ["bin", "latest", "nowhere", "README"] {
        let mut payloads = v.payloads();
        payloads.push((extra, &b"#"[..]));
        assert_eq!(
            emit(&rows, &payloads),
            Err(EmitRefusal::Payload {
                path: extra.to_string()
            })
        );
    }
}

#[test]
fn the_layout_is_contiguous_and_field_at_follows_it() {
    let mut next = 0;
    for (field, _, offset, length) in LAYOUT {
        assert_eq!(offset, next);
        for o in offset..offset + length {
            assert_eq!(field_at(o), field);
        }
        next = offset + length;
    }
    assert_eq!(next, 512);
}

// ---- CI-T13 and the fixture predicate: source pins ----

#[test]
fn source_pins_no_network_spawn_environment_or_filesystem() {
    let source = include_str!("archive_profile.rs");
    for forbidden in [
        "std::net",
        "TcpStream",
        "UdpSocket",
        "http:",
        "https:",
        "std::process",
        "Command",
        "spawn",
        "std::env",
        "env!",
        "std::fs",
        "unsafe",
        "let _ =",
    ] {
        assert!(!source.contains(forbidden), "{forbidden}");
    }
}

#[test]
fn source_pins_the_emitter_behind_the_fixture_predicate() {
    let source = include_str!("archive_profile.rs");
    let predicate =
        "#[cfg(any(test, feature = \"crash-matrix\", feature = \"scenario-fixtures\"))]";
    assert_eq!(source.matches(predicate).count(), 2);
    assert_eq!(source.matches("pub fn emit(").count(), 1);
    assert_eq!(source.matches("pub enum EmitRefusal").count(), 1);
    let lines: Vec<&str> = source.lines().collect();
    for item in ["pub fn emit(", "pub enum EmitRefusal"] {
        let at = lines.iter().position(|l| l.starts_with(item)).unwrap();
        assert!(
            lines[..at]
                .iter()
                .rev()
                .take_while(|l| l.starts_with("#["))
                .any(|l| *l == predicate),
            "{item}"
        );
    }
    assert!(source.contains(PROFILE_SOURCE_SHA256));
    assert_eq!(PROFILE_ID, "opensip-archive-profile.1");
}

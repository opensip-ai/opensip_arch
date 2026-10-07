from pathlib import Path
p=Path('/tmp/opensip-implementation/g2-tar-members-authoring/product/providers/rust/src/dependency_inputs_tests.rs')
p.write_text(p.read_text()+r'''

fn tar_test_header(name: &[u8], kind: u8, size: usize) -> Vec<u8> {
    let mut h = vec![0u8; 512];
    h[..name.len()].copy_from_slice(name);
    h[124..136].copy_from_slice(format!("{size:011o}\0").as_bytes());
    h[156] = kind;
    h[257..265].copy_from_slice(b"ustar  \0");
    tar_test_checksum(&mut h);
    h
}
fn tar_test_checksum(h: &mut [u8]) {
    h[148..156].fill(b' ');
    let sum: usize = h.iter().map(|b| usize::from(*b)).sum();
    h[148..156].copy_from_slice(format!("{sum:06o}\0 ").as_bytes());
}
fn tar_test_entry(tar: &mut Vec<u8>, name: &[u8], kind: u8, content: &[u8]) {
    tar.extend(tar_test_header(name, kind, content.len()));
    tar.extend(content);
    tar.resize(tar.len().next_multiple_of(512), 0);
}
fn tar_test_end(tar: &mut Vec<u8>) { tar.extend(vec![0; 1024]); }
#[test]
fn declared_tar_members_are_sorted_and_borrow_exact_binary_contents() {
    let mut tar = vec![];
    tar_test_entry(&mut tar, b"pkg-1.0/z.rs", b'0', b"z\0\xff");
    tar_test_entry(&mut tar, b"pkg-1.0/a.rs", b'0', b"a");
    tar_test_end(&mut tar);
    let members = observe_declared_tar_members("pkg", "1.0", &tar).unwrap();
    assert_eq!(members.iter().map(|m| m.path()).collect::<Vec<_>>(), ["a.rs", "z.rs"]);
    assert_eq!(members[0].content(), b"a");
    assert_eq!(members[1].content(), b"z\0\xff");
    assert_eq!(members[1].content().as_ptr(), tar[512..].as_ptr());
}
#[test]
fn declared_tar_long_name_uses_effective_utf8_path_at_a_truncated_header() {
    let path = format!("pkg-1.0/{}/é.rs", "a".repeat(90));
    let mut long = path.as_bytes().to_vec();long.push(0);
    let mut tar = vec![];
    tar_test_entry(&mut tar, b"././@LongLink", b'L', &long);
    tar_test_entry(&mut tar, &path.as_bytes()[..99], b'0', b"long content");
    tar_test_end(&mut tar);
    let members=observe_declared_tar_members("pkg", "1.0", &tar).unwrap();
    assert_eq!(members[0].path(), &path[8..]);
    assert_eq!(members[0].content(), b"long content");
}
#[test]
fn declared_tar_long_name_prefix_need_not_fill_the_header() {
    let mut tar=vec![];
    tar_test_entry(&mut tar,b"././@LongLink",b'L',b"pkg-1.0/a.rs\0");
    tar_test_entry(&mut tar,b"pkg-1.0/",b'0',b"a");tar_test_end(&mut tar);
    assert_eq!(observe_declared_tar_members("pkg","1.0",&tar).unwrap()[0].path(),"a.rs");
}
#[test]
fn declared_tar_metadata_and_padding_do_not_enter_member_observations() {
    let mut tar=vec![];tar_test_entry(&mut tar,b"pkg-1.0/a",b'0',b"a");tar_test_end(&mut tar);
    tar[100..124].fill(b'7');tar[136..148].fill(b'2');tar[265..329].fill(b'Q');
    tar_test_checksum(&mut tar[..512]);tar[513..1024].fill(0xaa);
    let members=observe_declared_tar_members("pkg","1.0",&tar).unwrap();
    assert_eq!(members[0].path(),"a");assert_eq!(members[0].content(),b"a");
}
#[test]
fn declared_tar_duplicate_effective_paths_refuse_whole_observation() {
    let mut tar=vec![];tar_test_entry(&mut tar,b"pkg-1.0/a",b'0',b"a");
    tar_test_entry(&mut tar,b"././@LongLink",b'L',b"pkg-1.0/a\0");
    tar_test_entry(&mut tar,b"pkg-1.0/a",b'0',b"different");tar_test_end(&mut tar);
    assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::Duplicate)));
}
#[test]
fn declared_tar_all_nonprofile_types_refuse_including_null_regular_spelling() {
    for kind in [0,b'1',b'2',b'K',b'3',b'4',b'6',b'5',b'7',b'x',b'g',b'S',b'M',b'V',b'N',b'Z'] {
        let mut tar=vec![];tar_test_entry(&mut tar,b"pkg-1.0/a",kind,b"");tar_test_end(&mut tar);
        assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::EntryType)),"{kind}");
    }
}
#[test]
fn declared_tar_wrong_root_and_nonlogical_paths_refuse() {
    for path in [b"other-1.0/a".as_slice(),b"pkg-1.0/",b"pkg-1.0/../a",b"pkg-1.0/a//b",b"pkg-1.0/a\\b",b"pkg-1.0//a",b"pkg-1.0/a\0b",b"pkg-1.0/\xff"] {
        let mut tar=vec![];tar_test_entry(&mut tar,path,b'0',b"");tar_test_end(&mut tar);
        assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::Path)),"{path:?}");
    }
}
#[test]
fn declared_tar_checksum_and_gnu_magic_are_enforced() {
    let mut tar=vec![];tar_test_entry(&mut tar,b"pkg-1.0/a",b'0',b"");tar_test_end(&mut tar);
    tar[100]=1;assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::Checksum)));
    tar[257..265].copy_from_slice(b"ustar\000");tar_test_checksum(&mut tar[..512]);
    assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::Header)));
}
#[test]
fn declared_tar_end_region_has_exact_named_bounds_and_zero_blocks() {
    for size in [1024,10240] { assert!(observe_declared_tar_members("pkg","1.0",&vec![0;size]).unwrap().is_empty()); }
    for size in [512,1025,10752,29184] { assert!(matches!(observe_declared_tar_members("pkg","1.0",&vec![0;size]),Err(DeclaredTarError::EndRegion))); }
    let mut end=vec![0;1024];end[1023]=1;
    assert!(matches!(observe_declared_tar_members("pkg","1.0",&end),Err(DeclaredTarError::EndRegion)));
}
#[test]
fn declared_tar_late_failure_never_yields_partial_members() {
    let mut tar=vec![];tar_test_entry(&mut tar,b"pkg-1.0/a",b'0',b"a");tar.extend(vec![0;512]);
    assert!(observe_declared_tar_members("pkg","1.0",&tar).is_err());
    tar.truncate(513);assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::Truncated)));
}
#[test]
fn declared_tar_long_name_control_records_refuse_orphans_chains_and_mismatch() {
    for next in [b'L',b'2',b'0'] {
        let mut tar=vec![];tar_test_entry(&mut tar,b"././@LongLink",b'L',b"pkg-1.0/a\0");
        tar_test_entry(&mut tar,b"different",next,b"");tar_test_end(&mut tar);
        assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::LongName)));
    }
    let mut tar=vec![];tar_test_entry(&mut tar,b"././@LongLink",b'L',b"pkg-1.0/a\0");tar_test_end(&mut tar);
    assert!(observe_declared_tar_members("pkg","1.0",&tar).is_err());
    for payload in [b"x".as_slice(),b"pkg-1.0/a",b"pkg\0-1.0/a\0"] {
        let mut tar=vec![];tar_test_entry(&mut tar,b"././@LongLink",b'L',payload);tar_test_end(&mut tar);
        assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::LongName)));
    }
}
#[test]
fn declared_tar_d2_rejects_oversize_long_names_before_payload_slicing() {
    let mut tar=tar_test_header(b"././@LongLink",b'L',16386);tar_test_end(&mut tar);
    assert!(matches!(observe_declared_tar_members("pkg","1.0",&tar),Err(DeclaredTarError::LongName)));
}
#[test]
fn declared_tar_size_octal_and_positive_base256_follow_the_profile() {
    assert_eq!(tar_size(b"00000000000\0"),Some(0));
    assert_eq!(tar_size(b"77777777777\0"),Some(0o77777777777));
    let mut binary=[0u8;12];binary[0]=0x80;binary[4..].copy_from_slice(&0x200000000u64.to_be_bytes());
    assert_eq!(tar_size(&binary),Some(0x200000000));
    binary[4..].copy_from_slice(&1u64.to_be_bytes());assert_eq!(tar_size(&binary),None);
    binary[0]=0xff;assert_eq!(tar_size(&binary),None);
    assert_eq!(tar_size(b"00000000008\0"),None);
}
''')

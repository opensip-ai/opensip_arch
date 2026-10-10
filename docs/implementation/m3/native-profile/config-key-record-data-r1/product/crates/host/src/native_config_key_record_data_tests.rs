use super::{Error, PathPart, key, key_sets};
use PathPart::{Index as I, Name as N};

#[test]
fn ordinary_names_keep_exact_case_and_segments() {
    assert_eq!(
        key(&[N("build"), N("rustflags")]).unwrap(),
        "build.rustflags"
    );
    assert_eq!(
        key(&[N("resolver"), N("incompatible-rust-versions")]).unwrap(),
        "resolver.incompatible-rust-versions"
    );
    assert_eq!(key(&[N("A_Z-09")]).unwrap(), "A_Z-09");
    assert_ne!(key(&[N("Build")]).unwrap(), key(&[N("build")]).unwrap());
}

#[test]
fn exceptional_names_use_exact_canonical_strings() {
    for (name, expected) in [
        ("", "\"\""),
        ("*", "\"*\""),
        ("dot.key", "\"dot.key\""),
        ("a[0]", "\"a[0]\""),
        ("é", "\"é\""),
        ("e\u{301}", "\"e\u{301}\""),
        ("a\nb", "\"a\\nb\""),
        ("a\0b", "\"a\\u0000b\""),
        ("a\"b", "\"a\\\"b\""),
        ("a\\b", "\"a\\\\b\""),
        ("\u{8}\u{c}\r\t", "\"\\b\\f\\r\\t\""),
    ] {
        assert_eq!(key(&[N(name)]).unwrap(), expected);
    }
}

#[test]
fn literal_dots_and_index_spelling_do_not_coalesce() {
    assert_eq!(key(&[N("dot.key")]).unwrap(), "\"dot.key\"");
    assert_eq!(key(&[N("dot"), N("key")]).unwrap(), "dot.key");
    assert_eq!(key(&[N("a[0]"), N("b")]).unwrap(), "\"a[0]\".b");
    assert_eq!(key(&[N("a"), I(0), N("b")]).unwrap(), "a[0].b");
    let paths = [
        &[N("dot.key")][..],
        &[N("dot"), N("key")],
        &[N("a[0]"), N("b")],
        &[N("a"), I(0), N("b")],
    ];
    assert_eq!(key_sets(&paths, &[]).unwrap().honored.len(), 4);
}

#[test]
fn actual_nested_list_positions_have_decimal_no_padding() {
    assert_eq!(key(&[N("a"), I(0), I(10), N("")]).unwrap(), "a[0][10].\"\"");
    assert_eq!(
        key(&[N("a"), I(usize::MAX), N("b")]).unwrap(),
        format!("a[{}].b", usize::MAX)
    );
}

#[test]
fn missing_initial_names_refuse_instead_of_creating_keys() {
    assert_eq!(key(&[]), Err(Error::MissingInitialName));
    assert_eq!(key(&[I(0)]), Err(Error::MissingInitialName));
    assert_eq!(key(&[I(0), N("a")]), Err(Error::MissingInitialName));
    assert_eq!(key(&[N("a"), I(0)]), Err(Error::MissingFinalName));
    assert_eq!(key(&[N("a"), I(0), I(1)]), Err(Error::MissingFinalName));
    assert_eq!(key(&[N("")]).unwrap(), "\"\"");
}

#[test]
fn bare_scalar_boundary_is_exact_and_never_truncated() {
    assert_eq!(key(&[N(&"a".repeat(256))]).unwrap(), "a".repeat(256));
    assert_eq!(key(&[N(&"a".repeat(257))]), Err(Error::KeyTooLong));
    assert_eq!(key(&[N(&"a".repeat(255)), N("b")]), Err(Error::KeyTooLong));
    assert_eq!(key(&[N(&"a".repeat(254)), N("b")]).unwrap().len(), 256);
}

#[test]
fn encoded_unicode_boundary_counts_scalars_instead_of_utf8_bytes() {
    let encoded = key(&[N(&"é".repeat(254))]).unwrap();
    assert_eq!(encoded.chars().count(), 256);
    assert_eq!(encoded.len(), 510);
    assert_eq!(key(&[N(&"é".repeat(255))]), Err(Error::KeyTooLong));
    assert_ne!(key(&[N("é")]).unwrap(), key(&[N("e\u{301}")]).unwrap());
}

#[test]
fn escaped_controls_and_index_syntax_count_toward_full_boundary() {
    assert_eq!(
        key(&[N(&("\0".repeat(42) + "aa"))])
            .unwrap()
            .chars()
            .count(),
        256
    );
    assert_eq!(
        key(&[N(&("\0".repeat(42) + "aaa"))]),
        Err(Error::KeyTooLong)
    );
    assert_eq!(
        key(&[N(&"a".repeat(251)), I(0), N("b")])
            .unwrap()
            .chars()
            .count(),
        256
    );
    assert_eq!(
        key(&[N(&"a".repeat(252)), I(0), N("b")]),
        Err(Error::KeyTooLong)
    );
}

#[test]
fn sorting_is_invariant_under_every_three_key_insertion_permutation() {
    let paths = [vec![N("b")], vec![N("a")], vec![N("é")]];
    for permutation in [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0],
    ] {
        let input: Vec<_> = permutation.iter().map(|i| paths[*i].as_slice()).collect();
        assert_eq!(key_sets(&input, &[]).unwrap().honored, ["\"é\"", "a", "b"]);
    }
}

#[test]
fn each_complete_unique_set_has_exact_64_65_boundary() {
    let names: Vec<_> = (0..65).map(|n| format!("key{n:02}")).collect();
    let paths: Vec<_> = names.iter().map(|s| vec![N(s)]).collect();
    let refs: Vec<_> = paths.iter().map(Vec::as_slice).collect();
    assert_eq!(key_sets(&refs[..64], &[]).unwrap().honored.len(), 64);
    assert_eq!(key_sets(&[], &refs[..64]).unwrap().stripped.len(), 64);
    assert_eq!(key_sets(&refs, &[]), Err(Error::TooManyKeys));
    assert_eq!(key_sets(&[], &refs), Err(Error::TooManyKeys));
    let repeated = vec![paths[0].as_slice(); 65];
    assert_eq!(key_sets(&repeated, &[]).unwrap().honored, ["key00"]);
}

#[test]
fn supplied_cross_classification_refuses_without_partial_sets() {
    let a = [N("a")];
    let b = [N("b")];
    assert_eq!(key_sets(&[&a], &[&a]), Err(Error::CrossClassification));
    let data = key_sets(&[&a, &a], &[&b, &b]).unwrap();
    assert_eq!(data.honored, ["a"]);
    assert_eq!(data.stripped, ["b"]);
    assert!(key_sets(&[], &[]).unwrap().honored.is_empty());
    let too_long = [N(&"x".repeat(257))];
    assert_eq!(key_sets(&[&a, &too_long], &[&b]), Err(Error::KeyTooLong));
}

use super::group_indices;

#[test]
fn exact_fields_are_compared_without_concatenation() {
    let tuples = [
        ("ab", "c", ""),
        ("a", "bc", ""),
        ("a", "b", "z"),
        ("a", "b", "a"),
    ];
    assert_eq!(
        group_indices(&tuples),
        vec![vec![3], vec![2], vec![1], vec![0]]
    );
}

#[test]
fn raw_unicode_and_source_spelling_are_not_normalized() {
    let tuples = [
        ("é", "1", ""),
        ("e\u{301}", "1", ""),
        ("z", "1", ""),
        ("a", "1", "git+https://example.invalid/r?branch=a%2Fb#abc"),
        ("a", "1", "git+https://example.invalid/r?branch=a/b#abc"),
    ];
    assert_eq!(
        group_indices(&tuples),
        vec![vec![3], vec![4], vec![1], vec![2], vec![0]]
    );
}

#[test]
fn version_order_is_raw_bytes_not_semantic_versions() {
    let tuples = [("p", "2", "s"), ("p", "10", "s"), ("p", "1", "s")];
    assert_eq!(group_indices(&tuples), vec![vec![2], vec![1], vec![0]]);
}

#[test]
fn duplicate_tuples_keep_every_input_as_an_explicit_group() {
    let tuples = [
        ("b", "1", "s"),
        ("a", "1", "s"),
        ("b", "1", "s"),
        ("a", "1", "s"),
    ];
    assert_eq!(group_indices(&tuples), vec![vec![1, 3], vec![0, 2]]);
    let indices: Vec<usize> = group_indices(&tuples).into_iter().flatten().collect();
    let mut sorted = indices;
    sorted.sort_unstable();
    assert_eq!(sorted, vec![0, 1, 2, 3]);
}

#[test]
fn all_distinct_tuple_permutations_have_the_same_ordered_values() {
    let values = [("b", "1", "s"), ("a", "2", "s"), ("a", "1", "s")];
    let expected = vec![("a", "1", "s"), ("a", "2", "s"), ("b", "1", "s")];
    for permutation in [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0],
    ] {
        let input = permutation.map(|index| values[index]);
        let output: Vec<_> = group_indices(&input)
            .into_iter()
            .map(|group| input[group[0]])
            .collect();
        assert_eq!(output, expected);
    }
}

#[test]
fn empty_and_over_acquisition_count_remain_data_without_drop_rules() {
    assert!(group_indices(&[]).is_empty());
    let names: Vec<String> = (0..16385)
        .rev()
        .map(|index| format!("p{index:05}"))
        .collect();
    let input: Vec<_> = names.iter().map(|name| (name.as_str(), "1", "s")).collect();
    let output = group_indices(&input);
    assert_eq!(output.len(), 16385);
    assert_eq!(input[output[0][0]].0, "p00000");
    assert_eq!(input[output[16384][0]].0, "p16384");
    assert!(output.iter().all(|group| group.len() == 1));
}

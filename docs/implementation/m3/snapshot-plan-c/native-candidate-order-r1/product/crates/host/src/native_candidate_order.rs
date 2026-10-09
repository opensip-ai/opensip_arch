//! Unadmitted candidate tuple ordering data, not an importer or source capability.
//! Equal tuples remain explicit groups. Their policy and owning attempts stay external.

/// Group every supplied index by its exact raw `(name, version, sourceId)` tuple.
/// Groups follow ascending UTF-8 bytes field by field, without normalization,
/// source interpretation, key hashing, schema admission or population truncation.
/// Indices within an equal-tuple group remain in input order; this does not select
/// an acquisition order or duplicate policy for distinguishable source attempts.
pub(crate) fn group_indices(tuples: &[(&str, &str, &str)]) -> Vec<Vec<usize>> {
    let mut indices: Vec<usize> = (0..tuples.len()).collect();
    indices.sort_unstable_by(|&left, &right| {
        let left_tuple = tuples[left];
        let right_tuple = tuples[right];
        (
            left_tuple.0.as_bytes(),
            left_tuple.1.as_bytes(),
            left_tuple.2.as_bytes(),
        )
            .cmp(&(
                right_tuple.0.as_bytes(),
                right_tuple.1.as_bytes(),
                right_tuple.2.as_bytes(),
            ))
            .then_with(|| left.cmp(&right))
    });
    let mut groups: Vec<Vec<usize>> = Vec::with_capacity(tuples.len());
    for index in indices {
        match groups.last_mut() {
            Some(group) if tuples[group[0]] == tuples[index] => group.push(index),
            _ => groups.push(vec![index]),
        }
    }
    groups
}

#[cfg(test)]
#[path = "native_candidate_order_tests.rs"]
mod tests;

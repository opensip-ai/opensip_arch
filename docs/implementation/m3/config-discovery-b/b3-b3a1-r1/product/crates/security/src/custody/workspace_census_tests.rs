// Unit B3-b3a1's measured-against-model control (B3-b plan r2 section 4.2,
// amendment A5). tools/security/discovery_census.py predicts the whole D15
// composition's charges, the walker with its admitted members plus the
// reader, member and descent terms, for every accepted composition vector
// and for worst cases whose reads reach every cap (a 4 MiB carrier, a 64 KiB
// member configuration, a 4 MiB index, and H's global and five system
// sources at 64 KiB). Each is built as a scratch tree, composed natively with
// W spelled at each of the census's root lengths, and measured on the
// discovery ledger after item 6a: the discovery uses no more objects, edges
// or bytes than predicted.

const D15_PREDICTIONS: &[u8] = include_bytes!("discovery_census_vectors.json");
/// The census's root lengths (plan r4 section 2.1).
const ROOT_LENGTHS: [usize; 3] = [134, 1024, 4096];

/// An absolute spelling of exactly `length` bytes.
fn spelling_of(length: usize) -> PathBuf {
    Path::new(&format!("/{}", "r".repeat(length - 1))).to_path_buf()
}

/// `head`, then comment lines, to exactly `bytes` bytes: a Git configuration
/// item 6a parses and admits.
fn padded_config(head: &[u8], bytes: usize) -> Vec<u8> {
    let mut out = head.to_vec();
    while out.len() < bytes {
        let line = (bytes - out.len()).min(80);
        if line == 1 {
            out.push(b'\n');
            continue;
        }
        out.push(b'#');
        out.extend(std::iter::repeat_n(b'x', line - 2));
        out.push(b'\n');
    }
    out
}

/// A valid version-2 Git index of exactly `bytes` bytes: regular-file
/// entries of 72 and 80 bytes (paths `a` and `b` with seven and nine
/// digits), in path order, sealed with its SHA-1, so item 6b reads and
/// decodes it at that size.
fn valid_index(bytes: usize) -> Vec<u8> {
    let entries = bytes - 12 - 20;
    let wide = (0..=entries / 80)
        .find(|b| (entries - 80 * b).is_multiple_of(72))
        .expect("72a + 80b reaches the size");
    let narrow = (entries - 80 * wide) / 72;
    let mut out = b"DIRC".to_vec();
    out.extend_from_slice(&2u32.to_be_bytes());
    out.extend_from_slice(&((narrow + wide) as u32).to_be_bytes());
    let paths = (0..narrow)
        .map(|i| format!("a{i:07}"))
        .chain((0..wide).map(|i| format!("b{i:09}")));
    for path in paths {
        let start = out.len();
        out.extend_from_slice(&[0; 24]);
        out.extend_from_slice(&0o100644u32.to_be_bytes());
        out.extend_from_slice(&[0; 12]);
        out.extend_from_slice(&[0x11; 20]);
        out.extend_from_slice(&(path.len() as u16).to_be_bytes());
        out.extend_from_slice(path.as_bytes());
        let pad = 8 - ((out.len() - start) % 8);
        out.extend(std::iter::repeat_n(0, pad));
    }
    let seal = super::super::git_tracking::sha1(&out);
    out.extend_from_slice(&seal);
    assert_eq!(out.len(), bytes);
    out
}

fn write_mode(path: &Path, bytes: &[u8], mode: u32) {
    std::fs::write(path, bytes).unwrap();
    std::fs::set_permissions(path, std::fs::Permissions::from_mode(mode)).unwrap();
}

/// A worst case's pads: each member's configuration and index after `git
/// init`, H's two global sources, and the five system sources (returned).
fn padded(case: &V, home: &Path, w: &Path) -> Vec<PathBuf> {
    let V::Object(pads) = field(case, "gitPads") else {
        panic!("gitPads")
    };
    for (member, pad) in pads {
        let git = w.join(member).join(".git");
        if let V::Integer(n) = field(pad, "config") {
            let head = std::fs::read(git.join("config")).unwrap();
            write_mode(
                &git.join("config"),
                &padded_config(&head, n.get() as usize),
                0o644,
            );
        }
        if let V::Integer(n) = field(pad, "validIndex") {
            write_mode(&git.join("index"), &valid_index(n.get() as usize), 0o644);
        }
        if let V::Integer(n) = field(pad, "index") {
            write_mode(&git.join("index"), &vec![b'x'; n.get() as usize], 0o644);
        }
    }
    let size = |key: &str| match field(case, key) {
        V::Integer(n) => n.get() as usize,
        other => panic!("{other:?}"),
    };
    write_mode(
        &home.join(".gitconfig"),
        &padded_config(b"", size("homeSources")),
        0o644,
    );
    for dir in [home.join(".config"), home.join(".config/git")] {
        std::fs::create_dir(&dir).unwrap();
        std::fs::set_permissions(&dir, std::fs::Permissions::from_mode(0o755)).unwrap();
    }
    write_mode(
        &home.join(".config/git/config"),
        &padded_config(b"", size("homeSources")),
        0o644,
    );
    let parent = home.parent().unwrap();
    (0..5)
        .map(|i| {
            let path = parent.join(format!("system-{i}.gitconfig"));
            write_mode(&path, &padded_config(b"", size("systemSources")), 0o644);
            path
        })
        .collect()
}

/// One prediction measured at root length `r`: whether the composition
/// accepted, what it charged, and what was predicted there.
fn measured(
    prediction: &V,
    r: usize,
) -> (bool, opensip_platform::WorkCost, opensip_platform::WorkCost) {
    let id = text(field(prediction, "id"));
    let case = match text(field(prediction, "kind")) {
        "worst" => field(prediction, "case").clone(),
        _ => vector(id),
    };
    let (_s, home, _githome, w) = built(&case);
    let sources = if text(field(prediction, "kind")) == "worst" {
        padded(&case, &home, &w)
    } else {
        Vec::new()
    };
    let sources: Vec<&Path> = sources.iter().map(PathBuf::as_path).collect();
    let spelling = spelling_of(r);
    let (result, used) = discover_with(
        &home,
        &w,
        &upward_of(field(&case, "upward")),
        source_of(&case),
        None,
        Some(&spelling),
        &sources,
    );
    let accepted = matches!(
        result,
        Ok(WorkspaceDiscovery {
            result: DiscoveryResultV3::Accept(_),
            ..
        })
    );
    let number = |key: &str| match field(prediction, key) {
        V::Integer(n) => n.get() as usize,
        other => panic!("{id} {key}: {other:?}"),
    };
    let predicted = opensip_platform::WorkCost {
        objects: number("objects"),
        edges: number("edges"),
        bytes: number("bytes") + number("bytesPerRootByte") * r,
    };
    (accepted, used, predicted)
}

#[test]
fn the_census_bounds_the_composed_discovery_at_every_root_length() {
    churned(|| {
        let body = parse_json(D15_PREDICTIONS).unwrap();
        let predictions = items(field(&body, "compositionCases"));
        let worst = predictions
            .iter()
            .filter(|p| text(field(p, "kind")) == "worst")
            .count();
        assert!(predictions.len() > worst && worst >= 2);
        for prediction in predictions {
            let id = text(field(prediction, "id"));
            for r in ROOT_LENGTHS {
                let (accepted, used, predicted) = measured(prediction, r);
                assert!(accepted, "{id} at R={r}: the composition did not accept");
                assert!(
                    used.objects <= predicted.objects
                        && used.edges <= predicted.edges
                        && used.bytes <= predicted.bytes,
                    "{id} at R={r}: the composition used {used:?}; the census predicts {predicted:?}"
                );
                // The tightness, for review.
                println!(
                    "d15-soundness {id} R={r} used {} {} {} predicted {} {} {}",
                    used.objects,
                    used.edges,
                    used.bytes,
                    predicted.objects,
                    predicted.edges,
                    predicted.bytes
                );
            }
        }
    });
}

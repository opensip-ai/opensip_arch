mod core { pub use cargo::core::SourceId; }
#[path = "../native-source-join-kernel-2026-10-09/source_join.rs"]
mod comparison;
mod source_view;
use cargo::core::SourceId;
use source_view::MetadataSourceView;

fn main() {
    let cases = [
        "registry+https://example.com/index",
        "sparse+https://example.com/index/",
        "git+https://example.com/repo#arbitrary-precise",
        "git+https://example.com/repo?branch=topic%2Ffoo%2Bbar#same",
        "git+https://example.com/repo?branch=topic+foo#same",
        "git+https://example.com/repo?branch=topic%26foo%3Dbar#same",
        "git+https://example.com/repo?branch=%E9%9B%AA#same",
        "git+https://example.com/repo?tag=v%2B1#same",
        "git+https://example.com/repo?rev=a%2Bb#same",
        "git+https://github.com/Example/Repo.git?branch=a%2Bb#same",
    ];
    for raw in cases {
        let source = SourceId::from_url(raw).unwrap();
        let rendered = serde_json::to_value(MetadataSourceView(source)).unwrap();
        let text = rendered.as_str().unwrap();
        let joined = comparison::compare_nonpath(raw, Some(text)).unwrap();
        assert_eq!(joined.original_lock_source, raw);
        assert_eq!(joined.original_metadata_source, text);
        assert_eq!(joined.lock_source, joined.metadata_source);
        assert!(joined.lock_source.has_same_precise_as(joined.metadata_source));
        println!("{}", serde_json::json!({"originalLockSource":raw,"metadataSource":text,"comparison":true}));
    }
    let path = SourceId::from_url("path+file:///tmp/source-view-fixture").unwrap();
    assert_eq!(serde_json::to_value(MetadataSourceView(path)).unwrap(), serde_json::Value::Null);
    let plus = SourceId::from_url(cases[3]).unwrap();
    let stock = serde_json::to_value(plus).unwrap();
    assert!(comparison::compare_nonpath(cases[3], stock.as_str()).is_err());
    let a = SourceId::from_url("git+https://example.com/repo?branch=a%2Bb#one").unwrap();
    let b = SourceId::from_url("git+https://example.com/repo?branch=a%2Bb#two").unwrap();
    let rendered_b = serde_json::to_value(MetadataSourceView(b)).unwrap();
    assert!(comparison::compare_nonpath(&a.as_encoded_url().to_string(), rendered_b.as_str()).is_err());
    println!("13 source field controls PASS; no producer/admission integration");
}

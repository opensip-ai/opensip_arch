extern crate alloc;
mod logical_path;
struct GzipChecksum { crc: u32, isize: u32 }
impl GzipChecksum {
    fn new() -> Self { Self { crc: u32::MAX, isize: 0 } }
    fn update(&mut self, bytes: &[u8]) {
        for &byte in bytes {
            self.crc ^= u32::from(byte);
            for _ in 0..8 { self.crc = (self.crc >> 1) ^ (0xedb88320 & 0u32.wrapping_sub(self.crc & 1)); }
        }
        self.isize = self.isize.wrapping_add(bytes.len() as u32);
    }
    fn trailer(&self) -> [u8; 8] {
        let mut trailer = [0; 8];
        trailer[..4].copy_from_slice(&(!self.crc).to_le_bytes());
        trailer[4..].copy_from_slice(&self.isize.to_le_bytes()); trailer
    }
}
use std::io::{self, Read};
use miniz_oxide::inflate::{core::{DecompressorOxide, decompress_with_limit, inflate_flags::TINFL_FLAG_HAS_MORE_INPUT}, TINFLStatus};
#[derive(Debug, PartialEq, Eq)]
enum Failure { Io(io::ErrorKind), Truncated, Header, Name, Deflate, Ratio, Trailer, Tail, Consumer, Invariant }
struct Input<R> { reader: R, buffer: [u8;4096], at: usize, end: usize, eof: bool, consumed: u128 }
impl<R: Read> Input<R> {
    fn new(reader: R) -> Self { Self { reader, buffer:[0;4096], at:0, end:0, eof:false, consumed:0 } }
    fn refill(&mut self) -> Result<(), Failure> {
        if self.at != self.end || self.eof { return Ok(()); }
        loop {
            match self.reader.read(&mut self.buffer) {
                Ok(n) => { if n > self.buffer.len() { return Err(Failure::Invariant); } self.at=0;self.end=n;self.eof=n==0;return Ok(()); }
                Err(e) if e.kind()==io::ErrorKind::Interrupted => (),
                Err(e) => return Err(Failure::Io(e.kind())),
            }
        }
    }
    fn byte(&mut self) -> Result<Option<u8>, Failure> {
        self.refill()?;
        if self.at==self.end { return Ok(None); }
        let value=self.buffer[self.at];self.at+=1;
        self.consumed=self.consumed.checked_add(1).ok_or(Failure::Invariant)?;Ok(Some(value))
    }
    fn required_byte(&mut self) -> Result<u8, Failure> { self.byte()?.ok_or(Failure::Truncated) }
}
#[derive(Debug, PartialEq, Eq)]
struct Report { compressed: u128, inflated: u128 }
fn ratio(compressed:u128,inflated:u128) -> Result<(),Failure> {
    let left=compressed.checked_mul(100).ok_or(Failure::Invariant)?;
    let right=inflated.checked_mul(101).and_then(|n|n.checked_add(100*1048576)).ok_or(Failure::Invariant)?;
    if left>right {Err(Failure::Ratio)} else {Ok(())}
}
fn decode<R:Read>(reader:R, mut receive:impl FnMut(&[u8])->Result<(),()>) -> Result<Report,Failure> {
    let mut input=Input::new(reader);let mut header=[0u8;10];
    for b in &mut header {*b=input.required_byte()?;}
    if header[..3]!=[0x1f,0x8b,8] || header[3]&!9!=0 {return Err(Failure::Header);}
    if header[3]&8!=0 {
        let mut terminated=false;
        // Explicit probe interpretation: the field cap includes its NUL.
        for _ in 0..4096 {if input.required_byte()?==0 {terminated=true;break;}}
        if !terminated {return Err(Failure::Name);}
    }
    let mut decoder=DecompressorOxide::new();let mut ring=[0u8;32768];
    let mut offset=0;let mut inflated=0u128;let mut checksum=GzipChecksum::new();
    loop {
        input.refill()?;
        let flags=if input.eof {0} else {TINFL_FLAG_HAS_MORE_INPUT};
        let remaining=ring.len()-offset;
        let (status,used,made)=decompress_with_limit(&mut decoder,&input.buffer[input.at..input.end],&mut ring,offset,remaining,flags);
        if used>input.end-input.at || made>remaining {return Err(Failure::Invariant);}
        input.at+=used;input.consumed=input.consumed.checked_add(used as u128).ok_or(Failure::Invariant)?;
        inflated=inflated.checked_add(made as u128).ok_or(Failure::Invariant)?;
        ratio(input.consumed,inflated)?;
        let bytes=&ring[offset..offset+made];checksum.update(bytes);
        if !bytes.is_empty() {receive(bytes).map_err(|_|Failure::Consumer)?;}
        offset=(offset+made)%ring.len();
        match status {
            TINFLStatus::Done => break,
            TINFLStatus::NeedsMoreInput | TINFLStatus::HasMoreOutput if used!=0 || made!=0 => (),
            _ => return Err(Failure::Deflate),
        }
    }
    let mut trailer=[0u8;8];
    for b in &mut trailer {*b=input.required_byte()?;ratio(input.consumed,inflated)?;}
    if trailer!=checksum.trailer() {return Err(Failure::Trailer);}
    let consumed=input.consumed;
    if input.byte()?.is_some() {return Err(Failure::Tail);}
    Ok(Report {compressed:consumed,inflated})
}
struct ShortReader<'a> {bytes:&'a[u8],chunk:usize,largest_request:usize}
impl Read for ShortReader<'_> {
    fn read(&mut self,out:&mut[u8])->io::Result<usize> {
        self.largest_request=self.largest_request.max(out.len());
        let n=out.len().min(self.chunk).min(self.bytes.len());out[..n].copy_from_slice(&self.bytes[..n]);self.bytes=&self.bytes[n..];Ok(n)
    }
}
#[test]
fn original_sources_and_independent_streams_use_bounded_reads_and_complete_oracles() {
    let root=std::path::Path::new(env!("C3_STREAM_PROBE_ROOT"));
    for name in ["miniz_oxide-0.9.1.original.crate","adler2-2.0.1.original.crate","ring-wrap.gzip","empty.gzip","incompressible.gzip"] {
        let compressed=std::fs::read(root.join(name)).unwrap();
        let stem=name.strip_suffix(".original.crate").or_else(||name.strip_suffix(".gzip")).unwrap();
        let expected=std::fs::read(root.join(format!("{stem}.inflated"))).unwrap();
        for chunk in [1,7,4096] {
            let mut reader=ShortReader {bytes:&compressed,chunk,largest_request:0};let mut output=Vec::new();let mut largest_output=0;
            let report=decode(&mut reader,|bytes|{largest_output=largest_output.max(bytes.len());output.extend_from_slice(bytes);Ok(())}).unwrap();
            assert_eq!(output,expected,"{name}/{chunk}");assert_eq!(report,Report {compressed:compressed.len() as u128,inflated:expected.len() as u128});
            assert!(reader.largest_request<=4096 && largest_output<=32768);
        }
    }
}
#[test]
fn truncated_crc_size_extra_member_and_tail_refuse() {
    let root=std::path::Path::new(env!("C3_STREAM_PROBE_ROOT"));let bytes=std::fs::read(root.join("empty.gzip")).unwrap();
    for n in 0..bytes.len() {assert!(decode(&bytes[..n],|_|Ok(())).is_err(),"prefix {n}");}
    for at in [2,bytes.len()-8,bytes.len()-4] {let mut bad=bytes.clone();bad[at]^=1;assert!(decode(bad.as_slice(),|_|Ok(())).is_err());}
    let mut second=bytes.clone();second.extend_from_slice(&bytes);assert_eq!(decode(second.as_slice(),|_|Ok(())),Err(Failure::Tail));
    let mut tail=bytes.clone();tail.push(0);assert_eq!(decode(tail.as_slice(),|_|Ok(())),Err(Failure::Tail));
}
#[test]
fn flags_and_fname_boundary_are_checked_without_whole_input_materialization() {
    let root=std::path::Path::new(env!("C3_STREAM_PROBE_ROOT"));let bytes=std::fs::read(root.join("empty.gzip")).unwrap();
    for flag in [2,4,16,32,64,128] {let mut bad=bytes.clone();bad[3]=flag;assert_eq!(decode(bad.as_slice(),|_|Ok(())),Err(Failure::Header));}
    for len in [0,4095,4096] {
        let mut named=bytes.clone();named[3]=9;named.splice(10..10,std::iter::repeat_n(b'x',len).chain([0]));
        let result=decode(named.as_slice(),|_|Ok(()));if len<4096 {assert!(result.is_ok());} else {assert_eq!(result,Err(Failure::Name));}
    }
}
#[test]
fn consumption_guard_includes_trailer_and_consumer_can_stop_immediately() {
    fn member(n:usize)->Vec<u8> {let mut b=vec![0x1f,0x8b,8,0,0,0,0,0,0,255];for _ in 0..n {b.extend_from_slice(&[0,0,0,255,255]);}b.extend_from_slice(&[1,0,0,255,255]);b.extend_from_slice(&[0;8]);b}
    let below=member(209710);assert!(decode(below.as_slice(),|_|Ok(())).is_ok());
    let above=member(209711);assert_eq!(decode(above.as_slice(),|_|Ok(())),Err(Failure::Ratio));
    let root=std::path::Path::new(env!("C3_STREAM_PROBE_ROOT"));let bytes=std::fs::read(root.join("incompressible.gzip")).unwrap();
    let mut reader=ShortReader {bytes:&bytes,chunk:4096,largest_request:0};let mut calls=0;
    assert_eq!(decode(&mut reader,|_|{calls+=1;Err(())}),Err(Failure::Consumer));assert_eq!(calls,1);assert!(!reader.bytes.is_empty());
}

#[derive(Debug, PartialEq, Eq)]
enum TarFailure { Magic, Checksum, Size, Type, LongShape, LongChain, LongPrefix, OrphanLong, End, Truncated, Invariant, Path, Duplicate }
enum TarMode { Header([u8;512],usize), Body {left:u128,regular:bool,control:Vec<u8>,padding:usize}, Padding(usize), End(usize) }
struct Framer {mode:TarMode,pending:Option<Vec<u8>>,inflated:u128,content:u128,regular:u128,long_records:u128, paths:Option<PathProfile>}
fn octal(field:&[u8])->Result<u128,TarFailure> {
    let start=field.iter().position(|b|!matches!(b,b' '|0)).unwrap_or(field.len());
    let end=field.iter().rposition(|b|!matches!(b,b' '|0)).map_or(start,|n|n+1);
    field[start..end].iter().try_fold(0u128,|n,&b| if (b'0'..=b'7').contains(&b) {n.checked_mul(8).and_then(|n|n.checked_add(u128::from(b-b'0'))).ok_or(TarFailure::Size)} else {Err(TarFailure::Size)})
}
fn size(field:&[u8])->Result<u128,TarFailure> {
    if field[0]&128==0 {return octal(field);}
    if field[0]&64!=0 {return Err(TarFailure::Size);}
    let n=field.iter().enumerate().try_fold(0u128,|n,(i,&b)|n.checked_mul(256).and_then(|n|n.checked_add(u128::from(if i==0 {b&127} else {b}))).ok_or(TarFailure::Size))?;
    let octal_max=(1u128<<(3*(field.len()-1)))-1;
    if n<=octal_max {Err(TarFailure::Size)} else {Ok(n)}
}
fn name(field:&[u8])->&[u8] {&field[..field.iter().position(|b|*b==0).unwrap_or(field.len())]}
impl Framer {
    fn new()->Self {Self {mode:TarMode::Header([0;512],0),pending:None,inflated:0,content:0,regular:0,long_records:0,paths:None}}
    fn for_package(name:&str,version:&str)->Self {let mut f=Self::new();f.paths=Some(PathProfile {prefix:format!("{name}-{version}/"),seen:std::collections::BTreeSet::new()});f}
    fn account(&mut self,n:usize,content:bool)->Result<(),TarFailure> {
        self.inflated=self.inflated.checked_add(n as u128).ok_or(TarFailure::Invariant)?;
        if content {self.content=self.content.checked_add(n as u128).ok_or(TarFailure::Invariant)?;}
        let allowed=self.regular.checked_add(1).and_then(|n|n.checked_mul(18432)).and_then(|n|n.checked_add(10240)).ok_or(TarFailure::Invariant)?;
        if self.inflated-self.content>allowed {return Err(TarFailure::Invariant);}
        Ok(())
    }
    fn header(&mut self,h:[u8;512])->Result<TarMode,TarFailure> {
        if h.iter().all(|b|*b==0) {if self.pending.is_some() {return Err(TarFailure::OrphanLong);}return Ok(TarMode::End(512));}
        if &h[257..265]!=b"ustar  \0" {return Err(TarFailure::Magic);}
        let checksum=h.iter().enumerate().map(|(i,&b)|u128::from(if (148..156).contains(&i) {b' '} else {b})).sum::<u128>();
        if octal(&h[148..156]).map_err(|_|TarFailure::Checksum)?!=checksum {return Err(TarFailure::Checksum);}
        let n=size(&h[124..136])?;let padding=((512-n%512)%512) as usize;
        match h[156] {
            b'0'=>{
                let effective=if let Some(long)=self.pending.take() {if !long.starts_with(name(&h[..100])) {return Err(TarFailure::LongPrefix);}long} else {name(&h[..100]).to_vec()};
                if let Some(profile)=&mut self.paths {profile.admit(&effective)?;}
                self.regular+=1;Ok(TarMode::Body {left:n,regular:true,control:Vec::new(),padding})
            }
            b'L'=>{
                if self.pending.is_some() {return Err(TarFailure::LongChain);}
                if name(&h[..100])!=b"././@LongLink" || !(2..=16385).contains(&n) {return Err(TarFailure::LongShape);}
                self.long_records+=1;Ok(TarMode::Body {left:n,regular:false,control:Vec::with_capacity(n as usize),padding})
            }
            _=>Err(TarFailure::Type),
        }
    }
    fn feed(&mut self,mut bytes:&[u8])->Result<(),TarFailure> {
        while !bytes.is_empty() {
            let mode=std::mem::replace(&mut self.mode,TarMode::Header([0;512],0));
            self.mode=match mode {
                TarMode::Header(mut h,used)=>{
                    let n=(512-used).min(bytes.len());h[used..used+n].copy_from_slice(&bytes[..n]);bytes=&bytes[n..];self.account(n,false)?;
                    if used+n==512 {self.header(h)?} else {TarMode::Header(h,used+n)}
                }
                TarMode::Body {left,regular,mut control,padding}=>{
                    let n=(left.min(bytes.len() as u128)) as usize;
                    if !regular {control.extend_from_slice(&bytes[..n]);}bytes=&bytes[n..];self.account(n,regular)?;
                    if left==n as u128 {
                        if !regular {
                            if control.last()!=Some(&0) || control[..control.len()-1].contains(&0) {return Err(TarFailure::LongShape);}
                            control.pop();let text=std::str::from_utf8(&control).map_err(|_|TarFailure::LongShape)?;
                            if text.chars().count()>4096 {return Err(TarFailure::LongShape);}self.pending=Some(control);
                        }
                        TarMode::Padding(padding)
                    } else {TarMode::Body {left:left-n as u128,regular,control,padding}}
                }
                TarMode::Padding(left)=>{
                    let n=left.min(bytes.len());bytes=&bytes[n..];self.account(n,false)?;
                    if left==n {TarMode::Header([0;512],0)} else {TarMode::Padding(left-n)}
                }
                TarMode::End(total)=>{
                    let n=bytes.len().min(10241-total);
                    if bytes[..n].iter().any(|b|*b!=0) || total+n>10240 {return Err(TarFailure::End);}
                    bytes=&bytes[n..];self.account(n,false)?;TarMode::End(total+n)
                }
            };
        }
        Ok(())
    }
    fn finish(&self)->Result<(),TarFailure> {
        if self.pending.is_some() {return Err(TarFailure::OrphanLong);}
        match self.mode {TarMode::End(n) if (1024..=10240).contains(&n) && n%512==0=>Ok(()),TarMode::End(_)=>Err(TarFailure::End),_=>Err(TarFailure::Truncated)}
    }
}
fn gnu_header(path:&[u8],kind:u8,n:u64)->[u8;512] {
    let mut h=[0u8;512];let width=path.len().min(100);h[..width].copy_from_slice(&path[..width]);
    h[124..136].copy_from_slice(format!("{n:011o}\0").as_bytes());h[156]=kind;h[257..265].copy_from_slice(b"ustar  \0");h[148..156].fill(b' ');
    let sum=h.iter().map(|&b|u64::from(b)).sum::<u64>();h[148..156].copy_from_slice(format!("{sum:06o}\0 ").as_bytes());h
}
fn entry(output:&mut Vec<u8>,path:&[u8],kind:u8,body:&[u8]) {output.extend_from_slice(&gnu_header(path,kind,body.len() as u64));output.extend_from_slice(body);let pad=(512-body.len()%512)%512;output.extend(std::iter::repeat_n(0,pad));}
fn framing(bytes:&[u8],chunk:usize)->Result<Framer,TarFailure> {let mut f=Framer::new();for b in bytes.chunks(chunk) {f.feed(b)?;}f.finish()?;Ok(f)}
#[test]
fn original_gnu_archives_frame_incrementally_after_streamed_gzip() {
    let root=std::path::Path::new(env!("C3_STREAM_PROBE_ROOT"));
    for (n,expected_files) in [("miniz_oxide-0.9.1",0u128),("adler2-2.0.1",0)] {
        let compressed=std::fs::read(root.join(format!("{n}.original.crate"))).unwrap();
        let mut f=Framer::new();decode(compressed.as_slice(),|b|f.feed(b).map_err(|_|())).unwrap();f.finish().unwrap();
        assert!(f.regular>expected_files);assert_eq!(f.inflated,std::fs::metadata(root.join(format!("{n}.inflated"))).unwrap().len() as u128);
        let inflated=std::fs::read(root.join(format!("{n}.inflated"))).unwrap();
        for chunk in [1,7,511,512,32768] {let other=framing(&inflated,chunk).unwrap();assert_eq!((other.regular,other.content,other.inflated),(f.regular,f.content,f.inflated));}
    }
}
#[test]
fn longest_long_payload_and_end_region_boundaries_preserve_framing_allowance() {
    let long="\u{1f600}".repeat(4096).into_bytes();assert_eq!(long.len(),16384);
    let mut payload=long.clone();payload.push(0);
    let mut bytes=Vec::new();entry(&mut bytes,b"././@LongLink",b'L',&payload);entry(&mut bytes,&long[..100],b'0',b"x");bytes.extend([0;1024]);
    for chunk in [1,7,512,32768] {let f=framing(&bytes,chunk).unwrap();assert_eq!((f.regular,f.long_records,f.content),(1,1,1));assert_eq!(f.inflated-f.content,19455);}
    for end in [512,1024,10240,10752] {let zeros=vec![0;end];let result=framing(&zeros,7);assert_eq!(result.is_ok(),matches!(end,1024|10240));}
    assert_eq!(framing(&vec![0;10241],512).err(),Some(TarFailure::End));
}
#[test]
fn malformed_control_sequences_and_entry_types_refuse_before_unbounded_work() {
    for kind in [0,b'1',b'2',b'K',b'3',b'4',b'6',b'5',b'7',b'x',b'g',b'S',b'M',b'V',b'N',b'Z'] {let mut bytes=Vec::new();entry(&mut bytes,b"a-1/file",kind,b"");bytes.extend([0;1024]);assert_eq!(framing(&bytes,7).err(),Some(TarFailure::Type));}
    let mut orphan=Vec::new();entry(&mut orphan,b"././@LongLink",b'L',b"a-1/long\0");orphan.extend([0;1024]);assert_eq!(framing(&orphan,7).err(),Some(TarFailure::OrphanLong));
    let mut chained=Vec::new();entry(&mut chained,b"././@LongLink",b'L',b"a-1/long\0");entry(&mut chained,b"././@LongLink",b'L',b"a-1/next\0");assert_eq!(framing(&chained,7).err(),Some(TarFailure::LongChain));
    let mut mismatched=Vec::new();entry(&mut mismatched,b"././@LongLink",b'L',b"a-1/long\0");entry(&mut mismatched,b"different",b'0',b"");assert_eq!(framing(&mismatched,7).err(),Some(TarFailure::LongPrefix));
    let mut oversized=gnu_header(b"././@LongLink",b'L',16386).to_vec();oversized.extend([0;512]);assert_eq!(framing(&oversized,7).err(),Some(TarFailure::LongShape));
}
#[test]
fn gnu_base256_is_positive_and_above_the_octal_range_and_checksum_is_independent() {
    let mut field=[0u8;12];field[0]=128;field[4..].copy_from_slice(&(1u64<<33).to_be_bytes());assert_eq!(size(&field),Ok(1u128<<33));
    field[4..].copy_from_slice(&((1u64<<33)-1).to_be_bytes());assert_eq!(size(&field),Err(TarFailure::Size));field[0]=255;assert_eq!(size(&field),Err(TarFailure::Size));
    let mut bytes=Vec::new();entry(&mut bytes,b"a-1/file",b'0',b"x");bytes.extend([0;1024]);bytes[100]^=1;assert_eq!(framing(&bytes,7).err(),Some(TarFailure::Checksum));
}

struct PathProfile {prefix:String,seen:std::collections::BTreeSet<String>}
impl PathProfile {
    fn admit(&mut self,path:&[u8])->Result<(),TarFailure> {
        let text=std::str::from_utf8(path).map_err(|_|TarFailure::Path)?;
        let remainder=text.strip_prefix(&self.prefix).ok_or(TarFailure::Path)?;
        let admitted=logical_path::LogicalPath::parse(remainder).map_err(|_|TarFailure::Path)?;assert_eq!(admitted.as_str(),remainder);assert_eq!(admitted.into_string(),remainder);
        if !self.seen.insert(text.to_owned()) {return Err(TarFailure::Duplicate);}Ok(())
    }
}
fn package(bytes:&[u8],name:&str,version:&str,chunk:usize)->Result<Framer,TarFailure> {
    let mut f=Framer::for_package(name,version);for b in bytes.chunks(chunk) {f.feed(b)?;}f.finish()?;Ok(f)
}
#[test]
fn exact_original_packages_validate_paths_without_normalization() {
    let root=std::path::Path::new(env!("C3_STREAM_PROBE_ROOT"));
    for (name,version) in [("miniz_oxide","0.9.1"),("adler2","2.0.1")] {
        let bytes=std::fs::read(root.join(format!("{name}-{version}.inflated"))).unwrap();
        let compressed=std::fs::read(root.join(format!("{name}-{version}.original.crate"))).unwrap();let mut streamed=Framer::for_package(name,version);decode(compressed.as_slice(),|b|streamed.feed(b).map_err(|_|())).unwrap();streamed.finish().unwrap();
        for chunk in [1,7,512,32768] {let f=package(&bytes,name,version,chunk).unwrap();assert_eq!(f.paths.as_ref().unwrap().seen.len() as u128,f.regular); let expected=match name {"miniz_oxide"=>(23u128,296000u128), "adler2"=>(13u128,38832u128),_=>unreachable!()};assert_eq!((f.regular,f.content),expected);}
    }
}
#[test]
fn package_prefix_and_logical_path_are_exact_and_utf8_checked() {
    for path in [b"a-1/".as_slice(),b"b-1/file",b"a-10/file",b"a-1//file",b"a-1/./file",b"a-1/../file",b"a-1/x/..",b"a-1/x\\y",b"a-1/\xff"] {
        let mut bytes=Vec::new();entry(&mut bytes,path,b'0',b"");bytes.extend([0;1024]);assert_eq!(package(&bytes,"a","1",7).err(),Some(TarFailure::Path),"{path:?}");
    }
    for path in ["a-1/file", "a-1/x\n/y", "a-1/é/😀"] {let mut bytes=Vec::new();entry(&mut bytes,path.as_bytes(),b'0',b"x");bytes.extend([0;1024]);assert!(package(&bytes,"a","1",7).is_ok());}
}
#[test]
fn duplicates_compare_effective_long_and_short_paths_even_when_content_differs() {
    let mut bytes=Vec::new();entry(&mut bytes,b"a-1/file",b'0',b"first");entry(&mut bytes,b"././@LongLink",b'L',b"a-1/file\0");entry(&mut bytes,b"a-1/",b'0',b"second");bytes.extend([0;1024]);
    for chunk in [1,7,32768] {assert_eq!(package(&bytes,"a","1",chunk).err(),Some(TarFailure::Duplicate));}
    let path=format!("a-1/{}/file", "é".repeat(100));let mut payload=path.as_bytes().to_vec();payload.push(0);
    let mut valid=Vec::new();entry(&mut valid,b"././@LongLink",b'L',&payload);entry(&mut valid,&path.as_bytes()[..100],b'0',b"x");valid.extend([0;1024]);
    let f=package(&valid,"a","1",7).unwrap();assert!(f.paths.unwrap().seen.contains(&path));
}

#[test]
fn long_name_payload_encoding_and_immediate_successor_are_strict() {
    let mut oversized_scalars="x".repeat(4097).into_bytes();oversized_scalars.push(0);
    for payload in [vec![0],vec![b'x'],vec![b'x',0,0],vec![b'x',0,b'y',0],vec![0xff,0],oversized_scalars] {
        let mut bytes=Vec::new();entry(&mut bytes,b"././@LongLink",b'L',&payload);entry(&mut bytes,b"x",b'0',b"");bytes.extend([0;1024]);
        assert_eq!(framing(&bytes,7).err(),Some(TarFailure::LongShape));
    }
    let mut smallest=Vec::new();entry(&mut smallest,b"././@LongLink",b'L',b"x\0");entry(&mut smallest,b"x",b'0',b"");smallest.extend([0;1024]);assert!(framing(&smallest,1).is_ok());
    let mut wrong_name=Vec::new();entry(&mut wrong_name,b"././@LongLink/",b'L',b"x\0");assert_eq!(framing(&wrong_name,7).err(),Some(TarFailure::LongShape));
    for kind in [b'1',b'5',b'x'] {let mut bytes=Vec::new();entry(&mut bytes,b"././@LongLink",b'L',b"x\0");entry(&mut bytes,b"x",kind,b"");assert_eq!(framing(&bytes,7).err(),Some(TarFailure::Type));}
}

#[test]
fn long_header_byte_prefix_may_split_utf8() {
    let path=format!("ab-1/{}/file", "😀".repeat(40));
    let short=&path.as_bytes()[..100];
    assert!(std::str::from_utf8(short).is_err());
    let mut payload=path.as_bytes().to_vec();payload.push(0);
    let mut bytes=Vec::new();entry(&mut bytes,b"././@LongLink",b'L',&payload);entry(&mut bytes,short,b'0',b"x");bytes.extend([0;1024]);
    for chunk in [1,7,511,512,32768] {
        let f=package(&bytes,"ab","1",chunk).unwrap();
        assert_eq!((f.regular,f.long_records,f.content),(1,1,1));
        assert!(f.paths.unwrap().seen.contains(&path));
    }
}

#[derive(Debug, PartialEq, Eq)]
enum ProfileFailure { Gzip(Failure), Tar(TarFailure) }
fn decode_package<R:Read>(reader:R,name:&str,version:&str)->Result<(Report,Framer),ProfileFailure> {
    let mut framer=Framer::for_package(name,version);
    let mut cause=None;
    let outcome=decode(reader,|bytes| match framer.feed(bytes) {
        Ok(())=>Ok(()),
        Err(error)=>{cause=Some(error);Err(())}
    });
    let report=match outcome {
        Ok(report)=>report,
        Err(Failure::Consumer)=>return Err(ProfileFailure::Tar(cause.expect("fallible consumer retained its cause"))),
        Err(error)=>return Err(ProfileFailure::Gzip(error)),
    };
    framer.finish().map_err(ProfileFailure::Tar)?;
    Ok((report,framer))
}
fn stored_gzip(bytes:&[u8])->Vec<u8> {
    let mut output=vec![0x1f,0x8b,8,0,0,0,0,0,0,255];
    if bytes.is_empty() {output.extend_from_slice(&[1,0,0,255,255]);}
    let chunks=bytes.chunks(65535);
    let total=chunks.len();
    for (i,chunk) in chunks.enumerate() {
        output.push(u8::from(i+1==total));
        let n=chunk.len() as u16;output.extend_from_slice(&n.to_le_bytes());output.extend_from_slice(&(!n).to_le_bytes());output.extend_from_slice(chunk);
    }
    let mut sum=GzipChecksum::new();sum.update(bytes);output.extend_from_slice(&sum.trailer());output
}
#[test]
fn streamed_profile_preserves_consumer_errors_and_finish_errors() {
    let mut duplicate=Vec::new();entry(&mut duplicate,b"a-1/file",b'0',b"first");entry(&mut duplicate,b"a-1/file",b'0',b"different");duplicate.extend([0;1024]);
    let zipped=stored_gzip(&duplicate);
    for chunk in [1,7,511,4096] {
        let reader=ShortReader {bytes:&zipped,chunk,largest_request:0};
        assert_eq!(decode_package(reader,"a","1").err(),Some(ProfileFailure::Tar(TarFailure::Duplicate)));
    }
    let mut valid=Vec::new();entry(&mut valid,b"a-1/file",b'0',b"x");valid.extend([0;1024]);let zipped=stored_gzip(&valid);
    let (report,framer)=decode_package(zipped.as_slice(),"a","1").unwrap();assert_eq!(report.inflated,valid.len() as u128);assert_eq!(framer.content,1);
    assert_eq!(decode_package(stored_gzip(&valid[..valid.len()-512]).as_slice(),"a","1").err(),Some(ProfileFailure::Tar(TarFailure::End)));
    let mut corrupt=zipped;let n=corrupt.len();corrupt[n-8]^=1;
    assert_eq!(decode_package(corrupt.as_slice(),"a","1").err(),Some(ProfileFailure::Gzip(Failure::Trailer)));
    let mut bad_path=Vec::new();entry(&mut bad_path,b"a-1/../file",b'0',b"");bad_path.extend([0;1024]);
    assert_eq!(decode_package(stored_gzip(&bad_path).as_slice(),"a","1").err(),Some(ProfileFailure::Tar(TarFailure::Path)));
}

#[test]
fn exact_pinned_cargo_long_name_archive_passes_incremental_profile() {
    let bytes=std::fs::read("/tmp/opensip-implementation/c3-pinned-producer-source/target/package/opensip-c3-archive-probe-0.1.0.crate").unwrap();
    for chunk in [1,7,511,512,4096,32768] {
        let mut reader=ShortReader {bytes:&bytes,chunk,largest_request:0};
        let (report,framer)=decode_package(&mut reader,"opensip-c3-archive-probe","0.1.0").unwrap();
        assert_eq!(report,Report {compressed:938,inflated:10752});
        assert_eq!((framer.regular,framer.content),(5,4660));
        assert!(framer.long_records>=1);
        assert!(reader.largest_request<=4096);
    }
}

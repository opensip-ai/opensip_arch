use std::io::{self,BufRead,Write};
use unicode_normalization::{UnicodeNormalization,is_nfc,UNICODE_VERSION};
fn main(){
 assert_eq!(UNICODE_VERSION,(16,0,0));
 let input=io::stdin();let mut output=io::BufWriter::new(io::stdout().lock());
 for line in input.lock().lines(){let line=line.unwrap();let chars=line.split_whitespace().map(|h|char::from_u32(u32::from_str_radix(h,16).unwrap()).unwrap());let s=chars.collect::<String>();let normalized=s.nfc().collect::<String>();assert_eq!(is_nfc(&s),normalized==s);write!(output,"{};",is_nfc(&s)).unwrap();for ch in normalized.chars(){write!(output,"{:x} ",ch as u32).unwrap();}writeln!(output).unwrap();}
}

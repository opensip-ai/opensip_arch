"""Check local links in selected current Markdown, with an optional staged overlay."""
import argparse,json,re,urllib.parse
from pathlib import Path

def read_path(root, overlay, rel):
    if overlay and (overlay/rel).exists():return overlay/rel
    return root/rel

def anchors(text):
    text=re.sub(r'(?ms)^```.*?^```[^\n]*','',text)
    found=set();counts={}
    for title in re.findall(r'(?m)^#{1,6}\s+(.+?)\s*#*$',text):
        title=re.sub(r'\[([^]]+)\]\([^)]*\)',r'\1',title)
        base=re.sub(r'[^\w\s-]','',title.lower()).replace(' ','-')
        count=counts.get(base,0);counts[base]=count+1
        found.add(base+('-'+str(count) if count else ''))
    found.update(re.findall(r'(?:id|name)=["\']([^"\']+)["\']',text))
    return found

def check(root,overlay,paths):
    checked=[];bad=[]
    for rel in paths:
        if not rel.endswith('.md'):continue
        src=read_path(root,overlay,Path(rel));text=src.read_text()
        text=re.sub(r'(?ms)^```.*?^```[^\n]*','',text)
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',text):
            target=target.strip().split(' "',1)[0].strip('<>')
            if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target):continue
            path,_,fragment=target.partition('#');path=urllib.parse.unquote(path)
            resolved=(root/rel).parent/path if path else root/rel
            try:destrel=resolved.resolve().relative_to(root.resolve())
            except ValueError:
                bad.append({'from':rel,'target':target,'reason':'outside repository'});continue
            dest=read_path(root,overlay,destrel)
            reason=None
            if not dest.exists():reason='missing path'
            elif fragment and dest.is_file() and dest.suffix=='.md' and urllib.parse.unquote(fragment) not in anchors(dest.read_text()):reason='missing Markdown anchor'
            item={'from':rel,'target':target}
            (bad if reason else checked).append(dict(item,reason=reason) if reason else item)
    return {'checked':len(checked),'failures':bad,'passed':not bad}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--overlay',type=Path);p.add_argument('--paths',type=Path,required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    result=check(a.root,a.overlay,json.loads(a.paths.read_text()));a.report.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checked':result['checked'],'failures':len(result['failures'])}));raise SystemExit(not result['passed'])

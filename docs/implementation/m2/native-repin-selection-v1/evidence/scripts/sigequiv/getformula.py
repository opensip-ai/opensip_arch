import json,urllib.request,sys
T='/opt/homebrew/Library/Taps/sb/homebrew-pins/Formula'
p,c=sys.argv[1],sys.argv[2]
full=json.load(urllib.request.urlopen(f'https://api.github.com/repos/Homebrew/homebrew-core/commits/{c}'))['sha']
s=urllib.request.urlopen(f'https://raw.githubusercontent.com/Homebrew/homebrew-core/{full}/Formula/{p}').read().decode()
if 'root_url' not in s: s=s.replace('  bottle do\n','  bottle do\n    root_url "https://ghcr.io/v2/homebrew/core"\n',1)
for d in ['xz','zstd','openssl@3']: s=s.replace(f'depends_on "{d}"',f'depends_on "sb/pins/{d}"')
open(f"{T}/{p.split('/')[1]}",'w').write(s)
import re; print(re.search(r'bottle do\n(.*?)\n  end',s,re.S).group(1).splitlines()[:3])

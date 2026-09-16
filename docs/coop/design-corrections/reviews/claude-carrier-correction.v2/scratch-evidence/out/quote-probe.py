# quoting probe v2
import re
print('single ok')
print('newline-escape:', len('a\nb'))
print('regex:', re.fullmatch('[0-9a-f]{4}', 'abcd') is not None)

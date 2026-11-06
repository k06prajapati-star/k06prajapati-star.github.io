# Swap the embedded vault data in the page source for a fresh vault_site.json (from vault_layout.py).
import re, sys, os
src = os.path.join(os.path.dirname(__file__), '..', 'src', 'index.src.html')
s = open(src).read(); data = open(sys.argv[1]).read().strip()
s2, n = re.subn(r"  var VAULT = \{.*?\};\n", lambda m: "  var VAULT = " + data + ";\n", s, count=1, flags=re.S)
assert n == 1, 'VAULT block not found'
open(src, 'w').write(s2); print('injected', len(data), 'bytes')

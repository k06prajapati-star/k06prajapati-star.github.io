# Reads the vault, writes ONLY structure: counts, dates, links, agent wiring, SHA-256 hashes. No titles, no text.
import os, re, json, hashlib, time
ROOT = os.path.expanduser('~/mnt/KathanLTD')
SKIP = {'.obsidian', 'Claude Outputs', '.claude', '.git', '.trash'}
G0 = {'the business', 'Modelling', 'PM -mentorship', 'sectors'}
G1 = {'the stock', 'markets', 'idea generation', 'ideas'}
notes, agentbriefs = [], 0
for dp, dn, fn in os.walk(ROOT):
    rel = os.path.relpath(dp, ROOT); top = rel.split(os.sep)[0]
    dn[:] = [d for d in dn if d not in SKIP]
    if top in SKIP: continue
    for f in fn:
        if not f.endswith('.md'): continue
        p = os.path.join(dp, f); r = os.path.relpath(p, ROOT)
        if r.startswith(os.path.join('markets', 'daily')): agentbriefs += 1; continue
        notes.append(r)
notes.sort()
base = {}
for i, r in enumerate(notes): base.setdefault(os.path.splitext(os.path.basename(r))[0].lower(), i)
mt = [os.path.getmtime(os.path.join(ROOT, r)) for r in notes]
t0 = min(mt); WK = 7 * 86400
link = re.compile(r'\[\[([^\]|#]+)')
edges, hashes, nodes = set(), [], []
for i, r in enumerate(notes):
    b = open(os.path.join(ROOT, r), 'rb').read(); hashes.append(hashlib.sha256(b).hexdigest())
    top = r.split(os.sep)[0] if os.sep in r else ''
    g = 0 if top in G0 else 1 if top in G1 else 2
    nodes.append([g, int((mt[i] - t0) // WK)])
    for m in link.findall(b.decode('utf-8', 'ignore')):
        j = base.get(os.path.basename(m.strip()).lower())
        if j is not None and j != i: edges.add((min(i, j), max(i, j)))
agents = []
ad = os.path.join(ROOT, '.claude', 'agents')
for f in sorted(os.listdir(ad)):
    if not f.endswith('.md'): continue
    t = open(os.path.join(ad, f), encoding='utf-8', errors='ignore').read()
    refs = set(m.strip() for m in link.findall(t)) | set(os.path.splitext(os.path.basename(m))[0] for m in re.findall(r'`([^`]+\.md)`', t))
    reads = sorted(set(base[x.lower()] for x in refs if x.lower() in base))
    agents.append([os.path.splitext(f)[0], reads])
skills = len([d for d in os.listdir(os.path.join(ROOT, '.claude', 'skills')) if os.path.isdir(os.path.join(ROOT, '.claude', 'skills', d))])
root = hashlib.sha256(''.join(hashes).encode()).hexdigest()
now = time.time()
out = {'synced': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime(now)), 'first': time.strftime('%Y-%m-%d', time.gmtime(t0)),
       'notes': len(notes), 'links': len(edges), 'agentBriefs': agentbriefs, 'skills': skills,
       'edited7d': sum(1 for m in mt if now - m < 7 * 86400), 'edited30d': sum(1 for m in mt if now - m < 30 * 86400),
       'weeks': int((now - t0) // WK) + 1, 'n': nodes, 'e': sorted(edges), 'agents': agents, 'root': root, 'h': hashes}
open(os.path.join(ROOT, 'Claude Outputs', 'fellowship-site', 'vault_live.json'), 'w').write(json.dumps(out, separators=(',', ':')))
print(json.dumps({k: out[k] for k in ['synced','first','notes','links','agentBriefs','skills','edited7d','edited30d','weeks','root']}))
print('agents', [(a[0], len(a[1])) for a in agents])

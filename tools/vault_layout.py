# Turns vault_live.json (structure only, from sync_vault.py) into the compact data the page embeds.
import json, sys, networkx as nx, numpy as np
src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src)); N = len(d['n'])
G = nx.Graph(); G.add_nodes_from(range(N)); G.add_edges_from(d['e'])
for i, n in enumerate(d['n']): G.add_edge(i, 'g%d' % n[0])
for g in range(3): G.add_edge('g%d' % g, 'root')
pos = nx.kamada_kawai_layout(G)
P = np.array([pos[i] for i in range(N)]); P = P - P.mean(0); P = (P / np.abs(P).max() + 1) / 2
wk = [0] * d['weeks']
for n in d['n']: wk[min(n[1], d['weeks'] - 1)] += 1
out = {k: d[k] for k in ['synced', 'first', 'notes', 'links', 'agentBriefs', 'skills', 'edited7d', 'edited30d', 'weeks', 'root', 'h', 'agents']}
out['n'] = [[int(P[i, 0] * 1000), int(P[i, 1] * 1000), n[1], n[0]] for i, n in enumerate(d['n'])]
out['e'] = d['e']; out['wk'] = wk
json.dump(out, open(dst, 'w'), separators=(',', ':'))
print(N, len(d['e']), wk)

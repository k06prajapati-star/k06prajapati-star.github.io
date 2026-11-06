# How this site is built and synced

- `src/index.src.html` is the source (a page fragment). `tools/build.py index.html` wraps it into the published `index.html`.
- The vault section is real structure from Kathan's Obsidian vault: counts, dates, links, agent wiring and SHA-256 hashes. **Never titles or text.**

## Sync the vault (on demand)
1. On Kathan's computer (vault mounted at `~/mnt/KathanLTD`): `python3 tools/sync_vault.py` writes `Claude Outputs/fellowship-site/vault_live.json`.
2. `python3 tools/vault_layout.py vault_live.json vault_site.json` lays out the graph.
3. `python3 tools/inject.py vault_site.json`, then `python3 tools/build.py index.html`, commit, push.

## Verify a note
Hash the note file with SHA-256. The hash appears in the published list; the root is SHA-256 of all note hashes concatenated in path order. Git history dates each sync.

"""
Run from your repo root:
  python extract_beeve_umap.py

Reads  project_assets/beeve/viz_data.json
Writes project_assets/beeve/umap_data.js   (works locally AND on GitHub Pages)
"""

import json, os

SRC     = 'project_assets/beeve/viz_data.json'
DST     = 'project_assets/beeve/umap_data.js'
MAX_PTS = 6000

print(f'Reading {SRC} ...')
with open(SRC, 'r') as f:
    data = json.load(f)

frames = data['frames']
tokens = frames['token']
umap   = frames['x_umap']
N      = len(tokens)
print(f'Total frames: {N}')

step = max(1, N // MAX_PTS)
idxs = list(range(0, N, step))[:MAX_PTS]

xs = [umap[i*3]   for i in idxs]
ys = [umap[i*3+1] for i in idxs]
zs = [umap[i*3+2] for i in idxs]

mn  = [min(xs), min(ys), min(zs)]
mx  = [max(xs), max(ys), max(zs)]
rng = max(mx[j] - mn[j] for j in range(3)) or 1.0
scl = 3.0 / rng
mid = [(mn[j] + mx[j]) / 2 for j in range(3)]

out = {
    'x':   [round((v - mid[0]) * scl, 4) for v in xs],
    'y':   [round((v - mid[1]) * scl, 4) for v in ys],
    'z':   [round((v - mid[2]) * scl, 4) for v in zs],
    'tok': [tokens[i] for i in idxs],
    'active_tokens': data['meta']['active_tokens']
}

js = 'window.BEEVE_UMAP = ' + json.dumps(out, separators=(',', ':')) + ';'

with open(DST, 'w') as f:
    f.write(js)

size_kb = os.path.getsize(DST) / 1024
print(f'Written {DST}  ({len(idxs)} points, {size_kb:.0f} KB)')
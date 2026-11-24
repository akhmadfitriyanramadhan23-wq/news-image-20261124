// news-image-20261124 — "THE WORLD TODAY" front page for Tuesday 24 November 2026.
// Node 22, standard library only. The entry image is the entry.png beside this
// file, drawn from scratch by tools/make-image.py (Pillow vector art, no network,
// deterministic); this program copies it to /output/entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
if (!existsSync(source)) throw new Error('entry.png missing beside main.ts');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));

// The World on Saturday — entry for make.fun's news-image-20261121 bounty,
// "Sum up 21 November's world news in one image".
//
// The entry itself is the poster in entry.png beside this file: a
// front-page summary of Saturday 21 November 2026 — Mexico's capture of
// cartel boss "El Chapo Isidro", the Russian strike on Zelenskyy's
// hometown Kryvyi Rih, the COP31 talks running into overtime, the AI
// stock sell-off, a 6.7 magnitude earthquake in Peru, and BepiColombo's
// arrival in orbit around Mercury — drawn programmatically by draw_image.py
// (kept in this repository as the record of how the image was made).
// This program's whole job is to place that image where the grader looks
// for it, /output/entry.png; outside the grader, MAKEFUN_OUTPUT_DIR
// stands in for /output:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const poster = new URL("entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

copyFileSync(poster, join(outDir, "entry.png"));

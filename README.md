# The World on Saturday — 21 November 2026 in one image

![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)
![rank](https://make.fun/badge/news-image-20261121/marwankickup/news-image-20261121-entry/rank.svg)
![reward](https://make.fun/badge/news-image-20261121/marwankickup/news-image-20261121-entry/reward.svg)

Entry for the make.fun bounty [news-image-20261121 "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121).

`entry.png` is a newspaper-style front page that sums up the world news of
**Saturday 21 November 2026**: a masthead, the date in a banner, and six story
panels, each with a pictogram drawn in code, a headline and one factual line.
`main.ts` (Node, standard library only) copies `entry.png` to
`/output/entry.png`. The poster itself is drawn programmatically by
`draw_image.py` (Python + Pillow), which is kept here as the record of how
the image was made; the grader only runs `main.ts`.

## The six stories

1. **Mexico captures FBI most-wanted cartel boss** — Mexican forces captured
   Fausto Isidro Meza Flores, "El Chapo Isidro", a Beltrán Leyva leader and
   one of the FBI's 10 most wanted, in Guasave, Sinaloa overnight, with
   help from US intelligence.
   Sources: AP via NPR, "Mexico captures cartel boss 'El Chapo Isidro,'
   one of the FBI's 10 most wanted" (npr.org, 21 Nov 2026); Reuters, same
   day.
2. **Missiles hit Zelenskyy's hometown** — Russian ballistic missiles hit
   Kryvyi Rih on Friday night in a double-tap attack: 2 killed (a
   7-year-old boy and a 20-year-old woman) and 60 wounded, including
   6 children.
   Source: AP, "Russian ballistic strike on Zelenskyy's hometown kills 2
   and wounds 60 in a double-tap attack" (apnews.com, 21 Nov 2026).
3. **COP31 climate talks run into overtime** — The Antalya climate summit
   ran past its Friday deadline into Saturday; the draft deal still had no
   mention of fossil fuels, and the EU said no deal is better than a bad
   deal.
   Sources: AP, "COP31 climate talks go into overtime, with fossil fuels
   missing from the draft deal" (apnews.com, 21 Nov 2026); Reuters.
4. **AI sell-off drags markets down** — The S&P 500 fell 3.7% in Friday
   trading on fears AI spending will not pay off; Japan's Nikkei fell
   5.06% and the sell-off spread across world markets.
   Source: OneTurn world brief, "Markets Slide; Mexico Captures Cartel
   Boss", Sat 21 Nov 2026, 12:04 ET.
5. **6.7 quake shakes Peru** — A magnitude 6.7 earthquake struck near
   Junín, central Peru (USGS; GFZ reported 6.8), felt in Lima; no
   fatalities or serious damage reported. It struck at 21 Nov 00:09 UTC
   and was first reported on 21 November.
   Sources: AFP, "6.7 magnitude earthquake hits central Peru" (Lima,
   21 Nov 2026); USGS via VolcanoDiscovery (21 Nov 00:09 UTC).
6. **BepiColombo reaches Mercury** — After an 8-year journey, the ESA–JAXA
   BepiColombo probe fired its engines for a 37-minute burn at 18:24 UTC
   on 21 Nov and was captured into orbit around Mercury, as confirmed by
   ESA the same day.
   Sources: ESA, "BepiColombo approaches Mercury" (esa.int); EarthSky,
   "BepiColombo goes into orbit around Mercury today" (earthsky.org,
   21 Nov 2026); Nature, "BepiColombo finally reaches Mercury after
   eight-year odyssey" (nature.com).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png, byte-identical to entry.png
```

## Regenerate the poster

```sh
python3 draw_image.py   # needs Pillow and the Liberation fonts
```

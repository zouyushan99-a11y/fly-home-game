# Urban Wings — Glass Building District / UW-GLASS-4

Baseline: `3bd43a3` (learning release). Scope: day-time Glass Building District.

## Layout and route identities

The old B outer branch and C inner branch almost overlapped in the middle. B's internal paths now form a more compact urban avenue; C's paths occupy the eastern green side of the existing flight envelope. A's outermost path and C's outermost path, common entrances, reconnection coordinates, rest coordinates, and all night-city paths remain unchanged. No route menu, teleport, automatic navigation or resource rule was added.

Near architecture increases from **21 to 31 buildings**: four old B inner blocks conflicted with the revised layout and were removed; fourteen fixed buildings were added, and three existing towers enlarged. Across the day district, buildings at least 60 world units high increase from **67 to 79**. The ecological side intentionally loses dense low-rise background blocks rather than retaining a uniformly urban scene. New candidates are checked against all nine paths, building footprints, roads and designated resting areas.

- **A:** tall unmarked curtain walls, denser street corners and less steering margin.
- **B:** wider, more forgiving spaces and clearly marked near facades. Boundary buildings have fixed treatments on their different sides, so the side facing A can be unmarked while the side facing B has white dots. Nothing changes material according to the selected route.
- **C:** continuous planted land, low trees/shrubs/reeds, three water features and the existing designated rest. The park continues to the reconnection area; nearby residential groups are replaced by planting. The shared city's distant skyline remains visible. Distance haze on the next district is identical for all three routes and fades continuously during approach.

Branch lengths (world units, from split to branch reconnection): A **193–209**, B **203–235**, C **263–294**. Route costs and once-only recovery rules are unchanged.

## Quantitative visual checks

`glass-visual-test.cjs` renders a segmentation pass using the same camera, building geometry, depth order and clipping. It counts visible glass-facade pixels whose building centre is within **80 world units** of the bird. Sky, ground, non-glass buildings and farther background are not the denominator. Three points (progress 27, 31, 36) on each of three internal paths give nine views per environment. The test requires at least 90% of the intended treatment in every A/B sample. This is a sampled measure of main facades, not a guarantee for every possible camera heading.

For C, a separate world-space audit samples its three internal paths every two world units through the separated section (z 140–260): **98.4–100%** of samples have no glass footprint within 15 units laterally. This measures the local corridor, **not ecological pixels as a percentage of the entire screenshot**. Before/after and three-size screenshots accompany the measurement; neighbouring city buildings can still appear in the distance.

Day-city facade strip drawing uses direct destination rectangles rather than repeated per-strip Canvas state transforms; strip spacing and texture resolution are unchanged. Vertical source cropping avoids work outside the viewport. The day district uses bounded caches of 192 facade textures and 96 composites instead of 96/32; caches clear at area transitions. Their maximum pixel storage is about 144 MiB on desktop and 36 MiB below 900px width, excluding other assets/browser overhead. Other districts retain their original 96/32 limits. `glass-render-equivalence.cjs` compares output against the original implementation at A/B/C views: mean channel difference is below 0.0001/255; the maximum is 4/255, with only four pixels in the B sample differing by more than 2/255 (fractional crop-edge sampling).

## Glare and collision feedback

Unmarked day-city glass retains cached sky/cloud and neighbouring-silhouette reflections. A surface sheen increases gently during approach (maximum 7.5% opacity); it is confined to the glass polygon. The screen-edge cue eases toward a maximum **5.5% opacity** and occupies only the outer 14% on each side. There is no full-screen flash or random damage. Reduced-effects mode disables both additions. Pausing freezes the cue; restart clears it.

Day-city impact shake/border is softer. Existing swept collision, Health deduction, protection time, recovery and educational explanation remain. Browser tests drive a head-on collision with 0.25-second input steps: Health drops from 100 to 75 once, the bird remains outside the wall, and another contact during protection does not deduct Health again. After closing the card and holding forward, all three screen-size tests also exercise position recovery and verify renewed forward progress. This follows the existing severe-impact rule; ordinary impact still costs 15.

Glare is a restrained game visualisation, not a measurement of bird vision.

## Tests and evidence

- `glass-layout-test.cjs`: Journey code byte-identical to baseline; night layout, entrances and rests unchanged; 3,360 boundary cross-sections identical; all nine revised centre paths clear. With an additional ±5-unit lateral offset, 62/360 A segment-offset samples intersect a building, compared with 9/360 B and 0/360 C. These are clearance probes, **not human collision probabilities**.
- `glass-browser-test.cjs`: 1280×720, 390×844 and 844×390; actual keyboard/CDP touch input; released input retains heading; glare increases smoothly, leaves central pixels unchanged, freezes with pause, and disables with reduced effects; collision feedback and protection; no browser errors.
- `glass-flight-test.cjs`: nine complete browser test-pilot journeys through all five areas, with sampled rendering and actual observation-triggered cards. All nine finish at Health 100, with five visited areas and no position recovery. Final Energy: A 45; B 45–55; C 25–45. C’s revised paths reach different existing rest opportunities; reward/cost values are unchanged. Each reconnects, reaches the destination and checks the existing educational sequence.
- `glass-scenes.cjs`: same viewport and corresponding route-progress points before/after, using actual replay positions/headings. Since internal layouts changed, the old and new routes do not necessarily have identical world positions. Camera smoothing is reset between isolated captures.
- `glass-performance.cjs`: serial baseline/current rendering at identical world position, heading and 1000×650 viewport; 8 warmups and 24 timed frames per scene, each followed by a tiny readback to flush deferred Canvas work. Results in `evidence/glass/performance.json`; software-renderer timings are not physical-phone FPS.

## Measured renderer cost

Same world camera and software-rendering conditions; values are milliseconds per forced-complete draw, not physical-device FPS.

| Route | Before median / p95 | After median / p95 |
|---|---:|---:|
| A | 298.2 / 326.1 | 50.4 / 53.2 |
| B | 46.4 / 65.9 | 38.0 / 48.7 |
| C | 292.6 / 306.9 | 21.3 / 25.0 |

The timing table measures warm-cache drawing, not initial asset loading or an end-to-end frame-rate guarantee.

## Limits

No physical mobile device or student comfort/playability trial. Full journeys use a test pilot; DOM keyboard/touch checks verify the controls separately. Visual percentages are sampled with the definitions above, not all possible player views. C's requested “80–90% ecological environment” is supported by local corridor composition and screenshots; an entire-frame ecological pixel percentage has **not** been established. The game keeps a stylised city and distant urban skyline.

Deployment success is checked independently; direct public Pages playtesting is blocked by this environment's network policy.

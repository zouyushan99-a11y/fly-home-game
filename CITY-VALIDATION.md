# Shared connected city — 2026-11-08

Implemented on the existing game, retaining six stages, first-person controls, health/energy, educational cards, bilingual UI, touch controls and endings. The supplied reference image informs the three facade categories and spatial hierarchy; it is not copied into the game or used to replace its art direction.

## World and gameplay

Both day and night city districts now contain all three routes simultaneously in fixed world coordinates. Four natural entrance buildings identify the common branching area. Selection rebases the lateral coordinate to preserve the exact world position; it does not replace geometry. Smooth route centerlines reconverge before the existing stage boundary. Camera heading follows the curve smoothly; player left/right control remains additive. Reduced-effects disables camera yaw.

| Route | Day centerline length | Night length | Challenge opening | Appearance |
|---|---:|---:|---:|---|
| A | 341.5 | 341.7 | 10.4 | Continuous unmarked reflective curtain wall |
| B | 378.8 | 378.2 | 16 | Reflective curtain wall with repeated circular white dots |
| C | 421.2 | 419.0 | 26 | Ordinary residential walls, separate windows, trees, designated rest |

Lengths/openings use game world units. Not all parcels can contain two obstacle buildings: road/bridge reservations and the neighboring routes take precedence. The layout diagram shows actual placed solids. A has the tighter alternating openings; B retains steering challenges. Damage rules are unchanged, including for marked buildings. No probabilistic or invisible damage is introduced.

25/24 near buildings and 163/163 retained skyline buildings serve the day/night shared districts. Geometry is not triplicated per route. All reachable retained skyline buildings participate in swept collision checks. Nearby solids have depth and visible side faces; distant detail uses existing cached materials. The facade sampler now uses inverse-depth screen-space columns to avoid the coarse-strip stretching exposed by oblique residential facades.

## Full-journey balance

Identical test driver strategy, 60 Hz simulation; all six knowledge cards are opened and continued. Card reading time is excluded. Driver is collision-aware test automation, not a claim that all first-time human players will avoid every obstacle.

| All-stage route choice | Before time / remaining Energy | After time / remaining Energy | Final Health |
|---|---|---|---:|
| A | 144.92 s / 15.75 | 148.28 s / 13.93 | 100 |
| B | 144.92 s / 42.75 | 155.33 s / 37.12 | 100 |
| C | 152.22 s / 45.80 | 165.12 s / 55.84 | 100 |

Before is commit `0f6b627`. After A/B/C day-city durations are 27.67 / 31.15 / 33.97 seconds; night 27.57 / 31.12 / 33.97 seconds. Continuous Energy drain remains 0.54/s; C still pays 7 per selected detour. B day rest +7, C day and night rest +17, once each, only inside the actual designated zone. C therefore has one additional suitable night-city rest compared with baseline, explaining its larger final reserve despite the extra flight cost. Other chapter rests and arrival +8 remain unchanged. These values are game design, not scientific measurements.

## Verification and limitations

See machine-readable evidence in `evidence/city/`: model.json, invariants.json, journey-stats.json, layout.json, camera.json and browser.json. Replays are actual steering-input sequences through the simulation, not position teleports. Browser screenshots labelled `flight-*` follow those continuous trajectories. Before/after screenshots are controlled same-pose comparisons, not a claim of identical geometry.

Checks cover shared geometry identity, exactly-once entry, world-position continuity, spatial rest hit/miss and no repeated recovery, all three complete routes, educational content, pause/help/bilingual controls, keyboard/touch input, endings/restart, three viewports, and expanded ±36° near-plane/ground projection stress.

No physical phone used: Chromium emulates 1280×720 desktop, 390×844 portrait and 844×390 landscape. The renderer remains the existing Canvas pseudo-3D system; reflections approximate sky and nearby silhouettes rather than ray tracing. Automatic route guidance follows the chosen centerline, with manual steering needed around obstacles. Mobile human difficulty and device GPU performance still need physical-device playtesting.

The GitHub Pages destination returns proxy HTTP 403 from this environment. Local browser verification cannot be represented as online verification. Publication status is recorded separately after push.

## Final local browser results

All 9 full journeys passed (3 routes × 3 viewports), with Health 100 and all six knowledge topics continued. No page errors. Keyboard/touch, pause/help, bilingual toggles, success/failure/skip/restart passed.

Mean renderer CPU milliseconds for A / B / C, before → after:

- desktop: 19.23 / 5.08 / 4.57 → 8.24 / 7.06 / 5.75 ms.
- portrait: 9.85 / 4.01 / 3.57 → 5.18 / 4.24 / 3.99 ms.
- landscape: 11.51 / 4.46 / 4.51 → 8.05 / 6.43 / 5.86 ms.

B/C cost slightly more in the denser shared world; A improved with the new facade sampler. These are serial, same-viewport, fixed-pose CPU draw measurements, not end-user FPS or proof of phone GPU performance. Full P95 figures are in the browser report.

Final additional checks: all nine route entries passed actual keyboard/CDP touch events; facade and roof clipping at ±36° passed on all three viewport sizes, with no invalid near-plane projections, no green roof pixels above the horizon, restored Canvas state, and ground projection round-trip error below 1e-8. See entry.json and camera.json.

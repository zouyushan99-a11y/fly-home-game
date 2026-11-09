# Urban Wings — player heading and collision correction

## Root causes and changes

1. Previously, city heading was recalculated directly from current steering input. Release therefore reset the motion vector. Outside selected city routes, path-center displacement and environmental drift still moved the bird. Heading is now persistent in **all six stages**. Held A/D or arrow/touch buttons change heading; releasing immediately stops angular input and preserves the new heading. Path data describes geography only. Wind/light cues never rotate or translate the bird. Route confirmation only records crossing a real entrance; no nearest-route fallback was added.
2. The old collision code detected a swept intersection but then deducted Health and nudged/clamped lateral position. It did not first stop at the contact point, and damage grace skipped collision handling entirely. The new resolver computes the earliest swept time against rotated, altitude-specific building parts expanded by a 1.1-unit body radius, stops just outside the contact, then applies existing damage feedback. Geometry blocks motion even during damage grace and previously recorded contacts. No automatic lateral shove, steering correction or obstacle avoidance occurs.
3. Input is integrated in steps no larger than 1/120 second, including a low-frame-rate supplied step up to 0.25 seconds. The renderer uses the actual heading in both views. Chase-camera building checks include adjacent stages and the camera's movement between frames; only camera distance changes. Nearby background buildings render as complete solids rather than disappearing behind a center-depth cutoff.
4. The view button is highlighted, labelled by the actual first/third state (視角 1 / 視角 3), with full bilingual descriptions. The permanent control hint includes V. Pause/help/knowledge-card view buttons remain available. Reduced effects disables cosmetic sway/banking, not the actual heading needed to see the direction of travel.

## Controls

- Hold A/D, Left/Right, or the on-screen arrows to turn; release to maintain heading.
- V or the highlighted view button switches first/third person without changing position, heading, speed, Health, Energy or progress.
- The existing forward-flight level constrains heading to ±90° from the journey's forward axis. Sideways flight is possible to leave a wall; U-turn/backward traversal is not implemented. At a collision, turn clear of the wall; the game will not choose a way around it.
- Under very restricted camera clearance the chase distance shortens, and the bird may temporarily fade out when too close to the near plane. This never changes the player's motion.

## Completed evidence

- `model.json`: neutral heading is preserved in every gameplay region; swept rotated-wall blocking at 120/30/10/4 Hz, speed stress, freeze and cooldown checks.
- `corners.json`: frontal contact followed by manual escape around rotated corners at 60 and 10 Hz, without penetration or repeated contact damage.
- `browser.json`: desktop 1280×720, portrait 390×844, landscape 844×390, both views; actual keyboard/touch steering, release, view button/V, real entry-building collision, visible chase bird and header bounds.
- `entries.json`: all three natural entrances reached via real browser keyboard press/release events using the new heading model.
- `journeys.json`: nine complete model-driven routes/path combinations using the new control law. This test pilot is external test code, not in-game autopilot.
- `geometry.json`: entry-road reservations and near-building footprints checked; no overlap found, so no speculative road-layout changes were made.
- `camera.json`: facade/roof near-plane stress to ±89°, Canvas state restoration and terrain inverse-projection consistency.
- `replay-browser.json` and `view-check.json`: complete browser replays and camera/CPU timings, added on completion.

Tests use local Chromium. Mobile sizes are emulation, not physical phones. Automated replay success does not establish first-time human difficulty. Long real-time browser stalls still use the existing capped accumulator, preferring stable simulation over unlimited catch-up. Online deployment must be reported separately; previous access to GitHub Pages was denied by the environment proxy.

## Final verification — 2026-11-10

18 full browser replays passed (A/B/C × two views × three viewport sizes), Health 100, no page errors. Nine model journeys cover all internal path combinations under the new steering law. 24 early/late entrance cases across all four choice stages preserve exact world position and heading; the late C-route coordinate rebase was corrected in non-city stages too.

Touch knowledge cards/help, language switching, pause, view changes, success/failure/skip/restart passed. Reduced effects retains real heading while removing cosmetic motion. Camera corner sweeps found no camera penetration and left player physics unchanged.

Serial camera draw timings (CPU milliseconds, not handset FPS):
- desktop, first: mean 303.30, P95 360.40.
- desktop, third: mean 327.57, P95 355.90.
- portrait, first: mean 112.75, P95 135.10.
- portrait, third: mean 117.26, P95 136.30.
- landscape, first: mean 120.58, P95 140.10.
- landscape, third: mean 145.21, P95 169.20.

Online check on 2026-11-10: proxy HTTP 403. No physical-phone or online browser verification claimed.

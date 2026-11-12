# Urban Wings — UW-HABITAT-6

Recoverable baseline: commit `46725bc`, local branch `checkpoint/pre-targeted-improvements-46725bc`. The working tree was clean before editing. Existing engine, player camera, steering, forward motion, boundaries, glass reflection assets, learning UI, ending and recovery are retained.

## Inspection and changes

The four targeted short glass blocks are `0-inner-A-2--1`, `0-inner-A-2-1`, `0-inner-A-3--1`, `0-inner-A-3-1`, originally at x −37.935/−21.140/−36.396/−18.396 and z 181/181/196/196. Their original dimensions were 7×8×44. They are now 10×12×100/108/116/124, offset sideways by 0.6 and staggered longitudinally by 4 units. Exact before/after geometry is in `evidence/targeted/buildings.json`. Collision and rendering consume the same building records. Village houses are not converted. The near-tower paired gaps are approximately 8 and 9.2 units, versus the bird collision diameter of 2.2.

Glass teaching now reserves `glass_collision_education` immediately when queued, using per-playthrough state shared by approach and impact. This also suppresses the old repeated glass feedback banner after an already-read card. Restart resets it; recovery does not. Approach wording remains general, with no injury claim. Only a collision-first card carries a Health-loss consequence note. Marked-glass education remains a distinct topic.

Damage now identifies contact episodes rather than granting permanent immunity after one collision with a building. Continuous contact cannot deduct every frame; separating and colliding again can. Existing swept collision, stop-before-wall and recovery remain. No automatic route following or evasive steering was added.

The shared city retains its three real entrances and nine internal routes. Route signs and the steering instruction now render only in the two city districts, not in the non-fork ecological/village sections. City entry geometry is unchanged and provides roughly 4–6 seconds from the normal early approach. Sky/cloud/environment reflection textures and visible glass seams remain; the proximity/view-dependent glare added in UW-GLASS-5 is retained. This is the existing Canvas reflection approximation, not a new real-time reflection renderer.

The ecological stream uses adjacent world-anchored polygon segments with shared varying-width bank vertices, muted mud banks and shallow water, replacing yellowish parallel borders. The village contains five separate widened water basins with raised earth banks and low houses. Standing white egrets/grey herons have bodies, necks, legs and bills; additional birds fly beside the route with wing animation. Models remain stylised.

An ecological feeding bank contains six birds and three pedestrians on a visible path. After one second of readable observation, birds begin leaving; only after another 1.4 seconds of visible reaction is the disturbance card eligible. Behind-camera, obstructed, or too-small scenes do not unlock it. Simulation time freezes with paused cards. The former distance-only wildlife triggers no longer schedule this lesson. If the encounter is bypassed, its card is suppressed rather than appearing without evidence.

Mai Po retains broad tidal water, irregular mud islands, mangroves/reeds and three managed ponds. Ponds are moved closer to the playable view, separated from island vegetation, with water below bank tops, and additional recognisable flying waterbirds. Final-stage duration and ending boundary remain unchanged; this task does not shorten the destination approach.

## Final settings

- Normal forward speed: 12.15 world units/s at full throttle; wetland target 10.3275. Unchanged.
- Collision radius: 1.1 world units; normal/severe damage: 15/25 Health. Unchanged.
- Contact protection: 1.25 seconds (previously 1 second).
- Energy: −5 once per 162 actual travelled world units (18×9), accumulated from movement, not frames. Previously −5 per 15 units of longitudinal progress.
- Removed the extra −5 route-entry detour charge: longer paths now cost more through actual distance, with no double charge.
- Existing lighting event −5; designated rest +20 once, capped at 100; arrival +10. No Health restoration at rest. Zero-Energy glide and checkpoint recovery remain.
- These are game-design numbers, not biological measurements.

## Evidence and limitations

`tools/targeted-model-test.cjs` checks shared teaching reservation, approach without injury, collision-first wording, repeat contact versus recontact, restart, pause, five time-step sizes (120/60/30/15 Hz and 0.25-second updates), passive impact, all four collision volumes and once-only rest. Frame-step tests produce identical distance and Energy deductions.

`tools/targeted-browser-test.cjs` checks the visible disturbance-before-card sequence, freeze while reading, behind-camera suppression, no misleading route signs, and captures stream/pond/wetland scenes at desktop 1280×720, portrait 390×844 and landscape 844×390. `tools/targeted-entry-test.cjs` uses DOM keyboard and emulated touch input to steer into the real entrances. Full journey tests use an instrumented pilot; they are not human playability studies.

See `evidence/targeted/` JSON reports and `habitat.html` for actual results and gameplay-camera images. Performance comparisons use serial Chromium software rendering, fixed viewport and camera, warm caches and readback-flushed draws; they are not real-phone FPS. No physical phone was used. Online gameplay cannot be tested from this environment because the public Pages host is blocked by network policy; GitHub deployment is checked separately.

## Recorded results

All nine browser journeys and the final A/B/C centre-route rerun finished at Health 100. Keyboard and touch entry tests passed all three openings at all three sizes. The no-input run after normal A entry incurred a real collision. All three scene-size tests passed.

| Route/path | Seconds | Flight cost | Actual rest | Final Energy |
|---|---:|---:|---:|---:|
| A1 | 155.8 | 55 | 0 | 50 |
| A2 | 153.8 | 50 | 0 | 55 |
| A3 | 153.1 | 50 | 0 | 55 |
| B1 | 151.7 | 50 | 0 | 55 |
| B2 | 154.4 | 50 | 10 | 65 |
| B3 | 158.5 | 55 | 0 | 50 |
| C1 | 167.3 | 55 | 10 | 60 |
| C2 | 170.6 | 60 | 20 | 65 |
| C3 | 174.6 | 60 | 0 | 45 |

The ecological routes consume 55–60 flight Energy versus 50–55 on A. This is approximately 12.9% more on average across the three tested paths, slightly below the initial 15–25% suggestion; it is retained to preserve forgiving completion. A direct clean run uses 55–60 including lighting, before arrival rewards.

| Scene | Before median / p95 (ms) | After median / p95 (ms) |
|---|---:|---:|
| A | 56.7 / 72.1 | 54.0 / 63.9 |
| B | 45.2 / 79.4 | 37.3 / 58.3 |
| C | 21.1 / 25.0 | 19.4 / 23.1 |

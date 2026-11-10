# Urban Wings — area recognition and learning clarity

Baseline: `7fea83d`. Existing project and six-stage journey retained.

## Implementation

- Five once-per-journey pre-entry previews at progress 9 / 44 / 79 / 114 / 139. Actual scene images, bilingual title/description/observation hint, immediate Continue. No simulation, Energy or interference time advances while open.
- First-time, skippable left/right practice over the coast. It teaches persistent heading, route observation, Health and Energy. Completion/skip persists locally; help explicitly offers **Restart and practise controls**. Practice changes heading but freezes journey position/resources, keeping the section safe.
- Health/Safety and Energy/Flying Strength labels plus contextual one-time explanations. Damage, recovery and Energy constants are unchanged.
- Night sky, terrain and building palettes are dark; route A retains substantially more lit windows than B/C. Existing reflections and white glass patterns remain.
- Five world-fixed fishponds with water, raised banks, ripples and reeds; ten low village houses available before choosing a route. Rural entrance/gate high-rise models replaced by low village models or individual trees; pond footprints exclude overlapping decorations. Ecological entrance structures are low public buildings rather than towers. Wetland water expanded while retaining mudflats and bird habitat.
- Educational topics unlock only after relevant objects project into view (or an actual glass collision/designated rest event). Normal cards defer during substantial steering. Removed the forced end-of-journey catch-up stack. Unread material is explicitly additional information inside a collapsed section of the existing summary.
- After the existing four-second ending animation (or its skip), two questions from different topics precede the existing summary. Ten bilingual questions cover five topics. Three shuffled options, one correct, immediate explanation, free retry, no timer, no resource penalty. Last pair excluded from the next draw. Existing ending summary retained; no replacement dashboard.
- Existing navigation renderer, educational content payload and numeric Energy configuration are byte-identical to baseline; see `evidence/clarity/preservation.json`.

## Controls

A/D or arrows; on-screen left/right. V or view button switches camera. New overlays offer bilingual controls. Continue closes the area preview immediately. Tutorial can be skipped; Learning Check advances after a correct answer to each of two questions.

## Verification and evidence

See [comparison gallery](clarity.html). Machine-readable results are in `evidence/clarity/`.

- `clarity-model-test.cjs`: five previews freeze state and trigger once; practice freezes resources; unseen/duplicate knowledge blocked; steering deferral; 1,000 randomized question draws.
- `clarity-journey-test.cjs`: nine model-piloted combinations complete, Health 100. Final Energy approximately A 9.9–11.3, B 27.9–37.6, C 16.5–53.4. Flight time 151–175 seconds excluding reading/quiz. This demonstrates feasible paths, not human ease-of-use.
- `clarity-browser-test.cjs`: desktop 1280×720, portrait 390×844 and landscape 844×390. Keyboard practice, touch-pointer handling, actual DOM buttons, replay/skip, all previews and image loading, freeze, bilingual, knowledge gating, wrong-answer retry, success/failure ending → quiz → existing summary, restart.
- `clarity-flight-test.cjs`: instrumented Chromium pilot follows A0/B1/C2 through the actual renderer; records previews and observed topics before each card. It does not replace manual playtesting.
- `clarity-live-test.cjs`: real requestAnimationFrame loop, keyboard practice, touch UI, pause, camera toggle, pre-entry continuation, returning-player persistence, offline embedded-image decoding without network requests.
- `clarity-clipping-test.cjs`: retained near-plane material regression at five headings and seven depths, matrix/alpha/filter restoration, ground projection and state resets.
- `clarity-performance.cjs`: baseline/current serial render samples under identical dimensions/scenes, after warm-up. Headless CPU Canvas timings are not physical-device FPS.

## Limits

No physical phone or classroom child-user test. Browser policy blocks direct `file://` navigation; the offline HTML was instead served as the sole document with every additional network request blocked, and all embedded WebP assets decoded. Touch validation uses browser emulation and pointer events; complete journeys use a pilot. The intended 15–30-second quiz duration is a design target, not a measured child-reading result. Environmental observation uses projected representative object points, not pixel-perfect occlusion analysis. Long content remains scrollable on small screens. Actual sky/texture source attribution remains in the existing asset documentation.

Publishing to the existing `gh-pages` branch preserves the URL. Local verification does not prove the publicly hosted version: the cloud proxy currently denies the GitHub Pages host (403); the final delivery states publication and online verification separately.

## Measured rendering cost

Headless Chromium, GPU disabled, 20 warm-up frames and 80 samples; measurements run sequentially. Values are CPU rendering milliseconds, not playable FPS.

| Viewport | Scene | Before median / p95 | After median / p95 |
| --- | --- | --- | --- |
| desktop | night | 518.7 / 589.1 | 520.2 / 594.2 |
| desktop | pond | 2.2 / 112.6 | 3.9 / 95.2 |
| portrait | night | 189.4 / 232.6 | 186.7 / 232.7 |
| portrait | pond | 1.3 / 73.3 | 1.8 / 71.0 |
| landscape | night | 218.6 / 278.0 | 226.3 / 288.1 |
| landscape | pond | 2.0 / 72.0 | 2.4 / 62.6 |

Night-scene median changes range from −1.4% to +3.5%; both versions are expensive in this software-only environment. Pond median increases by 0.4–1.7 ms with the new scenery; p95 decreases in this run. These results do not establish smoothness on a physical phone.

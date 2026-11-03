# Real-time flight navigation

Baseline: `2fa31e3ffe6532467110bceec2d74cb0351e894b`. Play `index.html`; screenshots and raw results are linked from `navigation.html`.

## Gameplay

Route cards, their click handler and menu option data have been removed. The player steers continuously with A/D, arrow keys or held touch buttons. There is no route-wait state. Knowledge encounters now use the existing brief bilingual feedback and field notebook rather than blocking cards. Explicit pause/help still freeze gameplay.

Three fixed corridors coexist in the same district. All buildings are generated before the choice and do not swap or fade when a route is entered. A is a narrower, unmarked reflective passage; B has wider clearance and repeated white exterior patterns on its glass-facing walls; C follows the greener outside corridor and bends back toward the shared passage. Ground guides and world-positioned labels indicate the actual gaps, not clickable options. Region-specific labels preserve the night, corridor and village contexts.

The Glass Building District has three forks, followed by reconnection spaces. Night and ecological districts also have three; the village has two: 11 forks across a complete six-stage journey. Fork entry is recorded from physical lateral position at an entry plane; steering remains available afterward. Cross-corridor movement can hit the real separators. Open areas between sections allow a different choice at the next fork; no camera snapping or automatic lateral repositioning is used.

The left passage has 8 world units between façades, B has 12; the unchanged swept bird radius still applies. Collision damage remains −25 ordinary / −35 severe. A deterministic lateral-offset sample at the same passage depth produced 18 collision samples for A and 4 for B, so B is safer but not collision-free. These are geometry test samples, not scientific probabilities.

C retains the existing −7 detour charge once per district, including if entered after the first decision plane. Green sections use slower progress to represent the additional travel time and have a curved guide. Designated ground rings identify B (+7) / C (+17) rests in the existing eligible districts; rewards remain once per district, not once per fork or button press. Continuous Energy use remains 0.40 per flight second; night interference and arrival values are unchanged. Scoring values are game design, not scientific measurements.

Reflective glass, exterior markers and green habitat are visible from the shared approach. Short messages about all three are triggered along the first city section even when the player stays in only one corridor. Detailed educational content remains in the notebook, and the simplified end summary remains available.

## Validation

Run a local server on port 8080, then:

```
node tools/interaction-test.cjs
node tools/navigation-live-smoke.cjs
node tools/smoke.cjs
```

`interaction-test.cjs` now runs `flight-navigation-test.cjs`. Old click-to-choose assertions were replaced because that interaction intentionally no longer exists. Historical tests that assume the old route-card API or old obstacle geometry do not describe this new navigation workflow.

- Five complete deterministic simulations passed, all with 11 recorded forks, no knowledge/route freeze, no recovery and Health 100. Mixed A→C→B and C→A→B runs confirm repeated choices. Building array identity remains constant across choices.
- Physical separator collisions retain their Health deduction. Pause freezes resources. Repeated navigation updates cannot farm rests; entering C after the entry plane still costs Energy once.
- Actual Chromium input tests cover 1280×720 desktop, 390×844 portrait, 844×390 landscape and 768×1024 touch tablet. Each also completed an accelerated mixed-route browser journey, rendered once per 60 simulation steps (about 1 Hz sampling), without script errors. These sampled runs are not real-time full-journey videos.
- A separate, unmodified `index.html` run uses real CDP touch events and the normal animation loop: the player steers into C at the first fork, then B at the next while the clock continues. No test hooks or simulation jumps are injected in this live check. See `live.json` and `live-touch-*.png`.
- Pause, help, language switching, end summary and restart are checked; restart clears branch history. The formal web and self-contained offline builds pass their existing smoke test.
- Sky and building assets are required to decode before the screenshot suite captures frames. Six-stage progression, Health/Energy, first-person rendering, materials, night lamps, vegetation and the roof near-clipping fix are retained. This task intentionally changes foreground obstacle layout to make simultaneous physical paths; it does not claim the old foreground geometry remains identical.

## Complete-route resource results

The three letters describe the choices repeated within each district (the village has two forks). All choices are achieved by steering; no menu/API selection is used.

| Pattern | Forks | Health | Final Energy | Flight seconds |
|---|---:|---:|---:|---:|
| AAA | 11 | 100 | 25.89 | 170.3 |
| BBB | 11 | 100 | 52.44 | 171.4 |
| CCC | 11 | 100 | 51.84 | 186.4 |
| ACB | 11 | 100 | 57.73 | 175.7 |
| CAB | 11 | 100 | 44.93 | 176.1 |

The longer C run consumes more flight time; workable mixed routes also finish. These are successful controlled paths, not a guarantee that arbitrary steering avoids collision or exhaustion.

## Limits and online status

Desktop/mobile/tablet results come from Chromium viewport and touch emulation, not physical phones or tablets. Performance has not been benchmarked across real hardware in this task. The live smoke check covers two consecutive forks; full journeys are accelerated, sampled runs. Canvas remains a pseudo-3D renderer with approximate transparency and perspective.

The current environment still receives proxy 403 when requesting the GitHub Pages domain. Local tests do not establish online deployment or online behavior. Git push confirmation is reported separately at delivery.

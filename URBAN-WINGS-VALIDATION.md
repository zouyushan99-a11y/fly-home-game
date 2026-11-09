# Urban Wings: views and internal passages

Work based on b30cf2c. Existing six stages, resources, educational content, ending and controls retained. Repository and publication path remain unchanged.

## Design

First person remains at the bird's original eye position. Third person places the camera up to 13 world units behind and 2.34 units above the bird. Buildings, terrain, glass reflections, lights and the bird use that same camera. The bird consists of world-space body/head/tail/wing polygons, depth sorted with the scene. Wing motion and banking stop/reduce with reduced effects. The camera shortens against swept building footprints immediately for safety and extends smoothly when clear. At extremely short camera distance the bird hides to prevent filling the screen. The view preference survives restart; follow distance resets. V and a bilingual button switch views independently of gameplay state.

Inside selected city environments, forward/side velocity now comes from actual steering heading. The previous centerline displacement is subtracted from the lateral coordinate; it cannot move the bird automatically. Centerline data is only used to describe geography, not to force its horizontal movement. Subsequent legacy non-city stages retain their original guidance. Lateral range does not suddenly snap when leaving a city off-center.

Each day/night A/B/C environment has three cleared interior paths between local depths 110 and 290, joined before/after. Buildings between paths form islands with cross-links. C uses world-anchored ground trails and the existing tree/residential setting. Only the designated rest zone restores Energy. There is no second selection menu, subroute lock, random damage, or reward for merely entering vegetation. Routes remain in a single fixed shared world. The data and day/night SVG diagrams contain all 18 paths.

Corridor clearance radii used by the planner: A 3.5, B 4.5, C 5.5 world units; outer path offsets vary continuously and have different curves rather than fixed parallel lanes. Buildings/roads and neighboring paths are checked before placing divider buildings. Relative route and branch risks are spatial, not different damage rules. The nine input replay runs use the same internal path index in both day and night, covering all 18 city paths, then complete the original remaining stages.

All resource values are game balancing parameters, not scientific measurements. Manual heading gives longer physical paths real time/energy costs; button presses do not directly deduct Energy. See model.json for complete elapsed times and reserves.

## Evidence

- `evidence/urban-wings/model.json`: nine complete model trajectories.
- `evidence/urban-wings/replays.json`: steering inputs, no position teleportation during the route.
- Browser, camera and actual keyboard/touch checks are recorded separately when completed.

The renderer remains Canvas pseudo-3D; facade reflections are approximations using existing sky assets. Automated trajectory completion proves connectivity but does not establish first-time human difficulty. Browser mobile viewports are emulation; no physical handset has been tested. Online GitHub Pages access was denied by the environment's proxy in the previous iteration; online verification must be reported separately from publishing.

## Completed tests

54 complete browser runs passed: 9 route/path combinations × 2 views × 3 viewports. Each includes both city districts, original remaining stages and all educational cards; final Health 100. Actual keyboard/CDP-touch entry checks passed on all 9 device/route combinations in third person. Neutral steering preserves world X instead of following the path; off-center range does not snap on stage changes. Paused/knowledge-card view buttons were clicked in-browser without changing progress or resources.

Camera fixture retracted from 13 to 3 world units before a rear wall; reset preserved third-person preference with distance zero. Roof/facade and terrain clipping regression passed at ±36°. Real phone not used.

Serial CPU draw timing (first / third person), same scene and dimensions, 20 warmup + 60 samples:
- desktop first: mean 6.93 ms; P95 10.10 ms.
- desktop third: mean 7.13 ms; P95 9.10 ms.
- portrait first: mean 4.69 ms; P95 6.90 ms.
- portrait third: mean 4.76 ms; P95 5.70 ms.
- landscape first: mean 5.86 ms; P95 8.30 ms.
- landscape third: mean 6.33 ms; P95 8.20 ms.

These are CPU Canvas draw timings, not physical handset FPS. Camera retraction prioritizes avoiding walls over maintaining its full follow distance; the bird hides if camera clearance becomes extremely short. Exterior paths remain open enough to permit cross-links, rather than locking the player to one of three numerical lane IDs.

The final portrait header was corrected after screenshot review: compact 1P/3P text with full bilingual accessible labeling; bounds tests ensure all buttons fit the viewport and the header does not overlap the HUD. New first/third screenshots reflect that fix.

Final cross-link test: switching from each outer path to the opposite path through the final open connection (local depth 265) passed for A/B/C in both city districts, without collision or teleportation. Success/failure endings, skip/restart and reduced-motion yaw checks also passed on all three viewport sizes.

2026-11-09: GitHub Pages still returns proxy HTTP 403; online deployment is not browser-verified.

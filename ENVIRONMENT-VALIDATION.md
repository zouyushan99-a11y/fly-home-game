# Urban Wings — environment identity and wetland update

Baseline `6597a8f` / UW-STABILITY-1. New release label: UW-ENVIRONMENT-1.

## Scope and preservation

The existing bird-following view is now the only user-facing view. No new camera was introduced. The menu button, V shortcut and view switches in help/knowledge dialogs are removed. The existing camera-follow and camera-wall avoidance code remains. Near-wall retraction can temporarily show wing tips instead of the whole bird.

`environment-preservation-test.py` verifies that Journey logic is byte-identical except its default view; collision detection, educational content, quiz logic, ending flow, route control points, entrances, all internal route polylines and designated rest coordinates are unchanged. No damage, resource, boundary or recovery rule was changed.

## Environment changes

- **Glass district:** 11 existing commercial towers raised by up to 18 world units (maximum 135); six widened by 12% and deepened by 10%. Entrances remain untouched. Widening is accepted only after conservative neighbour and route-clearance checks. Existing models, reflections and facade materials are reused.
- **Urban ground:** the cached ground map now starts with paving; green land follows the fixed C branches. Building foundations and roads meet hard surfaces. Grass patches are restricted to the ecological detour rather than spread beneath commercial towers.
- **Route A/B distinction:** A towers retain unmarked reflective glass. B-facing facets on interior B towers carry the white patterns; facets more directly facing A remain unmarked. This is a fixed world-space facade choice, not a texture change when the player selects a route. Shared entrances still show the alternatives. A small amount of the neighbouring district remains visible as background.
- **Glass dots:** corrected the texture-space aspect ratio so facade stretching does not turn all circular marks into long vertical ovals. Night markings use a muted pale colour rather than looking like self-illuminated lamps. Glass reflection remains a separate sky-dependent layer.
- **Night:** darker curtain-wall base materials, ground lighting and distant haze. The existing difference in illuminated-window density between A and B/C remains. No lighting gameplay events were added.
- **Ecological green space:** lower tree groups and retained shrubs, stream, open areas and designated rest marker. Dense commercial paving stays in the city rather than becoming the green corridor's terrain.
- **Village/fishponds:** retained the five fixed water-filled ponds, embankments and low houses; reduced surrounding trees and removed the excessive trunk-plus-canopy stacking. Ponds remain actual world-space surfaces.
- **Mai Po:** broad tidal water replaces the uniform bank-lined channel. Seven irregular mudflat/vegetation islands, three managed pond cells with banks, shallow-water margins, wet-mud patches, tidal channels, 140 mangrove/reed plants, 28 standing waterbirds, a low background hide and short boardwalk. The existing destination/family-reunion flow is unchanged.

## Tree scale correction

Previously, converted obstacle trees had 36–40-unit trunks with extra 15–20-unit crowns placed above them. The total silhouette could exceed the fixed flight altitude substantially. Converted trees now use a single total-height model: ecological groups approximately 11–14 units, village groups 7–10 units. Ordinary decorative trees are capped by their fixed world region: city 12, ecological 16, village 11, wetland 6. Wetland planting uses mangroves and reeds rather than generic tall trees.

The model height is also what the existing collision code sees. These lowered trees therefore no longer leave invisible high-altitude collision walls. This changes those assets' occupied space, but does not change collision algorithms or close any tested corridor.

## Validation and evidence

- Same-camera before/after captures for A/B/C, night A/B, ecology, village and wetlands: `environment-scenes.cjs`.
- Desktop 1280×720, portrait 390×844, landscape 844×390: actual bird-view rendering, all five regions, distinct route samples, no view selector, V does not change view, knowledge/help remain usable (`environment-browser-test.cjs`).
- All nine complete model-piloted journeys finish with Health 100 and the same final Energy as the stability baseline: A 45, B 45–55, C 25–60 (`environment-journey-test.cjs`).
- All nine instrumented browser pilot journeys check rendering, area previews, observed-topic knowledge timing, resource logs and arrival (`environment-flight-test.cjs`).
- Stability model regression and 1,251 geometry cross-section checks rerun after tower/tree edits. All 18 city branch centerlines remain inside the unchanged boundaries.

## Limits

No physical phone or classroom user test. Mobile layouts use Chromium emulation. Full journeys use a test pilot; normal play does not auto-navigate. The landscape is a schematic habitat composition in the existing renderer, not a survey-accurate model of Mai Po. White facade patterns illustrate visibility measures; their game-scale appearance is not a construction specification. Low-detail distant geometry and the existing stylised bird remain.

Public Pages deployment status is checked separately from local browser tests. This environment cannot directly access the public Pages hostname, so deployment success is not described as online playtesting.

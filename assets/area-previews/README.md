# Actual scene previews — UW-ENVIRONMENT-1

These five WebP assets are self-generated captures of the actual Urban Wings renderer using the existing bird-following camera. They reuse the game’s existing architecture, textures and attributed sky assets; no new external image source is introduced.

Generated with `tools/environment-scenes.cjs --after-only`, 1000×650, then encoded at WebP quality 90.

| Asset | Scene |
| --- | --- |
| glass.webp | Glass route A, progress 28 |
| light.webp | Night route A, progress 63 |
| green.webp | Ecological C, progress 97 |
| pond.webp | Village/fishpond C, progress 120 |
| wetland.webp | Wetland destination area, progress 165 |

City captures use the actual position and heading recorded by the complete-flight test pilot (`evidence/environment/flight-poses.json`).

These are representative gameplay views, not a survey map or concept artwork. The existing preview UI and educational logic are unchanged. The offline build embeds all five assets.

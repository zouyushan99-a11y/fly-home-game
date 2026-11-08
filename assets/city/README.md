# Shared city design

Original procedural layout and SVG, generated for this project; no third-party assets added. Existing building atlases, sky images, grass, roads, bridges and lighting are reused with their existing attribution.

The same world geometry is rendered before and after selection. A/B/C are smooth world-space centerlines through one district, with the same entrance and exit. They are not three maps or parallel fixed lanes. World movement is preserved at selection. Forward progress uses centerline arc length; player steering remains additive and does not add Energy penalties.

A: deep commercial glass solids, no markings, 10.4-unit challenge openings; alternating offsets require steering. B: reflective glass plus cached regular circular white dots, 16-unit challenge openings. C: ordinary residential facade/side textures, green landscape, 26-unit challenge openings, designated one-time rest. All values are game design, not ecological measurements. Glass markings communicate visibility; lower game collision risk comes from wider geometry, not random damage or immunity.

`plan-shared-city.py` uses footprint intersection tests to preserve ground roads/bridge reservations, other route centerlines, and building separation. Existing skyline parcels intruding on the new route footprints are removed. Background buildings close to routes now participate in the same collision system. Regenerate with the planner, then sync-shared-city.py and sync-building-art.py.

# Layout provenance and regeneration

Original deterministic procedural layout; no third-party bridge models. Baseline foreground and roads: repository commit 215a5dd. All road, parcel and bridge coordinates are precomputed once and embedded in index.html.

Regenerate from the repository root:

```
node tools/export-world-input.cjs
python3 tools/plan-urban-world.py
python3 tools/sync-world-layout.py
python3 tools/sync-ground-art.py
python3 tools/sync-building-art.py
node tools/urban-model-test.cjs
python3 tools/urban-layout-test.py
```

The new end progress in layout.json must match STAGE_ENDS[4]. The old natural-layout rebuild check targets the earlier seven-road layout; use the urban suites for this revision.

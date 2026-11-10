# Urban Wings — UW-LEARNING-3

Baseline: `5cbb62e` (environment update). This release changes educational content and interaction, not the world layout or flight rules.

## Completed features

- A three-step bilingual first-time tutorial: separated migratory bird / Hong Kong / Mai Po mission; visibly distinct Health and Energy explanations; safe left/right practice using the existing controls. Skip, saved completion, explicit start-screen review and help-menu restart-and-review are available. Practice never advances the journey or consumes resources.
- Five existing area introductions retain their actual scene images, prominent titles, descriptions, observation hints and Continue buttons. Fishpond wording now explicitly qualifies management, species and conditions.
- Seven contextual cards retain existing accurate content, with an additional marked-glass encounter card. Marked-glass detection checks a nearby visible, camera-facing marked facade; it does not unlock from choosing B alone. Existing pause/Continue behaviour and duplicate prevention remain.
- Comparison panels receive accessible green ✓ / red ✕ overlays: glass, marked glass, light and lawn/habitat compare less-friendly left with friendlier right; disturbance compares quiet observation left with close disturbance right. Pond/wetland diagrams show complementary habitats, so neither half is falsely labelled wrong.
- Six bilingual quiz topics with plausible misunderstandings instead of absurd distractors. Two different topics are randomly selected, answer positions shuffled, and the last pair avoided where possible. Explanatory feedback, retry, no countdown and no resource penalty remain. The quiz follows successful reunion and precedes completion. Failure goes directly to its truthful recap after the existing ending animation.
- Actual visited areas are recorded separately from cards read. The ending includes only those areas as experiences, three practical actions, SDG 15, a reflection question and optional unread-topic learning. Existing conservation research and citizen-science material remains in expandable reading; unverified statistics remain omitted.
- Help text now matches the existing damage/resource rules; no numeric gameplay rule changed. Offline HTML embeds the same updated content and images.

## Validation

- `learning-model-test.cjs`: all five introductions before their boundaries; frozen progress/resources/time; safe tutorial; seven topics require observation and do not repeat; 1,000 random quiz pairs across six topics and all six answer orders; exact baseline comparison of Journey logic except tutorial/bookkeeping and of renderer except encounter observation. Shared city data unchanged.
- `learning-browser-test.cjs`: Chromium at 1280×720, 390×844 and 844×390. Actual keyboard or CDP touch input in practice; completion, skip, review, restart; all five image introductions; all seven cards and correct badge sides; wrong/correct answers and retry; no resource changes; two-question ordering; personalised subset-of-areas recap; bilingual summary; success and failure flows. Screenshots under `evidence/learning`.
- `learning-flight-test.cjs`: nine complete browser test-pilot journeys, recording rendered observations, five introductions, knowledge events, resources and visited areas. All nine finish at Health 100; final Energy A 45, B 45–55, C 25–60. Complete resource ledgers match the previous environment release, and no position recovery is needed. Results in `evidence/learning/flights.json`.
- `learning-live-test.cjs`: uninstrumented served page with real animation loop, keyboard and emulated touch practice, actual flight to the first area introduction and first encountered knowledge card.

## Limits and incomplete validation

- No physical phone, child classroom trial or teacher readability review. Mobile tests are Chromium emulation.
- Full journeys use a test pilot and sampled rendering; they do not substitute for manual playability testing. Real-page input smoke tests cover the opening sequence.
- The requested approximately 15–30 second quiz duration is a design target, **not established by learner testing**. There is intentionally no timer; students may take longer to read and retry.
- No new field research or numerical ecological claims. Existing qualified educational content and source links are retained. Original source statistics remain unverified and are not displayed as facts.
- Public Pages deployment status is checked separately. The managed network blocks direct access to the public Pages hostname, so a successful deployment is not a claim of online playtesting.

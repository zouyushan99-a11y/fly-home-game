# Urban Wings — flight boundaries and collision recovery

Baseline: `39da2c0` (UW-CLARITY-2). New release identifier: UW-STABILITY-1.

## Causes verified in the previous implementation

1. Heading could reach ±90°, so forward velocity approached zero. There was no world-space lateral limit. The player could reach dense backdrop buildings that were originally outside the designed routes.
2. Swept collisions prevented penetration but stopped at the wall indefinitely. There was no last-safe-position recovery. Continuous time-based Energy drain continued during obstruction.
3. Ecology/village rest rewards depended on progress ≥21 within a stage, not spatial contact with the visible rest point. Depleted Energy automatically became 25 after three seconds. These caused apparently unexplained increases.
4. Existing damage/energy constants differed from the explicit values in this request. The new requested values take precedence.

## Repairs to the existing systems

- Retained Journey movement, heading input and swept building-part collision. Forward heading is limited to ±64.8°, with a positive forward component. Left/right remain real steering; there is no general auto-navigation or automatic obstacle avoidance.
- Added outer flight bounds derived from the shared city’s existing branch polylines and entrance/reconnection routes. Ecology/village/wetland use bounded corridors around the existing world path. All internal city paths remain available. Dense outer decorations remain in the world; the player cannot wander indefinitely into them.
- A light translucent blue boundary appears only nearby. Outward motion is clipped without injury, with immediate inward steering. Normal distance-based flight costs still apply when genuinely completing a flight segment; touching the boundary adds no charge.
- Collision uses the existing swept rotated geometry and body radius. Injury is recorded once per obstacle per attempt. On persistent blockage (0.4 seconds of active simulation), search nearby valid positions at the **same longitudinal progress**, favour the selected route, verify body clearance and forward clearance, reset heading for escape, and grant 1.5 seconds of injury protection. Controls remain available. Normal operation does not use this recovery steering.
- A stored safe position contributes a candidate for recovery. Already-invalid positions recover without treating a programming trap as a new injury. No Health/Energy refill accompanies positional recovery; route and lesson progress are retained.
- Resource changes now use the existing idempotent event mechanism, with an auditable `resourceLog` and explicit on-screen reasons. Time spent blocked cannot repeatedly drain Energy.
- Rest requires actual radial overlap with the same marked rest point used by the scene. Each point is consumed once, including across checkpoint retry. Removed automatic three-second Energy refill. At zero Energy, players can glide and steer toward a marked rest; zero Energy does not cause injury or death.
- Kept the existing single checkpoint retry (Health 70 / Energy 60, explained by the retry dialog), and the existing failure flow after the retry is used. Completed educational cards and resource-event IDs are retained; injury protection for previously hit obstacles resets on the checkpoint retry.

## Resource values (game-design units)

| Event | Value |
| --- | --- |
| Starting Health / Energy | 100 / 100 |
| Minor / severe injury | −15 / −25 Health |
| Flight segment | −5 Energy per 15 progress units / 135 world units of forward travel |
| Detour | −5 once per selected C section |
| Light correction | −5 once in night city |
| Designated ecological rest | +20 once per point |
| Wetland arrival | +10 once |
| Boundary contact / positional recovery | No additional cost or refill |

All resources clamp to 0–100. Thus a +20 rest at Energy 90 actually adds 10; the notice reports the actual gain. These values are game design, not biological measurements. Checkpoint restoration is the preserved, explicitly explained exception to normal rest/arrival recovery.

## Verification

- `tools/stability-model-test.cjs`: sustained left/right, immediate inward response, boundary checks in every region, minor/severe damage, duplicate contact, front collision recovery at 60 Hz and 4 Hz, embedded-position recovery, resource events, pause freeze, spatial/one-time rest, zero-Energy glide, arrival, and one checkpoint retry.
- `tools/stability-layout-test.cjs`: 1,251 longitudinal cross-sections have a valid safe forward position; all 18 day/night branch centerlines remain inside the boundary. This is sampled geometric validation, not proof for every possible coordinate.
- `tools/stability-journey-test.cjs`: nine complete model-piloted route combinations reach the destination with Health 100. Final Energy A 45; B 45–55; C 25–60. No normal-route collision recovery was needed.
- `tools/stability-browser-test.cjs`: Chromium desktop 1280×720, portrait 390×844 and landscape 844×390. Real keyboard events and CDP touch events operate the game input handlers; both cameras, boundary contact, collision escape, spatial rest feedback and zero-Energy controls tested. Simulation time is advanced deterministically in this fixture.
- `tools/stability-flight-test.cjs`: nine complete browser-rendered, instrumented pilot journeys, including previews, knowledge, both city chapters and wetland arrival. Resource logs record each cause. All nine histories reconcile exactly to final Energy; every positive event is a designated rest or arrival. Automated pilots establish connectivity, not child-player usability.

Screenshots and JSON results: `evidence/stability/`; gallery: `stability.html`.

## Limits

No physical phone tested. Touch is Chromium emulation. Normal gameplay is not auto-piloted; only the test harness uses a pilot. Some camera translation is visible during exceptional collision recovery, because a safe same-progress location must replace the blocked position. Normal collisions still cause injury, and repeated distinct injuries can legitimately end a journey under the retained Health rules. Boundary contact itself is harmless.

The cloud proxy blocks direct access to the public Pages host. Local game testing and public GitHub Actions deployment status are reported separately; successful deployment is not a claim of having played the online page.

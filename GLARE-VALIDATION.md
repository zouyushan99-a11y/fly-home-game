# UW-GLASS-5: visible approach glare

The previous edge cue peaked at 5.5% opacity and reached only about 2% at the tested approach. Its centre-only visibility test also missed visible side facades. The new geometry samples the rotated facade extent, extends approach distance from 32 to 65 world units, and caps edge opacity at 14%. Surface sheen extends from 55 to 85 units, with a smooth quadratic rise capped at 18%; existing sky/cloud reflections and pane detail remain underneath.

Only the outer 14% of either screen edge receives screen glare. The centre remains unchanged by that overlay. There is no full-screen flash, oscillation, added damage, steering or new resource rule. Existing smoothing and reduced-effects disable behaviour remain.

Chromium browser tests passed at 1280×720, 390×844 and 844×390: gradual rise, central overlay pixel changes zero, freeze on pause, disable with reduced effects, unchanged resources, keyboard/touch steering, collision protection and recovery. Layout regression passed all nine centre paths and unchanged gameplay/education/boundaries. These are browser-emulated devices, not physical phones; no user comfort study. Public online gameplay remains unverified due to network policy.

Before/after images use the same scripted approach position. Historical UW-GLASS-4 measurements remain in GLASS-VALIDATION.md; updated browser metrics are in evidence/glass/browser.json.

# Scheduled Update: Trend Check via Inertia Flow

**Status:** `Planned`

---

## Current Situation

The `Trend_Check` function currently determines the direction of emotional change by comparing newly generated `target_emotion_tank` values against the existing tank values. This gives a direction signal (rising, falling, stable) based on the difference between the new target and the previous target.

---

## Planned Change

Replace the target-comparison approach with tracking the **actual flow of emotion through the inertia system** — i.e., monitor the trajectory of the live emotion state as it moves toward its target under inertia rates, rather than comparing target values directly.

---

## Reason for Change

The target-comparison approach tracks where the emotion is *going*, not where it *is* or *how fast it is moving*. Tracking inertia flow would give a more accurate and continuous signal of the emotional trajectory — capturing whether an emotion is actively accelerating, coasting, or decelerating toward a target. This is more representative of actual emotional momentum.

---

## Current Status

**Planned.** No design work has started. Depends partially on the inertia tuning work (`emotion_inertia_tuning.md`) being resolved first, since the inertia flow signal is only meaningful if inertia rates are calibrated to realistic values.

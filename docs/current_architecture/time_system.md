# Time System

## Overview

MindSim operates two parallel time domains simultaneously. The distinction exists because the mind has both fast, reactive processes that must respond to real-world events in real time, and slow, long-term processes that simulate the gradual evolution of neural structure over days and weeks.

---

## Real Time

**Scale:** 1 : 1 with wall clock time.

Used for all **short-term, reactive** system processes where responsiveness to the actual pace of stimulus arrival matters.

| Process | Domain |
|---|---|
| Neuron Decay | Real Time |
| Refractory Timers | Real Time |
| Emotional Inertia | Real Time |

---

## Simulated Time

**Scale:** `1 second real = 96 seconds simulated`

Used for all **long-term, structural** simulation tasks that represent changes occurring over days or weeks in biological systems.

| Process | Domain |
|---|---|
| Hebbian Decay | Simulated Time |

> Hebbian bond decay begins if a cluster pair's `last_strengthening` is more than 2 days in **simulated time**. At 96x acceleration, 2 simulated days corresponds to approximately 30 real-time minutes.

---

## Design Rationale

The dual-time system allows MindSim to:
- React to stimuli with biologically plausible short-term timing (neuron refractory periods in seconds, emotional inertia in seconds-to-minutes).
- Simulate long-term structural learning and forgetting (Hebbian bond decay over simulated days) without requiring the system to run for actual days between test cycles.

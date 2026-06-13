# ADR-006: Dual Time System — Real Time and Simulated Time

**Status:** Accepted

---

## Context

MindSim simulates both fast, reactive neural processes and slow, long-term structural changes (e.g., synaptic bond decay over days). Running the system at real-time pace would require actual days to observe long-term effects like Hebbian decay. This is impractical for development, testing, and simulation use.

At the same time, fast processes like refractory timers (2 seconds) and emotional inertia must track actual wall clock time to remain coherent with real-world stimulus timing.

---

## Decision

Operate two parallel time domains:

| Domain | Scale | Processes |
|--------|-------|-----------|
| Real Time | 1 : 1 | Neuron decay, refractory timers, emotional inertia |
| Simulated Time | 1s real = 96s simulated | Hebbian decay (bond decay after 2 simulated days) |

At 96x acceleration, 2 simulated days = approximately 30 real minutes.

---

## Alternatives Considered

- **Single real-time clock for all processes:** Rejected — long-term processes like Hebbian decay would require the system to run for actual days to produce any structural change.
- **Single simulated-time clock for all processes:** Rejected — fast processes like refractory timers would fire at 96x speed, making a 2-second refractory period fire effectively every ~125ms of real time.
- **Configurable time multiplier (global):** More flexible but adds complexity; the two-domain approach with fixed scales for fast vs. slow processes is cleaner.

---

## Consequences

**Benefits:**
- Long-term structural changes (synaptic decay) can be observed and tested in minutes of real time.
- Short-term reactive processes remain calibrated to real stimulus timing.
- Clean separation: fast = real time, slow = simulated time.

**Tradeoffs:**
- The 96x ratio is a fixed design parameter. Changes to the target simulation timescales require adjusting this constant.
- Developers must be explicit about which time domain applies when implementing new processes.
- The 96x ratio may need re-evaluation as more long-term processes are added (e.g., memory consolidation in the Dream Layer).

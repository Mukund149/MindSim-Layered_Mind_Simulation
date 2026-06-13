# Scheduled Update: Emotion Inertia Rate Tuning

**Status:** `Blocked` — deferred pending resolution of emergent interaction with neuron decay

---

## Current Situation

The `Update_Inertia` function moves the current emotion state gradually toward `target_emotion_tank` values using per-emotion inertia rates, rather than snapping directly to the target. This is the intended mechanism for producing the **lingering emotional effect** — emotions rise and fall slowly rather than instantly.

**Known issue:** Current inertia rates are set too high. Emotions converge to their target values faster than intended — the gradual movement is happening, but over too short a time window to produce meaningful lingering.

---

## Planned Change

Tune the inertia rates for each of the 8 base emotions downward so that emotional transitions take longer and produce a more realistic persistence of emotional state.

---

## Reason Deferred

The neuron decay system in the neuron layer **also** creates a lingering effect: decayed (but non-zero) cluster signals from prior stimuli persist in the activation map and contribute to emotion scoring on subsequent stimuli. This is an **emergent interaction** between the two systems.

If inertia rates are tuned down independently of this interaction, it is unclear whether the combined lingering effect will be over-tuned (too much persistence) or correctly calibrated. The two mechanisms — direct inertia in the emotion layer and indirect lingering via neuron decay — are not independently controllable without understanding their joint contribution.

The emergent interaction is considered a feature, not a bug (*"EMERGENCE BABY"*).

---

## Open Questions

- What is the relative contribution of neuron decay vs. inertia rates to the observed emotional persistence?
- Should inertia rates be tuned without changing neuron decay rates, or should both be adjusted together?
- Is the current combined effect already producing satisfactory lingering, making explicit inertia tuning unnecessary?

---

## Current Status

**Blocked** on answering the open questions above. No tuning will be done until the interaction between neuron decay lingering and emotion inertia is characterised. The system currently relies on neuron decay as the primary lingering mechanism.

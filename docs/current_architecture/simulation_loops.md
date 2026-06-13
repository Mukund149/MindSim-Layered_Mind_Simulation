# Simulation Loops

## Overview

MindSim runs two concurrent simulation loops as threads. Together they produce the dual nature of a mind: reactive processing of stimuli, and continuous background evolution of internal state.

---

## Loop 1 — Stimulus Loop (Event-Driven)

Triggered on each incoming stimulus. Executes the full processing pipeline in sequence.

| Step | Action |
|---|---|
| a | Stimulus arrives → Neuron Layer generates `activation_map` |
| b | Memory Layer retrieves memories related to the stimulus |
| c | Emotion Layer creates `emotion_map` using `activation_map` and retrieved memories |
| d | Personality Layer modulates emotions based on current personality state |
| e | Cognition + Meta-Cognition generates the final response using all available data |
| f | Final response is converted into memory and stored in the brain |

---

## Loop 2 — Background Process Loop (Continuous)

Runs independently of stimulus arrival. Responsible for the continuously evolving internal state of the mind — decay, lingering, emotional drift.

| Step | Action |
|---|---|
| a | Continuously applies decay to activated neuron clusters |
| b | Decays synaptic bonds not recently strengthened |
| c | Updates emotional inertia; compounds emotions; checks intensity of growing emotions |

---

## Interaction Between Loops

The two loops share MindState. The background loop modifies the `activation_map` (via decay) and the emotion state (via inertia updates) continuously, so by the time the next stimulus arrives in Loop 1, the system is already in a partially evolved state — not a clean reset. This is what produces the emergent lingering effects across stimulus boundaries.

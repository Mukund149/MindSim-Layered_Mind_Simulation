# MindSim — Project Overview

## What Is MindSim

MindSim is a layered simulation of the human mind. It processes external stimuli through a biologically-inspired pipeline of neuron activation, memory retrieval, emotion generation, personality modulation, and cognitive response — all running as a continuous-state, emergent system.

---

## Current Architecture Pipeline

```
Neuron Layer → Memory Layer (retrieval) → Emotion Layer → Personality Layer → Cognition + Meta-Cognition → Memory Layer (storage) → Dream Layer
```

> Memory appears twice: once before the emotion layer for context retrieval, and once after cognition for storing the final response.

---

## Layer Responsibilities

| Layer | Responsibility |
|---|---|
| **Neuron Layer** | Converts stimulus to vector embeddings, fires neuron clusters, applies Hebbian learning, decays activations over time |
| **Memory Layer (retrieval)** | Retrieves memories related to the current stimulus before emotion processing |
| **Emotion Layer** | Generates 8 base emotions from the activation map, regulates, compounds, and tracks emotional state over time |
| **Personality Layer** | Modulates the generated emotions according to the current personality state of the brain |
| **Cognition + Meta-Cognition** | Generates the final response using all available data (activation map, emotion map, working memory) |
| **Memory Layer (storage)** | Converts the final response into memory and stores it in the brain |
| **Dream Layer** | Runs during idle/background state — design pending |

---

## MindState — Central Data Bus

MindState is the central managing body of the system. It is the **only** entity responsible for information exchange between layers. It represents the complete current state of the mind at any moment.

**Stored in MindState:**
- `current_stimulus` — the active input
- `activation_map` — output from the neuron layer
- `emotion_map` — output from the emotion layer
- `working_memory` — context for the current situation

---

## Simulation Loops

Two concurrent threads run the simulation:

**1. Stimulus Loop** (event-driven)
Processes each incoming stimulus through the full pipeline: neuron → memory retrieval → emotion → personality → cognition → memory storage.

**2. Background Process Loop** (continuous)
Maintains the ever-evolving nature of the mind independently of stimulus arrival:
- Performs decay on activated neuron clusters
- Decays unused synaptic bonds
- Updates emotional inertia, compounds emotions, checks emotion intensity

---

## Time Systems

MindSim operates two parallel time domains:

| Domain | Scale | Used For |
|---|---|---|
| **Real Time** | 1 : 1 | Neuron decay, refractory timers, emotional inertia |
| **Simulated Time** | 1s real = 96s simulated | Hebbian decay, long-term memory processes |

---

## Major Architectural Principles

- **Emergent behaviour over hard rules** — the system is designed so complex behaviour (emotions, lingering, pattern recognition) arises from simple interacting mechanisms rather than explicit mappings.
- **Continuous state** — the mind is never reset between stimuli; activations, emotions, and synaptic weights persist and decay naturally.
- **Biologically-inspired references** — Appraisal Theory, OCC Model, Plutchik's Wheel, Hebbian Theory are used as design references, adapted for simulation constraints.
- **Pending boost pattern** — boosts (Hebbian pre-activation, emotional regulation) are always collected first and applied in a single batch to prevent mid-calculation contamination.
- **Bounded absorption** — accumulation of signals uses `value += boost * (1 - value)` to impose natural resistance at high ranges, preventing runaway amplification.

# ADR-003: Streak-Based Hebbian Bond Formation

**Status:** Accepted

---

## Context

Hebbian learning in MindSim creates unidirectional synaptic bonds between co-activated neuron clusters (`source → target`). These bonds produce `Pre_Activation_Boost` — when the source fires, the target receives a signal boost proportional to the synaptic weight.

The initial implementation formed a bond after **a single co-activation** of a cluster pair. Testing revealed this caused the system to learn coincidental relationships — two clusters that happened to both be active in a single stimulus would form a bond and begin boosting each other indefinitely.

A naive fix of requiring N total co-activations (e.g., 5 over any time period) was also rejected: 5 coincidental co-activations scattered over days are not evidence of a real pattern.

---

## Decision

Implement a **streak-based bond formation system**:

- A cluster pair must co-activate **consecutively** a minimum of **5 times** to begin forming a meaningful synaptic bond.
- If the source cluster fires **without** the target cluster during an active streak, the streak is decremented by 1.
- The required streak length is **dynamic**: it grows with the current `synaptic_weight` of the pair, starting at 5.
- Bonds decay if `last_strengthening` exceeds 2 days in simulated time.

---

## Alternatives Considered

- **Single co-activation (v1):** Rejected — too easily triggered by coincidence.
- **N total co-activations (no streak):** Rejected — coincidences can accumulate to N over time without representing a real pattern.
- **Time-windowed co-activations:** Not mentioned as an explicit candidate; streak approach was chosen as more robust.

---

## Consequences

**Benefits:**
- Only genuine, repeated, uninterrupted co-activation patterns form bonds.
- Coincidental single activations or scattered occasional co-activations are naturally rejected.
- Produces actual pattern recognition in the neuron layer: recurring stimulus types that reliably co-activate the same clusters develop structural relationships.

**Tradeoffs:**
- A real relationship that has occasional single-fire interruptions (source fires, target doesn't) will be slowed in bond formation — streak decrements penalise even natural variation.
- The dynamic streak threshold means that once a bond starts forming, it becomes progressively harder to continue strengthening it — intended to prevent runaway bond formation but may slow legitimate learning.

# Archive: Hebbian Learning v1 — Single Co-Activation Bond Formation

## Previous Design

A synaptic bond between two clusters was formed after just **one co-activation** of the pair.

---

## Why It Was Created

This was a direct, simple implementation of Hebbian theory: if two neurons fire together, they wire together. One joint firing was considered sufficient evidence of a relationship.

---

## Problems Discovered

Testing revealed that a single co-activation is easily coincidental. Unrelated clusters that happened to both be active during one stimulus would form a synaptic bond, causing the system to learn and reinforce coincidental co-occurrences. This resulted in false associations between cluster pairs — the pre-activation boost would then artificially inflate cluster signals based on irrelevant prior coincidences.

Furthermore, simply requiring N total co-activations (e.g., 5 over any time span) was also insufficient, as 5 coincidental co-activations could accumulate slowly over days with no real pattern.

---

## Why It Was Replaced

The current architecture uses a **streak-based system**. A cluster pair must co-activate **5 consecutive times** without interruption to form a meaningful bond. If the source fires without the target during an active streak, the streak is decremented by 1. This enforces that only genuine, repeated patterns produce synaptic bonds — coincidental single or scattered co-activations are rejected.

The dynamic streak threshold (growing with `synaptic_weight`) adds further resistance to low-confidence bonds forming prematurely.

See [ADR-003](../adr/ADR-003-streak-based-hebbian.md).

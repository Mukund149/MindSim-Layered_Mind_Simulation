# Archive: Neuron Decay v1 — Uniform Fast Decay

## Previous Design

All neuron clusters shared a single, uniform decay rate of approximately `0.05`.

Decay formula was the same as current:
```
cluster.current_signal *= (1 - cluster.decay_rate)
```

But with `decay_rate = 0.05` applied uniformly across all clusters.

---

## Why It Was Created

A uniform decay rate was the simplest implementation to get the decay system running. The intent was always to have clusters fade after firing rather than remain permanently active.

---

## Problems Discovered

With `decay_rate = 0.05`, the entire activation map was emptied in under **2 seconds**. By the time the next stimulus arrived, all cluster signals had already decayed to zero. The intended lingering effect — where prior emotional context carries forward into the processing of subsequent stimuli — was present in the code but had no practical effect at runtime.

---

## Why It Was Replaced

The current architecture assigns **individual decay rates per cluster**. Stronger signals can now persist for up to **10 minutes**, creating genuine lingering effects. Clusters activated by highly threatening or emotionally intense stimuli continue to influence subsequent stimulus processing, which is the biologically inspired behaviour MindSim targets.

See [ADR-002](../adr/ADR-002-per-cluster-decay-rates.md).

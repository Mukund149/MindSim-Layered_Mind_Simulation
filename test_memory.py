import numpy as np

from Brain.Memory_layer import MemoryLayer
from Simulation.mind_state import MindState

mind_state = MindState()

memory_layer = MemoryLayer(mind_state)
print(
    memory_layer.collection.count()
)
print("Creating memories...")

memory_layer.create_memory(
    stimulus="I failed my interview",
    response="I felt anxious",
    stimulus_vector=np.array([1.0, 2.0, 3.0]),
    emotion_map={
        "fear": 0.9,
        "sadness": 0.7
    }
)

memory_layer.create_memory(
    stimulus="I won a football match",
    response="I felt happy",
    stimulus_vector=np.array([4.0, 5.0, 6.0]),
    emotion_map={
        "joy": 0.95
    }
)
print(
    "\nChromaDB Memory Count:",
    memory_layer.collection.count()
)

print("\nStored Memories:")
print(len(memory_layer.memories))

for memory in memory_layer.memories:
    print(memory.stimulus_summary)

print("\nTesting Retrieval...")

results = memory_layer.retrieve_memories(
    np.array([1.0, 2.0, 3.0])
)

print("\nRetrieved Memories:")

for memory, score in results:
    print(
        f"{memory.stimulus_summary}"
        f" | Score = {score:.3f}"
    )

print("\nTesting Emotion Merge...")

combined = memory_layer.combine_memory_emotions(
    results
)

print(combined)

print("\nTesting Retrieval Pipeline...")

pipeline = memory_layer.memory_retrieval_pipeline(
    np.array([1.0, 2.0, 3.0])
)

print(pipeline)

print("\nTesting Decay...")

for memory in memory_layer.memories:
    print(
        memory.stimulus_summary,
        memory.strength
    )

memory_layer.decay_memories()

print("\nAfter Decay:")

for memory in memory_layer.memories:
    print(
        memory.stimulus_summary,
        memory.strength
    )


print("\nMemory Layer Test Complete!")
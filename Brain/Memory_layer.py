from dataclasses import dataclass
from datetime import datetime
from collections import deque
from typing import List, Dict
import uuid
import numpy as np
import chromadb
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Memory:
    id: str
    stimulus_summary: str
    response_summary: str
    stimulus_vector: List[float]
    emotion_map: Dict[str, float]
    emotional_weight: float
    strength: float
    timestamp: datetime
    recall_count: int = 0
    last_recalled: datetime = None
    permanent: bool = False

class MemoryLayer:

    MAX_CONTEXT_WINDOW = 5
    DECAY_RATE = 0.005
    DELETE_THRESHOLD = 0.1
    RECALL_BOOST = 0.05

    def __init__(self, mind_state):
        self.mind_state = mind_state

        self.memories: List[Memory] = []

        self.context_window = deque(
            maxlen=self.MAX_CONTEXT_WINDOW
        )

        self.chroma_client = chromadb.HttpClient(
        host="localhost",
        port=8000
    )
        

        self.collection = (
            self.chroma_client.get_or_create_collection(
                name="mindsim_memories"
            )
        )

        print(
            f"ChromaDB Ready | Stored Memories: "
            f"{self.collection.count()}"
        )

    
    def retrieve_memories(self,stimulus_vector,top_k=5):
        if len(self.memories) == 0:
            return []
        retrieval_results = []
        for memory in self.memories:
            similarity = cosine_similarity([stimulus_vector],[memory.stimulus_vector])[0][0]
            retrieval_score = (similarity * memory.strength)
            retrieval_results.append((memory, retrieval_score))
        retrieval_results.sort(key=lambda x: x[1],reverse=True)
        top_memories = retrieval_results[:top_k]
       
        for memory, _ in top_memories:
            memory.recall_count += 1
            memory.last_recalled = datetime.now()
            memory.strength = min(memory.strength + self.RECALL_BOOST,1.0)
        return top_memories
    #checks if there are any memories, then calculates similarity between stimulus vector and memory stimulus vector, multiplies 
    # by strength to get retrieval score, sorts by retrieval score and returns top k memories. 
    # Also updates recall count, last recalled timestamp and boosts strength of recalled memories

    def combine_memory_emotions(self,retrieved_memories):
        combined_emotion_map = {}
        total_strength = 0.0
        for memory, _ in retrieved_memories:
            total_strength += memory.strength
            for emotion, value in memory.emotion_map.items():
                if emotion not in combined_emotion_map:
                    combined_emotion_map[emotion] = 0.0
                combined_emotion_map[emotion] += (value * memory.strength)
        if total_strength > 0:
            for emotion in combined_emotion_map:
                combined_emotion_map[emotion] /= total_strength
        return combined_emotion_map
    # all the memories are taken into account and unke emotions are merged together.
    #  stronger memories ka influence will be more in the combined emotion map.
    
    def memory_retrieval_pipeline(self,stimulus_vector):
        retrieved = self.retrieve_memories(stimulus_vector) #memory search 
        combined_emotions = (
            self.combine_memory_emotions(retrieved)) # Merges emotions
        return {
            "retrieved_memories": retrieved, #actual retrieved memories
            "combined_emotion_map": combined_emotions, #emotional influence from past experiences
            "context_window": list (self.context_window) #short term memories returned
        }
    

############################################### STORAGE SUBMODULE #################################################


    def create_memory(
        self,
        stimulus: str,
        response: str,
        stimulus_vector,
        emotion_map: Dict[str, float] 
    ): #to create a memory mujhe chaiye what happened, the response to it , semantic meaning aur emotional state   

        emotional_weight = self.calculate_emotional_weight(emotion_map)
        memory = Memory(
            id=str(uuid.uuid4()),
            stimulus_summary=stimulus,
            response_summary=response,
            stimulus_vector=stimulus_vector.tolist(),
            emotion_map=emotion_map,
            emotional_weight=emotional_weight,
            strength=emotional_weight,
            timestamp=datetime.now(),
            permanent=emotional_weight > 0.95
        ) 
        # how important the memory is based on emotional weight, memory object bnega usme stimulus, response
         # semantic vector, emotion map, emotional weight, strength, timestamp and permanent flag hoga        
        self.memories.append(memory)
        self.collection.add(
        ids=[memory.id],
        embeddings=[memory.stimulus_vector],
        metadatas=[{
            "stimulus": memory.stimulus_summary,
            "response": memory.response_summary,
            "emotional_weight": memory.emotional_weight,
            "strength": memory.strength,
            "permanent": memory.permanent,
            "timestamp": str(memory.timestamp)
        }]
)
        return memory
    
    def update_context_window(self,stimulus,response):
        self.context_window.append({
            "stimulus": stimulus,
            "response": response,
            "timestamp": datetime.now()
        })
   
    def calculate_emotional_weight(self,emotion_map):
        if len(emotion_map) == 0:
            return 0.0
        values = list(emotion_map.values())
        peak_emotion = max(values)
        average_emotion = (sum(values) / len(values))
        emotional_weight = (peak_emotion * 0.6 + average_emotion * 0.4)
        emotional_weight = max(0.0,min(emotional_weight, 1.0))
        return emotional_weight

    
    def decay_memories(self):
        surviving_memories = []
        for memory in self.memories:
            if memory.permanent:
                surviving_memories.append(memory)
                continue
            memory.strength *= (1 - self.DECAY_RATE)
            if memory.strength > self.DELETE_THRESHOLD:
                surviving_memories.append(memory)
        self.memories = surviving_memories

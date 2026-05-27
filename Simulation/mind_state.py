from dataclasses import dataclass, field

BASE_EMOTIONS = [
    "fear",
    "anger",
    "joy",
    "sadness",
    "trust",
    "disgust",
    "anticipation",
    "surprise"
]

def create_emotion_state():
    return {
        emotions:{
            "value":0.0,
            "label":None,
            "strength":0.0
        }
        for emotions in BASE_EMOTIONS
    }

@dataclass
class MindState:
    final_response: str = ""
    current_stimulus: str = ""
    activation_map: dict = field(default_factory=dict)
    stimulus_vector: list = field( default_factory=list )
    working_memory: dict = field(default_factory=dict)
    emotional_state: dict = field(
        default_factory=lambda:{
            "base": create_emotion_state(),
            "compounds": {},
            "trends":{},
            "dominant": None
        })
    personality_state: dict = field(default_factory=dict)
    active_thoughts: list = field(default_factory=list)
    mode: str = "active"



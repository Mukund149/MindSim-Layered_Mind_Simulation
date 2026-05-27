from config.emotions import NEURON_EMOTION_MAPPING, EMOTION_INTENSITY_ZONES, REGULATIONS, COMPOUNDING_RULES
from Simulation.mind_state import MindState

class EmotionLayer:
    
    REGULATION_THRESHOLD = 0.66 
    SUPRESSION_STRENGTH = 0.10
    RELEASE_STRENGTH = 0.10
    TREND_THRESHOLD = 0.05
    def __init__(self, mind_state:MindState):
        self.mind_state = mind_state
        self.compounds = {}
        self.trends = {}
        self.emotion_inertia = {
            "fear":0.7,
            "anger":0.6,
            "joy":0.5,
            "sadness":0.2,
            "trust":0.3,
            "disgust":0.4,
            "anticipation":0.5,
            "surprise":0.65
        }
        self.emotion_tanks = {
            "fear":0.0,
            "anger":0.0,
            "joy":0.0,
            "sadness":0.0,
            "trust":0.0,
            "disgust":0.0,
            "anticipation":0.0,
            "surprise":0.0
        }

    def process_emotions(self):
        activation_map = self.mind_state.activation_map
        self.emotion_tanks = {
            "fear":0.0,
            "anger":0.0,
            "joy":0.0,
            "sadness":0.0,
            "trust":0.0,
            "disgust":0.0,
            "anticipation":0.0,
            "surprise":0.0
        }
        for cluster, intensity in activation_map.items():
            mappings = NEURON_EMOTION_MAPPING[cluster]
            for emotion, weight in mappings.items():
                incoming = intensity*weight
                current = self.emotion_tanks[emotion]
                self.emotion_tanks[emotion] = min(current + incoming*(1-current), 1.0)

## MEMORY INFLUENCE PENDING

    
    def update_inertia(self):
        current_base = self.mind_state.emotional_state["base"]
        for emotion, target_value in self.emotion_tanks.items():
            current_value = current_base[emotion]["value"]
            inertia_rate = self.emotion_inertia[emotion]
            new_value = current_value + ( inertia_rate * (target_value - current_value))
            new_value = max(0.0, min(new_value, 1))
            current_base[emotion]["value"] = new_value
        
        return self.mind_state.emotional_state

    def intensity_check(self):
        current_base = self.mind_state.emotional_state["base"]

        for emotion, data in current_base.items():
            value = data["value"]
            
            data["label"] = None
            data["strength"] = 0.0
            for (zone_low, zone_high, label) in EMOTION_INTENSITY_ZONES[emotion]:
                if zone_low <= value < zone_high:
                    data["label"] = label
                    data["strength"] = (value - zone_low) / (zone_high - zone_low) 
                    break

    def regulate_emotions(self):
        current_base = self.mind_state.emotional_state["base"]
        pending_regulations = {
            emotion:0.0
            for emotion in self.emotion_tanks
        }
        for emotions, value in self.emotion_tanks.items():
            if value > self.REGULATION_THRESHOLD:
                supress = REGULATIONS[emotions]["suppress"]
                release = REGULATIONS[emotions]["release"] 
                supress_value = self.emotion_tanks[supress] * self.SUPRESSION_STRENGTH 
                pending_regulations[supress] -= supress_value
                release_value = self.RELEASE_STRENGTH * (1 - self.emotion_tanks[release])
                pending_regulations[release] += release_value
        

        for emotion, delta in pending_regulations.items():
            current_value = self.emotion_tanks[emotion]  
            new_value = min(1, max(0, current_value + delta))
            self.emotion_tanks[emotion] = new_value
            

    def compound_emotions(self):
        self.compounds = {}
        current_base = self.mind_state.emotional_state["base"]
        for (emotion_a, emotion_b, compound) in COMPOUNDING_RULES:
            if(current_base[emotion_a]["value"] > 0.4 and current_base[emotion_b]["value"] > 0.4):
                compound_strength = (current_base[emotion_a]["value"] * current_base[emotion_b]["value"]) ** 0.5
                self.compounds[compound] = compound_strength

        self.mind_state.emotional_state["compounds"] = self.compounds

    def trend_check(self):
        self.trends = {}
        for emotion, target_values in self.emotion_tanks.items():
            previous_value = self.mind_state.emotional_state["base"][emotion]["value"]
            delta = target_values - previous_value

            if delta > self.TREND_THRESHOLD:
                self.trends[emotion] = "rising"
            elif delta < -self.TREND_THRESHOLD:
                self.trends[emotion] = "declining"
            else:
                self.trends[emotion] = "stable"
        
        self.mind_state.emotional_state["trends"] = self.trends

    def dominant_emotion(self):
        base_emotions = {
            emotion:data["value"]
            for emotion, data in self.mind_state.emotional_state["base"].items()
        }
        all_emotions = {
            **base_emotions,
            **self.mind_state.emotional_state["compounds"]
        }
        dominant = max(all_emotions, key=all_emotions.get)

        if dominant in base_emotions:
            dominant_label = self.mind_state.emotional_state["base"][dominant]["label"]
        else:
            dominant_label = dominant

        self.mind_state.emotional_state["dominant"] = dominant_label 
        

    def process_targets(self):
        self.process_emotions()
        self.regulate_emotions()
        self.trend_check()

    def emotional_tick(self):
        self.update_inertia()
        self.intensity_check()
        self.compound_emotions()
        self.dominant_emotion()

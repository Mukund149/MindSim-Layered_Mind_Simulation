from Brain.Emotion_layer import EmotionLayer
from Brain.Neuron_Layer import NeuronLayer
from Simulation.mind_state import MindState
import threading
import time

class SimulationEngine:

    TICK_RATE = 0.5
    
    def start(self):
        self.running = True
        threading.Thread(
            target=self.background_process,
            daemon=True
        ).start()
    def stop(self):
        self.running = False
    
    def __init__(self):
        self.running = False
        self.mind_state = MindState()
        self.neuron_layer: NeuronLayer = NeuronLayer()
        self.emotion_layer = EmotionLayer(self.mind_state)

    def process_stimulus(self, stimulus):
        self.mind_state.current_stimulus = stimulus
        stimulus_vector = self.neuron_layer.process_stimulus(stimulus)
        activation_map = self.neuron_layer.fireActivations()
        self.mind_state.activation_map = activation_map
        self.mind_state.stimulus_vector = stimulus_vector
        self.neuron_layer.hebbian_strengthening()
        self.emotion_layer.process_targets()
    
    def background_process(self):
        while self.running:
            self.neuron_layer.decay()
            self.neuron_layer.hebbian_decay()
            self.emotion_layer.emotional_tick()
            time.sleep(self.TICK_RATE)

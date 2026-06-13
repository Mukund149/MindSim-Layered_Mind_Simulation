
from config.Clusters import CLUSTER_REFERENCES
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from Model.sentence_transformer import model, REFERENCE_VECTORS
from sklearn.metrics.pairwise import cosine_similarity
from Simulation.TimeSimulations import Mind_clock

@dataclass
class NeuronCluster : 
    type: str
    threshold: float
    refractory_timer: float = 2.0
    current_signal: float = 0.0
    decay_rate: float = 0.05 
    last_fired: Optional[datetime] = None
    is_fired: bool = False

@dataclass
class SynapticWeights :
    source_cluster : str
    target_cluster : str
    weight: float = 0.0
    co_activation_count: int = 0
    decay: float = 0.01
    streak: int = 0
    last_strengthened: Optional[datetime] = None

class NeuronLayer:

    MAX_SEMANTIC_RANGE = 0.75
    LEARNING_RATE = 0.01

    def __init__(self):
        self.mind_time = Mind_clock() 
        self.activation_map = {}
        self.Full_activation_map = {}
        self.clusters = {

            "threat": NeuronCluster(
                type="threat",
                threshold= 0.25,
                decay_rate= 0.008
            ),

            "reward": NeuronCluster(
                type="reward",
                threshold=0.30,
                decay_rate = 0.010
            ),

            "novelty" : NeuronCluster(
                type="novelty",
                threshold= 0.25,
                decay_rate= 0.025
            ),

            "familiarity" : NeuronCluster(
                type="familiarity",
                threshold= 0.35,
                decay_rate= 0.030
            ),

            "urgency" : NeuronCluster(
                type="urgency",
                threshold=0.30,
                decay_rate= 0.010
            ),

            "social_relevance" : NeuronCluster(
                type="social_relevance",
                threshold= 0.25,
                decay_rate= 0.010
            ),

            "discomfort" : NeuronCluster(
                type="discomfort",
                threshold=0.30,
                decay_rate= 0.008
            ),

            "affinity" : NeuronCluster(
                type="affinity",
                threshold=0.35,
                decay_rate= 0.005
            )
        }

        self.synaptic_weights = {}

        for source in self.clusters:
            for target in self.clusters:
                if(source != target):
                    self.synaptic_weights[(source, target)] = SynapticWeights(
                        source_cluster= source,
                        target_cluster= target
                    )

    def process_stimulus(self, stimulus:str):
        stimulus_vector = model.encode(stimulus)
        for cluster_name, ref_vector in REFERENCE_VECTORS.items():

            current_signal = self.clusters[cluster_name].current_signal
            scores = cosine_similarity([stimulus_vector], ref_vector)
            cluster_score = float(max(scores[0]))
            scaled_score = min(cluster_score / self.MAX_SEMANTIC_RANGE, 1)
            new_signal = current_signal + (scaled_score * (1 - current_signal))
            self.clusters[cluster_name].current_signal = min(new_signal, 1)

        self.pre_activation_boost()

        return stimulus_vector
    
    def pre_activation_boost(self):
        pending_boost_signals = {
            name: 0.0
            for name in self.clusters
        }
        for source in self.clusters:
            source_signal = self.clusters[source].current_signal
            for target in self.clusters:
                if(source != target):
                    synaptice_weight = self.synaptic_weights[(source, target)]
                    boost = synaptice_weight.weight * source_signal
                    pending_boost_signals[target] += boost * (1 - pending_boost_signals[target])
                    pending_boost_signals[target] = min(pending_boost_signals[target], 1.0)
        
        for cluster_name, boosted_signal in pending_boost_signals.items():
            current_signal = self.clusters[cluster_name].current_signal
            new_signal = current_signal + (boosted_signal * (1 - current_signal))
            self.clusters[cluster_name].current_signal = min(new_signal, 1)

    def decay(self):
        for cluster in self.clusters.values():
            cluster.current_signal *= 1 - cluster.decay_rate
            cluster.current_signal = max(cluster.current_signal, 0)


    def fireActivations(self):
        self.activation_map = {}
        for cluster in self.clusters.values():
            cluster.is_fired = False
            if cluster.last_fired == None:
                if cluster.current_signal >= cluster.threshold:
                    cluster.is_fired = True
                    cluster.last_fired = datetime.now()
                    self.activation_map[cluster.type] = cluster.current_signal

            else:
                time_since_fired = datetime.now() - cluster.last_fired
                seconds_since_fired = time_since_fired.total_seconds()
                if cluster.current_signal >= cluster.threshold and seconds_since_fired > cluster.refractory_timer:
                    cluster.is_fired = True
                    cluster.last_fired = datetime.now()
                    self.activation_map[cluster.type] = cluster.current_signal
        
        for cluster in self.clusters.values():
            self.Full_activation_map[cluster.type] = cluster.current_signal
    
        return self.activation_map 
    
    def hebbian_strengthening(self):
        for source in self.activation_map:
            for target in self.clusters.keys():
                if(source != target):
                    synaptic = self.synaptic_weights[(source, target)]
                    if target in self.activation_map:
                        synaptic.co_activation_count += 1
                        synaptic.streak += 1
                    else:
                        synaptic.streak = max(0, synaptic.streak - 1)
                        continue
                    
                    required_streak = max(1, int(5 * (1 - synaptic.weight)))
                    if(synaptic.streak >= required_streak):
                        synaptic.weight +=  self.LEARNING_RATE * (1 - synaptic.weight)
                        self.synaptic_weights[(source, target)].weight = min(synaptic.weight, 1)
                        synaptic.last_strengthened = self.mind_time.now()
                        synaptic.streak = 0

    def hebbian_decay(self):
        now = self.mind_time.now()

        for synaptic in self.synaptic_weights.values():
            if(synaptic.last_strengthened == None):
                continue

            days_threshold = 1 + (synaptic.weight * 6)

            if now - synaptic.last_strengthened > timedelta(days=days_threshold):
                count = synaptic.co_activation_count
                effective_decay = synaptic.decay / (1 + count * 0.1)
                synaptic.weight *= (1 - effective_decay)
                synaptic.weight = max(synaptic.weight, 0.0)



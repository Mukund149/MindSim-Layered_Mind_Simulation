from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
from typing import Dict, List, Optional
import uuid
import ast
import json
import math
import chromadb



@dataclass
class Memory:
    id: str
    stimulusSummary: str
    responseSummary: str
    stimulusVector: List[float]
    emotionMap: Dict[str, float]
    initialEmotionalWeight: float
    createdAt: datetime
    recallHistory: List[datetime] = field(default_factory=list)
    emotionContext: str = ""
    temporalLinks: Dict[str, float] = field(default_factory=dict)
    semanticLinks: Dict[str, float] = field(default_factory=dict)
    emotionalLinks: Dict[str, float] = field(default_factory=dict)



class MemoryLayer:

    MIN_DECAY_PARAMETER = 0.3
    MAX_DECAY_PARAMETER = 0.7

    ACTIVE_EMOTION_THRESHOLD = 0.1
    COMPOUND_BONUS           = 0.08
    COMPLEXITY_CAP           = 0.20

    SEMANTIC_CANDIDATE_LIMIT  = 30
    EMOTIONAL_CANDIDATE_LIMIT = 30

    SEMANTIC_CANDIDATE_THRESHOLD   = 0.5
    RETRIEVAL_ACTIVATION_THRESHOLD = 0.5

    LOW_MEDIUM_THRESHOLD  = 0.33
    MEDIUM_HIGH_THRESHOLD = 0.66

    LOW_BUCKET_VALUE    = 0.15
    MEDIUM_BUCKET_VALUE = 0.5
    HIGH_BUCKET_VALUE   = 1.0

    EMOTION_CONTEXT_SIMILARITY_THRESHOLD = 0.85

    TEMPORAL_HALF_LIFE = 30
    MINIMUM_TEMPORAL_LINK_STRENGTH = 0.1

    MIN_ELAPSED_DAYS_EPSILON = 1e-6

    LATENCY_FACTOR = 0.3

    MAX_CONTEXT_WINDOW = 5

    def __init__(self, mindState):
        self.mindState = mindState
        self.contextWindow = deque(maxlen=self.MAX_CONTEXT_WINDOW)

        self.emotionOrder = sorted(mindState.emotional_state["base"].keys())

        self.temporalDecayRate = math.log(2) / self.TEMPORAL_HALF_LIFE

        self.temporalWindowMinutes = math.log(1 / self.MINIMUM_TEMPORAL_LINK_STRENGTH) / self.temporalDecayRate

        self.chromaClient = chromadb.HttpClient(host="localhost", port=8000)

        self.collection = self.chromaClient.get_or_create_collection(
            name="mindsim_memories",
            metadata={"hnsw:space": "cosine"}
        )

        self.contextBoxes: Dict[str, List[str]] = self.loadContextBoxes()

        print(f"ChromaDB Ready | Memories: {self.collection.count()} | Emotion boxes: {len(self.contextBoxes)}")


    # ═════════════════════════════════════════════════════════════════════════
    # STORAGE
    # ═════════════════════════════════════════════════════════════════════════

    def createMemory(
        self,
        stimulusSummary: str,
        responseSummary: str,
    ) -> Memory:

        stimulusVector = self.mindState.stimulus_vector.tolist()
        emotionSnapshot = self.snapshotEmotionMap()
        initialEmotionalWeight = self.calculateEmotionalWeight()
        emotionContext = self.computeEmotionContext(emotionSnapshot)

        memory = Memory(
            id=str(uuid.uuid4()),
            stimulusSummary=stimulusSummary,
            responseSummary=responseSummary,
            stimulusVector=stimulusVector,
            emotionMap=emotionSnapshot,
            initialEmotionalWeight=initialEmotionalWeight,
            createdAt=datetime.now(),
            recallHistory=[],
            emotionContext=emotionContext,
        )

        self.collection.add(
            ids=[memory.id],
            embeddings=[memory.stimulusVector],
            metadatas=[{
                "stimulusSummary":         memory.stimulusSummary,
                "responseSummary":         memory.responseSummary,
                "initialEmotionalWeight": memory.initialEmotionalWeight,
                "createdAt":               memory.createdAt.isoformat(),
                "createdAtEpoch":         memory.createdAt.timestamp(),
                "recallHistory":           json.dumps([]),
                "emotionMap":              str(emotionSnapshot),
                "emotionContext":          memory.emotionContext,
                "temporalLinks":           json.dumps({}),
                "semanticLinks":           json.dumps({}),
                "emotionalLinks":          json.dumps({}),
            }]
        )

        self.establishLinksForNewMemory(memory)
        self.registerMemoryInContextBox(memory.id, memory.emotionContext)

        print(
            f"Memory stored | "
            f"weight: {memory.initialEmotionalWeight:.2f} | "
            f"context: {memory.emotionContext} | "
            f"'{memory.stimulusSummary}'"
        )

        return memory


    def establishLinksForNewMemory(self, memory: Memory):
        temporalNeighbors  = self.getTemporalCandidates(memory.createdAt, excludeId=memory.id)
        semanticNeighbors  = self.getSemanticLinkCandidates(memory.id, memory.stimulusVector)
        emotionalNeighbors = self.getEmotionalCandidates(memory.emotionMap)
        emotionalNeighbors.pop(memory.id, None)   # a memory always matches its own box perfectly — exclude that trivial hit

        self.writeLinkPair(memory.id, temporalNeighbors, "temporalLinks")
        self.writeLinkPair(memory.id, semanticNeighbors, "semanticLinks")
        self.writeLinkPair(memory.id, emotionalNeighbors, "emotionalLinks")


    def writeLinkPair(self, newMemoryId: str, neighbors: Dict[str, float], fieldName: str):
        if not neighbors:
            return

        newMemoryMetadata = self.fetchMemoryById(newMemoryId)
        newMemoryLinks = json.loads(newMemoryMetadata[fieldName])

        for neighborId, strength in neighbors.items():
            newMemoryLinks[neighborId] = strength

            neighborMetadata = self.fetchMemoryById(neighborId)
            if neighborMetadata is None:
                continue
            neighborLinks = json.loads(neighborMetadata[fieldName])
            neighborLinks[newMemoryId] = strength   # undirected — write the same strength on the other side too
            self.collection.update(
                ids=[neighborId],
                metadatas=[{**neighborMetadata, fieldName: json.dumps(neighborLinks)}]
            )

        self.collection.update(
            ids=[newMemoryId],
            metadatas=[{**newMemoryMetadata, fieldName: json.dumps(newMemoryLinks)}]
        )


    def updateContextWindow(self, stimulus: str, response: str):
        self.contextWindow.append({
            "stimulus":  stimulus,
            "response":  response,
            "timestamp": datetime.now()
        })


    def snapshotEmotionMap(self) -> Dict[str, float]:
        snapshot = {}
        for emotion, data in self.mindState.emotional_state["base"].items():
            snapshot[emotion] = data["value"]
        for compound, value in self.mindState.emotional_state["compounds"].items():
            snapshot[compound] = value
        return snapshot


    def calculateEmotionalWeight(self) -> float:
        baseValues = [
            data["value"]
            for data in self.mindState.emotional_state["base"].values()
        ]
        compoundValues = list(
            self.mindState.emotional_state["compounds"].values()
        )
        allValues = baseValues + compoundValues

        if not allValues:
            return 0.0

        peak = max(allValues)
        activeEmotions = [v for v in baseValues if v >= self.ACTIVE_EMOTION_THRESHOLD]
        activeAverage = (sum(activeEmotions) / len(activeEmotions)) if activeEmotions else 0.0
        complexity = min(len(compoundValues) * self.COMPOUND_BONUS, self.COMPLEXITY_CAP)

        emotionalWeight = (peak * 0.65) + (activeAverage * 0.25) + complexity
        return max(0.0, min(emotionalWeight, 1.0))


    def memoryFromMetadata(self, memoryId: str, metadata: dict) -> Memory:
        return Memory(
            id=memoryId,
            stimulusSummary=metadata["stimulusSummary"],
            responseSummary=metadata["responseSummary"],
            stimulusVector=[],
            emotionMap=ast.literal_eval(metadata["emotionMap"]),
            initialEmotionalWeight=metadata["initialEmotionalWeight"],
            createdAt=datetime.fromisoformat(metadata["createdAt"]),
            recallHistory=[datetime.fromisoformat(t) for t in json.loads(metadata["recallHistory"])],
            emotionContext=metadata.get("emotionContext", ""),
            temporalLinks=json.loads(metadata.get("temporalLinks", "{}")),
            semanticLinks=json.loads(metadata.get("semanticLinks", "{}")),
            emotionalLinks=json.loads(metadata.get("emotionalLinks", "{}")),
        )


    def fetchMemoryById(self, memoryId: str):
        result = self.collection.get(ids=[memoryId])
        if result["ids"]:
            return result["metadatas"][0]
        return None


    # ═════════════════════════════════════════════════════════════════════════
    # CANDIDATE GENERATION
    # ═════════════════════════════════════════════════════════════════════════

    def getSemanticCandidates(self, stimulusVector) -> Dict[str, dict]:
        candidates = {}

        if self.collection.count() == 0:
            return candidates

        results = self.collection.query(
            query_embeddings=[stimulusVector],
            n_results=min(self.SEMANTIC_CANDIDATE_LIMIT, self.collection.count())
        )

        ids       = results["ids"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for id_, metadata, distance in zip(ids, metadatas, distances):
            similarity = 1 - distance
            if similarity < self.SEMANTIC_CANDIDATE_THRESHOLD:
                continue
            candidates[id_] = {
                "memory":            self.memoryFromMetadata(id_, metadata),
                "semanticRelevance": similarity,
            }

        return candidates


    # ═════════════════════════════════════════════════════════════════════════
    # SEMANTIC LINKING (memory-to-memory)
    # ═════════════════════════════════════════════════════════════════════════

    def getSemanticLinkCandidates(self, memoryId: str, stimulusVector: List[float]) -> Dict[str, float]:
        candidates: Dict[str, float] = {}

        if self.collection.count() == 0:
            return candidates

        results = self.collection.query(
            query_embeddings=[stimulusVector],
            n_results=min(self.SEMANTIC_CANDIDATE_LIMIT, self.collection.count())
        )

        ids       = results["ids"][0]
        distances = results["distances"][0]

        for id_, distance in zip(ids, distances):
            if id_ == memoryId:
                continue
            similarity = 1 - distance
            if similarity < self.SEMANTIC_CANDIDATE_THRESHOLD:
                continue
            candidates[id_] = similarity

        return candidates


    def calculateTemporalSpread(self, memory: Memory) -> float:
        return sum(memory.temporalLinks.values())


    def calculateSemanticSpread(self, memory: Memory) -> float:
        return sum(memory.semanticLinks.values())


    def calculateEmotionalSpread(self, memory: Memory) -> float:
        return sum(memory.emotionalLinks.values())



    def bucketLetter(self, value: float) -> str:
        if value < self.LOW_MEDIUM_THRESHOLD:
            return "L"
        elif value < self.MEDIUM_HIGH_THRESHOLD:
            return "M"
        else:
            return "H"


    def computeEmotionContext(self, emotionMap: Dict[str, float]) -> str:
        return "".join(self.bucketLetter(emotionMap.get(name, 0.0)) for name in self.emotionOrder)


    def contextToVector(self, context: str) -> List[float]:
        bucketValues = {"L": self.LOW_BUCKET_VALUE, "M": self.MEDIUM_BUCKET_VALUE, "H": self.HIGH_BUCKET_VALUE}
        return [bucketValues[letter] for letter in context]


    def cosineSimilarity(self, vectorA: List[float], vectorB: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vectorA, vectorB))
        magnitudeA = math.sqrt(sum(a * a for a in vectorA))
        magnitudeB = math.sqrt(sum(b * b for b in vectorB))
        if magnitudeA == 0 or magnitudeB == 0:
            return 0.0
        return dot / (magnitudeA * magnitudeB)


    def loadContextBoxes(self) -> Dict[str, List[str]]:
        boxes: Dict[str, List[str]] = {}
        if self.collection.count() == 0:
            return boxes
        records = self.collection.get()
        for memoryId, metadata in zip(records["ids"], records["metadatas"]):
            context = metadata.get("emotionContext", "")
            if not context:
                continue
            boxes.setdefault(context, []).append(memoryId)
        return boxes


    def registerMemoryInContextBox(self, memoryId: str, context: str):
        if not context:
            return
        self.contextBoxes.setdefault(context, []).append(memoryId)


    def getPatternInfo(self, context: str) -> dict:
        memberIds = self.contextBoxes.get(context, [])
        return {
            "signature": context,
            "memoryIds": list(memberIds),
            "count": len(memberIds),
        }


    def getEmotionalCandidates(self, currentEmotionMap: Dict[str, float]) -> Dict[str, float]:
        stimulusContext = self.computeEmotionContext(currentEmotionMap)
        stimulusVector = self.contextToVector(stimulusContext)

        candidates: Dict[str, float] = {}
        for context, memberIds in self.contextBoxes.items():
            similarity = self.cosineSimilarity(stimulusVector, self.contextToVector(context))
            if similarity < self.EMOTION_CONTEXT_SIMILARITY_THRESHOLD:
                continue

            for memoryId in memberIds:
                candidates[memoryId] = similarity

        topCandidates = sorted(candidates.items(), key=lambda pair: pair[1], reverse=True)[:self.EMOTIONAL_CANDIDATE_LIMIT]
        return dict(topCandidates)


    # ═════════════════════════════════════════════════════════════════════════
    # TEMPORAL LINKING
    # ═════════════════════════════════════════════════════════════════════════

    def calculateTemporalLinkStrength(self, deltaMinutes: float) -> float:
        return math.exp(-self.temporalDecayRate * deltaMinutes)


    def getTemporalCandidates(self, referenceTime: datetime, excludeId: Optional[str] = None) -> Dict[str, float]:
        referenceEpoch = referenceTime.timestamp()
        windowSeconds = self.temporalWindowMinutes * 60

        candidates: Dict[str, float] = {}
        if self.collection.count() == 0:
            return candidates

        results = self.collection.get(
            where={
                "$and": [
                    {"createdAtEpoch": {"$gte": referenceEpoch - windowSeconds}},
                    {"createdAtEpoch": {"$lte": referenceEpoch + windowSeconds}},
                ]
            }
        )

        for memoryId, metadata in zip(results["ids"], results["metadatas"]):
            if memoryId == excludeId:
                continue
            deltaMinutes = abs(referenceEpoch - metadata["createdAtEpoch"]) / 60
            strength = self.calculateTemporalLinkStrength(deltaMinutes)
            if strength >= self.MINIMUM_TEMPORAL_LINK_STRENGTH:
                candidates[memoryId] = strength

        return candidates


    def mergeCandidates(self, semanticCandidates: Dict[str, dict], emotionalCandidates: Dict[str, float]) -> Dict[str, dict]:
        merged = {}

        for memoryId, info in semanticCandidates.items():
            merged[memoryId] = {
                "memory":              info["memory"],
                "semanticRelevance":  info["semanticRelevance"],
                "emotionalRelevance": 0.0,
            }

        for memoryId, linkStrength in emotionalCandidates.items():
            if memoryId in merged:
                merged[memoryId]["emotionalRelevance"] = linkStrength
            else:
                metadata = self.fetchMemoryById(memoryId)
                if metadata is None:
                    continue
                merged[memoryId] = {
                    "memory":              self.memoryFromMetadata(memoryId, metadata),
                    "semanticRelevance":  0.0,
                    "emotionalRelevance": linkStrength,
                }

        return merged


    # ═════════════════════════════════════════════════════════════════════════
    # RELEVANCE
    # ═════════════════════════════════════════════════════════════════════════

    def calculateUnifiedRelevance(self, semanticRelevance: float, emotionalRelevance: float) -> float:
        return semanticRelevance + emotionalRelevance - (semanticRelevance * emotionalRelevance)


    # ═════════════════════════════════════════════════════════════════════════
    # ACCESSIBILITY (Base-Level Activation)
    # ═════════════════════════════════════════════════════════════════════════

    def calculateDecayParameter(self, emotionalWeight: float) -> float:
        d = 0.5 - 0.2 * ((2 * emotionalWeight - 1) ** 3)
        return max(self.MIN_DECAY_PARAMETER, min(d, self.MAX_DECAY_PARAMETER))


    def calculateBla(self, memory: Memory, currentTime: datetime) -> float:
        dI = self.calculateDecayParameter(memory.initialEmotionalWeight)
        referencePoints = [memory.createdAt] + memory.recallHistory

        total = 0.0
        for referenceTime in referencePoints:
            elapsedDays = (currentTime - referenceTime).total_seconds() / 86400
            elapsedDays = max(elapsedDays, self.MIN_ELAPSED_DAYS_EPSILON)
            total += elapsedDays ** (-dI)

        return math.log(total)


    # ═════════════════════════════════════════════════════════════════════════
    # RETRIEVAL
    # ═════════════════════════════════════════════════════════════════════════

    def calculateRetrievalActivation(
        self,
        unifiedRelevance: float,
        bla: float,
        spreadTemporal: float = 0.0,
        spreadSemantic: float = 0.0,
        spreadEmotional: float = 0.0,
    ) -> float:
        return unifiedRelevance + bla + spreadTemporal + spreadSemantic + spreadEmotional


    def passesRetrievalCriterion(self, activation: float) -> bool:
        return activation >= self.RETRIEVAL_ACTIVATION_THRESHOLD


    def calculateRetrievalLatency(self, activation: float) -> float:
        return self.LATENCY_FACTOR * math.exp(-activation)


    def retrieveMemories(self, stimulusVector, currentTime: Optional[datetime] = None) -> Dict[str, list]:
        if currentTime is None:
            currentTime = datetime.now()

        stimulusVector = stimulusVector.tolist() if hasattr(stimulusVector, "tolist") else stimulusVector

        semanticCandidates  = self.getSemanticCandidates(stimulusVector)
        emotionalCandidates = self.getEmotionalCandidates(self.snapshotEmotionMap())

        merged = self.mergeCandidates(semanticCandidates, emotionalCandidates)

        successes = []
        for memoryId, candidate in merged.items():
            unifiedRelevance = self.calculateUnifiedRelevance(
                candidate["semanticRelevance"], candidate["emotionalRelevance"]
            )

            memory = candidate["memory"]
            bla = self.calculateBla(memory, currentTime)
            spreadTemporal = self.calculateTemporalSpread(memory)
            spreadSemantic = self.calculateSemanticSpread(memory)
            spreadEmotional = self.calculateEmotionalSpread(memory)

            activation = self.calculateRetrievalActivation(
                unifiedRelevance, bla, spreadTemporal, spreadSemantic, spreadEmotional
            )
            if not self.passesRetrievalCriterion(activation):
                continue

            latency = self.calculateRetrievalLatency(activation)
            self.recordSuccessfulRecall(candidate, memoryId, currentTime)

            successes.append(self.formatOutput(
                memoryId, candidate, candidate["semanticRelevance"], candidate["emotionalRelevance"],
                bla, spreadTemporal, spreadSemantic, spreadEmotional, activation, latency
            ))

        recalledIds = {memory["id"] for memory in successes}
        associative = self.expandViaMemoryLinks(recalledIds, currentTime)

        result = {
            "recalled": successes,
            "associativelyActivated": associative,
        }

        self.mindState.working_memory = result
        self.mindState.memory_activation_map = {
            memory["id"]: memory["retrievalActivation"] for memory in successes
        }

        return result


    def expandViaMemoryLinks(self, recalledIds: set, currentTime: datetime) -> List[dict]:
        linkedVia: Dict[str, List[dict]] = {}

        for sourceId in recalledIds:
            sourceMetadata = self.fetchMemoryById(sourceId)
            sourceMemory = self.memoryFromMetadata(sourceId, sourceMetadata)

            for linkType, neighbors in [
                ("temporal", sourceMemory.temporalLinks),
                ("semantic", sourceMemory.semanticLinks),
                ("emotional", sourceMemory.emotionalLinks),
            ]:
                for neighborId, strength in neighbors.items():
                    if neighborId in recalledIds:
                        continue   
                    linkedVia.setdefault(neighborId, []).append(
                        {"sourceMemoryId": sourceId, "linkType": linkType, "strength": strength}
                    )

        associativeOutput = []
        for neighborId, links in linkedVia.items():
            metadata = self.fetchMemoryById(neighborId)
            memory = self.memoryFromMetadata(neighborId, metadata)

            memory.recallHistory.append(currentTime)
            self.persistRecall(memory)

            associativeOutput.append({
                "id":               neighborId,
                "stimulusSummary": memory.stimulusSummary,
                "responseSummary": memory.responseSummary,
                "emotionMap":      memory.emotionMap,
                "linkedVia":       links,
            })

        return associativeOutput


    # ═════════════════════════════════════════════════════════════════════════
    # RECALL UPDATE
    # ═════════════════════════════════════════════════════════════════════════

    def persistRecall(self, memory: Memory):
        self.collection.update(
            ids=[memory.id],
            metadatas=[{
                "stimulusSummary":         memory.stimulusSummary,
                "responseSummary":         memory.responseSummary,
                "initialEmotionalWeight": memory.initialEmotionalWeight,
                "createdAt":               memory.createdAt.isoformat(),
                "createdAtEpoch":         memory.createdAt.timestamp(),
                "recallHistory":           json.dumps([t.isoformat() for t in memory.recallHistory]),
                "emotionMap":              str(memory.emotionMap),
                "emotionContext":          memory.emotionContext,
                "temporalLinks":           json.dumps(memory.temporalLinks),
                "semanticLinks":           json.dumps(memory.semanticLinks),
                "emotionalLinks":          json.dumps(memory.emotionalLinks),
            }]
        )


    def recordSuccessfulRecall(self, candidate: dict, memoryId: str, currentTime: datetime):
        memory = candidate["memory"]
        memory.recallHistory.append(currentTime)
        self.persistRecall(memory)


    def formatOutput(
        self,
        memoryId: str,
        candidate: dict,
        semanticRelevance: float,
        emotionalRelevance: float,
        bla: float,
        spreadTemporal: float,
        spreadSemantic: float,
        spreadEmotional: float,
        activation: float,
        latency: float,
    ) -> dict:
        memory = candidate["memory"]
        return {
            "id":                   memoryId,
            "stimulusSummary":     memory.stimulusSummary,
            "responseSummary":     memory.responseSummary,
            "emotionMap":          memory.emotionMap,
            "semanticRelevance":   semanticRelevance,
            "emotionalRelevance":  emotionalRelevance,
            "baseLevelActivation": bla,
            "temporal_spread_activation": spreadTemporal,
            "semanticSpreadActivation": spreadSemantic,
            "emotionalSpreadActivation": spreadEmotional,
            "retrievalActivation":  activation,
            "retrievalLatency":     latency,
        }
from sentence_transformers import SentenceTransformer
from config.Clusters import CLUSTER_REFERENCES

model = SentenceTransformer('all-mpnet-base-v2')

REFERENCE_VECTORS = {}
for cluster, ref in CLUSTER_REFERENCES.items():
    REFERENCE_VECTORS[cluster] = model.encode(ref)


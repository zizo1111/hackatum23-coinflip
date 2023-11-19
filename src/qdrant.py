from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct

class Qdrant:

    def __init__(self) -> None:
        self.client  = QdrantClient(":memory:")
        self.create_collection()
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def create_collection(self, name='my_collection'):
         self.client.create_collection(name, vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE) )
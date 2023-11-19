from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct

class Qdrant:

    def __init__(self) -> None:
        self.client  = QdrantClient(":memory:")
        self.create_collection("my_collection")
        self.create_collection("second_coll")        
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def create_collection(self, name):
         self.client.create_collection(name, vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE) )


    def calculate_embeddings(self,data,max_lines, chunk_size):
        """
        This method gets an array of strings and returns an array of the vectors embeddings of this strings
        """
        to_encode = self.chunk(data,max_lines, chunk_size)
        embeddings = self.model.encode(to_encode)
        return embeddings
    
    def populate_qdrant(self, collection_name, embeddings):
        """
        This method populates a qdrant collection
        it recieves a collection_name
        The embeddings and the data in order to keep track of the original line
        """
        self.client.upsert(
                    collection_name,
            points=[
                PointStruct(
                        id=idx,
                        vector=vector.tolist(),
                        payload={"line_id": idx}
                )
            for idx, vector in enumerate(embeddings)
        ]
        )

    def search_collection(self,collection_name,query_vector,limit):
        """
        Searches the Qdrant database for the most similiar
        Return the limit most top hits with the highest similarity
        """
        hits = self.client.search(
            collection_name,
            query_vector,
            limit=limit
        )
        return hits
    
    def chunk(self, data , max_lines, chunk_size):
        if max_lines == 0:
            return data
        all_chunks = []
        for i in range(0, max_lines, chunk_size):
            chunked_str = " ;;; ".join(data[i:i+chunk_size])
            all_chunks.append(chunked_str)
        self.chunks = all_chunks
        return all_chunks

    
    # create the embeddings
    def search_vector(self,query_vector,hit,messages):
        idx = hit.id
        embeddings = self.calculate_embeddings(messages[idx:idx+100],0,0)
        self.populate_qdrant("second_coll", embeddings=embeddings)
        """
        Searches the Qdrant database for the most similiar
        Return the limit most top hits with the highest similarity
        """
        hits = self.client.search(
            "second_coll",
            query_vector,
            limit=10
        )
        return hits
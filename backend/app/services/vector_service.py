from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

class VectorDatabase:
    def __init__(self):
        # 1. Load the Embedding Model (same as our sandbox lesson!)
        print("Loading Embedding Model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 2. Initialize Qdrant (saving to a local folder in the backend)
        self.collection_name = "financial_documents"
        self.client = QdrantClient(path="vector_db_data")
        
        # 3. Create the collection if it doesn't exist
        # 384 is the exact number of dimensions our 'all-MiniLM-L6-v2' model outputs
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
            print(f"Created Qdrant collection: {self.collection_name}")

    def store_chunks(self, chunks: list[str], filename: str) -> int:
        """
        Takes a list of text chunks, converts them to vectors, 
        and saves them into the Qdrant database.
        """
        if not chunks:
            return 0
            
        print(f"Converting {len(chunks)} chunks into vectors...")
        # Convert all chunks into GPS coordinates (Embeddings)
        embeddings = self.model.encode(chunks)
        
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Each piece of data needs a unique ID, the vector, and the original text (payload)
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "filename": filename,
                    "chunk_index": i,
                    "text": chunk
                }
            )
            points.append(point)
            
        # Upsert (insert or update) the points into Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"Successfully stored {len(points)} vectors in Qdrant!")
        
        return len(points)

# Create a single instance to be used by our API
vector_db = VectorDatabase()

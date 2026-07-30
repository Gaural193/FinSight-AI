"""
Lesson 1: Vector Embeddings & Semantic Similarity
-------------------------------------------------
In this experiment, we will see how AI converts words into numbers (embeddings)
and how we can use math (cosine similarity) to determine if two sentences have
the same meaning, even if they use different words.

Prerequisites:
pip install sentence-transformers numpy
"""

from sentence_transformers import SentenceTransformer
import numpy as np

# 1. Load a pre-trained embedding model.
# 'all-MiniLM-L6-v2' is a small, fast model perfect for learning.
print("Loading AI Model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Define our sentences
sentences = [
    "The company's revenue grew by 10 percent this year.", # Sentence 0
    "Sales increased by ten percent over the last 12 months.", # Sentence 1 (Semantically similar to 0)
    "The new smartphone model has a better battery life." # Sentence 2 (Completely unrelated)
]

# 3. Convert sentences into mathematical vectors (Embeddings)
print("\nGenerating Embeddings (converting text to numbers)...")
embeddings = model.encode(sentences)

print(f"\nEach sentence is now a vector of {len(embeddings[0])} numbers!")
print(f"Here are the first 5 numbers of Sentence 0's vector: {embeddings[0][:5]}")

# 4. Calculate Cosine Similarity
# Cosine similarity measures the angle between two vectors.
# 1.0 means identical, 0.0 means orthogonal (unrelated), -1.0 means opposite.

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# Compare Sentence 0 and Sentence 1 (Should be high similarity)
sim_0_1 = cosine_similarity(embeddings[0], embeddings[1])

# Compare Sentence 0 and Sentence 2 (Should be low similarity)
sim_0_2 = cosine_similarity(embeddings[0], embeddings[2])

print("\n--- RESULTS ---")
print(f"Similarity between '{sentences[0][:20]}...' AND '{sentences[1][:20]}...':")
print(f"Score: {sim_0_1:.4f} (High similarity means the AI understands they mean the same thing!)")

print(f"\nSimilarity between '{sentences[0][:20]}...' AND '{sentences[2][:20]}...':")
print(f"Score: {sim_0_2:.4f} (Low similarity means they are unrelated topics)")

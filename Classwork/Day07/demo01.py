from sentence_transformers import SentenceTransformer
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b)/(np.linalg.norm(a) * np.linalg.norm(b))


embed_model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = [
    "I love football.",
    "Soccer is my favorite sports.",
    "Messi talks spanish."
]

embedding = embed_model.encode(sentences)

for i in embedding:
    print("Len", len(i),"------->",i[:3])

print("Sentence 1 & 2 ", cosine_similarity(embedding[0] , embedding[1]))
print("Sentence 1 & 3 ", cosine_similarity(embedding[0], embedding[2]))
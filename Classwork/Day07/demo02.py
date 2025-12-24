from langchain_openai import OpenAIEmbeddings
import numpy as np

def cosine_similarity(a,b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))

embed_model = OpenAIEmbeddings(
    model = "text-embedding-nomic-embed-text-v1.5",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy-token",
    check_embedding_ctx_length=False
)

sentences = [
    "I love Football",
    "Soccer is my favourite sports",
    "Messi talks spanish"
]

embeddings = embed_model.embed_documents(sentences)

for i in embeddings:
    print("Len : ", len(i), "------>" , i[:4])

print("Sentence 1 & 2 similarity: ", cosine_similarity(embeddings[0],embeddings[1]))
print("Sentence 1 & 3 similarity: ", cosine_similarity(embeddings[0],embeddings[2]))
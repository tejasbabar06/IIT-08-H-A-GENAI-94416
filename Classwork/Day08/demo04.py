import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain.embeddings import init_embeddings
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent


text = [
    """Artificial Intelligence is a field of computer science that focuses on 
creating machines capable of performing tasks that require human intelligence.
Examples include speech recognition, image processing, and decision making.


Retrieval Augmented Generation, also known as RAG, is a technique that improves
language model responses by retrieving relevant documents from a vector database
and using them as context for answer generation.



ChromaDB is a vector database used to store and search embeddings.
It enables fast similarity search and is commonly used in RAG applications.
ChromaDB works well with local and cloud-based language models.


Embeddings are numerical representations of text.
They capture the semantic meaning of sentences and paragraphs.
Similar texts have embeddings that are close to each other in vector space.


Chunking is the process of splitting large documents into smaller parts.
Chunking helps improve retrieval accuracy and ensures that only relevant
information is passed to the language model.
"""
]


text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50, separators=[" ", "\n", "\n\n"])
docs = text_splitter.create_documents(text)

# for i in docs:
#     print(i.page_content,"\n")
texts = [doc.page_content for doc in docs]

embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="Dummy-key",
    check_embedding_ctx_length = False
)
#print(type(docs))
embeddings = embed_model.embed_documents(texts)

# for i in embeddings:
#     print(i[:3])

db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("embeddings")
ids = [f"chunk_{i}" for i in range(len(texts))]
collection.add(
    ids=ids,
    documents=texts,
    embeddings=embeddings
)

user_input = input("Entre your question : ")

query_embedding = embed_model.embed_query(user_input)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

out_put = "\n".join(results["documents"][0])


llm = init_chat_model(
    model="google/gemma-3n-e4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key = "Dummy-api"
)

agent = create_agent(
    tools=[],
    model=llm,
    system_prompt=f"""
Answer ONLY using the information below.
If the answer is not present, say "I don't know".

Context:
{out_put}

Question:
{user_input}

Answer (point-wise, short):
"""

)
prompt = f"""
Answer ONLY using the information below.
If the answer is not present, say "I don't know".

Context:
{out_put}

Question:
{user_input}

Answer (point-wise, short):
"""

conversation = [
    {"role": "system", "content": "You are a professional teacher."},
    {"role": "user", "content": prompt}
]

result = agent.invoke({"messages":conversation})
print(result["messages"][-1].content)



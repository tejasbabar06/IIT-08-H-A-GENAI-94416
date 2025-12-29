import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain.embeddings import init_embeddings
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
import os


loader = DirectoryLoader(
    path=r"C:\Users\TEJAS BABAR\Downloads\fake-resumes",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

documents = loader.load()
docs = documents


ids = []
texts = []

for doc in docs:
    file_name = os.path.splitext(os.path.basename(doc.metadata["source"]))[0]
    page_no = doc.metadata.get("page", 0)

    doc_id = f"{file_name}_page_{page_no}"
    doc.metadata["doc_id"] = doc_id

    ids.append(doc_id)
    texts.append(doc.page_content)


embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="Dummy-key",
    check_embedding_ctx_length=False
)
embeddings = embed_model.embed_documents(texts)
db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("embeddings")
collection.add(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=[doc.metadata for doc in docs]
)
user_input = input("Enter your question: ")
query_embedding = embed_model.embed_query(user_input)
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

context = "\n\n".join(results["documents"][0])
llm = init_chat_model(
    model="google/gemma-3n-e4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="Dummy-api"
)

agent = create_agent(
    tools=[],
    model=llm,
    system_prompt=f"""
You are a resume screening expert.

From the resumes below, select the ONE BEST resume
based on the user question.

Explain briefly why you selected it.

Resumes:
{context}

Question:
{user_input}

Answer (point-wise, short):
"""
)
conversation = [
    {"role": "user", "content": user_input}
]
result = agent.invoke({"messages": conversation})
print(result["messages"][-1].content)

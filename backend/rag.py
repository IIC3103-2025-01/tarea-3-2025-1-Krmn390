# rag.py

import requests
import logging
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from my_config import (
    db_user, db_password, db_database, db_host, db_port,
    EMBEDDING_API_URL, embedding_model
)

# 🚀 API de embeddings proporcionada por la tarea
def generate_embedding(text):
    response = requests.post(
        EMBEDDING_API_URL,
        json={"model": embedding_model, "input": text}
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]

# 🚀 Splitter para dividir el texto en chunks
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,      # tamaño en tokens
        chunk_overlap=50,    # solapamiento
        separators=["\n", "."]
    )
    res = splitter.split_text(text)
    return res

# 🚀 Wrapper que cumple la interfaz esperada por PGVector
class EmbeddingFunction:
    def __init__(self):
        self.api_url = EMBEDDING_API_URL
        self.model = embedding_model

    def embed_query(self, text):
        response = requests.post(self.api_url, json={
            "model": self.model,
            "input": text
        })
        response.raise_for_status()
        return response.json()["embeddings"][0]

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = requests.post(self.api_url, json={
                "model": self.model,
                "input": text
            })
            response.raise_for_status()
            embeddings.append(response.json()["embeddings"][0])
        return embeddings

# 🚀 Guardar embeddings en Postgres
def store_embeddings(chunks, collection_name="wikipedia_articles"):
    embeddings = []
    for chunk in chunks:
        embedding = generate_embedding(chunk)
        embeddings.append((chunk, embedding))

    connection = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
    embedding_function = EmbeddingFunction()

    vectorstore = PGVector(
        collection_name=collection_name,
        connection=connection,
        embeddings=embedding_function,
        use_jsonb=True
    )

    documents = [
        Document(page_content=text, metadata={"id": idx})
        for idx, (text, _) in enumerate(embeddings)
    ]
    embedding_vectors = [emb for _, emb in embeddings]
    texts = [text for text, _ in embeddings]  # ✅ lista de los textos puros

    vectorstore.add_embeddings(
        embeddings=embedding_vectors,
        documents=documents,
        texts=texts,  # ✅ ¡nuevo parámetro!
        ids=[str(i) for i in range(len(documents))]
    )

# 🚀 Buscar documentos relevantes a partir de una query
def similarity_search(query, collection_name="wikipedia_articles", k=5):
    # 1. Genera el embedding de la pregunta
    query_embedding = generate_embedding(query)

    # 2. Conectar a PGVector
    connection = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
    embedding_function = EmbeddingFunction()

    vectorstore = PGVector(
        collection_name=collection_name,
        connection=connection,
        embeddings=embedding_function,   # <-- obligatorio
        use_jsonb=True
    )

    # 3. Realizar la búsqueda por vector
    results = vectorstore.similarity_search_by_vector(query_embedding, k=k)

    # 4. Retorna los textos
    return [doc.page_content for doc in results]

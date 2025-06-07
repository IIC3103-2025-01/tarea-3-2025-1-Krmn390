from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_wikipedia_article  
from langdetect import detect
from llm_client import query_llm
from rag import split_text, store_embeddings, similarity_search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    url: str
    question: str

@app.post("/query")
def query_wikipedia(data: QueryRequest):
    try:
        if not data.url.startswith("https://en.wikipedia.org/wiki/"):
            return {"error": "El artículo debe ser de Wikipedia en inglés (https://en.wikipedia.org/)."}

        # 1. Scrapeo
        text = scrape_wikipedia_article(data.url)
        lang = detect(text)
        if lang != 'en':
            return {"error": "El artículo no está escrito en inglés."}

        # 2. Preprocesamiento: split + embedding + almacenar (idealmente hacerlo una vez y cachearlo)
        chunks = split_text(text)
        store_embeddings(chunks)

        # 3. Recuperar fragmentos relevantes
        relevant_chunks = similarity_search(data.question, k=5)
        context = "\n\n".join(relevant_chunks)

        # 4. Llamar al LLM
        answer = query_llm(context, data.question)

    except Exception as e:
        return {"error": str(e)}

    return {
        "result": answer
    }
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_wikipedia_article  
from langdetect import detect

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
            print("error: El artículo no está escrito en inglés.")
            return {"error": "El artículo debe ser de Wikipedia en inglés (https://en.wikipedia.org/)."}
        text = scrape_wikipedia_article(data.url)
        lang = detect(text)
        if lang != 'en':
            print("error: El artículo no está escrito en inglés.")
            return {"error": "El artículo no está escrito en inglés."}
    except Exception as e:
        return {"error": str(e)}

    return {
        "result": "Artículo scrapeado exitosamente.",
        "text_excerpt": text[:1000] + "..."
    }

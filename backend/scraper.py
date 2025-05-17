import requests
from bs4 import BeautifulSoup
import re

def clean_text(text: str) -> str:
    # Elimina referencias tipo [23]
    text = re.sub(r'\[\d+\]', '', text)
    # Reemplaza múltiples espacios, tabs o saltos de línea por uno solo
    text = re.sub(r'\s+', ' ', text)
    # Elimina caracteres no imprimibles o especiales
    text = text.replace('\xa0', ' ').replace('\n', ' ').strip()
    return text

def scrape_wikipedia_article(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"Error al acceder al artículo: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', {'id': 'mw-content-text'})
    if not content_div:
        raise Exception("No se encontró el contenido principal del artículo.")

    paragraphs = content_div.find_all('p')
    raw_text = '\n'.join(
        [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
    )
    cool_text = clean_text(raw_text)
    print(cool_text)

    return cool_text

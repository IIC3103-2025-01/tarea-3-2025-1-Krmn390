# config.py

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# LLM API Configuración
LLM_API_URL = os.getenv("LLM_API_URL", "https://asteroide.ing.uc.cl/api/chat")
LLM_MODEL = os.getenv("LLM_MODEL", "integracion")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 6))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 512))
LLM_REPEAT_LAST_N = int(os.getenv("LLM_REPEAT_LAST_N", 10))
LLM_TOP_K = int(os.getenv("LLM_TOP_K", 18))
LLM_RATE_LIMIT = int(os.getenv("LLM_RATE_LIMIT", 10))
LLM_RESPONSE_TIME_LIMIT = int(os.getenv("LLM_RESPONSE_TIME_LIMIT", 120))

# Base de Datos (PostgreSQL + PGVector) Configuración

db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
db_database = os.getenv("DB_DATABASE", "postgres")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")


embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL", "https://api.nomic.ai/v1/embed-text")
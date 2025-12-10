from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_firestore_db

app = FastAPI(
    title="Proyecto-Taximetro API",
    description="Backend Nivel Experto con FastAPI y Firebase",
    version="3.0.0"
)

# Configuración CORS (Permitir que el frontend local hable con el backend)
origins = [
    "http://127.0.0.1:5500",  # Live Server de VSCode
    "http://localhost:5500",
    "http://localhost:3000",
    "null"  # Para abrir archivos HTML directamente
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Verificar conexión al iniciar"""
    try:
        get_firestore_db()
        print("✅ Sistema iniciado y conectado a BD")
    except Exception as e:
        print(f"❌ Fallo en inicio: {e}")

@app.get("/")
def read_root():
    return {"status": "online", "system": "Taximetro API"}

@app.get("/health")
def health_check():
    """Endpoint para verificar estado"""
    db = get_firestore_db()
    # Intentar una operación ligera (listar colecciones)
    cols = [col.id for col in db.collections()]
    return {"db_status": "connected", "collections": cols}
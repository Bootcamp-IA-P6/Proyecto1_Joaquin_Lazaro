import os
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Configuración de Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno (útil si decidimos usar .env luego)
load_dotenv()

class FirebaseManager:
    _db = None

    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls._initialize()
        return cls._db

    @classmethod
    def _initialize(cls):
        try:
            # Ruta relativa al archivo json dentro de backend/
            # NOTA: En producción, esto debería ser una variable de entorno con el contenido
            cred_path = "firebase_credentials.json"
            
            if not firebase_admin._apps:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                logger.info("🔥 Firebase App inicializada correctamente.")
            
            cls._db = firestore.client()
            logger.info("💾 Conexión a Firestore establecida.")
            
        except Exception as e:
            logger.critical(f"❌ Error fatal conectando a Firebase: {e}")
            raise e

# Función helper para inyección de dependencias en FastAPI
def get_firestore_db():
    return FirebaseManager.get_db()
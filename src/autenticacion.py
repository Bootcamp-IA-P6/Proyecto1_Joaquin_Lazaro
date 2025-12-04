import hashlib
import json
import secrets
import logging
import os
from typing import Dict, Optional
from src.constantes import ARCHIVO_USUARIOS

class GestorAuth:
    def __init__(self):
        self.usuarios: Dict[str, str] = self._cargar_usuarios()
        self.usuario_actual: Optional[str] = None

    def _cargar_usuarios(self) -> Dict[str, str]:
        if not os.path.exists(ARCHIVO_USUARIOS):
            logging.warning("BD usuarios no encontrada. Iniciando vacía.")
            return {}
        try:
            with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error cargando usuarios: {e}")
            return {}

    def _guardar_usuarios(self) -> bool:
        try:
            with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
                json.dump(self.usuarios, f, indent=4)
            return True
        except IOError as e:
            logging.error(f"Error guardando usuarios: {e}")
            return False

    def _generar_hash(self, password: str, salt: Optional[str] = None) -> str:
        if salt is None:
            salt = secrets.token_hex(16)
        input_str = salt + password
        hash_obj = hashlib.sha256(input_str.encode('utf-8'))
        return f"{salt}${hash_obj.hexdigest()}"

    def registrar_usuario(self, username: str, password: str) -> bool:
        if username in self.usuarios:
            return False
        self.usuarios[username] = self._generar_hash(password)
        return self._guardar_usuarios()

    def login(self, username: str, password: str) -> bool:
        if username not in self.usuarios:
            return False
        
        almacenado = self.usuarios[username]
        try:
            salt, _ = almacenado.split('$')
            check_hash = self._generar_hash(password, salt)
            if secrets.compare_digest(almacenado, check_hash):
                self.usuario_actual = username
                logging.info(f"Login exitoso: {username}")
                return True
        except ValueError:
            logging.error(f"Hash corrupto para usuario {username}")
            
        return False

    def logout(self):
        logging.info(f"Logout: {self.usuario_actual}")
        self.usuario_actual = None
from dotenv import load_dotenv
import os
from supabase import create_client

class ConexionDB:
    def __init__(self):
        load_dotenv()

    def conectar(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_API_KEY")

        if not url or not key:
            raise Exception("Variables de entorno no configuradas")

        return create_client(url, key)

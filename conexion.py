import streamlit as st
from supabase import create_client

class ConexionDB:
    def conectar(self):
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
        except Exception:
            raise Exception("SUPABASE_URL o SUPABASE_KEY no configuradas en Streamlit Secrets")

        return create_client(url, key)

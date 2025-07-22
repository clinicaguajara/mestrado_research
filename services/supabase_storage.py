from datetime import datetime
from supabase import create_client
import streamlit as st

def salvar_respostas_supabase(respostas_dict: dict, aceitou_tcle: bool = True) -> bool:
    """
    Salva respostas do questionário no Supabase (sem login).
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        supabase = create_client(url, key)

        payload = {
            "timestamp": datetime.now().isoformat(),
            "respostas": respostas_dict,
            "aceitou_tcle": aceitou_tcle,
        }

        response = supabase.table("respostas_questionario").insert(payload).execute()

        # ✅ SUPABASE-PY v2: sucesso = presença de dados
        if response.data:
            return True
        else:
            st.error("❌ Erro: Supabase não retornou dados após o insert.")
            return False

    except Exception as e:
        st.error(f"❌ Erro ao salvar no Supabase: {e}")
        return False

import streamlit as st
from modules.componentes import render_questionario_neurociencia
from modules.itens_neurociencia import SOCIODEMOGRAFICO, LPFS_BF, LSM, PID_5_BF, AQ_50
from modules.metadados import metadados_blocos
from services.correcao_escala import corrigir_aq50_estatistico
from services.export import preparar_resultado_exportacao_estatistico
import pandas as pd

# Config da página
st.set_page_config(page_title="Questionário Neurociência", layout="centered")

# Define os blocos do questionário
BLOCOS = {
    "1. Sociodemográfico": SOCIODEMOGRAFICO,
    "2. LPFS-BF": LPFS_BF,
    "3. LSM-21": LSM,
    "4. PID-5-BF": PID_5_BF,
    "5. AQ-50": AQ_50,
}

# Inicializa o estado
if "respostas_enviadas" not in st.session_state:
    st.session_state["respostas_enviadas"] = False
if "respostas" not in st.session_state:
    st.session_state["respostas"] = {}

# Renderiza o formulário apenas se ainda não foi enviado
if not st.session_state["respostas_enviadas"]:
    payload = render_questionario_neurociencia(BLOCOS, metadados_blocos)
    if payload:
        st.session_state["respostas_enviadas"] = True
        st.session_state["respostas"] = payload["respostas"]

# Se o formulário foi enviado, mostra a análise
if st.session_state["respostas_enviadas"]:
    st.success("✅ Respostas recebidas com sucesso.")

    grupo = st.selectbox(
        "Selecione o grupo normativo de referência para correção:",
        [
            "controle_masculino",
            "controle_feminino",
            "autista_masculino",
            "autista_feminino"
        ],
        key="grupo_normativo"
    )

    # Corrige com base no grupo escolhido
    resultado = corrigir_aq50_estatistico(st.session_state["respostas"], grupo=grupo)
    exportavel = preparar_resultado_exportacao_estatistico(resultado)

    # Mostra em tabela
    st.subheader("📊 Correção do AQ-50 (grupo: " + grupo.replace("_", " ").title() + ")")
    df = pd.DataFrame(resultado).T[["escore", "percentil_estimado"]]
    st.dataframe(df, use_container_width=True)

    # Botões de download
    json_bytes = pd.Series(exportavel).to_json(indent=2).encode("utf-8")
    st.download_button("📥 Baixar resultado (JSON)", json_bytes, file_name="resultado_aq50.json", use_container_width=True)

    csv_bytes = pd.DataFrame([exportavel]).to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar resultado (CSV)", csv_bytes, file_name="resultado_aq50.csv", use_container_width=True)

    st.write("**Importante:** percentis não medem “acerto”, mas posição relativa. Eles são úteis para comparar seu resultado com um grupo normativo, como estudantes da mesma área ou idade.")
    st.caption("Um percentil 99 significa que você está no 1\% mais alto.")            
    st.caption("Um percentil 50 indica um desempenho mediano, igual à maioria.")
    st.caption("Um percentil 20 significa que 80\% das pessoas ficaram acima da sua pontuação.")

    st.markdown("Conheça o meu trabalho no [instagram](https://www.instagram.com/clinicaguajara/)")
    st.write("Se houver dúvidas sobre a correção, me coloco à disposição para esclarescer. Lembrando que esse resultado não confere um diagnóstico de autismo, mas permite você comparar o seu resultado com outros cientistas autistas e não autistas.")

    st.info("Baron-Cohen, S., Wheelwright, S., Skinner, R., Martin, J., & Clubley, E. (2001). The autism-spectrum quotient (AQ): Evidence from Asperger syndrome/high-functioning autism, males and females, scientists and mathematicians. Journal of Autism and Developmental Disorders, 31(1), 5–17. https://doi.org/10.1023/A:1005653411471")
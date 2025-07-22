# componentes.py

import streamlit as st
from typing import Dict, List
from services.supabase_storage import salvar_respostas_supabase

def render_questionario_neurociencia(blocos: Dict[str, List[str]], metadados_blocos: Dict[str, dict]) -> dict | None:
    """
    Renderiza um questionário neurocientífico com tipos mistos (Likert, selectbox, campo aberto),
    com validação de campos obrigatórios no bloco sociodemográfico.
    """
    with st.form(key="form_questionario_neuro"):
        respostas_usuario = {}
        contador = 1
        campos_vazios = []

        with st.expander("🧾 TERMO DE CONSENTIMENTO LIVRE E ESCLARECIDO (TCLE)", expanded=False):
            st.markdown("""

            **Pesquisador Responsável:** Pedro Henrique Ramos Pinto  
            **Instituição:** Universidade Federal da Paraíba  
            **Contato:** (67) 99107-1045  

            **1. Apresentação da Pesquisa**  
            Você está sendo convidado(a) a participar desta pesquisa, que tem como objetivo investigar a relação entre características cognitivas e emocionais.  
            Para isso, você responderá a questionários sobre suas experiências e características psicológicas.

            **2. Procedimentos**  
            A pesquisa consiste no preenchimento de uma série de questionários online, com duração estimada de 20 minutos.  
            As perguntas abordarão aspectos relacionados à sua atenção, emoções e experiência cotidiana.  
            Sua participação é voluntária e você pode desistir a qualquer momento, sem necessidade de justificativa.

            **3. Riscos e Benefícios**  
            Embora não existam riscos físicos, alguns participantes podem sentir desconforto emocional ao refletir sobre questões relacionadas à ansiedade, depressão ou experiências pessoais.  
            Caso sinta necessidade, você pode interromper sua participação a qualquer momento.  
            Embora não haja benefícios diretos para você, sua colaboração será essencial para avanços no campo da neurociência e psicologia.

            **4. Confidencialidade**  
            As informações coletadas serão utilizadas exclusivamente para fins acadêmicos e científicos.  
            Os dados serão analisados de forma agregada, sem qualquer identificação pessoal.  
            No final do processo, o banco de dados dessa pesquisa será publicado.  
            Entretanto, todas as medidas de segurança serão adotadas para garantir sua privacidade e anonimato.
            """)


        for nome_bloco, itens in blocos.items():
            st.markdown(f"### {nome_bloco}")
            meta = metadados_blocos.get(nome_bloco, {})
            tipo_bloco = meta.get("tipo", "likert")
            escala = meta.get("escala", (1, 7))
            labels = meta.get("labels", ("", ""))
            tipos_personalizados = meta.get("tipos_personalizados", {})

            if tipo_bloco == "likert":
                st.markdown(f"<small>{labels[0]} | {labels[1]}</small>", unsafe_allow_html=True)

            for item in itens:
                chave = f"item_{contador}"

                if tipo_bloco == "sociodemografico":
                    tipo_item = tipos_personalizados.get(item)
                    if tipo_item == "numero":
                        resposta = st.number_input(item, min_value=0, max_value=120, step=1, key=chave)
                    elif isinstance(tipo_item, list) and tipo_item:
                        resposta = st.selectbox(item, options=tipo_item, key=chave, index=0)
                        if resposta == "":
                            campos_vazios.append(item)
                    else:
                        resposta = st.selectbox(item, options=["", "Sim", "Não"], key=chave)
                        if resposta == "":
                            campos_vazios.append(item)

                elif tipo_bloco == "likert":
                    resposta = st.slider(
                        label=f"{contador}. {item}",
                        min_value=escala[0],
                        max_value=escala[1],
                        value=(escala[0] + escala[1]) // 2,
                        format="%d",
                        key=chave,
                    )

                else:
                    resposta = st.text_input(label=item, key=chave)

                respostas_usuario[chave] = resposta
                contador += 1

        # ✅ Confirmação do Termo de Consentimento
        aceitou_termo = st.checkbox("Declaro que li e aceito o Termo de Consentimento Livre e Esclarecido.", key="aceite_tcle")

        enviado = st.form_submit_button("Enviar Respostas", use_container_width=True)
        
        if enviado:
            if campos_vazios:
                st.error("⚠️ Por favor, responda todas as perguntas do bloco sociodemográfico antes de enviar.")
                return None

            if not aceitou_termo:
                st.error("⚠️ Você deve aceitar o Termo de Consentimento para prosseguir.")
                return None

            # ✅ Tentativa de salvar no Supabase
            salvou = salvar_respostas_supabase(
                respostas_dict=respostas_usuario,
                aceitou_tcle=aceitou_termo,
            )

            if salvou:
                return {"respostas": respostas_usuario}
            else:
                st.error("❌ Ocorreu um erro ao salvar suas respostas. Por favor, tente novamente.")
                return None
    return None

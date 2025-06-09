import streamlit as st
import pandas as pd
import os

# 🛠️ Configuração inicial da página
st.set_page_config(page_title="Dashboard de Veículos", layout="centered")

# 📥 Caminho do seu arquivo Excel (uso relativo para funcionar no GitHub e Streamlit Cloud)
excel_path = "dados_veiculos_enriquecidos.xlsx"

# 📁 Caminho da pasta com as imagens (uso relativo para funcionar no repositório)
images_path = "images"

# 🚗 Título da aplicação
st.title("🚗 Dashboard de Dados Técnicos de Veículos")

# 📊 Carregando os dados com cache
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel(excel_path)

        # Conversão automática para evitar erro com Arrow
        for col in df.columns:
            if df[col].dtype == object:
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    pass
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

df = carregar_dados()

# ✅ Se dados carregados corretamente
if not df.empty:
    # 🔍 Seleção do modelo
    modelos = df["Modelo"].dropna().unique().tolist()
    modelo_escolhido = st.selectbox("Selecione um modelo de veículo:", modelos)

    # 📋 Exibe os dados do modelo escolhido
    if modelo_escolhido:
        # 🖼️ Mostra imagem primeiro
        image_filename = f"{modelo_escolhido}.jpg"
        image_path = os.path.join(images_path, image_filename)

        if os.path.exists(image_path):
            st.image(image_path, caption=modelo_escolhido, use_container_width=True)
        else:
            st.info("📷 Imagem do veículo não encontrada.")

        # Exibe a tabela de dados
        dados_modelo = df[df["Modelo"] == modelo_escolhido].T
        dados_modelo.columns = ["Especificação"]

        st.subheader(f"📌 Especificações do {modelo_escolhido}")

        # Aplica estilo de fonte maior via CSS
        st.markdown("""
        <style>
        .dataframe td {
            font-size: 18px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.dataframe(dados_modelo, use_container_width=True)

        # 🚨 Mensagem de atenção
        st.markdown(
            """
            <div style='color: red; font-weight: bold; margin-top: 30px;'>
                🚨 Atenção: Este produto é um trial produzido pela <strong>Booming Marketing IA</strong>.<br>
                Não deve ser compartilhado com terceiros por tratar-se de material de validação de projeto.
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.warning("Nenhum dado encontrado para exibir.")

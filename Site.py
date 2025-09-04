import streamlit as st
import pandas as pd
import time

# Links convertidos para CSV
url_1 = "https://docs.google.com/spreadsheets/d/1IZIvIwvy2r-k2Tys19Fb-iZQ0LM1DP0C/export?format=csv"
url_2 = "https://docs.google.com/spreadsheets/d/1CAV6BkA6sZy51nPE8fuwoslgC0Mxa5kO/export?format=csv"

st.set_page_config(page_title="📊 Informações dos Irmãos", layout="wide")
st.title("📊 Informações dos Irmãos e Irmãs")

# Função para carregar os dados
@st.cache_data(ttl=5)
def load_data(url):
    return pd.read_csv(url)

# Container para atualizar dinamicamente
placeholder = st.empty()

while True:
    try:
        df1 = load_data(url_1)
        df2 = load_data(url_2)

        with placeholder.container():
            st.subheader("👥 Arquivo 1 - Presença")
            st.dataframe(df1.head())

            st.subheader("📖 Arquivo 2 - Recitativos")
            st.dataframe(df2.head())

            # =============================
            # Gráficos
            # =============================
            if "Data" in df1.columns and "Quantidade" in df1.columns:
                st.subheader("Irmãozinhos por Domingo")
                st.bar_chart(df1.set_index("Data")["Quantidade"])

            if "Recitativo" in df2.columns:
                total_recitativos = df2["Recitativo"].count()
                st.metric("Total de Recitativos", total_recitativos)

            if "Idade" in df1.columns:
                idade_count = df1["Idade"].value_counts()
                st.subheader("Irmãozinhos e Jovens por Idade")
                st.bar_chart(idade_count)

            st.subheader("📞 Informações de Contato")
            if "Nome" in df1.columns and "Telefone" in df1.columns and "Endereço" in df1.columns:
                st.dataframe(df1[["Nome", "Telefone", "Endereço"]])

    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")

    # Espera 5 segundos antes de atualizar novamente
    time.sleep(5)

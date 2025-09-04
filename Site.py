import streamlit as st
import pandas as pd
import time

# Links convertidos para CSV (coloque o format=csv no final)
url_1 = "https://docs.google.com/spreadsheets/d/1IZIvIwvy2r-k2Tys19Fb-iZQ0LM1DP0C/export?format=csv"
url_2 = "https://docs.google.com/spreadsheets/d/1CAV6BkA6sZy51nPE8fuwoslgC0Mxa5kO/export?format=csv"

st.set_page_config(page_title="📊 Informações dos Irmãos", layout="wide")

st.title("📊 Informações dos Irmãos e Irmãs")

# Auto refresh a cada 5 segundos
st.experimental_autorefresh(interval=5000, key="refresh")

# Função para carregar os dados
@st.cache_data(ttl=5)
def load_data(url):
    return pd.read_csv(url)

try:
    df1 = load_data(url_1)
    df2 = load_data(url_2)

    st.subheader("👥 Arquivo 1 - Presença")
    st.dataframe(df1.head())

    st.subheader("📖 Arquivo 2 - Recitativos")
    st.dataframe(df2.head())

    # =============================
    # Exemplos de gráficos
    # =============================

    # Quantos irmãozinhos por domingo (supondo colunas: "Data" e "Quantidade")
    if "Data" in df1.columns and "Quantidade" in df1.columns:
        st.bar_chart(df1.set_index("Data")["Quantidade"])

    # Quantos recitativos no total (supondo coluna "Recitativo")
    if "Recitativo" in df2.columns:
        total_recitativos = df2["Recitativo"].count()
        st.metric("Total de Recitativos", total_recitativos)

    # Quantos irmãozinhos e jovens por idade (supondo colunas "Idade" e "Nome")
    if "Idade" in df1.columns:
        idade_count = df1["Idade"].value_counts()
        st.bar_chart(idade_count)

    # =============================
    # Informações extras
    # =============================
    st.subheader("📞 Informações de Contato")
    if "Nome" in df1.columns and "Telefone" in df1.columns and "Endereço" in df1.columns:
        st.dataframe(df1[["Nome", "Telefone", "Endereço"]])

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

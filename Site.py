import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🔄 Atualização automática a cada 5 segundos
st.experimental_autorefresh(interval=5000, limit=None, key="refresh")

# Links dos arquivos Google Sheets
url_arquivo_1 = "https://docs.google.com/spreadsheets/d/1IZIvIwvy2r-k2Tys19Fb-iZQ0LM1DP0C/export?format=csv"
url_arquivo_2 = "https://docs.google.com/spreadsheets/d/1CAV6BkA6sZy51nPE8fuwoslgC0Mxa5kO/export?format=csv"

# Carregar dados
try:
    df1 = pd.read_csv(url_arquivo_1)
    df2 = pd.read_csv(url_arquivo_2)
except Exception as e:
    st.error(f"Erro ao carregar os arquivos: {e}")
    st.stop()

# Título
st.title("📊 Painel da Reunião de Jovens e Menores")
st.caption("Dados carregados automaticamente do Google Drive (atualização a cada 5s).")

# 📌 Gráfico 1 – Quantos irmãozinhos foram por cada domingo
if "Data" in df1.columns:
    freq_por_dia = df1.groupby("Data").size()
    st.subheader("👶 Irmãozinhos por Domingo")
    st.bar_chart(freq_por_dia)

# 📌 Gráfico 2 – Total de recitativos
if "Recitativo" in df1.columns:
    total_recitativos = df1["Recitativo"].count()
    st.subheader("🎤 Total de Recitativos")
    st.metric("Quantidade", total_recitativos)

# 📌 Gráfico 3 – Quantos irmãozinhos e jovens por idade
if "Idade" in df2.columns:
    idade_counts = df2["Idade"].value_counts().sort_index()
    st.subheader("📈 Distribuição por Idade")
    st.line_chart(idade_counts)

# 📌 Tabela final com informações de contato
st.subheader("📒 Informações de Contato")
if "Nome" in df2.columns and "Endereço" in df2.columns and "Telefone" in df2.columns:
    st.dataframe(df2[["Nome", "Endereço", "Telefone"]])
else:
    st.warning("Colunas de contato não encontradas no arquivo.")

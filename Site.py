import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para converter link em ID e montar link de download
def get_download_url(drive_url):
    file_id = drive_url.split("/d/")[1].split("/")[0]
    return f"https://drive.google.com/uc?id={file_id}"

# Links das suas planilhas
url_arquivo1 = "https://docs.google.com/spreadsheets/d/1IZIvIwvy2r-k2Tys19Fb-iZQ0LM1DP0C/edit?usp=sharing"
url_arquivo2 = "https://docs.google.com/spreadsheets/d/1CAV6BkA6sZy51nPE8fuwoslgC0Mxa5kO/edit?usp=sharing"

download1 = get_download_url(url_arquivo1)
download2 = get_download_url(url_arquivo2)

# Atualiza a cada 5 segundos
st_autorefresh = st.experimental_autorefresh(interval=5000, limit=None, key="refresh")

st.set_page_config(page_title="📊 Painel de Jovens e Menores", layout="wide")
st.title("📊 Painel da Reunião de Jovens e Menores")
st.caption("Dados carregados automaticamente do Google Drive (atualização a cada 5s).")

try:
    # Lendo os dois arquivos
    df1 = pd.read_excel(download1)
    df2 = pd.read_excel(download2)

    # --- 1. Irmãozinhos por Domingo ---
    st.subheader("👨‍👩‍👧‍👦 Irmãozinhos por Domingo")
    fig1, ax1 = plt.subplots()
    df1.groupby("Data")["Irmãozinhos"].sum().plot(kind="bar", ax=ax1)
    ax1.set_ylabel("Quantidade")
    st.pyplot(fig1)

    # --- 2. Recitativos totais ---
    st.subheader("🎶 Recitativos")
    total_recitativos = df1["Recitativos"].sum()
    st.metric("Total de Recitativos", total_recitativos)

    # --- 3. Idade dos irmãos ---
    st.subheader("📈 Distribuição por Idade")
    fig2, ax2 = plt.subplots()
    df2["Idade"].plot(kind="hist", bins=10, ax=ax2, rwidth=0.8)
    ax2.set_xlabel("Idade")
    ax2.set_ylabel("Quantidade")
    st.pyplot(fig2)

    # --- 4. Consulta individual ---
    st.subheader("🔍 Consulta de Irmão/Jovem")
    nome_pesquisa = st.text_input("Digite o nome do irmão/jovem:")
    if nome_pesquisa:
        resultado = df2[df2["Nome"].str.contains(nome_pesquisa, case=False, na=False)]
        if not resultado.empty:
            st.dataframe(resultado)
        else:
            st.warning("Nenhum registro encontrado.")

except Exception as e:
    st.error(f"Erro ao carregar os arquivos: {e}")



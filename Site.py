import streamlit as st
import pandas as pd
import altair as alt

# Configuração da página
st.set_page_config(page_title="📊 Painel de Jovens e Menores", layout="wide")

st.title("📊 Painel da Reunião de Jovens e Menores")
st.caption("Dados carregados automaticamente do Google Drive (atualização a cada 5s).")

# 🔄 Auto-refresh a cada 5 segundos
st_autorefresh = st.autorefresh(interval=5000, limit=None, key="refresh")

# Função para converter link do Google Drive em link de download
def get_download_url(drive_url):
    file_id = drive_url.split("/d/")[1].split("/")[0]
    return f"https://drive.google.com/uc?id={file_id}"

# Links dos arquivos (seus)
url_arquivo1 = "https://docs.google.com/spreadsheets/d/1IZIvIwvy2r-k2Tys19Fb-iZQ0LM1DP0C/edit?usp=sharing"
url_arquivo2 = "https://docs.google.com/spreadsheets/d/1CAV6BkA6sZy51nPE8fuwoslgC0Mxa5kO/edit?usp=sharing"

download1 = get_download_url(url_arquivo1)
download2 = get_download_url(url_arquivo2)

try:
    # --- Ler os dados ---
    df1 = pd.read_excel(download1)  # Arquivo 1 (dados por domingo, recitativos)
    df2 = pd.read_excel(download2)  # Arquivo 2 (dados pessoais e idades)

    # --- 1. Irmãozinhos por Domingo ---
    st.subheader("👨‍👩‍👧‍👦 Irmãozinhos por Domingo")
    if "Data" in df1.columns and "Irmãozinhos" in df1.columns:
        chart1 = alt.Chart(df1).mark_bar().encode(
            x="Data:T",  # assume que Data é coluna de datas
            y="Irmãozinhos:Q",
            tooltip=["Data", "Irmãozinhos"]
        ).properties(width=600, height=400)
        st.altair_chart(chart1, use_container_width=True)
    else:
        st.warning("⚠️ Verifique se o arquivo 1 contém as colunas 'Data' e 'Irmãozinhos'.")

    # --- 2. Recitativos totais ---
    st.subheader("🎶 Recitativos")
    if "Recitativos" in df1.columns:
        total_recitativos = df1["Recitativos"].sum()
        st.metric("Total de Recitativos", total_recitativos)
    else:
        st.warning("⚠️ Coluna 'Recitativos' não encontrada no arquivo 1.")

    # --- 3. Idade dos irmãos ---
    st.subheader("📈 Distribuição por Idade")
    if "Idade" in df2.columns:
        chart2 = alt.Chart(df2).mark_bar().encode(
            x=alt.X("Idade:Q", bin=alt.Bin(maxbins=15)),  # histograma
            y="count()",
            tooltip=["Idade"]
        ).properties(width=600, height=400)
        st.altair_chart(chart2, use_container_width=True)
    else:
        st.warning("⚠️ Coluna 'Idade' não encontrada no arquivo 2.")

    # --- 4. Consulta individual ---
    st.subheader("🔍 Consulta de Irmão/Jovem")
    if "Nome" in df2.columns:
        nome_pesquisa = st.text_input("Digite o nome do irmão/jovem:")
        if nome_pesquisa:
            resultado = df2[df2["Nome"].str.contains(nome_pesquisa, case=False, na=False)]
            if not resultado.empty:
                st.dataframe(resultado)
            else:
                st.warning("Nenhum registro encontrado.")
    else:
        st.warning("⚠️ Coluna 'Nome' não encontrada no arquivo 2.")

except Exception as e:
    st.error(f"Erro ao carregar os arquivos: {e}")

import streamlit as st
import pandas as pd
import time
import io

# Links convertidos para CSV - o 'export?format=csv' no final é a chave!
URL_ARQUIVO_1 = "https://docs.google.com/spreadsheets/d/1IZIvIwvy2r-k2Tys19Fb-iZQ0LM1DP0C/export?format=csv"
URL_ARQUIVO_2 = "https://docs.google.com/spreadsheets/d/1CAV6BkA6sZy51nPE8fuwoslgC0Mxa5kO/export?format=csv"

# Configuração da página e título
st.set_page_config(page_title="📊 Dashboard da Paróquia", layout="wide")
st.title("📊 Dashboard de Informações da Paróquia")
st.markdown("---")

# Use st.cache_data para carregar os dados de forma eficiente.
# ttl=5 significa que os dados serão recarregados a cada 5 segundos.
@st.cache_data(ttl=5)
def load_data(url):
    """Carrega dados da URL e retorna um DataFrame."""
    try:
        df = pd.read_csv(url)
        # Converte nomes de colunas para minúsculas e sem acento para facilitar a busca
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da URL: {url}\nDetalhes: {e}")
        return pd.DataFrame()

# Carregar os dados das duas planilhas
df_presenca = load_data(URL_ARQUIVO_1)
df_recitativos = load_data(URL_ARQUIVO_2)

# Verificar se os DataFrames não estão vazios antes de tentar criar gráficos
if not df_presenca.empty:
    # Quantos irmãozinhos foram por cada domingo
    st.subheader("👥 Presença por Domingo")
    # Certifique-se de que as colunas 'data' e 'presenca' existem
    if 'data' in df_presenca.columns and 'presenca' in df_presenca.columns:
        df_presenca['data'] = pd.to_datetime(df_presenca['data'])
        chart_presenca = pd.DataFrame({
            'Domingo': df_presenca['data'].dt.strftime('%d/%m'),
            'Irmãozinhos': df_presenca['presenca']
        }).set_index('Domingo')
        st.bar_chart(chart_presenca)
    else:
        st.warning("O arquivo de Presença não tem as colunas 'data' ou 'presenca'. Gráfico não pode ser criado.")
        st.dataframe(df_presenca.head())

if not df_recitativos.empty:
    # Quantos recitativos no total
    st.subheader("📖 Recitativos")
    if 'recitativos' in df_recitativos.columns:
        total_recitativos = df_recitativos['recitativos'].sum()
        st.metric(label="Total de Recitativos", value=total_recitativos)
    else:
        st.warning("O arquivo de Recitativos não tem a coluna 'recitativos'. Métrica não pode ser criada.")

    # Quantos irmãozinhos e jovens por idade
    st.subheader("👶 Jovens e Irmãozinhos por Idade")
    if 'idade' in df_recitativos.columns:
        contagem_idade = df_recitativos['idade'].value_counts().sort_index()
        st.bar_chart(contagem_idade)
    else:
        st.warning("O arquivo de Recitativos não tem a coluna 'idade'. Gráfico não pode ser criado.")

# Rodapé para indicar o horário da última atualização
st.markdown("---")
st.info(f"Última atualização: {time.strftime('%H:%M:%S', time.localtime())}")

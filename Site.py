import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# --- URLs dos arquivos no Google Drive (ajustados para download) ---
URL_CADASTRO = "https://drive.google.com/uc?id=1IZIvIwvy2r-k2Tys19Fb-iZQ0LM1DP0C"
URL_PRESENCA = "https://drive.google.com/uc?id=1CAV6BkA6sZy51nPE8fuwoslgC0Mxa5kO"

# --- Configuração da Página ---
st.set_page_config(
    page_title="Dashboard Jd. São Pedro",
    page_icon="📊",
    layout="wide"
)

# --- Título e Descrição ---
st.title("📊 Painel de Análise - Reunião de Jovens e Menores")
st.caption("Dados atualizados automaticamente a cada 5 segundos.")

# --- Auto-Refresh (recarrega a página a cada 5 segundos) ---
def autorefresh(interval_sec):
    st.markdown(
        f"""
        <script>
            setTimeout(() => {{
                window.location.reload();
            }}, {interval_sec * 1000});
        </script>
        """,
        unsafe_allow_html=True
    )

autorefresh(5) # Recarrega a página a cada 5 segundos

# --- Carregar e Processar os Dados (função com cache) ---
@st.cache_data(ttl=5) # Cache os dados por 5 segundos
def load_data():
    try:
        # Carrega o arquivo de cadastro
        df_cadastro = pd.read_excel(URL_CADASTRO, engine='openpyxl')
        df_cadastro = df_cadastro.dropna(how='all') # Remove linhas vazias

        # Carrega o arquivo de presença/recitativos
        df_presenca = pd.read_excel(URL_PRESENCA, engine='openpyxl')
        df_presenca = df_presenca.dropna(how='all') # Remove linhas vazias
        
        # Converte a coluna de data para o formato correto
        df_presenca['Data'] = pd.to_datetime(df_presenca['Data'], format='%d/%m/%Y', errors='coerce')
        
        # Pega a última data de atualização da planilha de presença
        ultima_data_atualizacao = df_presenca['Data'].max().strftime('%d/%m/%Y')
        
        return df_cadastro, df_presenca, ultima_data_atualizacao
    except Exception as e:
        st.error(f"❌ Erro ao carregar os dados do Google Drive. Verifique se os links estão públicos ou se o formato é 'xlsx'/'xls'. Erro: {e}")
        return None, None, None

# --- Main Dashboard Layout ---
df_cadastro, df_presenca, ultima_data = load_data()

if df_cadastro is not None and df_presenca is not None:
    
    st.subheader(f"Última Atualização: {ultima_data}")
    st.markdown("---")

    # --- K-P-I's (Indicadores Chave) ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_irmaos = df_cadastro['Nome'].nunique()
        st.metric(label="Total de Irmãos Cadastrados", value=f"{total_irmaos}")
    
    with col2:
        total_recitativos = df_presenca['Recitativo'].sum()
        st.metric(label="Total de Recitativos", value=f"{int(total_recitativos)}")
        
    with col3:
        total_presencas = df_presenca['Presentes'].sum()
        st.metric(label="Total de Presenças (Somatório)", value=f"{int(total_presencas)}")

    with col4:
        # Contar "sim" na coluna "Músico/Organista/Estudando Música?"
        musicos = df_cadastro[df_cadastro['Músico/Organista/Estudando Música?'] == 'Sim']['Nome'].count()
        st.metric(label="Total de Músicos e Organistas", value=f"{musicos}")

    st.markdown("---")

    # --- Gráficos da Primeira Coluna (Presença e Recitativos) ---
    st.header("Análise de Presença e Recitativos")
    
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.subheader("Presença por Domingo")
        
        # Agrupar a presença por data
        presenca_por_data = df_presenca.groupby('Data')['Presentes'].sum().reset_index()
        fig_presenca = px.line(
            presenca_por_data, 
            x='Data', 
            y='Presentes', 
            markers=True, 
            labels={'Data': 'Data', 'Presentes': 'Número de Presentes'},
            title="Evolução da Presença em Cada Reunião"
        )
        st.plotly_chart(fig_presenca, use_container_width=True)
        
    with col_graph2:
        st.subheader("Recitativos por Domingo")
        
        # Agrupar os recitativos por data
        recitativos_por_data = df_presenca.groupby('Data')['Recitativo'].sum().reset_index()
        fig_recitativos = px.bar(
            recitativos_por_data, 
            x='Data', 
            y='Recitativo', 
            labels={'Data': 'Data', 'Recitativo': 'Número de Recitativos'},
            title="Evolução dos Recitativos por Reunião"
        )
        st.plotly_chart(fig_recitativos, use_container_width=True)

    st.markdown("---")

    # --- Gráficos da Segunda Coluna (Idade) ---
    st.header("Análise por Idade")
    
    col_graph3, col_graph4 = st.columns(2)
    
    with col_graph3:
        st.subheader("Distribuição de Irmãos por Faixa Etária")
        
        # Calcula a idade
        df_cadastro['Idade'] = df_cadastro['Data de Nascimento'].apply(
            lambda x: (datetime.now().year - x.year) - ((datetime.now().month, datetime.now().day) < (x.month, x.day))
        )
        
        fig_idade = px.histogram(
            df_cadastro, 
            x='Idade', 
            nbins=20, 
            labels={'Idade': 'Idade'},
            title="Quantidade de Irmãos por Idade"
        )
        st.plotly_chart(fig_idade, use_container_width=True)

    with col_graph4:
        st.subheader("Irmãos por Faixa Etária")

        # Cria as faixas de idade
        bins = [0, 12, 18, 25, 100]
        labels = ['0-12 anos', '13-18 anos', '19-25 anos', 'Acima de 25 anos']
        df_cadastro['Faixa Etária'] = pd.cut(df_cadastro['Idade'], bins=bins, labels=labels, right=False)

        # Conta a quantidade por faixa etária
        faixa_etaria_counts = df_cadastro['Faixa Etária'].value_counts().reset_index()
        faixa_etaria_counts.columns = ['Faixa Etária', 'Quantidade']

        fig_pie = px.pie(
            faixa_etaria_counts, 
            values='Quantidade', 
            names='Faixa Etária', 
            title='Proporção de Irmãos por Faixa Etária'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    
    # --- Seção para visualização de dados pessoais ---
    st.header("Visualização de Dados Pessoais (Protegida)")
    st.warning("⚠️ Esta seção contém dados sensíveis. Utilize com discrição.")
    
    # Adicione uma senha para visualização
    senha = st.text_input("Digite a senha para visualizar os dados:", type="password")
    
    # Verifique a senha
    SENHA_CORRETA = "CCB2025" 
    
    if senha == SENHA_CORRETA:
        st.success("✅ Senha correta!")
        
        # Exibe a tabela completa de cadastro
        st.dataframe(df_cadastro[[
            'Nome',
            'Telefones', 
            'Endereço Residencial', 
            'Nome dos Responsáveis'
        ]], hide_index=True)
        
    elif senha:
        st.error("❌ Senha incorreta. Tente novamente.")

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- URLs dos arquivos no Google Drive (compartilhados como "Qualquer pessoa com o link") ---
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

# --- Auto-Refresh manual com HTML/JS ---
def autorefresh(interval_sec=5):
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

autorefresh(5)  # Atualiza a cada 5 segundos

# --- Função para carregar os dados ---
@st.cache_data(ttl=5)  # cache expira a cada 5 segundos
def load_data():
    try:
        df_cadastro = pd.read_excel(URL_CADASTRO, engine="openpyxl").dropna(how="all")
        df_presenca = pd.read_excel(URL_PRESENCA, engine="openpyxl").dropna(how="all")

        # Converter coluna de data
        if "Data" in df_presenca.columns:
            df_presenca["Data"] = pd.to_datetime(
                df_presenca["Data"], format="%d/%m/%Y", errors="coerce"
            )

        ultima_data_atualizacao = None
        if "Data" in df_presenca.columns:
            ultima_data_atualizacao = df_presenca["Data"].max().strftime("%d/%m/%Y")

        return df_cadastro, df_presenca, ultima_data_atualizacao
    except Exception as e:
        st.error(f"❌ Erro ao carregar os dados do Google Drive: {e}")
        return None, None, None

# --- Main Dashboard ---
df_cadastro, df_presenca, ultima_data = load_data()

if df_cadastro is not None and df_presenca is not None:
    if ultima_data:
        st.subheader(f"📅 Última Atualização: {ultima_data}")
    st.markdown("---")

    # --- KPIs ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_irmaos = df_cadastro["Nome"].nunique() if "Nome" in df_cadastro.columns else 0
        st.metric("Total de Irmãos Cadastrados", total_irmaos)

    with col2:
        total_recitativos = df_presenca["Recitativo"].sum() if "Recitativo" in df_presenca.columns else 0
        st.metric("Total de Recitativos", int(total_recitativos))

    with col3:
        total_presencas = df_presenca["Presentes"].sum() if "Presentes" in df_presenca.columns else 0
        st.metric("Total de Presenças", int(total_presencas))

    with col4:
        if "Músico/Organista/Estudando Música?" in df_cadastro.columns:
            musicos = df_cadastro[df_cadastro["Músico/Organista/Estudando Música?"] == "Sim"]["Nome"].count()
        else:
            musicos = 0
        st.metric("Músicos e Organistas", musicos)

    st.markdown("---")

    # --- Gráficos: Presença e Recitativos ---
    st.header("📈 Análise de Presença e Recitativos")
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        if "Data" in df_presenca.columns and "Presentes" in df_presenca.columns:
            presenca_por_data = df_presenca.groupby("Data")["Presentes"].sum().reset_index()
            fig = px.line(presenca_por_data, x="Data", y="Presentes", markers=True,
                          title="Presença por Domingo")
            st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        if "Data" in df_presenca.columns and "Recitativo" in df_presenca.columns:
            recitativos_por_data = df_presenca.groupby("Data")["Recitativo"].sum().reset_index()
            fig = px.bar(recitativos_por_data, x="Data", y="Recitativo",
                         title="Recitativos por Domingo")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- Gráficos: Idade ---
    st.header("👶 Análise por Idade")
    col_g3, col_g4 = st.columns(2)

    with col_g3:
        if "Data de Nascimento" in df_cadastro.columns:
            df_cadastro["Idade"] = df_cadastro["Data de Nascimento"].apply(
                lambda x: (datetime.now().year - x.year)
                - ((datetime.now().month, datetime.now().day) < (x.month, x.day))
                if pd.notnull(x) else None
            )
            fig = px.histogram(df_cadastro, x="Idade", nbins=20,
                               title="Distribuição de Idade dos Irmãos")
            st.plotly_chart(fig, use_container_width=True)

    with col_g4:
        if "Idade" in df_cadastro.columns:
            bins = [0, 12, 18, 25, 100]
            labels = ["0-12 anos", "13-18 anos", "19-25 anos", "Acima de 25 anos"]
            df_cadastro["Faixa Etária"] = pd.cut(df_cadastro["Idade"], bins=bins, labels=labels, right=False)

            faixa_counts = df_cadastro["Faixa Etária"].value_counts().reset_index()
            faixa_counts.columns = ["Faixa Etária", "Quantidade"]

            fig = px.pie(faixa_counts, values="Quantidade", names="Faixa Etária",
                         title="Proporção por Faixa Etária")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- Dados pessoais protegidos ---
    st.header("🔒 Dados Pessoais")
    senha = st.text_input("Digite a senha para visualizar os dados:", type="password")
    SENHA_CORRETA = "CCB2025"

    if senha == SENHA_CORRETA:
        st.success("✅ Senha correta!")
        cols_mostrar = [c for c in ["Nome", "Telefones", "Endereço Residencial", "Nome dos Responsáveis"] if c in df_cadastro.columns]
        st.dataframe(df_cadastro[cols_mostrar], hide_index=True)
    elif senha:
        st.error("❌ Senha incorreta. Tente novamente.")

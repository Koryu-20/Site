import streamlit as st

# Configuração da página
st.set_page_config(page_title="Cartão de Visita - CCB", layout="centered")

# Caminho RAW da imagem do GitHub
background_image_url = "https://raw.githubusercontent.com/Koryu-20/Site/main/CCB.png"

# Estilo com imagem de fundo do GitHub
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.94);
        padding: 2rem;
        border-radius: 15px;
        max-width: 850px;
        margin: auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Cartão de Visita - Reuniões e Visitas")

with st.form("formulario_visita"):
    col1, col2 = st.columns(2)

    with col1:
        nome_irmao = st.text_input("Nome do irmão:")
        telefone = st.text_input("Telefone:")
        logradouro = st.text_input("Logradouro:")
        cep = st.text_input("CEP:")
        bairro = st.text_input("Bairro:")
        cidade = st.text_input("Cidade:")

    with col2:
        nome_irma = st.text_input("Nome da irmã:")
        comum = st.text_input("Comum Congregação:")
        complemento = st.text_input("Complemento:")
        numero = st.text_input("Nº:")
        estado = st.text_input("Estado:")
        batizado_irmao = st.radio("Batizado (irmão):", ["Sim", "Não"], horizontal=True)
        data_batismo_irmao = st.date_input("Data Batismo (irmão):")
        batizado_irma = st.radio("Batizado (irmã):", ["Sim", "Não"], horizontal=True)
        data_batismo_irma = st.date_input("Data Batismo (irmã):")

    st.markdown("### Tipo de Visita:")
    visita_gvi = st.checkbox("GVI - Grupo de Visitas Entre a Irmandade")
    visita_gvm = st.checkbox("GVM - Grupo de Visitas com a Mocidade")
    visita_rf = st.checkbox("RF - Reunião Familiar")
    visita_re = st.checkbox("RE - Reunião de Evangelização")

    col3, col4 = st.columns(2)
    with col3:
        filhos = st.radio("Filhos:", ["Sim", "Não"], horizontal=True)
    with col4:
        qtde_filhos = st.number_input("Qtde:", min_value=0, step=1)

    atendimento = st.text_input("Atendimento:")
    data_atendimento = st.date_input("Data:")

    observacoes = st.text_area("Obs.:")

    enviar = st.form_submit_button("Enviar Cartão")

    if enviar:
        st.success("✅ Cartão de Visita enviado com sucesso!")

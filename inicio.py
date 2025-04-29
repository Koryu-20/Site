import streamlit as st

# Configurações da página
st.set_page_config(page_title="Cadastro Jovens e Menores - CCB", layout="centered")

# CSS ajustado para imagem menor e mais suave
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT8s0MG4WMMrRWvrodkdk8afUF_7v6YtSAOiw&s");
        background-size: 30%;  /* Tamanho reduzido da imagem */
        background-repeat: repeat;
        background-attachment: fixed;
        background-position: top center;
        filter: brightness(0.9);  /* Deixa o fundo mais suave */
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.93);
        padding: 2rem;
        border-radius: 15px;
        max-width: 800px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo da CCB
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Congregacao_Crista_no_Brasil.svg/1200px-Congregacao_Crista_no_Brasil.svg.png", width=150)

# Título
st.title("Cadastro de Participação da Reunião de Jovens e Menores - Jd. São Pedro")

# Formulário
with st.form("cadastro_form"):
    st.subheader("Dados Pessoais")
    nome = st.text_input("Nome")
    col1, col2, col3 = st.columns(3)
    with col1:
        idade = st.number_input("Idade", min_value=0, max_value=100, step=1)
    with col2:
        data_nascimento = st.date_input("Data de Nascimento")
    with col3:
        batizado = st.selectbox("É Batizado?", ["Sim", "Não"])

    col4, col5 = st.columns(2)
    with col4:
        data_batismo = st.date_input("Data do Batismo", disabled=(batizado == "Não"))
    with col5:
        musica = st.selectbox("É Músico/Organista/Estudando Música?", ["Sim", "Não"])

    st.subheader("Responsáveis")
    nome_responsaveis = st.text_input("Nome dos Responsáveis")
    col6, col7, col8 = st.columns(3)
    with col6:
        grau_parentesco = st.text_input("Grau de Parentesco")
    with col7:
        responsavel_batizado = st.selectbox("Responsável é Batizado?", ["Sim", "Não"])
    with col8:
        telefones = st.text_input("Telefones para Contato")

    st.subheader("Endereço")
    endereco = st.text_area("Endereço Residencial")

    st.subheader("Informações Escolares")
    col9, col10, col11 = st.columns(3)
    with col9:
        estuda = st.selectbox("A criança/moço(a) estuda?", ["Sim", "Não"])
    with col10:
        serie = st.text_input("Qual série?")
    with col11:
        escola = st.text_input("Escola")

    enviar = st.form_submit_button("Enviar Cadastro")

    if enviar:
        st.success("✅ Cadastro enviado com sucesso!")

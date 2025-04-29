import streamlit as st
import pandas as pd
from io import BytesIO
import smtplib
from email.message import EmailMessage

# Função para envio de e-mail com o Excel em anexo
def enviar_email_com_anexo(email_destino, assunto, corpo, arquivo):
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = 'tuguitosmartins@gmail.com'
    msg['To'] = email_destino
    msg.set_content(corpo)

    msg.add_attachment(arquivo, maintype='application', subtype='octet-stream', filename="cadastro_jovens.xlsx")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('tuguitosmartins@gmail.com', 'vgmu rdva ysaw iytt')  # Substitua por sua App Password
            server.send_message(msg)
        st.success("✅ E-mail enviado com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro ao enviar e-mail: {e}")

# Configuração da página
st.set_page_config(page_title="Cadastro Jovens e Menores - CCB", layout="centered")

# CSS com imagem de fundo grande e suave
st.markdown(
    """
    <style>
    .stApp {
        background: url("https://raw.githubusercontent.com/Koryu-20/Site/main/CCB.png") no-repeat center top;
        background-size: cover;
        background-attachment: fixed;
        background-color: white;
    }
    .block-container {
        background-color: rgba(255, 255, 255, 0.94);
        padding: 2rem;
        border-radius: 15px;
        max-width: 850px;
        margin: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo e título
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Congregacao_Crista_no_Brasil.svg/1200px-Congregacao_Crista_no_Brasil.svg.png", width=150)
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

    st.subheader("Confirmação de envio")
    email_destino = st.text_input("Seu e-mail para receber o cadastro:")

    enviar = st.form_submit_button("Enviar Cadastro")

    if enviar:
        dados = {
            "Nome": [nome],
            "Idade": [idade],
            "Data de Nascimento": [data_nascimento],
            "Batizado": [batizado],
            "Data Batismo": [data_batismo if batizado == "Sim" else ""],
            "Música": [musica],
            "Nome Responsáveis": [nome_responsaveis],
            "Parentesco": [grau_parentesco],
            "Responsável Batizado": [responsavel_batizado],
            "Telefones": [telefones],
            "Endereço": [endereco],
            "Estuda": [estuda],
            "Série": [serie],
            "Escola": [escola],
        }

        df = pd.DataFrame(dados)

        # Gerar Excel em memória
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Cadastro Jovens")
        output.seek(0)

        corpo = "Segue em anexo o cadastro enviado da Reunião de Jovens e Menores."
        enviar_email_com_anexo(email_destino, "Cadastro Jovens e Menores - CCB", corpo, output.getvalue())

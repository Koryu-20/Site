import streamlit as st
import pandas as pd
from io import BytesIO
import smtplib
from email.message import EmailMessage

# Função para enviar e-mail com anexo
def enviar_email_com_anexo(email_destino, assunto, corpo, arquivo):
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = 'tuguitosmartins@gmail.com'  # Altere para seu e-mail
    msg['To'] = email_destino
    msg.set_content(corpo)

    # Anexando o arquivo Excel gerado
    msg.add_attachment(arquivo, maintype='application', subtype='octet-stream', filename="cartao_visita.xlsx")

    # Enviar o e-mail via SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('tuguitosmartins@gmail.com', 'vgmu rdva ysaw iyt')  # Use a senha ou App Password aqui
            server.send_message(msg)
        st.success("✅ E-mail enviado com sucesso!")
    except Exception as e:
        st.error(f"❌ Ocorreu um erro ao enviar o e-mail: {e}")

# Configuração da página
st.set_page_config(page_title="Cartão de Visita - CCB", layout="wide")

background_image_url = "https://raw.githubusercontent.com/Koryu-20/Site/main/CCB.png"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: url("{background_image_url}") no-repeat center top;
        background-size: 100% 100%;
        background-attachment: fixed;
        background-color: white;
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
        # Monta o DataFrame
        data = {
            "Nome do Irmão": [nome_irmao],
            "Telefone": [telefone],
            "Logradouro": [logradouro],
            "CEP": [cep],
            "Bairro": [bairro],
            "Cidade": [cidade],
            "Nome da Irmã": [nome_irma],
            "Comum Congregação": [comum],
            "Complemento": [complemento],
            "Número": [numero],
            "Estado": [estado],
            "Batizado Irmão": [batizado_irmao],
            "Data Batismo Irmão": [data_batismo_irmao],
            "Batizado Irmã": [batizado_irma],
            "Data Batismo Irmã": [data_batismo_irma],
            "Visita GVI": [visita_gvi],
            "Visita GVM": [visita_gvm],
            "Visita RF": [visita_rf],
            "Visita RE": [visita_re],
            "Filhos": [filhos],
            "Quantidade de Filhos": [qtde_filhos],
            "Atendimento": [atendimento],
            "Data Atendimento": [data_atendimento],
            "Observações": [observacoes]
        }
        df = pd.DataFrame(data)

        # Salva em memória
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Cartão de Visita')
        output.seek(0)

        # Enviar e-mail
        corpo_email = "Segue em anexo o Cartão de Visita solicitado."
        enviar_email_com_anexo('tuguitosmartins@gmail.com', 'Cartão de Visita - CCB', corpo_email, output.getvalue())

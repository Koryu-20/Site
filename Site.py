import streamlit as st
import pandas as pd
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Configuração da página
st.set_page_config(page_title="Cartão de Visita - CCB", layout="centered")

# Caminho RAW da imagem no GitHub
background_image_url = "https://raw.githubusercontent.com/Koryu-20/Site/main/CCB.png"

# Estilo
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

# Formulário
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
        # ----------------- Criar DataFrame e Excel ----------------- #
        dados = {
            "Nome Irmão": [nome_irmao],
            "Telefone": [telefone],
            "Logradouro": [logradouro],
            "CEP": [cep],
            "Bairro": [bairro],
            "Cidade": [cidade],
            "Nome Irmã": [nome_irma],
            "Comum": [comum],
            "Complemento": [complemento],
            "Número": [numero],
            "Estado": [estado],
            "Batizado Irmão": [batizado_irmao],
            "Data Batismo Irmão": [data_batismo_irmao.strftime("%d/%m/%Y")],
            "Batizado Irmã": [batizado_irma],
            "Data Batismo Irmã": [data_batismo_irma.strftime("%d/%m/%Y")],
            "Visita GVI": [visita_gvi],
            "Visita GVM": [visita_gvm],
            "Visita RF": [visita_rf],
            "Visita RE": [visita_re],
            "Filhos": [filhos],
            "Quantidade Filhos": [qtde_filhos],
            "Atendimento": [atendimento],
            "Data Atendimento": [data_atendimento.strftime("%d/%m/%Y")],
            "Observações": [observacoes]
        }

        df = pd.DataFrame(dados)

        # Nome do arquivo
        data_atual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"cartao_visita_{data_atual}.xlsx"
        df.to_excel(nome_arquivo, index=False)

        # ----------------- Upload para Google Drive ----------------- #
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        pasta_id = "1F7SGlWDjUTQEmG0tS_gZMAkPJzHxragq"  # Sua pasta

        file_drive = drive.CreateFile({'title': nome_arquivo, 'parents': [{'id': pasta_id}]})
        file_drive.SetContentFile(nome_arquivo)
        file_drive.Upload()

        # ----------------- Enviar E-mail ----------------- #
        remetente = "tuguitosmartins@gmail.com"  # Troque para seu Gmail
        senha = "04082004VDBr"          # Senha de App do Gmail
        destinatario = "tuguitosmartins@gmail.com"  # Você mesmo (pode trocar)

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = "Novo Cartão de Visita Registrado"
        body = f"Foi registrado um novo cartão de visita em {data_atual}."
        msg.attach(MIMEText(body, 'plain'))

        try:
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
            servidor.quit()
            st.success("✅ Cartão de Visita enviado, salvo no Drive e e-mail enviado!")
        except Exception as e:
            st.error(f"❌ Falha ao enviar e-mail: {e}")

        # Remove o arquivo local depois de upload (limpeza)
        if os.path.exists(nome_arquivo):
            os.remove(nome_arquivo)

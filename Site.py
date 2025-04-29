import streamlit as st
import pandas as pd
from io import BytesIO
import smtplib
from email.message import EmailMessage

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

        # Botão de download
        st.success("✅ Cartão de Visita enviado com sucesso!")
        st.download_button(
            label="📥 Baixar Excel",
            data=output,
            file_name="cartao_visita.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # ENVIAR POR E-MAIL
        destinatario = "tuguitosmartins@gmail.com"  # <-- Substitua por seu e-mail
        remetente = "tuguitosmartins@gmail.com"    # <-- Deve ser o mesmo do login abaixo
        senha_app = "04082004VDBr"           # <-- Substitua pela senha de app do Gmail

        # Monta o e-mail
        msg = EmailMessage()
        msg['Subject'] = "Cartão de Visita - Reuniões e Visitas"
        msg['From'] = remetente
        msg['To'] = destinatario
        msg.set_content("Segue em anexo o Cartão de Visita preenchido.")

        # Adiciona o anexo (Excel)
        msg.add_attachment(output.read(),
                           maintype='application',
                           subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                           filename='cartao_visita.xlsx')

        # Envia o e-mail
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(remetente, senha_app)
                smtp.send_message(msg)
            st.success("📧 Cartão de Visita enviado para seu e-mail com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao enviar e-mail: {e}")

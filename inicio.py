# Inicio.py

import streamlit as st
from datetime import datetime

# Configurações da página
st.set_page_config(page_title="Aurora's Realm: The Enchanted Adventure", layout="wide")

# Variáveis do jogo
nome_jogo = "Aurora's Realm: The Enchanted Adventure"
data_lancamento = datetime(2025, 12, 20)
hoje = datetime.now()
dias_restantes = (data_lancamento - hoje).days

# Estilo CSS profissional
st.markdown("""
    <style>
    .container {
        padding: 30px;
        background-color: #1a1a1a;
        border-radius: 15px;
        box-shadow: 0 0 20px #6c00ff;
        color: white;
        font-family: 'Trebuchet MS', sans-serif;
        margin: 20px;
    }
    h1, h2, h3 {
        color: #9f7aea;
    }
    p {
        font-size: 18px;
        line-height: 1.6;
    }
    .button {
        background-color: #6c00ff;
        color: white;
        padding: 12px 25px;
        margin: 10px 5px 30px 5px;
        border: none;
        border-radius: 8px;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
        display: inline-block;
    }
    .button:hover {
        background-color: #9f7aea;
    }
    .social-links {
        text-align: center;
        margin-top: 50px;
    }
    .social-links a {
        margin: 0 15px;
        text-decoration: none;
        font-size: 22px;
        color: #6c00ff;
        font-weight: bold;
        transition: 0.3s;
    }
    .social-links a:hover {
        color: #9f7aea;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: gray;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# HTML do conteúdo
st.markdown(f"""
<div class="container">
    <h1>🎮 {nome_jogo}</h1>
    <h3>🌟 About the Game</h3>
    <p>
        Welcome to <strong>Aurora's Realm: The Enchanted Adventure</strong>! Prepare for an epic journey where magic, courage, 
        and friendship are your greatest weapons. Create your hero, master unique skills, and explore a world full of mysteries.<br><br>

        🧙‍♂️ Train with wise masters.<br>
        🛡️ Forge alliances and battle legendary creatures.<br>
        ⚔️ Conquer ancient artifacts to unlock hidden powers.<br>
        📜 Live an immersive story where every decision changes the fate of the world!
    </p>

    <h3>📅 Release Date:</h3>
    <p><strong>{data_lancamento.strftime('%B %d, %Y')}</strong></p>

    <h3>⏳ Countdown:</h3>
    <p><strong>{"🚀 Only " + str(dias_restantes) + " days left!" if dias_restantes > 0 else "🎉 The game has been launched!"}</strong></p>

    <a href="#" class="button">🔑 Login</a>
    <a href="#" class="button">📝 Sign Up</a>

    <div class="social-links">
        <h3>🔗 Me Sigam:</h3>
        <a href="https://www.youtube.com/" target="_blank">YouTube</a>
        <a href="https://www.facebook.com/" target="_blank">Facebook</a>
        <a href="https://www.instagram.com/" target="_blank">Instagram</a>
    </div>

</div>

<div class="footer">
    © 2025 Aurora's Realm Studios. All rights reserved.
</div>
""", unsafe_allow_html=True)

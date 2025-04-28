# Inicio.py

import streamlit as st
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page

# Configurações iniciais da página
st.set_page_config(page_title="Aurora's Realm: The Enchanted Adventure", layout="wide")

# Informações do jogo
nome_jogo = "Aurora's Realm: The Enchanted Adventure"
descricao = """
<div style="text-align: justify;">
<strong>Welcome to Aurora's Realm: The Enchanted Adventure!</strong><br><br>

Prepare yourself for an epic journey where magic, courage, and friendship are your greatest weapons.
In this enchanted world, you will create your own hero, choose unique abilities, explore mysterious realms, 
and face legendary creatures.<br><br>

<strong>The story begins</strong> in a land forgotten by time, where an ancient prophecy speaks of a chosen one 
capable of restoring the balance between light and darkness. Your character will be guided by wise masters, face difficult dilemmas,
and carry the fate of the world in their hands.<br><br>

You will be able to:
<ul>
<li>🌍 Explore vast open maps full of secrets.</li>
<li>🛡️ Forge alliances with magical clans and legendary warriors.</li>
<li>⚔️ Conquer ancient artifacts to enhance your powers.</li>
<li>🧙‍♂️ Customize skills and equipment to create your unique strategy.</li>
<li>📜 Live a story where every decision shapes the future of the world.</li>
</ul>

<strong>Aurora's Realm</strong> promises a unique experience of immersion, adventure, and emotion!
</div>
"""

data_lancamento = datetime(2025, 12, 20)

# Calculando o tempo restante para o lançamento
hoje = datetime.now()
tempo_restante = data_lancamento - hoje
dias_restantes = tempo_restante.days

# Layout da página
col1, col2 = st.columns([2, 1])

with col1:
    st.title(f"🎮 {nome_jogo}")
    
    st.subheader("🌟 About the Game:")
    st.markdown(descricao, unsafe_allow_html=True)

    st.subheader("📅 Release Date:")
    st.write(f"**{data_lancamento.strftime('%B %d, %Y')}**")

    st.subheader("⏳ Countdown to Launch:")
    if dias_restantes > 0:
        st.success(f"🚀 Only **{dias_restantes} days** left for the grand launch!")
    else:
        st.warning("🎉 The game has already been launched!")

    st.markdown("---")
    st.info("⚙️ Currently, the game is in its final polishing and adjustments phase. Soon, adventurers from around the world will embark on this magical journey! 🌟")
    
with col2:
    with st.container(border=True):
        st.write("## 🔐 Quick Access")
        st.write("---")
        if st.button("🔑 Login"):
            switch_page("Login")
        if st.button("📝 Sign Up"):
            switch_page("Cadastro")

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2025 Aurora's Realm Studios. All rights reserved.</p>",
    unsafe_allow_html=True
)

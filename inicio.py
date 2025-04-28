import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Aurora's Realm: The Enchanted Adventure", layout="wide")

# Variáveis
nome_jogo = "Aurora's Realm: The Enchanted Adventure"
data_lancamento = datetime(2025, 12, 20)
dias_restantes = (data_lancamento - datetime.now()).days

# Conteúdo
st.title(f"🎮 {nome_jogo}")

st.header("🌟 About the Game")
st.write("""
Welcome to **Aurora's Realm: The Enchanted Adventure**! Prepare for an epic journey where magic, courage, 
and friendship are your greatest weapons. Create your hero, master unique skills, and explore a world full of mysteries.

🧙‍♂️ Train with wise masters  
🛡️ Forge alliances and battle legendary creatures  
⚔️ Conquer ancient artifacts to unlock hidden powers  
📜 Live an immersive story where every decision changes the fate of the world!
""")

st.header("📅 Release Date")
st.write("**December 20, 2025**")

st.header("⏳ Countdown")
st.write(f"**🚀 Only {dias_restantes} days left!**")

# Botões de ação
col1, col2 = st.columns(2)
with col1:
    st.button("🔑 Login")
with col2:
    st.button("📝 Sign Up")

# Redes sociais
st.header("🔗 Me Sigam")
st.markdown("[YouTube](https://www.youtube.com/)")
st.markdown("[Facebook](https://www.facebook.com/)")
st.markdown("[Instagram](https://www.instagram.com/)")

# Rodapé
st.markdown("---")
st.caption("© 2025 Aurora's Realm Studios. All rights reserved.")

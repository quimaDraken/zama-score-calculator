import math
import streamlit as st

def calculate_final_score(smart_followers, impressions, likes, retweets, quotes, followers, posts, smart_engagement):
    # Passo 1: ER%
    er_percent = (likes + retweets + quotes) / impressions * 100 if impressions > 0 else 0
    
    # Guard: Se ER% > 20, finalScore = 0
    if er_percent > 20:
        return 0
    
    # Passo 2: SRM
    srm = min(1, impressions / 100000)
    
    # Passo 3: SF
    sf = min(math.log10(smart_followers + 1), 3.0)
    
    # Passo 4: IMP
    imp = math.sqrt(impressions)
    
    # Passo 5: qW
    qw = 4 + 2 * srm
    
    # Passo 6: ENG
    eng = likes + 3 * retweets + qw * quotes
    
    # Passo 7: EngObs
    eng_obs = max(eng, (er_percent / 100) * impressions)
    
    # Passo 8: ER_cap
    er_cap = 0.01 + 0.04 * srm
    
    # Passo 9: EffEng
    eff_eng = min(eng_obs, impressions * er_cap)
    
    # Passo 10: Clamp
    clamp = eff_eng / eng_obs if eng_obs > 0 else 0
    
    # Passo 11: SENG
    seng = min(smart_engagement, 0.5 * eff_eng)
    
    # Passo 12: QE
    max_followers = max(followers, 1)
    qe_inner = math.log(1 + impressions / max_followers)  # log natural (ln)
    qe = min(qe_inner, 2.0) * srm
    
    # Passo 13: postMult
    post_mult = 1 + 0.02 * min(posts, 20)
    
    # Passo 14: erMult
    er_mult = 0.90 + 2 * min(er_percent / 100, 0.05)
    
    # Passo 15: engageBlock
    engage_block = ((eng * 0.7) * clamp + (seng * 150)) * (srm ** 1.5)
    
    # Passo 16: baseScore
    base_score = (sf * 500) + (imp * 10) + engage_block + (qe * 120)
    
    # Passo 17: finalScore antes de penalty
    final_score = base_score * er_mult * post_mult
    
    # Penalty: Se ER% > 10 e impressions < 50000, multiply by 0.30
    if er_percent > 10 and impressions < 50000:
        final_score *= 0.30
    
    return final_score

# Injetar CSS personalizado para background e melhoria de contraste
st.markdown("""
<style>
.stApp {
    background-color: #FFDE21;  /* Fundo cinza claro (exemplo) */
    color: #000000;  /* Texto principal em preto para alto contraste */
}

/* Labels dos inputs em negrito (já existente, mas reforçado) */
div.element-container .stNumberInput label {
    font-weight: bold;
    color: #000000;  /* Preto para contraste alto com fundo claro */
}

/* Texto geral e títulos com melhor contraste */
.stApp > header, .stApp > div {
    color: #000000;  /* Garante texto escuro */
}

/* Botão de calcular com contraste e centralizado */
.stButton {
    text-align: center;
}
.stButton > button {
    background-color: #007bff;  /* Azul para destaque */
    color: white;  /* Texto branco para contraste */
}

/* Resultado de sucesso com contraste */
.stAlert {
    background-color: #d4edda;  /* Verde claro */
    color: #155724;  /* Verde escuro para texto */
}
</style>
""", unsafe_allow_html=True)

# Interface Streamlit
st.title("Final Score Calculator for Zama Creators ")

# Texto de introdução baseado na imagem
st.write("This tool is based on the formulas provided by Zama . Your actual score will depend on human analysis factors performed by the team. **Share the link with the Zama community!**")

# Frase realçada (em negrito e com destaque)
st.markdown("""<p style="font-weight: bold; font-size: 18px;">Enter the values below and click 'Calculate' to get your score.</p>
""", unsafe_allow_html=True)
# Inputs
smart_followers = st.number_input("**Smart Followers**", min_value=0.0, value=0.0)
impressions = st.number_input("**Impressions**", min_value=0.0, value=0.0)
likes = st.number_input("**Likes**", min_value=0.0, value=0.0)
retweets = st.number_input("**Retweets (RT)**", min_value=0.0, value=0.0)
quotes = st.number_input("**Quotes**", min_value=0.0, value=0.0)
followers = st.number_input("**Followers**", min_value=0.0, value=1.0)  # Evita divisão por zero
posts = st.number_input("**Posts**", min_value=0.0, value=0.0)
smart_engagement = st.number_input("**Smart Engagement (if you don't know, use 0)**", min_value=0.0, value=0.0)

if st.button("Calculate the finalscore"):
    result = calculate_final_score(smart_followers, impressions, likes, retweets, quotes, followers, posts, smart_engagement)
    st.success(f"**Your final score is: {result:.2f}**")

# Rodapé separado com hyperlinks e botões de follow do X
st.markdown("""
<p style="font-size: 18px; font-weight: bold;">
Developed by <a href="https://x.com/Unnamed_Degen">@unnamed_degen</a> for <a href="https://x.com/zama_fhe">@zama_fhe</a>. Follow us on X.
</p>
""", unsafe_allow_html=True)
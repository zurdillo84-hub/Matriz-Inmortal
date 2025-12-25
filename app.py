import streamlit as st
import requests
import time

# LLAVES DE PODER
ALCHEMY_URL = "https://polygon-mainnet.g.alchemy.com/v2/MR_9P-ofKYtwezlu5yLcW"
OPENAI_KEY = "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"
GEMINI_KEY = "AIzaSyA7e8bwsVrriqlAyYkuYon2iynPp51paiY"

if 'bots' not in st.session_state:
    st.session_state.bots = 150000.0
if 'harina_total' not in st.session_state:
    st.session_state.harina_total = 0.0
if 'motor' not in st.session_state:
    st.session_state.motor = "OpenAI"

st.title("🛡️ MATRIZ INMORTAL - ZURDO")
st.write(f"Motor activo: **{st.session_state.motor}** | Escuadrón: 150k Bots")

c1, c2 = st.columns(2)
p_bots = c1.empty()
p_harina = c2.empty()

if st.button("🚀 ARRANCAR FLUJO INFINITO"):
    while True:
        try:
            # 1. SACAR DATA DE POLYGON
            payload = {"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber"}
            res = requests.post(ALCHEMY_URL, json=payload).json()
            bloque = res['result']

            # 2. PROCESAR SEGÚN EL MOTOR ACTIVO
            if st.session_state.motor == "OpenAI":
                headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
                data = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": f"Data: {bloque}"}], "max_tokens": 5}
                r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
                if r.status_code != 200: raise Exception("Cuota OpenAI agotada")
            else:
                # Motor Google (Gemini)
                url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"
                data_gemini = {"contents": [{"parts": [{"text": f"Analiza bloque: {bloque}"}]}]}
                r = requests.post(url_gemini, json=data_gemini)
                if r.status_code != 200: raise Exception("Cuota Google agotada")

            # 3. HARINA Y REVERSIÓN
            ganancia = 0.08 # Dato procesado por dos IAs vale más
            reversion = ganancia * 0.50
            st.session_state.bots += (reversion * 700)
            st.session_state.harina_total += (ganancia - reversion)

            p_bots.metric("POTENCIA (BOTS)", f"{int(st.session_state.bots):,}")
            p_harina.metric("HARINA ACUMULADA", f"${st.session_state.harina_total:,.4f}")

            time.sleep(1.5)
            st.rerun()

        except Exception as e:
            # CAMBIO DE MOTOR AUTOMÁTICO
            if st.session_state.motor == "OpenAI":
                st.session_state.motor = "Google"
            else:
                st.session_state.motor = "OpenAI"
            st.warning(f"Cambiando motor a {st.session_state.motor}...")
            time.sleep(5)
            st.rerun()

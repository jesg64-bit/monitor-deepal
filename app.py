import streamlit as st
from datetime import datetime, timedelta
import base64

st.set_page_config(page_title="Deepal S07 Monitor", page_icon="⚡")
st.title("🚗 Deepal S07: Monitor de Carga")

# --- SONIDO DE ALARMA ---
def play_alarm():
    # Sonido de campana profesional
    audio_url = "https://www.soundjay.com/buttons/beep-01a.mp3"
    audio_html = f"""
        <audio autoplay>
            <source src="{audio_url}" type="audio/mpeg">
        </audio>
    """
    st.components.v1.html(audio_html, height=0)

# --- CONFIGURACIÓN Y ENTRADAS ---
with st.sidebar:
    st.header("⚙️ Ajustes del Vehículo")
    capacidad = st.number_input("Capacidad Batería (kWh)", value=66.8)
    # Acepta decimales con step=0.1
    amperaje = st.number_input("Amperaje (A)", value=32.0, step=0.1, format="%.1f")

col1, col2 = st.columns(2)
with col1:
    voltaje = st.number_input("Voltaje (V)", value=220)
    actual = st.slider("Carga Actual (%)", 0, 100, 20)
with col2:
    objetivo = st.slider("Carga Objetivo (%)", 0, 100, 80)
    st.info(f"🕒 Hora actual: {datetime.now().strftime('%H:%M')}")

# --- CÁLCULO ---
if st.button("🚀 INICIAR MONITOR"):
    if actual >= objetivo:
        st.error("¡El objetivo debe ser mayor al actual!")
    else:
        potencia = (voltaje * amperaje) / 1000
        energia = capacidad * (objetivo - actual) / 100
        tiempo_decimal = energia / (potencia * 0.9) # 90% eficiencia
        
        # Hora de fin
        hora_fin = datetime.now() + timedelta(hours=tiempo_decimal)
        
        st.divider()
        st.balloons()
        st.success(f"### ✅ Carga lista a las: {hora_fin.strftime('%H:%M %p')}")
        
        c1, c2 = st.columns(2)
        c1.metric("Tiempo restante", f"{int(tiempo_decimal)}h {int((tiempo_decimal%1)*60)}m")
        c2.metric("Potencia Real", f"{potencia:.2f} kW")
        
        # Alarma visual y sonora
        st.warning(f"🔔 Desconecta a las {hora_fin.strftime('%H:%M')}")
        play_alarm()

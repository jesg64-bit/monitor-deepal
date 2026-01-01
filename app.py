import streamlit as st
from datetime import datetime, timedelta
import pytz # Para la hora exacta

# Configuración de página con fondo azul mediante CSS personalizado
st.set_page_config(page_title="Deepal S07 Digital Monitor", page_icon="⚡", layout="centered")

# CSS para fondo azul, letra blanca y tipografía digital
st.markdown("""
    <style>
    .stApp {
        background-color: #003366;
        color: white;
    }
    @font-face {
        font-family: 'Digital';
        src: url('https://fonts.cdnfonts.com/s/14101/digital-7.woff') format('woff');
    }
    .digital-font {
        font-family: 'Digital', sans-serif;
        font-size: 60px;
        color: #00FF00;
        text-align: center;
    }
    h1, h2, h3, p, span {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Deepal S07 Digital Monitor")

# --- VALORES FIJOS ---
BATTERY_CAPACITY = 31.87  # kWh fijo
FIXED_AMPERAGE = 22.6    # A fijo

# Zona horaria (Ajustada a UTC-5, común en nuestra región)
tz = pytz.timezone('America/Bogota') 
hora_actual = datetime.now(tz)

with st.container():
    st.subheader("Datos de Carga")
    col1, col2 = st.columns(2)
    
    with col1:
        voltaje = st.number_input("Voltaje (V)", value=220)
        st.write(f"**Batería:** {BATTERY_CAPACITY} kWh")
    
    with col2:
        actual_pct = st.slider("Carga Actual (%)", 0, 100, 20)
        target_pct = st.slider("Carga Objetivo (%)", 0, 100, 80)

# --- CÁLCULOS ---
if st.button("🚀 INICIAR CÁLCULO"):
    if actual_pct >= target_pct:
        st.error("La carga actual es mayor al objetivo.")
    else:
        # P = V * I / 1000
        potencia_kw = (voltaje * FIXED_AMPERAGE) / 1000
        energia_necesaria = BATTERY_CAPACITY * (target_pct - actual_pct) / 100
        # Tiempo con 90% eficiencia
        tiempo_horas = energia_necesaria / (potencia_kw * 0.9)
        
        # Hora de finalización
        hora_fin = datetime.now(tz) + timedelta(hours=tiempo_horas)
        
        # Formato de tiempo
        h = int(tiempo_horas)
        m = int((tiempo_horas - h) * 60)

        st.divider()
        
        # RESULTADOS CON ESTILO DIGITAL
        st.markdown("### HORA ESTIMADA DE FINALIZACIÓN:")
        st.markdown(f'<p class="digital-font">{hora_fin.strftime("%H:%M %p")}</p>', unsafe_allow_html=True)
        
        st.markdown("### TIEMPO RESTANTE DE CARGA:")
        st.markdown(f'<p class="digital-font">{h}h {m}m</p>', unsafe_allow_html=True)

        st.info(f"Potencia de carga: {potencia_kw:.2f} kW | Energía a recuperar: {energia_necesaria:.2f} kWh")import streamlit as st
from datetime import datetime, timedelta
import base64



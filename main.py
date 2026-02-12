import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Phoenix Empire 🔥", page_icon="🔥", layout="centered")

# Estilo visual Rojo y Negro
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #FF4B4B !important; text-align: center; }
    div.stButton > button {
        background-color: #FF4B4B;
        color: white;
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        text-align: center;
        border-color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'
        })
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")

# --- INTERFAZ ---
st.title("PHOENIX EMPIRE 🔥")
st.write("---")

st.markdown("### 🛡️ Acceso de Guerrero")
id_usuario = st.text_input("Ingresa tu ID de Jugador", placeholder="Ej: 123456", type="default")

if st.button("CONSULTAR ESTADO"):
    if id_usuario:
        # Buscamos en la ruta 'usuarios/ID'
        usuario_ref = db.reference(f'usuarios/{id_usuario}').get()
        
        if usuario_ref:
            st.success(f"¡Bienvenido al frente, {usuario_ref.get('nombre', 'Guerrero')}!")
            
            # Tarjetas de datos
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="💎 DIAMANTES", value=f"{usuario_ref.get('Diamantes', 0)}")
            with col2:
                st.metric(label="💰 DEUDA", value=f"{usuario_ref.get('deuda', 0)}")
            
            st.write("---")
            st.info(f"Rango actual: {usuario_ref.get('rol', 'Miembro')}")
        else:
            st.error("ID no encontrado en el sistema del Imperio.")
    else:
        st.warning("Por favor, ingresa un ID válido.")

st.caption("Phoenix Empire Control System © 2026")
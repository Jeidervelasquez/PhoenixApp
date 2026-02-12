import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE CONTROL", layout="wide")

if not firebase_admin._apps:
    cred = credentials.Certificate("llave.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})

# --- ESTILO ---
st.markdown("<style>h1, h2 {color: #E74C3C; text-align: center;} .stButton>button {background-color: #E74C3C; color: white;}</style>", unsafe_allow_html=True)

# --- MENÚ LATERAL (OPCIONES DEL PROGRAMA) ---
st.sidebar.title("🎮 MENÚ LÍDER")
opcion = st.sidebar.radio("Ir a:", ["Consultar ID", "Gestionar Diamantes/Deuda", "Ranking del Clan"])

# --- OPCIÓN 1: CONSULTAR ---
if opcion == "Consultar ID":
    st.title("🔍 CONSULTA DE GUERRERO")
    id_buscado = st.text_input("Ingresa el ID")
    if st.button("Buscar"):
        user = db.reference(f'usuarios/{id_buscado}').get()
        if user:
            st.subheader(f"Guerrero: {user.get('nombre')}")
            st.metric("💎 Diamantes", user.get('Diamantes', 0))
            st.metric("💰 Deuda", user.get('deuda', 0))
        else: st.error("No existe.")

# --- OPCIÓN 2: GESTIONAR (COMO EN TU PC) ---
elif opcion == "Gestionar Diamantes/Deuda":
    st.title("⚒️ PANEL DE CONTROL")
    id_gest = st.text_input("ID del Miembro")
    tipo = st.selectbox("¿Qué vas a modificar?", ["Diamantes", "Deuda"])
    cantidad = st.number_input("Cantidad", step=1)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ SUMAR"):
            ref = db.reference(f'usuarios/{id_gest}')
            datos = ref.get()
            if datos:
                actual = datos.get(tipo, 0)
                ref.update({tipo: actual + cantidad})
                st.success("¡Actualizado!")
    with col2:
        if st.button("➖ RESTAR"):
            ref = db.reference(f'usuarios/{id_gest}')
            datos = ref.get()
            if datos:
                actual = datos.get(tipo, 0)
                ref.update({tipo: max(0, actual - cantidad)})
                st.success("¡Actualizado!")

# --- OPCIÓN 3: RANKING ---
elif opcion == "Ranking del Clan":
    st.title("🏆 RANKING DE DIAMANTES")
    todos = db.reference('usuarios').get()
    if todos:
        lista = [{"Nombre": v.get('nombre'), "Diamantes": v.get('Diamantes', 0)} for v in todos.values()]
        lista_ordenada = sorted(lista, key=lambda x: x['Diamantes'], reverse=True)
        st.table(lista_ordenada)

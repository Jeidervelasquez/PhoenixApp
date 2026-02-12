
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE SYSTEM", layout="centered")

if not firebase_admin._apps:
    cred = credentials.Certificate("llave.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})

# Estilo Phoenix
st.markdown("<style>h1, h2 {color: #E74C3C; text-align: center;} .stButton>button {background-color: #E74C3C; color: white; border-radius:10px;}</style>", unsafe_allow_html=True)

# --- LOGIN ---
if 'usuario' not in st.session_state:
    st.title("🔥 PHOENIX EMPIRE 🔥")
    id_login = st.text_input("INGRESA TU ID DE GUERRERO", type="password")
    if st.button("ACCEDER"):
        res = db.reference(f'usuarios/{id_login}').get()
        if res:
            st.session_state['usuario'] = res
            st.session_state['id_actual'] = id_login
            st.rerun()
        else:
            st.error("ID no reconocido por el Imperio.")
else:
    user = st.session_state['usuario']
    rol = user.get('rol', 'Miembro') # Lee el rol de Firebase
    
    st.sidebar.title(f"Bienvenido, {user.get('nombre')}")
    st.sidebar.write(f"Rango: **{rol}**")
    
    # --- MENÚ SEGÚN ROL ---
    opciones = ["Mi Perfil"]
    if rol in ["Líder", "Moderador"]:
        opciones.append("Gestionar Miembros")
    if rol == "Líder":
        opciones.append("Panel de Administración")
    
    menu = st.sidebar.radio("Navegación", opciones)

    # --- VISTA: MI PERFIL (Para todos) ---
    if menu == "Mi Perfil":
        st.title("🛡️ ESTADO DEL GUERRERO")
        col1, col2 = st.columns(2)
        col1.metric("💎 DIAMANTES", user.get('Diamantes', 0))
        col2.metric("💰 DEUDA", user.get('deuda', 0))
        
    # --- VISTA: GESTIÓN (Moderadores y Líder) ---
    elif menu == "Gestionar Miembros":
        st.title("⚒️ CONTROL DE ESCUADRÓN")
        id_edit = st.text_input("ID del Miembro a modificar")
        cantidad = st.number_input("Cantidad", step=1)
        
        c1, c2 = st.columns(2)
        if c1.button("➕ SUMAR DIAMANTES"):
            ref = db.reference(f'usuarios/{id_edit}')
            u = ref.get()
            if u:
                ref.update({"Diamantes": u.get('Diamantes', 0) + cantidad})
                st.success("Diamantes sumados.")
        if c2.button("➕ ANOTAR DEUDA"):
            ref = db.reference(f'usuarios/{id_edit}')
            u = ref.get()
            if u:
                ref.update({"deuda": u.get('deuda', 0) + cantidad})
                st.success("Deuda actualizada.")

    # --- VISTA: ADMIN (Solo Líder) ---
    elif menu == "Panel de Administración":
        st.title("👑 COMANDO CENTRAL")
        st.write("Aquí puedes ver a todos los miembros y sus rangos.")
        todos = db.reference('usuarios').get()
        if todos:
            st.table([{"ID": k, "Nombre": v.get('nombre'), "Rol": v.get('rol')} for k, v in todos.items()])

    if st.sidebar.button("Cerrar Sesión"):
        del st.session_state['usuario']
        st.rerun()

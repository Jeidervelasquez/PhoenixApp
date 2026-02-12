
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. CONFIGURACIÓN Y CONEXIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE SYSTEM", layout="centered")

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'
        })
    except:
        st.error("Error: No se encontró el archivo llave.json")

# Estilo visual (Rojo y Negro)
st.markdown("<style>h1, h2 {color: #E74C3C; text-align: center;} .stButton>button {background-color: #E74C3C; color: white; width: 100%; border-radius:10px; font-weight: bold;}</style>", unsafe_allow_html=True)

# --- 2. SISTEMA DE LOGIN Y REGISTRO ---
if 'usuario' not in st.session_state:
    st.title("🔥 PHOENIX EMPIRE 🔥")
    tab_login, tab_registro = st.tabs(["INICIAR SESIÓN", "REGISTRARSE"])

    with tab_login:
        id_login = st.text_input("ID DE GUERRERO", key="id_log")
        if st.button("ACCEDER AL SISTEMA"):
            res = db.reference(f'usuarios/{id_login}').get()
            if res:
                st.session_state['usuario'] = res
                st.session_state['id_actual'] = id_login
                st.rerun()
            else:
                st.error("ID no registrado.")

    with tab_registro:
        st.subheader("📝 UNIRSE AL IMPERIO")
        nuevo_id = st.text_input("Define tu ID")
        nuevo_nombre = st.text_input("Tu Nombre/Nick")
        if st.button("REGISTRARME"):
            if nuevo_id and nuevo_nombre:
                db.reference(f'usuarios/{nuevo_id}').set({
                    'nombre': nuevo_nombre,
                    'Diamantes': 0,
                    'deuda': 0,
                    'rol': 'Miembro'
                })
                st.success("¡Registro exitoso! Ya puedes iniciar sesión.")
            else:
                st.warning("Completa todos los campos.")

# --- 3. PANEL DE CONTROL (DENTRO DEL SISTEMA) ---
else:
    user = st.session_state['usuario']
    id_yo = st.session_state['id_actual']
    # Recargar datos frescos de la DB
    datos_frescos = db.reference(f'usuarios/{id_yo}').get()
    rol = datos_frescos.get('rol', 'Miembro')

    st.sidebar.title(f"👤 {datos_frescos.get('nombre')}")
    st.sidebar.write(f"Rango: **{rol}**")
    
    opciones = ["📊 Mi Perfil", "🏆 Ranking"]
    if rol in ["Líder", "Moderador"]:
        opciones.append("⚒️ Gestionar Miembros")
    if rol == "Líder":
        opciones.append("👑 Panel de Control")
    
    menu = st.sidebar.radio("MENÚ", opciones)

    # VISTA: MI PERFIL
    if menu == "📊 Mi Perfil":
        st.title("🛡️ ESTADO DEL GUERRERO")
        c1, c2 = st.columns(2)
        c1.metric("💎 DIAMANTES", datos_frescos.get('Diamantes', 0))
        c2.metric("💰 DEUDA", datos_frescos.get('deuda', 0))

    # VISTA: GESTIÓN (MODERADORES Y LÍDER)
    elif menu == "⚒️ Gestionar Miembros":
        st.title("⚒️ GESTIÓN DE ESCUADRÓN")
        id_target = st.text_input("ID del Miembro a modificar")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        
        col_d, col_v = st.columns(2)
        if col_d.button("➕ SUMAR DIAMANTES"):
            ref = db.reference(f'usuarios/{id_target}')
            u = ref.get()
            if u:
                ref.update({"Diamantes": u.get('Diamantes', 0) + cantidad})
                st.success("Actualizado en la Base de Datos.")
            else: st.error("ID no existe.")
            
        if col_v.button("➕ SUMAR DEUDA"):
            ref = db.reference(f'usuarios/{id_target}')
            u = ref.get()
            if u:
                ref.update({"deuda": u.get('deuda', 0) + cantidad})
                st.success("Deuda anotada.")
            else: st.error("ID no existe.")

    # VISTA: RANKING
    elif menu == "🏆 Ranking":
        st.title("🏆 TOP DIAMANTES")
        todos = db.reference('usuarios').get()
        if todos:
            lista = [{"Nombre": v.get('nombre'), "💎": v.get('Diamantes', 0)} for v in todos.values()]
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))

    if st.sidebar.button("SALIR"):
        del st.session_state['usuario']
        st.rerun()

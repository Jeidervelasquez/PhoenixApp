import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. CONEXIÓN ---
if not firebase_admin._apps:
    cred = credentials.Certificate("llave.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})

# --- 2. CONFIGURACIÓN DE ROLES (EL SECRETO) ---
# Aquí pon tu ID de Free Fire. Con este ID, la App siempre te dará permisos de Líder.
ID_MAESTRO_LIDER = "TU_ID_AQUÍ" 

def obtener_rol_real(user_id, datos_db):
    # Si el ID coincide con el tuyo, eres Líder automáticamente
    if str(user_id) == ID_MAESTRO_LIDER:
        return "Líder"
    # Si no, buscamos lo que diga la base de datos (sea lo que sea que guarde tu PC)
    rol_db = str(datos_db.get('rol', 'Miembro')).upper()
    if "LIDER" in rol_db or "ADMIN" in rol_db:
        return "Líder"
    if "MOD" in rol_db or "MODERADOR" in rol_db:
        return "Moderador"
    return "Miembro"

# --- 3. LOGIN Y PANTALLA PRINCIPAL ---
if 'usuario' not in st.session_state:
    st.title("🔥 PHOENIX EMPIRE 🔥")
    id_log = st.text_input("INGRESA TU ID")
    if st.button("ACCEDER"):
        res = db.reference(f'usuarios/{id_log}').get()
        if res:
            st.session_state['usuario'] = res
            st.session_state['id_actual'] = id_log
            st.rerun()
else:
    id_yo = st.session_state['id_actual']
    datos = db.reference(f'usuarios/{id_yo}').get()
    
    # Aplicamos la lógica de la Llave Maestra
    rol_efectivo = obtener_rol_real(id_yo, datos)
    
    st.sidebar.title(f"🛡️ {datos.get('nombre')}")
    st.sidebar.write(f"RANGO: **{rol_efectivo}**")

    # Menú dinámico según el rol detectado
    opciones = ["📊 Mi Perfil", "🏆 Ranking"]
    if rol_efectivo in ["Líder", "Moderador"]:
        opciones.append("⚒️ Gestionar Miembros")
    if rol_efectivo == "Líder":
        opciones.append("👑 Panel de Control")
        opciones.append("📝 Registrar Miembro")

    menu = st.sidebar.radio("MENÚ", opciones)

    # --- AQUÍ VAN LAS FUNCIONES (GESTIÓN, RANKING, ETC.) ---
    if menu == "📊 Mi Perfil":
        st.header("ESTADO DE GUERRERO")
        st.metric("💎 DIAMANTES", datos.get('Diamantes', 0))
        st.metric("💰 DEUDA", datos.get('deuda', 0))

    elif menu == "⚒️ Gestionar Miembros":
        st.header("GESTIÓN DE SALDOS")
        target = st.text_input("ID del Miembro")
        cant = st.number_input("Cantidad", step=1)
        if st.button("SUMAR DIAMANTES"):
            ref = db.reference(f'usuarios/{target}')
            u = ref.get()
            if u:
                ref.update({"Diamantes": u.get('Diamantes', 0) + cant})
                st.success("¡Hecho!")
    
    elif menu == "👑 Panel de Control":
        st.header("COMANDO CENTRAL")
        todos = db.reference('usuarios').get()
        if todos:
            for k, v in todos.items():
                st.write(f"ID: {k} | Nombre: {v.get('nombre')} | Rol: {v.get('rol')}")

    if st.sidebar.button("CERRAR SESIÓN"):
        del st.session_state['usuario']
        st.rerun()

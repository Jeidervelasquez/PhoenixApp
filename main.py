
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="SISTEMA CENTRAL PHOENIX", layout="wide")

# Estilo para que no se vea vacío y tenga los colores del clan
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    h1, h2, h3 { color: #FF4B4B !important; text-align: center; }
    .css-1r6slb0 { background-color: #1c1f26; border-radius: 10px; padding: 20px; border: 1px solid #FF4B4B; }
    .stButton>button { background-color: #FF4B4B; color: white; width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN ---
if not firebase_admin._apps:
    cred = credentials.Certificate("llave.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})

# --- 3. TU ID MAESTRO ---
ID_DEL_LIDER = "TU_ID_AQUÍ"  # <--- COLOCA TU ID AQUÍ

# --- 4. LÓGICA DE LOGIN ---
if 'usuario' not in st.session_state:
    st.title("🔥 PHOENIX EMPIRE 🔥")
    col1, col2 = st.tabs(["ACCESO", "NUEVO REGISTRO"])
    with col1:
        id_log = st.text_input("INGRESA TU ID")
        if st.button("INICIAR SESIÓN"):
            res = db.reference(f'usuarios/{id_log}').get()
            if res:
                st.session_state['usuario'] = res
                st.session_state['id_actual'] = id_log
                st.rerun()
            else: st.error("ID no registrado.")
    with col2:
        n_id = st.text_input("ID Nuevo")
        n_nom = st.text_input("Nombre de Jugador")
        if st.button("REGISTRAR"):
            db.reference(f'usuarios/{n_id}').set({'nombre': n_nom, 'Diamantes': 0, 'deuda': 0, 'rol': 'Miembro'})
            st.success("Registrado.")

# --- 5. INTERFAZ COMPLETA (Clon del Programa de PC) ---
else:
    id_yo = st.session_state['id_actual']
    # Sincronización real
    datos = db.reference(f'usuarios/{id_yo}').get()
    
    # Determinar Rango (Prioridad a tu ID Maestro)
    rol_real = "Líder" if str(id_yo) == ID_DEL_LIDER else datos.get('rol', 'Miembro')

    st.sidebar.title(f"👤 {datos.get('nombre')}")
    st.sidebar.write(f"Rango: **{rol_real}**")
    
    menu = st.sidebar.selectbox("MENÚ DE COMANDO", 
        ["ESTADO ACTUAL", "RANKING GENERAL", "MODIFICAR DIAMANTES", "MODIFICAR DEUDAS", "LISTA DE MIEMBROS", "BUSCADOR AVANZADO"])

    # --- PANTALLA: ESTADO ACTUAL ---
    if menu == "ESTADO ACTUAL":
        st.title("🛡️ PANEL DE GUERRERO")
        c1, c2 = st.columns(2)
        with c1: st.metric("💎 MIS DIAMANTES", datos.get('Diamantes', 0))
        with c2: st.metric("💰 MI DEUDA", datos.get('deuda', 0))
        st.write("---")
        st.info(f"Bienvenido de nuevo al sistema, {datos.get('nombre')}.")

    # --- PANTALLA: RANKING ---
    elif menu == "RANKING GENERAL":
        st.title("🏆 TOP DIAMANTES")
        all_u = db.reference('usuarios').get()
        if all_u:
            # Convertimos a lista para ordenar
            lista = [{"Nombre": v.get('nombre'), "Diamantes": v.get('Diamantes', 0)} for v in all_u.values()]
            ranking = sorted(lista, key=lambda x: x['Diamantes'], reverse=True)
            st.table(ranking)

    # --- PANTALLA: GESTIÓN DE DIAMANTES ---
    elif menu == "MODIFICAR DIAMANTES":
        if rol_real in ["Líder", "Moderador"]:
            st.title("⚒️ EDITOR DE DIAMANTES")
            t_id = st.text_input("ID del Miembro")
            cant = st.number_input("Cantidad", min_value=1, step=1)
            col_a, col_b = st.columns(2)
            if col_a.button("➕ SUMAR"):
                ref = db.reference(f'usuarios/{t_id}')
                u = ref.get()
                if u: ref.update({"Diamantes": u.get('Diamantes', 0) + cant}); st.success("Actualizado")
            if col_b.button("➖ RESTAR"):
                ref = db.reference(f'usuarios/{t_id}')
                u = ref.get()
                if u: ref.update({"Diamantes": max(0, u.get('Diamantes', 0) - cant)}); st.success("Actualizado")
        else: st.error("Acceso denegado.")

    # --- PANTALLA: DEUDAS ---
    elif menu == "MODIFICAR DEUDAS":
        if rol_real in ["Líder", "Moderador"]:
            st.title("💰 EDITOR DE DEUDAS")
            d_id = st.text_input("ID del Miembro")
            d_cant = st.number_input("Monto de Deuda", min_value=1)
            if st.button("ACTUALIZAR DEUDA"):
                ref = db.reference(f'usuarios/{d_id}')
                u = ref.get()
                if u: ref.update({"deuda": u.get('deuda', 0) + d_cant}); st.success("Deuda anotada")
        else: st.error("Acceso denegado.")

    # --- PANTALLA: LISTA DE MIEMBROS ---
    elif menu == "LISTA DE MIEMBROS":
        st.title("📋 REGISTRO DEL CLAN")
        todos = db.reference('usuarios').get()
        if todos:
            for k, v in todos.items():
                with st.expander(f"Guerrero: {v.get('nombre')} (ID: {k})"):
                    st.write(f"Rol: {v.get('rol')}")
                    st.write(f"Diamantes: {v.get('Diamantes')}")
                    if rol_real == "Líder":
                        if st.button(f"ELIMINAR MIEMBRO {k}"):
                            db.reference(f'usuarios/{k}').delete()
                            st.rerun()

    # --- PANTALLA: BUSCADOR (Igual al del PC) ---
    elif menu == "BUSCADOR AVANZADO":
        st.title("🔍 BUSCADOR DE GUERREROS")
        search_id = st.text_input("Ingresa el ID para ver todo el historial")
        if search_id:
            buscado = db.reference(f'usuarios/{search_id}').get()
            if buscado:
                st.subheader(f"Resultados para: {buscado.get('nombre')}")
                st.json(buscado)
            else: st.warning("No se encontró ese ID.")

    if st.sidebar.button("SALIR DEL SISTEMA"):
        del st.session_state['usuario']
        st.rerun()

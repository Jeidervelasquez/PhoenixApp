import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE", layout="centered")

if not firebase_admin._apps:
    cred = credentials.Certificate("llave.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})

# --- TU ID MAESTRO ---
ID_LIDER_MAESTRO = "TU_ID_AQUÍ" 

# --- ESTILOS DE BOTONES ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: white; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3.5em; border: none; width: 100%; }
    div.stButton > button:first-child { background-color: #1f538d; color: white; } /* Azul por defecto */
    .btn-volver button { background-color: #606060 !important; }
    .btn-rojo button { background-color: #FF0000 !important; }
    .btn-verde button { background-color: #2fa572 !important; }
    </style>
    """, unsafe_allow_html=True)

# Inicializar el estado de la ventana si no existe
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'login'

# --- FUNCIÓN PARA CAMBIAR DE VENTANA ---
def navegar_a(nombre_pagina):
    st.session_state['pagina'] = nombre_pagina
    st.rerun()

# --- LÓGICA DE VENTANAS ---

# 1. VENTANA DE LOGIN
if st.session_state['pagina'] == 'login':
    st.markdown("<h1 style='color: #E74C3C; text-align: center;'>Phoenix Empire<br>escuadrón 🔥</h1>", unsafe_allow_html=True)
    id_log = st.text_input("ID de Jugador", key="login_id")
    if st.button("ENTRAR"):
        res = db.reference(f'usuarios/{id_log}').get()
        if res:
            st.session_state['usuario'] = res
            st.session_state['id_actual'] = id_log
            navegar_a('menu')
        else:
            st.error("ID no registrado")

# 2. VENTANA MENÚ PRINCIPAL (Solo se ve esto al entrar)
elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    id_yo = st.session_state['id_actual']
    rol = "Lider" if str(id_yo) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')
    
    st.markdown(f"<h1 style='color: #3b8ed0; text-align: center;'>PANEL DE {rol.upper()}</h1>", unsafe_allow_html=True)
    st.write(f"**Bienvenido:** {u.get('nombre')}")
    st.divider()

    # BOTONES QUE CAMBIAN LA VENTANA
    if rol == "Lider":
        if st.button("📊 RANKING Y DEUDAS"): navegar_a('ranking')
        if st.button("📝 REGISTRAR MIEMBRO"): navegar_a('registro')
        if st.button("💎 GESTIONAR DIAMANTES"): navegar_a('diamantes')
        if st.button("🔧 CAMBIAR ID / CUENTAS"): navegar_a('cambio_id')
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): navegar_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    if rol in ["Lider", "Moderador"]:
        if st.button("📅 CREAR EVENTO"): navegar_a('crear_evento')

    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DEL CLAN"): navegar_a('lista')
    if st.button("🏆 EVENTOS Y PARTICIPAR"): navegar_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚪 CERRAR SESIÓN"):
        del st.session_state['usuario']
        navegar_a('login')

# 3. VENTANAS ESPECÍFICAS (Se reemplazan una a la otra)
else:
    # Botón para volver siempre visible en las sub-ventanas
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"):
        navegar_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    pag = st.session_state['pagina']

    if pag == 'ranking':
        st.subheader("🏆 Ranking y Deudas")
        us = db.reference('usuarios').get()
        if us:
            lista = [{"Nombre": v.get('nombre'), "💎": v.get('Diamantes',0), "💰": v.get('deuda',0)} for v in us.values()]
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))

    elif pag == 'registro':
        st.subheader("📝 Registrar Guerrero")
        r_id = st.text_input("ID Nuevo")
        r_nom = st.text_input("Nombre")
        r_rol = st.selectbox("Rango", ["Miembro", "Moderador", "Lider"])
        if st.button("GUARDAR REGISTRO"):
            db.reference(f'usuarios/{r_id}').set({'nombre': r_nom, 'rol': r_rol, 'Diamantes': 0, 'deuda': 0})
            st.success("Guardado correctamente")

    elif pag == 'diamantes':
        st.subheader("💎 Gestionar Diamantes")
        t_id = st.text_input("ID del Jugador")
        cant = st.number_input("Cantidad", min_value=1)
        if st.button("SUMAR DIAMANTES"):
            ref = db.reference(f'usuarios/{t_id}')
            data = ref.get()
            if data:
                ref.update({'Diamantes': data.get('Diamantes',0) + cant})
                st.success("Diamantes sumados")
        if st.button("ANOTAR DEUDA"):
            ref = db.reference(f'usuarios/{t_id}')
            data = ref.get()
            if data:
                ref.update({'deuda': data.get('deuda',0) + cant})
                st.warning("Deuda registrada")

    elif pag == 'lista':
        st.subheader("📋 Miembros del Clan")
        us = db.reference('usuarios').get()
        if us:
            for k, v in us.items():
                st.text(f"ID: {k} | {v.get('nombre')} ({v.get('rol')})")

    elif pag == 'ver_eventos':
        st.subheader("🏆 Eventos del Imperio")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                with st.expander(f"EVENTO: {info['nombre']}"):
                    st.write(info['descripcion'])
                    st.caption(f"Fecha: {info['fecha']}")


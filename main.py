
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE CONTROL", layout="centered")

if not firebase_admin._apps:
    cred = credentials.Certificate("llave.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})

# --- TU ID MAESTRO ---
ID_LIDER_MAESTRO = "TU_ID_AQUÍ" 

# --- ESTILOS ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: white; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3.5em; width: 100%; border: none; }
    .btn-menu button { background-color: #1f538d !important; color: white; margin-bottom: 10px; }
    .btn-volver button { background-color: #606060 !important; color: white; }
    .btn-rojo button { background-color: #FF0000 !important; color: white; }
    .btn-verde button { background-color: #2fa572 !important; color: white; }
    .card { background-color: #262626; padding: 20px; border-radius: 10px; border: 1px solid #E74C3C; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'login'

def navegar(pag):
    st.session_state['pagina'] = pag
    st.rerun()

# --- LÓGICA DE NAVEGACIÓN ---

if st.session_state['pagina'] == 'login':
    st.markdown("<h1 style='color: #E74C3C; text-align: center;'>Phoenix Empire 🔥</h1>", unsafe_allow_html=True)
    id_log = st.text_input("ID DE GUERRERO", key="id_log")
    if st.button("ENTRAR AL IMPERIO"):
        res = db.reference(f'usuarios/{id_log}').get()
        if res:
            st.session_state['usuario'] = res
            st.session_state['id_actual'] = id_log
            navegar('menu')
        else: st.error("ID no registrado.")

elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    id_yo = st.session_state['id_actual']
    rol = "Lider" if str(id_yo) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')

    st.markdown(f"<h1 style='color: #3b8ed0; text-align: center;'>PANEL DE {rol.upper()}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Guerrero: <b>{u.get('nombre')}</b></p>", unsafe_allow_html=True)
    
    # BOTONES DE NAVEGACIÓN
    st.markdown('<div class="btn-menu">', unsafe_allow_html=True)
    if rol == "Lider":
        if st.button("📊 RANKING Y DEUDAS"): navegar('ranking')
        if st.button("📝 REGISTRAR MIEMBRO"): navegar('registro')
        if st.button("💎 GESTIONAR DIAMANTES"): navegar('diamantes')
        if st.button("⚠️ SANCIONES (NUEVO)"): navegar('sanciones')
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): navegar('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DEL CLAN"): navegar('lista')
    if st.button("🏆 EVENTOS"): navegar('eventos')
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): navegar('login')
    st.markdown('</div>', unsafe_allow_html=True)

# --- VENTANAS DE FUNCIONES ---
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): navegar('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    st.divider()

    pag = st.session_state['pagina']

    if pag == 'ranking':
        st.header("🏆 Top del Escuadrón")
        us = db.reference('usuarios').get()
        if us:
            for uid, info in sorted(us.items(), key=lambda x: x[1].get('Diamantes',0), reverse=True):
                st.markdown(f"""<div class='card'>
                    <b>{info.get('nombre')}</b> (ID: {uid})<br>
                    💎 Diamantes: {info.get('Diamantes',0)} | 💰 Deuda: {info.get('deuda',0)}
                </div>""", unsafe_allow_html=True)

    elif pag == 'sanciones':
        st.header("⚠️ Control de Sanciones")
        target_id = st.text_input("ID del Guerrero a sancionar")
        motivo = st.text_input("Motivo de la sanción")
        if st.button("APLICAR SANCIÓN"):
            ref = db.reference(f'usuarios/{target_id}')
            data = ref.get()
            if data:
                sanciones_actuales = data.get('sanciones', 0)
                ref.update({'sanciones': sanciones_actuales + 1})
                st.error(f"Sanción aplicada a {data.get('nombre')}. Total: {sanciones_actuales + 1}")
            else: st.warning("ID no encontrado.")
        
        st.divider()
        st.subheader("Lista de Sancionados")
        todos = db.reference('usuarios').get()
        if todos:
            for k, v in todos.items():
                if v.get('sanciones', 0) > 0:
                    st.write(f"🚫 **{v['nombre']}**: {v['sanciones']} sanciones. (Motivo: {motivo if motivo else 'No especificado'})")

    elif pag == 'diamantes':
        st.header("💎 Gestión de Diamantes")
        id_d = st.text_input("ID del Jugador")
        cant = st.number_input("Cantidad", min_value=1)
        col1, col2 = st.columns(2)
        if col1.button("➕ SUMAR"):
            ref = db.reference(f'usuarios/{id_d}')
            u = ref.get()
            if u: ref.update({'Diamantes': u.get('Diamantes',0) + cant}); st.success("💎 Sumados")
        if col2.button("➕ DEUDA"):
            ref = db.reference(f'usuarios/{id_d}')
            u = ref.get()
            if u: ref.update({'deuda': u.get('deuda',0) + cant}); st.warning("💰 Deuda anotada")

    elif pag == 'lista':
        st.header("📋 Miembros Registrados")
        us = db.reference('usuarios').get()
        if us:
            for k, v in us.items():
                st.markdown(f"**ID:** `{k}` | **Nombre:** {v.get('nombre')} | **Sanciones:** {v.get('sanciones', 0)}")

    elif pag == 'registro':
        st.header("📝 Nuevo Registro")
        n_id = st.text_input("ID Nuevo")
        n_nom = st.text_input("Nombre")
        n_rol = st.selectbox("Rol", ["Miembro", "Moderador", "Lider"])
        if st.button("GUARDAR EN FIREBASE"):
            db.reference(f'usuarios/{n_id}').set({'nombre': n_nom, 'rol': n_rol, 'Diamantes': 0, 'deuda': 0, 'sanciones': 0})
            st.success("¡Guerrero registrado con éxito!")

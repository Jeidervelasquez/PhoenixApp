
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE TOTAL", layout="centered")

if not firebase_admin._apps:
    cred = credentials.Certificate("llave.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})

# --- TU ID MAESTRO (PONLO AQUÍ) ---
ID_LIDER_MAESTRO = "PON_TU_ID_AQUI" 

# --- ESTILOS VISUALES (IGUAL AL PC) ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: white; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3.5em; width: 100%; border: none; margin-bottom: 10px; }
    
    /* CLASES DE COLORES */
    div.row-widget.stButton > button[kind="primary"] { background-color: #1f538d; }
    
    .btn-azul button { background-color: #1f538d !important; color: white; }
    .btn-verde button { background-color: #2fa572 !important; color: white; }
    .btn-gris button { background-color: #606060 !important; color: white; }
    .btn-rojo button { background-color: #FF0000 !important; color: white; }
    .btn-volver button { background-color: #333333 !important; border: 1px solid white; color: white; }
    
    h1, h2, h3 { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- GESTIÓN DE NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state['pagina'] = 'login'

def ir_a(pagina):
    st.session_state['pagina'] = pagina
    st.rerun()

# ==========================================
# 1. PANTALLA DE LOGIN
# ==========================================
if st.session_state['pagina'] == 'login':
    st.markdown("<h1 style='color: #E74C3C;'>PHOENIX EMPIRE<br>ESCUADRÓN 🔥</h1>", unsafe_allow_html=True)
    id_input = st.text_input("INGRESA TU ID DE JUGADOR")
    
    if st.button("ENTRAR AL SISTEMA"):
        if id_input:
            res = db.reference(f'usuarios/{id_input}').get()
            if res:
                st.session_state['usuario'] = res
                st.session_state['id_actual'] = id_input
                ir_a('menu')
            else:
                st.error("ID no encontrado en la base de datos.")

# ==========================================
# 2. MENÚ PRINCIPAL (TODAS LAS OPCIONES)
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    my_id = st.session_state['id_actual']
    
    # Lógica de Rol Maestro
    rol = "Lider" if str(my_id) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')

    st.markdown(f"<h2 style='color: #3b8ed0;'>PANEL DE CONTROL: {rol.upper()}</h2>", unsafe_allow_html=True)
    st.info(f"Bienvenido, {u.get('nombre')}")

    # --- BLOQUE DE LÍDER ---
    if rol == "Lider":
        st.markdown("### 🛠️ GESTIÓN")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 RANKING"): ir_a('ranking')
            if st.button("💎 DIAMANTES/DEUDA"): ir_a('diamantes')
            if st.button("⚠️ SANCIONES (NUEVO)"): ir_a('sanciones')
        with col2:
            if st.button("📝 REGISTRAR"): ir_a('registro')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')

        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    # --- BLOQUE DE MODERADOR ---
    elif rol == "Moderador":
        st.markdown("### 🛠️ GESTIÓN")
        if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
        if st.button("💎 GESTIONAR DIAMANTES"): ir_a('diamantes')
    
    # --- BLOQUE GENERAL (TODOS) ---
    st.markdown("### 🌎 CLAN")
    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DE MIEMBROS"): ir_a('lista')
    if st.button("🏆 VER EVENTOS"): ir_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. PANTALLAS DE FUNCIONES
# ==========================================
else:
    # Botón Volver SIEMPRE ARRIBA
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag = st.session_state['pagina']

    # --- RANKING ---
    if pag == 'ranking':
        st.header("🏆 RANKING Y DEUDAS")
        data = db.reference('usuarios').get()
        if data:
            lista = [{"Nombre": v['nombre'], "💎": v.get('Diamantes',0), "💰": v.get('deuda',0)} for v in data.values()]
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))

    # --- DIAMANTES Y DEUDAS ---
    elif pag == 'diamantes':
        st.header("💎 GESTIÓN DE TESORERÍA")
        target = st.text_input("ID del Jugador")
        cant = st.number_input("Cantidad", step=1, min_value=1)
        c1, c2 = st.columns(2)
        if c1.button("➕ SUMAR DIAMANTES"):
            ref = db.reference(f'usuarios/{target}')
            curr = ref.get()
            if curr:
                ref.update({'Diamantes': curr.get('Diamantes',0) + cant})
                st.success("Diamantes sumados.")
            else: st.error("ID no existe")
            
        if c2.button("➕ ANOTAR DEUDA"):
            ref = db.reference(f'usuarios/{target}')
            curr = ref.get()
            if curr:
                ref.update({'deuda': curr.get('deuda',0) + cant})
                st.warning("Deuda anotada.")
            else: st.error("ID no existe")

    # --- SANCIONES (NUEVO) ---
    elif pag == 'sanciones':
        st.header("⚠️ TRIBUNAL DE SANCIONES")
        st.write("Aplica faltas a los miembros que rompan las reglas.")
        
        s_id = st.text_input("ID del Infractor")
        motivo = st.text_input("Motivo (Opcional)")
        
        if st.button("APLICAR SANCIÓN (+1)"):
            ref = db.reference(f'usuarios/{s_id}')
            u = ref.get()
            if u:
                nuevas_sanciones = u.get('sanciones', 0) + 1
                ref.update({'sanciones': nuevas_sanciones})
                st.error(f"Sanción aplicada a {u['nombre']}. Total: {nuevas_sanciones}")
            else: st.error("Usuario no encontrado.")

        st.subheader("Lista de Sancionados")
        all_u = db.reference('usuarios').get()
        if all_u:
            for k, v in all_u.items():
                if v.get('sanciones', 0) > 0:
                    st.write(f"🚫 **{v['nombre']}**: {v['sanciones']} faltas.")

    # --- REGISTRO ---
    elif pag == 'registro':
        st.header("📝 NUEVO GUERRERO")
        r_id = st.text_input("ID Nuevo")
        r_nom = st.text_input("Nombre")
        r_rol = st.selectbox("Rol", ["Miembro", "Moderador", "Lider"])
        if st.button("REGISTRAR"):
            db.reference(f'usuarios/{r_id}').set({
                'nombre': r_nom, 'rol': r_rol, 'Diamantes': 0, 'deuda': 0, 'sanciones': 0
            })
            st.success("Usuario creado correctamente.")

    # --- CAMBIO DE ID ---
    elif pag == 'cambio_id':
        st.header("🔧 CAMBIO DE CUENTA")
        old = st.text_input("ID Antiguo")
        new = st.text_input("ID Nuevo")
        if st.button("TRASPASAR DATOS"):
            ref_old = db.reference(f'usuarios/{old}')
            data = ref_old.get()
            if data:
                db.reference(f'usuarios/{new}').set(data)
                ref_old.delete()
                st.success("Cuenta migrada con éxito.")
            else: st.error("ID antiguo no existe.")

    # --- ELIMINAR ---
    elif pag == 'eliminar':
        st.header("❌ ZONA DE PELIGRO")
        del_id = st.text_input("ID a Eliminar")
        if st.button("ELIMINAR DEFINITIVAMENTE"):
            db.reference(f'usuarios/{del_id}').delete()
            st.warning("Usuario eliminado.")

    # --- CREAR EVENTO ---
    elif pag == 'crear_evento':
        st.header("📅 NUEVO EVENTO")
        e_tit = st.text_input("Título")
        e_fecha = st.text_input("Fecha/Hora")
        e_desc = st.text_area("Descripción")
        if st.button("PUBLICAR"):
            db.reference('eventos').push().set({
                'nombre': e_tit, 'fecha': e_fecha, 'descripcion': e_desc
            })
            st.success("Evento publicado.")

    # --- VER EVENTOS ---
    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS ACTIVOS")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                with st.expander(f"🔥 {info['nombre']} ({info['fecha']})"):
                    st.write(info['descripcion'])
                    if st.button("Asistiré", key=eid):
                        st.success("Te has anotado.")

    # --- LISTA ---
    elif pag == 'lista':
        st.header("📋 LISTA DEL CLAN")
        all_u = db.reference('usuarios').get()
        if all_u:
            for k, v in all_u.items():
                st.text(f"ID: {k} | {v['nombre']} [{v['rol']}] - Sanciones: {v.get('sanciones',0)}")

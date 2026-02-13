
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="PHOENIX EMPIRE TOTAL", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. FUNCIÓN PARA FONDO ---
def set_bg_hack(main_bg):
    try:
        with open(main_bg, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url(data:image/png;base64,{bin_str});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        st.markdown("<style>.stApp {background-color: #0E1117;}</style>", unsafe_allow_html=True)

set_bg_hack('fondo.jpg')

# --- 3. CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})
    except:
        st.error("Error crítico: No se encontró el archivo llave.json")

# --- TU ID MAESTRO ---
ID_LIDER_MAESTRO = "1234" # Cambia esto por tu ID real

# --- 4. ESTILOS CSS ---
st.markdown("""
    <style>
    h1, h2, h3, p, div, span, label, .stMarkdown { 
        color: white !important; 
        text-shadow: 2px 2px 4px #000000 !important; 
    }
    .card { 
        background-color: rgba(0, 0, 0, 0.8) !important; 
        padding: 20px; 
        border-radius: 12px; 
        border: 2px solid #E74C3C !important; 
        margin-bottom: 15px; 
    }
    .stButton>button { 
        border-radius: 10px !important; 
        font-weight: bold !important; 
        height: 3.5em; 
        width: 100%; 
        border: 1px solid white !important;
    }
    .btn-rojo button { background-color: #FF0000 !important; color: white !important; }
    .btn-verde button { background-color: #2fa572 !important; color: white !important; }
    .btn-gris button { background-color: #606060 !important; color: white !important; }
    .btn-volver button { background-color: #333333 !important; border: 2px solid #E74C3C !important; }
    .stTextInput > div > div > input { color: white !important; background-color: rgba(255,255,255,0.1) !important; border: 1px solid #E74C3C !important; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'pagina' not in st.session_state: st.session_state['pagina'] = 'login'
def ir_a(pag): 
    st.session_state['pagina'] = pag
    st.rerun()

# ==========================================
# PANTALLA: LOGIN
# ==========================================
if st.session_state['pagina'] == 'login':
    st.markdown("<h1 style='text-align: center; color: #E74C3C;'>PHOENIX EMPIRE 🔥</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        id_input = st.text_input("INGRESA TU ID DE JUGADOR").strip()
        if st.button("ENTRAR AL SISTEMA"):
            if id_input:
                res = db.reference(f'usuarios/{id_input}').get()
                if res:
                    st.session_state['usuario'] = res
                    st.session_state['id_actual'] = id_input
                    ir_a('menu')
                else: st.error("ID no registrado.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PANTALLA: MENÚ
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    my_id = st.session_state['id_actual']
    rol = "Lider" if str(my_id) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')

    st.markdown(f"<div class='card'><h2 style='color: #3b8ed0; text-align:center;'>PANEL: {rol.upper()}</h2><p style='text-align:center;'>Guerrero: <b>{u.get('nombre')}</b></p></div>", unsafe_allow_html=True)

    if rol == "Lider":
        st.markdown("### 🛠️ GESTIÓN")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📊 RANKING"): ir_a('ranking')
            if st.button("💎 TESORERÍA"): ir_a('diamantes')
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
        with c2:
            if st.button("📝 REGISTRAR"): ir_a('registro')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
        
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    elif rol == "Moderador":
        if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
        if st.button("💎 GESTIONAR DIAMANTES"): ir_a('diamantes')

    st.markdown("### 🌎 CLAN")
    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DE MIEMBROS"): ir_a('lista')
    if st.button("🏆 VER EVENTOS"): ir_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# SECCIONES INTERNAS
# ==========================================
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag = st.session_state['pagina']

    if pag == 'ranking':
        st.header("🏆 RANKING")
        data = db.reference('usuarios').get()
        if data:
            lista = [{"Nombre": v.get('nombre'), "💎": v.get('Diamantes',0), "💰": v.get('deuda',0)} 
                    for k, v in data.items() if isinstance(v, dict)]
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))

    elif pag == 'lista':
        st.header("📋 MIEMBROS")
        all_u = db.reference('usuarios').get()
        if all_u:
            for k, v in all_u.items():
                if isinstance(v, dict):
                    st.markdown(f'<div class="card">ID: `{k}` | <b>{v.get("nombre")}</b> | {v.get("rol")} | ⚠️ {v.get("sanciones",0)}</div>', unsafe_allow_html=True)

    elif pag == 'diamantes':
        st.header("💎 TESORERÍA")
        target = st.text_input("ID del Jugador")
        cant = st.number_input("Cantidad", step=1, min_value=1)
        col1, col2 = st.columns(2)
        if col1.button("➕ DIAMANTES"):
            ref = db.reference(f'usuarios/{target}')
            if ref.get(): ref.update({'Diamantes': ref.get().get('Diamantes',0) + cant}); st.success("Sumado")
        if col2.button("➕ DEUDA"):
            ref = db.reference(f'usuarios/{target}')
            if ref.get(): ref.update({'deuda': ref.get().get('deuda',0) + cant}); st.warning("Anotado")

    elif pag == 'sanciones':
        st.header("⚠️ SANCIONES")
        sid = st.text_input("ID del Infractor")
        if st.button("APLICAR SANCIÓN"):
            ref = db.reference(f'usuarios/{sid}')
            u = ref.get()
            if u: ref.update({'sanciones': u.get('sanciones',0) + 1}); st.error("Sancionado")

    elif pag == 'eliminar':
        st.header("❌ ELIMINAR")
        st.markdown('<div class="card" style="border-color: red !important;">', unsafe_allow_html=True)
        eid = st.text_input("ID a borrar")
        if eid:
            u_del = db.reference(f'usuarios/{eid}').get()
            if u_del:
                st.write(f"¿Borrar a **{u_del.get('nombre')}**?")
                if st.button("CONFIRMAR ELIMINACIÓN"):
                    db.reference(f'usuarios/{eid}').delete()
                    st.success("Borrado"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif pag == 'crear_evento':
        st.header("📅 NUEVO EVENTO")
        tit = st.text_input("Título"); fec = st.text_input("Fecha"); des = st.text_area("Descripción")
        if st.button("PUBLICAR"):
            db.reference('eventos').push().set({'nombre': tit, 'fecha': fec, 'descripcion': des})
            st.success("Publicado")

    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f'<div class="card"><h3 style="color:#E74C3C;">{info.get("nombre")}</h3><b>{info.get("fecha")}</b><br>{info.get("descripcion")}</div>', unsafe_allow_html=True)

    elif pag == 'registro':
        st.header("📝 REGISTRO")
        rid = st.text_input("ID"); rnom = st.text_input("Nombre"); rrol = st.selectbox("Rol", ["Miembro", "Moderador", "Lider"])
        if st.button("GUARDAR"):
            db.reference(f'usuarios/{rid}').set({'nombre': rnom, 'rol': rrol, 'Diamantes': 0, 'deuda': 0, 'sanciones': 0})
            st.success("Registrado")

    elif pag == 'cambio_id':
        st.header("🔧 CAMBIO ID")
        old = st.text_input("ID Antiguo"); new = st.text_input("ID Nuevo")
        if st.button("EJECUTAR TRASPASO"):
            d = db.reference(f'usuarios/{old}').get()
            if d:
                db.reference(f'usuarios/{new}').set(d)
                db.reference(f'usuarios/{old}').delete()
                st.success("ID Actualizado")

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64

# --- 1. CONFIGURACIÓN DE PÁGINA (FORZAR TEMA OSCURO) ---
st.set_page_config(
    page_title="PHOENIX EMPIRE TOTAL", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. FUNCIÓN PARA FONDO (MEJORADA) ---
def set_bg_hack(main_bg):
    try:
        with open(main_bg, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(data:image/png;base64,{bin_str});
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
        st.error("Error al conectar con la llave de Firebase.")

# --- TU ID MAESTRO ---
ID_LIDER_MAESTRO = "1234"  # CAMBIA ESTO POR TU ID REAL

# --- 4. ESTILOS CSS "BLINDADOS" (Para que no pierda color) ---
st.markdown("""
    <style>
    /* Forzar color de texto en toda la app */
    h1, h2, h3, p, div, span, label, .stMarkdown { 
        color: white !important; 
        text-shadow: 2px 2px 4px #000000 !important; 
    }
    
    /* Estilo de las tarjetas */
    .card { 
        background-color: rgba(0, 0, 0, 0.8) !important; 
        padding: 20px; 
        border-radius: 12px; 
        border: 2px solid #E74C3C !important; 
        margin-bottom: 15px; 
        box-shadow: 0px 4px 15px rgba(231, 76, 60, 0.3);
    }

    /* Botones generales */
    .stButton>button { 
        border-radius: 10px !important; 
        font-weight: bold !important; 
        height: 3.5em; 
        width: 100%; 
        border: 1px solid white !important;
        transition: 0.3s;
    }

    /* Colores específicos de botones usando Clases */
    div[data-testid="stVerticalBlock"] > div:nth-child(1) .btn-azul button { background-color: #1f538d !important; }
    .btn-azul button { background-color: #1f538d !important; color: white !important; }
    .btn-verde button { background-color: #2fa572 !important; color: white !important; }
    .btn-gris button { background-color: #606060 !important; color: white !important; }
    .btn-rojo button { background-color: #FF0000 !important; color: white !important; }
    .btn-volver button { background-color: #333333 !important; border: 2px solid #E74C3C !important; }

    /* Inputs */
    .stTextInput > div > div > input { 
        color: white !important; 
        background-color: rgba(255,255,255,0.1) !important; 
        border: 1px solid #E74C3C !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'pagina' not in st.session_state: st.session_state['pagina'] = 'login'
def ir_a(pag): 
    st.session_state['pagina'] = pag
    st.rerun()

# ==========================================
# 1. LOGIN
# ==========================================
if st.session_state['pagina'] == 'login':
    st.markdown("<h1 style='text-align: center; color: #E74C3C;'>PHOENIX EMPIRE<br>ESCUADRÓN 🔥</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        id_input = st.text_input("INGRESA TU ID DE JUGADOR")
        if st.button("ENTRAR AL SISTEMA"):
            if id_input:
                res = db.reference(f'usuarios/{id_input}').get()
                if res:
                    st.session_state['usuario'] = res
                    st.session_state['id_actual'] = id_input
                    ir_a('menu')
                else: st.error("ID no encontrado en la base de datos.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 2. MENÚ PRINCIPAL
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    my_id = st.session_state['id_actual']
    rol = "Lider" if str(my_id) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')

    st.markdown(f"<div class='card'><h2 style='color: #3b8ed0; text-align:center;'>PANEL: {rol.upper()}</h2><p style='text-align:center;'>Bienvenido, <b>{u.get('nombre')}</b></p></div>", unsafe_allow_html=True)

    if rol == "Lider":
        st.markdown("### 🛠️ GESTIÓN SUPERIOR")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 RANKING"): ir_a('ranking')
            if st.button("💎 TESORERÍA"): ir_a('diamantes')
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
        with col2:
            if st.button("📝 REGISTRAR"): ir_a('registro')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
        
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    elif rol == "Moderador":
        if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
        if st.button("💎 GESTIONAR DIAMANTES"): ir_a('diamantes')

    st.markdown("### 🌎 COMUNIDAD")
    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DE MIEMBROS"): ir_a('lista')
    if st.button("🏆 VER EVENTOS"): ir_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. PÁGINAS INTERNAS
# ==========================================
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag = st.session_state['pagina']

    if pag == 'ranking':
        st.header("🏆 TOP GUERREROS")
        data = db.reference('usuarios').get()
        if data:
            lista = [{"Nombre": v.get('nombre'), "💎": v.get('Diamantes',0), "💰 Deuda": v.get('deuda',0)} 
                    for k, v in data.items() if isinstance(v, dict)]
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))

    elif pag == 'lista':
        st.header("📋 INTEGRANTES")
        all_u = db.reference('usuarios').get()
        if all_u:
            for k, v in all_u.items():
                if isinstance(v, dict):
                    st.markdown(f"""<div class="card">
                    ID: `{k}` | **{v.get('nombre')}** | Rango: {v.get('rol')}<br>
                    💎 {v.get('Diamantes')} | ⚠️ Sanciones: {v.get('sanciones')}
                    </div>""", unsafe_allow_html=True)

    elif pag == 'diamantes':
        st.header("💎 TESORERÍA")
        with st.form("tesoro"):
            target = st.text_input("ID del Jugador")
            cant = st.number_input("Cantidad", step=1)
            c1, c2 = st.columns(2)
            sub1 = c1.form_submit_button("➕ SUMAR DIAMANTES")
            sub2 = c2.form_submit_button("➕ ANOTAR DEUDA")
            if sub1 or sub2:
                ref = db.reference(f'usuarios/{target}')
                u = ref.get()
                if u:
                    if sub1: ref.update({'Diamantes': u.get('Diamantes',0) + cant})
                    if sub2: ref.update({'deuda': u.get('deuda',0) + cant})
                    st.success("Operación realizada")
                else: st.error("No existe el ID")

    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS ACTIVOS")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f"""<div class="card">
                <h3>🔥 {info.get('nombre')}</h3>
                <p>📅 <b>Fecha:</b> {info.get('fecha')}</p>
                <p>{info.get('descripcion')}</p>
                </div>""", unsafe_allow_html=True)
        else: st.info("No hay eventos programados.")

    elif pag == 'sanciones':
        st.header("⚠️ APLICAR SANCIÓN")
        s_id = st.text_input("ID del Infractor")
        if st.button("MULTAR (+1 Sanción)"):
            ref = db.reference(f'usuarios/{s_id}')
            u = ref.get()
            if u:
                ref.update({'sanciones': u.get('sanciones', 0) + 1})
                st.error(f"Sanción registrada para {u.get('nombre')}")

    elif pag == 'registro':
        st.header("📝 REGISTRAR")
        with st.form("reg"):
            r_id = st.text_input("ID Nuevo")
            r_nom = st.text_input("Nombre")
            r_rol = st.selectbox("Rol", ["Miembro", "Moderador", "Lider"])
            if st.form_submit_button("GUARDAR EN FIREBASE"):
                db.reference(f'usuarios/{r_id}').set({'nombre': r_nom, 'rol': r_rol, 'Diamantes': 0, 'deuda': 0, 'sanciones': 0})
                st.success("Usuario Creado")

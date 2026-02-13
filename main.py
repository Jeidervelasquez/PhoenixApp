import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE TOTAL", layout="centered")

# --- 2. FUNCIÓN PARA FONDO ---
def set_bg_hack(main_bg):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/png;base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
             background-position: center;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

try: set_bg_hack('fondo.jpg') 
except: pass

# --- 3. CONEXIÓN ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})
    except: pass

# --- TU ID MAESTRO ---
ID_LIDER_MAESTRO = "PON_TU_ID_AQUI" 

# --- ESTILOS ---
st.markdown("""
    <style>
    h1, h2, h3, p, div, span, label { color: white !important; text-shadow: 2px 2px 4px #000000; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3.5em; width: 100%; border: 1px solid white; margin-bottom: 10px; }
    .card { background-color: rgba(0, 0, 0, 0.7); padding: 20px; border-radius: 10px; border: 1px solid #E74C3C; margin-bottom: 10px; }
    div.row-widget.stButton > button[kind="primary"] { background-color: #1f538d; }
    .btn-azul button { background-color: rgba(31, 83, 141, 0.9) !important; color: white; }
    .btn-verde button { background-color: rgba(47, 165, 114, 0.9) !important; color: white; }
    .btn-gris button { background-color: rgba(96, 96, 96, 0.9) !important; color: white; }
    .btn-rojo button { background-color: rgba(255, 0, 0, 0.8) !important; color: white; }
    .btn-volver button { background-color: rgba(50, 50, 50, 0.9) !important; border: 1px solid white; color: white; }
    .stTextInput > div > div > input { color: white; background-color: rgba(0,0,0,0.8); }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'pagina' not in st.session_state: st.session_state['pagina'] = 'login'
def ir_a(pag): st.session_state['pagina'] = pag; st.rerun()

# ==========================================
# 1. LOGIN
# ==========================================
if st.session_state['pagina'] == 'login':
    st.markdown("<h1 style='color: #E74C3C; text-shadow: 3px 3px 0px #000;'>PHOENIX EMPIRE<br>ESCUADRÓN 🔥</h1>", unsafe_allow_html=True)
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
                else: st.error("ID no encontrado.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 2. MENÚ
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    my_id = st.session_state['id_actual']
    rol = "Lider" if str(my_id) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')

    st.markdown(f"<div class='card'><h2 style='color: #3b8ed0; margin:0;'>PANEL DE CONTROL: {rol.upper()}</h2><p style='text-align:center;'>Guerrero: <b>{u.get('nombre')}</b></p></div>", unsafe_allow_html=True)

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

    elif rol == "Moderador":
        if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
        if st.button("💎 GESTIONAR DIAMANTES"): ir_a('diamantes')
    
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
# 3. FUNCIONES
# ==========================================
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag = st.session_state['pagina']

    # --- RANKING (Protegido contra errores) ---
    if pag == 'ranking':
        st.header("🏆 RANKING Y DEUDAS")
        data = db.reference('usuarios').get()
        if data:
            lista = []
            for k, v in data.items():
                if isinstance(v, dict): # Solo si es un diccionario válido
                    lista.append({
                        "Nombre": v.get('nombre', 'Desconocido'), 
                        "💎": v.get('Diamantes',0), 
                        "💰": v.get('deuda',0)
                    })
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))
            st.markdown('</div>', unsafe_allow_html=True)

    # --- LISTA (¡AQUÍ ESTABA EL ERROR!) ---
    elif pag == 'lista':
        st.header("📋 LISTA DEL CLAN")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        all_u = db.reference('usuarios').get()
        if all_u:
            for k, v in all_u.items():
                if isinstance(v, dict): # Protección anti-errores
                    nombre = v.get('nombre', 'Sin Nombre')
                    rol_u = v.get('rol', 'Miembro')
                    sanc = v.get('sanciones', 0)
                    st.write(f"🆔 `{k}` | 👤 **{nombre}** | 🛡️ {rol_u} | ⚠️ {sanc}")
                    st.markdown("<hr style='margin: 5px 0; border-color: #555;'>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- OTRAS FUNCIONES ---
    elif pag == 'diamantes':
        st.header("💎 GESTIÓN DE TESORERÍA")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        target = st.text_input("ID del Jugador")
        cant = st.number_input("Cantidad", step=1, min_value=1)
        c1, c2 = st.columns(2)
        if c1.button("➕ SUMAR DIAMANTES"):
            ref = db.reference(f'usuarios/{target}')
            if ref.get(): 
                ref.update({'Diamantes': ref.get().get('Diamantes',0) + cant})
                st.success("Hecho")
            else: st.error("ID no existe")
        if c2.button("➕ ANOTAR DEUDA"):
            ref = db.reference(f'usuarios/{target}')
            if ref.get(): 
                ref.update({'deuda': ref.get().get('deuda',0) + cant})
                st.warning("Hecho")
            else: st.error("ID no existe")
        st.markdown('</div>', unsafe_allow_html=True)

    elif pag == 'sanciones':
        st.header("⚠️ SANCIONES")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        s_id = st.text_input("ID Infractor")
        if st.button("APLICAR SANCIÓN (+1)"):
            ref = db.reference(f'usuarios/{s_id}')
            u = ref.get()
            if u:
                ref.update({'sanciones': u.get('sanciones', 0) + 1})
                st.error(f"Sanción aplicada a {u.get('nombre')}")
        st.markdown('</div>', unsafe_allow_html=True)

    elif pag == 'registro':
        st.header("📝 REGISTRO")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        r_id = st.text_input("ID Nuevo")
        r_nom = st.text_input("Nombre")
        r_rol = st.selectbox("Rol", ["Miembro", "Moderador", "Lider"])
        if st.button("GUARDAR"):
            db.reference(f'usuarios/{r_id}').set({'nombre': r_nom, 'rol': r_rol, 'Diamantes': 0, 'deuda': 0, 'sanciones': 0})
            st.success("Listo")
        st.markdown('</div>', unsafe_allow_html=True)

    elif pag == 'cambio_id':
        st.header("🔧 CAMBIO ID")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        old = st.text_input("ID Viejo"); new = st.text_input("ID Nuevo")
        if st.button("CAMBIAR"):
            d = db.reference(f'usuarios/{old}').get()
            if d:
                db.reference(f'usuarios/{new}').set(d)
                db.reference(f'usuarios/{old}').delete()
                st.success("Cambiado")
        st.markdown('</div>', unsafe_allow_html=True)

    elif pag == 'eliminar':
        st.header("❌ ELIMINAR")
        st.markdown('<div class="card" style="border-color:red;">', unsafe_allow_html=True)
        d_id = st.text_input("ID a borrar")
        if st.button("BORRAR DEFINITIVAMENTE"):
            db.reference(f'usuarios/{d_id}').delete()
            st.warning("Eliminado")
        st.markdown('</div>', unsafe_allow_html=True)

    elif pag == 'crear_evento':
        st.header("📅 CREAR EVENTO")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        t = st.text_input("Título"); f = st.text_input("Fecha"); d = st.text_area("Info")
        if st.button("PUBLICAR"):
            db.reference('eventos').push().set({'nombre': t, 'fecha': f, 'descripcion': d})
            st.success("Publicado")
        st.markdown('</div>', unsafe_allow_html=True)

    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f"<div class='card'><h3>{info['nombre']}</h3><p>{info['fecha']}</p><p>{info['descripcion']}</p></div>", unsafe_allow_html=True)
                if st.button("Asistiré", key=eid): st.success("Anotado")

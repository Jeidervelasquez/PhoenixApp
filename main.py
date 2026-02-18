
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE - PRO", layout="centered", initial_sidebar_state="collapsed")

def set_bg_hack(main_bg):
    try:
        with open(main_bg, "rb") as f: data = f.read()
        bin_str = base64.b64encode(data).decode()
        st.markdown(f"""<style>.stApp {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url(data:image/png;base64,{bin_str}); background-size: cover; background-position: center; background-attachment: fixed; }}</style>""", unsafe_allow_html=True)
    except: st.markdown("<style>.stApp {background-color: #0E1117;}</style>", unsafe_allow_html=True)

set_bg_hack('fondo.jpg')

# --- 2. CONEXIÓN ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})
    except: st.error("Error: Falta llave.json")

# --- CONSTANTES ---
ID_LIDER_MAESTRO = "1234" # <--- CAMBIA ESTO
ID_COACH = "0000"
ROLES_JUEGO = ["Jungla", "Experiencia", "Mid", "Roam", "ADC"]

# --- 3. ESTILOS ---
st.markdown("""
    <style>
    h1, h2, h3, p, div, span, label, .stMarkdown { color: white !important; text-shadow: 2px 2px 4px #000000 !important; }
    .card { background-color: rgba(0, 0, 0, 0.8) !important; padding: 20px; border-radius: 12px; border: 2px solid #E74C3C !important; margin-bottom: 15px; }
    .stButton>button { border-radius: 10px !important; font-weight: bold !important; height: 3.5em; width: 100%; border: 1px solid white !important; }
    .btn-rojo button { background-color: #FF0000 !important; color: white !important; }
    .btn-verde button { background-color: #2fa572 !important; color: white !important; }
    .btn-gris button { background-color: #606060 !important; color: white !important; }
    .btn-volver button { background-color: #333333 !important; border: 2px solid #E74C3C !important; }
    .stTextInput > div > div > input { color: white !important; background-color: rgba(255,255,255,0.1) !important; border: 1px solid #E74C3C !important; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'pagina' not in st.session_state: st.session_state['pagina'] = 'login'
def ir_a(pag): st.session_state['pagina'] = pag; st.rerun()

# ==========================================
# 1. LOGIN
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
# 2. MENÚ
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    my_id = st.session_state['id_actual']
    rol = "Lider" if str(my_id) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')
    if str(my_id) == ID_COACH: rol = "Coach"

    st.markdown(f"<div class='card'><h2 style='color: #3b8ed0; text-align:center;'>PANEL: {rol.upper()}</h2><p style='text-align:center;'>Guerrero: <b>{u.get('nombre')}</b></p></div>", unsafe_allow_html=True)

    if rol == "Lider":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📊 RANKING"): ir_a('ranking')
            if st.button("💎 TESORERÍA"): ir_a('diamantes')
            if st.button("📝 REGISTRAR"): ir_a('registro')
        with c2:
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("📅 EVENTOS"): ir_a('crear_evento')
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    elif rol == "Coach":
        if st.button("📈 PANEL DE COACH"): ir_a('coach_panel')
        if st.button("⚔️ CREAR EQUIPOS"): ir_a('coach_equipos')
        if st.button("🎁 SUGERIR PREMIOS"): ir_a('coach_premios')

    elif rol == "Moderador":
        if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
        if st.button("💎 GESTIONAR DIAMANTES"): ir_a('diamantes')

    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DEL CLAN"): ir_a('lista')
    if st.button("🏆 VER EVENTOS"): ir_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. SECCIONES
# ==========================================
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    pag = st.session_state['pagina']
    u_act = st.session_state['usuario']
    id_act = st.session_state['id_actual']
    rol_sesion = "Lider" if str(id_act) == ID_LIDER_MAESTRO else u_act.get('rol', 'Miembro')
    if str(id_act) == ID_COACH: rol_sesion = "Coach"

    # --- LISTA DE MIEMBROS (PRIVACIDAD DE ID) ---
    if pag == 'lista':
        st.header("📋 MIEMBROS DEL ESCUADRÓN")
        data = db.reference('usuarios').get()
        if data:
            for k, v in data.items():
                if isinstance(v, dict):
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    # Privacidad: Solo Lider y Mod ven IDs ajenos
                    id_mostrar = f"🆔 `{k}` | " if (rol_sesion in ["Lider", "Moderador"] or str(id_act) == str(k)) else ""
                    st.write(f"{id_mostrar}👤 **{v.get('nombre')}**")
                    st.write(f"🛡️ Rol: {v.get('rol')} | 🎮 {v.get('rol_primario', 'N/A')} - {v.get('rol_secundario', 'N/A')}")
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- REGISTRO (CON ROLES DE JUEGO) ---
    elif pag == 'registro':
        st.header("📝 REGISTRO DE GUERREROS")
        with st.form("reg_form"):
            rid = st.text_input("ID Nuevo")
            rnom = st.text_input("Nombre")
            rrol = st.selectbox("Rango en el Clan", ["Miembro", "Moderador", "Lider", "Coach"])
            st.write("--- Roles de Juego ---")
            rp = st.selectbox("Rol Principal", ROLES_JUEGO)
            rs = st.selectbox("Rol Secundario", ROLES_JUEGO)
            
            if st.form_submit_button("GUARDAR"):
                if rrol == "Coach" and rol_sesion != "Lider":
                    st.error("Solo el Líder puede crear un Coach.")
                else:
                    data_new = {'nombre': rnom, 'rol': rrol, 'Diamantes':0, 'deuda':0, 'sanciones':0, 'puntos_coach':0}
                    if rrol != "Coach":
                        data_new['rol_primario'] = rp
                        data_new['rol_secundario'] = rs
                    db.reference(f'usuarios/{rid}').set(data_new)
                    st.success("Registrado con éxito")

    # --- SANCIONES (CORREGIDO) ---
    elif pag == 'sanciones':
        st.header("⚠️ GESTIÓN DE DISCIPLINA")
        sid = st.text_input("ID del Infractor")
        if st.button("APLICAR SANCIÓN (+1)"):
            ref = db.reference(f'usuarios/{sid}')
            u_s = ref.get()
            if u_s:
                ref.update({'sanciones': u_s.get('sanciones', 0) + 1})
                st.error(f"Sanción aplicada a {u_s.get('nombre')}")
            else: st.error("ID no encontrado")

    # --- CAMBIAR ID (CORREGIDO) ---
    elif pag == 'cambio_id':
        st.header("🔧 ACTUALIZAR ID")
        old = st.text_input("ID Actual")
        new = st.text_input("ID Nuevo")
        if st.button("TRANSFERIR DATOS"):
            ref_old = db.reference(f'usuarios/{old}')
            data_old = ref_old.get()
            if data_old:
                db.reference(f'usuarios/{new}').set(data_old)
                ref_old.delete()
                st.success("ID actualizado correctamente")
            else: st.error("El ID original no existe")

    # --- PANEL COACH: PUNTOS Y VISTA ---
    elif pag == 'coach_panel':
        st.header("📈 GESTIÓN DEL COACH")
        all_u = db.reference('usuarios').get()
        if all_u:
            miembros = {k:v for k,v in all_u.items() if v.get('rol') != 'Coach'}
            st.metric("Total Escuadrón", len(miembros))
            
            for k, v in miembros.items():
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.write(f"👤 **{v.get('nombre')}** | 🎮 {v.get('rol_primario')} / {v.get('rol_secundario')}")
                    st.write(f"⭐ Puntos Coach: {v.get('puntos_coach', 0)}")
                    pts = st.number_input(f"Puntos para {v.get('nombre')}", step=1, key=f"pts_{k}")
                    if st.button(f"OTORGAR PUNTOS A {v.get('nombre')}", key=f"btn_pts_{k}"):
                        db.reference(f'usuarios/{k}').update({'puntos_coach': v.get('puntos_coach', 0) + pts})
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- COACH: CREAR EQUIPOS ---
    elif pag == 'coach_equipos':
        st.header("⚔️ FORMACIÓN DE ESCUADRAS")
        all_u = db.reference('usuarios').get()
        if all_u:
            miembros_nombres = {k: v.get('nombre') for k, v in all_u.items() if v.get('rol') != 'Coach'}
            nom_equipo = st.text_input("Nombre del Equipo")
            seleccionados = st.multiselect("Selecciona 5 jugadores", list(miembros_nombres.values()))
            
            if st.button("CREAR EQUIPO"):
                if len(seleccionados) == 5:
                    db.reference('equipos').push().set({'nombre': nom_equipo, 'jugadores': seleccionados})
                    st.success("Equipo formado")
                else: st.warning("Debes seleccionar exactamente 5 jugadores")
        
        st.subheader("Equipos Actuales")
        eqs = db.reference('equipos').get()
        if eqs:
            for ek, ev in eqs.items():
                st.write(f"🚩 **{ev['nombre']}**: {', '.join(ev['jugadores'])}")

    # --- COACH: PREMIOS ---
    elif pag == 'coach_premios':
        st.header("🎁 SUGERENCIA DE PREMIOS")
        txt = st.text_area("Descripción (Ej: El jugador X merece una skin por su desempeño)")
        if st.button("ENVIAR SUGERENCIA AL LÍDER"):
            db.reference('premios_sugeridos').push().set({'coach': u_act.get('nombre'), 'nota': txt})
            st.success("Enviado")

    # --- RANKING ---
    elif pag == 'ranking':
        st.header("🏆 RANKING")
        data = db.reference('usuarios').get()
        if data:
            lista = [{"Nombre": v.get('nombre'), "💎": v.get('Diamantes',0), "💰": v.get('deuda',0), "⭐ Coach": v.get('puntos_coach',0)} for k, v in data.items() if isinstance(v, dict) and v.get('rol') != 'Coach']
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))

    # --- EVENTOS (VER) ---
    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f'<div class="card"><h3>{info.get("nombre")}</h3>{info.get("descripcion")}<br><b>Asistentes:</b> {", ".join(info.get("asistentes", {}).values()) if info.get("asistentes") else "Ninguno"}</div>', unsafe_allow_html=True)
                if st.button("YO ASISTIRÉ", key=f"asis_{eid}"):
                    db.reference(f'eventos/{eid}/asistentes/{id_act}').set(u_act.get('nombre'))
                    st.rerun()

    # --- CREAR EVENTO ---
    elif pag == 'crear_evento':
        st.header("📅 NUEVO EVENTO")
        t = st.text_input("Título"); d = st.text_area("Info")
        if st.button("PUBLICAR"):
            db.reference('eventos').push().set({'nombre': t, 'descripcion': d})
            st.success("Evento Creado")

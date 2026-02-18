import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="PHOENIX EMPIRE PRO", layout="centered", initial_sidebar_state="collapsed")

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
    except: st.error("Falta llave.json")

# --- CONSTANTES ---
ID_LIDER_MAESTRO = "1234" # CAMBIA ESTO POR TU ID
ID_COACH = "0000"
ROLES_ML = ["Jungla", "Experiencia", "Mid", "Roam", "ADC"]

# --- 3. ESTILOS ---
st.markdown("""
    <style>
    h1, h2, h3, p, div, span, label, .stMarkdown { color: white !important; text-shadow: 2px 2px 4px #000000 !important; }
    .card { background-color: rgba(0, 0, 0, 0.8) !important; padding: 20px; border-radius: 12px; border: 2px solid #E74C3C !important; margin-bottom: 15px; }
    .stButton>button { border-radius: 10px !important; font-weight: bold !important; height: 3em; width: 100%; border: 1px solid white !important; }
    .btn-rojo button { background-color: #FF0000 !important; }
    .btn-verde button { background-color: #2fa572 !important; }
    .btn-gris button { background-color: #606060 !important; }
    .btn-volver button { background-color: #333333 !important; border: 2px solid #E74C3C !important; }
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
    st.markdown('<div class="card">', unsafe_allow_html=True)
    id_in = st.text_input("ID DE JUGADOR").strip()
    if st.button("ENTRAR"):
        res = db.reference(f'usuarios/{id_in}').get()
        if res:
            st.session_state['usuario'], st.session_state['id_actual'] = res, id_in
            ir_a('menu')
        else: st.error("ID no registrado.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 2. MENÚ PRINCIPAL
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u, my_id = st.session_state['usuario'], st.session_state['id_actual']
    rol = "Lider" if str(my_id) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')
    if str(my_id) == ID_COACH: rol = "Coach"

    st.markdown(f"<div class='card'><h2 style='text-align:center;'>{rol.upper()}: {u.get('nombre')}</h2></div>", unsafe_allow_html=True)

    if rol == "Lider":
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 RANKING"): ir_a('ranking')
            if st.button("📝 REGISTRAR"): ir_a('registro')
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
        with col2:
            if st.button("💎 TESORERÍA"): ir_a('diamantes')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("🎁 VER SUGERENCIAS"): ir_a('ver_sugerencias')
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    elif rol == "Coach":
        if st.button("📉 PUNTOS ESCUADRÓN"): ir_a('coach_puntos')
        if st.button("⚔️ FORMAR EQUIPOS"): ir_a('coach_equipos')
        if st.button("🎁 SUGERIR PREMIO"): ir_a('coach_premios')

    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DEL CLAN"): ir_a('lista')
    if st.button("🏆 EVENTOS"): ir_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 SALIR"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. FUNCIONES
# ==========================================
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag, u_act, id_act = st.session_state['pagina'], st.session_state['usuario'], st.session_state['id_actual']
    rol_s = "Lider" if str(id_act) == ID_LIDER_MAESTRO else u_act.get('rol', 'Miembro')
    if str(id_act) == ID_COACH: rol_s = "Coach"

    # --- LISTA (PRIVACIDAD DE ID) ---
    if pag == 'lista':
        st.header("📋 MIEMBROS")
        data = db.reference('usuarios').get()
        if data:
            for k, v in data.items():
                if isinstance(v, dict):
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    # Solo Lider/Mod ven IDs de otros. Miembro solo ve su propio ID.
                    visible_id = f"🆔 `{k}` | " if (rol_s in ["Lider", "Moderador"] or str(id_act) == str(k)) else ""
                    st.write(f"{visible_id}👤 **{v.get('nombre')}**")
                    if v.get('rol') != 'Coach':
                        st.write(f"🎮 {v.get('rol_primario')} / {v.get('rol_secundario')}")
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- REGISTRO (LOGICA COACH) ---
    elif pag == 'registro':
        st.header("📝 REGISTRO")
        with st.form("reg"):
            rid = st.text_input("ID")
            rnom = st.text_input("Nombre")
            rrol = st.selectbox("Rol", ["Miembro", "Moderador", "Coach"])
            # Si es Coach, no se muestran roles de juego
            if rrol != "Coach":
                rp = st.selectbox("Rol Primario", ROLES_ML)
                rs = st.selectbox("Rol Secundario", ROLES_ML)
            
            if st.form_submit_button("GUARDAR"):
                new_data = {'nombre': rnom, 'rol': rrol, 'Diamantes':0, 'deuda':0, 'sanciones':0, 'puntos_coach':0}
                if rrol != "Coach":
                    new_data.update({'rol_primario': rp, 'rol_secundario': rs})
                db.reference(f'usuarios/{rid}').set(new_data)
                st.success("Registrado")

    # --- ELIMINAR (COMPLETO) ---
    elif pag == 'eliminar':
        st.header("❌ ELIMINAR")
        del_id = st.text_input("ID a borrar")
        if del_id:
            info = db.reference(f'usuarios/{del_id}').get()
            if info:
                st.warning(f"¿Borrar a {info['nombre']}?")
                if st.button("CONFIRMAR BORRADO"):
                    db.reference(f'usuarios/{del_id}').delete()
                    st.success("Eliminado"); st.rerun()

    # --- CAMBIAR ID (COMPLETO) ---
    elif pag == 'cambio_id':
        st.header("🔧 CAMBIAR ID")
        old, new = st.text_input("ID Viejo"), st.text_input("ID Nuevo")
        if st.button("ACTUALIZAR"):
            old_data = db.reference(f'usuarios/{old}').get()
            if old_data:
                db.reference(f'usuarios/{new}').set(old_data)
                db.reference(f'usuarios/{old}').delete()
                st.success("ID Cambiado"); st.rerun()

    # --- SANCIONES (COMPLETO) ---
    elif pag == 'sanciones':
        st.header("⚠️ SANCIONES")
        sid = st.text_input("ID Infractor")
        if st.button("MULTAR (+1)"):
            r = db.reference(f'usuarios/{sid}')
            if r.get(): r.update({'sanciones': r.get().get('sanciones',0)+1}); st.error("Sancionado")

    # --- COACH: PUNTOS ---
    elif pag == 'coach_puntos':
        st.header("📈 PUNTOS DE COACH")
        all_u = db.reference('usuarios').get()
        if all_u:
            ms = {k:v for k,v in all_u.items() if v.get('rol') != 'Coach'}
            st.write(f"Total miembros: {len(ms)}")
            for k, v in ms.items():
                st.markdown(f'<div class="card"><b>{v["nombre"]}</b> | ⭐ {v.get("puntos_coach",0)}</div>', unsafe_allow_html=True)
                p = st.number_input(f"Sumar a {v['nombre']}", step=1, key=f"p_{k}")
                if st.button(f"OTORGAR", key=f"b_{k}"):
                    db.reference(f'usuarios/{k}').update({'puntos_coach': v.get('puntos_coach',0)+p}); st.rerun()

    # --- COACH: EQUIPOS ---
    elif pag == 'coach_equipos':
        st.header("⚔️ NUEVO EQUIPO")
        all_u = db.reference('usuarios').get()
        if all_u:
            nombres = {k:v['nombre'] for k,v in all_u.items() if v.get('rol') != 'Coach'}
            e_nom = st.text_input("Nombre Equipo")
            s = st.multiselect("Selecciona 5", list(nombres.values()))
            if st.button("CREAR"):
                if len(s) == 5:
                    db.reference('equipos').push().set({'nombre': e_nom, 'jugadores': s})
                    st.success("Equipo Creado")
        
        st.subheader("Equipos")
        eqs = db.reference('equipos').get()
        if eqs:
            for ek, ev in eqs.items(): st.write(f"🚩 {ev['nombre']}: {', '.join(ev['jugadores'])}")

    # --- COACH: PREMIOS ---
    elif pag == 'coach_premios':
        st.header("🎁 SUGERIR PREMIO")
        nota = st.text_area("¿Quién merece premio y por qué?")
        if st.button("ENVIAR AL LIDER"):
            db.reference('sugerencias').push().set({'msg': nota, 'autor': u_act['nombre']})
            st.success("Enviado")

    # --- LIDER: VER SUGERENCIAS ---
    elif pag == 'ver_sugerencias':
        st.header("🎁 NOTAS DEL COACH")
        sug = db.reference('sugerencias').get()
        if sug:
            for sk, sv in sug.items():
                st.markdown(f'<div class="card"><b>De: {sv["autor"]}</b><br>{sv["msg"]}</div>', unsafe_allow_html=True)
                if st.button("Eliminar Nota", key=sk): db.reference(f'sugerencias/{sk}').delete(); st.rerun()

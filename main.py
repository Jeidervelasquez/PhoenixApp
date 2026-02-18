import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64

# --- 1. CONFIGURACIÓN E IMAGEN DE FONDO ---
st.set_page_config(page_title="PHOENIX EMPIRE PRO", layout="centered", initial_sidebar_state="collapsed")

def set_bg_hack(main_bg):
    try:
        with open(main_bg, "rb") as f: data = f.read()
        bin_str = base64.b64encode(data).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url(data:image/png;base64,{bin_str});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>""", unsafe_allow_html=True)
    except: st.markdown("<style>.stApp {background-color: #0E1117;}</style>", unsafe_allow_html=True)

set_bg_hack('fondo.jpg')

# --- 2. CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})
    except: st.error("⚠️ Error: No se encuentra el archivo llave.json")

# --- CONSTANTES ---
ID_LIDER_MAESTRO = "1234" # <--- ¡CAMBIA ESTO POR TU ID REAL!
ID_COACH = "0000"
ROLES_JUEGO = ["Jungla", "Experiencia", "Mid", "Roam", "ADC"]

# --- 3. ESTILOS VISUALES ---
st.markdown("""
    <style>
    h1, h2, h3, p, div, span, label, .stMarkdown, td, th { color: white !important; text-shadow: 2px 2px 4px #000000 !important; }
    .card { background-color: rgba(0, 0, 0, 0.85) !important; padding: 20px; border-radius: 12px; border: 2px solid #E74C3C !important; margin-bottom: 15px; }
    .stButton>button { border-radius: 8px !important; font-weight: bold !important; height: 3em; width: 100%; border: 1px solid white !important; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    .btn-rojo button { background-color: #922B21 !important; }
    .btn-verde button { background-color: #1E8449 !important; }
    .btn-gris button { background-color: #566573 !important; }
    .btn-dorado button { background-color: #D4AC0D !important; color: white !important; border: 1px solid #F1C40F !important; }
    .btn-volver button { background-color: #17202A !important; border: 2px solid #E74C3C !important; }
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
    st.markdown('<div class="card">', unsafe_allow_html=True)
    id_in = st.text_input("ID DE JUGADOR").strip()
    if st.button("ENTRAR AL SISTEMA"):
        if id_in:
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
    rol = u.get('rol', 'Miembro')
    if str(my_id) == ID_LIDER_MAESTRO: rol = "Lider"
    if str(my_id) == ID_COACH: rol = "Coach"

    st.markdown(f"<div class='card'><h2 style='text-align:center;'>{rol.upper()}: {u.get('nombre')}</h2></div>", unsafe_allow_html=True)

    if rol == "Lider":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📊 RANKING GENERAL"): ir_a('ranking')
            if st.button("💎 TESORERÍA"): ir_a('diamantes')
            if st.button("📝 REGISTRAR"): ir_a('registro')
        with c2:
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("🎁 SUGERENCIAS"): ir_a('ver_sugerencias')
        
        st.markdown('<div class="btn-dorado">', unsafe_allow_html=True)
        if st.button("👀 VER LINEUP (TITULARES/SUPLENTES)"): ir_a('ver_lineup')
        if st.button("⭐ RANKING DE COACH"): ir_a('ranking_coach')
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    elif rol == "Coach":
        st.markdown('<div class="btn-dorado">', unsafe_allow_html=True)
        if st.button("🎮 GESTIONAR TITULARES Y SUPLENTES"): ir_a('coach_lineup')
        if st.button("⭐ VER MI RANKING"): ir_a('ranking_coach')
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("📈 DAR PUNTOS"): ir_a('coach_puntos')
        if st.button("⚔️ EQUIPOS DE 5"): ir_a('coach_equipos')
        if st.button("🎁 SUGERIR PREMIO"): ir_a('coach_premios')

    # Comunes
    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DEL CLAN"): ir_a('lista')
    if st.button("🏆 EVENTOS"): ir_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 SALIR"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. PÁGINAS DE FUNCIONES
# ==========================================
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag, u_act, id_act = st.session_state['pagina'], st.session_state['usuario'], st.session_state['id_actual']
    rol_s = u_act.get('rol', 'Miembro')
    if str(id_act) == ID_LIDER_MAESTRO: rol_s = "Lider"
    if str(id_act) == ID_COACH: rol_s = "Coach"

    # --- NUEVA FUNCIÓN: GESTIÓN DE LINEUP (COACH) ---
    if pag == 'coach_lineup':
        st.header("🎮 FORMACIÓN TÁCTICA")
        data = db.reference('usuarios').get()
        if data:
            nombres_ids = {k: f"{v['nombre']} ({v.get('rol_primario','?')})" for k,v in data.items() if v.get('rol') != 'Coach'}
            
            st.subheader("Selecciona 5 Titulares")
            tits = st.multiselect("Titulares", list(nombres_ids.values()), key="sel_tit")
            
            st.subheader("Selecciona 5 Suplentes")
            sups = st.multiselect("Suplentes", list(nombres_ids.values()), key="sel_sup")
            
            if st.button("💾 GUARDAR FORMACIÓN"):
                if len(tits) == 5 and len(sups) == 5:
                    db.reference('lineup_actual').set({'titulares': tits, 'suplentes': sups})
                    st.success("Lineup actualizado correctamente")
                else: st.warning("Debes elegir exactamente 5 titulares y 5 suplentes.")

    # --- NUEVA FUNCIÓN: VER LINEUP (LIDER Y MIEMBROS) ---
    elif pag == 'ver_lineup':
        st.header("👀 FORMACIÓN ACTUAL")
        lineup = db.reference('lineup_actual').get()
        if lineup:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### 🔥 TITULARES")
                for p in lineup.get('titulares', []): st.info(p)
            with c2:
                st.markdown("### 💤 SUPLENTES")
                for p in lineup.get('suplentes', []): st.warning(p)
        else: st.info("El Coach aún no ha definido la formación.")

    # --- RANKING COACH ---
    elif pag == 'ranking_coach':
        st.header("⭐ RANKING DE RENDIMIENTO")
        data = db.reference('usuarios').get()
        if data:
            lista = [{"n": v['nombre'], "p": v.get('puntos_coach',0)} for k,v in data.items() if v.get('rol') != 'Coach']
            lista = sorted(lista, key=lambda x: x['p'], reverse=True)
            for i, j in enumerate(lista):
                med = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"#{i+1}"
                st.markdown(f'<div class="card">{med} <b>{j["n"]}</b> - ⭐ {j["p"]} Pts</div>', unsafe_allow_html=True)

    # --- TESORERÍA ---
    elif pag == 'diamantes':
        st.header("💎 TESORERÍA")
        target = st.text_input("ID Jugador")
        cant = st.number_input("Monto", step=1, min_value=1)
        if st.button("➕ DIAMANTES"):
            r = db.reference(f'usuarios/{target}')
            if r.get(): r.update({'Diamantes': r.get().get('Diamantes',0)+cant}); st.success("Ok")
        if st.button("➕ DEUDA"):
            r = db.reference(f'usuarios/{target}')
            if r.get(): r.update({'deuda': r.get().get('deuda',0)+cant}); st.warning("Anotado")

    # --- RANKING GENERAL ---
    elif pag == 'ranking':
        st.header("🏆 RANKING GENERAL")
        data = db.reference('usuarios').get()
        if data:
            lista = [{"Nombre": v['nombre'], "💎": v.get('Diamantes',0), "💰": v.get('deuda',0)} for k,v in data.items() if v.get('rol') != 'Coach']
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))

    # --- REGISTRO ---
    elif pag == 'registro':
        st.header("📝 REGISTRO")
        with st.form("f"):
            rid = st.text_input("ID"); rnom = st.text_input("Nombre"); rrol = st.selectbox("Rango", ["Miembro", "Moderador", "Coach"])
            rp, rs = "N/A", "N/A"
            if rrol != "Coach":
                rp = st.selectbox("Primario", ROLES_JUEGO); rs = st.selectbox("Secundario", ROLES_JUEGO)
            if st.form_submit_button("GUARDAR"):
                d = {'nombre': rnom, 'rol': rrol, 'Diamantes':0, 'deuda':0, 'sanciones':0, 'puntos_coach':0}
                if rrol != "Coach": d.update({'rol_primario': rp, 'rol_secundario': rs})
                db.reference(f'usuarios/{rid}').set(d); st.success("Registrado")

    # --- LISTA ---
    elif pag == 'lista':
        st.header("📋 MIEMBROS")
        data = db.reference('usuarios').get()
        if data:
            for k, v in data.items():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                if rol_s in ["Lider", "Moderador", "Coach"] or str(id_act) == str(k): st.write(f"🆔 `{k}`")
                st.write(f"👤 **{v['nombre']}** | 🛡️ {v['rol']}")
                if v.get('rol') != 'Coach': st.write(f"🎮 {v.get('rol_primario')} / {v.get('rol_secundario')}")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- COACH PUNTOS ---
    elif pag == 'coach_puntos':
        st.header("📈 PUNTOS")
        data = db.reference('usuarios').get()
        for k, v in data.items():
            if v.get('rol') != 'Coach':
                pts = st.number_input(f"Sumar a {v['nombre']}", step=1, key=k)
                if st.button(f"DAR PUNTOS", key=f"b{k}"):
                    db.reference(f'usuarios/{k}').update({'puntos_coach': v.get('puntos_coach',0)+pts}); st.rerun()

    # --- ELIMINAR ---
    elif pag == 'eliminar':
        st.header("❌ ELIMINAR")
        did = st.text_input("ID")
        if st.button("CONFIRMAR ELIMINAR"):
            db.reference(f'usuarios/{did}').delete(); st.success("Eliminado")

    # --- CAMBIAR ID ---
    elif pag == 'cambio_id':
        st.header("🔧 CAMBIO ID")
        oid, nid = st.text_input("Viejo"), st.text_input("Nuevo")
        if st.button("CAMBIAR"):
            data = db.reference(f'usuarios/{oid}').get()
            if data: db.reference(f'usuarios/{nid}').set(data); db.reference(f'usuarios/{oid}').delete(); st.success("Listo")

    # --- SANCIONES ---
    elif pag == 'sanciones':
        st.header("⚠️ SANCIONES")
        sid = st.text_input("ID")
        if st.button("SANCIONAR (+1)"):
            r = db.reference(f'usuarios/{sid}')
            if r.get(): r.update({'sanciones': r.get().get('sanciones',0)+1}); st.error("Sancionado")

    # --- PREMIOS (SUGERENCIAS) ---
    elif pag == 'coach_premios':
        st.header("🎁 SUGERIR PREMIO")
        n = st.text_area("Nota")
        if st.button("ENVIAR"): db.reference('sugerencias').push().set({'m': n, 'c': u_act['nombre']}); st.success("Enviado")

    elif pag == 'ver_sugerencias':
        st.header("📩 BUZÓN")
        s = db.reference('sugerencias').get()
        if s:
            for k, v in s.items():
                st.markdown(f'<div class="card"><b>De: {v["c"]}</b><br>{v["m"]}</div>', unsafe_allow_html=True)
                if st.button("Leído", key=k): db.reference(f'sugerencias/{k}').delete(); st.rerun()

    # --- EVENTOS ---
    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS")
        evs = db.reference('eventos').get()
        if evs:
            for k, v in evs.items():
                st.markdown(f'<div class="card"><h3>{v["nombre"]}</h3>{v["descripcion"]}</div>', unsafe_allow_html=True)
                if st.button("ASISTIR", key=k): db.reference(f'eventos/{k}/asistentes/{id_act}').set(u_act['nombre']); st.success("Anotado")
 

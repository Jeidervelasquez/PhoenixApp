import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64
import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="ZENITH E-SPORTS", layout="wide", initial_sidebar_state="collapsed")

def set_bg_hack(main_bg):
    try:
        with open(main_bg, "rb") as f: data = f.read()
        bin_str = base64.b64encode(data).decode()
        st.markdown(f"""<style>.stApp {{ background: linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url(data:image/png;base64,{bin_str}); background-size: cover; background-position: center; background-attachment: fixed; }}</style>""", unsafe_allow_html=True)
    except: st.markdown("<style>.stApp {background-color: #0E1117;}</style>", unsafe_allow_html=True)

set_bg_hack('fondo.jpg')

# --- 2. CONEXIÓN FIREBASE ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})
    except: st.error("⚠️ Error Crítico: No se encontró 'llave.json'.")

# --- CONSTANTES ---
ID_LIDER_MAESTRO = "1234" # Tu Contraseña Maestra de Líder
ROLES_JUEGO = ["Jungla", "Experiencia", "Mid", "Roam", "ADC"]

def notificar_telefono(mensaje):
    st.toast(f"🔔 NOTIFICACIÓN ENVIADA: {mensaje}")

# --- 3. ESTILOS PRO ---
st.markdown("""
    <style>
    h1, h2, h3, p, div, span, label, th, td { color: white !important; text-shadow: 1px 1px 3px #000; }
    .card { background-color: rgba(15, 23, 42, 0.85) !important; padding: 20px; border-radius: 12px; border: 2px solid #3B82F6 !important; margin-bottom: 15px; }
    .stButton>button { border-radius: 8px !important; font-weight: bold !important; height: 3em; width: 100%; border: 1px solid white !important; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); filter: brightness(1.2); }
    .btn-rojo button { background-color: #E63946 !important; }
    .btn-verde button { background-color: #2A9D8F !important; }
    .btn-dorado button { background-color: #F4A261 !important; color: black !important; }
    .btn-cyan button { background-color: #457B9D !important; }
    .btn-gris button { background-color: #1D3557 !important; }
    .stTextInput > div > div > input { color: white !important; background-color: rgba(255,255,255,0.1) !important; border: 1px solid #3B82F6 !important; }
    </style>
    """, unsafe_allow_html=True)

if 'pagina' not in st.session_state: st.session_state['pagina'] = 'login'
def ir_a(pag): st.session_state['pagina'] = pag; st.rerun()

# ==========================================
# 1. LOGIN
# ==========================================
if st.session_state['pagina'] == 'login':
    st.markdown("<h1 style='text-align: center; color: #48CAE4; font-size: 50px;'>⚡ ZENITH E-SPORTS ⚡</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        id_in = st.text_input("Ingresa tu Contraseña", type="password").strip()
        if st.button("ENTRAR A ZENITH"):
            if id_in:
                res = db.reference(f'usuarios/{id_in}').get()
                if res:
                    st.session_state['usuario'], st.session_state['id_actual'] = res, id_in
                    ir_a('menu')
                else: st.error("❌ Contraseña incorrecta.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 2. MENÚ PRINCIPAL
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u, my_id = st.session_state['usuario'], st.session_state['id_actual']
    rol = u.get('rol', 'Miembro')
    if str(my_id) == ID_LIDER_MAESTRO: rol = "Lider"

    sanciones_actuales = u.get('sanciones', 0)
    suspendido = sanciones_actuales >= 3

    st.markdown(f"<div class='card'><h2 style='text-align:center; color:#48CAE4;'>🖥️ DASHBOARD {rol.upper()}</h2><p style='text-align:center; font-size:20px;'>Bienvenido, <b>{u.get('nombre')}</b></p></div>", unsafe_allow_html=True)

    anuncios = db.reference('anuncios').get()
    if anuncios:
        for k, a in anuncios.items(): st.warning(f"📢 **AVISO DE {a['autor']}:** {a['texto']}")

    if suspendido:
        st.error(f"🚫 ATENCIÓN: Tienes {sanciones_actuales} sanciones. ESTÁS SUSPENDIDO esta semana. No podrás participar en eventos ni scrims.")

    c1, c2, c3 = st.columns(3)

    # --- COLUMNA 1: GESTIÓN ---
    with c1:
        st.subheader("🛡️ Gestión y Clan")
        st.markdown('<div class="btn-cyan">', unsafe_allow_html=True)
        if st.button("📋 LISTA DEL CLAN"): ir_a('lista')
        if st.button("🏆 VER EVENTOS"): ir_a('ver_eventos')
        if st.button("📜 REGLAS OFICIALES"): ir_a('reglas')
        if st.button("🎥 CLIPS DESTACADOS"): ir_a('clips')
        st.markdown('</div>', unsafe_allow_html=True)

        if rol in ["Lider", "Administrador", "Moderador"]:
            st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
            if st.button("📝 REGISTRAR MIEMBRO"): ir_a('registro')
            if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
            st.markdown('</div>', unsafe_allow_html=True)

    # --- COLUMNA 2: DEPORTIVO ---
    with c2:
        st.subheader("⚔️ Área Deportiva")
        st.markdown('<div class="btn-dorado">', unsafe_allow_html=True)
        if st.button("🏅 HALL OF FAME"): ir_a('hall_of_fame')
        if st.button("🎮 HISTORIAL DE SCRIMS"): ir_a('partidas')
        if st.button("👀 VER LINEUP"): ir_a('ver_lineup')
        if st.button("⭐ RANKING DE PUNTOS"): ir_a('ranking_coach')
        st.markdown('</div>', unsafe_allow_html=True)

        if rol in ["Lider", "Coach", "Moderador"]:
            if st.button("⚔️ FORMAR EQUIPOS (5v5)"): ir_a('coach_equipos')
        
        if rol in ["Lider", "Coach"]:
            if st.button("📝 DEFINIR LINEUP OFICIAL"): ir_a('definir_lineup')

        if rol in ["Administrador", "Coach"]:
            if st.button("📈 DAR PUNTOS (COACH)"): ir_a('coach_puntos')

    # --- COLUMNA 3: ADMINISTRACIÓN / EXCLUSIVO LÍDER ---
    with c3:
        st.subheader("⚙️ Administración")
        if rol in ["Lider", "Administrador"]:
            st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
            if st.button("📢 PUBLICAR ANUNCIO"): ir_a('crear_anuncio')
            if st.button("📊 EVALUAR JUGADORES"): ir_a('evaluar_jugadores')
            if st.button("⚖️ EVALUAR MODERADORES"): ir_a('evaluar_mods')
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
            st.markdown('</div>', unsafe_allow_html=True)

        if rol == "Lider":
            st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
            if st.button("💎 TESORERÍA (DIAMANTES)"): ir_a('diamantes')
            if st.button("📩 VER NOTAS DEL COACH"): ir_a('ver_sugerencias')
            if st.button("🔧 CAMBIAR CONTRASEÑA DE ALGUIEN"): ir_a('cambio_id')
            if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
            st.markdown('</div>', unsafe_allow_html=True)
            
        if rol == "Coach":
            if st.button("🎁 SUGERIR PREMIO AL LÍDER"): ir_a('coach_premios')

    st.markdown("---")
    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. FUNCIONES
# ==========================================
else:
    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL DASHBOARD"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag, u_act, id_act = st.session_state['pagina'], st.session_state['usuario'], st.session_state['id_actual']
    rol_s = u_act.get('rol', 'Miembro')
    if str(id_act) == ID_LIDER_MAESTRO: rol_s = "Lider"
    suspendido = u_act.get('sanciones', 0) >= 3

    # --- EVENTOS: CREAR (CORREGIDO) ---
    if pag == 'crear_evento':
        st.header("📅 CREAR EVENTO / SCRIM")
        with st.form("ev"):
            t = st.text_input("Nombre del Evento (Ej: Entrenamiento, Torneo)")
            f = st.date_input("Fecha del Evento")
            d = st.text_area("Nota / Descripción para los miembros")
            
            if st.form_submit_button("PUBLICAR EVENTO"):
                db.reference('eventos').push().set({'nombre': t, 'fecha': str(f), 'descripcion': d})
                notificar_telefono(f"NUEVO EVENTO: {t} para la fecha {f}")
                st.success("Evento publicado correctamente.")

    # --- EVENTOS: VER Y ELIMINAR ---
    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS ACTIVOS")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f'<div class="card"><h3 style="color:#F4A261;">⚡ {info["nombre"]}</h3><b>📅 Fecha:</b> {info.get("fecha", "Sin fecha")}<br><br><b>📝 Nota:</b> {info["descripcion"]}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                if not suspendido:
                    if c1.button("🙋 ASISTIR", key=f"a_{eid}"):
                        db.reference(f'eventos/{eid}/asistentes/{id_act}').set(u_act['nombre'])
                        st.success("Anotado")
                else: c1.error("Estás suspendido.")

                # SOLO LÍDER Y MODERADOR ELIMINAN
                if rol_s in ["Lider", "Moderador"]:
                    st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
                    if c2.button("🗑️ ELIMINAR EVENTO", key=f"del_{eid}"):
                        db.reference(f'eventos/{eid}').delete(); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                asis = info.get('asistentes', {})
                if asis: st.write(f"✅ **Asistentes:** {', '.join(asis.values())}")
        else: st.info("No hay eventos próximos.")

    # --- LISTA DEL CLAN (PRIVACIDAD ESTRICTA) ---
    elif pag == 'lista':
        st.header("📋 INTEGRANTES DE ZENITH")
        data = db.reference('usuarios').get()
        if data:
            for k, v in data.items():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                # SOLO EL LÍDER VE CONTRASEÑAS DE OTROS.
                if rol_s == "Lider":
                    st.error(f"🔑 Contraseña del usuario: {k}")
                elif str(id_act) == str(k):
                    st.error(f"🔑 Tu Contraseña: {k}")
                
                st.write(f"👤 **{v['nombre']}** | 🛡️ {v['rol']}")
                if v.get('rol') not in ['Coach', 'Administrador']:
                    st.write(f"🎮 **Roles:** {v.get('rol_primario')} / {v.get('rol_secundario')}")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- REGISTRO DE MIEMBROS (LÍDER EXCLUIDO) ---
    elif pag == 'registro':
        st.header("📝 REGISTRAR NUEVO GUERRERO")
        with st.form("reg"):
            ni = st.text_input("Contraseña del Nuevo Usuario")
            nn = st.text_input("Nombre / Nickname")
            
            # NADIE puede crear un Líder.
            nr = st.selectbox("Rango", ["Miembro", "Moderador", "Coach", "Administrador"])
            
            p_rol, s_rol = "N/A", "N/A"
            if nr not in ["Coach", "Administrador"]:
                p_rol = st.selectbox("Rol Primario", ROLES_JUEGO)
                s_rol = st.selectbox("Rol Secundario", ROLES_JUEGO)
                
            if st.form_submit_button("REGISTRAR"):
                datos = {'nombre':nn, 'rol':nr, 'Diamantes':0, 'deuda':0, 'sanciones':0, 'puntos_coach':0, 'rol_primario':p_rol, 'rol_secundario':s_rol}
                db.reference(f'usuarios/{ni}').set(datos)
                st.success("Registrado correctamente.")

    # --- DEFINIR LINEUP (LIDER / COACH) ---
    elif pag == 'definir_lineup':
        st.header("📝 DEFINIR LINEUP OFICIAL")
        data = db.reference('usuarios').get()
        if data:
            opc = [f"{v['nombre']} ({v.get('rol_primario','?')})" for k,v in data.items() if v.get('rol') not in ['Coach', 'Administrador']]
            tits = st.multiselect("5 Titulares", opc)
            sups = st.multiselect("5 Suplentes", opc)
            if st.button("GUARDAR LINEUP"):
                if len(tits) == 5 and len(sups) == 5:
                    db.reference('lineup_actual').set({'titulares': tits, 'suplentes': sups, 'autor': u_act['nombre']})
                    st.success("Lineup Actualizado")
                else: st.warning("Debes elegir 5 de cada uno.")

    # --- CREAR EQUIPOS 5v5 (Lider, Mod, Coach) ---
    elif pag == 'coach_equipos':
        st.header("⚔️ CREAR EQUIPOS 5v5")
        data = db.reference('usuarios').get()
        if data:
            opc = [f"{v['nombre']} ({v.get('rol_primario','?')})" for k,v in data.items() if v.get('rol') not in ['Coach', 'Administrador']]
            n_eq = st.text_input("Nombre del Equipo")
            j_eq = st.multiselect("Selecciona 5 Integrantes", opc)
            if st.button("REGISTRAR EQUIPO"):
                db.reference('equipos').push().set({'nombre': n_eq, 'jugadores': j_eq})
                st.success("Equipo Creado.")
        
        st.subheader("Equipos Registrados")
        eqs = db.reference('equipos').get()
        if eqs:
            for k, v in eqs.items():
                st.info(f"🚩 **{v['nombre']}**: {', '.join(v['jugadores'])}")
                if st.button("Borrar Equipo", key=k): db.reference(f'equipos/{k}').delete(); st.rerun()

    # --- RESTO DE FUNCIONES (Solo código estructurado) ---
    elif pag == 'coach_puntos':
        st.header("📈 DAR PUNTOS (COACH / ADMIN)")
        data = db.reference('usuarios').get()
        for k, v in data.items():
            if v.get('rol') not in ['Coach', 'Administrador']:
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"👤 {v['nombre']} (Actual: {v.get('puntos_coach', 0)})")
                    pts = c2.number_input("Pts", step=1, key=f"p_{k}")
                    if st.button("DAR", key=f"b_{k}"):
                        db.reference(f'usuarios/{k}').update({'puntos_coach': v.get('puntos_coach', 0) + pts}); st.rerun()

    elif pag == 'evaluar_jugadores':
        st.header("📊 EVALUACIÓN DE JUGADORES (1 al 10)")
        data = db.reference('usuarios').get()
        jugadores = {k: v['nombre'] for k, v in data.items() if v.get('rol') == 'Miembro'}
        j_sel = st.selectbox("Jugador", list(jugadores.keys()), format_func=lambda x: jugadores[x])
        if j_sel:
            rend = st.slider("Rendimiento", 1, 10, 5); act = st.slider("Actitud", 1, 10, 5)
            com = st.slider("Comunicación", 1, 10, 5); comp = st.slider("Compromiso", 1, 10, 5)
            if st.button("GUARDAR"):
                db.reference(f'usuarios/{j_sel}/evaluacion_admin').set({'rendimiento': rend, 'actitud': act, 'comunicacion': com, 'compromiso': comp})
                st.success("Guardado.")

    elif pag == 'evaluar_mods':
        st.header("⚖️ EVALUACIÓN DE MODERADORES")
        data = db.reference('usuarios').get()
        mods = {k: v['nombre'] for k, v in data.items() if v.get('rol') == 'Moderador'}
        if mods:
            m_sel = st.selectbox("Moderador", list(mods.keys()), format_func=lambda x: mods[x])
            actividad = st.slider("Actividad", 1, 10, 5); inter = st.slider("Intervención", 1, 10, 5)
            if st.button("EVALUAR"):
                db.reference(f'usuarios/{m_sel}/evaluacion_mod').set({'actividad': actividad, 'inter': inter})
                st.success("Guardado.")
        else: st.info("No hay moderadores.")

    elif pag == 'sanciones':
        st.header("⚠️ SANCIONES")
        tid = st.text_input("Contraseña (ID) del Infractor")
        if st.button("APLICAR MULTA (+1)"):
            r = db.reference(f'usuarios/{tid}')
            if r.get():
                n = r.get().get('sanciones', 0) + 1
                r.update({'sanciones': n})
                if n >= 3: notificar_telefono(f"¡{r.get()['nombre']} ha sido SUSPENDIDO!")
                st.error(f"Sancionado. Total: {n}")
        if st.button("PERDONAR (CERO)"):
            r = db.reference(f'usuarios/{tid}')
            if r.get(): r.update({'sanciones': 0}); st.success("Limpiado.")

    elif pag == 'eliminar':
        st.header("❌ ELIMINAR MIEMBRO")
        did = st.text_input("Contraseña a eliminar")
        if st.button("CONFIRMAR DESPIDO"):
            db.reference(f'usuarios/{did}').delete(); st.success("Borrado"); st.rerun()

    elif pag == 'cambio_id':
        st.header("🔧 CAMBIAR CONTRASEÑA")
        oid, nid = st.text_input("Actual"), st.text_input("Nueva")
        if st.button("CAMBIAR"):
            d = db.reference(f'usuarios/{oid}').get()
            if d: db.reference(f'usuarios/{nid}').set(d); db.reference(f'usuarios/{oid}').delete(); st.success("Listo")
            
    elif pag == 'diamantes':
        st.header("💎 TESORERÍA")
        tid = st.text_input("Contraseña (ID)"); amt = st.number_input("Monto", step=1)
        if st.button("SUMAR"):
            r = db.reference(f'usuarios/{tid}')
            if r.get(): r.update({'Diamantes': r.get().get('Diamantes',0)+amt}); st.success("Ok")

    elif pag == 'crear_anuncio':
        st.header("📢 PUBLICAR ANUNCIO GLOBAL")
        txt = st.text_area("Anuncio para el clan")
        if st.button("PUBLICAR"):
            db.reference('anuncios').push().set({'texto': txt, 'autor': u_act['nombre']})
            st.success("Publicado.")

    elif pag == 'hall_of_fame':
        st.header("🏅 HALL OF FAME ZENITH")
        if rol_s == "Lider":
            with st.expander("Modificar"):
                mj = st.text_input("Mejor Jugador"); md = st.text_input("Más Disciplinado")
                ma = st.text_input("Más Asistente"); mvp = st.text_input("MVP Histórico")
                if st.button("ACTUALIZAR"):
                    db.reference('hall_of_fame').set({'mejor_jugador': mj, 'mas_disciplinado': md, 'mas_asistente': ma, 'mvp': mvp})
                    st.success("Actualizado")
        hof = db.reference('hall_of_fame').get() or {}
        st.markdown(f'<div class="card" style="text-align:center;"><h3>Mejor Jugador: {hof.get("mejor_jugador", "N/A")}</h3><h3>MVP: {hof.get("mvp", "N/A")}</h3></div>', unsafe_allow_html=True)

    elif pag == 'reglas':
        st.header("📜 REGLAS OFICIALES")
        if rol_s == "Lider":
            nr = st.text_area("Editar Reglas")
            if st.button("GUARDAR"): db.reference('reglas_oficiales').set({'texto': nr}); st.success("Ok")
        r = db.reference('reglas_oficiales').get()
        if r: st.markdown(f'<div class="card">{r["texto"]}</div>', unsafe_allow_html=True)
        
    elif pag == 'ver_lineup':
        st.header("👀 LINEUP OFICIAL")
        l = db.reference('lineup_actual').get()
        if l:
            st.success(f"📌 Por: {l.get('autor')}")
            st.markdown("### 🔥 TITULARES"); [st.info(t) for t in l.get('titulares', [])]
            st.markdown("### 💤 SUPLENTES"); [st.warning(s) for s in l.get('suplentes', [])]
            
    elif pag == 'ranking_coach':
        st.header("⭐ RANKING PUNTOS")
        data = db.reference('usuarios').get()
        if data:
            r = sorted([{'n':v['nombre'], 'p':v.get('puntos_coach',0)} for k,v in data.items() if v.get('rol') not in ['Coach', 'Admin']], key=lambda x:x['p'], reverse=True)
            for i, j in enumerate(r): st.write(f"{i+1}. {j['n']} - {j['p']} Pts")
            
    elif pag == 'partidas':
        st.header("🎮 HISTORIAL DE SCRIMS")
        if rol_s in ["Lider", "Administrador", "Coach", "Moderador"]:
            with st.form("s"):
                riv = st.text_input("Rival"); f = st.date_input("Fecha"); res = st.selectbox("Resultado", ["Victoria", "Derrota"])
                if st.form_submit_button("GUARDAR"): db.reference('partidas').push().set({'rival': riv, 'fecha': str(f), 'resultado': res}); st.success("Ok")
        ps = db.reference('partidas').get()
        if ps:
            for k, v in ps.items(): st.markdown(f'<div class="card">🆚 Zenith vs {v["rival"]} | {v["fecha"]} | <b>{v["resultado"]}</b></div>', unsafe_allow_html=True)
            
    elif pag == 'clips':
        st.header("🎥 CLIPS")
        if rol_s in ["Lider", "Administrador", "Moderador"]:
            url = st.text_input("URL"); tit = st.text_input("Título")
            if st.button("SUBIR"): db.reference('clips').push().set({'url': url, 'titulo': tit, 'autor': u_act['nombre']}); st.success("Ok")
        c = db.reference('clips').get()
        if c:
            for k, v in c.items(): st.markdown(f'<div class="card"><h4>{v["titulo"]}</h4><a href="{v["url"]}">Ver Video</a></div>', unsafe_allow_html=True)
            
    elif pag == 'ver_sugerencias':
        st.header("📩 NOTAS DEL COACH")
        s = db.reference('sugerencias').get()
        if s:
            for k, v in s.items():
                st.write(f"De: {v['c']} - {v['m']}")
                if st.button("Borrar", key=k): db.reference(f'sugerencias/{k}').delete(); st.rerun()
                
    elif pag == 'coach_premios':
        st.header("🎁 SUGERIR PREMIO")
        n = st.text_area("Nota al Líder")
        if st.button("ENVIAR"): db.reference('sugerencias').push().set({'m': n, 'c': u_act['nombre']}); st.success("Ok")

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64
import datetime
import os

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="KYSEN E-SPORTS", layout="wide", initial_sidebar_state="collapsed")

def set_bg_hack(main_bg):
    try:
        with open(main_bg, "rb") as f: data = f.read()
        bin_str = base64.b64encode(data).decode()
        st.markdown(f"""
            <style>
            .stApp {{ 
                background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(data:image/png;base64,{bin_str}) !important; 
                background-size: cover !important; 
                background-position: center center !important; 
                background-repeat: no-repeat !important; 
            }}
            </style>
            """, unsafe_allow_html=True)
    except: 
        st.markdown("<style>.stApp {background-color: #0E1117;}</style>", unsafe_allow_html=True)

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

def mostrar_logo():
    if os.path.exists("logo.png"):
        col_logo, col_espacio = st.columns([1, 8])
        with col_logo:
            st.image("logo.png", use_container_width=True)

# NUEVA FUNCIÓN PARA LAS IMÁGENES DE LAS SCRIMS
def procesar_imagen(archivo_subido):
    if archivo_subido is not None:
        return base64.b64encode(archivo_subido.read()).decode()
    return None

# --- 3. ESTILOS PRO (COMPATIBLE CON iOS / iPHONE) ---
st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
        color: white !important;
    }

    h1, h2, h3, p, div, span, label, th, td { 
        color: white !important; 
        text-shadow: 1px 1px 4px rgba(0,0,0,0.9); 
    }
    
    .stButton>button { 
        background-color: rgba(255, 255, 255, 0.15) !important; 
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border-radius: 12px !important; 
        font-weight: bold !important; 
        height: 3em; 
        width: 100%; 
        border: 1px solid rgba(255, 255, 255, 0.3) !important; 
        transition: 0.3s; 
        color: white !important;
    }
    .stButton>button:hover { 
        transform: scale(1.02); 
        background-color: rgba(72, 202, 228, 0.3) !important; 
    }
    
    .btn-rojo button { border-color: #E63946 !important; }
    .btn-verde button { border-color: #2A9D8F !important; }
    .btn-dorado button { border-color: #F4A261 !important; }
    .btn-cyan button { border-color: #457B9D !important; }
    .btn-gris button { border-color: #adb5bd !important; }
    
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { 
        color: white !important; 
        background-color: rgba(0,0,0,0.4) !important; 
        border: 1px solid rgba(255,255,255,0.2) !important; 
        border-bottom: 2px solid #3B82F6 !important; 
        border-radius: 8px !important;
        box-shadow: none !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-bottom: 2px solid #48CAE4 !important; 
        background-color: rgba(0,0,0,0.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)

if 'pagina' not in st.session_state: st.session_state['pagina'] = 'login'
def ir_a(pag): st.session_state['pagina'] = pag; st.rerun()

mostrar_logo()

# ==========================================
# 1. LOGIN
# ==========================================
if st.session_state['pagina'] == 'login':
    st.markdown("<h1 style='text-align: center; color: #48CAE4; font-size: 50px; margin-top: 50px;'>⚡ KYSEN E-SPORTS ⚡</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.write("")
        id_in = st.text_input("Ingresa tu Contraseña", type="password").strip()
        st.write("")
        if st.button("ENTRAR A KYSEN"):
            if id_in:
                res = db.reference(f'usuarios/{id_in}').get()
                if res:
                    st.session_state['usuario'], st.session_state['id_actual'] = res, id_in
                    ir_a('menu')
                else: st.error("❌ Contraseña incorrecta.")

# ==========================================
# 2. MENÚ PRINCIPAL
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u, my_id = st.session_state['usuario'], st.session_state['id_actual']
    rol = u.get('rol', 'Miembro')
    if str(my_id) == ID_LIDER_MAESTRO: rol = "Lider"

    sanciones_actuales = u.get('sanciones', 0)
    suspendido = sanciones_actuales >= 3

    id_juego_u = u.get('id_juego', 'No registrado')
    rol_primario = u.get('rol_primario', 'N/A')
    rol_secundario = u.get('rol_secundario', 'N/A')

    st.markdown(f"""
        <div style='text-align:center; margin-bottom: 30px;'>
            <h2 style='color:#48CAE4;'>🖥️ DASHBOARD {rol.upper()}</h2>
            <p style='font-size:24px;'>Bienvenido, <b>{u.get('nombre')}</b></p>
            <p style='font-size:18px; color:#F4A261;'>🎮 ID del Juego: <b>{id_juego_u}</b></p>
            <p style='font-size:18px;'>⚔️ Rol Primario: <b style='color:#2A9D8F;'>{rol_primario}</b> &nbsp;&nbsp;|&nbsp;&nbsp; 🛡️ Rol Secundario: <b style='color:#E63946;'>{rol_secundario}</b></p>
        </div>
    """, unsafe_allow_html=True)

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
        st.markdown('</div>', unsafe_allow_html=True)

        if rol in ["Lider", "Administrador"]:
            st.markdown('<div class="btn-dorado">', unsafe_allow_html=True)
            if st.button("⭐ RANKING PTS BENEFICIO"): ir_a('ranking_beneficios')
            st.markdown('</div>', unsafe_allow_html=True)

        if rol in ["Lider", "Coach"]:
            st.markdown('<div class="btn-dorado">', unsafe_allow_html=True)
            if st.button("⭐ RANKING PTS COACH"): ir_a('ranking_coach')
            st.markdown('</div>', unsafe_allow_html=True)

        if rol in ["Lider", "Coach", "Moderador"]:
            if st.button("⚔️ FORMAR EQUIPOS (5v5)"): ir_a('coach_equipos')
        
        if rol in ["Lider", "Coach"]:
            if st.button("📝 DEFINIR LINEUP OFICIAL"): ir_a('definir_lineup')

        if rol == "Coach":
            st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
            if st.button("📈 DAR PUNTOS (COACH)"): ir_a('dar_puntos_coach')
            st.markdown('</div>', unsafe_allow_html=True)
            
        if rol in ["Lider", "Administrador"]:
            st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
            if st.button("🎁 DAR PUNTOS BENEFICIO"): ir_a('dar_puntos_beneficios')
            st.markdown('</div>', unsafe_allow_html=True)

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
    st.write("---")
    
    pag, u_act, id_act = st.session_state['pagina'], st.session_state['usuario'], st.session_state['id_actual']
    rol_s = u_act.get('rol', 'Miembro')
    if str(id_act) == ID_LIDER_MAESTRO: rol_s = "Lider"
    suspendido = u_act.get('sanciones', 0) >= 3

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

    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS ACTIVOS")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f'<h3 style="color:#F4A261;">⚡ {info["nombre"]}</h3><p><b>📅 Fecha:</b> {info.get("fecha", "Sin fecha")}<br><b>📝 Nota:</b> {info["descripcion"]}</p>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                if not suspendido:
                    if c1.button("🙋 ASISTIR", key=f"a_{eid}"):
                        db.reference(f'eventos/{eid}/asistentes/{id_act}').set(u_act['nombre'])
                        st.success("Anotado")
                else: c1.error("Estás suspendido.")

                if rol_s in ["Lider", "Moderador"]:
                    st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
                    if c2.button("🗑️ ELIMINAR EVENTO", key=f"del_{eid}"):
                        db.reference(f'eventos/{eid}').delete(); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                asis = info.get('asistentes', {})
                if asis: st.write(f"✅ **Asistentes:** {', '.join(asis.values())}")
                st.write("---")
        else: st.info("No hay eventos próximos.")

    elif pag == 'lista':
        st.header("📋 INTEGRANTES DE KYSEN")
        data = db.reference('usuarios').get()
        if data:
            for k, v in data.items():
                if rol_s == "Lider":
                    st.error(f"🔑 Contraseña del usuario: {k}")
                elif str(id_act) == str(k):
                    st.error(f"🔑 Tu Contraseña: {k}")
                
                st.write(f"👤 **{v['nombre']}** | 🛡️ {v['rol']} | 🎮 ID: {v.get('id_juego', 'N/A')}")
                if v.get('rol') not in ['Coach', 'Administrador']:
                    st.write(f"⚔️ **Roles:** {v.get('rol_primario')} / {v.get('rol_secundario')}")
                st.write("---")

    elif pag == 'registro':
        st.header("📝 REGISTRAR NUEVO GUERRERO")
        with st.form("reg"):
            ni = st.text_input("Contraseña del Nuevo Usuario")
            nn = st.text_input("Nombre / Nickname")
            id_j = st.text_input("ID del Juego (Obligatorio)") 
            
            nr = st.selectbox("Rango", ["Miembro", "Moderador", "Coach", "Administrador"])
            
            p_rol, s_rol = "N/A", "N/A"
            if nr not in ["Coach", "Administrador"]:
                p_rol = st.selectbox("Rol Primario", ROLES_JUEGO)
                s_rol = st.selectbox("Rol Secundario", ROLES_JUEGO)
                
            if st.form_submit_button("REGISTRAR"):
                if id_j.strip() == "":
                    st.error("⚠️ El ID del Juego no puede estar vacío.")
                else:
                    datos = {'nombre':nn, 'id_juego': id_j, 'rol':nr, 'Diamantes':0, 'deuda':0, 'sanciones':0, 'puntos_coach':0, 'puntos_beneficio': 0, 'rol_primario':p_rol, 'rol_secundario':s_rol}
                    db.reference(f'usuarios/{ni}').set(datos)
                    st.success(f"Miembro {nn} registrado correctamente.")

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
                st.write(f"🚩 **{v['nombre']}**: {', '.join(v['jugadores'])}")
                if st.button("Borrar Equipo", key=k): db.reference(f'equipos/{k}').delete(); st.rerun()

    elif pag == 'dar_puntos_coach':
        st.header("📈 DAR PUNTOS COACH (Solo Coach)")
        data = db.reference('usuarios').get()
        for k, v in data.items():
            if v.get('rol') not in ['Coach', 'Administrador', 'Lider']:
                c1, c2 = st.columns([3, 1])
                c1.write(f"👤 {v['nombre']} (Actual: {v.get('puntos_coach', 0)})")
                pts = c2.number_input("Pts Coach", step=1, key=f"pc_{k}")
                if st.button("DAR", key=f"bc_{k}"):
                    db.reference(f'usuarios/{k}').update({'puntos_coach': v.get('puntos_coach', 0) + pts}); st.rerun()

    elif pag == 'ranking_coach':
        st.header("⭐ RANKING PUNTOS COACH")
        data = db.reference('usuarios').get()
        if data:
            r = sorted([{'n':v['nombre'], 'p':v.get('puntos_coach',0)} for k,v in data.items() if v.get('rol') not in ['Coach', 'Admin', 'Lider']], key=lambda x:x['p'], reverse=True)
            for i, j in enumerate(r): st.write(f"{i+1}. **{j['n']}** - {j['p']} Pts Coach")

    elif pag == 'dar_puntos_beneficios':
        st.header("🎁 DAR PUNTOS DE BENEFICIO")
        data = db.reference('usuarios').get()
        for k, v in data.items():
            if v.get('rol') not in ['Coach', 'Administrador', 'Lider']:
                c1, c2 = st.columns([3, 1])
                c1.write(f"👤 {v['nombre']} (Actual: {v.get('puntos_beneficio', 0)})")
                pts = c2.number_input("Pts Beneficio", step=1, key=f"pb_{k}")
                if st.button("DAR", key=f"bb_{k}"):
                    db.reference(f'usuarios/{k}').update({'puntos_beneficio': v.get('puntos_beneficio', 0) + pts}); st.rerun()

    elif pag == 'ranking_beneficios':
        st.header("⭐ RANKING PUNTOS DE BENEFICIO")
        data = db.reference('usuarios').get()
        if data:
            r = sorted([{'n':v['nombre'], 'p':v.get('puntos_beneficio',0)} for k,v in data.items() if v.get('rol') not in ['Coach', 'Admin', 'Lider']], key=lambda x:x['p'], reverse=True)
            for i, j in enumerate(r): st.write(f"{i+1}. **{j['n']}** - {j['p']} Pts Beneficio")

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
        st.header("🏅 HALL OF FAME KYSEN")
        if rol_s == "Lider":
            with st.expander("Modificar"):
                mj = st.text_input("Mejor Jugador"); md = st.text_input("Más Disciplinado")
                ma = st.text_input("Más Asistente"); mvp = st.text_input("MVP Histórico")
                if st.button("ACTUALIZAR"):
                    db.reference('hall_of_fame').set({'mejor_jugador': mj, 'mas_disciplinado': md, 'mas_asistente': ma, 'mvp': mvp})
                    st.success("Actualizado")
        hof = db.reference('hall_of_fame').get() or {}
        st.markdown(f'<div style="text-align:center;"><h3>Mejor Jugador: <span style="color:#48CAE4;">{hof.get("mejor_jugador", "N/A")}</span></h3><h3>MVP: <span style="color:#F4A261;">{hof.get("mvp", "N/A")}</span></h3></div>', unsafe_allow_html=True)

    elif pag == 'reglas':
        st.header("📜 REGLAS OFICIALES")
        if rol_s == "Lider":
            nr = st.text_area("Editar Reglas")
            if st.button("GUARDAR"): db.reference('reglas_oficiales').set({'texto': nr}); st.success("Ok")
        r = db.reference('reglas_oficiales').get()
        if r: st.markdown(f'<p>{r["texto"]}</p>', unsafe_allow_html=True)
        
    elif pag == 'ver_lineup':
        st.header("👀 LINEUP OFICIAL")
        l = db.reference('lineup_actual').get()
        if l:
            st.success(f"📌 Por: {l.get('autor')}")
            st.markdown("### 🔥 TITULARES"); [st.write(f"⚔️ {t}") for t in l.get('titulares', [])]
            st.markdown("### 💤 SUPLENTES"); [st.write(f"🛡️ {s}") for s in l.get('suplentes', [])]
            
    # --- LA NUEVA SECCIÓN PRO DE PARTIDAS ---
    elif pag == 'partidas':
        st.header("🎮 HISTORIAL DE SCRIMS Y ESTADÍSTICAS")
        ps = db.reference('partidas').get() or {}

        # --- 1. ESTADÍSTICAS CONTRA ESCUADRONES ---
        if ps:
            st.subheader("📊 NUESTRO RÉCORD CONTRA RIVALES")
            stats = {}
            for k, v in ps.items():
                rival = str(v.get('rival', 'Desconocido')).upper().strip()
                if rival not in stats:
                    stats[rival] = {'Victoria': 0, 'Derrota': 0}
                res = v.get('resultado', 'Derrota')
                if res in stats[rival]:
                    stats[rival][res] += 1

            cols = st.columns(3)
            idx = 0
            for rival, data in stats.items():
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style='background-color:rgba(0,0,0,0.4); padding:10px; border-radius:10px; border:1px solid #48CAE4; text-align:center; margin-bottom: 10px;'>
                        <h4 style='color:#F4A261; margin:0;'>{rival}</h4>
                        <span style='color:#2A9D8F; font-size:18px;'><b>V: {data['Victoria']}</b></span> |
                        <span style='color:#E63946; font-size:18px;'><b>D: {data['Derrota']}</b></span>
                    </div>
                    """, unsafe_allow_html=True)
                idx += 1
            st.write("---")

        # --- 2. HERRAMIENTAS DE GESTIÓN ---
        if rol_s in ["Lider", "Administrador", "Coach", "Moderador"]:
            col_reg, col_img = st.columns(2)
            with col_reg:
                with st.expander("📝 1. REGISTRAR RESULTADO"):
                    with st.form("form_scrim"):
                        riv = st.text_input("Nombre del Clan Rival")
                        f = st.date_input("Fecha del encuentro")
                        res = st.selectbox("Resultado Final", ["Victoria", "Derrota"])
                        if st.form_submit_button("GUARDAR REGISTRO"):
                            db.reference('partidas').push().set({'rival': riv, 'fecha': str(f), 'resultado': res})
                            st.success("✅ Partida registrada en la base de datos.")
                            st.rerun()

            with col_img:
                with st.expander("🖼️ 2. ADJUNTAR CAPTURA"):
                    if ps:
                        opciones = {k: f"{v['fecha']} | Kysen vs {v['rival']} ({v['resultado']})" for k, v in ps.items()}
                        id_partida = st.selectbox("Selecciona a quién le ponemos la foto:", list(opciones.keys()), format_func=lambda x: opciones[x])
                        img_file = st.file_uploader("Sube la imagen (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
                        if st.button("VINCULAR IMAGEN"):
                            if img_file and id_partida:
                                img_str = procesar_imagen(img_file)
                                db.reference(f'partidas/{id_partida}').update({'imagen': img_str})
                                st.success("✅ Captura guardada para este escuadrón.")
                                st.rerun()
                            else:
                                st.warning("⚠️ Debes seleccionar un rival y subir un archivo primero.")
                    else:
                        st.info("Primero debes registrar un resultado en el paso 1.")

            st.write("---")

        # --- 3. HISTORIAL DETALLADO ---
        st.subheader("📜 REGISTRO DETALLADO")
        if ps:
            items = list(ps.items())
            items.reverse()
            for k, v in items:
                c1, c2 = st.columns([2, 1])
                with c1:
                    color_r = "#2A9D8F" if v.get('resultado') == "Victoria" else "#E63946"
                    st.markdown(f"<h3 style='margin-bottom:0;'>🆚 Kysen vs {v['rival']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"**Resultado:** <span style='color:{color_r}; font-size:18px;'>{v['resultado']}</span> | **Fecha:** {v['fecha']}", unsafe_allow_html=True)
                    if rol_s == "Lider":
                        if st.button("🗑️ Eliminar Registro", key=f"del_scrim_{k}"):
                            db.reference(f'partidas/{k}').delete()
                            st.rerun()
                with c2:
                    if v.get('imagen'):
                        st.image(f"data:image/png;base64,{v['imagen']}", use_container_width=True)
                    else:
                        st.markdown("<p style='color:#adb5bd; font-style:italic; margin-top:15px;'>Sin captura adjunta</p>", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.info("No hay historial de partidas todavía.")
            
    elif pag == 'ver_sugerencias':
        st.header("📩 NOTAS DEL COACH")
        s = db.reference('sugerencias').get()
        if s:
            for k, v in s.items():
                st.write(f"De: **{v['c']}** - {v['m']}")
                if st.button("Borrar", key=k): db.reference(f'sugerencias/{k}').delete(); st.rerun()
                st.write("---")
                
    elif pag == 'coach_premios':
        st.header("🎁 SUGERIR PREMIO")
        n = st.text_area("Nota al Líder")
        if st.button("ENVIAR"): db.reference('sugerencias').push().set({'m': n, 'c': u_act['nombre']}); st.success("Ok")

import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="PHOENIX EMPIRE PRO", layout="centered", initial_sidebar_state="collapsed")

def set_bg_hack(main_bg):
    try:
        with open(main_bg, "rb") as f: data = f.read()
        bin_str = base64.b64encode(data).decode()
        st.markdown(f"""<style>.stApp {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url(data:image/png;base64,{bin_str}); background-size: cover; background-position: center; background-attachment: fixed; }}</style>""", unsafe_allow_html=True)
    except: st.markdown("<style>.stApp {background-color: #0E1117;}</style>", unsafe_allow_html=True)

set_bg_hack('fondo.jpg')

# --- 2. CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})
    except: st.error("⚠️ Error Crítico: No se encontró 'llave.json'.")

# --- CONSTANTES ---
ID_LIDER_MAESTRO = "1234"  # <--- CAMBIA ESTO POR TU ID
ID_COACH = "0000"          # <--- ID DEL COACH
ROLES_JUEGO = ["Jungla", "Experiencia", "Mid", "Roam", "ADC"]

# --- 3. ESTILOS VISUALES MEJORADOS ---
st.markdown("""
    <style>
    h1, h2, h3, p, div, span, label, .stMarkdown, td, th { color: white !important; text-shadow: 2px 2px 4px #000000 !important; }
    .card { background-color: rgba(0, 0, 0, 0.85) !important; padding: 20px; border-radius: 12px; border: 2px solid #E74C3C !important; margin-bottom: 15px; }
    .stButton>button { border-radius: 8px !important; font-weight: bold !important; height: 3em; width: 100%; border: 1px solid white !important; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); background-color: #E74C3C !important; }
    .btn-rojo button { background-color: #922B21 !important; }
    .btn-verde button { background-color: #1E8449 !important; }
    .btn-dorado button { background-color: #D4AC0D !important; color: black !important; border: 1px solid #F1C40F !important; }
    .btn-gris button { background-color: #566573 !important; }
    .btn-volver button { background-color: #17202A !important; border: 2px solid #E74C3C !important; }
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
            else: st.error("❌ ID no registrado.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 2. MENÚ PRINCIPAL (POR ROLES)
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u, my_id = st.session_state['usuario'], st.session_state['id_actual']
    rol = u.get('rol', 'Miembro')
    if str(my_id) == ID_LIDER_MAESTRO: rol = "Lider"
    if str(my_id) == ID_COACH: rol = "Coach"

    st.markdown(f"<div class='card'><h2 style='text-align:center; color:#3498DB;'>PANEL {rol.upper()}</h2><p style='text-align:center;'>Bienvenido, <b>{u.get('nombre')}</b></p></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if rol in ["Lider", "Moderador", "Miembro"]:
            if st.button("📋 LISTA DEL CLAN"): ir_a('lista')
            if st.button("🏆 VER EVENTOS"): ir_a('ver_eventos')
        
        if rol == "Lider":
            if st.button("📊 RANKING DIAMANTES"): ir_a('ranking')
            if st.button("💎 TESORERÍA"): ir_a('diamantes')
            if st.button("📝 REGISTRAR MIEMBRO"): ir_a('registro')
        
        if rol == "Coach":
            st.markdown('<div class="btn-dorado">', unsafe_allow_html=True)
            if st.button("⚔️ GESTIÓN DE EQUIPOS"): ir_a('coach_equipos')
            if st.button("⭐ RANKING DE PUNTOS"): ir_a('ranking_coach')
            st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        if rol == "Lider":
            if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("📩 VER SUGERENCIAS"): ir_a('ver_sugerencias')
        
        if rol == "Moderador":
            if st.button("💎 GESTIONAR DIAMANTES"): ir_a('diamantes')
            if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
            
        if rol == "Coach":
            if st.button("📈 DAR PUNTOS"): ir_a('coach_puntos')
            if st.button("🎁 SUGERIR PREMIO"): ir_a('coach_premios')

    st.markdown("---")
    # Botones de Acción Rápida (Estilo Colorido)
    if rol in ["Lider", "Coach"]:
        st.markdown('<div class="btn-dorado">', unsafe_allow_html=True)
        if st.button("👀 VER LINEUP ACTUAL"): ir_a('ver_lineup')
        st.markdown('</div>', unsafe_allow_html=True)

    if rol == "Lider":
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. PÁGINAS DE FUNCIONALIDAD
# ==========================================
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag, u_act, id_act = st.session_state['pagina'], st.session_state['usuario'], st.session_state['id_actual']
    
    # Recalcular rol para seguridad en páginas
    rol_s = u_act.get('rol', 'Miembro')
    if str(id_act) == ID_LIDER_MAESTRO: rol_s = "Lider"
    if str(id_act) == ID_COACH: rol_s = "Coach"

    # --- ⚔️ GESTIÓN DE EQUIPOS Y LINEUP (COACH) ---
    if pag == 'coach_equipos':
        st.header("⚔️ GESTIÓN TÁCTICA")
        data = db.reference('usuarios').get()
        if data:
            # Filtrar solo jugadores reales para los selectores
            jugadores_opt = {k: f"{v['nombre']} ({v.get('rol_primario','?')})" for k,v in data.items() if v.get('rol') != 'Coach'}
            opciones = list(jugadores_opt.values())

            # A. SECCIÓN LINEUP
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🔥 Definir Lineup Oficial")
            tits = st.multiselect("Selecciona 5 Titulares", opciones, key="t_lineup")
            sups = st.multiselect("Selecciona 5 Suplentes", opciones, key="s_lineup")
            if st.button("💾 GUARDAR LINEUP"):
                if len(tits) == 5 and len(sups) == 5:
                    db.reference('lineup_actual').set({'titulares': tits, 'suplentes': sups, 'coach': u_act['nombre']})
                    st.success("✅ Lineup guardado exitosamente.")
                else: st.warning("⚠️ Debes elegir exactamente 5 titulares y 5 suplentes.")
            st.markdown('</div>', unsafe_allow_html=True)

            # B. SECCIÓN CREAR EQUIPOS LIBRES
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🚩 Crear Equipo Personalizado")
            nom_eq = st.text_input("Nombre del Equipo (Ej: Escuadrón A)")
            jug_eq = st.multiselect("Integrantes", opciones)
            if st.button("➕ REGISTRAR EQUIPO"):
                if nom_eq and jug_eq:
                    db.reference('equipos').push().set({'nombre': nom_eq, 'jugadores': jug_eq})
                    st.success(f"Equipo '{nom_eq}' creado.")
                else: st.error("Completa el nombre y elige jugadores.")
            st.markdown('</div>', unsafe_allow_html=True)

            # C. VER EQUIPOS CREADOS
            st.subheader("📋 Equipos Registrados")
            eqs = db.reference('equipos').get()
            if eqs:
                for ek, ev in eqs.items():
                    with st.expander(f"📍 {ev['nombre']}"):
                        st.write(f"Jugadores: {', '.join(ev['jugadores'])}")
                        if st.button("Eliminar", key=ek):
                            db.reference(f'equipos/{ek}').delete(); st.rerun()

    # --- 🏆 VER Y ELIMINAR EVENTOS ---
    elif pag == 'ver_eventos':
        st.header("📅 EVENTOS DEL CLAN")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f"""
                <div class="card">
                    <h3 style='color:#E74C3C;'>{info.get('nombre')}</h3>
                    <p>{info.get('descripcion')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                if c1.button("🙋 ASISTIRÉ", key=f"as_{eid}"):
                    db.reference(f'eventos/{eid}/asistentes/{id_act}').set(u_act['nombre'])
                    st.success("Asistencia marcada.")
                
                # SOLO LIDER Y MODERADOR ELIMINAN
                if rol_s in ["Lider", "Moderador"]:
                    st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
                    if c2.button("🗑️ ELIMINAR EVENTO", key=f"del_{eid}"):
                        db.reference(f'eventos/{eid}').delete()
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                asistentes = info.get('asistentes', {})
                if asistentes:
                    st.write(f"✅ **Confirmados:** {', '.join(asistentes.values())}")
        else: st.info("No hay eventos próximos.")

    # --- 📊 RANKING COACH (PUNTOS) ---
    elif pag == 'ranking_coach':
        st.header("⭐ RANKING DE RENDIMIENTO")
        data = db.reference('usuarios').get()
        if data:
            # Lista de diccionarios para ordenar
            ranking_p = []
            for k, v in data.items():
                if v.get('rol') != 'Coach':
                    ranking_p.append({'nombre': v['nombre'], 'pts': v.get('puntos_coach', 0)})
            
            ranking_p = sorted(ranking_p, key=lambda x: x['pts'], reverse=True)
            
            for i, jug in enumerate(ranking_p):
                medalla = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                st.markdown(f'<div class="card">{medalla} <b>{jug["nombre"]}</b> — {jug["pts"]} Puntos</div>', unsafe_allow_html=True)

    # --- 💎 TESORERÍA (COMPLETA) ---
    elif pag == 'diamantes':
        st.header("💎 GESTIÓN FINANCIERA")
        target = st.text_input("ID del Guerrero")
        monto = st.number_input("Cantidad", step=1, min_value=1)
        
        c1, c2 = st.columns(2)
        if c1.button("➕ AÑADIR DIAMANTES"):
            ref = db.reference(f'usuarios/{target}')
            if ref.get():
                ref.update({'Diamantes': ref.get().get('Diamantes', 0) + monto})
                st.success("Diamantes cargados.")
            else: st.error("ID no encontrado.")
            
        if c2.button("➕ REGISTRAR DEUDA"):
            ref = db.reference(f'usuarios/{target}')
            if ref.get():
                ref.update({'deuda': ref.get().get('deuda', 0) + monto})
                st.warning("Deuda registrada.")
            else: st.error("ID no encontrado.")

    # --- ❌ ELIMINAR MIEMBRO ---
    elif pag == 'eliminar':
        st.header("❌ ELIMINAR GUERRERO")
        st.error("Esta acción no se puede deshacer.")
        del_id = st.text_input("Ingresa el ID a eliminar")
        if st.button("ELIMINAR DEFINITIVAMENTE"):
            if del_id:
                db.reference(f'usuarios/{del_id}').delete()
                st.success(f"ID {del_id} eliminado de la base de datos.")
            else: st.warning("Escribe un ID.")

    # --- 📋 LISTA DE MIEMBROS ---
    elif pag == 'lista':
        st.header("📋 INTEGRANTES DEL CLAN")
        data = db.reference('usuarios').get()
        if data:
            for k, v in data.items():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                # Privacidad de ID
                if rol_s in ["Lider", "Moderador", "Coach"] or str(id_act) == str(k):
                    st.code(f"ID: {k}")
                st.write(f"👤 **Nombre:** {v.get('nombre')}")
                st.write(f"🛡️ **Rango:** {v.get('rol')}")
                if v.get('rol') != 'Coach':
                    st.write(f"🎮 **Roles:** {v.get('rol_primario')} / {v.get('rol_secundario')}")
                    st.write(f"⚠️ **Sanciones:** {v.get('sanciones', 0)}")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 📝 REGISTRO DE MIEMBROS ---
    elif pag == 'registro':
        st.header("📝 NUEVO REGISTRO")
        with st.form("reg_form"):
            new_id = st.text_input("ID de Jugador")
            new_nom = st.text_input("Nombre / Nick")
            new_rol = st.selectbox("Rango", ["Miembro", "Moderador", "Coach"])
            
            p_rol, s_rol = "N/A", "N/A"
            if new_rol != "Coach":
                p_rol = st.selectbox("Rol Primario", ROLES_JUEGO)
                s_rol = st.selectbox("Rol Secundario", ROLES_JUEGO)
            
            if st.form_submit_button("REGISTRAR"):
                datos = {
                    'nombre': new_nom, 'rol': new_rol, 
                    'Diamantes': 0, 'deuda': 0, 
                    'sanciones': 0, 'puntos_coach': 0,
                    'rol_primario': p_rol, 'rol_secundario': s_rol
                }
                db.reference(f'usuarios/{new_id}').set(datos)
                st.success("✅ Miembro registrado.")

    # --- 📈 DAR PUNTOS (COACH) ---
    elif pag == 'coach_puntos':
        st.header("📈 ASIGNAR PUNTOS")
        data = db.reference('usuarios').get()
        if data:
            for k, v in data.items():
                if v.get('rol') != 'Coach':
                    with st.container():
                        c1, c2 = st.columns([3, 1])
                        c1.write(f"👤 {v['nombre']} (Actual: {v.get('puntos_coach', 0)})")
                        pts = c2.number_input("Pts", step=1, key=f"p_{k}")
                        if st.button("DAR", key=f"b_{k}"):
                            db.reference(f'usuarios/{k}').update({'puntos_coach': v.get('puntos_coach', 0) + pts})
                            st.rerun()

    # --- 👀 VER LINEUP ---
    elif pag == 'ver_lineup':
        st.header("👀 FORMACIÓN ACTUAL")
        lineup = db.reference('lineup_actual').get()
        if lineup:
            st.subheader("🔥 TITULARES")
            for t in lineup.get('titulares', []): st.info(t)
            st.subheader("💤 SUPLENTES")
            for s in lineup.get('suplentes', []): st.warning(s)
            st.write(f"📝 *Definido por Coach: {lineup.get('coach', 'N/A')}*")
        else: st.info("No hay formación definida aún.")

    # --- 📅 CREAR EVENTO ---
    elif pag == 'crear_evento':
        st.header("📅 PUBLICAR EVENTO")
        with st.form("event_form"):
            t = st.text_input("Nombre del Evento")
            d = st.text_area("Descripción/Requisitos")
            if st.form_submit_button("PUBLICAR"):
                db.reference('eventos').push().set({'nombre': t, 'descripcion': d})
                st.success("Evento publicado.")

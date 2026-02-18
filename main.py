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
ID_LIDER_MAESTRO = "1234" # <--- ¡PON AQUÍ TU ID DE LÍDER!
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
                st.session_state['usuario'] = res
                st.session_state['id_actual'] = id_in
                ir_a('menu')
            else: st.error("ID incorrecto o no registrado.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 2. MENÚ PRINCIPAL
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    my_id = st.session_state['id_actual']
    
    # Determinamos el Rol de Sesión
    rol = u.get('rol', 'Miembro')
    if str(my_id) == ID_LIDER_MAESTRO: rol = "Lider"
    if str(my_id) == ID_COACH: rol = "Coach"

    st.markdown(f"<div class='card'><h2 style='text-align:center; color:#3498DB;'>PANEL: {rol.upper()}</h2><p style='text-align:center;'>Usuario: <b>{u.get('nombre')}</b></p></div>", unsafe_allow_html=True)

    if rol == "Lider":
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📊 RANKING"): ir_a('ranking')
            if st.button("💎 TESORERÍA"): ir_a('diamantes')
            if st.button("📝 REGISTRAR"): ir_a('registro')
        with c2:
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("🎁 SUGERENCIAS"): ir_a('ver_sugerencias')
        
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    elif rol == "Coach":
        if st.button("📈 PUNTOS DE COACH"): ir_a('coach_puntos')
        if st.button("⚔️ CREAR EQUIPOS"): ir_a('coach_equipos')
        if st.button("🎁 PREMIOS"): ir_a('coach_premios')

    elif rol == "Moderador":
        if st.button("💎 GESTIONAR DIAMANTES"): ir_a('diamantes')
        if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')

    # Botones comunes
    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 MIEMBROS DEL ESCUADRÓN"): ir_a('lista')
    if st.button("🏆 EVENTOS Y ASISTENCIA"): ir_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 3. PÁGINAS DE FUNCIONES
# ==========================================
else:
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag = st.session_state['pagina']
    u_act = st.session_state['usuario']
    id_act = st.session_state['id_actual']
    
    # Recalculamos rol por seguridad
    rol_s = u_act.get('rol', 'Miembro')
    if str(id_act) == ID_LIDER_MAESTRO: rol_s = "Lider"
    if str(id_act) == ID_COACH: rol_s = "Coach"

    # --- 1. TESORERÍA (DIAMANTES Y DEUDA) ---
    if pag == 'diamantes':
        st.header("💎 TESORERÍA DEL CLAN")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Solo Lider y Moderador pueden usar esto
        if rol_s in ["Lider", "Moderador"]:
            target = st.text_input("ID del Jugador a gestionar")
            cant = st.number_input("Cantidad", step=1, min_value=1)
            
            c1, c2 = st.columns(2)
            if c1.button("➕ SUMAR DIAMANTES"):
                ref = db.reference(f'usuarios/{target}')
                if ref.get():
                    nuevo_valor = ref.get().get('Diamantes', 0) + cant
                    ref.update({'Diamantes': nuevo_valor})
                    st.success(f"Diamantes añadidos al ID {target}")
                else: st.error("ID no existe")
            
            if c2.button("➕ ANOTAR DEUDA"):
                ref = db.reference(f'usuarios/{target}')
                if ref.get():
                    nuevo_valor = ref.get().get('deuda', 0) + cant
                    ref.update({'deuda': nuevo_valor})
                    st.warning(f"Deuda anotada al ID {target}")
                else: st.error("ID no existe")
        else:
            st.error("Acceso denegado. Solo Líder y Moderadores.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. RANKING (TABLA COMPLETA) ---
    elif pag == 'ranking':
        st.header("🏆 RANKING GENERAL")
        data = db.reference('usuarios').get()
        if data:
            # Filtramos para NO mostrar al Coach en el ranking
            lista = []
            for k, v in data.items():
                if isinstance(v, dict) and v.get('rol') != 'Coach':
                    lista.append({
                        "Guerrero": v.get('nombre'),
                        "💎 Diamantes": v.get('Diamantes', 0),
                        "⭐ Ptos Coach": v.get('puntos_coach', 0),
                        "💰 Deuda": v.get('deuda', 0)
                    })
            
            # Ordenamos por Diamantes (Mayor a menor)
            st.table(sorted(lista, key=lambda x: x['💎 Diamantes'], reverse=True))
        else:
            st.info("No hay datos todavía.")

    # --- 3. REGISTRO (CON ROLES DE JUEGO) ---
    elif pag == 'registro':
        st.header("📝 REGISTRAR NUEVO MIEMBRO")
        with st.form("reg_form"):
            rid = st.text_input("ID Nuevo (Ej: 5566)")
            rnom = st.text_input("Nombre / Nickname")
            rrol = st.selectbox("Rango", ["Miembro", "Moderador", "Lider", "Coach"])
            
            # Lógica visual: Si es Coach, no pedimos roles de juego
            rp, rs = "N/A", "N/A"
            if rrol != "Coach":
                st.markdown("---")
                st.write("🎮 **Roles de Juego:**")
                rp = st.selectbox("Rol Principal", ROLES_JUEGO)
                rs = st.selectbox("Rol Secundario", ROLES_JUEGO)
            
            if st.form_submit_button("GUARDAR USUARIO"):
                if rrol == "Coach" and rol_s != "Lider":
                    st.error("Solo el Líder puede crear al Coach.")
                else:
                    datos = {
                        'nombre': rnom, 
                        'rol': rrol, 
                        'Diamantes': 0, 
                        'deuda': 0, 
                        'sanciones': 0, 
                        'puntos_coach': 0
                    }
                    if rrol != "Coach":
                        datos['rol_primario'] = rp
                        datos['rol_secundario'] = rs
                    
                    db.reference(f'usuarios/{rid}').set(datos)
                    st.success(f"✅ Usuario {rnom} registrado correctamente.")

    # --- 4. LISTA DE MIEMBROS (PRIVACIDAD DE ID) ---
    elif pag == 'lista':
        st.header("📋 ESCUADRÓN PHOENIX")
        data = db.reference('usuarios').get()
        if data:
            for k, v in data.items():
                if isinstance(v, dict):
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    
                    # LOGICA DE PRIVACIDAD:
                    # El Líder, Mods y el propio usuario ven el ID. El Coach también.
                    # Los miembros normales NO ven el ID de otros.
                    puede_ver_id = (rol_s in ["Lider", "Moderador", "Coach"]) or (str(id_act) == str(k))
                    
                    if puede_ver_id:
                        st.write(f"🆔 **ID:** `{k}`")
                    
                    st.write(f"👤 **{v.get('nombre')}**")
                    st.write(f"🛡️ {v.get('rol')}")
                    
                    if v.get('rol') != 'Coach':
                        st.write(f"🎮 {v.get('rol_primario', '?')} | {v.get('rol_secundario', '?')}")
                        st.write(f"⭐ Puntos de Coach: {v.get('puntos_coach', 0)}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. COACH: PUNTOS ---
    elif pag == 'coach_puntos':
        st.header("📈 GESTIÓN DE PUNTOS (COACH)")
        all_u = db.reference('usuarios').get()
        if all_u:
            # Filtramos: Solo mostramos miembros que NO sean Coach
            jugadores = {k:v for k,v in all_u.items() if v.get('rol') != 'Coach'}
            
            for k, v in jugadores.items():
                with st.container():
                    st.markdown(f'<div class="card">', unsafe_allow_html=True)
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.write(f"👤 **{v['nombre']}**")
                        st.write(f"🎮 {v.get('rol_primario')} / {v.get('rol_secundario')}")
                        st.write(f"⭐ Puntos Actuales: **{v.get('puntos_coach', 0)}**")
                    with c2:
                        puntos = st.number_input("Sumar", step=1, key=f"inp_{k}")
                        if st.button("DAR", key=f"btn_{k}"):
                            db.reference(f'usuarios/{k}').update({
                                'puntos_coach': v.get('puntos_coach', 0) + puntos
                            })
                            st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    # --- 6. COACH: EQUIPOS ---
    elif pag == 'coach_equipos':
        st.header("⚔️ FORMADOR DE EQUIPOS")
        
        # 1. Crear Equipo
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Nuevo Equipo")
        all_u = db.reference('usuarios').get()
        if all_u:
            nombres = [f"{v['nombre']} ({v.get('rol_primario','?')})" for k,v in all_u.items() if v.get('rol') != 'Coach']
            
            team_name = st.text_input("Nombre del Equipo")
            seleccion = st.multiselect("Selecciona 5 Guerreros", nombres)
            
            if st.button("CONFIRMAR EQUIPO"):
                if len(seleccion) == 5:
                    db.reference('equipos').push().set({
                        'nombre': team_name,
                        'jugadores': seleccion,
                        'coach': u_act.get('nombre')
                    })
                    st.success("Equipo creado exitosamente")
                else:
                    st.warning("⚠️ Debes seleccionar exactamente 5 jugadores.")
        st.markdown('</div>', unsafe_allow_html=True)

        # 2. Ver Equipos
        st.subheader("Equipos Activos")
        eqs = db.reference('equipos').get()
        if eqs:
            for ek, ev in eqs.items():
                st.markdown(f"""
                <div class="card" style="border-color: #3498DB !important;">
                <h3>🚩 {ev.get('nombre')}</h3>
                <p><b>Coach:</b> {ev.get('coach')}</p>
                <p><b>Integrantes:</b><br>{', '.join(ev.get('jugadores', []))}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Eliminar Equipo", key=ek):
                    db.reference(f'equipos/{ek}').delete()
                    st.rerun()

    # --- 7. COACH: PREMIOS ---
    elif pag == 'coach_premios':
        st.header("🎁 SUGERENCIA DE PREMIOS")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        nota = st.text_area("Escribe aquí tu sugerencia para el Líder:")
        if st.button("ENVIAR SUGERENCIA"):
            if nota:
                db.reference('sugerencias').push().set({
                    'mensaje': nota,
                    'coach': u_act.get('nombre')
                })
                st.success("Sugerencia enviada.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 8. LÍDER: VER SUGERENCIAS ---
    elif pag == 'ver_sugerencias':
        st.header("📩 BUZÓN DEL COACH")
        sugs = db.reference('sugerencias').get()
        if sugs:
            for sk, sv in sugs.items():
                st.markdown(f'<div class="card"><b>De: {sv.get("coach")}</b><br><br>{sv.get("mensaje")}</div>', unsafe_allow_html=True)
                if st.button("Marcar como Leído (Borrar)", key=sk):
                    db.reference(f'sugerencias/{sk}').delete()
                    st.rerun()
        else:
            st.info("No hay sugerencias nuevas.")

    # --- 9. ELIMINAR MIEMBRO ---
    elif pag == 'eliminar':
        st.header("❌ ELIMINAR MIEMBRO")
        st.markdown('<div class="card" style="border-color:red !important;">', unsafe_allow_html=True)
        del_id = st.text_input("ID del usuario a eliminar")
        if del_id:
            info = db.reference(f'usuarios/{del_id}').get()
            if info:
                st.error(f"⚠️ ATENCIÓN: Vas a eliminar a **{info['nombre']}**")
                if st.button("SÍ, ELIMINAR DEFINITIVAMENTE"):
                    db.reference(f'usuarios/{del_id}').delete()
                    st.success("Usuario eliminado.")
                    st.rerun()
            else:
                st.warning("ID no encontrado para verificar.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 10. CAMBIAR ID ---
    elif pag == 'cambio_id':
        st.header("🔧 CAMBIAR ID")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        old_id = st.text_input("ID Viejo")
        new_id = st.text_input("ID Nuevo")
        if st.button("EJECUTAR CAMBIO"):
            old_data = db.reference(f'usuarios/{old_id}').get()
            if old_data:
                # Copiamos datos al nuevo ID
                db.reference(f'usuarios/{new_id}').set(old_data)
                # Borramos el viejo
                db.reference(f'usuarios/{old_id}').delete()
                st.success("✅ Traspaso completado exitosamente.")
            else:
                st.error("El ID Viejo no existe.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 11. SANCIONES ---
    elif pag == 'sanciones':
        st.header("⚠️ APLICAR SANCIÓN")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        s_id = st.text_input("ID del Infractor")
        if st.button("MULTAR (+1 Sanción)"):
            ref = db.reference(f'usuarios/{s_id}')
            if ref.get():
                ref.update({'sanciones': ref.get().get('sanciones', 0) + 1})
                st.error("Sanción aplicada.")
            else:
                st.error("ID no encontrado.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 12. EVENTOS Y CREAR EVENTO ---
    elif pag == 'crear_evento':
        st.header("📅 CREAR EVENTO")
        tit = st.text_input("Título"); desc = st.text_area("Detalles")
        if st.button("PUBLICAR"):
            db.reference('eventos').push().set({'nombre': tit, 'descripcion': desc, 'fecha': 'Pendiente'})
            st.success("Evento creado.")

    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS ACTIVO")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f'<div class="card"><h3>{info.get("nombre")}</h3><p>{info.get("descripcion")}</p></div>', unsafe_allow_html=True)
                
                # Asistencia rápida
                if st.button("🙋 YO ASISTIRÉ", key=f"yo_{eid}"):
                    db.reference(f'eventos/{eid}/asistentes/{id_act}').set(u_act.get('nombre'))
                    st.success("Anotado")
                
                # Ver lista
                asis = info.get('asistentes', {})
                if asis: st.write(f"✅ **Asistentes:** {', '.join(asis.values())}")

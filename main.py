import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import base64

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="PHOENIX EMPIRE - CONTROL", layout="centered")

# --- TU LLAVE MAESTRA (¡PON TU ID AQUÍ!) ---
ID_LIDER_MAESTRO = 12345 

# --- CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})
    except: pass

# ==========================================
# 2. ESTILOS Y FONDO
# ==========================================
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
         """, unsafe_allow_html=True)

# Intenta cargar el fondo (si no existe, no pasa nada)
try: set_bg_hack('fondo.jpg') 
except: pass

st.markdown("""
    <style>
    /* Textos Legibles sobre Fondo */
    h1, h2, h3, p, div, span, label { color: white !important; text-shadow: 2px 2px 4px #000000; font-family: sans-serif; }
    
    /* Botones Estilo App */
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3.5em; width: 100%; border: 1px solid white; margin-bottom: 8px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    
    /* Tarjetas Semitransparentes */
    .card { background-color: rgba(0, 0, 0, 0.8); padding: 20px; border-radius: 12px; border: 1px solid #E74C3C; margin-bottom: 15px; }
    
    /* Colores Específicos (Clases CSS) */
    .btn-azul button { background-color: rgba(31, 83, 141, 0.95) !important; color: white; }
    .btn-verde button { background-color: rgba(47, 165, 114, 0.95) !important; color: white; }
    .btn-gris button { background-color: rgba(96, 96, 96, 0.95) !important; color: white; }
    .btn-rojo button { background-color: rgba(220, 20, 20, 0.9) !important; color: white; border-color: red; }
    .btn-volver button { background-color: rgba(40, 40, 40, 0.9) !important; border: 1px solid #999; color: #ddd; }
    
    /* Inputs Oscuros */
    .stTextInput > div > div > input { color: white; background-color: rgba(20,20,20,0.9); border: 1px solid #E74C3C; text-align: center; }
    .stNumberInput > div > div > input { color: white; background-color: rgba(20,20,20,0.9); text-align: center; }
    .stSelectbox > div > div > div { color: white; background-color: rgba(20,20,20,0.9); }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. GESTIÓN DE PANTALLAS (NAVEGACIÓN)
# ==========================================
if 'pagina' not in st.session_state: st.session_state['pagina'] = 'login'

def ir_a(pag): 
    st.session_state['pagina'] = pag
    st.rerun()

# ==========================================
# PANTALLA 1: LOGIN (Con corrección de espacios)
# ==========================================
if st.session_state['pagina'] == 'login':
    st.markdown("<br><h1 style='color: #E74C3C; text-align: center; font-size: 50px;'>PHOENIX<br>EMPIRE 🔥</h1><br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center'>IDENTIFÍCATE GUERRERO</h3>", unsafe_allow_html=True)
        id_input = st.text_input("ID DE JUGADOR", placeholder="Escribe tu ID aquí")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("ENTRAR AL SISTEMA"):
            if id_input:
                # CORRECCIÓN: Quitamos espacios vacíos (El error del 1234)
                id_limpio = id_input.strip() 
                
                # Buscamos en Firebase
                res = db.reference(f'usuarios/{id_limpio}').get()
                
                if res:
                    st.session_state['usuario'] = res
                    st.session_state['id_actual'] = id_limpio
                    ir_a('menu')
                else:
                    st.error(f"❌ El ID '{id_limpio}' no está registrado. Pide al Líder que te registre.")
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PANTALLA 2: MENÚ PRINCIPAL
# ==========================================
elif st.session_state['pagina'] == 'menu':
    u = st.session_state['usuario']
    my_id = st.session_state['id_actual']
    
    # Detectar Rol (Prioridad a tu ID Maestro)
    rol = "Lider" if str(my_id) == ID_LIDER_MAESTRO else u.get('rol', 'Miembro')

    # Encabezado con datos del usuario
    st.markdown(f"""
    <div class='card' style='text-align:center;'>
        <h2 style='color: #3b8ed0; margin:0;'>PANEL DE COMANDO</h2>
        <p style='font-size: 18px;'>👤 <b>{u.get('nombre')}</b> | Rango: <span style='color:#E74C3C'>{rol.upper()}</span></p>
    </div>
    """, unsafe_allow_html=True)

    # --- MENÚ LÍDER ---
    if rol == "Lider":
        st.markdown("### 🛠️ GESTIÓN DEL LÍDER")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
            if st.button("📊 RANKING"): ir_a('ranking')
            if st.button("💎 DIAMANTES/DEUDA"): ir_a('diamantes')
            if st.button("⚠️ SANCIONES"): ir_a('sanciones')
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
            if st.button("📝 REGISTRAR"): ir_a('registro')
            if st.button("🔧 CAMBIAR ID"): ir_a('cambio_id')
            if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("❌ ELIMINAR MIEMBRO"): ir_a('eliminar')
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MENÚ MODERADOR ---
    elif rol == "Moderador":
        st.markdown("### 🛠️ GESTIÓN MOD")
        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("📅 CREAR EVENTO"): ir_a('crear_evento')
        if st.button("💎 GESTIONAR DIAMANTES"): ir_a('diamantes')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # --- MENÚ COMÚN (PARA TODOS) ---
    st.markdown("### 🌎 CLAN PHOENIX")
    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DE MIEMBROS"): ir_a('lista')
    if st.button("🏆 VER EVENTOS ACTIVOS"): ir_a('ver_eventos')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"): ir_a('login')
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PANTALLAS DE FUNCIONES (TODO EN UNO)
# ==========================================
else:
    # Botón Volver SIEMPRE Visible Arriba
    st.markdown('<div class="btn-volver">', unsafe_allow_html=True)
    if st.button("⬅️ VOLVER AL MENÚ PRINCIPAL"): ir_a('menu')
    st.markdown('</div>', unsafe_allow_html=True)
    
    pag = st.session_state['pagina']

    # --- 1. RANKING ---
    if pag == 'ranking':
        st.header("🏆 RANKING Y DEUDAS")
        data = db.reference('usuarios').get()
        if data:
            lista = []
            for k, v in data.items():
                if isinstance(v, dict):
                    lista.append({
                        "Nombre": v.get('nombre', 'Desconocido'), 
                        "💎": v.get('Diamantes',0), 
                        "💰": v.get('deuda',0)
                    })
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))
            st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. LISTA DE MIEMBROS (CON FIX) ---
    elif pag == 'lista':
        st.header("📋 LISTA DEL CLAN")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        all_u = db.reference('usuarios').get()
        if all_u:
            for k, v in all_u.items():
                if isinstance(v, dict):
                    # Protección contra datos vacíos
                    nom = v.get('nombre', 'Sin Nombre')
                    r = v.get('rol', 'Miembro')
                    sanc = v.get('sanciones', 0)
                    
                    color_rol = "#E74C3C" if r == "Lider" else "#3b8ed0" if r == "Moderador" else "white"
                    
                    st.markdown(f"""
                    <div style='border-bottom: 1px solid #555; padding: 5px;'>
                        <b>🆔 {k}</b> | <span style='color:{color_rol}'>{nom}</span><br>
                        Rol: {r} | ⚠️ Sanciones: <b>{sanc}</b>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 3. DIAMANTES Y DEUDAS ---
    elif pag == 'diamantes':
        st.header("💎 GESTIÓN DE TESORERÍA")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.info("Ingresa el ID del jugador para modificar su saldo.")
        target = st.text_input("ID del Jugador")
        cant = st.number_input("Cantidad", step=1, min_value=1)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
            if st.button("➕ SUMAR DIAMANTES"):
                ref = db.reference(f'usuarios/{target}')
                if ref.get(): 
                    ref.update({'Diamantes': ref.get().get('Diamantes',0) + cant})
                    st.success(f"Se sumaron {cant} 💎")
                else: st.error("ID no existe")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
            if st.button("➕ ANOTAR DEUDA"):
                ref = db.reference(f'usuarios/{target}')
                if ref.get(): 
                    ref.update({'deuda': ref.get().get('deuda',0) + cant})
                    st.warning(f"Se anotó deuda de {cant} 💰")
                else: st.error("ID no existe")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. SANCIONES (NUEVO) ---
    elif pag == 'sanciones':
        st.header("⚠️ TRIBUNAL DE SANCIONES")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        s_id = st.text_input("ID del Infractor")
        
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("APLICAR SANCIÓN (+1)"):
            ref = db.reference(f'usuarios/{s_id}')
            u = ref.get()
            if u:
                tot = u.get('sanciones', 0) + 1
                ref.update({'sanciones': tot})
                st.error(f"Sanción aplicada a {u.get('nombre')}. Total: {tot}")
            else: st.error("Usuario no encontrado")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. REGISTRO ---
    elif pag == 'registro':
        st.header("📝 NUEVO GUERRERO")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        r_id = st.text_input("ID Nuevo (Sin espacios)")
        r_nom = st.text_input("Nombre / Nick")
        r_rol = st.selectbox("Asignar Rol", ["Miembro", "Moderador", "Lider"])
        
        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("GUARDAR REGISTRO"):
            if r_id and r_nom:
                db.reference(f'usuarios/{r_id.strip()}').set({
                    'nombre': r_nom, 'rol': r_rol, 'Diamantes': 0, 'deuda': 0, 'sanciones': 0
                })
                st.success(f"¡{r_nom} ha sido registrado!")
            else:
                st.warning("Faltan datos.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 6. CAMBIO DE ID ---
    elif pag == 'cambio_id':
        st.header("🔧 MIGRACIÓN DE CUENTA")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        old = st.text_input("ID Antiguo")
        new = st.text_input("ID Nuevo")
        
        st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
        if st.button("TRASPASAR DATOS"):
            ref_old = db.reference(f'usuarios/{old}')
            data = ref_old.get()
            if data:
                db.reference(f'usuarios/{new}').set(data)
                ref_old.delete()
                st.success("Cuenta migrada con éxito.")
            else: st.error("ID antiguo no existe.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 7. ELIMINAR ---
    elif pag == 'eliminar':
        st.header("❌ ZONA DE PELIGRO")
        st.markdown('<div class="card" style="border: 2px solid red;">', unsafe_allow_html=True)
        st.write("Esta acción borrará al usuario permanentemente.")
        d_id = st.text_input("Escribe el ID a borrar")
        
        st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
        if st.button("BORRAR DEFINITIVAMENTE"):
            if db.reference(f'usuarios/{d_id}').get():
                db.reference(f'usuarios/{d_id}').delete()
                st.warning("Usuario eliminado del sistema.")
            else: st.error("ID no encontrado.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 8. CREAR EVENTO ---
    elif pag == 'crear_evento':
        st.header("📅 CREAR EVENTO")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        t = st.text_input("Título del Evento")
        f = st.text_input("Fecha y Hora (Ej: Hoy 8PM)")
        d = st.text_area("Descripción / Reglas")
        
        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("PUBLICAR PARA TODOS"):
            if t and f:
                db.reference('eventos').push().set({'nombre': t, 'fecha': f, 'descripcion': d})
                st.success("Evento publicado.")
            else: st.warning("Falta título o fecha.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 9. VER EVENTOS ---
    elif pag == 'ver_eventos':
        st.header("🏆 EVENTOS ACTIVOS")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                st.markdown(f"""
                <div class="card">
                    <h3 style="color:#E74C3C; margin-bottom:5px;">{info.get('nombre')}</h3>
                    <p style="color:#aaa; font-style:italic;">📅 {info.get('fecha')}</p>
                    <p>{info.get('descripcion')}</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
                if st.button("✅ Asistiré", key=eid):
                    st.success("Te has anotado en la lista.")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No hay eventos activos por ahora.")


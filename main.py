import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="PHOENIX EMPIRE - SISTEMA CENTRAL", layout="wide", initial_sidebar_state="expanded")

# Diseño Visual IDÉNTICO al estilo del Imperio (Rojo y Negro)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    [data-testid="stSidebar"] { background-color: #111111; border-right: 2px solid #E74C3C; }
    h1, h2, h3 { color: #E74C3C !important; text-align: center; font-family: 'Impact', sans-serif; text-transform: uppercase; }
    .stButton>button { 
        background-color: #E74C3C; color: white; border-radius: 5px; 
        font-weight: bold; border: 1px solid #c0392b; width: 100%; height: 3em;
    }
    .stButton>button:hover { background-color: #ff4b4b; border: 1px solid white; }
    div[data-testid="stMetricValue"] { color: #3b8ed0 !important; font-size: 35px !important; }
    .stTextInput>div>div>input { background-color: #1a1a1a; color: white; border: 1px solid #E74C3C; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("llave.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'
        })
    except Exception as e:
        st.error(f"⚠️ ERROR CRÍTICO DE CONEXIÓN: {e}")

# --- 3. LÓGICA DE ACCESO (LOGIN Y REGISTRO) ---
if 'usuario_id' not in st.session_state:
    st.title("🔥 PHOENIX EMPIRE 🔥")
    st.subheader("SISTEMA DE CONTROL CENTRALIZADO")
    
    col_log, col_reg = st.tabs(["🔒 ENTRAR AL SISTEMA", "📝 REGISTRAR NUEVO GUERRERO"])
    
    with col_log:
        id_login = st.text_input("IDENTIFICADOR DE JUGADOR", placeholder="Ingresa tu ID")
        if st.button("AUTENTICAR"):
            user_data = db.reference(f'usuarios/{id_login}').get()
            if user_data:
                st.session_state['usuario_id'] = id_login
                st.session_state['datos'] = user_data
                st.success("Acceso concedido. Cargando interfaz...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("ID no reconocido. Verifica con el Líder.")

    with col_reg:
        new_id = st.text_input("CREAR ID")
        new_name = st.text_input("NOMBRE EN JUEGO / NICK")
        if st.button("FINALIZAR REGISTRO"):
            if new_id and new_name:
                db.reference(f'usuarios/{new_id}').set({
                    'nombre': new_name, 'Diamantes': 0, 'deuda': 0, 'rol': 'Miembro'
                })
                st.success(f"¡Guerrero {new_name} registrado! Ya puedes iniciar sesión.")
            else:
                st.warning("Debes completar todos los campos.")

# --- 4. INTERFAZ COMPLETA DEL PROGRAMA ---
else:
    # Sincronización en tiempo real con Firebase
    id_actual = st.session_state['usuario_id']
    datos = db.reference(f'usuarios/{id_actual}').get()
    rol = datos.get('rol', 'Miembro')

    # BARRA LATERAL (Panel de Navegación)
    st.sidebar.markdown(f"### 🎖️ {datos.get('nombre')}")
    st.sidebar.markdown(f"RANGO: **{rol.upper()}**")
    st.sidebar.divider()
    
    menu = st.sidebar.radio("MENÚ DE COMANDO", 
        ["📊 MI ESTADO", "🏆 RANKING DEL CLAN", "💎 GESTIÓN DE DIAMANTES", "💰 CONTROL DE DEUDAS", "👥 LISTA DE MIEMBROS", "⚙️ AJUSTES"])

    # --- FUNCIONALIDADES ---
    
    if menu == "📊 MI ESTADO":
        st.title(f"ESTADO DE {datos.get('nombre').upper()}")
        c1, c2 = st.columns(2)
        with c1: st.metric("DIAMANTES TOTALES", f"💎 {datos.get('Diamantes', 0)}")
        with c2: st.metric("DEUDA PENDIENTE", f"💰 {datos.get('deuda', 0)}")
        st.divider()
        st.info("Nota: Los diamantes se actualizan después de cada evento del clan.")

    elif menu == "🏆 RANKING DEL CLAN":
        st.title("🏆 TOP GUERREROS PHOENIX")
        all_users = db.reference('usuarios').get()
        if all_users:
            lista = [{"Nombre": v.get('nombre'), "Diamantes": v.get('Diamantes', 0)} for v in all_users.values()]
            ranking = sorted(lista, key=lambda x: x['Diamantes'], reverse=True)
            st.table(ranking)

    elif menu == "💎 GESTIÓN DE DIAMANTES":
        if rol in ["Líder", "Moderador"]:
            st.title("💎 CONTROL DE TESORERÍA")
            target_id = st.text_input("ID del Jugador a modificar")
            amount = st.number_input("Cantidad de Diamantes", min_value=1, step=1)
            
            col_add, col_sub = st.columns(2)
            if col_add.button("➕ SUMAR AL SALDO"):
                ref = db.reference(f'usuarios/{target_id}')
                u = ref.get()
                if u:
                    ref.update({"Diamantes": u.get('Diamantes', 0) + amount})
                    st.success(f"Se sumaron {amount} diamantes a {u.get('nombre')}")
                else: st.error("ID no encontrado.")
            
            if col_sub.button("➖ RESTAR DEL SALDO"):
                ref = db.reference(f'usuarios/{target_id}')
                u = ref.get()
                if u:
                    ref.update({"Diamantes": max(0, u.get('Diamantes', 0) - amount)})
                    st.success("Saldo actualizado.")
                else: st.error("ID no encontrado.")
        else:
            st.error("⛔ ACCESO DENEGADO. Solo Líderes o Moderadores.")

    elif menu == "💰 CONTROL DE DEUDAS":
        if rol in ["Líder", "Moderador"]:
            st.title("💰 REGISTRO DE DEUDAS")
            d_id = st.text_input("ID del Deudor")
            d_amount = st.number_input("Monto de la Deuda", min_value=1)
            
            if st.button("REGISTRAR DEUDA"):
                ref = db.reference(f'usuarios/{d_id}')
                u = ref.get()
                if u:
                    ref.update({"deuda": u.get('deuda', 0) + d_amount})
                    st.success(f"Deuda de {d_amount} anotada a {u.get('nombre')}")
                else: st.error("ID no encontrado.")
        else:
            st.error("⛔ No tienes permisos para gestionar deudas.")

    elif menu == "👥 LISTA DE MIEMBROS":
        st.title("📋 REGISTRO GENERAL DEL CLAN")
        all_data = db.reference('usuarios').get()
        if all_data:
            for k, v in all_data.items():
                with st.expander(f"👤 {v.get('nombre')} (ID: {k})"):
                    st.write(f"Rol: {v.get('rol')}")
                    st.write(f"Diamantes: {v.get('Diamantes')}")
                    st.write(f"Deuda: {v.get('deuda')}")
                    if rol == "Líder":
                        if st.button(f"Eliminar {k}", key=k):
                            db.reference(f'usuarios/{k}').delete()
                            st.rerun()

    elif menu == "⚙️ AJUSTES":
        st.title("⚙️ CONFIGURACIÓN")
        if st.button("CERRAR SESIÓN DEL SISTEMA"):
            del st.session_state['usuario_id']
            st.rerun()

    st.sidebar.divider()
    st.sidebar.caption("SISTEMA PHOENIX EMPIRE v2.0")

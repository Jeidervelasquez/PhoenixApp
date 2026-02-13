import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time

# --- 1. CONFIGURACIÓN Y CONEXIÓN ---
st.set_page_config(page_title="SISTEMA PHOENIX - JEIDER", layout="centered")

if not firebase_admin._apps:
    cred = credentials.Certificate("llave.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'
    })

# --- 2. TU ID MAESTRO (PARA QUE TENGAS TODO EL CONTROL) ---
ID_LIDER_MAESTRO = "PON_AQUI_TU_ID_REAL" 

# --- 3. ESTILO VISUAL (Colores de tu programa CustomTkinter) ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: white; }
    .stButton>button { border-radius: 8px; font-weight: bold; height: 3em; border: none; }
    /* Colores de botones según tu código de PC */
    .btn-azul button { background-color: #1f538d !important; color: white; }
    .btn-verde button { background-color: #2fa572 !important; color: white; }
    .btn-gris button { background-color: #606060 !important; color: white; }
    .btn-rojo button { background-color: #FF0000 !important; color: white; }
    .btn-phoenix button { background-color: #E74C3C !important; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LÓGICA DE SESIÓN ---
if 'usuario' not in st.session_state:
    st.markdown(f"<h1 style='color: #E74C3C;'>Phoenix Empire<br>escuadrón 🔥</h1>", unsafe_allow_html=True)
    
    with st.container():
        id_input = st.text_input("ID de Jugador", placeholder="Ingresa tu ID")
        if st.markdown('<div class="btn-phoenix">', unsafe_allow_html=True):
            if st.button("ENTRAR"):
                res = db.reference(f'usuarios/{id_input}').get()
                if res:
                    st.session_state['usuario'] = res
                    st.session_state['id_actual'] = id_input
                    st.rerun()
                else:
                    st.error("ID no registrado")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    u_id = st.session_state['id_actual']
    # Sincronización en tiempo real
    datos = db.reference(f'usuarios/{u_id}').get()
    
    # Lógica de Rol (Si es tu ID, eres Lider automáticamente)
    rol = "Lider" if str(u_id) == ID_LIDER_MAESTRO else datos.get('rol', 'Miembro')

    st.markdown(f"<h1 style='color: #3b8ed0;'>PANEL DE {rol.upper()}</h1>", unsafe_allow_html=True)
    st.write(f"**Usuario:** {datos.get('nombre')}")

    # --- BOTONES DEL MENÚ (IDÉNTICOS A TU PC) ---
    
    if rol == "Lider":
        col_lider = st.container()
        with col_lider:
            st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
            if st.button("📊 RANKING Y DEUDAS"): st.session_state['seccion'] = "ranking"
            if st.button("📝 REGISTRAR MIEMBRO"): st.session_state['seccion'] = "registro"
            if st.button("💎 GESTIONAR DIAMANTES"): st.session_state['seccion'] = "diamantes"
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
            if st.button("🔧 CAMBIAR ID / CUENTAS"): st.session_state['seccion'] = "cambio_id"
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="btn-rojo">', unsafe_allow_html=True)
            if st.button("❌ ELIMINAR MIEMBRO"): st.session_state['seccion'] = "eliminar"
            st.markdown('</div>', unsafe_allow_html=True)

    if rol in ["Lider", "Moderador"]:
        st.markdown('<div class="btn-azul">', unsafe_allow_html=True)
        if st.button("📅 CREAR EVENTO"): st.session_state['seccion'] = "crear_evento"
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📋 LISTA DEL CLAN"): st.session_state['seccion'] = "lista"
    if st.button("🏆 EVENTOS Y PARTICIPAR"): st.session_state['seccion'] = "ver_eventos"
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-gris">', unsafe_allow_html=True)
    if st.button("🚪 CERRAR SESIÓN"):
        del st.session_state['usuario']
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- LÓGICA DE LAS VENTANAS (CONTENIDO) ---
    st.divider()
    sec = st.session_state.get('seccion', 'inicio')

    if sec == "ranking":
        st.subheader("Ranking de Diamantes")
        us = db.reference('usuarios').get()
        if us:
            lista = [{"Nombre": v.get('nombre'), "💎": v.get('Diamantes', 0), "💰": v.get('deuda', 0)} for v in us.values()]
            st.table(sorted(lista, key=lambda x: x['💎'], reverse=True))

    elif sec == "registro":
        st.subheader("Registrar Guerrero")
        r_id = st.text_input("Nuevo ID")
        r_nom = st.text_input("Nombre")
        r_rol = st.selectbox("Rol", ["Miembro", "Moderador", "Lider"])
        if st.button("Guardar en el Imperio"):
            db.reference(f'usuarios/{r_id}').set({'nombre': r_nom, 'rol': r_rol, 'Diamantes': 0, 'deuda': 0})
            st.success("¡Registrado!")

    elif sec == "diamantes":
        st.subheader("Gestión de Saldo")
        target = st.text_input("ID Jugador")
        cant = st.number_input("Cantidad", min_value=1)
        if st.button("Entregar Diamantes"):
            ref = db.reference(f'usuarios/{target}')
            u = ref.get()
            if u: ref.update({'Diamantes': u.get('Diamantes', 0) + cant}); st.success("💎 Entregados")
        if st.button("Anotar Deuda"):
            ref = db.reference(f'usuarios/{target}')
            u = ref.get()
            if u: ref.update({'deuda': u.get('deuda', 0) + cant}); st.warning("💰 Deuda anotada")

    elif sec == "cambio_id":
        st.subheader("Traspaso de Cuentas")
        old_id = st.text_input("ID Antiguo")
        new_id = st.text_input("ID Nuevo")
        if st.button("Confirmar Traspaso"):
            ref = db.reference(f'usuarios/{old_id}')
            data = ref.get()
            if data:
                db.reference(f'usuarios/{new_id}').set(data)
                ref.delete()
                st.success("ID cambiado correctamente")

    elif sec == "eliminar":
        st.subheader("Desterrar Miembro")
        e_id = st.text_input("ID a eliminar")
        if st.button("ELIMINAR DEFINITIVAMENTE", help="¡Cuidado!"):
            db.reference(f'usuarios/{e_id}').delete()
            st.error("Miembro eliminado")

    elif sec == "crear_evento":
        st.subheader("Nuevo Evento 🔥")
        e_tit = st.text_input("Nombre del Evento")
        e_fec = st.text_input("Fecha y Hora")
        e_desc = st.text_area("Descripción")
        if st.button("Publicar"):
            db.reference('eventos').push().set({'nombre': e_tit, 'fecha': e_fec, 'descripcion': e_desc})
            st.success("Evento publicado")

    elif sec == "lista":
        st.subheader("Lista del Clan")
        us = db.reference('usuarios').get()
        if us:
            for uid, info in us.items():
                st.write(f"ID: `{uid}` | **{info.get('nombre')}** - *{info.get('rol')}*")

    elif sec == "ver_eventos":
        st.subheader("Eventos Disponibles")
        evs = db.reference('eventos').get()
        if evs:
            for eid, info in evs.items():
                with st.expander(f"🔥 {info['nombre']} - {info['fecha']}"):
                    st.write(info.get('descripcion'))
                    if st.button("Participar", key=eid): st.success("¡Te has unido!")

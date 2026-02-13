# --- LÓGICA DE ROLES MEJORADA ---
user = st.session_state['usuario']
id_yo = st.session_state['id_actual']

# AQUÍ PONES TU ID REAL DE FREE FIRE PARA QUE SIEMPRE SEAS ADMIN
ID_DEL_LIDER_REAL = "TU_ID_AQUÍ" 

# El sistema verifica: ¿Es el ID del jefe o dice Líder en la DB?
if id_yo == ID_DEL_LIDER_REAL or user.get('rol') == "Líder":
    rol_efectivo = "Líder"
elif user.get('rol') == "Moderador":
    rol_efectivo = "Moderador"
else:
    rol_efectivo = "Miembro"

st.sidebar.title(f"👤 {user.get('nombre')}")
st.sidebar.write(f"Rango detectado: **{rol_efectivo}**")

# Ahora usamos 'rol_efectivo' para mostrar los botones
opciones = ["📊 Mi Perfil", "🏆 Ranking"]
if rol_efectivo in ["Líder", "Moderador"]:
    opciones.append("⚒️ Gestionar Miembros")
if rol_efectivo == "Líder":
    opciones.append("👑 Panel de Control")


import customtkinter as ctk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, db
import os
import sys

# --- 1. CONFIGURACIÓN DE RUTA ---
def recurso_ruta(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- 2. CONEXIÓN A FIREBASE ---
ruta_llave = recurso_ruta("llave.json")
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(ruta_llave)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://escuadron-control-default-rtdb.firebaseio.com/'})
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar: {e}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppEscuadron(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PHOENIX EMPIRE - RECOVERY MODE")
        self.geometry("600x850")
        self.usuario_actual = {}
        self.mostrar_login()

    def limpiar_pantalla(self):
        for widget in self.winfo_children(): widget.destroy()

    # --- FUNCIÓN MAESTRA: RECONSTRUIR ENTIDADES ---
    def reparar_base_datos(self):
        try:
            # Esto crea la estructura exacta que perdiste
            admin_id = "1234"
            db.reference(f'usuarios/{admin_id}').set({
                'nombre': "Yosbel (Lider)",
                'rol': "Lider",
                'Diamantes': 0,
                'deuda': 0,
                'sanciones': 0
            })
            messagebox.showinfo("Éxito", "¡Entidades reconstruidas! Ya puedes entrar con el ID 1234")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo reparar: {e}")

    def mostrar_login(self):
        self.limpiar_pantalla()
        self.frame_login = ctk.CTkFrame(self, border_width=2, border_color="#E74C3C")
        self.frame_login.pack(pady=60, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(self.frame_login, text="Phoenix Empire\nescuadrón 🔥", 
                     font=("Roboto", 35, "bold"), text_color="#E74C3C").pack(pady=40)
        
        self.entry_id = ctk.CTkEntry(self.frame_login, placeholder_text="ID de Jugador", 
                                     width=280, height=45, border_color="#E74C3C")
        self.entry_id.pack(pady=10)
        
        ctk.CTkButton(self.frame_login, text="ENTRAR", command=self.verificar_acceso, 
                      height=50, width=200, fg_color="#E74C3C", hover_color="#C0392B").pack(pady=20)

        # BOTÓN DE EMERGENCIA (Usa esto una sola vez)
        ctk.CTkButton(self.frame_login, text="🛠 REPARAR ENTIDADES", command=self.reparar_base_datos, 
                      fg_color="transparent", border_width=1, text_color="gray").pack(pady=10)

    def verificar_acceso(self):
        mi_id = self.entry_id.get().strip()
        if not mi_id: return
        try:
            # Buscamos en 'usuarios' (en minúsculas para evitar errores)
            u = db.reference(f'usuarios/{mi_id}').get()
            if u:
                self.usuario_actual = {'id': mi_id, 'nombre': u.get('nombre'), 'rol': u.get('rol')}
                self.mostrar_menu_principal()
            else: 
                messagebox.showerror("Error", "ID no encontrado. Dale al botón 'REPARAR' si la base está vacía.")
        except: 
            messagebox.showerror("Error", "Error de conexión")

    def mostrar_menu_principal(self):
        self.limpiar_pantalla()
        u = self.usuario_actual
        ctk.CTkLabel(self, text="PANEL DE LIDER", font=("Roboto", 35, "bold"), text_color="#3b8ed0").pack(pady=20)
        ctk.CTkLabel(self, text=f"Usuario: {u['nombre']}", font=("Roboto", 22)).pack(pady=5)

        # Botón para registrar a otros (esto crea la estructura completa para cada uno)
        if u['rol'] == "Lider":
            self.crear_boton("📝 REGISTRAR NUEVO MIEMBRO", self.abrir_registro, "#1f538d")
            self.crear_boton("📊 RANKING Y DEUDAS", self.abrir_ranking, "#1f538d")
            self.crear_boton("❌ ELIMINAR MIEMBRO", self.abrir_eliminar, "#FF0000")

        self.crear_boton("🚪 CERRAR SESIÓN", self.mostrar_login, "#606060")

    def crear_boton(self, texto, comando, color):
        btn = ctk.CTkButton(self, text=texto, command=comando, fg_color=color, height=50, font=("bold", 15))
        btn.pack(pady=7, padx=60, fill="x")

    def abrir_registro(self):
        v = ctk.CTkToplevel(self); v.geometry("400x450"); v.attributes("-topmost", True)
        ctk.CTkLabel(v, text="Registrar Guerrero", font=("bold", 20), text_color="#E74C3C").pack(pady=20)
        id_n = ctk.CTkEntry(v, placeholder_text="Nuevo ID", width=250); id_n.pack(pady=10)
        nom = ctk.CTkEntry(v, placeholder_text="Nombre", width=250); nom.pack(pady=10)
        rol = ctk.CTkOptionMenu(v, values=["Miembro", "Moderador", "Lider"], fg_color="#E74C3C"); rol.pack(pady=10)
        
        def reg():
            # Esta es la parte que "repite" la estructura por cada miembro
            db.reference(f'usuarios/{id_n.get().strip()}').set({
                'nombre': nom.get(),
                'rol': rol.get(),
                'Diamantes': 0,
                'deuda': 0,
                'sanciones': 0
            })
            messagebox.showinfo("Éxito", "Guerrero registrado")
            v.destroy()
        
        ctk.CTkButton(v, text="Guardar en el Imperio", command=reg, fg_color="#E74C3C").pack(pady=30)

    # (Las demás funciones Ranking y Eliminar se mantienen igual)
    def abrir_ranking(self): pass
    def abrir_eliminar(self): pass

if __name__ == "__main__":
    app = AppEscuadron()
    app.mainloop()

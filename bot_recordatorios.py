import schedule
import time
import requests

TOKEN_TELEGRAM = "8682305104:AAEJVSbX2uvBH2qXcRqtiMpfpBy4_2n42XY"
ID_GRUPO_KYSEN = "-5114492594"

def enviar_aviso(mensaje="⚠️ *¡RECORDATORIO KYSEN!* ⚠️\n\nGuerreros, revisa la App de gestión. Confirmen sus roles, asistencias a eventos y mantengan la disciplina. ¡El clan los necesita!"):
    # Asegúrate de tener tu TOKEN y ID arriba de esto
    URL = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    carga_util = {"chat_id": ID_GRUPO_KYSEN, "text": mensaje, "parse_mode": "Markdown"}
    
    try:
        requests.post(URL, data=carga_util)
        print("Recordatorio enviado con éxito al grupo de Telegram.")
    except Exception as e:
        print(f"Error al enviar: {e}")

# Aquí ajustas las horas a las que quieres que se envíe el mensaje
schedule.every().day.at("09:00").do(enviar_aviso)
schedule.every().day.at("16:00").do(enviar_aviso)
schedule.every().day.at("21:00").do(enviar_aviso)

print("Iniciando motor de alarmas Kysen E-Sports. Presiona Ctrl+C para detenerlo.")

# Mensaje de prueba de vida
print("Iniciando sistema... Enviando mensaje de prueba.")
enviar_aviso("🤖 *SISTEMA KYSEN:* El bot de recordatorios acaba de ser encendido y está vigilando los eventos.")

while True:
    schedule.run_pending()
    time.sleep(60) # Revisa cada minuto para no gastar recursos




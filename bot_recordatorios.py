import schedule
import time
import requests

TOKEN_TELEGRAM = "8682305104:AAEJVSbX2uvBH2qXcRqtiMpfpBy4_2n42XY"
ID_GRUPO_KYSEN = "-5114492594"

def enviar_aviso():
    mensaje = "⚠️ *¡RECORDATORIO KYSEN!* ⚠️\n\nGuerreros, revisen la App de gestión. Confirmen sus roles, asistencias a eventos y mantengan la disciplina. ¡El clan los necesita!"
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {"chat_id": ID_GRUPO_KYSEN, "text": mensaje, "parse_mode": "Markdown"}
    
    try:
        requests.post(url, data=payload)
        print("Recordatorio enviado con éxito al grupo de Telegram.")
    except Exception as e:
        print(f"Error al enviar: {e}")

# Aquí ajustas las horas a las que quieres que se envíe el mensaje a tu equipo
schedule.every().day.at("09:00").do(enviar_aviso)
schedule.every().day.at("14:30").do(enviar_aviso)
schedule.every().day.at("20:00").do(enviar_aviso)

print("Iniciando motor de alarmas Kysen E-Sports. Presiona Ctrl+C para detenerlo.")

while True:
    schedule.run_pending()
    time.sleep(60) # Revisa cada minuto para no gastar recursos
import datetime

def chequear_y_enviar():
    # 1. Obtener las horas configuradas desde Firebase
    config = db.reference('configuracion/horarios').get()
    if not config:
        return # Si no hay nada en Firebase, no hace nada

    # 2. Obtener la hora actual (Ajustada a Venezuela -4)
    # PythonAnywhere usa UTC, así que restamos 4 horas para saber tu hora local
    ahora = datetime.datetime.now() - datetime.timedelta(hours=4)
    hora_actual = ahora.strftime("%H:%M")

    # 3. Comparar si la hora actual coincide con alguna de las de Firebase
    if hora_actual in [config['h1'], config['h2'], config['h3']]:
        print(f"¡Coincidencia! Son las {hora_actual}. Enviando aviso...")
        enviar_aviso()
        time.sleep(61) # Dormimos un minuto para que no envíe el mensaje varias veces en el mismo minuto

print("Motor Kysen Inteligente Iniciado. Leyendo horarios de Firebase...")

while True:
    chequear_y_enviar()
    time.sleep(30) # Revisa Firebase cada 30 segundos

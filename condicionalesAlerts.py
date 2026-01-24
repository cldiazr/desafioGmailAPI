import re
from webhookAlert import alert_webhook

def revision_correo(bodyCorreo,asuntoCorreo,fromCorreo,listAlerts):
    partMensaje = (f"Asunto: {asuntoCorreo}" +" | "+ f"De: {fromCorreo}" +" | ")
    if re.search(r'\bcontraseña\b', bodyCorreo):
        mensaje = partMensaje + "Palabra: Contraseña"
        print(mensaje)
        listAlerts.add(mensaje)
        alert_webhook(mensaje)
    if re.search(r'\bconfidencial\b', bodyCorreo):
        mensaje = partMensaje + "Palabra: Confidencial"
        print(mensaje)
        listAlerts.add(mensaje)
        alert_webhook(mensaje)

def es_archivo_peligroso(filename,asuntoCorreo,fromCorreo,listAlerts):
    partMensaje = (f"Asunto: {asuntoCorreo}" +" | "+ f"De: {fromCorreo}" +" | Archivo adjunto encontrado: ")
    nombre_limpio = filename.lower().strip()
    
    extensiones_prohibidas = (".zip", ".exe", ".js", ".bat")
    if nombre_limpio.endswith(extensiones_prohibidas):
        mensaje = partMensaje + filename
        print(mensaje)
        listAlerts.add(mensaje)
        alert_webhook(mensaje)
    partes = nombre_limpio.split('.')
    
    if len(partes) > 2:
        for parte in partes[1:-1]:
            if f".{parte}" in extensiones_prohibidas:
                mensaje = partMensaje + filename
                print(mensaje)
                listAlerts.add(mensaje)
                alert_webhook(mensaje)
    return False

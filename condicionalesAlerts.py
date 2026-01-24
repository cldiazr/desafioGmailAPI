import re
from webhookAlert import alert_webhook

"""
    * Analiza el cuerpo del correo, para detectar las palabras claves "Contraseña" o "Confidencial".
    * El cuerpo del correo se recibe todo en minuscula para evitar fallos al momento de detectar las palabras
    * Muestra en consola un mensaje donde se describe Asunto, emisor y la palabra detectada
    * Se guardan como mensajes en un Conjunto de alertas y se envia el mensaje en un WebHook
    
    Args:
        bodyCorreo (str): Cuerpo del correo.
        asuntoCorreo (str): Asunto del correo
        fromCorreo (str) : Emisor del correo
        listAlerts (set) : Conjunto donde estan almacenadas las alertas
"""

def revision_correo(bodyCorreo,asuntoCorreo,fromCorreo,listAlerts):
    partMensaje = (f"Asunto: {asuntoCorreo}" +" | "+ f"De: {fromCorreo}" +" | ")
    correo = bodyCorreo.strip() +" "+ asuntoCorreo.strip()
    if re.search(r'\bcontraseña\b', correo.lower()):
        mensaje = partMensaje + "Palabra: Contraseña"
        print(mensaje)
        listAlerts.add(mensaje)
        alert_webhook(mensaje)
    if re.search(r'\bconfidencial\b', correo.lower()):
        mensaje = partMensaje + "Palabra: Confidencial"
        print(mensaje)
        listAlerts.add(mensaje)
        alert_webhook(mensaje)
    return

"""
    * Analiza el nombre del archivo para detectar extensiones maliciosas.
    * El analisis se realiza en todo el nombre del archivo, para evitar extensiones ocultas.
    * Cumple con el hito de analizar adjuntos .zip, .exe, .js, .bat.
    * Muestra en consola un mensaje donde se describe Asunto, emisor y nombre del archivo sospechoso
    * Se guardan como mensajes en un Conjunto de alertas y se envia el mensaje en un WebHook
    
    Args:
        filename (str): Nombre del archivo adjunto.
        asuntoCorreo (str): Asunto del correo
        fromCorreo (str) : Emisor del correo
        listAlerts (set) : Conjunto donde estan almacenadas las alertas
"""

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
    return

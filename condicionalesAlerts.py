import re

def revision_correo(bodyCorreo,asuntoCorreo,fromCorreo,listAlerts):
    if re.search(r'\bcontraseña\b', bodyCorreo):
        print(f"Asunto: {asuntoCorreo}" +" | "+ f"De: {fromCorreo}" +" | "+ "Palabra: Contraseña")
        listAlerts.add(f"Asunto: {asuntoCorreo}" +" | "+ f"De: {fromCorreo}" +" | "+ "Palabra: Contraseña")
    if re.search(r'\bconfidencial\b', bodyCorreo):
        print(f"Asunto: {asuntoCorreo}" +" | "+f"De: {fromCorreo}" +" | "+ "Palabra: Confidencial")
        listAlerts.add(f"Asunto: {asuntoCorreo}" +" | "+ f"De: {fromCorreo}" +" | "+ "Palabra: Confidencial")

def es_archivo_peligroso(filename):
    # 1. Normalización básica
    nombre_limpio = filename.lower().strip()
    
    extensiones_prohibidas = (".zip", ".exe", ".js", ".bat")
    # 3. Verificación de extensión final
    if nombre_limpio.endswith(extensiones_prohibidas):
        return True

    # 4. Verificación de doble extensión
    # Dividimos el nombre por los puntos
    partes = nombre_limpio.split('.')
    
    if len(partes) > 2:
        # Revisamos si alguna de las extensiones intermedias es peligrosa
        for parte in partes[1:-1]: # Saltamos el nombre y la extensión final
            if f".{parte}" in extensiones_prohibidas:
                return True

    return False
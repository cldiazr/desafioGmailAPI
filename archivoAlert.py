
"""
    * Las alertas se reciben en un conjunto
    * Se crea otro conjunto donde se van a almacenar las alertas que ya estan guardadas en el archivo
        Esto se realiza para comparar ambos conjuntos y evitar guardar alertas repetidas
    * El archivo se lee con utf-8 para guardar el contenido con los caracteres especiales
    * Se itera cada elemento del conjunto para guardar las alertas en una linea cada uno
    * Se establece una constante donde se almacena el nombre del archivo.
    
    Args:
        listAlerts (set): Conjuntos con las alertas detectadas en el analisis.
        
"""

ARCHIVO_ALERTS = "alertas.txt"

def save_archivo(listAlerts):
    alertas_existentes = set()
    try:
        with open(ARCHIVO_ALERTS, "r", encoding="utf-8") as f:
            alertas_existentes = {line.strip() for line in f.readlines()}
    except FileNotFoundError:
        pass
    with open(ARCHIVO_ALERTS, "a", encoding="utf-8") as archivo:
        for alert in listAlerts:
            if alert not in alertas_existentes:
                archivo.write(alert + "\n")
    return
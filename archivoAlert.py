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
ARCHIVO_ALERTS = "alertas.txt"

def save_archivo(listAlerts):
    try:
        readAlerts = None
        with open(ARCHIVO_ALERTS, "r", encoding="utf-8") as validar:
            readAlerts = validar.readlines()
    except FileNotFoundError:
        pass
    with open(ARCHIVO_ALERTS, "a", encoding="utf-8") as archivo:
        for alert in listAlerts:
            c = 0
            if readAlerts : 
                for i, read in enumerate(readAlerts, start=1):
                    if (read.strip() == alert):
                        c += 1
                if not(c) :
                    archivo.write(alert + "\n")
            else:
                archivo.write(alert + "\n")
    return
from email import header
import requests
import json

WEBHOOK_URL = "https://webhook.site/a68dc9de-1c92-4304-834e-86ac27d80368"

def alert_webhook(mensaje):
    payload = {"text" : mensaje}
    try:
        response = requests.post(
            WEBHOOK_URL,
            data = json.dumps(payload),
            headers = {'Content-Type': 'application/json'}
        )
        if response.status_code == 200 :
            print("✓ Alerta enviada al webhook")
        else :
            print(f"X Error enviando webhook: {response.status_code}")
    except Exception:
        print("Error de conexión con webhook")
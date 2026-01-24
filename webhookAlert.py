import requests
import json

'''
    WEBHOOK
        * Se utiliza la app web Webhook.site
        * Genera una URL unica para poder realizar las peticiones post
            esta URL se guarda en una constante.
        * Se establece un variable de tipo diccionario donde se establece el formato
            que va a tener el mensaje a enviar "text", aqui si guardara el mensaje.
        * El diccionario se convierte en una cadena de texto tipo JSON, para que 
            la webhook pueda leer el mensaje.
        * Por cada mensaje enviado se muestra en pantalla un mensaje indicando
            si fue satisfactorio el envio o no.
        * El mensaje que se envia es la alerta detectada en el analisis de cada correo.
'''

WEBHOOK_URL = "https://webhook.site/c5109a32-c479-409d-a480-e96d9cb49fd3"

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
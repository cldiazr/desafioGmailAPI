import os.path
from stringprep import c22_specials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email import policy
from email.parser import BytesParser
import re

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
ARCHIVO_ALERTS = "archivo.txt"

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

def save_archivo(listAlerts):
    try:
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

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail messages.
    """
    listAlert = set()
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = (
            service.users().messages().list(userId="me", includeSpamTrash=True).execute()
        )
        messages = results.get("messages", [])

        if not messages:
            print("No messages found.")
            return
        print("Alertas:")
        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"], format='raw').execute()
            )
            msg_bytes = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            mime_msg = BytesParser(policy=policy.default).parsebytes(msg_bytes)
            if mime_msg.is_multipart():
                for part in mime_msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        if not((re.search(r'\bgoogle.com\b', mime_msg['from'])) or (re.search(r'\bcashea.app\b', mime_msg['from'])) or (re.search(r'\bspicosmos.com\b', mime_msg['from']))):
                            if re.search(r'\bcontraseña\b', body.lower()):
                                print(f"Asunto: {mime_msg['subject']}" +" | "+ f"De: {mime_msg['from']}" +" | "+ "Palabra: Contraseña")
                                
                                listAlert.add(f"Asunto: {mime_msg['subject']}" +" | "+ f"De: {mime_msg['from']}" +" | "+ "Palabra: Contraseña")
                            if re.search(r'\bconfidencial\b', body.lower()):
                                print(f"Asunto: {mime_msg['subject']}" +" | "+f"De: {mime_msg['from']}" +" | "+ "Palabra: Confidencial")
                                listAlert.add(f"Asunto: {mime_msg['subject']}" +" | "+ f"De: {mime_msg['from']}" +" | "+ "Palabra: Confidencial")
                    elif "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            if es_archivo_peligroso(filename):
                                print(f"Asunto: {mime_msg['subject']}" +" | "+ f"De: {mime_msg['from']}" +" | "+ f"Archivo adjunto encontrado: {filename}")
                                
                                listAlert.add(f"Asunto: {mime_msg['subject']}" +" | "+ f"De: {mime_msg['from']}" +" | "+ f"Archivo adjunto encontrado: {filename}")
            else:
                body = mime_msg.get_payload(decode=True).decode()
                if not((re.search(r'\bgoogle.com\b', mime_msg['from'])) and (re.search(r'\bcashea.app\b', mime_msg['from'])) and (re.search(r'\bspicosmos.com\b', mime_msg['from']))):
                    if re.search(r'\bcontraseña\b', body.lower()):
                        print(f"Asunto: {mime_msg['subject']}" +" | "+ f"De: {mime_msg['from']}" +" | "+ "Palabra: Contraseña")
                        listAlert.add(f"Asunto: {mime_msg['subject']}" +" | "+ f"De: {mime_msg['from']}" +" | "+ "Palabra: Contraseña")
                    if re.search(r'\bconfidencial\b', body.lower()):
                        print(f"Asunto: {mime_msg['subject']}" +" | "+f"De: {mime_msg['from']}" +" | "+ "Palabra: Confidencial")
                        listAlert.add(f"Asunto: {mime_msg['subject']}" +" | "+f"De: {mime_msg['from']}" +" | "+ "Palabra: Confidencial")
        save_archivo(listAlert)
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
    


if __name__ == "__main__":
    main()
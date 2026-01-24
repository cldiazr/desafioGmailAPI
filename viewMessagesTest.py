from connectApiGmail import connectApi
from googleapiclient.discovery import build
from archivoAlert import  save_archivo
from condicionalesAlerts import revision_correo, es_archivo_peligroso
from googleapiclient.errors import HttpError
import httplib2
import base64
from email import policy
from email.parser import BytesParser
import re

DOMINIOS_SEGUROS = ["google.com", "cashea.app", "spicosmos.com", "empresa.com"]

def main():
    listAlert = set()
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials= connectApi())
        results = (
            service.users().messages().list(userId="me", includeSpamTrash=True).execute()
        )
        messages = results.get("messages", [])

        if not messages:
            print("Sin mensajes")
            return
        print("Alertas:")
        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"], format='raw').execute()
            )
            msg_bytes = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            mime_msg = BytesParser(policy=policy.default).parsebytes(msg_bytes)
            remitente = mime_msg['from'].lower()
            if not(any(dominio in remitente for dominio in DOMINIOS_SEGUROS)):
                if mime_msg.is_multipart():
                    for part in mime_msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode('utf-8', errors='replace')
                            revision_correo(body.lower(),mime_msg['subject'],mime_msg['from'],listAlert)
                        elif "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename:
                                    es_archivo_peligroso(filename,mime_msg['subject'],mime_msg['from'],listAlert)
                else:
                    body = mime_msg.get_payload(decode=True).decode('utf-8', errors='replace')
                    revision_correo(body.lower(),mime_msg['subject'],mime_msg['from'],listAlert)
        save_archivo(listAlert)
    except HttpError as error:
        if error: 
            print("Ocurrio un error al conectarse a la API de Gmail")
    except httplib2.ServerNotFoundError as error:
        if error: 
            print("Ocurrio un error al conectarse a la API de Gmail")
    except Exception as e:
        if e:
            print("Ocurrió un error inesperado")
    


if __name__ == "__main__":
    main()
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

"""
    * Se indica el permiso solicitado, que es de lectura de correos "SCOPES"
    * Se establece la conexion con la API de Gmail, donde se envia el token y credenciales para 
        establecer la conexion. Como lo indica la documentacion de Google.
    * Se necesitan en la carpeta del proyecto los archivos token.json y credentials.json
        * token.json se crea de forma automatica al momento de establecer una conexion satisfactoria
        * credentials.json se tiene que descargar desde el dashboard de la API de Gmail
"""

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def connectApi():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
     
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email import policy
from email.parser import BytesParser
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail messages.
    """
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
        print("Messages:")
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
                        if not((re.search(r'\bgoogle.com\b', mime_msg['from'])) and (re.search(r'\bcashea.app\b', mime_msg['from'])) and (re.search(r'\bspicosmos.com\b', mime_msg['from']))):
                            if re.search(r'\bcontraseña\b', body.lower()):
                                print(f"Asunto: {mime_msg['subject']}")
                                print(f"De: {mime_msg['from']}")
                                print("Palabra: Contraseña")
                            if re.search(r'\bconfidencial\b', body.lower()):
                                print(f"Asunto: {mime_msg['subject']}")
                                print(f"De: {mime_msg['from']}")
                                print("Palabra: Confidencial")
                    elif "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            if filename.lower().replace(" ", "").endswith(".pdf"):
                                print(f"Asunto: {mime_msg['subject']}")
                                print(f"Archivo adjunto encontrado: {filename}")
            else:
                body = mime_msg.get_payload(decode=True).decode()
                if not((re.search(r'\bgoogle.com\b', mime_msg['from'])) and (re.search(r'\bcashea.app\b', mime_msg['from'])) and (re.search(r'\bspicosmos.com\b', mime_msg['from']))):
                            if re.search(r'\bcontraseña\b', body.lower()):
                                print(f"Asunto: {mime_msg['subject']}")
                                print(f"De: {mime_msg['from']}")
                                print("Palabra: Contraseña")
                            if re.search(r'\bconfidencial\b', body.lower()):
                                print(f"Asunto: {mime_msg['subject']}")
                                print(f"De: {mime_msg['from']}")
                                print("Palabra: Confidencial")
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
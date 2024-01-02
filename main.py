import requests, json, yaml, datetime

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gmail import create_schedule, create_events_object
from notion import create_notion_object
from deleteEmail import delete_old_entries

if os.path.exists('credentials.yml'):
  with open("credentials.yml") as f:
    content = f.read()

my_credentials = yaml.load(content, Loader=yaml.FullLoader)

token, database = my_credentials["secret"], my_credentials["database"]

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/calendar"]
HEADER = ["Día", "Mes", "Entrada", "Salida", "Posición"]
NOTION_HEADERS = {
  "Authorization": "Bearer " + token,
  "Content-Type": "application/json",
  "Notion-Version": "2022-06-28"
}
NOTION_URL = "https://api.notion.com/v1/pages"
DATABASE = f"https://api.notion.com/v1/databases/{database}/query"
DATENOW = datetime.datetime.now()

def main():
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

  # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        schedule = create_schedule()
    
        # check if the current day is greater than 15 to delete all the relations
        # in the pasts months, with that we can have a clear look of the next payment
        delete_old_entries(DATABASE, NOTION_HEADERS, NOTION_URL)

        if schedule:
            events = create_events_object(schedule)
            pages = create_notion_object(schedule)

        # ! con timedelta(day=x) puedes sumar o restar dias si vas a crear el modulo para los pagos

        print("Iniciando inserciones en Google Calendar...")
        for event in events:
            service.events().insert(calendarId='primary', body=event).execute()
        print("¡Inserciones en Google Calendar añadidas correctamente!")

        print("Iniciando inserciones en Notion...")
        for page in pages:
            data = json.dumps(page)
            response = requests.request("POST", NOTION_URL, headers=NOTION_HEADERS, data=data)
        print("¡Inserciones en Notion añadidas correctamente!")

    except HttpError as error:
        print('An error occurred: %s' % error)

if __name__ == '__main__':
  main()
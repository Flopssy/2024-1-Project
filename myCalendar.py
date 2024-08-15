import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_calendar_events(service, days=1):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat() + 'Z'
    
    print(f"{now} 부터 {end} 까지의 일정을 가져오는 중...")
    
    events_result = service.events().list(
        calendarId='primary', timeMin=now, timeMax=end,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('일정이 없습니다.')
    else:
        print(f"Found {len(events)} event(s).")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(f"이름: {event['summary']}, 시간: {start}")
    
    return events

service = get_calendar_service()
events = get_calendar_events(service)
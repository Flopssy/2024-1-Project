import os
import datetime
import requests
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

SERVICE_KEY = 'mM+MUWusU3iCXgBG3OsPA+vkdB70NOA288gOyI58OVUR/DYG+dW5hJwoyYT2POuUtwdEzy7rnA7dx8FmhlPJNg=='
LOCATION = {'nx': 76, 'ny': 92}

def get_kma_weather(nx, ny, target_date):
    base_date = target_date.strftime('%Y%m%d')
    base_time = '0500'

    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        'serviceKey': SERVICE_KEY,
        'pageNo': '1',
        'numOfRows': '100',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if data['response']['header']['resultCode'] == '00':
            items = data['response']['body']['items']['item']
            return items
        else:
            print(f"No data available: {data['response']['header']['resultMsg']}")
            return None
    else:
        print(f"HTTP request error: {response.status_code}, {response.text}")
        return None

def recommend_clothing(temperature):
    if temperature < 0:
        return "기온이 영하입니다. 겨울용 옷을 추천합니다."
    elif 0 <= temperature < 10:
        return "겨울용 옷을 추천합니다."
    elif 10 <= temperature < 20:
        return "가벼운 재킷을 걸치거나 니트를 추천합니다."
    elif 20 <= temperature < 25:
        return "얇은 셔츠나 가벼운 니트를 추천합니다."
    elif 25 <= temperature < 30:
        return "반팔과 반바지를 추천합니다."
    else:
        return "얇은 긴팔 티와 얇은 긴바지 혹은 반바지를 추천합니다."

test_date = datetime.datetime.now().date()
weather_data = get_kma_weather(LOCATION['nx'], LOCATION['ny'], test_date)

if weather_data:
    for item in weather_data:
        if isinstance(item, dict) and item.get('category') == 'TMP':
            temperature = float(item['fcstValue'])
            clothing_recommendation = recommend_clothing(temperature)
            print(f"기온: {temperature}°C, 의상: {clothing_recommendation}")
            break
else:
    print("날씨 데이터를 불러오지 못했습니다.")
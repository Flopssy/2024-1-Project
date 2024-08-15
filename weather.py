import datetime
import requests


SERVICE_KEY = 'mM+MUWusU3iCXgBG3OsPA+vkdB70NOA288gOyI58OVUR/DYG+dW5hJwoyYT2POuUtwdEzy7rnA7dx8FmhlPJNg=='
LOCATION = {'nx': 76, 'ny': 92}

def get_kma_weather(nx, ny, target_date):
    base_date = target_date.strftime('%Y%m%d')
    base_time = '1100'

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

    print(f"{base_date} nx = {nx}, ny = {ny} 위치의 날씨 요청 중입니다.")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("API 요청 성공")
        data = response.json()
        print(f"수신된 데이터: {data}")
        return data
    else:
        print(f"오류 {response.status_code}, {response.text}")
        return None

test_date = datetime.datetime.now().date()
weather_data = get_kma_weather(LOCATION['nx'], LOCATION['ny'], test_date)

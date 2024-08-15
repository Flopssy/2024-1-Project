# 일정 날씨 기반 옷 추천 시스템

개발 과정
-
1. Google Calender API 사용을 위한 OAuth 2.0 ID 발급
2. Google API에서 제공한 quickstart.py 예제를 사용하여 Google Calender API 접근 확인
3. 기상청 API에 접근하여 기상 정보 수집 확인

코드 설명
-
- myCalendar.py: Google Calendar API를 이용하여 현재 날짜로부터 24시간 내에 등록된 일정 확인
- weather.py: 기상청 단기예보 API로부터 지정된 좌표의 기상 데이터 확인

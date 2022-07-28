from datetime import datetime
import json
import requests

def current_date():
    today = datetime.now()

    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    minute = today.minute
    weekday = ''
    weekday_num = today.weekday()

    if weekday_num == 0: weekday = '월요일'
    elif weekday_num == 1: weekday = '화요일'
    elif weekday_num == 2: weekday = '수요일'
    elif weekday_num == 3: weekday = '목요일'
    elif weekday_num == 4: weekday = '금요일'
    elif weekday_num == 5: weekday = '토요일'
    elif weekday_num == 6: weekday = '일요일'
    
    return [year, month, day, hour, minute, weekday]

def current_weather():
    city = "Seoul"
    lat = '37.5683'
    lon = '126.9778'
    part = 'daily,hourly,minutely'
    api_key = 'd592bc04129c77f12ac6e306d45ea0c4'
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    result = requests.get(api)
    data = json.loads(result.text)

    temp = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    weather = data['weather'][0]['main']
    rain = ''
    snow = ''

    try:
        rain = data['rain']['1h']
    except:
        pass

    try:
        snow = data['snow']['1h']
    except:
        pass
    
    weather_list = ['Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'Mist', 'Smoke', 'Haze', 'Dust',
                'Fog', 'Sand', 'Ash', 'Squall', 'Tornado', 'Clear', 'Clouds']
    current_w = ''

    if weather == 'Thunderstorm': current_w = '뇌우'
    elif weather == 'Drizzle': current_w = '이슬비'
    elif weather == 'Rain': current_w = '비'
    elif weather == 'Snow': current_w = '눈'
    elif weather == 'Mist': current_w = '안개'
    elif weather == 'Smoke': current_w = '안개'
    elif weather == 'Haze': current_w = '안개'
    elif weather == 'Dust': current_w = '먼지'
    elif weather == 'Fog': current_w = '안개'
    elif weather == 'Sand': current_w = '모래먼지'
    elif weather == 'Ash': current_w = '화산재'
    elif weather == 'Squall': current_w = '돌풍'
    elif weather == 'Tornado': current_w = '폭풍'
    elif weather == 'Clear': current_w = '맑음' 
    elif weather == 'Clouds': current_w = '구름' 

    curent_rain = ''
    if rain == '':
        current_rain = 0
    else:
        curent_rain = rain

    current_snow = ''
    if rain == '':
        curent_snow = 0
    else:
        curent_snow = rain

    return [current_w, temp, humidity, wind_speed, curent_rain, current_snow]

def current_date_weather():
    today = datetime.now()

    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    minute = today.minute
    weekday = ''
    weekday_num = today.weekday()

    if weekday_num == 0: weekday = '월요일'
    elif weekday_num == 1: weekday = '화요일'
    elif weekday_num == 2: weekday = '수요일'
    elif weekday_num == 3: weekday = '목요일'
    elif weekday_num == 4: weekday = '금요일'
    elif weekday_num == 5: weekday = '토요일'
    elif weekday_num == 6: weekday = '일요일'
    
    city = "Seoul"
    lat = '37.5683'
    lon = '126.9778'
    part = 'daily,hourly,minutely'
    api_key = 'd592bc04129c77f12ac6e306d45ea0c4'
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    result = requests.get(api)
    data = json.loads(result.text)

    temp = round(data['main']['temp'])
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    weather = data['weather'][0]['main']
    rain = ''
    snow = ''

    try:
        rain = data['rain']['1h']
    except:
        pass

    try:
        snow = data['snow']['1h']
    except:
        pass
    
    weather_list = ['Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'Mist', 'Smoke', 'Haze', 'Dust',
                'Fog', 'Sand', 'Ash', 'Squall', 'Tornado', 'Clear', 'Clouds']
    current_w = ''

    if weather == 'Thunderstorm': current_w = '뇌우'
    elif weather == 'Drizzle': current_w = '이슬비'
    elif weather == 'Rain': current_w = '비'
    elif weather == 'Snow': current_w = '눈'
    elif weather == 'Mist': current_w = '안개'
    elif weather == 'Smoke': current_w = '안개'
    elif weather == 'Haze': current_w = '안개'
    elif weather == 'Dust': current_w = '먼지'
    elif weather == 'Fog': current_w = '안개'
    elif weather == 'Sand': current_w = '모래먼지'
    elif weather == 'Ash': current_w = '화산재'
    elif weather == 'Squall': current_w = '돌풍'
    elif weather == 'Tornado': current_w = '폭풍'
    elif weather == 'Clear': current_w = '맑음' 
    elif weather == 'Clouds': current_w = '구름' 

    curent_rain = ''
    if rain == '':
        current_rain = 0
    else:
        curent_rain = rain

    current_snow = ''
    if rain == '':
        curent_snow = 0
    else:
        curent_snow = rain

    total = f"{year}년 {month}월 {day}일 {weekday} 현재 {temp} °C {current_w}" 

    return total
   
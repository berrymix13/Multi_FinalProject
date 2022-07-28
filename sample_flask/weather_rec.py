import json
import random
import copy
from weather import current_date, current_weather

def weather_nail():

    year, month, day, hour, minute, weekday = current_date()
    current_w, temp, humidity, wind_speed, current_rain, current_snow = current_weather()

    season = ''
    weather = ''
    
    if month == 12 or month == 1 or month == 2:
        season = "겨울"
    elif month == 3 or month == 4 or month == 5:
        season = "봄"
    elif month == 6 or month == 7 or month == 8:
        season = "여름"
    elif month == 9 or month == 10 or month == 11:
        season = "가을"
    
    if current_w == '맑음':
        weather = '맑음'
    elif current_w == '비':
        weather = '비'
    elif current_w == '눈':
        weather = '눈'    
    
    with open('static/json/nail_tag.json', 'r', encoding="UTF-8") as f:
        json_data = json.load(f)

    value_list = list(json_data.values())
    key_list = list(json_data.keys())

    sample_list = []
    sample_key_list = []

    if weather == '':

        idx_list = []

        for i in range(len(value_list)):
            for we in value_list[i]['날씨']:
                if we == season:
                    idx_list.append(i)

        choice_list = []
        choice_key_list = []

        for i in idx_list:
            choice_list.append(value_list[i]['이름'])
            choice_key_list.append(key_list[i])

        if len(choice_list) > 4:
            random_list = random.sample(range(0, len(choice_list)), 4)
            for i in random_list:
                sample_list.append(choice_list[i])
                sample_key_list.append(choice_key_list[i])

    else :
        se_we = [season, weather]
        nweather = se_we
        tmp4=[]; key_lst=[]
        for nail in json_data:
            try:
                if nweather[0] in weather:
                    for nd in nweather:
                        if nd in weather:
                            if nd in list(json_data[nail].values())[3]:
                                tmp4.append(list(json_data[nail].values())[4])
                                key_lst.append(nail)
                else:
                    tmp4.append(list(json_data[nail].values())[4])
                    key_lst.append(nail)
            except:
                pass

        if len(tmp4) > 4:
            random_list = random.sample(range(0, len(tmp4)), 4)      
            for i in random_list:
                    sample_list.append(tmp4[i])
                    sample_key_list.append(key_lst[i])       
            
    return sample_list, sample_key_list

def weather_pedi():

    year, month, day, hour, minute, weekday = current_date()
    current_w, temp, humidity, wind_speed, current_rain, current_snow = current_weather()

    season = ''
    weather = ''
    if month == 12 or month == 1 or month == 2:
        season = "겨울"
    elif month == 3 or month == 4 or month == 5:
        season = "봄"
    elif month == 6 or month == 7 or month == 8:
        season = "여름"
    elif month == 9 or month == 10 or month == 11:
        season = "가을"
    
    if current_w == '맑음':
        weather = '맑음'
    elif current_w == '비':
        weather = '비'
    elif current_w == '눈':
        weather = '눈'   

    with open('static/json/pedi_tag.json', 'r', encoding="UTF-8") as f:
        json_data = json.load(f)
    
    value_list = list(json_data.values())
    key_list = list(json_data.keys())

    sample_list = []
    sample_key_list = []

    if weather == '':

        idx_list = []

        for i in range(len(value_list)):
            for we in value_list[i]['날씨']:
                if we == season:
                    idx_list.append(i)

        choice_list = []
        choice_key_list = []

        for i in idx_list:
            choice_list.append(value_list[i]['이름'])
            choice_key_list.append(key_list[i])

        if len(choice_list) > 4:
            random_list = random.sample(range(0, len(choice_list)), 4)
            for i in random_list:
                sample_list.append(choice_list[i])
                sample_key_list.append(choice_key_list[i])
        
    else :
        se_we = [season, weather]
        nweather = se_we
        tmp4=[]; key_lst=[]
        for nail in json_data:
            try:
                if nweather[0] in weather:
                    for nd in nweather:
                        if nd in weather:
                            if nd in list(json_data[nail].values())[3]:
                                tmp4.append(list(json_data[nail].values())[4])
                                key_lst.append(nail)
                else:
                    tmp4.append(list(json_data[nail].values())[4])
                    key_lst.append(nail)
            except:
                pass

        if len(tmp4) > 4:
            random_list = random.sample(range(0, len(tmp4)), 4)      
            for i in random_list:
                    sample_list.append(tmp4[i])
                    sample_key_list.append(key_lst[i])
        
    return sample_list, sample_key_list
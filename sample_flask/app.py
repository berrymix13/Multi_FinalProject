from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import time
import os
import json
import random

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model
from torch import div

from filter import nail_filter, pedi_filter
from weather import current_date_weather
from sandle_rec import pedi_recommend_ones, pedi_recommend_diverse
from weather_rec import weather_nail, weather_pedi
from AdaIN import set_design

from after_Adain import nail_image_make

from nail_model import fit_nail
from foot_model import fit_pedi

app = Flask(__name__)

@app.route("/")
def main():
    weather = current_date_weather()

    return render_template("main.html", weather = weather)

@app.route("/popup")
def popup():
    weather = current_date_weather()

    return render_template("0_popup.html", weather = weather)

@app.route("/weather_rec_nail")
def weather_rec_nail():
    weather = current_date_weather()

    nail_name_list, nail_key_list = weather_nail()

    nail_dict = dict(zip(nail_key_list, nail_name_list))

    return render_template("weather_rec_nail.html", weather = weather,
                                                    nail_dict = nail_dict)

@app.route("/weather_rec_pedi")
def weather_rec_pedi():
    weather = current_date_weather()

    pedi_name_list, pedi_key_list = weather_pedi()

    pedi_dict = dict(zip(pedi_key_list, pedi_name_list))

    return render_template("weather_rec_pedi.html", weather = weather,
                                                    pedi_dict = pedi_dict)

@app.route("/upload_hand", methods = ['POST', 'GET'])
def upload_hand():
    weather = current_date_weather()

    if request.method == 'POST':
        
        file = request.files['file']

        fname = file.filename

        file.save(os.path.join('static/adain/hand/', fname))
        time.sleep(5)
        f_name = os.path.join(fname)

        nail_name_list = request.form.getlist("nail_name_list")
        nail_key_list = request.form.getlist("nail_key_list")
        nail_dict = dict(zip(nail_key_list, nail_name_list))
        

    return render_template("nail_view.html", weather = weather,
                                             f_name = f_name,
                                             nail_dict = nail_dict)

@app.route("/nail_view")
def nail_view():
    weather = current_date_weather()

    return render_template("nail_view.html", weather = weather)

@app.route("/paint_nail/<f_name>/<key>/<nail_dict>", methods = ['GET'])
def paint_nail(f_name, key, nail_dict):
    weather = current_date_weather()

    nail_name_list = []
    nail_key_list = []

    fname = f_name
    n_key = key
    split_list = list(nail_dict.split("'"))

    for i in range(len(list(nail_dict.split("'")))):
        if i % 4 == 1:  
            nail_key_list.append((list(nail_dict.split("'"))[i]))
        if i % 4 == 3:
            nail_name_list.append((list(nail_dict.split("'"))[i]))

    nail_dict = dict(zip(nail_key_list, nail_name_list))

    fit_nail(f_name, f_name, n_key)

    return render_template("paint_nail_view.html", weather = weather,
                                                   f_name = fname,
                                                   nail_dict = nail_dict)

@app.route("/paint_nail_view")
def paint_nail_view():
    weather = current_date_weather()

    return render_template("paint_nail_view.html", weather = weather)


@app.route("/upload_foot", methods = ['POST', 'GET'])
def upload_foot():
    weather = current_date_weather()

    if request.method == 'POST':
        
        file = request.files['file']

        fname = file.filename

        file.save(os.path.join('static/adain/foot/', fname))
        time.sleep(5)
        f_name = os.path.join(fname)

        pedi_name_list = request.form.getlist("pedi_name_list")
        pedi_key_list = request.form.getlist("pedi_key_list")
        pedi_dict = dict(zip(pedi_key_list, pedi_name_list))
        
    return render_template("pedi_view.html", weather = weather,
                                             f_name = f_name,
                                             pedi_dict = pedi_dict)
@app.route("/pedi_view")
def pedi_view():
    weather = current_date_weather()  

    return render_template("pedi_view.html", weather = weather)

@app.route("/paint_pedi/<f_name>/<key>/<pedi_dict>", methods = ['GET'])
def paint_pedi(f_name, key, pedi_dict):
    weather = current_date_weather()

    pedi_name_list = []
    pedi_key_list = []

    fname = f_name
    n_key = key
    split_list = list(pedi_dict.split("'"))

    for i in range(len(list(pedi_dict.split("'")))):
        if i % 4 == 1:  
            pedi_key_list.append((list(pedi_dict.split("'"))[i]))
        if i % 4 == 3:
            pedi_name_list.append((list(pedi_dict.split("'"))[i]))

    pedi_dict = dict(zip(pedi_key_list, pedi_name_list))

    fit_pedi(f_name, f_name, n_key)

    return render_template("paint_pedi_view.html", weather = weather,
                                                   f_name = fname,
                                                   pedi_dict = pedi_dict)

@app.route("/paint_pedi_view")
def paint_pedi_view():
    weather = current_date_weather()

    return render_template("paint_pedi_view.html", weather = weather)

@app.route("/select_nail")
def select_nail():
    weather = current_date_weather()

    color = ['red', 'orange', 'yellow', 'blue', 'green', 'purple', 'pink', 'gold', 'black', 'white', 'beige', 'brown', 'gray', 'silver']
    mood = ['청순', '활발', '시크', '데일리', '화려', '웨딩', '큐티', '시원']
    design = ['풀컬러', '마블', '매트', '시럽', '자개', '그라데이션', '글리터', '프렌치', '시스루', '체크', '패턴', '드로잉']
    weather_list = ['봄', '여름', '가을', '겨울', '눈', '비', '맑음']

    return render_template("select_nail.html", weather = weather,
                                               color_list = color,
                                               mood_list = mood,
                                               design_list = design,
                                               weather_list = weather_list)

@app.route("/select_design_nail", methods = ['GET', 'POST'])
def select_design_nail():
    weather = current_date_weather()

    if request.method == 'POST':
        color = request.form.getlist('color')
        mood = request.form.getlist('mood')
        design = request.form.getlist('design')
        weather_list = request.form.getlist('weather')
    
    with open('static/json/nail_tag.json', 'r', encoding="UTF-8") as f:
        nail_json = json.load(f)

    f_nail_key,nails_title = nail_filter(color, mood, design, weather_list, nail_json)

    f_nail_dict = dict(zip(f_nail_key, nails_title))
    
    return render_template("select_view_nail.html",  weather = weather, 
                                                     f_nail_dict = f_nail_dict)

@app.route("/select_view_nail")
def select_view_nail():
    weather = current_date_weather()

    return render_template("select_view_nail.html", weather = weather)

@app.route("/upload_hand_select", methods = ['POST', 'GET'])
def upload_hand_select():
    weather = current_date_weather()

    if request.method == 'POST':
        
        file = request.files['file']

        fname = file.filename

        file.save(os.path.join('static/adain/hand/', fname))
        time.sleep(5)
        f_name = os.path.join(fname)

        nail_name_list = request.form.getlist("nail_name_list")
        nail_key_list = request.form.getlist("nail_key_list")
        nail_dict = dict(zip(nail_key_list, nail_name_list))
        
    return render_template("select_view_nail_next.html", weather = weather,
                                                         f_name = f_name,
                                                         nail_dict = nail_dict)

@app.route("/select_view_nail_next")
def select_view_nail_next():
    weather = current_date_weather()  

    return render_template("select_view_nail_next.html", weather = weather)

@app.route("/select_view_nail_paint/<f_name>/<key>/<nail_dict>", methods = ['GET'])
def select_view_nail_paint(f_name, key, nail_dict):
    weather = current_date_weather()

    nail_name_list = []
    nail_key_list = []

    fname = f_name
    n_key = key
    split_list = list(nail_dict.split("'"))

    for i in range(len(list(nail_dict.split("'")))):
        if i % 4 == 1:  
            nail_key_list.append((list(nail_dict.split("'"))[i]))
        if i % 4 == 3:
            nail_name_list.append((list(nail_dict.split("'"))[i]))

    nail_dict = dict(zip(nail_key_list, nail_name_list))

    fit_nail(f_name, f_name, n_key)

    return render_template("select_view_nail_final.html", weather = weather,
                                                   f_name = fname,
                                                   nail_dict = nail_dict)

@app.route("/select_view_nail_final")
def select_view_nail_final():
    weather = current_date_weather()

    return render_template("select_view_nail_final.html", weather = weather)

@app.route("/select_pedi")
def select_pedi():  
    weather = current_date_weather()

    color = ['red', 'orange', 'yellow', 'blue', 'green', 'purple', 'pink', 'gold', 'black', 'white', 'beige', 'brown', 'gray', 'silver']
    mood = ['청순', '활발', '시크', '데일리', '화려', '웨딩', '큐티', '시원']
    design = ['풀컬러', '마블', '매트', '시럽', '자개', '그라데이션', '글리터', '프렌치', '시스루', '체크', '패턴', '드로잉']
    weather_list = ['봄', '여름', '가을', '겨울', '눈', '비', '맑음']

    return render_template("select_pedi.html", weather = weather,
                                               color_list = color,
                                               mood_list = mood,
                                               design_list = design,
                                               weather_list = weather_list)

@app.route("/select_design_pedi", methods = ['GET', 'POST'])
def select_design_pedi():
    weather = current_date_weather()

    if request.method == 'POST':
        color = request.form.getlist('color')
        mood = request.form.getlist('mood')
        design = request.form.getlist('design')
        weather_list = request.form.getlist('weather')
    
    with open('static/json/pedi_tag.json', 'r', encoding="UTF-8") as f:
        pedi_json = json.load(f)
    
    f_pedi = ''

    f_pedi_key, pedies_title = pedi_filter(color, mood, design, weather_list, pedi_json)

    f_pedi_dict = dict(zip(f_pedi_key, pedies_title))
    
    return render_template("select_view_pedi.html", weather = weather,
                                                    f_pedi_dict = f_pedi_dict)

@app.route("/select_view_pedi")
def select_view_pedi():
    weather = current_date_weather()

    return render_template("select_view_pedi.html", weather = weather)

@app.route("/upload_foot_select", methods = ['POST', 'GET'])
def upload_foot_select():
    weather = current_date_weather()

    if request.method == 'POST':
        
        file = request.files['file']

        fname = file.filename

        file.save(os.path.join('static/adain/foot/', fname))
        time.sleep(5)
        f_name = os.path.join(fname)

        pedi_name_list = request.form.getlist("pedi_name_list")
        pedi_key_list = request.form.getlist("pedi_key_list")
        pedi_dict = dict(zip(pedi_key_list, pedi_name_list))
        
    return render_template("select_view_pedi_next.html", weather = weather,
                                                         f_name = f_name,
                                                         pedi_dict = pedi_dict)

@app.route("/select_view_pedi_next")
def select_view_pedi_next():
    weather = current_date_weather()  

    return render_template("select_view_pedi_next.html", weather = weather)

@app.route("/select_view_pedi_paint/<f_name>/<key>/<pedi_dict>", methods = ['GET'])
def select_view_pedi_paint(f_name, key, pedi_dict):
    weather = current_date_weather()

    pedi_name_list = []
    pedi_key_list = []

    fname = f_name
    n_key = key
    split_list = list(pedi_dict.split("'"))

    for i in range(len(list(pedi_dict.split("'")))):
        if i % 4 == 1:  
            pedi_key_list.append((list(pedi_dict.split("'"))[i]))
        if i % 4 == 3:
            pedi_name_list.append((list(pedi_dict.split("'"))[i]))

    pedi_dict = dict(zip(pedi_key_list, pedi_name_list))

    fit_pedi(f_name, f_name, n_key)

    return render_template("select_view_pedi_final.html", weather = weather,
                                                   f_name = fname,
                                                   pedi_dict = pedi_dict)

@app.route("/select_view_pedi_final")
def select_view_pedi_final():
    weather = current_date_weather()

    return render_template("select_view_pedi_final.html", weather = weather)

@app.route("/sandle_upload")
def sandle_upload():
    weather = current_date_weather()
    return render_template("sandle_upload.html", weather = weather)

@app.route("/uploader", methods = ['GET', 'POST'])
def uploader():
    weather = current_date_weather()

    file = request.files['file']

    fname = file.filename

    file.save(os.path.join('static/upload/', fname))
    time.sleep(5)
    f_name = os.path.join(fname)

    ones_key_list, ones_name_list = pedi_recommend_ones(f_name)
    diverse_key_list, diverse_name_list = pedi_recommend_diverse(f_name)

    one_dict = dict(zip(ones_key_list, ones_name_list))
    diverse_dict = dict(zip(diverse_key_list, diverse_name_list))

    print(one_dict)
    print(diverse_dict)

    return render_template("sandle_view.html", weather = weather,
                                               f_name = f_name, 
                                               one_dict = one_dict,
                                               diverse_dict = diverse_dict)

@app.route("/sandle_view")
def sandle_view():
    weather = current_date_weather()


    return render_template("sandle_view.html", weather = weather)

@app.route("/upload_foot_sandle", methods = ['POST', 'GET'])
def upload_foot_sandle():
    weather = current_date_weather()

    if request.method == 'POST':
        
        file = request.files['file']

        fname = file.filename

        file.save(os.path.join('static/adain/hand/', fname))
        time.sleep(5)
        f_name = os.path.join(fname)

        sandle_name = request.form.get("sandle_name")
        print(sandle_name)
        f_name = f_name
        
        ones_name_list = request.form.getlist("ones_name_list")
        ones_key_list = request.form.getlist("ones_key_list")
        one_dict = dict(zip(ones_key_list, ones_name_list))

        diverse_name_list = request.form.getlist("diverse_name_list")
        diverse_key_list = request.form.getlist("diverse_key_list")
        diverse_dict = dict(zip(diverse_key_list, diverse_name_list))
        

    return render_template("foot_sandle_view.html", weather = weather,
                                                    f_name = f_name,
                                                    sandle_name = sandle_name,
                                                    one_dict = one_dict,
                                                    diverse_dict = diverse_dict)

@app.route("/foot_sandle_view", methods = ['POST', 'GET'])
def foot_sandle_view():
    weather = current_date_weather()       

    return render_template("foot_sandle_view.html", weather = weather)


@app.route("/foot_sandle_one/<key>/<sandle_name>/<f_name>/<one_dict>/<diverse_dict>", methods = ['GET'])
def foot_sandle_one(key, sandle_name, f_name, one_dict, diverse_dict):
    weather = current_date_weather()     
    
    pedi_name = key
    sandle_name = sandle_name 
    f_name = f_name 

    one_dict_str = one_dict
    diverse_dict_str = diverse_dict

    ones_key_list = []
    ones_name_list = []

    for i in range(len(list(one_dict_str.split("'")))):
        if i % 4 == 1:  
            ones_key_list.append((list(one_dict_str.split("'"))[i]))
        if i % 4 == 3:
            ones_name_list.append((list(one_dict_str.split("'"))[i]))

    one_dict = dict(zip(ones_key_list, ones_name_list))

    diverse_key_list = []
    diverse_name_list = []

    for i in range(len(list(diverse_dict_str.split("'")))):
        if i % 4 == 1:  
            diverse_key_list.append((list(diverse_dict_str.split("'"))[i]))
        if i % 4 == 3:
            diverse_name_list.append((list(diverse_dict_str.split("'"))[i]))

    diverse_dict = dict(zip(diverse_key_list, diverse_name_list))

    fit_pedi(f_name, f_name, pedi_name)

    return render_template("foot_sandle_one_view.html", weather = weather,
                                                        f_name = f_name,
                                                        sandle_name = sandle_name,
                                                        one_dict = one_dict,
                                                        diverse_dict = diverse_dict)

@app.route("/foot_sandle_one_view", methods = ['POST', 'GET'])
def foot_sandle_one_view():
    weather = current_date_weather()       

    return render_template("foot_sandle_one_view.html", weather = weather)

@app.route("/foot_sandle_diverse/<key>/<sandle_name>/<f_name>/<one_dict>/<diverse_dict>", methods = ['GET'])
def foot_sandle_diverse(key, sandle_name, f_name, one_dict, diverse_dict):
    weather = current_date_weather()     
    
    pedi_name = key
    sandle_name = sandle_name 
    f_name = f_name 

    one_dict_str = one_dict
    diverse_dict_str = diverse_dict

    ones_key_list = []
    ones_name_list = []

    for i in range(len(list(one_dict_str.split("'")))):
        if i % 4 == 1:  
            ones_key_list.append((list(one_dict_str.split("'"))[i]))
        if i % 4 == 3:
            ones_name_list.append((list(one_dict_str.split("'"))[i]))

    one_dict = dict(zip(ones_key_list, ones_name_list))

    diverse_key_list = []
    diverse_name_list = []

    for i in range(len(list(diverse_dict_str.split("'")))):
        if i % 4 == 1:  
            diverse_key_list.append((list(diverse_dict_str.split("'"))[i]))
        if i % 4 == 3:
            diverse_name_list.append((list(diverse_dict_str.split("'"))[i]))

    diverse_dict = dict(zip(diverse_key_list, diverse_name_list))

    fit_pedi(f_name, f_name, pedi_name)

    return render_template("foot_sandle_diverse_view.html", weather = weather,
                                                            f_name = f_name,
                                                            sandle_name = sandle_name,
                                                            one_dict = one_dict,
                                                            diverse_dict = diverse_dict)

@app.route("/foot_sandle_diverse_view", methods = ['POST', 'GET'])
def foot_sandle_diverse_view():
    weather = current_date_weather()       

    return render_template("foot_sandle_diverse_view.html", weather = weather)




@app.route("/adain_choose")
def adain_choose():
    weather = current_date_weather()

    shape = ["라운디드", "발레리나", "스퀘어", "스틸레토", "아몬드", "오벌"]
    pattern = ["자개", "마블", "꽃잎", "체크", "패턴"]
    draw = ["동양화", "만화", "서양화", "팝아트"]
    
    oriental_list = os.listdir("static/adain/그림/동양화")
    cartoon_list = os.listdir("static/adain/그림/만화")
    western_list = os.listdir("static/adain/그림/서양화")
    popart_list = os.listdir("static/adain/그림/팝아트")

    return render_template("adain_choose.html", weather = weather,
                                                shape_list = shape,
                                                pattern_list = pattern,
                                                draw_list = draw,
                                                oriental_list = oriental_list,
                                                cartoon_list = cartoon_list,
                                                western_list = western_list,
                                                popart_list = popart_list)


@app.route("/adain_design", methods = ['GET', 'POST'])
def adain_design():
    weather = current_date_weather()

    design = ''
    if request.method == 'POST':
        shape = request.form.get("shape")
        
        pattern = request.form.get("pattern")
        draw = request.form.get("draw")
        

        if request.form.get("oriental"):
            design = request.form.get("oriental")
        elif request.form.get("cartoon"):
            design = request.form.get("cartoon")
        elif request.form.get("western"):
            design = request.form.get("western")
        elif request.form.get("popart"):
            design = request.form.get("popart")
    draw_design = design
    
    fname, user_shape, final_path = set_design(pattern, draw, design, shape)
    # fname(만들어진 이미지), user_shape(쉐입), desgin(그림이름)
    
    return render_template("adain_making.html", weather = weather,
                                                making = fname,
                                                user_shape = user_shape,
                                                draw_design = draw_design,
                                                final_path = final_path)

@app.route("/adain_making", methods = ['GET', 'POST'])
def adain_making():
    weather = current_date_weather()

    if request.method == 'POST':

        file = request.files['file']

        fname = file.filename

        file.save(os.path.join('static/adain/hand/', fname))
        time.sleep(5)
        f_name = os.path.join(fname)

        making = request.form.get("making")
        shape = request.form.get("shape")
        draw_design = request.form.get("draw_design")
        final_path = request.form.get("final_path")
        print(draw_design)
        print(final_path)

    
    file_name = nail_image_make(f_name, making, shape)

    return render_template("adain_show.html", weather = weather,
                                              final_path = final_path,
                                              draw_design = draw_design,
                                              making = making,
                                              file_name = file_name)


@app.route("/adain_show")
def adain_show():
    weather = current_date_weather()

    return render_template("adain_show.html", weather = weather)

@app.route("/celeb_nail")
def celeb_nail():
    weather = current_date_weather()

    return render_template("celeb_nail.html", weather = weather)

@app.route("/celeb_select_nail/<celeb>/<nail>", methods = ['GET'])
def celeb_select_nail(celeb, nail):
    weather = current_date_weather()

    celeb_image = celeb
    nail_image = nail

    return render_template("celeb_select_view.html", weather = weather,
                                                     celeb = celeb_image,
                                                     nail = nail_image)

@app.route("/celeb_select_view")
def celeb_select_view():
    weather = current_date_weather()

    return render_template("celeb_select_view.html", weather = weather)

@app.route("/celeb_making", methods = ["POST", "GET"])
def celeb_making():
    weather = current_date_weather()

    if request.method == 'POST':
        
        file = request.files['file']

        fname = file.filename

        file.save(os.path.join('static/adain/hand/', fname))
        time.sleep(5)
        f_name = os.path.join(fname)

        celeb = request.form.get("celeb")
        nail = request.form.get("nail")

    
    fit_nail(f_name, f_name, nail)

    return render_template("celeb_making.html", weather = weather,
                                                celeb = celeb,
                                                nail = nail)



@app.route("/0_zero")
def zero():
    weather = current_date_weather()

    return render_template("0_zero.html", weather = weather)

if __name__ == "__main__":
    app.run(port='5001', debug=True)


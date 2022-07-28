import numpy as np
import os
import json
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential, load_model

import copy
from tqdm import tqdm
import pandas as pd

with open('static/json/pedi_tag.json', 'r', encoding="UTF-8") as f:
        pedi_data = json.load(f)
    
with open('static/json/color_set.json', 'r', encoding="UTF-8") as f:
        color_data = json.load(f)


def pedi_ones(ncolor):
    color = ['red', 'orange', 'yellow', 'blue', 'green', 'purple', 'pink', 'gold', 'black', 'white', 'beige', 'brown', 'gray', 'silver']
    
    #### 색조합  외의 색 리스트 생성
    ncolor = color_data['color_set'][0][ncolor]
    ncolor = list(set(color) - set(ncolor))

    #### 목록 색 외의 페디 검출
    f_pedi = []; tmp1 = []; tmp2 = []
    for pedi in pedi_data:
        f_pedi.append(pedi)
        for nc in ncolor:
            if nc in list(pedi_data[pedi].values())[0]:
                tmp1.append(pedi)
    # tmp1 중복 제거: tmp2
    for pedi in tmp1:
        if pedi not in tmp2:
            tmp2.append(pedi)
    # 최종 페디 리스트: f_nail
    f_pedi = list(set(f_pedi) - set(tmp2))

    pedies_title=[]
    for pedi in f_pedi:
        pedies_title.append(list(pedi_data[pedi].values())[4]) 

    sample_list = []
    sample_key_list = []

    if len(f_pedi) > 4:
        random_list = random.sample(range(0, len(f_pedi)), 4)      
        for i in random_list:
                sample_key_list.append(f_pedi[i])
                sample_list.append(pedies_title[i])      

    return sample_key_list, sample_list

def pedi_diverse(ncolor):
    color = ['red', 'orange', 'yellow', 'blue', 'green', 'purple', 'pink', 'gold', 'black', 'white', 'beige', 'brown', 'gray', 'silver']

    # 색조합 내의 색을 가진 페디들
    ncolor_1 = color_data['color_set'][0][ncolor]; tmp1=[]  
    for nail in pedi_data:
        for nc in ncolor_1:
            if nc in list(pedi_data[nail].values())[0]:
                #if len(list(b_dict[nail].values())[0]) > 2:
                    tmp1.append(nail)

    #### 색조합  외의 색 리스트 생성
    ncolor_2 = color_data['color_set'][0][ncolor]
    ncolor_2 = list(set(color) - set(ncolor_2))

    tot=[];tmp2=[];tmp3=[];tmp4=[]
    # 목록 색 외의 페디 검출
    for pedi in pedi_data:
        tot.append(pedi)
        for nc in ncolor_2:
            if nc in list(pedi_data[pedi].values())[0]:
                tmp3.append(pedi)
    # 중복 제거         
    for pedi in tmp3:
        if pedi not in tmp4:
            tmp4.append(pedi)
    # 통일성 친구들
    tmp2 = list(set(tot) - set(tmp4))

    # 다양성 - 통일성(tmp1-tmp2)
    f_pedi=[]
    f_pedi = list(set(tmp1) - set(tmp2))

    ################################## 네일 이름: nails_title #######################################
    pedies_title=[]
    for pedi in f_pedi:
        pedies_title.append(list(pedi_data[pedi].values())[4])
                
    sample_list = []
    sample_key_list = []

    if len(f_pedi) > 4:
        random_list = random.sample(range(0, len(f_pedi)), 4)      
        for i in random_list:
                sample_key_list.append(f_pedi[i])
                sample_list.append(pedies_title[i])      

    return sample_key_list, sample_list

def pedi_recommend_ones(f_name):
    model = load_model('static/model/sandle_color.h5')  

    img_height = 128
    img_width = 128 
    class_names = ['beige', 'black', 'blue', 'brown', 'green', 'pink', 'red', 'white', 'yellow']

    img = keras.preprocessing.image.load_img(
    'static/upload/' + f_name, target_size=(img_height, img_width))

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) 

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    sandle_color = class_names[np.argmax(score)]

    print(sandle_color)
    
    pedies_key_list , pedies_name_list = pedi_ones(sandle_color)

    return pedies_key_list , pedies_name_list

def pedi_recommend_diverse(f_name):
    model = load_model('static/model/sandle_color.h5')  

    img_height = 128
    img_width = 128 
    class_names = ['beige', 'black', 'blue', 'brown', 'green', 'pink', 'red', 'white', 'yellow']

    img = keras.preprocessing.image.load_img(
    'static/upload/' + f_name, target_size=(img_height, img_width))

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) 

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    sandle_color = class_names[np.argmax(score)]

    print(sandle_color)
    
    pedies_key_list , pedies_name_list = pedi_diverse(sandle_color)

    return pedies_key_list , pedies_name_list
import glob as gb
import json
import copy
import numpy as np
from tqdm import tqdm
import pandas as pd
import os
import random

color = ['red', 'orange', 'yellow', 'blue', 'green', 'purple', 'pink', 'gold', 'black', 'white', 'beige', 'brown', 'gray', 'silver']
mood = ['청순', '활발', '시크', '데일리', '화려', '웨딩', '큐티', '시원']
design = ['풀컬러', '마블', '매트', '시럽', '자개', '그라데이션', '글리터', '프렌치', '시스루', '체크', '패턴', '드로잉', '별자리']
weather = ['봄', '여름', '가을', '겨울', '눈', '비', '맑음']

def nail_filter(ncolor,nmood,ndesign,nweather,a_dict):
    tmp1=[];tmp2=[];tmp3=[];tmp4=[]
    
    if ncolor == []:
        ncolor.append("")
    if nmood == []:
        nmood.append("")
    if ndesign == []:
        ndesign.append("")
    if nweather == []:
        nweather.append("")

    for nail in a_dict:
    # 색
        try:
            if ncolor[0] in color:
                for nc in ncolor:
                    if nc in color:
                        if nc in a_dict[nail]['색상']:
                            tmp1.append(nail)
            else:tmp1.append(nail)
        except:
            pass

    # 무드
        try:
            if nmood[0] in mood:
                for nm in nmood:
                    if nm in mood:
                        if nm in a_dict[nail]['분위기']:
                            tmp2.append(nail)
            else: tmp2.append(nail)
        except:
            pass
    # 디자인
        try:
            if ndesign[0] in design:
                for nd in ndesign:
                    if nd in design:
                        if nd in a_dict[nail]['디자인']:
                            tmp3.append(nail)
            else: tmp3.append(nail)
        except:
            pass
    # 날씨
        try:
            if nweather[0] in weather:
                for nd in nweather:
                    if nd in weather:
                        if nd in a_dict[nail]['날씨']:
                            tmp4.append(nail)
            else:tmp4.append(nail)
        except:
            pass

  # 모든 조건이 겹치는 네일(f_nail) 찾기
    new_a = list(set(tmp1).intersection(set(tmp2)))
    new_b = list(set(tmp3).intersection(set(tmp4)))
    f_nail = list(set(new_a).intersection(set(new_b)))

    ################################## 네일 이름: nails_title #######################################
    nails_title=[]
    for nail in f_nail:
        nails_title.append(list(a_dict[nail].values())[4])

    sample_list = []
    sample_key_list = []

    if len(f_nail) > 4:
        random_list = random.sample(range(0, len(f_nail)), 4)      
        for i in random_list:
                sample_key_list.append(f_nail[i])
                sample_list.append(nails_title[i])      

    return sample_key_list, sample_list



def pedi_filter(ncolor,nmood,ndesign,nweather,a_dict):
    tmp1=[];tmp2=[];tmp3=[];tmp4=[]
    
    if ncolor == []:
        ncolor.append("")
    if nmood == []:
        nmood.append("")
    if ndesign == []:
        ndesign.append("")
    if nweather == []:
        nweather.append("")

    for nail in a_dict:
    # 색
        try:
            if ncolor[0] in color:
                for nc in ncolor:
                    if nc in color:
                        if nc in a_dict[nail]['색상']:
                            tmp1.append(nail)
            else:tmp1.append(nail)
        except:
            pass

    # 무드
        try:
            if nmood[0] in mood:
                for nm in nmood:
                    if nm in mood:
                        if nm in a_dict[nail]['분위기']:
                            tmp2.append(nail)
            else: tmp2.append(nail)
        except:
            pass
    # 디자인
        try:
            if ndesign[0] in design:
                for nd in ndesign:
                    if nd in design:
                        if nd in a_dict[nail]['디자인']:
                            tmp3.append(nail)
            else: tmp3.append(nail)
        except:
            pass
    # 날씨
        try:
            if nweather[0] in weather:
                for nd in nweather:
                    if nd in weather:
                        if nd in a_dict[nail]['날씨']:
                            tmp4.append(nail)
            else:tmp4.append(nail)
        except:
            pass

  # 모든 조건이 겹치는 네일(f_nail) 찾기
    new_a = list(set(tmp1).intersection(set(tmp2)))
    new_b = list(set(tmp3).intersection(set(tmp4)))
    f_nail = list(set(new_a).intersection(set(new_b)))

    ################################## 네일 이름: nails_title #######################################
    nails_title=[]
    for nail in f_nail:
        nails_title.append(list(a_dict[nail].values())[4])

    sample_list = []
    sample_key_list = []

    if len(f_nail) > 4:
        random_list = random.sample(range(0, len(f_nail)), 4)      
        for i in random_list:
                sample_key_list.append(f_nail[i])
                sample_list.append(nails_title[i])      

    return sample_key_list, sample_list



    
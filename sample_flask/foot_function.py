import cv2, warnings
import matplotlib.pyplot as plt
import numpy as np


def bgrrgb(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)


def brightness(design, foot):
    foot_resize = cv2.resize(foot, (design.shape[1], design.shape[0]))
    val = (design.mean() - foot_resize.mean()) * 0.2
    arr = np.full(design.shape, val, dtype=np.uint8)
    if arr[0][0][0] >= 200:
        arr = np.full(design.shape, 256 - val, dtype=np.uint8)
    if (design.mean() - foot_resize.mean()) < 0:
        design = cv2.subtract(design, arr)

    return design



def Contours(img):
    mask =img.copy()
    b,g,r = cv2.split(mask)
    merged_img = cv2.merge([r,g,b])
    edge = cv2.dilate(merged_img, None)
    blur = cv2.GaussianBlur(merged_img, ksize = (3, 3), sigmaX = 0)
    edged = cv2.Canny(blur, 200, 255)       # 경계선 따기
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    Contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return Contours


def pts_box(img):
    '''
    이미지 입력하면 좌표를 빼내주는 함수
    순서대로 아래, 왼쪽, 오른쪽의 좌표값을 리턴한다
    
    '''
    # 이미지 좌표 추출
    img_color = img
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    ret, img_binary = cv2.threshold(img_gray, 100, 255, 0)
    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    lst = []
    for cnt in contours:
        for i in range(len(cnt)):
            lst.append(cnt[i][0])

    left_point = [9999,9999]
    right_point = [0,0]
    num = 0
    top_point = [9999,9999]
    low_point = [0,0]
    while True:
        
        for i in lst:
            # y값 중간 지점에서 출발
            if top_point[1] > i[1]:
                top_point = i
            if low_point[1] < i[1]:
                low_point = i
            if left_point[0] > i[0]:
                left_point = i
            if right_point[0] < i[0]:
                right_point = i
        if len(left_point) == 0 or len(top_point) == 0 or len(low_point) == 0 or len(right_point) == 0:
            num += 1
        else:
            break
    return top_point, left_point, right_point, low_point



def rot_crop_box3(img, tag='foot'):   # 이미지 먼저 불러오고 사용하기
  global crop_img, img_box, angle_lst ,angle_lst2, cenetr_lst, side_x_lst, side_y_lst, box_lst

#   img = cv2.imread(img_path)
  
  mult = 1  # 자르는 이미지 비율, 1: 딱 맞게 자르기
  # img_box = cv2.cvtColor(img5.copy(), cv2.COLOR_GRAY2BGR)
  img_box = img.copy()
  
  edge = cv2.dilate(img_box, None)
  blur = cv2.GaussianBlur(edge, ksize = (3, 3), sigmaX = 0)
  edged = cv2.Canny(blur, 200, 255)       # 경계선 따기
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
  closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel) 
  contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     

  crop_img, angle_lst = [], []     # 자른 이미지 담을 리스트 , 변환 전 좌표 
  angle_lst2, cenetr_lst = [], []  # 변환 후 좌표, 각 객체 중심 좌표
  box_lst = []
  for i, cnt in enumerate(contours):
      rect = cv2.minAreaRect(cnt)
      box = cv2.boxPoints(rect)
      box = np.int0(box)
      box_lst.append(box)

      W, H = rect[1][0], rect[1][1]

      Xs = [i[0] for i in box]
      Ys = [i[1] for i in box]
      x1, x2, y1, y2 = min(Xs), max(Xs), min(Ys), max(Ys)

      angle = rect[2]
      angle_lst.append(angle) # 확인용 - 원래 각도 확인 

      if tag == 'foot':
          if W > H:
              angle = (angle)
          else:                                    # 높이가 너비보다 작으면
              angle = (angle)  +90             # 90-angle 만큼 시계방향 회전
              # print(f' BB // index num :{i}, {angle}') # 확인용
      else:
          if W > H:
            angle = angle+90


      # if angle <0: # 혹시 몰라서 남겨둠! 불필요하면 제거하기
      #     if W < H:
      #       angle = (-90-angle)
      #
      angle_lst2.append(angle) # 확인용 - 변형 후 각도 확인
            
      center, size  = (int((x1+x2)/2), int((y1+y2)/2)), (int(mult*(x2-x1)),int(mult*(y2-y1)))
      cenetr_lst.append(center) # 확인용 - 중심좌표

      M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0) # angle 만큼 반시계방향 회전
      
      cropped = cv2.getRectSubPix(img_box, size, center)
      cropped = cv2.warpAffine(cropped, M, size)
      
      croppedW = W # if W < H else H
      croppedH = H # if W < H else W

      croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW * mult), int(croppedH * mult)), (size[0]/2, size[1]/2))
      crop_img.append(croppedRotated)

  return crop_img



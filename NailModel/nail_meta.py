import cv2, math, warnings
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
warnings.filterwarnings('ignore')

def find_point(image):    
    max_num_hands = 1

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    drawing_spec = mp_drawing.DrawingSpec(thickness=50, circle_radius=20)

    hands = mp_hands.Hands(
        max_num_hands=max_num_hands,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    img_copy = image.copy()
    result = hands.process(img_copy)

    if result.multi_hand_landmarks is not None:
        index = 1 - result.multi_handedness[0].classification[0].index
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            if len(joint) == 21:
                h, w, c = img_copy.shape
                point = joint * [w, h, c]

                # 관절의 각도를 계산하기 위한 vector
                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19],:] # Parent joint
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:] # Child joint
                v = v2 - v1 # [20,3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                angle = np.arccos(np.einsum('nt,nt->n',
                        v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                        v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,] 

                angle = np.degrees(angle) # Convert radian to degree

                # Inference gesture
                data = np.array([angle], dtype=np.float32)
        
                # mp_drawing.draw_landmarks(img_copy, res, mp_hands.HAND_CONNECTIONS, 
                #                         mp_drawing.DrawingSpec(color=(112, 146, 190), thickness=20, circle_radius=10), 
                #                         mp_drawing.DrawingSpec(color=(153, 217, 234), thickness=20, circle_radius=10))
                return img_copy, point, index
            
            else:
                print('손을 가운데에 위치시켜주세요.')
    
    else:
        print('손을 가운데에 위치시켜주세요.')
# 163,73,164 / 200,191,231


# 각 손가락의 각도에 맞게 1자로 세우는 함수
def rotation_finger(img, point):
    # plt.figure(figsize=(15, 6))
    for num, idx in enumerate(range(4,21,4)):
        A = point[idx]; B = point[idx-1]; D = point[idx-3]

        globals()['center{}'.format(num)] = ((A[0]+B[0])/2, (A[1]+B[1])/2)             # 중심 좌표 계산
        globals()['dist{}'.format(num)] = ((A[1]-B[1])**2 + (A[0]-B[0])**2)**(1/2)     # 피타고라스 정리
        if num == 0 :
            globals()['rad{}'.format(num)] = math.atan2(A[1] - B[1],A[0] - B[0] )
        else:
            globals()['rad{}'.format(num)] = math.atan2(A[1] - D[1],A[0] - D[0] )

        globals()['degree{}'.format(num)] = 90+(globals()['rad{}'.format(num)] *180)/ math.pi

        # 이미지 회전
        img_copy = img.copy()
        matrix = cv2.getRotationMatrix2D(globals()['center{}'.format(num)], globals()['degree{}'.format(num)], scale=1)
        globals()['hand{}'.format(num)] = cv2.warpAffine(img_copy, matrix, (img_copy.shape[1], img_copy.shape[0]))
        # plt.subplot(2, 5, num+1);
        # plt.axis('off')
        # plt.imshow(globals()['hand{}'.format(num)])       

        globals()['pt{}_x1'.format(num)] = int(globals()['center{}'.format(num)][0] - globals()['dist{}'.format(num)]*0.7)
        globals()['pt{}_y1'.format(num)] = int(globals()['center{}'.format(num)][1] - globals()['dist{}'.format(num)]*1.5)
        globals()['pt{}_x2'.format(num)] = int(globals()['center{}'.format(num)][0] + globals()['dist{}'.format(num)]*0.7)
        globals()['pt{}_y2'.format(num)] = int(globals()['center{}'.format(num)][1] + globals()['dist{}'.format(num)]*0.8)
        
        if globals()['pt{}_x1'.format(num)] < 0 :
            globals()['pt{}_x1'.format(num)] = 0
        if globals()['pt{}_x2'.format(num)] > img.shape[1]:
            globals()['pt{}_x2'.format(num)] = img.shape[1]

        # print(globals()['pt{}_y1'.format(num)], globals()['pt{}_y2'.format(num)], globals()['pt{}_x1'.format(num)], globals()['pt{}_x2'.format(num)])

        globals()['img{}'.format(num)] = globals()['hand{}'.format(num)][globals()['pt{}_y1'.format(num)]:globals()['pt{}_y2'.format(num)], 
                                                    globals()['pt{}_x1'.format(num)]:globals()['pt{}_x2'.format(num)]]             # [y범위, x범위]

        # print(globals()['img{}'.format(num)].shape)

        # plt.subplot(2, 5, 5+num+1)
        # plt.axis('off')
        # plt.imshow(globals()['img{}'.format(num)]);
        
        
# 마스크 이미지를 원본 이미지의 좌표에 맞춰 회전, 자르기
def rotation_mask(mask, point):
    # plt.figure(figsize=(15, 6))
    for num, idx in enumerate(range(4,21,4)):
        A = point[idx]; B = point[idx-1]; D = point[idx-3]

        globals()['center{}'.format(num)] = ((A[0]+B[0])/2, (A[1]+B[1])/2)             # 중심 좌표 계산
        globals()['dist{}'.format(num)] = ((A[1]-B[1])**2 + (A[0]-B[0])**2)**(1/2)     # 피타고라스 정리
        if num == 0 :
            globals()['rad{}'.format(num)] = math.atan2(A[1] - B[1],A[0] - B[0] )
        else:
            globals()['rad{}'.format(num)] = math.atan2(A[1] - D[1],A[0] - D[0] )

        globals()['degree{}'.format(num)] = 90+(globals()['rad{}'.format(num)] *180)/ math.pi
        
        # 이미지 회전
        mask_copy = mask.copy()
        matrix = cv2.getRotationMatrix2D(globals()['center{}'.format(num)], globals()['degree{}'.format(num)], scale=1)
        mask_copy = cv2.warpAffine(mask_copy,matrix, (mask_copy.shape[1], mask_copy.shape[0]))
        # plt.subplot(2, 5, num+1);
        # plt.axis('off')
        # plt.imshow(mask_copy);

        globals()['pt{}_x1'.format(num)] = int(globals()['center{}'.format(num)][0] - globals()['dist{}'.format(num)]*0.7)
        globals()['pt{}_y1'.format(num)] = int(globals()['center{}'.format(num)][1] - globals()['dist{}'.format(num)]*1.5)
        globals()['pt{}_x2'.format(num)] = int(globals()['center{}'.format(num)][0] + globals()['dist{}'.format(num)]*0.7)
        globals()['pt{}_y2'.format(num)] = int(globals()['center{}'.format(num)][1] + globals()['dist{}'.format(num)]*0.8)
        
        if globals()['pt{}_x1'.format(num)] < 0 :
            globals()['pt{}_x1'.format(num)] = 0
        if globals()['pt{}_x2'.format(num)] > mask.shape[1]:
            globals()['pt{}_x2'.format(num)] = mask.shape[1]

        globals()['mask{}'.format(num)] = mask_copy[globals()['pt{}_y1'.format(num)]:globals()['pt{}_y2'.format(num)], 
                                                    globals()['pt{}_x1'.format(num)]:globals()['pt{}_x2'.format(num)]]             # [y범위, x범위]

        div5 = int(globals()['mask{}'.format(num)].shape[1]//5)                           # 마스크의 x축 길이를 5로 나눈 값
        # 손톱 이외의 영역 지우기
        for row in globals()['mask{}'.format(num)]:
            row[:div5] = 0
            row[div5*4:] = 0

        # plt.subplot(2, 5, 5+num+1)
        # plt.axis('off')
        # plt.imshow(globals()['mask{}'.format(num)]);
    return mask0, mask1, mask2, mask3, mask4


def rot_crop_box(img):  
  global crop_img, img_box, angle_lst ,angle_lst2, cenetr_lst
  '''
  마스크 이미지를 넣으면 손톱 5개 마스크가 들어있는 `0-4 리스트` 리턴
  '''


  mult = 1.5  # 자르는 이미지 비율, 1: 딱 맞게 자르기
  # img_box = cv2.cvtColor(img5.copy(), cv2.COLOR_GRAY2BGR)
  img_box = img.copy()
  crop_list = []

  edge = cv2.dilate(img_box, None)
  blur = cv2.GaussianBlur(edge, ksize = (3, 3), sigmaX = 0)
  edged = cv2.Canny(blur, 200, 255)       # 경계선 따기
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
  closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel) 
  contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)      

  crop_img, angle_lst = [], []    # 자른 이미지 담을 리스트 , 변환 전 좌표 
  angle_lst2, cenetr_lst = [], []  # 변환 후 좌표, 각 객체 중심 좌표
  for i, cnt in enumerate(contours):
      rect = cv2.minAreaRect(cnt) 
      box = cv2.boxPoints(rect)
      box = np.int0(box)
      # cv2.drawContours(img_box, [box], 0, (0,255,0), 2) # 박스 그리기

      W = rect[1][0] 
      H = rect[1][1]

      Xs = [i[0] for i in box]
      Ys = [i[1] for i in box]
      x1 = min(Xs)
      x2 = max(Xs)
      y1 = min(Ys)
      y2 = max(Ys)

      angle = rect[2] # 각도
      angle_lst.append(angle)

      if angle == 90: # 90도이면 0도로 변경 
          angle-=90
          rotated = True
      else:
        rotated = False
        
      angle_lst2.append(angle)

      center = (int((x1+x2)/2), int((y1+y2)/2))
      size = (int(mult*(x2-x1)),int(mult*(y2-y1)))
      # cv2.circle(img_box, center, 10, (0,255,0), -1) # 가운데 점 그리기
      cenetr_lst.append(center)
      
      M = cv2.getRotationMatrix2D((size[0]/2, size[1]/2), angle, 1.0)

      cropped = cv2.getRectSubPix(img_box, size, center)    
      cropped = cv2.warpAffine(cropped, M, size)

      croppedW = W if not rotated else H 
      croppedH = H if not rotated else W

      croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW*mult), int(croppedH*mult)), (size[0]/2, size[1]/2)) 
      crop_list.append(croppedRotated)
  return crop_list


def nail_pts(img):
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

    left_point = []
    right_point = []
    num = 0
    low_point = [0,0]
    while True:
        
        for i in lst:
            # y값 중간 지점에서 출발
            if i[1] ==  int(img_color.shape[0]/2)+num:
                # x 값의 중간지점보다 작으면 왼쪽
                if i[0] < int(img_color.shape[1]/2):
                    left_point.append(i)
                else:
                    right_point.append(i)
            if low_point[1] < i[1]:
                low_point = i
        if len(left_point) == 0 or len(right_point) == 0:
            num -= 1
        else:
            break
    return low_point, left_point[0], right_point[0]




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
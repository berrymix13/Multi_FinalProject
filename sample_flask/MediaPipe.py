import cv2, sys, warnings, math
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
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
                v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]  # Parent joint
                v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]  # Child joint
                v = v2 - v1  # [20,3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                angle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

                angle = np.degrees(angle)  # Convert radian to degree

                # Inference gesture
                data = np.array([angle], dtype=np.float32)

                mp_drawing.draw_landmarks(img_copy, res, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(112, 146, 190), thickness=20, circle_radius=10),
                                          mp_drawing.DrawingSpec(color=(153, 217, 234), thickness=20, circle_radius=10))
                return img_copy, point, index

            else:
                print('손을 가운데에 위치시켜주세요.')

    else:
        print('손을 가운데에 위치시켜주세요.')

def degree_finger(point):
    lst = []
    for num, idx in enumerate(range(4,21,4)):
        A = point[idx]; B = point[idx-1]; D = point[idx-3]
        if num == 0:
            rad = math.atan2(A[1] - B[1],A[0] - B[0] )
        else:
            rad = math.atan2(A[1] - D[1],A[0] - D[0] )

        degree = 90 +((rad *180)/ math.pi)
        lst.append([num, degree])

    return lst


# 각 손가락의 각도에 맞게 1자로 세우는 함수
def rotation_finger(son_mask, point):
    center_lst = []; dist_lst = []; degree_lst = []
    pt_x_lst = []; pt_y_lst = []; mask_lst = []

    for num, idx in enumerate(range(4, 21, 4)):
        A = point[idx];
        B = point[idx - 1];
        D = point[idx - 3]

        center = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)  # 중심 좌표 계산
        center_lst.append(center)

        dist = ((A[1] - B[1]) ** 2 + (A[0] - B[0]) ** 2) ** (1 / 2)  # 피타고라스 정리
        dist_lst.append(dist)
        rad = math.atan2(A[1] - B[1], A[0] - B[0])
        # if num == 0:
        #     rad = math.atan2(A[1] - B[1], A[0] - B[0])
        # else:
        #     rad = math.atan2(A[1] - D[1], A[0] - D[0])

        degree = 90 + (rad * 180) / math.pi

        # 이미지 회전
        son_mask_copy = son_mask.copy()
        matrix = cv2.getRotationMatrix2D(center, degree, scale=1)
        degree_lst.append(degree)

        hand = cv2.warpAffine(son_mask_copy, matrix, (son_mask_copy.shape[1], son_mask_copy.shape[0]))

        pt_x1 = int(center[0] - dist * 0.7)
        pt_y1 = int(center[1] - dist * 1.5)
        pt_x2 = int(center[0] + dist * 0.7)
        pt_y2 = int(center[1] + dist * 0.8)

        if pt_x1 < 0:
            pt_x1 = 0
        if pt_x2 > son_mask.shape[1]:
            pt_x2 = son_mask.shape[1]

        pt_x_lst.append((pt_x1, pt_x2))
        pt_y_lst.append((pt_y1, pt_y2))

        # print(pt_y1, pt_y2, pt_x1,pt_x2)

        img = hand[pt_y1:pt_y2, pt_x1:pt_x2]  # [y범위, x범위]
        div5 = int(img.shape[1] // 5)
        # 손톱 이외의 영역 지우기
        for row in img:
            row[:div5] = 0
            row[div5*4:] = 0

        mask_lst.append(img)

    return center_lst , dist_lst , degree_lst , pt_x_lst , pt_y_lst , mask_lst
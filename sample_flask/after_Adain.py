import cv2, warnings
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

import albumentations
from albumentations.pytorch import ToTensorV2
from typing import List
import torch
import numpy as np
import albumentations as A
import torchvision.transforms as T
import segmentation_models_pytorch as smp
import os
import torchvision.transforms.functional as F
from torch.utils.data import Dataset, DataLoader
from matplotlib import colors, pyplot as plt
from PIL import Image
import warnings
warnings.filterwarnings("ignore")
from skimage.filters import threshold_otsu
from torchvision.utils import draw_segmentation_masks
from tqdm import tqdm

  # mask_segmentation 모델 불러옴
from MediaPipe import find_point, degree_finger

##############################################################################
############################ 모델 선언부 #####################################
# 으어어어어

best_model = torch.load('static/model/nail_foot_seg_best_model.pth', map_location=torch.device('cpu'))

class test_NailsDataset(torch.utils.data.Dataset):
    def __init__(self, images: List[str], transform):
        self._images = images
        # self._masks = masks
        self._transform = transform
        # assert len(images) == len(masks)

    def __len__(self):
        return len(self._images)

    def __getitem__(self, index):
        image = Image.open(self._images[index])
        augmented = self._transform(image=np.array(image))
        image = augmented['image']
        return image

def test_dataset(test_image, img_name):
    test_dataset = test_NailsDataset(
        images=test_image,
        transform=A.Compose([
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            A.Resize(height=224, width=224),  # 사이즈 변경하면 오류
            A.Sharpen(p=0.5),
            ToTensorV2(transpose_mask=True),
        ]),
    )
  
    test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False)
   
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   
    iou_score, iou_score2, mean_acc, otsu = 0, 0, 0, 0
    for i, imgs in tqdm(enumerate(test_dataloader)):
        for img in imgs:
            img = torch.unsqueeze(img, 0)  # torch.unsqueeze(): 1차원 제거 함수
            pred = best_model((img).to(device))[0][0].cpu().detach().numpy() > 0.47
            
            # 시각화
            fig, axes = plt.subplots(1, 2)
            axes[0].imshow(pred)
            axes[0].set_title("Predicted mask")
            
            img_o = ((img).to(device))[0][0].cpu().detach().numpy()
            axes[1].imshow(img_o)
            axes[1].set_title("Target image")
            
            fig.set_figwidth(12)
            fig.set_figheight(6)
            
            # 마스크 이미지 저장
            plt.imsave(f'static/adain/hand_mask/model_mask_v2_{img_name}', pred, cmap='gray')  # 경로 변경

##############################################################################
############################ 함수 정의부 #####################################

def rot_crop_box3(img):  # 이미지 먼저 불러오고 사용하기
    global crop_img, img_box, angle_lst, angle_lst2, cenetr_lst, side_x_lst, side_y_lst, box_lst

    #   img = cv2.imread(img_path)

    mult = 1  # 자르는 이미지 비율, 1: 딱 맞게 자르기
    # img_box = cv2.cvtColor(img5.copy(), cv2.COLOR_GRAY2BGR)
    img_box = img.copy()

    edge = cv2.dilate(img_box, None)
    blur = cv2.GaussianBlur(edge, ksize=(3, 3), sigmaX=0)
    edged = cv2.Canny(blur, 200, 255)  # 경계선 따기
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    crop_img, angle_lst = [], []  # 자른 이미지 담을 리스트 , 변환 전 좌표
    angle_lst2, cenetr_lst = [], []  # 변환 후 좌표, 각 객체 중심 좌표
    side_x_lst, side_y_lst = [], []  # x1-x2, y1-y2
    box_lst = []

    for i, cnt in enumerate(contours):
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img_box, [box], 0, (0, 255, 0), 2)  # 박스 그리기|

        W, H = rect[1][0], rect[1][1]

        # if W <= 20 or H <= 20:
        #     continue

        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1, x2, y1, y2 = min(Xs), max(Xs), min(Ys), max(Ys)

        if x1 < 0:
            x1 = 0
        elif x2 > img_box.shape[1]:
            x2 = img_box.shape[1]
        elif y1 < 0:
            y1 = 0
        elif y2 > img_box.shape[0]:
            y2 = img_box.shape[0]

        side_x_lst.append((x1, x2))
        side_y_lst.append((y1, y2))

        angle = rect[2]
        angle_lst.append(angle)  # 확인용 - 원래 각도 확인

        if angle > 0:
            if W < H:  # 너비가 높이보다 작으면
                angle = angle  # 원래 각도만큼 반시계방향 회전
            else:  # 높이가 너비보다 작으면
                angle = -(90 - angle)  # 90-angle 만큼 시계방향 회전

        angle_lst2.append(angle)  # 확인용 - 변형 후 각도 확인

        center, size = (int((x1 + x2) / 2), int((y1 + y2) / 2)), (int(mult * (x2 - x1)), int(mult * (y2 - y1)))
        cv2.circle(img_box, center, 1, (0, 255, 0), -1)  # 가운데 점 그리기'
        cenetr_lst.append(center)  # 확인용 - 중심좌표

        M = cv2.getRotationMatrix2D((size[0] / 2, size[1] / 2), angle, 1.0)  # angle 만큼 반시계방향 회전

        cropped = cv2.getRectSubPix(img_box, size, center)
        cropped = cv2.warpAffine(cropped, M, size)

        croppedW = W if W < H else H
        croppedH = H if W < H else W

        croppedRotated = cv2.getRectSubPix(cropped, (int(croppedW * mult), int(croppedH * mult)),
                                           (size[0] / 2, size[1] / 2))
        crop_img.append(croppedRotated)

# 손톱 디자인 합성 함수
def add_nail(design_bt, image, crop_img, degree_lst, side_x_lst, side_y_lst, index, texture_name):
    texture = cv2.imread(f'static/adain/texture/{texture_name}.jpg')

    result = image.copy()
    if index == 0:
        # aa = degree_lst[-1]
        # degree_lst[-1] = degree_lst[0]
        # degree_lst[0] = aa
        degree_lst = degree_lst[::-1]

    # if len(side_x_lst) > 5:
    #     side_x_lst = side_x_lst[:5]
    #     side_y_lst = side_y_lst[:5]

    try:
        # 기존 v5 부분
        # degree_lst2 = [0 for _ in range(len(degree_lst))]
        # for idx1, val2 in enumerate(sorted(side_x_lst)):
        #     idx2 = side_x_lst.index(val2)
        #     degree_lst2[idx2] = degree_lst[idx1][1]

        degree_lst2 = [0 for _ in range(len(degree_lst))]
        print(side_x_lst)
        print(sorted(side_x_lst), end = '\n\n')
        for idx1, val2 in enumerate(sorted(side_x_lst)):
            idx2 = side_x_lst.index(val2)
            degree_lst2[idx2] = degree_lst[idx1][1]
    except:
        return result

    # print(len(crop_img))
    for i in range(len(crop_img)):
        width = int(crop_img[i].shape[1])
        vertical = int(crop_img[i].shape[0] *1.2)
        trans = False

        # 손톱의 너비를 줄이기 위한 작업
        if width > vertical * 0.7:
            width = int(vertical * 0.7)
        if width < vertical * 0.6:
            width = int(vertical * 0.6)
            print('Trans True')

        nail_exp = np.ones_like(crop_img[i])
        nail_exp = cv2.resize(nail_exp, (vertical, vertical))
        c = nail_exp.shape[0] / 2

        # 생성된 네일 이미지를 손톱 하나씩 자르는 부분
        a1 = design_bt.shape[1]/5 *i; a2 = (design_bt.shape[1]/5)*(i+1) + 1
        nail = design_bt[:, int(a1): int(a2)]

        # texture 추가하는 함수 적용
        b1 = int(round(c - width / 2, 0))
        b2 = int(round(c + width / 2, 0))

        if b1 < 0:
            b1 = 0

        if b2 > nail_exp.shape[0]:
            b2 = nail_exp.shape[0]

        nail = contrast(nail, texture)
        # plt.axis('off')
        # plt.imshow(nail)
        # plt.show()

        # 네일 맛크 크기에 맞게 nail 이미지 조정
        nail = cv2.resize(nail, (b2 - b1, int(vertical)))
        nail_exp[:, b1: b2] = nail
        # plt.axis('off')
        # plt.imshow(nail_exp)
        # plt.show()

        # 자연스러움을 위한 높이 추가
        plus = int(nail_exp.shape[0]*0.1)
        center = (int(nail_exp.shape[1]/2), int(nail_exp.shape[0]/2))

        # 각도 계산
        if index == 1:
            angle = -degree_lst2[i]
        else:
            if i == 0:
                angle = -degree_lst2[i] -10
            else:
                angle = -degree_lst2[i]

        matrix = cv2.getRotationMatrix2D(center, angle, scale=1)
        nail_rotation = cv2.warpAffine(nail_exp, matrix,(0, 0))
        # plt.axis('off')
        # plt.imshow(nail_rotation)
        # plt.show()

        # 합성 시 부족한 X축 너비 채우기
        if (side_x_lst[i][1] - side_x_lst[i][0]) < vertical * 0.8:
            val1 = int((vertical * 0.8 - (side_x_lst[i][1] - side_x_lst[i][0]) ) / 2)
            print('x 너비 수정', i)
        else:
            val1 = 0

        if texture_name == 'stileto' or texture_name == 'ballerina' :
            val = int((side_y_lst[i][1] - side_y_lst[i][0]) * 0.4)
            img = result[side_y_lst[i][0] - val:side_y_lst[i][1] - plus, side_x_lst[i][0] -val1:side_x_lst[i][1] +val1]

            nail_rotation = cv2.resize(nail_rotation, (img.shape[1], img.shape[0]))

            result[side_y_lst[i][0] - val:side_y_lst[i][1] - plus ,
            side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1] = cv2.subtract(img, nail_rotation)
            result[side_y_lst[i][0] - val:side_y_lst[i][1] - plus ,
            side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1] = cv2.subtract(img, nail_rotation)
            result[side_y_lst[i][0] - val:side_y_lst[i][1] - plus ,
            side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1] = cv2.subtract(img, nail_rotation)
            result[side_y_lst[i][0] - val:side_y_lst[i][1] - plus ,
            side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1] = cv2.add(img, nail_rotation)

        else:
            img = result[side_y_lst[i][0]-int(1.2*plus):side_y_lst[i][1]-plus , side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1]
            nail_rotation = cv2.resize(nail_rotation, (img.shape[1], img.shape[0]))

            result[side_y_lst[i][0]-int(1.2*plus):side_y_lst[i][1]-plus , side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1] = cv2.subtract(img, nail_rotation)
            result[side_y_lst[i][0]-int(1.2*plus):side_y_lst[i][1]-plus , side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1] = cv2.subtract(img, nail_rotation)
            result[side_y_lst[i][0]-int(1.2*plus):side_y_lst[i][1]-plus , side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1] = cv2.subtract(img, nail_rotation)
            result[side_y_lst[i][0]-int(1.2*plus):side_y_lst[i][1]-plus , side_x_lst[i][0]-val1 :side_x_lst[i][1]+val1] = cv2.add(img, nail_rotation)
        print('nail: ', i, 'done')

    return result

# 손톱 디자인의 밝기를 손의 밝기만큼 줄이기
def brightness(design, hand_resize):
    val = (design.mean() - hand_resize.mean()) * 0.2
    arr = np.full(design.shape, val, dtype=np.uint8)
    if arr[0][0][0] >= 200:
        arr =  np.full(design.shape, 256-val, dtype=np.uint8)
    if (design.mean() - hand_resize.mean()) < 0:
        design = cv2.subtract(design, arr)
    else:
        design = cv2.subtract(design, arr)
    return design

# nail: 네일 손톱 하나 이미지, mask: 쉐입에 따른 명암 이미지
def contrast(nail, mask, alpha=0.8, num=0.5):
    global img_nail, img_mask
    img_nail = nail.copy()
    img_mask = mask.copy()

    # 네일 이미지에 맞게 그림자 크기 조정
    img_mask = cv2.resize(img_mask, (img_nail.shape[1], img_nail.shape[0]))

    dst = cv2.addWeighted(img_nail, alpha, img_mask, (1 - alpha), 0)

    dst = dst.astype('int32')
    # 채도 조절 부분 (자연스럽게 하기 위해 빼놓음)
    # dst = np.clip(dst+(dst-128)*num, 0, 255)
    dst = dst.astype('uint8')

    return dst


            

##############################################################################
############################ 변수 선언부 #####################################
# 손 이미지  불러오기
def nail_image_make(img_name, fname, select_shape):
    image = cv2.imread(f"static/adain/hand/{img_name}")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    test_dataset_dir = Path('static/adain/hand')
    test_hand_images = [test_dataset_dir / img_name]
    print('1완')

    # 손 이미지에 mask_segmentation 적용
    test_dataset(test_hand_images, img_name)
    print('2완')

    # 손톱 segmentation 모델 실행 후 받아온 솝톱 마스크 이미지
    son_mask = cv2.imread(f"static/adain/hand_mask/model_mask_{img_name}")
    son_mask = cv2.resize(son_mask, (image.shape[1], image.shape[0]))
    rot_crop_box3(son_mask)
    print('3완')

    # 생성된 디자인 불러오기
    design_path = 'static/adain/result/'
    design = cv2.imread(design_path + fname + '.jpg')
    design = cv2.cvtColor(design, cv2.COLOR_BGR2RGB)

    # 네일 디자인 밝기 조절을 위한 hand image resize
    hand_resize = cv2.resize(image, (design.shape[1], design.shape[0]))

    # 네일 디자인 밝기 조절
    # texture_path = 'static/adain/texture/'
    design_bt = brightness(design, hand_resize)
    
    # texture = cv2.imread(texture_path + select_shape + '.jpg')

    ##############################################################################
    ############################ 코드 실행부 #####################################
    # mediapipe 적용해서 손톱 각도 구하기
    img_copy, point, index = find_point(image)
    print('4완')

    degree_lst = degree_finger(point)
    print('5완')

    result = add_nail(design_bt, image, crop_img, degree_lst, side_x_lst, side_y_lst, index, select_shape)
    
    
    print('6완')
    save_path = 'static/adain/final_result/'
    plt.imsave(save_path + f'{fname}.jpg', result);

    return fname


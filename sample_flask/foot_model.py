import cv2
import matplotlib.pyplot as plt
import numpy as np
from foot_function import *

def fit_pedi(foot_raw: str, foot_mask: str, design: str) -> np.ndarray :
    raw_foot_dir = "static/adain/foot"
    raw_foot = cv2.imread(f"{raw_foot_dir}/{foot_raw}", cv2.IMREAD_UNCHANGED)

    raw_foot = bgrrgb(raw_foot)
    mask_foot_dir = 'static/adain/foot_mask'
    raw_mask = cv2.imread(f"{mask_foot_dir}/model_mask_{foot_mask}")
    rows, cols = raw_foot.shape[:2]
    nTop = int(rows*0.009)
    nBottom = int(rows*0.04)
    nLeft = int(cols*0.04)
    nRight = int(cols*0.04)

    dst = cv2.imread(f"static/image/pedi_design_mask/{design}.jpg")
    
    dst = bgrrgb(dst)
    # dst = brightness(dst, raw_foot)
    # top_point, left_point, right_point, low_point = pts_box(dst)
    # point1 , point2, point3, point4 = [left_point[0],top_point[1]], [right_point[0],top_point[1]], [right_point[0],low_point[1]], [left_point[0],low_point[1]]
    raw_mask_ct = Contours(raw_mask)
    try:
        crop_img = rot_crop_box3(dst)
    except:
        pass
    crop_img = [x for x in crop_img if x is not None]
    crop_design_lst = []
    
    if len(crop_img) != 5:
        for i in crop_img:
            if (i.shape[0] + i.shape[1]) > (dst.shape[0] + dst.shape[1])/12:
                crop_design_lst.append(i)
                print('추가')

        while len(crop_design_lst) < 5 :
            crop_design_lst.append(crop_design_lst[0])

        crop_img = crop_design_lst.copy()
    for num in range(5):
        crop_list = rot_crop_box3(raw_mask)
        if len(crop_list) != 5:
            count_err = len(crop_list)
            print(f"손톱 검출 개수 이상!\n필요개수: 5 \n현재: {count_err}")
            return None


        resized_dst = cv2.resize(crop_img[num],(raw_foot.shape[1],raw_foot.shape[0]))
        
        # 사이즈 조절부
        ISOLATED = cv2.copyMakeBorder(resized_dst, nTop, nBottom, nLeft, nRight, 
                                    borderType=cv2.BORDER_ISOLATED)
        resized_dst = ISOLATED.copy()
        
        resized_dst = cv2.resize(resized_dst,(raw_foot.shape[1],raw_foot.shape[0]))

        top_point, left_point, right_point, low_point = pts_box(resized_dst)
        point1 , point2, point3, point4 = [left_point[0],top_point[1]], [right_point[0],top_point[1]], [right_point[0],low_point[1]], [left_point[0],low_point[1]]

        cnt = raw_mask_ct[num]
        # Rotated Rectangle
        rect = cv2.minAreaRect(cnt)
        hand_box = cv2.boxPoints(rect)
        hand_box = np.int0(hand_box)

        final_before = np.float32([ [0, 0], [cols, 0], [0, rows], [cols, rows] ])
        # 변환 후
        
        
        final_after = np.float32([hand_box[0], hand_box[1],hand_box[3],hand_box[2]])

        mtrx2 = cv2.getPerspectiveTransform(final_before, final_after)
        dst2 = cv2.warpPerspective(resized_dst, mtrx2, (cols, rows))
        dst3 = np.where(dst2 > 1, 255, dst2)
        
        # 네일 색이 어두우면 dst3로 subtract
        if dst2.mean() < 0.6:
            output=cv2.subtract(raw_foot, dst3)
        else:
            output=cv2.subtract(raw_foot, dst2)
        output2 = cv2.add(output,dst2)
        raw_foot = output2.copy()
        

        save_path = 'static/pedi_make/'
        plt.imsave(save_path + 'sample.jpg', raw_foot)
    
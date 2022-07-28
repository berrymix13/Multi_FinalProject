import cv2
import matplotlib.pyplot as plt
import numpy as np
from nail_function import *

def fit_nail(hand_raw: str, hand_mask: str, design: str) -> np.ndarray :
    '''
    hand_raw              ->    사용자 입력 손 이미지 ( 현재는 파일명 )\n
    hand_mask           ->     손 이미지의 손톱 마스크 ( 현재는 파일명 )\n
    design                  ->      사용자 선택 네일 디자인 명 (영어)\n
    '''
    raw_hand = cv2.imread(f"./NailModel/{hand_raw}", cv2.IMREAD_UNCHANGED)
    raw_mask = cv2.imread(f"./NailModel/{hand_mask}")
    raw_mask = cv2.resize(raw_mask, (raw_hand.shape[1],raw_hand.shape[0]))
    rows, cols = raw_hand.shape[:2]
    nTop = int(rows*0.009)
    nBottom = int(rows*0.04)
    nLeft = int(cols*0.04)
    nRight = int(cols*0.04)
    nail_img = cv2.imread(f"./NailModel/design/{design}")
    crop_nail_img = rot_crop_box3(nail_img)
    crop_nail_img = [i for i in crop_nail_img if i is not None]
    

    for num, dst in enumerate([i for i in crop_nail_img if i.shape[0]+i.shape[1] > (nail_img.shape[0]+nail_img.shape[1])/7]):
        crop_list = rot_crop_box3(raw_mask)
        if len(crop_list) != 5:
            count_err = len(crop_list)
            print(f"손톱 검출 개수 이상!\n필요개수: 5 \n현재: {count_err}")
            return None
        raw_mask_ct = Contours(raw_mask)

        resized_dst = cv2.resize(dst,(raw_hand.shape[1],raw_hand.shape[0]))
        
        # 사이즈 조절부
        ISOLATED = cv2.copyMakeBorder(resized_dst, nTop, nBottom, nLeft, nRight, 
                                    borderType=cv2.BORDER_ISOLATED)
        resized_dst = ISOLATED.copy()
        
        resized_dst = cv2.resize(resized_dst,(raw_hand.shape[1],raw_hand.shape[0]))

        cnt = raw_mask_ct[num]
        # Rotated Rectangle
        rect = cv2.minAreaRect(cnt)
        hand_box = cv2.boxPoints(rect)
        hand_box = np.int0(hand_box)

        final_before = np.float32([ [0, 0], [cols, 0], [0, rows], [cols, rows] ])
        # 변환 후
        if num == 0:
            final_after = np.float32([hand_box[1], hand_box[2],hand_box[0],hand_box[3]])
        else:
            final_after = np.float32([hand_box[0], hand_box[1],hand_box[3],hand_box[2]])

        mtrx2 = cv2.getPerspectiveTransform(final_before, final_after)
        dst2 = cv2.warpPerspective(resized_dst, mtrx2, (cols, rows))
        dst3 = np.where(dst2>5, 255, dst2)
        # 네일 색이 어두우면 dst3로 subtract
        if dst2.mean() < 0.55:
            output=cv2.subtract(raw_hand, dst3)
        else:
            output=cv2.subtract(raw_hand, dst2)
        output2 = cv2.add(output,dst2)
        raw_hand = output2.copy()
    return raw_hand

if __name__ == "__main__":
    rt = fit_nail("model_hand.jpg", "model_hand_mask.jpg", "design (55).jpg")
    cv2.namedWindow("show", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("show",400,800)
    cv2.imshow("show",rt)
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
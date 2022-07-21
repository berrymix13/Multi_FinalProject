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
    
    fdir = "C:/workspace/05.FinalProject/Multi_FinalProject/NailModel/practice"
    raw_hand = cv2.imread(f"{fdir}/{hand_raw}", cv2.IMREAD_UNCHANGED)
    raw_mask = cv2.imread(f"{fdir}/{hand_mask}")
    rows, cols = raw_hand.shape[:2]
    nTop = int(rows*0.009)
    nBottom = int(rows*0.04)
    nLeft = int(cols*0.04)
    nRight = int(cols*0.04)
    design_name = design
    

    for num in range(5):
        crop_list = rot_crop_box3(raw_mask)
        if len(crop_list) != 5:
            count_err = len(crop_list)
            print(f"손톱 검출 개수 이상!\n필요개수: 5 \n현재: {count_err}")
            return None
        dst = cv2.imread(f"{fdir}/design/{design_name}/design{num}.jpg")
        # dst = brightness(dst, raw_hand)
        # top_point, left_point, right_point, low_point = pts_box(dst)
        # point1 , point2, point3, point4 = [left_point[0],top_point[1]], [right_point[0],top_point[1]], [right_point[0],low_point[1]], [left_point[0],low_point[1]]
        raw_mask_ct = Contours(raw_mask)

        dst_ct = Contours(dst)
        resized_dst = cv2.resize(dst,(raw_hand.shape[1],raw_hand.shape[0]))
        
        # 사이즈 조절부
        ISOLATED = cv2.copyMakeBorder(resized_dst, nTop, nBottom, nLeft, nRight, 
                                    borderType=cv2.BORDER_ISOLATED)
        resized_dst = ISOLATED.copy()
        
        resized_dst = cv2.resize(resized_dst,(raw_hand.shape[1],raw_hand.shape[0]))

        top_point, left_point, right_point, low_point = pts_box(resized_dst)
        point1 , point2, point3, point4 = [left_point[0],top_point[1]], [right_point[0],top_point[1]], [right_point[0],low_point[1]], [left_point[0],low_point[1]]

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
        output=cv2.subtract(raw_hand, dst2)
        output2 = cv2.cvtColor(cv2.add(output,dst2),cv2.COLOR_BGR2RGB)
        raw_hand = output2.copy()
    return output2
    
    
if __name__ == "__main__":
    rt = fit_nail("hand_raw.jpg", "hand_mask.jpg", "design1" )
    cv2.namedWindow("show", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("show",400,800)
    cv2.imshow("show",cv2.cvtColor(rt,cv2.COLOR_BGR2RGB))
    key = cv2.waitKey(0)
    cv2.destroyAllWindows()
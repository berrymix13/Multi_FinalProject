## 네일 디자인 합성

> 목적

사용자가 선택한 네일 디자인과 손 사진을 합성</br></br>

> 사용법

`손` 사진, `손톱 마스크` 사진, `네일 디자인` 사진을 준비 한 후 nail_model.py 에서 fit_nail 함수에 각각 순서대로 인자로 입력한다</br>
<div>예시)
  <body>
   <table border="1" width="700" height="500">
      <th align="center">손</th> 
      <th align="center">손톱 마스크</th> 
      <th align="center">네일 디자인</th> 
      <tr>
        <td align="center"> <img src="https://user-images.githubusercontent.com/102013100/183286074-827b7f70-e6cb-4830-874e-7c4867fef222.jpg" width=200 height=400>
        </td> 
        <td align="center"><img src="https://user-images.githubusercontent.com/102013100/183286085-68af3198-1ce2-4f7e-952c-b0200ee12fad.jpg" width=200 height=400>
        </td>
        <td align="center"><img src="https://user-images.githubusercontent.com/102013100/183286100-0c6c305a-e54d-4763-b6f9-df269cec0f9c.png" width=200 height=400>
        </td>
      </tr>
  </table>
  </body>
</div>
</br></br></br></br>

### Function
---

- [fit_nail]("https://github.com/9mynamemj7/Multi_FinalProject/blob/master/NailModel/fit_nail/nail_model.py")

  <img align="right" alt="GIF" src="https://user-images.githubusercontent.com/102013100/181448792-c469c376-63f2-42b9-bb9e-94689a3007f1.gif?raw=true" width="150" height="200" />

```python
rt = fit_nail("model_hand.jpg", "model_hand_mask.jpg", "design (1).png")
cv2.namedWindow("show", cv2.WINDOW_NORMAL)
cv2.resizeWindow("show",400,800)
cv2.imshow("show",rt)
key = cv2.waitKey(0)
cv2.destroyAllWindows()
```
메인코드
</br>
</br>

-  [Contours]("https://github.com/9mynamemj7/Multi_FinalProject/blob/master/NailModel/fit_nail/nail_function.py")

```python
raw_mask_ct = Contours(raw_mask)
cnt = raw_mask_ct[num]
rect = cv2.minAreaRect(cnt)
hand_box = cv2.boxPoints(rect)
hand_box = np.int0(hand_box)
```
손톱 마스크의 좌표를 컨투어를 이용하여 구한다.</br>
hand_box는 리스트 형태로 각 끝점의 좌표를 가진다

</br>
</br>

- [rot_crop_box3]("https://github.com/9mynamemj7/Multi_FinalProject/blob/master/NailModel/fit_nail/nail_function.py")

```python
crop_nail_img = rot_crop_box3(nail_img)
plt.figure(figsize=(15,9))
for i in range(5):
    plt.subplot(1,5,i+1)
    plt.title(f"finger{i}")
    plt.imshow(bgrrgb(crop_nail_img[i]));
```
네일 디자인에서 네일을 검출해 낸다.</br>
검출 후 수직으로 세운다

<body>
  <div>
    <p>결과)</p>
    <img align="left" alt="crop" src="https://user-images.githubusercontent.com/102013100/183378958-ebfe48b7-3004-45e1-93cf-5fad61300998.png" width=500 height=200>
  </div>
</body>
</br></br></br></br></br></br></br></br></br></br></br></br>


### 추후 개선 필요사항
---
- 손톱이 아래를 보고있는 경우도 고려한 기능을 추가
- 어두운 색감의 네일디자인 합성에서 주변부가 검은색이 되는것 개선
- 종종 손톱 좌표가 의도와 맞지않게 잘못 구해지는 경우 개선 


</br></br></br>
### Environment
---


__OS__</br>
<img src="https://img.shields.io/badge/Windows10-0078D6?style=flat-square&logo=Windows&logoColor=white"/></br>
__Language__</br>
<img src="https://img.shields.io/badge/Python 3.7-3776AB?style=flat-square&logo=Python&logoColor=white"/></br>
__IDE__</br>
<img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=#F37626"/></br>
__Library__</br>
<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=OpenCV&logoColor=white"/>
<img src="https://img.shields.io/badge/Numpy-013243?style=flat-square&logo=Numpy&logoColor=white"/>
<img src="https://img.shields.io/badge/Matplotlib-013243?style=flat-square&logo=Matplotlib&logoColor=white"/>




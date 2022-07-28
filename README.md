#  가상네일 서비스

> __DDD (데이터 뚝딱이들)__<br>
> 
> [Sujin Jeong](https://github.com/berrymix13)\*<sup>Leader</sup>, [Minjung Kim](https://github.com/9mynamemj7)\*<sup>B</sup>, [Hyunjin Kim](https://github.com/Jinimo)\*<sup>B</sup>, [Sungho Park](https://github.com/alexnkan)\*<sup>A</sup>, [Hyunsun Bang](https://github.com/banghs17)\*<sup>A</sup> ,[Byungjun Yoon](https://github.com/choonsik24)\*<sup>A</sup>

<br></br>
<br></br>

###  배경

>셀프 네일의 수요가 많아짐에 따라 내 손톱에 어울리는 지 미리 체험하는 수요가 생기게 되었고, 네일아트는 내 손톱에 어울리는지 해보고 결정할 수 없다. 때문에 자신의 손 사진을 찍어서 디자인을 입힌 모습을 보기 위해 이 서비스를 개발하게 되었으며, 추가로 날씨나, 선택된 그림, 연예인의 네일디자인, 샌들이미지와 어울리는 디자인을 추천 해 준다.

<br></br>
<br></br>
<br></br>
<br></br>


## 작업


### 손톱 검출
___

Pytorch를 활용한 U-net model
<center><img src="https://user-images.githubusercontent.com/102013100/181456356-b542319f-aece-45ce-b9cd-d90f84ef4e52.png" width="80%" height="100%"></center>

<br></br><br></br>

###  네일 디자인 합성
___
<body>
 <table border="1" width="900" height="600" align="center">
    <th bgcolor="gray">INPUT</th> 
    <th bgcolor="gray">OUTPUT</th> 
    <tr><!-- 첫번째 줄 시작 --> 
      <td> <img src="https://user-images.githubusercontent.com/102013100/181449002-1e7993a6-85d2-409f-983c-5d6059258877.jpg" width=300 height=500>
      </td> 
      <td><img src="https://user-images.githubusercontent.com/102013100/181448792-c469c376-63f2-42b9-bb9e-94689a3007f1.gif" width=300 height=500>
      </td> 
    </tr><!-- 첫번째 줄 끝 -->
</table>
</body>

<br></br><br></br>

### 네일 디자인 생성
___

- Style Transfer

    그림(Style)과 패턴(Pattern)을 합성하여 새로운 디자인 생성
<center><img src="https://user-images.githubusercontent.com/102013100/181467223-a41fc229-b337-4677-91e4-cbacd7ff7fa4.png" width="80%" height="100%"></center>

<br></br>

- Media Pipe + Object Detection

    네일 디자인 합성
<center><img src="https://user-images.githubusercontent.com/102013100/181458716-fda92186-4899-4fdd-8a2f-a4e0d0bc3a47.png" width="80%" height="100%"></center>

<br></br><br></br>


### 추천시스템
___
- 사용자 요구에 맞는 디자인 추천

  <center><img src="https://user-images.githubusercontent.com/102013100/181468989-c1fd856d-0e05-4cf3-847e-310c81bdd6f7.png" width="80%" height="100%"></center>
  <br></br>

- 계절 & 날씨와 어울리는 네일 디자인 추천
    
    
    <center><img src="https://user-images.githubusercontent.com/102013100/181469156-678b4b81-aa6f-4509-b515-622ea200d190.png" width="80%" height="100%"></center>
  
    
    <center><img src="https://user-images.githubusercontent.com/102013100/181469835-15ef22ab-545c-4704-93e4-79db0f0c7149.png" width="80%" height="100%"></center>

- 관심 연예인의 네일 디자인 추천

    <center><img src="https://user-images.githubusercontent.com/102013100/181470263-583da94d-a549-4e0e-b527-734823d89b2e.png" width="80%" height="100%"></center>
  
- 샌들에 어울리는 페디 디자인 추천

    <center><img src="https://user-images.githubusercontent.com/102013100/181470692-b2076e2b-868c-4140-baf1-0f36641b07ed.png" width="80%" height="100%"></center>




<br></br>
<br></br>
<br></br>
<br></br>


### Tech
---
<body>
<img src="https://img.shields.io/badge/python-3776AB?style=flat-square&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Jupyter Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white"/>

<img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=flat-square&logo=Visual Studio Code&logoColor=#F37626"/> <img src="https://img.shields.io/badge/Google Colab-F9AB00?style=flat-square&logo=Google Colab&logoColor=white"/>

<img src="https://img.shields.io/badge/Google Drive-4285F4?style=flat-square&logo=Google Drive&logoColor=white"/> <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=#F37626"/>

<img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=OpenCV&logoColor=white"/> <img src="https://img.shields.io/badge/Numpy-013243?style=flat-square&logo=Numpy&logoColor=white"/> <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=PyTorch&logoColor=white"/> <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=TensorFlow&logoColor=white"/> <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask&logoColor=white"/>	
</body>

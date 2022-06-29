import json
# 계정 아이디 비밀번호
with open('user_id_pw.json') as f:
    insta = json.load(f)
user_id = insta['user_id']
user_pw = insta['user_pw']
tag = []
upload_id = []
img_url = []
user_id=user_id 
user_pw=user_pw
wish_num=3
login_option="instagram"
driver_path="c:/pydata/chromedriver.exe"
keyword="네일아트"
instagram_id_name='//*[@id="loginForm"]/div/div[1]/div/label/input'
instagram_pw_name='//*[@id="loginForm"]/div/div[2]/div/label/input'
instagram_login_btn='//*[@id="loginForm"]/div/div[3]/button'
first_img_xpath='//*[@id="mount_0_0_At"]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div[1]/div[1]/img'
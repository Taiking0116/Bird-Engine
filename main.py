#モジュールのインポート
import requests

import cv2
import numpy as np

import time

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Notifyの定義
TOKEN = 'アクセストークン'
api_url = 'https://notify-api.line.me/api/notify'
send_contents = '時間割が更新されました。スプレッドシート：https://docs.google.com/spreadsheets/d/128mFFj6w1drdDzxsKsoc9Xdba2FEWSffcM2iUSrnZ0c/edit?usp=sharing。'
TOKEN_dic = {'Authorization': 'Bearer' + ' ' + TOKEN} 
send_dic = {'message': send_contents}

#スプレッドシートのアイコン取得
img_url = ''
response = requests.get(img_url)
image = response.content
file_name = "new.png"

with open(file_name, "wb") as f:
    f.write(image)

#現在の取得したアイコンの要素
img_diff_new = cv2.imread("new.png", cv2.IMREAD_GRAYSCALE)
whitePixels_new = np.count_nonzero(img_diff_new)
blackPixels_new = img_diff_new.size - whitePixels_new
element_new = whitePixels_new / img_diff_new.size * 100

#GoogleDriveの定義
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)
 
#古いアイコンの要素
img_url_old = ''
response_old = requests.get(img_url_old)
image_old = response_old.content
file_name_old = "old.png"
with open(file_name_old, "wb") as f:
    f.write(image_old)

img_diff_old = cv2.imread("old.png", cv2.IMREAD_GRAYSCALE)
whitePixels_old = np.count_nonzero(img_diff_old)
blackPixels_old = img_diff_old.size - whitePixels_old
element_old = whitePixels_old / img_diff_old.size * 100


#アイコンの変化を認識
if element_new == element_old:
    print('変化なし')
else:
    folder_id = 'フォルダID'
    file_path = 'new.png'
    qstr = "title = \"new.png\" and \"" + folder_id + "\" in parents and trashed=false"
    files = drive.ListFile({'q': qstr}).GetList()
    file = files[0]
    print('File Exists on Drive :\t', file['title'], ' (', file['id'], ')')
    file.SetContentFile(file_path)
    file.Upload()
    image_file = 'new.png'
    binary = open(image_file, mode='rb')
    image_dic = {'imageFile': binary}
    requests.post(api_url, headers=TOKEN_dic, data=send_dic, files=image_dic)
    print('変化あり')

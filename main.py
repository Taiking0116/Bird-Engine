#モジュールのインポート
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
import cv2
import numpy as np
import time
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import json

#-------------------------------------
#Statusの確認
img_url = 'Status画像のURｌ'
response = requests.get(img_url)
image = response.content
file_name = "now_statas.png"

with open(file_name, "wb") as f:
    f.write(image)
#Statasアイコンの要素
img_diff_new = cv2.imread("now_statas.png", cv2.IMREAD_GRAYSCALE)
whitePixels_new = np.count_nonzero(img_diff_new)
blackPixels_new = img_diff_new.size - whitePixels_new
element_now = whitePixels_new / img_diff_new.size * 100
if element_now == 100.0:
    print('Statas実行')
else:
    print('Statas終了')
    sys.exit()

#-------------------------------------
#各システムの定義
#GoogleDriveの定義
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)
#Notifyの定義
TOKEN = 'アクセストークン'
api_url = 'https://notify-api.line.me/api/notify'
send_contents = '時間割が更新されました。'
TOKEN_dic = {'Authorization': 'Bearer' + ' ' + TOKEN} 
send_dic = {'message': send_contents}

#-------------------------------------
#スプレッドシートから画像を取得
# スプレッドシートのURLを指定する
url = "https://docs.google.com/spreadsheets/u/0/d/128mFFj6w1drdDzxsKsoc9Xdba2FEWSffcM2iUSrnZ0c/？？？？？"　#コピペ防止措置

# リクエストを送信し、レスポンスを受け取る
response = requests.get(url)

# レスポンスからHTMLを抽出する
html = response.content

# BeautifulSoupを使用してHTMLを解析する
soup = BeautifulSoup(html, "html.parser")

# 画像タグを検索して、画像のURLを取得する
img_tags = soup.find_all("img")
image_urls = [img['src'] for img in img_tags]

# 画像を取得してPillowのImageオブジェクトとして読み込む
images = []
for url in image_urls:
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    images.append(image)

# 画像を縦方向につなげる
widths, heights = zip(*(i.size for i in images))
max_width = max(widths)
total_height = sum(heights)

new_im = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
y_offset = 0
for im in images:
    new_im.paste(im, (0, y_offset))
    y_offset += im.size[1]

# 画像を保存する
new_im.save("new.png")
#---------------------------------------
#現在の取得した時間割画像の要素
img_diff_new = cv2.imread("new.png", cv2.IMREAD_GRAYSCALE)
whitePixels_new = np.count_nonzero(img_diff_new)
blackPixels_new = img_diff_new.size - whitePixels_new
element_new = whitePixels_new / img_diff_new.size * 100

#---------------------------------------
#古るい画像の取得
img_url_old = '古い（現在公開中）時間割画像を取得'
response_old = requests.get(img_url_old)
image_old = response_old.content
file_name_old = "old.png"
with open(file_name_old, "wb") as f:
    f.write(image_old)
#---------------------------------------
#古い時間割の要素
img_diff_old = cv2.imread("old.png", cv2.IMREAD_GRAYSCALE)
whitePixels_old = np.count_nonzero(img_diff_old)
blackPixels_old = img_diff_old.size - whitePixels_old
element_old = whitePixels_old / img_diff_old.size * 100

#---------------------------------------
#時間割画像の変化を認識
if element_new == element_old:
    print('変化なし')
else:
    #GoogleDriveに保存（公開）
    folder_id = 'フォルダID'
    file_path = 'new.png'
    qstr = "title = \"new.png\" and \"" + folder_id + "\" in parents and trashed=false"
    files = drive.ListFile({'q': qstr}).GetList()
    file = files[0]
    file.SetContentFile(file_path)
    file.Upload()
    #運営側に送信
    #Slack
    SLACK_POST_URL = "IncommingWebhookのURL"
    post_json = {
        "text": "時間割が更新されました。",
        "attachments": [{
            "fields": [
                {
                    "title": "時間割が更新されました。",
                    "value": "時間割が更新されました。",
                }],
            "image_url": "時間割画像URL"
        }]
    }
    requests.post(SLACK_POST_URL, data = json.dumps(post_json))
    #LINENotify
    image_file = 'new.png'
    binary = open(image_file, mode='rb')
    image_dic = {'imageFile': binary}
    requests.post(api_url, headers=TOKEN_dic, data=send_dic, files=image_dic)
    print('変化あり')

#モジュールのインポート
import requests

import cv2
import numpy as np

import time

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#Notifyの定義
TOKEN = 'K4xJ3pnAMlsS8miF1qSM3jnKG3sCs453OEzakNn4llR'
api_url = 'https://notify-api.line.me/api/notify'
send_contents = '時間割が更新されました。スプレッドシート：https://docs.google.com/spreadsheets/d/128mFFj6w1drdDzxsKsoc9Xdba2FEWSffcM2iUSrnZ0c/edit?usp=sharing。'
TOKEN_dic = {'Authorization': 'Bearer' + ' ' + TOKEN} 
send_dic = {'message': send_contents}

#スプレッドシートのアイコン取得
img_url = 'https://lh3.googleusercontent.com/fife/AAbDypD3ebQbvlb_eC56W4kuj8yuADLeeemPHKO8oxwpe-WGOvZaXOcuYWcN-kSkdr1FPd8ulOoiXo110LgApXe0hdJiv8IXyra5ncWKBpQSsoCKLN8yFnUr0tUX57FX0P_GN0anNiPwdTWCGYtY1oGJ-HmVjJioHgME-wziwudW0OenaH3gKduEto_Aid19g8DIOUXf148v1HH2Y8fVXCT2lQi8SHEgmtu8fjOX4eFJ8tCN5C-NYlL8X2G5MONB5B3qXTXD2-OqSCtFGSNkA4GF22w7wfy5lxo7DVYA3cM9h7gSOyuXElImGvj3XEdiSLLBUMNN4sOj1h-ewBSpckaxeU3gend6JPSTyvJDz4cinDdobiRNCgswNllHOMM7N6-bXPGYiYXgaBy59AKceaIJjkNaqnJmAlBf2glJ-o7UnEFXjjYEguG0Ei3MCq7zKIQL5_fazfoTj8pLcY4pEm0spjunw5AFaZH43IuTHXa6z9sPjmuBz4qpQ0jQBhWqf_gq6Ccuwr0XIV90aOfgw4h14CQOlpUonS-CFRaJlrIjyjvvlF5frqAxwfz6_nH0opIoTpp8G1AmdEaltbMAwoxCc0UNT_z9gc_pzGL42e8mrTAeU-WsRDQ0yelVf13wr4qxOxlAoOxa1d-N2SLtiq3WgZ6iv-vWrcsASzGCTtQA6yIfQ9CRODF0zSiT_S1cltQPa-H3XDkgFEj4uQqEV1AOuxWIbUS67Xo7UYi7Q5LFXyHot8rFHh0p_djKLRRU1ChjgnbbkuwYaEjG-gVokpNYwLkNyZBn_tDIdF_WhMTrNywPVKbY9cPUzSrTiNAXeR70siR0muHT7bK2I6yp1CbmlbwaZyhfK9Wtih8M8UOb3etgmCZQDGVk2U7997-S9g8LRdjrH-84_5wkxRzaqJg66-PlwDEZxIqLH_AJih1YUmEE4USavFeQ0RANji5pg2yIISPjPRd8tEf22g7LNtcJ0vKdkYgnsVwoTGyUUT3_06yRpvxFTIahINq5CIcNAG65ULrNqk8ChOkNb0Oyw8wlFLO8_ffQ4kooM91UH077Dnt-GRTLWQ34XpiTPApQbOsEpgLVi6lQe1qRQlAkXw0UUEDQv3WmjPh161ecaRgSkySlEZ8dDThJ3ZF7CaIG9-42gcHgYbZownhGzDzvEXoCG_h4joUn7_rV9ZJ5y1zoYfq7EKy_UvPMB1VjG-mnWLwZ64l1LKl41krMTIWwDcpsE4E5DlYTwyWEcZUyqIS2xzhgUHx0bWLjqaitqypih1dc7yHl-TFMaYdzBkl7Fv5xWiRloAktSsehn5Unz5VOXvXCuW9soRLHPxHqMEEoe0fr9lNG0cjSHhVB-5iTXdnXknFJv1JdazqDRNeSxobxQ1KCn-SVUEitZYz0xjiUswt7SQjIgTSlPXL_ckGYomxIfzx5czAv-NlH0l4C89JXlBPRd88RG71G0X2s8ME_y3iqJfMQt1eaMDTy9QWveetJxejh0OEl4qdaSbE1PRzg83v_3yy2IUv_dsnrh1P3omPRTb31=w416-h312-p'
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
img_url_old = 'https://lh3.googleusercontent.com/fife/AAbDypDPmseLsNNm5-3YyWw9TkiQBZ0vNDgqyUm3q9cL4LzwkrQcCT8cw_G6iPQE0S6KH0-2A4nrPYbK9XtJzM5Q1LmM4-aq-OV_WP9uNMmJA-72UtYbp3jywZPPbx89cgHuwosGBeI8tLydVzWXY3kNUs6llZrHLAtVAKAKJNfKtVMUb9kBcw0oHIpcqDMPbVpebIMI7oY3JtpFqnkZhKbtvBS_4X6i-fgGhrDg-ezCC3OVogQbZE6ybPxJMrAqUzNE9AOcAdXUF_CHJLPaC44uQOjVvm6kKHPDZ7mhaXn_6cGjnBfz93hk7yBlPpJHyKtu4HDI62mtWblQXstop06a0A13k4oLLgLZK_m68fUkao7jDUMmZBPRSovUhcFrNVHBa1rPkHU5BufnpKB_x7-LZo4U4cYE7v2xwY2GkoJlwe9ptpsHVWutKM4xWlNCPt7NIfiB3YOGKn28zEFCmbGkX5f0qZ6nF3w6M8HMK3aXMmbMHOo10npDMfdjpYslzGVkTj-1-XduZ_HvuStDLNVqgCFQxDs4Ce8rtacmc9Fio8NVgYDvvctrgh0qI7wMJwKHIgWbOOzTubNaORIjg6VVnRSo3_Nd1lQHrhxDNJBI-ybEENGi8pN_lM6M69YkunRelua8y8Lhq7-Rr3-BGJd5iabEZ2eq5KtszULI9VqepWHV3MTEKMuYpoXrhxWjuVJsI0W0NyAotKWGcyQp7xDSyVbBBtjXkgOM2cgIJBZ77G1EfOgsTP5upw0HRI-9SzrTvn8SGjn6Ph1UqCs_1W-HdXhfD495JBF7peW0ddUkfYZWaqVWDYdJZ7wi5ySPM9pb-JAOzdV0wUzWkO4NJwRRCKWFVh0AN18nHiZ0vn-usQXKs_nkll84YU5Vwi7aklrrfuo_seHXZz48cO_5FRD9oX7BfxEFRZ5anUtURbT5Mvalo0spLR1pQJqYQgP4eMTlBv9xx70rIL-e7ovqbd4uMaULn86w6hR6VaUvScGGFuxnP9VCAFw6dObB7pTRlD9JU12iNr0pQO5qNeAHLlUjXar2Io_HHMuurynNHbmNzT8HHhtDC81zbChbsIg7m1fUBZmXu7c9lw67Wdf13ZNAvBUNCsqmZXKctac0wBAi455QPt0QnGEzuOI950YQOSqaPaK3ZnTZ5tdYnBYelRKByjzN_bADLCpxAV6j94QoM90Eg1GNO-AI8ysexAABWa8MKDJbv9bayQUexGd_CXkXELu8Jcn0l7YPmL90-BBVGZkWGzM_BijFIoC8OCViBE9NOgrRYy2P6iPOso7IkXVfJ_Y4s9KkKdlSw4GJ_Q51HeBecRcpQfq2riEnRXuVG37qUNPkxV0dNBUGy7mmOCq0omgHDbgy5pXPCJsG0Ni4a1dlv-03r4VMcnVdcovwAXWeXMERir74DUNCD1Ejrq55CW4e_Ta5UyXWylTvCkBUAMQIzFHxSZJSsat1CKYv6Hwncn6XdyAsoYxb34Cv0A9LH5jy9L88rcRP-_RBS-PrjLDkmAqd0YkhSDht=w2880-h1712'
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
    folder_id = '1-iyLVKdqqT9wt7G7eTP9qa18ps_7rM1A'
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

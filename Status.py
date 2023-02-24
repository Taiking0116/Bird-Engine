#時間割Bot（BirdEngine）が更新チェックするかしないかをコントロールするプログラム
#モジュールを増やすのが面倒だったので、画像の白のピクセルの割合でコントロールすることにした。

#ステータス停止
def stop():
  from pydrive.auth import GoogleAuth
  from pydrive.drive import GoogleDrive
  gauth = GoogleAuth()
  gauth.CommandLineAuth()
  drive = GoogleDrive(gauth)
  folder_id = 'ファイルID'
  file_path = 'statas0.png'
  qstr = "title = \"status.png\" and \"" + folder_id + "\" in parents and trashed=false"
  files = drive.ListFile({'q': qstr}).GetList()
  file = files[0]
  #アップロード
  file.SetContentFile(file_path)
  file.Upload()
  
#ステータス再開（実行）

def restart():
  from pydrive.auth import GoogleAuth
  from pydrive.drive import GoogleDrive
  gauth = GoogleAuth()
  gauth.CommandLineAuth()
  drive = GoogleDrive(gauth)
  folder_id = 'ファイルID'
  file_path = 'statas1.png'
  qstr = "title = \"status.png\" and \"" + folder_id + "\" in parents and trashed=false"
  files = drive.ListFile({'q': qstr}).GetList()
  file = files[0]
  #アップロード
  file.SetContentFile(file_path)
  file.Upload()
  
  #ステータスの確認
  def check_status():
    #Statas画像取得
    img_url = '画像URL'
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

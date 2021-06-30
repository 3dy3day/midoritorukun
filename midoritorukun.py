from plyer import notification
import cv2
import numpy as np
import os

joint = os.path.join
current = os.getcwd()
inpath = 'input_img'
outpath = 'output_img'
icon = 'python.ico'

path = joint(current, inpath)
# print(path)
load = os.listdir(path)
# print(load)


def imread(filename, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        decimg = cv2.imdecode(n, cv2.IMREAD_COLOR)
        return decimg
    except:
        print("ERROR!!")
        return None


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except:
        print("ERROR!!")
        return False


for j in load:
    if j.endswith('.png') or j.endswith('.jpeg') or j.endswith('.jpg') or j.endswith('.JPG') or j.endswith('.JPEG'):
        path1 = joint(path, j)
        # print("\n\n\n", path1)
        img = imread(path1)

        hsvLower = np.array([50 / 360 * 179, 50, 50])    # 抽出する色の下限(HSV)
        hsvUpper = np.array([150 / 360 * 179, 255, 255])    # 抽出する色の上限(HSV)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 画像をHSVに変換

        hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)    # HSVからマスクを作成
        result = cv2.bitwise_and(img, img, mask=hsv_mask)
        export_name = j + '_result.png'
        imwrite(joint(outpath, export_name), result)

notification.notify(
    title="Python",
    message="Extraction Complete!",
    app_name="Midoritorukun",
    app_icon=joint(current, icon),
    timeout=10
)

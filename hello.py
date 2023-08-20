import os
import uuid
import datetime
import pyautogui
import pytesseract
from PIL import Image

# 使用する外部ライブラリ
# `pip install pyautogui pytesseract Pillow` 

def main():
    # 画像ファイルとして保存
    target_region = get_target_region()
    screenshot = pyautogui.screenshot(region=target_region)
    target_img_path = get_img_save_path()
    screenshot.save(target_img_path)

    if not os.path.exists(target_img_path):
        print('failed')
        return

    # 画像からテキストを抽出
    # 前提条件: Tesseractがインストールされていること
    # https://github.com/tesseract-ocr/tesseract
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    get_text_from_img = str(pytesseract.image_to_string(Image.open(target_img_path)))

    # DeepLで翻訳しやすいようにするため、改行をなくしテキストファイルに保存
    output_text = ''.join(get_text_from_img.splitlines())
    f = open('output.txt', 'w', encoding='UTF-8')
    f.write(output_text)
    f.close()

# カレントディレクトリのscreenshot_dirディレクトリのパスを取得
# screenshot_dirがなければ作成
def get_img_path():
    screenshot_dir = 'screenshot_dir'
    if not os.path.exists(screenshot_dir):
        os.mkdir(screenshot_dir)
    current_dir = os.getcwd()
    current_dir_joined_img_path = os.path.join(current_dir, screenshot_dir)
    return current_dir_joined_img_path

# カレントディレクトリのimgディレクトリ内に`現在時刻+uuid.png`のファイルパスを取得
def get_img_save_path():
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f_')
    generated_uuid_str = str(uuid.uuid4())
    img_extension = '.jpg'
    save_img_name = now + generated_uuid_str + img_extension
    return os.path.join(get_img_path(), save_img_name)

# ディスプレイの画面右側のサイズを取得
def get_target_region():
    window_page_size = pyautogui.size()
    width_half = int(window_page_size.width / 2)
    height = int(window_page_size.height)
    x = width_half
    # y = 0
    y = 200
    w = width_half
    # h = height
    h = height - 350
    target_range = (x, y, w, h)
    return target_range

if __name__ == '__main__':
    main()
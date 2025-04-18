import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

width, height = 11, 19  # 이미 구한 width

img = np.full((height * 4, width * (127-32), 3), 255, np.uint8)  # 흰색 캔버스 (높이(행), 너비(열))

font_name = "Consolas.ttf"
consolas = ImageFont.truetype("/scripts/"+font_name, 20)  # 폰트 로딩
img_pil = Image.fromarray(img)  # PIL에서 사용 가능한 형태로 바꾸기

draw = ImageDraw.Draw(img_pil)  # img_pil에 그릴 준비

# 아스키 다 가져오기 (특문 포함 32~126까지)
text_all_ASCII = [chr(i) + "\n" + chr(i) for i in range(32, 127, 1)]
# 영어만
text_only_alp = [chr(i) + "\n" + chr(i) for i in range(65, 91, 1)] + [
    chr(i) + "\n" + chr(i) for i in range(97, 123, 1)
]

for idx, char in enumerate(text_all_ASCII):
    draw.text((idx * width, 0), char, font=consolas, fill=(0, 0, 0))
    # bbox = draw.textbbox((0, 0), text=char, font=font) # 너비 계산을 위한 텍스트 박싱 함수 textbbox
    # print(char, bbox)

for idx, char in enumerate(text_only_alp):
    draw.text((idx * width, 2 * height), char, font=consolas, fill=(0, 0, 0))
    # bbox = draw.textbbox((0, 0), text=char, font=font) # 너비 계산을 위한 텍스트 박싱 함수 textbbox
    # print(char, bbox)

img = np.array(img_pil)
cv2.imshow("img", img)
cv2.imwrite("scripts/reference/img_"+font_name+".png", img)

# 콘솔라스 정보
"""
consolas 너비 11, 높이 19
높이 Q[2~19] / A[2~15] / i[0~15] / j[0~19] / b,d,f...[1~15] / q,p[5~19]
"""

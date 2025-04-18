import cv2

width, height = 11, 19  # 이미 구한 width

img = cv2.imread("scripts/reference/Consolas.ttf.png") # 미리 만든 레퍼런스 가져오기



cv2.waitKey(0)

# 이미지를 받으면 widht, height정보를 받아서 문자 별 밝기 등급은 최대 255로 저장하기
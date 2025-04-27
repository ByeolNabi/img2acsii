import cv2
import numpy as np  # numpy 추가

width, height = 11, 19  # 이미 구한 width
MAX_pixel = 11 * 19
numberOfAscii = 127 - 32  # 32~126


# =========== 함수구현 ============= #
# 레퍼런스 이미지를 넣으면 lut를 뽑아줘요
def img2lut(img):
    white_level_arr = img2array(img)
    lut = array2lut(white_level_arr)
    return lut


# 이미지를 array로 (255를 기준으로 재구성)
def img2array(img):
    # 이미지가 컬러이면 그레이스케일로 변환
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
    # 일단 32~126 문자들 다 순회하기

    white_arr = [0] * numberOfAscii
    for i in range(numberOfAscii):
        x = i * width
        y = 0
        char_roi = img_gray[y : y + height, x : x + width]
        while_pixel_cnt = int((np.sum(char_roi == 255) / MAX_pixel) * 255)
        white_arr[i] = while_pixel_cnt

    print([num for num in white_arr])
    return white_arr


# imag
def array2lut(char_arr):
    """
    Args:
        char_arr (list): 각 문자의 밝기 레벨(0~255)을 담은 리스트.
                         char_arr[i]는 ASCII (i+32) 문자의 밝기 레벨.

    Returns:
        list: 0~255의 각 그레이스케일 값에 가장 가까운 밝기 레벨을 가진
              문자의 인덱스(0~94)를 저장한 LUT. lut[g] = index.
    """
    lut = [0] * 256  # 0~255 그레이스케일 값에 대한 LUT 초기화
    char_arr_np = np.array(char_arr)  # 계산을 위해 numpy 배열로 변환

    # 0부터 255까지 각 그레이스케일 값(g)에 대해 반복
    for g in range(256):
        # 현재 그레이스케일 값(g)과 모든 문자의 밝기 레벨(char_arr_np) 간의 절대 차이 계산
        diffs = np.abs(char_arr_np - g)

        # 절대 차이가 가장 작은 값의 인덱스를 찾음
        # 이 인덱스는 char_arr에서의 인덱스이며, (ASCII 값 - 32)에 해당
        min_idx = np.argmin(diffs)

        # LUT의 g번째 위치에 가장 가까운 문자의 인덱스(min_idx) 저장
        lut[g] = min_idx + 32

    return lut


# ================ 실행 코드 ================= #
# 이미지를 받으면 widht, height정보를 받아서 문자 별 밝기 등급은 최대 255로 저장하기
img_path = "scripts/reference/img_Consolas.ttf.png"  # 경로 변수화
img = cv2.imread(img_path)  # 미리 만든 레퍼런스 가져오기

# 이미지 로드 확인
if img is None:
    print("Error: 이미지를 로드할 수 없습니다. 경로를 확인하세요.")
else:
    LUT_table = img2lut(img)

    # 이미지 로드 확인
if img is None:
    print(f"Error: 이미지를 로드할 수 없습니다. 경로를 확인하세요: {img_path}")
else:
    print(f"이미지 로드 성공: {img_path}, 크기: {img.shape}")
    LUT_table = img2lut(img)

    if LUT_table is not None:  # LUT가 성공적으로 생성되었는지 확인
        print("생성된 LUT (일부):", LUT_table[:10], "...")  # 전체 대신 일부만 출력

        # 생성된 LUT를 txt 파일로 저장
        output_filename = "scripts/reference/Consolas_LUT.txt"
        try:
            # NumPy 배열로 변환하여 저장 (각 숫자를 정수로 저장)
            np.savetxt(output_filename, np.array(LUT_table), fmt="%d")
            print(f"LUT가 '{output_filename}' 파일로 저장되었습니다.")
        except Exception as e:
            print(f"Error: LUT를 파일로 저장하는 중 오류 발생 - {e}")

    else:
        print("LUT 생성에 실패했습니다.")

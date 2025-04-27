import cv2
import numpy as np  # numpy 추가

width, height = 11, 19  # 이미 구한 width
MAX_pixel = 11 * 19
numberOfAscii = 127 - 32  # 32~126


# 선형 대비 늘리기를 적용하는 함수
def stretch_contrast(arr, min_out=0, max_out=255):
    """
    주어진 배열에 선형 대비 늘리기를 적용합니다.

    Args:
        arr (np.ndarray or list): 입력 배열 (예: white_arr).
        min_out (int): 출력 범위의 최소값.
        max_out (int): 출력 범위의 최대값.

    Returns:
        np.ndarray: 대비가 늘려진 새로운 NumPy 배열. 입력 배열이 비어있거나
                    최대/최소값이 같으면 원본 배열(NumPy로 변환됨)을 반환.
    """
    if isinstance(arr, list):
        arr = np.array(arr)  # NumPy 배열로 변환

    if arr.size == 0:
        print("Warning: 대비 늘리기 입력 배열이 비어 있습니다.")
        return arr  # 빈 배열 반환

    min_val = np.min(arr)
    max_val = np.max(arr)

    # 최대값과 최소값이 같으면 대비 늘리기 불가 (분모 0 방지)
    if min_val == max_val:
        print("Warning: 배열의 모든 값이 동일하여 대비 늘리기를 적용할 수 없습니다.")
        # 모든 값을 중간값(예: 128) 또는 최소/최대값으로 설정하거나 원본 반환
        # 여기서는 원본 배열을 그대로 반환
        return arr

    # 선형 변환 적용
    # v_out = ((v_in - min_in) / (max_in - min_in)) * (max_out - min_out) + min_out
    stretched_arr = ((arr - min_val) / (max_val - min_val)) * (
        max_out - min_out
    ) + min_out

    # 결과를 정수형으로 변환하고 0~255 범위로 클리핑
    stretched_arr = np.clip(np.round(stretched_arr), min_out, max_out).astype(int)

    print("대비 늘리기 전 min/max:", min_val, max_val)
    print("대비 늘리기 후 min/max:", np.min(stretched_arr), np.max(stretched_arr))

    print("[func stretch_contrast] 선형 대비 늘리기 후 배열 값 : ", stretched_arr[:])

    return stretched_arr


# =========== 함수구현 ============= #
# 레퍼런스 이미지를 넣으면 lut를 뽑아줘요
def img2lut(img, apply_contrast_stretch=True):  # 대비 늘리기 적용 여부 옵션 추가
    white_level_arr = img2array(img)
    if white_level_arr is not None:
        if apply_contrast_stretch:
            print("선형 대비 늘리기 적용 중...")
            white_level_arr = stretch_contrast(white_level_arr)  # 대비 늘리기 적용

        lut = array2lut(white_level_arr)  # 기존 방식

        print("[func img2lut] 리턴된 lut : ", lut[:])

        return lut
    else:
        return None


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
        while_pixel_cnt = int((np.sum(char_roi) / MAX_pixel))
        white_arr[i] = while_pixel_cnt

    print([num for num in white_arr])
    return np.array(white_arr)


# 기존 array2lut 함수 (가장 가까운 밝기 매핑)
def array2lut(char_arr):
    """기존 방식: 가장 가까운 밝기 매핑"""
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
        print("생성된 LUT (일부):", LUT_table[:], "...")  # 전체 대신 일부만 출력

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
